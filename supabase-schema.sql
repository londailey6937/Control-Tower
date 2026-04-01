-- ============================================================
-- SUPABASE SCHEMA: Message Board for Control Tower
-- Run this in Supabase SQL Editor (Dashboard → SQL Editor → New query)
-- ============================================================

-- 1. Messages table
CREATE TABLE IF NOT EXISTS messages (
  id         UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  project_id TEXT NOT NULL DEFAULT 'demo',
  q_num      INTEGER NOT NULL,
  sender     TEXT NOT NULL CHECK (sender IN ('pmp', 'technology', 'business', 'accounting', 'inventor')),
  text       TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT now() NOT NULL,
  read_by    TEXT[] DEFAULT '{}'::TEXT[] NOT NULL
);

-- Index for quick per-question queries
CREATE INDEX IF NOT EXISTS idx_messages_q_num ON messages (q_num, created_at);
CREATE INDEX IF NOT EXISTS idx_messages_project ON messages (project_id);

-- 2. Enable Row-Level Security
ALTER TABLE messages ENABLE ROW LEVEL SECURITY;

-- Allow anyone with the anon key to read messages (if tier allows)
CREATE POLICY "Tier-gated message read"
  ON messages FOR SELECT
  USING (project_tier(project_id) IN ('growth', 'scale'));

-- Allow inserts if tier allows
CREATE POLICY "Tier-gated message insert"
  ON messages FOR INSERT
  WITH CHECK (project_tier(project_id) IN ('growth', 'scale'));

-- Allow updates if tier allows (for read receipts)
CREATE POLICY "Tier-gated message update"
  ON messages FOR UPDATE
  USING (project_tier(project_id) IN ('growth', 'scale'));

-- Allow deletes if tier allows (for archiving)
CREATE POLICY "Tier-gated message delete"
  ON messages FOR DELETE
  USING (project_tier(project_id) IN ('growth', 'scale'));

-- Service role bypass (admin API / webhooks)
CREATE POLICY "Service role full access messages"
  ON messages FOR ALL
  USING (auth.role() = 'service_role')
  WITH CHECK (auth.role() = 'service_role');

-- 3. Function: atomically mark a message as read by a role
CREATE OR REPLACE FUNCTION mark_read(msg_id UUID, reader TEXT)
RETURNS VOID AS $$
BEGIN
  UPDATE messages
  SET read_by = array_append(read_by, reader)
  WHERE id = msg_id
    AND NOT (read_by @> ARRAY[reader]);
END;
$$ LANGUAGE plpgsql;

-- 4. Enable Realtime for the messages table
ALTER PUBLICATION supabase_realtime ADD TABLE messages;

-- ============================================================
-- MIGRATION: Expand sender CHECK constraint for multi-role
-- Run this if the table already exists with the old 2-role constraint
-- ============================================================
-- ALTER TABLE messages DROP CONSTRAINT IF EXISTS messages_sender_check;
-- ALTER TABLE messages ADD CONSTRAINT messages_sender_check
--   CHECK (sender IN ('pmp', 'technology', 'business', 'accounting', 'inventor'));

-- ============================================================
-- SUBSCRIPTIONS TABLE — SaaS tier enforcement
-- Stores the active subscription tier per project
-- ============================================================

CREATE TABLE IF NOT EXISTS subscriptions (
  id                UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  project_id        TEXT NOT NULL UNIQUE,
  tier              TEXT NOT NULL DEFAULT 'starter'
                      CHECK (tier IN ('starter', 'growth', 'scale')),
  max_seats         INTEGER NOT NULL DEFAULT 2,
  stripe_customer_id TEXT,
  created_at        TIMESTAMPTZ DEFAULT now() NOT NULL,
  updated_at        TIMESTAMPTZ DEFAULT now() NOT NULL
);

-- Index for fast project lookup
CREATE INDEX IF NOT EXISTS idx_subscriptions_project
  ON subscriptions (project_id);

-- Enable RLS
ALTER TABLE subscriptions ENABLE ROW LEVEL SECURITY;

-- Anyone with anon key can read their project's subscription
CREATE POLICY "Anon can read subscriptions"
  ON subscriptions FOR SELECT
  USING (true);

-- Only service_role can modify subscriptions (via webhook or admin API)
CREATE POLICY "Service role insert subscriptions"
  ON subscriptions FOR INSERT
  WITH CHECK (auth.role() = 'service_role');

