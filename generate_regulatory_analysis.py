#!/usr/bin/env python3
"""
Generate Regulatory Strategy Analysis PDF – EN and CN versions.
Covers: FDA Clearance vs Approval, Predicate Analysis, K-number Audit,
        sEMG/EIT Predicate Strategy, De Novo Risk Scenarios.
Session date: March 21, 2026
"""

from fpdf import FPDF
import os

def _a(t):
    if not t:
        return ""
    t = t.replace("\u2014", "--")   # em dash
    t = t.replace("\u2013", "-")    # en dash
    t = t.replace("\u2022", "-")    # bullet
    t = t.replace("\u2018", "'").replace("\u2019", "'")   # smart quotes
    t = t.replace("\u201c", '"').replace("\u201d", '"')
    return t.encode("latin-1", "replace").decode("latin-1")


class AnalysisPDF(FPDF):
    CARDINAL = (140, 21, 21)
    ACCENT = (0, 100, 60)
    DARK = (30, 30, 30)
    WHITE = (255, 255, 255)
    WARN_BG = (255, 248, 230)
    WARN_BORDER = (200, 150, 50)
    LIGHT_BG = (245, 248, 252)

    def __init__(self, lang="en"):
        super().__init__()
        self.lang = lang
        self.set_auto_page_break(auto=True, margin=20)

    def header(self):
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(120, 120, 120)
        title = ("FDA Regulatory Strategy Analysis  |  ICU Respiratory Digital Twin  |  March 2026"
                 if self.lang == "en" else
                 "FDA\u76d1\u7ba1\u7b56\u7565\u5206\u6790  |  ICU\u547c\u5438\u6570\u5b57\u5b6a\u751f  |  2026\u5e743\u6708")
        self.cell(0, 4, _a(title), align="R")
        self.ln(6)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(150, 150, 150)
        lbl = "Page" if self.lang == "en" else "\u9875"
        self.cell(0, 10, f"{lbl} {self.page_no()}/{{nb}}", align="C")

    def section_heading(self, num, title):
        if self.get_y() > self.page_break_trigger - 30:
            self.add_page()
        self.ln(3)
        self.set_fill_color(*self.CARDINAL)
        self.set_text_color(*self.WHITE)
        self.set_font("Helvetica", "B", 12)
        self.cell(0, 8, _a(f"  {num}. {title}"), fill=True, new_x="LMARGIN", new_y="NEXT")
        self.ln(3)
        self.set_text_color(*self.DARK)

    def sub_heading(self, title):
        if self.get_y() > self.page_break_trigger - 20:
            self.add_page()
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(*self.ACCENT)
        self.cell(0, 6, _a(title), new_x="LMARGIN", new_y="NEXT")
        self.ln(1)
        self.set_text_color(*self.DARK)

    def body(self, text):
        self.set_font("Helvetica", "", 9)
        self.set_text_color(*self.DARK)
        self.multi_cell(0, 5, _a(text))
        self.ln(2)

    def bullet(self, text, bold_prefix=""):
        self.set_font("Helvetica", "", 9)
        self.set_text_color(*self.DARK)
        x = self.l_margin + 6
        self.set_x(x)
        bw = self.w - x - self.r_margin
        if bold_prefix:
            self.set_font("Helvetica", "B", 9)
            self.cell(self.get_string_width(_a(bold_prefix)) + 1, 5, _a(bold_prefix))
            self.set_font("Helvetica", "", 9)
            self.multi_cell(bw - self.get_string_width(_a(bold_prefix)) - 1, 5, _a(text))
        else:
            self.cell(4, 5, _a("\u2022"))
            self.multi_cell(bw - 4, 5, _a(text))
        self.ln(0.5)

    def table_row(self, cells, widths, header=False, bold_first=False):
        h = 6
        if header:
            self.set_font("Helvetica", "B", 8)
            self.set_fill_color(*self.CARDINAL)
            self.set_text_color(*self.WHITE)
            for i, c in enumerate(cells):
                self.cell(widths[i], h, _a(c), border=1, fill=True, align="C")
            self.ln()
            return
        self.set_text_color(*self.DARK)
        for i, c in enumerate(cells):
            self.set_font("Helvetica", "B" if (i == 0 and bold_first) else "", 8)
            self.cell(widths[i], h, _a(c), border=1)
        self.ln()

    def callout_box(self, text, style="key"):
        if style == "warn":
            self.set_fill_color(*self.WARN_BG)
            self.set_draw_color(*self.WARN_BORDER)
            self.set_text_color(160, 90, 0)
            prefix = "WARNING:  " if self.lang == "en" else "\u8b66\u544a\uff1a "
        else:
            self.set_fill_color(240, 250, 245)
            self.set_draw_color(*self.ACCENT)
            self.set_text_color(*self.ACCENT)
            prefix = "KEY INSIGHT:  " if self.lang == "en" else "\u5173\u952e\u6d1e\u5bdf\uff1a "
        self.set_line_width(0.5)
        if self.get_y() > self.page_break_trigger - 35:
            self.add_page()
        x = self.l_margin + 2
        y = self.get_y()
        page_before = self.page
        self.set_xy(x + 3, y + 2)
        self.set_font("Helvetica", "B", 9)
        self.cell(self.get_string_width(_a(prefix)) + 1, 5, _a(prefix))
        self.set_font("Helvetica", "", 9)
        box_w = self.w - self.l_margin - self.r_margin - 7
        text_w = box_w - self.get_string_width(_a(prefix)) - 1
        self.multi_cell(text_w, 5, _a(text), align="L")
        if self.page == page_before:
            h = self.get_y() - y + 2
            self.rect(x, y, box_w + 3, h, style="D")
        self.ln(4)
        self.set_text_color(*self.DARK)


