"""Generate English and Chinese roadmap checklist PDFs for ICU Respiratory Digital Twin."""
from fpdf import FPDF

# ── Colors ──────────────────────────────────────────────────────
DARK   = (30, 30, 35)
BLUE   = (25, 70, 170)
GREEN  = (20, 130, 60)
YELLOW = (180, 140, 0)
RED    = (190, 40, 30)
PURPLE = (110, 50, 160)
ORANGE = (200, 110, 20)
GRAY   = (100, 100, 110)
RULE   = (180, 180, 190)
CHECK_GRAY = (160, 160, 170)
BG_BLUE   = (230, 240, 255)
BG_GREEN  = (225, 248, 230)
BG_YELLOW = (255, 248, 220)
BG_RED    = (255, 230, 228)
BG_PURPLE = (242, 230, 255)
BG_ORANGE = (255, 240, 220)

FONT_PATH = "/Library/Fonts/Arial Unicode.ttf"
FONT_NAME = "ARUNI"


class Checklist(FPDF):
    """Base checklist PDF with checkbox helpers."""

    def __init__(self, use_cjk=False):
        super().__init__()
        self.use_cjk = use_cjk
        if use_cjk:
            self.add_font(FONT_NAME, "", FONT_PATH)
            self.add_font(FONT_NAME, "B", FONT_PATH)
            self.add_font(FONT_NAME, "I", FONT_PATH)
        self.set_auto_page_break(auto=True, margin=18)
        self._fn = FONT_NAME if use_cjk else "Helvetica"

    # ── primitives ──────────────────────────────────────────────

    def _font(self, style="", size=10):
        self.set_font(self._fn, style, size)

    def cover(self, title, subtitle, date_str):
        self.add_page()
        self.set_margin(18)
        self.ln(30)
        self._font("B", 26)
        self.set_text_color(*BLUE)
        self.multi_cell(0, 11, title, align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(6)
        self._font("", 12)
        self.set_text_color(*GRAY)
        self.multi_cell(0, 6, subtitle, align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(20)
        self._font("", 10)
        self.set_text_color(*DARK)
        self.cell(0, 6, date_str, align="C", new_x="LMARGIN", new_y="NEXT")

    def phase_banner(self, label, color, bg):
        self.ln(4)
        self.set_fill_color(*bg)
        self.set_draw_color(*color)
        self.set_line_width(0.6)
        self._font("B", 13)
        self.set_text_color(*color)
        x = self.l_margin
        w = self.w - self.l_margin - self.r_margin
        y = self.get_y()
        self.rect(x, y, w, 9, style="DF")
        self.set_xy(x + 4, y + 1)
        self.cell(w - 8, 7, label, new_x="LMARGIN", new_y="NEXT")
        self.ln(3)

    def rule(self):
        self.set_draw_color(*RULE)
        self.set_line_width(0.3)
        y = self.get_y()
        self.line(self.l_margin, y, self.w - self.r_margin, y)
        self.ln(3)

    def step_header(self, number, title):
        self.rule()
        self._font("B", 11)
        self.set_text_color(*DARK)
        label = f"{number})  {title}"
        self.cell(0, 6, label, new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def note(self, text):
        self._font("I", 9)
        self.set_text_color(*GRAY)
        self.set_x(self.l_margin + 4)
        self.multi_cell(0, 4.5, text, new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def sub_label(self, text):
        self._font("B", 10)
        self.set_text_color(*BLUE)
        self.set_x(self.l_margin + 2)
        self.cell(0, 5.5, text, new_x="LMARGIN", new_y="NEXT")
        self.ln(0.5)

    def checkbox(self, text, indent=0):
        """Draw an empty checkbox square followed by text."""
        self._font("", 10)
        self.set_text_color(*DARK)
        x0 = self.l_margin + 6 + indent
        y0 = self.get_y() + 0.8
        box = 3.2
        # draw box
        self.set_draw_color(*CHECK_GRAY)
        self.set_line_width(0.35)
        self.rect(x0, y0, box, box)
        # text
        self.set_xy(x0 + box + 2, y0 - 0.5)
        self.multi_cell(self.w - self.r_margin - x0 - box - 3, 4.8, text,
                        new_x="LMARGIN", new_y="NEXT")
        if self.get_y() - y0 < 5:
            self.set_y(y0 + 5)

    def callout(self, text):
        self._font("B", 9)
        self.set_text_color(*ORANGE)
        self.set_x(self.l_margin + 6)
        self.multi_cell(0, 4.5, text, new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def body(self, text):
        self._font("", 10)
        self.set_text_color(*DARK)
        self.multi_cell(0, 5, text, new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def bold_body(self, text):
        self._font("B", 10)
        self.set_text_color(*DARK)
        self.multi_cell(0, 5, text, new_x="LMARGIN", new_y="NEXT")
        self.ln(1)


# ════════════════════════════════════════════════════════════════
#  ENGLISH VERSION
# ════════════════════════════════════════════════════════════════
def build_english():
    pdf = Checklist(use_cjk=False)

    # Cover
    pdf.cover(
        "ICU Respiratory Digital Twin\nExecution Roadmap & Checklist",
        "sEMG Neural Drive  +  EIT V/Q Imaging\nModular 510(k) Strategy",
        "Prepared March 2026"
    )

    # ── OVERALL STRATEGY ────────────────────────────────────────
    pdf.add_page()
    pdf.set_margin(18)
    pdf.phase_banner("OVERALL STRATEGY  --  Anchor Everything to This", BLUE, BG_BLUE)
    pdf.body("You are running a modular approval plan:")
    pdf.checkbox("Module A (sEMG) -> faster 510(k), lower risk")
    pdf.checkbox("Module B (EIT) -> follows after validation")
    pdf.ln(1)
    pdf.callout("> This is explicitly your fastest path to value creation and funding inflection.")

    # ── FIRST 90 DAYS ───────────────────────────────────────────
    pdf.phase_banner("FIRST 90 DAYS  --  Critical Window", GREEN, BG_GREEN)

    # Step 1
    pdf.step_header(1, "Lock Structure (Non-negotiable)  --  Week 1-2")
    pdf.sub_label("Confirm:")
    pdf.checkbox("IP assigned to US entity")
    pdf.checkbox("Roles defined: CEO, CTO (PhD), PM/Operations")
    pdf.sub_label("Create:")
    pdf.checkbox("Cap table")
    pdf.checkbox("Advisor agreements")

    # Step 2
    pdf.step_header(2, "Build Your Control System  --  Week 1-2")
    pdf.note("Start simple (spreadsheet or Notion) with 4 core tabs:")
    pdf.checkbox("Milestones tab")
    pdf.checkbox("Regulatory tab")
    pdf.checkbox("Risks tab")
    pdf.checkbox("Cash / Runway tab")

    # Step 3
    pdf.step_header(3, "Prepare Pre-Submission (Q-Sub)  --  Week 2-4")
    pdf.note("Through the U.S. Food and Drug Administration")
    pdf.sub_label("Confirm:")
    pdf.checkbox("Predicate device (NAVA / Timpel strategy)")
    pdf.checkbox("Testing plan")
    pdf.checkbox("Software classification")
    pdf.callout("> Do NOT skip or delay this. Already planned at M+0.")

    # Step 4
    pdf.step_header(4, "Freeze Module A Scope (sEMG)  --  Week 2-4")
    pdf.checkbox("Define what IS included in first 510(k)")
    pdf.checkbox("Define what is NOT included")
    pdf.callout("> Prevents scope creep from the PhD side.")

    # Step 5
    pdf.step_header(5, "Build the Milestone Narrative  --  Week 3-6")
    pdf.note("Translate your roadmap into investor language:")
    pdf.checkbox("\"$X gets us to Pre-Sub meeting\"")
    pdf.checkbox("\"$Y gets us to 510(k) submission\"")
    pdf.checkbox("\"$Z gets us to clearance\"")
    pdf.sub_label("Timeline anchors:")
    pdf.checkbox("M+2 -> FDA meeting")
    pdf.checkbox("M+6 -> submission")
    pdf.checkbox("M+9 -> clearance")

    # Step 6
    pdf.step_header(6, "Start Investor Updates (even pre-funding)  --  Week 3-6")
    pdf.note("Every 2-4 weeks send:")
    pdf.checkbox("What we achieved")
    pdf.checkbox("What's next")
    pdf.checkbox("Risks")
    pdf.checkbox("Cash position")
    pdf.callout("> This builds trust early.")

    # Step 7
    pdf.step_header(7, "Launch Bench & Verification Testing  --  Week 4-8")
    pdf.checkbox("IEC 60601 (safety) testing")
    pdf.checkbox("EMC testing")
    pdf.checkbox("sEMG validation vs esophageal reference")
    pdf.callout("> These are critical path items.")

    # Step 8
    pdf.step_header(8, "Implement Quality System (QMS Lite -> Full)  --  Week 4-8")
    pdf.sub_label("Start with:")
    pdf.checkbox("Design History File (DHF)")
    pdf.checkbox("Risk management (ISO 14971)")
    pdf.checkbox("Document control")
    pdf.sub_label("Then expand toward:")
    pdf.checkbox("Full 21 CFR 820 compliance")

    # Step 9
    pdf.step_header(9, "Activate Risk Dashboard  --  Week 6-10")
    pdf.sub_label("From your risk table:")
    pdf.checkbox("False negatives")
    pdf.checkbox("ECG artifact errors")
    pdf.checkbox("Misinterpretation risk")
    pdf.checkbox("Cybersecurity")
    pdf.sub_label("Turn into:")
    pdf.checkbox("Top 5 weekly risks identified")
    pdf.checkbox("Mitigation owner assigned")
    pdf.checkbox("Status (red/yellow/green) updated")

    # Step 10
    pdf.step_header(10, "Conduct Pre-Sub Meeting  --  Week 8-12")
    pdf.sub_label("Outcomes you need -- agreement on:")
    pdf.checkbox("Predicate device")
    pdf.checkbox("Testing requirements")
    pdf.checkbox("Submission structure")
    pdf.callout("> This is your biggest de-risking moment.")

    # ── MONTHS 3-6 ──────────────────────────────────────────────
    pdf.phase_banner("MONTHS 3-6  --  Build to Submission", YELLOW, BG_YELLOW)

    # Step 11
    pdf.step_header(11, "Complete Testing (Parallel Workstreams)")
    pdf.sub_label("Technical:")
    pdf.checkbox("Finalize sEMG performance")
    pdf.checkbox("Validate algorithms")
    pdf.sub_label("Regulatory:")
    pdf.checkbox("Biocompatibility (ISO 10993)")
    pdf.checkbox("Electrical safety")
    pdf.checkbox("Software documentation")

    # Step 12
    pdf.step_header(12, "Build 510(k) Package")
    pdf.checkbox("Device description")
    pdf.checkbox("Substantial equivalence")
    pdf.checkbox("Risk analysis")
    pdf.checkbox("Labeling")
    pdf.callout("> Now it becomes execution.")

    # Step 13
    pdf.step_header(13, "Raise Funding (Timed to Momentum)")
    pdf.note("Best window: after Pre-Sub feedback, during strong test results.")
    pdf.checkbox("Funding pitch prepared")
    pdf.checkbox("Investor outreach begun")
    pdf.checkbox("Message locked: \"Defined path to clearance in ~6 months\"")

    # ── MONTHS 6-12 ─────────────────────────────────────────────
    pdf.phase_banner("MONTHS 6-12  --  Value Inflection", RED, BG_RED)

    # Step 14
    pdf.step_header(14, "Submit 510(k) (Module A)")
    pdf.checkbox("510(k) Module A submitted to FDA")
    pdf.checkbox("~90-day review tracked")
    pdf.checkbox("AI/additional-info requests responded to")

    # Step 15
    pdf.step_header(15, "Prepare Module B (EIT in Parallel)")
    pdf.checkbox("V/Q validation started")
    pdf.checkbox("EIT-specific testing underway")
    pdf.checkbox("Predicate comparison completed")
    pdf.callout("> Don't wait -- parallelize.")

    # Step 16
    pdf.step_header(16, "Prepare Manufacturing")
    pdf.checkbox("Audit manufacturer (China site)")
    pdf.checkbox("ISO 13485 confirmed")
    pdf.checkbox("FDA registration completed")

    # ── MONTHS 12-24 ────────────────────────────────────────────
    pdf.phase_banner("MONTHS 12-24  --  Scale", PURPLE, BG_PURPLE)

    # Step 17
    pdf.step_header(17, "Clearance -> Launch (Module A)")
    pdf.checkbox("Limited clinical rollout")
    pdf.checkbox("Real-world data collection begun")

    # Step 18
    pdf.step_header(18, "Submit Module B (EIT)")
    pdf.checkbox("M+17 submission completed")
    pdf.checkbox("M+23 clearance tracked")

    # Step 19
    pdf.step_header(19, "Expand to Full Platform")
    pdf.checkbox("Integrate MyoBus system")
    pdf.checkbox("Position as \"complete respiratory monitoring platform\"")

    # ── WEEKLY OPERATING SYSTEM ─────────────────────────────────
    pdf.phase_banner("WEEKLY OPERATING SYSTEM  --  Run This Every Week", ORANGE, BG_ORANGE)

    pdf.sub_label("1) Technical Check (PhD)")
    pdf.checkbox("What improved?")
    pdf.checkbox("What failed?")
    pdf.sub_label("2) Regulatory Check")
    pdf.checkbox("What moved toward submission?")
    pdf.checkbox("Any blockers?")
    pdf.sub_label("3) Business Check")
    pdf.checkbox("Runway reviewed")
    pdf.checkbox("Investor communication sent")
    pdf.sub_label("4) Risk Review")
    pdf.checkbox("Top 3 risks identified")
    pdf.checkbox("Mitigation progress updated")

    # ── TOP 5 ───────────────────────────────────────────────────
    pdf.ln(2)
    pdf.rule()
    pdf._font("B", 12)
    pdf.set_text_color(*RED)
    pdf.cell(0, 7, "THE 5 MOST IMPORTANT THINGS YOU MUST CONTROL", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(1)
    pdf.checkbox("1. Scope discipline (Module A first)")
    pdf.checkbox("2. FDA alignment early (Pre-Sub)")
    pdf.checkbox("3. Testing on schedule (critical path)")
    pdf.checkbox("4. Cash vs milestone timing")
    pdf.checkbox("5. Translation between tech and investor language")

    # ── ASSESSMENT ──────────────────────────────────────────────
    pdf.ln(4)
    pdf.rule()
    pdf._font("B", 11)
    pdf.set_text_color(*DARK)
    pdf.cell(0, 6, "Assessment", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(1)
    pdf.body(
        "You are in a strong position because:\n"
        "  - The regulatory strategy is already well thought out\n"
        "  - The modular approach reduces risk\n"
        "  - The clinical need is clear"
    )
    pdf._font("B", 10)
    pdf.set_text_color(*RED)
    pdf.multi_cell(0, 5,
        "The biggest risk is NOT the technology.\n"
        "It is: misalignment between timeline, funding, and regulatory reality.",
        new_x="LMARGIN", new_y="NEXT")

    out = "ICU_Roadmap_Checklist_EN.pdf"
    pdf.output(out)
    print(f"English checklist: {out}")


# ════════════════════════════════════════════════════════════════
#  CHINESE VERSION
# ════════════════════════════════════════════════════════════════
def build_chinese():
    pdf = Checklist(use_cjk=True)

    pdf.cover(
        "ICU \u547c\u5438\u6570\u5b57\u5b5e\u751f\n\u6267\u884c\u8def\u7ebf\u56fe\u4e0e\u68c0\u67e5\u6e05\u5355",
        "sEMG \u795e\u7ecf\u9a71\u52a8  +  EIT V/Q \u6210\u50cf\n\u6a21\u5757\u5316 510(k) \u7b56\u7565",
        "2026\u5e743\u6708\u7f16\u5236"
    )

    # ── FIRST 90 DAYS ───────────────────────────────────────────
    pdf.add_page()
    pdf.set_margin(18)
    pdf.phase_banner("\u524d 90 \u5929 \u2014 \u5173\u952e\u7a97\u53e3\u671f", GREEN, BG_GREEN)

    pdf.step_header(1, "\u9501\u5b9a\u7ed3\u6784\uff08\u4e0d\u53ef\u534f\u5546\uff09\u2014 \u7b2c 1\u20132 \u5468")
    pdf.sub_label("\u786e\u8ba4\uff1a")
    pdf.checkbox("IP \u5df2\u8f6c\u8ba9\u7ed9\u7f8e\u56fd\u5b9e\u4f53")
    pdf.checkbox("\u89d2\u8272\u5b9a\u4e49\uff1aCEO\u3001CTO\uff08\u535a\u58eb\uff09\u3001PM/\u8fd0\u8425")
    pdf.sub_label("\u521b\u5efa\uff1a")
    pdf.checkbox("\u80a1\u6743\u7ed3\u6784\u8868")
    pdf.checkbox("\u987e\u95ee\u534f\u8bae")

    pdf.step_header(2, "\u5efa\u7acb\u63a7\u5236\u7cfb\u7edf \u2014 \u7b2c 1\u20132 \u5468")
    pdf.note("\u4ece\u7b80\u5355\u5f00\u59cb\uff08\u7535\u5b50\u8868\u683c\u6216 Notion\uff09\uff0c4 \u4e2a\u6838\u5fc3\u9009\u9879\u5361\uff1a")
    pdf.checkbox("\u91cc\u7a0b\u7891\u9009\u9879\u5361")
    pdf.checkbox("\u6cd5\u89c4\u9009\u9879\u5361")
    pdf.checkbox("\u98ce\u9669\u9009\u9879\u5361")
    pdf.checkbox("\u73b0\u91d1/\u8dd1\u9053\u9009\u9879\u5361")

    pdf.step_header(3, "\u51c6\u5907\u9884\u63d0\u4ea4 (Q-Sub) \u2014 \u7b2c 2\u20134 \u5468")
    pdf.note("\u901a\u8fc7\u7f8e\u56fd\u98df\u54c1\u836f\u54c1\u76d1\u7763\u7ba1\u7406\u5c40 (FDA)")
    pdf.sub_label("\u786e\u8ba4\uff1a")
    pdf.checkbox("\u53c2\u8003\u8bbe\u5907\uff08NAVA / Timpel \u7b56\u7565\uff09")
    pdf.checkbox("\u6d4b\u8bd5\u8ba1\u5212")
    pdf.checkbox("\u8f6f\u4ef6\u5206\u7c7b")
    pdf.callout("\u27a4 \u4e0d\u8981\u8df3\u8fc7\u6216\u5ef6\u8fdf\u3002\u5df2\u5728 M+0 \u89c4\u5212\u4e2d\u3002")

    pdf.step_header(4, "\u51bb\u7ed3\u6a21\u5757 A \u8303\u56f4 (sEMG) \u2014 \u7b2c 2\u20134 \u5468")
    pdf.checkbox("\u5b9a\u4e49\u7b2c\u4e00\u6b21 510(k) \u5305\u542b\u7684\u5185\u5bb9")
    pdf.checkbox("\u5b9a\u4e49\u4e0d\u5305\u542b\u7684\u5185\u5bb9")
    pdf.callout("\u27a4 \u9632\u6b62\u535a\u58eb\u65b9\u9762\u7684\u8303\u56f4\u8513\u5ef6\u3002")

    pdf.step_header(5, "\u6784\u5efa\u91cc\u7a0b\u7891\u53d9\u4e8b \u2014 \u7b2c 3\u20136 \u5468")
    pdf.note("\u5c06\u8def\u7ebf\u56fe\u8f6c\u5316\u4e3a\u6295\u8d44\u8005\u8bed\u8a00\uff1a")
    pdf.checkbox("\"$X \u8ba9\u6211\u4eec\u5230\u8fbe\u9884\u63d0\u4ea4\u4f1a\u8bae\"")
    pdf.checkbox("\"$Y \u8ba9\u6211\u4eec\u5230\u8fbe 510(k) \u63d0\u4ea4\"")
    pdf.checkbox("\"$Z \u8ba9\u6211\u4eec\u5230\u8fbe\u83b7\u6279\"")
    pdf.sub_label("\u65f6\u95f4\u7ebf\u951a\u70b9\uff1a")
    pdf.checkbox("M+2 \u2192 FDA \u4f1a\u8bae")
    pdf.checkbox("M+6 \u2192 \u63d0\u4ea4")
    pdf.checkbox("M+9 \u2192 \u83b7\u6279")

    pdf.step_header(6, "\u5f00\u59cb\u6295\u8d44\u8005\u66f4\u65b0\uff08\u5373\u4f7f\u878d\u8d44\u524d\uff09\u2014 \u7b2c 3\u20136 \u5468")
    pdf.note("\u6bcf 2\u20134 \u5468\u53d1\u9001\uff1a")
    pdf.checkbox("\u6211\u4eec\u53d6\u5f97\u4e86\u4ec0\u4e48\u6210\u679c")
    pdf.checkbox("\u4e0b\u4e00\u6b65\u662f\u4ec0\u4e48")
    pdf.checkbox("\u98ce\u9669")
    pdf.checkbox("\u73b0\u91d1\u72b6\u51b5")
    pdf.callout("\u27a4 \u8fd9\u80fd\u65e9\u671f\u5efa\u7acb\u4fe1\u4efb\u3002")

    pdf.step_header(7, "\u542f\u52a8\u53f0\u67b6\u4e0e\u9a8c\u8bc1\u6d4b\u8bd5 \u2014 \u7b2c 4\u20138 \u5468")
    pdf.checkbox("IEC 60601\uff08\u5b89\u5168\uff09\u6d4b\u8bd5")
    pdf.checkbox("EMC \u6d4b\u8bd5")
    pdf.checkbox("sEMG \u4e0e\u98df\u7ba1\u53c2\u8003\u7684\u9a8c\u8bc1")
    pdf.callout("\u27a4 \u8fd9\u4e9b\u662f\u5173\u952e\u8def\u5f84\u9879\u76ee\u3002")

    pdf.step_header(8, "\u5b9e\u65bd\u8d28\u91cf\u4f53\u7cfb (QMS \u7cbe\u7b80\u7248 \u2192 \u5b8c\u6574\u7248) \u2014 \u7b2c 4\u20138 \u5468")
    pdf.sub_label("\u5148\u5f00\u59cb\uff1a")
    pdf.checkbox("\u8bbe\u8ba1\u5386\u53f2\u6587\u4ef6 (DHF)")
    pdf.checkbox("\u98ce\u9669\u7ba1\u7406 (ISO 14971)")
    pdf.checkbox("\u6587\u4ef6\u63a7\u5236")
    pdf.sub_label("\u7136\u540e\u6269\u5c55\u5230\uff1a")
    pdf.checkbox("\u5b8c\u6574 21 CFR 820 \u5408\u89c4")

    pdf.step_header(9, "\u6fc0\u6d3b\u98ce\u9669\u4eea\u8868\u677f \u2014 \u7b2c 6\u201310 \u5468")
    pdf.sub_label("\u6765\u81ea\u60a8\u7684\u98ce\u9669\u8868\uff1a")
    pdf.checkbox("\u5047\u9634\u6027")
    pdf.checkbox("ECG \u4f2a\u5f71\u9519\u8bef")
    pdf.checkbox("\u8bef\u89e3\u98ce\u9669")
    pdf.checkbox("\u7f51\u7edc\u5b89\u5168")
    pdf.sub_label("\u8f6c\u5316\u4e3a\uff1a")
    pdf.checkbox("\u8bc6\u522b\u6bcf\u5468\u524d 5 \u5927\u98ce\u9669")
    pdf.checkbox("\u5206\u914d\u7f13\u89e3\u8d1f\u8d23\u4eba")
    pdf.checkbox("\u66f4\u65b0\u72b6\u6001\uff08\u7ea2/\u9ec4/\u7eff\uff09")

    pdf.step_header(10, "\u5f00\u5c55\u9884\u63d0\u4ea4\u4f1a\u8bae \u2014 \u7b2c 8\u201312 \u5468")
    pdf.sub_label("\u60a8\u9700\u8981\u7684\u7ed3\u679c \u2014 \u5c31\u4ee5\u4e0b\u5185\u5bb9\u8fbe\u6210\u4e00\u81f4\uff1a")
    pdf.checkbox("\u53c2\u8003\u8bbe\u5907")
    pdf.checkbox("\u6d4b\u8bd5\u8981\u6c42")
    pdf.checkbox("\u63d0\u4ea4\u7ed3\u6784")
    pdf.callout("\u27a4 \u8fd9\u662f\u60a8\u6700\u5927\u7684\u964d\u4f4e\u98ce\u9669\u65f6\u523b\u3002")

    # ── MONTHS 3–6 ──────────────────────────────────────────────
    pdf.phase_banner("\u7b2c 3\u20136 \u4e2a\u6708 \u2014 \u6784\u5efa\u5230\u63d0\u4ea4", YELLOW, BG_YELLOW)

    pdf.step_header(11, "\u5b8c\u6210\u6d4b\u8bd5\uff08\u5e76\u884c\u5de5\u4f5c\u6d41\uff09")
    pdf.sub_label("\u6280\u672f\uff1a")
    pdf.checkbox("\u5b8c\u6210 sEMG \u6027\u80fd\u9a8c\u8bc1")
    pdf.checkbox("\u9a8c\u8bc1\u7b97\u6cd5")
    pdf.sub_label("\u6cd5\u89c4\uff1a")
    pdf.checkbox("\u751f\u7269\u76f8\u5bb9\u6027 (ISO 10993)")
    pdf.checkbox("\u7535\u6c14\u5b89\u5168")
    pdf.checkbox("\u8f6f\u4ef6\u6587\u6863")

    pdf.step_header(12, "\u6784\u5efa 510(k) \u5305")
    pdf.checkbox("\u8bbe\u5907\u63cf\u8ff0")
    pdf.checkbox("\u5b9e\u8d28\u7b49\u6548\u6027")
    pdf.checkbox("\u98ce\u9669\u5206\u6790")
    pdf.checkbox("\u6807\u7b7e")
    pdf.callout("\u27a4 \u73b0\u5728\u5c31\u662f\u6267\u884c\u3002")

    pdf.step_header(13, "\u878d\u8d44\uff08\u5339\u914d\u52bf\u5934\u65f6\u673a\uff09")
    pdf.note("\u6700\u4f73\u7a97\u53e3\uff1a\u9884\u63d0\u4ea4\u53cd\u9988\u540e\uff0c\u6d4b\u8bd5\u7ed3\u679c\u826f\u597d\u65f6\u3002")
    pdf.checkbox("\u878d\u8d44\u6f14\u8bb2\u51c6\u5907\u5b8c\u6bd5")
    pdf.checkbox("\u6295\u8d44\u8005\u62d3\u5c55\u5df2\u5f00\u59cb")
    pdf.checkbox("\u4fe1\u606f\u786e\u5b9a\uff1a\"\u6e05\u6670\u7684\u83b7\u6279\u8def\u5f84\uff0c\u7ea6 6 \u4e2a\u6708\"")

    # ── MONTHS 6–12 ─────────────────────────────────────────────
    pdf.phase_banner("\u7b2c 6\u201312 \u4e2a\u6708 \u2014 \u4ef7\u503c\u8f6c\u6298\u70b9", RED, BG_RED)

    pdf.step_header(14, "\u63d0\u4ea4 510(k)\uff08\u6a21\u5757 A\uff09")
    pdf.checkbox("510(k) \u6a21\u5757 A \u5df2\u63d0\u4ea4\u81f3 FDA")
    pdf.checkbox("\u8ddf\u8e2a ~90 \u5929\u5ba1\u67e5")
    pdf.checkbox("\u5df2\u56de\u5e94 AI/\u8865\u5145\u4fe1\u606f\u8bf7\u6c42")

    pdf.step_header(15, "\u51c6\u5907\u6a21\u5757 B\uff08EIT \u5e76\u884c\u63a8\u8fdb\uff09")
    pdf.checkbox("V/Q \u9a8c\u8bc1\u5df2\u5f00\u59cb")
    pdf.checkbox("EIT \u4e13\u9879\u6d4b\u8bd5\u8fdb\u884c\u4e2d")
    pdf.checkbox("\u53c2\u8003\u8bbe\u5907\u5bf9\u6bd4\u5df2\u5b8c\u6210")
    pdf.callout("\u27a4 \u4e0d\u8981\u7b49\u5f85 \u2014 \u5e76\u884c\u63a8\u8fdb\u3002")

    pdf.step_header(16, "\u51c6\u5907\u5236\u9020")
    pdf.checkbox("\u5ba1\u8ba1\u5236\u9020\u5546\uff08\u4e2d\u56fd\u5de5\u5382\uff09")
    pdf.checkbox("ISO 13485 \u5df2\u786e\u8ba4")
    pdf.checkbox("FDA \u6ce8\u518c\u5df2\u5b8c\u6210")

    # ── MONTHS 12–24 ────────────────────────────────────────────
    pdf.phase_banner("\u7b2c 12\u201324 \u4e2a\u6708 \u2014 \u89c4\u6a21\u5316", PURPLE, BG_PURPLE)

    pdf.step_header(17, "\u83b7\u6279 \u2192 \u4e0a\u5e02\uff08\u6a21\u5757 A\uff09")
    pdf.checkbox("\u6709\u9650\u4e34\u5e8a\u63a8\u5e7f")
    pdf.checkbox("\u5f00\u59cb\u6536\u96c6\u771f\u5b9e\u4e16\u754c\u6570\u636e")

    pdf.step_header(18, "\u63d0\u4ea4\u6a21\u5757 B (EIT)")
    pdf.checkbox("M+17 \u63d0\u4ea4\u5df2\u5b8c\u6210")
    pdf.checkbox("M+23 \u83b7\u6279\u8ddf\u8e2a\u4e2d")

    pdf.step_header(19, "\u6269\u5c55\u4e3a\u5b8c\u6574\u5e73\u53f0")
    pdf.checkbox("\u96c6\u6210 MyoBus \u7cfb\u7edf")
    pdf.checkbox("\u5b9a\u4f4d\u4e3a\"\u5b8c\u6574\u547c\u5438\u76d1\u6d4b\u5e73\u53f0\"")

    # ── WEEKLY OPERATING SYSTEM ─────────────────────────────────
    pdf.phase_banner("\u6bcf\u5468\u8fd0\u8425\u7cfb\u7edf \u2014 \u6bcf\u5468\u6267\u884c", ORANGE, BG_ORANGE)

    pdf.sub_label("1) \u6280\u672f\u68c0\u67e5\uff08\u535a\u58eb\uff09")
    pdf.checkbox("\u6709\u4ec0\u4e48\u6539\u8fdb\uff1f")
    pdf.checkbox("\u6709\u4ec0\u4e48\u5931\u8d25\uff1f")
    pdf.sub_label("2) \u6cd5\u89c4\u68c0\u67e5")
    pdf.checkbox("\u4ec0\u4e48\u5411\u63d0\u4ea4\u63a8\u8fdb\u4e86\uff1f")
    pdf.checkbox("\u6709\u4efb\u4f55\u963b\u788d\u5417\uff1f")
    pdf.sub_label("3) \u4e1a\u52a1\u68c0\u67e5")
    pdf.checkbox("\u8dd1\u9053\u5ba1\u67e5")
    pdf.checkbox("\u6295\u8d44\u8005\u6c9f\u901a\u5df2\u53d1\u9001")
    pdf.sub_label("4) \u98ce\u9669\u5ba1\u67e5")
    pdf.checkbox("\u8bc6\u522b\u524d 3 \u5927\u98ce\u9669")
    pdf.checkbox("\u7f13\u89e3\u8fdb\u5c55\u5df2\u66f4\u65b0")

    out = "ICU_Roadmap_Checklist_CN.pdf"
    pdf.output(out)
    print(f"Chinese checklist: {out}")


if __name__ == "__main__":
    build_english()
    build_chinese()
    print("Done.")
