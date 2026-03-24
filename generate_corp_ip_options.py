#!/usr/bin/env python3
"""
Generate Corporate Structure & IP Ownership Options PDF.
Companion to the Meeting Prep for Dr. Dai (March 23, 2026).
Covers Delaware C-Corp structural options and IP transfer strategies.
"""

import os
from fpdf import FPDF

OUT_DIR = os.path.dirname(os.path.abspath(__file__))

BLUE = (30, 90, 200)
DARK = (15, 17, 23)
GRAY = (120, 120, 130)
TEXT = (40, 40, 45)
RED = (180, 40, 40)
GREEN = (20, 130, 70)
ORANGE = (200, 120, 20)
WHITE = (255, 255, 255)


class OptionsReport(FPDF):
    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(*GRAY)
        self.cell(0, 5, "Corporate Structure & IP Ownership  |  Company B USA", align="R")
        self.ln(8)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(*GRAY)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")

    # ── helpers ──
    def sec(self, num, title):
        self.set_font("Helvetica", "B", 15)
        self.set_text_color(*BLUE)
        self.cell(0, 10, f"{num}. {title}", new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(*BLUE)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(4)

    def sub(self, title, color=BLUE):
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(*color)
        self.cell(0, 7, title, new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def txt(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*TEXT)
        self.multi_cell(0, 5.5, text, new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def bullet(self, text, indent=6):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*TEXT)
        self.set_x(self.l_margin + indent)
        self.multi_cell(self.w - self.l_margin - self.r_margin - indent, 5.5,
                        f"- {text}", new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def option_header(self, label, title, color):
        self.set_draw_color(*color)
        self.set_fill_color(*color)
        y = self.get_y()
        w = self.w - self.l_margin - self.r_margin
        self.rect(self.l_margin, y, w, 8, style="DF")
        self.set_xy(self.l_margin + 3, y + 1)
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(*WHITE)
        self.cell(0, 6, f"{label}: {title}")
        self.set_y(y + 10)

    def pros_cons(self, pros, cons):
        x_mid = self.l_margin + (self.w - self.l_margin - self.r_margin) / 2
        y_start = self.get_y()

        # Pros header
        self.set_xy(self.l_margin, y_start)
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*GREEN)
        self.cell(80, 5.5, "ADVANTAGES")
        self.set_xy(x_mid, y_start)
        self.set_text_color(*RED)
        self.cell(80, 5.5, "DISADVANTAGES")
        self.ln(6)

        self.set_font("Helvetica", "", 9)
        max_lines = max(len(pros), len(cons))
        for i in range(max_lines):
            y = self.get_y()
            if y > self.h - 25:
                self.add_page()
                y = self.get_y()
            if i < len(pros):
                self.set_xy(self.l_margin + 2, y)
                self.set_text_color(*TEXT)
                self.multi_cell(
                    x_mid - self.l_margin - 4, 4.5,
                    f"+ {pros[i]}", new_x="LMARGIN", new_y="NEXT")
            y_after_left = self.get_y()
            if i < len(cons):
                self.set_xy(x_mid + 2, y)
                self.set_text_color(*TEXT)
                self.multi_cell(
                    self.w - self.r_margin - x_mid - 4, 4.5,
                    f"- {cons[i]}", new_x="LMARGIN", new_y="NEXT")
            y_after_right = self.get_y()
            self.set_y(max(y_after_left, y_after_right) + 1)
        self.ln(2)

    def info_box(self, title, items, color=BLUE):
        self.set_draw_color(*color)
        bg = (240, 243, 255) if color == BLUE else (255, 240, 240) if color == RED else (240, 255, 240)
        self.set_fill_color(*bg)
        y = self.get_y()
        line_h = 5.5
        box_h = 10 + len(items) * line_h + 4
        if y + box_h > self.h - 20:
            self.add_page()
            y = self.get_y()
        self.rect(self.l_margin, y, self.w - self.l_margin - self.r_margin, box_h, style="DF")
        self.set_xy(self.l_margin + 4, y + 3)
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(*color)
        self.cell(0, 5.5, title)
        self.set_xy(self.l_margin + 6, y + 10)
        self.set_font("Helvetica", "", 9)
        self.set_text_color(*TEXT)
        for item in items:
            self.set_x(self.l_margin + 6)
            self.cell(0, line_h, item, new_x="LMARGIN", new_y="NEXT")
        self.set_y(y + box_h + 4)

    def diagram(self, lines):
        self.set_font("Courier", "", 8.5)
        self.set_text_color(*TEXT)
        for line in lines:
            if self.get_y() > self.h - 20:
                self.add_page()
            self.cell(0, 4.2, line, new_x="LMARGIN", new_y="NEXT")
        self.ln(4)

    def table(self, headers, rows, col_w):
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*WHITE)
        self.set_fill_color(*BLUE)
        for i, h in enumerate(headers):
            self.cell(col_w[i], 7, h, border=1, fill=True, align="C")
        self.ln()
        self.set_font("Helvetica", "", 9)
        self.set_text_color(*TEXT)
        for ri, row in enumerate(rows):
            is_last = ri == len(rows) - 1
            if is_last:
                self.set_font("Helvetica", "B", 9)
                self.set_fill_color(230, 235, 250)
            else:
                self.set_font("Helvetica", "", 9)
                self.set_fill_color(250, 250, 255) if ri % 2 == 0 else self.set_fill_color(255, 255, 255)
            for ci, val in enumerate(row):
                align = "C" if ci > 0 else "L"
                self.cell(col_w[ci], 6, val, border=1, fill=True, align=align)
            self.ln()
        self.ln(3)

    def recommendation_badge(self, text):
        self.set_fill_color(*GREEN)
        y = self.get_y()
        self.rect(self.l_margin, y, 100, 7, style="DF")
        self.set_xy(self.l_margin + 2, y + 1)
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*WHITE)
        self.cell(96, 5, text)
        self.set_y(y + 9)

    def not_recommended_badge(self, text):
        self.set_fill_color(*RED)
        y = self.get_y()
        self.rect(self.l_margin, y, 100, 7, style="DF")
        self.set_xy(self.l_margin + 2, y + 1)
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*WHITE)
        self.cell(96, 5, text)
        self.set_y(y + 9)

    def conditional_badge(self, text):
        self.set_fill_color(*ORANGE)
        y = self.get_y()
        self.rect(self.l_margin, y, 100, 7, style="DF")
        self.set_xy(self.l_margin + 2, y + 1)
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*WHITE)
        self.cell(96, 5, text)
        self.set_y(y + 9)


