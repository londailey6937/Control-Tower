#!/usr/bin/env python3
"""Generate two PDFs:
1. Message Board Q&A Sheet — questions for the PMP to ask Dr. Dai
2. China Control Tower Implementation Fact Sheet
"""

import os
from fpdf import FPDF

OUT_DIR = os.path.dirname(os.path.abspath(__file__))

# Map non-latin-1 chars to ASCII equivalents so Helvetica doesn't choke
_CHAR_MAP = str.maketrans({
    "\u2014": "--",   # em-dash
    "\u2013": "-",    # en-dash
    "\u2022": "*",    # bullet
    "\u2018": "'",    # left single quote
    "\u2019": "'",    # right single quote
    "\u201c": '"',    # left double quote
    "\u201d": '"',    # right double quote
    "\u2265": ">=",   # >=
    "\u2264": "<=",   # <=
    "\u00b5": "u",    # micro sign -> u
    "\u00d7": "x",    # multiplication sign
})

def _a(s: str) -> str:
    """Ensure string is ASCII-safe for Helvetica."""
    return s.translate(_CHAR_MAP)

BLUE = (30, 90, 200)
DARK = (15, 17, 23)
GRAY = (120, 120, 130)
TEXT = (40, 40, 45)
RED = (180, 40, 40)
GREEN = (20, 130, 70)
ORANGE = (200, 120, 20)

# ────────────────────────────────────────
#  1.  MESSAGE BOARD Q&A SHEET
# ────────────────────────────────────────

class SafePDF(FPDF):
    """FPDF subclass that auto-sanitises text for latin-1 safe fonts."""
    def cell(self, *a, **kw):
        if "text" in kw and isinstance(kw["text"], str):
            kw["text"] = _a(kw["text"])
        elif len(a) >= 3 and isinstance(a[2], str):
            a = list(a); a[2] = _a(a[2]); a = tuple(a)
        return super().cell(*a, **kw)

    def multi_cell(self, *a, **kw):
        if "text" in kw and isinstance(kw["text"], str):
            kw["text"] = _a(kw["text"])
        elif len(a) >= 3 and isinstance(a[2], str):
            a = list(a); a[2] = _a(a[2]); a = tuple(a)
        return super().multi_cell(*a, **kw)


