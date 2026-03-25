# Arch Medical Management — Business Strategy (March 2026)

## Corporate Structure

- **Operating Entity**: Pilot Software LLC (Oregon LLC, active)
- **Trade Name / DBA**: Arch Medical Management (to be filed under Pilot Software LLC — $50 Oregon Assumed Business Name)
- **Arch Medical Management LLC**: Oregon LLC (currently dissolved — not needed if DBA route used)
- **Client-Facing Brand**: Arch Medical Management
- **Contracts & Invoices**: "Pilot Software LLC dba Arch Medical Management"
- **Target Market**: Chinese entrepreneurs seeking FDA pathway for medical devices
- **Core Asset**: Control Tower PM Dashboard (Vite+TS, Supabase, CloudFlare Pages)
- **Demo URL**: control-tower-bmx.pages.dev

## DBA Filing Checklist

- [ ] File Assumed Business Name "Arch Medical Management" at Oregon Secretary of State ($50)
- [ ] Update Pilot Software LLC registered agent if needed
- [ ] Open business bank account (or add DBA to existing Pilot Software account)
- [ ] Verify Pilot Software LLC annual report is current

## Lead Magnets

1. **Stanford PMP Course** — free giveaway to attract clients
2. **FDA 510(k) Pathway Guide for Chinese Medical Device Companies** — polished PDF from existing `generate_fda_510k_guide.py`
3. **US Market Entry Checklist** — LLC formation, FDA registration, agent requirements, labeling, QSR/ISO 13485
4. **Mandarin webinars** — live Control Tower walkthrough, gated replay

## Revenue Tiers

| Tier         | Offering                                                                           | Price Range         |
| ------------ | ---------------------------------------------------------------------------------- | ------------------- |
| Free         | PMP course, 510(k) guide PDF, webinar replays                                      | $0 (lead gen)       |
| Starter      | Control Tower SaaS license (read-only dashboard per project)                       | $500-2K/mo          |
| Professional | Full PM engagement — run their Control Tower, manage gates, regulatory submissions | $10-25K/mo retainer |
| Enterprise   | End-to-end: regulatory strategy + PM + supplier mgmt + US entity setup             | $50-200K+ project   |

## Website & Digital

- Bilingual (EN/CN) landing page with live Control Tower demo embed
- Domain options: archmedicalmanagement.com, archmedical.com, + .cn domain
- SEO: long-tail keywords in EN + CN ("FDA 510(k) process for Chinese company", "美国FDA 510(k) 申请流程")
- Blog + LinkedIn articles in both languages
- **WeChat Official Account** — essential for Chinese entrepreneur reach

## Partnerships & Channels

- Chinese medical device accelerators/incubators (Shenzhen, Suzhou, Hangzhou biotech parks)
- US immigration attorneys (EB-1/E-2 visa clients)
- CROs and testing labs (UL, TÜV, Intertek) — referral partnerships
- Trade associations: CBIA, AdvaMed, RAPS — speaking, articles

## Technology Roadmap

- **Multi-tenant Control Tower**: Row-level security per client in Supabase → SaaS play
- **Template library**: Pre-built templates for common 510(k) predicate categories (respiratory, cardiovascular, orthopedic, IVD)
- **AI regulatory gap analysis**: Expose `generate_regulatory_analysis.py` as self-service tool

## Immediate Next Steps (discussed March 25, 2026)

1. Build bilingual landing page (Next.js or static) with Control Tower demo embed + lead capture
2. WeChat Official Account setup
3. Package 510(k) guide with Arch Medical branding
4. CRM setup (Notion or HubSpot free tier)

## Context

- Built on ICU Respiratory Digital Twin medical device project experience
- Control Tower has 14 tabs: Dual-Track, Gate System, Regulatory Tracker, Risk Dashboard, Audit Trail, Document Control, Actions, Timeline, Budget, Cash/Runway, US Investment, Resources, Suppliers, Message Board
- GitHub: londailey6937/Control-Tower, master branch
- Supabase backend with audit trail + message board
- Existing generators: guides, charter, roadmap, pitch (EN+CN), resume (EN+CN), regulatory analysis, FDA 510(k) guide, Q&A factsheet
