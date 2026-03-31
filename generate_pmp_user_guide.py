#!/usr/bin/env python3
"""
Generate PMP User's Guide — EN + CN
Comprehensive guide for using the Control Tower PM Dashboard.
"""

import os
from fpdf import FPDF

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
CJK_FONT = "/Library/Fonts/Arial Unicode.ttf"

# Colors
NAVY = (10, 40, 100)
ACCENT = (0, 120, 200)
DARK = (25, 25, 30)
TEXT = (40, 40, 45)
GRAY = (110, 110, 120)
LIGHT_BG = (245, 245, 248)
GREEN = (16, 120, 80)
AMBER = (180, 120, 10)
RED = (200, 40, 40)

# Unicode sanitization for CJK
_MAP = str.maketrans(
    {
        "\u2014": "--",
        "\u2013": "-",
        "\u2019": "'",
        "\u2018": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2026": "...",
        "\u00a0": " ",
        "\u2022": "-",
        "\u00b7": "-",
        "\u2192": "->",
        "\u2190": "<-",
        "\u2003": " ",
    }
)


def _a(s):
    return s.translate(_MAP)


# ────────────────────────────────────────────
# English PDF class
# ────────────────────────────────────────────
class ENGuide(FPDF):
    @staticmethod
    def _s(text):
        return text.translate(_MAP)

    def header(self):
        if self.page_no() <= 2:
            return
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(*GRAY)
        self.cell(
            0, 8, self._s("Control Tower PM Dashboard -- PMP User's Guide"), align="R", ln=True
        )
        self.ln(2)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(*GRAY)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")

    def sec(self, num, title):
        self.set_font("Helvetica", "B", 15)
        self.set_text_color(*NAVY)
        self.cell(0, 9, self._s(f"{num}. {title}"), ln=True)
        self.set_draw_color(*ACCENT)
        self.set_line_width(0.6)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(5)

    def sub(self, title):
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(*DARK)
        self.cell(0, 7, self._s(title), ln=True)
        self.ln(1)

    def txt(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*TEXT)
        self.multi_cell(0, 5.5, self._s(text))
        self.ln(2)

    def bul(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*TEXT)
        self.multi_cell(0, 5.5, self._s(f"  - {text}"))
        self.ln(1)

    def kv(self, key, val):
        x = self.get_x()
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(*ACCENT)
        self.cell(50, 6, self._s(key + ":"))
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*TEXT)
        self.multi_cell(0, 6, self._s(val))
        self.ln(1)

    def tip_box(self, text):
        self.set_fill_color(*LIGHT_BG)
        self.set_draw_color(*GREEN)
        self.set_line_width(0.4)
        x, y = self.get_x(), self.get_y()
        self.rect(10, y, 190, 18, style="DF")
        self.set_xy(14, y + 2)
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*GREEN)
        self.cell(20, 5, "TIP:")
        self.set_font("Helvetica", "", 9)
        self.set_text_color(*TEXT)
        self.multi_cell(160, 5, self._s(text))
        self.set_y(y + 20)

    def warn_box(self, text):
        self.set_fill_color(255, 248, 230)
        self.set_draw_color(*AMBER)
        self.set_line_width(0.4)
        x, y = self.get_x(), self.get_y()
        self.rect(10, y, 190, 18, style="DF")
        self.set_xy(14, y + 2)
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*AMBER)
        self.cell(30, 5, "IMPORTANT:")
        self.set_font("Helvetica", "", 9)
        self.set_text_color(*TEXT)
        self.multi_cell(152, 5, self._s(text))
        self.set_y(y + 20)


# ────────────────────────────────────────────
# Chinese PDF class
# ────────────────────────────────────────────
class CNGuide(FPDF):
    def __init__(self):
        super().__init__()
        self.add_font("CJK", "", CJK_FONT, uni=True)
        self.add_font("CJK", "B", CJK_FONT, uni=True)
        self.add_font("CJK", "I", CJK_FONT, uni=True)

    def header(self):
        if self.page_no() <= 2:
            return
        self.set_font("CJK", "I", 8)
        self.set_text_color(*GRAY)
        self.cell(0, 8, _a("Control Tower PM 仪表板 — PMP 用户指南"), align="R", ln=True)
        self.ln(2)

    def footer(self):
        self.set_y(-15)
        self.set_font("CJK", "I", 8)
        self.set_text_color(*GRAY)
        self.cell(0, 10, _a(f"第 {self.page_no()}/{{nb}} 页"), align="C")

    def sec(self, num, title):
        self.set_font("CJK", "B", 15)
        self.set_text_color(*NAVY)
        self.cell(0, 9, _a(f"{num}. {title}"), ln=True)
        self.set_draw_color(*ACCENT)
        self.set_line_width(0.6)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(5)

    def sub(self, title):
        self.set_font("CJK", "B", 11)
        self.set_text_color(*DARK)
        self.cell(0, 7, _a(title), ln=True)
        self.ln(1)

    def txt(self, text):
        self.set_font("CJK", "", 10)
        self.set_text_color(*TEXT)
        self.multi_cell(0, 6, _a(text))
        self.ln(2)

    def bul(self, text):
        self.set_font("CJK", "", 10)
        self.set_text_color(*TEXT)
        self.multi_cell(0, 6, _a(f"  - {text}"))
        self.ln(1)

    def kv(self, key, val):
        self.set_font("CJK", "B", 10)
        self.set_text_color(*ACCENT)
        self.cell(55, 6, _a(key + ":"))
        self.set_font("CJK", "", 10)
        self.set_text_color(*TEXT)
        self.multi_cell(0, 6, _a(val))
        self.ln(1)

    def tip_box(self, text):
        self.set_fill_color(*LIGHT_BG)
        self.set_draw_color(*GREEN)
        self.set_line_width(0.4)
        y = self.get_y()
        self.rect(10, y, 190, 18, style="DF")
        self.set_xy(14, y + 2)
        self.set_font("CJK", "B", 9)
        self.set_text_color(*GREEN)
        self.cell(25, 5, _a("提示:"))
        self.set_font("CJK", "", 9)
        self.set_text_color(*TEXT)
        self.multi_cell(155, 5, _a(text))
        self.set_y(y + 20)

    def warn_box(self, text):
        self.set_fill_color(255, 248, 230)
        self.set_draw_color(*AMBER)
        self.set_line_width(0.4)
        y = self.get_y()
        self.rect(10, y, 190, 18, style="DF")
        self.set_xy(14, y + 2)
        self.set_font("CJK", "B", 9)
        self.set_text_color(*AMBER)
        self.cell(30, 5, _a("重要:"))
        self.set_font("CJK", "", 9)
        self.set_text_color(*TEXT)
        self.multi_cell(152, 5, _a(text))
        self.set_y(y + 20)


# ────────────────────────────────────────────
# Content builders
# ────────────────────────────────────────────


