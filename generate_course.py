#!/usr/bin/env python3
"""
Stanford-Style Certificate Course in Project Management
========================================================
Uses the ICU Respiratory Digital Twin System as the central case study.
Generates a comprehensive PDF suitable for a certificate-level program.
"""

import os
from fpdf import FPDF

OUT_DIR = os.path.dirname(os.path.abspath(__file__))

# Color palette
NAVY = (10, 40, 100)
STANFORD = (140, 21, 21)   # Cardinal red
BLUE = (30, 90, 200)
DARK = (25, 25, 30)
TEXT = (40, 40, 45)
GRAY = (120, 120, 130)
LIGHT_BG = (245, 245, 248)
WHITE = (255, 255, 255)
GREEN = (34, 139, 34)
AMBER = (200, 150, 0)
RED = (200, 40, 40)


class CoursePDF(FPDF):

    def header(self):
        if self.page_no() <= 2:
            return
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(*GRAY)
        self.cell(0, 5, "Stanford Certificate in Project Management  |  ICU Digital Twin Case Study", align="L")
        self.ln(8)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(*GRAY)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")

    # ---- Layout helpers ----

    def module_title(self, num, title):
        """Top-level module heading -- full page breaker."""
        self.add_page()
        self.ln(25)
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(*STANFORD)
        self.cell(0, 8, f"MODULE {num}", align="C", new_x="LMARGIN", new_y="NEXT")
        self.set_font("Helvetica", "B", 22)
        self.set_text_color(*NAVY)
        self.cell(0, 12, title, align="C", new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(*STANFORD)
        mid = self.w / 2
        self.line(mid - 40, self.get_y() + 3, mid + 40, self.get_y() + 3)
        self.ln(12)

    def sec(self, title):
        self.ln(3)
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(*NAVY)
        self.cell(0, 8, title, new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(*BLUE)
        self.line(self.l_margin, self.get_y(), self.l_margin + 60, self.get_y())
        self.ln(4)

    def sub(self, title):
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(*DARK)
        self.cell(0, 7, title, new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def txt(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*TEXT)
        self.multi_cell(0, 5.5, text, new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def bul(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*TEXT)
        self.multi_cell(0, 5.5, "  - " + text, new_x="LMARGIN", new_y="NEXT")

    def case_box(self, text):
        """Shaded case-study callout box."""
        self.ln(2)
        x = self.l_margin
        w = self.w - self.l_margin - self.r_margin
        self.set_fill_color(*LIGHT_BG)
        self.set_draw_color(*BLUE)
        y_start = self.get_y()
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*STANFORD)
        self.set_x(x + 3)
        self.cell(0, 5, "CASE STUDY: ICU Respiratory Digital Twin", new_x="LMARGIN", new_y="NEXT")
        self.set_font("Helvetica", "", 9.5)
        self.set_text_color(*DARK)
        self.set_x(x + 3)
        self.multi_cell(w - 6, 5, text, new_x="LMARGIN", new_y="NEXT")
        y_end = self.get_y() + 2
        self.rect(x, y_start - 1, w, y_end - y_start + 2, style="DF")
        # Re-draw text over the rect
        self.set_y(y_start)
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*STANFORD)
        self.set_x(x + 3)
        self.cell(0, 5, "CASE STUDY: ICU Respiratory Digital Twin", new_x="LMARGIN", new_y="NEXT")
        self.set_font("Helvetica", "", 9.5)
        self.set_text_color(*DARK)
        self.set_x(x + 3)
        self.multi_cell(w - 6, 5, text, new_x="LMARGIN", new_y="NEXT")
        self.ln(3)

    def exercise(self, text):
        self.ln(1)
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(*GREEN)
        self.cell(30, 6, "EXERCISE:", new_x="END", new_y="LAST")
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*TEXT)
        self.multi_cell(0, 5.5, text, new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def key_concept(self, text):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(*STANFORD)
        self.cell(0, 6, "KEY CONCEPT: " + text, new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def kv(self, key, val):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(*BLUE)
        self.cell(50, 5.5, key, new_x="END", new_y="LAST")
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*TEXT)
        self.multi_cell(0, 5.5, val, new_x="LMARGIN", new_y="NEXT")


def build():
    pdf = CoursePDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)

    # ================================================================
    # COVER PAGE
    # ================================================================
    pdf.add_page()
    pdf.ln(35)
    pdf.set_font("Helvetica", "B", 32)
    pdf.set_text_color(*STANFORD)
    pdf.cell(0, 14, "Certificate in", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 14, "Project Management", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(6)
    pdf.set_font("Helvetica", "", 14)
    pdf.set_text_color(*NAVY)
    pdf.cell(0, 8, "Stanford School of Engineering  |  Professional Education", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)
    pdf.set_draw_color(*STANFORD)
    mid = pdf.w / 2
    pdf.line(mid - 50, pdf.get_y(), mid + 50, pdf.get_y())
    pdf.ln(10)
    pdf.set_font("Helvetica", "I", 12)
    pdf.set_text_color(*TEXT)
    pdf.cell(0, 7, "Case Study: ICU Respiratory Digital Twin System", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 7, "FDA 510(k) Medical Device Development", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(20)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(*GRAY)
    pdf.cell(0, 6, "12-Module Certificate Program", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 6, "March 2026 Edition", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(30)
    pdf.set_font("Helvetica", "I", 9)
    pdf.cell(0, 5, "This course uses a live medical device project as its primary teaching vehicle.", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 5, "All frameworks taught are universally applicable to any project domain.", align="C", new_x="LMARGIN", new_y="NEXT")

    # ================================================================
    # TABLE OF CONTENTS
    # ================================================================
    pdf.add_page()
    pdf.ln(10)
    pdf.set_font("Helvetica", "B", 20)
    pdf.set_text_color(*NAVY)
    pdf.cell(0, 10, "Table of Contents", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(8)

    toc = [
        ("Module 1", "Foundations of Project Management"),
        ("Module 2", "Project Initiation & the Charter"),
        ("Module 3", "Scope Management & the Work Breakdown Structure"),
        ("Module 4", "Schedule Management & Critical Path"),
        ("Module 5", "Cost Management, Budgeting & Earned Value"),
        ("Module 6", "Risk Management (ISO 14971 & Beyond)"),
        ("Module 7", "Quality Management & Regulatory Compliance"),
        ("Module 8", "Stakeholder & Communications Management"),
        ("Module 9", "Phase-Gate Decision Systems"),
        ("Module 10", "Agile, Hybrid & Adaptive Frameworks"),
        ("Module 11", "Leadership, Teams & Organizational Change"),
        ("Module 12", "Capstone: Integrated Project Simulation"),
        ("", ""),
        ("Appendix A", "Comprehensive Glossary of Terms"),
        ("Appendix B", "Case Study Reference Data"),
    ]
    for mod, title in toc:
        if not mod:
            pdf.ln(3)
            continue
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_text_color(*STANFORD)
        pdf.cell(30, 7, mod, new_x="END", new_y="LAST")
        pdf.set_font("Helvetica", "", 11)
        pdf.set_text_color(*TEXT)
        pdf.cell(0, 7, title, new_x="LMARGIN", new_y="NEXT")

    # ================================================================
    # COURSE INTRODUCTION
    # ================================================================
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 18)
    pdf.set_text_color(*NAVY)
    pdf.cell(0, 10, "Course Introduction", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    pdf.sec("Who This Course Is For")
    pdf.txt(
        "This certificate program is designed for professionals seeking to master the discipline "
        "of project management at a level sufficient to manage any project -- from software "
        "launches to construction programs to FDA-regulated medical devices. No prior PM "
        "certification is required, though familiarity with basic business concepts is assumed.")
    pdf.txt(
        "The course uses a real, active project as its central case study: the ICU Respiratory "
        "Digital Twin System, a dual-module Class II medical device currently pursuing FDA 510(k) "
        "clearance. This project was chosen because it combines almost every dimension of modern "
        "project management: technical complexity, regulatory compliance, risk management, "
        "financial constraints, cross-cultural teams, and multi-stakeholder governance.")

    pdf.sec("Learning Architecture")
    pdf.txt(
        "Each of the 12 modules follows a consistent learning architecture:\n\n"
        "  1. THEORY -- Core PM concepts grounded in PMBOK, ISO 21502, and PRINCE2\n"
        "  2. FRAMEWORK -- Tools and templates you will use in practice\n"
        "  3. CASE APPLICATION -- How the concept applies to the Digital Twin project\n"
        "  4. EXERCISES -- Hands-on assignments to build competence\n"
        "  5. KEY TAKEAWAYS -- Distilled principles for reference\n\n"
        "By the end of Module 12, you will have built a complete project management plan using "
        "the case study, giving you a portfolio-ready artifact and the competence to manage "
        "any project in any domain.")

    pdf.sec("The Case Study: ICU Respiratory Digital Twin System")
    pdf.txt(
        "Product: A non-invasive ICU monitoring platform combining two modules:\n"
        "  Module A: sEMG (surface electromyography) for neural respiratory drive monitoring\n"
        "  Module B: EIT (electrical impedance tomography) for ventilation/perfusion imaging\n\n"
        "Applicant: Company B USA (Global IP Holder)\n"
        "Manufacturer: Silan Technology (Chengdu) Co., Ltd.\n"
        "Regulatory Pathway: 510(k) Modular Approval (pending Pre-Sub confirmation)\n"
        "Timeline: 23 months from M+0 (March 2026) to full platform clearance\n"
        "Budget: $5M total funding target ($2M Phase 1 Seed)\n"
        "Key Standards: IEC 60601-1, ISO 14971, IEC 62304, ISO 13485, 21 CFR 820")
    pdf.txt(
        "This project is ideal for teaching because it features:\n"
        "  - Dual parallel tracks (technical + regulatory)\n"
        "  - Six phase gates with measurable criteria\n"
        "  - Eight active risks rated by ISO 14971\n"
        "  - Twelve regulatory standards to track\n"
        "  - Cross-border manufacturing (US/China structure)\n"
        "  - Constrained funding with milestone-based releases\n"
        "  - Multiple stakeholder groups (FDA, investors, engineering, business)")

    # ================================================================
    # MODULE 1: Foundations
    # ================================================================
    pdf.module_title(1, "Foundations of Project Management")

    pdf.sec("1.1 What Is a Project?")
    pdf.txt(
        "A project is a temporary endeavor undertaken to create a unique product, service, "
        "or result (PMBOK 7th Edition). Every project has four defining characteristics:\n\n"
        "  1. Temporary -- It has a defined beginning and end\n"
        "  2. Unique -- It produces something that did not exist before\n"
        "  3. Progressive elaboration -- Details emerge over time\n"
        "  4. Constrained -- It operates within limits of scope, time, cost, quality, and risk")
    pdf.key_concept("The Triple Constraint (Iron Triangle): Scope, Schedule, Cost -- change one, the others shift.")
    pdf.case_box(
        "The Digital Twin project is temporary (M+0 to M+23), unique (first sEMG+EIT combined "
        "platform), progressively elaborated (predicate device TBD until Pre-Sub meeting at M+2), "
        "and constrained ($5M budget, 23-month timeline, FDA regulatory requirements).")

    pdf.sec("1.2 The Project Life Cycle")
    pdf.txt(
        "All projects pass through phases. The PMBOK identifies five process groups that map "
        "onto these phases:\n\n"
        "  INITIATING -- Define the project, authorize resources, identify stakeholders\n"
        "  PLANNING -- Build the roadmap: scope, schedule, cost, risk, quality, comms\n"
        "  EXECUTING -- Do the work, manage teams, produce deliverables\n"
        "  MONITORING & CONTROLLING -- Track performance vs. plan, manage changes\n"
        "  CLOSING -- Finalize deliverables, release resources, capture lessons learned")
    pdf.case_box(
        "The Digital Twin project is currently at M+0 (Initiating/early Planning). "
        "The Pre-Sub Q-Meeting has been filed (R1 complete), the sEMG prototype is finalized "
        "(T1 complete), and IP transfer is in progress (R8). The project has not yet entered "
        "full Execution -- that begins at M+3 when bench testing starts.")

    pdf.sec("1.3 Predictive vs. Adaptive vs. Hybrid Approaches")
    pdf.txt(
        "Predictive (Waterfall): Requirements are well-defined upfront. Plan the work, work the "
        "plan. Best for construction, manufacturing, and regulated industries.\n\n"
        "Adaptive (Agile): Requirements emerge through iteration. Sprint-based delivery. Best "
        "for software, R&D with high uncertainty.\n\n"
        "Hybrid: Combines both. Regulated industries often use a predictive backbone (gates, "
        "compliance milestones) with agile sprints for technical development.")
    pdf.key_concept("Choose your approach based on requirements stability, stakeholder availability, and risk tolerance.")
    pdf.case_box(
        "The Digital Twin project uses a Hybrid approach: the regulatory track is strictly "
        "predictive (FDA deadlines are non-negotiable), while the technical track uses iterative "
        "development for algorithm validation (ECG-gating at 97.5%, iterating toward 98%).")

    pdf.sec("1.4 The Role of the Project Manager")
    pdf.txt(
        "The project manager (PM) is the single point of accountability for project success. "
        "The PM does not need to be the deepest technical expert -- they need to be the best "
        "integrator. Core PM competencies include:\n\n"
        "  - Technical Project Management (scheduling, budgeting, risk)\n"
        "  - Strategic & Business Management (alignment with organizational goals)\n"
        "  - Leadership (influence, motivation, conflict resolution)\n\n"
        "In this course, we use the title PMP (Project Management Professional) to denote the "
        "lead project manager, who holds overriding decision authority at all gates.")
    pdf.exercise(
        "List 5 decisions in the Digital Twin project that ONLY the PMP should make. "
        "For each, explain why delegating it to a technical lead or business lead would be risky.")

    # ================================================================
    # MODULE 2: Initiation & Charter
    # ================================================================
    pdf.module_title(2, "Project Initiation & the Charter")

    pdf.sec("2.1 The Project Charter")
    pdf.txt(
        "The project charter is the founding document that formally authorizes the project. "
        "It answers six essential questions:\n\n"
        "  1. WHY -- Business case and justification\n"
        "  2. WHAT -- High-level scope and deliverables\n"
        "  3. WHO -- Key stakeholders, sponsor, PM assignment\n"
        "  4. WHEN -- High-level milestones and constraints\n"
        "  5. HOW MUCH -- Preliminary budget and resource needs\n"
        "  6. RISKS -- Major uncertainties that could derail the project")
    pdf.key_concept("No charter = no project. The charter creates the PM's authority to use organizational resources.")
    pdf.case_box(
        "The Digital Twin charter would include:\n"
        "  WHY: $6B respiratory monitoring market, $10K+ per-patient waste from mismanaged ventilation\n"
        "  WHAT: Two FDA-cleared modules (sEMG + EIT) integrated via MyoBus protocol\n"
        "  WHO: PMP (overriding authority), Tech Lead, Regulatory Lead, Business Lead, FDA (external)\n"
        "  WHEN: M+0 to M+23 (March 2026 to February 2028)\n"
        "  HOW MUCH: $5M total ($2M Phase 1 seed, $3M Phase 2 growth)\n"
        "  RISKS: Predicate rejection (RISK-007), funding runway (RISK-008)")

    pdf.sec("2.2 Stakeholder Identification")
    pdf.txt(
        "Stakeholder identification begins at initiation and continues throughout the project. "
        "A stakeholder is any individual or group who can affect or be affected by the project.\n\n"
        "The Stakeholder Register captures:\n"
        "  - Name / Role / Organization\n"
        "  - Interest level (High / Medium / Low)\n"
        "  - Influence level (High / Medium / Low)\n"
        "  - Engagement strategy (Manage Closely, Keep Informed, Monitor, Keep Satisfied)")

    pdf.sub("Stakeholder Power/Interest Grid")
    pdf.txt(
        "        HIGH POWER                          \n"
        "  +-----------------+-----------------+     \n"
        "  | Keep Satisfied  | Manage Closely  |     \n"
        "  | (Investors)     | (FDA, PMP)      |     \n"
        "  +-----------------+-----------------+     \n"
        "  | Monitor         | Keep Informed   |     \n"
        "  | (Competitors)   | (Eng Team)      |     \n"
        "  +-----------------+-----------------+     \n"
        "        LOW POWER                           \n"
        "    LOW INTEREST      HIGH INTEREST         ")
    pdf.case_box(
        "Key stakeholders in the Digital Twin project:\n"
        "  - FDA/CDRH (high power, high interest) -- Manage Closely\n"
        "  - Investors/Board (high power, medium interest) -- Keep Satisfied\n"
        "  - Silan Technology engineering team (low power, high interest) -- Keep Informed\n"
        "  - Competing devices: Getinge NAVA, Timpel (low power, low interest) -- Monitor")

    pdf.sec("2.3 Business Case & Benefits Realization")
    pdf.txt(
        "The business case justifies the investment by quantifying expected benefits against costs. "
        "It includes:\n\n"
        "  - Net Present Value (NPV) of expected revenue\n"
        "  - Return on Investment (ROI)\n"
        "  - Payback period\n"
        "  - Strategic alignment with company mission\n"
        "  - Opportunity cost of NOT doing the project")
    pdf.case_box(
        "The Digital Twin business case: $6B total addressable market, device ASP in the Timpel "
        "benchmark range ($20-40M acquisition value for comparable companies). $5M investment "
        "with potential 4-8x return through strategic acquisition by Drager, Getinge, or Mindray.")
    pdf.exercise(
        "Draft a one-page project charter for the Digital Twin project. Include all six elements. "
        "Your charter should be specific enough that a new PM could pick up the project from it.")

    # ================================================================
    # MODULE 3: Scope Management & WBS
    # ================================================================
    pdf.module_title(3, "Scope Management & the Work Breakdown Structure")

    pdf.sec("3.1 Defining Scope")
    pdf.txt(
        "Scope management ensures the project includes all the work required -- and only the work "
        "required -- to complete the project successfully. Scope has two dimensions:\n\n"
        "  Product Scope: The features and functions of the deliverable\n"
        "  Project Scope: The work needed to deliver the product scope\n\n"
        "The Scope Statement documents: deliverables, acceptance criteria, exclusions, constraints, "
        "and assumptions.")
    pdf.key_concept("Scope creep is the #1 killer of projects. Every addition must go through formal change control.")
    pdf.case_box(
        "Product Scope: sEMG module (IKN product code) + EIT module (DQS product code) integrated "
        "via MyoBus protocol.\n"
        "Project Scope: All work from M+0 to M+23 including prototyping, testing, FDA submissions, "
        "IP transfer, manufacturing scale-up, and commercial launch.\n"
        "Exclusions: Clinical trials (device is 510(k) not PMA), international regulatory filings "
        "(EU MDR, China NMPA), post-market surveillance system.")

    pdf.sec("3.2 The Work Breakdown Structure (WBS)")
    pdf.txt(
        "The WBS is a hierarchical decomposition of the total scope into manageable work packages. "
        "It is the foundation for ALL downstream planning -- schedule, cost, risk, and resources "
        "all derive from the WBS.\n\n"
        "Rules for a good WBS:\n"
        "  1. 100% Rule -- The WBS must capture 100% of the project scope\n"
        "  2. Mutually exclusive -- No overlap between work packages\n"
        "  3. Deliverable-oriented -- Decompose by deliverables, not activities\n"
        "  4. 8/80 Rule -- Work packages should be 8-80 hours of effort")

    pdf.sub("WBS for the Digital Twin Project (Level 2)")
    pdf.txt(
        "1.0  ICU Respiratory Digital Twin System\n"
        "  1.1  Project Management\n"
        "    1.1.1  Charter & Kickoff\n"
        "    1.1.2  Gate Reviews (G1-G6)\n"
        "    1.1.3  Stakeholder Communications\n"
        "    1.1.4  Change Control\n"
        "  1.2  Module A -- sEMG\n"
        "    1.2.1  Prototype Finalization (T1)\n"
        "    1.2.2  Algorithm Validation (T2)\n"
        "    1.2.3  Bench & Performance Testing (T3)\n"
        "    1.2.4  510(k) Submission (R3)\n"
        "  1.3  Module B -- EIT\n"
        "    1.3.1  32-Electrode Belt Prototype (T5)\n"
        "    1.3.2  V/Q Algorithm Validation (T6)\n"
        "    1.3.3  Biocompatibility Testing (T7)\n"
        "    1.3.4  510(k) Submission (R6)\n"
        "  1.4  MyoBus Integration (T8)\n"
        "  1.5  Regulatory & Compliance\n"
        "    1.5.1  Pre-Sub Meeting (R2)\n"
        "    1.5.2  ISO 13485 Audit (R9)\n"
        "    1.5.3  Standards Compliance (12 standards)\n"
        "  1.6  Business Operations\n"
        "    1.6.1  IP Buyout & Legal (R8)\n"
        "    1.6.2  Funding Rounds (FR-001 to FR-004)\n"
        "    1.6.3  Commercial Launch Prep")
    pdf.exercise(
        "Decompose WBS item 1.2.3 (Bench & Performance Testing) to Level 4. "
        "Identify at least 6 work packages using the IEC 60601-1 test categories as a guide.")

    # ================================================================
    # MODULE 4: Schedule Management
    # ================================================================
    pdf.module_title(4, "Schedule Management & Critical Path")

    pdf.sec("4.1 Activity Sequencing")
    pdf.txt(
        "Once the WBS identifies work packages, Schedule Management sequences them into a timeline. "
        "The key tools are:\n\n"
        "  Precedence Diagramming Method (PDM) -- Activities connected by dependencies:\n"
        "    FS (Finish-to-Start): B cannot start until A finishes [most common]\n"
        "    SS (Start-to-Start): B starts when A starts\n"
        "    FF (Finish-to-Finish): B finishes when A finishes\n"
        "    SF (Start-to-Finish): B finishes when A starts [rare]\n\n"
        "  Lead: An acceleration of the successor (overlap)\n"
        "  Lag: A delay between predecessor and successor")
    pdf.case_box(
        "Critical dependencies in the Digital Twin project:\n"
        "  - R2 (Pre-Sub Meeting, M+2) must finish before R3 (510(k) submission) can start (FS)\n"
        "  - T1 (Prototype) must finish before T3 (Bench Testing) can start (FS)\n"
        "  - T2 (ECG-Gating) and T8 (MyoBus) run in parallel (SS with T1)\n"
        "  - R4 (sEMG Clearance, M+9) must finish before G4 (Commercial Launch) can pass (FS)\n"
        "  - T5 (EIT Prototype) and T6 (V/Q Algorithm) can overlap (SS + 4 month lag)")

    pdf.sec("4.2 The Critical Path Method (CPM)")
    pdf.txt(
        "The Critical Path is the longest path through the project network. It determines the "
        "minimum project duration. Activities on the critical path have ZERO float -- any delay "
        "to a critical path activity delays the entire project.\n\n"
        "Float (Slack) = Late Start - Early Start\n\n"
        "To find the critical path:\n"
        "  1. Forward Pass -- Calculate Early Start (ES) and Early Finish (EF) for every activity\n"
        "  2. Backward Pass -- Calculate Late Finish (LF) and Late Start (LS) from the end\n"
        "  3. Float = LS - ES (or LF - EF)\n"
        "  4. Activities with Float = 0 are on the critical path")
    pdf.key_concept("Manage the critical path obsessively. Non-critical activities have float; critical ones do not.")

    pdf.sub("Digital Twin Critical Path (simplified)")
    pdf.txt(
        "T1(M+0) -> T3(M+3) -> R3(M+6) -> R4(M+9) -> R5(M+12) -> T6(M+12) -> R6(M+17) -> R7(M+23)\n\n"
        "Total critical path duration: 23 months\n"
        "Float on T2 (ECG-Gating): 2 months (starts M+1, needed by M+3)\n"
        "Float on T8 (MyoBus): Can lag up to T5 completion at M+8\n\n"
        "The regulatory submissions (R3, R6) are hard deadlines -- FDA review periods "
        "are external constraints that cannot be crashed.")

    pdf.sec("4.3 Schedule Compression")
    pdf.txt(
        "When the schedule is too long, two compression techniques apply:\n\n"
        "  Crashing: Add resources to critical-path activities to shorten duration. "
        "Increases cost. Only works if the activity is resource-constrained.\n\n"
        "  Fast-Tracking: Overlap activities that were planned sequentially. "
        "Increases risk. Only works if overlapping is technically feasible.")
    pdf.case_box(
        "The Digital Twin uses fast-tracking: Module B development (EIT prototype at M+8) "
        "begins while Module A is still in FDA review (R3 submitted at M+6, clearance at M+9). "
        "This saves ~8 months vs. a purely sequential approach but increases the risk that "
        "FDA feedback on Module A could force rework on Module B's approach.")
    pdf.exercise(
        "Draw the network diagram for the Digital Twin project using the 8 technical milestones "
        "(T1-T8) and 9 regulatory milestones (R1-R9). Identify which activities have float "
        "and calculate the total float for each.")

    # ================================================================
    # MODULE 5: Cost Management
    # ================================================================
    pdf.module_title(5, "Cost Management, Budgeting & Earned Value")

    pdf.sec("5.1 Estimating Costs")
    pdf.txt(
        "Cost estimation techniques (from least to most accurate):\n\n"
        "  Analogous: Use costs from similar past projects. Quick but rough. (-25% to +75%)\n"
        "  Parametric: Statistical models (e.g., cost per test = $X times number of tests)\n"
        "  Bottom-Up: Estimate each work package individually and roll up. Most accurate.\n"
        "  Three-Point: (Optimistic + 4*Most Likely + Pessimistic) / 6  [PERT formula]")

    pdf.sec("5.2 The Project Budget")
    pdf.txt(
        "The budget is built bottom-up from cost estimates plus reserves:\n\n"
        "  Work Package Estimates (from WBS)\n"
        "  + Contingency Reserve (known risks -- managed by PM)\n"
        "  + Management Reserve (unknown risks -- controlled by sponsor)\n"
        "  = Total Project Budget (Cost Baseline + Management Reserve)\n\n"
        "The Cost Baseline is the approved, time-phased budget against which Earned Value "
        "is measured. It cannot change without formal change control.")
    pdf.case_box(
        "Digital Twin budget structure (from PPT Slide 15):\n"
        "  40% -- IP Buyout ($2.0M): Transfer patents, software, MyoBus to US entity\n"
        "  30% -- FDA/Regulatory ($1.5M): Testing, submissions, consultants\n"
        "  20% -- US Operations ($1.0M): R&D center, quality system, staffing\n"
        "  10% -- Supply Chain ($0.5M): Manufacturing setup at Silan\n"
        "  Total: $5.0M  |  Phase 1 Seed: $2.0M  |  Phase 2: $3.0M\n"
        "  Monthly burn rate: $45,000  |  Current cash on hand: $320,000  |  Runway: ~7 months")

    pdf.sec("5.3 Earned Value Management (EVM)")
    pdf.txt(
        "EVM is the gold standard for integrated scope-schedule-cost performance measurement. "
        "Three base measurements:\n\n"
        "  PV (Planned Value): What SHOULD have been done by now (budgeted cost of planned work)\n"
        "  EV (Earned Value): What HAS been done (budgeted cost of work performed)\n"
        "  AC (Actual Cost): What it ACTUALLY cost (actual cost of work performed)\n\n"
        "Key formulas:\n"
        "  SV  = EV - PV         (Schedule Variance; positive = ahead)\n"
        "  CV  = EV - AC         (Cost Variance; positive = under budget)\n"
        "  SPI = EV / PV         (Schedule Performance Index; >1 = ahead)\n"
        "  CPI = EV / AC         (Cost Performance Index; >1 = under budget)\n"
        "  EAC = BAC / CPI       (Estimate at Completion -- if trend continues)\n"
        "  ETC = EAC - AC        (Estimate to Complete)\n"
        "  TCPI = (BAC - EV) / (BAC - AC)  (To-Complete Performance Index)")
    pdf.key_concept("EVM tells you the truth. A project can be on schedule but over budget, or under budget but behind schedule. EVM reveals both.")
    pdf.exercise(
        "At M+3, the Digital Twin has completed T1 (budgeted $80K, actual $75K), T2 (budgeted "
        "$60K, actual $72K), and R1 (budgeted $15K, actual $12K). T3 is 20% complete (budgeted "
        "$120K, actual spend to date $30K). Calculate PV, EV, AC, SV, CV, SPI, and CPI.")

    # ================================================================
    # MODULE 6: Risk Management
    # ================================================================
    pdf.module_title(6, "Risk Management (ISO 14971 & Beyond)")

    pdf.sec("6.1 Risk Management Framework")
    pdf.txt(
        "Risk is an uncertain event or condition that, if it occurs, has a positive or negative "
        "effect on project objectives. Risk management follows a continuous cycle:\n\n"
        "  1. IDENTIFY -- Brainstorm, checklists, expert interviews, SWOT analysis\n"
        "  2. ANALYZE (Qualitative) -- Probability x Impact matrix, risk rating\n"
        "  3. ANALYZE (Quantitative) -- Monte Carlo simulation, decision trees, EMV\n"
        "  4. PLAN RESPONSES -- Avoid, Mitigate, Transfer, Accept (negative risks)\n"
        "                       Exploit, Enhance, Share, Accept (positive risks)\n"
        "  5. IMPLEMENT -- Execute the response strategies\n"
        "  6. MONITOR -- Track triggers, update register, report to stakeholders")

    pdf.sec("6.2 Probability-Impact Matrix")
    pdf.txt(
        "The P-I Matrix maps risks onto a grid:\n\n"
        "  Impact:   Very Low | Low | Medium | High | Very High\n"
        "  Prob:     Very Low | Low | Medium | High | Very High\n\n"
        "  Risk Level = f(Probability, Impact)\n"
        "    Green: Acceptable -- monitor\n"
        "    Yellow: Elevated -- active mitigation plan required\n"
        "    Red: Critical -- escalate to sponsor, aggressive mitigation")

    pdf.sub("Digital Twin Risk Register (from ISO 14971)")
    pdf.txt(
        "RISK-001 [Yellow] False-negative sEMG signal\n"
        "  Severity: High | Probability: Low\n"
        "  Controls: Dual-threshold algorithm + alarm; labeled as adjunct\n\n"
        "RISK-004 [Red] V/Q image misinterpretation -> wrong ventilator setting\n"
        "  Severity: High | Probability: Low\n"
        "  Controls: Labeled 'investigational adjunct'; mandated clinical training\n\n"
        "RISK-007 [Red] 510(k) rejection -- predicate device not accepted\n"
        "  Severity: High | Probability: Medium\n"
        "  Controls: Pre-Sub strategy; K numbers must be verified before Q-Sub;\n"
        "  De Novo pathway as contingency (+~60 days); modular submission\n\n"
        "RISK-008 [Red] Funding runway insufficient before M+9 clearance\n"
        "  Severity: High | Probability: Medium\n"
        "  Controls: Phased milestone funding; sEMG-first for earlier revenue")

    pdf.sec("6.3 ISO 14971: Risk Management for Medical Devices")
    pdf.txt(
        "ISO 14971:2019 is the international standard for risk management specific to medical "
        "devices. It requires:\n\n"
        "  - Risk Management Plan (scope, roles, acceptance criteria)\n"
        "  - Hazard Identification (intended use, foreseeable misuse)\n"
        "  - Risk Estimation (severity + probability for each hazard)\n"
        "  - Risk Evaluation (is residual risk acceptable?)\n"
        "  - Risk Control (design changes, protective measures, labeling)\n"
        "  - Residual Risk Assessment (overall residual risk acceptable?)\n"
        "  - Risk Management Report (compiled throughout device lifecycle)\n\n"
        "ISO 14971 differs from PMBOK risk management in one critical way: medical device risks "
        "focus on PATIENT HARM, not project schedule or budget. A project manager in medtech "
        "must manage both types simultaneously.")
    pdf.key_concept("In regulated industries, risk management is not optional -- it is a legal requirement.")
    pdf.exercise(
        "RISK-007 (predicate rejection) has medium probability because the Timpel predicate K "
        "number has not been verified. Draft a Risk Response Plan with specific actions, owners, "
        "triggers, and a De Novo contingency timeline showing the +60 day impact on the schedule.")

    # ================================================================
    # MODULE 7: Quality & Regulatory
    # ================================================================
    pdf.module_title(7, "Quality Management & Regulatory Compliance")

    pdf.sec("7.1 Quality Management Principles")
    pdf.txt(
        "Quality has two dimensions:\n\n"
        "  Grade: Category of characteristics (e.g., a basic vs. premium electrode belt)\n"
        "  Quality: Degree to which requirements are fulfilled (zero defects ideal)\n\n"
        "Low quality is always a problem. Low grade may be acceptable (intentional trade-off).\n\n"
        "Core quality tools:\n"
        "  - Cost of Quality (COQ): Prevention + Appraisal + Internal Failure + External Failure\n"
        "  - Plan-Do-Check-Act (PDCA): Deming cycle for continuous improvement\n"
        "  - Statistical Process Control: Control charts, capability indices\n"
        "  - Root Cause Analysis: 5 Whys, Ishikawa (fishbone) diagrams")

    pdf.sec("7.2 Regulatory Compliance as a Quality System")
    pdf.txt(
        "In medical devices, quality is not aspirational -- it is legally mandated. "
        "The two foundational systems are:\n\n"
        "  ISO 13485:2016 -- Quality Management System for Medical Devices\n"
        "    - Design controls (design input, output, verification, validation, transfer)\n"
        "    - Document control, CAPA, management review\n"
        "    - Required for CE marking, often expected by FDA\n\n"
        "  21 CFR Part 820 -- FDA Quality System Regulation (QSR)\n"
        "    - US-specific requirements overlapping with ISO 13485\n"
        "    - Design History File (DHF), Device Master Record (DMR)\n"
        "    - Production and process controls, corrective/preventive action")

    pdf.sub("Regulatory Standards Tracked in the Digital Twin Project")
    pdf.txt(
        "  STD-01: IEC 60601-1 -- Medical Electrical Equipment Safety (30% complete)\n"
        "  STD-02: IEC 60601-1-2 -- EMC (0%)\n"
        "  STD-03: IEC 60601-1-6 -- Usability Engineering (0%)\n"
        "  STD-04: ISO 14971 -- Risk Management (45%)\n"
        "  STD-05: ISO 10993-1 -- Biocompatibility Framework (0%)\n"
        "  STD-06: ISO 10993-5 -- Cytotoxicity (0%)\n"
        "  STD-07: ISO 10993-10 -- Sensitization & Irritation (0%)\n"
        "  STD-08: FDA Cybersecurity 2023 (25%)\n"
        "  STD-09: 21 CFR Part 820 -- QSR (40%)\n"
        "  STD-10: 21 CFR Part 11 -- Electronic Records (0%)\n"
        "  STD-11: IEC 62304 -- Software Lifecycle (20%)\n"
        "  STD-12: ISO 13485 -- QMS at Silan Manufacturing (60%)")
    pdf.case_box(
        "The Digital Twin must comply with 12 regulatory standards before FDA submission. "
        "The PM tracks each standard's completion percentage, assigns module applicability, "
        "and ensures gap remediation is complete before each gate. At G3 (M+6), all standards "
        "applicable to sEMG must be at 100%. At G5 (M+17), all EIT standards must be complete.")
    pdf.exercise(
        "Create a compliance traceability matrix mapping each of the 12 standards to specific "
        "WBS work packages. For each standard, identify the gate at which it must be complete.")

    # ================================================================
    # MODULE 8: Stakeholder & Communications
    # ================================================================
    pdf.module_title(8, "Stakeholder & Communications Management")

    pdf.sec("8.1 The Communications Model")
    pdf.txt(
        "Communication is the PM's most important skill. Research consistently shows PMs spend "
        "75-90% of their time communicating. The communications model includes:\n\n"
        "  Sender -> Encode -> Message -> Medium -> Decode -> Receiver -> Feedback\n\n"
        "  Noise can enter at any stage. The PM's job is to minimize noise through:\n"
        "  - Clear messaging (encode precisely)\n"
        "  - Right medium (email for record, meeting for discussion, dashboard for status)\n"
        "  - Active listening (decode and confirm understanding)\n"
        "  - Feedback loops (two-way communication)")

    pdf.sec("8.2 Communications Management Plan")
    pdf.txt(
        "The plan defines: what information, who needs it, when, in what format, and thru which "
        "channel. For each stakeholder group:\n\n"
        "  FDA/CDRH: Formal written submissions only. No informal communication.\n"
        "  Investor Board: Monthly reports from M+3, tied to gate KPIs (per INP-002).\n"
        "  Engineering Team: Weekly standups, milestone-by-milestone dashboards.\n"
        "  PMP: Real-time dashboard (the Control Tower) with all data streams.\n"
        "  Business Team: Biweekly business impact translations of technical events.")

    pdf.sec("8.3 Translating Technical into Business Language")
    pdf.txt(
        "One of the most critical PM skills is translating between audiences. A technical "
        "milestone means nothing to an investor unless you translate it into business impact:\n\n"
        "  Technical: '510(k) sEMG submitted to FDA at M+6'\n"
        "  Business: 'Submission milestone hit -- investor confidence checkpoint (CRITICAL)'\n\n"
        "  Technical: 'sEMG 510(k) clearance expected at M+9'\n"
        "  Business: 'Module A revenue-ready -- funding runway extended'\n\n"
        "  Technical: 'EIT testing & validation begins at M+12'\n"
        "  Business: 'Second major investment tranche needed (WARNING)'")
    pdf.case_box(
        "The Digital Twin dashboard includes a full Translation Timeline that pairs every "
        "technical event with its business-language equivalent and impact rating (Critical, "
        "Warning, Neutral). This is a best practice any PM should replicate: every technical "
        "milestone should have a pre-written business translation ready for stakeholder reports.")
    pdf.exercise(
        "Write a one-page investor update for Month 3, using only information from the "
        "case study data. Include: progress vs plan, risk status (traffic lights), "
        "cash position, and the next milestone to watch.")

    # ================================================================
    # MODULE 9: Phase-Gate Decision Systems
    # ================================================================
    pdf.module_title(9, "Phase-Gate Decision Systems")

    pdf.sec("9.1 What Is a Phase-Gate System?")
    pdf.txt(
        "A Phase-Gate (Stage-Gate) system divides the project into phases separated by decision "
        "checkpoints called gates. At each gate, the project is evaluated against predefined "
        "criteria, and a go/no-go decision is made.\n\n"
        "Gate decisions are typically:\n"
        "  - PROCEED (green) -- All criteria met, move to next phase\n"
        "  - CONDITIONAL PROCEED (yellow) -- Minor gaps, proceed with remediation plan\n"
        "  - HOLD (amber) -- Significant gaps, pause and resolve before re-evaluation\n"
        "  - STOP (red) -- Fatal gaps, terminate or fundamentally restructure\n\n"
        "The gate review is NOT a status update -- it is a DECISION MEETING. "
        "The PMP has final decision authority.")
    pdf.key_concept("Gates prevent sunk-cost fallacy. They create structured moments to kill or pivot a project.")

    pdf.sec("9.2 Designing Gate Criteria")
    pdf.txt(
        "Effective gate criteria are:\n"
        "  - Measurable: Binary yes/no or quantitative threshold\n"
        "  - Traceable: Linked to a specific deliverable or test result\n"
        "  - Non-negotiable: The minimum bar, not aspirational targets\n"
        "  - Pre-agreed: Defined at project initiation, not at the gate review")

    pdf.sub("The Six Gates of the Digital Twin Project")
    pdf.txt(
        "G1 (M+3) sEMG Design Verification Complete\n"
        "  - ECG-gating suppression >98%\n"
        "  - IEC 60601-1 bench testing passed\n"
        "  - sEMG sensitivity >= 92% confirmed\n"
        "  - EMC compliance verified\n\n"
        "G2 (M+2) Pre-Sub FDA Feedback Received\n"
        "  - FDA written feedback received\n"
        "  - Predicate device strategy accepted\n"
        "  - Testing protocol approved\n"
        "  - Software classification confirmed (Class C / IEC 62304 Class B)\n\n"
        "G3 (M+6) 510(k) sEMG Submission Ready\n"
        "  - All 15 submission sections complete\n"
        "  - Risk analysis (ISO 14971) finalized\n"
        "  - Clinical evidence dossier compiled\n"
        "  - Labeling & IFU reviewed (21 CFR 801)\n"
        "  - Quality system audit passed\n\n"
        "G4 (M+9) sEMG Module Commercial Launch\n"
        "  - 510(k) clearance received (IKN product code)\n"
        "  - Manufacturing scaled -- Silan production ready\n"
        "  - Funding secured for commercial operations\n\n"
        "G5 (M+17) EIT 510(k) Submission Ready\n"
        "  - V/Q algorithm validated (>85% vs DCE-CT)\n"
        "  - EIT biocompatibility testing complete\n"
        "  - Timpel predicate comparison documented (K number TBD)\n"
        "  - EIT-specific EMC testing passed\n\n"
        "G6 (M+23) Full Platform Launch -- FDA Cleared\n"
        "  - EIT 510(k) clearance (DQS product code)\n"
        "  - MyoBus integrated platform validated\n"
        "  - Commercial deployment plan finalized")
    pdf.exercise(
        "Gate G2 is at M+2 (May 2026). The FDA has not yet sent written feedback. "
        "As PMP, draft the gate review agenda, list the data you would present, "
        "and describe what decision options you would present to the steering committee. "
        "What is your recommended decision if only 2 of 4 criteria are met?")

    # ================================================================
    # MODULE 10: Agile & Hybrid
    # ================================================================
    pdf.module_title(10, "Agile, Hybrid & Adaptive Frameworks")

    pdf.sec("10.1 The Agile Manifesto & Principles")
    pdf.txt(
        "The Agile Manifesto (2001) prioritizes:\n"
        "  - Individuals and interactions over processes and tools\n"
        "  - Working software over comprehensive documentation\n"
        "  - Customer collaboration over contract negotiation\n"
        "  - Responding to change over following a plan\n\n"
        "Key Agile frameworks:\n"
        "  Scrum: Sprints (1-4 weeks), Product Owner, Scrum Master, Daily Standup\n"
        "  Kanban: Continuous flow, WIP limits, visual board\n"
        "  SAFe: Scaled Agile for enterprises (Release Trains, PI Planning)\n"
        "  XP: Pair programming, TDD, continuous integration")

    pdf.sec("10.2 When Agile Works (and When It Doesn't)")
    pdf.txt(
        "Agile works best when:\n"
        "  - Requirements are uncertain or rapidly evolving\n"
        "  - Stakeholders are available for frequent feedback\n"
        "  - The team is co-located or highly collaborative\n"
        "  - Incremental delivery provides value\n\n"
        "Agile struggles when:\n"
        "  - Regulatory requirements demand extensive upfront documentation\n"
        "  - External dependencies have fixed timelines (e.g., FDA review periods)\n"
        "  - Contracts are fixed-price/fixed-scope\n"
        "  - Safety-critical systems require formal verification")

    pdf.sec("10.3 The Hybrid Model: Best of Both Worlds")
    pdf.txt(
        "Most real-world projects use a hybrid approach that combines:\n\n"
        "  Predictive backbone: Fixed milestones, gates, regulatory deadlines\n"
        "  Agile execution: Iterative development within each phase\n\n"
        "The key is knowing which elements are fixed (non-negotiable gates) and which are "
        "flexible (how the team gets from one gate to the next).")
    pdf.case_box(
        "The Digital Twin project is inherently hybrid:\n"
        "  PREDICTIVE: Regulatory milestones (R1-R9) and gates (G1-G6) are fixed. FDA "
        "  review periods are external constraints. Submission documents must be comprehensive.\n"
        "  AGILE: Algorithm development (T2 ECG-gating, T6 V/Q validation) uses iterative "
        "  testing. The team at Silan runs 2-week development sprints for software. "
        "  INP-001 shows the team requesting 2 extra weeks for optimization -- classic "
        "  agile adaptation within a predictive gate structure.")
    pdf.exercise(
        "Design a sprint board (Kanban) for the two-week period between M+1 and M+2, "
        "when T2 (ECG-Gating) and T8 (MyoBus) are both in progress. Define columns, "
        "WIP limits, and the Definition of Done for each work item.")

    # ================================================================
    # MODULE 11: Leadership & Teams
    # ================================================================
    pdf.module_title(11, "Leadership, Teams & Organizational Change")

    pdf.sec("11.1 Leadership vs. Management")
    pdf.txt(
        "Management is about doing things right. Leadership is about doing the right things.\n\n"
        "  Management: Planning, organizing, staffing, controlling\n"
        "  Leadership: Vision, motivation, influence, conflict resolution\n\n"
        "The PM must be both. The PMBOK 7th Edition emphasizes 'servant leadership' -- "
        "the PM serves the team by removing impediments, not by commanding.")

    pdf.sec("11.2 Team Development Stages")
    pdf.txt(
        "Tuckman's Model:\n\n"
        "  FORMING -- Team assembles, roles unclear, polite and cautious\n"
        "  STORMING -- Conflicts emerge, power struggles, disagreements on approach\n"
        "  NORMING -- Conflicts resolve, norms established, trust builds\n"
        "  PERFORMING -- Team is self-directing, high productivity, psychological safety\n"
        "  ADJOURNING -- Project ends, team disbands, lessons captured")
    pdf.case_box(
        "The Digital Twin team spans two countries (US and China), two languages, and "
        "multiple disciplines (engineering, regulatory, business, legal). The cross-cultural "
        "dimension amplifies Storming. The PM must actively manage:\n"
        "  - Time zone differences (US/China ~13-16 hours)\n"
        "  - Language barriers (bilingual dashboard was built for this reason)\n"
        "  - Cultural norms around conflict expression and hierarchy\n"
        "  - Legal entity boundaries (Company B USA vs Silan Technology)")

    pdf.sec("11.3 Conflict Resolution")
    pdf.txt(
        "Thomas-Kilmann Conflict Modes:\n\n"
        "  Competing (win-lose): Assertive, uncooperative. Use for emergencies.\n"
        "  Collaborating (win-win): Assertive, cooperative. Best for important issues.\n"
        "  Compromising (split): Moderate assertiveness, moderate cooperation.\n"
        "  Avoiding (withdraw): Unassertive, uncooperative. Use for trivial issues.\n"
        "  Accommodating (yield): Unassertive, cooperative. Use to preserve relationships.\n\n"
        "The PM's default should be COLLABORATING. Most project conflicts have solutions "
        "that satisfy both parties if the PM invests time in understanding interests (not positions).")
    pdf.exercise(
        "The tech team (INP-001) wants 2 extra weeks for ECG-gating optimization. The business "
        "team (INP-002) wants monthly reports starting immediately. As PMP, how do you "
        "resolve the tension between 'more time for quality' and 'investor visibility now'? "
        "Write your decision memo with rationale.")

    # ================================================================
    # MODULE 12: Capstone
    # ================================================================
    pdf.module_title(12, "Capstone: Integrated Project Simulation")

    pdf.sec("12.1 The Capstone Challenge")
    pdf.txt(
        "You have been appointed PMP for the ICU Respiratory Digital Twin System effective M+0. "
        "Using everything you have learned in Modules 1-11, produce the following deliverables:\n\n"
        "  1. PROJECT CHARTER (1-2 pages)\n"
        "     - Business case, scope, stakeholders, budget, top 5 risks\n\n"
        "  2. WORK BREAKDOWN STRUCTURE (to Level 3)\n"
        "     - Covering all deliverables from M+0 to M+23\n\n"
        "  3. NETWORK DIAGRAM with Critical Path\n"
        "     - Show dependencies, float, and the critical path\n\n"
        "  4. RISK REGISTER (minimum 8 risks)\n"
        "     - Using ISO 14971 format: Hazard, Severity, Probability, Controls, Residual\n\n"
        "  5. COMMUNICATIONS PLAN\n"
        "     - One page mapping stakeholders to communication frequency/format\n\n"
        "  6. GATE REVIEW PACKAGE for G1 (M+3)\n"
        "     - Pre-populate with the criteria, mock decision recommendation\n\n"
        "  7. EARNED VALUE REPORT at M+6\n"
        "     - Using hypothetical progress data, calculate all EVM metrics\n\n"
        "  8. LESSONS LEARNED REPORT\n"
        "     - 5 lessons from the project so far, with recommendations for future projects")

    pdf.sec("12.2 Evaluation Criteria")
    pdf.txt(
        "Each deliverable is scored on:\n"
        "  - Completeness (all required elements present)\n"
        "  - Accuracy (numbers check out, dependencies are logical)\n"
        "  - Professionalism (clear, concise, presentation-ready)\n"
        "  - Judgment (decisions show PM thinking, not just data compilation)\n\n"
        "A passing score requires 75% or higher on each deliverable. "
        "The capstone constitutes 40% of the certificate grade.")

    pdf.sec("12.3 After This Course")
    pdf.txt(
        "Upon completing this certificate, you should be able to:\n\n"
        "  1. Initiate any project with a proper charter and stakeholder register\n"
        "  2. Build a WBS that captures 100% of scope\n"
        "  3. Create a network diagram and identify the critical path\n"
        "  4. Estimate costs and build a time-phased budget\n"
        "  5. Manage risks using both PMBOK and ISO 14971 frameworks\n"
        "  6. Design and run a phase-gate decision system\n"
        "  7. Track performance using Earned Value Management\n"
        "  8. Communicate effectively with all stakeholder groups\n"
        "  9. Lead cross-functional, cross-cultural teams\n"
        "  10. Choose the right methodology (predictive, agile, hybrid) for any project\n\n"
        "These skills are transferable to ANY project domain -- software, construction, "
        "pharma, aerospace, consumer products, or government programs. "
        "The principles are universal; only the domain vocabulary changes.")

    # ================================================================
    # APPENDIX A: GLOSSARY
    # ================================================================
    pdf.module_title("A", "Comprehensive Glossary of Terms")

    glossary = [
        ("AC (Actual Cost)", "The total cost actually incurred for work performed during a specific time period."),
        ("Acceptance Criteria", "Measurable conditions that must be met for deliverables to be accepted by stakeholders."),
        ("Adaptive (Agile)", "An iterative project approach where requirements and solutions evolve through collaboration."),
        ("ALARP", "As Low As Reasonably Practicable -- a risk acceptance threshold used in safety-critical industries."),
        ("Assumption", "A factor considered true for planning purposes without proof. Must be documented and validated."),
        ("BAC (Budget at Completion)", "The total planned budget for the project (the sum of all PV)."),
        ("Baseline", "An approved version of the scope, schedule, or cost plan used as a reference for measurement."),
        ("Bench Testing", "Laboratory testing of a device against technical specifications before clinical use."),
        ("Biocompatibility", "The ability of a material to perform without causing harmful biological responses (ISO 10993)."),
        ("Burn Rate", "The rate at which a company spends capital (typically expressed as monthly cash outflow)."),
        ("CAPA", "Corrective and Preventive Action -- a quality system process required by FDA and ISO 13485."),
        ("CDRH", "Center for Devices and Radiological Health -- the FDA division that regulates medical devices."),
        ("Change Control", "A formal process for evaluating, approving, and tracking changes to project baselines."),
        ("Charter", "The formal document that authorizes a project and grants the PM authority to allocate resources."),
        ("Class II Device", "FDA classification for medium-risk devices, typically cleared via 510(k) or De Novo."),
        ("Constraint", "A limiting factor (time, cost, scope, quality, risk, resources) that restricts project options."),
        ("Contingency Reserve", "Budget or schedule buffer for identified (known) risks, managed by the PM."),
        ("Cost Baseline", "The approved time-phased budget used to measure cost performance (excludes management reserve)."),
        ("CPI (Cost Performance Index)", "EV / AC. Measures cost efficiency. >1 = under budget. <1 = over budget."),
        ("Crashing", "Schedule compression by adding resources to critical-path activities (increases cost)."),
        ("Critical Path", "The longest sequence of dependent activities that determines the minimum project duration."),
        ("CTPA", "CT Pulmonary Angiography -- a gold-standard clinical imaging reference for perfusion measurement."),
        ("CV (Cost Variance)", "EV - AC. Positive = under budget. Negative = over budget."),
        ("De Novo", "FDA pathway for novel devices without a predicate. More rigorous than 510(k), less than PMA."),
        ("Decision Tree", "A quantitative risk analysis tool modeling sequential decisions and chance events."),
        ("Deliverable", "A tangible or intangible output produced as part of the project."),
        ("Design Controls", "FDA-required systematic processes for device design: input, output, review, verification, validation."),
        ("Design History File (DHF)", "A compilation of records describing the design history of a finished medical device."),
        ("Device Master Record (DMR)", "The complete set of documents specifying how to manufacture a medical device."),
        ("DQS", "FDA product code for electrical impedance tomography thoracic imaging devices."),
        ("Dual-Track", "A project structure running two parallel workstreams (e.g., Technical + Regulatory)."),
        ("EAC (Estimate at Completion)", "The projected total cost at project end. EAC = BAC / CPI (if trend continues)."),
        ("EIT", "Electrical Impedance Tomography -- technology that creates cross-sectional images using electrical currents."),
        ("EMC", "Electromagnetic Compatibility -- testing per IEC 60601-1-2 that devices don't interfere with other equipment."),
        ("EMV (Expected Monetary Value)", "Probability x Impact for each risk, used in quantitative risk analysis."),
        ("Earned Value (EV)", "The budgeted cost of work actually performed. Measures physical progress in dollar terms."),
        ("ETC (Estimate to Complete)", "The expected cost to finish remaining work. ETC = EAC - AC."),
        ("EVM (Earned Value Management)", "An integrated scope-schedule-cost performance measurement system."),
        ("Fast-Tracking", "Schedule compression by overlapping activities normally done sequentially (increases risk)."),
        ("510(k)", "FDA premarket notification pathway. Demonstrates substantial equivalence to a predicate device."),
        ("Float (Slack)", "The amount of time an activity can be delayed without delaying the project end date."),
        ("FMEA", "Failure Mode and Effects Analysis -- systematic method for identifying potential failure modes."),
        ("Gate", "A phase-gate decision checkpoint where the project is evaluated against criteria for go/no-go."),
        ("Gantt Chart", "A bar chart showing project activities plotted against time. Widely used for schedule visualization."),
        ("Gold Plating", "Adding extras not in the scope. Unlike scope creep, it is initiated by the team. Never acceptable."),
        ("Hazard", "A potential source of harm to a patient or user (ISO 14971 terminology)."),
        ("Hybrid Approach", "A project methodology combining predictive (waterfall) and adaptive (agile) elements."),
        ("IEC 60601-1", "International standard for basic safety and essential performance of medical electrical equipment."),
        ("IEC 62304", "International standard for medical device software lifecycle processes."),
        ("IFU", "Instructions for Use -- required labeling document for medical devices."),
        ("IKN", "FDA product code for surface electromyography respiratory monitoring devices."),
        ("ISO 13485", "International standard for quality management systems specific to medical devices."),
        ("ISO 14971", "International standard for risk management in medical devices."),
        ("ISO 10993", "Series of standards for biological evaluation and biocompatibility of medical devices."),
        ("Iteration", "A single development cycle in agile (equivalent to a sprint in Scrum)."),
        ("Kanban", "A visual workflow management method using cards, columns, and WIP limits."),
        ("KPI (Key Performance Indicator)", "A measurable value demonstrating progress toward a critical objective."),
        ("Lag", "A mandatory delay between the end of a predecessor activity and start of a successor."),
        ("Lead", "An acceleration that allows a successor to begin before its predecessor finishes (overlap)."),
        ("Lessons Learned", "Documented knowledge gained during the project for application to future projects."),
        ("M+N", "Month notation relative to project start. M+0 = project kickoff. M+6 = six months after start."),
        ("Management Reserve", "Budget set aside for unknown risks (unknown-unknowns). Controlled by the sponsor, not PM."),
        ("Milestone", "A significant point or event in the project timeline (zero-duration marker)."),
        ("Monte Carlo Simulation", "A quantitative technique running thousands of scenarios to model schedule/cost uncertainty."),
        ("MyoBus", "Proprietary integration protocol synchronizing sEMG and EIT data with <1ms alignment."),
        ("NRD", "Neural Respiratory Drive -- the brain's output signal commanding breathing muscles."),
        ("OBS (Organizational Breakdown Structure)", "Hierarchical representation of the project organization."),
        ("Parametric Estimating", "Cost/duration estimation using statistical relationships (e.g., cost per unit)."),
        ("PDM (Precedence Diagramming Method)", "Network diagramming technique showing activities as nodes and dependencies as arrows."),
        ("PERT", "Program Evaluation and Review Technique. Three-point estimate: (O + 4M + P) / 6."),
        ("Phase-Gate", "A project structure dividing work into phases separated by decision checkpoints (gates)."),
        ("Planned Value (PV)", "The authorized budget assigned to scheduled work (what SHOULD be done by now)."),
        ("PMA (Premarket Approval)", "FDA's most rigorous device approval pathway, required for Class III devices."),
        ("PMBOK", "Project Management Body of Knowledge -- the foundational guide published by PMI."),
        ("PMP", "Project Management Professional -- both a certification (PMI) and the lead PM role in this course."),
        ("Predicate Device", "A legally marketed device to which a new 510(k) device is compared for substantial equivalence."),
        ("Pre-Sub (Pre-Submission)", "An optional FDA meeting where the agency provides feedback before formal submission."),
        ("PRINCE2", "Projects IN Controlled Environments -- a process-based PM methodology popular in Europe."),
        ("Product Code", "An FDA alphanumeric code categorizing medical devices by type (e.g., IKN, DQS)."),
        ("Q-Sub", "FDA Q-Submission -- a formal request for a Pre-Submission meeting."),
        ("QSR (Quality System Regulation)", "21 CFR Part 820 -- FDA regulation governing medical device manufacturing quality."),
        ("RACI", "Responsibility matrix: Responsible, Accountable, Consulted, Informed."),
        ("RAM (Responsibility Assignment Matrix)", "A grid mapping work packages to team members/roles."),
        ("Residual Risk", "The risk remaining after control measures have been applied."),
        ("Risk Appetite", "The degree of uncertainty an organization is willing to accept in pursuit of objectives."),
        ("Risk Register", "The document listing all identified risks, their analysis, response plans, and current status."),
        ("Risk Tolerance", "The specific level of risk an organization can withstand (more precise than risk appetite)."),
        ("ROI (Return on Investment)", "A financial metric: (Net Profit / Investment Cost) x 100."),
        ("Runway", "The number of months a startup can operate before running out of cash (Cash / Monthly Burn)."),
        ("SAFe", "Scaled Agile Framework -- an enterprise agile methodology for large organizations."),
        ("Scope Baseline", "The approved scope statement, WBS, and WBS dictionary."),
        ("Scope Creep", "Uncontrolled expansion of project scope without adjustments to time, cost, or resources."),
        ("Scrum", "An agile framework using time-boxed sprints, a Product Owner, Scrum Master, and ceremonies."),
        ("sEMG", "Surface Electromyography -- non-invasive monitoring of muscle electrical activity."),
        ("Sensitivity Analysis", "Determines which risks have the most potential impact on project objectives."),
        ("Servant Leadership", "A leadership philosophy where the PM's role is to serve and empower the team."),
        ("SiMD", "Software in a Medical Device -- software that is an integral part of a medical device."),
        ("SPI (Schedule Performance Index)", "EV / PV. Measures schedule efficiency. >1 = ahead. <1 = behind."),
        ("Sprint", "A time-boxed iteration in Scrum (typically 1-4 weeks)."),
        ("Stakeholder", "Any individual, group, or organization that can affect, be affected by, or perceive itself as affected by the project."),
        ("Substantial Equivalence", "The FDA standard for 510(k) devices: new device is as safe/effective as a predicate."),
        ("SV (Schedule Variance)", "EV - PV. Positive = ahead of schedule. Negative = behind schedule."),
        ("SWOT Analysis", "Strategic assessment: Strengths, Weaknesses, Opportunities, Threats."),
        ("TCPI (To-Complete Performance Index)", "(BAC - EV) / (BAC - AC). The CPI needed to finish on budget."),
        ("Three-Point Estimate", "Duration or cost estimate using Optimistic, Most Likely, and Pessimistic values."),
        ("Triple Constraint", "The interdependent relationship between Scope, Schedule, and Cost (the Iron Triangle)."),
        ("Tuckman Model", "Team development stages: Forming, Storming, Norming, Performing, Adjourning."),
        ("V/Q", "Ventilation/Perfusion ratio -- a critical clinical measurement in pulmonary diagnostics."),
        ("Validation", "Confirmation that the intended user needs/requirements are fulfilled (right product built)."),
        ("Verification", "Confirmation that specified requirements have been fulfilled (product built right)."),
        ("WBS (Work Breakdown Structure)", "A hierarchical decomposition of the total scope into manageable work packages."),
        ("WBS Dictionary", "A document detailing each WBS element: description, owner, acceptance criteria, resources."),
        ("WIP (Work in Progress)", "The number of items currently being worked on. Agile/Kanban limits WIP to improve flow."),
    ]

    for term, definition in glossary:
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(*NAVY)
        pdf.cell(0, 5.5, term, new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "", 9.5)
        pdf.set_text_color(*TEXT)
        pdf.multi_cell(0, 5, "    " + definition, new_x="LMARGIN", new_y="NEXT")
        pdf.ln(1.5)

    # ================================================================
    # APPENDIX B: Case Study Reference Data
    # ================================================================
    pdf.module_title("B", "Case Study Reference Data")

    pdf.sec("Project Overview")
    pdf.kv("Product:", "ICU Respiratory Digital Twin System")
    pdf.kv("Applicant:", "Company B USA (Global IP Holder)")
    pdf.kv("Manufacturer:", "Silan Technology (Chengdu) Co., Ltd.")
    pdf.kv("Pathway:", "510(k) Modular Approval (pending Pre-Sub confirmation)")
    pdf.kv("Timeline:", "M+0 (March 2026) to M+23 (February 2028)")
    pdf.kv("Budget:", "$5.0M total ($2M seed + $3M growth)")
    pdf.kv("Cash on Hand:", "$320,000")
    pdf.kv("Monthly Burn:", "$45,000")
    pdf.kv("Runway:", "~7 months")
    pdf.ln(3)

    pdf.sec("Milestone Summary (Technical)")
    milestones_t = [
        ("T1", "M+0", "Prototype Finalization -- sEMG Module", "Complete"),
        ("T2", "M+1", "ECG-Gating Algorithm Validation", "In Progress"),
        ("T3", "M+3", "Bench & Performance Testing -- sEMG", "Not Started"),
        ("T4", "M+6", "sEMG Sensitivity/Specificity Targets", "Not Started"),
        ("T5", "M+8", "EIT Prototype -- 32-Electrode Belt", "Not Started"),
        ("T6", "M+12", "V/Q Algorithm Validation (vs. DCE-CT)", "Not Started"),
        ("T7", "M+14", "EIT Biocompatibility Testing", "Not Started"),
        ("T8", "M+2", "MyoBus Protocol Integration", "In Progress"),
    ]
    for mid, month, title, status in milestones_t:
        pdf.kv(f"{mid} ({month}):", f"{title} [{status}]")

    pdf.ln(3)
    pdf.sec("Milestone Summary (Regulatory)")
    milestones_r = [
        ("R1", "M+0", "Pre-Sub Q-Meeting Request Filed", "Complete"),
        ("R2", "M+2", "Pre-Submission Meeting (FDA)", "Not Started"),
        ("R3", "M+6", "510(k) Submission -- sEMG Module", "Not Started"),
        ("R4", "M+9", "Expected 510(k) Clearance -- sEMG", "Not Started"),
        ("R5", "M+12", "Begin EIT 510(k) Preparation", "Not Started"),
        ("R6", "M+17", "510(k) Submission -- EIT System", "Not Started"),
        ("R7", "M+23", "Expected 510(k) Clearance -- EIT", "Not Started"),
        ("R8", "M+1", "IP Buyout & US Legal Structure", "In Progress"),
        ("R9", "M+2", "ISO 13485 Audit -- Silan Technology", "Not Started"),
    ]
    for mid, month, title, status in milestones_r:
        pdf.kv(f"{mid} ({month}):", f"{title} [{status}]")

    pdf.ln(3)
    pdf.sec("Gate Summary")
    gates = [
        ("G1", "M+3", "sEMG Design Verification Complete", "4 criteria"),
        ("G2", "M+2", "Pre-Sub FDA Feedback Received", "4 criteria"),
        ("G3", "M+6", "510(k) sEMG Submission Ready", "5 criteria"),
        ("G4", "M+9", "sEMG Module Commercial Launch", "3 criteria"),
        ("G5", "M+17", "EIT 510(k) Submission Ready", "4 criteria"),
        ("G6", "M+23", "Full Platform Launch -- FDA Cleared", "3 criteria"),
    ]
    for gid, month, title, criteria in gates:
        pdf.kv(f"{gid} ({month}):", f"{title} [{criteria}]")

    pdf.ln(3)
    pdf.sec("Risk Summary")
    risks = [
        ("RISK-001", "Yellow", "False-negative sEMG signal"),
        ("RISK-002", "Yellow", "ECG artifact false positive"),
        ("RISK-003", "Green", "EIT belt electrical leakage"),
        ("RISK-004", "Red", "V/Q image misinterpretation"),
        ("RISK-005", "Yellow", "Cybersecurity breach"),
        ("RISK-006", "Green", "MyoBus sync failure"),
        ("RISK-007", "Red", "510(k) predicate rejection (De Novo fallback)"),
        ("RISK-008", "Red", "Funding runway insufficient before M+9"),
    ]
    for rid, level, title in risks:
        color_map = {"Red": RED, "Yellow": AMBER, "Green": GREEN}
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(*color_map.get(level, TEXT))
        pdf.cell(50, 5.5, f"{rid} [{level}]:", new_x="END", new_y="LAST")
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(*TEXT)
        pdf.cell(0, 5.5, title, new_x="LMARGIN", new_y="NEXT")

    # ---- Save ----
    out_path = os.path.join(OUT_DIR, "PMP_Certificate_Course.pdf")
    pdf.output(out_path)
    print(f"Course PDF: {out_path}")
    print(f"Pages: {pdf.page_no()}")


if __name__ == "__main__":
    build()
    print("Done.")