# ═══════════════════════════════════════════════════════════════
#  BUILD
# ═══════════════════════════════════════════════════════════════
def build():
    pdf = OptionsReport()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)

    # ── COVER PAGE ──
    pdf.add_page()
    pdf.ln(30)
    pdf.set_font("Helvetica", "B", 28)
    pdf.set_text_color(*BLUE)
    pdf.cell(0, 14, "Corporate Structure &", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 14, "IP Ownership Options", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(6)
    pdf.set_font("Helvetica", "", 14)
    pdf.set_text_color(*TEXT)
    pdf.cell(0, 8, "ICU Respiratory Digital Twin System", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)
    pdf.set_font("Helvetica", "", 12)
    pdf.set_text_color(*GRAY)
    pdf.cell(0, 7, "Company B USA  --  Delaware C-Corp Formation", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 7, "March 23, 2026", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(12)

    pdf.set_font("Helvetica", "I", 10)
    pdf.set_text_color(*GRAY)
    pdf.multi_cell(0, 5.5,
        "This document presents structural options for the Delaware C-Corp formation "
        "and intellectual property ownership strategy. Each option includes a description, "
        "advantages and disadvantages, structural diagram, and applicability assessment. "
        "It is designed to support decision-making between Dr. Dai, Lawrence Liu, "
        "and the project management team.",
        align="C")
    pdf.ln(10)

    # Context box
    pdf.info_box("Project Context", [
        "Device: sEMG Neural Drive + EIT Ventilation/Perfusion ICU Monitor",
        "Regulatory Path: FDA 510(k) Class II clearance (18-23 month program)",
        "Current IP Holder: Dr. Dai / Silan Technology (Chengdu, China)",
        "Proposed US Entity: Delaware C-Corp ('Company B USA')",
        "Inventor: Dr. Dai (CTO, 100% allocation)",
        "Investor: Lawrence Liu (proposed CEO or operational lead, lead investor)",
        "PMP / Regulatory Lead: Lon Dailey (Arch Medical Management, LLC)",
        "Seed Round: $1.8M raised (direct equity) -- funds available for deployment",
        "Monthly Burn: ~$45K  |  Estimated Runway: ~40 months at seed level",
    ])

    # ═══════════════════════════════════════
    # PART I: CORPORATE STRUCTURE
    # ═══════════════════════════════════════
    pdf.add_page()
    pdf.sec("I", "Corporate Structure Options")
    pdf.txt(
        "The corporate structure determines ownership, governance, liability, tax treatment, "
        "and -- critically for this project -- CFIUS exposure and FDA applicant status. "
        "Three primary options are evaluated below, each with distinct trade-offs.")

    # ─── OPTION A ───
    pdf.add_page()
    pdf.option_header("Option A", "Standard Delaware C-Corp (Single Entity)", GREEN)
    pdf.recommendation_badge("RECOMMENDED")
    pdf.ln(2)

    pdf.sub("Description")
    pdf.txt(
        "A single Delaware C-Corp ('Company B USA') is formed. All IP, operations, "
        "FDA submissions, and investor equity live inside this one entity. Silan Technology "
        "in Chengdu operates as an independent contract manufacturer under a Master "
        "Manufacturing Agreement -- it has no equity stake, no board representation, "
        "and no ownership in Company B USA.")

    pdf.sub("Structure")
    pdf.diagram([
        "+===========================================================+",
        "|              COMPANY B USA (Delaware C-Corp)               |",
        "|                                                           |",
        "|  - Owns ALL IP (patents, software, trade secrets)         |",
        "|  - 510(k) applicant & FDA establishment holder            |",
        "|  - Issues common + preferred stock                        |",
        "|  - US-majority board of directors                         |",
        "+===========================================================+",
        "        |                                     |",
        "        | Employment/Consulting               | Manufacturing",
        "        | Agreements                          | Agreement",
        "        v                                     v",
        " +-----------------+              +------------------------+",
        " |  Team Members   |              |  Silan Technology      |",
        " |  Dr. Dai (CTO)  |              |  (Chengdu, China)      |",
        " |  Lon (PMP)      |              |  Contract manufacturer |",
        " |  Future hires   |              |  No equity or control  |",
        " +-----------------+              +------------------------+",
    ])

    pdf.sub("Governance")
    pdf.txt(
        "Board of Directors (3 seats):\n"
        "  Seat 1 -- Lon Dailey (US citizen, elected by common holders)\n"
        "  Seat 2 -- Dr. Dai (inventor seat, elected by common holders)\n"
        "  Seat 3 -- Independent director (mutually agreed, US person preferred)\n\n"
        "Officers:\n"
        "  CEO -- Lawrence Liu (if he takes operational role; inventor's plan\n"
        "         shows Founder as CEO/CTO -- role assignment to be confirmed)\n"
        "  CTO -- Dr. Dai\n"
        "  Secretary/Treasurer -- Lon Dailey\n\n"
        "Lawrence holds a board OBSERVER seat (non-voting) to avoid triggering CFIUS "
        "'foreign control' -- he retains protective provisions (veto rights) on major "
        "decisions without holding a voting board seat.")

    pdf.sub("Dr. Dai's Immigration Status -- CFIUS Variable")
    pdf.txt(
        "It is not yet known whether Dr. Dai holds US citizenship or a green card. "
        "He has relatives in the United States who may hold US citizenship or permanent "
        "residency. This is a critical variable for board composition and CFIUS analysis:\n\n"
        "  Scenario A -- Dr. Dai is a US person (citizen or green card holder):\n"
        "    Board = 2 US persons (Lon + Dr. Dai) + 1 independent\n"
        "    CFIUS impact: STRONGEST position. US persons hold 2 of 3 board seats\n"
        "    without relying on the independent director. If the independent is also\n"
        "    US, the board is 3/3 US-controlled. Lawrence as observer is clean.\n\n"
        "  Scenario B -- Dr. Dai is NOT a US person (foreign national):\n"
        "    Board = 1 confirmed US (Lon) + 1 foreign (Dr. Dai) + 1 independent\n"
        "    CFIUS impact: US majority depends on the independent director being a\n"
        "    US person. This is still workable but the independent seat becomes\n"
        "    essential for CFIUS compliance, not optional.\n\n"
        "  Note on relatives: Dr. Dai's US-based relatives cannot hold shares or\n"
        "  board seats as proxies for him -- CFIUS looks through nominee structures\n"
        "  to the beneficial owner. However, if Dr. Dai has a path to US permanent\n"
        "  residency (e.g., family-sponsored green card), this should be factored\n"
        "  into the long-term governance plan.\n\n"
        "  ACTION ITEM: Confirm Dr. Dai's immigration status before finalizing\n"
        "  the board structure and CFIUS filing strategy.")

    pdf.sub("Equity Allocation (Illustrative)")
    pdf.table(
        ["Party", "Shares", "Ownership", "Type", "Contribution"],
        [
            ("Dr. Dai", "4,000,000", "40%", "Common", "IP + CTO"),
            ("Lawrence Liu", "3,000,000", "30%", "Preferred", "Cash"),
            ("Lon Dailey", "1,500,000", "15%", "Common", "PMP + Reg"),
            ("Option Pool", "1,500,000", "15%", "Reserved", "Future hires"),
            ("TOTAL", "10,000,000", "100%", "", ""),
        ],
        [45, 25, 20, 22, 58],
    )

    pdf.pros_cons(
        [
            "Simplest structure -- one entity, one cap table",
            "Cleanest for FDA: applicant owns IP outright",
            "Easiest for investors to evaluate and fund",
            "Lowest formation and maintenance cost (~$2K)",
            "US board majority satisfies CFIUS (under either Dr. Dai scenario)",
            "Standard structure for Series A fundraising",
            "Delaware courts have deepest body of corp law",
        ],
        [
            "No structural separation between US and China ops",
            "All liability in one entity (mitigated by insurance)",
            "Dr. Dai trades IP ownership for equity (requires trust)",
            "If Lawrence or Dr. Dai is foreign national, CFIUS filing still needed",
            "Silan has no structural incentive beyond the contract",
        ],
    )

    pdf.info_box("CFIUS Analysis for Option A", [
        "IP owned by US entity: YES (full assignment)",
        "Board controlled by US persons: YES (2 of 3 if Dr. Dai is US person,",
        "  or 2 of 3 via Lon + independent if Dr. Dai is foreign national)",
        "Foreign person has operational control: NO (observer only)",
        "Critical technology in US entity: YES (510(k) applicant)",
        "Dr. Dai status: UNKNOWN -- must confirm citizenship/green card",
        "Likely CFIUS outcome: Voluntary declaration advisable;",
        "  structure is designed to survive review under either scenario.",
    ])

    # ─── OPTION B ───
    pdf.add_page()
    pdf.option_header("Option B", "US Parent + China Subsidiary (Holding Structure)", ORANGE)
    pdf.conditional_badge("CONDITIONAL -- Higher complexity")
    pdf.ln(2)

    pdf.sub("Description")
    pdf.txt(
        "Company B USA (Delaware C-Corp) is formed as the parent company. Silan Technology "
        "in Chengdu becomes a wholly-owned subsidiary (WFOE -- Wholly Foreign-Owned "
        "Enterprise) of Company B USA. All IP is still assigned to the US parent, but the "
        "China subsidiary is formally inside the corporate family rather than arms-length.")

    pdf.sub("Structure")
    pdf.diagram([
        "+===========================================================+",
        "|              COMPANY B USA (Delaware C-Corp)               |",
        "|              PARENT COMPANY                                |",
        "|  - Owns ALL IP                                            |",
        "|  - 510(k) applicant                                       |",
        "|  - Issues equity to Dr. Dai, Lawrence, Lon                |",
        "+===========================================================+",
        "                          |",
        "                   100% ownership",
        "                          |",
        "                          v",
        "+===========================================================+",
        "|              SILAN TECHNOLOGY (Chengdu)                    |",
        "|              WFOE -- Wholly Foreign-Owned Enterprise       |",
        "|  - Manufacturing operations                               |",
        "|  - Employees / lab / equipment                            |",
        "|  - Operates under Company B USA's direction               |",
        "|  - Licensed to use IP for manufacturing only              |",
        "+===========================================================+",
    ])

    pdf.sub("When This Makes Sense")
    pdf.txt(
        "This structure is appropriate if:\n"
        "  - The company plans to hire employees directly in China (not just contract mfg)\n"
        "  - There are significant China-side assets (lab equipment, facilities) to own\n"
        "  - Future plans include NMPA registration for the Chinese domestic market\n"
        "  - Lawrence or Dr. Dai want the China operation formally inside the company\n"
        "  - Long-term plan is dual-market (US + China) commercialization")

    pdf.pros_cons(
        [
            "Full operational control over China manufacturing",
            "Consolidated financial statements for investors",
            "China entity is a subsidiary, not a partner -- cleaner",
            "Can hire Chinese employees directly (not just Silan staff)",
            "Positions company for NMPA (China FDA) submission later",
            "IP still owned by US parent (same FDA benefit as Option A)",
        ],
        [
            "WFOE formation in China costs $30K-$80K and takes 3-6 months",
            "Chinese regulatory approvals (MOFCOM, SAMR) required",
            "Ongoing China compliance: tax filings, annual audits, labor law",
            "Transfer pricing rules apply (US-China intercompany transactions)",
            "Increases CFIUS scrutiny -- US company now owns China operations",
            "Repatriation of profits from China subject to withholding tax (10%)",
            "Adds $15K-$30K/year in accounting and legal overhead",
            "China's data localization laws may apply to subsidiary data",
        ],
    )

    pdf.info_box("CFIUS Analysis for Option B", [
        "IP owned by US entity: YES (parent holds IP)",
        "Board controlled by US persons: YES (same as Option A)",
        "Foreign subsidiary: YES -- adds complexity to CFIUS review",
        "Likely CFIUS outcome: More intensive review than Option A;",
        "  CFIUS may require a mitigation agreement restricting data",
        "  flow between parent and subsidiary.",
    ])

    pdf.info_box("Cost Comparison vs. Option A", [
        "Formation cost: +$30K-$80K (WFOE registration in China)",
        "Annual overhead: +$15K-$30K (China compliance, audit, legal)",
        "Time to establish: 3-6 months (vs. 1-2 weeks for Option A)",
        "Net: Adds ~$60K-$110K in Year 1 costs over Option A.",
    ])

    # ─── OPTION C ───
    pdf.add_page()
    pdf.option_header("Option C", "Parallel Entities (Contractual Alliance)", RED)
    pdf.not_recommended_badge("NOT RECOMMENDED for 510(k) path")
    pdf.ln(2)

    pdf.sub("Description")
    pdf.txt(
        "Two independent companies operate in parallel: Company B USA (Delaware C-Corp) "
        "in the United States, and Silan Technology (existing entity) in China. They are "
        "connected only by contractual agreements -- a manufacturing contract, an IP license, "
        "and cross-equity provisions. Neither owns the other.")

    pdf.sub("Structure")
    pdf.diagram([
        "+---------------------------+           +---------------------------+",
        "|    Company B USA          |           |    Silan Technology       |",
        "|    (Delaware C-Corp)      |  License  |    (Chengdu, China)      |",
        "|                           | <=======> |                           |",
        "|  - 510(k) applicant      |  Mfg Agmt |  - Retains some/all IP   |",
        "|  - US market operations  |           |  - Manufacturing          |",
        "|  - US investors          |  Revenue  |  - China market (own)     |",
        "|  - Lon, Lawrence         |  sharing  |  - Dr. Dai's base entity |",
        "+---------------------------+           +---------------------------+",
        "",
        "        No ownership link -- contractual only",
    ])

    pdf.sub("Variations")
    pdf.txt(
        "C1 -- License Model: Silan retains IP, licenses to Company B USA\n"
        "C2 -- Split Model: IP split by territory (US rights to Company B, China to Silan)\n"
        "C3 -- Revenue Share: Both entities co-own IP, split revenue by market")

    pdf.pros_cons(
        [
            "No WFOE formation needed (Silan already exists)",
            "Dr. Dai retains IP control in China (may prefer this)",
            "Avoids consolidating China operations into US entity",
            "Silan can independently pursue China/APAC market",
            "Simpler China-side compliance (no foreign ownership issues)",
        ],
        [
            "FDA concern: applicant does not own the technology",
            "Investors avoid this -- they can't assess IP value",
            "Acquirers must negotiate with BOTH entities",
            "CFIUS risk: Chinese entity controls critical technology",
            "License can be revoked, destabilizing the US company",
            "Transfer pricing and royalty payments create tax complexity",
            "No consolidated financials -- two separate P&Ls",
            "Governance disputes have no internal resolution mechanism",
            "IP disputes cross two legal systems (US + China)",
            "510(k) predicate strategy weakened without IP ownership",
        ],
    )

    pdf.info_box("FDA Impact for Option C", [
        "The 510(k) applicant must demonstrate it controls the technology.",
        "A license from a foreign entity creates dependency that FDA can question.",
        "If the license is revoked, the cleared device has no IP backing.",
        "FDA reviewers may request proof of IP ownership -- a license is weaker.",
        "This does NOT prevent 510(k) clearance, but adds risk and review time.",
    ], RED)

    pdf.info_box("CFIUS Analysis for Option C", [
        "IP owned by US entity: NO (or only partial)",
        "Chinese entity controls critical technology: YES",
        "Likely CFIUS outcome: Highest risk of the three options;",
        "  may result in mandatory filing and potential block if",
        "  Chinese entity retains control of medical device IP.",
    ], RED)

    # ─── COMPARISON TABLE ───
    pdf.add_page()
    pdf.sub("Corporate Structure -- Side-by-Side Comparison")
    pdf.ln(2)

    comp_col = [48, 48, 48, 26]
    pdf.table(
        ["Criterion", "A: Single Corp", "B: Parent+Sub", "C: Parallel"],
        [
            ("Formation cost", "$1.5K-$2K", "$30K-$80K", "$1.5K-$2K"),
            ("Formation time", "1-2 weeks", "3-6 months", "1-2 weeks"),
            ("Annual overhead", "$2K-$5K", "$20K-$35K", "$5K-$10K"),
            ("IP location", "US entity", "US parent", "Split/China"),
            ("FDA strength", "Strongest", "Strong", "Weakest"),
            ("Investor appeal", "Highest", "High", "Low"),
            ("CFIUS risk", "Low-Moderate", "Moderate", "High"),
            ("China market", "Via contract", "Via subsidiary", "Direct"),
            ("Acquirer appeal", "Highest", "High", "Complex"),
            ("Complexity", "Low", "High", "Moderate"),
            ("RECOMMENDATION", "YES", "CONDITIONAL", "NO"),
        ],
        comp_col,
    )

    pdf.txt(
        "Recommendation: Option A is the correct starting structure. If the company "
        "later decides to hire Chinese employees directly or pursue NMPA registration, "
        "it can convert to Option B by forming a WFOE at that time. There is no reason "
        "to absorb the cost and complexity of Option B at formation. Option C should be "
        "avoided for the 510(k) path.")

    # ═══════════════════════════════════════
    # PART II: IP OWNERSHIP & TRANSFER
    # ═══════════════════════════════════════
    pdf.add_page()
    pdf.sec("II", "IP Ownership & Technology Transfer Options")
    pdf.txt(
        "Intellectual property is the core asset of this venture. The IP strategy determines "
        "FDA applicant eligibility, investor confidence, CFIUS exposure, and acquisition "
        "readiness. Three options are presented, with the recommended path first.")

    pdf.ln(2)
    pdf.info_box("Current IP Inventory (to be confirmed with Dr. Dai)", [
        "sEMG Neural Drive algorithms and signal processing software",
        "EIT Ventilation/Perfusion reconstruction algorithms",
        "MyoBus communication protocol and firmware",
        "Hardware design files (PCB, sensor array, electrode configurations)",
        "Patent applications (jurisdictions and status TBD)",
        "Trade secrets (calibration methods, training data, signal models)",
        "Software copyrights (embedded firmware, desktop analysis tools)",
    ])

    pdf.info_box("IMPORTANT: Two-Phase IP Transfer (per Inventor Business Plan v7)", [
        "Phase 1 (Immediate / Seed): sEMG IP + MyoBus protocol + related software",
        "  -- Transferred to Company B USA at formation for founder equity",
        "  -- Required before FDA Pre-Sub meeting (M+2)",
        "",
        "Phase 2 (Deferred / Series A): EIT algorithms + EIT hardware designs",
        "  -- EIT IP currently held by Company A (China)",
        "  -- Transfer negotiation begins after Series A funding (Year 1 Q2-Q4)",
        "  -- May be outright purchase or exclusive license, TBD by negotiation",
        "  -- Does NOT block sEMG 510(k) submission (Module A is independent)",
        "",
        "The equity-for-IP calculation (40% for Dr. Dai) must account for whether",
        "the 40% covers sEMG IP only (Phase 1) or includes future EIT transfer.",
    ], color=ORANGE)

    # ─── IP OPTION 1 ───
    pdf.add_page()
    pdf.option_header("IP Option 1", "Full Assignment to US Entity + Back-License", GREEN)
    pdf.recommendation_badge("RECOMMENDED -- Cleanest for FDA + Investors")
    pdf.ln(2)

    pdf.sub("How It Works")
    pdf.txt(
        "This is a two-step legal transaction:\n\n"
        "Step 1 -- IP Assignment (China to US)\n"
        "Dr. Dai (or Silan Technology, whoever holds the IP) executes an IP Assignment "
        "Agreement transferring ALL rights, title, and interest in the patents, patent "
        "applications, software copyrights, trade secrets, and know-how to Company B USA. "
        "This is a permanent, irrevocable transfer. Company B USA becomes the legal owner.\n\n"
        "Step 2 -- Manufacturing Back-License (US to China)\n"
        "Company B USA grants Silan Technology a limited license to use the IP ONLY for "
        "manufacturing the device on behalf of Company B USA. This license is:\n"
        "  - Non-exclusive (Company B USA can use other manufacturers later)\n"
        "  - Revocable (Company B USA can terminate if Silan underperforms)\n"
        "  - Limited in scope (manufacturing only, not independent sales)\n"
        "  - Controlled by the US entity at all times\n\n"
        "Step 3 (Optional) -- Academic/Research Back-License\n"
        "A separate perpetual, royalty-free license to Dr. Dai personally for academic "
        "research, teaching, and publication -- non-commercial use only. This preserves "
        "Dr. Dai's ability to continue scholarly work without restriction.")

    pdf.sub("Structure Diagram")
    pdf.diagram([
        "+---------------------------+    Full IP Assignment     +---------------------------+",
        "|   Dr. Dai / Silan Tech    | ========================>|    Company B USA           |",
        "|   (Chengdu, China)        |   (permanent, all rights)|    (Delaware C-Corp)       |",
        "|                           |                          |                            |",
        "|   Current IP holder       |                          |    NEW legal IP owner      |",
        "|   Inventor                |                          |    510(k) applicant        |",
        "+---------------------------+                          +----------------------------+",
        "            ^                                                      |",
        "            |          Manufacturing Back-License                  |",
        "            +<====================================================+",
        "              (non-exclusive, revocable, mfg only, US controlled)",
        "",
        "Dr. Dai's value exchange:  IP ownership  --->  Equity ownership (40%)",
        "If Company B USA valued at $20M:  40% = $8M (vs. holding IP personally)",
    ])

    pdf.sub("Key Terms of the Assignment Agreement")
    pdf.txt(
        "  Assignor:          Dr. Dai and/or Silan Technology\n"
        "  Assignee:          Company B USA (Delaware C-Corp)\n"
        "  Scope:             All patents, patent applications, copyrights,\n"
        "                     trade secrets, know-how, and derivative works\n"
        "  Consideration:     Founder shares (4,000,000 common shares = 40%)\n"
        "  Governing Law:     Delaware (US)\n"
        "  Representations:   Assignor warrants clear title, no encumbrances,\n"
        "                     no third-party claims, no university ownership\n"
        "  Recordation:       Assignment recorded with USPTO and any foreign\n"
        "                     patent offices where applications are pending")

    pdf.sub("Key Terms of the Back-License")
    pdf.txt(
        "  Licensor:          Company B USA\n"
        "  Licensee:          Silan Technology\n"
        "  Scope:             Manufacturing of the ICU Respiratory Digital Twin\n"
        "                     device and components, per Company B USA specifications\n"
        "  Exclusivity:       Non-exclusive\n"
        "  Territory:         China (manufacturing only, not sales)\n"
        "  Royalty:           $0 (costs absorbed in manufacturing agreement pricing)\n"
        "  Duration:          Co-terminus with the Manufacturing Agreement\n"
        "  Termination:       Company B USA may terminate with 90-day notice\n"
        "  Sub-licensing:     Not permitted without written consent")

    pdf.sub("Dr. Dai's Protections Under This Option")
    pdf.info_box("Inventor Protection Mechanisms", [
        "1. EQUITY: 40% founder shares = largest individual stake",
        "2. VESTING ACCELERATION: If terminated without cause, 100% vests immediately",
        "3. IP VETO: Dr. Dai must consent to any sale, license, or sub-license of IP",
        "4. REVERSION CLAUSE: If Company B USA abandons the device (12 months of no",
        "   commercial activity + no active FDA submission), IP reverts to Dr. Dai",
        "5. ACADEMIC LICENSE: Perpetual right to use IP for research and teaching",
        "6. BOARD SEAT: Guaranteed as long as he holds >10% equity",
        "7. ANTI-DILUTION: Broad-based weighted-average protection on future rounds",
    ], GREEN)

    pdf.pros_cons(
        [
            "FDA: Applicant owns IP outright -- strongest position",
            "Investors: Clean IP title in a US entity under US law",
            "Acquirers: Single entity owns everything -- simplest M&A",
            "CFIUS: US entity owns critical technology",
            "No ongoing royalty negotiations or license disputes",
            "Dr. Dai retains value through equity (potentially greater)",
            "Reversion clause protects Dr. Dai if company fails",
            "Standard structure used by thousands of startups",
        ],
        [
            "Dr. Dai must trust the equity model over IP retention",
            "Assignment is legally permanent (reversion is the safety net)",
            "Cross-border IP assignment requires careful legal drafting",
            "China patent office recordation may take 3-6 months",
            "If Dr. Dai's equity is diluted below 10%, he loses board seat",
        ],
    )

    # ─── IP OPTION 2 ───
    pdf.add_page()
    pdf.option_header("IP Option 2", "Exclusive License to US Entity (China Retains Ownership)", ORANGE)
    pdf.conditional_badge("CONDITIONAL -- Weaker for FDA, workable")
    pdf.ln(2)

    pdf.sub("How It Works")
    pdf.txt(
        "Dr. Dai or Silan Technology retains legal ownership of all IP. Company B USA "
        "receives an exclusive, worldwide license to use the IP for the development, "
        "regulatory clearance, manufacturing, and commercialization of the ICU Respiratory "
        "Digital Twin device. The license is irrevocable for a fixed term (e.g., 20 years) "
        "or tied to the life of the underlying patents.")

    pdf.sub("Structure Diagram")
    pdf.diagram([
        "+---------------------------+   Exclusive License      +---------------------------+",
        "|   Dr. Dai / Silan Tech    | ========================>|    Company B USA           |",
        "|   (Chengdu, China)        |  (worldwide, irrevocable)|    (Delaware C-Corp)       |",
        "|                           |  (20-year or patent-life)|                            |",
        "|   RETAINS IP OWNERSHIP    |                          |    Exclusive licensee      |",
        "|   Licensor                |                          |    510(k) applicant        |",
        "+---------------------------+                          +----------------------------+",
        "",
        "Ownership stays in China.  Usage rights go to the US.",
    ])

    pdf.sub("Key License Terms")
    pdf.txt(
        "  Licensor:          Dr. Dai / Silan Technology\n"
        "  Licensee:          Company B USA\n"
        "  Scope:             All uses related to the ICU Respiratory Digital Twin\n"
        "  Exclusivity:       Exclusive worldwide (licensor cannot license to others)\n"
        "  Irrevocability:    Cannot be revoked except for material breach\n"
        "  Royalty:           Options -- (a) $0 with equity as consideration,\n"
        "                     (b) X% of net sales, (c) annual flat fee\n"
        "  Sub-license:       Company B USA may sub-license to contract manufacturers\n"
        "  Improvements:      All improvements by either party flow into the license")

    pdf.pros_cons(
        [
            "Dr. Dai retains formal IP ownership (may feel safer)",
            "No cross-border assignment paperwork / patent recordation",
            "Dr. Dai can use IP independently for China/APAC market",
            "License can include revenue-sharing provisions",
            "Faster to execute than a full assignment",
        ],
        [
            "FDA: Applicant does not own the technology -- weaker position",
            "FDA may request proof that license cannot be revoked",
            "Investors strongly dislike this -- IP risk sits outside the company",
            "Acquirer must negotiate with licensor separately (deal-breaker for some)",
            "CFIUS: Chinese entity controls critical medical device technology",
            "If Dr. Dai/Silan disputes arise, US company is vulnerable",
            "Royalty payments create ongoing cost and transfer pricing issues",
            "Insurance (D&O, E&O) may be more expensive due to IP structure",
            "Complicates future fundraising -- VCs may require conversion to Option 1",
        ],
    )

    pdf.info_box("FDA Impact", [
        "FDA does not require IP ownership for 510(k) clearance.",
        "However, FDA expects the applicant to control the technology.",
        "An exclusive, irrevocable license can satisfy this -- but reviewers",
        "may ask follow-up questions about the arrangement.",
        "Net: Workable, but adds 1-3 months to review timeline.",
    ], ORANGE)

    pdf.info_box("Investor Impact", [
        "Most US VCs will NOT invest under this structure.",
        "Due diligence will flag the IP risk immediately.",
        "If a Series A is planned, investors will likely require",
        "conversion to Option 1 (full assignment) as a condition.",
        "Net: This option works for angel/seed but blocks institutional rounds.",
    ], RED)

    # ─── IP OPTION 3 ───
    pdf.add_page()
    pdf.option_header("IP Option 3", "Split Ownership by Territory", RED)
    pdf.not_recommended_badge("NOT RECOMMENDED")
    pdf.ln(2)

    pdf.sub("How It Works")
    pdf.txt(
        "The IP is divided by geographic territory. Company B USA owns all rights for the "
        "United States (and optionally EU/other Western markets). Dr. Dai or Silan retains "
        "all rights for China, Asia-Pacific, and other territories. Each entity is free to "
        "commercialize independently in its assigned territory.")

    pdf.sub("Structure Diagram")
    pdf.diagram([
        "+---------------------------+           +---------------------------+",
        "|    Company B USA          |           |    Dr. Dai / Silan       |",
        "|    (Delaware C-Corp)      |           |    (Chengdu, China)      |",
        "|                           |           |                           |",
        "|  Owns: US patent rights   |           |  Owns: China/APAC patent |",
        "|  Owns: US software (c)    |           |  Owns: China software (c)|",
        "|  Market: USA, EU, Canada  |           |  Market: China, APAC     |",
        "|  510(k) applicant         |           |  NMPA applicant          |",
        "+---------------------------+           +---------------------------+",
        "",
        "        Coordination Agreement (cross-improvements, no-compete by territory)",
    ])

    pdf.pros_cons(
        [
            "Both entities are independent -- no cross-border control issues",
            "Dr. Dai can commercialize freely in China/APAC",
            "No need for full IP assignment agreement",
            "Each entity can fundraise independently in its market",
            "Silan can pursue NMPA registration in parallel",
        ],
        [
            "FDA: Unclear who owns 'the' technology -- split confuses reviewers",
            "Patents are not easily split by territory (especially US utility patents)",
            "Software copyrights are intrinsically worldwide -- hard to divide",
            "Trade secrets cannot be 'split' -- both parties know them",
            "Investors see two companies competing with the same technology",
            "Acquirer would only get half the IP -- significantly less valuable",
            "CFIUS: Chinese entity still controls critical technology",
            "Coordination agreement creates ongoing legal overhead",
            "Improvement allocation disputes are inevitable",
            "If one party modifies the technology, who owns the derivative?",
            "Two separate regulatory submissions (FDA + NMPA) = double cost",
        ],
    )

    pdf.info_box("Why This Fails for 510(k)", [
        "The FDA 510(k) submission requires a clear chain of IP ownership.",
        "Split ownership creates ambiguity about who controls the technology.",
        "If the Chinese entity independently modifies the device, the US",
        "510(k) may no longer represent the commercially marketed device.",
        "Net: Theoretically possible but practically unworkable for FDA.",
    ], RED)

    # ─── IP COMPARISON TABLE ───
    pdf.add_page()
    pdf.sub("IP Options -- Side-by-Side Comparison")
    pdf.ln(2)

    pdf.table(
        ["Criterion", "1: Full Assign", "2: Excl License", "3: Split"],
        [
            ("IP legal owner", "US entity", "China entity", "Both"),
            ("FDA strength", "Strongest", "Workable", "Weakest"),
            ("Investor appeal", "Highest", "Low-Moderate", "Very Low"),
            ("Acquirer appeal", "Highest", "Moderate", "Low"),
            ("CFIUS risk", "Lowest", "Moderate-High", "High"),
            ("Dr. Dai IP control", "Via equity + veto", "Retains ownership", "Retains China"),
            ("Formation complexity", "Moderate", "Low", "High"),
            ("Ongoing legal cost", "Low", "Moderate", "High"),
            ("Fundraising impact", "No friction", "Blocks VCs", "Blocks all"),
            ("Reversion possible", "Yes (contractual)", "N/A (still owns)", "N/A"),
            ("RECOMMENDATION", "YES", "CONDITIONAL", "NO"),
        ],
        [42, 42, 42, 42],
    )

    # ═══════════════════════════════════════
    # PART III: IP TRANSFER MECHANICS
    # ═══════════════════════════════════════
    pdf.add_page()
    pdf.sec("III", "IP Transfer Mechanics & Timeline")
    pdf.txt(
        "If Option 1 (Full Assignment) is selected, the following steps must be executed. "
        "Note: Per the inventor's business plan (v7), the initial IP transfer covers "
        "sEMG algorithms, MyoBus protocol, and related software. EIT IP transfer is a "
        "separate negotiation deferred to Series A (Year 1 Q2-Q4).\n\n"
        "The sEMG IP assignment should be completed before the FDA Pre-Submission meeting "
        "(M+2) so that Company B USA can demonstrate IP ownership to FDA reviewers.")

    pdf.sub("Transfer Checklist")
    pdf.txt(
        "  1. IP Inventory\n"
        "     Catalog ALL IP: patents, patent applications, copyrights, trade secrets,\n"
        "     know-how, source code, hardware designs, training data.\n"
        "     Identify current legal owner for each item.\n"
        "     Confirm no university, employer, or government claims.\n\n"
        "  2. IP Assignment Agreement\n"
        "     Drafted by US IP attorney (Delaware-governed).\n"
        "     Signed by Dr. Dai / Silan and Company B USA.\n"
        "     Consideration: founder equity (4M shares) documented in agreement.\n"
        "     Notarized and apostilled for international recognition.\n\n"
        "  3. Patent Office Recordation\n"
        "     USPTO: Record assignment for any US patent applications.\n"
        "     CNIPA (China): Record assignment for Chinese patent applications.\n"
        "     Other jurisdictions: PCT applications, EP applications, etc.\n"
        "     Timeline: 1-6 months depending on jurisdiction.\n\n"
        "  4. Software Copyright Registration\n"
        "     Register key software copyrights with US Copyright Office.\n"
        "     Provides legal presumption of ownership in US courts.\n"
        "     Cost: ~$65 per registration.\n\n"
        "  5. Trade Secret Documentation\n"
        "     Document trade secrets in a confidential registry.\n"
        "     Implement access controls (who can see what).\n"
        "     Company B USA must demonstrate 'reasonable measures' to protect.\n\n"
        "  6. Manufacturing Back-License Execution\n"
        "     Drafted concurrently with the Assignment Agreement.\n"
        "     Defines scope, limitations, and termination rights.\n"
        "     Tied to a Master Manufacturing Agreement with Silan.")

    pdf.sub("Estimated Timeline (from decision to completion)")
    pdf.table(
        ["Step", "Duration", "Dependencies", "Cost"],
        [
            ("IP inventory + audit", "2-3 weeks", "Dr. Dai cooperation", "$5K-$10K"),
            ("Assignment agreement draft", "2-3 weeks", "IP attorney engagement", "$8K-$15K"),
            ("Negotiation + signature", "1-2 weeks", "All parties aligned", "Included"),
            ("USPTO recordation", "2-4 weeks", "Signed agreement", "$500-$1K"),
            ("CNIPA recordation", "2-6 months", "Chinese patent agent", "$2K-$5K"),
            ("Back-license execution", "1-2 weeks", "Assignment complete", "$3K-$5K"),
            ("Copyright registration", "3-6 months", "Filed with USCO", "$500-$1K"),
            ("TOTAL", "3-4 months*", "* Concurrent tasks", "$19K-$37K"),
        ],
        [48, 30, 48, 30],
    )

    pdf.set_font("Helvetica", "I", 9)
    pdf.set_text_color(*GRAY)
    pdf.txt(
        "* CNIPA recordation and copyright registration can proceed in parallel with "
        "FDA Pre-Sub preparation. The key milestone is the signed Assignment Agreement, "
        "which can be completed within 6-8 weeks of engagement.")

    # ═══════════════════════════════════════
    # PART IV: COMBINED RECOMMENDATION
    # ═══════════════════════════════════════
    pdf.add_page()
    pdf.sec("IV", "Combined Recommendation")

    pdf.sub("Recommended Structure", GREEN)
    pdf.txt(
        "Based on the FDA 510(k) pathway, US investor expectations, CFIUS risk management, "
        "and acquisition readiness, the recommended combination is:\n\n"
        "  Corporate Structure:  Option A -- Standard Delaware C-Corp (single entity)\n"
        "  IP Strategy:          Option 1 -- Full assignment to US entity + back-license\n\n"
        "This is the standard, proven path for US medical device startups with foreign-origin "
        "technology. It is the structure expected by institutional investors, FDA reviewers, "
        "and potential acquirers.")

    pdf.sub("Why This Combination Works")
    pdf.txt(
        "  FDA: The 510(k) applicant owns the technology. No questions about IP control.\n"
        "  Investors: Clean cap table, single entity, IP in US jurisdiction.\n"
        "  CFIUS: US entity owns IP, US-majority board, no foreign control.\n"
        "  Acquirers: One entity to buy, one IP portfolio, one cap table.\n"
        "  Dr. Dai: Protected by equity (40%), vesting acceleration, IP veto, reversion.\n"
        "  Lawrence: Protected by preferred stock, liquidation preference, protective provisions.\n"
        "  Lon: Protected by equity (15%), vesting, double-trigger acceleration.\n"
        "  Silan: Protected by manufacturing agreement (revenue stream continues).")

    pdf.sub("Decision Points for Today's Discussion")
    pdf.info_box("Questions That Must Be Answered", [
        "1. Who currently holds the IP? (Dr. Dai personally? Silan? University?)",
        "2. Is Dr. Dai willing to assign IP in exchange for founder equity?",
        "3. Is Lawrence aligned on IP residing in the US entity?",
        "4. Are there any co-inventors, collaborators, or government grants?",
        "5. Are there any third-party licenses (software, algorithms, hardware)?",
        "6. What is Lawrence's citizenship/residency status? (CFIUS impact)",
        "7. What is Dr. Dai's citizenship/residency status? (US citizen,",
        "   green card, visa, or none? Relatives in US with status?)",
        "8. Target equity split: 40/30/15/15 acceptable as a starting point?",
        "9. Is a 3-person board (2 US seats + 1 inventor seat) acceptable?",
    ])

    pdf.ln(2)
    pdf.sub("Next Steps After Decision")
    pdf.txt(
        "  1. Engage Delaware registered agent + file Certificate of Incorporation\n"
        "  2. Engage US IP attorney to draft IP Assignment Agreement\n"
        "  3. Draft Term Sheet for Lawrence's investment (amount, valuation, terms)\n"
        "  4. Draft Restricted Stock Agreements (Dr. Dai + Lon)\n"
        "  5. Draft Master Services Agreement (Arch Medical Management, LLC)\n"
        "  6. Draft Manufacturing Agreement with Silan Technology\n"
        "  7. File voluntary CFIUS declaration (if Lawrence or Dr. Dai are foreign persons)\n"
        "  8. Prepare FDA Pre-Submission package (requires IP ownership documented)")

    pdf.ln(4)
    pdf.set_draw_color(*BLUE)
    mid = pdf.w / 2
    pdf.line(mid - 40, pdf.get_y(), mid + 40, pdf.get_y())
    pdf.ln(4)
    pdf.set_font("Helvetica", "I", 9)
    pdf.set_text_color(*GRAY)
    pdf.multi_cell(0, 5,
        "This document is for internal decision-making purposes only. It does not "
        "constitute legal advice. All structural decisions should be reviewed by "
        "a qualified corporate attorney and IP counsel before execution.",
        align="C")

    path = os.path.join(OUT_DIR, "Corporate_Structure_IP_Options.pdf")
    pdf.output(path)
    return path


if __name__ == "__main__":
    p = build()
    print(f"Generated: {p}")
