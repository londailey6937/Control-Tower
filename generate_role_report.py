#!/usr/bin/env python3
"""
Generate a consultant role breakdown PDF for the ICU Respiratory Digital Twin project.
Three roles: PMP, FDA Regulatory Lead, US Investor Relations.
"""

from fpdf import FPDF
from datetime import date


class RoleReport(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=20)

    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 6, "Consultant Role & Compensation Analysis  |  ICU Respiratory Digital Twin", align="C")
        self.ln(8)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(140, 140, 140)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")

    def title_page(self):
        self.add_page()
        self.ln(50)
        self.set_font("Helvetica", "B", 28)
        self.set_text_color(30, 60, 120)
        self.cell(0, 14, "Consultant Role &", align="C", new_x="LMARGIN", new_y="NEXT")
        self.cell(0, 14, "Compensation Analysis", align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(12)
        self.set_font("Helvetica", "", 14)
        self.set_text_color(80, 80, 80)
        self.cell(0, 8, "ICU Respiratory Digital Twin", align="C", new_x="LMARGIN", new_y="NEXT")
        self.cell(0, 8, "Medical Device Development Program", align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(20)
        self.set_draw_color(30, 60, 120)
        self.set_line_width(0.8)
        x = 60
        self.line(x, self.get_y(), 210 - x, self.get_y())
        self.ln(12)
        self.set_font("Helvetica", "", 11)
        self.set_text_color(60, 60, 60)
        self.cell(0, 7, "Prepared by: Lon Dailey, PMP", align="C", new_x="LMARGIN", new_y="NEXT")
        self.cell(0, 7, f"Date: {date.today().strftime('%B %d, %Y')}", align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(8)
        self.set_font("Helvetica", "I", 10)
        self.set_text_color(100, 100, 100)
        self.cell(0, 7, "Three-Role Engagement: PMP  |  FDA Regulatory Lead  |  US Investor Relations", align="C")

    def section(self, num, title):
        self.ln(4)
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(30, 60, 120)
        self.cell(0, 8, f"{num}. {title}", new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(30, 60, 120)
        self.set_line_width(0.4)
        self.line(self.l_margin, self.get_y(), 190, self.get_y())
        self.ln(4)

    def sub(self, title):
        self.ln(2)
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(50, 50, 50)
        self.cell(0, 6, title, new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def txt(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(40, 40, 40)
        self.multi_cell(0, 5.5, text, new_x="LMARGIN", new_y="NEXT")

    def task_table(self, headers, rows):
        self.ln(2)
        col_w = [72, 22, 30, 50]
        # Header
        self.set_font("Helvetica", "B", 9)
        self.set_fill_color(30, 60, 120)
        self.set_text_color(255, 255, 255)
        for i, h in enumerate(headers):
            self.cell(col_w[i], 7, h, border=1, fill=True, align="C")
        self.ln()
        # Rows
        self.set_font("Helvetica", "", 9)
        self.set_text_color(40, 40, 40)
        fill = False
        for row in rows:
            if fill:
                self.set_fill_color(240, 244, 250)
            else:
                self.set_fill_color(255, 255, 255)
            for i, val in enumerate(row):
                align = "L" if i == 0 else "C" if i < 3 else "L"
                self.cell(col_w[i], 6.5, val, border=1, fill=True, align=align)
            self.ln()
            fill = not fill
        self.ln(2)

    def summary_table(self, headers, rows, col_w=None):
        self.ln(2)
        if col_w is None:
            col_w = [60, 28, 30, 30, 30]
        # Header
        self.set_font("Helvetica", "B", 9)
        self.set_fill_color(30, 60, 120)
        self.set_text_color(255, 255, 255)
        for i, h in enumerate(headers):
            self.cell(col_w[i], 7, h, border=1, fill=True, align="C")
        self.ln()
        # Rows
        self.set_font("Helvetica", "", 9)
        self.set_text_color(40, 40, 40)
        fill = False
        for row in rows:
            if fill:
                self.set_fill_color(240, 244, 250)
            else:
                self.set_fill_color(255, 255, 255)
            bold = row[0].startswith("TOTAL") or row[0].startswith("Grand")
            if bold:
                self.set_font("Helvetica", "B", 9)
                self.set_fill_color(220, 230, 245)
            for i, val in enumerate(row):
                align = "L" if i == 0 else "C"
                self.cell(col_w[i], 6.5, val, border=1, fill=True, align=align)
            self.ln()
            if bold:
                self.set_font("Helvetica", "", 9)
            fill = not fill
        self.ln(2)


def build():
    pdf = RoleReport()
    pdf.alias_nb_pages()

    # ── TITLE PAGE ─────────────────────────────
    pdf.title_page()

    # ── 1. EXECUTIVE SUMMARY ───────────────────
    pdf.add_page()
    pdf.section(1, "Executive Summary")
    pdf.txt(
        "This document outlines a three-role consulting engagement for the ICU "
        "Respiratory Digital Twin medical device development program. The roles "
        "span the full lifecycle from design control through FDA clearance to "
        "investor relations, reflecting the cross-functional demands of bringing "
        "a Class II medical device to market.\n\n"
        "A core principle: startups do not pay for 'project management' as a "
        "service category. They pay for three measurable outcomes:\n\n"
        "  - Risk Reduction: lowering the probability of FDA rejection, which\n"
        "    can cost 12+ months and $500K+ in rework and resubmission\n\n"
        "  - Time Compression: collapsing the design-to-clearance timeline by\n"
        "    6-12 months through parallel-track execution and gate discipline\n\n"
        "  - Team Alignment: preventing burn waste -- the silent killer of\n"
        "    startup cash -- by keeping engineering, regulatory, and business\n"
        "    functions synchronized on a single source of truth\n\n"
        "Every task, hour, and dollar described in this document is evaluated "
        "against those three outcomes. If an activity does not reduce risk, "
        "compress time, or align the team, it does not belong in the engagement.\n\n"
        "The three roles are:\n\n"
        "  1. Project Management Professional (PMP) -- Design control, gate\n"
        "     reviews, team coordination, timeline/budget management\n\n"
        "  2. FDA Regulatory Lead -- 510(k) submission strategy, predicate\n"
        "     analysis, FDA communications, QMS compliance\n\n"
        "  3. US Investor Relations -- Fundraising strategy, investor\n"
        "     communications, pitch materials, due diligence support\n\n"
        "Each role is broken down by task, estimated weekly hours, and market-rate "
        "compensation. The analysis assumes a 23-month program timeline (M+0 through "
        "M+23) with varying intensity across phases.")

    # ── 2. ROLE 1: PMP ─────────────────────────
    pdf.add_page()
    pdf.section(2, "Role 1: Project Management Professional (PMP)")

    pdf.sub("2.1 Scope of Responsibilities")
    pdf.txt(
        "The PMP serves as the central authority for design control governance, "
        "team coordination, and program execution. This role is the backbone of "
        "the Control Tower dashboard and the single point of accountability for "
        "the project's adherence to 21 CFR 820.30 design control requirements.\n\n"
        "Value delivered through this role:\n\n"
        "  Risk Reduction -- Gate reviews catch design control gaps before they\n"
        "  become 510(k) deficiencies. A missed DHF item discovered during FDA\n"
        "  review costs 3-6 months; caught at a gate review, it costs a week.\n\n"
        "  Time Compression -- Dual-track execution (technical + regulatory in\n"
        "  parallel) saves 6-12 months vs. sequential waterfall approaches that\n"
        "  most first-time device companies default to.\n\n"
        "  Team Alignment -- The Control Tower dashboard eliminates the 'status\n"
        "  meeting tax' and gives every stakeholder real-time visibility into\n"
        "  milestones, risks, and burn rate -- preventing misaligned effort.\n\n"
        "Key responsibilities:\n\n"
        "  - Gate review preparation and decision authority (G1-G6)\n"
        "  - Design History File (DHF) oversight and maintenance\n"
        "  - Change Request (CR) review, approval, and tracking\n"
        "  - Risk register management (ISO 14971 compliance)\n"
        "  - Milestone tracking across Technical and Regulatory tracks\n"
        "  - Budget vs. actual monitoring and variance reporting\n"
        "  - Resource allocation and capacity planning\n"
        "  - Supplier qualification oversight\n"
        "  - CAPA log management and closure tracking\n"
        "  - Stakeholder input review and response\n"
        "  - Weekly status reporting and escalation management\n"
        "  - Audit trail integrity and export for compliance")

    pdf.sub("2.2 Task Breakdown & Time Allocation")
    pdf.task_table(
        ["Task", "Hrs/Wk", "Phase", "Notes"],
        [
            ["Gate review prep & facilitation", "4", "All", "6 gates across 23 months"],
            ["DHF oversight & CR review", "3", "All", "Continuous design control"],
            ["Risk register maintenance", "2", "All", "ISO 14971 updates"],
            ["Milestone & timeline tracking", "2", "All", "Dashboard management"],
            ["Budget monitoring & reporting", "1.5", "All", "Monthly variance review"],
            ["Team coordination & meetings", "3", "All", "Cross-functional sync"],
            ["Supplier qualification", "1", "M+0-M+6", "Initial vendor setup"],
            ["CAPA management", "1.5", "M+3+", "Post-testing phase"],
            ["Stakeholder communications", "2", "All", "Input review & response"],
            ["Audit trail & compliance docs", "1", "All", "21 CFR Part 11 prep"],
        ],
    )

    pdf.sub("2.3 Time Summary")
    pdf.txt(
        "Average: 20 hours/week\n"
        "Peak periods (gate reviews, submission prep): 25-30 hours/week\n"
        "Lighter periods (steady-state execution): 15-18 hours/week")

    pdf.sub("2.4 Market Rate")
    pdf.txt(
        "Medical device PMP consultants with design control experience:\n\n"
        "  Market range:     $150 - $250/hour\n"
        "  Recommended rate: $175/hour\n"
        "  Justification:    PMP certification + medical device domain + FDA\n"
        "                    design control experience + technical publications\n"
        "                    leadership")

    # ── 3. ROLE 2: FDA REGULATORY LEAD ─────────
    pdf.add_page()
    pdf.section(3, "Role 2: FDA Regulatory Lead")

    pdf.sub("3.1 Scope of Responsibilities")
    pdf.txt(
        "The FDA Regulatory Lead owns the regulatory strategy and execution for "
        "the 510(k) pathway. This includes predicate device analysis, FDA "
        "communications, submission package preparation, and ongoing compliance "
        "with applicable standards (IEC 62304, IEC 60601-1, ISO 14971, 21 CFR 820).\n\n"
        "A critical insight: a 510(k) submission is fundamentally a technical "
        "publication. The FDA does not review your device in person -- they review "
        "your documentation. The submission package IS the product under review. "
        "This is why the PMP's 14 years of technical publications experience and "
        "BS in Technical Communication are directly relevant: the same skills that "
        "produce clear, structured, audience-aware engineering documentation are "
        "exactly the skills that produce a clean 510(k) filing. The FDA regulatory "
        "process is not a foreign discipline -- it is another application of a core "
        "professional skill set.\n\n"
        "Key responsibilities:\n\n"
        "  - 510(k) submission strategy development\n"
        "  - Predicate device identification and equivalence analysis\n"
        "  - Pre-submission (Q-Sub) meeting preparation and FDA correspondence\n"
        "  - Regulatory standards matrix management (IEC/ISO/21 CFR)\n"
        "  - Software classification and IEC 62304 lifecycle documentation\n"
        "  - Biocompatibility assessment coordination (ISO 10993)\n"
        "  - EMC/electrical safety testing oversight (IEC 60601-1)\n"
        "  - Clinical evidence compilation and literature review\n"
        "  - eSTAR submission package preparation\n"
        "  - FDA reviewer question responses\n"
        "  - Post-submission deficiency response management\n"
        "  - 510(k) clearance follow-through and labeling review")

    pdf.sub("3.2 Task Breakdown & Time Allocation")
    pdf.task_table(
        ["Task", "Hrs/Wk", "Phase", "Notes"],
        [
            ["Predicate analysis & literature", "4", "M+0-M+3", "Front-loaded research"],
            ["Regulatory strategy & standards", "3", "M+0-M+6", "Framework setup"],
            ["Pre-Sub (Q-Sub) preparation", "5", "M+1-M+2", "FDA meeting prep"],
            ["510(k) submission drafting", "8", "M+4-M+9", "Peak writing phase"],
            ["Testing protocol review", "2", "M+3-M+8", "V&V oversight"],
            ["Standards compliance tracking", "2", "All", "IEC/ISO matrix"],
            ["FDA correspondence", "2", "M+2+", "Q-Sub + deficiency mgmt"],
            ["eSTAR package assembly", "6", "M+5-M+6", "Submission prep sprint"],
            ["Post-submission management", "3", "M+6-M+9", "Deficiency responses"],
            ["Clearance & labeling review", "2", "M+9-M+12", "Final clearance"],
        ],
    )

    pdf.sub("3.3 Time Summary")
    pdf.txt(
        "Average: 15 hours/week\n"
        "Peak periods (submission drafting, M+4-M+9): 25-30 hours/week\n"
        "Lighter periods (post-clearance): 5-8 hours/week\n\n"
        "Note: Regulatory load is heavily front-loaded for sEMG (first 510(k)) "
        "and ramps again for the full Digital Twin platform submission.")

    pdf.sub("3.4 Market Rate")
    pdf.txt(
        "FDA regulatory affairs consultants for Class II medical devices:\n\n"
        "  Market range:     $200 - $350/hour\n"
        "  Recommended rate: $225/hour\n"
        "  Justification:    510(k) submission experience + predicate analysis\n"
        "                    + multi-standard compliance (IEC 62304, 60601,\n"
        "                    ISO 14971, 21 CFR 820) + FDA Q-Sub experience")

    # ── 4. ROLE 3: US INVESTOR RELATIONS ───────
    pdf.add_page()
    pdf.section(4, "Role 3: US Investor Relations")

    pdf.sub("4.1 Scope of Responsibilities")
    pdf.txt(
        "The US Investor Relations lead manages the North American fundraising "
        "pipeline, investor communications, and due diligence support. This role "
        "bridges the technical/regulatory program with the financial stakeholders "
        "who fund it.\n\n"
        "Key responsibilities:\n\n"
        "  - Fundraising strategy and target investor identification\n"
        "  - Pitch deck development and maintenance (EN + CN)\n"
        "  - Investor outreach and relationship management\n"
        "  - Due diligence package preparation\n"
        "  - Term sheet negotiation support\n"
        "  - Board/investor update communications\n"
        "  - Financial modeling and runway projections\n"
        "  - US market entry strategy documentation\n"
        "  - SEC/regulatory compliance for fundraising (if applicable)\n"
        "  - Coordination with legal counsel on corporate structure\n"
        "  - Delaware incorporation and corporate governance support")

    pdf.sub("4.2 Task Breakdown & Time Allocation")
    pdf.task_table(
        ["Task", "Hrs/Wk", "Phase", "Notes"],
        [
            ["Investor identification & CRM", "3", "All", "Pipeline management"],
            ["Pitch deck & materials", "3", "M+0-M+3", "Initial creation + updates"],
            ["Investor meetings & follow-up", "4", "All", "Avg 2-3 meetings/week"],
            ["Due diligence support", "3", "M+3-M+9", "Data room preparation"],
            ["Financial modeling & runway", "2", "All", "Monthly updates"],
            ["Board/investor updates", "2", "M+3+", "Quarterly reporting"],
            ["Term sheet & legal coord", "2", "M+3-M+6", "Negotiation phase"],
            ["Market strategy documentation", "1.5", "M+0-M+6", "US market positioning"],
            ["Corporate governance", "1", "M+0-M+3", "Delaware setup, bylaws"],
            ["Ad hoc investor requests", "1.5", "All", "Responsive support"],
        ],
    )

    pdf.sub("4.3 Time Summary")
    pdf.txt(
        "Average: 12 hours/week\n"
        "Peak periods (active fundraising rounds): 20-25 hours/week\n"
        "Lighter periods (between rounds): 6-8 hours/week\n\n"
        "Note: IR intensity correlates with fundraising milestones. Expect peak "
        "activity around seed/Series A closes and during investor due diligence.")

    pdf.sub("4.4 Market Rate")
    pdf.txt(
        "Investor relations / fundraising consultants for medical device startups:\n\n"
        "  Market range:     $150 - $275/hour\n"
        "  Recommended rate: $175/hour\n"
        "  Justification:    Medical device domain knowledge + US corporate\n"
        "                    structure expertise + financial modeling\n"
        "                    + pitch development")

    # ── 5. COMBINED ANALYSIS ───────────────────
    pdf.add_page()
    pdf.section(5, "Combined Time & Compensation Analysis")

    pdf.sub("5.1 Weekly Hours Summary")
    pdf.summary_table(
        ["Role", "Avg Hrs/Wk", "Peak Hrs/Wk", "Low Hrs/Wk", "Rate/Hr"],
        [
            ["PMP", "20", "25-30", "15-18", "$175"],
            ["FDA Regulatory Lead", "15", "25-30", "5-8", "$225"],
            ["US Investor Relations", "12", "20-25", "6-8", "$175"],
            ["TOTAL (Combined)", "47", "70-85", "26-34", "Blended"],
        ],
    )

    pdf.sub("5.2 Market-Rate Compensation (Reference Only)")
    pdf.txt("If each role were billed separately at market rates:")
    pdf.summary_table(
        ["Role", "Hrs/Month", "Rate", "Monthly", "Annual"],
        [
            ["PMP", "87", "$175", "$15,225", "$182,700"],
            ["FDA Regulatory Lead", "65", "$225", "$14,625", "$175,500"],
            ["US Investor Relations", "52", "$175", "$9,100", "$109,200"],
            ["TOTAL (Market Rate)", "204", "Blended", "$38,950", "$467,400"],
        ],
    )

    pdf.sub("5.3 Proposed Single Monthly Fee (Cash-Conserving)")
    pdf.txt(
        "The PMP does not expect to receive full market-rate compensation for all "
        "three roles simultaneously. The intent is to reduce cash pressure on the "
        "company during the critical pre-revenue phase, with the difference between "
        "the proposed fee and market rate compensated through founder equity in the "
        "Delaware C-Corp.\n\n"
        "Proposed consolidated fee covering all three roles:")
    pdf.summary_table(
        ["Model", "Monthly Fee", "Annual", "vs. Market", "Savings"],
        [
            ["Market rate (3 roles)", "$38,950", "$467,400", "--", "--"],
            ["Proposed single fee", "$10,000", "$120,000", "-74%", "$347,400/yr"],
        ],
        col_w=[50, 30, 30, 28, 30],
    )

    pdf.txt(
        "The single monthly fee of $10,000 covers all three roles -- PMP, FDA "
        "Regulatory Lead, and US Investor Relations -- under one invoice. This "
        "is 74% below market rate and is designed to:\n\n"
        "  - Preserve cash runway for the company\n"
        "  - Keep monthly burn manageable ($45K current + $10K PMP = $55K)\n"
        "  - Extend runway: $320K / $55K = 5.8 months (vs. $320K / $84K = 3.8 mo\n"
        "    if PMP were billed at market rate)\n"
        "  - Demonstrate PMP commitment as a founding team member, not a vendor\n\n"
        "Framed differently: the company is not paying $10,000/month for 'project\n"
        "management.' It is paying for risk reduction (avoiding a $500K+ FDA\n"
        "rejection), time compression (6-12 months faster to clearance), and team\n"
        "alignment (zero wasted engineering cycles on misunderstood requirements).\n"
        "These are the three outcomes that justify any PM engagement in a medical\n"
        "device startup -- and they are worth multiples of the proposed fee.\n\n"
        "The $28,950/month gap between market rate and proposed fee ($347,400/year) "
        "is the PMP's investment in the company, compensated through equity.")

    pdf.sub("5.4 Impact on Company Burn Rate & Runway")
    pdf.summary_table(
        ["Scenario", "Monthly Burn", "Cash", "Runway"],
        [
            ["Current (no PMP)", "$45,000", "$320,000", "7.1 months"],
            ["+ PMP at Market Rate", "$83,950", "$320,000", "3.8 months"],
            ["+ PMP at Proposed Fee", "$55,000", "$320,000", "5.8 months"],
            ["+ PMP + Lawrence $1M", "$55,000", "$1,320,000", "24.0 months"],
        ],
        col_w=[52, 32, 30, 30],
    )
    pdf.txt(
        "At the proposed $10,000/month fee, the company retains 5.8 months of "
        "runway without additional investment. With Lawrence's anticipated $1M "
        "investment (currently under due diligence), runway extends to 24 months "
        "-- providing 6 months of margin beyond the 18-month 510(k) clearance "
        "target for the sEMG module.")

    pdf.sub("5.5 Equivalent Full-Time Analysis")
    pdf.txt(
        "At 47 average hours/week across three roles, this represents:\n\n"
        "  - 1.175 FTE (based on 40-hour standard work week)\n"
        "  - Effectively a full-time-plus engagement\n"
        "  - Peak periods (gate reviews + submission + fundraising overlap)\n"
        "    could reach 70-85 hours/week\n\n"
        "The PMP is accepting $10,000/month for 1.17 FTE of senior-level work. "
        "This equates to an effective rate of $23/hour -- approximately 87% below "
        "the blended market rate. The equity stake compensates this investment.")

    # ── 6. PHASE-BASED INTENSITY ───────────────
    pdf.add_page()
    pdf.section(6, "Phase-Based Intensity Map")

    pdf.txt(
        "Hours/week vary significantly across the 23-month program. The table below "
        "shows estimated intensity by phase:")

    pdf.summary_table(
        ["Phase", "PMP", "Regulatory", "IR", "Combined"],
        [
            ["M+0 to M+3  (Setup)", "22", "18", "15", "55"],
            ["M+4 to M+6  (Build)", "20", "28", "12", "60"],
            ["M+6 to M+9  (Submit)", "25", "30", "10", "65"],
            ["M+9 to M+12 (Clear)", "18", "10", "20", "48"],
            ["M+12 to M+18 (Scale)", "20", "15", "15", "50"],
            ["M+18 to M+23 (Full)", "25", "25", "12", "62"],
        ],
    )

    pdf.txt(
        "Key observations:\n\n"
        "  - M+4 through M+9 is the highest-intensity period: simultaneous 510(k)\n"
        "    submission writing, gate reviews (G3-G4), and investor due diligence\n\n"
        "  - M+9 to M+12 sees regulatory load drop after sEMG clearance, but IR\n"
        "    picks up as clearance milestone triggers fundraising activity\n\n"
        "  - M+18 to M+23 is the second peak: full Digital Twin platform 510(k)\n"
        "    submission plus continued investor relations for growth capital")

    # ── 7. EQUITY & SHARE DISTRIBUTION ─────────
    pdf.add_page()
    pdf.section(7, "Delaware C-Corp Share Distribution")

    pdf.sub("7.1 Equity as Compensation for Below-Market Fees")
    pdf.txt(
        "NOTE: The equity allocation described in this section is the PMP's "
        "proposal. No equity terms have been agreed upon by any party. This "
        "section presents the rationale and is intended as a starting point for "
        "negotiation.\n\n"
        "The PMP's proposed $10,000/month fee is 74% below the combined market "
        "rate of $38,950/month. Over an 18-month engagement through 510(k) "
        "clearance, this represents:\n\n"
        "  Market-rate value delivered:     $38,950 x 18 = $701,100\n"
        "  Cash compensation received:      $10,000 x 18 = $180,000\n"
        "  Difference (PMP's investment):   $521,100\n\n"
        "This $521,100 gap is the PMP's sweat equity investment in the company. "
        "The proposal is to compensate this gap through founder shares in Company "
        "B USA (Delaware C-Corp), aligning the PMP's financial upside with the "
        "success of the venture.")

    pdf.sub("7.2 Proposed Cap Table -- Company B USA")
    pdf.txt(
        "Authorized shares: 10,000,000 common + preferred\n\n"
        "Based on Lawrence Liu's anticipated $1M Series Seed investment at a\n"
        "$6.67M post-money valuation ($5.67M pre-money), the proposed cap table\n"
        "is structured as follows:")
    pdf.summary_table(
        ["Party", "Shares", "Ownership", "Type", "Contribution"],
        [
            ["Dr. Dai (Inventor/CTO)", "5,000,000", "50%", "Common", "IP + Technical Lead"],
            ["Lawrence Liu (Investor)", "1,500,000", "15%", "Preferred", "$1M Cash Investment"],
            ["Lon Dailey (PMP)*", "1,500,000", "15%", "Common", "PMP+Reg+IR (3 roles)"],
            ["Employee Option Pool", "2,000,000", "20%", "Reserved", "Future hires"],
            ["TOTAL", "10,000,000", "100%", "", ""],
        ],
        col_w=[48, 24, 22, 22, 48],
    )
    pdf.txt(
        "* PMP equity allocation is a proposal and has not been agreed upon by "
        "any party. Subject to negotiation.")

    pdf.sub("7.3 How Shares Would Balance the Fee Discount")
    pdf.txt(
        "If the proposed 15% equity stake is accepted, it would compensate the "
        "gap between market rate and the proposed monthly fee. The potential "
        "value exchange at various company valuations:\n\n"
        "  At $6.67M (current round):  15% = $1,000,000 (1.9x the $521K gap)\n"
        "  At $10M company valuation:   15% = $1,500,000 (2.9x the gap)\n"
        "  At $20M company valuation:   15% = $3,000,000 (5.8x the gap)\n"
        "  At $50M acquisition:         15% = $7,500,000\n\n"
        "The equity would compensate the PMP only if the company succeeds. This "
        "is the fundamental startup trade-off: lower cash now in exchange for "
        "outsized upside later. The PMP bears real financial risk alongside the "
        "other founders.\n\n"
        "Note: The current round valuation of $6.67M post-money is set by "
        "Lawrence's $1M investment for 15%. At this valuation, the PMP's "
        "proposed 15% stake has a paper value of $1M -- approximately 1.9x "
        "the $521K market-rate gap, reflecting the risk premium appropriate "
        "for a pre-revenue, pre-clearance medical device startup.")

    pdf.sub("7.4 Vesting Schedule")
    pdf.txt(
        "  Total shares:       1,500,000\n"
        "  Vesting period:     4 years\n"
        "  Cliff:              1 year (no shares vest in first 12 months)\n"
        "  Post-cliff:         Monthly vesting (1/48 per month)\n"
        "  Acceleration:       Double-trigger on change of control\n"
        "                      (if acquired AND PMP is terminated, 100% vests)\n\n"
        "  Month 0-11:         0 shares vested (cliff period)\n"
        "  Month 12:           375,000 shares vest (25% cliff release)\n"
        "  Month 13-48:        31,250 shares vest each month\n"
        "  Month 48:           1,500,000 shares fully vested\n\n"
        "If the PMP departs before the 1-year cliff, all shares are forfeited. "
        "This protects the company while giving the PMP meaningful ownership for "
        "sustained contribution.")

    pdf.sub("7.5 Share Classes Explained")
    pdf.txt(
        "  Common Stock (Dr. Dai, Lon Dailey, Option Pool):\n"
        "    - Issued for IP contributions, sweat equity, and services\n"
        "    - Carries voting rights (1 share = 1 vote)\n"
        "    - Last in line during liquidation\n"
        "    - Lower price per share (typically $0.001 at founding)\n\n"
        "  Preferred Stock (Lawrence Liu -- $1M Series Seed):\n"
        "    - Issued to investors in exchange for cash\n"
        "    - Price per share: $0.667 ($1M / 1,500,000 shares)\n"
        "    - 1x non-participating liquidation preference: Lawrence gets his\n"
        "      $1M back FIRST in any liquidation or acquisition\n"
        "    - Pro-rata rights in future financing rounds\n"
        "    - Anti-dilution protection (weighted average)\n"
        "    - Convertible to common at Lawrence's option\n"
        "    - Information rights: quarterly financials, annual budget")

    pdf.sub("7.6 Board Governance")
    pdf.txt(
        "  Board of Directors (3 seats):\n"
        "    Seat 1: Lon Dailey (US citizen) -- Elected by common holders\n"
        "    Seat 2: Dr. Dai (Inventor) -- Elected by common holders\n"
        "    Seat 3: Independent Director -- Mutually agreed\n\n"
        "  Lawrence Liu: Board Observer (non-voting) + Protective Provisions\n"
        "    - Observer seat avoids CFIUS 'foreign control' trigger\n"
        "    - Protective provisions give veto on: dissolution, IP sale,\n"
        "      new debt >$100K, senior equity issuance\n\n"
        "  US-person board majority (2 of 3 seats) satisfies CFIUS requirements\n"
        "  while preserving Lawrence's economic rights and governance influence.\n\n"
        "  NOTE: Dr. Dai's US immigration status is not yet confirmed. He has\n"
        "  relatives in the US who may hold citizenship or green cards. If Dr. Dai\n"
        "  is a US person, the board has 2 confirmed US seats (Lon + Dr. Dai)\n"
        "  without relying on the independent director. If Dr. Dai is a foreign\n"
        "  national, US majority requires the independent director to be a US\n"
        "  person. Either scenario is workable -- but Dr. Dai's status must be\n"
        "  confirmed before finalizing the CFIUS filing strategy.")

    # ── 8. CONSULTANT BACKGROUND & QUALIFICATIONS ──
    pdf.add_page()
    pdf.section(8, "Consultant Background & Qualifications")

    pdf.sub("8.1 Technical Publications Leadership")
    pdf.txt(
        "The PMP brings 14 years of professional technical publications "
        "experience across semiconductor, industrial, and engineering sectors:\n\n"
        "  Technical Publications Manager, Cascade Microtech (1998-2004):\n"
        "    - Led a team of technical writers and design drafters\n"
        "    - Oversaw creation and maintenance of technical manuals and\n"
        "      documentation systems for semiconductor wafer probing equipment\n"
        "    - Improved documentation workflows and quality standards across\n"
        "      departments\n"
        "    - 6 years managing publications for precision engineering products\n"
        "      -- systems that, like medical devices, demand accuracy,\n"
        "      traceability, and regulatory awareness\n\n"
        "  Technical Writer, Cascade Microtech (1994-1998):\n"
        "    - Produced detailed technical documentation for wafer probing and\n"
        "      semiconductor testing systems\n"
        "    - Collaborated with engineering teams to ensure accuracy and clarity\n"
        "    - Developed user manuals, service guides, and training materials\n\n"
        "  Contract Technical Writer (1990-1994):\n"
        "    - Intel, Cascade Microtech, Lattice Semiconductor, and others\n"
        "    - Standardized documentation practices across organizations\n"
        "    - Delivered high-quality materials under tight deadlines\n\n"
        "  Field Controls Engineer, Coe Manufacturing (1984-1990):\n"
        "    - Programmed and maintained PLC-controlled machinery\n"
        "    - Troubleshot and optimized industrial control systems\n"
        "    - Hands-on engineering foundation before transitioning to\n"
        "      technical publications")

    pdf.sub("8.2 Education")
    pdf.txt(
        "  BS in Technical Communication\n"
        "    Charter Oak College, New Britain, Connecticut (2002)\n\n"
        "  AS in Hardware / Software Engineering\n"
        "    Portland Community College, Portland, Oregon (1984)\n\n"
        "  Project Management Professional (PMP)\n"
        "    Stanford University (2000)\n\n"
        "The combination is deliberately relevant. The technical communication "
        "degree provides the writing and documentation rigor that FDA submissions "
        "demand -- structure, audience awareness, precision, and traceability. The "
        "engineering degree provides the ability to understand the underlying device "
        "technology: not just document it, but evaluate it critically. Together, they "
        "produce someone who can both comprehend a device's technical architecture "
        "and translate it into the clear, structured narrative that FDA reviewers "
        "require for a 510(k) determination.")

    pdf.sub("8.3 FDA Submission Experience")
    pdf.txt(
        "The PMP has prior direct experience with the 510(k) submission process, "
        "having initiated a 510(k) application for a previous medical device "
        "concept. The submission was not completed because the device did not "
        "advance to prototype -- a disciplined decision that reflects understanding "
        "of when to proceed and when to pivot. The process provided hands-on "
        "exposure to:\n\n"
        "  - Predicate device research and substantial equivalence analysis\n"
        "  - FDA submission structure and eSTAR requirements\n"
        "  - Regulatory standards mapping\n"
        "  - The documentation rigor required for a successful filing\n\n"
        "Since that initial experience, the PMP has undertaken extensive self-study "
        "of current FDA processes, updated regulations, and the specific standards "
        "applicable to the Digital Twin program (IEC 62304, IEC 60601-1, ISO 14971, "
        "21 CFR 820). This re-education -- combined with 14 years of technical "
        "publications expertise -- creates confidence that the FDA submission "
        "process is a natural extension of existing skills, not a new discipline "
        "to learn from scratch.")

    pdf.sub("8.4 Why Technical Publications Is the Core Differentiator")
    pdf.txt(
        "Most startups hire a 'regulatory consultant' for their 510(k). What they "
        "actually need is someone who can write -- clearly, precisely, and with an "
        "understanding of how a regulatory reviewer reads.\n\n"
        "A 510(k) submission is, at its foundation, a technical publication. "
        "Consider what causes FDA submissions to fail or trigger Additional "
        "Information (AI) requests:\n\n"
        "  - Poor structure and organization (adds 3-6 months per AI request)\n"
        "  - Ambiguous intended use statements\n"
        "  - Incomplete predicate comparison matrices\n"
        "  - Missing cross-references and traceability\n"
        "  - Unclear testing rationale and acceptance criteria\n\n"
        "Every one of these is a documentation problem. A technical publications "
        "professional solves these by instinct -- it is what they have been trained "
        "and practiced to do for their entire career.\n\n"
        "The PMP's specific advantages:\n\n"
        "  Structure & Clarity: 14 years of producing organized, navigable\n"
        "  technical documents -- user manuals, service guides, and system\n"
        "  documentation that must be unambiguous on first reading.\n\n"
        "  Audience Awareness: Technical writers are trained to write for a\n"
        "  specific reader. FDA reviewers have a decision framework (substantial\n"
        "  equivalence) -- the submission must be structured to answer their\n"
        "  questions before they ask them.\n\n"
        "  Document Control: Managing a 200+ page submission with cross-\n"
        "  references, version control, and traceability is a publications\n"
        "  management problem -- identical to managing technical manual sets\n"
        "  for complex engineering products.\n\n"
        "  Team Management: Leading writers and drafters at Cascade Microtech\n"
        "  required the same coordination skills needed to compile inputs from\n"
        "  engineering, testing, and clinical teams into a cohesive submission.\n\n"
        "The FDA process is just another excursion for someone whose career has "
        "been built on translating complex technical concepts into clear, "
        "structured, audience-appropriate documentation. The subject matter "
        "changes; the professional discipline does not.")

    # ── 9. RECOMMENDATION ──────────────────────
    pdf.add_page()
    pdf.section(9, "Recommendation")
    pdf.txt(
        "The recommended compensation structure is:\n\n"
        "  Single Monthly Fee:   $10,000/month (all three roles combined)\n"
        "  Equity Stake:         15% founder shares (proposed, subject to\n"
        "                        negotiation -- 1,500,000 common shares)\n"
        "  Vesting:              4-year vest, 1-year cliff, monthly thereafter\n"
        "  Contracting Entity:   Arch Medical Management, LLC (Oregon)\n"
        "  Engagement Type:      Independent contractor (1099)\n"
        "  Invoice:              Monthly, Net-15 payment terms\n"
        "  Duration:             Through 510(k) clearance (est. 18 months)\n\n"
        "This structure achieves three objectives:\n\n"
        "  1. Cash Preservation -- At $10,000/month (vs. $38,950 market rate),\n"
        "     the company saves $347,400/year. Combined with Lawrence's anticipated\n"
        "     $1M investment, this extends runway to ~24 months.\n\n"
        "  2. Aligned Incentives -- The PMP's primary upside is equity, not cash.\n"
        "     The PMP succeeds only if the company succeeds. This is the same\n"
        "     incentive structure as the inventor (Dr. Dai) and the investor\n"
        "     (Lawrence Liu) -- all three founders share the same outcome.\n\n"
        "  3. Founder Commitment -- The PMP is not a vendor billing hours.\n"
        "     At 15% equity with a 4-year vest, the PMP is a co-founder who\n"
        "     has accepted a $521K compensation reduction over 18 months as\n"
        "     a personal investment in the company.\n\n"
        "Underlying all three: startups do not pay for 'PM' -- they pay for risk\n"
        "reduction (lowering FDA rejection probability from typical first-timer\n"
        "rates of 30-40% to under 10%), time compression (6-12 months saved vs.\n"
        "ad-hoc execution), and team alignment (eliminating the burn waste that\n"
        "kills underfunded startups). This engagement delivers all three.\n\n"
        "The three-role structure is effectively a fractional C-suite engagement:\n"
        "the PMP role is a fractional VP of Program Management, the Regulatory\n"
        "role is a fractional VP of Regulatory Affairs, and the IR role is a\n"
        "fractional VP of Investor Relations.")

    pdf.sub("9.1 Summary: Cash + Equity Compensation (Proposed)")
    pdf.txt(
        "NOTE: Equity figures below reflect the PMP's proposal and are subject "
        "to negotiation with all parties.")
    pdf.summary_table(
        ["Component", "Amount", "Period", "Purpose"],
        [
            ["Monthly cash fee", "$10,000/mo", "18 months", "Living expenses"],
            ["Total cash", "$180,000", "18 months", "74% below market"],
            ["Equity (proposed)", "1,500,000 sh", "4-yr vest", "Founder shares"],
            ["Equity (at $6.67M)", "$1,000,000", "Paper value", "1.9x market gap"],
            ["Equity (at $20M)", "$3,000,000", "Potential", "5.8x market gap"],
        ],
        col_w=[46, 32, 30, 48],
    )

    pdf.sub("9.2 What the Company Gets")
    pdf.txt(
        "For $10,000/month, Company B USA receives:\n\n"
        "  - 47 hours/week of senior consulting across three critical functions\n"
        "  - PMP-certified project management with medical device design control\n"
        "  - FDA 510(k) regulatory strategy and submission execution\n"
        "  - 14 years of technical publications leadership -- the core skill\n"
        "    that produces clean, first-pass 510(k) submissions\n"
        "  - BS in Technical Communication + AS in Hardware/Software Engineering\n"
        "  - US investor relations, pitch materials, and fundraising support\n"
        "  - A US-citizen board member (critical for CFIUS compliance)\n"
        "  - A co-founder whose financial interests are fully aligned\n\n"
        "But more importantly, the company is buying three outcomes:\n\n"
        "  1. Risk Reduction -- An experienced PMP with FDA design control\n"
        "     knowledge reduces 510(k) rejection risk from the 30-40%\n"
        "     first-time failure rate to under 10%. A single rejection\n"
        "     costs $500K+ in rework, retesting, and delayed revenue.\n\n"
        "  2. Time Compression -- Dual-track execution, disciplined gate\n"
        "     reviews, and proactive deficiency prevention save 6-12 months\n"
        "     on the path to clearance. At $55K/month burn, each month\n"
        "     saved is $55K preserved in runway.\n\n"
        "  3. Team Alignment -- The Control Tower dashboard and weekly gate\n"
        "     cadence eliminate misaligned effort. When engineering, regulatory,\n"
        "     and business move in lockstep, zero dollars are burned on work\n"
        "     that gets thrown away due to miscommunication.\n\n"
        "Market cost for these services hired separately: $38,950/month.\n"
        "Proposed company cost with this structure: $10,000/month + 15% equity\n"
        "(equity subject to negotiation).")

    pdf.sub("9.3 Legal Documents Required (Upon Agreement)")
    pdf.txt(
        "  1. Restricted Stock Agreement (Company B USA -> Lon Dailey)\n"
        "     - Share count and vesting terms per negotiated equity agreement\n"
        "     - 83(b) election filed within 30 days of grant\n\n"
        "  2. Series Seed Preferred Stock Purchase Agreement\n"
        "     - Lawrence Liu: $1M for 1,500,000 preferred shares\n"
        "     - $6.67M post-money valuation\n"
        "     - 1x non-participating liquidation preference\n"
        "     - Legal cost: est. $15-25K (company expense)\n\n"
        "  3. Master Services Agreement (Company B USA -> Arch Medical Mgmt)\n"
        "     - Covers all three roles under one contract\n"
        "     - $10,000/month fixed fee, Net-15\n"
        "     - Work product IP assigned to Company B USA\n"
        "     - Mutual NDA, 30-day termination notice\n\n"
        "  4. Board Consent Resolution\n"
        "     - Approving the equity grants, preferred stock sale, and MSA\n"
        "     - Documenting the fair market value determination")

    pdf.ln(8)
    pdf.set_draw_color(30, 60, 120)
    pdf.set_line_width(0.4)
    pdf.line(pdf.l_margin, pdf.get_y(), 190, pdf.get_y())
    pdf.ln(6)
    pdf.set_font("Helvetica", "I", 10)
    pdf.set_text_color(80, 80, 80)
    pdf.multi_cell(0, 5.5,
        "This analysis is based on market rates for medical device consultants "
        "in the United States as of March 2026. Rates reflect the combination of "
        "PMP certification, FDA regulatory experience, and technical publications "
        "leadership. Actual compensation should be negotiated based on the specific "
        "engagement terms, equity structure, and mutual agreement.",
        new_x="LMARGIN", new_y="NEXT")

    # ── OUTPUT ─────────────────────────────────
    out = "Consultant_Role_Analysis.pdf"
    pdf.output(out)
    print(f"Generated: {out}")


if __name__ == "__main__":
    build()