CREATE POLICY "Service role update subscriptions"
  ON subscriptions FOR UPDATE
  USING (auth.role() = 'service_role');

CREATE POLICY "Service role delete subscriptions"
  ON subscriptions FOR DELETE
  USING (auth.role() = 'service_role');

-- Auto-update updated_at on changes
CREATE OR REPLACE FUNCTION update_subscriptions_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER subscriptions_updated_at
  BEFORE UPDATE ON subscriptions
  FOR EACH ROW
  EXECUTE FUNCTION update_subscriptions_updated_at();

-- Helper: look up tier for a given project (used in RLS policies)
CREATE OR REPLACE FUNCTION project_tier(p_project_id TEXT)
RETURNS TEXT AS $$
  SELECT COALESCE(
    (SELECT tier FROM subscriptions WHERE project_id = p_project_id),
    'starter'
  );
$$ LANGUAGE sql STABLE;

-- Server-authoritative allowed tabs RPC (SECURITY DEFINER)
-- Client calls this RPC to get the tab list; result cannot be spoofed.
CREATE OR REPLACE FUNCTION get_allowed_tabs(p_project_id TEXT)
RETURNS TEXT[] AS $$
DECLARE
  v_tier TEXT;
BEGIN
  SELECT tier INTO v_tier FROM subscriptions WHERE project_id = p_project_id;
  v_tier := COALESCE(v_tier, 'starter');

  CASE v_tier
    WHEN 'starter' THEN
      RETURN ARRAY['dual-track', 'gates', 'timeline', 'budget', 'predicate-finder'];
    WHEN 'growth' THEN
      RETURN ARRAY[
        'dual-track', 'gates', 'timeline', 'budget',
        'regulatory', 'risks', 'audit', 'doc-library',
        'cash-runway', 'cap-table', 'us-investment',
        'actions', 'qa-sheet', 'predicate-finder'
      ];
    WHEN 'scale' THEN
      RETURN ARRAY[
        'dual-track', 'gates', 'timeline', 'budget',
        'regulatory', 'risks', 'audit', 'doc-library',
        'cash-runway', 'cap-table', 'us-investment',
        'actions', 'qa-sheet', 'resources', 'suppliers',
        'fda-comms', 'predicate-finder'
      ];
    ELSE
      RETURN ARRAY['dual-track', 'gates', 'timeline', 'budget', 'predicate-finder'];
  END CASE;
END;
$$ LANGUAGE plpgsql STABLE SECURITY DEFINER;

-- Seed a default subscription for demo projects
-- INSERT INTO subscriptions (project_id, tier, max_seats)
-- VALUES ('demo', 'scale', 10)
-- ON CONFLICT (project_id) DO NOTHING;


-- ============================================================
-- AUDIT TRAIL TABLE — Immutable change log (21 CFR Part 11)
-- Every gate decision, document status change, risk update, etc.
-- ============================================================

CREATE TABLE IF NOT EXISTS audit_trail (
  id          UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  project_id  TEXT NOT NULL,
  timestamp   TIMESTAMPTZ DEFAULT now() NOT NULL,
  user_role   TEXT NOT NULL,
  user_name   TEXT NOT NULL DEFAULT '',
  action      TEXT NOT NULL,
  target_id   TEXT NOT NULL DEFAULT '',
  field       TEXT NOT NULL DEFAULT '',
  old_value   TEXT NOT NULL DEFAULT '',
  new_value   TEXT NOT NULL DEFAULT '',
  detail      TEXT NOT NULL DEFAULT ''
);

CREATE INDEX IF NOT EXISTS idx_audit_project ON audit_trail (project_id, timestamp);

ALTER TABLE audit_trail ENABLE ROW LEVEL SECURITY;

-- Read: any authenticated/anon key holder for their project
CREATE POLICY "Tier-gated audit read"
  ON audit_trail FOR SELECT
  USING (project_tier(project_id) IN ('growth', 'scale'));

-- Insert-only: audit entries are immutable (no UPDATE or DELETE for anon)
CREATE POLICY "Tier-gated audit insert"
  ON audit_trail FOR INSERT
  WITH CHECK (project_tier(project_id) IN ('growth', 'scale'));

-- Service role full access
CREATE POLICY "Service role full access audit"
  ON audit_trail FOR ALL
  USING (auth.role() = 'service_role')
  WITH CHECK (auth.role() = 'service_role');


-- ============================================================
-- GATE DECISIONS TABLE — PMP sign-off checkpoints
-- ============================================================