# ============================================================
#  ENGLISH VERSION
# ============================================================
def build_en():
    pdf = AnalysisPDF(lang="en")
    pdf.alias_nb_pages()
    pdf.add_page()

    # Cover
    pdf.set_fill_color(*pdf.CARDINAL)
    pdf.rect(0, 0, 210, 55, style="F")
    pdf.set_y(12)
    pdf.set_text_color(*pdf.WHITE)
    pdf.set_font("Helvetica", "B", 20)
    pdf.cell(0, 10, "FDA Regulatory Strategy Analysis", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 12)
    pdf.cell(0, 7, "ICU Respiratory Digital Twin System", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "I", 10)
    pdf.cell(0, 7, "Predicate Strategy, De Novo Risk, & Clearance vs. Approval", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(*pdf.DARK)
    pdf.ln(20)
    pdf.set_font("Helvetica", "", 9)
    pdf.cell(0, 5, "Prepared: March 21, 2026", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 5, "Program: ICU Respiratory Digital Twin  |  Arch Medical Management, LLC", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 5, "Classification: CONFIDENTIAL / Internal Use Only", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)

    # ── 1. Clearance vs Approval ────────────────────────
    pdf.section_heading("1", "FDA Clearance vs. Approval — The Legal Distinction")

    pdf.body(
        "\"Approval\" is reserved for devices that go through the Premarket Approval (PMA) "
        "pathway — 21 CFR Part 814. This is the most rigorous FDA review and applies to "
        "Class III devices (highest risk: implantable defibrillators, heart valves, etc.)."
    )

    pdf.sub_heading("Comparison Table")
    w = [35, 45, 45, 45]
    pdf.table_row(["", "510(k) Clearance", "PMA Approval", "De Novo Grant"], w, header=True)
    pdf.table_row(["Legal verb", "Cleared", "Approved", "Granted"], w, bold_first=True)
    pdf.table_row(["Standard", "Substantial equiv.", "Safety & effectiveness", "Low-mod risk, no pred."], w, bold_first=True)
    pdf.table_row(["Evidence", "Bench testing", "Clinical trials", "Bench + some clinical"], w, bold_first=True)
    pdf.table_row(["Device class", "Class I & II", "Class III", "Creates new I or II"], w, bold_first=True)
    pdf.table_row(["Review time", "3-6 months", "6-18 months", "6-12 months"], w, bold_first=True)
    pdf.table_row(["User fee", "$7K-$26K", "~$425K", "~$130K"], w, bold_first=True)
    pdf.ln(2)

    pdf.sub_heading("What Makes PMA 'Approval' Different")
    pdf.bullet("Clinical data requirement — PMA almost always requires prospective clinical trials demonstrating both safety and effectiveness.")
    pdf.bullet("No predicate needed — PMA stands on its own evidence.")
    pdf.bullet("FDA affirmatively finds safety & effectiveness — 510(k) only finds 'substantial equivalence.'")
    pdf.bullet("Conditions of approval — post-approval studies, periodic reporting, restrictions.")
    pdf.bullet("Supplements for changes — any change requires a PMA Supplement (far more restrictive than 510(k)).")

    pdf.callout_box(
        "You CANNOT say a 510(k)-cleared device is 'FDA approved.' This is a violation of "
        "FDA advertising regulations (21 CFR 807.97) and is considered misbranding under the "
        "FD&C Act. Correct language: 'FDA 510(k) cleared' or 'cleared by FDA.'"
    , style="warn")

    # ── 2. Timpel Enlight Predicate Review ──────────────
    pdf.section_heading("2", "Predicate Device Review: Timpel Enlight 2100 (K250464)")

    pdf.body(
        "The Timpel Enlight 2100 (K250464) was cleared by FDA on September 10, 2025 as a "
        "Ventilatory Electrical Impedance Tomograph under 21 CFR 868.1505, product codes QEB "
        "and BZK. The sponsor is Timpel S.A. (Brazil) with US regulatory consultant ProMedic "
        "Consulting LLC."
    )

    pdf.sub_heading("Relevance Assessment")
    w2 = [40, 60, 70]
    pdf.table_row(["Factor", "Enlight 2100 (K250464)", "Our Digital Twin"], w2, header=True)
    pdf.table_row(["Technology", "EIT only", "EIT + sEMG + MyoBus"], w2, bold_first=True)
    pdf.table_row(["Product Code", "QEB", "QEB (EIT) + IKN (sEMG)"], w2, bold_first=True)
    pdf.table_row(["Regulation", "21 CFR 868.1505", "Same for EIT component"], w2, bold_first=True)
    pdf.table_row(["Classification", "Class II", "Class II (expected)"], w2, bold_first=True)
    pdf.table_row(["Intended Use", "Ventilation imaging only", "Ventilation + V/Q perfusion"], w2, bold_first=True)
    pdf.table_row(["Patient Contact", "Surface electrodes", "EIT belt + sEMG electrodes"], w2, bold_first=True)
    pdf.ln(2)

    pdf.callout_box(
        "K250464 is a strong predicate candidate for the EIT MODULE only — not the full system. "
        "The sEMG module needs its own predicate (product code IKN). The fusion platform may "
        "require De Novo classification."
    )

    pdf.sub_heading("Strategic Observations")
    pdf.bullet("Cleared September 2025 — very recent, shows FDA actively reviewing EIT devices under QEB.")
    pdf.bullet("Software-only changes from K222897 — demonstrates FDA accepts iterative 510(k) for EIT.")
    pdf.bullet("Sponsor used US regulatory consultant while being a Brazilian company — parallel to our Oregon/Chengdu structure.")
    pdf.bullet("The predicate for K250464 was itself K222897 (prior Enlight version) — same device family.")

    # ── 3. sEMG Predicate Strategy ──────────────────────
    pdf.section_heading("3", "sEMG Module Predicate: Maquet NAVA Edi Catheter (K082437)")

    pdf.body(
        "The sEMG module (product code IKN — Electromyograph, diagnostic) references the "
        "Maquet/Getinge Servo-i with NAVA as the primary predicate. The NAVA system includes "
        "the Edi catheter, which measures diaphragm electrical activity to monitor neural "
        "respiratory drive (NRD)."
    )

    pdf.sub_heading("Critical Difference: Esophageal vs. Surface")
    pdf.body(
        "K082437 uses an esophageal catheter (Edi) for diaphragm EMG, while our device uses "
        "surface electrodes on the chest wall. This is a fundamental difference in transducer "
        "technology that FDA will scrutinize."
    )

    pdf.bullet("Same intended use — measure neural respiratory drive for ventilator optimization", bold_prefix="Similarity: ")
    pdf.bullet("Different transducer — esophageal catheter vs. surface electrodes", bold_prefix="Difference: ")
    pdf.bullet("Different signal — direct diaphragm EMG vs. surface EMG through chest wall", bold_prefix="Difference: ")
    pdf.bullet("Different invasiveness — catheter (invasive) vs. surface (non-invasive)", bold_prefix="Difference: ")
    pdf.ln(1)

    pdf.callout_box(
        "FDA may say: 'Different technological characteristics raise different questions of safety "
        "and effectiveness.' This is the specific language FDA uses when rejecting a predicate. "
        "The Pre-Sub Q-Meeting must address this directly."
    , style="warn")

    pdf.sub_heading("Mitigation: Alternative IKN Predicates")
    pdf.body(
        "If FDA rejects K082437 as the sEMG predicate, alternative surface EMG diagnostic devices "
        "under product code IKN should be identified. The Pre-Sub package should include 2-3 "
        "backup predicates that use surface electrodes, even if not respiratory-specific."
    )

    # ── 4. De Novo Risk Analysis ────────────────────────
    pdf.section_heading("4", "De Novo Reclassification Risk — Combined Platform")

    pdf.body(
        "Beyond per-module predicate rejection, there is a second higher-order risk: FDA may "
        "view the combined sEMG+EIT integrated system as a single novel device with no predicate, "
        "requiring De Novo classification instead of two separate 510(k)s."
    )

    pdf.sub_heading("Trigger Scenario")
    pdf.bullet("Two 510(k)s are filed — sEMG (IKN) and EIT (QEB)")
    pdf.bullet("Each submission mentions MyoBus integration and 'Digital Twin' fusion")
    pdf.bullet("FDA reviewer reads both and determines: the combined sEMG+EIT system with AI-driven fusion is a novel device with no predicate")
    pdf.bullet("FDA notifies applicant that De Novo classification is required for the combined platform")
    pdf.ln(1)

    pdf.sub_heading("Impact Comparison")
    w3 = [50, 55, 65]
    pdf.table_row(["Factor", "Two 510(k)s (current)", "De Novo (contingency)"], w3, header=True)
    pdf.table_row(["User fee", "~$13K ($6.5K x 2)", "~$130K"], w3, bold_first=True)
    pdf.table_row(["Review time", "3-6 months each", "10-14 months"], w3, bold_first=True)
    pdf.table_row(["Evidence", "Bench + limited clinical", "May need clinical study"], w3, bold_first=True)
    pdf.table_row(["Timeline impact", "24-month plan holds", "+6-12 months"], w3, bold_first=True)
    pdf.table_row(["Budget impact", "Within estimates", "+$200K-$400K total"], w3, bold_first=True)
    pdf.table_row(["Competitive moat", "Predicate exists", "YOU create the code"], w3, bold_first=True)
    pdf.ln(2)

    pdf.sub_heading("Mitigation Strategy (5 Actions)")
    pdf.bullet("Ask FDA directly at Pre-Sub: 'We propose two modular 510(k) submissions. Module A (sEMG, IKN) with predicate K082437. Module B (EIT, QEB) with predicate K250464. The modules are cleared independently and can function independently. Does FDA concur?'",
               bold_prefix="1. Pre-Sub Q-Meeting: ")
    pdf.bullet("Have 2-3 alternative IKN predicates researched (surface EMG devices) before the meeting.",
               bold_prefix="2. Backup Predicates: ")
    pdf.bullet("In 510(k) filings, describe each module as a standalone device. The 'Digital Twin' concept should be described only as a future planned integration, not the primary function.",
               bold_prefix="3. Decouple Digital Twin: ")
    pdf.bullet("If FDA says De Novo at Pre-Sub, pivot immediately. Finding out at M+2 saves $50K+ vs. finding out after filing.",
               bold_prefix="4. Early Detection: ")
    pdf.bullet("If De Novo is required, you create the classification. Your device becomes the predicate for all future competitors. This is a significant competitive moat and increases acquisition value by Drager, Getinge, or Mindray.",
               bold_prefix="5. Silver Lining: ")

    # ── 5. PPTX K-Number Audit ──────────────────────────
    pdf.section_heading("5", "PPTX K-Number Audit Results")

    pdf.body(
        "A systematic extraction of all text and table cells in 'ICU Digital Respiratory Twin.pptx' "
        "was performed, searching for patterns matching FDA clearance numbers (K followed by 5-6 digits)."
    )

    pdf.callout_box(
        "No K-numbers (clearance numbers) were found in the original PPTX. "
        "The PPTX only references '510(k)' generically in two locations: Slide 15 (fees in Chinese) "
        "and Slide 16 ('FDA 510(k) (sEMG)' milestone label). All specific K-numbers in the dashboard "
        "data were added during development."
    )

    pdf.sub_heading("K-Numbers Now in Dashboard")
    w4 = [30, 45, 55, 40]
    pdf.table_row(["Module", "Predicate Device", "K-Number", "Status"], w4, header=True)
    pdf.table_row(["EIT (DQS)", "Timpel Enlight 2100", "K250464", "Updated from K213494"], w4, bold_first=True)
    pdf.table_row(["sEMG (IKN)", "Maquet NAVA Edi", "K082437", "Added (was unnamed)"], w4, bold_first=True)
    pdf.ln(2)

    # ── 6. Updated RISK-007 ─────────────────────────────
    pdf.section_heading("6", "Updated RISK-007 — Dashboard Risk Register")

    pdf.body(
        "RISK-007 has been expanded from a single-scenario risk to a dual-scenario risk "
        "covering both per-module predicate rejection and combined platform De Novo reclassification."
    )

    pdf.sub_heading("Risk Card")
    pdf.bullet("510(k) rejection or De Novo reclassification — predicate not accepted or combined platform deemed novel", bold_prefix="Title: ")
    pdf.bullet("High", bold_prefix="Severity: ")
    pdf.bullet("Medium", bold_prefix="Probability: ")
    pdf.bullet("RED", bold_prefix="Risk Level: ")
    pdf.bullet("Manageable if detected at Pre-Sub (M+2)", bold_prefix="Residual: ")
    pdf.ln(1)

    pdf.sub_heading("CAPA-004: Predicate & De Novo Contingency Strategy")
    pdf.bullet("Identify 2-3 alternative IKN predicates for sEMG beyond K082437 (surface EMG, not catheter-based)", bold_prefix="Action 1: ")
    pdf.bullet("Prepare SE argument for EIT V/Q claim as performance enhancement vs. new intended use", bold_prefix="Action 2: ")
    pdf.bullet("Draft De Novo pre-submission package for combined platform if FDA rejects modular strategy", bold_prefix="Action 3: ")
    pdf.bullet("$130K De Novo fee + $200K clinical study contingency", bold_prefix="Budget Reserve: ")

    # ── 7. Recommendations ──────────────────────────────
    pdf.section_heading("7", "Recommendations & Next Steps")

    pdf.bullet("Both risks route through the same gate: the Pre-Sub Q-Meeting (R1/R2). That meeting is designed exactly for this purpose.")
    pdf.bullet("The worst outcome: spending 6+ months building submission packages only to have FDA reject the predicate strategy at review.")
    pdf.bullet("The best use of the first 2 months: get FDA's written position on predicate choices AND modular-vs-integrated classification before committing testing resources.")
    pdf.bullet("The dashboard already sequences this correctly: R1 at M+0, R2 at M+2, testing starts only after FDA feedback.")
    pdf.ln(2)

    pdf.callout_box(
        "Bottom Line: The Pre-Sub Q-Meeting is not optional — it is the single most important "
        "risk-mitigation action in the entire program. All predicate and classification questions "
        "must be resolved before any significant testing expenditure."
    )

    out = os.path.join(os.path.dirname(__file__), "Regulatory_Strategy_Analysis_EN.pdf")
    pdf.output(out)
    print(f"EN PDF: {out}")


# ============================================================
#  CHINESE VERSION
# ============================================================
def build_cn():
    CJK_FONT = "/Library/Fonts/Arial Unicode.ttf"

    class CnPDF(AnalysisPDF):
        def header(self):
            self.set_font("NotoSC", "I", 7)
            self.set_text_color(120, 120, 120)
            self.cell(0, 4, "FDA\u76d1\u7ba1\u7b56\u7565\u5206\u6790  |  ICU\u547c\u5438\u6570\u5b57\u5b6a\u751f  |  2026\u5e743\u6708", align="R")
            self.ln(6)

        def footer(self):
            self.set_y(-15)
            self.set_font("NotoSC", "I", 7)
            self.set_text_color(150, 150, 150)
            self.cell(0, 10, f"\u9875 {self.page_no()}/{{nb}}", align="C")

    pdf = CnPDF(lang="cn")
    pdf.alias_nb_pages()
    pdf.add_font("NotoSC", "", CJK_FONT)
    pdf.add_font("NotoSC", "B", CJK_FONT)
    pdf.add_font("NotoSC", "I", CJK_FONT)

    def sf(style="", size=9):
        pdf.set_font("NotoSC", style, size)

    pdf.add_page()

    # Cover
    pdf.set_fill_color(*pdf.CARDINAL)
    pdf.rect(0, 0, 210, 55, style="F")
    pdf.set_y(12)
    pdf.set_text_color(*pdf.WHITE)
    sf("B", 18)
    pdf.cell(0, 10, "FDA\u76d1\u7ba1\u7b56\u7565\u5206\u6790", align="C", new_x="LMARGIN", new_y="NEXT")
    sf("", 11)
    pdf.cell(0, 7, "ICU\u547c\u5438\u6570\u5b57\u5b6a\u751f\u7cfb\u7edf", align="C", new_x="LMARGIN", new_y="NEXT")
    sf("", 9)
    pdf.cell(0, 7, "\u524d\u7f6e\u5668\u68b0\u7b56\u7565\u3001De Novo\u98ce\u9669\u3001\u6279\u51c6vs\u8bb8\u53ef\u5206\u6790", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(*pdf.DARK)
    pdf.ln(20)
    sf("", 9)
    pdf.cell(0, 5, "\u7f16\u5236\u65e5\u671f\uff1a2026\u5e743\u670821\u65e5", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 5, "\u9879\u76ee\uff1aICU\u547c\u5438\u6570\u5b57\u5b6a\u751f  |  Arch Medical Management, LLC", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 5, "\u5bc6\u7ea7\uff1a\u673a\u5bc6 / \u4ec5\u9650\u5185\u90e8\u4f7f\u7528", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)

    def sec(num, title):
        if pdf.get_y() > pdf.page_break_trigger - 30:
            pdf.add_page()
        pdf.ln(3)
        pdf.set_fill_color(*pdf.CARDINAL)
        pdf.set_text_color(*pdf.WHITE)
        sf("B", 12)
        pdf.cell(0, 8, f"  {num}. {title}", fill=True, new_x="LMARGIN", new_y="NEXT")
        pdf.ln(3)
        pdf.set_text_color(*pdf.DARK)

    def sub(title):
        if pdf.get_y() > pdf.page_break_trigger - 20:
            pdf.add_page()
        sf("B", 10)
        pdf.set_text_color(*pdf.ACCENT)
        pdf.cell(0, 6, title, new_x="LMARGIN", new_y="NEXT")
        pdf.ln(1)
        pdf.set_text_color(*pdf.DARK)

    def body(text):
        sf("", 9)
        pdf.set_text_color(*pdf.DARK)
        pdf.multi_cell(0, 5.5, text, align="L")
        pdf.ln(2)

    def bul(text, bp=""):
        sf("", 9)
        pdf.set_text_color(*pdf.DARK)
        x = pdf.l_margin + 6
        pdf.set_x(x)
        bw = pdf.w - x - pdf.r_margin
        if bp:
            sf("B", 9)
            pdf.cell(pdf.get_string_width(bp) + 1, 5.5, bp)
            sf("", 9)
            pdf.multi_cell(bw - pdf.get_string_width(bp) - 1, 5.5, text, align="L")
        else:
            pdf.cell(4, 5.5, "\u2022")
            pdf.multi_cell(bw - 4, 5.5, text, align="L")
        pdf.ln(0.5)

    def trow(cells, widths, header=False, bold_first=False):
        h = 6
        if header:
            sf("B", 8)
            pdf.set_fill_color(*pdf.CARDINAL)
            pdf.set_text_color(*pdf.WHITE)
            for i, c in enumerate(cells):
                pdf.cell(widths[i], h, c, border=1, fill=True, align="C")
            pdf.ln()
            return
        pdf.set_text_color(*pdf.DARK)
        for i, c in enumerate(cells):
            sf("B" if (i == 0 and bold_first) else "", 8)
            pdf.cell(widths[i], h, c, border=1)
        pdf.ln()

    def callout(text, style="key"):
        if style == "warn":
            pdf.set_fill_color(*pdf.WARN_BG)
            pdf.set_draw_color(*pdf.WARN_BORDER)
            pdf.set_text_color(160, 90, 0)
            prefix = "\u8b66\u544a\uff1a "
        else:
            pdf.set_fill_color(240, 250, 245)
            pdf.set_draw_color(*pdf.ACCENT)
            pdf.set_text_color(*pdf.ACCENT)
            prefix = "\u5173\u952e\u6d1e\u5bdf\uff1a "
        pdf.set_line_width(0.5)
        if pdf.get_y() > pdf.page_break_trigger - 35:
            pdf.add_page()
        x = pdf.l_margin + 2
        y = pdf.get_y()
        page_before = pdf.page
        pdf.set_xy(x + 3, y + 2)
        sf("B", 9)
        pdf.cell(pdf.get_string_width(prefix) + 1, 5.5, prefix)
        sf("", 9)
        box_w = pdf.w - pdf.l_margin - pdf.r_margin - 7
        text_w = box_w - pdf.get_string_width(prefix) - 1
        pdf.multi_cell(text_w, 5.5, text, align="L")
        if pdf.page == page_before:
            ht = pdf.get_y() - y + 2
            pdf.rect(x, y, box_w + 3, ht, style="D")
        pdf.ln(4)
        pdf.set_text_color(*pdf.DARK)

    # ── 1 ───────────────────────────────────────────────
    sec("1", "FDA\u201c\u6279\u51c6\u201dvs\u201c\u8bb8\u53ef\u201d\u2014\u2014\u6cd5\u5f8b\u533a\u522b")

    body(
        "\u201c\u6279\u51c6\u201d\uff08Approval\uff09\u4ec5\u9002\u7528\u4e8e\u901a\u8fc7\u4e0a\u5e02\u524d\u6279\u51c6\uff08PMA\uff09\u9014\u5f84\u7684\u5668\u68b0\u2014\u201421 CFR Part 814\u3002\u8fd9\u662fFDA\u6700\u4e25\u683c\u7684\u5ba1\u67e5\uff0c\u9002\u7528\u4e8e"
        "\u7b2c\u4e09\u7c7b\u5668\u68b0\uff08\u6700\u9ad8\u98ce\u9669\uff1a\u690d\u5165\u5f0f\u9664\u98a4\u5668\u3001\u5fc3\u810f\u74e3\u819c\u7b49\uff09\u3002"
    )

    sub("\u6bd4\u8f83\u8868")
    w = [35, 45, 45, 45]
    trow(["", "510(k)\u8bb8\u53ef", "PMA\u6279\u51c6", "De Novo\u6388\u6743"], w, header=True)
    trow(["\u6cd5\u5f8b\u672f\u8bed", "Cleared(\u8bb8\u53ef)", "Approved(\u6279\u51c6)", "Granted(\u6388\u6743)"], w, bold_first=True)
    trow(["\u6807\u51c6", "\u5b9e\u8d28\u7b49\u6548", "\u5b89\u5168\u6027\u4e0e\u6709\u6548\u6027", "\u4f4e-\u4e2d\u98ce\u9669\uff0c\u65e0\u524d\u7f6e"], w, bold_first=True)
    trow(["\u8bc1\u636e\u8981\u6c42", "\u53f0\u67b6\u6d4b\u8bd5", "\u4e34\u5e8a\u8bd5\u9a8c", "\u53f0\u67b6+\u90e8\u5206\u4e34\u5e8a"], w, bold_first=True)
    trow(["\u5668\u68b0\u7c7b\u522b", "\u7b2c\u4e00/\u4e8c\u7c7b", "\u7b2c\u4e09\u7c7b", "\u521b\u5efa\u65b0\u7684\u4e00/\u4e8c\u7c7b"], w, bold_first=True)
    trow(["\u5ba1\u67e5\u65f6\u95f4", "3-6\u4e2a\u6708", "6-18\u4e2a\u6708", "6-12\u4e2a\u6708"], w, bold_first=True)
    trow(["\u7528\u6237\u8d39", "$7K-$26K", "~$425K", "~$130K"], w, bold_first=True)
    pdf.ln(2)

    sub("PMA\u201c\u6279\u51c6\u201d\u7684\u4e0d\u540c\u4e4b\u5904")
    bul("\u4e34\u5e8a\u6570\u636e\u8981\u6c42\u2014\u2014PMA\u51e0\u4e4e\u603b\u662f\u9700\u8981\u524d\u77bb\u6027\u4e34\u5e8a\u8bd5\u9a8c\u8bc1\u660e\u5b89\u5168\u6027\u548c\u6709\u6548\u6027\u3002")
    bul("\u65e0\u9700\u524d\u7f6e\u5668\u68b0\u2014\u2014PMA\u4ee5\u81ea\u8eab\u8bc1\u636e\u4e3a\u57fa\u7840\u3002")
    bul("FDA\u660e\u786e\u8ba4\u5b9a\u5b89\u5168\u6027\u4e0e\u6709\u6548\u6027\u2014\u2014510(k)\u4ec5\u8ba4\u5b9a\u201c\u5b9e\u8d28\u7b49\u6548\u201d\u3002")
    bul("\u6279\u51c6\u6761\u4ef6\u2014\u2014\u4e0a\u5e02\u540e\u7814\u7a76\u3001\u5b9a\u671f\u62a5\u544a\u3001\u9650\u5236\u6761\u4ef6\u3002")
    bul("\u53d8\u66f4\u8865\u5145\u7533\u8bf7\u2014\u2014\u4efb\u4f55\u53d8\u66f4\u5747\u9700PMA\u8865\u5145\uff08\u8fdc\u6bd4510(k)\u4e25\u683c\uff09\u3002")

    callout(
        "\u60a8\u4e0d\u80fd\u8bf4510(k)\u8bb8\u53ef\u7684\u5668\u68b0\u662f\u201cFDA\u6279\u51c6\u201d\u7684\u3002\u8fd9\u8fdd\u53cdFDA\u5e7f\u544a\u6cd5\u89c4\uff0821 CFR 807.97\uff09\uff0c"
        "\u6784\u6210FD&C\u6cd5\u4e0b\u7684\u9519\u8bef\u6807\u8bc6\u3002\u6b63\u786e\u7528\u8bed\uff1a\u201cFDA 510(k)\u8bb8\u53ef\u201d\u6216\u201c\u7ecfFDA\u8bb8\u53ef\u201d\u3002",
        style="warn"
    )

    # ── 2 ───────────────────────────────────────────────
    sec("2", "\u524d\u7f6e\u5668\u68b0\u5206\u6790\uff1aTimpel Enlight 2100 (K250464)")

    body(
        "Timpel Enlight 2100 (K250464)\u4e8e2025\u5e749\u670810\u65e5\u83b7\u5f97FDA\u8bb8\u53ef\uff0c\u5206\u7c7b\u4e3a\u901a\u6c14\u7535\u963b\u6297\u65ad\u5c42\u6210\u50cf\u4eea\uff0c"
        "\u9002\u7528\u4e8e21 CFR 868.1505\uff0c\u4ea7\u54c1\u4ee3\u7801QEB\u548cBZK\u3002\u7533\u8bf7\u4eba\u4e3aTimpel S.A.\uff08\u5df4\u897f\uff09\uff0c"
        "\u7f8e\u56fd\u76d1\u7ba1\u987e\u95ee\u4e3aProMedic Consulting LLC\u3002"
    )

    sub("\u76f8\u5173\u6027\u8bc4\u4f30")
    w2 = [40, 60, 70]
    trow(["\u56e0\u7d20", "Enlight 2100 (K250464)", "\u6211\u4eec\u7684\u6570\u5b57\u5b6a\u751f"], w2, header=True)
    trow(["\u6280\u672f", "\u4ec5EIT", "EIT + sEMG + MyoBus"], w2, bold_first=True)
    trow(["\u4ea7\u54c1\u4ee3\u7801", "QEB", "QEB(EIT) + IKN(sEMG)"], w2, bold_first=True)
    trow(["\u6cd5\u89c4", "21 CFR 868.1505", "EIT\u7ec4\u4ef6\u76f8\u540c"], w2, bold_first=True)
    trow(["\u5206\u7c7b", "\u7b2c\u4e8c\u7c7b", "\u7b2c\u4e8c\u7c7b\uff08\u9884\u671f\uff09"], w2, bold_first=True)
    trow(["\u9884\u671f\u7528\u9014", "\u4ec5\u901a\u6c14\u6210\u50cf", "\u901a\u6c14 + V/Q\u704c\u6ce8"], w2, bold_first=True)
    trow(["\u60a3\u8005\u63a5\u89e6", "\u8868\u9762\u7535\u6781", "EIT\u5e26 + sEMG\u7535\u6781"], w2, bold_first=True)
    pdf.ln(2)

    callout(
        "K250464\u662fEIT\u6a21\u5757\u7684\u5f3a\u5019\u9009\u524d\u7f6e\u5668\u68b0\u2014\u2014\u4f46\u4e0d\u662f\u6574\u4e2a\u7cfb\u7edf\u7684\u3002"
        "sEMG\u6a21\u5757\u9700\u8981\u81ea\u5df1\u7684\u524d\u7f6e\u5668\u68b0\uff08\u4ea7\u54c1\u4ee3\u7801IKN\uff09\u3002"
        "\u878d\u5408\u5e73\u53f0\u53ef\u80fd\u9700\u8981De Novo\u5206\u7c7b\u3002"
    )

    sub("\u7b56\u7565\u89c2\u5bdf")
    bul("2025\u5e749\u6708\u83b7\u6279\u2014\u2014\u975e\u5e38\u65b0\uff0c\u8868\u660eFDA\u6b63\u79ef\u6781\u5ba1\u67e5QEB\u4e0b\u7684EIT\u8bbe\u5907\u3002")
    bul("\u4ecek222897\u7684\u4ec5\u8f6f\u4ef6\u53d8\u66f4\u2014\u2014\u8bc1\u660eFDA\u63a5\u53d7EIT\u8bbe\u5907\u7684\u8fed\u4ee3510(k)\u3002")
    bul("\u7533\u8bf7\u4eba\u4e3a\u5df4\u897f\u516c\u53f8\u4f7f\u7528\u7f8e\u56fd\u76d1\u7ba1\u987e\u95ee\u2014\u2014\u4e0e\u6211\u4eec\u4fc4\u52d2\u5188/\u6210\u90fd\u7ed3\u6784\u5e73\u884c\u3002")

    # ── 3 ───────────────────────────────────────────────
    sec("3", "sEMG\u6a21\u5757\u524d\u7f6e\u5668\u68b0\uff1aMaquet NAVA Edi\u5bfc\u7ba1 (K082437)")

    body(
        "sEMG\u6a21\u5757\uff08\u4ea7\u54c1\u4ee3\u7801IKN\u2014\u2014\u8bca\u65ad\u7528\u808c\u7535\u56fe\uff09\u5f15\u7528Maquet/Getinge Servo-i NAVA\u4f5c\u4e3a\u4e3b\u8981\u524d\u7f6e\u5668\u68b0\u3002"
        "NAVA\u7cfb\u7edf\u5305\u542bEdi\u5bfc\u7ba1\uff0c\u7528\u4e8e\u6d4b\u91cf\u81a8\u808c\u7535\u6d3b\u52a8\u4ee5\u76d1\u6d4b\u795e\u7ecf\u547c\u5438\u9a71\u52a8\uff08NRD\uff09\u3002"
    )

    sub("\u5173\u952e\u5dee\u5f02\uff1a\u98df\u7ba1vs\u8868\u9762")
    body(
        "K082437\u4f7f\u7528\u98df\u7ba1\u5bfc\u7ba1\uff08Edi\uff09\u8fdb\u884c\u81a8\u808cEMG\uff0c\u800c\u6211\u4eec\u7684\u8bbe\u5907\u4f7f\u7528\u80f8\u58c1\u8868\u9762\u7535\u6781\u3002"
        "\u8fd9\u662f\u4f20\u611f\u5668\u6280\u672f\u7684\u6839\u672c\u5dee\u5f02\uff0cFDA\u5c06\u4e25\u683c\u5ba1\u67e5\u3002"
    )

    bul("\u76f8\u540c\u7684\u9884\u671f\u7528\u9014\u2014\u2014\u6d4b\u91cf\u795e\u7ecf\u547c\u5438\u9a71\u52a8\u7528\u4e8e\u547c\u5438\u673a\u4f18\u5316", bp="\u76f8\u4f3c\u6027\uff1a ")
    bul("\u4e0d\u540c\u7684\u4f20\u611f\u5668\u2014\u2014\u98df\u7ba1\u5bfc\u7ba1vs\u8868\u9762\u7535\u6781", bp="\u5dee\u5f02\uff1a ")
    bul("\u4e0d\u540c\u7684\u4fe1\u53f7\u2014\u2014\u76f4\u63a5\u81a8\u808cEMGvs\u901a\u8fc7\u80f8\u58c1\u7684\u8868\u9762EMG", bp="\u5dee\u5f02\uff1a ")
    bul("\u4e0d\u540c\u7684\u4fb5\u5165\u6027\u2014\u2014\u5bfc\u7ba1\uff08\u4fb5\u5165\u6027\uff09vs\u8868\u9762\uff08\u975e\u4fb5\u5165\u6027\uff09", bp="\u5dee\u5f02\uff1a ")

    callout(
        "FDA\u53ef\u80fd\u8bf4\uff1a\u201c\u4e0d\u540c\u7684\u6280\u672f\u7279\u5f81\u5f15\u53d1\u4e86\u4e0d\u540c\u7684\u5b89\u5168\u6027\u548c\u6709\u6548\u6027\u95ee\u9898\u3002\u201d"
        "\u8fd9\u662fFDA\u62d2\u7edd\u524d\u7f6e\u5668\u68b0\u65f6\u4f7f\u7528\u7684\u7279\u5b9a\u8bed\u8a00\u3002Pre-Sub Q\u4f1a\u8bae\u5fc5\u987b\u76f4\u63a5\u89e3\u51b3\u8fd9\u4e00\u95ee\u9898\u3002",
        style="warn"
    )

    # ── 4 ───────────────────────────────────────────────
    sec("4", "De Novo\u91cd\u5206\u7c7b\u98ce\u9669\u2014\u2014\u7ec4\u5408\u5e73\u53f0")

    body(
        "\u9664\u4e86\u5404\u6a21\u5757\u524d\u7f6e\u5668\u68b0\u88ab\u62d2\u5916\uff0c\u8fd8\u6709\u7b2c\u4e8c\u4e2a\u66f4\u9ad8\u5c42\u6b21\u7684\u98ce\u9669\uff1a"
        "FDA\u53ef\u80fd\u5c06\u7ec4\u5408sEMG+EIT\u96c6\u6210\u7cfb\u7edf\u89c6\u4e3a\u5355\u4e00\u65b0\u578b\u5668\u68b0\uff0c\u65e0\u524d\u7f6e\u5668\u68b0\uff0c"
        "\u9700\u8981De Novo\u5206\u7c7b\u800c\u975e\u4e24\u4e2a\u5355\u72ec\u7684510(k)\u3002"
    )

    sub("\u89e6\u53d1\u573a\u666f")
    bul("\u63d0\u4ea4\u4e24\u4e2a510(k)\u2014\u2014sEMG (IKN)\u548cEIT (QEB)")
    bul("\u6bcf\u4e2a\u63d0\u4ea4\u5747\u63d0\u53caMyoBus\u96c6\u6210\u548c\u201c\u6570\u5b57\u5b6a\u751f\u201d\u878d\u5408")
    bul("FDA\u5ba1\u67e5\u5458\u67e5\u770b\u4e24\u4e2a\u63d0\u4ea4\u540e\u8ba4\u5b9a\uff1a\u7ec4\u5408\u7cfb\u7edf\u662f\u65b0\u578b\u5668\u68b0")
    bul("FDA\u901a\u77e5\u7533\u8bf7\u4eba\u9700\u8981De Novo\u5206\u7c7b")

    sub("\u5f71\u54cd\u6bd4\u8f83")
    w3 = [50, 55, 65]
    trow(["\u56e0\u7d20", "\u4e24\u4e2a510(k)\uff08\u5f53\u524d\uff09", "De Novo\uff08\u5907\u7528\uff09"], w3, header=True)
    trow(["\u7528\u6237\u8d39", "~$13K ($6.5K x 2)", "~$130K"], w3, bold_first=True)
    trow(["\u5ba1\u67e5\u65f6\u95f4", "\u54043-6\u4e2a\u6708", "10-14\u4e2a\u6708"], w3, bold_first=True)
    trow(["\u8bc1\u636e\u8981\u6c42", "\u53f0\u67b6+\u6709\u9650\u4e34\u5e8a", "\u53ef\u80fd\u9700\u4e34\u5e8a\u7814\u7a76"], w3, bold_first=True)
    trow(["\u65f6\u95f4\u7ebf\u5f71\u54cd", "24\u4e2a\u6708\u8ba1\u5212\u4e0d\u53d8", "+6-12\u4e2a\u6708"], w3, bold_first=True)
    trow(["\u9884\u7b97\u5f71\u54cd", "\u5728\u4f30\u7b97\u5185", "\u603b\u8ba1+$200K-$400K"], w3, bold_first=True)
    trow(["\u7ade\u4e89\u62a4\u57ce\u6cb3", "\u524d\u7f6e\u5668\u68b0\u5df2\u5b58\u5728", "\u60a8\u521b\u5efa\u4ea7\u54c1\u4ee3\u7801"], w3, bold_first=True)
    pdf.ln(2)

    sub("\u7f13\u89e3\u7b56\u7565\uff085\u9879\u884c\u52a8\uff09")
    bul("Pre-Sub Q\u4f1a\u8bae\u76f4\u63a5\u8be2\u95eeFDA\uff1a\u201c\u6211\u4eec\u63d0\u8bae\u4e24\u4e2a\u6a21\u5757\u5316510(k)\u63d0\u4ea4\u3002\u6a21\u5757\u53ef\u72ec\u7acb\u529f\u80fd\u3002FDA\u662f\u5426\u8ba4\u53ef\uff1f\u201d",
        bp="1. \u76f4\u63a5\u8be2\u95eeFDA\uff1a ")
    bul("\u4f1a\u8bae\u524d\u7814\u7a76\u51c62-3\u4e2a\u66ff\u4ee3IKN\u524d\u7f6e\u5668\u68b0\uff08\u8868\u9762EMG\u8bbe\u5907\uff09\u3002",
        bp="2. \u5907\u7528\u524d\u7f6e\u5668\u68b0\uff1a ")
    bul("\u5728510(k)\u7533\u62a5\u4e2d\u5c06\u6bcf\u4e2a\u6a21\u5757\u63cf\u8ff0\u4e3a\u72ec\u7acb\u8bbe\u5907\u3002\u201c\u6570\u5b57\u5b6a\u751f\u201d\u4ec5\u63cf\u8ff0\u4e3a\u672a\u6765\u8ba1\u5212\u96c6\u6210\u3002",
        bp="3. \u8131\u94a9\u6570\u5b57\u5b6a\u751f\uff1a ")
    bul("\u5982FDA\u5728Pre-Sub\u8bf4\u9700\u8981De Novo\uff0c\u7acb\u5373\u8f6c\u5411\u3002M+2\u53d1\u73b0\u6bd4\u63d0\u4ea4\u540e\u53d1\u73b0\u8282\u7701$50K+\u3002",
        bp="4. \u65e9\u671f\u53d1\u73b0\uff1a ")
    bul("\u5982\u9700De Novo\uff0c\u60a8\u521b\u5efa\u5206\u7c7b\u3002\u60a8\u7684\u8bbe\u5907\u6210\u4e3a\u6240\u6709\u672a\u6765\u7ade\u4e89\u5bf9\u624b\u7684\u524d\u7f6e\u5668\u68b0\u3002\u8fd9\u662f\u91cd\u8981\u7684\u7ade\u4e89\u62a4\u57ce\u6cb3\u3002",
        bp="5. \u79ef\u6781\u9762\uff1a ")

    # ── 5 ───────────────────────────────────────────────
    sec("5", "PPTX K\u7f16\u53f7\u5ba1\u8ba1\u7ed3\u679c")

    body(
        "\u5bf9\u201cICU Digital Respiratory Twin.pptx\u201d\u7684\u6240\u6709\u6587\u672c\u548c\u8868\u683c\u5355\u5143\u683c\u8fdb\u884c\u4e86\u7cfb\u7edf\u63d0\u53d6\uff0c"
        "\u641c\u7d22\u5339\u914dFDA\u8bb8\u53ef\u7f16\u53f7\uff08K\u540e\u8ddf5-6\u4f4d\u6570\u5b57\uff09\u7684\u6a21\u5f0f\u3002"
    )

    callout(
        "\u539f\u59cbPPTX\u4e2d\u672a\u627e\u5230K\u7f16\u53f7\u3002PPTX\u4ec5\u5728\u4e24\u4e2a\u4f4d\u7f6e\u6cdb\u6cdb\u63d0\u53ca\u201c510(k)\u201d\uff1a"
        "\u5e7b\u706f\u724715\uff08\u4e2d\u6587\u8d39\u7528\u63d0\u53ca\uff09\u548c\u5e7b\u706f\u724716\uff08\u201cFDA 510(k) (sEMG)\u201d\u91cc\u7a0b\u7891\u6807\u7b7e\uff09\u3002"
        "\u4eea\u8868\u677f\u6570\u636e\u4e2d\u7684\u6240\u6709\u5177\u4f53K\u7f16\u53f7\u5747\u5728\u5f00\u53d1\u671f\u95f4\u6dfb\u52a0\u3002"
    )

    sub("\u4eea\u8868\u677f\u4e2d\u7684K\u7f16\u53f7")
    w4 = [30, 50, 50, 40]
    trow(["\u6a21\u5757", "\u524d\u7f6e\u5668\u68b0", "K\u7f16\u53f7", "\u72b6\u6001"], w4, header=True)
    trow(["EIT (DQS)", "Timpel Enlight 2100", "K250464", "\u4eceK213494\u66f4\u65b0"], w4, bold_first=True)
    trow(["sEMG (IKN)", "Maquet NAVA Edi", "K082437", "\u65b0\u589e\uff08\u539f\u65e0\u540d\u79f0\uff09"], w4, bold_first=True)

    # ── 6 ───────────────────────────────────────────────
    sec("6", "\u66f4\u65b0\u7684RISK-007 \u2014 \u4eea\u8868\u677f\u98ce\u9669\u767b\u8bb0\u518c")

    body(
        "RISK-007\u5df2\u4ece\u5355\u4e00\u573a\u666f\u98ce\u9669\u6269\u5c55\u4e3a\u53cc\u573a\u666f\u98ce\u9669\uff0c"
        "\u6db5\u76d6\u5404\u6a21\u5757\u524d\u7f6e\u5668\u68b0\u88ab\u62d2\u548c\u7ec4\u5408\u5e73\u53f0De Novo\u91cd\u5206\u7c7b\u3002"
    )

    sub("\u98ce\u9669\u5361")
    bul("510(k)\u88ab\u62d2\u6216De Novo\u91cd\u5206\u7c7b\u2014\u2014\u524d\u7f6e\u5668\u68b0\u672a\u88ab\u63a5\u53d7\u6216\u7ec4\u5408\u5e73\u53f0\u88ab\u8ba4\u5b9a\u4e3a\u65b0\u578b\u5668\u68b0", bp="\u6807\u9898\uff1a ")
    bul("\u9ad8", bp="\u4e25\u91cd\u6027\uff1a ")
    bul("\u4e2d", bp="\u6982\u7387\uff1a ")
    bul=bul
    bul("\u7ea2\u8272", bp="\u98ce\u9669\u7b49\u7ea7\uff1a ")
    bul("\u5982\u5728Pre-Sub(M+2)\u53d1\u73b0\u5219\u53ef\u63a7", bp="\u6b8b\u4f59\u98ce\u9669\uff1a ")

    sub("CAPA-004\uff1a\u524d\u7f6e\u5668\u68b0\u4e0eDe Novo\u5907\u7528\u7b56\u7565")
    bul("\u4e3asEMG\u8bc6\u522b2-3\u4e2aK082437\u4e4b\u5916\u7684\u66ff\u4ee3IKN\u524d\u7f6e\u5668\u68b0\uff08\u8868\u9762EMG\uff0c\u975e\u5bfc\u7ba1\u7c7b\uff09", bp="\u884c\u52a81\uff1a ")
    bul("\u51c6\u5907EIT V/Q\u58f0\u660e\u4f5c\u4e3a\u6027\u80fd\u589e\u5f3a\u800c\u975e\u65b0\u9884\u671f\u7528\u9014\u7684SE\u8bba\u8bc1", bp="\u884c\u52a82\uff1a ")
    bul("\u5982FDA\u62d2\u7edd\u6a21\u5757\u5316\u7b56\u7565\uff0c\u8d77\u8349\u7ec4\u5408\u5e73\u53f0De Novo\u9884\u63d0\u4ea4\u5305", bp="\u884c\u52a83\uff1a ")
    bul("$130K De Novo\u8d39\u7528 + $200K\u4e34\u5e8a\u7814\u7a76\u5907\u7528\u91d1", bp="\u9884\u7b97\u50a8\u5907\uff1a ")

    # ── 7 ───────────────────────────────────────────────
    sec("7", "\u5efa\u8bae\u4e0e\u4e0b\u4e00\u6b65")

    bul("\u4e24\u4e2a\u98ce\u9669\u90fd\u901a\u8fc7\u540c\u4e00\u4e2a\u95e8\u5173\uff1aPre-Sub Q\u4f1a\u8bae(R1/R2)\u3002\u8be5\u4f1a\u8bae\u6b63\u662f\u4e3a\u6b64\u800c\u8bbe\u8ba1\u7684\u3002")
    bul("\u6700\u574f\u7ed3\u679c\uff1a\u82b1\u8d396+\u4e2a\u6708\u51c6\u5907\u63d0\u4ea4\u5305\uff0c\u7ed3\u679cFDA\u5728\u5ba1\u67e5\u65f6\u62d2\u7edd\u524d\u7f6e\u5668\u68b0\u7b56\u7565\u3002")
    bul("\u524d2\u4e2a\u6708\u7684\u6700\u4f73\u5229\u7528\uff1a\u5728\u6295\u5165\u6d4b\u8bd5\u8d44\u6e90\u524d\u83b7\u53d6FDA\u5bf9\u524d\u7f6e\u5668\u68b0\u9009\u62e9\u548c\u6a21\u5757\u5316vs\u96c6\u6210\u5206\u7c7b\u7684\u4e66\u9762\u7acb\u573a\u3002")
    bul("\u4eea\u8868\u677f\u5df2\u6b63\u786e\u6392\u5e8f\uff1aR1\u5728M+0\uff0cR2\u5728M+2\uff0c\u6d4b\u8bd5\u4ec5\u5728FDA\u53cd\u9988\u540e\u5f00\u59cb\u3002")
    pdf.ln(2)

    callout(
        "\u5e95\u7ebf\uff1aPre-Sub Q\u4f1a\u8bae\u4e0d\u662f\u53ef\u9009\u7684\u2014\u2014\u5b83\u662f\u6574\u4e2a\u9879\u76ee\u4e2d\u6700\u91cd\u8981\u7684\u5355\u4e00\u98ce\u9669\u7f13\u89e3\u884c\u52a8\u3002"
        "\u6240\u6709\u524d\u7f6e\u5668\u68b0\u548c\u5206\u7c7b\u95ee\u9898\u5fc5\u987b\u5728\u4efb\u4f55\u91cd\u5927\u6d4b\u8bd5\u652f\u51fa\u4e4b\u524d\u89e3\u51b3\u3002"
    )

    out = os.path.join(os.path.dirname(__file__), "Regulatory_Strategy_Analysis_CN.pdf")
    pdf.output(out)
    print(f"CN PDF: {out}")


if __name__ == "__main__":
    build_en()
    build_cn()
