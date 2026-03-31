#!/usr/bin/env python3
"""
Generate 510(k) Bridge 5-Year Business Strategy — English PDF
510k Bridge, Inc.
"""

import os
from fpdf import FPDF

OUT_DIR = os.path.dirname(os.path.abspath(__file__))

BLUE = (30, 90, 200)
DARK = (15, 17, 23)
GRAY = (120, 120, 130)
TEXT = (40, 40, 45)
GREEN = (16, 120, 80)
AMBER = (180, 120, 10)
RED = (200, 40, 40)

_MAP = str.maketrans({
    "\u2014": "--", "\u2013": "-", "\u2019": "'", "\u2018": "'",
    "\u201c": '"', "\u201d": '"', "\u2026": "...", "\u00a0": " ",
    "\u2022": "-", "\u2192": "->",
})

def _s(t):
    return t.translate(_MAP)


class StrategyPDF(FPDF):
    def header(self):
        if self.page_no() <= 2:
            return
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(*GRAY)
        self.cell(0, 8, _s("510(k) Bridge -- 5-Year Business Strategy"), align="R", ln=True)
        self.ln(2)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(*GRAY)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")

    def sec(self, num, title):
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(*BLUE)
        self.cell(0, 10, _s(f"{num}. {title}"), new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(*BLUE)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(4)

    def sub(self, title):
        self.set_font("Helvetica", "B", 12)
        self.set_text_color(*TEXT)
        self.cell(0, 8, _s(title), new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def txt(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*TEXT)
        self.multi_cell(0, 5.5, _s(text), new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def bul(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*TEXT)
        self.multi_cell(0, 5.5, _s("  - " + text), new_x="LMARGIN", new_y="NEXT")

    def kv(self, key, val):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(*BLUE)
        self.cell(0, 5.5, _s(key), new_x="LMARGIN", new_y="NEXT")
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*TEXT)
        self.multi_cell(0, 5.5, _s("  " + val), new_x="LMARGIN", new_y="NEXT")
        self.ln(1)


def build():
    pdf = StrategyPDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()

    # ── Cover ──
    pdf.ln(30)
    pdf.set_font("Helvetica", "B", 28)
    pdf.set_text_color(*BLUE)
    pdf.cell(0, 14, "510(k) Bridge", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 16)
    pdf.set_text_color(*TEXT)
    pdf.cell(0, 9, "5-Year Business Strategy", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(6)
    pdf.set_font("Helvetica", "I", 11)
    pdf.set_text_color(*GRAY)
    pdf.cell(0, 7, "510k Bridge", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 7, "510k Bridge, Inc.", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 7, "Version 2.0 | March 2026", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(20)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(*TEXT)
    pdf.multi_cell(0, 5.5, _s(
        "This document outlines a five-year strategy for 510k Bridge to become "
        "the leading SaaS platform and professional services partner for Chinese medical "
        "device companies pursuing FDA 510(k) clearance in the United States."
    ), align="C")

    # ── 1. Executive Summary ──
    pdf.add_page()
    pdf.sec(1, "Executive Summary")
    pdf.txt(
        "510k Bridge operates two complementary SaaS products and a professional "
        "services practice targeting Chinese medical device companies entering the US market "
        "through the FDA 510(k) pathway.\n\n"
        "Core Products:\n"
        "  1. Control Tower -- Project management dashboard for 510(k) programs\n"
        "  2. 510(k) Predicate Finder -- FDA database search, predicate chain tracing, "
        "and substantial equivalence argument generation\n\n"
        "The combined product suite covers the full lifecycle from regulatory strategy "
        "(Predicate Finder) through execution management (Control Tower). Professional "
        "services layer on top for clients who need hands-on regulatory and project "
        "management support.")

    # ── 2. Market Opportunity ──
    pdf.add_page()
    pdf.sec(2, "Market Opportunity")
    pdf.txt(
        "China's medical device industry is the world's second largest ($80B+ in 2025) "
        "and growing 15-20% annually. Some 300+ Chinese device companies attempt US market "
        "entry each year, with most targeting the 510(k) pathway as the fastest route to "
        "FDA clearance.\n\n"
        "Key challenges these companies face:\n"
        "  1. Unknown US regulatory process -- 510(k) differs significantly from NMPA\n"
        "  2. Predicate device selection -- incorrect predicate is the #1 cause of FDA rejection\n"
        "  3. Language and cultural barriers -- most FDA guidance is English-only\n"
        "  4. Project management gaps -- multi-year regulatory programs fail without structure\n"
        "  5. US entity formation & investor relations -- EB-1/E-2 visa, Delaware LLC, banking")

    pdf.sub("2.1 Serviceable Addressable Market")
    pdf.txt(
        "  Total Addressable Market (TAM): $4.2B (global regulatory SaaS + services)\n"
        "  Serviceable Addressable Market (SAM): $420M (Chinese device companies, US 510(k))\n"
        "  Serviceable Obtainable Market (SOM): $8.4M at Year 5 (20 clients, $35K avg)")

    pdf.sub("2.2 Competitive Landscape")
    pdf.txt(
        "  Greenlight Guru  -- QMS + design control. $30K/yr. No bilingual, no predicate tool.\n"
        "  MasterControl     -- Enterprise QMS. $100K+/yr. Overkill for 510(k)-stage startups.\n"
        "  Qualio            -- Cloud QMS. $20K/yr. No PM dashboard, no Chinese market focus.\n"
        "  Regulatory consultants -- $300-500/hr. Fragmented, no tooling.\n"
        "  Immigration/corporate attorneys -- $5-15K per entity setup. Email-based, no dashboard.\n\n"
        "None of these competitors offer a bilingual (EN/CN) platform combining PM dashboard, "
        "predicate research, QMS, entity setup tracking, and SE argument generation. "
        "Full QMS systems cost $30K-$100K/yr and take months to implement -- startups need "
        "just enough QMS to pass FDA audit, which is the QMS-Lite opportunity.")

    # ── 3. Product Portfolio ──
    pdf.add_page()
    pdf.sec(3, "Product Portfolio")

    pdf.sub("3.1 Control Tower PM Dashboard")
    pdf.txt(
        "A Vite + TypeScript SaaS application with Supabase backend providing:\n\n"
        "  16 tabs covering dual-track milestones, gate system, risk dashboard, regulatory "
        "tracker, audit trail, document control, actions (DHF/DMR/CAPA), timeline, budget, "
        "cash/runway, US investment, cap table, resources, suppliers, message board, FDA comms\n\n"
        "  Multi-tenant with row-level security (Supabase RLS)\n"
        "  Bilingual EN/CN interface with one-click toggle\n"
        "  Role-based access: PMP, Technology, Business, Accounting\n"
        "  7 pre-built category templates for common device types\n"
        "  Setup Wizard for guided project configuration")

    pdf.sub("3.2 510(k) Predicate Finder")
    pdf.txt(
        "A standalone SaaS tool (Vite + TypeScript, Tailwind CSS) that searches the "
        "FDA openFDA 510(k) database and provides:\n\n"
        "  Database Search -- Query by product code, applicant, device name, or K-number\n"
        "  Advanced Filters -- Year range, decision type (SE/NSE), review type\n"
        "  Device Detail -- Full 510(k) record with predicate references\n"
        "  Predicate Chain -- Trace the predicate lineage backward up to 5 levels\n"
        "  Device Comparison -- Side-by-side comparison of up to 4 devices\n"
        "  SE Argument Generator -- Auto-generates substantial equivalence draft\n"
        "  Bilingual EN/CN -- Full interface translation\n\n"
        "Freemium Model:\n"
        "  Free Tier -- 5 searches/day, 1 chain trace/day, 2-device comparison\n"
        "  Pro Tier (email gate) -- Unlimited search, full chain, 4-device compare, "
        "SE argument, PDF export\n\n"
        "The Predicate Finder serves as the primary lead magnet: free users provide "
        "their email to unlock premium features, entering the sales funnel for Control "
        "Tower and professional services.")

    pdf.sub("3.3 QMS-Lite for Startups")
    pdf.txt(
        "A lightweight quality management system built for 510(k)-stage startups that need "
        "just enough QMS to pass FDA audit without the $30K-$100K/yr cost of full platforms.\n\n"
        "Modules (aligned to 21 CFR 820 / ISO 13485):\n"
        "  Document Control -- Version-controlled SOPs, work instructions, forms\n"
        "  CAPA -- Corrective and preventive action tracking with root cause analysis\n"
        "  Training Records -- Employee training matrix, sign-off tracking, competency logs\n"
        "  Supplier Qualification -- Approved supplier list, audit schedules, scorecards\n"
        "  Complaint Handling -- Customer complaint intake, investigation, trending\n\n"
        "Market: Every 510(k) applicant needs QMS and most are using spreadsheets.\n"
        "Pricing: $200-$500/mo per company (vs. $2.5K-$8K/mo for Greenlight Guru / MasterControl).\n"
        "Half the modules already exist as Control Tower tabs (Document Control, Actions/CAPA, "
        "Suppliers).")

    pdf.sub("3.4 Cross-Border Entity Setup Tracker")
    pdf.txt(
        "A dashboard for Chinese companies setting up US operations. Nobody has a "
        "structured tool for this -- it is all handled via email chains with lawyers.\n\n"
        "Checklist Modules:\n"
        "  Delaware C-Corp Formation -- Articles of incorporation, bylaws, EIN\n"
        "  Oregon Registration -- Foreign entity registration, business license\n"
        "  Washington Registration -- Foreign entity registration, B&O tax setup\n"
        "  Registered Agent -- Appointment and annual renewal tracking\n"
        "  US Bank Account -- Application status, signatory requirements\n"
        "  FDA Establishment Registration -- Facility registration, device listing\n"
        "  US Agent Appointment -- FDA-required US agent designation\n"
        "  Labeling Compliance -- 21 CFR 801 requirements checklist\n"
        "  State Business Licenses -- State-specific permits and renewals\n"
        "  Insurance -- Product liability, general liability, D&O\n\n"
        "Pricing: $1K-$5K one-time setup or $200/mo SaaS.\n"
        "Revenue kicker: Referral partnerships with immigration attorneys, corporate "
        "service providers, and registered agent companies.")

    pdf.sub("3.5 Lead Magnets & Content")
    pdf.txt(
        "  Stanford PMP Course -- Free professional development giveaway\n"
        "  FDA 510(k) Pathway Guide -- Branded PDF (EN + CN)\n"
        "  US Market Entry Checklist -- LLC formation, FDA registration, labeling, QSR\n"
        "  Mandarin Webinars -- Live Control Tower demos, gated replays\n"
        "  WeChat Official Account -- Content distribution for Chinese market")

    # ── 4. Revenue Model ──
    pdf.add_page()
    pdf.sec(4, "Revenue Model")

    pdf.sub("4.1 SaaS Tiers")
    pdf.txt(
        "  Predicate Finder Free -- $0 (lead generation, email capture)\n"
        "  Predicate Finder Pro -- $99/mo (unlimited searches, SE arguments, PDF export)\n"
        "  Control Tower Starter -- $500/mo (read-only dashboard per project)\n"
        "  Control Tower Growth -- $1,000/mo (full dashboard, 2 projects, message board)\n"
        "  Control Tower Scale -- $2,000/mo (multi-project, Predicate Finder embedded, "
        "cap table, FDA comms)\n"
        "  QMS-Lite Starter -- $200/mo (doc control, CAPA, training records)\n"
        "  QMS-Lite Pro -- $500/mo (full suite incl. supplier qual, complaint handling)\n"
        "  Entity Setup Tracker -- $200/mo SaaS or $1K-$5K one-time setup")

    pdf.sub("4.2 Professional Services")
    pdf.txt(
        "  Regulatory Consulting -- $250-500/hr ad hoc\n"
        "  Project Management Retainer -- $10-25K/mo (run their Control Tower)\n"
        "  Enterprise Engagement -- $50-200K+ per project "
        "(end-to-end: regulatory strategy + PM + supplier mgmt + US entity setup)")

    pdf.sub("4.3 Revenue Projections (5-Year)")
    pdf.txt(
        "  Year 1 -- Product launch + 3 clients  = $240K ARR\n"
        "    Predicate Finder: 500 free users, 20 Pro ($24K)\n"
        "    Control Tower: 3 Starter clients ($18K)\n"
        "    Entity Setup: 5 one-time setups at $3K avg ($15K)\n"
        "    QMS-Lite: 3 Starter clients ($7K, partial year)\n"
        "    Services: 1 retainer at $10K/mo ($120K) + ad hoc ($18K)\n"
        "    Referral commissions: immigration/corporate ($38K)\n\n"
        "  Year 2 -- Market validation + 8 clients = $780K ARR\n"
        "    Predicate Finder: 2,000 free users, 80 Pro ($95K)\n"
        "    Control Tower: 3 Starter + 4 Growth + 1 Scale ($102K)\n"
        "    QMS-Lite: 15 clients avg $300/mo ($54K)\n"
        "    Entity Setup: 20 setups + 10 SaaS ($86K)\n"
        "    Services: 3 retainers ($360K) + ad hoc ($43K)\n"
        "    Referral commissions ($40K)\n\n"
        "  Year 3 -- Growth phase + 15 clients = $2.1M ARR\n"
        "    Predicate Finder: 5,000 free users, 200 Pro ($238K)\n"
        "    Control Tower: 5 Starter + 6 Growth + 4 Scale ($198K)\n"
        "    QMS-Lite: 40 clients avg $350/mo ($168K)\n"
        "    Entity Setup: 40 setups + 25 SaaS ($170K)\n"
        "    Services: 6 retainers ($900K) + consulting ($264K)\n"
        "    Referral commissions ($62K)\n\n"
        "  Year 4 -- Scale + 30 clients = $4.5M ARR\n"
        "    Predicate Finder: 10,000 free, 500 Pro ($594K)\n"
        "    Control Tower: 10 Starter + 12 Growth + 8 Scale ($396K)\n"
        "    QMS-Lite: 80 clients avg $400/mo ($384K)\n"
        "    Entity Setup: 60 setups + 40 SaaS ($220K)\n"
        "    Services: 10 retainers ($1.8M) + enterprise ($710K)\n"
        "    Referral commissions ($96K) + QMS upsell ($300K)\n\n"
        "  Year 5 -- Market leader + 50 clients = $10.8M ARR\n"
        "    Predicate Finder: 20,000 free, 1,000 Pro ($1.2M)\n"
        "    Control Tower: 15 Starter + 20 Growth + 15 Scale ($690K)\n"
        "    QMS-Lite: 150 clients avg $420/mo ($756K)\n"
        "    Entity Setup: 100 setups + 60 SaaS ($360K)\n"
        "    Services: 15 retainers ($3.6M) + enterprise ($2.9M)\n"
        "    Referral commissions ($150K) + QMS upsell ($1.1M)")

    # ── 5. Go-to-Market Strategy ──
    pdf.add_page()
    pdf.sec(5, "Go-to-Market Strategy")

    pdf.sub("5.1 Funnel: Free -> SaaS -> Services")
    pdf.txt(
        "  Stage 1 -- Predicate Finder (free) attracts regulatory professionals\n"
        "  Stage 2 -- Email gate captures leads with 510(k) guide + PMP course\n"
        "  Stage 3 -- Pro upgrade ($99/mo) for power users doing active submissions\n"
        "  Stage 4 -- Control Tower demo for teams managing multi-month programs\n"
        "  Stage 5 -- Professional services engagement for hands-on clients\n\n"
        "Conversion targets: Free -> Pro: 5% | Pro -> CT Trial: 15% | Trial -> Paid: 30%")

    pdf.sub("5.2 China Market Channels")
    pdf.txt(
        "  WeChat Official Account -- Primary content distribution\n"
        "  Chinese medical device accelerators (Shenzhen, Suzhou, Hangzhou biotech parks)\n"
        "  US immigration attorneys (EB-1/E-2 visa clients needing FDA pathway)\n"
        "  CROs and testing labs (UL, TUV, Intertek) -- referral partnerships\n"
        "  Trade associations: CBIA, AdvaMed, RAPS -- speaking engagements\n"
        "  LinkedIn + bilingual blog content\n"
        "  Mandarin webinars with gated replays")

    pdf.sub("5.3 SEO & Digital")
    pdf.txt(
        "  Long-tail EN: 'FDA 510(k) process for Chinese company'\n"
        "  Long-tail CN: 'FDA 510(k) shenqing liucheng' (application process)\n"
        "  Domain: 510kbridge.com + .cn\n"
        "  Bilingual landing page with live Control Tower demo embed")

    # ── 6. Technology Roadmap ──
    pdf.add_page()
    pdf.sec(6, "Technology Roadmap")

    pdf.sub("6.1 Year 1 (2026)")
    pdf.txt(
        "  Q1 -- Control Tower v1.1: DMR tracker, FDA Comms tab, message board\n"
        "  Q2 -- Predicate Finder launch with freemium gating\n"
        "  Q2 -- 510k Bridge website launch (510kbridge.com)\n"
        "  Q3 -- Multi-tenant Control Tower (Supabase RLS per client)\n"
        "  Q3 -- Cross-Border Entity Setup Tracker v1 (DE C-Corp, OR, WA registration)\n"
        "  Q4 -- Predicate Finder Pro: PDF export, bulk comparison, saved searches\n"
        "  Q4 -- QMS-Lite MVP: Document Control + CAPA modules")

    pdf.sub("6.2 Year 2 (2027)")
    pdf.txt(
        "  Q1 -- QMS-Lite: Training Records + Supplier Qualification modules\n"
        "  Q1 -- Entity Setup Tracker: bank account + FDA registration workflows\n"
        "  Q2 -- QMS-Lite: Complaint Handling + full 21 CFR 820 alignment\n"
        "  Q2 -- Predicate Finder embedded as Control Tower Scale tab\n"
        "  Q3 -- AI regulatory gap analysis: expose generate_regulatory_analysis.py as self-service\n"
        "  Q3 -- Entity Setup referral partner portal (attorneys, CSPs)\n"
        "  Q4 -- API integrations: Supabase Edge Functions for automated notifications\n"
        "  Q4 -- QMS-Lite + Control Tower unified dashboard")

    pdf.sub("6.3 Years 3-5 (2028-2030)")
    pdf.txt(
        "  Template library for common predicate categories (respiratory, cardiovascular, "
        "orthopedic, IVD, imaging, rehab, SaMD)\n"
        "  QMS-Lite ISO 13485 audit-ready report generator\n"
        "  Entity Setup Tracker: automated state filings + annual renewal reminders\n"
        "  Mobile app for on-the-go project monitoring\n"
        "  De Novo and PMA pathway extensions\n"
        "  EU MDR / CE marking module (expand beyond FDA)\n"
        "  White-label option for regulatory consulting firms")

    # ── 7. Organizational Plan ──
    pdf.add_page()
    pdf.sec(7, "Organizational Plan")

    pdf.sub("7.1 Corporate Structure")
    pdf.txt(
        "  Operating Entity: 510k Bridge, Inc. (Delaware corporation)\n"
        "  Contracts & Invoices: '510k Bridge, Inc.'")

    pdf.sub("7.2 Team (Year 1)")
    pdf.txt(
        "  Founder / CEO -- Business development, product vision, regulatory strategy,\n"
        "    software development, frontend/backend maintenance\n"
        "  Sales / BD (China) -- WeChat, accelerator relationships")

    pdf.sub("7.3 Hiring Plan (Years 2-5)")
    pdf.txt(
        "  Year 2: Full-time developer, regulatory associate, sales lead\n"
        "  Year 3: Head of Product, 2 additional developers, customer success\n"
        "  Year 4: VP Sales, regulatory team (3), marketing lead\n"
        "  Year 5: COO, expanded engineering (8), enterprise sales team")

    # ── 8. Financial Plan ──
    pdf.add_page()
    pdf.sec(8, "Financial Plan")

    pdf.sub("8.1 Startup Costs")
    pdf.txt(
        "  Domain registration (510kbridge.com) -- $10/yr\n"
        "  CloudFlare Pages hosting -- $0 (free tier)\n"
        "  Supabase -- $0 free tier (upgrade at $25/mo at scale)\n"
        "  Development tools -- $0 (open source stack)\n"
        "  Legal (contract templates, prepared in China) -- $500\n"
        "  Initial marketing (WeChat, LinkedIn, China-based) -- $1,500\n"
        "  Total Year 1 startup: ~$2,500")

    pdf.sub("8.2 Operating Costs (Monthly, Year 1)")
    pdf.txt(
        "  Cloud hosting -- $25/mo\n"
        "  SaaS tools (email, CRM) -- $50/mo\n"
        "  Marketing (China-based) -- $200/mo\n"
        "  Total: ~$275/mo = $3,300/yr")

    pdf.sub("8.3 Break-Even Analysis")
    pdf.txt(
        "  Monthly cost: $275\n"
        "  Revenue needed: 1 CT Starter ($500) = $500/mo covers operating costs\n"
        "  Break-even: Month 1-2 with first paying client\n"
        "  Gross margin target: 85% (SaaS) / 65% (services)")

    # ── 9. Risk Factors ──
    pdf.add_page()
    pdf.sec(9, "Risk Factors")
    pdf.txt(
        "  1. Market adoption -- Chinese companies may prefer local consultants\n"
        "     Mitigation: Bilingual platform, WeChat presence, China-based BD\n\n"
        "  2. FDA regulatory changes -- New submission requirements\n"
        "     Mitigation: Modular architecture, rapid template updates\n\n"
        "  3. Competition -- Greenlight Guru or Qualio add Chinese support\n"
        "     Mitigation: First-mover advantage, predicate tool differentiation\n\n"
        "  4. Single-founder risk -- Key person dependency\n"
        "     Mitigation: Documented codebase, modular architecture, early hiring\n\n"
        "  5. openFDA API changes -- Rate limits or data format changes\n"
        "     Mitigation: Local caching, fallback to FDA 510(k) database downloads\n\n"
        "  6. QMS regulatory evolution -- 21 CFR 820 harmonization with ISO 13485\n"
        "     Mitigation: Modular QMS design, template-driven compliance updates\n\n"
        "  7. State registration complexity -- 50 states with different requirements\n"
        "     Mitigation: Start with DE/OR/WA, expand based on client demand")

    # ── 10. Milestones & KPIs ──
    pdf.add_page()
    pdf.sec(10, "Milestones & KPIs")

    pdf.sub("10.1 Year 1 Milestones")
    pdf.txt(
        "  Q1 -- Control Tower v1.1 shipped, Predicate Finder MVP\n"
        "  Q2 -- 510kbridge.com live, first 100 Predicate Finder users\n"
        "  Q3 -- First paying CT client, first professional services retainer\n"
        "  Q3 -- Entity Setup Tracker v1 live (DE/OR/WA)\n"
        "  Q4 -- QMS-Lite MVP live (Doc Control + CAPA)\n"
        "  Q4 -- 500 PF free users, 3 CT clients, $20K MRR")

    pdf.sub("10.2 Key Performance Indicators")
    pdf.txt(
        "  Predicate Finder free registrations (target: 500 Y1 / 20,000 Y5)\n"
        "  PF Free -> Pro conversion rate (target: 5%)\n"
        "  Control Tower paying clients (target: 3 Y1 / 50 Y5)\n"
        "  QMS-Lite paying clients (target: 3 Y1 / 150 Y5)\n"
        "  Entity Setup completions (target: 5 Y1 / 100 Y5)\n"
        "  Monthly Recurring Revenue (target: $20K Y1 / $900K Y5)\n"
        "  Professional services revenue (target: $140K Y1 / $6.5M Y5)\n"
        "  Net Promoter Score (target: 50+)\n"
        "  Client retention rate (target: 90%+)")

    pdf.sub("10.3 Exit Strategy")
    pdf.txt(
        "  Strategic acquisition by QMS vendor (Greenlight Guru, Qualio, MasterControl)\n"
        "  Private equity roll-up of regulatory tech platforms\n"
        "  Continue as lifestyle business at $5-11M ARR with 75% gross margins")

    path = os.path.join(OUT_DIR, "510kBridge_5Year_Business_Strategy_EN.pdf")
    pdf.output(path)
    return path


if __name__ == "__main__":
    p = build()
    print(f"Generated: {p}")