CREATE TABLE IF NOT EXISTS gate_decisions (
  id            UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  project_id    TEXT NOT NULL,
  gate_number   INTEGER NOT NULL CHECK (gate_number BETWEEN 1 AND 6),
  status        TEXT NOT NULL DEFAULT 'not-started'
                  CHECK (status IN ('not-started', 'pending-review', 'approved', 'blocked', 'needs-data')),
  decision      TEXT CHECK (decision IN ('proceed', 'more-data', 'stop')),
  decided_by    TEXT,
  decided_at    TIMESTAMPTZ,
  notes         JSONB NOT NULL DEFAULT '[]'::JSONB,
  criteria      JSONB NOT NULL DEFAULT '[]'::JSONB,
  updated_at    TIMESTAMPTZ DEFAULT now() NOT NULL,
  UNIQUE (project_id, gate_number)
);

CREATE INDEX IF NOT EXISTS idx_gates_project ON gate_decisions (project_id);

ALTER TABLE gate_decisions ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Anon read gates"
  ON gate_decisions FOR SELECT USING (true);

CREATE POLICY "Tier-gated gate insert"
  ON gate_decisions FOR INSERT
  WITH CHECK (project_tier(project_id) IN ('starter', 'growth', 'scale'));

CREATE POLICY "Tier-gated gate update"
  ON gate_decisions FOR UPDATE
  USING (project_tier(project_id) IN ('starter', 'growth', 'scale'));

CREATE POLICY "Service role full access gates"
  ON gate_decisions FOR ALL
  USING (auth.role() = 'service_role')
  WITH CHECK (auth.role() = 'service_role');


-- ============================================================
-- DHF DOCUMENTS TABLE — Design History File lifecycle
-- ============================================================

