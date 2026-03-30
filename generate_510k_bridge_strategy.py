#!/usr/bin/env python3
"""
Generate the 510kBridge 5-Year Business Strategy PDF.
Covers:
  - Pilot program in China market (Year 0-1)
  - EB-5 period with revenue from pilot clients, new clients,
    and WA State workforce programs (Years 1-2)
  - Post-green-card restructuring with bilingual US graduates (Year 3+)
  - Parent-sponsored on-the-job training program
  - 5-year financial projections
"""

import os
from datetime import date
from fpdf import FPDF

OUT_DIR = os.path.dirname(os.path.abspath(__file__))

NAVY = (10, 40, 100)
TEXT = (40, 40, 45)
GRAY = (120, 120, 130)
WHITE = (255, 255, 255)
LIGHT_BG = (245, 247, 252)
GREEN = (20, 120, 60)
RED = (170, 40, 40)
ACCENT = (0, 100, 180)
GOLD = (160, 120, 20)

_MAP = str.maketrans({
    "\u2014": "--", "\u2013": "-", "\u2019": "'", "\u201c": '"', "\u201d": '"',
    "\u2018": "'", "\u2265": ">=", "\u2264": "<=", "\u00b5": "u", "\u00d7": "x",
    "\u2022": "-", "\u2026": "...", "\u00ae": "(R)",
})


def _a(s: str) -> str:
    return s.translate(_MAP)


