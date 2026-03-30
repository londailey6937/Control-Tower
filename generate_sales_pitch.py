#!/usr/bin/env python3
"""
Generate a bilingual (EN + CN) sales pitch PDF for the Shanghai sales team.

Entity: 510kBridge Consulting (Shanghai) Co., Ltd. -- WFOE
Target audience: Chinese medical device companies seeking US FDA 510(k) clearance

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
        self.cell(0, 4, _a("CONFIDENTIAL -- 510kBridge Consulting  |  Client Sales Pitch"),
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
        self.cell(0, 4, "机密 -- 510kBridge Consulting  |  客户销售方案", align="R")
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
    pdf.cell(0, 10, "Client Sales Pitch", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 13)
    pdf.cell(0, 7, "FDA 510(k) Project Management & Regulatory Services",
             align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "I", 10)
    pdf.cell(0, 6, _a("Your Bridge to the US Medical Device Market"),
             align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)
    pdf.set_draw_color(*SalesPitchBase.WHITE)
    pdf.set_line_width(0.3)
    pdf.line(40, pdf.get_y(), 170, pdf.get_y())
    pdf.ln(3)
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(0, 5, _a("Prepared by:  510kBridge Consulting (Shanghai) Co., Ltd."),
             align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 9)
    pdf.cell(0, 5, _a("Wholly Foreign-Owned Enterprise (WFOE)"),
             align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 8)
    pdf.cell(0, 5, _a("US Headquarters:  Pilot Software LLC dba 510kBridge  |  Oregon, USA"),
             align="C", new_x="LMARGIN", new_y="NEXT")

    pdf.ln(8)
    pdf.set_text_color(*SalesPitchBase.DARK)

    # ── 1. WHY YOU NEED A US-BASED 510(k) PARTNER ──
    pdf.section("1", "Why You Need a US-Based 510(k) Partner", page_break=False)
    pdf.body(
        "Entering the US medical device market requires navigating a complex regulatory "
        "landscape that is unfamiliar to most Chinese manufacturers. The FDA 510(k) pathway "
        "demands substantial evidence of safety and effectiveness, rigorous quality system "
        "compliance, and precise documentation -- all in English and conforming to US "
        "regulatory expectations.\n\n"
        "Common pitfalls for Chinese companies include:\n"
    )
    pdf.bullet("25-30% of 510(k) submissions are refused within 15 days for documentation deficiencies",
               "High RTA Rejection Rate: ")
    pdf.bullet("Incorrectly identified predicates can invalidate your entire regulatory strategy",
               "Wrong Predicate Device: ")
    pdf.bullet("US law requires foreign manufacturers to designate a US Agent for FDA "
               "registration, correspondence, and recall coordination",
               "US Agent Requirement: ")
    pdf.bullet("Non-compliant Chinese filings cost months of rework and re-submission fees",
               "Rework Costs: ")

    pdf.callout_box(
        "510kBridge bridges the gap between Chinese manufacturing excellence and US "
        "regulatory requirements -- with bilingual support, proven project management, "
        "and a technology platform purpose-built for FDA 510(k) programs."
    )

    # ── 2. OUR SERVICE TIERS ──
    pdf.section("2", "Service Tiers & Pricing")
    pdf.body("We offer flexible engagement models scaled to your needs and budget:")

    pdf.tier_table(
        rows=[
            ["SaaS Starter", "$500/mo", "2 seats", "Control Tower dashboard, bilingual wizard, "
             "dual-track milestones, document control, risk & budget tracking"],
            ["SaaS Growth", "$1,000/mo", "5 seats", "All Starter features + regulatory tracker, "
             "audit trail, supplier management, cap table"],
            ["SaaS Scale", "$2,000/mo", "10 seats", "All Growth + FDA Comms Center, message board, "
             "cash/runway, US investment tracking"],
            ["Professional PM", "$10K-25K/mo", "Unlimited", "Dedicated PMP project manager, "
             "Q-Sub automation, US Agent, gate reviews, supplier coordination"],
            ["Enterprise", "$50K+/project", "Unlimited", "End-to-end: regulatory strategy, "
             "510(k) preparation & submission, US entity formation, DHF readiness"],
        ],
        col_widths=[32, 24, 18, 116],
        header=["Tier", "Price", "Seats", "Included Features"],
    )

    # ── 3. FDA 510(k) PROCESS ──
    pdf.section("3", "The FDA 510(k) Process -- What to Expect")
    pdf.body("A typical 510(k) submission follows six phases over 9-18 months:")

    pdf.tier_table(
        rows=[
            ["Phase 1: Pathway Analysis", "1-3 mo",
             "Identify predicate devices, determine classification, develop "
             "regulatory strategy, prepare Pre-Submission (Q-Sub) package"],
            ["Phase 2: Design Controls & Testing", "4-9 mo",
             "IEC 60601 safety ($15K-$40K), EMC ($15K-$30K), "
             "biocompatibility ISO 10993 ($10K-$25K), software V&V IEC 62304 ($20K-$50K), "
             "usability IEC 62366 ($15K-$40K)"],
            ["Phase 3: Quality System", "Ongoing",
             "ISO 13485 certification ($15K-$30K), establish CAPA system, "
             "document control, design history file (DHF)"],
            ["Phase 4: Submission Build", "1-2 mo",
             "Compile DHF, executive summary, substantial equivalence argument, "
             "RTA self-check against FDA guidance"],
            ["Phase 5: FDA Submission", "Day 1",
             "eSTAR electronic submission, user fee payment ($6,517 small business / "
             "$26,067 standard)"],
            ["Phase 6: FDA Review", "3-6 mo",
             "RTA check (15-30 days), substantive review (60-90 days), "
             "additional information requests if needed (up to 180 days each)"],
        ],
        col_widths=[44, 14, 132],
        header=["Phase", "Duration", "Key Activities"],
    )

    pdf.ln(2)
    pdf.body("Total estimated cost per device module: $130K-$320K "
             "(testing, consulting, FDA fees, and certification).")

    # ── 4. CONTROL TOWER PLATFORM ──
    pdf.section("4", "Control Tower -- Your FDA Command Center")
    pdf.body(
        "Every engagement includes access to our proprietary Control Tower platform -- "
        "a real-time, bilingual (EN/CN) dashboard with 16 integrated tabs:"
    )
    tabs = [
        ("Dual-Track", "Technical & regulatory milestones running in parallel"),
        ("Gate System", "Formal decision checkpoints: Proceed / Need Data / Stop"),
        ("Regulatory Tracker", "IEC 60601, ISO 10993, 21 CFR 820 compliance matrix"),
        ("Risk Dashboard", "ISO 14971 risk management with controls & mitigation status"),
        ("Audit Trail", "Complete change history for every decision and document revision"),
        ("Document Control", "Design History File library with version control & approval workflow"),
        ("Actions", "Task board tied to milestone deliverables"),
        ("Timeline", "Business-friendly view of technical milestones"),
        ("Budget", "Cost tracking: planned vs. actuals by category"),
        ("Cash / Runway", "Burn rate monitoring, funding rounds, critical date forecasting"),
        ("US Investment", "Fundraising pipeline and investor relationship tracking"),
        ("Cap Table", "Equity management, shareholder tracking, vesting schedules"),
        ("Resources", "Team allocation and capacity planning"),
        ("Suppliers", "Vendor management, PO status, and lead times"),
        ("Message Board", "Stakeholder Q&A thread and announcements"),
        ("FDA Comms", "Pre-Sub coordination, RTA checklist, Q-Sub automation (Scale/PM tier)"),
    ]
    for name, desc in tabs:
        pdf.bullet(desc, f"{name}: ")

    pdf.callout_box(
        "Live demo available at control-tower-bmx.pages.dev -- "
        "ask your 510kBridge representative for a guided walkthrough."
    )

    # ── 5. DEVICE CATEGORY TEMPLATES ──
    pdf.section("5", "7 Pre-Built Device Category Templates")
    pdf.body(
        "When you start a new project, select your device category and the Control Tower "
        "auto-configures regulatory standards, risk profiles, predicate examples, budget "
        "categories, and estimated timelines:"
    )
    templates = [
        ["Respiratory", "21 CFR 868", "18 months", "Ventilators, CPAP/BiPAP, nebulizers, airway management"],
        ["Cardiovascular", "21 CFR 870", "18 months", "ECG monitors, BP devices, cardiac catheters, stents"],
        ["Orthopedic", "21 CFR 888", "24 months", "Joint implants, bone plates, spinal devices, fixation"],
        ["IVD", "21 CFR 862-864", "15 months", "Analyzers, immunoassay, hematology, POC, molecular dx"],
        ["Imaging & Monitoring", "21 CFR 892", "15 months", "Ultrasound, X-ray, EEG, pulse oximeters, SaMD"],
        ["Rehabilitation", "21 CFR 890", "20 months", "Exoskeletons, neurostimulators, EMG biofeedback"],
        ["SaMD", "21 CFR 892.2020", "12 months", "Clinical decision support, AI/ML, telehealth, PACS"],
    ]
    pdf.tier_table(
        rows=templates,
        col_widths=[28, 26, 20, 116],
        header=["Category", "CFR Part", "Duration", "Device Examples"],
    )

    # ── 6. US ENTITY & COMPLIANCE REQUIREMENTS ──
    pdf.section("6", "US Entity & Compliance Requirements")
    pdf.body(
        "Foreign manufacturers selling devices in the US must meet several structural "
        "and regulatory requirements. We guide you through every step:"
    )

    pdf.key_value_row("US Agent (Required)", "$3,000-$6,000/year -- all foreign manufacturers must "
                      "designate a US person as point of contact for FDA", label_w=45)
    pdf.key_value_row("US Entity Formation", "Delaware C-Corp recommended for investors; ~$2K-$5K "
                      "setup + $300/yr registered agent", label_w=45)
    pdf.key_value_row("FDA Establishment", "Annual registration + device listing -- required before "
                      "commercial distribution", label_w=45)
    pdf.key_value_row("Quality System", "21 CFR 820 (QSR) / ISO 13485 -- continuous compliance, "
                      "CAPA system, MDR reporting", label_w=45)
    pdf.key_value_row("Document Storage", "FDA requires Design History File (DHF), Device Master Record "
                      "(DMR), and Device History Record (DHR) to be maintained and accessible for "
                      "inspection. Records must be legible, in English, and retained for the "
                      "lifetime of the device plus 2 years.", label_w=45)
    pdf.key_value_row("Labeling", "US labeling must comply with 21 CFR 801 -- English language, "
                      "intended use, warnings, UDI compliance", label_w=45)
    pdf.key_value_row("Post-Market", "Complaint handling, MDR adverse event reporting, periodic "
                      "updates, recall readiness", label_w=45)

    pdf.callout_box(
        "IMPORTANT: 21 CFR 820.180 requires that all quality records be maintained at the "
        "establishment where activities occur or be reasonably accessible to FDA inspectors. "
        "For foreign manufacturers, this means your US Agent must be able to provide records "
        "to FDA within a reasonable time frame upon request. Our Control Tower platform "
        "stores and organizes all project documentation in a US-hosted, audit-ready format."
    )

    # ── 7. WHY 510kBridge ──
    pdf.section("7", "Why Choose 510kBridge?")
    pdf.bullet("US-citizen PMP (Stanford SCPM) managing FDA communications and project execution",
               "American Project Leadership: ")
    pdf.bullet("Native Mandarin-speaking team in Shanghai handles all client communications",
               "Bilingual Team: ")
    pdf.bullet("16-tab Control Tower with real-time dashboards, not spreadsheets or emails",
               "Purpose-Built Technology: ")
    pdf.bullet("We handle your FDA address, correspondence, and inspection readiness",
               "US Agent Services: ")
    pdf.bullet("7 pre-configured device templates auto-load standards, risks, and timelines",
               "Category Templates: ")
    pdf.bullet("From Pre-Sub Q-meeting through FDA clearance letter",
               "End-to-End Coverage: ")
    pdf.bullet("Shanghai WFOE office provides local contracts, invoicing in RMB, "
               "and face-to-face meetings",
               "Local Presence: ")

    # ── 8. TYPICAL ENGAGEMENT TIMELINE ──
    pdf.section("8", "Typical Engagement Timeline")
    timeline = [
        ["Week 1", "Kickoff & onboarding", "Template selection, Control Tower setup, "
         "team access provisioning"],
        ["Month 1", "Regulatory strategy", "Predicate device search, classification "
         "confirmation, pathway selection"],
        ["Month 2-3", "Pre-Submission", "Q-Sub package preparation, FDA meeting scheduling "
         "(75-90 day lead time)"],
        ["Month 3-9", "Testing & V&V", "Standards testing, design verification, "
         "biocompatibility, usability study"],
        ["Month 9-10", "Submission build", "DHF compilation, RTA self-check, "
         "executive summary, eSTAR packaging"],
        ["Month 10-15", "FDA review", "Submission, RTA clearance, substantive review, "
         "AI response management"],
        ["Post-Clearance", "Market entry", "Establishment registration, device listing, "
         "labeling compliance, QMS maintenance"],
    ]
    pdf.tier_table(
        rows=timeline,
        col_widths=[25, 35, 130],
        header=["When", "Milestone", "Key Activities"],
    )

    # ── 9. NEXT STEPS ──
    pdf.section("9", "Next Steps")
    pdf.body("Ready to start your US market entry journey? Here is how to begin:")
    pdf.bullet("Schedule a free 30-minute Control Tower demo with your 510kBridge rep", "1. ")
    pdf.bullet("Share your device description and target predicate (if known)", "2. ")
    pdf.bullet("Receive a customized regulatory pathway assessment and cost estimate", "3. ")
    pdf.bullet("Select your service tier and begin onboarding", "4. ")

    pdf.ln(3)
    pdf.body("Contact us:")
    pdf.key_value_row("Shanghai Office:", "510kBridge Consulting (Shanghai) Co., Ltd.", label_w=32)
    pdf.key_value_row("US Office:", "Pilot Software LLC dba 510kBridge  |  Oregon, USA", label_w=32)
    pdf.key_value_row("Website:", "510kbridge.com  |  control-tower-bmx.pages.dev", label_w=32)
    pdf.key_value_row("WeChat:", "510kBridge", label_w=32)
    pdf.key_value_row("Email:", "info@510kbridge.com", label_w=32)

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
    pdf.cell(0, 10, "\u5ba2\u6237\u9500\u552e\u65b9\u6848", align="C",
             new_x="LMARGIN", new_y="NEXT")       # 客户销售方案
    pdf._set_font("", 13)
    pdf.cell(0, 7, "FDA 510(k) \u9879\u76ee\u7ba1\u7406\u4e0e\u6cd5\u89c4\u670d\u52a1",
             align="C", new_x="LMARGIN", new_y="NEXT")  # 项目管理与法规服务
    pdf._set_font("I", 10)
    pdf.cell(0, 6, "\u60a8\u901a\u5f80\u7f8e\u56fd\u533b\u7597\u5668\u68b0\u5e02\u573a\u7684\u6865\u6881",
             align="C", new_x="LMARGIN", new_y="NEXT")  # 您通往美国医疗器械市场的桥梁
    pdf.ln(2)
    pdf.set_draw_color(*SalesPitchBase.WHITE)
    pdf.set_line_width(0.3)
    pdf.line(40, pdf.get_y(), 170, pdf.get_y())
    pdf.ln(3)
    pdf._set_font("B", 10)
    pdf.cell(0, 5, "\u7f16\u5236\u5355\u4f4d\uff1a510kBridge Consulting (\u4e0a\u6d77) Co., Ltd.",
             align="C", new_x="LMARGIN", new_y="NEXT")  # 编制单位
    pdf._set_font("", 9)
    pdf.cell(0, 5, "\u5916\u5546\u72ec\u8d44\u4f01\u4e1a (WFOE)",
             align="C", new_x="LMARGIN", new_y="NEXT")  # 外商独资企业
    pdf._set_font("", 8)
    pdf.cell(0, 5, "\u7f8e\u56fd\u603b\u90e8\uff1aPilot Software LLC dba 510kBridge  |  \u4fc4\u52d2\u5188\u5dde",
             align="C", new_x="LMARGIN", new_y="NEXT")  # 美国总部 / 俄勒冈州

    pdf.ln(8)
    pdf.set_text_color(*SalesPitchBase.DARK)

    # ── 1 ──
    pdf.section("1", "\u4e3a\u4ec0\u4e48\u60a8\u9700\u8981\u7f8e\u56fd510(k)\u5408\u4f5c\u4f19\u4f34")
    # 为什么您需要美国510(k)合作伙伴
    pdf.body(
        "\u8fdb\u5165\u7f8e\u56fd\u533b\u7597\u5668\u68b0\u5e02\u573a\u9700\u8981\u5e94\u5bf9"
        "\u590d\u6742\u7684\u6cd5\u89c4\u73af\u5883\uff0c\u8fd9\u5bf9\u5927\u591a\u6570\u4e2d"
        "\u56fd\u5236\u9020\u5546\u6765\u8bf4\u662f\u964c\u751f\u7684\u3002FDA 510(k)\u9014\u5f84"
        "\u8981\u6c42\u63d0\u4f9b\u5145\u5206\u7684\u5b89\u5168\u6027\u548c\u6709\u6548\u6027"
        "\u8bc1\u636e\u3001\u4e25\u683c\u7684\u8d28\u91cf\u4f53\u7cfb\u5408\u89c4\u4ee5\u53ca"
        "\u7cbe\u786e\u7684\u6587\u6863 -- \u5168\u90e8\u7528\u82f1\u6587\u5e76\u7b26\u5408"
        "\u7f8e\u56fd\u6cd5\u89c4\u8981\u6c42\u3002\n\n"
        "\u4e2d\u56fd\u4f01\u4e1a\u5e38\u89c1\u95ee\u9898\uff1a"
    )
    pdf.bullet("25-30%\u7684510(k)\u7533\u8bf7\u572815\u5929\u5185\u56e0\u6587\u4ef6\u7f3a\u9677\u88ab\u62d2\u7edd",
               "\u9ad8RTA\u62d2\u7edd\u7387\uff1a")
    pdf.bullet("\u9519\u8bef\u7684\u5bf9\u6bd4\u5668\u68b0\u4f1a\u5bfc\u81f4\u6574\u4e2a\u6cd5\u89c4\u7b56\u7565\u5931\u6548",
               "\u5bf9\u6bd4\u5668\u68b0\u9009\u62e9\u9519\u8bef\uff1a")
    pdf.bullet("\u7f8e\u56fd\u6cd5\u5f8b\u8981\u6c42\u5916\u56fd\u5236\u9020\u5546\u6307\u5b9a"
               "\u7f8e\u56fd\u4ee3\u7406\u4eba\u7528\u4e8eFDA\u6ce8\u518c\u3001\u901a\u4fe1\u548c\u53ec\u56de\u534f\u8c03",
               "\u7f8e\u56fd\u4ee3\u7406\u4eba\u8981\u6c42\uff1a")
    pdf.bullet("\u4e0d\u5408\u89c4\u7684\u7533\u8bf7\u4f1a\u5bfc\u81f4\u6570\u6708\u7684\u8fd4\u5de5\u548c\u91cd\u65b0\u63d0\u4ea4\u8d39\u7528",
               "\u8fd4\u5de5\u6210\u672c\uff1a")

    pdf.callout_box(
        "510kBridge\u5f25\u5408\u4e2d\u56fd\u5236\u9020\u5b9e\u529b\u4e0e\u7f8e\u56fd\u6cd5\u89c4"
        "\u8981\u6c42\u4e4b\u95f4\u7684\u5dee\u8ddd -- \u63d0\u4f9b\u53cc\u8bed\u652f\u6301\u3001"
        "\u6210\u719f\u7684\u9879\u76ee\u7ba1\u7406\u4ee5\u53ca\u4e13\u4e3aFDA 510(k)\u9879\u76ee"
        "\u6253\u9020\u7684\u6280\u672f\u5e73\u53f0\u3002"
    )

    # ── 2 ──
    pdf.section("2", "\u670d\u52a1\u5c42\u7ea7\u4e0e\u4ef7\u683c")  # 服务层级与价格
    pdf.body("\u6211\u4eec\u63d0\u4f9b\u7075\u6d3b\u7684\u5408\u4f5c\u6a21\u5f0f\uff0c\u6839\u636e\u60a8\u7684\u9700\u6c42\u548c\u9884\u7b97\u8fdb\u884c\u8c03\u6574\uff1a")

    pdf.tier_table(
        rows=[
            ["SaaS \u5165\u95e8\u7248", "$500/\u6708", "2\u5e2d\u4f4d",
             "Control Tower\u4eea\u8868\u677f\u3001\u53cc\u8bed\u5411\u5bfc\u3001\u53cc\u8f68\u91cc\u7a0b\u7891\u3001\u6587\u6863\u7ba1\u63a7\u3001\u98ce\u9669\u548c\u9884\u7b97\u8ddf\u8e2a"],
            ["SaaS \u589e\u957f\u7248", "$1,000/\u6708", "5\u5e2d\u4f4d",
             "\u5305\u542b\u5165\u95e8\u7248\u6240\u6709\u529f\u80fd + \u6cd5\u89c4\u8ddf\u8e2a\u5668\u3001\u5ba1\u8ba1\u8ddf\u8e2a\u3001\u4f9b\u5e94\u5546\u7ba1\u7406\u3001\u80a1\u6743\u8868"],
            ["SaaS \u89c4\u6a21\u7248", "$2,000/\u6708", "10\u5e2d\u4f4d",
             "\u5305\u542b\u589e\u957f\u7248\u6240\u6709\u529f\u80fd + FDA\u901a\u4fe1\u4e2d\u5fc3\u3001\u6d88\u606f\u677f\u3001\u73b0\u91d1/\u8dd1\u9053\u3001\u7f8e\u56fd\u6295\u8d44\u8ddf\u8e2a"],
            ["\u4e13\u4e1aPM", "$10K-25K/\u6708", "\u65e0\u9650",
             "\u4e13\u5c5ePMP\u9879\u76ee\u7ecf\u7406\u3001Q-Sub\u81ea\u52a8\u5316\u3001\u7f8e\u56fd\u4ee3\u7406\u4eba\u3001\u95e8\u5ba1\u67e5\u3001\u4f9b\u5e94\u5546\u534f\u8c03"],
            ["\u4f01\u4e1a\u7248", "$50K+/\u9879\u76ee", "\u65e0\u9650",
             "\u7aef\u5230\u7aef\u670d\u52a1\uff1a\u6cd5\u89c4\u7b56\u7565\u3001510(k)\u51c6\u5907\u4e0e\u63d0\u4ea4\u3001\u7f8e\u56fd\u5b9e\u4f53\u7ec4\u5efa\u3001DHF\u5c31\u7eea"],
        ],
        col_widths=[28, 26, 16, 120],
        header=["\u5c42\u7ea7", "\u4ef7\u683c", "\u5e2d\u4f4d", "\u5305\u542b\u529f\u80fd"],
    )

    # ── 3 ──
    pdf.section("3", "FDA 510(k)\u6d41\u7a0b -- \u671f\u671b\u4e8b\u9879")
    pdf.body("\u5178\u578b\u7684510(k)\u7533\u8bf7\u5206\u4e3a\u516d\u4e2a\u9636\u6bb5\uff0c\u5386\u65f69-18\u4e2a\u6708\uff1a")

    pdf.tier_table(
        rows=[
            ["\u7b2c1\u9636\u6bb5\uff1a\u9014\u5f84\u5206\u6790", "1-3\u4e2a\u6708",
             "\u786e\u5b9a\u5bf9\u6bd4\u5668\u68b0\u3001\u5206\u7c7b\u786e\u8ba4\u3001\u5236\u5b9a"
             "\u6cd5\u89c4\u7b56\u7565\u3001\u51c6\u5907Pre-Submission (Q-Sub)\u6587\u4ef6\u5305"],
            ["\u7b2c2\u9636\u6bb5\uff1a\u8bbe\u8ba1\u63a7\u5236\u4e0e\u6d4b\u8bd5", "4-9\u4e2a\u6708",
             "IEC 60601\u5b89\u5168($15K-$40K)\u3001EMC($15K-$30K)\u3001"
             "ISO 10993\u751f\u7269\u76f8\u5bb9\u6027($10K-$25K)\u3001IEC 62304\u8f6f\u4ef6V&V($20K-$50K)\u3001"
             "IEC 62366\u53ef\u7528\u6027($15K-$40K)"],
            ["\u7b2c3\u9636\u6bb5\uff1a\u8d28\u91cf\u4f53\u7cfb", "\u6301\u7eed",
             "ISO 13485\u8ba4\u8bc1($15K-$30K)\u3001\u5efa\u7acbCAPA\u7cfb\u7edf\u3001"
             "\u6587\u6863\u7ba1\u63a7\u3001\u8bbe\u8ba1\u5386\u53f2\u6587\u4ef6(DHF)"],
            ["\u7b2c4\u9636\u6bb5\uff1a\u63d0\u4ea4\u7f16\u5236", "1-2\u4e2a\u6708",
             "\u7f16\u8bd1DHF\u3001\u6267\u884c\u6458\u8981\u3001\u5b9e\u8d28\u7b49\u6548\u8bba\u8bc1\u3001"
             "RTA\u81ea\u67e5"],
            ["\u7b2c5\u9636\u6bb5\uff1aFDA\u63d0\u4ea4", "\u7b2c1\u5929",
             "eSTAR\u7535\u5b50\u63d0\u4ea4\u3001\u7528\u6237\u8d39\u7f34\u7eb3"
             "(\u5c0f\u4f01\u4e1a$6,517 / \u6807\u51c6$26,067)"],
            ["\u7b2c6\u9636\u6bb5\uff1aFDA\u5ba1\u67e5", "3-6\u4e2a\u6708",
             "RTA\u68c0\u67e5(15-30\u5929)\u3001\u5b9e\u8d28\u5ba1\u67e5(60-90\u5929)\u3001"
             "\u5982\u9700\u8981\u8865\u5145\u4fe1\u606f\u8bf7\u6c42(\u6bcf\u6b21\u6700\u591a180\u5929)"],
        ],
        col_widths=[44, 14, 132],
        header=["\u9636\u6bb5", "\u5468\u671f", "\u5173\u952e\u6d3b\u52a8"],
    )

    pdf.ln(2)
    pdf.body("\u6bcf\u4e2a\u5668\u68b0\u6a21\u5757\u7684\u603b\u4f30\u8ba1\u6210\u672c\uff1a"
             "$130K-$320K\uff08\u6d4b\u8bd5\u3001\u54a8\u8be2\u3001FDA\u8d39\u7528\u548c\u8ba4\u8bc1\uff09\u3002")

    # ── 4 ──
    pdf.section("4", "Control Tower -- \u60a8\u7684FDA\u6307\u6325\u4e2d\u5fc3")
    pdf.body(
        "\u6bcf\u6b21\u5408\u4f5c\u5747\u5305\u542b\u6211\u4eec\u4e13\u6709Control Tower\u5e73\u53f0"
        "\u7684\u8bbf\u95ee\u6743\u9650 -- \u5b9e\u65f6\u53cc\u8bed(\u4e2d/\u82f1)\u4eea\u8868\u677f"
        "\uff0c\u96c616\u4e2a\u529f\u80fd\u6a21\u5757\uff1a"
    )
    tabs_cn = [
        ("\u53cc\u8f68\u8ddf\u8e2a", "\u6280\u672f\u4e0e\u6cd5\u89c4\u91cc\u7a0b\u7891\u5e76\u884c\u8fd0\u884c"),
        ("\u95e8\u7cfb\u7edf", "\u6b63\u5f0f\u51b3\u7b56\u68c0\u67e5\u70b9\uff1a\u7ee7\u7eed / \u9700\u8981\u6570\u636e / \u505c\u6b62"),
        ("\u6cd5\u89c4\u8ddf\u8e2a\u5668", "IEC 60601\u3001ISO 10993\u300121 CFR 820\u5408\u89c4\u77e9\u9635"),
        ("\u98ce\u9669\u4eea\u8868\u677f", "ISO 14971\u98ce\u9669\u7ba1\u7406\uff0c\u63a7\u5236\u4e0e\u7f13\u89e3\u72b6\u6001"),
        ("\u5ba1\u8ba1\u8ddf\u8e2a", "\u6bcf\u4e2a\u51b3\u7b56\u548c\u6587\u6863\u4fee\u8ba2\u7684\u5b8c\u6574\u53d8\u66f4\u5386\u53f2"),
        ("\u6587\u6863\u63a7\u5236", "\u8bbe\u8ba1\u5386\u53f2\u6587\u4ef6\u5e93\uff0c\u7248\u672c\u63a7\u5236\u548c\u5ba1\u6279\u5de5\u4f5c\u6d41"),
        ("\u884c\u52a8\u9879", "\u4e0e\u91cc\u7a0b\u7891\u4ea4\u4ed8\u7269\u5173\u8054\u7684\u4efb\u52a1\u677f"),
        ("\u65f6\u95f4\u7ebf", "\u6280\u672f\u91cc\u7a0b\u7891\u7684\u4e1a\u52a1\u53cb\u597d\u89c6\u56fe"),
        ("\u9884\u7b97", "\u6309\u7c7b\u522b\u8ddf\u8e2a\u6210\u672c\uff1a\u8ba1\u5212 vs. \u5b9e\u9645"),
        ("\u73b0\u91d1/\u8dd1\u9053", "\u71c3\u70e7\u7387\u76d1\u63a7\u3001\u878d\u8d44\u8f6e\u6b21\u3001\u5173\u952e\u65e5\u671f\u9884\u6d4b"),
        ("\u7f8e\u56fd\u6295\u8d44", "\u878d\u8d44\u7ba1\u9053\u548c\u6295\u8d44\u8005\u5173\u7cfb\u8ddf\u8e2a"),
        ("\u80a1\u6743\u8868", "\u80a1\u6743\u7ba1\u7406\u3001\u80a1\u4e1c\u8ddf\u8e2a\u3001\u5f52\u5c5e\u8ba1\u5212"),
        ("\u8d44\u6e90", "\u56e2\u961f\u5206\u914d\u548c\u80fd\u529b\u89c4\u5212"),
        ("\u4f9b\u5e94\u5546", "\u4f9b\u5e94\u5546\u7ba1\u7406\u3001\u91c7\u8d2d\u8ba2\u5355\u72b6\u6001\u3001\u4ea4\u8d27\u65f6\u95f4"),
        ("\u6d88\u606f\u677f", "\u5229\u76ca\u76f8\u5173\u8005\u95ee\u7b54\u548c\u516c\u544a"),
        ("FDA\u901a\u4fe1", "Pre-Sub\u534f\u8c03\u3001RTA\u6e05\u5355\u3001Q-Sub\u81ea\u52a8\u5316\uff08\u89c4\u6a21\u7248/PM\u5c42\u7ea7\uff09"),
    ]
    for name, desc in tabs_cn:
        pdf.bullet(desc, f"{name}\uff1a")

    pdf.callout_box(
        "\u5728\u7ebf\u6f14\u793a\uff1acontrol-tower-bmx.pages.dev -- "
        "\u8bf7\u8054\u7cfb\u60a8\u7684510kBridge\u4ee3\u8868\u5b89\u6392\u5f15\u5bfc\u6f14\u793a\u3002"
    )

    # ── 5 ──
    pdf.section("5", "7\u4e2a\u9884\u5efa\u5668\u68b0\u7c7b\u522b\u6a21\u677f")
    pdf.body(
        "\u5f00\u59cb\u65b0\u9879\u76ee\u65f6\uff0c\u9009\u62e9\u60a8\u7684\u5668\u68b0\u7c7b\u522b\uff0c"
        "Control Tower\u4f1a\u81ea\u52a8\u914d\u7f6e\u6cd5\u89c4\u6807\u51c6\u3001\u98ce\u9669\u6982\u51b5\u3001"
        "\u5bf9\u6bd4\u5668\u68b0\u793a\u4f8b\u3001\u9884\u7b97\u7c7b\u522b\u548c\u9884\u4f30\u65f6\u95f4\u7ebf\uff1a"
    )
    templates_cn = [
        ["\u547c\u5438\u7cfb\u7edf", "21 CFR 868", "18\u4e2a\u6708",
         "\u547c\u5438\u673a\u3001CPAP/BiPAP\u3001\u96fe\u5316\u5668\u3001\u6c14\u9053\u7ba1\u7406"],
        ["\u5fc3\u8840\u7ba1", "21 CFR 870", "18\u4e2a\u6708",
         "ECG\u76d1\u62a4\u4eea\u3001\u8840\u538b\u8bbe\u5907\u3001\u5fc3\u810f\u5bfc\u7ba1\u3001\u652f\u67b6"],
        ["\u9aa8\u79d1", "21 CFR 888", "24\u4e2a\u6708",
         "\u5173\u8282\u690d\u5165\u7269\u3001\u9aa8\u677f\u3001\u810a\u67f1\u5668\u68b0\u3001\u56fa\u5b9a\u88c5\u7f6e"],
        ["IVD\u4f53\u5916\u8bca\u65ad", "21 CFR 862-864", "15\u4e2a\u6708",
         "\u5206\u6790\u4eea\u3001\u514d\u75ab\u5206\u6790\u3001\u8840\u6db2\u5b66\u3001POCT\u3001\u5206\u5b50\u8bca\u65ad"],
        ["\u5f71\u50cf\u4e0e\u76d1\u62a4", "21 CFR 892", "15\u4e2a\u6708",
         "\u8d85\u58f0\u3001X\u5c04\u7ebf\u3001EEG\u3001\u8109\u640f\u8840\u6c27\u4eea\u3001SaMD"],
        ["\u5eb7\u590d", "21 CFR 890", "20\u4e2a\u6708",
         "\u5916\u9aa8\u9abc\u3001\u795e\u7ecf\u523a\u6fc0\u5668\u3001EMG\u751f\u7269\u53cd\u9988"],
        ["\u8f6f\u4ef6\u533b\u7597\u5668\u68b0", "21 CFR 892.2020", "12\u4e2a\u6708",
         "\u4e34\u5e8a\u51b3\u7b56\u652f\u6301\u3001AI/ML\u3001\u8fdc\u7a0b\u533b\u7597\u3001PACS"],
    ]
    pdf.tier_table(
        rows=templates_cn,
        col_widths=[28, 28, 18, 116],
        header=["\u7c7b\u522b", "CFR\u90e8\u5206", "\u5468\u671f", "\u5668\u68b0\u793a\u4f8b"],
    )

    # ── 6 ──
    pdf.section("6", "\u7f8e\u56fd\u5b9e\u4f53\u4e0e\u5408\u89c4\u8981\u6c42")
    pdf.body(
        "\u5916\u56fd\u5236\u9020\u5546\u5728\u7f8e\u56fd\u9500\u552e\u5668\u68b0\u5fc5\u987b\u6ee1\u8db3"
        "\u591a\u9879\u7ed3\u6784\u6027\u548c\u6cd5\u89c4\u8981\u6c42\u3002\u6211\u4eec\u5c06\u6307\u5bfc"
        "\u60a8\u5b8c\u6210\u6bcf\u4e00\u6b65\uff1a"
    )
    pdf.key_value_row("\u7f8e\u56fd\u4ee3\u7406\u4eba(\u5fc5\u9700)",
                      "$3,000-$6,000/\u5e74 -- \u6240\u6709\u5916\u56fd\u5236\u9020\u5546\u5fc5\u987b"
                      "\u6307\u5b9a\u7f8e\u56fd\u4eba\u4f5c\u4e3aFDA\u8054\u7cfb\u4eba", label_w=45)
    pdf.key_value_row("\u7f8e\u56fd\u5b9e\u4f53\u7ec4\u5efa",
                      "\u5efa\u8bae\u7279\u62c9\u534eC-Corp\uff08\u6295\u8d44\u8005\u9996\u9009\uff09\uff1b"
                      "~$2K-$5K\u8bbe\u7acb + $300/\u5e74\u6ce8\u518c\u4ee3\u7406\u4eba", label_w=45)
    pdf.key_value_row("FDA\u673a\u6784\u6ce8\u518c",
                      "\u5e74\u5ea6\u6ce8\u518c + \u5668\u68b0\u5217\u540d -- \u5546\u4e1a\u5206\u9500"
                      "\u524d\u5fc5\u987b\u5b8c\u6210", label_w=45)
    pdf.key_value_row("\u8d28\u91cf\u4f53\u7cfb",
                      "21 CFR 820 (QSR) / ISO 13485 -- \u6301\u7eed\u5408\u89c4\u3001CAPA\u7cfb\u7edf\u3001"
                      "MDR\u62a5\u544a", label_w=45)
    pdf.key_value_row("\u6587\u4ef6\u5b58\u50a8",
                      "FDA\u8981\u6c42\u4fdd\u7559\u8bbe\u8ba1\u5386\u53f2\u6587\u4ef6(DHF)\u3001\u5668\u68b0"
                      "\u4e3b\u8bb0\u5f55(DMR)\u548c\u5668\u68b0\u5386\u53f2\u8bb0\u5f55(DHR)\uff0c\u5e76\u786e"
                      "\u4fdd\u53ef\u4f9b\u68c0\u67e5\u3002\u8bb0\u5f55\u5fc5\u987b\u6e05\u6670\u3001\u7528"
                      "\u82f1\u6587\u7f16\u5199\u3001\u4fdd\u7559\u81f3\u5668\u68b0\u5bff\u547d\u671f\u52a02\u5e74\u3002", label_w=45)
    pdf.key_value_row("\u6807\u7b7e",
                      "\u7f8e\u56fd\u6807\u7b7e\u5fc5\u987b\u7b26\u540821 CFR 801 -- \u82f1\u6587\u3001"
                      "\u9884\u671f\u7528\u9014\u3001\u8b66\u544a\u3001UDI\u5408\u89c4", label_w=45)
    pdf.key_value_row("\u4e0a\u5e02\u540e",
                      "\u6295\u8bc9\u5904\u7406\u3001MDR\u4e0d\u826f\u4e8b\u4ef6\u62a5\u544a\u3001\u5b9a\u671f"
                      "\u66f4\u65b0\u3001\u53ec\u56de\u51c6\u5907", label_w=45)

    pdf.callout_box(
        "\u91cd\u8981\uff1a21 CFR 820.180\u8981\u6c42\u6240\u6709\u8d28\u91cf\u8bb0\u5f55\u4fdd\u5b58"
        "\u5728\u6d3b\u52a8\u53d1\u751f\u5730\u6216FDA\u68c0\u67e5\u5458\u53ef\u5408\u7406\u83b7\u53d6"
        "\u7684\u5730\u70b9\u3002\u5bf9\u4e8e\u5916\u56fd\u5236\u9020\u5546\uff0c\u8fd9\u610f\u5473\u7740"
        "\u60a8\u7684\u7f8e\u56fd\u4ee3\u7406\u4eba\u5fc5\u987b\u80fd\u591f\u5728\u5408\u7406\u65f6\u95f4"
        "\u5185\u5e94FDA\u8981\u6c42\u63d0\u4f9b\u8bb0\u5f55\u3002\u6211\u4eec\u7684Control Tower\u5e73\u53f0"
        "\u4ee5\u7f8e\u56fd\u6258\u7ba1\u3001\u5ba1\u8ba1\u5c31\u7eea\u7684\u683c\u5f0f\u5b58\u50a8\u548c"
        "\u7ec4\u7ec7\u6240\u6709\u9879\u76ee\u6587\u6863\u3002"
    )

    # ── 7 ──
    pdf.section("7", "\u4e3a\u4ec0\u4e48\u9009\u62e9510kBridge\uff1f")
    pdf.bullet("\u7f8e\u56fd\u516c\u6c11PMP\uff08\u65af\u5766\u798f\u5927\u5b66SCPM\uff09\u7ba1\u7406FDA\u6c9f\u901a\u548c\u9879\u76ee\u6267\u884c",
               "\u7f8e\u56fd\u9879\u76ee\u9886\u5bfc\uff1a")
    pdf.bullet("\u4e0a\u6d77\u672c\u571f\u666e\u901a\u8bdd\u56e2\u961f\u5904\u7406\u6240\u6709\u5ba2\u6237\u6c9f\u901a",
               "\u53cc\u8bed\u56e2\u961f\uff1a")
    pdf.bullet("16\u4e2a\u6a21\u5757\u7684Control Tower\u5b9e\u65f6\u4eea\u8868\u677f\uff0c\u800c\u975e\u7535\u5b50\u8868\u683c\u6216\u90ae\u4ef6",
               "\u4e13\u5efa\u6280\u672f\u5e73\u53f0\uff1a")
    pdf.bullet("\u6211\u4eec\u5904\u7406\u60a8\u7684FDA\u5730\u5740\u3001\u901a\u4fe1\u548c\u68c0\u67e5\u51c6\u5907",
               "\u7f8e\u56fd\u4ee3\u7406\u4eba\u670d\u52a1\uff1a")
    pdf.bullet("7\u4e2a\u9884\u914d\u7f6e\u5668\u68b0\u6a21\u677f\u81ea\u52a8\u52a0\u8f7d\u6807\u51c6\u3001\u98ce\u9669\u548c\u65f6\u95f4\u7ebf",
               "\u7c7b\u522b\u6a21\u677f\uff1a")
    pdf.bullet("\u4ecePre-Sub Q\u4f1a\u8bae\u5230FDA\u6e05\u9664\u4fe1",
               "\u7aef\u5230\u7aef\u8986\u76d6\uff1a")
    pdf.bullet("\u4e0a\u6d77WFOE\u529e\u516c\u5ba4\u63d0\u4f9b\u672c\u5730\u5408\u540c\u3001\u4eba\u6c11\u5e01"
               "\u5f00\u7968\u548c\u9762\u5bf9\u9762\u4f1a\u8bae",
               "\u672c\u5730\u5316\u670d\u52a1\uff1a")

    # ── 8 ──
    pdf.section("8", "\u5178\u578b\u5408\u4f5c\u65f6\u95f4\u7ebf")
    timeline_cn = [
        ["\u7b2c1\u5468", "\u542f\u52a8\u4e0e\u5165\u804c", "\u6a21\u677f\u9009\u62e9\u3001Control Tower\u8bbe\u7f6e\u3001\u56e2\u961f\u8bbf\u95ee\u914d\u7f6e"],
        ["\u7b2c1\u4e2a\u6708", "\u6cd5\u89c4\u7b56\u7565", "\u5bf9\u6bd4\u5668\u68b0\u641c\u7d22\u3001\u5206\u7c7b\u786e\u8ba4\u3001\u9014\u5f84\u9009\u62e9"],
        ["\u7b2c2-3\u4e2a\u6708", "Pre-Submission", "Q-Sub\u6587\u4ef6\u5305\u51c6\u5907\u3001FDA\u4f1a\u8bae\u5b89\u6392\uff0875-90\u5929\u63d0\u524d\u91cf\uff09"],
        ["\u7b2c3-9\u4e2a\u6708", "\u6d4b\u8bd5\u4e0eV&V", "\u6807\u51c6\u6d4b\u8bd5\u3001\u8bbe\u8ba1\u9a8c\u8bc1\u3001\u751f\u7269\u76f8\u5bb9\u6027\u3001\u53ef\u7528\u6027\u7814\u7a76"],
        ["\u7b2c9-10\u4e2a\u6708", "\u63d0\u4ea4\u7f16\u5236", "DHF\u7f16\u8bd1\u3001RTA\u81ea\u67e5\u3001\u6267\u884c\u6458\u8981\u3001eSTAR\u5c01\u88c5"],
        ["\u7b2c10-15\u4e2a\u6708", "FDA\u5ba1\u67e5", "\u63d0\u4ea4\u3001RTA\u901a\u8fc7\u3001\u5b9e\u8d28\u5ba1\u67e5\u3001AI\u54cd\u5e94\u7ba1\u7406"],
        ["\u6e05\u9664\u540e", "\u5e02\u573a\u51c6\u5165", "\u673a\u6784\u6ce8\u518c\u3001\u5668\u68b0\u5217\u540d\u3001\u6807\u7b7e\u5408\u89c4\u3001QMS\u7ef4\u62a4"],
    ]
    pdf.tier_table(
        rows=timeline_cn,
        col_widths=[22, 30, 138],
        header=["\u65f6\u95f4", "\u91cc\u7a0b\u7891", "\u5173\u952e\u6d3b\u52a8"],
    )

    # ── 9 ──
    pdf.section("9", "\u4e0b\u4e00\u6b65")
    pdf.body("\u51c6\u5907\u597d\u5f00\u59cb\u60a8\u7684\u7f8e\u56fd\u5e02\u573a\u51c6\u5165\u4e4b\u65c5\u4e86\u5417\uff1f\u4ee5\u4e0b\u662f\u5f00\u59cb\u65b9\u5f0f\uff1a")
    pdf.bullet("\u5b89\u6392\u514d\u8d3930\u5206\u949fControl Tower\u6f14\u793a", "1. ")
    pdf.bullet("\u5206\u4eab\u60a8\u7684\u5668\u68b0\u63cf\u8ff0\u548c\u76ee\u6807\u5bf9\u6bd4\u5668\u68b0\uff08\u5982\u5df2\u77e5\uff09", "2. ")
    pdf.bullet("\u83b7\u53d6\u5b9a\u5236\u7684\u6cd5\u89c4\u9014\u5f84\u8bc4\u4f30\u548c\u6210\u672c\u4f30\u7b97", "3. ")
    pdf.bullet("\u9009\u62e9\u60a8\u7684\u670d\u52a1\u5c42\u7ea7\u5e76\u5f00\u59cb\u5165\u804c", "4. ")

    pdf.ln(3)
    pdf.body("\u8054\u7cfb\u6211\u4eec\uff1a")
    pdf.key_value_row("\u4e0a\u6d77\u529e\u516c\u5ba4\uff1a",
                      "510kBridge Consulting (\u4e0a\u6d77) Co., Ltd.", label_w=32)
    pdf.key_value_row("\u7f8e\u56fd\u529e\u516c\u5ba4\uff1a",
                      "Pilot Software LLC dba 510kBridge  |  \u4fc4\u52d2\u5188\u5dde", label_w=32)
    pdf.key_value_row("\u7f51\u7ad9\uff1a",
                      "510kbridge.com  |  control-tower-bmx.pages.dev", label_w=32)
    pdf.key_value_row("\u5fae\u4fe1\uff1a", "510kBridge", label_w=32)
    pdf.key_value_row("\u90ae\u7bb1\uff1a", "info@510kbridge.com", label_w=32)

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
