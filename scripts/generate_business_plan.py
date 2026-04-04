#!/usr/bin/env python3
"""
Generate the ICU Respiratory Digital Twin Business Execution Plan PDF (English).
Translated and structured from the original Chinese 商业执行计划与融资路线图.
23-page investor-grade document covering product, FDA, market, funding, and IPO.
"""

import os
from fpdf import FPDF

OUT_DIR = os.path.dirname(os.path.abspath(__file__))

NAVY = (10, 40, 100)
DARK = (25, 25, 30)
TEXT = (40, 40, 45)
GRAY = (120, 120, 130)
WHITE = (255, 255, 255)
GREEN = (20, 130, 70)
RED = (170, 40, 40)
ACCENT = (0, 100, 180)
LIGHT_BG = (245, 247, 252)


class BizPlanPDF(FPDF):

    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(*GRAY)
        self.cell(0, 5,
                  "CONFIDENTIAL -- ICU Respiratory Digital Twin  |  Business Execution Plan",
                  align="R")
        self.ln(7)

    def footer(self):
        self.set_y(-13)
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(*GRAY)
        self.cell(0, 5, f"Page {self.page_no()}/{{nb}}", align="C")

    # ── formatting helpers ──
    def sec(self, num, title):
        if self.get_y() > self.h - 40:
            self.add_page()
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(*NAVY)
        label = f"{num}. {title}" if num else title
        self.cell(0, 9, label, new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(*NAVY)
        self.set_line_width(0.5)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(4)

    def sub(self, title, color=NAVY):
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

    def bold_bullet(self, label, text, indent=6):
        self.set_x(self.l_margin + indent)
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(*TEXT)
        lw = self.get_string_width(label) + 1
        self.cell(lw, 5.5, label)
        self.set_font("Helvetica", "", 10)
        self.multi_cell(0, 5.5, text, new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def table(self, headers, rows, col_w, bold_last=False):
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*WHITE)
        self.set_fill_color(*NAVY)
        for i, h in enumerate(headers):
            self.cell(col_w[i], 7, h, border=1, fill=True, align="C")
        self.ln()
        self.set_text_color(*TEXT)
        for ri, row in enumerate(rows):
            is_last = bold_last and ri == len(rows) - 1
            self.set_font("Helvetica", "B" if is_last else "", 9)
            bg = (230, 235, 250) if is_last else (LIGHT_BG if ri % 2 == 0 else WHITE)
            self.set_fill_color(*bg)
            for ci, val in enumerate(row):
                align = "L" if ci == 0 else "C"
                self.cell(col_w[ci], 6, val, border=1, fill=True, align=align)
            self.ln()
        self.ln(3)

    def info_box(self, title, items, color=ACCENT):
        bg = (235, 245, 255) if color == ACCENT else (255, 240, 240)
        self.set_draw_color(*color)
        self.set_fill_color(*bg)
        y = self.get_y()
        lh = 5.5
        box_h = 10 + len(items) * lh + 4
        if y + box_h > self.h - 20:
            self.add_page()
            y = self.get_y()
        self.rect(self.l_margin, y, self.w - self.l_margin - self.r_margin, box_h, style="DF")
        self.set_xy(self.l_margin + 4, y + 3)
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(*color)
        self.cell(0, lh, title)
        self.set_xy(self.l_margin + 6, y + 10)
        self.set_font("Helvetica", "", 9)
        self.set_text_color(*TEXT)
        for item in items:
            self.set_x(self.l_margin + 6)
            self.cell(0, lh, item, new_x="LMARGIN", new_y="NEXT")
        self.set_y(y + box_h + 4)

    def check_badge(self, text):
        self.set_fill_color(*GREEN)
        y = self.get_y()
        self.rect(self.l_margin, y, 130, 7, style="DF")
        self.set_xy(self.l_margin + 2, y + 1)
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*WHITE)
        self.cell(126, 5, text)
        self.set_y(y + 10)


