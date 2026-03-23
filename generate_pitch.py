#!/usr/bin/env python3
"""
Generate a professional pitch PDF from Lon Dailey (Stanford SCPM)
to Dr. Dai (Chief Technology Scientist) on why Lon should serve as
PMP for the ICU Respiratory Digital Twin project.
"""

import os
from fpdf import FPDF

OUT = os.path.dirname(os.path.abspath(__file__))

_MAP = str.maketrans({
    "\u2014": "--", "\u2013": "-", "\u2019": "'", "\u201c": '"', "\u201d": '"',
    "\u2018": "'", "\u2265": ">=", "\u2264": "<=", "\u00b5": "u", "\u00d7": "x",
    "\u2022": "-", "\u2026": "...", "\u00ae": "(R)",
})
def _a(s):
    return s.translate(_MAP)


class PitchPDF(FPDF):
    CARDINAL = (140, 21, 21)     # Stanford cardinal red
    DARK = (35, 35, 40)
    GRAY = (110, 110, 120)
    SANDSTONE = (210, 194, 149)  # Stanford sandstone
    ACCENT = (0, 98, 71)        # Stanford dark green
    WHITE = (255, 255, 255)

    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(*self.GRAY)
        self.cell(0, 4, _a("CONFIDENTIAL -- Lon Dailey  |  Stanford SCPM  |  PMP Engagement Proposal"), align="R")
        self.ln(5)

    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(*self.GRAY)
        self.cell(0, 4, f"Page {self.page_no()}/{{nb}}", align="C")

    def section(self, num, title, page_break=True):
        # Only page-break if heading would land in the last ~25mm of the page body
        page_body_bottom = self.h - self.b_margin
        if page_break and self.get_y() > (page_body_bottom - 25):
            self.add_page()
        self.set_font("Helvetica", "B", 12)
        self.set_text_color(*self.CARDINAL)
        self.cell(0, 7, _a(f"{num}.  {title}" if num else title), new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(*self.CARDINAL)
        self.set_line_width(0.4)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(3)

    def body(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*self.DARK)
        self.multi_cell(0, 5.2, _a(text), align="L")
        self.ln(2)

    def bullet(self, text, bold_prefix="", dash=True):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*self.DARK)
        if dash:
            self.cell(6, 5.2, _a("-"))
        if bold_prefix:
            self.set_font("Helvetica", "B", 10)
            self.cell(self.get_string_width(_a(bold_prefix)) + 1, 5.2, _a(bold_prefix))
            self.set_font("Helvetica", "", 10)
        self.multi_cell(0, 5.2, _a(text), align="L")
        self.ln(0.5)

    def bullet_aligned(self, label, text, dash=True):
        """Bullet with bold label + colon, body text indented/aligned below the label."""
        indent = 6
        label_w = 42  # fixed label column width for alignment
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*self.DARK)
        y_start = self.get_y()
        if dash:
            self.cell(indent, 5.2, _a("-"))
            # Bold label
            self.set_font("Helvetica", "B", 10)
            self.cell(label_w, 5.2, _a(label))
            # Body text flows from the same line
            body_w = self.w - self.l_margin - self.r_margin - indent - label_w
            self.set_font("Helvetica", "", 10)
            self.multi_cell(body_w, 5.2, _a(text), align="L")
        else:
            # No dash: bold label on its own line, body indented below
            self.set_font("Helvetica", "B", 10)
            self.cell(0, 5.5, _a(label), new_x="LMARGIN", new_y="NEXT")
            self.set_font("Helvetica", "", 10)
            body_indent = 8
            self.set_x(self.l_margin + body_indent)
            body_w = self.w - self.l_margin - self.r_margin - body_indent
            self.multi_cell(body_w, 5.2, _a(text), align="L")
        self.ln(0.8)

    def quote_box(self, text):
        self.set_fill_color(255, 245, 245)
        self.set_draw_color(*self.CARDINAL)
        self.set_line_width(0.5)
        x = self.l_margin + 3
        y = self.get_y()
        self.set_xy(x + 2, y + 2)
        self.set_font("Helvetica", "I", 10)
        self.set_text_color(*self.CARDINAL)
        self.multi_cell(self.w - self.l_margin - self.r_margin - 10, 5.2, _a(text), align="L")
        h = self.get_y() - y + 2
        self.rect(x, y, self.w - self.l_margin - self.r_margin - 6, h, style="D")
        self.ln(4)