def build_english():
    pdf = ENGuide()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)

    # ── Cover ──
    pdf.add_page()
    pdf.ln(50)
    pdf.set_font("Helvetica", "B", 28)
    pdf.set_text_color(*NAVY)
    pdf.cell(0, 14, "Control Tower", align="C", ln=True)
    pdf.set_font("Helvetica", "", 18)
    pdf.set_text_color(*ACCENT)
    pdf.cell(0, 10, "PM Dashboard", align="C", ln=True)
    pdf.ln(8)
    pdf.set_font("Helvetica", "B", 22)
    pdf.set_text_color(*DARK)
    pdf.cell(0, 12, "PMP User's Guide", align="C", ln=True)
    pdf.ln(20)
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(*GRAY)
    pdf.cell(0, 7, "Medical Device Development Project Management", align="C", ln=True)
    pdf.cell(0, 7, "FDA 510(k) Regulatory Pathway", align="C", ln=True)
    pdf.ln(30)
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 6, "510k Bridge", align="C", ln=True)
    pdf.cell(0, 6, "Version 1.0 -- March 2026", align="C", ln=True)

    # ── Table of Contents ──
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(*NAVY)
    pdf.cell(0, 10, "Table of Contents", ln=True)
    pdf.ln(5)
    toc = [
        ("1", "Getting Started"),
        ("2", "Dashboard Overview"),
        ("3", "Role-Based Access & Tier System"),
        ("4", "Dual-Track Milestones"),
        ("5", "Gate System"),
        ("6", "Regulatory Tracker"),
        ("7", "Risk Dashboard"),
        ("8", "Audit Trail"),
        ("9", "Document Control"),
        ("10", "Actions"),
        ("11", "Timeline"),
        ("12", "Budget"),
        ("13", "Cash / Runway"),
        ("14", "US Investment"),
        ("15", "Cap Table"),
        ("16", "Resources"),
        ("17", "Suppliers"),
        ("18", "Message Board"),
        ("19", "FDA Communications Center"),
        ("20", "Setup Wizard & Templates"),
        ("21", "Keyboard Shortcuts & Tips"),
        ("22", "Troubleshooting"),
        ("23", "Glossary of FDA & Regulatory Terms"),
    ]
    pdf.set_font("Helvetica", "", 11)
    for num, title in toc:
        pdf.set_text_color(*DARK)
        pdf.cell(12, 7, num + ".")
        pdf.set_text_color(*TEXT)
        pdf.cell(0, 7, title, ln=True)

    # ── 1. Getting Started ──
    pdf.add_page()
    pdf.sec(1, "Getting Started")
    pdf.txt(
        "The Control Tower PM Dashboard is a comprehensive project management platform "
        "designed specifically for FDA 510(k) medical device development. It provides "
        "real-time visibility across regulatory, technical, and business workstreams."
    )
    pdf.sub("System Requirements")
    pdf.bul("Modern web browser (Chrome, Firefox, Safari, Edge)")
    pdf.bul("Internet connection for Supabase sync (offline mode available)")
    pdf.bul("Screen resolution 1280x720 or higher recommended")

    pdf.sub("First Launch")
    pdf.txt(
        "When you first open the dashboard, the Setup Wizard will guide you through "
        "project configuration. You can choose from 7 device templates (Respiratory, "
        "Cardiovascular, Orthopedic, IVD, Imaging, Rehabilitation, SaMD) or start "
        "from scratch. Alternatively, click 'Load Demo Data' to explore with sample data."
    )

    pdf.sub("Login & Authentication")
    pdf.txt(
        "The dashboard uses a role-based login. Enter the password provided by your "
        "project administrator. After authentication, you will see the dashboard with "
        "tabs appropriate for your assigned role and subscription tier."
    )

    pdf.tip_box("Bookmark the dashboard URL for quick access. Your project data is saved automatically.")

    # ── 2. Dashboard Overview ──
    pdf.add_page()
    pdf.sec(2, "Dashboard Overview")
    pdf.txt(
        "The dashboard consists of a header bar with role/tier selectors, a horizontal "
        "tab navigation bar with 16 functional tabs, and a main content area. Each tab "
        "focuses on a specific aspect of the 510(k) project lifecycle."
    )

    pdf.sub("Header Bar")
    pdf.bul("Project name and subtitle (bilingual EN/CN)")
    pdf.bul("Role selector: Switch between PMP, Technology, Business, and Accounting views")
    pdf.bul("Tier indicator: Shows your current subscription tier (Starter/Growth/Scale)")
    pdf.bul("Language toggle: Switch between English and Chinese interface")

    pdf.sub("The 16 Tabs")
    tabs = [
        ("Dual-Track", "Technical and regulatory milestone tracking"),
        ("Gate System", "Phase-gate reviews with criteria checklists"),
        ("Regulatory Tracker", "Standards compliance and progress monitoring"),
        ("Risk Dashboard", "ISO 14971 risk matrix with severity/probability"),
        ("Audit Trail", "Timestamped log of all dashboard changes"),
        ("Document Control", "ISO 13485-aligned document lifecycle management"),
        ("Actions", "Task board, DHF Document Tracker, DMR Document Tracker, and CAPA Log"),
        ("Timeline", "Month-by-month project timeline view"),
        ("Budget", "Budget categories with planned vs. actual tracking"),
        ("Cash / Runway", "Cash position, burn rate, and runway forecast"),
        ("US Investment", "Investor pipeline and IR activity tracking"),
        ("Cap Table", "Shareholder registry, equity events, vesting schedules"),
        ("Resources", "Team allocation and utilization monitoring"),
        ("Suppliers", "Supplier qualification and lead-time tracking"),
        ("Message Board", "Threaded discussions with decisions and action tracking"),
        ("FDA Comms", "Q-Sub generator, RTA checklist, and regulatory timelines (PMP only)"),
    ]
    for name, desc in tabs:
        pdf.kv(name, desc)

    pdf.warn_box("Some tabs may be restricted based on your role or subscription tier.")

    # ── 3. Role-Based Access ──
    pdf.add_page()
    pdf.sec(3, "Role-Based Access & Tier System")

    pdf.sub("User Roles")
    pdf.txt("The dashboard supports four primary roles, each with different access levels:")
    pdf.kv("PMP (Project Manager)", "Full access to all tabs. Can edit milestones, gates, risks, budgets, documents, and team. Only role that can see FDA Communications.")
    pdf.kv("Technology", "Can view and update technical milestones, risks, and documents. Can participate in Message Board. Cannot access financial tabs.")
    pdf.kv("Business", "Access to business milestones, budget, investment, and cap table. Can participate in Message Board.")
    pdf.kv("Accounting", "Read-only access to Budget, Cash/Runway, and Cap Table. Limited editing capabilities.")

    pdf.sub("Subscription Tiers")
    pdf.txt("Tab access is server-controlled via Supabase RLS. The tier determines which tabs are available:")
    pdf.kv("Starter ($500/mo)", "2 seats, 4 tabs: Dual-Track, Gates, Timeline, Budget")
    pdf.kv("Growth ($1,000/mo)", "5 seats, 13 tabs: All except Cap Table, FDA Comms, and US Investment")
    pdf.kv("Scale ($2,000/mo)", "10 seats, all 16 tabs including FDA Comms and Cap Table")

    pdf.tip_box("Your tier is managed server-side and cannot be changed from the dashboard UI.")

    # ── 4. Dual-Track ──
    pdf.add_page()
    pdf.sec(4, "Dual-Track Milestones")
    pdf.txt(
        "The Dual-Track tab displays parallel regulatory and technical milestone tracks. "
        "This mirrors the actual FDA 510(k) process where engineering development and "
        "regulatory preparation run concurrently."
    )
    pdf.sub("Technical Milestones")
    pdf.txt(
        "Technical milestones track engineering deliverables: design freeze, prototype "
        "testing, verification and validation activities, and design transfer. Each "
        "milestone shows its month, status, owner, and category."
    )
    pdf.sub("Regulatory Milestones")
    pdf.txt(
        "Regulatory milestones track FDA deliverables: Pre-Submission meeting, "
        "510(k) preparation, and submission filing. These are auto-generated based "
        "on your project duration."
    )
    pdf.sub("Editing Milestones")
    pdf.txt(
        "Click on a milestone status badge to cycle through: Not Started, In Progress, "
        "Complete, and Blocked. Only PMP and the owning role can change status. "
        "All changes are logged in the Audit Trail."
    )

    # ── 5. Gate System ──
    pdf.add_page()
    pdf.sec(5, "Gate System")
    pdf.txt(
        "The Gate System implements a phase-gate review process. Gates are automatically "
        "generated based on project duration (2-6 gates). Each gate has criteria that "
        "must be met before the project can proceed."
    )
    pdf.sub("Gate Criteria")
    pdf.txt(
        "Each gate has a checklist of criteria (e.g., 'Technical deliverables complete', "
        "'Budget on track', 'Risk mitigations confirmed'). Check criteria individually "
        "by clicking them. The gate status updates based on criteria completion."
    )
    pdf.sub("Gate Decisions")
    pdf.txt(
        "PMP can record gate decisions: Go, No-Go, or Conditional Go. Decisions are "
        "timestamped and attributed. Gate notes can capture discussion points and "
        "conditions for conditional approvals."
    )
    pdf.sub("Stakeholder Inputs")
    pdf.txt(
        "Technical and Business stakeholders can submit gate inputs. These appear "
        "in the gate review panel, providing a complete picture for the gate decision."
    )

    # ── 6. Regulatory Tracker ──
    pdf.add_page()
    pdf.sec(6, "Regulatory Tracker")
    pdf.txt(
        "The Regulatory Tracker monitors compliance with applicable standards. "
        "Standards are pre-populated based on your device template (e.g., IEC 60601-1 "
        "for electrical devices, ISO 10993 for biocompatibility) or entered manually."
    )
    pdf.sub("Tracking Standards")
    pdf.bul("Status: Not Started, In Progress, Complete")
    pdf.bul("Progress bar: 0-100% completion percentage")
    pdf.bul("Clause-level tracking for detailed compliance")
    pdf.txt(
        "Click the status badge to cycle through states. Update the progress slider "
        "to reflect actual completion. The FDA Comms tab uses these values to auto-populate "
        "the RTA checklist."
    )

    # ── 7. Risk Dashboard ──
    pdf.add_page()
    pdf.sec(7, "Risk Dashboard")
    pdf.txt(
        "The Risk Dashboard implements ISO 14971 risk management. Risks are displayed "
        "in a color-coded matrix showing severity, probability, and risk level. "
        "Template-specific risks are auto-populated from your device category."
    )
    pdf.sub("Risk Fields")
    pdf.kv("Severity", "How serious the harm would be (Low/Medium/High)")
    pdf.kv("Probability", "How likely the hazardous situation occurs (Low/Medium/High)")
    pdf.kv("Risk Level", "Color-coded: Green (acceptable), Yellow (ALARP), Red (unacceptable)")
    pdf.kv("Controls", "Risk control measures implemented")
    pdf.kv("Residual Risk", "Remaining risk after controls")
    pdf.kv("Mitigation Status", "Not Started, In Progress, Complete")

    pdf.tip_box("Red risks trigger alerts in the FDA Comms panel and should be addressed before 510(k) submission.")

    # ── 8. Audit Trail ──
    pdf.add_page()
    pdf.sec(8, "Audit Trail")
    pdf.txt(
        "Every change made in the dashboard is recorded in the Audit Trail with a "
        "timestamp, user role, action type, field changed, old value, new value, and "
        "detail description. This supports 21 CFR Part 11 traceability requirements."
    )
    pdf.sub("Supabase Sync")
    pdf.txt(
        "Audit entries are automatically synced to the Supabase backend. If you are "
        "offline, entries queue locally and flush when connectivity is restored."
    )
    pdf.sub("Filtering")
    pdf.txt(
        "The audit trail supports filtering by action type and searching by keyword. "
        "Recent entries appear first. Export functionality allows downloading the "
        "complete audit history."
    )

    # ── 9. Document Control ──
    pdf.add_page()
    pdf.sec(9, "Document Control")
    pdf.txt(
        "Document Control provides ISO 13485-aligned document lifecycle management. "
        "Documents are tracked locally in the browser to protect intellectual property, "
        "with server sync available for approved/effective documents."
    )
    pdf.sub("Document Lifecycle")
    pdf.bul("Draft: Initial document creation")
    pdf.bul("In Review: Under stakeholder review")
    pdf.bul("Approved: Formally approved by designated authority")
    pdf.bul("Effective: Active and controlling (effective date set automatically)")
    pdf.bul("Obsolete: Superseded or withdrawn")
    pdf.txt(
        "Click the status badge to cycle through the lifecycle. Only PMP can change "
        "document status."
    )
    pdf.sub("Document Fields")
    pdf.kv("DCN", "Document Control Number (auto-generated, e.g., DCN-REG-001)")
    pdf.kv("Category", "Regulatory, Technical, Business, Legal, Finance, Templates")
    pdf.kv("Version", "Version number with revision history")
    pdf.kv("Owner", "Responsible person or role")
    pdf.kv("Source Ref", "External reference (GitHub commit, SVN revision, etc.)")
    pdf.kv("Linked", "Linked milestone or gate (e.g., R8, T2)")

    pdf.sub("Sync to Server")
    pdf.txt(
        "When documents reach 'Approved' or 'Effective' status, use the 'Sync to Server' "
        "button to upload them to the Supabase dhf_documents table. This creates a "
        "server-side record for regulatory compliance. The FDA Communications tab shows "
        "an alert when approved documents have not been synced."
    )

    pdf.warn_box("Documents are stored in browser localStorage. Clear browser data = lose documents. Sync critical documents to the server.")

    # ── 10. Actions ──
    pdf.add_page()
    pdf.sec(10, "Actions")
    pdf.txt(
        "The Actions tab tracks action items arising from gate reviews, risk mitigation, "
        "and general project management. Each action has an assignee, priority, due date, "
        "and linked gate."
    )
    pdf.sub("Action Fields")
    pdf.kv("Assignee", "Team member responsible")
    pdf.kv("Priority", "High, Medium, Low")
    pdf.kv("Status", "Todo, In Progress, Done, Blocked")
    pdf.kv("Due Date", "Target completion date")
    pdf.kv("Linked Gate", "Associated gate review (e.g., G1, G2)")

    pdf.sub("DHF Document Tracker")
    pdf.txt(
        "The Design History File (DHF) Document Tracker appears within the Actions tab. "
        "It tracks all design-phase documents required by 21 CFR 820.30. Click a document's "
        "status badge to cycle through: Not Started \u2192 Draft \u2192 In Review \u2192 Approved."
    )

    pdf.sub("DMR Document Tracker")
    pdf.txt(
        "The Device Master Record (DMR) Document Tracker is also within the Actions tab, "
        "below the DHF tracker. It tracks 12 documents required by 21 CFR 820.181 covering "
        "device specifications, production processes, quality procedures, and packaging/labeling. "
        "Status cycling works identically to the DHF tracker."
    )
    pdf.txt(
        "DMR documents become critical at Gate 4 (Manufacturing Scale-Up / Design Transfer). "
        "Gate 4 criteria include \u2018Manufacturing scaled\u2014production ready.\u2019"
    )

    pdf.sub("CAPA Log")
    pdf.txt(
        "The Corrective and Preventive Action (CAPA) Log is also within the Actions tab. "
        "It tracks CAPA items with type (Corrective or Preventive), status, owner, and linked gate."
    )

    # ── 11. Timeline ──
    pdf.add_page()
    pdf.sec(11, "Timeline")
    pdf.txt(
        "The Timeline provides a month-by-month view of project events. Each entry "
        "shows technical and business activities with an impact indicator "
        "(positive/neutral/negative). Timeline events are auto-generated during wizard "
        "setup and can be edited."
    )

    # ── 12. Budget ──
    pdf.sec(12, "Budget")
    pdf.txt(
        "The Budget tab tracks spending against planned budgets by category. Categories "
        "are defined during wizard setup (or from template budget lines). Each category "
        "shows planned amount, actual spend, and variance."
    )
    pdf.sub("Budget Management")
    pdf.bul("Add, edit, or delete budget categories")
    pdf.bul("Update actual spend values to track variance")
    pdf.bul("Currency display toggles between USD and CNY")
    pdf.bul("All changes logged in Audit Trail")

    # ── 13. Cash / Runway ──
    pdf.add_page()
    pdf.sec(13, "Cash / Runway")
    pdf.txt(
        "Cash/Runway provides financial health visibility: current cash position, "
        "monthly burn rate, and projected runway in months. It includes funding round "
        "tracking and burn history charts."
    )
    pdf.sub("Key Metrics")
    pdf.kv("Cash on Hand", "Current available cash balance")
    pdf.kv("Monthly Burn", "Average monthly expenditure rate")
    pdf.kv("Runway", "Months of operation at current burn rate")
    pdf.sub("Funding Rounds")
    pdf.txt(
        "Track funding rounds with status (Planned, In Progress, Received). "
        "Each round records amount, date, and funding source."
    )

    # ── 14. US Investment ──
    pdf.add_page()
    pdf.sec(14, "US Investment")
    pdf.txt(
        "The US Investment tab manages investor relations for medical device ventures "
        "seeking US market entry. It includes target investor tracking and IR activity "
        "logging."
    )
    pdf.sub("Target Investors")
    pdf.kv("Type", "VC, Angel Group, Strategic, PE, Government")
    pdf.kv("Stage", "Seed, Series A, Series B, Growth")
    pdf.kv("Contact Status", "Prospect, Contacted, In Discussions, Term Sheet, Committed")

    pdf.sub("IR Activities")
    pdf.txt(
        "Log investor relations activities: meetings, presentations, due diligence "
        "sessions, term sheet negotiations. Each activity has a date, type, and status."
    )

    # ── 15. Cap Table ──
    pdf.add_page()
    pdf.sec(15, "Cap Table")
    pdf.txt(
        "The Cap Table tracks equity ownership, equity events (rounds, conversions, "
        "option grants), and vesting schedules. It provides a complete capitalization "
        "overview for the entity."
    )
    pdf.sub("Shareholders")
    pdf.bul("Name, share class (Common, Preferred A/B/C, Options, Warrants)")
    pdf.bul("Share count and ownership percentage")
    pdf.bul("Board seat, vesting status, and notes")

    pdf.sub("Equity Events")
    pdf.bul("Track funding rounds, stock splits, option grants, conversions")
    pdf.bul("Each event records shares issued, price per share, and total raised")

    pdf.sub("Vesting Schedules")
    pdf.bul("Standard 4-year vest with 1-year cliff, or custom schedules")
    pdf.bul("Track cliff date, total shares, vested shares, and next vest date")

    # ── 16. Resources ──
    pdf.add_page()
    pdf.sec(16, "Resources")
    pdf.txt(
        "The Resources tab displays team members with their role, allocation across "
        "workstreams, and utilization percentage. Allocation bars show how each team "
        "member's capacity is distributed."
    )
    pdf.sub("Managing Team Members")
    pdf.bul("Add team members with name, role, email, and workstream allocation")
    pdf.bul("Click allocation percentages to edit them inline (PMP/Tech/Business roles)")
    pdf.bul("Utilization gauge: Green (<85%), Yellow (85-100%), Red (>100% over-allocated)")
    pdf.bul("Delete team members via the X button on each card")

    pdf.sub("Workstream Allocation")
    pdf.txt(
        "Each team member can be allocated across multiple workstreams. Percentages "
        "are editable inline — click the % value, type a new number, press Enter. "
        "The utilization gauge updates automatically. Changes are audit-logged."
    )

    pdf.tip_box("Keep total allocation at or below 100% to avoid burnout. The dashboard flags over-allocation in red.")

    # ── 17. Suppliers ──
    pdf.add_page()
    pdf.sec(17, "Suppliers")
    pdf.txt(
        "The Suppliers tab tracks supplier qualification status, lead times, "
        "purchase order status, and contract manufacturing milestones. This supports "
        "21 CFR 820 supplier controls."
    )
    pdf.sub("Supplier Status")
    pdf.bul("Under Review: Initial evaluation")
    pdf.bul("Qualified: Approved for use")
    pdf.bul("Active: Currently supplying")
    pdf.bul("On Hold: Temporarily suspended")
    pdf.bul("Rejected: Failed qualification")

    # ── 18. Message Board ──
    pdf.add_page()
    pdf.sec(18, "Message Board")
    pdf.txt(
        "The Message Board is a purpose-driven messaging system for cross-functional "
        "communication. It supports threaded discussions with lifecycle management, "
        "decisions tracking, and action item creation."
    )
    pdf.sub("Threads")
    pdf.txt(
        "Create threads with a title, workstream assignment, priority level, and "
        "intent (Discuss, Decide, Inform, Escalate). Threads flow through an "
        "Open -> Resolved lifecycle."
    )
    pdf.sub("Posting Messages")
    pdf.txt(
        "Select your posting role (PMP, Technology, Business, Accounting) from the "
        "role picker toolbar. Type your message and press Send. Use [DECISION] or "
        "[ACTION] prefixes to tag messages with special intent."
    )
    pdf.sub("Settings")
    pdf.txt(
        "Click the Settings gear icon to configure email addresses for each role "
        "(PMP, Technology, Business, Accounting). Toggle Test Mode for development. "
        "Click Settings again to close the panel."
    )
    pdf.sub("Views & Filters")
    pdf.bul("All Threads: Complete thread list")
    pdf.bul("My Items: Threads where you are owner or assignee")
    pdf.bul("Decisions: Threads with active decisions")
    pdf.bul("Executive: High-priority and decision threads")
    pdf.bul("Workstream filter: Filter by workstream category")
    pdf.bul("Lifecycle filter: Open, Resolved, or All")

    # ── 19. FDA Communications ──
    pdf.add_page()
    pdf.sec(19, "FDA Communications Center")
    pdf.txt(
        "The FDA Comms tab is PMP-only and provides tools for FDA regulatory "
        "interactions. It includes a Q-Sub cover letter generator, RTA checklist, "
        "SE decision flow, and MDUFA timeline tracking."
    )

    pdf.sub("Q-Sub Cover Letter Generator")
    pdf.txt(
        "Auto-generates a Pre-Submission meeting request letter using your project "
        "data (applicant name, device description, submission type). Export as HTML "
        "for final formatting."
    )

    pdf.sub("Refuse-to-Accept (RTA) Checklist")
    pdf.txt(
        "Self-check against FDA's 17-item RTA checklist. Items auto-populate from "
        "your DHF documents and standards compliance data. The progress bar shows "
        "overall readiness percentage."
    )

    pdf.sub("Document Sync Alert")
    pdf.txt(
        "When approved or effective documents in Document Control have not been "
        "synced to the server, an amber alert banner appears at the top of FDA Comms. "
        "Click 'Go to Document Control' to navigate directly and sync."
    )

    pdf.sub("MDUFA Review Timeline")
    pdf.txt(
        "Tracks the 510(k) MDUFA review milestones: submission received, K-number "
        "assignment (Day 7), RTA screening (Day 15), substantive review (Day 60), "
        "and MDUFA decision goal (Day 90)."
    )

    pdf.sub("SE Decision Flowchart")
    pdf.txt(
        "Visual representation of FDA's Substantial Equivalence decision flow: "
        "predicate identification, intended use comparison, technological "
        "characteristics analysis, and safety/effectiveness evaluation."
    )

    # ── 20. Setup Wizard ──
    pdf.add_page()
    pdf.sec(20, "Setup Wizard & Templates")
    pdf.txt(
        "The Setup Wizard launches on first visit (or when no project data exists). "
        "It guides you through a 3-phase setup process."
    )
    pdf.sub("Phase 1: Language Selection")
    pdf.txt("Choose English or Chinese for the wizard and dashboard interface.")

    pdf.sub("Phase 2: Device Template")
    pdf.txt("Select from 7 pre-configured device templates or start from scratch:")
    pdf.bul("Respiratory Devices (ventilators, CPAP, nebulizers)")
    pdf.bul("Cardiovascular (stents, pacemakers, monitors)")
    pdf.bul("Orthopedic (implants, instruments, fixation)")
    pdf.bul("IVD (in-vitro diagnostics, assays, analyzers)")
    pdf.bul("Imaging (X-ray, ultrasound, MRI accessories)")
    pdf.bul("Rehabilitation (therapy devices, mobility aids)")
    pdf.bul("SaMD (Software as a Medical Device)")
    pdf.txt(
        "Templates pre-populate: submission type, device class, product codes, "
        "regulation section, predicate examples, tech areas, budget categories, "
        "standards, and template-specific risks."
    )

    pdf.sub("Phase 3: Project Details (8 Steps)")
    pdf.bul("Step 1: Project name and subtitle")
    pdf.bul("Step 2: Regulatory details (submission type, device class, predicate devices)")
    pdf.bul("Step 3: Applicant and manufacturer information")
    pdf.bul("Step 4: Team members with roles and workstream allocation")
    pdf.bul("Step 5: Budget categories and amounts")
    pdf.bul("Step 6: Cash on hand and project duration")
    pdf.bul("Step 7: Suppliers and components")
    pdf.bul("Step 8: DHF document selection")

    # ── 21. Shortcuts & Tips ──
    pdf.add_page()
    pdf.sec(21, "Keyboard Shortcuts & Tips")
    pdf.sub("General Tips")
    pdf.bul("All data saves automatically to browser localStorage -- including full dashboard state (milestones, gates, risks, budget, investors, etc.)")
    pdf.bul("Dashboard state survives browser crashes and power outages -- data reloads automatically on next visit")
    pdf.bul("Supabase sync happens in real-time when online")
    pdf.bul("Offline changes queue and sync when connection is restored")
    pdf.bul("Currency display toggles between USD and CNY based on language setting")
    pdf.bul("The floating action button (bottom-right) provides quick actions")

    pdf.sub("URL Parameters")
    pdf.kv("?test=respiratory", "Load test data for the respiratory template")
    pdf.kv("?test=cardiovascular", "Load test data for the cardiovascular template")
    pdf.txt(
        "Use ?test=<templateId> to load pre-built test data for any of the 7 templates. "
        "This bypasses the wizard and loads a complete project dataset."
    )

    pdf.sub("Data Persistence")
    pdf.bul("Project configuration: ctower_project_data (localStorage)")
    pdf.bul("Live dashboard state: ctower_live_state (localStorage) -- milestones, gates, risks, standards, budget, cash/runway, action items, DHF, DMR, CAPA, team, suppliers, investors, cap table, audit log")
    pdf.bul("Message Board threads: ctower_mb_threads (localStorage)")
    pdf.bul("Documents: ctower_doclib_docs (localStorage)")
    pdf.bul("Messages: Supabase messages table (synced)")
    pdf.bul("Audit log: Supabase audit_log table (synced)")
    pdf.tip_box("All dashboard state is automatically saved to localStorage after every change. If power is lost or the browser crashes, your data is preserved and will reload on next visit.")

    # ── 22. Troubleshooting ──
    pdf.add_page()
    pdf.sec(22, "Troubleshooting")

    pdf.sub("Dashboard won't load")
    pdf.bul("Check internet connection for initial Supabase authentication")
    pdf.bul("Clear browser cache and reload")
    pdf.bul("Verify the deployment URL is correct")

    pdf.sub("Tabs are grayed out")
    pdf.txt(
        "Tab access is controlled by your subscription tier. Grayed-out tabs with "
        "strikethrough text indicate they are not included in your tier. Contact your "
        "administrator to upgrade."
    )

    pdf.sub("Messages not syncing")
    pdf.bul("Verify internet connectivity (green indicator)")
    pdf.bul("Check browser console for Supabase errors")
    pdf.bul("Messages sync automatically when connection is restored")

    pdf.sub("Settings panel not visible")
    pdf.txt(
        "On the Message Board, click the Settings gear icon. The panel appears above "
        "the thread list and scrolls into view. Click Settings again to close."
    )

    pdf.sub("Stale demo data")
    pdf.txt(
        "If you see data from a previous project, the wizard's 'Load Demo Data' "
        "will clear all existing data and generate fresh sample data from the "
        "respiratory device template."
    )

    pdf.sub("Resetting the Dashboard")
    pdf.txt(
        "To completely reset, clear the following localStorage keys: "
        "ctower_project_data, ctower_live_state, ctower_mb_threads, ctower_mb_decisions, "
        "ctower_doclib_docs, ctower_qa_messages, ctower_qa_settings, "
        "ctower_qa_archive. Or clear all site data in browser settings."
    )

    # ── 23. 510(k) Predicate Finder ──
    pdf.add_page()
    pdf.sec(23, "510(k) Predicate Finder")
    pdf.txt(
        "The 510(k) Predicate Finder is a companion SaaS tool that connects to the "
        "FDA openFDA database. It helps PMPs and regulatory teams identify predicate "
        "devices, trace predicate chains, and draft Substantial Equivalence arguments "
        "-- tasks that are critical to planning a 510(k) submission.")

    pdf.sub("Free vs Pro")
    pdf.txt(
        "The Predicate Finder is available free with daily limits (5 searches, "
        "1 chain trace, 2-device comparison). Pro ($99/month) unlocks unlimited "
        "searches, unlimited chain tracing, 4-device comparison, SE argument "
        "generation, and PDF export.")
    pdf.tip_box(
        "The Predicate Finder is the primary lead-generation tool for 510k Bridge. "
        "Free users provide their email to unlock the tool, creating a "
        "natural upgrade funnel to Control Tower subscriptions.")

    pdf.sub("Integration with Control Tower (Scale Tier)")
    pdf.txt(
        "On the Scale tier ($2,000/mo), the Predicate Finder is embedded directly "
        "in the Control Tower dashboard. Predicate research informs:"
    )
    pdf.bul("Regulatory Tracker -- predicate device references and SE strategy")
    pdf.bul("Risk Dashboard -- risks identified during predicate comparison")
    pdf.bul("FDA Communications Center -- Pre-Sub discussion points based on predicate analysis")
    pdf.bul("Document Control -- predicate comparison reports as DHF artifacts")

    pdf.sub("PMP Workflow")
    pdf.txt(
        "1. Use Predicate Finder to search for candidate predicate devices by product "
        "code or keyword.\n"
        "2. Trace the predicate chain to understand the regulatory lineage.\n"
        "3. Compare up to 4 devices side-by-side (Pro) to select the strongest predicate.\n"
        "4. Generate a draft SE argument (Pro) as a starting point for the regulatory team.\n"
        "5. Export results to PDF and attach to the 510(k) submission package in Document Control.")

    # ── 24. Glossary of FDA & Regulatory Terms ──
    pdf.add_page()
    pdf.sec(24, "Glossary of FDA & Regulatory Terms")
    pdf.ln(2)
    fda_terms = [
        ("510(k)", "Premarket Notification submitted to FDA to demonstrate a Class II device is substantially equivalent to a legally marketed predicate device. Named after Section 510(k) of the Food, Drug, and Cosmetic Act."),
        ("PMA", "Premarket Approval. The most stringent FDA pathway, required for Class III devices that cannot demonstrate substantial equivalence. Requires clinical data."),
        ("De Novo", "FDA classification pathway for novel low-to-moderate risk devices with no predicate. Creates a new regulatory classification if granted."),
        ("Substantial Equivalence (SE)", "The legal standard for 510(k) clearance. The new device must have the same intended use and similar technological characteristics as the predicate, or different characteristics that do not raise new safety/effectiveness questions."),
        ("Predicate Device", "A legally marketed device (cleared via 510(k) or pre-Amendments) used as the comparison basis for a new 510(k) submission."),
        ("Product Code", "FDA's alphanumeric classification code for device types (e.g., IKN for sEMG respiratory monitors, DQS for EIT thoracic imagers, BZG for spirometers)."),
        ("Regulation Number", "The CFR citation defining a device classification (e.g., 21 CFR 882.1400 for EEG devices, 21 CFR 890.1850 for powered exercise equipment)."),
        ("Class I / II / III", "FDA risk-based device classifications. Class I = lowest risk (general controls). Class II = moderate risk (special controls + 510(k)). Class III = highest risk (PMA required)."),
        ("General Controls", "Baseline FDA requirements for all devices: registration, listing, labeling, GMP, premarket notification, and adverse event reporting."),
        ("Special Controls", "Additional FDA requirements for Class II devices beyond general controls: guidance documents, performance standards, postmarket surveillance, or patient registries."),
        ("Pre-Submission (Pre-Sub)", "A formal FDA meeting request (formerly Q-Sub) to discuss regulatory strategy, testing plans, or clinical study design before filing a 510(k) or PMA."),
        ("Q-Submission (Q-Sub)", "Legacy term for Pre-Submission. The formal process for requesting a Pre-Sub meeting with FDA's review division."),
        ("DICE", "Division of Industry and Consumer Education. FDA division that handles Pre-Sub logistics, meeting scheduling, and general submission inquiries."),
        ("RTA", "Refuse to Accept. FDA's initial administrative screening of a 510(k) submission against a checklist. Failure triggers immediate rejection before substantive review begins."),
        ("SE Report", "Substantial Equivalence determination report. FDA's decision document that either clears (SESE) or denies (NSE) a 510(k)."),
        ("SESE", "Substantially Equivalent -- the positive outcome of a 510(k) review, resulting in clearance to market."),
        ("NSE", "Not Substantially Equivalent -- negative 510(k) determination. Device cannot be marketed under 510(k); applicant may pursue De Novo or PMA."),
        ("21 CFR Part 820", "Quality System Regulation (QSR). FDA's current Good Manufacturing Practice (cGMP) requirements for medical devices. Being revised to align with ISO 13485."),
        ("ISO 13485", "International standard for medical device quality management systems. Widely accepted globally and increasingly harmonized with FDA QSR."),
        ("ISO 14971", "International standard for medical device risk management. Defines the process for hazard identification, risk estimation, risk evaluation, and risk control."),
        ("IEC 60601-1", "International standard for basic safety and essential performance of medical electrical equipment. The foundation standard for most powered medical devices."),
        ("IEC 62304", "International standard for medical device software lifecycle processes. Defines software safety classes (A, B, C) and development requirements."),
        ("IEC 62366", "International standard for usability engineering of medical devices. Requires formative and summative usability testing."),
        ("DHF", "Design History File. The complete collection of records documenting the design and development of a medical device, as required by 21 CFR 820.30."),
        ("DMR", "Device Master Record. Documentation specifying the finished device, including device specifications, production processes, quality assurance procedures, and packaging/labeling specifications."),
        ("DHR", "Device History Record. Production records for each unit or batch, demonstrating the device was manufactured according to the DMR."),
        ("CAPA", "Corrective and Preventive Action. A systematic process required by 21 CFR 820.90 for investigating nonconformities, identifying root causes, and implementing corrective/preventive measures."),
        ("Design Controls", "21 CFR 820.30 requirements for the design process: design planning, input, output, review, verification, validation, transfer, and changes."),
        ("V&V", "Verification and Validation. Verification confirms design outputs meet design inputs (built right). Validation confirms the device meets user needs and intended use (built the right thing)."),
        ("Biocompatibility", "Assessment of biological safety per ISO 10993. Required for any device with direct or indirect patient contact. Testing includes cytotoxicity, sensitization, irritation, and more based on contact type and duration."),
        ("EMC", "Electromagnetic Compatibility. Testing per IEC 60601-1-2 to ensure a device neither emits harmful interference nor is susceptible to external electromagnetic fields."),
        ("UDI", "Unique Device Identification. FDA-mandated system requiring a unique identifier on device labels and packages for tracking, recalls, and adverse event reporting."),
        ("MDR / eMDR", "Medical Device Report / Electronic MDR. Mandatory adverse event reporting to FDA when a device may have caused or contributed to a death or serious injury."),
        ("510(k) Summary", "A publicly available summary of the 510(k) submission describing the device, predicate comparison, and basis for substantial equivalence."),
        ("Indications for Use", "The specific clinical conditions, patient populations, and purposes for which the device is intended. Must match or be a subset of the predicate's indications."),
        ("Labeling", "All written, printed, or graphic material on or accompanying a device, including instructions for use (IFU), package inserts, and promotional materials."),
        ("GMP", "Good Manufacturing Practice. FDA's manufacturing quality requirements codified in 21 CFR Part 820 (QSR)."),
        ("FDA Establishment Registration", "Annual registration required for all facilities involved in the production and distribution of medical devices marketed in the US."),
        ("FDA Device Listing", "Requirement to list each device being commercially distributed with FDA, including product codes and proprietary names."),
        ("US Agent", "Required for foreign device manufacturers. A person residing in the US designated as FDA's point of contact for the foreign establishment."),
        ("510(k) Holder", "The legal entity (typically a US LLC or corporation) that owns the 510(k) clearance. Foreign companies often establish a US subsidiary for this purpose."),
        ("eSTAR", "Electronic Submission Template and Resource. FDA's standardized electronic submission format for 510(k) applications, replacing the former paper/eCopy process."),
        ("MDSAP", "Medical Device Single Audit Program. A program allowing a single regulatory audit to satisfy requirements of multiple participating countries (US, Canada, Australia, Brazil, Japan)."),
        ("PAC", "Premarket Assessment Committee. Internal FDA committee that reviews complex 510(k) submissions requiring multi-disciplinary expertise."),
        ("sEMG", "Surface Electromyography. Non-invasive measurement of muscle electrical activity. In respiratory monitoring, measures neural respiratory drive from intercostal and diaphragm muscles."),
        ("EIT", "Electrical Impedance Tomography. Non-invasive imaging technique that creates cross-sectional images of tissue conductivity. Used for real-time lung ventilation monitoring."),
        ("V/Q Ratio", "Ventilation/Perfusion ratio. The relationship between air reaching the alveoli and blood reaching the alveoli. A key indicator of gas exchange efficiency."),
        ("FES", "Functional Electrical Stimulation. Therapeutic application of electrical current to activate paralyzed or weakened muscles for functional movement."),
        ("NRE", "Non-Recurring Engineering. One-time engineering costs for product development, tooling, and manufacturing setup that are not repeated for each unit produced."),
        ("openFDA", "FDA's public API providing searchable access to 510(k) clearance records, adverse events, recalls, and other regulatory data."),
        ("Predicate Finder", "510k Bridge's SaaS tool for searching, comparing, and tracing predicate devices using the openFDA database. Free and Pro tiers available."),
        ("Predicate Chain", "The lineage of predicate references connecting a cleared device back through prior generations of 510(k) clearances."),
    ]
    for k, v in fda_terms:
        pdf.kv(k, v)
        pdf.ln(1)

    out = os.path.join(OUT_DIR, "PMP_Users_Guide_EN.pdf")
    pdf.output(out)
    return out


