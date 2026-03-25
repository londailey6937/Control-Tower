#!/usr/bin/env python3
"""
Generate a comprehensive FDA 510(k) Submission Process Guide PDF
for Class II (non-invasive, non-radiative) medical devices.
Phase-by-phase project plan aligned to Control Tower workflow.
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


class GuidePDF(FPDF):
    CARDINAL = (140, 21, 21)
    DARK = (35, 35, 40)
    GRAY = (110, 110, 120)
    ACCENT = (0, 98, 71)
    WHITE = (255, 255, 255)
    LIGHT_BG = (248, 248, 252)
    WARN_BG = (255, 248, 240)
    WARN_BORDER = (200, 120, 20)

    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(*self.GRAY)
        self.cell(0, 4, _a("FDA 510(k) Submission Process Guide  |  ICU Respiratory Digital Twin System  |  Control Tower Reference"), align="R")
        self.ln(5)

    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(*self.GRAY)
        self.cell(0, 4, f"Page {self.page_no()}/{{nb}}", align="C")

    def phase_heading(self, num, title, subtitle=""):
        """Major phase heading -- always starts a new page."""
        self.add_page()
        # Phase banner
        self.set_fill_color(*self.CARDINAL)
        self.rect(self.l_margin, self.get_y(), self.w - self.l_margin - self.r_margin, 14, style="F")
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(*self.WHITE)
        self.set_x(self.l_margin + 4)
        self.cell(0, 14, _a(f"Phase {num}:  {title}"))
        self.ln(16)
        if subtitle:
            self.set_font("Helvetica", "I", 9)
            self.set_text_color(*self.GRAY)
            self.cell(0, 5, _a(subtitle), new_x="LMARGIN", new_y="NEXT")
            self.ln(2)

    def sub_heading(self, text):
        """Green sub-heading within a phase."""
        page_body_bottom = self.h - self.b_margin
        if self.get_y() > (page_body_bottom - 30):
            self.add_page()
        self.ln(2)
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(*self.ACCENT)
        self.cell(0, 6, _a(text), new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(*self.ACCENT)
        self.set_line_width(0.3)
        self.line(self.l_margin, self.get_y(), self.l_margin + 60, self.get_y())
        self.ln(2)

    def body(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*self.DARK)
        self.multi_cell(0, 5.2, _a(text), align="L")
        self.ln(2)

    def bullet(self, text, bold_prefix=""):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*self.DARK)
        self.cell(6, 5.2, _a("-"))
        if bold_prefix:
            self.set_font("Helvetica", "B", 10)
            self.cell(self.get_string_width(_a(bold_prefix)) + 1, 5.2, _a(bold_prefix))
            self.set_font("Helvetica", "", 10)
        self.multi_cell(0, 5.2, _a(text), align="L")
        self.ln(0.5)

    def labeled_item(self, label, text):
        """Bold label on its own line, body indented below."""
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(*self.DARK)
        self.cell(0, 5.5, _a(label), new_x="LMARGIN", new_y="NEXT")
        self.set_font("Helvetica", "", 10)
        self.set_x(self.l_margin + 8)
        body_w = self.w - self.l_margin - self.r_margin - 8
        self.multi_cell(body_w, 5.2, _a(text), align="L")
        self.ln(1)

    def callout_box(self, text, style="key"):
        """Highlighted callout box. style='key' (green) or 'warn' (amber)."""
        if style == "warn":
            self.set_fill_color(*self.WARN_BG)
            self.set_draw_color(*self.WARN_BORDER)
            self.set_text_color(160, 90, 0)
            prefix = "CHALLENGE:  "
        else:
            self.set_fill_color(240, 250, 245)
            self.set_draw_color(*self.ACCENT)
            self.set_text_color(*self.ACCENT)
            prefix = "KEY INSIGHT:  "
        self.set_line_width(0.5)
        # Prevent page-break mid-callout: ensure at least 35mm of space
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

    def challenge_box(self, text):
        self.callout_box(text, style="warn")

    def table_row(self, cells, widths, bold_first=False, header=False):
        """Render a table row."""
        h = 6.5
        if header:
            self.set_font("Helvetica", "B", 9)
            self.set_fill_color(*self.CARDINAL)
            self.set_text_color(*self.WHITE)
            for i, cell in enumerate(cells):
                self.cell(widths[i], h, _a(cell), border=1, fill=True, align="C")
            self.ln()
            return
        self.set_text_color(*self.DARK)
        for i, cell in enumerate(cells):
            if i == 0 and bold_first:
                self.set_font("Helvetica", "B", 9)
            else:
                self.set_font("Helvetica", "", 9)
            self.cell(widths[i], h, _a(cell), border=1)
        self.ln()


def build():
    pdf = GuidePDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.add_page()

    # ════════════════════════════════════════════════════
    # COVER PAGE
    # ════════════════════════════════════════════════════
    pdf.set_fill_color(*GuidePDF.CARDINAL)
    pdf.rect(0, 0, 210, 60, style="F")
    pdf.set_font("Helvetica", "B", 24)
    pdf.set_text_color(*GuidePDF.WHITE)
    pdf.set_y(12)
    pdf.cell(0, 10, "FDA 510(k) Submission", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 10, "Process Guide", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 7, _a("Class II Non-Invasive Medical Device -- End-to-End Workflow"), align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "I", 9)
    pdf.ln(1)
    pdf.set_draw_color(*GuidePDF.WHITE)
    pdf.set_line_width(0.3)
    pdf.line(45, pdf.get_y(), 165, pdf.get_y())
    pdf.ln(2)
    pdf.cell(0, 5, _a("ICU Respiratory Digital Twin System  |  Control Tower Reference Document"), align="C", new_x="LMARGIN", new_y="NEXT")

    pdf.ln(12)
    pdf.set_text_color(*GuidePDF.DARK)

    # Table of Contents
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(*GuidePDF.CARDINAL)
    pdf.cell(0, 8, "Table of Contents", new_x="LMARGIN", new_y="NEXT")
    pdf.set_draw_color(*GuidePDF.CARDINAL)
    pdf.set_line_width(0.4)
    pdf.line(pdf.l_margin, pdf.get_y(), pdf.w - pdf.r_margin, pdf.get_y())
    pdf.ln(4)

    toc = [
        ("Phase 1", "Confirm Regulatory Pathway", "Pathway selection, product codes, predicate identification"),
        ("Phase 2", "Pre-Submission (Q-Sub)", "FDA engagement strategy, meeting preparation, risk reduction"),
        ("Phase 3", "Design Controls", "21 CFR 820, ISO 13485, DHF construction, design reviews"),
        ("Phase 4", "Testing & Validation", "Bench testing, electrical safety, software, biocompatibility, usability"),
        ("Phase 5", "Build the 510(k) Submission", "Administrative, device description, SE comparison, labeling"),
        ("Phase 6", "Submit to FDA", "eSTAR format, RTA preparation, submission logistics"),
        ("Phase 7", "FDA Review Process", "RTA, substantive review, AI requests, timeline management"),
        ("Phase 8", "Clearance Decision", "Clearance letter, 510(k) number, next-step triggers"),
        ("Phase 9", "Post-Clearance Requirements", "Registration, QSR compliance, post-market surveillance"),
    ]
    for phase, title, desc in toc:
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(*GuidePDF.ACCENT)
        pdf.cell(20, 5.5, _a(phase))
        pdf.set_text_color(*GuidePDF.DARK)
        pdf.cell(60, 5.5, _a(title))
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(*GuidePDF.GRAY)
        pdf.cell(0, 5.5, _a(desc), new_x="LMARGIN", new_y="NEXT")
        pdf.ln(1)

    pdf.ln(4)

    # Timeline overview box
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(*GuidePDF.CARDINAL)
    pdf.cell(0, 6, "Realistic Timeline Overview", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(1)
    w = [60, 60, 60]
    pdf.table_row(["Activity", "Duration", "Cumulative"], w, header=True)
    pdf.table_row(["Pathway + Pre-Sub", "1-3 months", "Months 0-3"], w, bold_first=True)
    pdf.table_row(["Design Controls + Testing", "4-9 months", "Months 2-10"], w, bold_first=True)
    pdf.table_row(["Build Submission", "1-2 months", "Months 8-12"], w, bold_first=True)
    pdf.table_row(["FDA Review", "3-6 months", "Months 10-15"], w, bold_first=True)
    pdf.table_row(["Post-Clearance Setup", "1-2 months", "Months 13-17"], w, bold_first=True)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(*GuidePDF.CARDINAL)
    pdf.ln(2)
    pdf.cell(0, 6, _a("Typical Total:  7-15 months  |  Digital Twin Program Target:  22 months (dual-module)"), new_x="LMARGIN", new_y="NEXT")

    # ════════════════════════════════════════════════════
    # PHASE 1: CONFIRM REGULATORY PATHWAY
    # ════════════════════════════════════════════════════
    pdf.phase_heading("1", "Confirm Regulatory Pathway",
                      "Duration: 2-4 weeks  |  Control Tower Gate: G0 (Pathway Confirmed)")

    pdf.body(
        "Before any design, testing, or documentation begins, the regulatory pathway must be locked. "
        "For Class II non-invasive, non-radiative devices, the standard pathway is FDA 510(k) clearance. "
        "This phase establishes the regulatory foundation upon which every subsequent activity depends."
    )

    pdf.sub_heading("Step 1.1: Classify the Device")
    pdf.body("Use the FDA Product Classification Database (https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfPCD/classification.cfm) to confirm:")
    pdf.bullet("The device class (should confirm Class II)")
    pdf.bullet("Product code (e.g., IKN for sEMG, DQS for EIT)")
    pdf.bullet("Regulation number (e.g., 21 CFR 882.1400, 21 CFR 870.2710)")
    pdf.bullet("Whether the device is exempt from 510(k) or requires premarket notification")

    pdf.callout_box(
        "For the Digital Twin program, we have TWO separate product codes (IKN and DQS), "
        "meaning two independent 510(k) submissions. This doubles the regulatory workload "
        "and introduces sequential dependencies on the critical path."
    )

    pdf.sub_heading("Step 1.2: Identify Predicate Device(s)")
    pdf.body(
        "The predicate device is the legally marketed device to which you claim substantial equivalence. "
        "This is the single most important decision in the entire 510(k) process."
    )
    pdf.labeled_item("How to Find Predicates:",
        "Search the FDA 510(k) Premarket Notification Database. Filter by product code. "
        "Review cleared devices with similar intended use, technology, and indications.")
    pdf.labeled_item("Selection Criteria:",
        "Identical intended use (strongly preferred). Same or similar technology. "
        "Same target population. Similar performance characteristics.")
    pdf.labeled_item("Documentation Required:",
        "Full predicate analysis document. Side-by-side comparison table. "
        "Justification for any differences in technology or intended use.")

    pdf.challenge_box(
        "A poorly chosen predicate is the #1 reason for 510(k) rejection. If the predicate's "
        "intended use differs even slightly, FDA may require a de novo classification instead -- "
        "adding 6-12 months and significantly more data requirements."
    )

    pdf.sub_heading("Step 1.3: Confirm Pathway Decision")
    pdf.body("Document the pathway decision formally:")
    pdf.bullet("510(k) Traditional vs. 510(k) Special vs. De Novo -- justify the choice")
    pdf.bullet("If Special 510(k): can only be used for modifications to your own cleared device")
    pdf.bullet("If De Novo: required when no predicate exists; longer timeline (6-12 months review)")

    pdf.sub_heading("Challenges & Risk Factors")
    pdf.labeled_item("Novel Technology Risk:",
        "If your device uses technology significantly different from any cleared predicate, "
        "FDA may determine 510(k) is not appropriate. EIT-based lung imaging falls into a "
        "relatively novel category -- predicate selection here is critical.")
    pdf.labeled_item("Dual-Module Complexity:",
        "sEMG and EIT modules have different product codes, different predicates, and potentially "
        "different review divisions within FDA. Coordination between the two submissions requires "
        "careful planning.")
    pdf.labeled_item("Intended Use Creep:",
        "Marketing or clinical teams may want to expand the intended use statement after pathway "
        "selection. Any change here can invalidate the predicate choice and force a restart.")

    pdf.sub_heading("Control Tower Deliverables")
    pdf.bullet("Regulatory Pathway Decision Document (signed off)")
    pdf.bullet("Predicate Device Analysis Report (per module)")
    pdf.bullet("Product code and regulation number confirmed in data.ts")
    pdf.bullet("Gate G0 review completed and documented")

    # ════════════════════════════════════════════════════
    # PHASE 2: PRE-SUBMISSION (Q-SUB)
    # ════════════════════════════════════════════════════
    pdf.phase_heading("2", "Pre-Submission (Q-Sub) Meeting",
                      "Duration: 6-12 weeks  |  Control Tower Gate: G1 (FDA Feedback Received)")

    pdf.body(
        "The Pre-Submission (formerly Pre-IDE, now Q-Sub) is a formal meeting with FDA where you present "
        "your regulatory strategy, testing plan, and intended use for feedback BEFORE spending months on "
        "testing and documentation. This is strongly recommended for any non-trivial Class II device."
    )

    pdf.callout_box(
        "Skipping the Pre-Submission is one of the biggest causes of 510(k) delays and rejections. "
        "Companies that skip this step often discover during review that their testing strategy was "
        "inadequate, their predicate was wrong, or their intended use was too broad -- all of which "
        "require starting over."
    )

    pdf.sub_heading("Step 2.1: Prepare the Pre-Sub Package")
    pdf.body("The Pre-Sub package is a formal document submitted to FDA at least 90 days before the requested meeting date. It must include:")
    pdf.labeled_item("Device Description:",
        "Complete technical description of the device, including principles of operation, "
        "components, materials, and block diagrams.")
    pdf.labeled_item("Intended Use Statement:",
        "Draft intended use / indications for use. This will be reviewed and potentially "
        "modified based on FDA feedback.")
    pdf.labeled_item("Proposed Predicate(s):",
        "Your predicate analysis with the side-by-side comparison table. "
        "Include justification for why the devices are substantially equivalent.")
    pdf.labeled_item("Proposed Testing Strategy:",
        "Detailed list of all planned testing (bench, electrical safety, software validation, "
        "biocompatibility, usability). Include test protocols or summaries. "
        "Identify any testing you believe is NOT needed and explain why.")
    pdf.labeled_item("Specific Questions for FDA:",
        "Numbered list of questions you want FDA to address. These should be specific, "
        "not generic. Example: 'Does FDA agree that clinical data is not required given "
        "that our device uses the same transducer technology as predicate K123456?'")

    pdf.sub_heading("Step 2.2: The Pre-Sub Meeting")
    pdf.body("FDA scheduling and meeting process:")
    pdf.bullet("FDA will acknowledge receipt within 3-5 business days")
    pdf.bullet("FDA provides written feedback 1-2 weeks before the meeting")
    pdf.bullet("The meeting itself is typically 60 minutes, teleconference or in-person")
    pdf.bullet("FDA feedback is documented in official meeting minutes (you may draft these)")

    pdf.sub_heading("Step 2.3: Incorporate FDA Feedback")
    pdf.body("After the meeting, you must:")
    pdf.bullet("Update the testing strategy to reflect any FDA requests for additional testing")
    pdf.bullet("Revise the intended use if FDA suggested changes")
    pdf.bullet("Reassess the predicate if FDA raised concerns about substantial equivalence")
    pdf.bullet("Document all feedback in the DHF as a formal design input")

    pdf.sub_heading("Challenges & Risk Factors")
    pdf.challenge_box(
        "FDA scheduling can take 75-90 days from submission of the Pre-Sub package. "
        "If your questions are unclear or your package is incomplete, FDA may refuse to "
        "schedule the meeting -- adding another 2-3 months to the timeline."
    )

    pdf.labeled_item("FDA Disagreement on Predicate:",
        "If FDA rejects your proposed predicate, your entire regulatory strategy may need "
        "to change. This is why the Pre-Sub is so valuable -- better to learn this early "
        "than after you've spent 6 months testing against the wrong benchmark.")
    pdf.labeled_item("Additional Testing Requirements:",
        "FDA may request testing you didn't plan for (e.g., clinical data, specific "
        "biocompatibility tests, additional software documentation). Budget and schedule "
        "must have contingency for this.")
    pdf.labeled_item("Dual-Module Coordination:",
        "For the Digital Twin program, we may need TWO separate Pre-Sub meetings (one per "
        "module) or a single combined meeting covering both. Strategy must be decided early.")

    pdf.sub_heading("Control Tower Deliverables")
    pdf.bullet("Pre-Sub Package (submitted to FDA)")
    pdf.bullet("FDA Meeting Minutes (official record)")
    pdf.bullet("Updated Testing Strategy (post-feedback)")
    pdf.bullet("Revised Intended Use Statement (if applicable)")
    pdf.bullet("Gate G1 review: all FDA feedback incorporated into project plan")
    pdf.bullet("FDA Comms tab: auto-generated Q-Sub cover letter and question package export (PMP-only)")
    pdf.bullet("FDA Comms tab: RTA self-check status updated from DHF/Standards trackers")

    # ════════════════════════════════════════════════════
    # PHASE 3: DESIGN CONTROLS
    # ════════════════════════════════════════════════════
    pdf.phase_heading("3", "Design Controls",
                      "Duration: Continuous (parallel with Phases 2-5)  |  21 CFR 820 / ISO 13485")

    pdf.body(
        "Design Controls are not a phase you 'complete' -- they are a continuous, documented process "
        "that runs from concept through production. FDA does not just review your device; they review "
        "your design process. Failure to maintain proper design controls is one of the most common "
        "FDA warning letter topics."
    )

    pdf.callout_box(
        "FDA's expectation: every design decision must be traceable from user need to design input "
        "to design output to verification to validation. If you cannot show this traceability, "
        "your 510(k) will be questioned regardless of how good the device actually is."
    )

    pdf.sub_heading("Step 3.1: Design Inputs (Requirements)")
    pdf.body("Design inputs define what the device must do. They must be:")
    pdf.bullet("Measurable and verifiable (not vague)")
    pdf.bullet("Traced to user needs, regulatory requirements, or risk analysis outputs")
    pdf.bullet("Reviewed and approved by the design team")
    pdf.bullet("Maintained under document control")

    pdf.labeled_item("Common Failure Mode:",
        "Requirements that are too vague to test. Example: 'The device shall be accurate' is "
        "not a valid design input. 'The device shall measure tidal volume with accuracy of +/-5% "
        "over the range of 200-1500 mL' IS a valid design input.")

    pdf.sub_heading("Step 3.2: Design Outputs (Specifications)")
    pdf.body("Design outputs are the physical embodiment of design inputs:")
    pdf.bullet("Engineering drawings and specifications")
    pdf.bullet("Software architecture documents and source code")
    pdf.bullet("Bill of materials (BOM)")
    pdf.bullet("Manufacturing procedures")
    pdf.bullet("Device master record (DMR)")

    pdf.sub_heading("Step 3.3: Risk Analysis (ISO 14971)")
    pdf.body(
        "Risk management is not a one-time activity. It must be maintained throughout the entire "
        "product lifecycle. The risk management file includes:"
    )
    pdf.bullet("Hazard identification (what can go wrong)")
    pdf.bullet("Risk estimation (probability x severity)")
    pdf.bullet("Risk evaluation (acceptable vs. unacceptable)")
    pdf.bullet("Risk controls (design changes, protective measures, labeling)")
    pdf.bullet("Residual risk assessment (what remains after controls)")

    pdf.challenge_box(
        "For the Digital Twin system, risk analysis is complex because sEMG and EIT modules "
        "have different hazard profiles. sEMG involves surface electrode contact; EIT involves "
        "injecting small currents. Each requires independent risk analysis with different "
        "severity categories and failure modes."
    )

    pdf.sub_heading("Step 3.4: Design Reviews")
    pdf.body("Formal design reviews are required at defined stages:")
    pdf.bullet("Concept review (design inputs complete)")
    pdf.bullet("Preliminary design review (architecture finalized)")
    pdf.bullet("Critical design review (outputs complete, ready for V&V)")
    pdf.bullet("Final design review (all V&V complete, ready for production)")

    pdf.labeled_item("Review Requirements:",
        "Each review must include independent reviewers (not just the design team). "
        "Meeting minutes, action items, and decisions must be documented and maintained "
        "in the DHF.")

    pdf.sub_heading("Step 3.5: Design History File (DHF)")
    pdf.body(
        "The DHF is the complete record of your design process. It contains or references "
        "every document listed above. FDA may request the DHF during review or during a "
        "post-market inspection."
    )
    pdf.bullet("One DHF per product (or per module if they are separate devices)")
    pdf.bullet("Must be maintained under document control with revision history")
    pdf.bullet("Must demonstrate traceability: need -> input -> output -> V&V -> review")

    pdf.sub_heading("Control Tower Deliverables")
    pdf.bullet("Design Input Document (approved and under revision control)")
    pdf.bullet("Design Output Package (specs, drawings, BOM)")
    pdf.bullet("Risk Management File (ISO 14971 compliant)")
    pdf.bullet("Design Review Meeting Records (per stage)")
    pdf.bullet("Design History File (indexed and complete)")
    pdf.bullet("Traceability Matrix (requirements to V&V results)")

    # ════════════════════════════════════════════════════
    # PHASE 4: TESTING & VALIDATION
    # ════════════════════════════════════════════════════
    pdf.phase_heading("4", "Testing & Validation",
                      "Duration: 3-6 months  |  Control Tower Gate: G3 (V&V Complete)")

    pdf.body(
        "Testing for a Class II non-invasive device must demonstrate that the device is safe and "
        "performs as intended. The specific tests depend on the device type, but for the Digital Twin "
        "program, the following categories apply."
    )

    pdf.sub_heading("4.1: Bench / Performance Testing")
    pdf.body("Core performance metrics that must be objectively verified:")
    pdf.bullet("Accuracy against known standards (e.g., calibrated lung simulators for EIT)")
    pdf.bullet("Repeatability and reproducibility (R&R studies)")
    pdf.bullet("Durability and reliability (lifecycle testing, stress testing)")
    pdf.bullet("Environmental testing (temperature, humidity, vibration -- per IEC 60068)")

    pdf.labeled_item("sEMG-Specific Testing:",
        "Signal-to-noise ratio, common-mode rejection ratio (CMRR), electrode impedance "
        "range, sampling rate accuracy, frequency response verification.")
    pdf.labeled_item("EIT-Specific Testing:",
        "Reconstruction accuracy against known phantoms, current injection safety limits, "
        "electrode contact impedance monitoring, frame rate verification, image resolution metrics.")

    pdf.sub_heading("4.2: Electrical Safety (IEC 60601-1)")
    pdf.body(
        "All medical electrical equipment must comply with IEC 60601-1 (general requirements) "
        "plus applicable particular standards:"
    )
    pdf.bullet("IEC 60601-1: General requirements for safety and essential performance")
    pdf.bullet("IEC 60601-1-2: EMC (electromagnetic compatibility) -- conducted and radiated emissions, immunity")
    pdf.bullet("IEC 60601-1-6: Usability")
    pdf.bullet("IEC 60601-1-8: Alarms systems (if applicable)")
    pdf.bullet("IEC 60601-2-49: Particular requirements for multi-function patient monitoring (if applicable)")

    pdf.challenge_box(
        "EMC testing alone can take 2-4 weeks at an accredited lab and costs $15,000-$40,000. "
        "If the device fails, redesign and retest can add 2-3 months. Pre-compliance testing "
        "in-house before formal submission is strongly recommended."
    )

    pdf.sub_heading("4.3: Software Validation")
    pdf.body("If the device includes software (both sEMG and EIT modules do), FDA requires:")
    pdf.bullet("Software level of concern classification (Minor / Moderate / Major)")
    pdf.bullet("Software requirements specification (SRS)")
    pdf.bullet("Software architecture document")
    pdf.bullet("Software testing (unit, integration, system)")
    pdf.bullet("Traceability from requirements to test cases")
    pdf.bullet("Anomaly/bug tracking and resolution records")

    pdf.labeled_item("FDA Guidance Documents:",
        "Guidance for the Content of Premarket Submissions for Software Contained in Medical Devices. "
        "For devices using AI/ML: Predetermined Change Control Plan guidance may apply "
        "if the algorithm adapts over time.")

    pdf.callout_box(
        "The Digital Twin system's software is the device. Unlike a hardware device with "
        "embedded firmware, the algorithms for sEMG analysis and EIT reconstruction ARE the "
        "core technology. Software documentation must be exceptionally thorough."
    )

    pdf.sub_heading("4.4: Biocompatibility (ISO 10993)")
    pdf.body(
        "If the device contacts the patient's skin (both sEMG electrodes and EIT electrode arrays do), "
        "biocompatibility testing is required per ISO 10993:"
    )
    pdf.bullet("Cytotoxicity (required for all skin-contact devices)")
    pdf.bullet("Sensitization (required for extended skin contact)")
    pdf.bullet("Irritation (required for extended skin contact)")
    pdf.bullet("Possibly: Material characterization if using novel materials")

    pdf.labeled_item("Duration Matters:",
        "Contact duration determines the number of tests required. Less than 24 hours (limited), "
        "24 hours to 30 days (prolonged), more than 30 days (permanent). ICU monitoring would "
        "likely be 'prolonged' contact, requiring the full battery.")

    pdf.sub_heading("4.5: Usability / Human Factors (IEC 62366)")
    pdf.body(
        "FDA requires human factors evaluation if user interaction could impact safety. "
        "For an ICU device used by clinicians, this is required:"
    )
    pdf.bullet("Use-related risk analysis (identify critical tasks)")
    pdf.bullet("Formative usability evaluations (iterative prototype testing)")
    pdf.bullet("Summative (validation) usability study (formal, protocol-driven)")
    pdf.bullet("Use error analysis and residual risk assessment")

    pdf.challenge_box(
        "Usability studies require recruiting actual intended users (ICU clinicians) for testing. "
        "Scheduling, IRB/ethics review (if required), and the study itself can take 2-4 months. "
        "This is a frequent bottleneck on the critical path."
    )

    pdf.sub_heading("4.6: Clinical Data")
    pdf.body(
        "Clinical trials are typically NOT required for Class II non-invasive devices via 510(k), "
        "UNLESS:"
    )
    pdf.bullet("The device has a novel mechanism of action not present in the predicate")
    pdf.bullet("The intended use involves a new patient population")
    pdf.bullet("FDA specifically requests clinical data during Pre-Sub or review")
    pdf.bullet("The substantial equivalence argument cannot be supported by bench data alone")

    pdf.callout_box(
        "EIT-based lung imaging is a relatively novel modality in the US market. FDA may "
        "request limited clinical performance data (e.g., comparison to CT reference standard) "
        "even if a predicate exists. This should be explicitly addressed in the Pre-Sub meeting."
    )

    pdf.sub_heading("Control Tower Deliverables")
    pdf.bullet("Test Protocols (per test category, approved before execution)")
    pdf.bullet("Test Reports (per test category, with raw data)")
    pdf.bullet("Software V&V Report (complete traceability)")
    pdf.bullet("Biocompatibility Test Reports (ISO 10993)")
    pdf.bullet("Human Factors Report (IEC 62366)")
    pdf.bullet("Gate G3 review: all V&V complete and accepted")

    # ════════════════════════════════════════════════════
    # PHASE 5: BUILD THE 510(k) SUBMISSION
    # ════════════════════════════════════════════════════
    pdf.phase_heading("5", "Build the 510(k) Submission",
                      "Duration: 4-8 weeks  |  Control Tower Gate: G4 (Submission Assembled)")

    pdf.body(
        "The 510(k) submission is a comprehensive document package that presents your device, "
        "your testing, and your argument for substantial equivalence. It must be structured "
        "according to FDA requirements and is now submitted electronically in eSTAR format."
    )

    pdf.sub_heading("5.1: Administrative Section")
    pdf.bullet("Cover letter (signed by authorized representative)")
    pdf.bullet("FDA Form 3514 (CDRH Premarket Review Submission Cover Sheet)")
    pdf.bullet("User fee payment confirmation (MDUFA -- $6,517 for small business, $26,067 standard)")
    pdf.bullet("Truthful and Accurate Statement")
    pdf.bullet("Class III certification and summary (if applicable)")
    pdf.bullet("Letters of authorization (if referencing another company's data)")

    pdf.sub_heading("5.2: Device Description")
    pdf.body("A complete, clear description of the device:")
    pdf.bullet("Principles of operation (how the device works)")
    pdf.bullet("Block diagram and system architecture")
    pdf.bullet("Hardware components and materials")
    pdf.bullet("Software description (including SOUP/OTS components)")
    pdf.bullet("Accessories and peripherals")
    pdf.bullet("Packaging description")

    pdf.challenge_box(
        "The device description must be detailed enough for FDA to understand the device "
        "without having it in front of them, but clear enough for a non-specialist reviewer "
        "to follow. Technical writing skill is critical here."
    )

    pdf.sub_heading("5.3: Indications for Use")
    pdf.body(
        "The exact intended use statement that will appear on the device labeling. "
        "This must closely match the predicate's intended use."
    )
    pdf.labeled_item("Critical Rule:",
        "If your intended use is BROADER than the predicate, FDA will likely reject the "
        "510(k) and require either a different predicate or a De Novo. If your intended use "
        "is NARROWER, that is generally acceptable.")

    pdf.sub_heading("5.4: Substantial Equivalence Comparison")
    pdf.body(
        "This is the core argument of your 510(k). You must demonstrate, point by point, "
        "that your device is substantially equivalent to the predicate:"
    )
    w_se = [45, 55, 55, 25]
    pdf.table_row(["Feature", "Your Device", "Predicate", "Same?"], w_se, header=True)
    pdf.table_row(["Intended use", "(your statement)", "(predicate statement)", "Same"], w_se, bold_first=True)
    pdf.table_row(["Technology", "(your technology)", "(predicate technology)", "Similar"], w_se, bold_first=True)
    pdf.table_row(["Energy type", "(e.g., electrical)", "(predicate energy)", "Same"], w_se, bold_first=True)
    pdf.table_row(["Patient contact", "(e.g., skin surface)", "(predicate contact)", "Same"], w_se, bold_first=True)
    pdf.table_row(["Target population", "(e.g., adult ICU)", "(predicate population)", "Same"], w_se, bold_first=True)
    pdf.table_row(["Output / display", "(your output)", "(predicate output)", "Similar"], w_se, bold_first=True)
    pdf.ln(2)

    pdf.body(
        "For any feature marked 'Similar' rather than 'Same', you must provide scientific "
        "evidence (bench testing, performance data) demonstrating that the difference does not "
        "raise new questions of safety and effectiveness."
    )

    pdf.sub_heading("5.5: Performance Testing Data")
    pdf.body("All test reports from Phase 4, organized by category:")
    pdf.bullet("Bench / performance testing results")
    pdf.bullet("Software validation results")
    pdf.bullet("Electrical safety (IEC 60601) test reports")
    pdf.bullet("Biocompatibility test reports (ISO 10993)")
    pdf.bullet("EMC test reports (IEC 60601-1-2)")
    pdf.bullet("Clinical data (if applicable)")

    pdf.sub_heading("5.6: Risk Analysis Summary")
    pdf.bullet("Complete risk management report (ISO 14971)")
    pdf.bullet("Hazard analysis with mitigations")
    pdf.bullet("Residual risk evaluation")
    pdf.bullet("Risk-benefit analysis (if residual risks exist)")

    pdf.sub_heading("5.7: Labeling")
    pdf.body("All proposed device labeling materials:")
    pdf.bullet("Instructions for Use (IFU) -- complete user manual")
    pdf.bullet("Package labeling (outer box, inner packaging)")
    pdf.bullet("Device labels (affixed to the device itself)")
    pdf.bullet("Warnings and cautions")
    pdf.bullet("Electromagnetic compatibility declaration tables")

    pdf.sub_heading("5.8: 510(k) Summary")
    pdf.body(
        "A public-facing summary document that becomes part of the FDA's public database "
        "after clearance. It summarizes the device, testing, and equivalence argument. "
        "This is typically 3-5 pages."
    )

    pdf.sub_heading("Control Tower Deliverables")
    pdf.bullet("Complete 510(k) submission package (eSTAR format)")
    pdf.bullet("Internal review checklist (all sections verified complete)")
    pdf.bullet("Submission readiness review (Gate G4)")
    pdf.bullet("FDA Comms tab: DHF Readiness Snapshot confirms all sections complete")

    # ════════════════════════════════════════════════════
    # PHASE 6: SUBMIT TO FDA
    # ════════════════════════════════════════════════════
    pdf.phase_heading("6", "Submit to FDA",
                      "Duration: 1-2 weeks  |  Control Tower Milestone: M-SUBMIT")

    pdf.body(
        "Submission is now electronic. FDA's eSTAR (electronic Submission Template And Resource) "
        "is the required format for 510(k) submissions as of October 2023."
    )

    pdf.sub_heading("Step 6.1: eSTAR Preparation")
    pdf.body("The eSTAR template guides you through the submission and validates completeness:")
    pdf.bullet("Download the current eSTAR template from FDA's website")
    pdf.bullet("Complete each section (administrative, device description, testing, labeling)")
    pdf.bullet("Attach all supporting documents as PDFs")
    pdf.bullet("Run the built-in validation check to catch missing elements")

    pdf.sub_heading("Step 6.2: Pre-Submission Quality Check")
    pdf.body("Before submitting, perform an internal Refuse to Accept (RTA) self-check:")
    pdf.bullet("Use FDA's RTA checklist (publicly available) to verify completeness")
    pdf.bullet("Confirm user fee has been paid and confirmation number is included")
    pdf.bullet("Verify all forms are signed and dated")
    pdf.bullet("Check that all cross-references between sections are correct")
    pdf.bullet("Ensure the 510(k) summary and indications for use statement are included")

    pdf.callout_box(
        "FDA's RTA (Refuse to Accept) policy means incomplete submissions are rejected "
        "within 15 days -- no review, no feedback, just rejection. The most common RTA "
        "reasons: missing performance data, missing biocompatibility data, and incomplete "
        "software documentation."
    )

    pdf.sub_heading("Step 6.3: Submit")
    pdf.bullet("Submit via FDA's eStar portal")
    pdf.bullet("Receive acknowledgment letter with 510(k) number (e.g., K2XXXXX)")
    pdf.bullet("Clock starts for FDA review")

    pdf.sub_heading("Challenges & Risk Factors")
    pdf.challenge_box(
        "If RTA'd, you must fix all deficiencies and resubmit. The FDA review clock resets "
        "completely. Average RTA rate is approximately 25-30% of all 510(k) submissions. "
        "Thorough pre-submission review using the RTA checklist is essential."
    )

    pdf.sub_heading("Control Tower Deliverables")
    pdf.bullet("eSTAR submission package (finalized)")
    pdf.bullet("RTA self-check completed and documented")
    pdf.bullet("FDA acknowledgment letter received")
    pdf.bullet("Control Tower milestone M-SUBMIT marked complete")
    pdf.bullet("FDA Comms tab: RTA self-check checklist verified (14-item cross-reference)")
    pdf.bullet("FDA Comms tab: FDA Interaction Timeline updated with submission date")

    # ════════════════════════════════════════════════════
    # PHASE 7: FDA REVIEW PROCESS
    # ════════════════════════════════════════════════════
    pdf.phase_heading("7", "FDA Review Process",
                      "Duration: 3-6 months  |  Control Tower Gate: G5 (Review Complete)")

    pdf.body(
        "After accepting the submission, FDA conducts a substantive review. The review process "
        "has defined timelines but can extend significantly if FDA requests additional information."
    )

    pdf.sub_heading("Step 7.1: Refuse to Accept (RTA) Check")
    pdf.body("Within 15-30 calendar days of submission:")
    pdf.bullet("FDA checks completeness against the RTA checklist")
    pdf.bullet("If acceptable: submission proceeds to substantive review")
    pdf.bullet("If not acceptable: FDA issues RTA letter listing deficiencies; you must resubmit")

    pdf.sub_heading("Step 7.2: Substantive Review")
    pdf.body("The primary FDA review period, typically 60-90 calendar days (MDUFA target: 90 days total):")
    pdf.bullet("FDA reviewer evaluates substantial equivalence argument")
    pdf.bullet("Reviews all test data against the proposed intended use")
    pdf.bullet("Assesses risk analysis for completeness and adequacy")
    pdf.bullet("Reviews software documentation (often the most scrutinized section)")
    pdf.bullet("Evaluates labeling for accuracy, completeness, and regulatory compliance")

    pdf.sub_heading("Step 7.3: Additional Information (AI) Requests")
    pdf.body(
        "During review, FDA may send one or more Additional Information (AI) requests. "
        "This is the interactive review phase:"
    )
    pdf.bullet("FDA sends a letter listing specific questions or deficiencies")
    pdf.bullet("You have 180 calendar days to respond")
    pdf.bullet("The review clock STOPS while you prepare your response")
    pdf.bullet("FDA may send multiple rounds of AI requests")

    pdf.challenge_box(
        "AI requests are where most 510(k) timelines slip. A single AI request can add "
        "30-90 days to your timeline. Multiple rounds can add 6+ months. The best defense: "
        "thorough pre-submission preparation and a strong Pre-Sub meeting that aligned "
        "your testing strategy with FDA expectations."
    )

    pdf.labeled_item("Common AI Request Topics:",
        "Incomplete performance data. Inadequate software documentation. Unclear substantial "
        "equivalence argument. Missing biocompatibility endpoints. Labeling deficiencies. "
        "Risk analysis gaps.")
    pdf.labeled_item("Response Strategy:",
        "Respond to every question completely. Do not leave any item partially addressed. "
        "If a question requires additional testing, include the test protocol, results, "
        "and updated analysis in your response. Treat each AI response as a mini-submission.")

    pdf.sub_heading("Step 7.4: Advisory Committee (Rare for 510(k))")
    pdf.body(
        "In rare cases, FDA may convene an advisory panel to review a 510(k). This is unusual "
        "for standard Class II devices but can occur for devices with novel technology. "
        "If triggered, it adds 3-6 months to the review timeline."
    )

    pdf.sub_heading("Control Tower Deliverables")
    pdf.bullet("AI response packages (if requested)")
    pdf.bullet("Updated test data (if additional testing required)")
    pdf.bullet("Communication log with FDA (all interactions documented)")
    pdf.bullet("Timeline tracker updated with actual vs. planned review dates")
    pdf.bullet("FDA Comms tab: timeline tracker reflects review milestones and AI rounds")

    # ════════════════════════════════════════════════════
    # PHASE 8: CLEARANCE DECISION
    # ════════════════════════════════════════════════════
    pdf.phase_heading("8", "Clearance Decision",
                      "Control Tower Milestone: M-CLEAR")

    pdf.body(
        "After completing the review (including any AI rounds), FDA issues a final decision."
    )

    pdf.sub_heading("Possible Outcomes")
    pdf.labeled_item("Substantially Equivalent (SE) -- CLEARED:",
        "The device is cleared for marketing. You receive a 510(k) clearance letter and a "
        "510(k) number (e.g., K2XXXXX). The device can be legally marketed in the US once "
        "all post-clearance requirements are met.")
    pdf.labeled_item("Not Substantially Equivalent (NSE):",
        "The device is NOT cleared. Options: (1) Request a De Novo classification, "
        "(2) Submit a new 510(k) with a different predicate, (3) Submit additional data "
        "to address FDA's concerns, (4) Request a meeting with FDA to discuss the path forward.")
    pdf.labeled_item("Withdrawn:",
        "If you do not respond to AI requests within 180 days, FDA will send a 'letter of intent "
        "to withdraw.' If still no response, the submission is withdrawn. You must start over.")

    pdf.callout_box(
        "Clearance is NOT approval. The 510(k) only establishes that the device is substantially "
        "equivalent to a legally marketed predicate. The distinction matters legally and for marketing claims."
    )

    pdf.sub_heading("Post-Decision Actions")
    pdf.bullet("Review clearance letter carefully for any conditions or limitations")
    pdf.bullet("Update all labeling to include the 510(k) number")
    pdf.bullet("Notify the team and trigger post-clearance activities")
    pdf.bullet("Archive the complete submission and review correspondence in the DHF")

    pdf.sub_heading("Control Tower Deliverables")
    pdf.bullet("510(k) clearance letter (archived)")
    pdf.bullet("Updated labeling with 510(k) number")
    pdf.bullet("Control Tower milestone M-CLEAR marked complete")
    pdf.bullet("Trigger post-clearance phase activities")

    # ════════════════════════════════════════════════════
    # PHASE 9: POST-CLEARANCE REQUIREMENTS
    # ════════════════════════════════════════════════════
    pdf.phase_heading("9", "Post-Clearance Requirements",
                      "Duration: Ongoing  |  Control Tower: Continuous Compliance Monitoring")

    pdf.body(
        "Clearance does not mean 'done.' Post-clearance requirements are ongoing obligations "
        "that continue for as long as the device is on the market."
    )

    pdf.sub_heading("9.1: Establishment Registration & Device Listing")
    pdf.body("Before commercially distributing the device:")
    pdf.bullet("Register the manufacturing establishment with FDA (FDA FURLS system)")
    pdf.bullet("List each device with its product code and 510(k) number")
    pdf.bullet("Annual registration renewal (by December 31 each year)")
    pdf.bullet("Annual registration fee (currently ~$7,653 per establishment)")

    pdf.labeled_item("Dual-Entity Note:",
        "If manufacturing occurs at Silan Technology (Chengdu) and Arch Medical is the US agent/importer, "
        "BOTH entities may need to register. Foreign manufacturers must designate a US Agent.")

    pdf.sub_heading("9.2: Quality System Regulation (QSR) Compliance")
    pdf.body(
        "21 CFR Part 820 (QSR) governs the manufacturing and quality management system. "
        "Key requirements include:"
    )
    pdf.bullet("Document controls (SOPs, work instructions, forms)")
    pdf.bullet("Design controls (maintained from Phase 3)")
    pdf.bullet("Purchasing controls (supplier qualification)")
    pdf.bullet("Production and process controls (manufacturing procedures)")
    pdf.bullet("CAPA system (Corrective and Preventive Action)")
    pdf.bullet("Complaint handling (mandatory for all customer complaints)")
    pdf.bullet("Management review (periodic review of quality system effectiveness)")

    pdf.callout_box(
        "FDA is transitioning from QSR (21 CFR 820) to ISO 13485 harmonization via the "
        "QMSR final rule (effective February 2026). This means your quality system should "
        "be built on ISO 13485 from the start -- it will satisfy both the current QSR and "
        "the future QMSR requirements."
    )

    pdf.sub_heading("9.3: Post-Market Surveillance")
    pdf.labeled_item("Medical Device Reporting (MDR):",
        "Mandatory reporting to FDA of any adverse events: deaths, serious injuries, or "
        "malfunctions that could cause death or serious injury. Reports must be filed within "
        "30 calendar days (or 5 days for events requiring remedial action).")
    pdf.labeled_item("Corrections and Removals:",
        "If a safety issue is identified after market release, you must report any corrections "
        "(fixes) or removals (recalls) to FDA. Voluntary recalls must still be reported.")
    pdf.labeled_item("Post-Market Clinical Follow-Up:",
        "While not required by FDA for most 510(k) devices, some international markets "
        "(EU MDR) require proactive post-market clinical follow-up (PMCF). Building this "
        "infrastructure early simplifies future international expansion.")

    pdf.sub_heading("9.4: Labeling & Marketing Compliance")
    pdf.bullet("Marketing claims must not exceed the cleared intended use")
    pdf.bullet("All promotional materials must be consistent with the 510(k) clearance")
    pdf.bullet("Any changes to intended use, technology, or materials may require a new 510(k)")

    pdf.challenge_box(
        "The most common post-clearance compliance failure: making marketing claims that "
        "exceed the cleared intended use. This can trigger FDA warning letters, consent "
        "decrees, or even criminal prosecution in severe cases."
    )

    pdf.sub_heading("9.5: Design Change Management")
    pdf.body(
        "After clearance, any change to the device must be evaluated to determine if a new "
        "510(k) is required:"
    )
    pdf.bullet("Changes to intended use: ALWAYS require a new 510(k)")
    pdf.bullet("Changes to materials, energy source, or fundamental technology: usually require new 510(k)")
    pdf.bullet("Minor design changes: evaluate using FDA's 'Deciding When to Submit a 510(k)' guidance")
    pdf.bullet("Software changes: evaluate using FDA's software modification guidance document")

    pdf.sub_heading("Control Tower Deliverables")
    pdf.bullet("FDA establishment registration confirmation")
    pdf.bullet("Device listing confirmation")
    pdf.bullet("Quality system procedures (ISO 13485 / QSR compliant)")
    pdf.bullet("CAPA system operational")
    pdf.bullet("Complaint handling procedure active")
    pdf.bullet("MDR reporting procedure documented")
    pdf.bullet("Post-market surveillance plan")
    pdf.bullet("Design change evaluation procedure")

    # ════════════════════════════════════════════════════
    # APPENDIX: DIGITAL TWIN SPECIFIC CONSIDERATIONS
    # ════════════════════════════════════════════════════
    pdf.phase_heading("A", "Digital Twin Program -- Specific Considerations",
                      "Appendix: Unique challenges for the ICU Respiratory Digital Twin System")

    pdf.body(
        "The Digital Twin program presents several unique challenges beyond a single-device "
        "510(k). This appendix summarizes the program-specific considerations that affect "
        "planning and execution."
    )

    pdf.sub_heading("A.1: Dual-Module Strategy")
    pdf.labeled_item("Two Separate 510(k) Submissions:",
        "Module A (sEMG, product code IKN) and Module B (EIT, product code DQS) are different "
        "device types with different predicates, different testing requirements, and different "
        "review divisions at FDA. They must be submitted as separate 510(k)s.")
    pdf.labeled_item("Sequential vs. Parallel Submission:",
        "The current plan sequences sEMG first (less novel, clearer predicate pathway) followed "
        "by EIT. This allows lessons learned from the sEMG submission to improve the EIT "
        "submission. However, it extends the total timeline.")
    pdf.labeled_item("Combined Device Considerations:",
        "If the final commercial product integrates both modules into a single system, a third "
        "510(k) may be needed for the combined device -- or the EIT 510(k) may need to address "
        "the combined use case. This must be resolved during Phase 1 pathway confirmation.")

    pdf.sub_heading("A.2: Cross-Border Manufacturing")
    pdf.labeled_item("Foreign Manufacturer Registration:",
        "Silan Technology (Chengdu) must register as a foreign manufacturer with FDA and "
        "designate a US Agent. Annual registration fees apply.")
    pdf.labeled_item("ISO 13485 Certification:",
        "The Chengdu facility must hold ISO 13485 certification. If not already certified, "
        "this process takes 6-12 months and is on the critical path.")
    pdf.labeled_item("Import Controls:",
        "FDA may inspect foreign manufacturing facilities. Initial Importer (Arch Medical) "
        "has specific labeling and record-keeping obligations.")

    pdf.sub_heading("A.3: Software as Core Technology")
    pdf.labeled_item("Software Level of Concern:",
        "Both sEMG and EIT involve diagnostic algorithms that process physiological signals. "
        "These are likely 'Moderate' level of concern (incorrect output could lead to incorrect "
        "clinical decisions). FDA will scrutinize software documentation heavily.")
    pdf.labeled_item("Algorithm Validation:",
        "The signal processing algorithms (sEMG neural drive quantification, EIT image "
        "reconstruction) must be validated against accepted clinical reference methods. "
        "This may require clinical performance data even for a 510(k).")
    pdf.labeled_item("Cybersecurity:",
        "FDA requires a cybersecurity assessment for all networked medical devices. If the "
        "Digital Twin system connects to hospital networks, a comprehensive cybersecurity "
        "risk analysis and mitigation plan is required in the 510(k).")

    pdf.sub_heading("A.4: Budget and Timeline Impact")
    w_budget = [60, 50, 70]
    pdf.table_row(["Cost Category", "Estimated Range", "Notes"], w_budget, header=True)
    pdf.table_row(["FDA User Fee (per 510k)", "$7K-$26K", "$6,517 small biz / $26,067 std"], w_budget, bold_first=True)
    pdf.table_row(["IEC 60601 Testing", "$15K-$40K", "Per module, accredited lab"], w_budget, bold_first=True)
    pdf.table_row(["EMC Testing", "$15K-$30K", "Per module"], w_budget, bold_first=True)
    pdf.table_row(["Biocompatibility", "$10K-$25K", "Per unique patient contact"], w_budget, bold_first=True)
    pdf.table_row(["Software V&V (external)", "$20K-$50K", "If using external consultant"], w_budget, bold_first=True)
    pdf.table_row(["Usability Study", "$15K-$40K", "Depends on # participants"], w_budget, bold_first=True)
    pdf.table_row(["Regulatory Consultant", "$30K-$80K", "If external RA support used"], w_budget, bold_first=True)
    pdf.table_row(["ISO 13485 Certification", "$15K-$30K", "If not already certified"], w_budget, bold_first=True)
    pdf.table_row(["Total (per module)", "$130K-$320K", "Highly variable"], w_budget, bold_first=True)
    pdf.ln(2)

    pdf.challenge_box(
        "With two modules, total regulatory costs could range from $260K to $640K. "
        "Against a $320K cash position with $45K/month burn, the funding timeline is extremely "
        "tight. Investor or grant funding may be needed before the EIT module submission."
    )

    # ── Closing ──
    pdf.ln(6)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(*GuidePDF.DARK)
    pdf.multi_cell(0, 5.5, _a(
        "This guide is maintained as a living document within the Control Tower system. "
        "All phase gates, deliverables, and milestones are tracked in the PM Dashboard. "
        "As the program progresses, each phase will be updated with actual dates, actual costs, "
        "and lessons learned."
    ), align="L")
    pdf.ln(6)
    pdf.set_font("Helvetica", "I", 9)
    pdf.set_text_color(*GuidePDF.GRAY)
    pdf.cell(0, 5, _a("Prepared by: Lon Dailey  |  Stanford SCPM  |  Arch Medical Management, LLC"), new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 5, _a("Reference: 21 CFR 807 Subpart E, FDA Guidance Documents, ISO 13485:2016, ISO 14971:2019"), new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 5, "March 21, 2026", new_x="LMARGIN", new_y="NEXT")

    path = os.path.join(OUT, "FDA_510k_Process_Guide.pdf")
    pdf.output(path)
    return path


if __name__ == "__main__":
    p = build()
    print(f"PDF: {p}")
    print("Done.")
