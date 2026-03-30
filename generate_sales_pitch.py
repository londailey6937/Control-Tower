#!/usr/bin/env python3
"""
Generate a bilingual (EN + CN) sales pitch PDF for internal sales managers.

This is a SALES MANAGER'S PLAYBOOK — not a client-facing document.
It tells the sales team exactly what to say, how to set expectations,
what support the client gets, security details, and answers to common
client questions.

Entity: 510kBridge Consulting (Shanghai) Co., Ltd. -- WFOE
Target audience: 510kBridge sales managers / account executives

Outputs:
  Sales_Pitch_EN.pdf   (English)
  Sales_Pitch_CN.pdf   (Chinese)
"""

import os
from fpdf import FPDF

OUT = os.path.dirname(os.path.abspath(__file__))
CJK_FONT = "/Library/Fonts/Arial Unicode.ttf"

_MAP = str.maketrans({
    "\u2014": "--", "\u2013": "-", "\u2019": "'", "\u201c": '"', "\u201d": '"',
    "\u2018": "'", "\u2265": ">=", "\u2264": "<=", "\u00b5": "u", "\u00d7": "x",
    "\u2022": "-", "\u2026": "...", "\u00ae": "(R)",
})

def _a(s):
    return s.translate(_MAP)


# ═══════════════════════════════════════════════════════════════════════════════
#  BASE CLASS
# ═══════════════════════════════════════════════════════════════════════════════

