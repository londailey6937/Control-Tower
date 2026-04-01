-- ============================================================
-- MIGRATION: Add predicate-finder tab to all subscription tiers
-- ============================================================

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