CREATE TABLE IF NOT EXISTS dhf_documents (
  id              UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  project_id      TEXT NOT NULL,
  doc_name        TEXT NOT NULL,
  doc_type        TEXT NOT NULL DEFAULT 'general',
  version         TEXT NOT NULL DEFAULT '1.0',
  status          TEXT NOT NULL DEFAULT 'draft'
                    CHECK (status IN ('draft', 'in-review', 'approved', 'effective', 'obsolete')),
  owner           TEXT NOT NULL DEFAULT '',
  effective_date  DATE,
  next_review     DATE,
  linked_milestone TEXT,
  data_source_ref TEXT NOT NULL DEFAULT '',
  revisions       JSONB NOT NULL DEFAULT '[]'::JSONB,
  created_at      TIMESTAMPTZ DEFAULT now() NOT NULL,
  updated_at      TIMESTAMPTZ DEFAULT now() NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_dhf_project ON dhf_documents (project_id);

ALTER TABLE dhf_documents ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Anon read dhf"
  ON dhf_documents FOR SELECT USING (true);

CREATE POLICY "Tier-gated dhf insert"
  ON dhf_documents FOR INSERT
  WITH CHECK (project_tier(project_id) IN ('starter', 'growth', 'scale'));

CREATE POLICY "Tier-gated dhf update"
  ON dhf_documents FOR UPDATE
  USING (project_tier(project_id) IN ('starter', 'growth', 'scale'));

CREATE POLICY "Service role full access dhf"
  ON dhf_documents FOR ALL
  USING (auth.role() = 'service_role')
  WITH CHECK (auth.role() = 'service_role');

CREATE TRIGGER dhf_updated_at
  BEFORE UPDATE ON dhf_documents
  FOR EACH ROW
  EXECUTE FUNCTION update_subscriptions_updated_at();


-- ============================================================
-- RISKS TABLE — ISO 14971 risk register
-- ============================================================

CREATE TABLE IF NOT EXISTS risks (
  id                UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  project_id        TEXT NOT NULL,
  title             TEXT NOT NULL,
  severity          TEXT NOT NULL CHECK (severity IN ('high', 'medium', 'low')),
  probability       TEXT NOT NULL CHECK (probability IN ('very-low', 'low', 'medium', 'high')),
  risk_level        TEXT NOT NULL CHECK (risk_level IN ('red', 'yellow', 'green')),
  controls          TEXT NOT NULL DEFAULT '',
  residual          TEXT NOT NULL DEFAULT '',
  mitigation_status TEXT NOT NULL DEFAULT 'not-started'
                      CHECK (mitigation_status IN ('complete', 'in-progress', 'not-started')),
  module            TEXT NOT NULL DEFAULT '',
  standard          TEXT NOT NULL DEFAULT '',
  created_at        TIMESTAMPTZ DEFAULT now() NOT NULL,
  updated_at        TIMESTAMPTZ DEFAULT now() NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_risks_project ON risks (project_id);

ALTER TABLE risks ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Anon read risks"
  ON risks FOR SELECT USING (true);

CREATE POLICY "Tier-gated risk write"
  ON risks FOR INSERT
  WITH CHECK (project_tier(project_id) IN ('growth', 'scale'));

CREATE POLICY "Tier-gated risk update"
  ON risks FOR UPDATE
  USING (project_tier(project_id) IN ('growth', 'scale'));

CREATE POLICY "Service role full access risks"
  ON risks FOR ALL
  USING (auth.role() = 'service_role')
  WITH CHECK (auth.role() = 'service_role');

CREATE TRIGGER risks_updated_at
  BEFORE UPDATE ON risks
  FOR EACH ROW
  EXECUTE FUNCTION update_subscriptions_updated_at();


-- ============================================================
-- CAPA LOG TABLE — Corrective / Preventive Actions
-- ============================================================

CREATE TABLE IF NOT EXISTS capa_log (
  id            UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  project_id    TEXT NOT NULL,
  capa_type     TEXT NOT NULL CHECK (capa_type IN ('corrective', 'preventive')),
  title         TEXT NOT NULL,
  description   TEXT NOT NULL DEFAULT '',
  root_cause    TEXT NOT NULL DEFAULT '',
  action_taken  TEXT NOT NULL DEFAULT '',
  status        TEXT NOT NULL DEFAULT 'open'
                  CHECK (status IN ('open', 'in-progress', 'closed', 'verified')),
  owner         TEXT NOT NULL DEFAULT '',
  opened_date   DATE DEFAULT CURRENT_DATE,
  target_date   DATE,
  closed_date   DATE,
  linked_risk   UUID REFERENCES risks(id),
  created_at    TIMESTAMPTZ DEFAULT now() NOT NULL,
  updated_at    TIMESTAMPTZ DEFAULT now() NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_capa_project ON capa_log (project_id);

ALTER TABLE capa_log ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Anon read capa"
  ON capa_log FOR SELECT USING (true);

CREATE POLICY "Tier-gated capa write"
  ON capa_log FOR INSERT
  WITH CHECK (project_tier(project_id) IN ('growth', 'scale'));

CREATE POLICY "Tier-gated capa update"
  ON capa_log FOR UPDATE
  USING (project_tier(project_id) IN ('growth', 'scale'));

CREATE POLICY "Service role full access capa"
  ON capa_log FOR ALL
  USING (auth.role() = 'service_role')
  WITH CHECK (auth.role() = 'service_role');

CREATE TRIGGER capa_updated_at
  BEFORE UPDATE ON capa_log
  FOR EACH ROW
  EXECUTE FUNCTION update_subscriptions_updated_at();


-- ============================================================
-- BUDGET TABLE — Planned vs. Actual per category
-- ============================================================

CREATE TABLE IF NOT EXISTS budget_items (
  id          UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  project_id  TEXT NOT NULL,
  label       TEXT NOT NULL,
  planned     NUMERIC(12,2) NOT NULL DEFAULT 0,
  actual      NUMERIC(12,2) NOT NULL DEFAULT 0,
  currency    TEXT NOT NULL DEFAULT 'USD',
  notes       TEXT NOT NULL DEFAULT '',
  created_at  TIMESTAMPTZ DEFAULT now() NOT NULL,
  updated_at  TIMESTAMPTZ DEFAULT now() NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_budget_project ON budget_items (project_id);

ALTER TABLE budget_items ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Anon read budget"
  ON budget_items FOR SELECT USING (true);

CREATE POLICY "Tier-gated budget write"
  ON budget_items FOR INSERT
  WITH CHECK (project_tier(project_id) IN ('starter', 'growth', 'scale'));

CREATE POLICY "Tier-gated budget update"
  ON budget_items FOR UPDATE
  USING (project_tier(project_id) IN ('starter', 'growth', 'scale'));

CREATE POLICY "Service role full access budget"
  ON budget_items FOR ALL
  USING (auth.role() = 'service_role')
  WITH CHECK (auth.role() = 'service_role');

CREATE TRIGGER budget_updated_at
  BEFORE UPDATE ON budget_items
  FOR EACH ROW
  EXECUTE FUNCTION update_subscriptions_updated_at();


-- ============================================================
-- ACTION ITEMS TABLE — Task board
-- ============================================================

CREATE TABLE IF NOT EXISTS action_items (
  id              UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  project_id      TEXT NOT NULL,
  title           TEXT NOT NULL,
  description     TEXT NOT NULL DEFAULT '',
  status          TEXT NOT NULL DEFAULT 'todo'
                    CHECK (status IN ('todo', 'in-progress', 'done', 'blocked')),
  priority        TEXT NOT NULL DEFAULT 'normal'
                    CHECK (priority IN ('low', 'normal', 'high', 'urgent')),
  owner           TEXT NOT NULL DEFAULT '',
  due_date        DATE,
  linked_milestone TEXT,
  created_at      TIMESTAMPTZ DEFAULT now() NOT NULL,
  updated_at      TIMESTAMPTZ DEFAULT now() NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_actions_project ON action_items (project_id);

ALTER TABLE action_items ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Anon read actions"
  ON action_items FOR SELECT USING (true);

CREATE POLICY "Tier-gated action write"
  ON action_items FOR INSERT
  WITH CHECK (project_tier(project_id) IN ('starter', 'growth', 'scale'));

CREATE POLICY "Tier-gated action update"
  ON action_items FOR UPDATE
  USING (project_tier(project_id) IN ('starter', 'growth', 'scale'));

CREATE POLICY "Tier-gated action delete"
  ON action_items FOR DELETE
  USING (project_tier(project_id) IN ('starter', 'growth', 'scale'));

CREATE POLICY "Service role full access actions"
  ON action_items FOR ALL
  USING (auth.role() = 'service_role')
  WITH CHECK (auth.role() = 'service_role');

CREATE TRIGGER actions_updated_at
  BEFORE UPDATE ON action_items
  FOR EACH ROW
  EXECUTE FUNCTION update_subscriptions_updated_at();


-- ============================================================
-- MILESTONES TABLE — Technical & Regulatory track items
-- ============================================================

CREATE TABLE IF NOT EXISTS milestones (
  id          UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  project_id  TEXT NOT NULL,
  track       TEXT NOT NULL CHECK (track IN ('technical', 'regulatory')),
  month       INTEGER NOT NULL,
  title       TEXT NOT NULL,
  description TEXT NOT NULL DEFAULT '',
  status      TEXT NOT NULL DEFAULT 'not-started'
                CHECK (status IN ('complete', 'in-progress', 'not-started')),
  owner       TEXT NOT NULL DEFAULT 'tech'
                CHECK (owner IN ('tech', 'regulatory', 'business')),
  category    TEXT NOT NULL DEFAULT '',
  created_at  TIMESTAMPTZ DEFAULT now() NOT NULL,
  updated_at  TIMESTAMPTZ DEFAULT now() NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_milestones_project ON milestones (project_id, track);

ALTER TABLE milestones ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Anon read milestones"
  ON milestones FOR SELECT USING (true);

CREATE POLICY "Tier-gated milestone write"
  ON milestones FOR INSERT
  WITH CHECK (project_tier(project_id) IN ('starter', 'growth', 'scale'));

CREATE POLICY "Tier-gated milestone update"
  ON milestones FOR UPDATE
  USING (project_tier(project_id) IN ('starter', 'growth', 'scale'));

CREATE POLICY "Service role full access milestones"
  ON milestones FOR ALL
  USING (auth.role() = 'service_role')
  WITH CHECK (auth.role() = 'service_role');

CREATE TRIGGER milestones_updated_at
  BEFORE UPDATE ON milestones
  FOR EACH ROW
  EXECUTE FUNCTION update_subscriptions_updated_at();


-- ============================================================
-- SUPPLIERS TABLE — Vendor management
-- ============================================================

CREATE TABLE IF NOT EXISTS suppliers (
  id              UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  project_id      TEXT NOT NULL,
  name            TEXT NOT NULL,
  component       TEXT NOT NULL DEFAULT '',
  lead_time_days  INTEGER NOT NULL DEFAULT 0,
  status          TEXT NOT NULL DEFAULT 'active'
                    CHECK (status IN ('active', 'qualified', 'pending', 'inactive')),
  contact_name    TEXT NOT NULL DEFAULT '',
  contact_email   TEXT NOT NULL DEFAULT '',
  notes           TEXT NOT NULL DEFAULT '',
  created_at      TIMESTAMPTZ DEFAULT now() NOT NULL,
  updated_at      TIMESTAMPTZ DEFAULT now() NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_suppliers_project ON suppliers (project_id);

ALTER TABLE suppliers ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Tier-gated supplier read"
  ON suppliers FOR SELECT
  USING (project_tier(project_id) IN ('growth', 'scale'));

CREATE POLICY "Tier-gated supplier write"
  ON suppliers FOR INSERT
  WITH CHECK (project_tier(project_id) IN ('growth', 'scale'));

CREATE POLICY "Tier-gated supplier update"
  ON suppliers FOR UPDATE
  USING (project_tier(project_id) IN ('growth', 'scale'));

CREATE POLICY "Service role full access suppliers"
  ON suppliers FOR ALL
  USING (auth.role() = 'service_role')
  WITH CHECK (auth.role() = 'service_role');

CREATE TRIGGER suppliers_updated_at
  BEFORE UPDATE ON suppliers
  FOR EACH ROW
  EXECUTE FUNCTION update_subscriptions_updated_at();


-- ============================================================
-- TEAM MEMBERS TABLE — Resource allocation
-- ============================================================

CREATE TABLE IF NOT EXISTS team_members (
  id          UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  project_id  TEXT NOT NULL,
  name        TEXT NOT NULL,
  role        TEXT NOT NULL DEFAULT '',
  email       TEXT NOT NULL DEFAULT '',
  workstreams JSONB NOT NULL DEFAULT '[]'::JSONB,
  created_at  TIMESTAMPTZ DEFAULT now() NOT NULL,
  updated_at  TIMESTAMPTZ DEFAULT now() NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_team_project ON team_members (project_id);

ALTER TABLE team_members ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Tier-gated team read"
  ON team_members FOR SELECT
  USING (project_tier(project_id) IN ('growth', 'scale'));

CREATE POLICY "Tier-gated team write"
  ON team_members FOR INSERT
  WITH CHECK (project_tier(project_id) IN ('growth', 'scale'));

CREATE POLICY "Tier-gated team update"
  ON team_members FOR UPDATE
  USING (project_tier(project_id) IN ('growth', 'scale'));

CREATE POLICY "Tier-gated team delete"
  ON team_members FOR DELETE
  USING (project_tier(project_id) IN ('growth', 'scale'));

CREATE POLICY "Service role full access team"
  ON team_members FOR ALL
  USING (auth.role() = 'service_role')
  WITH CHECK (auth.role() = 'service_role');

CREATE TRIGGER team_updated_at
  BEFORE UPDATE ON team_members
  FOR EACH ROW
  EXECUTE FUNCTION update_subscriptions_updated_at();


-- ============================================================
-- CLIENT ONBOARDING RPC
-- Provisions a new project: subscription + seed data in one call
-- Usage: SELECT onboard_client('silan-2026', 'growth', 5);
-- ============================================================

CREATE OR REPLACE FUNCTION onboard_client(
  p_project_id   TEXT,
  p_tier         TEXT DEFAULT 'starter',
  p_max_seats    INTEGER DEFAULT 2
)
RETURNS JSONB AS $$
DECLARE
  v_sub_id UUID;
BEGIN
  -- 1. Create subscription
  INSERT INTO subscriptions (project_id, tier, max_seats)
  VALUES (p_project_id, p_tier, p_max_seats)
  ON CONFLICT (project_id)
    DO UPDATE SET tier = EXCLUDED.tier, max_seats = EXCLUDED.max_seats
  RETURNING id INTO v_sub_id;

  -- 2. Seed 6 gate decision placeholders
  FOR i IN 1..6 LOOP
    INSERT INTO gate_decisions (project_id, gate_number, status)
    VALUES (p_project_id, i, 'not-started')
    ON CONFLICT (project_id, gate_number) DO NOTHING;
  END LOOP;

  -- 3. Log onboarding event
  INSERT INTO audit_trail (project_id, user_role, user_name, action, detail)
  VALUES (
    p_project_id, 'system', 'onboard_client',
    'project_created',
    format('Tier: %s, Seats: %s', p_tier, p_max_seats)
  );

  RETURN jsonb_build_object(
    'project_id', p_project_id,
    'subscription_id', v_sub_id,
    'tier', p_tier,
    'max_seats', p_max_seats,
    'gates_seeded', 6,
    'status', 'ok'
  );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