class SalesPitchBase(FPDF):
    BRAND   = (0, 82, 136)       # 510kBridge teal-blue
    DARK    = (35, 35, 40)
    GRAY    = (110, 110, 120)
    ACCENT  = (0, 128, 96)       # green accent
    RED     = (180, 30, 30)
    WHITE   = (255, 255, 255)
    LTGRAY  = (245, 245, 248)

    def section(self, num, title, page_break=True):
        page_body_bottom = self.h - self.b_margin
        if page_break and self.get_y() > (page_body_bottom - 25):
            self.add_page()
        self._set_font("B", 13)
        self.set_text_color(*self.BRAND)
        self.cell(0, 7, self._safe(f"{num}.  {title}" if num else title),
                  new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(*self.BRAND)
        self.set_line_width(0.4)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(3)

    def body(self, text):
        self._set_font("", 10)
        self.set_text_color(*self.DARK)
        self.multi_cell(0, 5.4, self._safe(text), align="L")
        self.ln(2)

    def bullet(self, text, bold_prefix=""):
        self._set_font("", 10)
        self.set_text_color(*self.DARK)
        self.cell(6, 5.4, self._safe("-"))
        if bold_prefix:
            self._set_font("B", 10)
            self.cell(self.get_string_width(self._safe(bold_prefix)) + 1,
                      5.4, self._safe(bold_prefix))
            self._set_font("", 10)
        self.multi_cell(0, 5.4, self._safe(text), align="L")
        self.ln(0.5)

    def key_value_row(self, label, value, label_w=58):
        self._set_font("B", 10)
        self.set_text_color(*self.DARK)
        self.cell(label_w, 5.4, self._safe(label))
        self._set_font("", 10)
        self.multi_cell(0, 5.4, self._safe(value), align="L")
        self.ln(0.5)

    def callout_box(self, text):
        self.set_fill_color(230, 242, 250)
        self.set_draw_color(*self.BRAND)
        self.set_line_width(0.5)
        x = self.l_margin + 3
        y = self.get_y()
        self.set_xy(x + 2, y + 2)
        self._set_font("I", 10)
        self.set_text_color(*self.BRAND)
        self.multi_cell(self.w - self.l_margin - self.r_margin - 10, 5.2,
                        self._safe(text), align="L")
        h = self.get_y() - y + 2
        self.rect(x, y, self.w - self.l_margin - self.r_margin - 6, h, style="D")
        self.ln(4)

    def tier_table(self, rows, col_widths, header):
        """Table with word-wrap support in the last column."""
        lh = 5  # line height
        # header
        self.set_fill_color(*self.BRAND)
        self._set_font("B", 8)
        self.set_text_color(*self.WHITE)
        for i, h in enumerate(header):
            self.cell(col_widths[i], 6, self._safe(h), border=1, fill=True, align="C")
        self.ln()
        # rows
        self._set_font("", 8)
        self.set_text_color(*self.DARK)
        for ri, row in enumerate(rows):
            fill = ri % 2 == 0
            if fill:
                self.set_fill_color(*self.LTGRAY)
            x0 = self.get_x()
            y0 = self.get_y()
            last = len(row) - 1
            # measure height of last column with multi_cell
            last_w = col_widths[last]
            last_text = self._safe(row[last])
            n_lines = max(1, len(self.multi_cell(
                last_w, lh, last_text, dry_run=True, output="LINES")))
            row_h = max(6, n_lines * lh)
            # check page break
            if y0 + row_h > self.h - self.b_margin:
                self.add_page()
                y0 = self.get_y()
            # draw fixed columns
            for i in range(last):
                self.set_xy(x0 + sum(col_widths[:i]), y0)
                self.cell(col_widths[i], row_h, self._safe(row[i]), border=1,
                          fill=fill, align="C" if i > 0 else "L")
            # draw last column with multi_cell
            self.set_xy(x0 + sum(col_widths[:last]), y0)
            self.multi_cell(last_w, lh, last_text, border=1, align="L",
                            fill=fill, new_x="LMARGIN", new_y="NEXT")
            # ensure cursor is below row
            if self.get_y() < y0 + row_h:
                self.set_y(y0 + row_h)
        self.ln(3)

    # Subclasses override
    def _set_font(self, style, size):
        raise NotImplementedError

    def _safe(self, s):
        raise NotImplementedError


# ═══════════════════════════════════════════════════════════════════════════════
#  ENGLISH PDF
# ═══════════════════════════════════════════════════════════════════════════════

class SalesPitchEN(SalesPitchBase):
    def _set_font(self, style, size):
        self.set_font("Helvetica", style, size)

    def _safe(self, s):
        return _a(s)

    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(*self.GRAY)
        self.cell(0, 4, _a("CONFIDENTIAL -- 510kBridge Consulting  |  Sales Manager Playbook"),
                  align="R")
        self.ln(5)

    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(*self.GRAY)
        self.cell(0, 4, f"Page {self.page_no()}/{{nb}}", align="C")


# ═══════════════════════════════════════════════════════════════════════════════
#  CHINESE PDF
# ═══════════════════════════════════════════════════════════════════════════════

class SalesPitchCN(SalesPitchBase):
    def __init__(self):
        super().__init__()
        self.add_font("CJK", "", CJK_FONT)
        self.add_font("CJK", "B", CJK_FONT)
        self.add_font("CJK", "I", CJK_FONT)

    def _set_font(self, style, size):
        self.set_font("CJK", style, size)

    def _safe(self, s):
        return s  # no transliteration for CJK

    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("CJK", "I", 7)
        self.set_text_color(*self.GRAY)
        self.cell(0, 4, "机密 -- 510kBridge Consulting  |  销售经理手册", align="R")
        self.ln(5)

    def footer(self):
        self.set_y(-12)
        self.set_font("CJK", "I", 7)
        self.set_text_color(*self.GRAY)
        self.cell(0, 4, f"\u7b2c {self.page_no()}/{{nb}} \u9875", align="C")


# ═══════════════════════════════════════════════════════════════════════════════
#  CONTENT BUILDERS
# ═══════════════════════════════════════════════════════════════════════════════

def _build_en():
    pdf = SalesPitchEN()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.add_page()

    # ── Cover ──
    pdf.set_fill_color(*SalesPitchBase.BRAND)
    pdf.rect(0, 0, 210, 55, style="F")
    pdf.set_font("Helvetica", "B", 22)
    pdf.set_text_color(*SalesPitchBase.WHITE)
    pdf.set_y(8)
    pdf.cell(0, 10, "Sales Manager Playbook", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 13)
    pdf.cell(0, 7, "FDA 510(k) Project Management & Regulatory Services",
             align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "I", 10)
    pdf.cell(0, 6, _a("INTERNAL USE ONLY -- Not for Client Distribution"),
             align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)
    pdf.set_draw_color(*SalesPitchBase.WHITE)
    pdf.set_line_width(0.3)
    pdf.line(40, pdf.get_y(), 170, pdf.get_y())
    pdf.ln(3)
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(0, 5, _a("510kBridge Consulting (Shanghai) Co., Ltd."),
             align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 9)
    pdf.cell(0, 5, _a("Wholly Foreign-Owned Enterprise (WFOE)"),
             align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 8)
    pdf.cell(0, 5, _a("US Headquarters:  Pilot Software LLC dba 510kBridge  |  Oregon, USA"),
             align="C", new_x="LMARGIN", new_y="NEXT")

    pdf.ln(8)
    pdf.set_text_color(*SalesPitchBase.DARK)

    # ══════════════════════════════════════════════════════════
    # 1. HOW TO POSITION 510kBridge
    # ══════════════════════════════════════════════════════════
    pdf.section("1", "How to Position 510kBridge to the Client", page_break=False)
    pdf.body(
        "Open every conversation with the client's pain point -- not our product. "
        "Chinese medical device companies face three recurring problems when "
        "entering the US market:"
    )
    pdf.bullet("25-30% of 510(k) submissions are refused within 15 days for "
               "documentation deficiencies. Our structured approach and RTA "
               "self-check eliminate this risk.",
               "High RTA Rejection Rate: ")
    pdf.bullet("Clients often pick the wrong predicate device, invalidating "
               "months of work. Our regulatory lead validates predicate selection "
               "before testing begins.",
               "Wrong Predicate Device: ")
    pdf.bullet("All foreign manufacturers must designate a US Agent. We serve as "
               "their US Agent, so this is included in Professional and Enterprise tiers.",
               "US Agent Requirement: ")

    pdf.callout_box(
        "KEY TALKING POINT:  \"We are not just consultants -- we are your US-based "
        "project management office. We run your FDA program, you focus on building "
        "the device.\""
    )

    # ══════════════════════════════════════════════════════════
    # 2. SERVICE TIERS -- WHAT TO SELL
    # ══════════════════════════════════════════════════════════
    pdf.section("2", "Service Tiers -- What to Sell and When")
    pdf.body(
        "Match the tier to the client's stage and budget. Use this guide to "
        "recommend the right starting point:"
    )

    pdf.tier_table(
        rows=[
            ["SaaS Starter", "$500/mo", "2", "Early-stage R&D, just exploring the US market. "
             "Gives them a real dashboard (dual-track, gates, timeline, budget). "
             "UPSELL to Growth once they begin testing."],
            ["SaaS Growth", "$1,000/mo", "5", "Active 510(k) program with testing underway. "
             "Adds regulatory tracker, audit trail, supplier management, cap table. "
             "UPSELL to Scale or Professional PM when they need FDA comms."],
            ["SaaS Scale", "$2,000/mo", "10", "Full platform including FDA Comms Center, "
             "message board, cash/runway, US investment tracking. "
             "Best for companies managing the process in-house with internal PMP."],
            ["Professional PM", "$10-25K/mo", "Unlimited", "Our PMP runs their entire FDA program. "
             "Includes US Agent, Q-Sub automation, gate reviews, supplier coordination. "
             "BEST MARGIN -- target this tier for companies with budget."],
            ["Enterprise", "$50K+/project", "Unlimited", "End-to-end turnkey engagement. We handle "
             "everything: regulatory strategy, 510(k) prep, US entity formation, DHF, submission. "
             "For clients who want to write one check and get FDA clearance."],
        ],
        col_widths=[28, 24, 8, 130],
        header=["Tier", "Price", "Seats", "When to Recommend / Sales Notes"],
    )

    pdf.callout_box(
        "PRICING NOTE:  All prices are in USD. Shanghai office can invoice in RMB at "
        "the prevailing exchange rate. Starter/Growth/Scale are monthly subscriptions. "
        "Professional PM is a retainer. Enterprise is project-based with milestone payments."
    )

    # ══════════════════════════════════════════════════════════
    # 3. SETTING CLIENT EXPECTATIONS
    # ══════════════════════════════════════════════════════════
    pdf.section("3", "Setting Client Expectations")
    pdf.body(
        "Be explicit about what the client should expect at each stage. "
        "Under-promising and over-delivering builds trust. Here is what to tell them:"
    )

    pdf.key_value_row("Timeline", "A typical 510(k) takes 9-18 months end-to-end. "
                      "Do NOT promise faster. Some clients expect 3-6 months -- "
                      "correct this immediately.", label_w=35)
    pdf.key_value_row("Cost Range", "$130K-$320K total per device module (testing, "
                      "consulting, FDA fees, certifications). SaaS fees are separate "
                      "from testing lab costs.", label_w=35)
    pdf.key_value_row("FDA Review", "FDA review takes 3-6 months AFTER submission. "
                      "We cannot control FDA's timeline. Additional Information "
                      "requests can add 60-180 days each.", label_w=35)
    pdf.key_value_row("Client Role", "The client must provide: device samples, "
                      "technical specifications, test reports, and timely responses "
                      "to our questions. Delays on their side delay the project.", label_w=35)
    pdf.key_value_row("No Guarantees", "We NEVER guarantee FDA clearance. We guarantee "
                      "a professionally managed, well-documented submission that "
                      "maximizes the probability of clearance.", label_w=35)
    pdf.key_value_row("Language", "All FDA submissions are in English. Our bilingual team "
                      "handles translation. The Control Tower dashboard is fully "
                      "bilingual (EN/CN).", label_w=35)

    pdf.callout_box(
        "SAY THIS EARLY:  \"Our job is to give your device the best possible chance "
        "of FDA clearance by managing every detail of the submission process. "
        "The FDA makes the final decision, but we make sure nothing is left to chance.\""
    )

    # ══════════════════════════════════════════════════════════
    # 4. CUSTOMER SUPPORT & ACCOUNT MANAGEMENT
    # ══════════════════════════════════════════════════════════
    pdf.section("4", "Customer Support & Account Management")
    pdf.body(
        "Every client gets a dedicated account manager. Here is the support model:"
    )

    pdf.tier_table(
        rows=[
            ["SaaS Starter", "Email support", "48-hour response", "Monthly status email",
             "Shanghai sales rep"],
            ["SaaS Growth", "Email + WeChat", "24-hour response", "Bi-weekly status call",
             "Shanghai account manager"],
            ["SaaS Scale", "Email + WeChat + phone", "Same-day response", "Weekly status call",
             "Dedicated account manager"],
            ["Professional PM", "Direct PMP access", "4-hour response", "Weekly standup + "
             "monthly gate review",
             "US PMP + Shanghai AM"],
            ["Enterprise", "Direct PMP + exec access", "2-hour response (business hrs)", "Weekly standup + "
             "bi-weekly exec briefing",
             "US PMP + Shanghai AM + exec sponsor"],
        ],
        col_widths=[28, 30, 28, 40, 64],
        header=["Tier", "Channels", "Response SLA", "Reporting Cadence", "Assigned Team"],
    )

    pdf.body("Account Manager Responsibilities:")
    pdf.bullet("Owns the client relationship -- first point of contact for all non-technical questions",
               "Relationship: ")
    pdf.bullet("Sends regular status updates on project milestones, gate decisions, and budget burn",
               "Reporting: ")
    pdf.bullet("Coordinates onboarding: Control Tower setup, team access, template selection",
               "Onboarding: ")
    pdf.bullet("Monitors client satisfaction and flags churn risk to sales leadership",
               "Retention: ")
    pdf.bullet("Identifies upsell opportunities (tier upgrades, additional device modules, US entity formation)",
               "Upsell: ")
    pdf.bullet("Schedules quarterly business reviews (QBRs) for Growth tier and above",
               "QBR: ")

    # ══════════════════════════════════════════════════════════
    # 5. SECURITY -- WHAT TO TELL THE CLIENT
    # ══════════════════════════════════════════════════════════
    pdf.section("5", "Security & Data Protection -- Talking Points")
    pdf.body(
        "Chinese clients will ask about data security. Here are the facts "
        "to share confidently:"
    )

    pdf.key_value_row("Data Location", "All project data is stored in the United States "
                      "(Supabase cloud infrastructure, US region). No data is stored "
                      "on Chinese servers.", label_w=38)
    pdf.key_value_row("Encryption", "Data encrypted in transit (TLS 1.2/1.3) and at rest "
                      "(AES-256). All connections use HTTPS -- HTTP is automatically "
                      "redirected.", label_w=38)
    pdf.key_value_row("Access Control", "Row-Level Security (RLS) enforced at the database level. "
                      "Each client's data is isolated by project_id -- no cross-project "
                      "visibility, even at the API level.", label_w=38)
    pdf.key_value_row("Edge Security", "HSTS (preload), Content Security Policy, "
                      "X-Content-Type-Options: nosniff, X-Frame-Options: SAMEORIGIN, "
                      "strict Referrer-Policy, Permissions-Policy (no camera/mic/geo).", label_w=38)
    pdf.key_value_row("Authentication", "Supabase Auth with API key enforcement. Service-role "
                      "keys are server-side only -- never exposed to browsers.", label_w=38)
    pdf.key_value_row("Audit Trail", "Every change (gate decisions, document status, "
                      "risk updates, milestone changes) is recorded with timestamp, "
                      "user, old value, and new value. Immutable -- cannot be deleted "
                      "by client users.", label_w=38)
    pdf.key_value_row("21 CFR Part 11", "Our audit trail and document control meet the "
                      "electronic records / electronic signatures requirements. "
                      "Records are retained for device lifetime + 2 years.", label_w=38)
    pdf.key_value_row("Hosting", "CloudFlare Pages (static assets) with CloudFlare CDN "
                      "for global performance. Database on Supabase (AWS us-west-2). "
                      "99.9% uptime SLA.", label_w=38)
    pdf.key_value_row("SOC Compliance", "Supabase infrastructure is SOC 2 Type II certified. "
                      "CloudFlare maintains SOC 2 Type II and ISO 27001.", label_w=38)

    pdf.callout_box(
        "IF ASKED ABOUT CHINA DATA LAWS:  Our servers are in the US, not China. "
        "This is intentional -- FDA requires records to be accessible to US inspectors. "
        "Data does not pass through Chinese servers. The Control Tower is accessed via "
        "standard HTTPS like any other website."
    )

    # ══════════════════════════════════════════════════════════
    # 6. CONTROL TOWER DEMO SCRIPT
    # ══════════════════════════════════════════════════════════
    pdf.section("6", "Control Tower -- Demo Script")
    pdf.body(
        "When giving the client a live demo, follow this sequence. Keep it under "
        "20 minutes. Focus on what matters to THEM, not every feature:"
    )

    pdf.bullet("Start with dual-track view: \"This is your project at a glance -- "
               "technical milestones on top, regulatory milestones below, all in "
               "one place.\"", "1. Dual-Track (2 min): ")
    pdf.bullet("Show Gate System: \"These are your go/no-go decision checkpoints. "
               "Our PMP reviews evidence and makes the call at each gate.\"",
               "2. Gates (2 min): ")
    pdf.bullet("Show Risk Dashboard: \"Every risk is tracked per ISO 14971, with "
               "severity, probability, controls, and mitigation status.\"",
               "3. Risks (1 min): ")
    pdf.bullet("Show Budget tab: \"Planned vs. actual for every cost category. "
               "No surprises.\"",
               "4. Budget (1 min): ")
    pdf.bullet("Switch to Chinese: \"Everything works in both languages -- toggle "
               "with one click. Your team in China sees Chinese, we see English.\"",
               "5. Language Toggle (30 sec): ")
    pdf.bullet("Show Document Control: \"Every document version tracked -- draft, "
               "in-review, approved, effective. Full revision history.\"",
               "6. Documents (2 min): ")
    pdf.bullet("Show Device Templates: \"Select your device category and we auto-configure "
               "standards, risks, budget lines, and timeline.\"",
               "7. Templates (2 min): ")
    pdf.bullet("Open the live demo at control-tower-bmx.pages.dev and let the client "
               "click around. Answer questions as they explore.",
               "8. Hands-On (5 min): ")

    pdf.callout_box(
        "DEMO TIP:  Always ask \"What type of device are you working on?\" FIRST. "
        "Then select their device template during the demo so they see their own "
        "category with realistic data."
    )

    # ══════════════════════════════════════════════════════════
    # 7. COMMON CLIENT QUESTIONS & ANSWERS
    # ══════════════════════════════════════════════════════════
    pdf.section("7", "Common Client Questions -- Prepared Answers")
    pdf.body(
        "Memorize these answers. Clients ask these questions in almost every meeting:"
    )

    qa = [
        ("How long does a 510(k) take?",
         "9-18 months end-to-end depending on device complexity, testing requirements, "
         "and how quickly you provide information. The FDA review alone is 3-6 months "
         "after submission."),
        ("How much does it cost?",
         "$130K-$320K total per device module. This includes testing lab fees ($75K-$185K), "
         "our project management ($10-25K/month), FDA user fees ($6.5K-$26K), and "
         "certifications ($15-30K). We provide a detailed cost estimate after the initial "
         "regulatory pathway assessment."),
        ("Can you guarantee FDA clearance?",
         "No one can guarantee FDA clearance -- that would be illegal to promise. "
         "What we guarantee is a professionally managed submission that addresses "
         "every FDA requirement. Our structured approach with gate reviews catches "
         "issues before they reach FDA."),
        ("Do we need a US company?",
         "You need a US Agent (required for all foreign manufacturers). A full US entity "
         "(Delaware C-Corp) is recommended if you plan to raise US investment or sell "
         "directly. We can help with both -- US Agent is included in Professional/Enterprise "
         "tiers, entity formation is an add-on service ($2K-5K)."),
        ("Is our data safe?",
         "All data is stored on US servers (SOC 2 Type II certified infrastructure), "
         "encrypted in transit and at rest. Each client has isolated data -- no other "
         "client can see your information. Our audit trail is immutable and meets "
         "21 CFR Part 11 requirements."),
        ("What if we already have a regulatory consultant?",
         "We complement existing consultants -- we are project managers, not just "
         "regulatory advisors. Our Control Tower platform keeps everyone aligned: "
         "your consultant, your engineering team, your QA team, and us. Many clients "
         "keep their regulatory consultant and add us for project execution."),
        ("Can we start with the cheapest plan?",
         "Absolutely. Start with the $500/month Starter tier to explore the platform. "
         "You can upgrade at any time, and all your data carries over. Most clients start "
         "at Starter or Growth and upgrade to Scale or Professional PM as their "
         "program accelerates."),
        ("Do you support our specific device type?",
         "We have 7 pre-built templates covering the most common 510(k) device categories: "
         "respiratory, cardiovascular, orthopedic, IVD, imaging, rehabilitation, and SaMD. "
         "If your device does not fit these categories, we configure a custom setup."),
        ("Who will manage our project?",
         "Lon Dailey -- US-citizen PMP certified by Stanford SCPM. He manages all FDA "
         "communications, gate decisions, and project execution directly. Your Shanghai "
         "account manager handles all day-to-day client communications in Chinese."),
        ("What happens after we get FDA clearance?",
         "We help with establishment registration, device listing, labeling compliance, "
         "and setting up your post-market surveillance system (complaint handling, MDR "
         "reporting). Many clients keep their Control Tower subscription for ongoing "
         "compliance management."),
        ("How do we communicate with the team?",
         "WeChat for daily communication with the Shanghai team. Email for formal "
         "correspondence. Control Tower message board for project-related discussions "
         "(all messages are logged and searchable). Video calls for weekly standups "
         "(Growth tier and above)."),
        ("What if FDA asks additional questions?",
         "This is normal -- FDA issues Additional Information (AI) requests on about "
         "40-50% of 510(k) submissions. We manage the response process: draft the answer, "
         "coordinate with your engineering team for technical data, and submit the response. "
         "Each AI request adds 60-180 days to the review timeline."),
    ]

    for q, a in qa:
        pdf.bullet(a, f"Q: {q}  A: ")
        pdf.ln(1)

    # ══════════════════════════════════════════════════════════
    # 8. ONBOARDING CHECKLIST
    # ══════════════════════════════════════════════════════════
    pdf.section("8", "Client Onboarding Checklist (Internal)")
    pdf.body(
        "Once the client signs, follow this checklist to get them set up. "
        "Target: complete within 5 business days."
    )

    pdf.bullet("Create project in Supabase: run onboard_client.sh <project_id> <tier> <seats>",
               "Day 1 -- Provision: ")
    pdf.bullet("Send the client their dashboard URL: control-tower-bmx.pages.dev/?project=<id>",
               "Day 1 -- Access: ")
    pdf.bullet("Schedule a 60-minute kickoff call (Shanghai AM + client team)",
               "Day 1 -- Kickoff: ")
    pdf.bullet("Walk client through the Setup Wizard: language, template selection, "
               "team members, budget, suppliers, documents",
               "Day 2 -- Wizard: ")
    pdf.bullet("Verify all team members have login access and can see the dashboard",
               "Day 2 -- Access Check: ")
    pdf.bullet("Collect device description, predicate device candidates, and "
               "any existing test reports from the client",
               "Day 3 -- Documents: ")
    pdf.bullet("Assign the US PMP and schedule the first weekly standup "
               "(Professional/Enterprise only)",
               "Day 3 -- PMP Assignment: ")
    pdf.bullet("Send welcome email with: dashboard URL, support contacts, "
               "WeChat group invitation, and first status report template",
               "Day 5 -- Welcome Pack: ")

    # ══════════════════════════════════════════════════════════
    # 9. COMPETITIVE DIFFERENTIATION
    # ══════════════════════════════════════════════════════════
    pdf.section("9", "How We Are Different -- Competitive Talking Points")

    pdf.tier_table(
        rows=[
            ["Traditional RA Firm", "Regulatory documents only, no PM, no dashboard, "
             "high hourly rates ($300-500/hr), English-only communication"],
            ["Chinese RA Consultant", "Cheaper but no US presence, cannot serve as "
             "US Agent, limited FDA interaction experience, no technology platform"],
            ["Big Consulting (Deloitte/KPMG)", "Expensive ($500K+), slow, "
             "generalist teams with no medical device specialization"],
            ["510kBridge", "US-based PMP + bilingual Shanghai team + 16-tab "
             "real-time dashboard + 7 device templates + US Agent -- all in one "
             "integrated service"],
        ],
        col_widths=[40, 150],
        header=["Competitor Type", "Our Advantage Over Them"],
    )

    # ══════════════════════════════════════════════════════════
    # 10. NEXT STEPS
    # ══════════════════════════════════════════════════════════
    pdf.section("10", "Sales Process -- Next Steps After This Meeting")
    pdf.body("Follow this sequence after every client meeting:")
    pdf.bullet("Send a follow-up email within 2 hours summarizing key discussion points", "1. ")
    pdf.bullet("Share the Control Tower demo link: control-tower-bmx.pages.dev", "2. ")
    pdf.bullet("If the client expressed interest, send a customized regulatory "
               "pathway assessment within 5 business days (coordinate with US PMP)", "3. ")
    pdf.bullet("Schedule a follow-up call within 1 week to review the assessment", "4. ")
    pdf.bullet("Prepare a formal proposal with recommended tier, estimated costs, "
               "and timeline", "5. ")
    pdf.bullet("Close the deal -- get signature on service agreement and initiate "
               "onboarding", "6. ")

    pdf.ln(3)
    pdf.body("Internal Contacts:")
    pdf.key_value_row("US PMP:", "Lon Dailey  |  info@510kbridge.com", label_w=32)
    pdf.key_value_row("Shanghai Office:", "510kBridge Consulting (Shanghai) Co., Ltd.", label_w=32)
    pdf.key_value_row("Demo URL:", "control-tower-bmx.pages.dev", label_w=32)
    pdf.key_value_row("Onboarding:", "Run onboard_client.sh (see Section 8)", label_w=32)

    path = os.path.join(OUT, "Sales_Pitch_EN.pdf")
    pdf.output(path)
    print(f"  [EN] {path}  ({os.path.getsize(path)//1024} KB)")
    return path


# ═══════════════════════════════════════════════════════════════════════════════
#  CHINESE VERSION
# ═══════════════════════════════════════════════════════════════════════════════

def _build_cn():
    pdf = SalesPitchCN()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.add_page()

    # ── Cover ──
    pdf.set_fill_color(*SalesPitchBase.BRAND)
    pdf.rect(0, 0, 210, 55, style="F")
    pdf._set_font("B", 22)
    pdf.set_text_color(*SalesPitchBase.WHITE)
    pdf.set_y(8)
    pdf.cell(0, 10, "\u9500\u552e\u7ecf\u7406\u624b\u518c", align="C",
             new_x="LMARGIN", new_y="NEXT")       # 销售经理手册
    pdf._set_font("", 13)
    pdf.cell(0, 7, "FDA 510(k) \u9879\u76ee\u7ba1\u7406\u4e0e\u6cd5\u89c4\u670d\u52a1",
             align="C", new_x="LMARGIN", new_y="NEXT")
    pdf._set_font("I", 10)
    pdf.cell(0, 6, "\u4ec5\u9650\u5185\u90e8\u4f7f\u7528 -- \u4e0d\u5f97\u5206\u53d1\u7ed9\u5ba2\u6237",
             align="C", new_x="LMARGIN", new_y="NEXT")  # 仅限内部使用
    pdf.ln(2)
    pdf.set_draw_color(*SalesPitchBase.WHITE)
    pdf.set_line_width(0.3)
    pdf.line(40, pdf.get_y(), 170, pdf.get_y())
    pdf.ln(3)
    pdf._set_font("B", 10)
    pdf.cell(0, 5, "510kBridge Consulting (\u4e0a\u6d77) Co., Ltd.",
             align="C", new_x="LMARGIN", new_y="NEXT")
    pdf._set_font("", 9)
    pdf.cell(0, 5, "\u5916\u5546\u72ec\u8d44\u4f01\u4e1a (WFOE)",
             align="C", new_x="LMARGIN", new_y="NEXT")
    pdf._set_font("", 8)
    pdf.cell(0, 5, "\u7f8e\u56fd\u603b\u90e8\uff1aPilot Software LLC dba 510kBridge  |  \u4fc4\u52d2\u5188\u5dde",
             align="C", new_x="LMARGIN", new_y="NEXT")

    pdf.ln(8)
    pdf.set_text_color(*SalesPitchBase.DARK)

    # ── 1. 如何定位510kBridge ──
    pdf.section("1", "\u5982\u4f55\u5411\u5ba2\u6237\u5b9a\u4f4d510kBridge")
    pdf.body(
        "\u6bcf\u6b21\u5bf9\u8bdd\u90fd\u4ece\u5ba2\u6237\u7684\u75db\u70b9\u5f00\u59cb -- "
        "\u800c\u4e0d\u662f\u6211\u4eec\u7684\u4ea7\u54c1\u3002\u4e2d\u56fd\u533b\u7597\u5668\u68b0"
        "\u4f01\u4e1a\u8fdb\u5165\u7f8e\u56fd\u5e02\u573a\u65f6\u9762\u4e34\u4e09\u4e2a\u53cd\u590d"
        "\u51fa\u73b0\u7684\u95ee\u9898\uff1a"
    )
    pdf.bullet("25-30%\u7684510(k)\u7533\u8bf7\u572815\u5929\u5185\u56e0\u6587\u4ef6\u7f3a\u9677"
               "\u88ab\u62d2\u7edd\u3002\u6211\u4eec\u7684\u7ed3\u6784\u5316\u65b9\u6cd5\u548c"
               "RTA\u81ea\u67e5\u6d88\u9664\u4e86\u8fd9\u4e00\u98ce\u9669\u3002",
               "\u9ad8RTA\u62d2\u7edd\u7387\uff1a")
    pdf.bullet("\u5ba2\u6237\u7ecf\u5e38\u9009\u62e9\u9519\u8bef\u7684\u5bf9\u6bd4\u5668\u68b0\uff0c"
               "\u5bfc\u81f4\u6570\u6708\u5de5\u4f5c\u767d\u8d39\u3002\u6211\u4eec\u7684\u6cd5\u89c4"
               "\u8d1f\u8d23\u4eba\u5728\u6d4b\u8bd5\u5f00\u59cb\u524d\u9a8c\u8bc1\u5bf9\u6bd4"
               "\u5668\u68b0\u9009\u62e9\u3002",
               "\u5bf9\u6bd4\u5668\u68b0\u9009\u62e9\u9519\u8bef\uff1a")
    pdf.bullet("\u6240\u6709\u5916\u56fd\u5236\u9020\u5546\u5fc5\u987b\u6307\u5b9a\u7f8e\u56fd"
               "\u4ee3\u7406\u4eba\u3002\u6211\u4eec\u62c5\u4efb\u7f8e\u56fd\u4ee3\u7406\u4eba\uff0c"
               "\u4e13\u4e1aPM\u548c\u4f01\u4e1a\u7248\u5c42\u7ea7\u5df2\u5305\u542b\u6b64\u670d\u52a1\u3002",
               "\u7f8e\u56fd\u4ee3\u7406\u4eba\u8981\u6c42\uff1a")

    pdf.callout_box(
        "\u6838\u5fc3\u8bdd\u672f\uff1a\u201c\u6211\u4eec\u4e0d\u4ec5\u4ec5\u662f\u987e\u95ee -- "
        "\u6211\u4eec\u662f\u60a8\u7684\u7f8e\u56fd\u9879\u76ee\u7ba1\u7406\u529e\u516c\u5ba4\u3002"
        "\u6211\u4eec\u8fd0\u884c\u60a8\u7684FDA\u9879\u76ee\uff0c\u60a8\u4e13\u6ce8\u4e8e\u5236\u9020"
        "\u5668\u68b0\u3002\u201d"
    )

    # ── 2. 服务层级 -- 什么时候卖什么 ──
    pdf.section("2", "\u670d\u52a1\u5c42\u7ea7 -- \u4ec0\u4e48\u65f6\u5019\u5356\u4ec0\u4e48")
    pdf.body(
        "\u6839\u636e\u5ba2\u6237\u7684\u9636\u6bb5\u548c\u9884\u7b97\u5339\u914d\u5c42\u7ea7\u3002"
        "\u4f7f\u7528\u6b64\u6307\u5357\u63a8\u8350\u6b63\u786e\u7684\u8d77\u59cb\u70b9\uff1a"
    )

    pdf.tier_table(
        rows=[
            ["SaaS \u5165\u95e8\u7248", "$500/\u6708", "2",
             "\u65e9\u671f\u7814\u53d1\uff0c\u521a\u5f00\u59cb\u63a2\u7d22\u7f8e\u56fd\u5e02\u573a\u3002"
             "\u63d0\u4f9b\u771f\u5b9e\u4eea\u8868\u677f\uff08\u53cc\u8f68\u3001\u95e8\u3001\u65f6\u95f4\u7ebf\u3001\u9884\u7b97\uff09\u3002"
             "\u5f53\u5ba2\u6237\u5f00\u59cb\u6d4b\u8bd5\u65f6\u5347\u7ea7\u5230\u589e\u957f\u7248\u3002"],
            ["SaaS \u589e\u957f\u7248", "$1,000/\u6708", "5",
             "\u6d3b\u8dc3\u7684510(k)\u9879\u76ee\uff0c\u6d4b\u8bd5\u8fdb\u884c\u4e2d\u3002"
             "\u6dfb\u52a0\u6cd5\u89c4\u8ddf\u8e2a\u5668\u3001\u5ba1\u8ba1\u8ddf\u8e2a\u3001\u4f9b\u5e94\u5546\u7ba1\u7406\u3001\u80a1\u6743\u8868\u3002"
             "\u5f53\u5ba2\u6237\u9700\u8981FDA\u901a\u4fe1\u65f6\u5347\u7ea7\u5230\u89c4\u6a21\u7248\u6216\u4e13\u4e1aPM\u3002"],
            ["SaaS \u89c4\u6a21\u7248", "$2,000/\u6708", "10",
             "\u5168\u5e73\u53f0\uff0c\u5305\u62ecFDA\u901a\u4fe1\u4e2d\u5fc3\u3001\u6d88\u606f\u677f\u3001"
             "\u73b0\u91d1/\u8dd1\u9053\u3001\u7f8e\u56fd\u6295\u8d44\u8ddf\u8e2a\u3002"
             "\u9002\u5408\u5185\u90e8\u6709PMP\u7684\u516c\u53f8\u81ea\u884c\u7ba1\u7406\u3002"],
            ["\u4e13\u4e1aPM", "$10-25K/\u6708", "\u65e0\u9650",
             "\u6211\u4eec\u7684PMP\u8fd0\u884c\u5176\u6574\u4e2aFDA\u9879\u76ee\u3002\u5305\u62ec\u7f8e\u56fd\u4ee3\u7406\u4eba\u3001"
             "Q-Sub\u81ea\u52a8\u5316\u3001\u95e8\u5ba1\u67e5\u3001\u4f9b\u5e94\u5546\u534f\u8c03\u3002"
             "\u6700\u4f73\u5229\u6da6 -- \u7784\u51c6\u6709\u9884\u7b97\u7684\u5ba2\u6237\u3002"],
            ["\u4f01\u4e1a\u7248", "$50K+/\u9879\u76ee", "\u65e0\u9650",
             "\u7aef\u5230\u7aef\u4ea4\u94a5\u5319\u670d\u52a1\u3002\u6211\u4eec\u5904\u7406\u4e00\u5207\uff1a"
             "\u6cd5\u89c4\u7b56\u7565\u3001510(k)\u51c6\u5907\u4e0e\u63d0\u4ea4\u3001\u7f8e\u56fd\u5b9e\u4f53"
             "\u7ec4\u5efa\u3001DHF\u3001\u63d0\u4ea4\u3002\u9002\u5408\u60f3\u5f00\u4e00\u5f20\u652f\u7968"
             "\u5c31\u83b7\u5f97FDA\u6e05\u9664\u7684\u5ba2\u6237\u3002"],
        ],
        col_widths=[28, 24, 8, 130],
        header=["\u5c42\u7ea7", "\u4ef7\u683c", "\u5e2d\u4f4d", "\u4f55\u65f6\u63a8\u8350 / \u9500\u552e\u5907\u6ce8"],
    )

    pdf.callout_box(
        "\u4ef7\u683c\u8bf4\u660e\uff1a\u6240\u6709\u4ef7\u683c\u5747\u4e3a\u7f8e\u5143\u3002\u4e0a\u6d77"
        "\u529e\u516c\u5ba4\u53ef\u4ee5\u6309\u5f53\u524d\u6c47\u7387\u4ee5\u4eba\u6c11\u5e01\u5f00\u7968\u3002"
        "\u5165\u95e8\u7248/\u589e\u957f\u7248/\u89c4\u6a21\u7248\u4e3a\u6708\u5ea6\u8ba2\u9605\u3002"
        "\u4e13\u4e1aPM\u4e3a\u6708\u5ea6\u62a4\u7ee7\u8d39\u3002\u4f01\u4e1a\u7248\u6309\u9879\u76ee"
        "\u91cc\u7a0b\u7891\u4ed8\u6b3e\u3002"
    )

    # ── 3. 设定客户期望 ──
    pdf.section("3", "\u8bbe\u5b9a\u5ba2\u6237\u671f\u671b")
    pdf.body(
        "\u660e\u786e\u544a\u77e5\u5ba2\u6237\u6bcf\u4e2a\u9636\u6bb5\u7684\u671f\u671b\u3002"
        "\u5c11\u8bf4\u591a\u505a\u5efa\u7acb\u4fe1\u4efb\u3002\u4ee5\u4e0b\u662f\u8981\u544a\u8bc9"
        "\u5ba2\u6237\u7684\u5185\u5bb9\uff1a"
    )

    pdf.key_value_row("\u65f6\u95f4\u7ebf",
                      "\u5178\u578b\u7684510(k)\u7aef\u5230\u7aef\u9700\u89819-18\u4e2a\u6708\u3002"
                      "\u4e0d\u8981\u627f\u8bfa\u66f4\u5feb\u3002\u67d0\u4e9b\u5ba2\u6237\u671f\u671b3-6\u4e2a\u6708 -- "
                      "\u7acb\u5373\u7ea0\u6b63\u8fd9\u4e00\u8bef\u89e3\u3002", label_w=35)
    pdf.key_value_row("\u6210\u672c\u8303\u56f4",
                      "\u6bcf\u4e2a\u5668\u68b0\u6a21\u5757\u603b\u8ba1$130K-$320K\uff08\u6d4b\u8bd5\u3001"
                      "\u54a8\u8be2\u3001FDA\u8d39\u7528\u3001\u8ba4\u8bc1\uff09\u3002SaaS\u8d39\u7528"
                      "\u4e0e\u6d4b\u8bd5\u5b9e\u9a8c\u5ba4\u8d39\u7528\u5206\u5f00\u3002", label_w=35)
    pdf.key_value_row("FDA\u5ba1\u67e5",
                      "FDA\u5ba1\u67e5\u5728\u63d0\u4ea4\u540e\u9700\u89813-6\u4e2a\u6708\u3002\u6211\u4eec"
                      "\u65e0\u6cd5\u63a7\u5236FDA\u7684\u65f6\u95f4\u7ebf\u3002\u8865\u5145\u4fe1\u606f"
                      "\u8bf7\u6c42\u53ef\u80fd\u6bcf\u6b21\u589e\u52a060-180\u5929\u3002", label_w=35)
    pdf.key_value_row("\u5ba2\u6237\u89d2\u8272",
                      "\u5ba2\u6237\u5fc5\u987b\u63d0\u4f9b\uff1a\u5668\u68b0\u6837\u54c1\u3001\u6280\u672f"
                      "\u89c4\u683c\u3001\u6d4b\u8bd5\u62a5\u544a\u3001\u53ca\u65f6\u56de\u590d\u95ee\u9898\u3002"
                      "\u5ba2\u6237\u65b9\u5ef6\u8fdf\u4f1a\u5ef6\u8fdf\u9879\u76ee\u3002", label_w=35)
    pdf.key_value_row("\u65e0\u4fdd\u8bc1",
                      "\u6211\u4eec\u7edd\u4e0d\u4fdd\u8bc1FDA\u6e05\u9664\u3002\u6211\u4eec\u4fdd\u8bc1"
                      "\u4e13\u4e1a\u7ba1\u7406\u7684\u3001\u6587\u6863\u5b8c\u5907\u7684\u63d0\u4ea4\uff0c"
                      "\u6700\u5927\u9650\u5ea6\u63d0\u9ad8\u6e05\u9664\u6982\u7387\u3002", label_w=35)
    pdf.key_value_row("\u8bed\u8a00",
                      "\u6240\u6709FDA\u63d0\u4ea4\u5747\u7528\u82f1\u6587\u3002\u6211\u4eec\u7684\u53cc\u8bed"
                      "\u56e2\u961f\u5904\u7406\u7ffb\u8bd1\u3002Control Tower\u4eea\u8868\u677f\u5b8c\u5168"
                      "\u53cc\u8bed\uff08\u4e2d/\u82f1\uff09\u3002", label_w=35)

    pdf.callout_box(
        "\u65e9\u671f\u8bf4\u8fd9\u53e5\u8bdd\uff1a\u201c\u6211\u4eec\u7684\u5de5\u4f5c\u662f\u901a\u8fc7"
        "\u7ba1\u7406\u63d0\u4ea4\u8fc7\u7a0b\u7684\u6bcf\u4e00\u4e2a\u7ec6\u8282\uff0c\u7ed9\u60a8\u7684"
        "\u5668\u68b0\u6700\u5927\u7684FDA\u6e05\u9664\u673a\u4f1a\u3002FDA\u505a\u6700\u7ec8\u51b3\u5b9a\uff0c"
        "\u4f46\u6211\u4eec\u786e\u4fdd\u4e0d\u7559\u4efb\u4f55\u4e8b\u60c5\u788d\u4e8e\u5076\u7136\u3002\u201d"
    )

    # ── 4. 客户支持与客户管理 ──
    pdf.section("4", "\u5ba2\u6237\u652f\u6301\u4e0e\u5ba2\u6237\u7ba1\u7406")
    pdf.body(
        "\u6bcf\u4e2a\u5ba2\u6237\u90fd\u6709\u4e13\u5c5e\u5ba2\u6237\u7ecf\u7406\u3002"
        "\u4ee5\u4e0b\u662f\u652f\u6301\u6a21\u5f0f\uff1a"
    )

    pdf.tier_table(
        rows=[
            ["SaaS \u5165\u95e8\u7248", "\u90ae\u4ef6", "48\u5c0f\u65f6\u54cd\u5e94",
             "\u6708\u5ea6\u72b6\u6001\u90ae\u4ef6",
             "\u4e0a\u6d77\u9500\u552e\u4ee3\u8868"],
            ["SaaS \u589e\u957f\u7248", "\u90ae\u4ef6 + \u5fae\u4fe1",
             "24\u5c0f\u65f6\u54cd\u5e94",
             "\u53cc\u5468\u72b6\u6001\u7535\u8bdd",
             "\u4e0a\u6d77\u5ba2\u6237\u7ecf\u7406"],
            ["SaaS \u89c4\u6a21\u7248", "\u90ae\u4ef6 + \u5fae\u4fe1 + \u7535\u8bdd",
             "\u5f53\u5929\u54cd\u5e94",
             "\u6bcf\u5468\u72b6\u6001\u7535\u8bdd",
             "\u4e13\u5c5e\u5ba2\u6237\u7ecf\u7406"],
            ["\u4e13\u4e1aPM", "\u76f4\u63a5\u8054\u7cfbPMP",
             "4\u5c0f\u65f6\u54cd\u5e94",
             "\u6bcf\u5468\u7ad9\u4f1a + \u6708\u5ea6\u95e8\u5ba1\u67e5",
             "\u7f8e\u56fdPMP + \u4e0a\u6d77AM"],
            ["\u4f01\u4e1a\u7248", "\u76f4\u63a5PMP + \u9ad8\u7ba1",
             "2\u5c0f\u65f6\u54cd\u5e94(\u5de5\u4f5c\u65f6\u95f4)",
             "\u6bcf\u5468\u7ad9\u4f1a + \u53cc\u5468\u9ad8\u7ba1\u7b80\u62a5",
             "\u7f8e\u56fdPMP + \u4e0a\u6d77AM + \u9ad8\u7ba1\u8d5e\u52a9\u4eba"],
        ],
        col_widths=[28, 30, 28, 40, 64],
        header=["\u5c42\u7ea7", "\u6e20\u9053", "\u54cd\u5e94SLA", "\u62a5\u544a\u8282\u594f", "\u5206\u914d\u56e2\u961f"],
    )

    pdf.body("\u5ba2\u6237\u7ecf\u7406\u804c\u8d23\uff1a")
    pdf.bullet("\u62e5\u6709\u5ba2\u6237\u5173\u7cfb -- \u6240\u6709\u975e\u6280\u672f\u95ee\u9898\u7684\u7b2c\u4e00\u8054\u7cfb\u4eba",
               "\u5173\u7cfb\uff1a")
    pdf.bullet("\u5b9a\u671f\u53d1\u9001\u9879\u76ee\u91cc\u7a0b\u7891\u3001\u95e8\u51b3\u7b56\u548c\u9884\u7b97\u71c3\u70e7\u7684\u72b6\u6001\u66f4\u65b0",
               "\u62a5\u544a\uff1a")
    pdf.bullet("\u534f\u8c03\u5165\u804c\uff1aControl Tower\u8bbe\u7f6e\u3001\u56e2\u961f\u8bbf\u95ee\u3001\u6a21\u677f\u9009\u62e9",
               "\u5165\u804c\uff1a")
    pdf.bullet("\u76d1\u63a7\u5ba2\u6237\u6ee1\u610f\u5ea6\uff0c\u5411\u9500\u552e\u9886\u5bfc\u5c42\u6807\u8bb0\u6d41\u5931\u98ce\u9669",
               "\u7559\u5b58\uff1a")
    pdf.bullet("\u8bc6\u522b\u8ffd\u52a0\u9500\u552e\u673a\u4f1a\uff08\u5c42\u7ea7\u5347\u7ea7\u3001\u989d\u5916\u5668\u68b0\u6a21\u5757\u3001\u7f8e\u56fd\u5b9e\u4f53\u7ec4\u5efa\uff09",
               "\u8ffd\u52a0\u9500\u552e\uff1a")
    pdf.bullet("\u4e3a\u589e\u957f\u7248\u53ca\u4ee5\u4e0a\u5ba2\u6237\u5b89\u6392\u5b63\u5ea6\u4e1a\u52a1\u56de\u987e(QBR)",
               "QBR\uff1a")

    # ── 5. 安全与数据保护 ──
    pdf.section("5", "\u5b89\u5168\u4e0e\u6570\u636e\u4fdd\u62a4 -- \u8bdd\u672f\u8981\u70b9")
    pdf.body(
        "\u4e2d\u56fd\u5ba2\u6237\u4f1a\u8be2\u95ee\u6570\u636e\u5b89\u5168\u3002"
        "\u4ee5\u4e0b\u662f\u53ef\u4ee5\u81ea\u4fe1\u5206\u4eab\u7684\u4e8b\u5b9e\uff1a"
    )

    pdf.key_value_row("\u6570\u636e\u4f4d\u7f6e",
                      "\u6240\u6709\u9879\u76ee\u6570\u636e\u5b58\u50a8\u5728\u7f8e\u56fd"
                      "\uff08Supabase\u4e91\u57fa\u7840\u8bbe\u65bd\uff0c\u7f8e\u56fd\u533a\u57df\uff09\u3002"
                      "\u6ca1\u6709\u6570\u636e\u5b58\u50a8\u5728\u4e2d\u56fd\u670d\u52a1\u5668\u4e0a\u3002", label_w=38)
    pdf.key_value_row("\u52a0\u5bc6",
                      "\u4f20\u8f93\u4e2d\u52a0\u5bc6\uff08TLS 1.2/1.3\uff09\u548c\u9759\u6001\u52a0\u5bc6"
                      "\uff08AES-256\uff09\u3002\u6240\u6709\u8fde\u63a5\u4f7f\u7528HTTPS -- HTTP\u81ea\u52a8"
                      "\u91cd\u5b9a\u5411\u3002", label_w=38)
    pdf.key_value_row("\u8bbf\u95ee\u63a7\u5236",
                      "\u884c\u7ea7\u5b89\u5168(RLS)\u5728\u6570\u636e\u5e93\u5c42\u7ea7\u5f3a\u5236\u6267\u884c\u3002"
                      "\u6bcf\u4e2a\u5ba2\u6237\u7684\u6570\u636e\u6309project_id\u9694\u79bb -- \u6ca1\u6709"
                      "\u8de8\u9879\u76ee\u53ef\u89c1\u6027\u3002", label_w=38)
    pdf.key_value_row("\u8fb9\u7f18\u5b89\u5168",
                      "HSTS\uff08\u9884\u52a0\u8f7d\uff09\u3001\u5185\u5bb9\u5b89\u5168\u7b56\u7565\u3001"
                      "X-Content-Type-Options: nosniff\u3001X-Frame-Options: SAMEORIGIN\u3001"
                      "\u4e25\u683cReferrer-Policy\u3001Permissions-Policy\u3002", label_w=38)
    pdf.key_value_row("\u8ba4\u8bc1",
                      "Supabase Auth\u4e0eAPI\u5bc6\u94a5\u5f3a\u5236\u3002\u670d\u52a1\u89d2\u8272\u5bc6\u94a5"
                      "\u4ec5\u670d\u52a1\u5668\u7aef -- \u6c38\u4e0d\u66b4\u9732\u7ed9\u6d4f\u89c8\u5668\u3002", label_w=38)
    pdf.key_value_row("\u5ba1\u8ba1\u8ddf\u8e2a",
                      "\u6bcf\u6b21\u66f4\u6539\uff08\u95e8\u51b3\u7b56\u3001\u6587\u6863\u72b6\u6001\u3001"
                      "\u98ce\u9669\u66f4\u65b0\u3001\u91cc\u7a0b\u7891\u53d8\u66f4\uff09\u5747\u8bb0\u5f55"
                      "\u65f6\u95f4\u6233\u3001\u7528\u6237\u3001\u65e7\u503c\u548c\u65b0\u503c\u3002"
                      "\u4e0d\u53ef\u53d8 -- \u5ba2\u6237\u7528\u6237\u65e0\u6cd5\u5220\u9664\u3002", label_w=38)
    pdf.key_value_row("21 CFR Part 11",
                      "\u6211\u4eec\u7684\u5ba1\u8ba1\u8ddf\u8e2a\u548c\u6587\u6863\u63a7\u5236\u6ee1\u8db3"
                      "\u7535\u5b50\u8bb0\u5f55/\u7535\u5b50\u7b7e\u540d\u8981\u6c42\u3002\u8bb0\u5f55\u4fdd\u7559"
                      "\u81f3\u5668\u68b0\u5bff\u547d\u671f+2\u5e74\u3002", label_w=38)
    pdf.key_value_row("\u6258\u7ba1",
                      "CloudFlare Pages\uff08\u9759\u6001\u8d44\u4ea7\uff09+ CloudFlare CDN\u3002"
                      "\u6570\u636e\u5e93\u5728Supabase\uff08AWS us-west-2\uff09\u3002"
                      "99.9%\u53ef\u7528\u6027SLA\u3002", label_w=38)
    pdf.key_value_row("SOC\u5408\u89c4",
                      "Supabase\u57fa\u7840\u8bbe\u65bd\u901a\u8fc7SOC 2 Type II\u8ba4\u8bc1\u3002"
                      "CloudFlare\u7ef4\u62a4SOC 2 Type II\u548cISO 27001\u3002", label_w=38)

    pdf.callout_box(
        "\u5982\u88ab\u95ee\u53ca\u4e2d\u56fd\u6570\u636e\u6cd5\uff1a\u6211\u4eec\u7684\u670d\u52a1\u5668\u5728"
        "\u7f8e\u56fd\uff0c\u4e0d\u5728\u4e2d\u56fd\u3002\u8fd9\u662f\u6709\u610f\u4e3a\u4e4b\u7684 -- FDA\u8981\u6c42"
        "\u8bb0\u5f55\u53ef\u4f9b\u7f8e\u56fd\u68c0\u67e5\u5458\u8bbf\u95ee\u3002\u6570\u636e\u4e0d\u7ecf\u8fc7"
        "\u4e2d\u56fd\u670d\u52a1\u5668\u3002Control Tower\u901a\u8fc7\u6807\u51c6HTTPS\u8bbf\u95ee\uff0c"
        "\u5982\u540c\u4efb\u4f55\u5176\u4ed6\u7f51\u7ad9\u3002"
    )

    # ── 6. Control Tower 演示脚本 ──
    pdf.section("6", "Control Tower -- \u6f14\u793a\u811a\u672c")
    pdf.body(
        "\u7ed9\u5ba2\u6237\u73b0\u573a\u6f14\u793a\u65f6\uff0c\u6309\u6b64\u987a\u5e8f\u8fdb\u884c\u3002"
        "\u4fdd\u630120\u5206\u949f\u4ee5\u5185\u3002\u4e13\u6ce8\u4e8e\u5bf9\u5ba2\u6237\u91cd\u8981\u7684"
        "\u5185\u5bb9\uff1a"
    )

    pdf.bullet("\u4ece\u53cc\u8f68\u89c6\u56fe\u5f00\u59cb\uff1a\u201c\u8fd9\u662f\u60a8\u7684\u9879\u76ee"
               "\u4e00\u89c8 -- \u6280\u672f\u91cc\u7a0b\u7891\u5728\u4e0a\uff0c\u6cd5\u89c4\u91cc\u7a0b\u7891"
               "\u5728\u4e0b\uff0c\u5168\u90e8\u5728\u4e00\u4e2a\u5730\u65b9\u3002\u201d",
               "1. \u53cc\u8f68 (2\u5206\u949f)\uff1a")
    pdf.bullet("\u5c55\u793a\u95e8\u7cfb\u7edf\uff1a\u201c\u8fd9\u4e9b\u662f\u60a8\u7684\u901a\u884c/"
               "\u4e0d\u901a\u884c\u51b3\u7b56\u68c0\u67e5\u70b9\u3002\u6211\u4eec\u7684PMP\u5728\u6bcf\u4e2a"
               "\u95e8\u5ba1\u67e5\u8bc1\u636e\u5e76\u505a\u51fa\u51b3\u5b9a\u3002\u201d",
               "2. \u95e8 (2\u5206\u949f)\uff1a")
    pdf.bullet("\u5c55\u793a\u98ce\u9669\u4eea\u8868\u677f\uff1a\u201c\u6bcf\u4e2a\u98ce\u9669\u6309"
               "ISO 14971\u8ddf\u8e2a\uff0c\u5305\u542b\u4e25\u91cd\u6027\u3001\u6982\u7387\u3001\u63a7\u5236"
               "\u548c\u7f13\u89e3\u72b6\u6001\u3002\u201d",
               "3. \u98ce\u9669 (1\u5206\u949f)\uff1a")
    pdf.bullet("\u5c55\u793a\u9884\u7b97\u9009\u9879\u5361\uff1a\u201c\u6bcf\u4e2a\u6210\u672c\u7c7b\u522b"
               "\u7684\u8ba1\u5212\u4e0e\u5b9e\u9645\u3002\u6ca1\u6709\u60ca\u559c\u3002\u201d",
               "4. \u9884\u7b97 (1\u5206\u949f)\uff1a")
    pdf.bullet("\u5207\u6362\u5230\u4e2d\u6587\uff1a\u201c\u4e00\u5207\u90fd\u652f\u6301\u53cc\u8bed -- "
               "\u4e00\u952e\u5207\u6362\u3002\u60a8\u5728\u4e2d\u56fd\u7684\u56e2\u961f\u770b\u4e2d\u6587\uff0c"
               "\u6211\u4eec\u770b\u82f1\u6587\u3002\u201d",
               "5. \u8bed\u8a00\u5207\u6362 (30\u79d2)\uff1a")
    pdf.bullet("\u5c55\u793a\u6587\u6863\u63a7\u5236\uff1a\u201c\u6bcf\u4e2a\u6587\u6863\u7248\u672c"
               "\u8ddf\u8e2a -- \u8349\u7a3f\u3001\u5ba1\u67e5\u4e2d\u3001\u5df2\u6279\u51c6\u3001\u751f\u6548\u3002"
               "\u5b8c\u6574\u4fee\u8ba2\u5386\u53f2\u3002\u201d",
               "6. \u6587\u6863 (2\u5206\u949f)\uff1a")
    pdf.bullet("\u5c55\u793a\u5668\u68b0\u6a21\u677f\uff1a\u201c\u9009\u62e9\u60a8\u7684\u5668\u68b0\u7c7b\u522b\uff0c"
               "\u6211\u4eec\u81ea\u52a8\u914d\u7f6e\u6807\u51c6\u3001\u98ce\u9669\u3001\u9884\u7b97\u548c\u65f6\u95f4\u7ebf\u3002\u201d",
               "7. \u6a21\u677f (2\u5206\u949f)\uff1a")
    pdf.bullet("\u6253\u5f00\u5728\u7ebc\u6f14\u793a control-tower-bmx.pages.dev \u8ba9\u5ba2\u6237"
               "\u81ea\u5df1\u70b9\u51fb\u63a2\u7d22\u3002",
               "8. \u52a8\u624b\u4f53\u9a8c (5\u5206\u949f)\uff1a")

    pdf.callout_box(
        "\u6f14\u793a\u63d0\u793a\uff1a\u603b\u662f\u5148\u95ee\u201c\u60a8\u5728\u505a\u4ec0\u4e48\u7c7b\u578b"
        "\u7684\u5668\u68b0\uff1f\u201d\u7136\u540e\u5728\u6f14\u793a\u4e2d\u9009\u62e9\u4ed6\u4eec\u7684\u5668\u68b0"
        "\u6a21\u677f\uff0c\u8ba9\u4ed6\u4eec\u770b\u5230\u81ea\u5df1\u7c7b\u522b\u7684\u771f\u5b9e\u6570\u636e\u3002"
    )

    # ── 7. 常见客户问题与答案 ──
    pdf.section("7", "\u5e38\u89c1\u5ba2\u6237\u95ee\u9898 -- \u51c6\u5907\u597d\u7684\u7b54\u6848")
    pdf.body(
        "\u8bb0\u4f4f\u8fd9\u4e9b\u7b54\u6848\u3002\u5ba2\u6237\u51e0\u4e4e\u5728\u6bcf\u6b21\u4f1a\u8bae"
        "\u4e2d\u90fd\u4f1a\u95ee\u8fd9\u4e9b\u95ee\u9898\uff1a"
    )

    qa_cn = [
        ("510(k)\u9700\u8981\u591a\u957f\u65f6\u95f4\uff1f",
         "\u7aef\u5230\u7aef9-18\u4e2a\u6708\uff0c\u53d6\u51b3\u4e8e\u5668\u68b0\u590d\u6742\u6027\u3001"
         "\u6d4b\u8bd5\u8981\u6c42\u548c\u4fe1\u606f\u63d0\u4f9b\u901f\u5ea6\u3002\u63d0\u4ea4\u540eFDA"
         "\u5ba1\u67e5\u5355\u72ec\u9700\u89813-6\u4e2a\u6708\u3002"),
        ("\u8d39\u7528\u662f\u591a\u5c11\uff1f",
         "\u6bcf\u4e2a\u5668\u68b0\u6a21\u5757\u603b\u8ba1$130K-$320K\u3002\u5305\u62ec\u6d4b\u8bd5\u8d39"
         "($75K-$185K)\u3001\u9879\u76ee\u7ba1\u7406($10-25K/\u6708)\u3001FDA\u7528\u6237\u8d39"
         "($6.5K-$26K)\u548c\u8ba4\u8bc1($15-30K)\u3002\u521d\u59cb\u6cd5\u89c4\u9014\u5f84\u8bc4\u4f30"
         "\u540e\u63d0\u4f9b\u8be6\u7ec6\u6210\u672c\u4f30\u7b97\u3002"),
        ("\u80fd\u4fdd\u8bc1FDA\u6e05\u9664\u5417\uff1f",
         "\u6ca1\u6709\u4eba\u80fd\u4fdd\u8bc1FDA\u6e05\u9664 -- \u8fd9\u6837\u627f\u8bfa\u662f\u8fdd\u6cd5\u7684\u3002"
         "\u6211\u4eec\u4fdd\u8bc1\u4e13\u4e1a\u7ba1\u7406\u7684\u63d0\u4ea4\uff0c\u6700\u5927\u9650\u5ea6"
         "\u63d0\u9ad8\u6e05\u9664\u6982\u7387\u3002\u6211\u4eec\u7684\u95e8\u5ba1\u67e5\u7ed3\u6784\u5728"
         "\u95ee\u9898\u5230\u8fbeFDA\u524d\u5c31\u53d1\u73b0\u5b83\u4eec\u3002"),
        ("\u6211\u4eec\u9700\u8981\u7f8e\u56fd\u516c\u53f8\u5417\uff1f",
         "\u9700\u8981\u7f8e\u56fd\u4ee3\u7406\u4eba\uff08\u6240\u6709\u5916\u56fd\u5236\u9020\u5546\u5fc5\u9700\uff09\u3002"
         "\u5982\u679c\u8ba1\u5212\u52df\u96c6\u7f8e\u56fd\u6295\u8d44\u6216\u76f4\u63a5\u9500\u552e\uff0c"
         "\u5efa\u8bae\u6210\u7acb\u7279\u62c9\u534eC-Corp\u3002\u7f8e\u56fd\u4ee3\u7406\u4eba\u5df2\u5305\u542b"
         "\u5728\u4e13\u4e1a/\u4f01\u4e1a\u7248\u5c42\u7ea7\u4e2d\uff0c\u5b9e\u4f53\u7ec4\u5efa\u4e3a"
         "\u9644\u52a0\u670d\u52a1($2K-5K)\u3002"),
        ("\u6211\u4eec\u7684\u6570\u636e\u5b89\u5168\u5417\uff1f",
         "\u6240\u6709\u6570\u636e\u5b58\u50a8\u5728\u7f8e\u56fd\u670d\u52a1\u5668\uff08SOC 2 Type II"
         "\u8ba4\u8bc1\u57fa\u7840\u8bbe\u65bd\uff09\uff0c\u4f20\u8f93\u4e2d\u548c\u9759\u6001\u52a0\u5bc6\u3002"
         "\u6bcf\u4e2a\u5ba2\u6237\u6570\u636e\u9694\u79bb -- \u5176\u4ed6\u5ba2\u6237\u770b\u4e0d\u5230"
         "\u60a8\u7684\u4fe1\u606f\u3002\u5ba1\u8ba1\u8ddf\u8e2a\u4e0d\u53ef\u53d8\uff0c\u7b26\u5408"
         "21 CFR Part 11\u8981\u6c42\u3002"),
        ("\u5982\u679c\u6211\u4eec\u5df2\u7ecf\u6709\u6cd5\u89c4\u987e\u95ee\u4e86\u5462\uff1f",
         "\u6211\u4eec\u8865\u5145\u73b0\u6709\u987e\u95ee -- \u6211\u4eec\u662f\u9879\u76ee\u7ecf\u7406\uff0c"
         "\u4e0d\u4ec5\u4ec5\u662f\u6cd5\u89c4\u987e\u95ee\u3002Control Tower\u5e73\u53f0\u4fdd\u6301"
         "\u6240\u6709\u4eba\u4e00\u81f4\uff1a\u60a8\u7684\u987e\u95ee\u3001\u5de5\u7a0b\u56e2\u961f\u3001"
         "QA\u56e2\u961f\u548c\u6211\u4eec\u3002\u8bb8\u591a\u5ba2\u6237\u4fdd\u7559\u4ed6\u4eec\u7684"
         "\u6cd5\u89c4\u987e\u95ee\u5e76\u6dfb\u52a0\u6211\u4eec\u8fdb\u884c\u9879\u76ee\u6267\u884c\u3002"),
        ("\u53ef\u4ee5\u4ece\u6700\u4fbf\u5b9c\u7684\u65b9\u6848\u5f00\u59cb\u5417\uff1f",
         "\u5f53\u7136\u53ef\u4ee5\u3002\u4ece$500/\u6708\u7684\u5165\u95e8\u7248\u5f00\u59cb\u63a2\u7d22"
         "\u5e73\u53f0\u3002\u53ef\u4ee5\u968f\u65f6\u5347\u7ea7\uff0c\u6240\u6709\u6570\u636e\u4fdd\u7559\u3002"
         "\u5927\u591a\u6570\u5ba2\u6237\u4ece\u5165\u95e8\u7248\u6216\u589e\u957f\u7248\u5f00\u59cb\uff0c"
         "\u9879\u76ee\u52a0\u901f\u65f6\u5347\u7ea7\u5230\u89c4\u6a21\u7248\u6216\u4e13\u4e1aPM\u3002"),
        ("\u652f\u6301\u6211\u4eec\u7684\u7279\u5b9a\u5668\u68b0\u7c7b\u578b\u5417\uff1f",
         "\u67097\u4e2a\u9884\u5efa\u6a21\u677f\u8986\u76d6\u6700\u5e38\u89c1\u7684510(k)\u5668\u68b0\u7c7b\u522b\uff1a"
         "\u547c\u5438\u3001\u5fc3\u8840\u7ba1\u3001\u9aa8\u79d1\u3001IVD\u3001\u5f71\u50cf\u3001\u5eb7\u590d\u548cSaMD\u3002"
         "\u5982\u679c\u60a8\u7684\u5668\u68b0\u4e0d\u5c5e\u4e8e\u8fd9\u4e9b\u7c7b\u522b\uff0c\u6211\u4eec"
         "\u914d\u7f6e\u81ea\u5b9a\u4e49\u8bbe\u7f6e\u3002"),
        ("\u8c01\u7ba1\u7406\u6211\u4eec\u7684\u9879\u76ee\uff1f",
         "Lon Dailey -- \u7f8e\u56fd\u516c\u6c11\uff0c\u65af\u5766\u798f\u5927\u5b66SCPM\u8ba4\u8bc1"
         "PMP\u3002\u4ed6\u76f4\u63a5\u7ba1\u7406\u6240\u6709FDA\u6c9f\u901a\u3001\u95e8\u51b3\u7b56\u548c"
         "\u9879\u76ee\u6267\u884c\u3002\u60a8\u7684\u4e0a\u6d77\u5ba2\u6237\u7ecf\u7406\u7528\u4e2d\u6587"
         "\u5904\u7406\u65e5\u5e38\u5ba2\u6237\u6c9f\u901a\u3002"),
        ("FDA\u6e05\u9664\u540e\u600e\u4e48\u529e\uff1f",
         "\u6211\u4eec\u5e2e\u52a9\u673a\u6784\u6ce8\u518c\u3001\u5668\u68b0\u5217\u540d\u3001\u6807\u7b7e\u5408\u89c4"
         "\u548c\u4e0a\u5e02\u540e\u76d1\u7763\u7cfb\u7edf\u8bbe\u7f6e\u3002\u8bb8\u591a\u5ba2\u6237\u4fdd\u7559"
         "Control Tower\u8ba2\u9605\u7528\u4e8e\u6301\u7eed\u5408\u89c4\u7ba1\u7406\u3002"),
        ("\u5982\u4f55\u4e0e\u56e2\u961f\u6c9f\u901a\uff1f",
         "\u5fae\u4fe1\u7528\u4e8e\u4e0e\u4e0a\u6d77\u56e2\u961f\u65e5\u5e38\u6c9f\u901a\u3002\u90ae\u4ef6"
         "\u7528\u4e8e\u6b63\u5f0f\u901a\u4fe1\u3002Control Tower\u6d88\u606f\u677f\u7528\u4e8e\u9879\u76ee"
         "\u76f8\u5173\u8ba8\u8bba\uff08\u6240\u6709\u6d88\u606f\u90fd\u6709\u8bb0\u5f55\u548c\u53ef\u641c\u7d22\uff09\u3002"
         "\u589e\u957f\u7248\u53ca\u4ee5\u4e0a\u7684\u6bcf\u5468\u89c6\u9891\u7535\u8bdd\u3002"),
        ("\u5982\u679cFDA\u63d0\u51fa\u989d\u5916\u95ee\u9898\u600e\u4e48\u529e\uff1f",
         "\u8fd9\u662f\u6b63\u5e38\u7684 -- FDA\u5bf9\u7ea640-50%\u7684510(k)\u63d0\u4ea4\u53d1\u51fa"
         "\u8865\u5145\u4fe1\u606f(AI)\u8bf7\u6c42\u3002\u6211\u4eec\u7ba1\u7406\u56de\u590d\u8fc7\u7a0b\uff1a"
         "\u8d77\u8349\u7b54\u6848\u3001\u4e0e\u60a8\u7684\u5de5\u7a0b\u56e2\u961f\u534f\u8c03\u6280\u672f"
         "\u6570\u636e\u3001\u63d0\u4ea4\u56de\u590d\u3002\u6bcf\u4e2aAI\u8bf7\u6c42\u589e\u52a060-180\u5929\u3002"),
    ]

    for q, a in qa_cn:
        pdf.bullet(a, f"\u95ee\uff1a{q}  \u7b54\uff1a")
        pdf.ln(1)

    # ── 8. \u5ba2\u6237\u5165\u804c\u6e05\u5355 ──
    pdf.section("8", "\u5ba2\u6237\u5165\u804c\u6e05\u5355\uff08\u5185\u90e8\uff09")
    pdf.body(
        "\u5ba2\u6237\u7b7e\u7ea6\u540e\uff0c\u6309\u6b64\u6e05\u5355\u5b8c\u6210\u8bbe\u7f6e\u3002"
        "\u76ee\u6807\uff1a5\u4e2a\u5de5\u4f5c\u65e5\u5185\u5b8c\u6210\u3002"
    )

    pdf.bullet("\u5728Supabase\u4e2d\u521b\u5efa\u9879\u76ee\uff1a\u8fd0\u884c onboard_client.sh <project_id> <tier> <seats>",
               "\u7b2c1\u5929 -- \u914d\u7f6e\uff1a")
    pdf.bullet("\u53d1\u9001\u5ba2\u6237\u4eea\u8868\u677fURL\uff1acontrol-tower-bmx.pages.dev/?project=<id>",
               "\u7b2c1\u5929 -- \u8bbf\u95ee\uff1a")
    pdf.bullet("\u5b89\u624260\u5206\u949f\u542f\u52a8\u7535\u8bdd\uff08\u4e0a\u6d77AM + \u5ba2\u6237\u56e2\u961f\uff09",
               "\u7b2c1\u5929 -- \u542f\u52a8\uff1a")
    pdf.bullet("\u5f15\u5bfc\u5ba2\u6237\u5b8c\u6210\u8bbe\u7f6e\u5411\u5bfc\uff1a\u8bed\u8a00\u3001\u6a21\u677f\u9009\u62e9\u3001"
               "\u56e2\u961f\u6210\u5458\u3001\u9884\u7b97\u3001\u4f9b\u5e94\u5546\u3001\u6587\u6863",
               "\u7b2c2\u5929 -- \u5411\u5bfc\uff1a")
    pdf.bullet("\u9a8c\u8bc1\u6240\u6709\u56e2\u961f\u6210\u5458\u5747\u53ef\u8bbf\u95ee\u4eea\u8868\u677f",
               "\u7b2c2\u5929 -- \u8bbf\u95ee\u68c0\u67e5\uff1a")
    pdf.bullet("\u6536\u96c6\u5668\u68b0\u63cf\u8ff0\u3001\u5bf9\u6bd4\u5668\u68b0\u5019\u9009\u548c\u73b0\u6709\u6d4b\u8bd5\u62a5\u544a",
               "\u7b2c3\u5929 -- \u6587\u6863\uff1a")
    pdf.bullet("\u5206\u914d\u7f8e\u56fdPMP\u5e76\u5b89\u6392\u7b2c\u4e00\u6b21\u6bcf\u5468\u7ad9\u4f1a"
               "\uff08\u4ec5\u4e13\u4e1a/\u4f01\u4e1a\u7248\uff09",
               "\u7b2c3\u5929 -- PMP\u5206\u914d\uff1a")
    pdf.bullet("\u53d1\u9001\u6b22\u8fce\u90ae\u4ef6\uff1a\u4eea\u8868\u677fURL\u3001\u652f\u6301\u8054\u7cfb\u4eba\u3001"
               "\u5fae\u4fe1\u7fa4\u9080\u8bf7\u3001\u7b2c\u4e00\u4efd\u72b6\u6001\u62a5\u544a\u6a21\u677f",
               "\u7b2c5\u5929 -- \u6b22\u8fce\u5305\uff1a")

    # ── 9. 竞争差异化 ──
    pdf.section("9", "\u6211\u4eec\u7684\u4e0d\u540c\u4e4b\u5904 -- \u7ade\u4e89\u8bdd\u672f")

    pdf.tier_table(
        rows=[
            ["\u4f20\u7edfRA\u516c\u53f8",
             "\u4ec5\u6cd5\u89c4\u6587\u6863\uff0c\u65e0PM\uff0c\u65e0\u4eea\u8868\u677f\uff0c"
             "\u9ad8\u5c0f\u65f6\u8d39\u7387($300-500/\u5c0f\u65f6)\uff0c\u4ec5\u82f1\u6587\u6c9f\u901a"],
            ["\u4e2d\u56fdRA\u987e\u95ee",
             "\u66f4\u4fbf\u5b9c\u4f46\u65e0\u7f8e\u56fd\u5b58\u5728\uff0c\u65e0\u6cd5\u62c5\u4efb\u7f8e\u56fd"
             "\u4ee3\u7406\u4eba\uff0cFDA\u4e92\u52a8\u7ecf\u9a8c\u6709\u9650\uff0c\u65e0\u6280\u672f\u5e73\u53f0"],
            ["\u5927\u578b\u54a8\u8be2\u516c\u53f8",
             "\u6602\u8d35($500K+)\u3001\u7f13\u6162\u3001\u901a\u624d\u56e2\u961f\u65e0\u533b\u7597\u5668\u68b0"
             "\u4e13\u4e1a\u5316"],
            ["510kBridge",
             "\u7f8e\u56fdPMP + \u53cc\u8bed\u4e0a\u6d77\u56e2\u961f + 16\u6a21\u5757\u5b9e\u65f6\u4eea\u8868\u677f"
             " + 7\u4e2a\u5668\u68b0\u6a21\u677f + \u7f8e\u56fd\u4ee3\u7406\u4eba -- \u4e00\u4f53\u5316\u670d\u52a1"],
        ],
        col_widths=[40, 150],
        header=["\u7ade\u4e89\u5bf9\u624b\u7c7b\u578b", "\u6211\u4eec\u7684\u4f18\u52bf"],
    )

    # ── 10. 会后下一步 ──
    pdf.section("10", "\u9500\u552e\u6d41\u7a0b -- \u4f1a\u540e\u4e0b\u4e00\u6b65")
    pdf.body("\u6bcf\u6b21\u5ba2\u6237\u4f1a\u8bae\u540e\u6309\u6b64\u987a\u5e8f\u6267\u884c\uff1a")
    pdf.bullet("\u57282\u5c0f\u65f6\u5185\u53d1\u9001\u8ddf\u8fdb\u90ae\u4ef6\uff0c\u603b\u7ed3\u5173\u952e\u8ba8\u8bba\u70b9", "1. ")
    pdf.bullet("\u5206\u4eabControl Tower\u6f14\u793a\u94fe\u63a5\uff1acontrol-tower-bmx.pages.dev", "2. ")
    pdf.bullet("\u5982\u679c\u5ba2\u6237\u8868\u8fbe\u4e86\u5174\u8da3\uff0c5\u4e2a\u5de5\u4f5c\u65e5\u5185\u53d1\u9001"
               "\u5b9a\u5236\u6cd5\u89c4\u9014\u5f84\u8bc4\u4f30\uff08\u4e0e\u7f8e\u56fdPMP\u534f\u8c03\uff09", "3. ")
    pdf.bullet("\u57281\u5468\u5185\u5b89\u6392\u8ddf\u8fdb\u7535\u8bdd\u5ba1\u67e5\u8bc4\u4f30", "4. ")
    pdf.bullet("\u51c6\u5907\u6b63\u5f0f\u63d0\u6848\uff1a\u63a8\u8350\u5c42\u7ea7\u3001\u4f30\u8ba1\u6210\u672c\u3001\u65f6\u95f4\u7ebf", "5. ")
    pdf.bullet("\u5b8c\u6210\u4ea4\u6613 -- \u7b7e\u7f72\u670d\u52a1\u534f\u8bae\u5e76\u542f\u52a8\u5165\u804c", "6. ")

    pdf.ln(3)
    pdf.body("\u5185\u90e8\u8054\u7cfb\u4eba\uff1a")
    pdf.key_value_row("\u7f8e\u56fdPMP\uff1a", "Lon Dailey  |  info@510kbridge.com", label_w=32)
    pdf.key_value_row("\u4e0a\u6d77\u529e\u516c\u5ba4\uff1a",
                      "510kBridge Consulting (\u4e0a\u6d77) Co., Ltd.", label_w=32)
    pdf.key_value_row("\u6f14\u793aURL\uff1a", "control-tower-bmx.pages.dev", label_w=32)
    pdf.key_value_row("\u5165\u804c\uff1a",
                      "\u8fd0\u884c onboard_client.sh\uff08\u89c1\u7b2c8\u8282\uff09", label_w=32)

    path = os.path.join(OUT, "Sales_Pitch_CN.pdf")
    pdf.output(path)
    print(f"  [CN] {path}  ({os.path.getsize(path)//1024} KB)")
    return path


# ═══════════════════════════════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("Generating Sales Pitch PDFs...")
    _build_en()
    _build_cn()
    print("Done.")