# ═══════════════════════════════════════════════════════════════════
def build():
    pdf = BizPlanPDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.add_page()

    # ── Cover Page ──
    pdf.set_fill_color(*NAVY)
    pdf.rect(0, 0, 210, 70, style="F")
    pdf.set_font("Helvetica", "B", 22)
    pdf.set_text_color(*WHITE)
    pdf.set_y(12)
    pdf.cell(0, 10, "ICU Respiratory Digital Twin System", align="C",
             new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 13)
    pdf.cell(0, 7, "EIT + sEMG Integrated Platform", align="C",
             new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)
    pdf.set_draw_color(*WHITE)
    pdf.set_line_width(0.3)
    pdf.line(40, pdf.get_y(), 170, pdf.get_y())
    pdf.ln(3)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 7, "Business Execution Plan & Funding Roadmap", align="C",
             new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "I", 10)
    pdf.cell(0, 6, "From R&D to FDA Clearance to NASDAQ IPO", align="C",
             new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)
    pdf.set_font("Helvetica", "", 9)
    pdf.cell(0, 5, "CONFIDENTIAL  |  March 2026", align="C",
             new_x="LMARGIN", new_y="NEXT")

    pdf.ln(10)
    pdf.set_text_color(*DARK)

    # ── Table of Contents ──
    pdf.sec("", "Table of Contents")
    toc = [
        ("I", "Executive Summary"),
        ("II", "Product & Technology Overview"),
        ("III", "Global Corporate Structure & Business Model"),
        ("IV", "FDA Registration Pathway & Timeline"),
        ("V", "Go-to-Market & Commercialization Strategy"),
        ("VI", "Funding Roadmap & Use of Proceeds"),
        ("VII", "Master Milestone Timeline"),
        ("VIII", "Exit Pathways & Strategic Value"),
        ("IX", "Risk Analysis & Mitigation"),
        ("X", "Team & Governance Structure"),
        ("XI", "Financial Projection Summary"),
        ("", "Appendix"),
    ]
    for num, title in toc:
        label = f"  {num}.  {title}" if num else f"  {title}"
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(*TEXT)
        pdf.cell(0, 5.5, label, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    # ══════════════════════════════════════════════════════════════
    # I. EXECUTIVE SUMMARY
    # ══════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.sec("I", "Executive Summary")
    pdf.txt(
        "The company is building the world's first integrated Electrical Impedance "
        "Tomography (EIT) and Surface Electromyography (sEMG) ICU respiratory monitoring "
        "platform, filling the gap in \"ventilation + drive\" closed-loop monitoring in "
        "critical care.\n\n"
        "Company B USA (Delaware C-Corp) serves as the global IP holder and FDA "
        "registration entity. Company A (China) serves as the hardware R&D and "
        "manufacturing base. This achieves a global architecture of \"R&D in China, "
        "asset ownership in the US.\"\n\n"
        "Company B USA independently owns all core software and algorithm IP, "
        "commissioning Company A for hardware R&D, data acquisition, and supply chain "
        "development. The product follows a modular 510(k) pathway for stepwise FDA "
        "clearance. The commercialization phase uses a \"third-party leasing company\" "
        "model for rapid market entry, with a target NASDAQ listing within 5 years.\n\n"
        "Current funding status: Seed round completed at $1.8M (direct equity). "
        "Upon fund deployment, US-based R&D, commissioned hardware development, and "
        "FDA submission preparation can begin immediately.")

    pdf.sub("Key Milestones at a Glance")
    pdf.table(
        ["Milestone", "Description", "Timeline"],
        [
            ["Seed Round (Complete)", "$1.8M direct equity", "Year 0 (2026)"],
            ["First FDA 510(k)", "sEMG general EMG module", "Year 1 Q3-Q4"],
            ["Series A", "$8-$15M, launch commercialization", "Year 1-Year 2"],
            ["EIT 510(k) Cleared", "EIT lung tomography system", "Year 3 Q1-Q2"],
            ["Series B", "$25-$40M, scale-up expansion", "Year 3-Year 4"],
            ["NASDAQ IPO", "Target valuation $300M+", "Year 5 (2031)"],
        ],
        [55, 70, 45],
    )

    # ══════════════════════════════════════════════════════════════
    # II. PRODUCT & TECHNOLOGY OVERVIEW
    # ══════════════════════════════════════════════════════════════
    pdf.sec("II", "Product & Technology Overview")
    pdf.sub("2.1 Clinical Pain Points")
    pdf.txt(
        "Over 15 million patients worldwide receive mechanical ventilation in ICUs "
        "each year. Traditional ventilator monitoring provides only global pressure and "
        "flow parameters, unable to reflect intrapulmonary gas distribution or the "
        "patient's spontaneous breathing effort. This leads to three major clinical "
        "challenges:")
    pdf.bold_bullet("VILI risk: ", "Blind PEEP titration causing ventilator-induced lung injury.")
    pdf.bold_bullet("Weaning failure: ", "Diaphragm atrophy making ventilator weaning difficult.")
    pdf.bold_bullet("Patient-ventilator asynchrony: ", "Reducing treatment effectiveness.")
    pdf.txt(
        "Clinicians need a \"dual vision\" that sees through the lungs AND senses "
        "respiratory drive -- this is the core value proposition of this product.")

    pdf.sub("2.2 Solution")
    pdf.txt(
        "This product is the world's only ICU respiratory monitoring platform integrating "
        "EIT and sEMG, achieving \"see the lung + see the drive\" dual-dimension monitoring:")
    pdf.bold_bullet("EIT Module (See the Lung): ",
                    "Real-time lung tomographic imaging, visualizes ventilation distribution, "
                    "precision PEEP titration, reduces VILI risk.")
    pdf.bold_bullet("sEMG Module (See the Drive): ",
                    "Microvolt-level high-sensitivity surface EMG acquisition, real-time "
                    "diaphragm activity monitoring, preserves spontaneous breathing capacity, "
                    "facilitates early weaning.")
    pdf.bold_bullet("Combined Value: ",
                    "Shortened ICU stays, reduced healthcare costs, improved weaning success "
                    "rates. At an average US ICU daily cost of $4,000-$10,000, each day of "
                    "reduced ventilation significantly lowers per-patient treatment costs.")

    pdf.sub("2.3 MyoBus Protocol & Technology Moat")
    pdf.txt(
        "MyoBus is a medical-grade wireless protocol based on Bluetooth Low Energy "
        "(BLE 5.0), achieving pure data interaction with complete electrical isolation, "
        "ensuring 100% patient safety. As an open platform protocol, it can extend to "
        "additional physiological monitoring sensors in the future, building an industry "
        "connectivity standard. Patent portfolio is complete.\n\n"
        "Core technology barriers include:")
    pdf.bullet("World's only EIT + sEMG integrated solution")
    pdf.bullet("MyoBus patented protocol ecosystem")
    pdf.bullet("Microvolt-level high-sensitivity sEMG acquisition technology")
    pdf.bullet("Years of accumulated EIT signal processing algorithms")

    # ══════════════════════════════════════════════════════════════
    # III. GLOBAL CORPORATE STRUCTURE & BUSINESS MODEL
    # ══════════════════════════════════════════════════════════════
    pdf.sec("III", "Global Corporate Structure & Business Model")
    pdf.sub("3.1 Dual-Entity Architecture")
    pdf.table(
        ["Entity", "Function & Role"],
        [
            ["Company B USA\n(Delaware C-Corp)",
             "Global IP holder, FDA Legal Manufacturer,\ncapital operations center, NASDAQ listing entity"],
            ["Company A (China)",
             "Hardware R&D center, ISO 13485 factory,\nNMPA registration entity, production base,\nsupply chain management"],
        ],
        [50, 120],
    )
    pdf.txt(
        "Strategic logic: Company B USA independently owns all core software, algorithms, "
        "and other IP, serving as the FDA-registered Legal Manufacturer. Company A operates "
        "as a Contract Manufacturer, handling hardware R&D, data acquisition, and production. "
        "The two entities collaborate through commissioned R&D agreements and supply chain "
        "contracts, achieving both geopolitical risk mitigation and cost optimization.")

    pdf.sub("3.2 Business Model: Third-Party Leasing Operations")
    pdf.txt(
        "After product launch, the company adopts a \"light-asset\" strategy, delegating "
        "equipment marketing, sales, installation, and after-sales service to specialized "
        "US medical equipment leasing companies. Core advantages:")
    pdf.bold_bullet("Lower upfront commercialization capital: ",
                    "No need to build a sales team or service network, significantly reducing "
                    "fixed costs and the break-even point.")
    pdf.bold_bullet("Rapid market penetration: ",
                    "Leverage leasing companies' existing hospital channels and customer "
                    "relationships for rapid deployment, shortening the approval-to-placement window.")
    pdf.bold_bullet("Recurring revenue: ",
                    "Leasing model generates stable cash flows, boosts valuation multiples, "
                    "and is more attractive to capital markets.")
    pdf.bold_bullet("Lower hospital procurement barrier: ",
                    "Hospitals can use equipment without capital expenditure, paying monthly or "
                    "per-use, accelerating clinical adoption.")

    pdf.sub("3.2.1 Leasing Partnership Model Details")
    pdf.bold_bullet("Model A -- Equipment Resale + Service Agreement: ",
                    "Company B sells equipment in bulk to the leasing company, which provides "
                    "leasing services to hospital clients. Company B continues to provide tech "
                    "support, software updates, and clinical training via service contracts "
                    "(SaaS-style annual fees). Revenue: one-time device + ongoing service income.")
    pdf.bold_bullet("Model B -- Revenue Sharing: ",
                    "Company B retains equipment ownership, commissioning the leasing company to "
                    "operate on its behalf. Rental income is shared at an agreed ratio (typically "
                    "B: 70-80%, leasing co: 20-30%). Higher long-term returns but requires upfront "
                    "equipment capital.")

    # ══════════════════════════════════════════════════════════════
    # IV. FDA REGISTRATION PATHWAY & TIMELINE
    # ══════════════════════════════════════════════════════════════
    pdf.sec("IV", "FDA Registration Pathway & Timeline")
    pdf.sub("4.1 Modular 510(k) Strategy")
    pdf.txt(
        "Abandoning the high-risk De Novo pathway, the company adopts the established "
        "510(k) route, splitting the product into two independent modules for sequential "
        "submission -- isolated from each other, spreading risk:")
    pdf.table(
        ["Phase", "Product & Pathway", "Duration"],
        [
            ["Phase 1", "sEMG General EMG Module -- 510(k),\nProduct Code IKN, predicate: existing EMG devices", "6-8 months"],
            ["Phase 2", "EIT Lung Tomography System -- 510(k),\nPredicate: Timpel Enlight 2100", "9-12 months"],
        ],
        [25, 105, 30],
    )

    pdf.sub("4.2 Registration Timeline Detail")
    pdf.sub("Phase 1: sEMG Module (Year 0 Q3 -- Year 1 Q4)")
    pdf.table(
        ["Timeline", "Task"],
        [
            ["Month 1-2", "Pre-Submission Meeting: confirm Intended Use & Predicate Device"],
            ["Month 3-4", "Third-party testing: EMC, electrical safety (IEC 60601), biocompatibility"],
            ["Month 4-5", "Cybersecurity verification (Cybersecurity Documentation)"],
            ["Month 5-6", "Submit 510(k) application"],
            ["Month 6-10", "FDA review period, respond to AI/RTA questions"],
        ],
        [28, 142],
    )

    pdf.sub("Phase 2: EIT System (Year 1 Q2 -- Year 3 Q2)")
    pdf.txt(
        "The EIT product line can only begin after Series A funding is secured. "
        "The overall process is divided into five stages:")
    pdf.bold_bullet("1. IP Transfer Negotiation (Y1 Q2-Q4): ",
                    "After Series A funds arrive, initiate EIT IP transfer negotiation with "
                    "Company A (outright purchase or license, depending on negotiations). "
                    "Complete agreement signing.")
    pdf.bold_bullet("2. FDA Localization (Y2 Q1-Q2): ",
                    "Adapt EIT hardware design to US FDA requirements, including electrical "
                    "safety standards, labeling regulations, software verification (IEC 62304), "
                    "cybersecurity compliance.")
    pdf.bold_bullet("3. Third-Party Testing & Validation (Y2 Q2-Q3): ",
                    "Complete IEC 60601, EMC third-party testing; compile clinical performance "
                    "validation data; prepare predicate device analysis report (Timpel Enlight 2100).")
    pdf.bold_bullet("4. 510(k) Submission (Y2 Q3-Q4): ",
                    "EIT system 510(k) formally submitted to FDA, predicate: Timpel Enlight 2100.")
    pdf.bold_bullet("5. FDA Review & Clearance (Y3 Q1-Q2): ",
                    "Expected review cycle 6-9 months. Upon clearance, dual product lines are "
                    "complete, entering full commercialization phase.")

    # ══════════════════════════════════════════════════════════════
    # V. GO-TO-MARKET & COMMERCIALIZATION
    # ══════════════════════════════════════════════════════════════
    pdf.sec("V", "Go-to-Market & Commercialization Strategy")
    pdf.sub("5.1 Target Market")
    pdf.txt(
        "The US ICU respiratory monitoring equipment market is approximately $4.5 billion, "
        "with the auxiliary monitoring segment (EIT/sEMG class) in early rapid growth. "
        "Initial target customers are ICU departments of US teaching hospitals and major "
        "medical centers.\n\n"
        "Market entry strategy: drive adoption through clinical evidence, build brand "
        "awareness via KOL academic networks, then achieve scale penetration through "
        "leasing channels.")

    pdf.sub("5.2 Phased Commercialization Plan")
    pdf.bold_bullet("Stage 1 -- Academic Seeding (Year 1-Year 2): ",
                    "Immediately post-FDA clearance. Establish KOL collaboration network with "
                    "5-10 top US teaching hospital ICUs. Conduct Clinical Evaluation Programs, "
                    "publish academic papers to build clinical evidence. Present at major "
                    "conferences (SCCM, AARC, ATS).")
    pdf.bold_bullet("Stage 2 -- Leasing Channel Development (Year 2-Year 3): ",
                    "Sign exclusive/priority cooperation agreements with 1-2 major US medical "
                    "equipment leasing companies. Potential partners: Hill-Rom (Baxter), Medline "
                    "Industries, US Med-Equip. Leasing companies handle marketing, installation, "
                    "maintenance; Company B provides clinical training, software updates, tech support.")
    pdf.bold_bullet("Stage 3 -- Scale Expansion (Year 3-Year 5): ",
                    "Expand leasing network to 3-5 companies covering major US regions. "
                    "Simultaneously begin EU CE certification and Japan PMDA registration for "
                    "international markets. Explore OEM/white-label partnerships with ventilator "
                    "manufacturers, embedding MyoBus protocol into mainstream ventilator platforms.")

    pdf.sub("5.3 Revenue Model")
    pdf.table(
        ["Revenue Stream", "Description", "Expected %"],
        [
            ["Device Sales / Leasing", "Bulk sales to leasing cos or rental share", "55-65%"],
            ["Software Subscription (SaaS)", "Clinical decision support, analytics platform", "25-35%"],
            ["Consumables", "Proprietary electrode belts, sensor patches", "10-15%"],
        ],
        [50, 85, 35],
    )

    # ══════════════════════════════════════════════════════════════
    # VI. FUNDING ROADMAP & USE OF PROCEEDS
    # ══════════════════════════════════════════════════════════════
    pdf.sec("VI", "Funding Roadmap & Use of Proceeds")

    pdf.sub("6.1 Seed Round (Complete)")
    pdf.check_badge("SEED ROUND COMPLETE  |  $1.8M  |  Direct Equity  |  Funded")
    pdf.table(
        ["Use of Funds", "Allocation"],
        [
            ["Commission Company A: hardware R&D, data acquisition, China supply chain", "30%"],
            ["FDA 510(k): fees, third-party testing, cybersecurity, clinical data", "40%"],
            ["US operations: team, KOL network, early market development", "30%"],
        ],
        [130, 40],
    )

    pdf.sub("6.2 Series A (Year 1 -- Year 2)")
    pdf.txt(
        "Raise: $8M - $15M\n"
        "Trigger: 510(k) submission filed (sEMG module) + initial KOL clinical data\n"
        "Valuation: $30M - $60M (pre-money)")
    pdf.table(
        ["Use of Funds", "Allocation"],
        [
            ["Commercialization launch: leasing partnerships, initial inventory, training", "40%"],
            ["EIT localization & FDA registration", "25%"],
            ["R&D iteration: next-gen product, software platform, AI algorithms", "20%"],
            ["Operations & talent reserves", "15%"],
        ],
        [130, 40],
    )

    pdf.sub("6.3 Series B (Year 3 -- Year 4)")
    pdf.txt(
        "Raise: $25M - $40M\n"
        "Trigger: EIT 510(k) cleared + leasing partnerships active + initial revenue\n"
        "Valuation: $100M - $200M (pre-money)")
    pdf.table(
        ["Use of Funds", "Allocation"],
        [
            ["Scale manufacturing & inventory", "35%"],
            ["International expansion (EU CE / Japan PMDA registration)", "25%"],
            ["Technology platform upgrade & new product pipeline", "25%"],
            ["Pre-IPO preparation (audit, compliance, IR team)", "15%"],
        ],
        [130, 40],
    )

    pdf.sub("6.4 Pre-IPO / NASDAQ Listing (Year 4 -- Year 5)")
    pdf.txt(
        "Target: NASDAQ IPO in Year 5 (2031).\n\n"
        "IPO readiness criteria:\n"
        "  - Annualized Recurring Revenue (ARR) reaches $15M+\n"
        "  - FDA dual product line cleared\n"
        "  - International markets initiated\n"
        "  - Clear growth curve and expansion pathway\n\n"
        "Why NASDAQ over NYSE: NASDAQ is the preferred listing venue for medical device "
        "innovators, more growth-company-friendly, with numerous med-tech companies "
        "already listed (Inspire Medical, Shockwave Medical, Inari Medical, etc.).")

    pdf.sub("IPO Preparation Timeline")
    pdf.table(
        ["Preparation", "Timeline", "Responsible Party"],
        [
            ["Engage underwriter & legal counsel", "Year 4 Q1", "CEO / CFO"],
            ["Draft SEC S-1 filing", "Year 4 Q2-Q3", "Underwriter + legal team"],
            ["Complete audit (PCAOB standards)", "Year 4 Q3", "External auditor"],
            ["Pre-IPO road show", "Year 4 Q4", "Management + underwriter"],
            ["NASDAQ listing", "Year 5 Q1-Q2", "All parties"],
        ],
        [65, 40, 65],
    )

    # ══════════════════════════════════════════════════════════════
    # VII. MASTER MILESTONE TIMELINE
    # ══════════════════════════════════════════════════════════════
    pdf.sec("VII", "Master Milestone Timeline")
    pdf.txt(
        "The company follows a \"dual-track parallel, stepwise progression\" strategy: "
        "the sEMG product line is driven by Company B's own IP directly toward FDA "
        "registration; the EIT product line requires Series A funding to complete IP "
        "transfer negotiations with Company A and hardware FDA localization before "
        "initiating the registration process.")

    pdf.sub("Phase I -- sEMG Product Line (Company B's Own IP, Seed Round Funded)")
    pdf.table(
        ["Timeline", "Milestone", "Key Tasks", "Funding"],
        [
            ["Y0 Q1-Q2", "Company Formation", "DE C-Corp, commission sEMG R&D,\nUS team build", "Seed Done"],
            ["Y0 Q3-Q4", "FDA Kickoff", "Pre-Sub Meeting, confirm\nIntended Use & Predicate", "--"],
            ["Y0 Q4", "Third-Party Testing", "IEC 60601, EMC, biocompat,\ncybersecurity verification", "--"],
            ["Y1 Q1-Q2", "510(k) Submission", "sEMG 510(k) filed with FDA", "Series A opens"],
            ["Y1 Q3-Q4", "sEMG CLEARED", "sEMG FDA 510(k) Clearance", "--"],
            ["Y1 Q4", "KOL Network", "5-10 teaching hospital ICU\nclinical evaluation partnerships", "--"],
        ],
        [25, 38, 62, 30],
    )

    pdf.sub("Phase II -- EIT Product Line (IP at Company A, Requires Series A)")
    pdf.table(
        ["Timeline", "Milestone", "Key Tasks", "Funding"],
        [
            ["Y1 Q2-Q3", "EIT IP Negotiation", "Initiate IP transfer negotiation\nwith Company A", "Series A ongoing"],
            ["Y1 Q4", "IP Agreement Signed", "Complete EIT IP transfer/license;\nB obtains US market rights", "--"],
            ["Y2 Q1-Q2", "FDA Localization", "Adapt EIT hardware to FDA:\nIEC 62304, cybersecurity", "--"],
            ["Y2 Q2-Q3", "EIT Testing", "IEC 60601, EMC, clinical\nperformance validation data", "--"],
            ["Y2 Q3-Q4", "EIT 510(k) Filed", "EIT 510(k) submitted, predicate:\nTimpel Enlight 2100", "Series A closes"],
            ["Y3 Q1-Q2", "EIT CLEARED", "EIT FDA 510(k) Clearance;\ndual product lines complete", "--"],
        ],
        [25, 40, 62, 28],
    )

    pdf.sub("Phase III -- Commercialization & Capital Markets")
    pdf.table(
        ["Timeline", "Milestone", "Key Tasks", "Funding"],
        [
            ["Y2 Q1-Q2", "sEMG Commercialization", "First market entry, sign first\nleasing partnership", "--"],
            ["Y2 Q3-Q4", "Initial Revenue", "sEMG in hospital ICUs,\nfirst revenue generated", "--"],
            ["Y3 Q1-Q2", "Dual Product Launch", "EIT + sEMG combined, leverage\nintegrated platform advantage", "Series B opens"],
            ["Y3 Q3-Q4", "Scale Expansion", "Leasing network to 3-5 cos,\ninitiate EU CE registration", "--"],
            ["Y4 Q1-Q2", "International Markets", "EU CE obtained, launch\nEuropean market", "Series B closes"],
            ["Y4 Q3-Q4", "IPO Preparation", "Underwriter, PCAOB audit,\nSEC S-1 drafting", "--"],
            ["Y5 Q1-Q2", "NASDAQ IPO", "NASDAQ listing", "IPO"],
        ],
        [25, 42, 58, 30],
    )

    pdf.txt(
        "Note: The EIT product line timeline depends on Series A funding progress and IP "
        "transfer negotiation outcomes. If negotiations proceed smoothly and Series A "
        "arrives on time, Phase II can run in parallel with the latter part of Phase I, "
        "compressing the overall timeline by 6-12 months.")

    # ══════════════════════════════════════════════════════════════
    # VIII. EXIT PATHWAYS & STRATEGIC VALUE
    # ══════════════════════════════════════════════════════════════
    pdf.sec("VIII", "Exit Pathways & Strategic Value")
    pdf.sub("8.1 Primary Exit Pathways")
    pdf.bold_bullet("Path A -- NASDAQ IPO: ",
                    "Preferred path. Target market cap $300M+, providing liquidity exit for "
                    "early investors.")
    pdf.bold_bullet("Path B -- Strategic Acquisition: ",
                    "If market conditions are unfavorable for IPO, accept strategic acquisition "
                    "by a major ventilator company.")

    pdf.sub("8.2 Potential Strategic Acquirers")
    pdf.table(
        ["Company", "Background", "Acquisition Logic"],
        [
            ["Drager", "Germany, ventilator leader", "Fill respiratory monitoring gap"],
            ["Medtronic", "US, med-device giant", "Expand ICU product line"],
            ["Hamilton Medical", "Switzerland, smart ventilation", "Acquire EIT+sEMG closed-loop tech"],
            ["Mindray", "China, patient monitoring leader", "Strengthen global market position"],
            ["GE HealthCare", "US, imaging & monitoring", "Enrich critical care portfolio"],
        ],
        [35, 55, 80],
    )

    pdf.sub("8.3 Core Acquisition Value Proposition")
    pdf.bullet("World's only EIT + sEMG integrated solution fills product line gaps for majors")
    pdf.bullet("MyoBus open protocol ecosystem provides platform-level value")
    pdf.bullet("Plug-and-play modular architecture reduces integration costs")
    pdf.bullet("FDA dual product line clearance eliminates regulatory risk")
    pdf.ln(2)
    pdf.txt(
        "Investor return expectations: Based on seed investment of $1.8M, at Series A "
        "median valuation of $45M, seed investors can expect 10-15x book returns. "
        "If NASDAQ listing is achieved, expected returns increase to 50-100x+.")

    # ══════════════════════════════════════════════════════════════
    # IX. RISK ANALYSIS & MITIGATION
    # ══════════════════════════════════════════════════════════════
    pdf.sec("IX", "Risk Analysis & Mitigation")
    pdf.table(
        ["Risk Category", "Specific Risk", "Mitigation"],
        [
            ["Regulatory", "510(k) approval delay\nor rejection", "Modular filing reduces single-\npoint risk; Pre-Sub confirms path"],
            ["Market", "Long ICU procurement\ndecision cycles", "Leasing model lowers barrier;\nKOL endorsement accelerates adoption"],
            ["Competitive", "Timpel etc. expand\nEIT functionality", "Only EIT+sEMG integration =\ntech moat; MyoBus patent protection"],
            ["Geopolitical", "US-China relations\naffect supply chain", "IP held in US; China is contract\nmanufacturer only"],
            ["Funding", "Funding pace below\nexpectations", "SBIR/STTR federal grants as\nsupplement; control burn rate"],
            ["Talent", "Key technical talent\nattrition", "Equity incentives (ESOP) bind core\nteam; dual-base reduces dependency"],
        ],
        [30, 40, 55],
    )

    # ══════════════════════════════════════════════════════════════
    # X. TEAM & GOVERNANCE
    # ══════════════════════════════════════════════════════════════
    pdf.sec("X", "Team & Governance Structure")
    pdf.sub("10.1 Core Team Plan")
    pdf.table(
        ["Position", "Responsibilities"],
        [
            ["CEO / CTO (Founder)", "Technology direction, FDA strategy, fundraising, strategic planning"],
            ["VP of Regulatory Affairs", "FDA registration full-cycle management, international registration"],
            ["VP of Clinical Affairs", "KOL network, clinical evaluation programs, academic publications"],
            ["VP of Business Development", "Leasing partnerships, channel expansion, OEM negotiations"],
            ["CFO (post-Series B hire)", "Financial management, IPO preparation, investor relations"],
        ],
        [55, 115],
    )

    pdf.sub("10.2 Board of Directors Plan")
    pdf.txt(
        "Initial board: 3-5 members, including founder, investor representatives, and "
        "independent directors (medical device industry experts). As IPO approaches, "
        "expand to 5-7 members with specialized committees (audit, compensation, etc.).")

    pdf.sub("10.3 Equity Structure")
    pdf.txt(
        "Post-seed equity structure is based on $1.8M direct equity financing. The company "
        "reserves a 15-20% option pool (ESOP) for future core talent recruitment and "
        "incentives. Subsequent funding rounds will dilute at market valuations, ensuring "
        "the founding team retains effective control through IPO.")

    # ══════════════════════════════════════════════════════════════
    # XI. FINANCIAL PROJECTION SUMMARY
    # ══════════════════════════════════════════════════════════════
    pdf.sec("XI", "Financial Projection Summary")
    pdf.txt(
        "Five-year revenue projection based on conservative assumptions, "
        "with gradual market penetration increases:")
    pdf.table(
        ["Year", "Installed Base", "Device Rev.", "SaaS Rev.", "Consumables", "Total Rev."],
        [
            ["Year 1", "10-20", "$0.5M", "--", "--", "$0.5M"],
            ["Year 2", "50-100", "$2.5M", "$0.3M", "$0.1M", "$2.9M"],
            ["Year 3", "150-300", "$7.5M", "$1.5M", "$0.5M", "$9.5M"],
            ["Year 4", "400-600", "$15M", "$4M", "$1.5M", "$20.5M"],
            ["Year 5", "800-1,200", "$25M", "$8M", "$3M", "$36M"],
        ],
        [20, 28, 28, 28, 28, 28],
        bold_last=True,
    )
    pdf.txt(
        "Note: Projections are based on US single-market assumptions and do not include "
        "international revenue. Actual figures will be adjusted based on leasing partner "
        "progress and market acceptance.")

    pdf.sub("Key Financial Targets")
    pdf.table(
        ["Metric", "Year 5 Target"],
        [
            ["Annualized Recurring Revenue (ARR)", "$15M+"],
            ["Gross Margin", "70-75%"],
            ["Hospital ICU Customers", "200-400"],
            ["International Revenue Share", "15-25%"],
        ],
        [95, 75],
    )

    # ══════════════════════════════════════════════════════════════
    # APPENDIX
    # ══════════════════════════════════════════════════════════════
    pdf.sec("", "Appendix")
    pdf.sub("A. Key Terminology")
    pdf.table(
        ["Term", "Explanation"],
        [
            ["EIT", "Electrical Impedance Tomography -- non-invasive real-time lung imaging"],
            ["sEMG", "Surface Electromyography -- non-invasive muscle electrical activity monitoring"],
            ["510(k)", "FDA premarket notification; demonstrates substantial equivalence to predicate"],
            ["ARR", "Annual Recurring Revenue -- core SaaS metric"],
            ["PEEP", "Positive End-Expiratory Pressure -- key ventilator treatment parameter"],
            ["KOL", "Key Opinion Leader -- academic/clinical thought leaders"],
            ["CDMO", "Contract Development & Manufacturing Organization"],
        ],
        [25, 145],
    )

    pdf.sub("B. References & Data Sources")
    pdf.bullet("Levine S, et al. Rapid disuse atrophy of diaphragm fibers in mechanically "
               "ventilated humans. NEJM 2008; 358:1327-35.")
    pdf.bullet("Costa ELV, et al. Bedside estimation of recruitable alveolar collapse and "
               "hyperdistension by EIT. Intensive Care Med 2009.")
    pdf.bullet("Society of Critical Care Medicine. ICU cost data and benchmarks.")
    pdf.bullet("FDA 510(k) database and guidance documents.")

    pdf.ln(8)
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(*NAVY)
    pdf.cell(0, 8, "-- END --", align="C")

    # ── write ──
    out = os.path.join(OUT_DIR, "Business_Execution_Plan.pdf")
    pdf.output(out)
    print(f"Generated: {out}")


if __name__ == "__main__":
    build()