def build():
    pdf = PitchPDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.add_page()

    # ── Cover banner ──
    pdf.set_fill_color(*PitchPDF.CARDINAL)
    pdf.rect(0, 0, 210, 52, style="F")
    pdf.set_font("Helvetica", "B", 22)
    pdf.set_text_color(*PitchPDF.WHITE)
    pdf.set_y(10)
    pdf.cell(0, 10, "Project Management Engagement Proposal", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 12)
    pdf.cell(0, 7, "ICU Respiratory Digital Twin System", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "I", 10)
    pdf.cell(0, 6, _a("sEMG Neural Drive + EIT Ventilation/Perfusion Monitoring Platform"), align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(1)
    pdf.set_draw_color(*PitchPDF.WHITE)
    pdf.set_line_width(0.3)
    pdf.line(40, pdf.get_y(), 170, pdf.get_y())
    pdf.ln(2)
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(0, 5, _a("Prepared by:  Lon Dailey  |  Stanford Certificate in Project Management (SCPM)"),
             align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 9)
    pdf.cell(0, 5, _a("Prepared for:  Stakeholders -- ICU Digital Twin Program"), align="C", new_x="LMARGIN", new_y="NEXT")

    pdf.ln(8)
    pdf.set_text_color(*PitchPDF.DARK)

    # ── 1. EXECUTIVE SUMMARY (with preface) ──
    pdf.section("1", "Executive Summary", page_break=False)
    pdf.body(
        "Based on your PowerPoint presentation, it is clear that this initiative will require dedicated "
        "project management to guide execution from concept through completion. I have begun modeling the "
        "program using the information provided, recognizing that some assumptions may need refinement as "
        "we align on current data. My goal is to synchronize these inputs with the Control Tower platform "
        "I developed, along with its supporting documentation, to establish a unified and actionable "
        "project framework.\n\n"
        "I am proposing to serve as the Project Management Professional (PMP) for the ICU Respiratory "
        "Digital Twin System -- a dual-track, 23-month FDA 510(k) program encompassing sEMG neural drive "
        "monitoring (Module A) and EIT-based ventilation and perfusion imaging (Module B).\n\n"
        "My Stanford Certificate in Project Management (SCPM) provides a disciplined, research-driven "
        "approach well suited to complex, regulated medical device programs. This includes structured "
        "scheduling, proactive risk management, and tight coordination across engineering, regulatory, "
        "and business functions to ensure timely and compliant execution."
    )

    pdf.quote_box(
        "\"The Stanford SCPM curriculum is specifically designed for technology-intensive projects "
        "where scope uncertainty, regulatory constraints, and multi-disciplinary teams converge -- "
        "precisely the environment of our Digital Twin program.\""
    )

    # ── 2. WHY THE PROJECT NEEDS A DEDICATED PMP ──
    pdf.section("2", "Why This Project Needs a Dedicated PMP")
    pdf.body("The Digital Twin program is not a routine product development. It presents five compounding complexities:")
    pdf.bullet("17 interdependent milestones across Technical and Regulatory tracks with a 22-month critical path and only 5 activities with float.", "Dual-Track Parallelism:  ", dash=False)
    pdf.bullet("Two separate 510(k) submissions (sEMG under product code IKN, EIT under DQS), each requiring rigorous DHF, V&V, risk management, and FDA Pre-Submission engagement.", "Sequential FDA Submissions:  ", dash=False)
    pdf.bullet("Arch Medical Management, LLC (PMP engagement entity, Oregon) + Silan Technology Chengdu (R&D/manufacturing) -- cross-border coordination, ISO 13485 audit, and CFIUS-aware structure.", "Dual-Entity, Cross-Border:  ", dash=False)
    pdf.bullet("12 IEC/ISO standards, 21 CFR 820 QSR compliance, biocompatibility testing, EMC testing -- each with interdependencies that affect the critical path.", "Regulatory Burden:  ", dash=False)
    pdf.bullet("This could mean for example, $320K cash on hand, $45K monthly burn, 7-month runway -- every schedule slip directly erodes financial viability.", "Constrained Budget:  ", dash=False)

    pdf.body(
        "Without a dedicated PMP applying CPM analysis, earned value tracking, and proactive risk management, "
        "the probability of schedule overrun and budget exhaustion rises sharply."
    )

    # ── 3. MY STANFORD SCPM QUALIFICATIONS ──
    pdf.section("3", "Stanford SCPM -- What It Brings to This Project")
    pdf.body(
        "The Stanford Certificate in Project Management is a graduate-level professional credential "
        "covering the full lifecycle of complex technology projects. Here is how each core competency "
        "maps directly to our Digital Twin program:"
    )

    items = [
        ("Critical Path Method (CPM) & Schedule Management",
         "I have already built the project network diagram with forward/backward pass analysis. "
         "12 of 17 activities sit on the critical path (TF=0). I identified that R9 (ISO 13485 Audit) "
         "has 6 months of float, R3/R4 (sEMG 510(k) submit/clearance) have 2 months each, and T2/R1 have 1 month. "
         "This analysis guides where we can absorb delay vs. where we cannot."),
        ("Risk Management & Quantification",
         "Stanford's framework goes beyond qualitative risk registers. I apply Expected Monetary Value (EMV) analysis, "
         "Monte Carlo schedule simulation, and risk-adjusted milestone confidence levels -- critical for FDA timelines "
         "where a single AI (Additional Information) request can add 90 days."),
        ("Earned Value Management (EVM)",
         "With a $320K budget and 7-month runway, we cannot afford to learn about cost overruns after the fact. "
         "I will implement CPI/SPI tracking from M+0 so we have early warning of any budget or schedule variance."),
        ("Stakeholder & Communication Management",
         "The program spans Dr. Dai (technical authority), Lawrence Liu, Lon Dailey -- plus external "
         "stakeholders (FDA, notified bodies, investors). Stanford's stakeholder engagement model ensures "
         "each party gets the right information at the right cadence."),
        ("Design Control & Regulatory Integration",
         "Stanford's curriculum covers the integration of project management with design control processes (ISO 13485, "
         "21 CFR 820). I understand how DHF documentation, design reviews, and V&V gates must be embedded in the project "
         "schedule as hard dependencies -- not afterthoughts."),
        ("Change Control & Configuration Management",
         "Our dashboard already implements a formal Change Request workflow with approval chains and audit trails. "
         "I will ensure every scope change is evaluated for schedule/cost/risk impact before approval."),
        ("Communication -- The PM's Most Important Skill",
         "Communication is widely recognized as the project manager's single most important competency. "
         "I bring a unique advantage here: my educational degree is in Technical Communication "
         "(as reflected on my resume). This means I am formally trained in translating complex technical "
         "concepts into clear, actionable information for diverse audiences -- whether that audience is "
         "the FDA, a Chinese manufacturing partner, a board of investors, or your own engineering team. "
         "Every status report, risk briefing, and stakeholder update benefits from this foundation."),
    ]
    for i, (title, desc) in enumerate(items):
        # Force page break before "Critical Path Method" heading
        if i == 0:
            pdf.add_page()
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(*PitchPDF.ACCENT)
        pdf.cell(0, 5.5, _a(title), new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "", 9.5)
        pdf.set_text_color(*PitchPDF.DARK)
        pdf.multi_cell(0, 5, _a(desc), align="L")
        pdf.ln(2)

    # ── 4. WHAT I HAVE ALREADY DELIVERED ──
    pdf.section("4", "What I Have Already Delivered (Proof of Capability)")
    pdf.body("Before asking for the engagement, I built the tools and analysis to demonstrate competence:")
    pdf.bullet_aligned("PM Dashboard:", "Fully interactive TypeScript + Vite + Tailwind CSS dashboard with 11 tabs: Overview, Milestones, Gates, Risks, Standards, Cash/Runway, Budget, Resources, Suppliers, CAPA, Executive Summary.", dash=False)
    pdf.bullet_aligned("CPM Network Analysis:", "Forward/backward pass on all 17 activities. 12 critical-path activities identified. 5 float activities quantified (R9: 6mo, R3: 2mo, R4: 2mo, T2: 1mo, R1: 1mo).", dash=False)
    pdf.bullet_aligned("Change Request System:", "Change Request submission with IndexedDB storage, approval workflow, and full audit trail.", dash=False)
    pdf.bullet_aligned("Role-Based Access Control:", "Role-based access (PMP/Tech/Business/Accounting) with appropriate visibility controls.", dash=False)
    pdf.bullet_aligned("Cash & Runway Tracking:", "PMP-editable cash-on-hand and monthly burn fields with automatic runway recalculation.", dash=False)
    pdf.bullet_aligned("Regulatory Compliance Tools:", "Design History File index, CAPA log, action items, supplier management, notification system.", dash=False)
    pdf.bullet_aligned("Documentation:", "EN + CN User Guides (25 sections each), Project Charters (EN/CN), Inventor Q&A Sheet.", dash=False)
    pdf.bullet_aligned("Risk Register:", "Eight defined risks with probability/impact scoring, mitigation strategies, and trigger conditions.", dash=False)

    # ── 5. PROPOSED ENGAGEMENT ──
    pdf.section("5", "Proposed Engagement Structure")
    pdf.body("I propose the following PMP engagement for the Digital Twin program:")

    # Table
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_fill_color(255, 245, 245)
    pdf.set_text_color(*PitchPDF.CARDINAL)
    col_w = [48, 132]
    headers = ["Element", "Detail"]
    for i, h in enumerate(headers):
        pdf.cell(col_w[i], 7, _a(h), border=1, fill=True, align="C")
    pdf.ln()

    rows = [
        ("Role", "Project Management Professional (PMP) -- full schedule, cost, risk, and quality authority"),
        ("Scope", "Dual-track program: sEMG (M+0 to M+9 clearance) + EIT (M+8 to M+23 clearance)"),
        ("Reporting", "Monthly EVM dashboard, weekly status to stakeholders, quarterly investor summary"),
        ("Authority", "Schedule baseline changes, CR approval/rejection, resource allocation adjustments"),
        ("Deliverables", "CPM updates, EVM reports, risk register reviews, gate readiness assessments, DHF oversight"),
        ("Tools", "PM Dashboard (live), Network Diagram, Risk Monte Carlo, Budget Tracker"),
        ("Relationship", "Technical lead retains full technical authority; PMP manages schedule, cost, and process"),
        ("Entity", "Arch Medical Management, LLC"),
    ]
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(*PitchPDF.DARK)
    for lbl, val in rows:
        pdf.set_font("Helvetica", "B", 9)
        pdf.cell(col_w[0], 6.5, _a(lbl), border=1)
        pdf.set_font("Helvetica", "", 9)
        pdf.cell(col_w[1], 6.5, _a(val), border=1)
        pdf.ln()

    pdf.ln(4)

    # ── 6. VALUE PROPOSITION ──
    pdf.section("6", "The Value Proposition -- Why Me, Why Now")
    pdf.body(
        "Your expertise is in the science -- bioimpedance tomography, sEMG signal processing, "
        "and the clinical algorithms that make this device transformative. My role is to ensure that expertise "
        "reaches patients on time and on budget.\n\n"
        "Here is the specific value I bring:"
    )
    pdf.bullet_aligned("Protect your technical focus:", "Every hour you spend managing timelines, chasing approvals, or reconciling budgets is an hour not spent on the science. I take that burden.", dash=False)
    pdf.bullet_aligned("De-risk the timeline:", "With only 7 months of runway, a 2-month schedule slip could be fatal. CPM-driven management with daily critical-path monitoring prevents this.", dash=False)
    pdf.bullet_aligned("Investor confidence:", "Investors and strategic partners expect professional project governance. A Stanford-credentialed PMP with a live dashboard and formal EVM reporting signals maturity.", dash=False)
    pdf.bullet_aligned("FDA readiness:", "FDA engagement (Pre-Sub, 510(k) submissions) benefits enormously from structured project management. I ensure submissions are complete, on time, and well-organized.", dash=False)
    pdf.bullet_aligned("Proven delivery:", "I have already built the dashboard, the network analysis, the risk register, the documentation. I am not proposing to start -- I am proposing to continue and formalize.", dash=False)

    pdf.ln(4)

    # ── 7. NEXT STEPS ──
    pdf.section("7", "Proposed Next Steps")
    pdf.body("If you agree to this engagement, I recommend the following immediate actions:")
    pdf.bullet("Formal agreement on PMP role, authority boundaries, and reporting cadence.", "Week 1:  ", dash=False)
    pdf.bullet("Schedule baseline review -- walk through the CPM network diagram together and confirm all durations and dependencies.", "Week 1:  ", dash=False)
    pdf.bullet("EVM baseline -- establish the Performance Measurement Baseline (PMB) using current budget allocations.", "Week 2:  ", dash=False)
    pdf.bullet("Risk review -- live walkthrough of all 8 risks, update probabilities, and agree on mitigation owners.", "Week 2:  ", dash=False)
    pdf.bullet("First monthly status report to all stakeholders.", "Week 4:  ", dash=False)

    pdf.ln(6)

    # ── Closing ──
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(*PitchPDF.DARK)
    pdf.multi_cell(0, 5.5, _a(
        "I am confident that a dedicated PMP function will materially improve our probability of "
        "on-time FDA clearance for both modules and responsible stewardship of our limited capital. "
        "I look forward to discussing this proposal with you."
    ), align="L")
    pdf.ln(8)
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 6, "Lon Dailey", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 5, "Stanford Certificate in Project Management (SCPM)", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 5, "Arch Medical Management, LLC", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "I", 9)
    pdf.set_text_color(*PitchPDF.GRAY)
    pdf.cell(0, 5, "March 21, 2026", new_x="LMARGIN", new_y="NEXT")

    path = os.path.join(OUT, "PMP_Engagement_Pitch.pdf")
    pdf.output(path)
    return path


if __name__ == "__main__":
    p = build()
    print(f"PDF: {p}")
    print("Done.")
