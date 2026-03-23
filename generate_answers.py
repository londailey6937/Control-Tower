#!/usr/bin/env python3
"""
Answer Sheet for PMP Certificate Course Exercises
===================================================
Model answers for all 11 exercises across 12 modules,
grounded in the ICU Respiratory Digital Twin case study data.
"""

import os
from fpdf import FPDF

OUT_DIR = os.path.dirname(os.path.abspath(__file__))

STANFORD = (140, 21, 21)
NAVY = (10, 40, 100)
BLUE = (30, 90, 200)
TEXT = (40, 40, 45)
DARK = (25, 25, 30)
GRAY = (120, 120, 130)
GREEN = (34, 139, 34)
LIGHT_BG = (245, 245, 248)


class AnswerPDF(FPDF):

    def header(self):
        if self.page_no() <= 1:
            return
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(*GRAY)
        self.cell(0, 5, "PMP Certificate Course  |  Exercise Answer Sheet  |  CONFIDENTIAL", align="L")
        self.ln(8)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(*GRAY)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")

    def ex_title(self, module, num, title):
        self.add_page()
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(*STANFORD)
        self.cell(0, 6, f"MODULE {module}  |  EXERCISE {num}", new_x="LMARGIN", new_y="NEXT")
        self.set_font("Helvetica", "B", 15)
        self.set_text_color(*NAVY)
        self.cell(0, 9, title, new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(*STANFORD)
        self.line(self.l_margin, self.get_y() + 1, self.w - self.r_margin, self.get_y() + 1)
        self.ln(6)

    def prompt(self, text):
        self.set_fill_color(*LIGHT_BG)
        x = self.l_margin
        w = self.w - self.l_margin - self.r_margin
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*GRAY)
        self.set_x(x)
        self.cell(w, 5, "QUESTION:", fill=True, new_x="LMARGIN", new_y="NEXT")
        self.set_font("Helvetica", "I", 9)
        self.set_text_color(*DARK)
        self.set_x(x)
        self.multi_cell(w, 5, text, fill=True, new_x="LMARGIN", new_y="NEXT")
        self.ln(4)

    def answer_head(self):
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(*GREEN)
        self.cell(0, 7, "MODEL ANSWER", new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def txt(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*TEXT)
        self.multi_cell(0, 5.5, text, new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def sub(self, title):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(*NAVY)
        self.cell(0, 7, title, new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def rubric(self, text):
        self.ln(2)
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*STANFORD)
        self.cell(0, 5, "GRADING RUBRIC:", new_x="LMARGIN", new_y="NEXT")
        self.set_font("Helvetica", "", 9)
        self.set_text_color(*TEXT)
        self.multi_cell(0, 5, text, new_x="LMARGIN", new_y="NEXT")
        self.ln(2)


def build():
    pdf = AnswerPDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)

    # ---- COVER ----
    pdf.add_page()
    pdf.ln(35)
    pdf.set_font("Helvetica", "B", 28)
    pdf.set_text_color(*STANFORD)
    pdf.cell(0, 12, "Exercise Answer Sheet", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)
    pdf.set_font("Helvetica", "", 14)
    pdf.set_text_color(*NAVY)
    pdf.cell(0, 8, "Certificate in Project Management", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 8, "Stanford School of Engineering", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)
    pdf.set_draw_color(*STANFORD)
    mid = pdf.w / 2
    pdf.line(mid - 50, pdf.get_y(), mid + 50, pdf.get_y())
    pdf.ln(10)
    pdf.set_font("Helvetica", "I", 12)
    pdf.set_text_color(*TEXT)
    pdf.cell(0, 7, "ICU Respiratory Digital Twin System -- Case Study", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(20)
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(*STANFORD)
    pdf.cell(0, 7, "CONFIDENTIAL -- FOR INSTRUCTOR USE ONLY", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(6)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(*GRAY)
    pdf.cell(0, 6, "11 Exercises  |  Modules 1-11  |  March 2026 Edition", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 6, "Model answers are illustrative. Accept equivalent responses demonstrating PM competence.", align="C", new_x="LMARGIN", new_y="NEXT")

    # ================================================================
    # EXERCISE 1 -- Module 1: PMP Decisions
    # ================================================================
    pdf.ex_title(1, 1, "Five PMP-Only Decisions")
    pdf.prompt(
        "List 5 decisions in the Digital Twin project that ONLY the PMP should make. "
        "For each, explain why delegating it to a technical lead or business lead would be risky.")
    pdf.answer_head()

    pdf.sub("Decision 1: Gate Go/No-Go at G1 (M+3)")
    pdf.txt(
        "The PMP alone decides whether the sEMG design verification gate passes. "
        "Delegating to the tech lead risks a biased 'proceed' because the team has invested months "
        "of effort and will be reluctant to admit 97.5% suppression falls short of the 98% criterion. "
        "Delegating to the business lead risks dismissing technical gaps to stay on the investor timeline.")

    pdf.sub("Decision 2: Regulatory pathway selection after Pre-Sub (M+2)")
    pdf.txt(
        "After FDA feedback at R2, the PMP must decide whether to proceed with 510(k) or pivot to "
        "De Novo. The regulatory lead may favor the pathway they have prepared for. The business lead "
        "may reject De Novo's +60 day timeline without appreciating the risk of a 510(k) rejection. "
        "Only the PMP can weigh both perspectives and make a binding call.")

    pdf.sub("Decision 3: Approving the 2-week extension request (INP-001)")
    pdf.txt(
        "The tech team requested 2 additional weeks to optimize the ECG-gating algorithm from 97.5% to "
        "98%. This impacts the critical path. The tech lead would always want more time; the business "
        "lead would always want faster delivery. The PMP must evaluate whether the 0.5% gap is worth "
        "the schedule impact against G1 criteria, which require >98%.")

    pdf.sub("Decision 4: Funding tranche release authorization")
    pdf.txt(
        "Phase 1 Seed ($2M) release should be tied to gate achievement. The business lead has an inherent "
        "conflict -- they need the money to operate. The tech lead doesn't see financial implications. "
        "Only the PMP can objectively certify that gate criteria are met before authorizing the next release.")

    pdf.sub("Decision 5: Scope change -- adding perfusion claims to initial EIT submission")
    pdf.txt(
        "If clinical data at T6 shows the V/Q algorithm exceeds expectations, the tech lead will push to "
        "include full perfusion claims in the R6 submission. The business lead will want maximum market "
        "impact. But adding claims changes the predicate strategy, testing requirements, and risk profile. "
        "Only the PMP can run the change through formal change control and decide whether the added scope "
        "is worth the schedule and regulatory risk.")

    pdf.rubric(
        "Full marks (5/5): Five distinct decisions, each with clear rationale for why delegation is risky. "
        "Partial marks: Accept any 5 decisions that are genuinely cross-functional and require integration "
        "of technical, regulatory, and business considerations. Deduct if decisions are only technical "
        "(e.g., 'which ADC to use') or only business (e.g., 'which investor to approach').")

    # ================================================================
    # EXERCISE 2 -- Module 2: Project Charter
    # ================================================================
    pdf.ex_title(2, 2, "One-Page Project Charter")
    pdf.prompt(
        "Draft a one-page project charter for the Digital Twin project. Include all six elements. "
        "Your charter should be specific enough that a new PM could pick up the project from it.")
    pdf.answer_head()

    pdf.sub("PROJECT CHARTER: ICU Respiratory Digital Twin System")
    pdf.txt("Date: March 2026  |  Prepared by: [Student Name], PMP  |  Version: 1.0")

    pdf.sub("1. WHY (Business Case)")
    pdf.txt(
        "The global ICU respiratory monitoring market is $6B+. Current solutions are either invasive "
        "(Getinge NAVA, requiring nasogastric catheter) or limited to ventilation only (Timpel EIT). "
        "No product integrates neural drive, ventilation, and perfusion non-invasively. Annual cost of "
        "ventilator-associated complications exceeds $10K per ICU patient. The Digital Twin addresses "
        "all three dimensions, creating a first-mover advantage in integrated respiratory monitoring.")

    pdf.sub("2. WHAT (Scope)")
    pdf.txt(
        "Deliverables:\n"
        "  Module A: sEMG Neural Drive Monitoring (FDA product code IKN)\n"
        "  Module B: EIT Ventilation/Perfusion Imaging (FDA product code DQS)\n"
        "  MyoBus Integration Protocol (<1ms data alignment)\n"
        "  Two FDA 510(k) clearances (modular approval strategy)\n"
        "Exclusions: Clinical trials (PMA not required), international regulatory filings, "
        "post-market surveillance system.")

    pdf.sub("3. WHO (Stakeholders)")
    pdf.txt(
        "  Sponsor: Company B USA Board of Directors\n"
        "  PMP: [Student Name] -- overriding decision authority at all gates\n"
        "  Tech Lead: Silan Technology CTO (Chengdu)\n"
        "  Regulatory Lead: US-based RA consultant\n"
        "  Business Lead: Company B USA COO\n"
        "  External: FDA/CDRH, investors, target acquirers (Drager, Getinge, Mindray)")

    pdf.sub("4. WHEN (Timeline)")
    pdf.txt(
        "  M+0 (Mar 2026): Project kickoff, Pre-Sub filed\n"
        "  M+2 (May 2026): FDA Pre-Submission meeting\n"
        "  M+6 (Sep 2026): 510(k) sEMG submission\n"
        "  M+9 (Dec 2026): sEMG clearance expected\n"
        "  M+17 (Aug 2027): 510(k) EIT submission\n"
        "  M+23 (Feb 2028): Full platform clearance\n"
        "  6 gates: G1(M+3), G2(M+2), G3(M+6), G4(M+9), G5(M+17), G6(M+23)")

    pdf.sub("5. HOW MUCH (Budget)")
    pdf.txt(
        "  Total: $5.0M\n"
        "  Phase 1 Seed: $2.0M (IP buyout, sEMG FDA, quality system)\n"
        "  Phase 2 Growth: $3.0M (EIT testing, US operations, supply chain)\n"
        "  Current cash: $320K  |  Monthly burn: $45K  |  Runway: ~7 months\n"
        "  Funding received: $400K (Founder Seed $150K + Angel $250K)")

    pdf.sub("6. RISKS (Top 5)")
    pdf.txt(
        "  1. RISK-007 [Red]: 510(k) predicate rejection -- De Novo fallback +60 days\n"
        "  2. RISK-008 [Red]: Funding runway insufficient before M+9 clearance\n"
        "  3. RISK-004 [Red]: V/Q image misinterpretation leading to clinical harm\n"
        "  4. RISK-001 [Yellow]: False-negative sEMG signal (missed apnea)\n"
        "  5. RISK-002 [Yellow]: ECG artifact false positive")

    pdf.rubric(
        "Full marks: All 6 sections present, accurate to case data, specific enough for a new PM. "
        "Deduct for: missing sections, vague statements ('some funding needed'), incorrect dates/amounts, "
        "or scope that contradicts the 510(k) pathway (e.g., including clinical trials).")

    # ================================================================
    # EXERCISE 3 -- Module 3: WBS Decomposition
    # ================================================================
    pdf.ex_title(3, 3, "WBS Level 4 Decomposition")
    pdf.prompt(
        "Decompose WBS item 1.2.3 (Bench & Performance Testing) to Level 4. "
        "Identify at least 6 work packages using the IEC 60601-1 test categories as a guide.")
    pdf.answer_head()

    pdf.sub("1.2.3  Bench & Performance Testing -- sEMG Module")
    pdf.txt(
        "  1.2.3.1  Electrical Safety Testing (IEC 60601-1)\n"
        "    - Patient leakage current (<10 uA), earth leakage, dielectric strength\n"
        "    - Duration: ~2 weeks  |  Owner: Test Lab\n\n"
        "  1.2.3.2  EMC Testing (IEC 60601-1-2 Ed.4.1)\n"
        "    - Radiated emissions, conducted emissions, ESD immunity, radiated immunity\n"
        "    - Duration: ~3 weeks  |  Owner: EMC Lab\n\n"
        "  1.2.3.3  Usability Study (IEC 62366 / IEC 60601-1-6)\n"
        "    - Formative usability evaluation with 15+ representative ICU clinicians\n"
        "    - Task analysis, use error risk analysis, summative report\n"
        "    - Duration: ~4 weeks  |  Owner: Human Factors Engineer\n\n"
        "  1.2.3.4  Algorithm Performance Validation\n"
        "    - sEMG vs. esophageal EMG reference (n>=30 subjects)\n"
        "    - Sensitivity >=92%, specificity >=88%, latency <50ms\n"
        "    - Duration: ~6 weeks  |  Owner: Algorithm Team + Clinical Site\n\n"
        "  1.2.3.5  ECG-Gating Algorithm Verification\n"
        "    - Confirm suppression >98% across diverse patient morphologies\n"
        "    - SNR improvement >20 dB documented\n"
        "    - Duration: ~2 weeks  |  Owner: Algorithm Team\n\n"
        "  1.2.3.6  Software Verification (IEC 62304)\n"
        "    - Unit testing, integration testing, system testing\n"
        "    - Software safety classification Class B confirmed\n"
        "    - Traceability matrix: requirements -> design -> test cases\n"
        "    - Duration: ~3 weeks  |  Owner: Software QA\n\n"
        "  1.2.3.7  Environmental & Transport Testing\n"
        "    - Temperature, humidity, vibration, drop testing\n"
        "    - Per IEC 60601-1 Clause 11 (environmental conditions)\n"
        "    - Duration: ~2 weeks  |  Owner: Test Lab\n\n"
        "  1.2.3.8  Test Report Compilation & Gap Analysis\n"
        "    - Consolidate all test reports into 510(k) format\n"
        "    - Gap analysis against acceptance criteria\n"
        "    - Duration: ~1 week  |  Owner: Regulatory Lead")

    pdf.rubric(
        "Full marks: 6+ work packages, each with clear deliverable, traceable to a standard, reasonable "
        "duration/owner. Accept any valid IEC 60601-1 test category not listed above. Deduct for: "
        "packages that are too broad ('do all testing'), missing standard references, or violating "
        "the 8/80 rule (packages <8 hours or >80 hours of effort).")

    # ================================================================
    # EXERCISE 4 -- Module 4: Network Diagram & Float
    # ================================================================
    pdf.ex_title(4, 4, "Network Diagram & Float Calculation")
    pdf.prompt(
        "Draw the network diagram for the Digital Twin project using the 8 technical milestones "
        "(T1-T8) and 9 regulatory milestones (R1-R9). Identify which activities have float "
        "and calculate the total float for each.")
    pdf.answer_head()

    pdf.sub("Activity List with Dependencies")
    pdf.txt(
        "  T1 (M+0, dur=0): Prototype Finalization   | Predecessors: none\n"
        "  T2 (M+1, dur=2): ECG-Gating Validation     | Predecessors: T1\n"
        "  T3 (M+3, dur=3): Bench Testing sEMG        | Predecessors: T1, T2\n"
        "  T4 (M+6, dur=0): Sensitivity Targets Met    | Predecessors: T3\n"
        "  T5 (M+8, dur=4): EIT Prototype              | Predecessors: none (can start independently)\n"
        "  T6 (M+12, dur=5): V/Q Algorithm Validation  | Predecessors: T5\n"
        "  T7 (M+14, dur=3): EIT Biocompatibility      | Predecessors: T5\n"
        "  T8 (M+2, dur=6): MyoBus Integration         | Predecessors: T1\n"
        "  R1 (M+0, dur=0): Pre-Sub Filed              | Predecessors: none\n"
        "  R2 (M+2, dur=0): Pre-Sub Meeting            | Predecessors: R1 + 2 month lag\n"
        "  R3 (M+6, dur=0): 510(k) sEMG Submission    | Predecessors: T3, T4, R2\n"
        "  R4 (M+9, dur=0): sEMG Clearance             | Predecessors: R3 + 3 month FDA review\n"
        "  R5 (M+12, dur=5): EIT 510(k) Prep           | Predecessors: R4, T5\n"
        "  R6 (M+17, dur=0): 510(k) EIT Submission     | Predecessors: R5, T6, T7\n"
        "  R7 (M+23, dur=0): EIT Clearance             | Predecessors: R6 + 6 month FDA review\n"
        "  R8 (M+1, dur=1): IP Buyout & Legal          | Predecessors: none\n"
        "  R9 (M+2, dur=1): ISO 13485 Audit            | Predecessors: none")

    pdf.sub("Critical Path")
    pdf.txt(
        "Path 1 (Critical): T1 -> T3 -> R3 -> R4 -> R5 -> T6 -> R6 -> R7 = 23 months\n"
        "Path 2: T1 -> T2 -> T3 -> R3 (merges with Path 1)  = same endpoint\n"
        "Path 3: T5 -> T6 -> R6 -> R7 = M+8 to M+23 = 15 months\n"
        "Path 4: T5 -> T7 -> R6 (merges) = M+8 to M+17 = 9 months")

    pdf.sub("Float Calculations")
    pdf.txt(
        "  T1:  Float = 0 (on critical path)\n"
        "  T2:  Float = 2 months (starts M+1, must finish before T3 at M+3; can slip 2 mo)\n"
        "  T3:  Float = 0 (on critical path)\n"
        "  T4:  Float = 0 (on critical path -- gates R3)\n"
        "  T5:  Float = 4 months (starts M+8, but T6 at M+12 is gated by R5 at M+12)\n"
        "  T6:  Float = 0 (on critical path via R6)\n"
        "  T7:  Float = 3 months (finishes M+17, same as R6 -- but T7 completes by M+17)\n"
        "  T8:  Float = large (MyoBus integration not on critical path; needed for launch)\n"
        "  R1:  Float = 0\n"
        "  R2:  Float = 0 (gates R3 submission)\n"
        "  R3:  Float = 0 (on critical path)\n"
        "  R4:  Float = 0 (external FDA constraint)\n"
        "  R5:  Float = 0 (on critical path)\n"
        "  R6:  Float = 0 (on critical path)\n"
        "  R7:  Float = 0 (project end)\n"
        "  R8:  Float = large (legal/IP work is parallel, not gating submissions directly)\n"
        "  R9:  Float = ~4 months (audit needed before G3 at M+6, scheduled at M+2)")

    pdf.rubric(
        "Full marks: Clear network diagram with correct dependencies, critical path identified, float "
        "calculated for at least 10 activities. Accept minor duration variations. Deduct for: missing "
        "dependencies between R2->R3, wrong critical path, or confusing milestones with activities.")

    # ================================================================
    # EXERCISE 5 -- Module 5: EVM Calculation
    # ================================================================
    pdf.ex_title(5, 5, "Earned Value Management Calculation")
    pdf.prompt(
        "At M+3, the Digital Twin has completed T1 (budgeted $80K, actual $75K), T2 (budgeted "
        "$60K, actual $72K), and R1 (budgeted $15K, actual $12K). T3 is 20% complete (budgeted "
        "$120K, actual spend to date $30K). Calculate PV, EV, AC, SV, CV, SPI, and CPI.")
    pdf.answer_head()

    pdf.sub("Step 1: Determine Planned Value (PV)")
    pdf.txt(
        "PV = budgeted cost of work SCHEDULED to be done by M+3.\n"
        "By M+3, the plan says T1, T2, R1 should be complete, and T3 should begin.\n"
        "Assuming T3 was planned to be 20% complete by M+3:\n"
        "  PV = $80K (T1) + $60K (T2) + $15K (R1) + 20% x $120K (T3)\n"
        "  PV = $80K + $60K + $15K + $24K = $179,000")

    pdf.sub("Step 2: Determine Earned Value (EV)")
    pdf.txt(
        "EV = budgeted cost of work ACTUALLY completed.\n"
        "  T1: 100% complete -> $80K earned\n"
        "  T2: 100% complete -> $60K earned\n"
        "  R1: 100% complete -> $15K earned\n"
        "  T3: 20% complete -> 20% x $120K = $24K earned\n"
        "  EV = $80K + $60K + $15K + $24K = $179,000")

    pdf.sub("Step 3: Determine Actual Cost (AC)")
    pdf.txt(
        "AC = actual money spent.\n"
        "  T1: $75K + T2: $72K + R1: $12K + T3: $30K\n"
        "  AC = $189,000")

    pdf.sub("Step 4: Calculate Variances and Indices")
    pdf.txt(
        "  SV = EV - PV = $179K - $179K = $0\n"
        "     Interpretation: Perfectly on schedule.\n\n"
        "  CV = EV - AC = $179K - $189K = -$10,000\n"
        "     Interpretation: $10K over budget.\n\n"
        "  SPI = EV / PV = $179K / $179K = 1.00\n"
        "     Interpretation: On schedule (SPI = 1.0 is perfect).\n\n"
        "  CPI = EV / AC = $179K / $189K = 0.948\n"
        "     Interpretation: For every $1 spent, only $0.95 of value earned.\n"
        "     The project is on schedule but 5.2% over budget.\n\n"
        "  Root cause: T2 (ECG-Gating) cost $72K vs. $60K budget (+$12K, +20% overrun).\n"
        "  This aligns with INP-001 -- the team needed extra optimization time.\n"
        "  T1 and R1 came in under budget, partially offsetting the T2 overrun.\n"
        "  T3 is slightly over ($30K actual vs. $24K earned -- CPI of 0.80 for T3 alone).")

    pdf.sub("Step 5: Forecasting (Bonus)")
    pdf.txt(
        "  BAC (Budget at Completion) = total project budget\n"
        "  If BAC = $5,000,000:\n"
        "    EAC = BAC / CPI = $5.0M / 0.948 = $5,274,262\n"
        "    ETC = EAC - AC = $5,274,262 - $189,000 = $5,085,262\n"
        "    VAC = BAC - EAC = $5.0M - $5.274M = -$274,262 (projected overrun)\n"
        "    TCPI = (BAC - EV) / (BAC - AC) = ($5.0M - $179K) / ($5.0M - $189K)\n"
        "         = $4,821,000 / $4,811,000 = 1.002\n"
        "    Interpretation: Must perform at CPI of 1.002 for remaining work to finish on budget.\n"
        "    This is achievable -- the overrun is minimal and correctable.")

    pdf.rubric(
        "Full marks: All 7 metrics correct with units. Show work. Interpretation for each metric. "
        "Bonus points for EAC/ETC/TCPI. Deduct for: wrong PV (forgetting T3 partial), wrong AC "
        "(using budget instead of actual), or missing interpretation. Accept minor rounding differences.")

    # ================================================================
    # EXERCISE 6 -- Module 6: Risk Response Plan
    # ================================================================
    pdf.ex_title(6, 6, "Risk Response Plan for RISK-007")
    pdf.prompt(
        "RISK-007 (predicate rejection) has medium probability because the Timpel predicate K "
        "number has not been verified. Draft a Risk Response Plan with specific actions, owners, "
        "triggers, and a De Novo contingency timeline showing the +60 day impact on the schedule.")
    pdf.answer_head()

    pdf.sub("RISK-007: 510(k) Predicate Device Rejection")
    pdf.txt(
        "Risk Statement: FDA does not accept the proposed predicate device for either Module A "
        "(sEMG, IKN) or Module B (EIT, DQS), requiring De Novo classification.\n"
        "Current Rating: Severity = High | Probability = Medium | Level = RED\n"
        "Response Strategy: MITIGATE (primary) + ACCEPT with contingency (secondary)")

    pdf.sub("Primary Mitigation Actions")
    pdf.txt(
        "  Action 1: Verify Timpel predicate K number through FDA 510(k) database search\n"
        "    Owner: Regulatory Lead  |  Deadline: M+0 (before Pre-Sub meeting)\n"
        "    Status: IN PROGRESS -- the K number cited in source documents was incorrect\n\n"
        "  Action 2: Identify 2-3 alternative predicate devices for each module\n"
        "    Owner: Regulatory Lead  |  Deadline: M+1\n"
        "    Approach: Search FDA 510(k) database for IKN and DQS product codes\n\n"
        "  Action 3: Include predicate strategy as Priority Item in Pre-Sub (R2)\n"
        "    Owner: PMP + Regulatory Lead  |  Deadline: M+2\n"
        "    Ask FDA directly: 'Do you concur with [Predicate X] as primary predicate?'\n\n"
        "  Action 4: Document substantial equivalence comparison table\n"
        "    Owner: Regulatory Lead + Tech Lead  |  Deadline: M+4\n"
        "    Side-by-side comparison: indications, technology, performance, labeling")

    pdf.sub("Triggers for Contingency Activation")
    pdf.txt(
        "  Trigger 1: FDA Pre-Sub feedback (R2) explicitly rejects all proposed predicates\n"
        "  Trigger 2: FDA 510(k) review issues Additional Information (AI) request citing\n"
        "             'no substantial equivalence' concerns\n"
        "  Trigger 3: Pre-Sub feedback indicates device is 'novel' with no predicate pathway")

    pdf.sub("Contingency Plan: De Novo Pathway")
    pdf.txt(
        "If triggered, the De Novo pathway adds approximately 60 days to the review timeline:\n\n"
        "  Original 510(k) Timeline:\n"
        "    R3 (M+6) -> FDA review 90 days -> R4 Clearance (M+9)\n\n"
        "  De Novo Timeline:\n"
        "    R3 (M+6) -> Convert to De Novo -> FDA review ~150 days -> Clearance (M+11)\n\n"
        "  Impact Summary:\n"
        "    - Schedule: +2 months for Module A (M+9 -> M+11)\n"
        "    - Cost: +$50-100K for additional De Novo documentation and fees\n"
        "    - Funding: Runway must extend to cover M+11 (currently 7 months from M+0)\n"
        "    - Cascade: G4 (Commercial Launch) shifts from M+9 to M+11\n"
        "    - Module B NOT directly affected if Module A De Novo succeeds\n\n"
        "  De Novo Advantages:\n"
        "    - Creates a NEW predicate (our device becomes the reference for future competitors)\n"
        "    - Demonstrates novelty, which may strengthen IP and acquisition value\n"
        "    - FDA has been receptive to De Novo for innovative diagnostic devices")

    pdf.sub("Residual Risk After Mitigation")
    pdf.txt(
        "With all 4 actions complete plus De Novo contingency documented:\n"
        "  Severity: High (unchanged -- regulatory rejection is always high impact)\n"
        "  Probability: Low (reduced from Medium by Pre-Sub engagement and backup predicates)\n"
        "  Revised Level: YELLOW (from RED)\n"
        "  Residual: Manageable")

    pdf.rubric(
        "Full marks: Clear risk statement, 3+ mitigation actions with owners/deadlines, defined "
        "triggers, De Novo timeline with specific month impacts, cost estimate, and residual re-rating. "
        "Deduct for: vague actions ('talk to FDA'), missing owners, no timeline impact calculation, "
        "or claiming De Novo is 'no big deal' without quantifying the schedule/cost impact.")

    # ================================================================
    # EXERCISE 7 -- Module 7: Compliance Traceability Matrix
    # ================================================================
    pdf.ex_title(7, 7, "Compliance Traceability Matrix")
    pdf.prompt(
        "Create a compliance traceability matrix mapping each of the 12 standards to specific "
        "WBS work packages. For each standard, identify the gate at which it must be complete.")
    pdf.answer_head()

    pdf.txt(
        "STD-01  IEC 60601-1 (General Safety)\n"
        "  WBS: 1.2.3.1 (Electrical Safety), 1.3.3 (EIT Safety)\n"
        "  Must be complete by: G3 (M+6) for sEMG, G5 (M+17) for EIT\n\n"
        "STD-02  IEC 60601-1-2 (EMC)\n"
        "  WBS: 1.2.3.2 (sEMG EMC), 1.3.3 (EIT EMC)\n"
        "  Must be complete by: G3 (M+6) for sEMG, G5 (M+17) for EIT\n\n"
        "STD-03  IEC 60601-1-6 (Usability)\n"
        "  WBS: 1.2.3.3 (Usability Study)\n"
        "  Must be complete by: G3 (M+6)\n\n"
        "STD-04  ISO 14971 (Risk Management)\n"
        "  WBS: 1.1.4 (Change Control), 1.2.3 (Testing), 1.3.3 (Testing)\n"
        "  Must be complete by: G3 (M+6) initial, maintained through G6 (M+23)\n\n"
        "STD-05  ISO 10993-1 (Biocompatibility Framework)\n"
        "  WBS: 1.2.3 (sEMG electrode materials)\n"
        "  Must be complete by: G3 (M+6)\n\n"
        "STD-06  ISO 10993-5 (Cytotoxicity)\n"
        "  WBS: 1.2.3 (sEMG electrodes), 1.3.3 (EIT belt)\n"
        "  Must be complete by: G3 (M+6) for sEMG, G5 (M+17) for EIT\n\n"
        "STD-07  ISO 10993-10 (Sensitization & Irritation)\n"
        "  WBS: 1.2.3 (sEMG electrodes), 1.3.3 (EIT belt)\n"
        "  Must be complete by: G3 (M+6) for sEMG, G5 (M+17) for EIT\n\n"
        "STD-08  FDA Cybersecurity 2023\n"
        "  WBS: 1.4 (MyoBus Integration), 1.2.3.6 (SW Verification)\n"
        "  Must be complete by: G3 (M+6) -- applies to all connected components\n\n"
        "STD-09  21 CFR Part 820 (QSR)\n"
        "  WBS: 1.5.2 (ISO 13485 Audit), 1.1 (PM processes)\n"
        "  Must be complete by: G1 (M+3) initial, maintained through G6\n\n"
        "STD-10  21 CFR Part 11 (Electronic Records)\n"
        "  WBS: 1.4 (MyoBus -- RBAC/encryption), 1.2.3.6 (SW Verification)\n"
        "  Must be complete by: G3 (M+6)\n\n"
        "STD-11  IEC 62304 (Software Lifecycle)\n"
        "  WBS: 1.2.3.6 (SW Verification), 1.4 (MyoBus)\n"
        "  Must be complete by: G3 (M+6) for sEMG SW, G5 (M+17) for EIT SW\n\n"
        "STD-12  ISO 13485 (QMS -- Silan Manufacturing)\n"
        "  WBS: 1.5.2 (ISO 13485 Audit at Silan)\n"
        "  Must be complete by: G1 (M+3) gap assessment, G3 (M+6) full compliance")

    pdf.rubric(
        "Full marks: All 12 standards mapped to at least one WBS item and one gate. "
        "Accept reasonable WBS numbering variations. Deduct for: missing standards, no gate assignment, "
        "or assigning all standards to the same gate (demonstrates no understanding of phased compliance).")

    # ================================================================
    # EXERCISE 8 -- Module 8: Investor Update
    # ================================================================
    pdf.ex_title(8, 8, "Month 3 Investor Update")
    pdf.prompt(
        "Write a one-page investor update for Month 3, using only information from the "
        "case study data. Include: progress vs plan, risk status (traffic lights), "
        "cash position, and the next milestone to watch.")
    pdf.answer_head()

    pdf.sub("INVESTOR UPDATE -- M+3 (June 2026)")
    pdf.txt("ICU Respiratory Digital Twin System  |  Company B USA  |  Confidential")

    pdf.sub("Executive Summary")
    pdf.txt(
        "The project is ON TRACK through Month 3. Two of eight technical milestones are complete, "
        "the FDA Pre-Submission meeting has occurred (G2 passed), and bench testing is underway. "
        "No red flags from FDA feedback. Burn rate is stable at $45K/month.")

    pdf.sub("Progress vs. Plan")
    pdf.txt(
        "  COMPLETE:\n"
        "    T1 (M+0): sEMG Prototype Finalized -- on time\n"
        "    T2 (M+1): ECG-Gating Algorithm at 97.5% -- within 0.5% of 98% target\n"
        "    R1 (M+0): Pre-Sub Q-Meeting Filed -- on time\n"
        "    R8 (M+1): IP Buyout & US Legal -- in progress, on track\n\n"
        "  IN PROGRESS:\n"
        "    T3 (M+3): Bench & Performance Testing -- just started, on schedule\n"
        "    T8 (M+2): MyoBus Protocol Integration -- in progress\n"
        "    R2 (M+2): Pre-Sub Meeting -- completed, FDA feedback received\n"
        "    R9 (M+2): ISO 13485 Audit at Silan -- initiated\n\n"
        "  GATE STATUS:\n"
        "    G1 (M+3): Under review -- ECG-gating at 97.5% (target 98%)\n"
        "    G2 (M+2): PASSED -- FDA feedback received on predicate strategy")

    pdf.sub("Risk Dashboard (Traffic Lights)")
    pdf.txt(
        "  [RED]    RISK-007: Predicate acceptance -- Pre-Sub feedback pending analysis\n"
        "  [RED]    RISK-008: Funding runway -- 7 months at current burn; need Phase 1 close\n"
        "  [RED]    RISK-004: V/Q imaging misinterpretation -- not yet active (Module B)\n"
        "  [YELLOW] RISK-001: sEMG false negative -- mitigation in progress\n"
        "  [YELLOW] RISK-002: ECG artifact -- algorithm at 97.5%, iterating\n"
        "  [GREEN]  RISK-003, RISK-006: Under control")

    pdf.sub("Cash Position")
    pdf.txt(
        "  Cash on hand: ~$185K (started $320K, 3 months at $45K/month)\n"
        "  Monthly burn: $45,000 (stable)\n"
        "  Runway remaining: ~4 months at current burn\n"
        "  Phase 1 Seed ($2M): In pipeline -- critical to close by M+5\n"
        "  ACTION NEEDED: Phase 1 close must accelerate to avoid runway crisis before R3 (M+6)")

    pdf.sub("Next Milestone to Watch")
    pdf.txt(
        "  G1 at M+3: sEMG Design Verification -- decision pending this month\n"
        "  The ECG-gating criterion (>98%) is 0.5% short. Tech team has requested 2 additional "
        "  weeks (INP-001). PMP will decide at gate review.\n\n"
        "  Next critical date: R3 at M+6 -- 510(k) sEMG submission to FDA\n"
        "  This is the single biggest investor confidence checkpoint on the roadmap.")

    pdf.rubric(
        "Full marks: Professional format, all four sections present, numbers accurate to case data, "
        "clear action item on funding, specific next milestone with date. Deduct for: vague risk "
        "descriptions, wrong cash numbers, missing traffic lights, or using jargon without translation "
        "(e.g., 'IKN product code' without explaining what it means to investors).")

    # ================================================================
    # EXERCISE 9 -- Module 9: Gate Review
    # ================================================================
    pdf.ex_title(9, 9, "Gate G2 Review Package")
    pdf.prompt(
        "Gate G2 is at M+2 (May 2026). The FDA has not yet sent written feedback. "
        "As PMP, draft the gate review agenda, list the data you would present, "
        "and describe what decision options you would present to the steering committee. "
        "What is your recommended decision if only 2 of 4 criteria are met?")
    pdf.answer_head()

    pdf.sub("GATE G2 REVIEW AGENDA")
    pdf.txt(
        "Date: May 2026 (M+2)  |  Gate: G2 -- Pre-Sub FDA Feedback Received\n"
        "Chair: PMP  |  Attendees: Regulatory Lead, Tech Lead, Business Lead, Sponsor Rep\n\n"
        "  1. Welcome & Purpose (5 min)\n"
        "  2. Gate Criteria Review -- status of each criterion (15 min)\n"
        "  3. Data Package Presentation (20 min)\n"
        "  4. Risk & Impact Discussion (15 min)\n"
        "  5. Decision & Action Items (15 min)")

    pdf.sub("Gate Criteria Status (scenario: 2 of 4 met)")
    pdf.txt(
        "  Criterion 1: FDA written feedback received\n"
        "    STATUS: NOT MET -- FDA acknowledged Q-Sub, meeting scheduled but not held yet\n\n"
        "  Criterion 2: Predicate device strategy accepted\n"
        "    STATUS: NOT MET -- cannot be confirmed without FDA feedback\n\n"
        "  Criterion 3: Testing protocol approved by FDA\n"
        "    STATUS: MET -- testing protocols prepared and submitted in Q-Sub package;\n"
        "    internal review complete; ready for FDA concurrence\n\n"
        "  Criterion 4: Software classification confirmed (Class C / IEC 62304 Class B)\n"
        "    STATUS: MET -- internal classification analysis complete, documentation ready")

    pdf.sub("Data Package Presented")
    pdf.txt(
        "  - Q-Sub submission confirmation (R1 documentation)\n"
        "  - FDA correspondence log (acknowledgment received, meeting date set)\n"
        "  - Predicate device comparison table (prepared, awaiting FDA concurrence)\n"
        "  - Testing protocol document (complete, IEC 60601-1, ISO 10993 coverage)\n"
        "  - Software classification report (IEC 62304 Class B rationale)\n"
        "  - Risk register update (RISK-007 status)\n"
        "  - Schedule impact analysis if gate delays")

    pdf.sub("Decision Options")
    pdf.txt(
        "  Option A: HOLD (Recommended)\n"
        "    Rationale: 2 of 4 criteria met. The unmet criteria (FDA feedback, predicate "
        "    acceptance) are EXTERNAL dependencies -- we cannot force them. But proceeding "
        "    without FDA concurrence on predicate strategy risks building a submission that "
        "    FDA will reject. HOLD for 2-4 weeks until FDA meeting occurs.\n"
        "    Impact: Minor (testing can continue in parallel, no critical path delay if FDA "
        "    meeting happens within the 2-4 week window)\n\n"
        "  Option B: CONDITIONAL PROCEED\n"
        "    Proceed with testing under current predicate assumption.\n"
        "    Risk: If FDA rejects predicate at meeting, testing may need to be redone.\n"
        "    Acceptable only if the testing investment is low ($<20K at risk).\n\n"
        "  Option C: STOP\n"
        "    Not warranted. FDA has not rejected anything -- they simply haven't responded yet.\n"
        "    Stopping would be premature.")

    pdf.sub("Recommended Decision: HOLD")
    pdf.txt(
        "HOLD for a maximum of 4 weeks. Continue all non-gate-dependent work (T3 bench testing "
        "prep, T8 MyoBus integration, R9 ISO 13485 audit). Re-evaluate G2 at M+3 when FDA "
        "meeting is expected. If FDA meeting slips beyond M+3, escalate to sponsor for "
        "schedule contingency discussion.\n\n"
        "This is a HOLD, not a STOP. The project continues on all non-gated activities. The "
        "only thing halted is the formal 'proceed to prepare 510(k) package' authorization.")

    pdf.rubric(
        "Full marks: Structured agenda, criteria status for all 4, clear recommendation with rationale, "
        "all three decision options presented. Key insight: unmet criteria are external (FDA timing), "
        "not internal failure. Deduct for: recommending PROCEED without acknowledging risk, recommending "
        "STOP (disproportionate), or missing the distinction between HOLD and STOP.")

    # ================================================================
    # EXERCISE 10 -- Module 10: Sprint Board
    # ================================================================
    pdf.ex_title(10, 10, "Kanban Sprint Board Design")
    pdf.prompt(
        "Design a sprint board (Kanban) for the two-week period between M+1 and M+2, "
        "when T2 (ECG-Gating) and T8 (MyoBus) are both in progress. Define columns, "
        "WIP limits, and the Definition of Done for each work item.")
    pdf.answer_head()

    pdf.sub("Board Structure")
    pdf.txt(
        "COLUMNS:\n"
        "  Backlog | Ready | In Progress (WIP=3) | Review (WIP=2) | Done\n\n"
        "WIP Limits Rationale:\n"
        "  In Progress = 3: Two parallel streams (T2, T8) plus one shared resource task\n"
        "  Review = 2: Only regulatory or tech lead can review; bottleneck if >2")

    pdf.sub("Backlog Items (prioritized)")
    pdf.txt(
        "T2 Items:\n"
        "  T2-A: Implement adaptive filter v3 (target 98% suppression)\n"
        "  T2-B: Run validation against 30-patient dataset\n"
        "  T2-C: Document SNR improvement report (>20 dB)\n"
        "  T2-D: Peer review of algorithm by external expert\n\n"
        "T8 Items:\n"
        "  T8-A: Implement timestamp alignment module (<1ms)\n"
        "  T8-B: Integrate AES-256 encryption layer\n"
        "  T8-C: Build RBAC access control framework\n"
        "  T8-D: HL7 FHIR output adapter\n"
        "  T8-E: Integration smoke test (sEMG + EIT data paths)")

    pdf.sub("Definition of Done")
    pdf.txt(
        "T2-A: Filter code merged, unit tests pass, suppression rate measured at >=97.8% on\n"
        "       test dataset (stepping stone to 98%)\n"
        "T2-B: Validation report generated, n>=30, sensitivity and specificity calculated\n"
        "T2-C: Written report reviewed by tech lead, numbers match test logs\n"
        "T2-D: External reviewer signs off, no critical findings\n\n"
        "T8-A: Alignment measured at <1ms on bench test with 1000 sample pairs\n"
        "T8-B: Encryption verified with test vectors, key management documented\n"
        "T8-C: Role definitions documented, access matrix tested\n"
        "T8-D: FHIR output validated against HL7 schema, sample messages generated\n"
        "T8-E: End-to-end data flow confirmed from sEMG sensor to FHIR output")

    pdf.sub("Sprint Goal")
    pdf.txt(
        "By end of sprint (M+2): T2 algorithm at >=97.8% suppression (on track for 98% by G1), "
        "MyoBus timestamp alignment and encryption operational. Blockers escalated prior to "
        "Pre-Sub meeting at M+2.")

    pdf.rubric(
        "Full marks: Clear columns with WIP limits and rationale, 6+ cards with team assignment, "
        "Definition of Done for each item (measurable, not vague), sprint goal stated. "
        "Accept Scrum-style sprint backlog as equivalent. Deduct for: no WIP limits, vague DoD "
        "('it works'), or mixing Module B (EIT) work into this sprint (EIT hasn't started yet).")

    # ================================================================
    # EXERCISE 11 -- Module 11: Decision Memo
    # ================================================================
    pdf.ex_title(11, 11, "Conflict Resolution Decision Memo")
    pdf.prompt(
        "The tech team (INP-001) wants 2 extra weeks for ECG-gating optimization. The business "
        "team (INP-002) wants monthly reports starting immediately. As PMP, how do you "
        "resolve the tension between 'more time for quality' and 'investor visibility now'? "
        "Write your decision memo with rationale.")
    pdf.answer_head()

    pdf.sub("DECISION MEMO")
    pdf.txt(
        "Date: M+1 (April 2026)\n"
        "From: PMP\n"
        "To: Tech Lead, Business Lead, Steering Committee\n"
        "Re: INP-001 (Extension Request) and INP-002 (Investor Reports)")

    pdf.sub("Background")
    pdf.txt(
        "INP-001 (Tech): ECG-gating algorithm showing 97.5% suppression vs. 98% target. "
        "Team requests 2 additional weeks for optimization before G1.\n\n"
        "INP-002 (Business): Investor board requests monthly progress reports starting M+3, "
        "with clear KPIs tied to each gate.\n\n"
        "Apparent conflict: Tech wants more time (delays visible progress); Business wants "
        "immediate visibility (creates pressure to report before work is mature).")

    pdf.sub("Analysis: These Are Not Actually in Conflict")
    pdf.txt(
        "The tension is a false dilemma. The 2-week extension pushes T2 completion from ~M+1 to "
        "~M+1.5. G1 is at M+3. There is ~6 weeks of float between T2 completion and G1.\n\n"
        "Monthly investor reports start at M+3 (per INP-002). The 2-week extension resolves long "
        "before the first report is due. In fact, granting the extension IMPROVES the M+3 report "
        "because we can report 98% achievement rather than 97.5%.\n\n"
        "The real question is: is 2 weeks enough to close the 0.5% gap? If not, the issue is not "
        "about time -- it's about technical feasibility.")

    pdf.sub("Decision")
    pdf.txt(
        "1. APPROVED: 2-week extension for T2 optimization.\n"
        "   Condition: Tech team must provide a written plan showing how they will close the\n"
        "   0.5% gap. If no measurable improvement after 2 weeks, we proceed to G1 with 97.5%\n"
        "   and document the gap with a mitigation plan (dual-threshold alarm as control).\n\n"
        "2. APPROVED: Monthly investor reports begin at M+3 as requested.\n"
        "   Format: One-page dashboard summary with traffic-light risk status, cash position,\n"
        "   gate status, and next milestone. KPIs tied directly to gate criteria.\n"
        "   Owner: PMP prepares draft; Business Lead reviews for investor-appropriate language.\n\n"
        "3. IMMEDIATE ACTION: Begin investor report template design now (M+1), so the format\n"
        "   is ready and tested before the M+3 deadline. This gives Business their 'visibility'\n"
        "   deliverable immediately while Tech gets their extension.\n\n"
        "Conflict Mode Used: COLLABORATING (win-win).\n"
        "Both parties get what they need. The extension improves report quality.\n"
        "The report template work starts in parallel, not after.")

    pdf.sub("Risk of This Decision")
    pdf.txt(
        "If the 97.5% -> 98% gap cannot be closed in 2 weeks, we face G1 with a shortfall. "
        "Mitigation: the 97.5% result is within normal optimization range. The dual-threshold "
        "alarm control (RISK-001) provides a safety net. G1 criteria say '>98%' but a PMP ruling "
        "of 'conditional proceed at 97.5% with documented mitigation' is defensible if FDA Pre-Sub "
        "feedback at R2 (M+2) does not flag this as a concern.")

    pdf.rubric(
        "Full marks: Identifies false dilemma, grants both requests with conditions, names specific "
        "conflict resolution mode (Collaborating), includes risk acknowledgment. Key insight: the "
        "requests are NOT mutually exclusive. Deduct for: choosing one side over the other without "
        "exploring integration, missing the timeline analysis (float calculation), or using Competing "
        "or Avoiding modes without strong justification.")

    # ---- Save ----
    out_path = os.path.join(OUT_DIR, "PMP_Course_Answer_Sheet.pdf")
    pdf.output(out_path)
    print(f"Answer Sheet: {out_path}")
    print(f"Pages: {pdf.page_no()}")


if __name__ == "__main__":
    build()
    print("Done.")
