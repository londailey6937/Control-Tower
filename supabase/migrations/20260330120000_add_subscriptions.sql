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

CREATE INDEX IF NOT EXISTS idx_subscriptions_project ON subscriptions (project_id);

ALTER TABLE subscriptions ENABLE ROW LEVEL SECURITY;

DO $do$ BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM pg_policies WHERE tablename = 'subscriptions' AND policyname = 'Anyone can read subscriptions'
  ) THEN
    CREATE POLICY "Anyone can read subscriptions" ON subscriptions FOR SELECT USING (true);
  END IF;
END $do$;

DO $do$ BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM pg_policies WHERE tablename = 'subscriptions' AND policyname = 'Service role can manage subscriptions'
  ) THEN
    CREATE POLICY "Service role can manage subscriptions" ON subscriptions FOR ALL USING (auth.role() = 'service_role');
  END IF;
END $do$;

CREATE OR REPLACE FUNCTION update_subscriptions_updated_at()
RETURNS TRIGGER AS $fn$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$fn$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS subscriptions_updated_at ON subscriptions;
CREATE TRIGGER subscriptions_updated_at
  BEFORE UPDATE ON subscriptions
  FOR EACH ROW
  EXECUTE FUNCTION update_subscriptions_updated_at();

CREATE OR REPLACE FUNCTION project_tier(p_project_id TEXT)
RETURNS TEXT AS $fn$
  SELECT COALESCE(
    (SELECT tier FROM subscriptions WHERE project_id = p_project_id),
    'starter'
  );
$fn$ LANGUAGE sql STABLE;

INSERT INTO subscriptions (project_id, tier, max_seats)
VALUES ('demo', 'scale', 10)
ON CONFLICT (project_id) DO NOTHING;