class QASheet(SafePDF):
    def header(self):
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*GRAY)
        self.cell(0, 6, "ICU Respiratory Digital Twin - Message Board Q&A Sheet  |  CONFIDENTIAL", align="R")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(*GRAY)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")

    def sec(self, num, title):
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(*BLUE)
        self.cell(0, 9, f"Section {num}: {title}", new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(*BLUE)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(4)

    def context(self, text):
        self.set_font("Helvetica", "I", 9)
        self.set_text_color(*GRAY)
        self.multi_cell(0, 5, text, new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def q(self, num, question, *, follow_ups=None, why=None):
        # Question number & text
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(*RED)
        self.cell(12, 6, f"Q{num}.")
        self.set_text_color(*TEXT)
        self.multi_cell(0, 6, question, new_x="LMARGIN", new_y="NEXT")
        # Why this matters
        if why:
            self.set_font("Helvetica", "I", 9)
            self.set_text_color(*GRAY)
            self.cell(12, 5, "")
            self.multi_cell(0, 5, f"[Why: {why}]", new_x="LMARGIN", new_y="NEXT")
        # Follow-ups
        if follow_ups:
            self.set_font("Helvetica", "", 9)
            self.set_text_color(*TEXT)
            for fu in follow_ups:
                self.cell(16, 5, "")
                self.multi_cell(0, 5, f"- {fu}", new_x="LMARGIN", new_y="NEXT")
        # Editable answer box (FreeText annotation — click to type in PDF viewer)
        self.ln(1)
        y = self.get_y()
        box_w = self.w - self.l_margin - self.r_margin
        box_h = 18
        self.set_draw_color(200, 200, 205)
        self.set_fill_color(248, 248, 250)
        self.rect(self.l_margin, y, box_w, box_h, style="DF")
        self.set_font("Helvetica", "", 14)
        self.set_draw_color(*TEXT)
        self.free_text_annotation(
            "Answer / Notes:",
            x=self.l_margin, y=y, w=box_w, h=box_h,
        )
        self.set_y(y + box_h + 2)
        self.ln(2)


def build_qa():
    pdf = QASheet()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=22)
    pdf.add_page()

    # ── Cover ──
    pdf.ln(25)
    pdf.set_font("Helvetica", "B", 26)
    pdf.set_text_color(*BLUE)
    pdf.cell(0, 12, "Inventor Interview", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 14)
    pdf.set_text_color(*TEXT)
    pdf.cell(0, 8, "Question & Answer Sheet", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)
    pdf.set_font("Helvetica", "I", 11)
    pdf.set_text_color(*GRAY)
    pdf.cell(0, 7, "ICU Respiratory Digital Twin System", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 7, "sEMG Neural Drive + EIT Ventilation/Perfusion Platform", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(8)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(*TEXT)
    pdf.cell(0, 6, "Prepared by: Project Management Professional (PMP)", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 6, "Company B USA  /  Silan Technology (Chengdu)", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 6, "Date: March 2026  |  Project Month: M+0", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)
    pdf.set_font("Helvetica", "I", 9)
    pdf.set_text_color(*GRAY)
    pdf.multi_cell(0, 5,
        "PURPOSE: This document is a structured interview guide for the PMP to question "
        "the inventor / lead engineer about the technical details, design decisions, IP status, "
        "and manufacturing readiness of the ICU Respiratory Digital Twin System. "
        "Each question includes context, follow-ups, and space for recording answers. "
        "Responses will feed directly into the Control Tower dashboard, DHF, risk register, "
        "and 510(k) submission package.",
        align="C")
    pdf.ln(6)
    pdf.set_draw_color(*BLUE)
    pdf.set_line_width(0.5)
    pdf.line(30, pdf.get_y(), pdf.w - 30, pdf.get_y())

    # ── Glossary of Acronyms ──
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(*BLUE)
    pdf.cell(0, 10, "Glossary of Acronyms", new_x="LMARGIN", new_y="NEXT")
    pdf.set_draw_color(*BLUE)
    pdf.line(pdf.l_margin, pdf.get_y(), pdf.w - pdf.r_margin, pdf.get_y())
    pdf.ln(4)

    acronyms = [
        ("510(k)", "Premarket Notification — FDA submission pathway for Class II medical devices"),
        ("ADC", "Analog-to-Digital Converter"),
        ("AES-256", "Advanced Encryption Standard (256-bit) — cryptographic algorithm"),
        ("ASP", "Average Selling Price"),
        ("BLE", "Bluetooth Low Energy — wireless communication standard"),
        ("BMI", "Body Mass Index"),
        ("BOM", "Bill of Materials — complete list of parts and components"),
        ("CAPA", "Corrective and Preventive Action"),
        ("CDRH", "Center for Devices and Radiological Health (FDA division)"),
        ("CE", "Conformite Europeenne — European product certification mark"),
        ("CFR", "Code of Federal Regulations (US)"),
        ("CRADA", "Cooperative Research and Development Agreement"),
        ("CT", "Computed Tomography"),
        ("CTO", "Chief Technology Officer"),
        ("DCE-CT", "Dynamic Contrast-Enhanced Computed Tomography"),
        ("De Novo", "FDA classification pathway for novel low-to-moderate risk devices"),
        ("DHF", "Design History File — complete record of a medical device's design"),
        ("DMR", "Device Master Record — manufacturing specifications"),
        ("DQS", "FDA product code for ventilatory EIT devices"),
        ("ECG", "Electrocardiogram"),
        ("Edi", "Electrical activity of the diaphragm"),
        ("EIT", "Electrical Impedance Tomography — imaging technique using electrical currents"),
        ("EMC", "Electromagnetic Compatibility"),
        ("EMG", "Electromyography — measurement of muscle electrical activity"),
        ("EOL", "End of Life (component discontinuation)"),
        ("eSTAR", "Electronic Submission Template and Resource (FDA format)"),
        ("GPL", "GNU General Public License (open-source software license)"),
        ("ICU", "Intensive Care Unit"),
        ("IEC", "International Electrotechnical Commission"),
        ("IFU", "Instructions for Use — user-facing device documentation"),
        ("IKN", "FDA product code for diagnostic electromyographs"),
        ("IND", "Investigational New Drug application"),
        ("IP", "Intellectual Property"),
        ("IRB", "Institutional Review Board — ethics committee for human research"),
        ("ISO", "International Organization for Standardization"),
        ("MSDS", "Material Safety Data Sheet"),
        ("NAVA", "Neurally Adjusted Ventilatory Assist"),
        ("NIH", "National Institutes of Health"),
        ("NMPA", "National Medical Products Administration (China's FDA equivalent)"),
        ("NRD", "Neural Respiratory Drive"),
        ("NSF", "National Science Foundation"),
        ("NVLAP", "National Voluntary Laboratory Accreditation Program"),
        ("OHT", "Office of Health Technology (FDA)"),
        ("PMP", "Project Management Professional"),
        ("Pre-Sub", "Pre-Submission — formal FDA meeting request before 510(k) filing"),
        ("RBAC", "Role-Based Access Control"),
        ("RTA", "Refuse to Accept — FDA rejection at initial review"),
        ("RTOS", "Real-Time Operating System"),
        ("SAFE", "Simple Agreement for Future Equity"),
        ("SBIR", "Small Business Innovation Research (US grant program)"),
        ("SBOM", "Software Bill of Materials"),
        ("sEMG", "Surface Electromyography"),
        ("SNR", "Signal-to-Noise Ratio"),
        ("SSED", "Summary of Safety and Effectiveness Data"),
        ("V/Q", "Ventilation/Perfusion — ratio of air flow to blood flow in lungs"),
        ("VIE", "Variable Interest Entity — cross-border corporate structure"),
    ]

    pdf.set_font("Helvetica", "", 9)
    for abbr, defn in acronyms:
        pdf.set_text_color(*RED)
        pdf.set_font("Helvetica", "B", 9)
        pdf.cell(28, 5, abbr)
        pdf.set_text_color(*TEXT)
        pdf.set_font("Helvetica", "", 9)
        pdf.multi_cell(0, 5, defn, new_x="LMARGIN", new_y="NEXT")
        pdf.ln(0.5)

    # ═══════════════════════════════════
    #  SECTION 1: DEVICE ARCHITECTURE
    # ═══════════════════════════════════
    pdf.add_page()
    pdf.sec(1, "Device Architecture & Design Decisions")
    pdf.context(
        "We need to validate every specification in the Pre-Sub package. "
        "Discrepancies between what was filed and what exists will delay FDA review.")

    pdf.q(1, "Walk me through the current sEMG module hardware. "
             "Is the 4-8 electrode array configuration final, or are you still iterating?",
        why="The Pre-Sub states 4-8 electrodes. FDA will ask which it is — we need a locked design.",
        follow_ups=[
            "What drove the electrode count choice?",
            "Are there any alternative array geometries under consideration?",
            "What material are the electrodes? Ag/AgCl confirmed?",
        ])

    pdf.q(2, "The ADC is spec'd as 24-bit (ADS1298) at 2000 Hz sampling. "
             "Is this the production design or a bench prototype?",
        why="TI ADS1298 is in our supplier tracker as delivered. Need to confirm it's the final BOM part.",
        follow_ups=[
            "Any plans to change the ADC? If so, it triggers a new EMC cycle.",
            "What is the actual measured SNR at 2000 Hz?",
            "Is the sampling rate configurable, or fixed at 2000 Hz?",
        ])

    pdf.q(3, "Describe the Bluetooth wireless isolation. Which BT standard — "
             "BLE 5.x? What is the measured patient leakage current?",
        why="IEC 60601-1 Type BF requires <10 µA patient leakage. This is a pass/fail gate.",
        follow_ups=[
            "NordicSemi nRF52840 is in our BOM — confirmed?",
            "What is the maximum transmission range needed in an ICU setting?",
            "How is the device paired to the bedside monitor?",
        ])

    pdf.q(4, "Explain the ECG-gating algorithm. You claim >98% artifact suppression — "
             "current bench tests show 97.5%. What's the path to 98%?",
        why="CAPA-001 is open for this. G1 criteria requires 98%. We need a realistic timeline.",
        follow_ups=[
            "Is the algorithm proprietary or based on published literature?",
            "What is the computational load? Can it run on the nRF52840?",
            "How was the 98% target derived — clinical requirement or engineering margin?",
            "What happens if 98% is not achievable? Is 97.5% clinically acceptable?",
        ])

    pdf.add_page()
    pdf.q(5, "Describe the EIT Belt — 32-electrode, 50 kHz AC injection, 50 Hz frame rate. "
             "What stage is the physical prototype at?",
        why="T5 (EIT Prototype) is NOT STARTED, targeted M+8. Need to understand actual readiness.",
        follow_ups=[
            "Do we have a working 32-electrode prototype or only simulation?",
            "Who manufactured the prototype belt? FlexBelt Medical?",
            "What is the spatial resolution of the 32x32 pixel reconstruction?",
            "Is 50 Hz frame rate sufficient for real-time ventilator feedback?",
        ])

    pdf.q(6, "MyoBus protocol — explain the <1ms timestamp alignment. "
             "How is this achieved across two wireless modules?",
        why="RISK-006 (sync failure) is rated GREEN — need to verify that's justified.",
        follow_ups=[
            "Is MyoBus a hardware clock sync or software post-processing alignment?",
            "What happens during a sync loss event? Describe the fallback mode.",
            "Has the <1ms claim been verified in a multi-patient ICU environment?",
        ])

    # ═══════════════════════════════════
    #  SECTION 2: PERFORMANCE & VALIDATION
    # ═══════════════════════════════════
    pdf.add_page()
    pdf.sec(2, "Performance Claims & Validation Evidence")
    pdf.context(
        "Every performance number in the 510(k) must be backed by test data. "
        "FDA will issue an Additional Information (AI) request if claims are unsupported.")

    pdf.q(7, "NRD detection sensitivity is claimed at ≥92%. "
             "What test protocol was used, and what is the current measured value?",
        why="T4 targets are sensitivity ≥92%, specificity ≥88%, latency <50ms. "
            "All three are 510(k) submission claims.",
        follow_ups=[
            "Was this tested against esophageal EMG as reference?",
            "What is the sample size so far? The Pre-Sub mentions n≥30.",
            "How does performance degrade with obese patients or high BMI?",
        ])

    pdf.q(8, "V/Q separation algorithm — you claim >85% accuracy vs. DCE-CT. "
             "Where does this number come from?",
        why="This is an EIT module claim (T6, M+12). If it's unvalidated, "
            "the EIT 510(k) timeline may need adjustment.",
        follow_ups=[
            "Is there published literature supporting this accuracy threshold?",
            "How many comparison studies have been done?",
            "Is there a predicate device that uses the same V/Q imaging approach?",
        ])

    pdf.q(9, "Signal latency claim: <50ms end-to-end. Is this sensor-to-screen "
             "or sensor-to-algorithm-output?",
        why="Clinicians making ventilator adjustments need real-time data. "
            "The definition of 'latency' matters for the IFU.",
        follow_ups=[
            "What are the individual latency contributions (acquisition, processing, display)?",
            "Is this measured or theoretical?",
            "Does BLE transmission add variable latency?",
        ])

    pdf.q(10, "What clinical evidence exists today? Any IRB-approved studies, "
              "published abstracts, or case reports?",
        why="510(k) Section 9 requires clinical evidence. If we have none, "
            "we need a clinical evidence strategy before M+3.",
        follow_ups=[
            "Are there plans for a clinical validation study? If so, at which hospital?",
            "Has the device been used on human subjects (even informally)?",
            "Are there any conference presentations or posters?",
        ])

    # ═══════════════════════════════════
    #  SECTION 3: IP & OWNERSHIP
    # ═══════════════════════════════════
    pdf.add_page()
    pdf.sec(3, "Intellectual Property & Ownership")
    pdf.context(
        "R8 (IP Buyout & US Legal Structure) is IN PROGRESS. The 510(k) applicant "
        "must be Company B USA. All IP must be transferred or licensed before filing.")

    pdf.q(11, "List every patent, patent application, and provisional filing "
              "related to this device. Include application numbers and jurisdictions.",
        why="We need a complete IP inventory for the DHF and investor due diligence.",
        follow_ups=[
            "Who is the named inventor on each filing?",
            "Are any patents jointly owned with a university or employer?",
            "Are there any freedom-to-operate concerns?",
        ])

    pdf.q(12, "Is there any third-party IP embedded in the device — "
              "licensed algorithms, open-source code, or university technology?",
        why="Software containing GPL or university-licensed code can create "
            "ownership disputes and FDA submission complications.",
        follow_ups=[
            "List all software libraries used, with license types.",
            "Is the ECG-gating algorithm entirely original work?",
            "Any research agreements, CRADA, or SBIR grants involved?",
        ])

    pdf.q(13, "What is the status of the IP transfer to Company B USA? "
              "Has a formal assignment agreement been executed?",
        why="R8 milestone depends on this. Cannot file 510(k) until Company B USA "
            "holds or has irrevocable license to all IP.",
        follow_ups=[
            "Is the inventor willing to assign all IP, or does he want to retain any rights?",
            "Is Silan Technology a co-owner of any IP?",
            "Are there any prior encumbrances (liens, pledges, prior licenses)?",
        ])

    # ═══════════════════════════════════
    #  SECTION 4: REGULATORY READINESS
    # ═══════════════════════════════════
    pdf.add_page()
    pdf.sec(4, "Regulatory & Standards Readiness")
    pdf.context(
        "12 regulatory standards are being tracked. Several are at 0% progress. "
        "The inventor's cooperation on test readiness is critical.")

    pdf.q(14, "Has the device undergone ANY formal IEC 60601-1 electrical safety testing? "
              "Even preliminary?",
        why="STD-01 is at 30% progress. Need to know what's been done.",
        follow_ups=[
            "Which test lab was used? Is it NVLAP-accredited?",
            "Do we have any test reports we can share with FDA at Pre-Sub?",
        ])

    pdf.q(15, "EMC testing (IEC 60601-1-2) — any testing done? "
              "ICU environments have extreme electromagnetic interference.",
        why="STD-02 is at 0%. EMC is a common 510(k) failure point. "
            "G1 requires EMC compliance verified.",
        follow_ups=[
            "Has the device been tested in an actual ICU environment?",
            "Any known interference issues (ventilators, infusion pumps, defibrillators)?",
        ])

    pdf.q(16, "Software classification — do you agree this is IEC 62304 Class B? "
              "Or could FDA classify it as Class C given it influences ventilator decisions?",
        why="G2 criteria includes software classification confirmation from FDA. "
            "Class C would significantly increase documentation requirements.",
        follow_ups=[
            "Does the software make autonomous decisions, or only display data?",
            "Is there a Software Development Plan per IEC 62304?",
            "What programming languages and RTOS are used?",
        ])

    pdf.q(17, "Cybersecurity — the Pre-Sub mentions AES-256 and RBAC. "
              "Is this implemented or planned?",
        why="RISK-005 (cybersecurity) is YELLOW. CAPA-003 found weak session tokens. "
            "FDA Cybersecurity 2023 guidance is mandatory.",
        follow_ups=[
            "Has a threat model been created (per FDA guidance)?",
            "SBOM (Software Bill of Materials) — do we have one?",
            "How are firmware updates delivered? Over-the-air?",
            "What vulnerability disclosure process exists?",
        ])

    # ═══════════════════════════════════
    #  SECTION 5: MANUFACTURING & SUPPLY CHAIN
    # ═══════════════════════════════════
    pdf.add_page()
    pdf.sec(5, "Manufacturing & Supply Chain")
    pdf.context(
        "Silan Technology (Chengdu) is the contract manufacturer. ISO 13485 audit "
        "is pending (R9, M+2). 6 suppliers are tracked.")

    pdf.q(18, "Describe Silan's current manufacturing capability for this device. "
              "Assembly line? Clean room? Soldering? Final test?",
        why="G4 criteria requires 'Manufacturing scaled — Silan production ready.' "
            "We need to understand the starting point.",
        follow_ups=[
            "What is the current production capacity (units/month)?",
            "What capital equipment upgrades are needed?",
            "Is there a Device Master Record (DMR)?",
        ])

    pdf.q(19, "Are there any single-source components that have no alternate supplier?",
        why="Supply chain risk. If NordicSemi or TI has allocation issues, "
            "we could miss milestones.",
        follow_ups=[
            "Can we qualify a second source for the ADC?",
            "ADS1298 is a mature part — any EOL concerns?",
            "What is the longest lead-time component in the BOM?",
        ])

    pdf.q(20, "Biocompatibility — have ANY ISO 10993 tests been done on the "
              "electrode materials or the EIT belt materials?",
        why="Three biocompatibility standards (STD-05/06/07) are at 0%. "
            "ACT-007 (order biocompat samples) is BLOCKED waiting on supplier.",
        follow_ups=[
            "Material Safety Data Sheets (MSDS) for all patient-contact materials?",
            "Any history of skin reactions in prototype testing?",
            "Who will perform ISO 10993 testing — in-house or contract lab?",
        ])

    # ═══════════════════════════════════
    #  SECTION 6: PREDICATE & COMPETITIVE
    # ═══════════════════════════════════
    pdf.add_page()
    pdf.sec(6, "Predicate Devices & Competitive Landscape")
    pdf.context(
        "The 510(k) pathway depends on demonstrating substantial equivalence. "
        "RISK-007 (510(k) rejection -- predicate not accepted) is rated RED.\n"
        "Working predicate assumptions:\n"
        "  * sEMG Module -- K082437 (Maquet NAVA Edi Catheter, product code IKN)\n"
        "  * EIT Module  -- K250464 (Timpel Enlight 2100, product code DQS, cleared Sep 2025)")

    pdf.q(21, "Our assumed sEMG predicate is K082437 (Maquet NAVA Edi Catheter). "
              "The Edi system uses an esophageal catheter while ours uses surface electrodes. "
              "Do you agree this is the strongest predicate, and how do you justify "
              "substantial equivalence given the different transducer technology?",
        why="Product code IKN (Electromyograph, diagnostic). The transducer difference "
            "(esophageal vs. surface) is the #1 risk FDA will challenge at Pre-Sub.",
        follow_ups=[
            "Is there a closer predicate that uses surface EMG for respiratory monitoring?",
            "What performance data can we present to bridge the transducer gap?",
            "Has K082437 been verified as still active (not recalled or superseded)?",
            "Do we have the SSED (Summary of Safety and Effectiveness Data) for K082437?",
            "Can we argue same intended use despite different measurement site?",
        ])

    pdf.q(22, "Our assumed EIT predicate is K250464 (Timpel Enlight 2100, cleared Sep 2025). "
              "Timpel is cleared for ventilation imaging only -- our device adds V/Q perfusion imaging. "
              "Does adding perfusion constitute a new intended use that invalidates this predicate?",
        why="CAPA-004 (Predicate Backup Strategy) is OPEN. If perfusion imaging is a new "
            "intended use, FDA may reject this predicate and require De Novo (+60 days, +$50-100K). "
            "K250464 evolved from K222897 and K213494 (prior Timpel versions).",
        follow_ups=[
            "Could we file the EIT module initially for ventilation-only (matching Timpel's claim) "
            "and add perfusion via a supplement later?",
            "Are there any other EIT-based cleared devices beyond Timpel in the FDA database?",
            "What is Timpel's exact intended use statement vs. our proposed IFU?",
            "If no valid predicate covers V/Q, are you prepared for a De Novo pathway?",
            "Would a split strategy (510(k) for ventilation + De Novo for perfusion) reduce risk?",
        ])

    pdf.q(23, "Who are the direct competitors in bedside respiratory monitoring? "
              "What is our differentiation?",
        why="Investor pitch and 510(k) Section 4 (Device Description) both need "
            "a clear competitive positioning.",
        follow_ups=[
            "Draeger, Getinge, Magnamed — any of these doing combined sEMG+EIT?",
            "Is there a published market size for ICU respiratory monitoring?",
            "What is our target price point vs. competitors?",
        ])

    # ═══════════════════════════════════
    #  SECTION 7: RISK & CLINICAL SAFETY
    # ═══════════════════════════════════
    pdf.add_page()
    pdf.sec(7, "Risk & Clinical Safety Concerns")
    pdf.context(
        "8 risks tracked in ISO 14971 register. 3 RED risks. "
        "The inventor's input is needed to assess residual risk accuracy.")

    pdf.q(24, "RISK-004 is rated RED: V/Q perfusion image misinterpretation leading "
              "to incorrect ventilator adjustment. How do you prevent this?",
        why="This is the highest clinical risk. 'Investigational adjunct' labeling "
            "reduces but does not eliminate risk.",
        follow_ups=[
            "Should perfusion imaging be excluded from the initial 510(k)?",
            "What training do clinicians need to interpret V/Q images correctly?",
            "Is there an on-screen confidence score or quality indicator?",
        ])

    pdf.q(25, "RISK-007 is RED: 510(k) rejection. What is your honest assessment "
              "of the probability that FDA accepts our predicate strategy?",
        why="A De Novo adds ~60 days and $50-100K. If this is likely, "
            "we need to budget and plan now, not at M+6.",
        follow_ups=[
            "Have you spoken with any regulatory consultants about predicate viability?",
            "Is there a published FDA guidance document for our device type?",
        ])

    pdf.q(26, "RISK-008 is RED: Funding runway insufficient before sEMG clearance. "
              "What is the minimum viable hardware cost to reach 510(k) submission?",
        why="$320K cash, $45K/mo burn, 7-month runway. Submission is at M+6. "
            "We need to know if the budget is realistic.",
        follow_ups=[
            "What are the largest unfunded cost items between now and M+6?",
            "Can any testing be deferred past sEMG submission?",
            "What is the minimum team size to keep the project on track?",
        ])

    # ═══════════════════════════════════
    #  SECTION 8: INVENTOR RELATIONSHIP
    # ═══════════════════════════════════
    pdf.add_page()
    pdf.sec(8, "Inventor Relationship & Ongoing Role")
    pdf.context("Clarifying the inventor's role going forward is essential for "
                "both the IP structure and the team resource plan.")

    pdf.q(27, "How is the $45K/month burn rate composed? Walk me through the "
              "major cost buckets that make up monthly operating expenses.",
        why="The burn rate drives runway calculations and investor reporting. "
            "Currently it is a static number -- we need the actual breakdown "
            "to forecast accurately and to know which costs are fixed vs. variable.",
        follow_ups=[
            "Which costs are fixed (salaries, rent) vs. variable (materials, testing)?",
            "How will the burn rate change at each project phase (M+3, M+6, M+9)?",
            "Is Silan charging a monthly retainer, or cost-plus per milestone?",
            "Are there any upcoming step-function cost increases (e.g., clinical study starts)?",
            "What is the minimum monthly spend to keep the project alive if funding is delayed?",
        ])

    pdf.q(28, "What is your expected role after IP transfer to Company B USA? "
              "CTO? Consultant? Advisory board?",
        why="Resource allocation planning. Dr. Dai is currently at 100% "
            "allocation across 3 workstreams.",
        follow_ups=[
            "Are you willing to be the named technical contact for FDA communications?",
            "What is your availability commitment (hours/week)?",
            "Employment agreement or consulting agreement?",
        ])

    pdf.q(29, "Are there any co-inventors, research collaborators, or students "
              "who contributed to the technology?",
        why="Unnamed contributors can surface as IP claimants later.",
        follow_ups=[
            "Any university affiliations that might claim IP rights?",
            "Were any government grants (NIH, NSF, DARPA) used in development?",
        ])

    pdf.q(30, "Is there anything about this device -- technical limitations, "
              "failed experiments, known issues -- that I should know about "
              "but hasn't been disclosed yet?",
        why="The PMP needs a complete picture. Undisclosed issues found during "
            "FDA review are far more damaging than issues disclosed upfront.",
        follow_ups=[
            "Any regulatory interactions in other countries (CE, NMPA)?",
            "Any adverse events or near-misses during prototype testing?",
            "Any previous FDA submissions (for any device) by the inventor?",
        ])

    # ═══════════════════════════════════
    #  SECTION 9: CURRENT FDA STATUS
    # ═══════════════════════════════════
    pdf.add_page()
    pdf.sec(9, "Current FDA Status")
    pdf.context(
        "We need to establish a clear baseline of all prior and current FDA interactions. "
        "Any undisclosed history could delay the 510(k) strategy.")

    pdf.q(31, "Has a Pre-Submission (Pre-Sub) meeting request been filed with FDA "
              "for this device? If so, what was the outcome?",
        why="Pre-Sub feedback shapes the entire 510(k) strategy. If FDA has already "
            "provided written feedback, it defines the path forward.",
        follow_ups=[
            "Do we have a Pre-Sub number (Q-number) for reference?",
            "Were any FDA meeting minutes or written responses received?",
            "Were there any surprises or concerns raised by FDA reviewers?",
        ])

    pdf.q(32, "Have there been ANY prior FDA submissions, 510(k) attempts, "
              "or IND applications related to this technology — even under a different company?",
        why="FDA's internal database retains all prior interactions. Undisclosed "
            "history can be flagged during review and damage credibility.",
        follow_ups=[
            "Any Refuse to Accept (RTA) letters received?",
            "Any Additional Information (AI) requests pending?",
            "Any prior correspondence with CDRH or an OHT division?",
        ])

    pdf.q(33, "What is the current realistic timeline expectation for the "
              "510(k) submission, and what are the critical-path blockers?",
        why="The M+6 target depends on multiple parallel workstreams. "
            "Need inventor's honest assessment of readiness.",
        follow_ups=[
            "What testing must be completed before submission?",
            "Are there any standards compliance gaps that could delay filing?",
            "Is the Design History File (DHF) in a submittable state?",
        ])

    pdf.q(34, "Has there been any interaction with FDA through "
              "the Q-Submission, Breakthrough Device, or De Novo programs?",
        why="Breakthrough Device designation could accelerate review. "
            "Any prior program interactions affect strategy.",
        follow_ups=[
            "Was a Breakthrough Device designation considered or applied for?",
            "Any communication with the FDA Innovation Pathway?",
            "Are there any FDA guidance documents specifically relevant to this device type?",
        ])

    # ═══════════════════════════════════
    #  SECTION 10: DEVELOPMENT TEAM
    # ═══════════════════════════════════
    pdf.add_page()
    pdf.sec(10, "Development Team & Resources")
    pdf.context(
        "Understanding team composition, capacity, and skill gaps is critical for "
        "resource planning, milestone feasibility, and investor due diligence.")

    pdf.q(35, "How many people are currently working on this product, "
              "and what are their roles?",
        why="Team size directly affects velocity and milestone timelines. "
            "The control tower needs accurate resource allocation data.",
        follow_ups=[
            "Provide names, titles, and percentage of time allocated to this project.",
            "Are team members full-time employees or contractors?",
            "Where is each person located (US, China, other)?",
        ])

    pdf.q(36, "What critical skills gaps exist in the current team?",
        why="Gaps in regulatory, quality, or clinical affairs could stall the project. "
            "Need to identify hiring or contracting needs early.",
        follow_ups=[
            "Do we have in-house regulatory affairs expertise?",
            "Who is responsible for quality system (ISO 13485) documentation?",
            "Is there clinical affairs / medical writing capability on the team?",
            "Who handles software verification and validation (IEC 62304)?",
        ])

    pdf.q(37, "What is the team's availability and commitment "
              "over the next 12 months?",
        why="Key person risk. If the inventor or lead engineer has competing "
            "obligations, milestones will slip.",
        follow_ups=[
            "Are any team members at risk of leaving in the next 6 months?",
            "Are there competing projects or academic obligations?",
            "What is the plan if Dr. Dai's availability drops below 50%?",
        ])

    pdf.q(38, "Who will be the designated FDA correspondent and "
              "US Agent for Company B USA?",
        why="510(k) requires a named US Agent. This person must be authorized "
            "to communicate with FDA on behalf of the company.",
        follow_ups=[
            "Is this person familiar with FDA eSTAR submission format?",
            "Who will attend the Pre-Sub Q-meeting with FDA?",
            "Do we need to hire or contract a US-based regulatory consultant?",
        ])

    # ═══════════════════════════════════
    #  SECTION 11: US COMPANY EXPECTATIONS
    # ═══════════════════════════════════
    pdf.add_page()
    pdf.sec(11, "Expectations for the US Company")
    pdf.context(
        "Company B USA is the entity that will hold the 510(k) clearance and be the "
        "legal manufacturer. Alignment on roles, revenue, and governance is essential "
        "before significant capital is deployed.")

    pdf.q(39, "What is the expected role of Company B USA — "
              "solely a regulatory holding entity, or an operational business?",
        why="This determines hiring, infrastructure, and burn rate in the US. "
            "A regulatory shell vs. operational entity have very different cost structures.",
        follow_ups=[
            "Will Company B USA have employees beyond the PMP?",
            "Will it hold inventory or manage US distribution?",
            "Is there a plan for Company B USA to generate its own revenue?",
        ])

    pdf.q(40, "What are the revenue expectations and financial projections "
              "for Company B USA in the first 3 years post-clearance?",
        why="Investors need credible financial projections. Revenue model "
            "(direct sales, distribution, licensing) drives valuation.",
        follow_ups=[
            "What is the target average selling price (ASP) per unit?",
            "What is the projected unit volume in Year 1, Year 2, Year 3?",
            "Is the revenue model device sales, SaaS subscription, or hybrid?",
            "What are the projected gross margins?",
        ])

    pdf.q(41, "What governance structure is envisioned for Company B USA? "
              "Who has decision-making authority?",
        why="Corporate governance must be clear before investor fundraising. "
            "Board composition and voting rights are key negotiation points.",
        follow_ups=[
            "Who are the current directors of Company B USA?",
            "How are major decisions (>$50K spend, hiring, strategy) approved?",
            "Is there a shareholders' agreement in place?",
            "What reporting obligations exist between Company B USA and Silan?",
        ])

    pdf.q(42, "What commercial milestones must Company B USA achieve "
              "to be considered successful?",
        why="Defining success criteria aligns stakeholder expectations "
            "and provides measurable targets for investor reporting.",
        follow_ups=[
            "Is 510(k) clearance the primary milestone, or is market launch required?",
            "What is the timeline expectation for first commercial sale?",
            "Are there conditional milestones tied to continued funding?",
        ])

    # ═══════════════════════════════════
    #  SECTION 12: PROPOSED STRUCTURE WITH INVESTOR INVOLVEMENT
    # ═══════════════════════════════════
    pdf.add_page()
    pdf.sec(12, "Proposed Structure & Investor Involvement")
    pdf.context(
        "The relationship between the inventor, Company B USA, Silan Technology, "
        "and potential investors must be clearly structured. Ambiguity in equity, "
        "control, and reporting will deter sophisticated investors.")

    pdf.q(43, "What is the proposed equity structure for Company B USA? "
              "Who holds what percentage, and on what terms?",
        why="Equity structure is the #1 question investors ask. This must be "
            "resolved before any fundraising conversations.",
        follow_ups=[
            "Are there any outstanding convertible notes or SAFEs?",
            "Is there an option pool reserved for employees/advisors?",
            "Has the company been formally valued (409A or equivalent)?",
        ])

    pdf.q(44, "What role will investors have in governance — "
              "board seats, observer rights, voting provisions?",
        why="Investors typically require board representation and protective provisions. "
            "Need to understand what the inventor is willing to grant.",
        follow_ups=[
            "Is the inventor willing to give investors a board seat?",
            "What decisions would require investor approval (veto rights)?",
            "Are there anti-dilution protections being offered?",
            "What information rights will investors receive?",
        ])

    pdf.q(45, "What is the relationship between Company B USA and Silan Technology? "
              "Is there a formal contract, licensing agreement, or ownership link?",
        why="Cross-border corporate structures create regulatory and tax complexity. "
            "Investors need to understand the money flow and control chain.",
        follow_ups=[
            "Does Silan hold equity in Company B USA, or vice versa?",
            "Is there a transfer pricing agreement for manufacturing services?",
            "How are costs allocated between the US and China entities?",
            "Are there any VIE (Variable Interest Entity) structures involved?",
        ])

    pdf.q(46, "What are the reporting obligations to investors, "
              "and how frequently will financial and milestone updates be provided?",
        why="Investor reporting cadence and content must be agreed upfront. "
            "This builds trust and is standard practice for institutional investors.",
        follow_ups=[
            "Monthly, quarterly, or annual reporting?",
            "Will investors have access to the Control Tower dashboard?",
            "Who is responsible for preparing investor reports?",
            "Are there any existing investor agreements or term sheets?",
        ])

    # ── Back page: scoring rubric ──
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(*BLUE)
    pdf.cell(0, 10, "Scoring Guide — Post-Interview Assessment", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(*TEXT)
    pdf.multi_cell(0, 5.5,
        "After completing the interview, score each section on a 1-5 scale to identify "
        "areas of strength and concern. This feeds into the Control Tower risk register.",
        new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    sections_score = [
        ("1. Device Architecture", "Design locked? Specs match Pre-Sub?"),
        ("2. Performance & Validation", "Claims backed by data? Test protocols solid?"),
        ("3. IP & Ownership", "Clean IP chain? Transfer on track?"),
        ("4. Regulatory Readiness", "Standards progress realistic? Lab access secured?"),
        ("5. Manufacturing & Supply Chain", "Silan ready? BOM stable? Single-source risks?"),
        ("6. Predicate & Competitive", "Predicate viable? Differentiation clear?"),
        ("7. Risk & Clinical Safety", "RED risks manageable? Budget realistic?"),
        ("8. Inventor Relationship", "Role clear? Full disclosure achieved?"),
        ("9. Current FDA Status", "Prior interactions known? Timeline realistic?"),
        ("10. Development Team", "Staffed? Skill gaps identified? Committed?"),
        ("11. US Company Expectations", "Role defined? Revenue model clear?"),
        ("12. Investor Structure", "Equity clear? Governance agreed? Reporting set?"),
    ]
    for s_title, s_desc in sections_score:
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(*TEXT)
        pdf.cell(90, 6, s_title)
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(*GRAY)
        pdf.cell(70, 6, s_desc)
        # Editable score box
        pdf.set_draw_color(200, 200, 205)
        pdf.set_fill_color(248, 248, 250)
        x = pdf.get_x()
        y = pdf.get_y()
        pdf.rect(x, y, 20, 6, style="DF")
        pdf.set_font("Helvetica", "", 14)
        pdf.set_draw_color(*TEXT)
        pdf.free_text_annotation("/5", x=x, y=y, w=20, h=6)
        pdf.ln(10)

    pdf.ln(6)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(*TEXT)
    pdf.cell(0, 6, "Overall Readiness Assessment:", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)
    for label, color in [("GREEN — Proceed as planned", GREEN),
                         ("YELLOW — Proceed with conditions (list below)", ORANGE),
                         ("RED — Hold until issues resolved (list below)", RED)]:
        cb_y = pdf.get_y()
        pdf.set_draw_color(*color)
        pdf.set_line_width(0.8)
        pdf.rect(pdf.l_margin, cb_y, 5, 5)
        pdf.set_line_width(0.2)
        pdf.set_font("Helvetica", "B", 14)
        pdf.set_draw_color(*color)
        pdf.free_text_annotation(" ", x=pdf.l_margin, y=cb_y, w=5, h=5)
        pdf.set_xy(pdf.l_margin + 8, cb_y)
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(*TEXT)
        pdf.cell(0, 6, label, new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)

    pdf.ln(4)
    pdf.set_font("Helvetica", "I", 9)
    pdf.set_text_color(*GRAY)
    pdf.cell(0, 5, "Conditions / Blockers:", new_x="LMARGIN", new_y="NEXT")
    y = pdf.get_y() + 2
    box_w = pdf.w - pdf.l_margin - pdf.r_margin
    pdf.set_draw_color(200, 200, 205)
    pdf.set_fill_color(248, 248, 250)
    pdf.rect(pdf.l_margin, y, box_w, 50, style="DF")
    pdf.set_font("Helvetica", "", 14)
    pdf.set_draw_color(*TEXT)
    pdf.free_text_annotation(
        "Enter conditions or blockers here...",
        x=pdf.l_margin, y=y, w=box_w, h=50,
    )

    path = os.path.join(OUT_DIR, "Message_Board_QA_Sheet.pdf")
    pdf.output(path)
    return path


# ────────────────────────────────────────
#  2.  CHINA CONTROL TOWER FACT SHEET
# ────────────────────────────────────────

class FactSheet(SafePDF):
    def header(self):
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*GRAY)
        self.cell(0, 6,
                  "Control Tower - China Implementation Fact Sheet  |  CONFIDENTIAL",
                  align="R")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(*GRAY)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")

    def sec(self, title):
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(*BLUE)
        self.cell(0, 9, title, new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(*BLUE)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(4)

    def sub(self, title):
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(*TEXT)
        self.cell(0, 7, title, new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def txt(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*TEXT)
        self.multi_cell(0, 5.5, text, new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def bul(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*TEXT)
        self.multi_cell(0, 5.5, "  *  " + text,
                        new_x="LMARGIN", new_y="NEXT")

    def kv(self, key, val):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(*BLUE)
        self.cell(0, 5.5, key, new_x="LMARGIN", new_y="NEXT")
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*TEXT)
        self.multi_cell(0, 5.5, "  " + val, new_x="LMARGIN", new_y="NEXT")
        self.ln(1)


def build_factsheet():
    pdf = FactSheet()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()

    # ── Cover ──
    pdf.ln(20)
    pdf.set_font("Helvetica", "B", 24)
    pdf.set_text_color(*BLUE)
    pdf.cell(0, 12, "Control Tower", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 16)
    pdf.set_text_color(*TEXT)
    pdf.cell(0, 8, "China Implementation Fact Sheet", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)
    pdf.set_font("Helvetica", "I", 11)
    pdf.set_text_color(*GRAY)
    pdf.cell(0, 7, "Silan Technology (Chengdu) Co., Ltd.", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 7, "ICU Respiratory Digital Twin System", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(6)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(*TEXT)
    pdf.cell(0, 6, "March 2026  |  Version 1.0", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 6, "Prepared by: Project Management Professional (PMP)", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 6, "Company B USA", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)
    pdf.set_font("Helvetica", "I", 9)
    pdf.set_text_color(*GRAY)
    pdf.multi_cell(0, 5,
        "This document describes how the PM Dashboard (Control Tower) will be deployed and "
        "accessed by the Chengdu engineering team. It covers hosting, access method, security, "
        "data handling, and team onboarding for cross-border project management.",
        align="C")

    # ═══════════════════════════
    #  EXECUTIVE SUMMARY
    # ═══════════════════════════
    pdf.add_page()
    pdf.sec("Executive Summary")
    pdf.txt(
        "The Control Tower is a browser-based PM dashboard that tracks every aspect of the "
        "ICU Respiratory Digital Twin project: milestones, gates, risks, financials, DHF documents, "
        "CAPA items, suppliers, and audit trail. It runs entirely in the browser as a static web app "
        "with no server-side processing or database — all data lives in the client.")
    pdf.txt(
        "For the Chengdu team (Silan Technology), we will deploy the dashboard to a US-based "
        "hosting platform. The team will access it via corporate VPN, ensuring that all project "
        "data remains on US-controlled infrastructure while being accessible to the China team.")

    # ═══════════════════════════
    #  ARCHITECTURE
    # ═══════════════════════════
    pdf.sec("Architecture Overview")
    pdf.sub("Technology Stack")
    pdf.kv("Frontend", "TypeScript + Vite + Tailwind CSS (static site, ~130 KB gzipped)")
    pdf.kv("Data Storage", "In-browser (localStorage + IndexedDB for documents)")
    pdf.kv("Backend", "None — fully client-side. No server, no database")
    pdf.kv("Build", "Vite 8.x produces a dist/ folder with HTML, CSS, JS")
    pdf.kv("Hosting", "Static file hosting (Vercel, Netlify, or AWS S3 + CloudFront)")
    pdf.ln(2)

    pdf.sub("What This Means for China Access")
    pdf.txt(
        "Because the app is a static site with no API calls to external servers (except optional "
        "API reference links), it loads quickly even over VPN. The entire app payload is under "
        "130 KB gzipped — equivalent to a single image file. After the initial load, the dashboard "
        "runs entirely offline-capable in the browser.")

    # ═══════════════════════════
    #  DEPLOYMENT PLAN
    # ═══════════════════════════
    pdf.add_page()
    pdf.sec("Deployment Plan")

    pdf.sub("Recommended: Vercel (US-hosted)")
    pdf.txt(
        "The dashboard will be deployed to Vercel, a US-based static hosting platform with "
        "global CDN. Deployment is automated — every code update automatically rebuilds and "
        "deploys within ~60 seconds.")
    pdf.kv("URL", "https://controltower.company-b.com (custom domain)")
    pdf.kv("SSL", "Automatic HTTPS via Let's Encrypt")
    pdf.kv("CDN", "Global edge network (US, Asia, Europe)")
    pdf.kv("Cost", "Free tier for static sites; $20/mo for team features")
    pdf.kv("Uptime SLA", "99.99% (Vercel Pro)")

    pdf.ln(2)
    pdf.sub("Alternative: AWS S3 + CloudFront")
    pdf.txt(
        "For organizations preferring AWS, the dist/ folder can be hosted in an S3 bucket "
        "behind CloudFront CDN with optional Cognito authentication. Estimated cost: ~$5/mo.")

    # ═══════════════════════════
    #  CHINA ACCESS METHOD
    # ═══════════════════════════
    pdf.add_page()
    pdf.sec("China Access — VPN Configuration")

    pdf.sub("Why VPN Is Required")
    pdf.txt(
        "Western hosting platforms (Vercel, AWS us-regions, Netlify) are accessible from China "
        "but experience unpredictable throttling by the Great Firewall (GFW). Performance can "
        "range from normal to unusable depending on time of day and ISP. A corporate VPN provides "
        "consistent, reliable access.")

    pdf.sub("Recommended VPN Setup")
    pdf.kv("Corporate VPN", "Company B USA operates a VPN service for all cross-border team communication")
    pdf.kv("Protocol", "WireGuard or IKEv2 (recommended for China — better GFW traversal than OpenVPN)")
    pdf.kv("VPN Endpoint", "US West Coast (lowest latency to Chengdu: ~150ms)")
    pdf.kv("Users", "All Silan Technology team members who need dashboard access")
    pdf.kv("Bandwidth", "Minimal — app is <130 KB. VPN need not be high-throughput")
    pdf.ln(2)

    pdf.sub("Access Without VPN (Fallback)")
    pdf.txt(
        "If VPN is temporarily unavailable, the team may still be able to access the dashboard "
        "directly — Vercel's CDN has Asia PoPs that sometimes bypass throttling. However, "
        "this is not guaranteed and should not be the primary access method.")
    pdf.txt(
        "Note: An alternative approach is dual-hosting to Alibaba Cloud OSS (China region), "
        "but this requires an ICP filing (ICP Recordal / ICP License) if a custom domain is used. "
        "This can be explored later if VPN access proves insufficient.")

    # ═══════════════════════════
    #  SECURITY & DATA
    # ═══════════════════════════
    pdf.add_page()
    pdf.sec("Security & Data Handling")

    pdf.sub("Data Sovereignty")
    pdf.bul("All project data (milestones, risks, financials, DHF) is embedded in the JavaScript bundle")
    pdf.bul("No data is transmitted to or stored on any server")
    pdf.bul("Document attachments (CR evidence files) are stored in IndexedDB on the user's local browser")
    pdf.bul("The hosting server only serves static files — it has no knowledge of project data")
    pdf.bul("Data sovereignty risk: NONE — data never leaves the user's browser after page load")
    pdf.ln(2)

    pdf.sub("Access Control")
    pdf.bul("Dashboard has 4 built-in roles: PMP (full), Tech (view + CR), Business (view + CR), Accounting (limited)")
    pdf.bul("Role switching is local — there is no server-side authentication in the current version")
    pdf.bul("For production use, Cloudflare Access or Vercel Auth can add email-based authentication ($0-20/mo)")
    pdf.bul("VPN itself acts as a network-level access gate — only VPN users can reach the dashboard URL")
    pdf.ln(2)

    pdf.sub("Sensitive Data Considerations")
    pdf.txt(
        "The dashboard contains sensitive information: FDA submission strategy, financial position, "
        "IP status, risk assessments, and supplier details. The following safeguards apply:")
    pdf.bul("HTTPS encryption in transit (TLS 1.3)")
    pdf.bul("VPN tunnel encryption (WireGuard: ChaCha20-Poly1305)")
    pdf.bul("No server-side data exposure — everything is client-rendered")
    pdf.bul("Audit trail logs all status changes with timestamp and user")
    pdf.bul("No data is sent to analytics services, ad networks, or third parties")

    # ═══════════════════════════
    #  FEATURES FOR CHINA TEAM
    # ═══════════════════════════
    pdf.add_page()
    pdf.sec("Features Relevant to the China Team")

    pdf.sub("Full Bilingual Support (EN/CN)")
    pdf.txt(
        "Every label, description, milestone, risk, and gate criterion has both English and "
        "Chinese translations. One-click language toggle switches the entire interface. "
        "The Chengdu team can work entirely in Chinese.")

    pdf.sub("11 Dashboard Tabs")
    pdf.bul("Dual-Track — Technical + Regulatory milestones (side-by-side)")
    pdf.bul("Gate System — Decision checkpoints with PMP authority")
    pdf.bul("Risk Dashboard — ISO 14971 risk register with filtering")
    pdf.bul("Timeline — Business-language translation of technical milestones")
    pdf.bul("Regulatory Tracker — 12 standards compliance matrix")
    pdf.bul("Cash / Runway — Financial position + China API integrations panel")
    pdf.bul("Action Items — Kanban task board + DHF document tracker + CAPA log")
    pdf.bul("Budget vs. Actual — Category-level spend tracking")
    pdf.bul("Resources — Team allocation and utilization")
    pdf.bul("Suppliers — Vendor status tracker (6 suppliers)")
    pdf.bul("Audit Trail — Complete change history for 21 CFR Part 11 traceability")
    pdf.ln(2)

    pdf.sub("China-Specific API Integrations Panel")
    pdf.txt(
        "The Cash / Runway tab includes a dedicated section showing China investor payment "
        "and banking APIs: Alipay Business, WeChat Pay Business, UnionPay International, "
        "China Merchants Bank, PingPong Global, XE Currency Data, and SWIFT gpi. "
        "These are reference cards with status badges and documentation links.")

    pdf.sub("Change Request Workflow")
    pdf.txt(
        "Chengdu engineers using the 'Technology' role can propose status changes (milestones, "
        "risks, standards) via the Change Request system. Each CR includes justification, evidence, "
        "and optional file attachments. The PMP (US-based) reviews and approves or rejects. "
        "This ensures proper governance while enabling asynchronous cross-border collaboration.")

    # ═══════════════════════════
    #  ONBOARDING PLAN
    # ═══════════════════════════
    pdf.add_page()
    pdf.sec("China Team Onboarding Plan")

    pdf.sub("Phase 1: Infrastructure (Week 1)")
    pdf.bul("Configure corporate VPN accounts for all Silan team members")
    pdf.bul("Deploy dashboard to Vercel with custom domain")
    pdf.bul("Verify access from Chengdu office (test load time and performance)")
    pdf.bul("Distribute Chinese User Guide PDF to all team members")
    pdf.ln(2)

    pdf.sub("Phase 2: Training (Week 2)")
    pdf.bul("Video call walkthrough of all 11 dashboard tabs (in Chinese)")
    pdf.bul("Practice session: submit a Change Request and attach a document")
    pdf.bul("Review roles and permissions — who has which role")
    pdf.bul("Q&A session for engineers and regulatory team")
    pdf.ln(2)

    pdf.sub("Phase 3: Operational (Week 3+)")
    pdf.bul("Daily use for milestone status tracking")
    pdf.bul("Weekly CR review cycle: Chengdu submits CRs by Thursday, PMP reviews by Monday")
    pdf.bul("Monthly: Export report generation for investor updates")
    pdf.bul("Quarterly: Full dashboard data refresh based on actual project progress")
    pdf.ln(2)

    pdf.sub("Support & Troubleshooting")
    pdf.kv("VPN Issues", "Contact Company B IT support — backup: direct Vercel URL (may work without VPN)")
    pdf.kv("Dashboard Bugs", "Report via WeChat group or email to PMP; include screenshot + browser version")
    pdf.kv("Data Discrepancy", "Submit a Change Request with evidence; do not directly modify source files")
    pdf.kv("Language Issue", "File an issue with screenshot; both EN and CN translations maintained by PMP")

    # ═══════════════════════════
    #  TEAM ROSTER
    # ═══════════════════════════
    pdf.add_page()
    pdf.sec("Team Members & Dashboard Roles")
    pdf.txt("The following team members will have dashboard access:")
    pdf.ln(2)

    members = [
        ("Dr. Dai", "Lead Engineer (sEMG)", "Technology", "VPN user"),
        ("Dr. Wang", "Lead Engineer (EIT)", "Technology", "VPN user"),
        ("Sarah Kim", "Regulatory Affairs Lead", "Technology", "Direct access (US-based)"),
        ("Mike Zhang", "Quality Manager", "Technology", "VPN user"),
        ("Li Wei", "Security Engineer", "Technology", "VPN user"),
        ("Jessica Park", "PM Analyst", "Business", "Direct access (US-based)"),
        ("PMP (Lon Dailey)", "Project Manager", "PMP", "Direct access (US-based)"),
    ]
    # Table header
    col_w = [40, 50, 30, 50]
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(255, 255, 255)
    pdf.set_fill_color(*BLUE)
    for i, h in enumerate(["Name", "Role", "Dashboard Role", "Access Method"]):
        pdf.cell(col_w[i], 7, h, border=1, fill=True, align="C")
    pdf.ln()
    # Table rows
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(*TEXT)
    for j, (n, r, dr, am) in enumerate(members):
        fill = j % 2 == 0
        pdf.set_fill_color(245, 245, 248)
        for i, val in enumerate([n, r, dr, am]):
            pdf.cell(col_w[i], 7, val, border=1, fill=fill)
        pdf.ln()

    pdf.ln(6)
    pdf.sec("Timeline Summary")
    pdf.txt("Key dates for China team integration:")
    pdf.ln(2)
    timeline = [
        ("Week 1 (Mar 23-27)", "VPN setup, dashboard deployment, access verification"),
        ("Week 2 (Mar 30 - Apr 3)", "Training sessions (video call, practice CRs)"),
        ("Week 3 (Apr 7+)", "Operational — daily dashboard use begins"),
        ("M+2 (May 2026)", "FDA Pre-Sub meeting — Chengdu provides technical inputs via dashboard"),
        ("M+3 (Jun 2026)", "G1 gate review — all team CRs must be submitted before review"),
        ("M+6 (Sep 2026)", "510(k) sEMG submission — DHF tracker must show all docs approved"),
    ]
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(255, 255, 255)
    pdf.set_fill_color(*BLUE)
    pdf.cell(45, 7, "Date", border=1, fill=True, align="C")
    pdf.cell(125, 7, "Milestone", border=1, fill=True, align="C")
    pdf.ln()
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(*TEXT)
    for j, (d, m) in enumerate(timeline):
        fill = j % 2 == 0
        pdf.set_fill_color(245, 245, 248)
        pdf.cell(45, 7, d, border=1, fill=fill)
        pdf.cell(125, 7, m, border=1, fill=fill)
        pdf.ln()

    pdf.ln(8)
    pdf.set_font("Helvetica", "I", 9)
    pdf.set_text_color(*GRAY)
    pdf.multi_cell(0, 5,
        "This fact sheet will be updated as deployment progresses. "
        "A Chinese-language version of this document is available upon request.",
        align="C")

    path = os.path.join(OUT_DIR, "China_Control_Tower_Fact_Sheet.pdf")
    pdf.output(path)
    return path


# ────────────────────────────────────
if __name__ == "__main__":
    qa = build_qa()
    print(f"Message Board Q&A Sheet: {qa}")
    fs = build_factsheet()
    print(f"China Fact Sheet:   {fs}")
    print("Done.")
