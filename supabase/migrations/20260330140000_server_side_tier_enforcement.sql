-- ============================================================
-- MIGRATION: Server-Side Tier Enforcement & Security Hardening
-- Ensures Supabase returns nothing for tabs the subscription
-- doesn't cover — client-side TIER_TABS becomes UX-only.
-- ============================================================

-- 1. Add project_id to messages for multi-tenant tier gating
ALTER TABLE messages ADD COLUMN IF NOT EXISTS project_id TEXT NOT NULL DEFAULT 'demo';
CREATE INDEX IF NOT EXISTS idx_messages_project ON messages (project_id);

-- 2. Server-side allowed-tabs RPC (SECURITY DEFINER — runs as table owner)
--    This is the authoritative source for which tabs a project can access.
--    Client calls this RPC; result cannot be spoofed.
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

-- 3. Replace permissive message RLS with tier-gated policies
--    Messages (Q&A board) require growth+ tier to access.
DROP POLICY IF EXISTS "Anyone can read messages" ON messages;
DROP POLICY IF EXISTS "Anyone can insert messages" ON messages;
DROP POLICY IF EXISTS "Anyone can update messages" ON messages;
DROP POLICY IF EXISTS "Anyone can delete messages" ON messages;

CREATE POLICY "Tier-gated message read" ON messages
  FOR SELECT USING (
    project_tier(project_id) IN ('growth', 'scale')
  );

CREATE POLICY "Tier-gated message insert" ON messages
  FOR INSERT WITH CHECK (
    project_tier(project_id) IN ('growth', 'scale')
  );

CREATE POLICY "Tier-gated message update" ON messages
  FOR UPDATE USING (
    project_tier(project_id) IN ('growth', 'scale')
  );

CREATE POLICY "Tier-gated message delete" ON messages
  FOR DELETE USING (
    project_tier(project_id) IN ('growth', 'scale')
  );

-- Service role bypass (admin API / webhooks) — always has full access
CREATE POLICY "Service role full access messages" ON messages
  FOR ALL
  USING (auth.role() = 'service_role')
  WITH CHECK (auth.role() = 'service_role');

-- 4. Tighten subscriptions write policy
--    Drop the old broad "Service role can manage subscriptions" FOR ALL
--    and replace with explicit INSERT/UPDATE/DELETE policies to be safe.
DROP POLICY IF EXISTS "Service role can manage subscriptions" ON subscriptions;

CREATE POLICY "Service role insert subscriptions" ON subscriptions
  FOR INSERT WITH CHECK (auth.role() = 'service_role');

CREATE POLICY "Service role update subscriptions" ON subscriptions
  FOR UPDATE USING (auth.role() = 'service_role');

CREATE POLICY "Service role delete subscriptions" ON subscriptions
  FOR DELETE USING (auth.role() = 'service_role');
