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
      RETURN ARRAY['dual-track', 'gates', 'timeline', 'budget'];
    WHEN 'growth' THEN
      RETURN ARRAY[
        'dual-track', 'gates', 'timeline', 'budget',
        'regulatory', 'risks', 'audit', 'doc-library',
        'cash-runway', 'cap-table', 'us-investment',
        'actions', 'qa-sheet'
      ];
    WHEN 'scale' THEN
      RETURN ARRAY[
        'dual-track', 'gates', 'timeline', 'budget',
        'regulatory', 'risks', 'audit', 'doc-library',
        'cash-runway', 'cap-table', 'us-investment',
        'actions', 'qa-sheet', 'resources', 'suppliers',
        'fda-comms'
      ];
    ELSE
      RETURN ARRAY['dual-track', 'gates', 'timeline', 'budget'];
  END CASE;
END;
$$ LANGUAGE plpgsql STABLE SECURITY DEFINER;

-- Seed a default subscription for demo projects
-- INSERT INTO subscriptions (project_id, tier, max_seats)
-- VALUES ('demo', 'scale', 10)
-- ON CONFLICT (project_id) DO NOTHING;