class StrategyPDF(FPDF):

    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(*GRAY)
        self.cell(0, 5, _a("CONFIDENTIAL  |  510kBridge 5-Year Business Strategy"),
                  align="R")
        self.ln(7)

    def footer(self):
        self.set_y(-13)
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(*GRAY)
        self.cell(0, 5, f"Page {self.page_no()}/{{nb}}", align="C")

    def sec(self, title):
        if self.get_y() > self.h - 40:
            self.add_page()
        self.ln(3)
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(*NAVY)
        self.cell(0, 8, _a(title), new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(*NAVY)
        self.set_line_width(0.5)
        self.line(self.l_margin, self.get_y(),
                  self.w - self.r_margin, self.get_y())
        self.ln(4)

    def sub(self, title, color=NAVY):
        if self.get_y() > self.h - 30:
            self.add_page()
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(*color)
        self.cell(0, 7, _a(title), new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def sub2(self, title, color=ACCENT):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(*color)
        self.cell(0, 6, _a(title), new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def txt(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*TEXT)
        self.multi_cell(0, 5.5, _a(text), new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def green_txt(self, text):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(*GREEN)
        self.multi_cell(0, 5.5, _a(text), new_x="LMARGIN", new_y="NEXT")
        self.set_text_color(*TEXT)
        self.ln(2)

    def gold_txt(self, text):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(*GOLD)
        self.multi_cell(0, 5.5, _a(text), new_x="LMARGIN", new_y="NEXT")
        self.set_text_color(*TEXT)
        self.ln(2)

    def bullet(self, text, indent=6):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*TEXT)
        self.set_x(self.l_margin + indent)
        self.multi_cell(self.w - self.l_margin - self.r_margin - indent, 5.5,
                        _a(f"- {text}"), new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def bold_bullet(self, label, text, indent=6):
        self.set_x(self.l_margin + indent)
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(*TEXT)
        lw = self.get_string_width(_a(label)) + 1
        self.cell(lw, 5.5, _a(label))
        self.set_font("Helvetica", "", 10)
        self.multi_cell(0, 5.5, _a(text), new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def table(self, headers, rows, col_w, bold_last=False):
        needed = 7 + len(rows) * 6 + 10
        if self.get_y() + needed > self.h - 20:
            self.add_page()
        self.set_font("Helvetica", "B", 8.5)
        self.set_text_color(*WHITE)
        self.set_fill_color(*NAVY)
        for i, h in enumerate(headers):
            self.cell(col_w[i], 7, _a(h), border=1, fill=True, align="C")
        self.ln()
        self.set_text_color(*TEXT)
        for ri, row in enumerate(rows):
            is_last = bold_last and ri == len(rows) - 1
            self.set_font("Helvetica", "B" if is_last else "", 8.5)
            bg = (230, 235, 250) if is_last else (LIGHT_BG if ri % 2 == 0 else WHITE)
            self.set_fill_color(*bg)
            for ci, val in enumerate(row):
                align = "L" if ci == 0 else "C"
                self.cell(col_w[ci], 6, _a(val), border=1, fill=True, align=align)
            self.ln()
        self.ln(3)

    def phase_banner(self, label, color):
        if self.get_y() > self.h - 50:
            self.add_page()
        self.ln(2)
        w = self.w - self.l_margin - self.r_margin
        self.set_fill_color(*color)
        y = self.get_y()
        self.rect(self.l_margin, y, w, 8, style="DF")
        self.set_xy(self.l_margin + 3, y + 1)
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(*WHITE)
        self.cell(0, 6, _a(label))
        self.set_y(y + 11)


def build():
    pdf = StrategyPDF("P", "mm", "Letter")
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.set_margins(22, 18, 22)

    # ══════════════════════════════════════════════════════════════
    # COVER PAGE
    # ══════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.set_fill_color(*NAVY)
    pdf.rect(0, 0, pdf.w, 65, style="F")
    pdf.set_y(14)
    pdf.set_font("Helvetica", "B", 22)
    pdf.set_text_color(*WHITE)
    pdf.cell(0, 10, "510kBridge", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 7, "A Delaware Corporation  |  Camas, Washington",
             align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)
    pdf.set_draw_color(*WHITE)
    pdf.set_line_width(0.3)
    pdf.line(50, pdf.get_y(), pdf.w - 50, pdf.get_y())
    pdf.ln(3)
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 8, "5-Year Business Formation Strategy",
             align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "I", 10)
    pdf.cell(0, 6, "From China Pilot to US Market Leadership",
             align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)
    pdf.set_font("Helvetica", "", 9)
    today = date.today().strftime("%B %d, %Y")
    pdf.cell(0, 5, f"CONFIDENTIAL  |  Prepared {today}",
             align="C", new_x="LMARGIN", new_y="NEXT")

    pdf.set_text_color(*TEXT)
    pdf.ln(12)

    # Table of Contents
    pdf.sec("Table of Contents")
    toc = [
        "1.  Executive Summary",
        "2.  Company Formation & Legal Structure",
        "3.  Phase 1: China Pilot Program (Months 0-12)",
        "4.  Phase 2: EB-5 Period & US Operations (Months 12-30)",
        "5.  Phase 3: Post-Green Card Restructuring (Year 3)",
        "6.  Phase 4: Growth & Optimization (Years 4-5)",
        "7.  Revenue Model & Income Streams",
        "8.  WA State Workforce Development Programs",
        "9.  Bilingual Graduate Hiring & Parent Sponsorship",
        "10. 5-Year Financial Projections",
        "11. Organizational Structure Evolution",
        "12. Risk Analysis & Mitigation",
        "13. Key Milestones & Success Metrics",
    ]
    for item in toc:
        pdf.set_font("Helvetica", "", 10)
        pdf.cell(0, 5.5, _a(f"  {item}"), new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    # ══════════════════════════════════════════════════════════════
    # 1. EXECUTIVE SUMMARY
    # ══════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.sec("1. Executive Summary")

    pdf.txt(
        "510kBridge is a Delaware corporation registered in Camas, Washington -- a "
        "designated Targeted Employment Area (TEA) qualifying for the EB-5 reduced "
        "investment threshold of $800,000. The company helps Chinese medical device "
        "companies navigate the FDA 510(k) clearance process using a proprietary "
        "bilingual (EN/CN) project management platform called Control Tower."
    )

    pdf.txt(
        "This 5-year strategy outlines a phased approach to company formation, "
        "beginning with a pilot program in the China market to validate the business "
        "model, progressing through the EB-5 immigration period with diversified "
        "revenue streams, and culminating in a lean, high-capability US operation "
        "staffed by bilingual business and technology graduates."
    )

    pdf.green_txt(
        "Strategic Thesis: Test in China, prove in the US, scale with talent."
    )

    pdf.sub("Strategic Phases at a Glance")
    pdf.table(
        ["Phase", "Timeline", "Focus", "Headcount"],
        [
            ["1: China Pilot", "Months 0-12", "Market validation, client acquisition", "4-6"],
            ["2: EB-5 Operations", "Months 12-30", "US office, job creation, revenue growth", "10-13"],
            ["3: Restructuring", "Year 3", "Green cards issued, talent upgrade", "6-8"],
            ["4: Growth", "Years 4-5", "Scale, premium talent, profitability", "8-12"],
        ],
        [35, 30, 55, 28]
    )

    pdf.sub("Core Value Proposition")
    pdf.bullet("Bilingual (EN/CN) 510(k) project management platform (Control Tower)")
    pdf.bullet("End-to-end FDA regulatory consulting for Chinese medical device companies")
    pdf.bullet("US-based team with deep understanding of both FDA and NMPA processes")
    pdf.bullet("Proprietary SaaS platform with 16-tab dashboard, dual-track milestones, "
               "and automated regulatory workflows")

    # ══════════════════════════════════════════════════════════════
    # 2. COMPANY FORMATION & LEGAL STRUCTURE
    # ══════════════════════════════════════════════════════════════
    pdf.sec("2. Company Formation & Legal Structure")

    pdf.sub("Corporate Entity")
    pdf.bold_bullet("Entity: ", "510kBridge, Inc. -- Delaware C-Corporation")
    pdf.bold_bullet("Principal Office: ", "Camas, Washington (TEA-qualified)")
    pdf.bold_bullet("China Subsidiary: ", "510kBridge Consulting (Shanghai) Co., Ltd. (WFOE)")
    pdf.bold_bullet("Website: ", "510kbridge.com")

    pdf.sub("Why Delaware C-Corp")
    pdf.bullet("Court of Chancery -- specialized business law expertise")
    pdf.bullet("Venture capital investors expect Delaware incorporation")
    pdf.bullet("Flexible share classes (common, preferred, options) for team equity")
    pdf.bullet("No state tax on income earned outside Delaware")
    pdf.bullet("Standard structure for medtech and SaaS companies")

    pdf.sub("Why Camas, Washington")
    pdf.bullet("Designated Targeted Employment Area (TEA) -- EB-5 threshold: $800,000 "
               "vs. $1,050,000 standard")
    pdf.bullet("20 minutes from Portland International Airport")
    pdf.bullet("No state income tax in Washington -- significant advantage for salaries")
    pdf.bullet("Growing tech corridor with access to Portland talent pool")
    pdf.bullet("Lower cost of living than major metro areas; attractive for families")

    pdf.sub("EB-5 Investment Structure")
    pdf.txt(
        "Total EB-5 capital required: $800,000 (TEA rate). The investor files Form "
        "I-526E as the principal EB-5 investor. The company must create at least 10 "
        "full-time US jobs within two years. The investment is at-risk capital deployed "
        "directly into the operating company -- not a passive fund."
    )

    pdf.sub("Ownership Structure")
    pdf.table(
        ["Shareholder", "Class", "Role"],
        [
            ["EB-5 Investor", "Common (majority)", "COO / Investor"],
            ["CEO", "Preferred (limited voting)", "CEO (China ops, then US)"],
            ["Founder", "Common (founder equity)", "Principal Consultant"],
        ],
        [45, 50, 60]
    )

    pdf.sub("Dual-Entity Operating Model")
    pdf.txt(
        "510kBridge operates through two complementary entities. Understanding the "
        "revenue flow between them is critical to the EB-5 structure and daily "
        "operations:"
    )

    pdf.sub2("Why Two Entities Are Required")
    pdf.bullet("EB-5 capital ($800,000) must be deployed into a US commercial enterprise "
               "(8 CFR 204.6). The investment flows into 510kBridge, Inc. (Delaware C-Corp) "
               "and is spent on US operations, salaries, and job creation.")
    pdf.bullet("Chinese medical device clients expect to contract and pay in RMB through "
               "a local Chinese entity. Without the Shanghai WFOE, every client would need "
               "to wire USD internationally -- a major friction point that kills deals.")
    pdf.bullet("FDA requires US-based document storage and a US Agent for foreign "
               "manufacturers (21 CFR 820.180). Regulatory work must originate from the US entity.")
    pdf.bullet("The WFOE satisfies EB-1C multinational manager requirements for the CEO's "
               "eventual transfer to the US.")

    pdf.sub2("Revenue Flow: China to US")
    pdf.txt(
        "Clients contract with the Shanghai WFOE and pay in RMB. The WFOE retains a "
        "margin for local operations (sales team salaries, office, marketing) and "
        "transfers management fees / service fees upstream to the US parent via "
        "intercompany agreements. This is standard WFOE-to-parent transfer pricing "
        "and must comply with two frameworks:"
    )
    pdf.bold_bullet("China SAFE (State Administration of Foreign Exchange): ",
        "The WFOE must register with SAFE to remit profits or management fees to the "
        "US parent. Registration takes 2-4 weeks and requires proper documentation "
        "of the intercompany agreement and fee basis.")
    pdf.bold_bullet("OECD Transfer Pricing: ",
        "Intercompany fees must be at arm's length -- priced as if the two entities "
        "were unrelated parties. Common structures include a percentage-of-revenue "
        "management fee (15-25%) or cost-plus arrangement.")

    pdf.sub2("Tax Treatment")
    pdf.txt(
        "The US-China tax treaty (Article 5/7) prevents double taxation on the same "
        "income. The WFOE pays China corporate tax (25%) on its local margin. The US "
        "parent pays US corporate tax on repatriated profits with foreign tax credits "
        "for taxes already paid in China. A cross-border CPA experienced in US-China "
        "structures is essential (many available in the Portland/Vancouver area).")

    pdf.sub2("Operating Model Summary")
    pdf.table(
        ["Function", "US Parent (Camas, WA)", "Shanghai WFOE"],
        [
            ["EB-5 compliance", "Yes -- capital deployed here", "N/A"],
            ["FDA regulatory work", "US Agent, submissions, DHF storage", "Cannot perform"],
            ["Client sales", "Secondary (EN-speaking clients)", "Primary -- Mandarin team"],
            ["Banking", "USD business accounts", "RMB accounts, local invoicing"],
            ["Contracts", "US-law (FDA, labs, agents)", "CN-law (client contracts)"],
            ["Tax jurisdiction", "US federal + WA (no state income tax)", "China 25% corporate"],
            ["Job creation", "W-2 employees count for EB-5", "Does NOT count for EB-5"],
        ],
        [35, 60, 60]
    )

    # ══════════════════════════════════════════════════════════════
    # 3. PHASE 1: CHINA PILOT PROGRAM
    # ══════════════════════════════════════════════════════════════
    pdf.sec("3. Phase 1: China Pilot Program (Months 0-12)")

    pdf.phase_banner("PHASE 1: MARKET VALIDATION", ACCENT)

    pdf.sub("Objective")
    pdf.txt(
        "Test the viability of 510kBridge's service model with real Chinese medical "
        "device companies before committing full US operations. The pilot proves "
        "demand, refines pricing, trains the team, and generates reference clients "
        "that strengthen the EB-5 business plan."
    )

    pdf.sub("China Entity Setup")
    pdf.txt(
        "510kBridge establishes a Chinese subsidiary -- '510kBridge Consulting "
        "(Shanghai) Co., Ltd.' -- as a Wholly Foreign-Owned Enterprise (WFOE). "
        "This entity serves as the China-side business development and client "
        "services arm. It also satisfies the EB-1C multinational manager requirement "
        "for the CEO's eventual transfer to the US."
    )

    pdf.sub("Pilot Program Structure")
    pdf.bold_bullet("Target: ", "3-5 Chinese medical device companies seeking FDA 510(k) clearance")
    pdf.bold_bullet("Duration: ", "12 months, with option to extend")
    pdf.bold_bullet("Services: ", "Regulatory gap analysis, submission strategy, Control Tower "
                    "SaaS access, bilingual project management")
    pdf.bold_bullet("Pricing: ", "Discounted introductory rates to build case studies "
                    "(Professional tier at $8,000-$12,000/month)")
    pdf.bold_bullet("Deliverables: ", "Each client receives a regulatory roadmap, "
                    "Control Tower instance, and dedicated PM contact")

    pdf.sub("Target Client Profile")
    pdf.bullet("Chinese manufacturers with NMPA-cleared Class II devices (patient monitors, "
               "imaging systems, rehabilitation equipment, diagnostic tools, SaMD)")
    pdf.bullet("Companies with $5M+ annual revenue seeking US market expansion")
    pdf.bullet("Companies where the founder/CEO has expressed interest in US presence")
    pdf.bullet("Referrals from medical industry networks, biotech parks (Shenzhen, Suzhou, "
               "Hangzhou), and professional contacts")

    pdf.sub("Pilot Success Criteria")
    pdf.table(
        ["Metric", "Target", "Significance"],
        [
            ["Clients signed", "3-5", "Proves market demand"],
            ["Monthly revenue", "$30K-$60K", "Validates pricing model"],
            ["Client retention", ">80%", "Service quality validated"],
            ["NPS score", ">40", "Client satisfaction benchmark"],
            ["Referrals generated", "2+", "Organic growth signal"],
        ],
        [45, 35, 75]
    )

    pdf.sub("Pilot Team (China-Based)")
    pdf.table(
        ["Role", "Person", "Responsibility"],
        [
            ["CEO", "Lawrence Liu", "Client relationships, BD, investor pipeline"],
            ["General Manager", "Jialun Li", "Daily operations, medical content, QC"],
            ["Sr. Account Manager", "Chensy Li", "Client acquisition, marketing"],
            ["Principal Consultant", "Lon Dailey (remote)", "US regulatory, FDA strategy"],
        ],
        [45, 40, 72]
    )

    pdf.sub("Key Activities -- Months 0-12")
    pdf.table(
        ["Month", "Activity"],
        [
            ["0-2", "Register Shanghai WFOE; set up office; hire admin support"],
            ["1-3", "Launch outreach: biotech parks, trade shows, WeChat campaigns"],
            ["2-4", "Sign first 2 pilot clients; onboard onto Control Tower"],
            ["3-6", "Deliver first regulatory gap analyses and submission strategies"],
            ["4-8", "Sign clients 3-5; begin generating case study material"],
            ["6-12", "Refine pricing model based on pilot data; document lessons learned"],
            ["9-12", "Prepare EB-5 I-526E petition with pilot revenue/client data as evidence"],
        ],
        [20, 135]
    )

    # ══════════════════════════════════════════════════════════════
    # 4. PHASE 2: EB-5 PERIOD & US OPERATIONS
    # ══════════════════════════════════════════════════════════════
    pdf.sec("4. Phase 2: EB-5 Period & US Operations (Months 12-30)")

    pdf.phase_banner("PHASE 2: EB-5 JOB CREATION & REVENUE DIVERSIFICATION", GREEN)

    pdf.sub("Objective")
    pdf.txt(
        "With pilot program data validating the business model, the EB-5 investor "
        "files the I-526E petition and $800,000 is deployed into 510kBridge US "
        "operations. During the two-year conditional green card period, the company "
        "must create at least 10 full-time US jobs and demonstrate the capital is "
        "at risk in an active business."
    )

    pdf.sub("Three Revenue Streams")
    pdf.txt(
        "During the EB-5 period, 510kBridge generates income from three distinct sources:"
    )

    pdf.sub2("Stream 1: Pilot Program Clients (Continuing)")
    pdf.txt(
        "Clients acquired during the China pilot continue their engagements, now "
        "with enhanced US-side support. These are proven revenue sources with "
        "established relationships. Expected: 3-5 clients at $10,000-$20,000/month."
    )

    pdf.sub2("Stream 2: New Client Acquisition")
    pdf.txt(
        "With a US office, proven case studies, and a growing reputation, 510kBridge "
        "actively acquires new clients through referrals, WeChat marketing, trade "
        "shows (AdvaMed, RAPS, MD&M), and partnerships with US testing labs (UL, "
        "TUV, Intertek). Target: 3-5 new clients in Year 2."
    )

    pdf.sub2("Stream 3: Washington State Workforce Development Programs")
    pdf.txt(
        "510kBridge participates in Washington State employment and workforce "
        "development programs designed to reduce unemployment and provide job "
        "training. These programs create a dual benefit: they help the company "
        "meet EB-5 job creation requirements while accessing state funding to "
        "offset training and wage costs."
    )

    pdf.sub("WA State Workforce Programs (Detail)")
    pdf.txt(
        "Washington State offers several programs that align with 510kBridge's "
        "EB-5 job creation requirements and workforce development mission:"
    )

    pdf.bold_bullet("Job Skills Program (JSP): ",
        "State-funded customized training for new or existing employees. The "
        "Employment Security Department (ESD) partners with community colleges "
        "to provide training contracts. 510kBridge employees receive training in "
        "FDA regulatory processes, medical device terminology, and project "
        "management -- funded partially or fully by the state.")
    pdf.bold_bullet("On-the-Job Training (OJT): ",
        "WorkSource Washington reimburses employers up to 50-75% of wages during "
        "the training period (typically 3-6 months) for new hires who need skill "
        "development. 510kBridge hires entry-level workers and trains them in "
        "regulatory support, data entry, document control, and bilingual "
        "business communication.")
    pdf.bold_bullet("Worker Retraining Program: ",
        "Community and technical colleges provide tuition-free training for "
        "unemployed or underemployed workers. 510kBridge partners with Clark "
        "College (Camas/Vancouver) to create a pipeline of trained candidates.")
    pdf.bold_bullet("Work Opportunity Tax Credit (WOTC): ",
        "Federal tax credit for hiring individuals from targeted groups "
        "(veterans, long-term unemployed, SNAP recipients). Credits of "
        "$2,400-$9,600 per qualifying employee per year.")

    pdf.sub("US Office & Workforce Plan")
    pdf.txt(
        "The Camas office is designed as a combined workspace and training center. "
        "During the EB-5 period, the company maintains a workforce of 10+ full-time "
        "employees, with entry-level positions earning Washington State minimum wage "
        "($16.66/hr in 2026) plus benefits. The work environment combines productive "
        "business operations with structured education and skill-building."
    )

    pdf.sub("Work/Education Model")
    pdf.txt(
        "Employees split their time between client-facing work and structured "
        "learning. This model ensures genuine job creation (satisfying EB-5) while "
        "building a skilled workforce:"
    )
    pdf.bullet("Morning sessions: Client work -- document processing, data entry, "
               "Control Tower updates, basic regulatory research")
    pdf.bullet("Afternoon sessions: Education -- FDA regulatory fundamentals, "
               "medical device terminology, PMP methodology, business English/Chinese")
    pdf.bullet("Weekly: Guest speakers from regulatory affairs, immigration law, "
               "medical device industry")
    pdf.bullet("Monthly: Skill assessments and competency advancement")

    pdf.sub("EB-5 Staffing Plan (Months 12-30)")
    pdf.table(
        ["#", "Role", "Wage", "Status"],
        [
            ["1", "COO / Investor", "Salary", "EB-5 principal"],
            ["2", "Principal Consultant (PMP)", "Salary", "US citizen"],
            ["3", "Operations Manager", "Salary", "EB-5 derivative"],
            ["4", "Regulatory Support Specialist", "$16.66/hr", "WA hire"],
            ["5", "Document Control Clerk", "$16.66/hr", "WA hire"],
            ["6", "Data Entry / Admin Assistant", "$16.66/hr", "WA hire"],
            ["7", "Marketing Assistant (bilingual)", "$16.66/hr", "WA hire"],
            ["8", "Office Administrator", "$16.66/hr", "WA hire"],
            ["9", "Training Coordinator", "$16.66/hr", "WA hire / OJT"],
            ["10", "Business Development Trainee", "$16.66/hr", "WA hire / OJT"],
            ["11", "Jr. Project Coordinator", "$16.66/hr", "WA hire / OJT"],
            ["12", "Accounting Clerk", "$16.66/hr", "WA hire"],
            ["13", "IT / Platform Support", "$16.66/hr", "WA hire"],
        ],
        [10, 60, 30, 50]
    )

    pdf.sub("EB-5 Period Budget (Annual -- Year 2)")
    pdf.table(
        ["Expense Category", "Annual Cost", "Notes"],
        [
            ["Salaried staff (3 positions)", "$210,000", "COO, Consultant, Ops Mgr"],
            ["Hourly staff (10 positions)", "$346,500", "10 x $16.66/hr x 2,080 hrs"],
            ["Benefits & payroll taxes", "$100,000", "~18% of total wages"],
            ["Office lease (Camas)", "$48,000", "$4,000/mo for ~2,000 sq ft"],
            ["Technology & software", "$24,000", "Control Tower hosting, tools"],
            ["Insurance (E&O, general)", "$18,000", "Professional liability"],
            ["Marketing & BD", "$36,000", "Trade shows, WeChat, content"],
            ["Legal & accounting", "$24,000", "Immigration counsel, CPA"],
            ["Training materials", "$12,000", "Course development, speakers"],
            ["Travel (US-China)", "$18,000", "Client visits, team coordination"],
            ["Miscellaneous", "$12,000", "Supplies, utilities, contingency"],
        ],
        [55, 35, 65],
        bold_last=False
    )

    pdf.table(
        ["", "Amount"],
        [
            ["Total Annual Expenses", "$848,500"],
            ["WA State Training Offsets (est.)", "($85,000)"],
            ["WOTC Tax Credits (est.)", "($48,000)"],
            ["Net Operating Cost", "$715,500"],
        ],
        [80, 75],
        bold_last=True
    )

    # ══════════════════════════════════════════════════════════════
    # 5. PHASE 3: POST-GREEN CARD RESTRUCTURING
    # ══════════════════════════════════════════════════════════════
    pdf.sec("5. Phase 3: Post-Green Card Restructuring (Year 3)")

    pdf.phase_banner("PHASE 3: TALENT UPGRADE & LEAN OPERATIONS", GOLD)

    pdf.sub("The Transition")
    pdf.txt(
        "When EB-5 conditional green cards are issued (typically Month 18-24), and "
        "the I-829 petition timeline permits, 510kBridge restructures its workforce. "
        "The company downsizes from 10+ entry-level positions to a smaller, more "
        "capable team of 6-8 bilingual professionals. This transition prioritizes "
        "quality over quantity -- replacing minimum-wage trainees with skilled "
        "graduates who can generate significantly more revenue per person."
    )

    pdf.green_txt(
        "Key Insight: The EB-5 job creation requirement is met during Phase 2. "
        "Phase 3 is about operational excellence."
    )

    pdf.sub("Hiring Profile: Bilingual US Graduates")
    pdf.txt(
        "510kBridge recruits exclusively from a pool of recent US university graduates "
        "who are bilingual in English and Mandarin Chinese, with degrees in:"
    )
    pdf.bullet("Business Administration / MBA")
    pdf.bullet("Biomedical Engineering / Bioengineering")
    pdf.bullet("Regulatory Affairs / Public Health")
    pdf.bullet("Information Technology / Computer Science")
    pdf.bullet("Technical Writing / Communications")
    pdf.bullet("Accounting / Finance")

    pdf.txt(
        "These graduates are typically children of Chinese families who have invested "
        "in US education. Their bilingual capability is the core competitive advantage "
        "-- they bridge the language and cultural gap that is 510kBridge's entire "
        "value proposition."
    )

    pdf.sub("Why This Talent Pool Is Available")
    pdf.txt(
        "There are approximately 300,000+ Chinese students enrolled in US universities "
        "at any given time. Upon graduation, many face uncertainty about employment and "
        "visa status (OPT, H-1B lottery). Their parents -- who have invested $200,000+ "
        "in US education -- strongly prefer their children remain in the United States. "
        "510kBridge offers exactly what these families want: meaningful employment in a "
        "bilingual environment with career growth in a high-demand industry."
    )

    pdf.sub("Parent-Sponsored On-the-Job Training Program")
    pdf.txt(
        "510kBridge creates a structured on-the-job training (OJT) program for "
        "bilingual graduates. Parents of these graduates can make tax-deductible "
        "donations to support their children's professional development at 510kBridge. "
        "This program offers several advantages:"
    )
    pdf.bullet("Parents gain peace of mind: their children have stable US employment "
               "with career development in a professional environment")
    pdf.bullet("Graduates gain real-world experience in FDA regulatory affairs, medical "
               "device project management, and US-China business consulting")
    pdf.bullet("510kBridge receives training support funding that offsets salary costs "
               "during the 3-6 month ramp-up period")
    pdf.bullet("The company builds a loyal workforce with deep investment in their success")

    pdf.sub("Work Authorization Pathway")
    pdf.txt(
        "510kBridge can issue employment authorization through several mechanisms, "
        "which may begin earlier in the EB-5 process:"
    )
    pdf.bold_bullet("OPT/STEM OPT: ", "Graduates on F-1 visas receive 12 months of "
                    "Optional Practical Training, extendable to 36 months for STEM "
                    "degrees. No sponsorship cost to the company.")
    pdf.bold_bullet("H-1B Sponsorship: ", "For long-term hires, 510kBridge sponsors "
                    "H-1B petitions for specialty occupation positions (regulatory "
                    "affairs, engineering, accounting).")
    pdf.bold_bullet("EB-2/EB-3 Green Card: ", "For exceptional performers, the company "
                    "can sponsor employment-based green cards, creating long-term retention.")

    pdf.sub("Post-Restructuring Team (Year 3)")
    pdf.table(
        ["Role", "Qualifications", "Salary Range"],
        [
            ["COO / Investor", "UCSB Accounting (current)", "$85,000-$100,000"],
            ["Principal Consultant (PMP)", "14 yrs regulated product dev.", "$110,000-$130,000"],
            ["Regulatory Affairs Specialist", "BS/MS Biomed Eng., bilingual", "$65,000-$80,000"],
            ["Project Manager", "BS Business, PMP track, bilingual", "$60,000-$75,000"],
            ["Business Development Mgr", "MBA, bilingual, BD experience", "$65,000-$80,000"],
            ["Technical Writer", "BA/MA Writing, bilingual", "$55,000-$65,000"],
            ["Platform Developer", "BS/MS CS, full-stack, bilingual", "$70,000-$90,000"],
            ["Accounting Analyst", "BS Accounting, bilingual", "$55,000-$65,000"],
        ],
        [55, 55, 42]
    )

    pdf.sub("Transition Timeline")
    pdf.table(
        ["Month", "Action"],
        [
            ["24-26", "Green cards issued; begin recruiting bilingual graduates"],
            ["26-28", "First 2-3 graduate hires onboarded; training program begins"],
            ["28-30", "Complete transition from entry-level WA workforce to graduates"],
            ["30-32", "Entry-level staff receive reference letters, job placement support"],
            ["32-36", "Full lean team operating; all staff bilingual and degree-qualified"],
        ],
        [22, 133]
    )

    # ══════════════════════════════════════════════════════════════
    # 6. PHASE 4: GROWTH & OPTIMIZATION
    # ══════════════════════════════════════════════════════════════
    pdf.sec("6. Phase 4: Growth & Optimization (Years 4-5)")

    pdf.phase_banner("PHASE 4: SCALE & MARKET LEADERSHIP", NAVY)

    pdf.sub("Strategic Objectives")
    pdf.bullet("Grow client base to 10-15 active Professional/Enterprise engagements")
    pdf.bullet("Launch multi-tenant Control Tower SaaS for self-service Starter clients")
    pdf.bullet("Establish 510kBridge as the recognized leader in China-to-FDA consulting")
    pdf.bullet("Build template library for common 510(k) predicate categories")
    pdf.bullet("Develop AI-powered regulatory gap analysis as premium service")
    pdf.bullet("Consider Series A funding or strategic partnership for platform expansion")

    pdf.sub("Revenue Growth Targets")
    pdf.table(
        ["Year", "Clients", "Avg. Monthly/Client", "Annual Revenue"],
        [
            ["Year 4", "8-10", "$18,000", "$1.7M-$2.2M"],
            ["Year 5", "12-15", "$20,000", "$2.9M-$3.6M"],
        ],
        [25, 25, 50, 50]
    )

    pdf.sub("Product Expansion")
    pdf.bold_bullet("Control Tower SaaS (Multi-Tenant): ",
        "Row-level security per client in Supabase enables a self-service platform "
        "where smaller companies manage their own 510(k) projects. Monthly "
        "subscription: $500-$2,000.")
    pdf.bold_bullet("Template Library: ",
        "Pre-built project templates for common 510(k) categories -- respiratory, "
        "cardiovascular, orthopedic, IVD -- reducing onboarding time from weeks to days.")
    pdf.bold_bullet("AI Regulatory Analysis: ",
        "The existing generate_regulatory_analysis.py engine is exposed as a "
        "self-service tool for clients to get preliminary gap analysis before "
        "engaging full services.")

    pdf.sub("Regulatory Pathway Expansion Strategy")
    pdf.txt(
        "510kBridge currently focuses exclusively on FDA 510(k) clearance for "
        "Class II devices. This is a deliberate strategic choice -- the 510(k) "
        "pathway represents the largest addressable market for Chinese medical "
        "device companies entering the US. However, future expansion into "
        "adjacent regulatory pathways is planned:"
    )

    pdf.sub2("Current Focus: 510(k) Class II")
    pdf.txt(
        "The vast majority of Chinese medical device companies seeking US market "
        "entry have Class II devices: patient monitors, imaging systems, IVD "
        "analyzers, rehabilitation equipment, and software as medical device (SaMD). "
        "Control Tower's 7 device category templates, dual-track milestones, and "
        "regulatory workflows are purpose-built for this pathway. This is where "
        "client demand lives and where 510kBridge's competitive advantage is strongest."
    )

    pdf.sub2("Next Expansion: De Novo Classification")
    pdf.txt(
        "De Novo is the natural adjacent pathway. It applies to novel devices "
        "that are low-to-moderate risk but have no existing predicate device. "
        "De Novo shares significant DNA with 510(k): similar testing requirements, "
        "similar FDA review timelines, and similar documentation structure. "
        "Control Tower can support De Novo with modest additions -- primarily "
        "replacing the predicate-equivalence argument with a risk-based "
        "classification argument. Target: Year 3-4."
    )

    pdf.sub2("Class III / PMA: A Different Business")
    pdf.txt(
        "Class III devices require Premarket Approval (PMA), which is "
        "fundamentally different from 510(k). PMA demands prospective clinical "
        "trials, Investigational Device Exemptions (IDE), and dramatically "
        "higher costs and timelines. 510kBridge does not plan to offer PMA "
        "services in its current form. The rationale:"
    )

    pdf.table(
        ["Factor", "510(k) Class II", "PMA Class III"],
        [
            ["Core argument", "Substantial equivalence", "Independent safety/effectiveness"],
            ["Clinical data", "Bench/algorithm validation", "Mandatory clinical trials"],
            ["FDA user fee", "$6.5K-$26K", "~$425K"],
            ["Review timeline", "90 days (MDUFA)", "6-18 months"],
            ["Total cost/device", "$130K-$320K", "$1M-$3M+"],
            ["Post-clearance", "Device listing, complaints", "Conditions of approval, PAS"],
            ["Typical client", "$5M-$50M revenue company", "$50M+ with RA team in place"],
        ],
        [35, 60, 60]
    )

    pdf.txt(
        "Companies with Class III devices typically have $50M+ in funding and "
        "established regulatory teams. They hire specialized CROs and regulatory "
        "firms (EMERGO, NAMSA, Hogan Lovells), not consulting firms for end-to-end "
        "PM. Additionally, PMA would require 510kBridge to build clinical trial "
        "management capabilities (IRB submissions, patient enrollment, adverse event "
        "monitoring, IDE submissions) that do not exist in Control Tower today. "
        "This represents a separate business with a different client profile, "
        "different pricing model ($50-100K/month for 2-3 years), and intense "
        "competition from entrenched players."
    )

    pdf.green_txt(
        "Strategic position: Own 510(k) Class II. Expand to De Novo in Year 3-4. "
        "Leave PMA/Class III to specialized firms -- or evaluate as a separate "
        "business unit only after achieving $3M+ annual revenue."
    )

    pdf.sub("Partnership Development")
    pdf.bullet("Testing labs (UL, TUV, Intertek) -- referral partnerships")
    pdf.bullet("Immigration attorneys -- EB-5/EB-1C clients with medical device interests")
    pdf.bullet("Chinese biotech parks (Shenzhen, Suzhou, Hangzhou) -- embedded partnerships")
    pdf.bullet("Trade associations: RAPS, AdvaMed, CBIA -- speaking, articles, visibility")
    pdf.bullet("WeChat Official Account -- essential for Chinese entrepreneur reach")

    # ══════════════════════════════════════════════════════════════
    # 7. REVENUE MODEL & INCOME STREAMS
    # ══════════════════════════════════════════════════════════════
    pdf.sec("7. Revenue Model & Income Streams")

    pdf.sub("Service Tiers")
    pdf.table(
        ["Tier", "What We Provide", "Monthly Fee"],
        [
            ["Starter (SaaS)", "Control Tower dashboard, bilingual wizard, "
             "dual-track milestones", "$500-$2,000"],
            ["Professional PM", "Full PM engagement, FDA Comms Center, gate reviews, "
             "submission oversight", "$10,000-$25,000"],
            ["Enterprise", "End-to-end: regulatory strategy + PM + US entity setup + "
             "investor docs", "$50,000+/project"],
        ],
        [35, 85, 35]
    )

    pdf.sub("Revenue Composition by Phase")
    pdf.table(
        ["Source", "Phase 1", "Phase 2", "Phase 3", "Phase 4"],
        [
            ["Pilot clients", "100%", "30-40%", "15-20%", "10%"],
            ["New client acquisition", "--", "40-50%", "50-60%", "55-65%"],
            ["WA workforce programs", "--", "10-15%", "--", "--"],
            ["Parent OJT sponsorship", "--", "5-10%", "15-20%", "10-15%"],
            ["SaaS subscriptions", "--", "--", "5-10%", "15-20%"],
        ],
        [40, 25, 25, 25, 25]
    )

    # ══════════════════════════════════════════════════════════════
    # 8. WA STATE WORKFORCE DEVELOPMENT PROGRAMS
    # ══════════════════════════════════════════════════════════════
    pdf.sec("8. Washington State Workforce Development Programs")

    pdf.txt(
        "510kBridge strategically aligns with Washington State programs designed to "
        "reduce unemployment and develop workforce skills. These programs create a "
        "virtuous cycle: state funding offsets training costs, employees gain marketable "
        "skills, and the company satisfies EB-5 job creation requirements."
    )

    pdf.sub("Program Summary")
    pdf.table(
        ["Program", "Benefit to 510kBridge", "Est. Annual Value"],
        [
            ["Job Skills Program (JSP)", "State-funded employee training via "
             "community colleges", "$15,000-$25,000"],
            ["On-the-Job Training (OJT)", "50-75% wage reimbursement during "
             "training (3-6 mo)", "$40,000-$60,000"],
            ["Worker Retraining", "Tuition-free training pipeline from "
             "Clark College", "$10,000-$15,000"],
            ["Work Opportunity Tax Credit", "$2,400-$9,600 per qualifying hire "
             "per year", "$20,000-$48,000"],
        ],
        [45, 75, 35]
    )

    pdf.sub("Training Curriculum for WA Workforce Hires")
    pdf.table(
        ["Module", "Duration", "Content"],
        [
            ["FDA Fundamentals", "4 weeks", "510(k) process, device classification, "
             "predicate search"],
            ["Medical Device Terminology", "2 weeks", "Anatomy, device function, "
             "clinical terminology"],
            ["Document Control", "3 weeks", "DHF structure, version control, audit trail"],
            ["Control Tower Platform", "2 weeks", "Dashboard navigation, data entry, "
             "reporting"],
            ["Business Communication", "Ongoing", "Professional writing, email, "
             "client interaction"],
            ["PMP Essentials", "4 weeks", "Project management fundamentals, "
             "scheduling, risk"],
        ],
        [48, 25, 82]
    )

    pdf.sub("Impact on Local Community")
    pdf.txt(
        "510kBridge's workforce program directly addresses unemployment in Clark "
        "County, Washington. The company provides entry-level positions with "
        "embedded training and skill development, creating a pathway from "
        "unemployment to careers in the growing medical device and regulatory "
        "affairs industry. Former 510kBridge trainees will carry these skills into "
        "the broader job market, creating lasting economic impact."
    )

    # ══════════════════════════════════════════════════════════════
    # 9. BILINGUAL GRADUATE HIRING & PARENT SPONSORSHIP
    # ══════════════════════════════════════════════════════════════
    pdf.sec("9. Bilingual Graduate Hiring & Parent Sponsorship Program")

    pdf.sub("The Opportunity")
    pdf.txt(
        "Chinese families invest an average of $200,000-$300,000 in their children's "
        "US university education. Upon graduation, these students face significant "
        "challenges: the H-1B visa lottery has an acceptance rate of approximately "
        "25%, OPT status is temporary, and many graduates struggle to find positions "
        "that leverage their bilingual skills and cultural competency."
    )

    pdf.txt(
        "510kBridge offers a solution: employment in a company whose entire business "
        "model depends on bilingual English-Chinese capability. Every role at "
        "510kBridge is enhanced by cultural fluency. Parents who have invested "
        "heavily in their children's education can support their career development "
        "through the 510kBridge Training Sponsorship Program."
    )

    pdf.sub("How the Sponsorship Program Works")
    pdf.bold_bullet("Step 1 -- Application: ", "Graduate submits resume, university "
                    "transcripts, and statement of interest")
    pdf.bold_bullet("Step 2 -- Assessment: ", "510kBridge evaluates bilingual proficiency, "
                    "technical skills, and cultural fit")
    pdf.bold_bullet("Step 3 -- Offer: ", "Graduate receives employment offer with "
                    "structured 6-month training plan")
    pdf.bold_bullet("Step 4 -- Sponsorship: ", "Parent makes a donation to 510kBridge's "
                    "Professional Development Fund to support their child's on-the-job "
                    "training program")
    pdf.bold_bullet("Step 5 -- Training: ", "Graduate enters 6-month OJT program with "
                    "mentorship, skill assessments, and professional certification tracks")
    pdf.bold_bullet("Step 6 -- Full Role: ", "Upon completion, graduate transitions to "
                    "a full salaried position with performance-based advancement")

    pdf.sub("Sponsorship Benefits")
    pdf.table(
        ["Stakeholder", "Benefit"],
        [
            ["Graduate", "Stable US employment, career path in FDA/medtech, visa support"],
            ["Parent", "Child stays in US, gains professional experience, peace of mind"],
            ["510kBridge", "High-quality bilingual talent, training cost offset, loyalty"],
            ["Clients", "Bilingual team with US education and cultural bridge capability"],
        ],
        [35, 120]
    )

    pdf.sub("Early Implementation (During EB-5 Period)")
    pdf.txt(
        "The parent sponsorship program can begin during the EB-5 conditional "
        "period (Phase 2), not only in Phase 3. 510kBridge can issue employment "
        "authorization to OPT-eligible graduates immediately, without waiting for "
        "green card issuance. This creates an overlapping workforce model where "
        "bilingual graduates begin replacing entry-level WA hires before the formal "
        "Phase 3 restructuring:"
    )
    pdf.bullet("Months 18-24: First 1-2 bilingual graduates hired under OPT to work "
               "alongside WA workforce hires")
    pdf.bullet("Months 24-30: Gradual transition as green cards are issued and graduate "
               "hires prove their capability")
    pdf.bullet("Month 30+: Full transition to lean bilingual team completed")

    # ══════════════════════════════════════════════════════════════
    # 10. 5-YEAR FINANCIAL PROJECTIONS
    # ══════════════════════════════════════════════════════════════
    pdf.sec("10. 5-Year Financial Projections")

    pdf.sub("Revenue Projections")
    pdf.table(
        ["", "Year 1", "Year 2", "Year 3", "Year 4", "Year 5"],
        [
            ["Active clients", "3-5", "6-8", "8-10", "10-12", "12-15"],
            ["Avg. fee/client/mo", "$10K", "$15K", "$17K", "$18K", "$20K"],
            ["Client revenue", "$360K", "$1.08M", "$1.63M", "$2.16M", "$3.0M"],
            ["WA programs", "--", "$85K", "--", "--", "--"],
            ["Parent sponsorship", "--", "$30K", "$90K", "$60K", "$40K"],
            ["SaaS subscriptions", "--", "--", "$36K", "$96K", "$180K"],
            ["Total Revenue", "$360K", "$1.20M", "$1.76M", "$2.32M", "$3.22M"],
        ],
        [35, 22, 22, 22, 22, 22],
        bold_last=True
    )

    pdf.sub("Expense Projections")
    pdf.table(
        ["", "Year 1", "Year 2", "Year 3", "Year 4", "Year 5"],
        [
            ["Salaries (salaried)", "$150K", "$210K", "$530K", "$580K", "$650K"],
            ["Wages (hourly)", "--", "$347K", "$85K", "--", "--"],
            ["Benefits & taxes", "$27K", "$100K", "$111K", "$105K", "$117K"],
            ["Office lease", "$12K", "$48K", "$48K", "$60K", "$72K"],
            ["Technology", "$12K", "$24K", "$30K", "$36K", "$48K"],
            ["Insurance", "$12K", "$18K", "$18K", "$24K", "$24K"],
            ["Marketing & BD", "$18K", "$36K", "$48K", "$60K", "$72K"],
            ["Legal & accounting", "$18K", "$24K", "$24K", "$30K", "$36K"],
            ["Training & materials", "$6K", "$12K", "$18K", "$12K", "$12K"],
            ["Travel", "$24K", "$18K", "$24K", "$30K", "$36K"],
            ["Miscellaneous", "$6K", "$12K", "$12K", "$15K", "$18K"],
            ["Total Expenses", "$285K", "$849K", "$948K", "$952K", "$1.09M"],
        ],
        [35, 22, 22, 22, 22, 22],
        bold_last=True
    )

    pdf.sub("Profitability Summary")
    pdf.table(
        ["", "Year 1", "Year 2", "Year 3", "Year 4", "Year 5"],
        [
            ["Total Revenue", "$360K", "$1.20M", "$1.76M", "$2.32M", "$3.22M"],
            ["Total Expenses", "$285K", "$849K", "$948K", "$952K", "$1.09M"],
            ["Net Income", "$75K", "$346K", "$808K", "$1.37M", "$2.13M"],
            ["Net Margin", "21%", "29%", "46%", "59%", "66%"],
        ],
        [35, 22, 22, 22, 22, 22],
        bold_last=True
    )

    pdf.green_txt(
        "Breakeven occurs early in Year 1 from pilot client revenue. By Year 3, "
        "the transition to bilingual graduates dramatically improves margins "
        "as revenue/employee increases while total headcount decreases."
    )

    pdf.sub("EB-5 Capital Deployment ($800,000)")
    pdf.table(
        ["Use of Funds", "Amount", "% of Total"],
        [
            ["Office buildout & equipment", "$80,000", "10%"],
            ["Year 1 operating reserve", "$200,000", "25%"],
            ["Salaries & wages (Year 1-2)", "$280,000", "35%"],
            ["Technology & platform dev.", "$80,000", "10%"],
            ["Marketing & BD", "$80,000", "10%"],
            ["Legal, insurance, accounting", "$50,000", "6%"],
            ["Contingency reserve", "$30,000", "4%"],
        ],
        [55, 45, 45],
        bold_last=False
    )

    # ══════════════════════════════════════════════════════════════
    # 11. ORGANIZATIONAL STRUCTURE EVOLUTION
    # ══════════════════════════════════════════════════════════════
    pdf.sec("11. Organizational Structure Evolution")

    pdf.sub("Phase 1: Pilot Team (4-6 people, China-based)")
    pdf.table(
        ["Role", "Location", "Focus"],
        [
            ["CEO", "Shanghai", "BD, client relationships, investor pipeline"],
            ["General Manager", "Shanghai", "Daily ops, medical content, QC"],
            ["Sr. Account Manager", "Shanghai", "Client acquisition, marketing"],
            ["Principal Consultant", "US (remote)", "FDA strategy, regulatory guidance"],
        ],
        [45, 30, 80]
    )

    pdf.sub("Phase 2: EB-5 Team (10-13 people, US-based)")
    pdf.table(
        ["Role", "Location", "Focus"],
        [
            ["COO / Investor", "Camas, WA", "US operations, accounting, compliance"],
            ["Principal Consultant", "Camas, WA", "FDA regulatory, PM, client delivery"],
            ["Operations Manager", "Camas, WA", "Office, logistics, procurement"],
            ["8-10 Entry-Level Hires", "Camas, WA", "Training + work/education program"],
            ["CEO", "Shanghai (transitioning)", "China BD, then US leadership"],
            ["GM / Account Mgr", "Shanghai", "China operations continuity"],
        ],
        [45, 45, 65]
    )

    pdf.sub("Phase 3-4: Lean Bilingual Team (6-12 people)")
    pdf.table(
        ["Role", "Profile", "Focus"],
        [
            ["COO", "UCSB Accounting, bilingual", "Finance, compliance, investor relations"],
            ["Principal Consultant", "PMP, 14 yrs medtech", "FDA strategy, client delivery"],
            ["Regulatory Specialist", "BS/MS Biomed, bilingual", "510(k) submissions, testing"],
            ["Project Manager", "BS Business, bilingual", "Client PM, Control Tower ops"],
            ["BD Manager", "MBA, bilingual", "Sales, partnerships, marketing"],
            ["Technical Writer", "BA/MA Writing, bilingual", "FDA docs, translations"],
            ["Platform Developer", "BS/MS CS, bilingual", "Control Tower SaaS development"],
            ["Accounting Analyst", "BS Acct, bilingual", "Books, payroll, tax compliance"],
        ],
        [45, 50, 60]
    )

    # ══════════════════════════════════════════════════════════════
    # 12. RISK ANALYSIS & MITIGATION
    # ══════════════════════════════════════════════════════════════
    pdf.sec("12. Risk Analysis & Mitigation")

    pdf.table(
        ["Risk", "Impact", "Likelihood", "Mitigation"],
        [
            ["Pilot fails to sign 3 clients", "High", "Low",
             "Network in place; discounted rates; strong value prop"],
            ["EB-5 I-526E petition denied", "Critical", "Low",
             "Experienced counsel; strong business plan with pilot data"],
            ["Insufficient job creation", "High", "Low",
             "WA programs ensure 10+ hires; documented in business plan"],
            ["Revenue shortfall in Year 2", "Medium", "Medium",
             "$800K reserve covers 18+ months; WA funding offsets costs"],
            ["Key person departure", "High", "Low",
             "Equity vesting; non-compete; cross-training program"],
            ["Regulatory market shift", "Medium", "Low",
             "Diversified client base; SaaS model creates recurring revenue"],
            ["H-1B visa denial for hire", "Medium", "Medium",
             "OPT/STEM OPT provides 36 months; multiple candidates in pipeline"],
            ["China-US political tensions", "Medium", "Medium",
             "FDA pathway is regulatory, not political; diversify client origins"],
        ],
        [42, 20, 22, 68]
    )

    # ══════════════════════════════════════════════════════════════
    # 13. KEY MILESTONES & SUCCESS METRICS
    # ══════════════════════════════════════════════════════════════
    pdf.sec("13. Key Milestones & Success Metrics")

    pdf.sub("Critical Path Milestones")
    pdf.table(
        ["Timeline", "Milestone", "Success Metric"],
        [
            ["Month 3", "Shanghai WFOE registered", "Business license issued"],
            ["Month 6", "First 2 pilot clients signed", "Signed contracts, revenue"],
            ["Month 9", "Pilot revenue > $30K/mo", "Bank statements"],
            ["Month 12", "I-526E petition filed", "USCIS receipt notice"],
            ["Month 15", "US office operational", "Lease signed, staff hiring"],
            ["Month 18", "10+ US employees hired", "Payroll records, W-2s"],
            ["Month 24", "Conditional green cards issued", "USCIS approval"],
            ["Month 30", "Bilingual team transition complete", "All staff degree-qualified"],
            ["Month 36", "8+ active clients", "Revenue > $1.5M/year"],
            ["Month 48", "I-829 filed (remove conditions)", "Job creation documented"],
            ["Month 54", "Permanent green cards", "USCIS approval"],
            ["Month 60", "12+ clients, $3M+ revenue", "Audited financials"],
        ],
        [25, 52, 78]
    )

    pdf.sub("5-Year KPIs")
    pdf.table(
        ["KPI", "Year 1", "Year 2", "Year 3", "Year 5"],
        [
            ["Active clients", "3-5", "6-8", "8-10", "12-15"],
            ["Revenue", "$360K", "$1.2M", "$1.76M", "$3.22M"],
            ["US employees", "1", "13", "8", "12"],
            ["Client retention", ">80%", ">85%", ">90%", ">90%"],
            ["Net margin", "21%", "29%", "46%", "66%"],
            ["Revenue/employee", "$90K", "$92K", "$220K", "$268K"],
        ],
        [40, 28, 28, 28, 28]
    )

    # ══════════════════════════════════════════════════════════════
    # CLOSING
    # ══════════════════════════════════════════════════════════════
    pdf.ln(4)
    pdf.sec("Conclusion")
    pdf.txt(
        "510kBridge's 5-year strategy is designed to minimize risk while maximizing "
        "the probability of success. The China pilot program validates the business "
        "model before significant capital is deployed. The EB-5 period creates US "
        "jobs and diversifies revenue through three independent streams. The post-"
        "green-card restructuring transforms the company into a lean, high-margin "
        "operation staffed by the best bilingual talent available."
    )

    pdf.txt(
        "The parent-sponsored training program is not just a cost offset -- it is "
        "a strategic differentiator. No other FDA consulting firm has access to a "
        "self-selecting pool of bilingual graduates whose families are financially "
        "motivated to support their US employment. This creates a sustainable "
        "competitive advantage that compounds over time."
    )

    pdf.green_txt(
        "510kBridge: Built by families, for families, bridging China and the US "
        "in the world's largest medical device market."
    )

    # ── DISCLAIMER ──────────────────────────────
    pdf.ln(8)
    pdf.set_draw_color(*GRAY)
    pdf.set_line_width(0.3)
    pdf.line(pdf.l_margin, pdf.get_y(), pdf.w - pdf.r_margin, pdf.get_y())
    pdf.ln(3)
    pdf.set_font("Helvetica", "I", 7.5)
    pdf.set_text_color(*GRAY)
    pdf.multi_cell(0, 4,
        _a("This document is for discussion purposes only and does not constitute legal, "
        "tax, or immigration advice. EB-5 and EB-1C eligibility must be confirmed by "
        "qualified immigration counsel. Financial projections are estimates based on "
        "market research and pilot program assumptions, not guarantees. Washington "
        "State workforce program availability and terms are subject to change. Parent "
        "sponsorship donations should be structured with guidance from tax counsel."),
        new_x="LMARGIN", new_y="NEXT")

    # ── SAVE ────────────────────────────────────
    out = os.path.join(OUT_DIR, "510kBridge_5Year_Business_Strategy.pdf")
    pdf.output(out)
    sz = os.path.getsize(out)
    print(f"Created {out}  ({sz:,} bytes, {pdf.pages_count} pages)")


if __name__ == "__main__":
    build()
