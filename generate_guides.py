#!/usr/bin/env python3
"""Generate bilingual PDF User Guides for the Medical Device Dashboard."""

import os
from fpdf import FPDF

OUT_DIR = os.path.dirname(os.path.abspath(__file__))

BLUE = (30, 90, 200)
DARK = (15, 17, 23)
GRAY = (120, 120, 130)
TEXT = (40, 40, 45)
CN_TEXT = (40, 40, 45)

# ===================== ENGLISH GUIDE =====================

class EnglishGuide(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*GRAY)
        self.cell(0, 6, "Medical Device Development Control Tower - User Guide", align="R")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(*GRAY)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")

    def sec(self, num, title):
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(*BLUE)
        self.cell(0, 10, f"{num}. {title}", new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(*BLUE)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(4)

    def sub(self, title):
        self.set_font("Helvetica", "B", 12)
        self.set_text_color(*TEXT)
        self.cell(0, 8, title, new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def txt(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*TEXT)
        self.multi_cell(0, 5.5, text, new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def kv(self, key, val):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(*BLUE)
        self.cell(0, 5.5, key, new_x="LMARGIN", new_y="NEXT")
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*TEXT)
        self.multi_cell(0, 5.5, "  " + val, new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def bul(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*TEXT)
        self.multi_cell(0, 5.5, "  - " + text, new_x="LMARGIN", new_y="NEXT")


def build_english():
    pdf = EnglishGuide()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()

    # Cover
    pdf.ln(30)
    pdf.set_font("Helvetica", "B", 28)
    pdf.set_text_color(*BLUE)
    pdf.cell(0, 14, "Control Tower", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 14)
    pdf.set_text_color(*TEXT)
    pdf.cell(0, 8, "Medical Device Development Dashboard", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)
    pdf.set_font("Helvetica", "I", 11)
    pdf.set_text_color(*GRAY)
    pdf.cell(0, 7, "ICU Respiratory Digital Twin System", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 7, "sEMG Neural Drive + EIT Ventilation/Perfusion Monitoring Platform", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(*TEXT)
    pdf.cell(0, 10, "User Guide", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(6)
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(*GRAY)
    pdf.cell(0, 7, "Version 1.0 | March 2026", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 7, "Company B USA / Silan Technology (Chengdu)", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(20)
    pdf.set_font("Helvetica", "I", 10)
    pdf.set_text_color(*GRAY)
    pdf.multi_cell(0, 5.5,
        "This guide explains every element of the PM Dashboard in detail. "
        "The dashboard is designed for bilingual (EN/CN) project management teams "
        "pursuing FDA 510(k) clearance for the ICU Respiratory Digital Twin System.",
        align="C")

    # 1. Overview
    pdf.add_page()
    pdf.sec(1, "Overview")
    pdf.txt(
        "The Control Tower is a Project Manager (PMP) central command dashboard for the "
        "ICU Respiratory Digital Twin System, a dual-module 510(k) medical device:\n\n"
        "  Module A: sEMG Neural Drive Monitoring (Product Code IKN)\n"
        "  Module B: EIT Ventilation/Perfusion System (Product Code DQS)\n\n"
        "The dashboard answers ONE master question at all times:\n"
        "  'Are we still on track to FDA clearance, and what is at risk?'")
    pdf.txt(
        "The PMP (Project Management Professional) holds overriding authority over all gate "
        "decisions. Business and Technology teams provide inputs, but the PMP makes the final call "
        "at every decision checkpoint.")

    # 2. Top Bar
    pdf.sec(2, "Top Bar")
    pdf.txt("The sticky header bar at the top of the screen contains:")

    pdf.sub("2.1 Logo & Title")
    pdf.txt(
        "The medical caduceus icon alongside 'Control Tower' and the subtitle "
        "'ICU Respiratory Digital Twin' identify the application. These change language "
        "when you toggle the language switch.")

    pdf.sub("2.2 Master Question")
    pdf.txt(
        "The italic text in the center reads: 'Are we still on track to FDA clearance, "
        "and what is at risk?' This is the overriding question the entire dashboard is "
        "designed to answer. Every panel, metric, and gate revolves around this question.")

    pdf.sub("2.3 PMP Authority Badge")
    pdf.txt(
        "The red shield badge (PMP Authority) indicates that the Project Management Professional "
        "has overriding decision authority. In the Gate System, only the PMP can set gate decisions "
        "(Proceed / Need More Data / Stop). Business and Technology teams submit inputs, but the "
        "PMP decision is final.")

    pdf.sub("2.4 Language Toggle (EN / CN)")
    pdf.txt(
        "Clicking the language button switches the entire dashboard between English (EN) and "
        "Chinese (CN). All labels, descriptions, milestone titles, risk descriptions, and gate "
        "criteria switch to the selected language. The HTML lang attribute also updates "
        "(en to zh-CN) for accessibility.")

    pdf.sub("2.5 Current Month Badge: 'Current: M+0'")
    pdf.txt(
        "This is one of the most important indicators on the dashboard.\n\n"
        "'M+' stands for 'Months after project start.' The project timeline is measured in "
        "months from the baseline date (March 2026).\n\n"
        "Examples:\n"
        "  M+0  = March 2026 (project kickoff)\n"
        "  M+2  = May 2026 (FDA Pre-Submission meeting)\n"
        "  M+6  = September 2026 (510(k) sEMG submission)\n"
        "  M+9  = December 2026 (sEMG clearance expected)\n"
        "  M+23 = February 2028 (full platform clearance)\n\n"
        "'Current: M+0' means the project is currently at Month 0, the very start. "
        "As the project advances, this number increments and all downstream calculations "
        "(days to milestone, gate targets, etc.) update accordingly.")

    # 3. Status Summary Bar
    pdf.add_page()
    pdf.sec(3, "Status Summary Bar")
    pdf.txt("The horizontal row of six cards below the tabs provides an at-a-glance health check:")

    pdf.sub("3.1 Overall Status")
    pdf.txt(
        "Displays one of three states, color-coded:\n\n"
        "  ON TRACK (green)  -- Fewer than 1 red risk. All systems nominal.\n"
        "  AT RISK  (yellow) -- 1-2 red risks present. Attention needed.\n"
        "  BLOCKED  (red)    -- 3 or more red risks. Critical intervention required.\n\n"
        "This value is computed automatically from the risk register.")

    pdf.sub("3.2 Next Gate")
    pdf.txt(
        "Shows the next upcoming decision gate. A gate is considered complete when its "
        "status is 'Approved', its decision is 'Proceed', or all of its criteria badges "
        "are marked Complete. The metric automatically advances once every criterion in "
        "the current gate is fulfilled. Format: 'G1 (M+3)' meaning Gate 1 is targeted "
        "at Month 3. This tells the PMP which decision checkpoint is coming up next, "
        "so they can prepare criteria reviews.")

    pdf.sub("3.3 Red Risks")
    pdf.txt(
        "A count of how many risks in the ISO 14971 risk register are classified as RED "
        "(high severity + meaningful probability). A red risk count of 3+ triggers "
        "the BLOCKED overall status.")

    pdf.sub("3.4 Pending Inputs")
    pdf.txt(
        "The number of stakeholder inputs (from Business or Technology teams) that are "
        "in 'Pending Review' status -- meaning the PMP has not yet reviewed and responded. "
        "This is also reflected in the Floating Action Button (FAB) badge.")

    pdf.sub("3.5 Days to Next Milestone")
    pdf.txt(
        "An estimate of when the next incomplete milestone occurs. Calculated as:\n"
        "  (next milestone month - current month) x 30 days\n\n"
        "Example: If current month is M+0 and the next milestone is at M+1, it shows '~30d'.")

    pdf.sub("3.6 Runway")
    pdf.txt(
        "Displays how many months of operation remain at the current burn rate. "
        "Calculated as Cash on Hand / Monthly Burn. The value is color-coded:\n\n"
        "  Green  -- 7+ months remaining. Healthy position.\n"
        "  Orange -- 4-6 months remaining. Begin fundraising / cost review.\n"
        "  Red    -- 3 months or fewer. Critical -- immediate funding action required.\n\n"
        "Click the Cash / Runway tab for the full financial breakdown, funding timeline, "
        "and API integration panel.")

    # 4. Navigation Tabs
    pdf.add_page()
    pdf.sec(4, "Navigation Tabs")
    pdf.txt("Fourteen tabs provide access to the main dashboard panels. The active tab has a blue underline.")
    pdf.ln(2)
    pdf.kv("Dual-Track", "Side-by-side view of Technical + Regulatory milestones")
    pdf.kv("Gate System", "Decision checkpoints with PMP authority controls")
    pdf.kv("Risk Dashboard", "ISO 14971 risk register with filtering and top-5 ranking")
    pdf.kv("Timeline", "Business-language translation of technical milestones")
    pdf.kv("Regulatory Tracker", "IEC/ISO/21 CFR compliance standards matrix")
    pdf.kv("Cash / Runway", "Financial position, burn rate, funding milestones, and API integrations")
    pdf.kv("Actions", "Task board, DHF Document Tracker, and CAPA Log")
    pdf.kv("Budget", "Budget vs. Actual spending per category")
    pdf.kv("Resources", "Team allocation and capacity utilization")
    pdf.kv("Suppliers", "Hardware component vendor tracking")
    pdf.kv("Audit Trail", "Chronological log of all dashboard actions for DHF traceability")
    pdf.kv("US Investment", "North America fundraising pipeline, investor tracking, and IR activities")
    pdf.kv("Document Control", "ISO 13485-aligned document lifecycle, revision history, and review scheduling")
    pdf.kv("Message Board", "Purpose-driven messaging with structured threads, decision logging, workstream filtering, and accountability")

    # 5. Dual-Track
    pdf.add_page()
    pdf.sec(5, "Tab 1: Dual-Track Dashboard")
    pdf.txt(
        "This is the default view. It displays two parallel columns:\n\n"
        "  LEFT:  Technical Track -- R&D, prototyping, testing, validation milestones\n"
        "  RIGHT: Regulatory Track -- FDA submissions, audits, clearances, legal\n\n"
        "Between the columns is a center timeline spine with dots for each month. "
        "Dots at or before the current month glow blue (active). Future months are gray.")

    pdf.sub("5.1 Milestone Cards")
    pdf.txt(
        "Each milestone card contains:\n\n"
        "  Title: What the milestone is (e.g., 'ECG-Gating Algorithm Validation')\n"
        "  M+N badge: Which project month this milestone is targeted at\n"
        "  Description: Technical details of the milestone\n"
        "  Status badge: One of three states:")
    pdf.bul("COMPLETE (green) -- Milestone finished successfully")
    pdf.bul("IN PROGRESS (yellow) -- Currently being worked on")
    pdf.bul("NOT STARTED (gray) -- Work has not begun")
    pdf.ln(2)
    pdf.txt(
        "Cards have a colored left border matching their status:\n"
        "  Green border  = Complete\n"
        "  Yellow border = In Progress\n"
        "  Gray border   = Not Started")

    pdf.sub("5.2 Milestone Owners")
    pdf.txt(
        "Each milestone has an owner category:\n"
        "  'tech'       -- Engineering / R&D team responsibility\n"
        "  'regulatory' -- Regulatory affairs team responsibility\n"
        "  'business'   -- Business / legal / investor team responsibility")

    # 6. Gate System
    pdf.add_page()
    pdf.sec(6, "Tab 2: Gate System")
    pdf.txt(
        "The Gate System implements a Phase-Gate project management methodology. "
        "There are six gates (G1-G6), each representing a critical decision checkpoint. "
        "Gates are displayed as a horizontal pipeline connected by arrows.")

    pdf.sub("6.1 Gate Cards")
    pdf.txt(
        "Each gate card shows:\n\n"
        "  Gate Number: G1, G2, G3, etc.\n"
        "  Title: What the gate represents\n"
        "  Target Month: 'Target: M+3' means this gate should be reached at Month 3\n"
        "  Criteria Progress: '2/4 criteria met' with a progress bar\n"
        "  Status Strip: A colored bar at the bottom indicating status")

    pdf.sub("6.2 Gate Statuses (Color Coding)")
    pdf.txt(
        "  Gray   (Not Started) -- Gate has not been evaluated yet\n"
        "  Yellow (Pending)     -- Gate is under review or needs more data\n"
        "  Green  (Approved)    -- PMP has decided to proceed\n"
        "  Red    (Blocked)     -- PMP has decided to stop")

    pdf.sub("6.3 Gate Detail Modal")
    pdf.txt("Clicking any gate card opens a detailed modal containing:")
    pdf.bul("Criteria Checklist -- Each criterion has a clickable checkbox. Check items as "
            "verified. The progress bar and count update in real-time.")
    pdf.bul("PMP Decision Buttons -- Three buttons only the PMP should use:\n"
            "    Proceed (green) -- Approve and move to next phase\n"
            "    Need More Data (yellow) -- Request additional evidence\n"
            "    Stop (red) -- Halt progress until issues are resolved")
    pdf.bul("Stakeholder Inputs -- Inputs from Tech or Business teams related to this gate, "
            "showing their status (Pending Review / Accepted) and any PMP response.")
    pdf.bul("Gate Notes -- Free-text notes added by the PMP. Each note is timestamped. "
            "Type in the textarea and click 'Add Note' to append a record.")

    pdf.sub("6.4 The Six Gates")
    pdf.kv("G1 (M+3)", "sEMG Design Verification Complete")
    pdf.kv("G2 (M+2)", "Pre-Sub FDA Feedback Received")
    pdf.kv("G3 (M+6)", "510(k) sEMG Submission Ready")
    pdf.kv("G4 (M+9)", "sEMG Module Commercial Launch")
    pdf.kv("G5 (M+17)", "EIT 510(k) Submission Ready")
    pdf.kv("G6 (M+23)", "Full Platform Launch -- FDA Cleared")

    # 7. Risk Dashboard
    pdf.add_page()
    pdf.sec(7, "Tab 3: Risk Dashboard")
    pdf.txt(
        "The Risk Dashboard implements ISO 14971 risk management for medical devices. "
        "It provides a visual overview of all risks, their severity, probability, "
        "current controls, and mitigation status.")

    pdf.sub("7.1 Risk Filters")
    pdf.txt(
        "Four filter buttons at the top:\n\n"
        "  All    -- Show all risks (default)\n"
        "  Red    -- Show only high-priority risks\n"
        "  Yellow -- Show only medium-priority risks\n"
        "  Green  -- Show only low-priority risks")

    pdf.sub("7.2 Risk Cards")
    pdf.txt(
        "Each risk card displays:\n\n"
        "  Risk ID: e.g., RISK-001\n"
        "  Risk Level Badge: RED / YELLOW / GREEN\n"
        "  Title: Description of the risk\n"
        "  Severity: High / Medium / Low\n"
        "  Probability: High / Medium / Low / Very Low\n"
        "  Module: Which device module is affected (A, B, Both, N/A)\n"
        "  Controls: Current risk mitigation controls in place\n"
        "  Mitigation Status: Complete / In Progress / Not Started\n"
        "    Complete (green bar, 100%)\n"
        "    In Progress (yellow bar, 50%)\n"
        "    Not Started (red bar, 0%)\n\n"
        "Cards have a colored left border matching their risk level.")

    pdf.sub("7.3 Risk Level Calculation")
    pdf.txt(
        "Risk levels follow a severity x probability matrix:\n\n"
        "  RED    = High severity risks needing immediate attention\n"
        "  YELLOW = Moderate risks under active monitoring\n"
        "  GREEN  = Low risks with adequate controls\n\n"
        "The number of RED risks directly affects Overall Status:\n"
        "  3+ red risks = BLOCKED; 1-2 = AT RISK; 0 = ON TRACK.")

    pdf.sub("7.4 Top 5 Risks This Week")
    pdf.txt(
        "Below the risk grid, a ranked list shows the top 5 highest-priority risks. "
        "Sorted by risk level (red > yellow > green), then severity (high > medium > low). "
        "Each entry shows a rank number, color indicator, title, and affected module.")

    # 8. Timeline
    pdf.add_page()
    pdf.sec(8, "Tab 4: Timeline -- Business Translation")
    pdf.txt(
        "This tab is designed for business stakeholders and investors who may not "
        "understand technical jargon. Each event shows TWO columns:\n\n"
        "  LEFT  (blue header 'Technical'): Engineering description\n"
        "  RIGHT (orange header 'Business Impact'): What it means for business\n\n"
        "Each event has a month badge (M+0, M+2, etc.) and a color-coded dot:")
    pdf.bul("Red dot (Critical) -- Major business impact, investor attention required")
    pdf.bul("Yellow dot (Warning) -- Notable cost or schedule impact")
    pdf.bul("Blue dot (Neutral) -- Standard progress marker")

    pdf.ln(2)
    pdf.sub("8.1 Timeline Events")
    pdf.kv("M+0", "Pre-Sub filed: FDA engagement initiated")
    pdf.kv("M+2", "FDA Pre-Sub meeting: Pivotal investor signal (CRITICAL)")
    pdf.kv("M+3", "Bench testing begins: Largest pre-submission spend (WARNING)")
    pdf.kv("M+6", "510(k) sEMG submitted: Investor confidence checkpoint (CRITICAL)")
    pdf.kv("M+9", "sEMG clearance: Module A revenue-ready (CRITICAL)")
    pdf.kv("M+12", "EIT testing begins: Second investment tranche needed (WARNING)")
    pdf.kv("M+17", "510(k) EIT submitted: Strategic partnerships viable (CRITICAL)")
    pdf.kv("M+23", "EIT clearance: Full commercial launch / ROI begins (CRITICAL)")

    # 9. Regulatory Tracker
    pdf.add_page()
    pdf.sec(9, "Tab 5: Regulatory Standards Tracker")
    pdf.txt("A compliance matrix tracking all applicable regulatory standards for the 510(k) submission:")
    pdf.ln(2)
    pdf.kv("Standard", "The standard code (e.g., IEC 60601-1:2005+AMD1)")
    pdf.kv("Description", "What the standard covers (e.g., Medical Electrical Equipment - General Safety)")
    pdf.kv("Applies To", "Which component: Both, sEMG Electrodes, EIT Belt, Software, or Silan Manufacturing")
    pdf.kv("Status", "Badge: Complete (green), In Progress (yellow), or Not Started (gray)")
    pdf.kv("Progress", "A percentage bar (0-100%) showing completion")
    pdf.ln(2)
    pdf.txt(
        "The 12 tracked standards include:\n\n"
        "  IEC 60601-1      -- General electrical safety\n"
        "  IEC 60601-1-2    -- EMC\n"
        "  IEC 60601-1-6    -- Usability\n"
        "  ISO 14971        -- Risk management\n"
        "  ISO 10993-1/5/10 -- Biocompatibility\n"
        "  FDA Cybersecurity 2023 -- Device cybersecurity\n"
        "  21 CFR 820       -- QSR\n"
        "  21 CFR Part 11   -- Electronic records\n"
        "  IEC 62304        -- Software lifecycle\n"
        "  ISO 13485        -- QMS")

    # 10. Stakeholder Input System
    pdf.add_page()
    pdf.sec(10, "Stakeholder Input System")
    pdf.txt(
        "The dashboard implements a structured input mechanism where Business and Technology "
        "teams can submit inputs to the PMP for review.")

    pdf.sub("10.1 Floating Action Button (FAB)")
    pdf.txt(
        "The blue circular button in the bottom-right corner opens the Stakeholder Input "
        "slide-in panel. A red badge on the FAB shows the count of pending (unreviewed) inputs. "
        "If there are no pending inputs, the badge is hidden.")

    pdf.sub("10.2 Input Panel")
    pdf.txt(
        "The slide-in panel from the right edge shows all stakeholder inputs:\n\n"
        "  Source: Technology Team (blue left border) or Business/Investors (orange)\n"
        "  Date: When the input was submitted\n"
        "  Related Gate: Which gate this input pertains to (e.g., G1, G4)\n"
        "  Status Badge: Pending Review (yellow) or Accepted (green)\n"
        "  Content: The actual feedback or request\n"
        "  PMP Response: Shown with a PMP: prefix in red (if responded)")

    pdf.sub("10.3 Input Statuses")
    pdf.txt(
        "  Pending Review -- PMP has not yet responded. Counted in the badge.\n"
        "  Accepted       -- PMP has reviewed and accepted the input.\n"
        "  Rejected       -- PMP has rejected the input.\n"
        "  Noted          -- PMP has acknowledged but taken no action.")

    # 11. Bilingual System
    pdf.sec(11, "Bilingual System (EN/CN)")
    pdf.txt(
        "The dashboard supports full English/Chinese switching. When you click "
        "the language toggle (EN/CN):\n\n"
        "  1. All static labels update (tab names, column headers, button text)\n"
        "  2. All data-driven content updates (milestone titles, risk descriptions, gate criteria)\n"
        "  3. The HTML lang attribute switches between 'en' and 'zh-CN'\n\n"
        "Designed for bilingual teams where engineering may work in Chinese and "
        "investors/regulatory consultants work in English.")

    # 12. Cash / Runway Tab
    pdf.add_page()
    pdf.sec(12, "Tab 6: Cash / Runway")
    pdf.txt(
        "The Cash / Runway tab shows real-time financial position for the project. "
        "This is the primary tab for business stakeholders and Accounting users.")

    pdf.sub("12.1 Financial Summary Cards")
    pdf.txt(
        "Three cards at the top display:\n\n"
        "  Cash on Hand -- Current available funds in USD\n"
        "  Monthly Burn -- Average monthly expenditure\n"
        "  Runway       -- How many months of operation remaining at current burn rate")

    pdf.sub("12.2 Funding Rounds")
    pdf.txt(
        "Each funding round has a card showing:\n\n"
        "  Label: Round name (e.g. Angel Round, Pre-Seed, Series A)\n"
        "  Amount: Dollar value\n"
        "  Date: Expected or received date\n"
        "  Status Badge (clickable by PMP): Pipeline / Committed / Received\n\n"
        "When a round transitions to 'Received', the dashboard automatically adds "
        "the amount to Cash on Hand and recalculates Runway months.\n\n"
        "Non-PMP users can request a status change through the Change Request workflow.")

    pdf.sub("12.3 Adding New Funding Rounds")
    pdf.txt(
        "Below the funding round cards, the PMP can record a new round by entering:\n\n"
        "  Label (e.g. Series A)\n"
        "  Amount in USD\n"
        "  Expected date (YYYY-MM)\n\n"
        "New rounds always start with 'Pipeline' status.")

    pdf.sub("12.4 Burn History")
    pdf.txt(
        "A table showing monthly burn amounts with notes (e.g., 'Pre-Sub filing costs', "
        "'Bench testing begins'). This helps investors and accounting understand spending patterns.")

    # 13. Role-Based Access Control
    pdf.add_page()
    pdf.sec(13, "Role-Based Access Control")
    pdf.txt(
        "The dashboard implements four user roles, selectable from the Role Switcher dropdown "
        "in the top-right corner of the header.")

    pdf.sub("13.1 Role Switcher")
    pdf.txt(
        "A dropdown menu in the top bar lets you switch between roles:\n\n"
        "  PMP (Full Authority) -- Can directly change any status, approve/reject change requests, "
        "make gate decisions, and access all tabs.\n"
        "  Technology Team -- Can view all tabs but cannot make direct changes. Must submit a "
        "Change Request for any status modification.\n"
        "  Business / Investors -- Same as Technology: full view, but changes require a CR.\n"
        "  Accounting -- Read-only access limited to three tabs only.")

    pdf.sub("13.2 PMP Role")
    pdf.txt(
        "The PMP has full authority:\n"
        "  - Click milestone badges to cycle status (Not Started / In Progress / Complete)\n"
        "  - Click risk cards to edit severity, probability, level, and mitigation\n"
        "  - Click standard status badges to cycle status\n"
        "  - Click funding status badges to cycle status\n"
        "  - Make gate decisions (Proceed / Need Data / Stop)\n"
        "  - Approve or Reject change requests from Tech/Business teams\n"
        "  - Add gate notes and manage all panels")

    pdf.sub("13.3 Technology & Business Roles")
    pdf.txt(
        "When a Tech or Business team member clicks a status to change it, instead of "
        "directly modifying the data, a Change Request form opens.\n\n"
        "They must provide:\n"
        "  - Proposed new value\n"
        "  - Justification (required) -- Why the change is warranted\n"
        "  - Evidence/Reference (optional) -- Link or document reference\n"
        "  - Attached Documents (optional) -- File uploads stored on the server\n\n"
        "The request is then queued for PMP review. The PMP can Approve (applies the change) "
        "or Reject (with a note explaining why).\n\n"
        "DIRECT EDIT PRIVILEGES:\n"
        "Business and Technology roles also have direct edit access (no CR required) for:\n"
        "  - Cash on Hand and Monthly Burn fields in the Cash / Runway tab\n"
        "  - Funding round status cycling (Pipeline / Committed / Received)\n"
        "  - Removing Payment & Banking API integrations they do not use (with Restore option)")

    pdf.sub("13.4 Accounting Role")
    pdf.txt(
        "Accounting has the most restricted access:\n\n"
        "  ALLOWED (read-only):\n"
        "    - Cash / Runway -- View balances, funding rounds, and burn history\n"
        "    - Timeline -- View milestone events in business language\n"
        "    - Gate System -- View gate statuses and criteria\n\n"
        "  RESTRICTED (tabs disabled):\n"
        "    - Dual-Track (contains proprietary technical details)\n"
        "    - Risk Dashboard (contains sensitive risk assessments)\n"
        "    - Regulatory Tracker (compliance implementation details)\n\n"
        "A yellow notice banner appears when Accounting is active, explaining the access limits. "
        "Restricted tabs are grayed out and unclickable.")

    # 14. Change Request Workflow & Document Storage
    pdf.add_page()
    pdf.sec(14, "Change Request Workflow & Document Storage")
    pdf.txt(
        "The Change Request (CR) system ensures that all status changes are verified before "
        "being applied. Only the PMP can make direct changes; Technology and Business teams "
        "must submit a CR that the PMP reviews.\n\n"
        "All CR data is automatically synced to the server (Supabase) with localStorage backup. "
        "Attached documents are stored separately in IndexedDB.")

    pdf.sub("14.1 Submitting a Change Request")
    pdf.txt(
        "When a non-PMP user tries to change a status (milestone, risk, standard, or funding), "
        "a tooltip reading 'Click to submit a Change Request' appears on hover. Clicking opens "
        "a modal form with the following fields:\n\n"
        "  Requested By: Automatically set based on active role (Tech or Business)\n"
        "  Field: Shows what is being changed (e.g., T1.1 -> status)\n"
        "  Current Value: The existing value that would be changed\n"
        "  Proposed Value: What the requester wants to change it to (required). "
        "The placeholder reads 'Enter the new value for the field shown above'.\n"
        "  Justification: Why the change is warranted (required). Reference test data, "
        "FDA feedback, clinical findings, or business conditions.\n"
        "  Evidence / Reference: Optional text field for links or document references.\n"
        "  Attached Documents: Optional file uploads (PDF, images, docs).\n\n"
        "After submission, a toast notification appears confirming the CR ID and that it is "
        "awaiting PMP approval.")

    pdf.sub("14.2 Document Storage")
    pdf.txt(
        "Documents attached to change requests are stored on the server with local "
        "IndexedDB backup. This means:\n\n"
        "  - Files are synced to the server database and cached locally\n"
        "  - Documents persist across page reloads within the same browser\n"
        "  - Multiple files can be attached to a single CR\n"
        "  - Attached files can be removed before submission\n"
        "  - After submission, files can be downloaded from the CR card\n\n"
        "Supported file types: PDF, images (PNG, JPG), Word documents, Excel spreadsheets, "
        "and any other file type the browser supports.\n\n"
        "File sizes are displayed in human-readable format (KB, MB).")

    pdf.sub("14.3 Change Request Tracking")
    pdf.txt(
        "Pending change requests are tracked through the Audit Trail and the notification "
        "system rather than a dedicated queue tab. When a non-PMP user submits a CR:\n\n"
        "  - The CR is recorded in the Audit Trail with a PENDING status\n"
        "  - The PMP receives a notification alerting them to the new CR\n"
        "  - CR cards are color-coded: PENDING (yellow), APPROVED (green), REJECTED (red)\n\n"
        "Each CR record displays: CR ID, requester, date, field being changed, old value, "
        "new value, justification, evidence, attached documents (with download links), "
        "and PMP response note (if any).")

    pdf.sub("14.4 PMP Review Process")
    pdf.txt(
        "The PMP reviews and acts on pending CRs through the notification system:\n\n"
        "  Approve: The proposed change is applied directly to the dashboard data. "
        "The CR is marked as 'Approved' with a PMP note and timestamp.\n\n"
        "  Reject: The change is NOT applied. The CR is marked as 'Rejected' with a "
        "PMP note explaining the reason. The requester can see the rejection and submit "
        "a new CR with additional justification if desired.")

    # 15. China Investor API Integrations
    pdf.add_page()
    pdf.sec(15, "China Investor API Integrations")
    pdf.txt(
        "Located in the Cash / Runway tab, this panel provides a reference guide for payment, "
        "banking, and currency APIs relevant to Chinese investors and cross-border transactions.")

    pdf.sub("15.1 API Status Badges")
    pdf.txt(
        "Each API card shows one of three statuses:\n\n"
        "  Active (green)    -- API is currently integrated and live\n"
        "  Available (blue)  -- API is available for integration, not yet connected\n"
        "  Planned (purple)  -- API integration is planned for a future phase")

    pdf.sub("15.2 Listed APIs")
    pdf.kv("Alipay Business", "Cross-border payment collection, investor wire tracking, RMB/USD settlement")
    pdf.kv("WeChat Pay Business", "Enterprise payments, investor communication channel, mini-program integration")
    pdf.kv("UnionPay International", "Corporate card payments, cross-border B2B transfers, multi-currency support")
    pdf.kv("China Merchants Bank (CMB)", "Corporate banking API, treasury management, real-time balance & FX rates")
    pdf.kv("PingPong Global", "Cross-border payment platform for startups, automated FX, VAT refund support")
    pdf.kv("XE Currency Data", "Real-time CNY/USD exchange rates, historical rate data, currency conversion")
    pdf.kv("SWIFT gpi", "Cross-border wire tracking, payment status confirmation, compliance screening")

    pdf.ln(2)
    pdf.txt(
        "Each card also shows the documentation source for developer reference. "
        "These APIs are particularly relevant for investors based in mainland China "
        "who need to transfer funds cross-border, track payments, and manage currency conversion.")

    pdf.sub("15.3 Removing & Restoring Integrations")
    pdf.txt(
        "PMP, Business, and Technology roles can remove API integration cards they do not need. "
        "Each card displays a close button (X) in the top-right corner. Clicking it shows a "
        "confirmation prompt; once confirmed, the card is hidden and the removal is logged in the "
        "Audit Trail.\n\n"
        "If any integrations have been removed, a 'Restore Removed Integrations' button appears "
        "at the bottom of the panel. Clicking it brings back all previously hidden cards. "
        "Removed integrations are remembered across sessions via the server database.")

    # 16. Action Items / Task Board
    pdf.add_page()
    pdf.sec(16, "Tab 7: Action Items / Task Board")
    pdf.txt(
        "The Action Items tab provides a Kanban-style task board for tracking all "
        "project action items. Items are organized in four columns representing their status.")

    pdf.sub("16.1 Kanban Columns")
    pdf.txt(
        "Four columns organize action items by status:\n\n"
        "  Todo       -- Items not yet started (gray header)\n"
        "  In-Progress -- Currently being worked on (blue header)\n"
        "  Blocked     -- Waiting on external dependency (red header)\n"
        "  Done        -- Completed items (green header)\n\n"
        "Click any action card to cycle its status: Todo -> In-Progress -> Done -> Todo. "
        "Blocked items cycle to In-Progress when clicked.")

    pdf.sub("16.2 Action Cards")
    pdf.txt(
        "Each card displays:\n\n"
        "  Action ID: e.g., ACT-001\n"
        "  Priority Badge: HIGH (red), MEDIUM (yellow), LOW (green)\n"
        "  Title: Description of the task\n"
        "  Assignee: Team member responsible\n"
        "  Owner: Functional area (tech, regulatory, business)\n"
        "  Due Date: Target completion date\n"
        "  Linked Gate: Which gate this action relates to (if any)\n"
        "  Notes: Additional context\n\n"
        "Cards have a colored left border matching their priority level.")

    # 17. DHF Document Tracker
    pdf.add_page()
    pdf.sec(17, "DHF Document Tracker")
    pdf.txt(
        "The Design History File (DHF) Document Tracker is located within the Actions tab. "
        "It tracks all required design control documents for the 510(k) submission per "
        "21 CFR 820 requirements.")

    pdf.sub("17.1 Document Table")
    pdf.txt(
        "Each row in the DHF table shows:\n\n"
        "  Code: Document identifier (e.g., DHF-001)\n"
        "  Title: Document name (e.g., Design Plan)\n"
        "  Category: Design Controls, Verification, Testing, Risk, Software, etc.\n"
        "  Owner: Responsible team member\n"
        "  Status: Clickable badge cycling through:\n"
        "    Not Started (gray) -> Draft (indigo) -> In-Review (yellow) -> Approved (green)\n"
        "  Due Month: Target month for completion (M+N format)\n"
        "  Notes: Additional context about the document")

    pdf.sub("17.2 Document Categories")
    pdf.txt(
        "DHF documents span these categories:\n\n"
        "  Design Controls   -- Design Plan, Inputs, Outputs\n"
        "  Verification      -- Design Verification protocols and reports\n"
        "  Validation        -- Clinical validation evidence\n"
        "  Risk Management   -- ISO 14971 Risk Analysis files\n"
        "  Software          -- IEC 62304 Software Documentation\n"
        "  Biocompatibility  -- ISO 10993 testing reports\n"
        "  Testing           -- EMC and electrical safety test results\n"
        "  Submission        -- Cover Letter and Device Description for FDA")

    # 18. CAPA Log
    pdf.add_page()
    pdf.sec(18, "CAPA Log")
    pdf.txt(
        "The Corrective and Preventive Actions (CAPA) log is also located in the Actions tab. "
        "CAPAs are linked to specific risks from the ISO 14971 risk register and track "
        "formal corrective or preventive measures.")

    pdf.sub("18.1 CAPA Cards")
    pdf.txt(
        "Each CAPA card displays:\n\n"
        "  CAPA ID: e.g., CAPA-001\n"
        "  Type Badge: Corrective (red) or Preventive (blue)\n"
        "  Status Badge: Clickable, cycling through:\n"
        "    Open (yellow) -> In-Progress (blue) -> Closed (green) -> Verified (purple)\n"
        "  Title: Short description of the action\n"
        "  Description: Detailed explanation\n"
        "  Linked Risk: Which risk register entry triggered this CAPA\n"
        "  Owner: Responsible team member\n"
        "  Opened Date / Due Date / Closed Date\n\n"
        "Cards have a colored left border matching their status. "
        "When a CAPA transitions to 'Closed', the closed date is automatically set.")

    pdf.sub("18.2 CAPA Types")
    pdf.txt(
        "  Corrective: Actions taken to eliminate the cause of an existing nonconformity. "
        "Example: Redesigning electrode arrays to solve ECG artifact interference.\n\n"
        "  Preventive: Actions taken to eliminate the cause of a potential nonconformity. "
        "Example: Adding cybersecurity penetration testing before it becomes an issue.")

    # 19. Budget vs. Actual
    pdf.add_page()
    pdf.sec(19, "Tab 8: Budget vs. Actual")
    pdf.txt(
        "The Budget tab shows a detailed breakdown of planned versus actual spending "
        "across all project categories. This tab is accessible to the Accounting role.")

    pdf.sub("19.1 Budget Table")
    pdf.txt(
        "Each row shows:\n\n"
        "  Category: Budget line item (e.g., Prototype Development, Lab Testing)\n"
        "  Planned ($): Budgeted amount\n"
        "  Actual ($): Amount spent to date\n"
        "  Variance ($): Difference (Actual - Planned)\n"
        "    Green = under budget (favorable)\n"
        "    Red   = over budget (unfavorable)\n"
        "  Notes: Context for the spending")

    pdf.sub("19.2 Budget Categories")
    pdf.txt(
        "Eight categories track project spending:\n\n"
        "  Prototype Development -- Hardware and firmware prototyping\n"
        "  Lab Testing           -- V&V, EMC, and bench testing\n"
        "  Regulatory Consulting -- FDA consultants and filing fees\n"
        "  Personnel             -- Engineering and regulatory staff\n"
        "  Clinical Studies      -- Clinical validation studies\n"
        "  Equipment & Software  -- Development tools and licenses\n"
        "  Manufacturing Setup   -- Contract manufacturing NRE\n"
        "  Travel & Meetings     -- FDA meetings, investor travel")

    pdf.sub("19.3 Totals Row")
    pdf.txt(
        "The bottom row shows the total Planned, Actual, and Variance across all categories. "
        "This provides a quick check on overall budget health.")

    # 20. Resource Allocation
    pdf.add_page()
    pdf.sec(20, "Tab 9: Resource Allocation")
    pdf.txt(
        "The Resources tab shows team member assignments and capacity utilization. "
        "Each team member's workload is visualized with allocation bars.")

    pdf.sub("20.1 Resource Cards")
    pdf.txt(
        "Each card displays:\n\n"
        "  Name: Team member name\n"
        "  Role: Job title / function\n"
        "  Utilization Badge: Total allocation percentage, color-coded:\n"
        "    Green  (<= 80%) -- OK, room for more work\n"
        "    Yellow (81-99%) -- High utilization, monitor closely\n"
        "    Red   (>= 100%) -- Over-allocated, action needed\n"
        "  Allocation Bars: Visual bars for each workstream assignment\n"
        "  Capacity: Available hours per week")

    pdf.sub("20.2 Workstream Allocations")
    pdf.txt(
        "Each team member may be allocated across multiple workstreams "
        "(e.g., sEMG Design 40%, EIT Research 30%, Documentation 20%). "
        "The percentage bars show at a glance where each person's time is committed. "
        "Total utilization is calculated by summing all allocation percentages.")

    # 21. Supplier / Vendor Tracker
    pdf.add_page()
    pdf.sec(21, "Tab 10: Supplier / Vendor Tracker")
    pdf.txt(
        "The Suppliers tab tracks all hardware component vendors, contract manufacturers, "
        "and material suppliers critical to the device build.")

    pdf.sub("21.1 Supplier Table")
    pdf.txt(
        "Each row shows:\n\n"
        "  Supplier Name: Company name\n"
        "  Component: What they provide\n"
        "  Status: Clickable badge cycling through:\n"
        "    Under Review (yellow) -> Qualified (blue) -> Active (green) -> Risk (red)\n"
        "  Lead Time: Delivery time in days\n"
        "  PO Status: Current purchase order status\n"
        "  Contract/Mfg Milestone: Related project milestone\n"
        "  Notes: Additional context")

    pdf.sub("21.2 Supplier Statuses")
    pdf.txt(
        "  Under Review -- Supplier is being evaluated / audited\n"
        "  Qualified    -- Supplier has passed qualification but not yet active\n"
        "  Active       -- Supplier is approved and currently fulfilling orders\n"
        "  Risk         -- Supplier has quality, delivery, or capacity issues")

    # 22. Audit Trail
    pdf.add_page()
    pdf.sec(22, "Tab 11: Audit Trail")
    pdf.txt(
        "The Audit Trail tab provides a complete log of every status change, decision, "
        "and action taken in the dashboard. This supports 21 CFR Part 11 traceability "
        "requirements for medical device development.")

    pdf.sub("22.1 Audit Table")
    pdf.txt(
        "Each entry shows:\n\n"
        "  Timestamp: Date and time of the action\n"
        "  User: Who performed the action (PMP, Tech, Business)\n"
        "  Action: Type of action (e.g., milestone-status, gate-decision, cr-approved)\n"
        "  Target: Which item was affected (e.g., T1.1, G3, RISK-004)\n"
        "  Old Value: Previous state\n"
        "  New Value: Updated state\n"
        "  Detail: Additional context about the change\n\n"
        "The audit trail shows the most recent 50 entries. All actions that modify data "
        "are automatically logged, including milestone status changes, gate decisions, "
        "criteria toggles, CR approvals/rejections, and all new feature interactions.")

    pdf.sub("22.2 Tracked Actions")
    pdf.txt(
        "The following action types are captured:\n\n"
        "  milestone-status   -- Milestone state changes (Not Started/In Progress/Complete)\n"
        "  gate-decision      -- PMP gate decisions (Proceed/Need Data/Stop)\n"
        "  gate-criteria      -- Gate criteria checkbox toggles\n"
        "  gate-note          -- Notes added to gates\n"
        "  risk-field         -- Risk register field edits\n"
        "  standard-status    -- Regulatory standard status changes\n"
        "  standard-progress  -- Standard progress percentage updates\n"
        "  funding-status     -- Funding round status changes\n"
        "  funding-added      -- New funding rounds added\n"
        "  cr-submitted       -- Change requests submitted\n"
        "  cr-approved        -- Change requests approved by PMP\n"
        "  cr-rejected        -- Change requests rejected by PMP\n"
        "  action-item        -- Action item status changes\n"
        "  dhf-status         -- DHF document status changes\n"
        "  capa-status        -- CAPA item status changes\n"
        "  supplier-status    -- Supplier status changes")

    # 23. Notifications / Alerts
    pdf.add_page()
    pdf.sec(23, "Notifications & Alerts")
    pdf.txt(
        "The Notifications bar appears above the Change Request queue and provides "
        "real-time alerts about items needing attention.")

    pdf.sub("23.1 Alert Types")
    pdf.txt(
        "Five types of notifications are generated automatically:\n\n"
        "  Pending CRs (amber)       -- Change requests awaiting PMP review\n"
        "  Overdue Actions (red)     -- Action items past their due date\n"
        "  Overdue CAPAs (red)       -- CAPA items past their due date\n"
        "  Budget Overruns (pink)    -- Categories where actual exceeds planned spending\n"
        "  Runway Warning (orange)   -- Cash runway falls below 6 months")

    pdf.sub("23.2 Dismissing Notifications")
    pdf.txt(
        "Each notification has a dismiss button (X) on the right side. "
        "Dismissed notifications are hidden for the current session but will "
        "reappear on page reload if the condition persists. "
        "This ensures important alerts cannot be permanently silenced.")

    # 24. Export / Report Generator
    pdf.sec(24, "Export / Report Generator")
    pdf.txt(
        "The Export button in the Notifications bar header generates a comprehensive "
        "text report summarizing the entire project status.")

    pdf.sub("24.1 Report Contents")
    pdf.txt(
        "The generated report includes:\n\n"
        "  Project header and generation timestamp\n"
        "  Risk Summary -- All risks with ID, level, severity, probability, and module\n"
        "  Milestone Summary -- All milestones with status and target month\n"
        "  Financial Summary -- Cash on hand, monthly burn, runway, and funding rounds\n"
        "  DHF Status -- All design history file documents with status\n"
        "  CAPA Summary -- All corrective/preventive actions with status\n"
        "  Action Items -- All tasks with status and assigned owner\n\n"
        "The report downloads as a .txt file named 'Control_Tower_Report_YYYY-MM-DD.txt'.")

    # 25. US-Specific API Integrations
    pdf.add_page()
    pdf.sec(25, "US-Specific API Integrations")
    pdf.txt(
        "Located in the Cash / Runway tab alongside the China Investor API panel, this section "
        "provides a reference for payment, banking, and compliance APIs relevant to US-based "
        "investors and North American operations.")

    pdf.sub("25.1 Listed US APIs")
    pdf.kv("Plaid", "Bank account linking, balance verification, transaction monitoring for US investor accounts")
    pdf.kv("Mercury Banking", "Startup banking API -- real-time balance, wire transfers, treasury management")
    pdf.kv("Stripe", "US payment processing, investor subscription billing, automated invoicing")
    pdf.kv("Silicon Valley Bank (SVB)", "Venture banking, capital call processing, fund administration API")
    pdf.kv("AngelList", "Fundraising platform integration, SPV management, cap table sync")
    pdf.kv("Carta", "Cap table management, 409A valuations, equity plan administration")
    pdf.kv("SEC EDGAR", "Regulatory filing monitoring, Form D tracking, investor accreditation verification")

    pdf.ln(2)
    pdf.txt(
        "These APIs support the US investment pipeline managed by Lon Dailey (Investor Relations, "
        "N. America). They enable automated financial tracking, investor reporting, and regulatory "
        "compliance for US-based fundraising activities.")

    pdf.sub("25.2 Removing & Restoring Integrations")
    pdf.txt(
        "PMP, Business, and Technology roles can remove API cards they do not need by clicking "
        "the close button (X) on any card. Removed cards can be restored at any time using the "
        "'Restore Removed Integrations' button that appears when any cards have been removed.\n\n"
        "Removals persist across sessions via the server database and are recorded in the Audit Trail.")

    # 26. US Investment & Investor Relations Tab
    pdf.add_page()
    pdf.sec(26, "Tab 12: US Investment & Investor Relations")
    pdf.txt(
        "This tab is the designated home for all investor relations (IR) activity in the "
        "dashboard. It consolidates the complete North America fundraising pipeline, investor "
        "tracking, and IR activities into a single view managed by Lon Dailey as IR lead for "
        "N. America.\n\n"
        "Because this tab provides dedicated investor-facing content -- pipeline metrics, "
        "target investor details, and an activity log -- standalone investor pitch deck "
        "documents were removed from Document Control to avoid duplication. All investor "
        "materials and engagement history now live here.")

    pdf.sub("26.1 IR Metrics Cards")
    pdf.txt(
        "Four summary cards at the top give an at-a-glance snapshot of fundraising progress:\n\n"
        "  Investor Meetings (Q1)  -- Count of meetings held this quarter\n"
        "  Pipeline Value          -- Total dollar value in fundraising pipeline\n"
        "  Converted This Quarter  -- Amount successfully raised\n"
        "  IR Lead (N. America)    -- Primary contact for US investor relations\n\n"
        "These metrics are the first thing an investor or board member sees, providing "
        "immediate context on fundraising momentum.")

    pdf.sub("26.2 Target Investors Table")
    pdf.txt(
        "A table tracking all prospective US investors with full relationship context:\n\n"
        "  Target        -- Investor firm name\n"
        "  Type          -- VC, Angel Group, Strategic, etc.\n"
        "  Stage         -- Seed, Series A, etc.\n"
        "  Contact Status -- Color-coded pipeline stage:\n"
        "      Prospect (gray) / Contacted (green) / In Due Diligence (blue) / "
        "Term Sheet (blue) / Closed (blue)\n"
        "  Target Amount  -- Dollar amount sought from this investor\n"
        "  Notes         -- Additional context, relationship details, and thesis fit\n\n"
        "This table replaces the need for separate pitch trackers or CRM exports; the "
        "dashboard itself serves as the live investor pipeline.")

    pdf.sub("26.3 Investor Relations Activities")
    pdf.txt(
        "A chronological log of IR activities with status badges:\n\n"
        "  Complete     -- Activity finished\n"
        "  In Progress  -- Currently underway\n"
        "  Not Started  -- Scheduled but not yet begun\n\n"
        "Activities include outreach calls, pitch meetings, data room setup, "
        "and fundraising presentation preparation. This log provides an auditable "
        "record of all investor engagement for both internal review and board reporting.")

    # 27. Document Control
    pdf.add_page()
    pdf.sec(27, "Tab 13: Document Control")
    pdf.txt(
        "Document Control provides ISO 13485-aligned document lifecycle management. "
        "Every document carries a Document Control Number (DCN), a 5-stage status "
        "workflow, full revision history, and automated review scheduling.")

    pdf.sub("27.1 Summary Bar")
    pdf.txt(
        "At the top of the panel, counter-cards provide an at-a-glance summary:\n\n"
        "  Total      -- Total number of controlled documents\n"
        "  Effective   -- Documents in active use\n"
        "  In Review   -- Documents awaiting approval\n"
        "  Draft       -- New or in-progress documents\n"
        "  Overdue     -- Documents past their scheduled review date (red badge)")

    pdf.sub("27.2 Category Filters")
    pdf.txt(
        "Filter buttons allow viewing documents by category:\n\n"
        "  All Categories  -- Show everything (default)\n"
        "  Regulatory       -- FDA submissions, pre-sub packages, compliance docs\n"
        "  Technical        -- Design specs, algorithm reports, protocol docs\n"
        "  Business         -- Pitch decks, investor materials, term sheets\n"
        "  Legal            -- IP assignments, corporate docs, agreements\n"
        "  Finance          -- Budget reports, burn reports, financial statements\n"
        "  Templates        -- Reusable templates for recurring documents")

    pdf.sub("27.3 Document Table")
    pdf.txt(
        "Each row shows:\n\n"
        "  Category         -- Color-coded badge (Regulatory=blue, Technical=green, etc.)\n"
        "  DCN              -- Unique Document Control Number (e.g., DCN-REG-001)\n"
        "  Document         -- Clickable name opens the Revision History panel\n"
        "  Version          -- Current version number\n"
        "  Last Updated     -- Date of most recent edit\n"
        "  Owner            -- Team member responsible for the document\n"
        "  Linked Milestone -- Associated R-number or T-number milestone\n"
        "  Status           -- Clickable badge (PMP only) to advance the workflow\n\n"
        "The status badge cycles through five lifecycle stages:\n\n"
        "  Draft -> In Review -> Approved -> Effective -> Obsolete\n\n"
        "Status changes are logged to the Audit Trail for DHF traceability.")

    pdf.sub("27.4 Revision History")
    pdf.txt(
        "Click any document name to open a modal panel showing:\n\n"
        "  Document metadata  -- Owner, version, effective date, next review, linked milestone\n"
        "  Revision table     -- Every revision with rev number, date, author, and change description\n\n"
        "This provides full traceability for design control documentation.")

    pdf.sub("27.5 Review Scheduling")
    pdf.txt(
        "Each document has a Next Review date. Documents past their review date are highlighted "
        "with a warning badge and a tinted row background. The summary bar shows the count of "
        "overdue reviews.")

    pdf.sub("27.6 Team Members & Dashboard Roles")
    pdf.txt(
        "The dashboard team consists of four members:\n\n"
        "  Lon Dailey -- Regulatory & Investor Relations (N. America)\n"
        "    Responsibilities: 510(k) preparation, standards compliance,\n"
        "    investor relations for North America, project management\n\n"
        "  Dr. Dai -- Chief Technology Officer\n"
        "    Responsibilities: sEMG algorithm development, EIT prototype,\n"
        "    MyoBus integration, technical documentation\n\n"
        "  Lawrence Liu -- CEO, Company B\n"
        "    Responsibilities: Investor relations (Asia), business strategy,\n"
        "    operations management\n\n"
        "  Danielle Liu -- Accounting\n"
        "    Responsibilities: Monthly burn reports, budget tracking, financial statements")

    # 28. Message Board
    pdf.add_page()
    pdf.sec(28, "Tab 14: Message Board")
    pdf.txt(
        "The Message Board is the dashboard's purpose-driven internal messaging "
        "layer. Every thread maps to one of three intents -- inform, decide, or act "
        "-- and is organized by workstream with an owner, objective, lifecycle, and "
        "priority. Messages are synced in real-time via the server database (Supabase) "
        "with localStorage as a fallback.")

    pdf.sub("28.1 Structured Threads")
    pdf.txt(
        "Each thread has:\n\n"
        "  Title       -- Descriptive name for the conversation\n"
        "  Workstream  -- project / regulatory / engineering / clinical / business / operations\n"
        "  Intent      -- inform (share info), decide (log a decision), act (assign action)\n"
        "  Owner       -- The role that created the thread\n"
        "  Objective   -- Optional statement of purpose\n"
        "  Priority    -- normal / urgent / escalated (visual indicators)\n"
        "  Lifecycle   -- open or resolved (with resolution summary)\n\n"
        "The original Q1-Q30 predefined questions auto-migrate to threads on first "
        "load. Existing messages are preserved via Supabase. New threads can be created "
        "at any time using the 'New Thread' button.")

    pdf.sub("28.2 Decision Visibility")
    pdf.txt(
        "Decisions are first-class objects, not buried in chat:\n\n"
        "  [DECISION] prefix -- Prefix any message with [DECISION] to auto-log it\n"
        "  Log Decision btn  -- Manually log a decision via the thread action bar\n"
        "  Decisions view    -- A dedicated view surfaces all threads with active decisions\n"
        "  Decision cards    -- Each decision shows text, rationale, who made it, and date\n"
        "  Audit trail       -- All decisions are recorded in the audit log")

    pdf.sub("28.3 Four Views")
    pdf.txt(
        "The view switcher provides four perspectives:\n\n"
        "  All Threads  -- Every thread matching current filters\n"
        "  My Items     -- Threads you own or are assigned to\n"
        "  Decisions    -- Threads that have active logged decisions\n"
        "  Executive    -- High-signal view: urgent, escalated, decisions, and resolved threads")

    pdf.sub("28.4 Filters & Summary Dashboard")
    pdf.txt(
        "  Workstream Filter  -- Dropdown to show only one workstream or all\n"
        "  Lifecycle Filter   -- Show open, resolved, or all threads\n"
        "  Sort Order         -- Escalated > urgent > normal, then by most recent message\n\n"
        "Five summary cards at the top:\n\n"
        "  Open Threads       -- Count of open threads\n"
        "  Urgent/Escalated   -- Count of high-priority open threads\n"
        "  Decisions          -- Count of active decisions logged\n"
        "  My Items           -- Threads owned or assigned to current role\n"
        "  Unread Messages    -- Messages not yet read by current role")

    pdf.sub("28.5 Accountability & Actions")
    pdf.txt(
        "  Create Action   -- Assigns a thread to a specific role with a due date\n"
        "  Assignee badge  -- Shows who is responsible on the thread card\n"
        "  Due date        -- Displayed alongside the assignee\n"
        "  Intent tagging  -- Prefix [ACTION] on a message for visual highlighting")

    pdf.sub("28.6 Linked Artifacts")
    pdf.txt(
        "Threads can be connected to other dashboard items:\n\n"
        "  Link types: milestone, risk, gate, document, standard, task\n"
        "  Each linked artifact appears as a badge on the thread card\n"
        "  Links are stored as part of the thread metadata")

    pdf.sub("28.7 Lifecycle Management")
    pdf.txt(
        "  Resolve       -- Mark a thread as resolved with a summary\n"
        "  Reopen        -- Reopen a previously resolved thread\n"
        "  Resolution    -- Displayed on resolved thread cards\n"
        "  Audit trail   -- All lifecycle changes are logged")

    pdf.sub("28.8 Read Receipts & Notifications")
    pdf.txt(
        "  Sent messages   -- Show single check (Unread) or double check (Read)\n"
        "  Received        -- Highlighted with a blue left border when unread\n"
        "  Mark as Read    -- Click the envelope icon to mark a message as read\n"
        "  Tab Badge       -- Red count badge shows total unread for current role\n"
        "  Toast           -- New messages from other parties trigger a slide-up toast\n"
        "  Cross-Tab Sync  -- Messages sync across browser tabs via StorageEvent")

    pdf.sub("28.9 Export & Archive")
    pdf.txt(
        "  Export  -- Downloads all threads and decisions as a .txt file\n"
        "  Archive -- Saves a thread's messages to archive storage and clears them\n"
        "  View Archive / Delete Archive -- Browse or remove archived entries")

    pdf.sub("28.10 Data Storage")
    pdf.txt(
        "Messages sync in real-time to the server database (Supabase). Thread metadata "
        "(title, workstream, intent, owner, lifecycle, linked items) is stored locally "
        "in localStorage under 'ctower_mb_threads'. Decisions are stored under "
        "'ctower_mb_decisions'. Message cache uses 'ctower_qa_messages' as local backup. "
        "Settings and archives also persist across sessions.")

    # 29. Glossary
    pdf.add_page()
    pdf.sec(29, "Glossary of Key Terms")
    pdf.ln(2)
    terms = [
        ("M+N", "Month notation. M+0 = project start (March 2026). M+6 = six months later (Sep 2026). Used throughout for all scheduling."),
        ("PMP", "Project Management Professional. Holds overriding decision authority over all gates."),
        ("510(k)", "FDA premarket notification pathway for Class II medical devices demonstrating substantial equivalence."),
        ("Gate", "A Phase-Gate decision checkpoint. The project cannot advance until the PMP decides to Proceed."),
        ("CR", "Change Request. A formal request from Tech or Business teams to modify a status, requiring PMP approval."),
        ("sEMG", "Surface Electromyography -- Module A. Monitors neural respiratory drive non-invasively."),
        ("EIT", "Electrical Impedance Tomography -- Module B. Cross-sectional images of lung V/Q."),
        ("V/Q", "Ventilation/Perfusion ratio -- key clinical measurement of lung oxygen exchange."),
        ("MyoBus", "Proprietary integration protocol synchronizing sEMG and EIT data with <1ms alignment."),
        ("IKN", "FDA product code for sEMG respiratory monitoring devices."),
        ("DQS", "FDA product code for EIT thoracic imaging devices."),
        ("Pre-Sub / Q-Sub", "Pre-Submission request to FDA for strategy discussion before formal submission."),
        ("ISO 14971", "International standard for medical device risk management (basis of Risk Dashboard)."),
        ("IEC 60601", "Family of standards for medical electrical equipment safety and performance."),
        ("DHF", "Design History File -- the regulated documentation package for device design."),
        ("CAPA", "Corrective and Preventive Action -- formal process for addressing nonconformities."),
        ("Kanban", "Visual task management board with columns representing work stages."),
        ("FAB", "Floating Action Button -- the circular button for quick access to stakeholder inputs."),
        ("IndexedDB", "Browser-based local storage used as a fallback for document persistence."),
        ("Runway", "Number of months the project can continue operating at current burn rate before funds run out."),
        ("NRE", "Non-Recurring Engineering -- one-time engineering costs for manufacturing setup."),
    ]
    for k, v in terms:
        pdf.kv(k, v)
        pdf.ln(1)

    path = os.path.join(OUT_DIR, "Dashboard_Users_Guide_EN.pdf")
    pdf.output(path)
    return path


# ===================== CHINESE GUIDE =====================

class ChineseGuide(FPDF):
    def __init__(self):
        super().__init__()
        font_path = "/Library/Fonts/Arial Unicode.ttf"
        self.add_font("ARUNI", "", font_path, uni=True)
        self.add_font("ARUNI", "B", font_path, uni=True)
        self.add_font("ARUNI", "I", font_path, uni=True)

    def header(self):
        self.set_font("ARUNI", "B", 9)
        self.set_text_color(*GRAY)
        self.cell(0, 6, "\u533b\u7597\u5668\u68b0\u5f00\u53d1\u63a7\u5236\u5854 \u2014 \u7528\u6237\u6307\u5357", align="R")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("ARUNI", "I", 8)
        self.set_text_color(*GRAY)
        self.cell(0, 10, f"\u7b2c {self.page_no()} \u9875 / \u5171 {{nb}} \u9875", align="C")

    def sec(self, num, title):
        self.set_font("ARUNI", "B", 16)
        self.set_text_color(*BLUE)
        self.cell(0, 10, f"{num}. {title}", new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(*BLUE)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(4)

    def sub(self, title):
        self.set_font("ARUNI", "B", 12)
        self.set_text_color(*CN_TEXT)
        self.cell(0, 8, title, new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def txt(self, text):
        self.set_font("ARUNI", "", 10)
        self.set_text_color(*CN_TEXT)
        self.multi_cell(0, 6, text, new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def kv(self, key, val):
        self.set_font("ARUNI", "B", 10)
        self.set_text_color(*BLUE)
        self.cell(0, 6, key, new_x="LMARGIN", new_y="NEXT")
        self.set_font("ARUNI", "", 10)
        self.set_text_color(*CN_TEXT)
        self.multi_cell(0, 6, "  " + val, new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def bul(self, text):
        self.set_font("ARUNI", "", 10)
        self.set_text_color(*CN_TEXT)
        self.multi_cell(0, 6, "  - " + text, new_x="LMARGIN", new_y="NEXT")


# Use a helper constant for Chinese left/right quotation marks
LQ = "\u201c"  # left double quotation mark
RQ = "\u201d"  # right double quotation mark
EM = "\u2014"   # em dash


def build_chinese():
    pdf = ChineseGuide()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()

    # Cover
    pdf.ln(30)
    pdf.set_font("ARUNI", "B", 28)
    pdf.set_text_color(*BLUE)
    pdf.cell(0, 14, "\u63a7\u5236\u5854", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("ARUNI", "", 14)
    pdf.set_text_color(*CN_TEXT)
    pdf.cell(0, 8, "\u533b\u7597\u5668\u68b0\u5f00\u53d1\u4eea\u8868\u76d8", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)
    pdf.set_font("ARUNI", "I", 11)
    pdf.set_text_color(*GRAY)
    pdf.cell(0, 7, "ICU\u547c\u5438\u76d1\u62a4\u6570\u5b57\u5b6a\u751f\u7cfb\u7edf", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 7, "sEMG\u795e\u7ecf\u9a71\u52a8 + EIT\u901a\u6c14/\u704c\u6ce8\u76d1\u6d4b\u5e73\u53f0", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)
    pdf.set_font("ARUNI", "B", 16)
    pdf.set_text_color(*CN_TEXT)
    pdf.cell(0, 10, "\u7528\u6237\u6307\u5357", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(6)
    pdf.set_font("ARUNI", "", 11)
    pdf.set_text_color(*GRAY)
    pdf.cell(0, 7, "\u7248\u672c 1.0 | 2026\u5e743\u6708", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 7, "B\u516c\u53f8\u7f8e\u56fd / \u601d\u5c9a\u79d1\u6280\uff08\u6210\u90fd\uff09\u6709\u9650\u516c\u53f8", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(20)
    pdf.set_font("ARUNI", "I", 10)
    pdf.set_text_color(*GRAY)
    pdf.multi_cell(0, 6,
        "\u672c\u6307\u5357\u8be6\u7ec6\u8bf4\u660ePM\u4eea\u8868\u76d8\u7684\u6bcf\u4e00\u4e2a\u754c\u9762\u5143\u7d20\u3002"
        "\u8be5\u4eea\u8868\u76d8\u4e3a\u53cc\u8bed\uff08\u4e2d/\u82f1\uff09\u9879\u76ee\u7ba1\u7406\u56e2\u961f\u8bbe\u8ba1\uff0c"
        "\u7528\u4e8e\u63a8\u8fdbICU\u547c\u5438\u76d1\u62a4\u6570\u5b57\u5b6a\u751f\u7cfb\u7edf\u7684FDA 510(k)\u5ba1\u6279\u6d41\u7a0b\u3002",
        align="C")

    # 1
    pdf.add_page()
    pdf.sec(1, "\u6982\u8ff0")
    pdf.txt(
        "\u63a7\u5236\u5854\u662f\u9879\u76ee\u7ecf\u7406(PMP)\u7684\u6838\u5fc3\u6307\u6325\u4eea\u8868\u76d8\uff0c"
        "\u7528\u4e8eICU\u547c\u5438\u76d1\u62a4\u6570\u5b57\u5b6a\u751f\u7cfb\u7edf" + EM + EM +
        "\u4e00\u4e2a\u7531\u4e24\u4e2a\u6a21\u5757\u7ec4\u6210\u7684510(k)\u533b\u7597\u5668\u68b0\uff1a\n\n"
        "  \u6a21\u5757A\uff1asEMG\u795e\u7ecf\u547c\u5438\u9a71\u52a8\u76d1\u6d4b\uff08\u4ea7\u54c1\u4ee3\u7801IKN\uff09\n"
        "  \u6a21\u5757B\uff1aEIT\u901a\u6c14/\u704c\u6ce8\u7cfb\u7edf\uff08\u4ea7\u54c1\u4ee3\u7801DQS\uff09\n\n"
        "\u4eea\u8868\u76d8\u59cb\u7ec8\u56f4\u7ed5\u4e00\u4e2a\u6838\u5fc3\u95ee\u9898\u8fd0\u884c\uff1a\n"
        + LQ + "\u6211\u4eec\u662f\u5426\u4ecd\u5728FDA\u6279\u51c6\u7684\u6b63\u8f68\u4e0a" + EM + EM + "\u6709\u4ec0\u4e48\u98ce\u9669\uff1f" + RQ)
    pdf.txt(
        "PMP\uff08\u9879\u76ee\u7ba1\u7406\u4e13\u4e1a\u4eba\u5458\uff09\u5bf9\u6240\u6709\u95e8\u63a7\u51b3\u7b56\u62e5\u6709\u6700\u9ad8\u6743\u9650\u3002"
        "\u5546\u4e1a\u548c\u6280\u672f\u56e2\u961f\u63d0\u4f9b\u8f93\u5165\uff0c\u4f46PMP\u505a\u51fa\u6700\u7ec8\u51b3\u7b56\u3002")

    # 2
    pdf.sec(2, "\u9876\u90e8\u680f")
    pdf.txt("\u5c4f\u5e55\u9876\u90e8\u7684\u56fa\u5b9a\u6807\u9898\u680f\u5305\u542b\u4ee5\u4e0b\u5143\u7d20\uff1a")

    pdf.sub("2.1 \u6807\u5fd7\u4e0e\u6807\u9898")
    pdf.txt(
        "\u533b\u7597\u6807\u5fd7\u56fe\u6807\u65c1\u8fb9\u662f" + LQ + "\u63a7\u5236\u5854" + RQ +
        "\u548c\u526f\u6807\u9898" + LQ + "ICU\u547c\u5438\u76d1\u62a4\u6570\u5b57\u5b6a\u751f" + RQ + "\u3002"
        "\u5207\u6362\u8bed\u8a00\u65f6\uff0c\u8fd9\u4e9b\u6587\u5b57\u4f1a\u76f8\u5e94\u53d8\u5316\u3002")

    pdf.sub("2.2 \u6838\u5fc3\u95ee\u9898")
    pdf.txt(
        "\u680f\u4e2d\u592e\u7684\u659c\u4f53\u6587\u5b57\u663e\u793a\uff1a"
        + LQ + "\u6211\u4eec\u662f\u5426\u4ecd\u5728FDA\u6279\u51c6\u7684\u6b63\u8f68\u4e0a" + EM + EM + "\u6709\u4ec0\u4e48\u98ce\u9669\uff1f" + RQ +
        "\u8fd9\u662f\u6574\u4e2a\u4eea\u8868\u76d8\u8bbe\u8ba1\u8981\u56de\u7b54\u7684\u6838\u5fc3\u95ee\u9898\u3002"
        "\u6bcf\u4e2a\u9762\u677f\u3001\u6307\u6807\u548c\u95e8\u63a7\u90fd\u56f4\u7ed5\u8fd9\u4e2a\u95ee\u9898\u8fd0\u8f6c\u3002")

    pdf.sub("2.3 PMP\u6743\u9650\u5fbd\u7ae0")
    pdf.txt(
        "\u7ea2\u8272\u76fe\u724c\u5fbd\u7ae0\uff08PMP\u6743\u9650\uff09\u8868\u793a\u9879\u76ee\u7ba1\u7406\u4e13\u4e1a\u4eba\u5458\u62e5\u6709\u6700\u9ad8\u51b3\u7b56\u6743\u3002"
        "\u5728\u95e8\u63a7\u7cfb\u7edf\u4e2d\uff0c\u53ea\u6709PMP\u53ef\u4ee5\u8bbe\u7f6e\u95e8\u63a7\u51b3\u7b56\uff08\u901a\u8fc7/\u9700\u66f4\u591a\u6570\u636e/\u505c\u6b62\uff09\u3002"
        "\u5546\u4e1a\u548c\u6280\u672f\u56e2\u961f\u63d0\u4ea4\u8f93\u5165\uff0c\u4f46PMP\u7684\u51b3\u7b56\u662f\u6700\u7ec8\u7684\u3002")

    pdf.sub("2.4 \u8bed\u8a00\u5207\u6362\uff08EN / \u4e2d\uff09")
    pdf.txt(
        "\u70b9\u51fb\u8bed\u8a00\u6309\u94ae\u53ef\u5728\u82f1\u6587(EN)\u548c\u4e2d\u6587(\u4e2d)\u4e4b\u95f4\u5207\u6362\u6574\u4e2a\u4eea\u8868\u76d8\u3002"
        "\u6240\u6709\u6807\u7b7e\u3001\u63cf\u8ff0\u3001\u91cc\u7a0b\u7891\u6807\u9898\u3001\u98ce\u9669\u63cf\u8ff0\u548c\u95e8\u63a7\u6807\u51c6\u90fd\u4f1a\u5207\u6362\u5230\u6240\u9009\u8bed\u8a00\u3002"
        "HTML\u7684lang\u5c5e\u6027\u4e5f\u4f1a\u66f4\u65b0\uff08en \u2192 zh-CN\uff09\u3002")

    pdf.sub("2.5 \u5f53\u524d\u6708\u4efd\u5fbd\u7ae0 " + EM + " " + LQ + "\u5f53\u524d: M+0" + RQ)
    pdf.txt(
        "\u8fd9\u662f\u4eea\u8868\u76d8\u4e0a\u6700\u91cd\u8981\u7684\u6307\u6807\u4e4b\u4e00\u3002\n\n"
        + LQ + "M+" + RQ + "\u4ee3\u8868" + LQ + "\u9879\u76ee\u542f\u52a8\u540e\u7684\u6708\u6570" + RQ +
        "\u3002\u9879\u76ee\u65f6\u95f4\u7ebf\u4ee5\u57fa\u51c6\u65e5\u671f\uff082026\u5e743\u6708\uff09\u540e\u7684\u6708\u6570\u8ba1\u91cf\u3002\n\n"
        "\u793a\u4f8b\uff1a\n"
        "  M+0 = 2026\u5e743\u6708\uff08\u9879\u76ee\u542f\u52a8\uff09\n"
        "  M+2 = 2026\u5e745\u6708\uff08FDA\u9884\u63d0\u4ea4\u4f1a\u8bae\uff09\n"
        "  M+6 = 2026\u5e749\u6708\uff08510(k) sEMG\u63d0\u4ea4\uff09\n"
        "  M+9 = 2026\u5e7412\u6708\uff08sEMG\u9884\u8ba1\u83b7\u6279\uff09\n"
        "  M+23 = 2028\u5e742\u6708\uff08\u5168\u5e73\u53f0\u83b7\u6279\uff09\n\n"
        + LQ + "\u5f53\u524d: M+0" + RQ + "\u8868\u793a\u9879\u76ee\u76ee\u524d\u5728\u7b2c0\u4e2a\u6708" + EM + EM + "\u521a\u521a\u5f00\u59cb\u3002"
        "\u968f\u7740\u9879\u76ee\u63a8\u8fdb\uff0c\u6b64\u6570\u5b57\u9012\u589e\uff0c\u6240\u6709\u4e0b\u6e38\u8ba1\u7b97\u76f8\u5e94\u66f4\u65b0\u3002")

    # 3
    pdf.add_page()
    pdf.sec(3, "\u72b6\u6001\u6458\u8981\u680f")
    pdf.txt("\u9009\u9879\u5361\u4e0b\u65b9\u7684\u516d\u5f20\u5361\u7247\u63d0\u4f9b\u6574\u4e2a\u9879\u76ee\u7684\u5feb\u901f\u5065\u5eb7\u68c0\u67e5\uff1a")

    pdf.sub("3.1 \u603b\u4f53\u72b6\u6001")
    pdf.txt(
        "\u663e\u793a\u4e09\u79cd\u72b6\u6001\u4e4b\u4e00\uff0c\u5e26\u989c\u8272\u7f16\u7801\uff1a\n\n"
        "  \u6b63\u8f68\uff08\u7eff\u8272\uff09" + EM + " \u7ea2\u8272\u98ce\u9669\u5c11\u4e8e1\u4e2a\u3002\u4e00\u5207\u6b63\u5e38\u3002\n"
        "  \u6709\u98ce\u9669\uff08\u9ec4\u8272\uff09" + EM + " \u5b58\u57281-2\u4e2a\u7ea2\u8272\u98ce\u9669\u3002\u9700\u8981\u5173\u6ce8\u3002\n"
        "  \u53d7\u963b\uff08\u7ea2\u8272\uff09" + EM + " 3\u4e2a\u6216\u66f4\u591a\u7ea2\u8272\u98ce\u9669\u3002\u9700\u8981\u7d27\u6025\u5e72\u9884\u3002\n\n"
        "\u6b64\u503c\u7531\u98ce\u9669\u767b\u8bb0\u8868\u81ea\u52a8\u8ba1\u7b97\u3002")

    pdf.sub("3.2 \u4e0b\u4e00\u95e8\u63a7")
    pdf.txt(
        "\u663e\u793a\u4e0b\u4e00\u4e2a\u5373\u5c06\u5230\u6765\u7684\u51b3\u7b56\u95e8\u63a7\u3002"
        "\u5f53\u95e8\u63a7\u72b6\u6001\u4e3a" + LQ + "\u5df2\u6279\u51c6" + RQ + "\u3001"
        "\u51b3\u7b56\u4e3a" + LQ + "\u7ee7\u7eed" + RQ + "\u3001"
        "\u6216\u6240\u6709\u51c6\u5219\u5fbd\u7ae0\u5747\u6807\u8bb0\u4e3a\u5b8c\u6210\u65f6\uff0c"
        "\u8be5\u95e8\u63a7\u89c6\u4e3a\u5df2\u5b8c\u6210\u3002"
        "\u5f53\u524d\u95e8\u63a7\u7684\u6240\u6709\u51c6\u5219\u6ee1\u8db3\u540e\uff0c\u6307\u6807\u4f1a\u81ea\u52a8\u63a8\u8fdb\u3002"
        "\u683c\u5f0f\uff1a" + LQ + "G1 (M+3)" + RQ +
        "\u8868\u793a\u95e8\u63a71\u7684\u76ee\u6807\u662f\u7b2c3\u4e2a\u6708\u3002"
        "\u8fd9\u544a\u8bc9PMP\u4e0b\u4e00\u4e2a\u51b3\u7b56\u68c0\u67e5\u70b9\u5373\u5c06\u5230\u6765\u3002")

    pdf.sub("3.3 \u7ea2\u8272\u98ce\u9669")
    pdf.txt(
        "ISO 14971\u98ce\u9669\u767b\u8bb0\u8868\u4e2d\u5206\u7c7b\u4e3a\u7ea2\u8272\uff08\u9ad8\u4e25\u91cd\u6027+\u6709\u610f\u4e49\u7684\u6982\u7387\uff09\u7684\u98ce\u9669\u6570\u91cf\u3002"
        "\u7ea2\u8272\u98ce\u9669\u8ba1\u6570\u8fbe\u52303\u4e2a\u6216\u4ee5\u4e0a\u4f1a\u89e6\u53d1" + LQ + "\u53d7\u963b" + RQ + "\u603b\u4f53\u72b6\u6001\u3002")

    pdf.sub("3.4 \u5f85\u5904\u7406\u8f93\u5165")
    pdf.txt(
        "\u6765\u81ea\u5546\u4e1a\u6216\u6280\u672f\u56e2\u961f\u7684\u3001\u5904\u4e8e" + LQ + "\u5f85\u5ba1\u6838" + RQ +
        "\u72b6\u6001\u7684\u5229\u76ca\u76f8\u5173\u65b9\u8f93\u5165\u6570\u91cf" + EM + EM +
        "\u5373PMP\u5c1a\u672a\u5ba1\u6838\u548c\u56de\u5e94\u7684\u8f93\u5165\u3002\u8fd9\u4e5f\u53cd\u6620\u5728\u6d6e\u52a8\u64cd\u4f5c\u6309\u94ae(FAB)\u7684\u5fbd\u7ae0\u4e0a\u3002")

    pdf.sub("3.5 \u8ddd\u4e0b\u4e00\u91cc\u7a0b\u7891")
    pdf.txt(
        "\u4e0b\u4e00\u4e2a\u672a\u5b8c\u6210\u91cc\u7a0b\u7891\u7684\u9884\u4f30\u65f6\u95f4\u3002\u8ba1\u7b97\u516c\u5f0f\uff1a\n"
        "  (\u4e0b\u4e00\u91cc\u7a0b\u7891\u6708\u6570 - \u5f53\u524d\u6708\u6570) \u00d7 30\u5929\n\n"
        "\u793a\u4f8b\uff1a\u5982\u679c\u5f53\u524d\u6708\u4efd\u662fM+0\uff0c\u4e0b\u4e00\u4e2a\u91cc\u7a0b\u7891\u5728M+1\uff0c\u5219\u663e\u793a"
        + LQ + "~30d" + RQ + "\u3002")

    pdf.sub("3.6 \u8d44\u91d1\u8ddd\u79bb")
    pdf.txt(
        "\u663e\u793a\u5728\u5f53\u524d\u71c3\u70e7\u7387\u4e0b\u8fd8\u53ef\u8fd0\u8425\u591a\u5c11\u4e2a\u6708\u3002"
        "\u8ba1\u7b97\u516c\u5f0f\uff1a\u73b0\u91d1 \u00f7 \u6708\u5ea6\u71c3\u70e7\u3002\u503c\u5e26\u989c\u8272\u7f16\u7801\uff1a\n\n"
        "  \u7eff\u8272 " + EM + " 7\u4e2a\u6708\u4ee5\u4e0a\u3002\u8d22\u52a1\u5065\u5eb7\u3002\n"
        "  \u6a59\u8272 " + EM + " 4-6\u4e2a\u6708\u3002\u5e94\u5f00\u59cb\u878d\u8d44/\u6210\u672c\u5ba1\u67e5\u3002\n"
        "  \u7ea2\u8272 " + EM + " 3\u4e2a\u6708\u6216\u66f4\u5c11\u3002\u7d27\u6025" + EM + EM + "\u9700\u7acb\u5373\u91c7\u53d6\u878d\u8d44\u884c\u52a8\u3002\n\n"
        "\u70b9\u51fb" + LQ + "\u8d44\u91d1/\u8ddd\u79bb" + RQ + "\u9009\u9879\u5361\u67e5\u770b\u5b8c\u6574\u7684\u8d22\u52a1\u660e\u7ec6\u3001"
        "\u878d\u8d44\u65f6\u95f4\u7ebf\u548cAPI\u96c6\u6210\u9762\u677f\u3002")

    # 4
    pdf.add_page()
    pdf.sec(4, "\u5bfc\u822a\u9009\u9879\u5361")
    pdf.txt(
        "\u5341\u56db\u4e2a\u9009\u9879\u5361\u63d0\u4f9b\u4e3b\u8981\u4eea\u8868\u76d8\u9762\u677f\u7684\u8bbf\u95ee\u3002"
        "\u6d3b\u52a8\u9009\u9879\u5361\u4ee5\u84dd\u8272\u4e0b\u5212\u7ebf\u9ad8\u4eae\u663e\u793a\u3002")
    pdf.ln(2)
    pdf.kv("\u53cc\u8f68\u89c6\u56fe", "\u6280\u672f+\u6cd5\u89c4\u91cc\u7a0b\u7891\u5e76\u6392\u663e\u793a")
    pdf.kv("\u95e8\u63a7\u7cfb\u7edf", "\u5e26PMP\u6743\u9650\u63a7\u5236\u7684\u51b3\u7b56\u68c0\u67e5\u70b9")
    pdf.kv("\u98ce\u9669\u4eea\u8868\u76d8", "ISO 14971\u98ce\u9669\u767b\u8bb0\u8868\uff0c\u5e26\u7b5b\u9009\u548c\u524d5\u6392\u540d")
    pdf.kv("\u65f6\u95f4\u7ebf", "\u6280\u672f\u91cc\u7a0b\u7891\u7684\u5546\u4e1a\u8bed\u8a00\u7ffb\u8bd1")
    pdf.kv("\u6cd5\u89c4\u8ffd\u8e2a", "IEC/ISO/21 CFR\u5408\u89c4\u6807\u51c6\u77e9\u9635")
    pdf.kv("\u8d44\u91d1/\u8dd1\u9053", "\u8d22\u52a1\u72b6\u51b5\u3001\u71c3\u70e7\u7387\u3001\u878d\u8d44\u91cc\u7a0b\u7891\u548cAPI\u96c6\u6210")
    pdf.kv("\u884c\u52a8\u9879", "\u4efb\u52a1\u770b\u677f\u3001DHF\u6587\u6863\u8ffd\u8e2a\u548cCAPA\u65e5\u5fd7")
    pdf.kv("\u9884\u7b97", "\u6309\u7c7b\u522b\u7684\u9884\u7b97\u4e0e\u5b9e\u9645\u652f\u51fa")
    pdf.kv("\u8d44\u6e90", "\u56e2\u961f\u5206\u914d\u548c\u4ea7\u80fd\u5229\u7528")
    pdf.kv("\u4f9b\u5e94\u5546", "\u786c\u4ef6\u7ec4\u4ef6\u4f9b\u5e94\u5546\u8ffd\u8e2a")
    pdf.kv("\u5ba1\u8ba1\u8ffd\u8e2a", "\u6240\u6709\u4eea\u8868\u76d8\u64cd\u4f5c\u7684\u65f6\u95f4\u5e8f\u65e5\u5fd7")
    pdf.kv("\u7f8e\u56fd\u6295\u8d44", "\u5317\u7f8e\u878d\u8d44\u7ba1\u9053\u3001\u6295\u8d44\u8005\u8ffd\u8e2a\u548cIR\u6d3b\u52a8")
    pdf.kv("\u6587\u6863\u63a7\u5236", "ISO 13485\u5bf9\u9f50\u7684\u6587\u6863\u751f\u547d\u5468\u671f\u3001\u4fee\u8ba2\u5386\u53f2\u548c\u5ba1\u67e5\u8ba1\u5212")
    pdf.kv("\u7559\u8a00\u677f", "PMP\u4e0e\u5229\u76ca\u76f8\u5173\u65b9\u4e4b\u95f4\u7684\u53cc\u5411\u7ebf\u7a0b\u5f0f\u6280\u672f\u5bf9\u8bdd\u6d88\u606f")

    # 5
    pdf.add_page()
    pdf.sec(5, "\u9009\u9879\u53611\uff1a\u53cc\u8f68\u4eea\u8868\u76d8")
    pdf.txt(
        "\u8fd9\u662f\u9ed8\u8ba4\u89c6\u56fe\u3002\u663e\u793a\u4e24\u4e2a\u5e76\u884c\u5217\uff1a\n\n"
        "  \u5de6\u4fa7\uff1a\u6280\u672f\u8def\u5f84 " + EM + " \u7814\u53d1\u3001\u539f\u578b\u3001\u6d4b\u8bd5\u3001\u9a8c\u8bc1\u91cc\u7a0b\u7891\n"
        "  \u53f3\u4fa7\uff1a\u6cd5\u89c4\u8def\u5f84 " + EM + " FDA\u63d0\u4ea4\u3001\u5ba1\u6838\u3001\u6279\u51c6\u3001\u6cd5\u5f8b\u4e8b\u52a1\n\n"
        "\u4e24\u5217\u4e4b\u95f4\u662f\u4e00\u4e2a\u4e2d\u592e\u65f6\u95f4\u7ebf\u8f74\uff0c\u70b9\u4ee3\u8868\u6bcf\u4e2a\u6708\u4efd\u3002"
        "\u5f53\u524d\u6708\u4efd\u53ca\u4e4b\u524d\u7684\u70b9\u4eae\u84dd\u8272\u3002\u672a\u6765\u6708\u4efd\u4e3a\u7070\u8272\u3002")

    pdf.sub("5.1 \u91cc\u7a0b\u7891\u5361\u7247")
    pdf.txt(
        "\u6bcf\u5f20\u91cc\u7a0b\u7891\u5361\u7247\u5305\u542b\uff1a\n\n"
        "  \u6807\u9898\uff1a\u91cc\u7a0b\u7891\u5185\u5bb9\n"
        "  M+N \u5fbd\u7ae0\uff1a\u6b64\u91cc\u7a0b\u7891\u76ee\u6807\u5728\u54ea\u4e2a\u9879\u76ee\u6708\u4efd\n"
        "  \u63cf\u8ff0\uff1a\u91cc\u7a0b\u7891\u7684\u6280\u672f\u8be6\u60c5\n"
        "  \u72b6\u6001\u5fbd\u7ae0\uff1a\u4e09\u79cd\u72b6\u6001\u4e4b\u4e00\uff1a")
    pdf.bul("\u5df2\u5b8c\u6210\uff08\u7eff\u8272\uff09" + EM + " \u91cc\u7a0b\u7891\u5df2\u6210\u529f\u5b8c\u6210")
    pdf.bul("\u8fdb\u884c\u4e2d\uff08\u9ec4\u8272\uff09" + EM + " \u6b63\u5728\u8fdb\u884c\u4e2d")
    pdf.bul("\u672a\u5f00\u59cb\uff08\u7070\u8272\uff09" + EM + " \u5c1a\u672a\u5f00\u59cb")
    pdf.ln(2)
    pdf.txt(
        "\u5361\u7247\u6709\u4e00\u6761\u4e0e\u5176\u72b6\u6001\u5339\u914d\u7684\u5f69\u8272\u5de6\u8fb9\u6846\uff1a\n"
        "  \u7eff\u8272\u8fb9\u6846 = \u5df2\u5b8c\u6210\n"
        "  \u9ec4\u8272\u8fb9\u6846 = \u8fdb\u884c\u4e2d\n"
        "  \u7070\u8272\u8fb9\u6846 = \u672a\u5f00\u59cb")

    pdf.sub("5.2 \u91cc\u7a0b\u7891\u8d1f\u8d23\u65b9")
    pdf.txt(
        "\u6bcf\u4e2a\u91cc\u7a0b\u7891\u6709\u4e00\u4e2a\u8d1f\u8d23\u65b9\u7c7b\u522b\uff1a\n"
        "  tech " + EM + " \u5de5\u7a0b/\u7814\u53d1\u56e2\u961f\u8d1f\u8d23\n"
        "  regulatory " + EM + " \u6cd5\u89c4\u4e8b\u52a1\u56e2\u961f\u8d1f\u8d23\n"
        "  business " + EM + " \u5546\u4e1a/\u6cd5\u5f8b/\u6295\u8d44\u56e2\u961f\u8d1f\u8d23")

    # 6
    pdf.add_page()
    pdf.sec(6, "\u9009\u9879\u53612\uff1a\u95e8\u63a7\u7cfb\u7edf")
    pdf.txt(
        "\u95e8\u63a7\u7cfb\u7edf\u5b9e\u65bd\u9636\u6bb5-\u95e8\u63a7\u9879\u76ee\u7ba1\u7406\u65b9\u6cd5\u8bba\u3002"
        "\u5171\u6709\u516d\u4e2a\u95e8\u63a7\uff08G1\u2013G6\uff09\uff0c\u6bcf\u4e2a\u4ee3\u8868\u4e00\u4e2a\u5173\u952e\u51b3\u7b56\u68c0\u67e5\u70b9\u3002"
        "\u95e8\u63a7\u4ee5\u6c34\u5e73\u7ba1\u7ebf\u65b9\u5f0f\u663e\u793a\uff0c\u4ee5\u7bad\u5934\u76f8\u8fde\u3002")

    pdf.sub("6.1 \u95e8\u63a7\u5361\u7247")
    pdf.txt(
        "\u6bcf\u5f20\u95e8\u63a7\u5361\u7247\u663e\u793a\uff1a\n\n"
        "  \u95e8\u63a7\u7f16\u53f7\uff1aG1\u3001G2\u3001G3\u7b49\n"
        "  \u6807\u9898\uff1a\u95e8\u63a7\u4ee3\u8868\u7684\u5185\u5bb9\n"
        "  \u76ee\u6807\u6708\u4efd\uff1a" + LQ + "\u76ee\u6807: M+3" + RQ + "\u8868\u793a\u6b64\u95e8\u63a7\u5e94\u5728\u7b2c3\u4e2a\u6708\u8fbe\u5230\n"
        "  \u6807\u51c6\u8fdb\u5ea6\uff1a" + LQ + "2/4 \u6807\u51c6\u5df2\u6ee1\u8db3" + RQ + "\uff0c\u5e26\u8fdb\u5ea6\u6761\n"
        "  \u72b6\u6001\u6761\uff1a\u5e95\u90e8\u4e00\u6761\u5f69\u8272\u6761\u8868\u793a\u72b6\u6001")

    pdf.sub("6.2 \u95e8\u63a7\u72b6\u6001\uff08\u989c\u8272\u7f16\u7801\uff09")
    pdf.txt(
        "  \u7070\u8272\uff08\u672a\u5f00\u59cb\uff09" + EM + " \u95e8\u63a7\u5c1a\u672a\u8bc4\u4f30\n"
        "  \u9ec4\u8272\uff08\u5f85\u5b9a\uff09" + EM + " \u95e8\u63a7\u6b63\u5728\u5ba1\u67e5\u4e2d\u6216\u9700\u8981\u66f4\u591a\u6570\u636e\n"
        "  \u7eff\u8272\uff08\u5df2\u6279\u51c6\uff09" + EM + " PMP\u5df2\u51b3\u5b9a\u901a\u8fc7\n"
        "  \u7ea2\u8272\uff08\u53d7\u963b\uff09" + EM + " PMP\u5df2\u51b3\u5b9a\u505c\u6b62")

    pdf.sub("6.3 \u95e8\u63a7\u8be6\u60c5\u5f39\u7a97")
    pdf.txt("\u70b9\u51fb\u4efb\u4f55\u95e8\u63a7\u5361\u7247\u4f1a\u6253\u5f00\u8be6\u7ec6\u5f39\u7a97\uff0c\u5305\u542b\uff1a")
    pdf.bul("\u6807\u51c6\u6e05\u5355 " + EM + " \u6bcf\u4e2a\u6807\u51c6\u6709\u4e00\u4e2a\u53ef\u70b9\u51fb\u7684\u590d\u9009\u6846\u3002\u9a8c\u8bc1\u540e\u52fe\u9009\u3002\u8fdb\u5ea6\u6761\u5b9e\u65f6\u66f4\u65b0\u3002")
    pdf.bul("PMP\u51b3\u7b56\u6309\u94ae " + EM + " \u4ec5PMP\u4f7f\u7528\u7684\u4e09\u4e2a\u6309\u94ae\uff1a\n"
            "    \u901a\u8fc7\uff08\u7eff\u8272\uff09" + EM + " \u6279\u51c6\u5e76\u8fdb\u5165\u4e0b\u4e00\u9636\u6bb5\n"
            "    \u9700\u66f4\u591a\u6570\u636e\uff08\u9ec4\u8272\uff09" + EM + " \u8bf7\u6c42\u989d\u5916\u8bc1\u636e\n"
            "    \u505c\u6b62\uff08\u7ea2\u8272\uff09" + EM + " \u6682\u505c\u76f4\u5230\u95ee\u9898\u89e3\u51b3")
    pdf.bul("\u5229\u76ca\u76f8\u5173\u65b9\u8f93\u5165 " + EM + " \u4e0e\u6b64\u95e8\u63a7\u76f8\u5173\u7684\u6280\u672f\u6216\u5546\u4e1a\u56e2\u961f\u8f93\u5165\u3002")
    pdf.bul("\u95e8\u63a7\u5907\u6ce8 " + EM + " PMP\u6dfb\u52a0\u7684\u81ea\u7531\u6587\u672c\u5907\u6ce8\u3002\u6bcf\u6761\u5907\u6ce8\u5e26\u65f6\u95f4\u6233\u3002")

    pdf.sub("6.4 \u516d\u4e2a\u95e8\u63a7")
    pdf.kv("G1 (M+3)", "sEMG\u8bbe\u8ba1\u9a8c\u8bc1\u5b8c\u6210")
    pdf.kv("G2 (M+2)", "\u9884\u63d0\u4ea4FDA\u53cd\u9988\u5df2\u6536\u5230")
    pdf.kv("G3 (M+6)", "510(k) sEMG\u63d0\u4ea4\u5c31\u7eea")
    pdf.kv("G4 (M+9)", "sEMG\u6a21\u5757\u5546\u4e1a\u53d1\u5e03")
    pdf.kv("G5 (M+17)", "EIT 510(k)\u63d0\u4ea4\u5c31\u7eea")
    pdf.kv("G6 (M+23)", "\u5b8c\u6574\u5e73\u53f0\u53d1\u5e03 " + EM + " FDA\u5df2\u6279\u51c6")

    # 7
    pdf.add_page()
    pdf.sec(7, "\u9009\u9879\u53613\uff1a\u98ce\u9669\u4eea\u8868\u76d8")
    pdf.txt(
        "\u98ce\u9669\u4eea\u8868\u76d8\u5b9e\u65bdISO 14971\u533b\u7597\u5668\u68b0\u98ce\u9669\u7ba1\u7406\u65b9\u6cd5\u8bba\u3002"
        "\u63d0\u4f9b\u6240\u6709\u5df2\u8bc6\u522b\u98ce\u9669\u7684\u53ef\u89c6\u5316\u6982\u89c8\u3002")

    pdf.sub("7.1 \u98ce\u9669\u7b5b\u9009\u5668")
    pdf.txt(
        "\u9876\u90e8\u56db\u4e2a\u7b5b\u9009\u6309\u94ae\uff1a\n\n"
        "  \u5168\u90e8 " + EM + " \u663e\u793a\u6240\u6709\u98ce\u9669\uff08\u9ed8\u8ba4\uff09\n"
        "  \u7ea2\u8272 " + EM + " \u4ec5\u663e\u793a\u9ad8\u4f18\u5148\u7ea7\u98ce\u9669\n"
        "  \u9ec4\u8272 " + EM + " \u4ec5\u663e\u793a\u4e2d\u4f18\u5148\u7ea7\u98ce\u9669\n"
        "  \u7eff\u8272 " + EM + " \u4ec5\u663e\u793a\u4f4e\u4f18\u5148\u7ea7\u98ce\u9669")

    pdf.sub("7.2 \u98ce\u9669\u5361\u7247")
    pdf.txt(
        "\u6bcf\u5f20\u98ce\u9669\u5361\u7247\u663e\u793a\uff1a\n\n"
        "  \u98ce\u9669ID\uff1a\u5982RISK-001\n"
        "  \u98ce\u9669\u7b49\u7ea7\u5fbd\u7ae0\uff1a\u7ea2\u8272/\u9ec4\u8272/\u7eff\u8272\n"
        "  \u6807\u9898\uff1a\u98ce\u9669\u63cf\u8ff0\n"
        "  \u4e25\u91cd\u6027\uff1a\u9ad8/\u4e2d/\u4f4e\n"
        "  \u53ef\u80fd\u6027\uff1a\u9ad8/\u4e2d/\u4f4e/\u6781\u4f4e\n"
        "  \u6a21\u5757\uff1a\u53d7\u5f71\u54cd\u7684\u8bbe\u5907\u6a21\u5757\n"
        "  \u63a7\u5236\u63aa\u65bd\uff1a\u5df2\u5b9e\u65bd\u7684\u98ce\u9669\u7f13\u89e3\u63a7\u5236\n"
        "  \u7f13\u89e3\u72b6\u6001\uff1a\u5df2\u5b8c\u6210/\u8fdb\u884c\u4e2d/\u672a\u5f00\u59cb")

    pdf.sub("7.3 \u98ce\u9669\u7b49\u7ea7\u8ba1\u7b97")
    pdf.txt(
        "\u98ce\u9669\u7b49\u7ea7\u9075\u5faa\u4e25\u91cd\u6027\u00d7\u6982\u7387\u77e9\u9635\uff1a\n\n"
        "  \u7ea2\u8272 = \u9700\u8981\u7acb\u5373\u5173\u6ce8\u7684\u9ad8\u4e25\u91cd\u6027\u98ce\u9669\n"
        "  \u9ec4\u8272 = \u6b63\u5728\u79ef\u6781\u76d1\u63a7\u7684\u4e2d\u7b49\u98ce\u9669\n"
        "  \u7eff\u8272 = \u5df2\u6709\u5145\u5206\u63a7\u5236\u7684\u4f4e\u98ce\u9669\n\n"
        "\u7ea2\u8272\u98ce\u9669\u6570\u91cf\u76f4\u63a5\u5f71\u54cd\u603b\u4f53\u72b6\u6001\uff1a\n"
        "  3+\u7ea2\u8272 = \u53d7\u963b\uff1b1-2\u4e2a = \u6709\u98ce\u9669\uff1b0\u4e2a = \u6b63\u8f68\u3002")

    pdf.sub("7.4 \u672c\u5468\u524d5\u5927\u98ce\u9669")
    pdf.txt(
        "\u98ce\u9669\u7f51\u683c\u4e0b\u65b9\u662f\u6392\u540d\u5217\u8868\uff0c\u663e\u793a\u524d5\u4e2a\u6700\u9ad8\u4f18\u5148\u7ea7\u98ce\u9669\u3002"
        "\u6309\u98ce\u9669\u7b49\u7ea7\u6392\u5e8f\uff0c\u7136\u540e\u6309\u4e25\u91cd\u6027\u6392\u5e8f\u3002")

    # 8
    pdf.add_page()
    pdf.sec(8, "\u9009\u9879\u53614\uff1a\u65f6\u95f4\u7ebf " + EM + " \u5546\u4e1a\u7ffb\u8bd1")
    pdf.txt(
        "\u6b64\u9009\u9879\u5361\u4e13\u4e3a\u5546\u4e1a\u5229\u76ca\u76f8\u5173\u65b9\u548c\u6295\u8d44\u8005\u8bbe\u8ba1\u3002"
        "\u6bcf\u4e2a\u65f6\u95f4\u7ebf\u4e8b\u4ef6\u5e76\u6392\u663e\u793a\u4e24\u5217\uff1a\n\n"
        "  \u5de6\u4fa7\uff08\u84dd\u8272\u6807\u9898\uff09\uff1a\u5de5\u7a0b\u672f\u8bed\u63cf\u8ff0\n"
        "  \u53f3\u4fa7\uff08\u6a59\u8272\u6807\u9898\uff09\uff1a\u5bf9\u4e1a\u52a1\u7684\u610f\u4e49\n\n"
        "\u6bcf\u4e2a\u4e8b\u4ef6\u6709\u4e00\u4e2a\u6708\u4efd\u5fbd\u7ae0\u548c\u4e00\u4e2a\u989c\u8272\u7f16\u7801\u7684\u70b9\uff1a")
    pdf.bul("\u7ea2\u70b9\uff08\u5173\u952e\uff09" + EM + " \u91cd\u5927\u5546\u4e1a\u5f71\u54cd\uff0c\u9700\u8981\u6295\u8d44\u8005\u5173\u6ce8")
    pdf.bul("\u9ec4\u70b9\uff08\u8b66\u544a\uff09" + EM + " \u663e\u8457\u7684\u6210\u672c\u6216\u8fdb\u5ea6\u5f71\u54cd")
    pdf.bul("\u84dd\u70b9\uff08\u4e2d\u6027\uff09" + EM + " \u6807\u51c6\u8fdb\u5ea6\u6807\u8bb0")

    pdf.ln(2)
    pdf.sub("8.1 \u65f6\u95f4\u7ebf\u4e8b\u4ef6")
    pdf.kv("M+0", "\u9884\u63d0\u4ea4\u5df2\u63d0\u4ea4 \u2192 FDA\u63a5\u89e6\u542f\u52a8")
    pdf.kv("M+2", "FDA\u9884\u63d0\u4ea4\u4f1a\u8bae \u2192 \u5173\u952e\u6295\u8d44\u8005\u4fe1\u53f7\uff08\u5173\u952e\uff09")
    pdf.kv("M+3", "\u53f0\u67b6\u6d4b\u8bd5\u5f00\u59cb \u2192 \u63d0\u4ea4\u524d\u6700\u5927\u652f\u51fa\uff08\u8b66\u544a\uff09")
    pdf.kv("M+6", "510(k) sEMG\u5df2\u63d0\u4ea4 \u2192 \u6295\u8d44\u8005\u4fe1\u5fc3\u68c0\u67e5\u70b9\uff08\u5173\u952e\uff09")
    pdf.kv("M+9", "sEMG\u83b7\u6279 \u2192 A\u6a21\u5757\u53ef\u4ea7\u751f\u6536\u5165\uff08\u5173\u952e\uff09")
    pdf.kv("M+12", "EIT\u6d4b\u8bd5\u5f00\u59cb \u2192 \u9700\u8981\u7b2c\u4e8c\u7b14\u4e3b\u8981\u6295\u8d44\uff08\u8b66\u544a\uff09")
    pdf.kv("M+17", "510(k) EIT\u5df2\u63d0\u4ea4 \u2192 \u6218\u7565\u5408\u4f5c\u53ef\u884c\uff08\u5173\u952e\uff09")
    pdf.kv("M+23", "EIT\u83b7\u6279 \u2192 \u5168\u9762\u5546\u4e1a\u53d1\u5e03/ROI\u5b9e\u73b0\uff08\u5173\u952e\uff09")

    # 9
    pdf.add_page()
    pdf.sec(9, "\u9009\u9879\u53615\uff1a\u6cd5\u89c4\u6807\u51c6\u8ffd\u8e2a\u5668")
    pdf.txt(
        "510(k)\u63d0\u4ea4\u6240\u6709\u9002\u7528\u6cd5\u89c4\u6807\u51c6\u7684\u5408\u89c4\u77e9\u9635\u8868\u3002\u6bcf\u4e00\u884c\u4ee3\u8868\u4e00\u4e2a\u6807\u51c6\uff1a")
    pdf.ln(2)
    pdf.kv("\u6807\u51c6", "\u6807\u51c6\u4ee3\u7801\uff08\u5982IEC 60601-1:2005+AMD1\uff09")
    pdf.kv("\u63cf\u8ff0", "\u6807\u51c6\u6db5\u76d6\u5185\u5bb9")
    pdf.kv("\u9002\u7528\u4e8e", "\u54ea\u4e2a\u7ec4\u4ef6\uff1aBoth\u3001sEMG\u7535\u6781\u3001EIT\u5e26\u3001\u8f6f\u4ef6\u6216\u601d\u5c9a\u5236\u9020")
    pdf.kv("\u72b6\u6001", "\u5fbd\u7ae0\u663e\u793a\u5df2\u5b8c\u6210/\u8fdb\u884c\u4e2d/\u672a\u5f00\u59cb")
    pdf.kv("\u8fdb\u5ea6", "\u767e\u5206\u6bd4\u6761\uff080-100%\uff09")
    pdf.ln(2)
    pdf.txt(
        "\u8ffd\u8e2a\u768412\u9879\u6807\u51c6\u5305\u62ec\uff1a\n\n"
        "  IEC 60601-1 " + EM + " \u901a\u7528\u7535\u6c14\u5b89\u5168\n"
        "  IEC 60601-1-2 " + EM + " EMC\u7535\u78c1\u517c\u5bb9\n"
        "  IEC 60601-1-6 " + EM + " \u53ef\u7528\u6027\n"
        "  ISO 14971 " + EM + " \u98ce\u9669\u7ba1\u7406\n"
        "  ISO 10993-1/5/10 " + EM + " \u751f\u7269\u76f8\u5bb9\u6027\n"
        "  FDA\u7f51\u7edc\u5b89\u51682023 " + EM + " \u8bbe\u5907\u7f51\u7edc\u5b89\u5168\n"
        "  21 CFR 820 " + EM + " QSR\u8d28\u91cf\u4f53\u7cfb\u6cd5\u89c4\n"
        "  21 CFR Part 11 " + EM + " \u7535\u5b50\u8bb0\u5f55\n"
        "  IEC 62304 " + EM + " \u8f6f\u4ef6\u751f\u547d\u5468\u671f\n"
        "  ISO 13485 " + EM + " QMS\u8d28\u91cf\u7ba1\u7406\u4f53\u7cfb")

    # 10
    pdf.add_page()
    pdf.sec(10, "\u5229\u76ca\u76f8\u5173\u65b9\u8f93\u5165\u7cfb\u7edf")
    pdf.txt(
        "\u4eea\u8868\u76d8\u5b9e\u65bd\u4e86\u7ed3\u6784\u5316\u7684\u8f93\u5165\u673a\u5236\uff0c"
        "\u5546\u4e1a\u548c\u6280\u672f\u56e2\u961f\u53ef\u4ee5\u5411PMP\u63d0\u4ea4\u8f93\u5165\u4f9b\u5ba1\u67e5\u3002")

    pdf.sub("10.1 \u6d6e\u52a8\u64cd\u4f5c\u6309\u94ae(FAB)")
    pdf.txt(
        "\u53f3\u4e0b\u89d2\u7684\u84dd\u8272\u5706\u5f62\u6309\u94ae\u6253\u5f00\u5229\u76ca\u76f8\u5173\u65b9\u8f93\u5165\u4fa7\u6ed1\u9762\u677f\u3002"
        "FAB\u4e0a\u7684\u7ea2\u8272\u5fbd\u7ae0\u663e\u793a\u5f85\u5904\u7406\u8f93\u5165\u7684\u6570\u91cf\u3002"
        "\u5982\u679c\u6ca1\u6709\u5f85\u5904\u7406\u8f93\u5165\uff0c\u5fbd\u7ae0\u4f1a\u9690\u85cf\u3002")

    pdf.sub("10.2 \u8f93\u5165\u9762\u677f")
    pdf.txt(
        "\u4ece\u53f3\u4fa7\u8fb9\u7f18\u6ed1\u5165\u7684\u9762\u677f\u663e\u793a\u6240\u6709\u5229\u76ca\u76f8\u5173\u65b9\u8f93\u5165\uff1a\n\n"
        "  \u6765\u6e90\uff1a\u6280\u672f\u56e2\u961f\uff08\u84dd\u8272\u5de6\u8fb9\u6846\uff09\u6216\u5546\u4e1a/\u6295\u8d44\u65b9\uff08\u6a59\u8272\u5de6\u8fb9\u6846\uff09\n"
        "  \u65e5\u671f\uff1a\u8f93\u5165\u63d0\u4ea4\u65f6\u95f4\n"
        "  \u5173\u8054\u95e8\u63a7\uff1a\u6b64\u8f93\u5165\u6d89\u53ca\u54ea\u4e2a\u95e8\u63a7\n"
        "  \u72b6\u6001\u5fbd\u7ae0\uff1a\u5f85\u5ba1\u6838\uff08\u9ec4\u8272\uff09\u6216\u5df2\u63a5\u53d7\uff08\u7eff\u8272\uff09\n"
        "  \u5185\u5bb9\uff1a\u5b9e\u9645\u7684\u53cd\u9988\u6216\u8bf7\u6c42\n"
        "  PMP\u56de\u590d\uff1a\u5982\u679cPMP\u5df2\u56de\u590d\uff0c\u4ee5PMP:\u524d\u7f00\u7ea2\u8272\u663e\u793a")

    pdf.sub("10.3 \u8f93\u5165\u72b6\u6001")
    pdf.txt(
        "  \u5f85\u5ba1\u6838 " + EM + " PMP\u5c1a\u672a\u56de\u590d\u3002\u8ba1\u5165\u5fbd\u7ae0\u6570\u3002\n"
        "  \u5df2\u63a5\u53d7 " + EM + " PMP\u5df2\u5ba1\u67e5\u5e76\u63a5\u53d7\u3002\n"
        "  \u5df2\u62d2\u7edd " + EM + " PMP\u5df2\u62d2\u7edd\u3002\n"
        "  \u5df2\u8bb0\u5f55 " + EM + " PMP\u5df2\u786e\u8ba4\u4f46\u672a\u91c7\u53d6\u884c\u52a8\u3002")

    # 11
    pdf.sec(11, "\u53cc\u8bed\u7cfb\u7edf\uff08\u4e2d/\u82f1\uff09")
    pdf.txt(
        "\u4eea\u8868\u76d8\u652f\u6301\u5b8c\u6574\u7684\u4e2d\u82f1\u6587\u5207\u6362\u3002\u70b9\u51fb\u8bed\u8a00\u5207\u6362\u6309\u94ae\uff08EN/\u4e2d\uff09\u65f6\uff1a\n\n"
        "  1. \u6240\u6709\u9759\u6001\u6807\u7b7e\u66f4\u65b0\n"
        "  2. \u6240\u6709\u6570\u636e\u9a71\u52a8\u5185\u5bb9\u66f4\u65b0\n"
        "  3. HTML\u7684lang\u5c5e\u6027\u5728'en'\u548c'zh-CN'\u4e4b\u95f4\u5207\u6362\n\n"
        "\u4e3a\u53cc\u8bed\u56e2\u961f\u8bbe\u8ba1" + EM + EM + "\u5de5\u7a0b\u56e2\u961f\u53ef\u80fd\u4f7f\u7528\u4e2d\u6587\uff0c"
        "\u6295\u8d44\u8005/\u6cd5\u89c4\u987e\u95ee\u4f7f\u7528\u82f1\u6587\u3002")

    # 12 \u8d44\u91d1/\u8dd1\u9053\u9009\u9879\u5361
    pdf.add_page()
    pdf.sec(12, "\u9009\u9879\u53616\uff1a\u8d44\u91d1/\u8dd1\u9053")
    pdf.txt(
        "\u8d44\u91d1/\u8dd1\u9053\u9009\u9879\u5361\u663e\u793a\u9879\u76ee\u7684\u5b9e\u65f6\u8d22\u52a1\u72b6\u51b5\u3002"
        "\u8fd9\u662f\u5546\u4e1a\u5229\u76ca\u76f8\u5173\u65b9\u548c\u8d22\u52a1\u7528\u6237\u7684\u4e3b\u8981\u9009\u9879\u5361\u3002")

    pdf.sub("12.1 \u8d22\u52a1\u6458\u8981\u5361\u7247")
    pdf.txt(
        "\u9876\u90e8\u4e09\u5f20\u5361\u7247\u663e\u793a\uff1a\n\n"
        "  \u73b0\u6709\u8d44\u91d1 " + EM + " \u5f53\u524d\u53ef\u7528\u8d44\u91d1\uff08\u7f8e\u5143\uff09\n"
        "  \u6708\u5ea6\u71c3\u70e7 " + EM + " \u5e73\u5747\u6708\u5ea6\u652f\u51fa\n"
        "  \u8dd1\u9053 " + EM + " \u6309\u5f53\u524d\u71c3\u70e7\u7387\u8fd8\u53ef\u7ef4\u6301\u8fd0\u884c\u7684\u6708\u6570")

    pdf.sub("12.2 \u878d\u8d44\u8f6e\u6b21")
    pdf.txt(
        "\u6bcf\u4e2a\u878d\u8d44\u8f6e\u6b21\u5361\u7247\u663e\u793a\uff1a\n\n"
        "  \u6807\u7b7e\uff1a\u8f6e\u6b21\u540d\u79f0\uff08\u5982\u5929\u4f7f\u8f6e\u3001Pre-Seed\u3001A\u8f6e\uff09\n"
        "  \u91d1\u989d\uff1a\u7f8e\u5143\u91d1\u989d\n"
        "  \u65e5\u671f\uff1a\u9884\u8ba1\u6216\u5b9e\u9645\u5230\u8d26\u65e5\u671f\n"
        "  \u72b6\u6001\u5fbd\u7ae0\uff08PMP\u53ef\u70b9\u51fb\uff09\uff1a\u6d3d\u8c08\u4e2d / \u5df2\u627f\u8bfa / \u5df2\u5230\u8d26\n\n"
        "\u5f53\u8f6e\u6b21\u72b6\u6001\u53d8\u4e3a" + LQ + "\u5df2\u5230\u8d26" + RQ + "\u65f6\uff0c"
        "\u4eea\u8868\u76d8\u81ea\u52a8\u5c06\u91d1\u989d\u52a0\u5165\u73b0\u6709\u8d44\u91d1\u5e76\u91cd\u65b0\u8ba1\u7b97\u8dd1\u9053\u6708\u6570\u3002\n\n"
        "\u975ePMP\u7528\u6237\u53ef\u901a\u8fc7\u53d8\u66f4\u8bf7\u6c42\u5de5\u4f5c\u6d41\u7533\u8bf7\u72b6\u6001\u53d8\u66f4\u3002")

    pdf.sub("12.3 \u6dfb\u52a0\u65b0\u878d\u8d44\u8f6e\u6b21")
    pdf.txt(
        "\u878d\u8d44\u8f6e\u6b21\u5361\u7247\u4e0b\u65b9\uff0cPMP\u53ef\u4ee5\u8f93\u5165\u4ee5\u4e0b\u4fe1\u606f\u6765\u8bb0\u5f55\u65b0\u8f6e\u6b21\uff1a\n\n"
        "  \u6807\u7b7e\uff08\u5982A\u8f6e\uff09\n"
        "  \u91d1\u989d\uff08\u7f8e\u5143\uff09\n"
        "  \u9884\u8ba1\u65e5\u671f\uff08YYYY-MM\uff09\n\n"
        "\u65b0\u8f6e\u6b21\u59cb\u7ec8\u4ee5" + LQ + "\u6d3d\u8c08\u4e2d" + RQ + "\u72b6\u6001\u5f00\u59cb\u3002")

    pdf.sub("12.4 \u71c3\u70e7\u5386\u53f2")
    pdf.txt(
        "\u663e\u793a\u6bcf\u6708\u71c3\u70e7\u91d1\u989d\u53ca\u5907\u6ce8\u7684\u8868\u683c\uff08\u5982" + LQ + "\u9884\u63d0\u4ea4\u7533\u8bf7\u8d39\u7528" + RQ +
        "\u3001" + LQ + "\u53f0\u67b6\u6d4b\u8bd5\u5f00\u59cb" + RQ + "\uff09\u3002\u5e2e\u52a9\u6295\u8d44\u8005\u548c\u8d22\u52a1\u4eba\u5458\u4e86\u89e3\u652f\u51fa\u6a21\u5f0f\u3002")

    # 13 \u89d2\u8272\u8bbf\u95ee\u63a7\u5236
    pdf.add_page()
    pdf.sec(13, "\u89d2\u8272\u8bbf\u95ee\u63a7\u5236")
    pdf.txt(
        "\u4eea\u8868\u76d8\u5b9e\u65bd\u56db\u79cd\u7528\u6237\u89d2\u8272\uff0c\u53ef\u4ece\u9876\u90e8\u680f\u53f3\u4fa7\u7684\u89d2\u8272\u5207\u6362\u5668\u4e0b\u62c9\u83dc\u5355\u4e2d\u9009\u62e9\u3002")

    pdf.sub("13.1 \u89d2\u8272\u5207\u6362\u5668")
    pdf.txt(
        "\u9876\u90e8\u680f\u4e2d\u7684\u4e0b\u62c9\u83dc\u5355\u5141\u8bb8\u60a8\u5207\u6362\u89d2\u8272\uff1a\n\n"
        "  PMP\uff08\u5b8c\u5168\u6743\u9650\uff09" + EM + " \u53ef\u76f4\u63a5\u4fee\u6539\u4efb\u4f55\u72b6\u6001\uff0c\u5ba1\u6279/\u62d2\u7edd\u53d8\u66f4\u8bf7\u6c42\uff0c"
        "\u505a\u51fa\u95e8\u63a7\u51b3\u7b56\uff0c\u8bbf\u95ee\u6240\u6709\u9009\u9879\u5361\u3002\n"
        "  \u6280\u672f\u56e2\u961f " + EM + " \u53ef\u67e5\u770b\u6240\u6709\u9009\u9879\u5361\uff0c\u4f46\u4e0d\u80fd\u76f4\u63a5\u4fee\u6539\u3002\u4efb\u4f55\u72b6\u6001\u53d8\u66f4\u5fc5\u987b\u63d0\u4ea4\u53d8\u66f4\u8bf7\u6c42\u3002\n"
        "  \u5546\u4e1a/\u6295\u8d44\u65b9 " + EM + " \u4e0e\u6280\u672f\u56e2\u961f\u76f8\u540c\uff1a\u53ef\u67e5\u770b\u5168\u90e8\uff0c\u4f46\u4fee\u6539\u9700\u8981\u63d0\u4ea4CR\u3002\n"
        "  \u8d22\u52a1\u4f1a\u8ba1 " + EM + " \u53ea\u8bfb\u8bbf\u95ee\uff0c\u4ec5\u9650\u4e09\u4e2a\u9009\u9879\u5361\u3002")

    pdf.sub("13.2 PMP\u89d2\u8272")
    pdf.txt(
        "PMP\u62e5\u6709\u5b8c\u5168\u6743\u9650\uff1a\n"
        "  - \u70b9\u51fb\u91cc\u7a0b\u7891\u5fbd\u7ae0\u5faa\u73af\u5207\u6362\u72b6\u6001\n"
        "  - \u70b9\u51fb\u98ce\u9669\u5361\u7247\u7f16\u8f91\u4e25\u91cd\u6027\u3001\u6982\u7387\u3001\u7b49\u7ea7\u548c\u7f13\u89e3\u72b6\u6001\n"
        "  - \u70b9\u51fb\u6807\u51c6\u72b6\u6001\u5fbd\u7ae0\u5207\u6362\u72b6\u6001\n"
        "  - \u70b9\u51fb\u878d\u8d44\u72b6\u6001\u5fbd\u7ae0\u5207\u6362\u72b6\u6001\n"
        "  - \u505a\u51fa\u95e8\u63a7\u51b3\u7b56\uff08\u901a\u8fc7/\u9700\u66f4\u591a\u6570\u636e/\u505c\u6b62\uff09\n"
        "  - \u5ba1\u6279\u6216\u62d2\u7edd\u6765\u81ea\u6280\u672f/\u5546\u4e1a\u56e2\u961f\u7684\u53d8\u66f4\u8bf7\u6c42\n"
        "  - \u6dfb\u52a0\u95e8\u63a7\u5907\u6ce8\u548c\u7ba1\u7406\u6240\u6709\u9762\u677f")

    pdf.sub("13.3 \u6280\u672f\u548c\u5546\u4e1a\u89d2\u8272")
    pdf.txt(
        "\u5f53\u6280\u672f\u6216\u5546\u4e1a\u56e2\u961f\u6210\u5458\u70b9\u51fb\u72b6\u6001\u8fdb\u884c\u4fee\u6539\u65f6\uff0c"
        "\u4e0d\u4f1a\u76f4\u63a5\u4fee\u6539\u6570\u636e\uff0c\u800c\u662f\u6253\u5f00\u53d8\u66f4\u8bf7\u6c42\u8868\u5355\u3002\n\n"
        "\u5fc5\u987b\u63d0\u4f9b\uff1a\n"
        "  - \u5efa\u8bae\u7684\u65b0\u503c\n"
        "  - \u7406\u7531\uff08\u5fc5\u586b\uff09" + EM + " \u4e3a\u4ec0\u4e48\u9700\u8981\u8fd9\u4e2a\u53d8\u66f4\n"
        "  - \u8bc1\u636e/\u53c2\u8003\uff08\u53ef\u9009\uff09" + EM + " \u94fe\u63a5\u6216\u6587\u6863\u53c2\u8003\n"
        "  - \u9644\u4ef6\u6587\u6863\uff08\u53ef\u9009\uff09" + EM + " \u672c\u5730\u5b58\u50a8\u7684\u6587\u4ef6\u4e0a\u4f20\n\n"
        "\u8bf7\u6c42\u5c06\u6392\u961f\u7b49\u5f85PMP\u5ba1\u6838\u3002PMP\u53ef\u4ee5\u6279\u51c6\uff08\u5e94\u7528\u53d8\u66f4\uff09\u6216\u62d2\u7edd\uff08\u9644\u5e26\u8bf4\u660e\uff09\u3002\n\n"
        "\u76f4\u63a5\u7f16\u8f91\u6743\u9650\uff1a\n"
        "\u5546\u4e1a\u548c\u6280\u672f\u89d2\u8272\u8fd8\u53ef\u4ee5\u76f4\u63a5\u7f16\u8f91\uff08\u65e0\u9700CR\uff09\uff1a\n"
        "  - \u8d44\u91d1/\u8dd1\u9053\u4e2d\u7684\u73b0\u91d1\u4f59\u989d\u548c\u6708\u5ea6\u71c3\u70e7\u7387\n"
        "  - \u878d\u8d44\u8f6e\u72b6\u6001\u5207\u6362\uff08\u7ba1\u9053/\u5df2\u627f\u8bfa/\u5df2\u6536\u5230\uff09\n"
        "  - \u79fb\u9664\u4e0d\u4f7f\u7528\u7684\u652f\u4ed8\u4e0e\u94f6\u884cAPI\u96c6\u6210\uff08\u53ef\u6062\u590d\uff09")

    pdf.sub("13.4 \u8d22\u52a1\u4f1a\u8ba1\u89d2\u8272")
    pdf.txt(
        "\u8d22\u52a1\u4f1a\u8ba1\u7684\u8bbf\u95ee\u6700\u53d7\u9650\u5236\uff1a\n\n"
        "  \u5141\u8bb8\uff08\u53ea\u8bfb\uff09\uff1a\n"
        "    - \u8d44\u91d1/\u8dd1\u9053 " + EM + " \u67e5\u770b\u4f59\u989d\u3001\u878d\u8d44\u8f6e\u6b21\u3001\u71c3\u70e7\u5386\u53f2\n"
        "    - \u65f6\u95f4\u7ebf " + EM + " \u67e5\u770b\u5546\u4e1a\u8bed\u8a00\u7684\u91cc\u7a0b\u7891\u4e8b\u4ef6\n"
        "    - \u95e8\u63a7\u7cfb\u7edf " + EM + " \u67e5\u770b\u95e8\u63a7\u72b6\u6001\u548c\u6807\u51c6\n\n"
        "  \u53d7\u9650\uff08\u9009\u9879\u5361\u7981\u7528\uff09\uff1a\n"
        "    - \u53cc\u8f68\u89c6\u56fe\uff08\u5305\u542b\u4e13\u6709\u6280\u672f\u7ec6\u8282\uff09\n"
        "    - \u98ce\u9669\u4eea\u8868\u76d8\uff08\u5305\u542b\u654f\u611f\u98ce\u9669\u8bc4\u4f30\uff09\n"
        "    - \u6cd5\u89c4\u8ffd\u8e2a\u5668\uff08\u5408\u89c4\u5b9e\u65bd\u7ec6\u8282\uff09\n\n"
        "\u8d22\u52a1\u89d2\u8272\u6fc0\u6d3b\u65f6\u4f1a\u663e\u793a\u9ec4\u8272\u63d0\u793a\u6846\uff0c\u8bf4\u660e\u8bbf\u95ee\u9650\u5236\u3002"
        "\u53d7\u9650\u9009\u9879\u5361\u4f1a\u53d8\u7070\u4e14\u65e0\u6cd5\u70b9\u51fb\u3002")

    # 14 \u53d8\u66f4\u8bf7\u6c42\u5de5\u4f5c\u6d41\u4e0e\u6587\u6863\u5b58\u50a8
    pdf.add_page()
    pdf.sec(14, "\u53d8\u66f4\u8bf7\u6c42\u5de5\u4f5c\u6d41\u4e0e\u6587\u6863\u5b58\u50a8")
    pdf.txt(
        "\u53d8\u66f4\u8bf7\u6c42(CR)\u7cfb\u7edf\u786e\u4fdd\u6240\u6709\u72b6\u6001\u53d8\u66f4\u5728\u5e94\u7528\u524d\u7ecf\u8fc7\u9a8c\u8bc1\u3002"
        "\u53ea\u6709PMP\u53ef\u4ee5\u76f4\u63a5\u4fee\u6539\uff1b\u6280\u672f\u548c\u5546\u4e1a\u56e2\u961f\u5fc5\u987b\u63d0\u4ea4CR\u7531PMP\u5ba1\u6838\u3002\n\n"
        "\u6240\u6709CR\u6570\u636e\u81ea\u52a8\u540c\u6b65\u5230\u670d\u52a1\u5668\uff08Supabase\uff09\uff0c\u5e76\u4ee5localStorage\u4f5c\u4e3a\u5907\u4efd\u3002"
        "\u9644\u4ef6\u6587\u6863\u5b58\u50a8\u5728\u670d\u52a1\u5668\u4e0a\u3002")

    pdf.sub("14.1 \u63d0\u4ea4\u53d8\u66f4\u8bf7\u6c42")
    pdf.txt(
        "\u5f53\u975ePMP\u7528\u6237\u5c1d\u8bd5\u4fee\u6539\u72b6\u6001\u65f6\uff0c\u9f20\u6807\u60ac\u505c\u4f1a\u663e\u793a\u201c\u70b9\u51fb\u63d0\u4ea4\u53d8\u66f4\u8bf7\u6c42\u201d\u7684\u63d0\u793a\u3002"
        "\u70b9\u51fb\u540e\u4f1a\u6253\u5f00\u4e00\u4e2a\u5f39\u7a97\u8868\u5355\uff0c\u5305\u542b\u4ee5\u4e0b\u5b57\u6bb5\uff1a\n\n"
        "  \u8bf7\u6c42\u65b9\uff1a\u6839\u636e\u5f53\u524d\u89d2\u8272\u81ea\u52a8\u8bbe\u7f6e\n"
        "  \u5b57\u6bb5\uff1a\u663e\u793a\u6b63\u5728\u4fee\u6539\u7684\u5185\u5bb9\n"
        "  \u5f53\u524d\u503c\uff1a\u73b0\u6709\u7684\u503c\n"
        "  \u5efa\u8bae\u503c\uff1a\u5e0c\u671b\u6539\u4e3a\u4ec0\u4e48\uff08\u5fc5\u586b\uff09\u3002\u5360\u4f4d\u7b26\u663e\u793a\u201c\u8f93\u5165\u4e0a\u65b9\u5b57\u6bb5\u7684\u65b0\u503c\u201d\u3002\n"
        "  \u7406\u7531\uff1a\u4e3a\u4ec0\u4e48\u9700\u8981\u8fd9\u4e2a\u53d8\u66f4\uff08\u5fc5\u586b\uff09\n"
        "  \u8bc1\u636e/\u53c2\u8003\uff1a\u94fe\u63a5\u6216\u6587\u6863\u53c2\u8003\uff08\u53ef\u9009\uff09\n"
        "  \u9644\u4ef6\u6587\u6863\uff1a\u6587\u4ef6\u4e0a\u4f20\uff08\u53ef\u9009\uff09\n\n"
        "\u63d0\u4ea4\u540e\uff0c\u4f1a\u51fa\u73b0\u4e00\u6761\u786e\u8ba4\u901a\u77e5\uff0c\u663e\u793aCR\u7f16\u53f7\u5e76\u8bf4\u660e\u6b63\u5728\u7b49\u5f85PMP\u5ba1\u6279\u3002")

    pdf.sub("14.2 \u6587\u6863\u5b58\u50a8")
    pdf.txt(
        "\u9644\u52a0\u5230\u53d8\u66f4\u8bf7\u6c42\u7684\u6587\u6863\u4f7f\u7528IndexedDB\u5b58\u50a8\u5728\u6d4f\u89c8\u5668\u672c\u5730\u3002\u8fd9\u610f\u5473\u7740\uff1a\n\n"
        "  - \u6587\u4ef6\u5b58\u50a8\u5728\u7528\u6237\u673a\u5668\u4e0a\uff0c\u4e0d\u4f1a\u4e0a\u4f20\u5230\u670d\u52a1\u5668\n"
        "  - \u6587\u6863\u5728\u540c\u4e00\u6d4f\u89c8\u5668\u4e2d\u7684\u9875\u9762\u5237\u65b0\u540e\u4ecd\u7136\u4fdd\u7559\n"
        "  - \u53ef\u4ee5\u5411\u5355\u4e2aCR\u9644\u52a0\u591a\u4e2a\u6587\u4ef6\n"
        "  - \u63d0\u4ea4\u524d\u53ef\u4ee5\u5220\u9664\u5df2\u6dfb\u52a0\u7684\u6587\u4ef6\n"
        "  - \u63d0\u4ea4\u540e\u53ef\u4ece CR\u5361\u7247\u4e0b\u8f7d\u6587\u4ef6\n\n"
        "\u652f\u6301\u7684\u6587\u4ef6\u7c7b\u578b\uff1aPDF\u3001\u56fe\u7247(PNG\u3001JPG)\u3001Word\u6587\u6863\u3001Excel\u7b49\u3002"
        "\u6587\u4ef6\u5927\u5c0f\u4ee5\u53ef\u8bfb\u683c\u5f0f\u663e\u793a(KB\u3001MB)\u3002")

    pdf.sub("14.3 \u53d8\u66f4\u8bf7\u6c42\u8ffd\u8e2a")
    pdf.txt(
        "\u5f85\u5904\u7406\u7684\u53d8\u66f4\u8bf7\u6c42\u901a\u8fc7\u5ba1\u8ba1\u8ffd\u8e2a\u548c\u901a\u77e5\u7cfb\u7edf\u8fdb\u884c\u8ddf\u8e2a\uff0c"
        "\u800c\u975e\u4e13\u7528\u7684\u961f\u5217\u9009\u9879\u5361\u3002\u5f53\u975ePMP\u7528\u6237\u63d0\u4ea4CR\u65f6\uff1a\n\n"
        "  - CR\u8bb0\u5f55\u5728\u5ba1\u8ba1\u8ffd\u8e2a\u4e2d\uff0c\u72b6\u6001\u4e3a\u5f85\u5904\u7406\n"
        "  - PMP\u4f1a\u6536\u5230\u65b0CR\u7684\u901a\u77e5\u63d0\u9192\n"
        "  - CR\u5361\u7247\u6309\u989c\u8272\u533a\u5206\uff1a\u5f85\u5ba1\u6279\uff08\u9ec4\u8272\uff09\u3001\u5df2\u6279\u51c6\uff08\u7eff\u8272\uff09\u3001\u5df2\u62d2\u7edd\uff08\u7ea2\u8272\uff09\n\n"
        "\u6bcf\u6761CR\u8bb0\u5f55\u663e\u793a\uff1aCR\u7f16\u53f7\u3001\u8bf7\u6c42\u65b9\u3001\u65e5\u671f\u3001\u4fee\u6539\u5b57\u6bb5\u3001\u65e7\u503c\u3001\u65b0\u503c\u3001"
        "\u7406\u7531\u3001\u8bc1\u636e\u3001\u9644\u4ef6\u6587\u6863\uff08\u5e26\u4e0b\u8f7d\u94fe\u63a5\uff09\u548cPMP\u56de\u590d\u3002")

    pdf.sub("14.4 PMP\u5ba1\u6838\u6d41\u7a0b")
    pdf.txt(
        "PMP\u901a\u8fc7\u901a\u77e5\u7cfb\u7edf\u5ba1\u6838\u548c\u5904\u7406\u5f85\u5904\u7406\u7684CR\uff1a\n\n"
        "  \u6279\u51c6\uff1a\u5efa\u8bae\u7684\u53d8\u66f4\u76f4\u63a5\u5e94\u7528\u5230\u4eea\u8868\u76d8\u6570\u636e\u3002"
        "CR\u6807\u8bb0\u4e3a" + LQ + "\u5df2\u6279\u51c6" + RQ + "\uff0c\u9644\u5e26PMP\u5907\u6ce8\u548c\u65f6\u95f4\u6233\u3002\n\n"
        "  \u62d2\u7edd\uff1a\u53d8\u66f4\u4e0d\u4f1a\u5e94\u7528\u3002"
        "CR\u6807\u8bb0\u4e3a" + LQ + "\u5df2\u62d2\u7edd" + RQ + "\uff0c\u9644\u5e26\u89e3\u91ca\u539f\u56e0\u7684PMP\u5907\u6ce8\u3002"
        "\u8bf7\u6c42\u65b9\u53ef\u4ee5\u67e5\u770b\u62d2\u7edd\u539f\u56e0\u5e76\u63d0\u4ea4\u65b0\u7684CR\u3002")

    # 15 \u4e2d\u56fd\u6295\u8d44\u8005API\u96c6\u6210
    pdf.add_page()
    pdf.sec(15, "\u4e2d\u56fd\u6295\u8d44\u8005API\u96c6\u6210")
    pdf.txt(
        "\u4f4d\u4e8e\u8d44\u91d1/\u8dd1\u9053\u9009\u9879\u5361\u4e2d\uff0c\u6b64\u9762\u677f\u63d0\u4f9b\u9488\u5bf9\u4e2d\u56fd\u6295\u8d44\u8005\u548c\u8de8\u5883\u4ea4\u6613\u7684"
        "\u652f\u4ed8\u3001\u94f6\u884c\u548c\u8d27\u5e01API\u53c2\u8003\u6307\u5357\u3002")

    pdf.sub("15.1 API\u72b6\u6001\u5fbd\u7ae0")
    pdf.txt(
        "\u6bcf\u5f20API\u5361\u7247\u663e\u793a\u4e09\u79cd\u72b6\u6001\u4e4b\u4e00\uff1a\n\n"
        "  \u5df2\u6fc0\u6d3b\uff08\u7eff\u8272\uff09" + EM + " API\u5df2\u96c6\u6210\u5e76\u4e0a\u7ebf\n"
        "  \u53ef\u7528\uff08\u84dd\u8272\uff09" + EM + " API\u53ef\u4ee5\u96c6\u6210\uff0c\u5c1a\u672a\u8fde\u63a5\n"
        "  \u8ba1\u5212\u4e2d\uff08\u7d2b\u8272\uff09" + EM + " API\u96c6\u6210\u8ba1\u5212\u5728\u672a\u6765\u9636\u6bb5")

    pdf.sub("15.2 \u5df2\u5217\u51faAPI")
    pdf.kv("\u652f\u4ed8\u5b9d\u5546\u6237", "\u8de8\u5883\u6536\u6b3e\u3001\u6295\u8d44\u8005\u6c47\u6b3e\u8ddf\u8e2a\u3001\u4eba\u6c11\u5e01/\u7f8e\u5143\u7ed3\u7b97")
    pdf.kv("\u5fae\u4fe1\u652f\u4ed8\u5546\u6237", "\u4f01\u4e1a\u652f\u4ed8\u3001\u6295\u8d44\u8005\u6c9f\u901a\u6e20\u9053\u3001\u5c0f\u7a0b\u5e8f\u96c6\u6210")
    pdf.kv("\u94f6\u8054\u56fd\u9645", "\u4f01\u4e1a\u5361\u652f\u4ed8\u3001\u8de8\u5883B2B\u8f6c\u8d26\u3001\u591a\u5e01\u79cd\u652f\u6301")
    pdf.kv("\u62db\u5546\u94f6\u884c", "\u4f01\u4e1a\u94f6\u884cAPI\u3001\u8d44\u91d1\u7ba1\u7406\u3001\u5b9e\u65f6\u4f59\u989d\u4e0e\u6c47\u7387")
    pdf.kv("PingPong\u5168\u7403", "\u521b\u4e1a\u516c\u53f8\u8de8\u5883\u652f\u4ed8\u5e73\u53f0\u3001\u81ea\u52a8\u5916\u6c47\u3001\u589e\u503c\u7a0e\u9000\u7a0e")
    pdf.kv("XE\u6c47\u7387\u6570\u636e", "\u5b9e\u65f6\u4eba\u6c11\u5e01/\u7f8e\u5143\u6c47\u7387\u3001\u5386\u53f2\u6c47\u7387\u3001\u8d27\u5e01\u8f6c\u6362")
    pdf.kv("SWIFT gpi", "\u8de8\u5883\u6c47\u6b3e\u8ddf\u8e2a\u3001\u652f\u4ed8\u72b6\u6001\u786e\u8ba4\u3001\u5408\u89c4\u5ba1\u67e5")

    pdf.ln(2)
    pdf.txt(
        "\u6bcf\u5f20\u5361\u7247\u8fd8\u663e\u793a\u5f00\u53d1\u8005\u53c2\u8003\u6587\u6863\u6765\u6e90\u3002"
        "\u8fd9\u4e9bAPI\u5bf9\u4e8e\u9700\u8981\u8de8\u5883\u8f6c\u8d26\u3001\u8ddf\u8e2a\u4ed8\u6b3e\u548c\u7ba1\u7406\u8d27\u5e01\u5151\u6362\u7684"
        "\u4e2d\u56fd\u5927\u9646\u6295\u8d44\u8005\u5c24\u5176\u91cd\u8981\u3002")

    pdf.sub("15.3 \u79fb\u9664\u548c\u6062\u590dAPI\u96c6\u6210")
    pdf.txt(
        "PMP\u3001\u5546\u4e1a\u548c\u6280\u672f\u89d2\u8272\u53ef\u4ee5\u79fb\u9664\u4e0d\u9700\u8981\u7684API\u96c6\u6210\u5361\u7247\u3002"
        "\u6bcf\u5f20\u5361\u7247\u53f3\u4e0a\u89d2\u663e\u793a\u5173\u95ed\u6309\u94ae(\u2715)\u3002\u70b9\u51fb\u540e\u663e\u793a\u786e\u8ba4\u63d0\u793a\uff0c"
        "\u786e\u8ba4\u540e\u5361\u7247\u88ab\u9690\u85cf\uff0c\u64cd\u4f5c\u8bb0\u5f55\u5728\u5ba1\u8ba1\u8ffd\u8e2a\u4e2d\u3002\n\n"
        "\u5982\u6709\u96c6\u6210\u88ab\u79fb\u9664\uff0c\u9762\u677f\u5e95\u90e8\u4f1a\u51fa\u73b0\u201c\u6062\u590d\u5df2\u79fb\u9664\u7684\u96c6\u6210\u201d\u6309\u94ae\uff0c"
        "\u70b9\u51fb\u53ef\u6062\u590d\u6240\u6709\u9690\u85cf\u7684\u5361\u7247\u3002\u79fb\u9664\u72b6\u6001\u901a\u8fc7\u670d\u52a1\u5668\u6570\u636e\u5e93\u8de8\u4f1a\u8bdd\u4fdd\u7559\u3002")


    # 16 行动项/任务看板
    pdf.add_page()
    pdf.sec(16, "选项卡7：行动项/任务看板")
    pdf.txt(
        "行动项选项卡提供看板式任务面板，用于跟踪所有项目行动项。"
        "项目按四列状态组织显示。")

    pdf.sub("16.1 看板列")
    pdf.txt(
        "四列按状态组织行动项：\n\n"
        "  待办     " + EM + " 尚未开始的项目（灰色标题）\n"
        "  进行中   " + EM + " 正在处理中（蓝色标题）\n"
        "  受阻     " + EM + " 等待外部依赖（红色标题）\n"
        "  已完成   " + EM + " 已完成的项目（绿色标题）\n\n"
        "点击任何行动卡片可循环切换状态：待办→进行中→已完成→待办。"
        "受阻项目点击后转为进行中。")

    pdf.sub("16.2 行动卡片")
    pdf.txt(
        "每张卡片显示：\n\n"
        "  行动ID：如ACT-001\n"
        "  优先级徽章：高（红）、中（黄）、低（绿）\n"
        "  标题：任务描述\n"
        "  负责人：负责的团队成员\n"
        "  归属：职能区域（技术、法规、商业）\n"
        "  截止日期：目标完成日期\n"
        "  关联门控：与哪个门控相关\n"
        "  备注：额外说明\n\n"
        "卡片有一条与其优先级匹配的彩色左边框。")

    # 17 DHF文档追踪器
    pdf.add_page()
    pdf.sec(17, "DHF文档追踪器")
    pdf.txt(
        "设计历史文件(DHF)文档追踪器位于行动项选项卡内。"
        "根据21 CFR 820要求，追踪510(k)提交所需的所有设计控制文档。")

    pdf.sub("17.1 文档表格")
    pdf.txt(
        "DHF表格每行显示：\n\n"
        "  代码：文档标识符（如DHF-001）\n"
        "  标题：文档名称（如设计计划）\n"
        "  类别：设计控制、验证、测试、风险、软件等\n"
        "  负责人：责任团队成员\n"
        "  状态：可点击徽章，循环切换：\n"
        "    未开始（灰色）→ 草稿（靛蓝色）→ 审核中（黄色）→ 已批准（绿色）\n"
        "  截止月份：目标完成月份（M+N格式）\n"
        "  备注：关于文档的额外说明")

    pdf.sub("17.2 文档类别")
    pdf.txt(
        "DHF文档涵盖以下类别：\n\n"
        "  设计控制     " + EM + " 设计计划、输入、输出\n"
        "  验证         " + EM + " 设计验证方案和报告\n"
        "  确认         " + EM + " 临床验证证据\n"
        "  风险管理     " + EM + " ISO 14971风险分析文件\n"
        "  软件         " + EM + " IEC 62304软件文档\n"
        "  生物相容性   " + EM + " ISO 10993测试报告\n"
        "  测试         " + EM + " EMC和电气安全测试结果\n"
        "  提交         " + EM + " FDA封面信和设备描述")

    # 18 CAPA日志
    pdf.add_page()
    pdf.sec(18, "CAPA日志")
    pdf.txt(
        "纠正和预防措施(CAPA)日志也位于行动项选项卡内。"
        "CAPA与ISO 14971风险登记表中的特定风险相关联，"
        "跟踪正式的纠正或预防措施。")

    pdf.sub("18.1 CAPA卡片")
    pdf.txt(
        "每张CAPA卡片显示：\n\n"
        "  CAPA ID：如CAPA-001\n"
        "  类型徽章：纠正（红色）或预防（蓝色）\n"
        "  状态徽章：可点击，循环切换：\n"
        "    开放（黄色）→ 进行中（蓝色）→ 已关闭（绿色）→ 已验证（紫色）\n"
        "  标题：措施简述\n"
        "  描述：详细说明\n"
        "  关联风险：触发此CAPA的风险登记条目\n"
        "  负责人：责任团队成员\n"
        "  开启日期 / 截止日期 / 关闭日期\n\n"
        "卡片有一条与其状态匹配的彩色左边框。"
        "当CAPA转为" + LQ + "已关闭" + RQ + "时，关闭日期自动设置。")

    pdf.sub("18.2 CAPA类型")
    pdf.txt(
        "  纠正：消除现有不合格原因的措施。"
        "例如：重新设计电极阵列以解决ECG伪影干扰。\n\n"
        "  预防：消除潜在不合格原因的措施。"
        "例如：在问题出现之前添加网络安全渗透测试。")

    # 19 预算vs实际
    pdf.add_page()
    pdf.sec(19, "选项卡8：预算vs实际")
    pdf.txt(
        "预算选项卡显示所有项目类别的计划支出与实际支出的详细对比。"
        "此选项卡对财务会计角色开放。")

    pdf.sub("19.1 预算表格")
    pdf.txt(
        "每行显示：\n\n"
        "  类别：预算项目（如原型开发、实验室测试）\n"
        "  计划($)：预算金额\n"
        "  实际($)：已支出金额\n"
        "  差额($)：差异（实际 - 计划）\n"
        "    绿色 = 低于预算（有利）\n"
        "    红色 = 超出预算（不利）\n"
        "  备注：支出说明")

    pdf.sub("19.2 预算类别")
    pdf.txt(
        "八个类别跟踪项目支出：\n\n"
        "  原型开发     " + EM + " 硬件和固件原型制作\n"
        "  实验室测试   " + EM + " V&V、EMC和台架测试\n"
        "  法规咨询     " + EM + " FDA顾问和申请费用\n"
        "  人员         " + EM + " 工程和法规人员\n"
        "  临床研究     " + EM + " 临床验证研究\n"
        "  设备和软件   " + EM + " 开发工具和许可证\n"
        "  制造设置     " + EM + " 合同制造NRE费用\n"
        "  差旅和会议   " + EM + " FDA会议、投资者差旅")

    pdf.sub("19.3 汇总行")
    pdf.txt(
        "底部行显示所有类别的计划总额、实际总额和差额总计。"
        "提供整体预算健康状况的快速检查。")

    # 20 资源配置
    pdf.add_page()
    pdf.sec(20, "选项卡9：资源配置")
    pdf.txt(
        "资源选项卡显示团队成员的分配和产能利用情况。"
        "每个团队成员的工作量通过分配条形图可视化。")

    pdf.sub("20.1 资源卡片")
    pdf.txt(
        "每张卡片显示：\n\n"
        "  姓名：团队成员姓名\n"
        "  角色：职位/职能\n"
        "  利用率徽章：总分配百分比，颜色编码：\n"
        "    绿色（<=80%）" + EM + " 正常，还有余力\n"
        "    黄色（81-99%）" + EM + " 高利用率，需密切关注\n"
        "    红色（>=100%）" + EM + " 超额分配，需采取行动\n"
        "  分配条形图：每个工作流分配的可视化条形图\n"
        "  产能：每周可用工时")

    pdf.sub("20.2 工作流分配")
    pdf.txt(
        "每个团队成员可能分配到多个工作流"
        "（如sEMG设计40%、EIT研究30%、文档20%）。"
        "百分比条形图一目了然地显示每个人的时间承诺。"
        "总利用率通过汇总所有分配百分比计算。")

    # 21 供应商追踪器
    pdf.add_page()
    pdf.sec(21, "选项卡10：供应商追踪器")
    pdf.txt(
        "供应商选项卡跟踪所有对设备制造至关重要的硬件组件供应商、"
        "合同制造商和材料供应商。")

    pdf.sub("21.1 供应商表格")
    pdf.txt(
        "每行显示：\n\n"
        "  供应商名称：公司名称\n"
        "  组件：提供的产品\n"
        "  状态：可点击徽章，循环切换：\n"
        "    审核中（黄色）→ 已认证（蓝色）→ 活跃（绿色）→ 风险（红色）\n"
        "  交货时间：以天为单位的交货时间\n"
        "  采购订单状态：当前采购订单状态\n"
        "  合同/制造里程碑：相关项目里程碑\n"
        "  备注：额外说明")

    pdf.sub("21.2 供应商状态")
    pdf.txt(
        "  审核中 " + EM + " 供应商正在评估/审计中\n"
        "  已认证 " + EM + " 供应商已通过认证但尚未启用\n"
        "  活跃   " + EM + " 供应商已批准并正在执行订单\n"
        "  风险   " + EM + " 供应商存在质量、交付或产能问题")

    # 22 审计追踪
    pdf.add_page()
    pdf.sec(22, "选项卡11：审计追踪")
    pdf.txt(
        "审计追踪选项卡提供仪表盘中每一次状态变更、决策和操作的完整日志。"
        "这支持21 CFR Part 11对医疗器械开发的可追溯性要求。")

    pdf.sub("22.1 审计表格")
    pdf.txt(
        "每条记录显示：\n\n"
        "  时间戳：操作的日期和时间\n"
        "  用户：谁执行了操作（PMP、技术、商业）\n"
        "  操作：操作类型（如里程碑状态、门控决策、CR批准）\n"
        "  目标：受影响的项目（如T1.1、G3、RISK-004）\n"
        "  旧值：之前的状态\n"
        "  新值：更新后的状态\n"
        "  详情：关于变更的额外说明\n\n"
        "审计追踪显示最近50条记录。所有修改数据的操作都会自动记录，"
        "包括里程碑状态变更、门控决策、标准切换、CR审批/拒绝、"
        "以及所有新功能的交互。")

    pdf.sub("22.2 追踪的操作类型")
    pdf.txt(
        "捕获以下操作类型：\n\n"
        "  milestone-status   " + EM + " 里程碑状态变更\n"
        "  gate-decision      " + EM + " PMP门控决策\n"
        "  gate-criteria      " + EM + " 门控标准复选框切换\n"
        "  gate-note          " + EM + " 门控备注添加\n"
        "  risk-field         " + EM + " 风险登记字段编辑\n"
        "  standard-status    " + EM + " 法规标准状态变更\n"
        "  standard-progress  " + EM + " 标准进度百分比更新\n"
        "  funding-status     " + EM + " 融资轮次状态变更\n"
        "  funding-added      " + EM + " 新增融资轮次\n"
        "  cr-submitted       " + EM + " 变更请求提交\n"
        "  cr-approved        " + EM + " 变更请求批准\n"
        "  cr-rejected        " + EM + " 变更请求拒绝\n"
        "  action-item        " + EM + " 行动项状态变更\n"
        "  dhf-status         " + EM + " DHF文档状态变更\n"
        "  capa-status        " + EM + " CAPA项目状态变更\n"
        "  supplier-status    " + EM + " 供应商状态变更")

    # 23 通知/警报
    pdf.add_page()
    pdf.sec(23, "通知与警报")
    pdf.txt(
        "通知栏显示在变更请求队列上方，提供需要关注事项的实时警报。")

    pdf.sub("23.1 警报类型")
    pdf.txt(
        "五种通知类型自动生成：\n\n"
        "  待处理CR（琥珀色）   " + EM + " 等待PMP审核的变更请求\n"
        "  逾期行动（红色）     " + EM + " 超过截止日期的行动项\n"
        "  逾期CAPA（红色）     " + EM + " 超过截止日期的CAPA\n"
        "  预算超支（粉色）     " + EM + " 实际支出超过计划的类别\n"
        "  跑道警告（橙色）     " + EM + " 现金跑道低于6个月")

    pdf.sub("23.2 关闭通知")
    pdf.txt(
        "每条通知右侧有一个关闭按钮（X）。"
        "关闭的通知在当前会话中隐藏，但如果条件持续存在，"
        "页面刷新后将重新出现。这确保重要警报不会被永久关闭。")

    # 24 导出/报告生成器
    pdf.sec(24, "导出/报告生成器")
    pdf.txt(
        "通知栏标题中的导出按钮生成一份全面的文本报告，"
        "总结整个项目状态。")

    pdf.sub("24.1 报告内容")
    pdf.txt(
        "生成的报告包括：\n\n"
        "  项目标题和生成时间戳\n"
        "  风险摘要 " + EM + " 所有风险及其ID、等级、严重性、概率和模块\n"
        "  里程碑摘要 " + EM + " 所有里程碑及其状态和目标月份\n"
        "  财务摘要 " + EM + " 现有资金、月度燃烧、跑道和融资轮次\n"
        "  DHF状态 " + EM + " 所有设计历史文件文档及状态\n"
        "  CAPA摘要 " + EM + " 所有纠正/预防措施及状态\n"
        "  行动项 " + EM + " 所有任务及状态和负责人\n\n"
        "报告以.txt文件下载，名为" + LQ + "Control_Tower_Report_YYYY-MM-DD.txt" + RQ + "。")

    # 25. 美国特定API集成
    pdf.add_page()
    pdf.sec(25, "\u7f8e\u56fd\u7279\u5b9aAPI\u96c6\u6210")
    pdf.txt(
        "\u4f4d\u4e8e\u8d44\u91d1/\u8dd1\u9053\u9009\u9879\u5361\u4e2d\uff0c\u4e0e\u4e2d\u56fd\u6295\u8d44\u8005API\u9762\u677f\u5e76\u5217\uff0c\u6b64\u90e8\u5206\u63d0\u4f9b\u4e0e\u7f8e\u56fd\u6295\u8d44\u8005\u548c\u5317\u7f8e\u8fd0\u8425\u76f8\u5173\u7684\u652f\u4ed8\u3001\u94f6\u884c\u548c\u5408\u89c4API\u53c2\u8003\u3002")

    pdf.sub("25.1 \u5217\u51fa\u7684\u7f8e\u56fdAPI")
    pdf.kv("Plaid", "\u94f6\u884c\u8d26\u6237\u5173\u8054\u3001\u4f59\u989d\u9a8c\u8bc1\u3001\u7f8e\u56fd\u6295\u8d44\u8005\u8d26\u6237\u4ea4\u6613\u76d1\u63a7")
    pdf.kv("Mercury\u94f6\u884c", "\u521b\u4e1a\u94f6\u884cAPI \u2014 \u5b9e\u65f6\u4f59\u989d\u3001\u7535\u6c47\u8f6c\u8d26\u3001\u8d44\u91d1\u7ba1\u7406")
    pdf.kv("Stripe", "\u7f8e\u56fd\u652f\u4ed8\u5904\u7406\u3001\u6295\u8d44\u8005\u8ba2\u9605\u8ba1\u8d39\u3001\u81ea\u52a8\u53d1\u7968")
    pdf.kv("\u7845\u8c37\u94f6\u884c (SVB)", "\u98ce\u6295\u94f6\u884c\u3001\u8d44\u672c\u53ec\u96c6\u5904\u7406\u3001\u57fa\u91d1\u7ba1\u7406API")
    pdf.kv("AngelList", "\u878d\u8d44\u5e73\u53f0\u96c6\u6210\u3001SPV\u7ba1\u7406\u3001\u80a1\u6743\u8868\u540c\u6b65")
    pdf.kv("Carta", "\u80a1\u6743\u8868\u7ba1\u7406\u3001409A\u4f30\u503c\u3001\u80a1\u6743\u8ba1\u5212\u7ba1\u7406")
    pdf.kv("SEC EDGAR", "\u76d1\u7ba1\u5907\u6848\u76d1\u63a7\u3001Form D\u8ffd\u8e2a\u3001\u6295\u8d44\u8005\u8d44\u8d28\u9a8c\u8bc1")

    pdf.sub("25.2 \u79fb\u9664\u548c\u6062\u590dAPI\u96c6\u6210")
    pdf.txt(
        "PMP\u3001\u5546\u4e1a\u548c\u6280\u672f\u89d2\u8272\u53ef\u4ee5\u70b9\u51fb\u5361\u7247\u4e0a\u7684\u5173\u95ed\u6309\u94ae(\u2715)\u79fb\u9664\u4e0d\u9700\u8981\u7684API\u3002"
        "\u5df2\u79fb\u9664\u7684\u5361\u7247\u53ef\u4ee5\u968f\u65f6\u901a\u8fc7\u201c\u6062\u590d\u5df2\u79fb\u9664\u7684\u96c6\u6210\u201d\u6309\u94ae\u6062\u590d\u3002\n\n"
        "\u79fb\u9664\u64cd\u4f5c\u901a\u8fc7\u670d\u52a1\u5668\u6570\u636e\u5e93\u8de8\u4f1a\u8bdd\u4fdd\u7559\uff0c\u5e76\u8bb0\u5f55\u5728\u5ba1\u8ba1\u8ffd\u8e2a\u4e2d\u3002")


    # 26. 美国投资与投资者关系选项卡
    pdf.add_page()
    pdf.sec(26, "\u9009\u9879\u530112\uff1a\u7f8e\u56fd\u6295\u8d44\u4e0e\u6295\u8d44\u8005\u5173\u7cfb")
    pdf.txt(
        "\u6b64\u9009\u9879\u5361\u662f\u4eea\u8868\u76d8\u4e2d\u6240\u6709\u6295\u8d44\u8005\u5173\u7cfb(IR)\u6d3b\u52a8\u7684\u6307\u5b9a\u4e3b\u9875\u3002"
        "\u5b83\u5c06\u5b8c\u6574\u7684\u5317\u7f8e\u878d\u8d44\u7ba1\u9053\u3001\u6295\u8d44\u8005\u8ffd\u8e2a\u548cIR\u6d3b\u52a8\u6574\u5408\u5230\u5355\u4e00\u89c6\u56fe\u4e2d\uff0c"
        "\u7531Lon Dailey\u4f5c\u4e3a\u5317\u7f8e IR\u8d1f\u8d23\u4eba\u7ba1\u7406\u3002\n\n"
        "\u7531\u4e8e\u6b64\u9009\u9879\u5361\u63d0\u4f9b\u4e13\u95e8\u7684\u6295\u8d44\u8005\u5185\u5bb9\u2014\u2014\u7ba1\u9053\u6307\u6807\u3001"
        "\u76ee\u6807\u6295\u8d44\u8005\u8be6\u7ec6\u4fe1\u606f\u548c\u6d3b\u52a8\u65e5\u5fd7\u2014\u2014\u72ec\u7acb\u7684\u6295\u8d44\u8005\u6f14\u793a\u6587\u7a3f"
        "\u5df2\u4ece\u6587\u6863\u63a7\u5236\u4e2d\u79fb\u9664\u4ee5\u907f\u514d\u91cd\u590d\u3002\u6240\u6709\u6295\u8d44\u8005\u6750\u6599\u548c\u4e92\u52a8\u5386\u53f2\u73b0\u5728\u90fd\u5728\u8fd9\u91cc\u3002")

    pdf.sub("26.1 IR\u6307\u6807\u5361\u7247")
    pdf.txt(
        "\u9876\u90e8\u56db\u5f20\u6458\u8981\u5361\u7247\u63d0\u4f9b\u878d\u8d44\u8fdb\u5ea6\u7684\u5feb\u901f\u6982\u89c8\uff1a\n\n"
        "  \u6295\u8d44\u8005\u4f1a\u8bae (Q1) -- \u672c\u5b63\u5ea6\u4e3e\u884c\u7684\u4f1a\u8bae\u6570\u91cf\n"
        "  \u7ba1\u9053\u4ef7\u503c         -- \u878d\u8d44\u7ba1\u9053\u603b\u7f8e\u5143\u4ef7\u503c\n"
        "  \u672c\u5b63\u5ea6\u8f6c\u5316       -- \u6210\u529f\u52df\u96c6\u7684\u91d1\u989d\n"
        "  IR\u8d1f\u8d23\u4eba (\u5317\u7f8e)   -- \u7f8e\u56fd\u6295\u8d44\u8005\u5173\u7cfb\u4e3b\u8981\u8054\u7cfb\u4eba\n\n"
        "\u8fd9\u4e9b\u6307\u6807\u662f\u6295\u8d44\u8005\u6216\u8463\u4e8b\u4f1a\u6210\u5458\u770b\u5230\u7684\u7b2c\u4e00\u5185\u5bb9\uff0c"
        "\u63d0\u4f9b\u878d\u8d44\u52bf\u5934\u7684\u5373\u65f6\u80cc\u666f\u3002")

    pdf.sub("26.2 \u76ee\u6807\u6295\u8d44\u8005\u8868\u683c")
    pdf.txt(
        "\u8ddf\u8e2a\u6240\u6709\u6f5c\u5728\u7f8e\u56fd\u6295\u8d44\u8005\u7684\u8868\u683c\uff0c\u5305\u542b\u5b8c\u6574\u7684\u5173\u7cfb\u80cc\u666f\uff1a\n\n"
        "  \u76ee\u6807        -- \u6295\u8d44\u516c\u53f8\u540d\u79f0\n"
        "  \u7c7b\u578b        -- \u98ce\u6295\u3001\u5929\u4f7f\u56e2\u4f53\u3001\u6218\u7565\u7b49\n"
        "  \u9636\u6bb5        -- \u79cd\u5b50\u3001A\u8f6e\u7b49\n"
        "  \u8054\u7cfb\u72b6\u6001    -- \u989c\u8272\u7f16\u7801\u7684\u7ba1\u9053\u9636\u6bb5\uff1a\n"
        "      \u6f5c\u5728(\u7070\u8272) / \u5df2\u8054\u7cfb(\u7eff\u8272) / \u5c3d\u8c03\u4e2d(\u84dd\u8272) / "
        "\u6761\u6b3e\u6e05\u5355(\u84dd\u8272) / \u5df2\u5173\u95ed(\u84dd\u8272)\n"
        "  \u76ee\u6807\u91d1\u989d    -- \u5bfb\u6c42\u7684\u7f8e\u5143\u91d1\u989d\n"
        "  \u5907\u6ce8        -- \u5173\u7cfb\u8be6\u60c5\u548c\u6295\u8d44\u8bba\u70b9\u5339\u914d\n\n"
        "\u6b64\u8868\u683c\u53d6\u4ee3\u4e86\u5355\u72ec\u7684\u6f14\u793a\u8ddf\u8e2a\u5668\u6216CRM\u5bfc\u51fa\uff1b"
        "\u4eea\u8868\u76d8\u672c\u8eab\u5373\u4e3a\u5b9e\u65f6\u6295\u8d44\u8005\u7ba1\u9053\u3002")

    pdf.sub("26.3 \u6295\u8d44\u8005\u5173\u7cfb\u6d3b\u52a8")
    pdf.txt(
        "\u6309\u65f6\u95f4\u987a\u5e8f\u8bb0\u5f55IR\u6d3b\u52a8\uff0c\u5e26\u72b6\u6001\u6807\u7b7e\uff1a\n\n"
        "  \u5df2\u5b8c\u6210    -- \u6d3b\u52a8\u5df2\u7ed3\u675f\n"
        "  \u8fdb\u884c\u4e2d    -- \u5f53\u524d\u6b63\u5728\u8fdb\u884c\n"
        "  \u672a\u5f00\u59cb    -- \u5df2\u5b89\u6392\u4f46\u5c1a\u672a\u5f00\u59cb\n\n"
        "\u6d3b\u52a8\u5305\u62ec\u62d3\u5c55\u7535\u8bdd\u3001\u6f14\u793a\u4f1a\u8bae\u3001\u6570\u636e\u5ba4\u8bbe\u7f6e\u548c"
        "\u878d\u8d44\u6f14\u793a\u51c6\u5907\u3002\u6b64\u65e5\u5fd7\u4e3a\u5185\u90e8\u5ba1\u67e5\u548c\u8463\u4e8b\u4f1a\u62a5\u544a"
        "\u63d0\u4f9b\u6240\u6709\u6295\u8d44\u8005\u4e92\u52a8\u7684\u53ef\u5ba1\u8ba1\u8bb0\u5f55\u3002")

    # 27. 文档控制
    pdf.add_page()
    pdf.sec(27, "\u9009\u9879\u530113\uff1a\u6587\u6863\u63a7\u5236")
    pdf.txt(
        "\u6587\u6863\u63a7\u5236\u63d0\u4f9bISO 13485\u5408\u89c4\u7684\u6587\u6863\u751f\u547d\u5468\u671f\u7ba1\u7406\u3002\u6bcf\u4e2a\u6587\u6863\u90fd\u5e26\u6709"
        "\u6587\u63a7\u7f16\u53f7(DCN)\u3001\u4e94\u9636\u6bb5\u72b6\u6001\u5de5\u4f5c\u6d41\u3001\u5b8c\u6574\u7684\u4fee\u8ba2\u5386\u53f2\u548c\u81ea\u52a8\u5ba1\u6838\u6392\u7a0b\u3002")

    pdf.sub("27.1 \u6458\u8981\u680f")
    pdf.txt(
        "\u9762\u677f\u9876\u90e8\u7684\u8ba1\u6570\u5361\u7247\u63d0\u4f9b\u5feb\u901f\u6982\u89c8\uff1a\n\n"
        "  \u603b\u8ba1      -- \u53d7\u63a7\u6587\u6863\u603b\u6570\n"
        "  \u5df2\u751f\u6548    -- \u5f53\u524d\u6709\u6548\u6587\u6863\n"
        "  \u5ba1\u6838\u4e2d    -- \u7b49\u5f85\u5ba1\u6279\u7684\u6587\u6863\n"
        "  \u8349\u7a3f      -- \u65b0\u5efa\u6216\u7f16\u5199\u4e2d\u7684\u6587\u6863\n"
        "  \u903e\u671f      -- \u8d85\u8fc7\u8ba1\u5212\u5ba1\u6838\u65e5\u671f\u7684\u6587\u6863\uff08\u7ea2\u8272\u6807\u8bb0\uff09")

    pdf.sub("27.2 \u7c7b\u522b\u7b5b\u9009")
    pdf.txt(
        "\u7b5b\u9009\u6309\u94ae\u5141\u8bb8\u6309\u7c7b\u522b\u67e5\u770b\u6587\u6863\uff1a\n\n"
        "  \u6240\u6709\u7c7b\u522b  -- \u663e\u793a\u6240\u6709\u5185\u5bb9\uff08\u9ed8\u8ba4\uff09\n"
        "  \u6cd5\u89c4      -- FDA\u63d0\u4ea4\u3001\u9884\u63d0\u4ea4\u5305\u3001\u5408\u89c4\u6587\u6863\n"
        "  \u6280\u672f      -- \u8bbe\u8ba1\u89c4\u683c\u3001\u7b97\u6cd5\u62a5\u544a\u3001\u534f\u8bae\u6587\u6863\n"
        "  \u5546\u4e1a      -- \u6f14\u793a\u6587\u7a3f\u3001\u6295\u8d44\u8005\u6750\u6599\u3001\u6761\u6b3e\u6e05\u5355\n"
        "  \u6cd5\u5f8b      -- IP\u8f6c\u8ba9\u3001\u516c\u53f8\u6587\u4ef6\u3001\u534f\u8bae\n"
        "  \u8d22\u52a1      -- \u9884\u7b97\u62a5\u544a\u3001\u71c3\u70e7\u62a5\u544a\u3001\u8d22\u52a1\u62a5\u8868\n"
        "  \u6a21\u677f      -- \u53ef\u91cd\u590d\u4f7f\u7528\u7684\u5e38\u89c4\u6587\u6863\u6a21\u677f")

    pdf.sub("27.3 \u6587\u6863\u8868\u683c")
    pdf.txt(
        "\u6bcf\u884c\u663e\u793a\uff1a\n\n"
        "  \u7c7b\u522b         -- \u989c\u8272\u7f16\u7801\u6807\u7b7e\n"
        "  \u6587\u63a7\u7f16\u53f7     -- \u552f\u4e00\u6587\u63a7\u7f16\u53f7\uff08\u5982 DCN-REG-001\uff09\n"
        "  \u6587\u6863         -- \u70b9\u51fb\u540d\u79f0\u6253\u5f00\u4fee\u8ba2\u5386\u53f2\u9762\u677f\n"
        "  \u7248\u672c         -- \u5f53\u524d\u7248\u672c\u53f7\n"
        "  \u6700\u540e\u66f4\u65b0     -- \u6700\u8fd1\u7f16\u8f91\u65e5\u671f\n"
        "  \u8d1f\u8d23\u4eba       -- \u8d1f\u8d23\u6587\u6863\u7684\u56e2\u961f\u6210\u5458\n"
        "  \u5173\u8054\u91cc\u7a0b\u7891   -- \u5173\u8054\u7684R\u7f16\u53f7\u6216T\u7f16\u53f7\u91cc\u7a0b\u7891\n"
        "  \u72b6\u6001         -- \u53ef\u70b9\u51fb\u6807\u7b7e\uff08\u4ec5PMP\uff09\u63a8\u8fdb\u5de5\u4f5c\u6d41\n\n"
        "\u72b6\u6001\u6807\u7b7e\u5728\u4e94\u4e2a\u751f\u547d\u5468\u671f\u9636\u6bb5\u4e4b\u95f4\u5faa\u73af\uff1a\n\n"
        "  \u8349\u7a3f -> \u5ba1\u6838\u4e2d -> \u5df2\u6279\u51c6 -> \u5df2\u751f\u6548 -> \u5df2\u5e9f\u6b62\n\n"
        "\u72b6\u6001\u53d8\u66f4\u8bb0\u5f55\u5230\u5ba1\u8ba1\u8ffd\u8e2a\u4ee5\u5b9e\u73b0DHF\u53ef\u8ffd\u6eaf\u6027\u3002")

    pdf.sub("27.4 \u4fee\u8ba2\u5386\u53f2")
    pdf.txt(
        "\u70b9\u51fb\u4efb\u4f55\u6587\u6863\u540d\u79f0\u53ef\u6253\u5f00\u6a21\u6001\u9762\u677f\uff0c\u663e\u793a\uff1a\n\n"
        "  \u6587\u6863\u5143\u6570\u636e  -- \u8d1f\u8d23\u4eba\u3001\u7248\u672c\u3001\u751f\u6548\u65e5\u671f\u3001\u4e0b\u6b21\u5ba1\u6838\u3001\u5173\u8054\u91cc\u7a0b\u7891\n"
        "  \u4fee\u8ba2\u8868     -- \u6bcf\u6b21\u4fee\u8ba2\u7684\u7248\u6b21\u3001\u65e5\u671f\u3001\u4f5c\u8005\u548c\u53d8\u66f4\u8bf4\u660e\n\n"
        "\u8fd9\u4e3a\u8bbe\u8ba1\u63a7\u5236\u6587\u6863\u63d0\u4f9b\u5b8c\u6574\u7684\u53ef\u8ffd\u6eaf\u6027\u3002")

    pdf.sub("27.5 \u5ba1\u6838\u6392\u7a0b")
    pdf.txt(
        "\u6bcf\u4e2a\u6587\u6863\u90fd\u6709\u4e0b\u6b21\u5ba1\u6838\u65e5\u671f\u3002\u8d85\u8fc7\u5ba1\u6838\u65e5\u671f\u7684\u6587\u6863\u4f1a\u4ee5"
        "\u8b66\u544a\u6807\u7b7e\u548c\u7740\u8272\u884c\u80cc\u666f\u9ad8\u4eae\u663e\u793a\u3002\u6458\u8981\u680f\u663e\u793a\u903e\u671f\u5ba1\u6838\u7684\u6570\u91cf\u3002")

    pdf.sub("27.6 \u56e2\u961f\u6210\u5458\u4e0e\u4eea\u8868\u76d8\u89d2\u8272")
    pdf.txt(
        "\u4eea\u8868\u76d8\u56e2\u961f\u7531\u56db\u540d\u6210\u5458\u7ec4\u6210\uff1a\n\n"
        "  Lon Dailey -- \u6cd5\u89c4\u53ca\u6295\u8d44\u8005\u5173\u7cfb\uff08\u5317\u7f8e\uff09\n"
        "    \u804c\u8d23\uff1a510(k)\u51c6\u5907\u3001\u6807\u51c6\u5408\u89c4\u3001\u5317\u7f8e\u6295\u8d44\u8005\u5173\u7cfb\u3001\u9879\u76ee\u7ba1\u7406\n\n"
        "  \u6234\u535a\u58eb -- \u9996\u5e2d\u6280\u672f\u5b98\n"
        "    \u804c\u8d23\uff1asEMG\u7b97\u6cd5\u5f00\u53d1\u3001EIT\u539f\u578b\u3001MyoBus\u96c6\u6210\u3001\u6280\u672f\u6587\u6863\n\n"
        "  Lawrence Liu -- CEO\uff0cB\u516c\u53f8\n"
        "    \u804c\u8d23\uff1a\u6295\u8d44\u8005\u5173\u7cfb\uff08\u4e9a\u6d32\uff09\u3001\u5546\u4e1a\u6218\u7565\u3001\u8fd0\u8425\u7ba1\u7406\n\n"
        "  Danielle Liu -- \u4f1a\u8ba1\n"
        "    \u804c\u8d23\uff1a\u6708\u5ea6\u71c3\u70e7\u62a5\u544a\u3001\u9884\u7b97\u8ffd\u8e2a\u3001\u8d22\u52a1\u62a5\u8868")

    # 28. 留言板
    pdf.add_page()
    pdf.sec(28, "\u9009\u9879\u530114\uff1a\u7559\u8a00\u677f")
    pdf.txt(
        "\u7559\u8a00\u677f\u662f\u4eea\u8868\u76d8\u7684\u76ee\u7684\u9a71\u52a8\u5185\u90e8\u6d88\u606f\u5c42\u3002"
        "\u6bcf\u4e2a\u4e3b\u9898\u5bf9\u5e94\u4e09\u79cd\u610f\u56fe\u4e4b\u4e00\u2014\u2014\u544a\u77e5\u3001\u51b3\u7b56\u6216\u884c\u52a8\u2014\u2014"
        "\u5e76\u6309\u5de5\u4f5c\u6d41\u7ec4\u7ec7\uff0c\u5177\u6709\u62e5\u6709\u8005\u3001\u76ee\u6807\u3001\u751f\u547d\u5468\u671f\u548c\u4f18\u5148\u7ea7\u3002"
        "\u6d88\u606f\u901a\u8fc7\u670d\u52a1\u5668\u6570\u636e\u5e93\uff08Supabase\uff09\u5b9e\u65f6\u540c\u6b65\uff0c"
        "localStorage\u4f5c\u4e3a\u5907\u4efd\u3002")

    pdf.sub("28.1 \u7ed3\u6784\u5316\u4e3b\u9898")
    pdf.txt(
        "\u6bcf\u4e2a\u4e3b\u9898\u5305\u542b\uff1a\n\n"
        "  \u6807\u9898       -- \u5bf9\u8bdd\u7684\u63cf\u8ff0\u6027\u540d\u79f0\n"
        "  \u5de5\u4f5c\u6d41     -- \u9879\u76ee / \u6cd5\u89c4 / \u5de5\u7a0b / \u4e34\u5e8a / \u5546\u52a1 / \u8fd0\u8425\n"
        "  \u610f\u56fe       -- \u544a\u77e5\uff08\u5206\u4eab\u4fe1\u606f\uff09\u3001\u51b3\u7b56\uff08\u8bb0\u5f55\u51b3\u5b9a\uff09\u3001\u884c\u52a8\uff08\u5206\u914d\u4efb\u52a1\uff09\n"
        "  \u62e5\u6709\u8005     -- \u521b\u5efa\u4e3b\u9898\u7684\u89d2\u8272\n"
        "  \u76ee\u6807       -- \u53ef\u9009\u7684\u76ee\u7684\u8bf4\u660e\n"
        "  \u4f18\u5148\u7ea7     -- \u6b63\u5e38 / \u7d27\u6025 / \u5347\u7ea7\uff08\u89c6\u89c9\u6307\u793a\u5668\uff09\n"
        "  \u751f\u547d\u5468\u671f   -- \u8fdb\u884c\u4e2d\u6216\u5df2\u89e3\u51b3\uff08\u542b\u89e3\u51b3\u65b9\u6848\u6458\u8981\uff09\n\n"
        "\u539f\u59cbQ1-Q30\u9884\u5b9a\u4e49\u95ee\u9898\u5728\u9996\u6b21\u52a0\u8f7d\u65f6\u81ea\u52a8\u8fc1\u79fb\u4e3a\u4e3b\u9898\u3002"
        "\u73b0\u6709\u6d88\u606f\u901a\u8fc7Supabase\u4fdd\u7559\u3002"
        "\u53ef\u968f\u65f6\u4f7f\u7528\u201c\u65b0\u4e3b\u9898\u201d\u6309\u94ae\u521b\u5efa\u65b0\u4e3b\u9898\u3002")

    pdf.sub("28.2 \u51b3\u7b56\u53ef\u89c1\u6027")
    pdf.txt(
        "\u51b3\u7b56\u662f\u4e00\u7b49\u5bf9\u8c61\uff0c\u4e0d\u4f1a\u57cb\u6ca1\u5728\u804a\u5929\u4e2d\uff1a\n\n"
        "  [DECISION]\u524d\u7f00 -- \u5728\u6d88\u606f\u524d\u52a0[DECISION]\u81ea\u52a8\u8bb0\u5f55\n"
        "  \u8bb0\u5f55\u51b3\u7b56\u6309\u94ae -- \u901a\u8fc7\u4e3b\u9898\u64cd\u4f5c\u680f\u624b\u52a8\u8bb0\u5f55\u51b3\u7b56\n"
        "  \u51b3\u7b56\u89c6\u56fe     -- \u4e13\u7528\u89c6\u56fe\u5c55\u793a\u6240\u6709\u6709\u6d3b\u52a8\u51b3\u7b56\u7684\u4e3b\u9898\n"
        "  \u51b3\u7b56\u5361\u7247     -- \u663e\u793a\u6587\u672c\u3001\u7406\u7531\u3001\u51b3\u7b56\u8005\u548c\u65e5\u671f\n"
        "  \u5ba1\u8ba1\u8ddf\u8e2a     -- \u6240\u6709\u51b3\u7b56\u8bb0\u5f55\u5728\u5ba1\u8ba1\u65e5\u5fd7\u4e2d")

    pdf.sub("28.3 \u56db\u4e2a\u89c6\u56fe")
    pdf.txt(
        "\u89c6\u56fe\u5207\u6362\u5668\u63d0\u4f9b\u56db\u4e2a\u89c6\u89d2\uff1a\n\n"
        "  \u6240\u6709\u4e3b\u9898   -- \u5339\u914d\u5f53\u524d\u8fc7\u6ee4\u6761\u4ef6\u7684\u6240\u6709\u4e3b\u9898\n"
        "  \u6211\u7684\u4e8b\u9879   -- \u60a8\u62e5\u6709\u6216\u88ab\u5206\u914d\u7684\u4e3b\u9898\n"
        "  \u51b3\u7b56\u8bb0\u5f55   -- \u6709\u6d3b\u52a8\u51b3\u7b56\u7684\u4e3b\u9898\n"
        "  \u7ba1\u7406\u89c6\u56fe   -- \u9ad8\u4fe1\u53f7\u89c6\u56fe\uff1a\u7d27\u6025\u3001\u5347\u7ea7\u3001\u51b3\u7b56\u548c\u5df2\u89e3\u51b3\u7684\u4e3b\u9898")

    pdf.sub("28.4 \u8fc7\u6ee4\u5668\u4e0e\u6458\u8981\u4eea\u8868\u76d8")
    pdf.txt(
        "  \u5de5\u4f5c\u6d41\u8fc7\u6ee4   -- \u4e0b\u62c9\u83dc\u5355\u663e\u793a\u5355\u4e2a\u5de5\u4f5c\u6d41\u6216\u5168\u90e8\n"
        "  \u751f\u547d\u5468\u671f\u8fc7\u6ee4 -- \u663e\u793a\u8fdb\u884c\u4e2d\u3001\u5df2\u89e3\u51b3\u6216\u5168\u90e8\u4e3b\u9898\n"
        "  \u6392\u5e8f\u987a\u5e8f       -- \u5347\u7ea7 > \u7d27\u6025 > \u6b63\u5e38\uff0c\u7136\u540e\u6309\u6700\u65b0\u6d88\u606f\u6392\u5e8f\n\n"
        "\u9876\u90e8\u4e94\u4e2a\u6458\u8981\u5361\u7247\uff1a\n\n"
        "  \u8fdb\u884c\u4e2d\u4e3b\u9898     -- \u8fdb\u884c\u4e2d\u7684\u4e3b\u9898\u6570\u91cf\n"
        "  \u7d27\u6025/\u5347\u7ea7     -- \u9ad8\u4f18\u5148\u7ea7\u8fdb\u884c\u4e2d\u4e3b\u9898\u6570\u91cf\n"
        "  \u51b3\u7b56           -- \u5df2\u8bb0\u5f55\u7684\u6d3b\u52a8\u51b3\u7b56\u6570\u91cf\n"
        "  \u6211\u7684\u4e8b\u9879       -- \u5f53\u524d\u89d2\u8272\u62e5\u6709\u6216\u88ab\u5206\u914d\u7684\u4e3b\u9898\n"
        "  \u672a\u8bfb\u6d88\u606f       -- \u5f53\u524d\u89d2\u8272\u5c1a\u672a\u8bfb\u53d6\u7684\u6d88\u606f")

    pdf.sub("28.5 \u8d23\u4efb\u4e0e\u884c\u52a8")
    pdf.txt(
        "  \u521b\u5efa\u884c\u52a8   -- \u5c06\u4e3b\u9898\u5206\u914d\u7ed9\u7279\u5b9a\u89d2\u8272\u5e76\u8bbe\u5b9a\u622a\u6b62\u65e5\u671f\n"
        "  \u8d1f\u8d23\u4eba\u5fbd\u7ae0 -- \u5728\u4e3b\u9898\u5361\u7247\u4e0a\u663e\u793a\u8d1f\u8d23\u4eba\n"
        "  \u622a\u6b62\u65e5\u671f   -- \u4e0e\u8d1f\u8d23\u4eba\u4e00\u8d77\u663e\u793a\n"
        "  \u610f\u56fe\u6807\u8bb0   -- \u6d88\u606f\u524d\u7f00[ACTION]\u8fdb\u884c\u89c6\u89c9\u9ad8\u4eae")

    pdf.sub("28.6 \u5173\u8054\u5de5\u4ef6")
    pdf.txt(
        "\u4e3b\u9898\u53ef\u4ee5\u8fde\u63a5\u5230\u5176\u4ed6\u4eea\u8868\u76d8\u9879\u76ee\uff1a\n\n"
        "  \u5173\u8054\u7c7b\u578b\uff1a\u91cc\u7a0b\u7891\u3001\u98ce\u9669\u3001\u95e8\u63a7\u3001\u6587\u6863\u3001\u6807\u51c6\u3001\u4efb\u52a1\n"
        "  \u6bcf\u4e2a\u5173\u8054\u5de5\u4ef6\u5728\u4e3b\u9898\u5361\u7247\u4e0a\u663e\u793a\u4e3a\u5fbd\u7ae0\n"
        "  \u5173\u8054\u5b58\u50a8\u4e3a\u4e3b\u9898\u5143\u6570\u636e\u7684\u4e00\u90e8\u5206")

    pdf.sub("28.7 \u751f\u547d\u5468\u671f\u7ba1\u7406")
    pdf.txt(
        "  \u89e3\u51b3       -- \u5c06\u4e3b\u9898\u6807\u8bb0\u4e3a\u5df2\u89e3\u51b3\u5e76\u9644\u6458\u8981\n"
        "  \u91cd\u65b0\u6253\u5f00   -- \u91cd\u65b0\u6253\u5f00\u5df2\u89e3\u51b3\u7684\u4e3b\u9898\n"
        "  \u89e3\u51b3\u65b9\u6848   -- \u5728\u5df2\u89e3\u51b3\u7684\u4e3b\u9898\u5361\u7247\u4e0a\u663e\u793a\n"
        "  \u5ba1\u8ba1\u8ddf\u8e2a   -- \u6240\u6709\u751f\u547d\u5468\u671f\u53d8\u66f4\u5747\u88ab\u8bb0\u5f55")

    pdf.sub("28.8 \u5df2\u8bfb\u56de\u6267\u4e0e\u901a\u77e5")
    pdf.txt(
        "  \u5df2\u53d1\u6d88\u606f   -- \u663e\u793a\u5355\u52fe\uff08\u672a\u8bfb\uff09\u6216\u53cc\u52fe\uff08\u5df2\u8bfb\uff09\n"
        "  \u6536\u5230\u7684\u6d88\u606f -- \u672a\u8bfb\u65f6\u5de6\u4fa7\u84dd\u8272\u8fb9\u6846\u9ad8\u4eae\n"
        "  \u6807\u8bb0\u5df2\u8bfb   -- \u70b9\u51fb\u4fe1\u5c01\u56fe\u6807\u6807\u8bb0\u4e3a\u5df2\u8bfb\n"
        "  \u6807\u7b7e\u5fbd\u7ae0   -- \u7ea2\u8272\u8ba1\u6570\u5fbd\u7ae0\u663e\u793a\u5f53\u524d\u89d2\u8272\u7684\u672a\u8bfb\u603b\u6570\n"
        "  \u5f39\u51fa\u901a\u77e5   -- \u5176\u4ed6\u89d2\u8272\u7684\u65b0\u6d88\u606f\u89e6\u53d1\u5f39\u51fa\u63d0\u793a\n"
        "  \u8de8\u6807\u7b7e\u540c\u6b65 -- \u6d88\u606f\u901a\u8fc7StorageEvent\u5728\u6d4f\u89c8\u5668\u6807\u7b7e\u95f4\u540c\u6b65")

    pdf.sub("28.9 \u5bfc\u51fa\u4e0e\u5f52\u6863")
    pdf.txt(
        "  \u5bfc\u51fa  -- \u5c06\u6240\u6709\u4e3b\u9898\u548c\u51b3\u7b56\u4e0b\u8f7d\u4e3a.txt\u6587\u4ef6\n"
        "  \u5f52\u6863  -- \u5c06\u4e3b\u9898\u6d88\u606f\u4fdd\u5b58\u5230\u5f52\u6863\u5b58\u50a8\u5e76\u6e05\u9664\n"
        "  \u67e5\u770b\u5f52\u6863 / \u5220\u9664\u5f52\u6863 -- \u6d4f\u89c8\u6216\u5220\u9664\u5f52\u6863\u6761\u76ee")

    pdf.sub("28.10 \u6570\u636e\u5b58\u50a8")
    pdf.txt(
        "\u6d88\u606f\u5b9e\u65f6\u540c\u6b65\u5230\u670d\u52a1\u5668\u6570\u636e\u5e93\uff08Supabase\uff09\u3002"
        "\u4e3b\u9898\u5143\u6570\u636e\uff08\u6807\u9898\u3001\u5de5\u4f5c\u6d41\u3001\u610f\u56fe\u3001\u62e5\u6709\u8005\u3001\u751f\u547d\u5468\u671f\u3001\u5173\u8054\u5de5\u4ef6\uff09"
        "\u5b58\u50a8\u5728localStorage\u7684\u2018ctower_mb_threads\u2019\u4e2d\u3002"
        "\u51b3\u7b56\u5b58\u50a8\u5728\u2018ctower_mb_decisions\u2019\u4e2d\u3002"
        "\u6d88\u606f\u7f13\u5b58\u4f7f\u7528\u2018ctower_qa_messages\u2019\u4f5c\u4e3a\u672c\u5730\u5907\u4efd\u3002"
        "\u8bbe\u7f6e\u548c\u5f52\u6863\u4e5f\u5728\u4f1a\u8bdd\u95f4\u6301\u4e45\u5316\u3002")

    # 29 关键术语表
    pdf.add_page()
    pdf.sec(29, "\u5173\u952e\u672f\u8bed\u8868")
    pdf.ln(2)
    terms = [
        ("M+N", "\u6708\u4efd\u6807\u8bb0\u3002M+0 = \u9879\u76ee\u542f\u52a8\uff082026\u5e743\u6708\uff09\u3002M+6 = \u542f\u52a8\u540e6\u4e2a\u6708\u3002\u8d2f\u7a7f\u6240\u6709\u8ba1\u5212\u4f7f\u7528\u3002"),
        ("PMP", "\u9879\u76ee\u7ba1\u7406\u4e13\u4e1a\u4eba\u5458\u3002\u5bf9\u6240\u6709\u95e8\u63a7\u62e5\u6709\u6700\u9ad8\u51b3\u7b56\u6743\u3002"),
        ("510(k)", "FDA\u4e0a\u5e02\u524d\u901a\u77e5\u9014\u5f84\uff0c\u9002\u7528\u4e8eII\u7c7b\u533b\u7597\u5668\u68b0\u3002"),
        ("\u95e8\u63a7(Gate)", "\u9636\u6bb5-\u95e8\u63a7\u51b3\u7b56\u68c0\u67e5\u70b9\u3002\u5728PMP\u51b3\u5b9a\u901a\u8fc7\u4e4b\u524d\u9879\u76ee\u4e0d\u80fd\u8d8a\u8fc7\u95e8\u63a7\u3002"),
        ("CR", "\u53d8\u66f4\u8bf7\u6c42\u3002\u6280\u672f\u6216\u5546\u4e1a\u56e2\u961f\u63d0\u4ea4\u7684\u72b6\u6001\u4fee\u6539\u6b63\u5f0f\u8bf7\u6c42\uff0c\u9700\u8981PMP\u5ba1\u6279\u3002"),
        ("sEMG", "\u8868\u9762\u808c\u7535\u56fe " + EM + " \u6a21\u5757A\u3002\u975e\u4fb5\u5165\u6027\u76d1\u6d4b\u795e\u7ecf\u547c\u5438\u9a71\u52a8\u3002"),
        ("EIT", "\u7535\u963b\u6297\u65ad\u5c42\u6210\u50cf " + EM + " \u6a21\u5757B\u3002\u80ba\u90e8\u901a\u6c14\u548c\u704c\u6ce8\u7684\u6a2a\u622a\u9762\u56fe\u50cf\u3002"),
        ("V/Q", "\u901a\u6c14/\u704c\u6ce8\u6bd4 " + EM + " \u5173\u952e\u4e34\u5e8a\u6d4b\u91cf\u3002"),
        ("MyoBus", "\u4e13\u6709\u96c6\u6210\u534f\u8bae\uff0c\u4ee5<1ms\u65f6\u95f4\u6233\u5bf9\u9f50\u540c\u6b65sEMG\u548cEIT\u6570\u636e\u3002"),
        ("IKN", "FDA\u4ea7\u54c1\u4ee3\u7801\uff0c\u7528\u4e8esEMG\u547c\u5438\u76d1\u6d4b\u8bbe\u5907\u3002"),
        ("DQS", "FDA\u4ea7\u54c1\u4ee3\u7801\uff0c\u7528\u4e8eEIT\u80f8\u90e8\u6210\u50cf\u8bbe\u5907\u3002"),
        ("\u9884\u63d0\u4ea4/Q-Sub", "\u5411FDA\u63d0\u4ea4\u7684\u9884\u63d0\u4ea4\u8bf7\u6c42\uff0c\u7528\u4e8eQ\u4f1a\u8bae\u8ba8\u8bba\u6cd5\u89c4\u7b56\u7565\u3002"),
        ("ISO 14971", "\u533b\u7597\u5668\u68b0\u98ce\u9669\u7ba1\u7406\u56fd\u9645\u6807\u51c6\u3002"),
        ("IEC 60601", "\u533b\u7528\u7535\u6c14\u8bbe\u5907\u5b89\u5168\u548c\u6027\u80fd\u6807\u51c6\u7cfb\u5217\u3002"),
        ("DHF", "\u8bbe\u8ba1\u5386\u53f2\u6587\u4ef6 " + EM + " \u533b\u7597\u5668\u68b0\u8bbe\u8ba1\u7684\u53d7\u76d1\u7ba1\u6587\u6863\u5305\u3002"),
        ("CAPA", "纠正和预防措施 " + EM + " 处理不合格项的正式流程。"),
        ("看板(Kanban)", "可视化任务管理面板，列代表工作阶段。"),
        ("FAB", "\u6d6e\u52a8\u64cd\u4f5c\u6309\u94ae " + EM + " \u53f3\u4e0b\u89d2\u7684\u5706\u5f62\u6309\u94ae\u3002"),
        ("IndexedDB", "\u6d4f\u89c8\u5668\u672c\u5730\u5b58\u50a8\uff0c\u7528\u4f5c\u6587\u6863\u6301\u4e45\u5316\u7684\u5907\u4efd\u3002"),
        ("\u8dd1\u9053", "\u6309\u5f53\u524d\u71c3\u70e7\u7387\uff0c\u9879\u76ee\u53ef\u7ee7\u7eed\u8fd0\u884c\u7684\u5269\u4f59\u6708\u6570\u3002"),
        ("NRE", "非经常性工程费用 " + EM + " 制造设置的一次性工程成本。"),
    ]
    for k, v in terms:
        pdf.kv(k, v)
        pdf.ln(1)

    path = os.path.join(OUT_DIR, "Dashboard_Users_Guide_CN.pdf")
    pdf.output(path)
    return path


if __name__ == "__main__":
    en = build_english()
    print(f"English guide: {en}")
    cn = build_chinese()
    print(f"Chinese guide: {cn}")
    print("Done.")
