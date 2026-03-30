#!/usr/bin/env bash
# ============================================================
# CLIENT ONBOARDING SCRIPT — 510kBridge Control Tower
#
# Provisions a new client project in Supabase:
#   1. Calls the onboard_client() RPC to create subscription + gates
#   2. Outputs the project URL and connection details
#
# Prerequisites:
#   - SUPABASE_SERVICE_KEY env var (service_role key, NOT anon key)
#   - curl installed
#
# Usage:
#   ./onboard_client.sh <project_id> <tier> <max_seats>
#
# Examples:
#   ./onboard_client.sh silan-2026 growth 5
#   ./onboard_client.sh hangzhou-ortho-2026 scale 10
#   ./onboard_client.sh demo-test starter 2
# ============================================================

set -euo pipefail

SUPABASE_URL="https://fllqdhvvnqoayugohzld.supabase.co"
DASHBOARD_URL="https://control-tower-bmx.pages.dev"

# ── Validate inputs ──────────────────────────────────────────

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <project_id> [tier] [max_seats]"
  echo ""
  echo "  project_id   Unique project identifier (e.g., silan-2026)"
  echo "  tier         starter | growth | scale  (default: starter)"
  echo "  max_seats    Number of team seats       (default: 2)"
  echo ""
  echo "Tiers:"
  echo "  starter   \$500/mo   2 seats   4 tabs"
  echo "  growth    \$1000/mo  5 seats   13 tabs"
  echo "  scale     \$2000/mo  10 seats  16 tabs"
  exit 1
fi

PROJECT_ID="$1"
TIER="${2:-starter}"
MAX_SEATS="${3:-2}"

# Validate tier
if [[ "$TIER" != "starter" && "$TIER" != "growth" && "$TIER" != "scale" ]]; then
  echo "ERROR: Invalid tier '$TIER'. Must be starter, growth, or scale."
  exit 1
fi

# Validate max_seats is a number
if ! [[ "$MAX_SEATS" =~ ^[0-9]+$ ]]; then
  echo "ERROR: max_seats must be a positive integer."
  exit 1
fi

# Check for service key
if [[ -z "${SUPABASE_SERVICE_KEY:-}" ]]; then
  echo "ERROR: SUPABASE_SERVICE_KEY environment variable is not set."
  echo ""
  echo "Set it with:"
  echo "  export SUPABASE_SERVICE_KEY='your-service-role-key'"
  echo ""
  echo "Find it in Supabase Dashboard → Settings → API → service_role key"
  exit 1
fi

# ── Call onboard_client RPC ──────────────────────────────────

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  510kBridge — Client Onboarding"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "  Project ID:  $PROJECT_ID"
echo "  Tier:        $TIER"
echo "  Max Seats:   $MAX_SEATS"
echo ""

RESPONSE=$(curl -s -w "\n%{http_code}" \
  "${SUPABASE_URL}/rest/v1/rpc/onboard_client" \
  -H "apikey: ${SUPABASE_SERVICE_KEY}" \
  -H "Authorization: Bearer ${SUPABASE_SERVICE_KEY}" \
  -H "Content-Type: application/json" \
  -d "{\"p_project_id\": \"${PROJECT_ID}\", \"p_tier\": \"${TIER}\", \"p_max_seats\": ${MAX_SEATS}}")

HTTP_CODE=$(echo "$RESPONSE" | tail -1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [[ "$HTTP_CODE" -ge 200 && "$HTTP_CODE" -lt 300 ]]; then
  echo "  ✅  Client provisioned successfully!"
  echo ""
  echo "  Response:"
  echo "  $BODY"
  echo ""
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "  NEXT STEPS"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo ""
  echo "  1. Share dashboard URL with client:"
  echo "     ${DASHBOARD_URL}/?project=${PROJECT_ID}"
  echo ""
  echo "  2. Client opens URL → Setup Wizard runs → selects"
  echo "     device template → enters team, budget, suppliers"
  echo ""
  echo "  3. All data is stored under project_id='${PROJECT_ID}'"
  echo "     with RLS isolation (no cross-project visibility)"
  echo ""
  echo "  4. Assign account manager and schedule kickoff call"
  echo ""
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
else
  echo "  ❌  Onboarding failed (HTTP $HTTP_CODE)"
  echo ""
  echo "  Error: $BODY"
  echo ""
  echo "  Common issues:"
  echo "  - Invalid service key (check SUPABASE_SERVICE_KEY)"
  echo "  - onboard_client() function not deployed (run supabase-schema.sql)"
  echo "  - Invalid tier value"
  exit 1
fi