def build_chinese():
    pdf = CNGuide()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)

    # ── Cover ──
    pdf.add_page()
    pdf.ln(50)
    pdf.set_font("CJK", "B", 28)
    pdf.set_text_color(*NAVY)
    pdf.cell(0, 14, _a("Control Tower"), align="C", ln=True)
    pdf.set_font("CJK", "", 18)
    pdf.set_text_color(*ACCENT)
    pdf.cell(0, 10, _a("PM 仪表板"), align="C", ln=True)
    pdf.ln(8)
    pdf.set_font("CJK", "B", 22)
    pdf.set_text_color(*DARK)
    pdf.cell(0, 12, _a("PMP 用户指南"), align="C", ln=True)
    pdf.ln(20)
    pdf.set_font("CJK", "", 11)
    pdf.set_text_color(*GRAY)
    pdf.cell(0, 7, _a("医疗器械开发项目管理"), align="C", ln=True)
    pdf.cell(0, 7, _a("FDA 510(k) 监管路径"), align="C", ln=True)
    pdf.ln(30)
    pdf.set_font("CJK", "", 10)
    pdf.cell(0, 6, _a("510k Bridge"), align="C", ln=True)
    pdf.cell(0, 6, _a("版本 1.0 -- 2026年3月"), align="C", ln=True)

    # ── Table of Contents ──
    pdf.add_page()
    pdf.set_font("CJK", "B", 16)
    pdf.set_text_color(*NAVY)
    pdf.cell(0, 10, _a("目录"), ln=True)
    pdf.ln(5)
    toc = [
        ("1", "快速入门"),
        ("2", "仪表板概览"),
        ("3", "角色权限与订阅层级"),
        ("4", "双轨里程碑"),
        ("5", "门控系统"),
        ("6", "监管追踪器"),
        ("7", "风险仪表板"),
        ("8", "审计跟踪"),
        ("9", "文档控制"),
        ("10", "行动项"),
        ("11", "时间线"),
        ("12", "预算"),
        ("13", "现金/续航"),
        ("14", "美国投资"),
        ("15", "股权结构表"),
        ("16", "资源"),
        ("17", "供应商"),
        ("18", "消息板"),
        ("19", "FDA通信中心"),
        ("20", "设置向导与模板"),
        ("21", "快捷操作与技巧"),
        ("22", "故障排除"),
        ("23", "FDA与法规术语表"),
    ]
    pdf.set_font("CJK", "", 11)
    for num, title in toc:
        pdf.set_text_color(*DARK)
        pdf.cell(12, 7, _a(num + "."))
        pdf.set_text_color(*TEXT)
        pdf.cell(0, 7, _a(title), ln=True)

    # ── 1. 快速入门 ──
    pdf.add_page()
    pdf.sec(1, "快速入门")
    pdf.txt(
        "Control Tower PM 仪表板是一个专为 FDA 510(k) 医疗器械开发设计的综合项目管理平台。"
        "它提供监管、技术和商务工作流的实时可视化。"
    )
    pdf.sub("系统要求")
    pdf.bul("现代网页浏览器 (Chrome, Firefox, Safari, Edge)")
    pdf.bul("需要互联网连接以同步 Supabase（支持离线模式）")
    pdf.bul("建议屏幕分辨率 1280x720 或更高")

    pdf.sub("首次启动")
    pdf.txt(
        "首次打开仪表板时，设置向导将引导您完成项目配置。您可以从7个设备模板中选择"
        "（呼吸设备、心血管、骨科、IVD、影像、康复、SaMD），也可以从零开始。"
        "或者，点击'加载演示数据'以使用示例数据进行探索。"
    )

    pdf.sub("登录与认证")
    pdf.txt(
        "仪表板使用基于角色的登录。输入项目管理员提供的密码。认证后，您将看到与"
        "您的角色和订阅层级对应的标签页。"
    )

    pdf.tip_box("收藏仪表板URL以便快速访问。您的项目数据会自动保存。")

    # ── 2. 仪表板概览 ──
    pdf.add_page()
    pdf.sec(2, "仪表板概览")
    pdf.txt(
        "仪表板由顶部导航栏（角色/层级选择器）、16个功能标签页的水平导航栏和"
        "主内容区组成。每个标签页专注于510(k)项目生命周期的特定方面。"
    )

    pdf.sub("顶部导航栏")
    pdf.bul("项目名称和副标题（双语 英文/中文）")
    pdf.bul("角色选择器: 在PMP、技术、商务和会计视图之间切换")
    pdf.bul("层级指示器: 显示当前订阅层级 (Starter/Growth/Scale)")
    pdf.bul("语言切换: 在英文和中文界面之间切换")

    pdf.sub("16个标签页")
    tabs_cn = [
        ("双轨", "技术和监管里程碑跟踪"),
        ("门控系统", "阶段门控审查与标准清单"),
        ("监管追踪器", "标准合规性和进度监控"),
        ("风险仪表板", "ISO 14971 风险矩阵（严重性/概率）"),
        ("审计跟踪", "所有仪表板变更的时间戳记录"),
        ("文档控制", "ISO 13485 对齐的文档生命周期管理"),
        ("行动项", "任务看板、DHF文档追踪、DMR文档追踪和CAPA日志"),
        ("时间线", "按月查看的项目时间线"),
        ("预算", "预算类别的计划与实际对比"),
        ("现金/续航", "现金状况、消耗率和续航预测"),
        ("美国投资", "投资者管道和IR活动跟踪"),
        ("股权结构表", "股东名册、股权事件、归属计划"),
        ("资源", "团队分配和利用率监控"),
        ("供应商", "供应商资质和交期跟踪"),
        ("消息板", "线程讨论、决策和行动跟踪"),
        ("FDA通信", "Q-Sub生成器、RTA清单和监管时间线（仅PMP）"),
    ]
    for name, desc in tabs_cn:
        pdf.kv(name, desc)

    pdf.warn_box("某些标签页可能因您的角色或订阅层级而受限。")

    # ── 3. 角色与层级 ──
    pdf.add_page()
    pdf.sec(3, "角色权限与订阅层级")

    pdf.sub("用户角色")
    pdf.txt("仪表板支持四种主要角色，每种角色具有不同的访问级别:")
    pdf.kv("PMP（项目经理）", "完全访问所有标签页。可编辑里程碑、门控、风险、预算、文档和团队。唯一可查看FDA通信的角色。")
    pdf.kv("技术", "可查看和更新技术里程碑、风险和文档。可参与消息板。无法访问财务标签页。")
    pdf.kv("商务", "可访问商务里程碑、预算、投资和股权结构表。可参与消息板。")
    pdf.kv("会计", "预算、现金/续航和股权结构表的只读访问。编辑能力有限。")

    pdf.sub("订阅层级")
    pdf.txt("标签页访问由 Supabase RLS 在服务器端控制。层级决定可用的标签页:")
    pdf.kv("Starter ($500/月)", "2个席位，4个标签页: 双轨、门控、时间线、预算")
    pdf.kv("Growth ($1,000/月)", "5个席位，13个标签页: 除股权表、FDA通信和美国投资外全部")
    pdf.kv("Scale ($2,000/月)", "10个席位，全部16个标签页，包括FDA通信和股权表")

    pdf.tip_box("您的层级由服务器端管理，无法从仪表板UI更改。")

    # ── 4. 双轨里程碑 ──
    pdf.add_page()
    pdf.sec(4, "双轨里程碑")
    pdf.txt(
        "双轨标签页显示并行的监管和技术里程碑轨道。这反映了FDA 510(k)流程中"
        "工程开发和监管准备同时进行的实际情况。"
    )
    pdf.sub("技术里程碑")
    pdf.txt(
        "技术里程碑跟踪工程交付物: 设计冻结、原型测试、验证与确认活动以及设计转移。"
        "每个里程碑显示其月份、状态、负责人和类别。"
    )
    pdf.sub("监管里程碑")
    pdf.txt(
        "监管里程碑跟踪FDA交付物: Pre-Submission会议、510(k)准备和提交申请。"
        "这些根据您的项目持续时间自动生成。"
    )
    pdf.sub("编辑里程碑")
    pdf.txt(
        "点击里程碑状态徽章可在以下状态间循环: 未开始、进行中、完成、受阻。"
        "只有PMP和负责角色可以更改状态。所有更改都记录在审计跟踪中。"
    )

    # ── 5. 门控系统 ──
    pdf.add_page()
    pdf.sec(5, "门控系统")
    pdf.txt(
        "门控系统实现阶段门控审查流程。门控根据项目持续时间自动生成（2-6个门控）。"
        "每个门控都有必须满足的标准才能继续项目。"
    )
    pdf.sub("门控标准")
    pdf.txt(
        "每个门控都有标准清单（如'技术交付物完成'、'预算正常'、'风险缓解已确认'）。"
        "逐项点击标准进行检查。门控状态根据标准完成情况更新。"
    )
    pdf.sub("门控决策")
    pdf.txt(
        "PMP可以记录门控决策: 通过、不通过或有条件通过。决策带有时间戳和归属。"
        "门控备注可记录讨论要点和有条件批准的条件。"
    )

    # ── 6. 监管追踪器 ──
    pdf.add_page()
    pdf.sec(6, "监管追踪器")
    pdf.txt(
        "监管追踪器监控适用标准的合规性。标准根据您的设备模板预填充"
        "（如电气设备的IEC 60601-1、生物相容性的ISO 10993）或手动输入。"
    )
    pdf.sub("跟踪标准")
    pdf.bul("状态: 未开始、进行中、完成")
    pdf.bul("进度条: 0-100% 完成百分比")
    pdf.bul("条款级别跟踪以实现详细合规")
    pdf.txt(
        "点击状态徽章在各状态间循环。更新进度滑块以反映实际完成情况。"
        "FDA通信标签页使用这些值自动填充RTA清单。"
    )

    # ── 7. 风险仪表板 ──
    pdf.add_page()
    pdf.sec(7, "风险仪表板")
    pdf.txt(
        "风险仪表板实现ISO 14971风险管理。风险以颜色编码矩阵显示，"
        "展示严重性、概率和风险级别。模板特定的风险从您的设备类别自动填充。"
    )
    pdf.sub("风险字段")
    pdf.kv("严重性", "危害程度（低/中/高）")
    pdf.kv("概率", "危险情况发生的可能性（低/中/高）")
    pdf.kv("风险级别", "颜色编码: 绿色（可接受）、黄色（ALARP）、红色（不可接受）")
    pdf.kv("控制措施", "已实施的风险控制措施")
    pdf.kv("残余风险", "控制措施后的剩余风险")
    pdf.kv("缓解状态", "未开始、进行中、完成")

    pdf.tip_box("红色风险会在FDA通信面板中触发警报，应在提交510(k)之前解决。")

    # ── 8. 审计跟踪 ──
    pdf.add_page()
    pdf.sec(8, "审计跟踪")
    pdf.txt(
        "仪表板中的每项更改都记录在审计跟踪中，包含时间戳、用户角色、操作类型、"
        "更改的字段、旧值、新值和详细描述。这支持21 CFR Part 11的可追溯性要求。"
    )
    pdf.sub("Supabase 同步")
    pdf.txt(
        "审计条目自动同步到Supabase后端。如果您处于离线状态，条目在本地排队，"
        "并在恢复连接时刷新。"
    )

    # ── 9. 文档控制 ──
    pdf.add_page()
    pdf.sec(9, "文档控制")
    pdf.txt(
        "文档控制提供ISO 13485对齐的文档生命周期管理。文档在浏览器中本地跟踪以保护知识产权，"
        "已批准/生效的文档可同步至服务器。"
    )
    pdf.sub("文档生命周期")
    pdf.bul("草稿: 初始文档创建")
    pdf.bul("审核中: 利益相关者审核中")
    pdf.bul("已批准: 由指定权限正式批准")
    pdf.bul("生效: 活跃且有约束力（生效日期自动设置）")
    pdf.bul("废弃: 被取代或撤回")

    pdf.sub("同步至服务器")
    pdf.txt(
        "当文档达到'已批准'或'生效'状态时，使用'同步至服务器'按钮将其上传到"
        "Supabase dhf_documents表。这为监管合规创建服务器端记录。"
        "当已批准文档未同步时，FDA通信标签页会显示警报。"
    )

    pdf.warn_box("文档存储在浏览器localStorage中。清除浏览器数据=丢失文档。请将关键文档同步到服务器。")

    # ── 10. 行动项 ──
    pdf.add_page()
    pdf.sec(10, "行动项")
    pdf.txt(
        "行动项标签页跟踪来自门控审查、风险缓解和一般项目管理的行动项。"
        "每个行动项有负责人、优先级、截止日期和关联门控。"
    )
    pdf.kv("负责人", "负责的团队成员")
    pdf.kv("优先级", "高、中、低")
    pdf.kv("状态", "待办、进行中、完成、受阻")
    pdf.kv("截止日期", "目标完成日期")

    pdf.sub("DHF文档追踪器")
    pdf.txt(
        "设计历史文件(DHF)文档追踪器位于行动项标签页内。"
        "它追踪所有21 CFR 820.30要求的设计阶段文档。点击文档状态徽章可循环切换："
        "未开始 \u2192 草稿 \u2192 审查中 \u2192 已批准。"
    )

    pdf.sub("DMR文档追踪器")
    pdf.txt(
        "器械主记录(DMR)文档追踪器也位于行动项标签页内，在DHF追踪器下方。"
        "它追踪按版21 CFR 820.181要求的12份文档，涵盖器械规格、"
        "生产工艺、质量程序和包装/标签。状态循环与DHF追踪器相同。"
    )
    pdf.txt(
        "DMR文档在门控4（制造规模化/设计转移）变得至关重要。"
        "门控4标准包括\u2018制造规模化\u2014\u2014生产就绪\u2019。"
    )

    pdf.sub("CAPA日志")
    pdf.txt(
        "纠正和预防措施(CAPA)日志也位于行动项标签页内。"
        "它跟踪CAPA项目的类型（纠正或预防）、状态、负责人和关联门控。"
    )

    # ── 11. 时间线 ──
    pdf.sec(11, "时间线")
    pdf.txt(
        "时间线按月查看项目事件。每个条目显示技术和商务活动，"
        "并带有影响指示器（积极/中性/消极）。"
    )

    # ── 12. 预算 ──
    pdf.add_page()
    pdf.sec(12, "预算")
    pdf.txt(
        "预算标签页按类别跟踪预算与实际支出的对比。类别在向导设置期间定义"
        "（或来自模板预算项）。每个类别显示计划金额、实际支出和差异。"
    )
    pdf.bul("添加、编辑或删除预算类别")
    pdf.bul("更新实际支出值以跟踪差异")
    pdf.bul("货币显示在USD和CNY之间切换")

    # ── 13. 现金/续航 ──
    pdf.sec(13, "现金/续航")
    pdf.txt(
        "现金/续航提供财务健康可视化: 当前现金状况、月消耗率和预计续航月数。"
        "包括融资轮次跟踪和消耗历史图表。"
    )
    pdf.kv("现金余额", "当前可用现金")
    pdf.kv("月消耗率", "平均每月支出")
    pdf.kv("续航", "按当前消耗率可运营的月数")

    # ── 14. 美国投资 ──
    pdf.add_page()
    pdf.sec(14, "美国投资")
    pdf.txt(
        "美国投资标签页管理寻求进入美国市场的医疗器械企业的投资者关系。"
        "包括目标投资者跟踪和IR活动记录。"
    )
    pdf.kv("投资者类型", "VC、天使团体、战略、PE、政府")
    pdf.kv("阶段", "种子轮、A轮、B轮、成长轮")
    pdf.kv("联系状态", "潜在客户、已联系、洽谈中、条款书、已承诺")

    # ── 15. 股权结构表 ──
    pdf.add_page()
    pdf.sec(15, "股权结构表")
    pdf.txt(
        "股权结构表跟踪股权所有权、股权事件（融资轮次、转换、期权授予）"
        "和归属计划。它提供实体的完整资本化概览。"
    )
    pdf.sub("股东")
    pdf.bul("姓名、股份类别（普通股、优先股A/B/C、期权、认股权证）")
    pdf.bul("股份数量和所有权百分比")
    pdf.bul("董事会席位、归属状态和备注")

    pdf.sub("归属计划")
    pdf.bul("标准4年归属，1年悬崖期，或自定义计划")
    pdf.bul("跟踪悬崖日期、总股份、已归属股份和下次归属日期")

    # ── 16. 资源 ──
    pdf.add_page()
    pdf.sec(16, "资源")
    pdf.txt(
        "资源标签页显示团队成员及其角色、跨工作流的分配和利用率百分比。"
        "分配条形图显示每个团队成员的能力如何分配。"
    )
    pdf.sub("管理团队成员")
    pdf.bul("添加团队成员（姓名、角色、邮箱、工作流分配）")
    pdf.bul("点击分配百分比可内联编辑（PMP/技术/商务角色）")
    pdf.bul("利用率指标: 绿色(<85%)、黄色(85-100%)、红色(>100%超额分配)")
    pdf.bul("通过每张卡片上的X按钮删除团队成员")

    pdf.sub("工作流分配")
    pdf.txt(
        "每个团队成员可在多个工作流间分配。百分比支持内联编辑 -- 点击%值，"
        "输入新数字，按Enter确认。利用率指标自动更新。更改记录在审计跟踪中。"
    )

    pdf.tip_box("保持总分配在100%或以下以避免过度负荷。仪表板以红色标记超额分配。")

    # ── 17. 供应商 ──
    pdf.add_page()
    pdf.sec(17, "供应商")
    pdf.txt(
        "供应商标签页跟踪供应商资质状态、交期、采购订单状态和合同制造里程碑。"
        "这支持21 CFR 820供应商控制。"
    )
    pdf.sub("供应商状态")
    pdf.bul("审核中: 初始评估")
    pdf.bul("已资质: 批准使用")
    pdf.bul("活跃: 当前供应中")
    pdf.bul("暂停: 临时中止")
    pdf.bul("拒绝: 资质未通过")

    # ── 18. 消息板 ──
    pdf.add_page()
    pdf.sec(18, "消息板")
    pdf.txt(
        "消息板是一个目的导向的消息系统，用于跨职能沟通。"
        "它支持带有生命周期管理、决策跟踪和行动项创建的线程讨论。"
    )
    pdf.sub("线程")
    pdf.txt(
        "创建线程时需要标题、工作流分配、优先级和意图（讨论、决定、通知、升级）。"
        "线程经历 打开 -> 已解决 的生命周期。"
    )
    pdf.sub("发送消息")
    pdf.txt(
        "从角色选择器工具栏中选择您的发布角色（PMP、技术、商务、会计）。"
        "输入消息并按发送。使用 [DECISION] 或 [ACTION] 前缀标记具有特殊意图的消息。"
    )
    pdf.sub("设置")
    pdf.txt(
        "点击设置齿轮图标配置每个角色的电子邮件地址。切换测试模式用于开发。"
        "再次点击设置关闭面板。"
    )
    pdf.sub("视图与过滤器")
    pdf.bul("所有线程: 完整线程列表")
    pdf.bul("我的项目: 您是所有者或被分配者的线程")
    pdf.bul("决策: 具有活跃决策的线程")
    pdf.bul("高管: 高优先级和决策线程")
    pdf.bul("工作流过滤器: 按工作流类别过滤")
    pdf.bul("生命周期过滤器: 打开、已解决或全部")

    # ── 19. FDA通信中心 ──
    pdf.add_page()
    pdf.sec(19, "FDA通信中心")
    pdf.txt(
        "FDA通信标签页仅限PMP访问，提供FDA监管互动工具。"
        "包括Q-Sub附信生成器、RTA清单、SE决策流程和MDUFA时间线跟踪。"
    )

    pdf.sub("Q-Sub附信生成器")
    pdf.txt(
        "使用您的项目数据（申请人名称、器械描述、提交类型）"
        "自动生成Pre-Submission会议请求信函。导出为HTML进行最终格式化。"
    )

    pdf.sub("拒绝接受 (RTA) 清单")
    pdf.txt(
        "对照FDA的17项RTA清单进行自检。项目从您的DHF文档和标准合规数据自动填充。"
        "进度条显示总体就绪百分比。"
    )

    pdf.sub("文档同步警报")
    pdf.txt(
        "当文档控制中已批准或生效的文档未同步至服务器时，"
        "FDA通信顶部会显示琥珀色警报横幅。点击'前往文档控制'直接导航并同步。"
    )

    pdf.sub("MDUFA审查时间线")
    pdf.txt(
        "跟踪510(k) MDUFA审查里程碑: 提交接收、K编号分配（第7天）、"
        "RTA筛查（第15天）、实质性审查（第60天）和MDUFA决定目标（第90天）。"
    )

    # ── 20. 设置向导 ──
    pdf.add_page()
    pdf.sec(20, "设置向导与模板")
    pdf.txt(
        "设置向导在首次访问时启动（或当不存在项目数据时）。"
        "它引导您完成3阶段设置过程。"
    )
    pdf.sub("阶段1: 语言选择")
    pdf.txt("为向导和仪表板界面选择英文或中文。")

    pdf.sub("阶段2: 设备模板")
    pdf.txt("从7个预配置的设备模板中选择或从零开始:")
    pdf.bul("呼吸设备（呼吸机、CPAP、雾化器）")
    pdf.bul("心血管（支架、起搏器、监护仪）")
    pdf.bul("骨科（植入物、器械、固定装置）")
    pdf.bul("IVD（体外诊断、分析仪）")
    pdf.bul("影像（X射线、超声、MRI配件）")
    pdf.bul("康复（治疗设备、移动辅助器具）")
    pdf.bul("SaMD（软件作为医疗器械）")
    pdf.txt(
        "模板预填充: 提交类型、器械分类、产品代码、法规章节、"
        "前置器械示例、技术领域、预算类别、标准和模板特定风险。"
    )

    pdf.sub("阶段3: 项目详情（8个步骤）")
    pdf.bul("步骤1: 项目名称和副标题")
    pdf.bul("步骤2: 监管详情（提交类型、器械分类、前置器械）")
    pdf.bul("步骤3: 申请人和制造商信息")
    pdf.bul("步骤4: 团队成员及角色和工作流分配")
    pdf.bul("步骤5: 预算类别和金额")
    pdf.bul("步骤6: 现金余额和项目持续时间")
    pdf.bul("步骤7: 供应商和组件")
    pdf.bul("步骤8: DHF文档选择")

    # ── 21. 快捷操作 ──
    pdf.add_page()
    pdf.sec(21, "快捷操作与技巧")
    pdf.sub("常用技巧")
    pdf.bul("所有数据自动保存到浏览器localStorage，包括全部仪表板状态")
    pdf.bul("在线时Supabase实时同步")
    pdf.bul("离线更改排队，恢复连接后同步")
    pdf.bul("货币显示根据语言设置在USD和CNY之间切换")
    pdf.bul("浮动操作按钮（右下角）提供快捷操作")

    pdf.sub("URL参数")
    pdf.kv("?test=respiratory", "加载呼吸设备模板的测试数据")
    pdf.kv("?test=cardiovascular", "加载心血管模板的测试数据")
    pdf.txt("使用 ?test=<templateId> 加载任何7个模板的预构建测试数据。")

    pdf.sub("数据持久化")
    pdf.bul("项目配置: ctower_project_data (localStorage)")
    pdf.bul("实时仪表板状态: ctower_live_state (localStorage) -- 里程碑、门控、风险、标准、预算、资金/跑道、行动项、DHF、CAPA、团队、供应商、投资者、股权表、审计日志")
    pdf.bul("消息板线程: ctower_mb_threads (localStorage)")
    pdf.bul("文档: ctower_doclib_docs (localStorage)")
    pdf.bul("消息: Supabase messages 表（已同步）")
    pdf.bul("审计日志: Supabase audit_log 表（已同步）")
    pdf.tip_box("所有仪表板状态在每次更改后自动保存到localStorage。如果断电或浏览器崩溃，您的数据将保留并在下次访问时重新加载。")

    # ── 22. 故障排除 ──
    pdf.add_page()
    pdf.sec(22, "故障排除")

    pdf.sub("仪表板无法加载")
    pdf.bul("检查互联网连接以进行初始Supabase认证")
    pdf.bul("清除浏览器缓存并重新加载")
    pdf.bul("验证部署URL是否正确")

    pdf.sub("标签页变灰")
    pdf.txt(
        "标签页访问由您的订阅层级控制。带有删除线文本的灰色标签页表示"
        "未包含在您的层级中。联系管理员进行升级。"
    )

    pdf.sub("消息未同步")
    pdf.bul("验证互联网连接（绿色指示灯）")
    pdf.bul("检查浏览器控制台的Supabase错误")
    pdf.bul("恢复连接后消息自动同步")

    pdf.sub("设置面板不可见")
    pdf.txt(
        "在消息板上，点击设置齿轮图标。面板出现在线程列表上方并滚动到视图中。"
        "再次点击设置关闭。"
    )

    pdf.sub("过时的演示数据")
    pdf.txt(
        "如果您看到以前项目的数据，向导的'加载演示数据'将清除所有现有数据"
        "并从呼吸设备模板生成全新的示例数据。"
    )

    pdf.sub("重置仪表板")
    pdf.txt(
        "要完全重置，清除以下localStorage键: "
        "ctower_project_data, ctower_live_state, ctower_mb_threads, ctower_mb_decisions, "
        "ctower_doclib_docs, ctower_qa_messages, ctower_qa_settings, "
        "ctower_qa_archive。或在浏览器设置中清除所有站点数据。"
    )

    # ── 23. 510(k) Predicate Finder ──
    pdf.add_page()
    pdf.sec(23, "510(k) Predicate Finder")
    pdf.txt(
        "510(k) Predicate Finder\u662f\u4e00\u6b3e\u914d\u5957SaaS\u5de5\u5177\uff0c"
        "\u8fde\u63a5\u5230FDA openFDA\u6570\u636e\u5e93\u3002\u5b83\u5e2e\u52a9PMP\u548c\u6cd5\u89c4\u56e2\u961f"
        "\u8bc6\u522b\u5148\u5bfc\u5668\u68b0\u3001\u8ffd\u6eaf\u5148\u5bfc\u94fe\u5e76\u8d77\u8349\u5b9e\u8d28\u7b49\u6548\u6027\u8bba\u8bc1"
        " -- \u8fd9\u4e9b\u4efb\u52a1\u5bf9\u89c4\u5212510(k)\u63d0\u4ea4\u81f3\u5173\u91cd\u8981\u3002")

    pdf.sub("\u514d\u8d39\u7248 vs Pro\u7248")
    pdf.txt(
        "Predicate Finder\u514d\u8d39\u63d0\u4f9b\uff0c\u6709\u6bcf\u65e5\u9650\u5236\uff085\u6b21\u641c\u7d22\u30011\u6b21\u94fe\u8ffd\u6eaf\u30012\u5668\u68b0\u5bf9\u6bd4\uff09\u3002"
        "Pro\u7248\uff08$99/\u6708\uff09\u89e3\u9501\u65e0\u9650\u641c\u7d22\u3001\u65e0\u9650\u94fe\u8ffd\u6eaf\u30014\u5668\u68b0\u5bf9\u6bd4\u3001"
        "SE\u8bba\u8bc1\u751f\u6210\u548cPDF\u5bfc\u51fa\u3002")
    pdf.tip_box(
        "Predicate Finder\u662f510k Bridge\u7684\u4e3b\u8981\u6f5c\u5728\u5ba2\u6237\u83b7\u53d6\u5de5\u5177\u3002"
        "\u514d\u8d39\u7528\u6237\u63d0\u4f9b\u90ae\u7bb1\u89e3\u9501\u5de5\u5177\uff0c\u521b\u5efa\u81ea\u7136\u7684\u5347\u7ea7\u6f0f\u6597\u3002")

    pdf.sub("\u4e0eControl Tower\u7684\u96c6\u6210\uff08Scale\u5c42\u7ea7\uff09")
    pdf.txt(
        "\u5728Scale\u5c42\u7ea7\uff08$2,000/\u6708\uff09\u4e0a\uff0cPredicate Finder\u76f4\u63a5\u5d4c\u5165\u5728"
        "Control Tower\u4eea\u8868\u677f\u4e2d\u3002\u5148\u5bfc\u7814\u7a76\u4e3a\u4ee5\u4e0b\u5185\u5bb9\u63d0\u4f9b\u4fe1\u606f\uff1a"
    )
    pdf.bul("\u6cd5\u89c4\u8ddf\u8e2a\u5668 -- \u5148\u5bfc\u5668\u68b0\u5f15\u7528\u548cSE\u7b56\u7565")
    pdf.bul("\u98ce\u9669\u4eea\u8868\u677f -- \u5148\u5bfc\u5bf9\u6bd4\u4e2d\u8bc6\u522b\u7684\u98ce\u9669")
    pdf.bul("FDA\u901a\u4fe1\u4e2d\u5fc3 -- \u57fa\u4e8e\u5148\u5bfc\u5206\u6790\u7684Pre-Sub\u8ba8\u8bba\u8981\u70b9")
    pdf.bul("\u6587\u6863\u63a7\u5236 -- \u5148\u5bfc\u5bf9\u6bd4\u62a5\u544a\u4f5c\u4e3aDHF\u5de5\u4ef6")

    pdf.sub("PMP\u5de5\u4f5c\u6d41\u7a0b")
    pdf.txt(
        "1. \u4f7f\u7528Predicate Finder\u6309\u4ea7\u54c1\u4ee3\u7801\u6216\u5173\u952e\u8bcd\u641c\u7d22\u5019\u9009\u5148\u5bfc\u5668\u68b0\u3002\n"
        "2. \u8ffd\u6eaf\u5148\u5bfc\u94fe\u4ee5\u4e86\u89e3\u6cd5\u89c4\u8c31\u7cfb\u3002\n"
        "3. \u5e76\u6392\u5bf9\u6bd4\u6700\u591a4\u4e2a\u5668\u68b0\uff08Pro\uff09\u4ee5\u9009\u62e9\u6700\u5f3a\u7684\u5148\u5bfc\u3002\n"
        "4. \u751f\u6210SE\u8bba\u8bc1\u8349\u7a3f\uff08Pro\uff09\u4f5c\u4e3a\u6cd5\u89c4\u56e2\u961f\u7684\u8d77\u70b9\u3002\n"
        "5. \u5bfc\u51fa\u7ed3\u679c\u4e3aPDF\u5e76\u9644\u52a0\u5230\u6587\u6863\u63a7\u5236\u4e2d\u7684510(k)\u63d0\u4ea4\u5305\u3002")

    # ── 24. FDA与法规术语表 ──
    pdf.add_page()
    pdf.sec(24, "FDA与法规术语表")
    pdf.ln(2)
    fda_terms_cn = [
        ("510(k)", "上市前通知。向FDA提交的文件，证明II类器械与已合法上市的对照器械实质等同。以《食品、药品和化妆品法》第510(k)条命名。"),
        ("PMA（上市前批准）", "最严格的FDA审批路径，适用于无法证明实质等同的III类器械。需要临床数据支持。"),
        ("De Novo（从新分类）", "针对无对照器械的新型低至中等风险器械的FDA分类途径。批准后创建新的监管分类。"),
        ("实质等同（SE）", "510(k)放行的法定标准。新器械必须与对照器械具有相同的预期用途和相似的技术特征，或不同的技术特征不会引发新的安全性/有效性问题。"),
        ("对照器械（Predicate）", "已合法上市的器械（通过510(k)放行或修正前上市），用作新510(k)提交的比较基础。"),
        ("产品代码（Product Code）", "FDA对器械类型的字母数字分类代码（如IKN用于sEMG呼吸监测器，DQS用于EIT胸部成像仪，BZG用于肺功能仪）。"),
        ("法规编号（Regulation Number）", "定义器械分类的CFR引用（如21 CFR 882.1400用于EEG器械，21 CFR 890.1850用于动力运动设备）。"),
        ("I类 / II类 / III类", "FDA基于风险的器械分类。I类=最低风险（一般控制）。II类=中等风险（特殊控制+510(k)）。III类=最高风险（需PMA）。"),
        ("一般控制（General Controls）", "所有器械的FDA基线要求：注册、列名、标签、GMP、上市前通知和不良事件报告。"),
        ("特殊控制（Special Controls）", "II类器械在一般控制之外的额外FDA要求：指南文件、性能标准、上市后监督或患者登记。"),
        ("Pre-Sub（上市前会议）", "正式的FDA会议请求（前称Q-Sub），用于在提交510(k)或PMA之前讨论监管策略、测试计划或临床研究设计。"),
        ("Q-Sub（Q提交）", "Pre-Sub的旧称。请求与FDA审查部门召开Pre-Sub会议的正式流程。"),
        ("DICE", "工业与消费者教育司。负责处理Pre-Sub后勤、会议安排和一般提交咨询的FDA部门。"),
        ("RTA（拒绝受理）", "FDA对510(k)提交的初步行政筛查。未通过检查清单将在实质审查前立即被退回。"),
        ("SE报告", "实质等同判定报告。FDA的决策文件，对510(k)做出放行（SESE）或拒绝（NSE）的决定。"),
        ("SESE", "实质等同——510(k)审查的肯定结果，获得上市许可。"),
        ("NSE", "非实质等同——510(k)的否定判定。器械不能通过510(k)上市；申请人可寻求De Novo或PMA途径。"),
        ("21 CFR Part 820", "质量体系法规（QSR）。FDA对医疗器械的现行良好生产规范（cGMP）要求。正在修订以与ISO 13485协调。"),
        ("ISO 13485", "医疗器械质量管理体系国际标准。在全球范围内广泛认可，并日益与FDA QSR协调。"),
        ("ISO 14971", "医疗器械风险管理国际标准。定义了危害识别、风险估计、风险评价和风险控制的流程。"),
        ("IEC 60601-1", "医用电气设备基本安全和基本性能的国际标准。大多数有源医疗器械的基础标准。"),
        ("IEC 62304", "医疗器械软件生命周期过程的国际标准。定义了软件安全等级（A、B、C）和开发要求。"),
        ("IEC 62366", "医疗器械可用性工程的国际标准。要求进行形成性和总结性可用性测试。"),
        ("DHF（设计历史文件）", "记录医疗器械设计和开发的完整记录集合，依据21 CFR 820.30要求。"),
        ("DMR（器械主记录）", "规定成品器械的文档，包括器械规格、生产工艺、质量保证程序和包装/标签规格。"),
        ("DHR（器械历史记录）", "每个单元或批次的生产记录，证明器械按照DMR制造。"),
        ("CAPA（纠正和预防措施）", "21 CFR 820.90要求的系统化流程，用于调查不合格品、识别根本原因并实施纠正/预防措施。"),
        ("设计控制（Design Controls）", "21 CFR 820.30对设计过程的要求：设计策划、输入、输出、评审、验证、确认、转换和变更。"),
        ("V&V（验证与确认）", "验证确认设计输出满足设计输入（构建正确）。确认确认器械满足用户需求和预期用途（构建正确的产品）。"),
        ("生物相容性", "依据ISO 10993的生物安全性评估。任何与患者直接或间接接触的器械均需评估。测试包括细胞毒性、致敏性、刺激性等，具体取决于接触类型和持续时间。"),
        ("EMC（电磁兼容性）", "依据IEC 60601-1-2的测试，确保器械既不发射有害干扰，也不受外部电磁场影响。"),
        ("UDI（唯一器械标识）", "FDA强制要求的系统，要求在器械标签和包装上标注唯一标识符，用于追踪、召回和不良事件报告。"),
        ("MDR / eMDR（医疗器械报告）", "当器械可能导致或促成死亡或严重伤害时，向FDA提交的强制性不良事件报告。"),
        ("510(k)摘要", "510(k)提交的公开摘要，描述器械、对照比较和实质等同的依据。"),
        ("预期用途（Indications for Use）", "器械的特定临床适应症、患者群体和使用目的。必须与对照器械的适应症相匹配或为其子集。"),
        ("标签（Labeling）", "器械上或随附的所有书面、印刷或图形材料，包括使用说明（IFU）、包装插页和推广材料。"),
        ("GMP（良好生产规范）", "FDA的制造质量要求，编入21 CFR Part 820（QSR）。"),
        ("FDA机构注册", "所有参与在美国市场销售的医疗器械生产和分销设施每年必须进行的注册。"),
        ("FDA器械列名", "要求将每个商业化分销的器械向FDA列名，包括产品代码和专有名称。"),
        ("美国代理人（US Agent）", "外国器械制造商的强制要求。指定一名居住在美国的人员作为FDA与外国机构的联系人。"),
        ("510(k)持有人", "拥有510(k)放行的法人实体（通常是美国LLC或公司）。外国公司通常为此设立美国子公司。"),
        ("eSTAR", "电子提交模板与资源。FDA标准化的510(k)电子提交格式，取代以前的纸质/eCopy流程。"),
        ("MDSAP", "医疗器械单一审计程序。允许通过一次监管审计满足多个参与国家的要求（美国、加拿大、澳大利亚、巴西、日本）。"),
        ("sEMG（表面肌电图）", "非侵入性肌肉电活动测量。在呼吸监测中，测量来自肋间肌和膈肌的神经呼吸驱动。"),
        ("EIT（电阻抗断层成像）", "非侵入性成像技术，创建组织电导率的横截面图像。用于实时肺通气监测。"),
        ("V/Q比值", "通气/灌注比。到达肺泡的空气与到达肺泡的血液之间的关系。气体交换效率的关键指标。"),
        ("FES（功能性电刺激）", "治疗性电流应用，激活瘫痪或虚弱的肌肉以实现功能性运动。"),
        ("NRE（非经常性工程费用）", "产品开发、工装和制造设置的一次性工程成本，不在每个单元生产中重复发生。"),
        ("openFDA", "FDA\u7684\u516c\u5171API\uff0c\u63d0\u4f9b\u5bf9510(k)\u6279\u51c6\u8bb0\u5f55\u3001\u4e0d\u826f\u4e8b\u4ef6\u3001\u53ec\u56de\u7b49\u6cd5\u89c4\u6570\u636e\u7684\u53ef\u641c\u7d22\u8bbf\u95ee\u3002"),
        ("Predicate Finder", "510k Bridge\u7684SaaS\u5de5\u5177\uff0c\u7528\u4e8e\u4f7f\u7528openFDA\u6570\u636e\u5e93\u641c\u7d22\u3001\u6bd4\u8f83\u548c\u8ffd\u6eaf\u5148\u5bfc\u5668\u68b0\u3002\u63d0\u4f9b\u514d\u8d39\u7248\u548cPro\u7248\u3002"),
        ("\u5148\u5bfc\u94fe", "\u5c06\u5df2\u6279\u51c6\u5668\u68b0\u901a\u8fc7\u5148\u524d\u51e0\u4ee3510(k)\u6279\u51c6\u8fde\u63a5\u8d77\u6765\u7684\u5148\u5bfc\u5f15\u7528\u8c31\u7cfb\u3002"),
    ]
    for k, v in fda_terms_cn:
        pdf.kv(k, v)
        pdf.ln(1)

    out = os.path.join(OUT_DIR, "PMP_Users_Guide_CN.pdf")
    pdf.output(out)
    return out


if __name__ == "__main__":
    print("Generating PMP User's Guide (EN)...")
    en = build_english()
    print(f"  EN: {en}")
    print("Generating PMP User's Guide (CN)...")
    cn = build_chinese()
    print(f"  CN: {cn}")
    print("Done.")
