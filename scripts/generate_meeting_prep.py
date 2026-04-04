#!/usr/bin/env python3
"""Generate Meeting Preparation PDF for Dr. Dai conversation — March 23, 2026."""

import os
from fpdf import FPDF

OUT_DIR = os.path.dirname(os.path.abspath(__file__))

BLUE = (30, 90, 200)
DARK = (15, 17, 23)
GRAY = (120, 120, 130)
TEXT = (40, 40, 45)
RED = (180, 40, 40)
GREEN = (20, 130, 70)
ORANGE = (200, 120, 20)


class MeetingPrepPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*GRAY)
        self.cell(0, 6, "Meeting Prep -- Dr. Dai -- March 23, 2026", align="R")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(*GRAY)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")

    def sec(self, num, title):
        self.set_font("Helvetica", "B", 15)
        self.set_text_color(*BLUE)
        self.cell(0, 10, f"{num}. {title}", new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(*BLUE)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(4)

    def sub(self, title):
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(*TEXT)
        self.cell(0, 7, title, new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def txt(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*TEXT)
        self.multi_cell(0, 5.5, text, new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def question(self, num, text):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(*BLUE)
        self.multi_cell(0, 5.5, f"Q{num}. {text}", new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def context_note(self, text):
        self.set_font("Helvetica", "I", 9)
        self.set_text_color(*GRAY)
        self.multi_cell(0, 5, f"  Context: {text}", new_x="LMARGIN", new_y="NEXT")
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*TEXT)
        self.ln(2)

    def notes_area(self):
        """Draw a lined area for handwritten notes."""
        y = self.get_y()
        x = self.l_margin
        w = self.w - self.l_margin - self.r_margin
        self.set_draw_color(200, 200, 210)
        for i in range(3):
            line_y = y + i * 8
            self.line(x, line_y, x + w, line_y)
        self.ln(28)

    def divider(self):
        self.set_draw_color(200, 200, 210)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(4)


def build():
    pdf = MeetingPrepPDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()

    # ── Cover ──
    pdf.ln(20)
    pdf.set_font("Helvetica", "B", 26)
    pdf.set_text_color(*BLUE)
    pdf.cell(0, 14, "Meeting Conversation Guide", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)
    pdf.set_font("Helvetica", "", 14)
    pdf.set_text_color(*TEXT)
    pdf.cell(0, 8, "Dr. Dai -- Initial Strategy Discussion", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(*GRAY)
    pdf.cell(0, 7, "March 23, 2026", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 7, "ICU Respiratory Digital Twin System", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 7, "sEMG Neural Drive + EIT Ventilation/Perfusion Monitoring", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)
    pdf.set_font("Helvetica", "I", 10)
    pdf.set_text_color(*GRAY)
    pdf.multi_cell(0, 5.5,
        "This document guides the conversation with Dr. Dai to clarify team structure, "
        "corporate formation, IP ownership, and the working relationship between "
        "Chinese and US entities. Answers will inform the Delaware C-Corp formation, "
        "IP licensing strategy, and equity allocation.",
        align="C")
    pdf.ln(8)

    # Key context box
    pdf.set_fill_color(240, 243, 255)
    pdf.set_draw_color(*BLUE)
    y = pdf.get_y()
    pdf.rect(pdf.l_margin, y, pdf.w - pdf.l_margin - pdf.r_margin, 42, style="DF")
    pdf.set_xy(pdf.l_margin + 4, y + 3)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(*BLUE)
    pdf.cell(0, 5.5, "Known Context Going In:")
    pdf.set_xy(pdf.l_margin + 4, y + 10)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(*TEXT)
    items = [
        "Dr. Dai is CTO and inventor of the sEMG/EIT technology (currently 100% allocation).",
        "Dr. Dai has approached Lawrence Liu as an investor. Lawrence wants US company control.",
        "Plan: Delaware C-Corp. Need to determine entity structure, IP licensing, equity split.",
        "Current burn: $45K/month, $320K cash on hand, ~7-month runway.",
        "IP is currently in China (Silan Technology, Chengdu). Must transfer to US entity for 510(k).",
    ]
    for item in items:
        pdf.set_x(pdf.l_margin + 6)
        pdf.cell(0, 5.5, f"  - {item}", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(8)

    # ═══════════════════════════════════════
    # SECTION 1: Team & Communication
    # ═══════════════════════════════════════
    pdf.add_page()
    pdf.sec(1, "Team & Communication")
    pdf.txt(
        "Clarify the full team landscape -- who are the key people, what are their "
        "roles, and how will day-to-day communication work.")

    pdf.question(1, "Who besides you (Dr. Dai) will I interact with regularly?")
    pdf.context_note(
        "Current team is Lon Dailey (PMP), Dr. Dai (CTO), Lawrence Liu (CEO, Company B). "
        "Need to understand if there are engineers, lab technicians, regulatory consultants, "
        "or other stakeholders in Chengdu who will be part of the workflow.")
    pdf.notes_area()

    pdf.question(2, "What is your email address? (And preferred communication channel?)")
    pdf.context_note(
        "Needed for the Q&A Message Board email notifications and day-to-day coordination. "
        "Also determine WeChat, Zoom, or other tools for meetings across time zones.")
    pdf.notes_area()

    pdf.question(3, "What time zone are you primarily working in, "
                    "and what hours overlap best for real-time calls?")
    pdf.context_note(
        "Chengdu is UTC+8 (CDT+13). Establishing a regular sync cadence early prevents drift.")
    pdf.notes_area()

    # ═══════════════════════════════════════
    # SECTION 2: FDA Experience & Strategy
    # ═══════════════════════════════════════
    pdf.add_page()
    pdf.sec(2, "FDA Experience & Regulatory Strategy")
    pdf.txt(
        "Understand Dr. Dai's prior exposure to US regulatory processes. "
        "This shapes how much regulatory education vs. strategic discussion we need.")

    pdf.question(4, "Is this the first product you have been involved with "
                    "that needs FDA clearance?")
    pdf.context_note(
        "If yes, we need more structured regulatory onboarding. If no, understanding "
        "prior submissions (success/failure) helps calibrate the approach. Also relevant: "
        "any NMPA (China) or CE (EU) submissions for this or other devices.")
    pdf.notes_area()

    pdf.question(5, "Are you structuring the FDA clearance towards an acquisition "
                    "by an established medical device company?")
    pdf.context_note(
        "This changes everything about the regulatory strategy. If the endgame is "
        "acquisition, the DHF must be 'acquirer-ready' from day one -- cleaner documentation, "
        "broader predicate search, and IP provenance that survives M&A due diligence. "
        "If building to operate, the strategy can be more streamlined.")
    pdf.notes_area()

    pdf.question(6, "Do you have a specific predicate device in mind for the 510(k), "
                    "or are we starting that search fresh?")
    pdf.context_note(
        "The Pre-Sub meeting with FDA (planned M+2) requires a proposed predicate. "
        "Product codes IKN (sEMG) and DQS (EIT) are already identified in the project plan.")
    pdf.notes_area()

    # ═══════════════════════════════════════
    # SECTION 3: Corporate Structure & Roles
    # ═══════════════════════════════════════
    pdf.add_page()
    pdf.sec(3, "Corporate Structure -- Delaware C-Corp")
    pdf.txt(
        "The plan is to form a Delaware C-Corp ('Company B USA'). Dr. Dai has brought "
        "Lawrence Liu in as an investor. Lawrence appears to want control of the US entity. "
        "These questions clarify how the pieces fit together.")

    pdf.question(7, "How do you foresee the relationship structure between "
                    "Chinese interests (Silan Technology) and the US company (Company B USA)?")
    pdf.context_note(
        "Key structural options: (a) Silan as a wholly-owned subsidiary of Company B USA, "
        "(b) Silan as an independent contract manufacturer with an IP license, "
        "(c) A cross-holding structure. Each has different CFIUS, tax, and control implications. "
        "The R8 milestone (IP Buyout & US Legal Structure) is already in progress.")
    pdf.notes_area()

    pdf.question(8, "What role does Lawrence Liu expect to play in Company B USA? "
                    "CEO? Board Chair? Investor only?")
    pdf.context_note(
        "If Lawrence wants operational control, the equity and governance structure "
        "must reflect that. If he's a financial investor, he may take a board seat "
        "but not an officer role. This also affects cap table design.")
    pdf.notes_area()

    pdf.question(9, "How should IP ownership be structured? Full assignment to "
                    "Company B USA, or licensing from a Chinese holding entity?")
    pdf.context_note(
        "FDA strongly prefers that the 510(k) applicant owns (not licenses) the IP. "
        "A full assignment with back-license to China for manufacturing is the cleanest "
        "path. R8 already contemplates full transfer to the US entity. Need to confirm "
        "Dr. Dai and Lawrence are aligned on this.")
    pdf.notes_area()

    # ── IP Structure Explainer (visual reference for the meeting) ──
    pdf.add_page()
    pdf.sub("IP Ownership Structure -- Explainer for Q9")
    pdf.ln(2)

    # Recommended path
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(*GREEN)
    pdf.cell(0, 7, "RECOMMENDED: Full Assignment + Back-License", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(*TEXT)
    pdf.txt(
        "This is a two-step structure:")
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(*BLUE)
    pdf.cell(0, 6, "Step 1 -- Assignment (China -> US)", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(*TEXT)
    pdf.txt(
        "Dr. Dai (or Silan Technology, whoever currently holds the patents) executes an "
        "IP Assignment Agreement transferring ALL rights, title, and interest in the patents, "
        "software copyrights, and trade secrets to Company B USA (the Delaware C-Corp). "
        "This is a permanent, irrevocable transfer -- Company B USA becomes the legal owner.")
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(*BLUE)
    pdf.cell(0, 6, "Step 2 -- Back-License (US -> China)", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(*TEXT)
    pdf.txt(
        "Company B USA then grants Silan Technology a limited license to use the IP ONLY "
        "for manufacturing the device on behalf of Company B USA. This license is:\n\n"
        "  - Non-exclusive (Company B USA can use other manufacturers later)\n"
        "  - Revocable (Company B USA can terminate if Silan underperforms)\n"
        "  - Limited in scope (manufacturing only, not independent sales)\n"
        "  - Controlled by the US entity")

    # Why FDA prefers this
    pdf.ln(2)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(*BLUE)
    pdf.cell(0, 6, "Why FDA Prefers This:", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(*TEXT)
    pdf.txt(
        "The 510(k) applicant (Company B USA) must demonstrate it controls the technology "
        "it is submitting. If Company B USA only licenses the IP from a Chinese entity, "
        "FDA sees a dependency -- the licensor could revoke the license, and the cleared "
        "device would have no IP backing. Ownership eliminates that risk.")

    # Why investors prefer this
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(*BLUE)
    pdf.cell(0, 6, "Why Investors Prefer This:", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(*TEXT)
    pdf.txt(
        "US investors and acquirers want IP domiciled in a US entity under US law. "
        "A Delaware C-Corp holding the IP is the cleanest structure for fundraising, "
        "acquisition, or IPO.")

    # Not recommended path
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(*RED)
    pdf.cell(0, 7, "NOT RECOMMENDED: License-Only (Chinese Entity Retains IP)", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(*TEXT)
    pdf.txt(
        "In this model, Silan/Dr. Dai retains ownership and licenses the IP to Company B USA. "
        "Problems include:\n\n"
        "  - FDA may question whether Company B USA truly controls the technology\n"
        "  - Investors see the Chinese entity as holding leverage over the US company\n"
        "  - An acquirer would need to negotiate with the Chinese IP holder separately\n"
        "  - CFIUS scrutiny increases if a Chinese entity controls IP for a US medical device")

    # How Dr. Dai retains value
    pdf.ln(2)
    pdf.set_draw_color(*BLUE)
    pdf.set_fill_color(240, 243, 255)
    y = pdf.get_y()
    box_h = 48
    pdf.rect(pdf.l_margin, y, pdf.w - pdf.l_margin - pdf.r_margin, box_h, style="DF")
    pdf.set_xy(pdf.l_margin + 4, y + 3)
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(*BLUE)
    pdf.cell(0, 6, "How Dr. Dai Retains Value (Key Talking Point)")
    pdf.set_xy(pdf.l_margin + 4, y + 11)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(*TEXT)
    box_items = [
        "Dr. Dai trades IP ownership for EQUITY ownership in Company B USA.",
        "He gets founder shares (typically 40-50% at this stage).",
        "His shares vest over time, tying his continued involvement to ownership.",
        "The IP becomes a corporate asset that increases the value of HIS shares.",
        "Example: If Company B USA is acquired for $50M, Dr. Dai's 40% = $20M.",
        "This is far more valuable than holding IP personally.",
    ]
    for item in box_items:
        pdf.set_x(pdf.l_margin + 6)
        pdf.cell(0, 5.5, f"  - {item}", new_x="LMARGIN", new_y="NEXT")
    pdf.set_y(y + box_h + 4)

    # Visual diagram
    pdf.ln(4)
    pdf.sub("Structure Diagram:")
    pdf.ln(2)
    pdf.set_font("Courier", "", 9)
    pdf.set_text_color(*TEXT)
    diagram_lines = [
        "+---------------------------+      IP Assignment      +---------------------------+",
        "|   Dr. Dai / Silan Tech    | ======================> |    Company B USA           |",
        "|   (Chengdu, China)        |    (permanent, full)    |    (Delaware C-Corp)       |",
        "|                           |                         |                            |",
        "|   - Current IP holder     |                         |    - 510(k) applicant      |",
        "|   - Inventor              |                         |    - IP owner (legal)      |",
        "|   - Manufacturer          |                         |    - Investor-ready        |",
        "+---------------------------+                         +---------------------------+",
        "            ^                                                     |",
        "            |              Manufacturing Back-License             |",
        "            +<===================================================+",
        "              (non-exclusive, revocable, mfg-only, US-controlled)",
        "",
        "Dr. Dai's value:  IP ownership  --->  Equity ownership (founder shares)",
        "Lawrence's value: Investment $   --->  Preferred shares + board seat",
        "Lon's value:      PMP services  --->  Equity (operating partner shares)",
    ]
    for line in diagram_lines:
        pdf.cell(0, 4.2, line, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    # What R8 already says
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(*TEXT)
    pdf.sub("What the Project Plan Already Contemplates (R8 Milestone):")
    pdf.txt(
        "  - All patents assigned to the US entity\n"
        "  - Software copyrights and MyoBus IP included in the transfer\n"
        "  - Formal assignment agreement under US law\n"
        "  - Must be completed before Pre-Sub meeting (M+2) because FDA\n"
        "    expects the submitting entity to demonstrate IP ownership")

    # Confirm with Dr. Dai
    pdf.ln(2)
    pdf.sub("What to Confirm With Dr. Dai Today:")
    pdf.txt(
        "  1. Who currently holds the IP? (Dr. Dai personally? Silan? University?)\n"
        "  2. Is Dr. Dai willing to assign? (Equity stake is the trade)\n"
        "  3. Is Lawrence aligned? (IP must come to Delaware entity)\n"
        "  4. Back-license scope: Silan manufactures only, no independent\n"
        "     commercialization in China without separate agreement")
    pdf.notes_area()

    pdf.add_page()
    pdf.question(10, "What is the planned equity/share allocation among Dr. Dai, "
                     "Lawrence Liu, and Lon Dailey?")
    pdf.context_note(
        "Typical early-stage medical device: Inventor 40-50%, Lead Investor 25-35%, "
        "Operating Partner/PMP 10-20%, with an employee option pool of 10-15%. "
        "Vesting schedules (4-year with 1-year cliff) are standard. Delaware C-Corp "
        "allows multiple share classes (common vs. preferred).")
    pdf.notes_area()

    # ── Equity Explainer (visual reference for the meeting) ──
    pdf.sub("Equity & Share Structure -- Explainer for Q10")
    pdf.ln(2)

    # Share classes
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(*BLUE)
    pdf.cell(0, 6, "Delaware C-Corp Share Classes", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(*TEXT)
    pdf.txt(
        "A Delaware C-Corp can issue multiple classes of stock. This is essential "
        "because each party is contributing something different:\n\n"
        "  Common Stock -- Issued to founders and employees for sweat equity,\n"
        "    IP contributions, and services. Lower price per share. Carries voting\n"
        "    rights but is last in line during liquidation.\n\n"
        "  Preferred Stock -- Issued to investors in exchange for cash. Higher price\n"
        "    per share (reflects a valuation premium). Carries liquidation preference\n"
        "    (investors get their money back first), anti-dilution protection, and\n"
        "    often a board seat.")

    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(*BLUE)
    pdf.cell(0, 6, "Why This Matters:", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(*TEXT)
    pdf.txt(
        "Dr. Dai's IP contribution and Lon's PMP services are valued as common stock. "
        "Lawrence's cash investment buys preferred stock at a negotiated valuation. "
        "The two classes protect Lawrence's cash while rewarding Dr. Dai and Lon for "
        "non-cash contributions.")

    # Cap table illustration
    pdf.add_page()
    pdf.sub("Illustrative Cap Table (Negotiating Starting Point)")
    pdf.ln(2)

    pdf.set_draw_color(*BLUE)
    pdf.set_fill_color(240, 243, 255)
    # Table header
    col_w = [60, 30, 30, 50]
    headers = ["Party", "Shares", "Ownership", "Contribution"]
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(255, 255, 255)
    pdf.set_fill_color(*BLUE)
    for i, h in enumerate(headers):
        pdf.cell(col_w[i], 7, h, border=1, fill=True, align="C")
    pdf.ln()

    # Table rows
    rows = [
        ("Dr. Dai (Inventor)", "4,000,000", "40%", "IP + Technical Lead"),
        ("Lawrence Liu (Investor)", "3,000,000", "30%", "Cash investment"),
        ("Lon Dailey (PMP)", "1,500,000", "15%", "PM + Regulatory"),
        ("Employee Option Pool", "1,500,000", "15%", "Future hires"),
        ("TOTAL", "10,000,000", "100%", ""),
    ]
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(*TEXT)
    for i, (party, shares, pct, contrib) in enumerate(rows):
        if i == len(rows) - 1:
            pdf.set_font("Helvetica", "B", 9)
            pdf.set_fill_color(230, 235, 250)
        else:
            pdf.set_font("Helvetica", "", 9)
            pdf.set_fill_color(250, 250, 255) if i % 2 == 0 else pdf.set_fill_color(255, 255, 255)
        pdf.cell(col_w[0], 6, party, border=1, fill=True)
        pdf.cell(col_w[1], 6, shares, border=1, fill=True, align="C")
        pdf.cell(col_w[2], 6, pct, border=1, fill=True, align="C")
        pdf.cell(col_w[3], 6, contrib, border=1, fill=True)
        pdf.ln()

    pdf.ln(2)
    pdf.set_font("Helvetica", "I", 9)
    pdf.set_text_color(*GRAY)
    pdf.txt(
        "Note: These are illustrative percentages for discussion. Actual allocation "
        "depends on negotiation, IP valuation, and investment amount. 10M authorized "
        "shares is standard for a Delaware C-Corp at incorporation.")

    # Vesting explanation
    pdf.ln(2)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(*BLUE)
    pdf.cell(0, 6, "Vesting Schedules -- Why They Matter", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(*TEXT)
    pdf.txt(
        "Vesting ensures that founders earn their shares over time by staying involved. "
        "If someone leaves early, unvested shares return to the company. Standard terms:\n\n"
        "  4-Year Vesting  -- Shares vest (become fully owned) over 4 years\n"
        "  1-Year Cliff    -- No shares vest in the first 12 months. If someone\n"
        "                     leaves before 1 year, they get nothing.\n"
        "  Monthly After   -- After the cliff, shares vest monthly (1/48 per month)\n\n"
        "Example for Dr. Dai (4M shares, 4-year vest, 1-year cliff):\n"
        "  - Month 0-11:   0 shares vested (cliff period)\n"
        "  - Month 12:     1,000,000 shares vest (25% cliff release)\n"
        "  - Month 13-48:  ~83,333 shares vest each month\n"
        "  - Month 48:     4,000,000 shares fully vested")

    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(*BLUE)
    pdf.cell(0, 6, "Should Everyone Vest?", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(*TEXT)
    pdf.txt(
        "  Dr. Dai    -- YES. His continued technical involvement is critical.\n"
        "                If he leaves, unvested shares return to the pool.\n"
        "  Lon Dailey -- YES. Same logic. PMP services vest over the project.\n"
        "  Lawrence   -- TYPICALLY NO. Investors buy shares outright with cash.\n"
        "                Their shares are fully owned at purchase. However, if\n"
        "                Lawrence takes an operational role (CEO), a portion of\n"
        "                his common shares (separate from his investment) should vest.")

    # Liquidation preference
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(*BLUE)
    pdf.cell(0, 6, "Liquidation Preference -- Protecting the Cash Investor", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(*TEXT)
    pdf.txt(
        "Lawrence is putting in cash. Preferred stock protects that investment:\n\n"
        "  1x Non-Participating Preferred (standard):\n"
        "  If the company is sold, Lawrence gets his investment back FIRST,\n"
        "  before any proceeds go to common shareholders. Then he can either\n"
        "  take his money or convert to common and share pro-rata.\n\n"
        "  Example -- Company sold for $10M, Lawrence invested $500K:\n"
        "    - Lawrence gets $500K back first (liquidation preference)\n"
        "    - Remaining $9.5M split among all shareholders pro-rata\n"
        "    - OR Lawrence converts: gets 30% of $10M = $3M (better deal)\n\n"
        "  Example -- Company sold for $400K (bad outcome):\n"
        "    - Lawrence gets $400K (all of it, up to his $500K preference)\n"
        "    - Common shareholders (Dr. Dai, Lon) get $0\n"
        "    - This protects the cash investor in a downside scenario")

    # Board composition
    pdf.ln(2)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(*BLUE)
    pdf.cell(0, 6, "Board of Directors -- Governance", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(*TEXT)
    pdf.txt(
        "A 3-person board is standard at this stage:\n\n"
        "  Seat 1 -- Founder seat (Dr. Dai or Lon, elected by common shareholders)\n"
        "  Seat 2 -- Investor seat (Lawrence, elected by preferred shareholders)\n"
        "  Seat 3 -- Independent (mutually agreed, often an industry advisor)\n\n"
        "If Lawrence wants to be CEO AND hold the investor board seat, that gives\n"
        "him significant control. Discuss whether the founder seat offsets this,\n"
        "or whether a 5-seat board (2 founder, 2 investor, 1 independent) is better.")

    # Key negotiation points
    pdf.ln(2)
    pdf.set_draw_color(*BLUE)
    pdf.set_fill_color(240, 243, 255)
    y = pdf.get_y()
    box_h = 48
    pdf.rect(pdf.l_margin, y, pdf.w - pdf.l_margin - pdf.r_margin, box_h, style="DF")
    pdf.set_xy(pdf.l_margin + 4, y + 3)
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(*BLUE)
    pdf.cell(0, 6, "Key Negotiation Points to Resolve Today")
    pdf.set_xy(pdf.l_margin + 4, y + 11)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(*TEXT)
    neg_items = [
        "1. What % does Dr. Dai expect? (His IP is the core asset)",
        "2. What % does Lawrence expect for his investment?",
        "3. Is Lon's equity tied to the PMP engagement, or separate?",
        "4. Will there be an option pool for future engineers/hires?",
        "5. Does Lawrence want common shares (CEO role) AND preferred (investor)?",
        "6. Vesting: Is everyone comfortable with 4-year / 1-year cliff?",
    ]
    for item in neg_items:
        pdf.set_x(pdf.l_margin + 6)
        pdf.cell(0, 5.5, f"  {item}", new_x="LMARGIN", new_y="NEXT")
    pdf.set_y(y + box_h + 4)
    pdf.notes_area()

    pdf.question(11, "What is Lawrence Liu's intended investment amount, and what "
                     "valuation is being discussed?")
    pdf.context_note(
        "With $320K cash and $45K/month burn, the 7-month runway needs extension. "
        "A Series Seed round sets the company valuation and determines dilution for all parties. "
        "Is this a priced round or a SAFE/convertible note?")
    pdf.notes_area()

    pdf.question(12, "Are there other investors besides Lawrence Liu, "
                     "either current or expected?")
    pdf.context_note(
        "Multiple investors affect the cap table, board composition, and governance rights. "
        "Chinese investors may trigger CFIUS review for a medical device company.")
    pdf.notes_area()

    # ── Investor Landscape & CFIUS Explainer ──
    pdf.add_page()
    pdf.sub("Investor Landscape & CFIUS -- Explainer for Q12")
    pdf.ln(2)

    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(*BLUE)
    pdf.cell(0, 6, "Why This Question Matters", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(*TEXT)
    pdf.txt(
        "Every investor who comes in reshapes the company. This is not just about money -- "
        "it changes governance, decision-making speed, regulatory risk, and the eventual "
        "exit path. For a medical device company with Chinese-origin technology, the "
        "investor mix has direct regulatory consequences.")

    # Investor types
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(*BLUE)
    pdf.cell(0, 6, "Types of Investors and What They Mean for the Company", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(*TEXT)
    pdf.txt(
        "  Angel / Individual (e.g., Lawrence Liu)\n"
        "    - Writes a personal check ($100K-$1M typical)\n"
        "    - May want a board seat and operational role\n"
        "    - Fastest to close, fewest strings attached\n"
        "    - Due diligence is lighter\n\n"
        "  Venture Capital (VC) Fund\n"
        "    - Institutional money ($1M-$10M+ for med device Series A)\n"
        "    - Will demand preferred stock with full protective provisions\n"
        "    - Board seat, veto rights on major decisions, quarterly reporting\n"
        "    - Longer due diligence (3-6 months), but brings credibility\n"
        "    - Most US VCs will NOT invest if Chinese entity retains IP control\n\n"
        "  Strategic Investor (established med device company)\n"
        "    - Invests with intent to acquire or distribute\n"
        "    - May want right of first refusal on acquisition\n"
        "    - Can accelerate FDA pathway (their regulatory team, predicates)\n"
        "    - But: may restrict freedom to sell to competitors\n\n"
        "  Chinese Investor (individual or fund based in PRC)\n"
        "    - Triggers CFIUS review (see below)\n"
        "    - May bring manufacturing connections and Asia market access\n"
        "    - US institutional co-investors may be uncomfortable")

    # CFIUS section
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(*RED)
    pdf.cell(0, 7, "CFIUS -- Critical Risk for This Company", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(*TEXT)
    pdf.txt(
        "CFIUS (Committee on Foreign Investment in the United States) reviews transactions "
        "where a foreign person could gain control of, or certain rights in, a US business. "
        "Medical devices are classified as critical technology under CFIUS regulations.")

    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(*BLUE)
    pdf.cell(0, 6, "When CFIUS Is Triggered:", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(*TEXT)
    pdf.txt(
        "  - A foreign person acquires CONTROL of a US business (board majority,\n"
        "    equity majority, or operational decision-making power)\n"
        "  - A foreign person acquires a significant NON-CONTROLLING stake in a\n"
        "    US business that deals in critical technology (includes FDA-regulated\n"
        "    medical devices) -- even a minority investment can trigger review\n"
        "  - The foreign person gains access to material non-public technical\n"
        "    information, board observer rights, or governance rights")

    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(*BLUE)
    pdf.cell(0, 6, "What This Means for Company B USA:", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(*TEXT)
    pdf.txt(
        "  - The sEMG/EIT technology is a Class II medical device under FDA\n"
        "    jurisdiction -- this IS critical technology under CFIUS rules\n"
        "  - If Lawrence Liu is a Chinese national or PRC-based, his investment\n"
        "    likely triggers a mandatory CFIUS declaration\n"
        "  - If Dr. Dai retains board control through Chinese-entity holdings,\n"
        "    that also triggers review\n"
        "  - Even if CFIUS clears the transaction, the review process takes\n"
        "    45-90+ days and costs $50K-$150K in legal fees")

    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(*GREEN)
    pdf.cell(0, 6, "How to Structure Around CFIUS:", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(*TEXT)
    pdf.txt(
        "  1. IP fully assigned to the Delaware C-Corp (already planned in R8)\n"
        "  2. US person(s) maintain board majority (e.g., Lon + independent > Lawrence)\n"
        "  3. No foreign person has unilateral veto over company decisions\n"
        "  4. Technical information access governed by a security protocol\n"
        "  5. Manufacturing agreement with Silan is arms-length, not a control\n"
        "     relationship -- Silan is a vendor, not a parent\n"
        "  6. File a voluntary CFIUS declaration proactively (shows good faith,\n"
        "     faster resolution than being flagged later)")

    # Granddaughter / US citizen nominee structure
    pdf.ln(2)
    pdf.set_draw_color(*RED)
    pdf.set_fill_color(255, 240, 240)
    y = pdf.get_y()
    box_h = 80
    pdf.rect(pdf.l_margin, y, pdf.w - pdf.l_margin - pdf.r_margin, box_h, style="DF")
    pdf.set_xy(pdf.l_margin + 4, y + 3)
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(*RED)
    pdf.cell(0, 6, "Can Lawrence's US-Citizen Granddaughter Hold Shares to Avoid CFIUS?")
    pdf.set_xy(pdf.l_margin + 4, y + 11)
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(*TEXT)
    pdf.cell(0, 5.5, "Short answer: No. This would likely make things worse.", new_x="LMARGIN", new_y="NEXT")
    pdf.set_xy(pdf.l_margin + 6, y + 18)
    pdf.set_font("Helvetica", "", 9)
    nominee_items = [
        "1. CFIUS looks through nominee/trust structures -- it examines the",
        "   BENEFICIAL OWNER, not just the legal titleholder. A 1-year-old",
        "   cannot exercise shareholder rights; CFIUS will treat the parent/",
        "   grandparent as the real decision-maker.",
        "2. Using a minor as a nominee to avoid regulatory review could be",
        "   construed as EVASION of CFIUS, which carries criminal penalties",
        "   (fines up to the value of the transaction, or imprisonment).",
        "3. Shares held by a minor require a custodian (UTMA/UGMA account or",
        "   trust). The custodian is the one who votes and controls -- CFIUS",
        "   will attribute the investment to the custodian.",
        "4. If Lawrence is the custodian, it is functionally identical to",
        "   Lawrence holding the shares himself -- no CFIUS benefit at all.",
        "5. Even if a US-citizen parent is custodian, CFIUS can still look at",
        "   the SOURCE OF FUNDS. If the money originates from Lawrence (a",
        "   foreign person), the transaction is still reviewable.",
    ]
    for item in nominee_items:
        pdf.set_x(pdf.l_margin + 6)
        pdf.cell(0, 4.8, item, new_x="LMARGIN", new_y="NEXT")
    pdf.set_y(y + box_h + 4)

    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(*GREEN)
    pdf.cell(0, 6, "What Lawrence SHOULD Do Instead:", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(*TEXT)
    pdf.txt(
        "  1. Invest through a US-domiciled entity he controls (still triggers\n"
        "     review, but cleaner structure)\n"
        "  2. Limit his stake to a passive minority (<10%) with no governance\n"
        "     rights -- may qualify for a CFIUS exclusion\n"
        "  3. Use a SAFE or convertible note that defers equity conversion until\n"
        "     after a voluntary CFIUS filing is resolved\n"
        "  4. If he has US permanent residency (green card), he may qualify as a\n"
        "     US person -- this is the strongest path to avoiding CFIUS\n"
        "  5. Proactively file a voluntary CFIUS declaration -- if cleared, the\n"
        "     transaction is safe and the company has a clean record for future\n"
        "     investors and FDA interactions")

    # Impact on cap table
    pdf.ln(2)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(*BLUE)
    pdf.cell(0, 6, "How Additional Investors Affect the Cap Table:", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(*TEXT)
    pdf.txt(
        "Every new investor dilutes existing shareholders. Example with a future\n"
        "Series A round:\n\n"
        "  Pre-money valuation:     $5M (negotiated with new investor)\n"
        "  New investment:          $2M\n"
        "  Post-money valuation:    $7M\n"
        "  New investor gets:       $2M / $7M = 28.6% of the company\n"
        "  Everyone else diluted:   Existing 100% becomes 71.4%\n\n"
        "  Dr. Dai:   40% -> 28.6%   (still worth $2M at $7M valuation)\n"
        "  Lawrence:  30% -> 21.4%\n"
        "  Lon:       15% -> 10.7%\n"
        "  Pool:      15% -> 10.7%\n"
        "  New VC:     0% -> 28.6%\n\n"
        "Dilution is not bad if the valuation grows. 28.6% of a $7M company is\n"
        "worth more than 40% of a $2M company.")

    # Key questions box
    pdf.ln(2)
    pdf.set_draw_color(*BLUE)
    pdf.set_fill_color(240, 243, 255)
    y = pdf.get_y()
    box_h = 44
    pdf.rect(pdf.l_margin, y, pdf.w - pdf.l_margin - pdf.r_margin, box_h, style="DF")
    pdf.set_xy(pdf.l_margin + 4, y + 3)
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(*BLUE)
    pdf.cell(0, 6, "What to Ask Dr. Dai About Other Investors")
    pdf.set_xy(pdf.l_margin + 4, y + 11)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(*TEXT)
    inv_items = [
        "1. Is Lawrence a US citizen/resident, or PRC-based? (CFIUS trigger)",
        "2. Has Dr. Dai discussed the project with any other investors?",
        "3. Are there Chinese government grants or state-backed funds involved?",
        "4. Is there a plan for a Series A? If so, US or Chinese VCs?",
        "5. Does anyone else (university, employer, lab) have a financial claim?",
        "6. What is Lawrence's citizenship/residency status?",
    ]
    for item in inv_items:
        pdf.set_x(pdf.l_margin + 6)
        pdf.cell(0, 5, f"  {item}", new_x="LMARGIN", new_y="NEXT")
    pdf.set_y(y + box_h + 4)
    pdf.notes_area()

    # ── Protecting Lawrence & Dr. Dai -- PMP as US-Person Anchor ──
    pdf.add_page()
    pdf.sub("Protecting Lawrence's & Dr. Dai's Interests")
    pdf.txt(
        "The PMP (Lon Dailey) is a US citizen. This is a structural advantage: "
        "the company can be US-person-controlled for CFIUS, FDA, and investor "
        "optics while still protecting the legitimate interests of the two founders "
        "who are potentially foreign persons. Below is a protection framework for each.")

    # Dr. Dai protection
    pdf.ln(2)
    pdf.set_draw_color(*BLUE)
    pdf.set_fill_color(240, 243, 255)
    y = pdf.get_y()
    box_h = 88
    pdf.rect(pdf.l_margin, y, pdf.w - pdf.l_margin - pdf.r_margin, box_h, style="DF")
    pdf.set_xy(pdf.l_margin + 4, y + 3)
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(*BLUE)
    pdf.cell(0, 6, "Dr. Dai -- Inventor & CTO (Current IP Holder)")
    pdf.set_xy(pdf.l_margin + 4, y + 11)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(*TEXT)
    dai_items = [
        "EQUITY PROTECTION:",
        "  - 40% founder shares with anti-dilution ratchet (broad-based weighted avg)",
        "  - Acceleration clause: if Dr. Dai is terminated without cause, 100% vests",
        "  - Right of first refusal on any share transfer by other founders",
        "",
        "IP PROTECTION (Assignment + Back-License):",
        "  - Assignment: IP transfers to Company B USA (required for 510(k))",
        "  - Back-License: Dr. Dai retains a perpetual, royalty-free license for",
        "    academic research, teaching, and non-commercial use",
        "  - If Company B USA fails or abandons the device, IP reverts to Dr. Dai",
        "  - Reversion trigger: 12 months of no commercial activity + no active",
        "    FDA submission or clearance",
        "",
        "GOVERNANCE PROTECTION:",
        "  - Guaranteed board seat as long as he holds >10% equity",
        "  - Protective provisions: Dr. Dai must consent to any IP sale, license,",
        "    or sub-license to a third party",
        "  - CTO title and technical decision-making authority written into bylaws",
    ]
    for item in dai_items:
        pdf.set_x(pdf.l_margin + 6)
        pdf.cell(0, 4.5, item, new_x="LMARGIN", new_y="NEXT")
    pdf.set_y(y + box_h + 4)

    # Lawrence protection
    pdf.set_draw_color(*BLUE)
    pdf.set_fill_color(240, 243, 255)
    y = pdf.get_y()
    box_h = 78
    pdf.rect(pdf.l_margin, y, pdf.w - pdf.l_margin - pdf.r_margin, box_h, style="DF")
    pdf.set_xy(pdf.l_margin + 4, y + 3)
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(*BLUE)
    pdf.cell(0, 6, "Lawrence Liu -- Investor & CEO")
    pdf.set_xy(pdf.l_margin + 4, y + 11)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(*TEXT)
    liu_items = [
        "INVESTMENT PROTECTION:",
        "  - Preferred stock with 1x non-participating liquidation preference",
        "    (gets his $500K back before common splits, or converts to common)",
        "  - Pro-rata rights: can invest in future rounds to maintain his %",
        "  - Information rights: monthly financials, quarterly board package",
        "  - Most-favored-nation clause: if better terms are given to a future",
        "    investor, Lawrence's terms automatically upgrade",
        "",
        "GOVERNANCE (CFIUS-Compatible):",
        "  - Board observer seat (not a voting seat -- avoids CFIUS 'control'",
        "    trigger while still giving him full visibility)",
        "  - OR: voting board seat IF he qualifies as a US person (green card)",
        "  - Protective provisions (veto rights) on: dissolution, sale of company,",
        "    new debt >$100K, issuance of senior equity, CEO compensation changes",
        "",
        "OPERATIONAL ROLE:",
        "  - CEO title with defined scope (business development, China market)",
        "  - Employment/consulting agreement with Company B USA",
        "  - Non-compete limited to ICU respiratory monitoring (not overly broad)",
    ]
    for item in liu_items:
        pdf.set_x(pdf.l_margin + 6)
        pdf.cell(0, 4.2, item, new_x="LMARGIN", new_y="NEXT")
    pdf.set_y(y + box_h + 4)

    # PMP as structural anchor
    pdf.add_page()
    pdf.sub("How the PMP's US Citizenship Enables This Structure")
    pdf.ln(2)

    # Structure diagram
    pdf.set_font("Courier", "", 9)
    pdf.set_text_color(*TEXT)
    structure_lines = [
        "                    COMPANY B USA (Delaware C-Corp)",
        "                    ================================",
        "                              |",
        "                         BOARD OF DIRECTORS",
        "                    +--------+--------+--------+",
        "                    |        |        |        |",
        "                  Seat 1   Seat 2   Seat 3   (Seat 4-5",
        "                  Lon      Dr. Dai  Indep.    if needed)",
        "                  (US)     (inv.)   (US)",
        "                    |",
        "                    +-- US majority maintained (2 of 3 or 3 of 5)",
        "",
        "               EQUITY                    GOVERNANCE",
        "          Dr. Dai   40%  common      Board seat + IP veto",
        "          Lawrence  30%  preferred    Observer + protective provisions",
        "          Lon       15%  common       Board seat (chair if needed)",
        "          Pool      15%  reserved     Future hires / advisors",
    ]
    for line in structure_lines:
        pdf.cell(0, 4.5, line, new_x="LMARGIN", new_y="NEXT")

    pdf.ln(4)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(*TEXT)
    pdf.txt(
        "Key principle: The PMP's US citizenship allows the board to maintain a "
        "US-person majority without marginalizing Lawrence or Dr. Dai. They retain "
        "full economic rights and meaningful governance protections -- the structure "
        "simply ensures that CFIUS sees a US-controlled entity.")

    pdf.ln(2)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(*BLUE)
    pdf.cell(0, 6, "Specific CFIUS-Safe Mechanisms:", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(*TEXT)
    pdf.txt(
        "  1. Board composition: US persons hold majority of voting seats\n"
        "  2. Officer structure: PMP as Secretary/Treasurer, Lawrence as CEO\n"
        "     (CEO alone does not trigger CFIUS 'control' if board is US-majority)\n"
        "  3. Lawrence's protective provisions are NEGATIVE rights (veto power)\n"
        "     not AFFIRMATIVE control -- CFIUS distinguishes between these\n"
        "  4. Dr. Dai's IP veto is limited to IP disposition, not company\n"
        "     operations -- this is a standard founder protection, not 'control'\n"
        "  5. Technical information access: Dr. Dai accesses all technical data\n"
        "     as CTO/employee, not as a foreign investor -- different CFIUS\n"
        "     analysis applies to employees vs. investors\n"
        "  6. If challenged, the company can show: US-majority board, US officer,\n"
        "     US-based regulatory lead, IP owned by US entity, FDA submissions\n"
        "     filed by US person (Lon) -- strong US nexus")

    pdf.ln(2)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(*RED)
    pdf.cell(0, 6, "What to Avoid (Red Lines):", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(*TEXT)
    pdf.txt(
        "  - Do NOT give Lawrence unilateral hiring/firing authority over the\n"
        "    board or officers (this = foreign 'control' under CFIUS)\n"
        "  - Do NOT route IP licensing decisions through any Chinese entity\n"
        "  - Do NOT allow Silan to have equity or board representation in\n"
        "    Company B USA (keep it as an arms-length manufacturing vendor)\n"
        "  - Do NOT store critical technical data exclusively on Chinese servers\n"
        "  - Do NOT structure Lawrence's investment as a loan convertible at\n"
        "    his sole discretion (CFIUS may treat this as latent control)")

    # Discussion points
    pdf.ln(2)
    pdf.set_draw_color(*BLUE)
    pdf.set_fill_color(240, 243, 255)
    y = pdf.get_y()
    box_h = 36
    pdf.rect(pdf.l_margin, y, pdf.w - pdf.l_margin - pdf.r_margin, box_h, style="DF")
    pdf.set_xy(pdf.l_margin + 4, y + 3)
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(*BLUE)
    pdf.cell(0, 6, "Discussion Points for Today's Meeting")
    pdf.set_xy(pdf.l_margin + 4, y + 11)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(*TEXT)
    protect_items = [
        "1. Is Dr. Dai comfortable with the IP assignment + back-license + reversion structure?",
        "2. Does Lawrence want a board VOTE or is an observer seat + veto rights sufficient?",
        "3. What is Lawrence's immigration status? (Green card changes everything)",
        "4. Should we engage a CFIUS attorney now, or wait until corporate formation?",
    ]
    for item in protect_items:
        pdf.set_x(pdf.l_margin + 6)
        pdf.cell(0, 5.5, f"  {item}", new_x="LMARGIN", new_y="NEXT")
    pdf.set_y(y + box_h + 4)
    pdf.notes_area()

    # ═══════════════════════════════════════
    # SECTION 4: IP & Technology
    # ═══════════════════════════════════════
    pdf.add_page()
    pdf.sec(4, "IP Ownership & Technology Transfer")
    pdf.txt(
        "The IP situation is the foundation of the entire structure. "
        "The 510(k) applicant must demonstrate clear IP ownership.")

    pdf.question(13, "Who currently owns the patents and patent applications? "
                     "Dr. Dai personally? Silan Technology? A university?")
    pdf.context_note(
        "This is the single most important question for the corporate formation. "
        "If a university or employer has claims, the assignment chain gets complicated. "
        "Need a complete IP inventory: patent numbers, jurisdictions, named inventors.")
    pdf.notes_area()

    pdf.question(14, "Are there any co-inventors, research collaborators, or students "
                     "who contributed to the sEMG/EIT technology?")
    pdf.context_note(
        "Unnamed contributors can surface as IP claimants. Government grants "
        "(NIH, NSFC, MOST) may create march-in rights or ownership claims.")
    pdf.notes_area()

    pdf.question(15, "Is there any third-party IP in the device -- licensed algorithms, "
                     "open-source software, or university technology?")
    pdf.context_note(
        "GPL-licensed code or university IP can create ownership disputes. "
        "This must be disclosed before the IP transfer agreement is executed.")
    pdf.notes_area()

    pdf.question(16, "Are you comfortable with a full IP assignment to Company B USA "
                     "(Delaware C-Corp), with a back-license to Silan for manufacturing?")
    pdf.context_note(
        "This is the recommended structure per R8. Dr. Dai retains value through equity, "
        "not through IP retention. The back-license allows Silan to manufacture but "
        "keeps the US entity as the IP owner for FDA and investor purposes.")
    pdf.notes_area()

    # ═══════════════════════════════════════
    # SECTION 5: Operational
    # ═══════════════════════════════════════
    pdf.add_page()
    pdf.sec(5, "Operational & Financial")
    pdf.txt(
        "Clarify the current financial picture and operational commitments.")

    pdf.question(17, "Walk me through the $45K/month burn rate -- "
                     "what are the major cost buckets?")
    pdf.context_note(
        "Need breakdown: salaries, lab costs, Silan retainer, materials, testing services. "
        "Which costs are fixed vs. variable? Any upcoming step-function increases? "
        "What is the minimum spend to keep the project alive if funding is delayed?")
    pdf.notes_area()

    pdf.question(18, "What is your expected role after IP transfer? "
                     "CTO? Consultant? Advisory board?")
    pdf.context_note(
        "Resource allocation planning. Currently Dr. Dai is at 100% across sEMG Algorithm "
        "(40%), EIT Prototype (30%), MyoBus Integration (20%), Documentation (10%). "
        "Employment agreement vs. consulting agreement has tax and control implications.")
    pdf.notes_area()

    pdf.question(19, "Is there anything about this device -- technical limitations, "
                     "failed experiments, known issues -- that hasn't been disclosed yet?")
    pdf.context_note(
        "The PMP needs a complete picture. Undisclosed issues found during FDA review "
        "are far more damaging than issues disclosed upfront. Any prior adverse events "
        "or near-misses during prototype testing?")
    pdf.notes_area()

    # ═══════════════════════════════════════
    # SECTION 6: PMP Compensation Structure
    # ═══════════════════════════════════════
    pdf.add_page()
    pdf.sec(6, "PMP Compensation -- Equity + Contractor Fees")
    pdf.txt(
        "The PMP (Lon Dailey) is taking on two significant roles: (1) FDA regulatory lead "
        "for the 510(k) submission, and (2) US investor relations. This is not a salaried "
        "employee position -- it is a founder/operating partner engagement with a blended "
        "compensation model of equity and contractor fees.")

    # Scope of work
    pdf.sub("Scope of PMP Responsibilities")
    pdf.ln(2)
    pdf.set_draw_color(*BLUE)
    pdf.set_fill_color(240, 243, 255)
    y = pdf.get_y()
    box_h = 60
    pdf.rect(pdf.l_margin, y, pdf.w - pdf.l_margin - pdf.r_margin, box_h, style="DF")
    pdf.set_xy(pdf.l_margin + 4, y + 3)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(*BLUE)
    pdf.cell(80, 5.5, "Regulatory (510(k) Lead)")
    pdf.cell(0, 5.5, "US Investor Relations")
    pdf.set_xy(pdf.l_margin + 4, y + 10)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(*TEXT)
    left_items = [
        "Pre-Sub strategy & FDA meetings",
        "510(k) submission preparation",
        "Predicate device analysis",
        "Standards compliance (IEC 60601, 14971)",
        "DHF oversight & document control",
        "Silan ISO 13485 audit coordination",
        "FDA establishment registration",
    ]
    right_items = [
        "Investor pipeline development",
        "Pitch deck & materials",
        "Due diligence coordination",
        "Monthly investor reporting",
        "Board meeting preparation",
        "Term sheet negotiation support",
        "CFIUS navigation (if needed)",
    ]
    for i, (l, r) in enumerate(zip(left_items, right_items)):
        pdf.set_x(pdf.l_margin + 6)
        pdf.cell(80, 5, f"- {l}")
        pdf.cell(0, 5, f"- {r}")
        pdf.ln()
    pdf.set_y(y + box_h + 4)

    # Compensation model
    pdf.sub("Blended Compensation Model")
    pdf.txt(
        "The PMP compensation has two components: equity (long-term upside) and "
        "contractor fees (near-term cash for living expenses and operational costs). "
        "This is standard for an operating partner at a pre-revenue startup.")

    # Equity component
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(*BLUE)
    pdf.cell(0, 6, "Component 1: Equity (Founder Shares)", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(*TEXT)
    pdf.txt(
        "  Allocation:    15% of Company B USA (1,500,000 shares at 10M authorized)\n"
        "  Type:          Common stock (same class as Dr. Dai's founder shares)\n"
        "  Vesting:       4-year vest, 1-year cliff\n"
        "  Acceleration:  Double-trigger acceleration on change of control\n"
        "                 (if acquired AND PMP is terminated, remaining shares vest)\n\n"
        "  Why 15%: The PMP is contributing regulatory expertise, project management,\n"
        "  and investor relations -- three functions that would each cost $150-300/hr\n"
        "  if hired separately as consultants. The equity reflects the risk of joining\n"
        "  a pre-revenue startup where cash compensation is below market.")

    # Contractor fee component
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(*BLUE)
    pdf.cell(0, 6, "Component 2: Contractor Fees (Monthly Cash)", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(*TEXT)
    pdf.txt(
        "  Structure:     Independent contractor (1099), not W-2 employee\n"
        "  Engagement:    510k Bridge, Inc. (Delaware) as the contracting entity\n"
        "  Rate:          $10,000 - $15,000/month (blended across both roles)\n"
        "  Hours:         ~30-40 hrs/week (regulatory + IR combined)\n"
        "  Invoice:       Monthly, Net-15 payment terms\n"
        "  Duration:      Through 510(k) clearance (estimated 18 months)")

    # Rate justification
    pdf.add_page()
    pdf.sub("Contractor Rate Context -- Market Comparison")
    pdf.ln(2)

    # Comparison table
    col_w = [70, 35, 35, 30]
    headers = ["Service", "Market Rate", "PMP Rate", "Discount"]
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(255, 255, 255)
    pdf.set_fill_color(*BLUE)
    for i, h in enumerate(headers):
        pdf.cell(col_w[i], 7, h, border=1, fill=True, align="C")
    pdf.ln()

    rate_rows = [
        ("FDA Regulatory Consultant", "$250-400/hr", "~$95/hr", "62-76%"),
        ("510(k) Submission Specialist", "$200-350/hr", "(included)", "--"),
        ("IR / Fundraising Advisor", "$200-300/hr", "(included)", "--"),
        ("PMP Project Manager (med device)", "$150-250/hr", "(included)", "--"),
        ("Blended if hired separately", "$35-50K/mo", "$10-15K/mo", "57-70%"),
    ]
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(*TEXT)
    for i, (svc, market, pmp, disc) in enumerate(rate_rows):
        if i == len(rate_rows) - 1:
            pdf.set_font("Helvetica", "B", 9)
            pdf.set_fill_color(230, 235, 250)
        else:
            pdf.set_font("Helvetica", "", 9)
            pdf.set_fill_color(250, 250, 255) if i % 2 == 0 else pdf.set_fill_color(255, 255, 255)
        pdf.cell(col_w[0], 6, svc, border=1, fill=True)
        pdf.cell(col_w[1], 6, market, border=1, fill=True, align="C")
        pdf.cell(col_w[2], 6, pmp, border=1, fill=True, align="C")
        pdf.cell(col_w[3], 6, disc, border=1, fill=True, align="C")
        pdf.ln()

    pdf.ln(2)
    pdf.set_font("Helvetica", "I", 9)
    pdf.set_text_color(*GRAY)
    pdf.txt(
        "The below-market contractor rate is offset by the equity component. This is the "
        "standard startup trade-off: the PMP accepts lower cash now in exchange for "
        "ownership upside if the company succeeds.")

    # Total compensation over 18 months
    pdf.ln(2)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(*BLUE)
    pdf.cell(0, 6, "Total PMP Compensation Over 18 Months (Estimated)", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(*TEXT)
    pdf.txt(
        "  Contractor fees:   $10-15K x 18 months = $180,000 - $270,000\n"
        "  Equity (at cost):  1,500,000 shares at $0.001/share = $1,500 (nominal)\n"
        "  Equity (at $5M):   15% x $5M pre-money = $750,000 (paper value)\n"
        "  Equity (at $20M):  15% x $20M exit = $3,000,000 (potential upside)\n\n"
        "  Total cash cost to the company: $180K-$270K over 18 months\n"
        "  Compared to hiring separately: $630K-$900K for the same period")

    # Impact on burn rate
    pdf.ln(2)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(*BLUE)
    pdf.cell(0, 6, "Impact on Burn Rate & Runway", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(*TEXT)
    pdf.txt(
        "  Current monthly burn:           $45,000\n"
        "  PMP contractor fee:           + $10,000 - $15,000\n"
        "  New monthly burn:               $55,000 - $60,000\n"
        "  Current cash on hand:           $320,000\n"
        "  Revised runway:                 5.3 - 5.8 months (down from ~7)\n\n"
        "This makes Lawrence's investment timing critical. If he invests $500K:\n"
        "  New cash:                       $820,000\n"
        "  Runway at $60K/month:           13.7 months (through 510(k) target)")

    # Phased fee structure
    pdf.add_page()
    pdf.sub("Proposed Phased Fee Schedule")
    pdf.txt(
        "Contractor fees can be phased to match project intensity and available cash:")

    phase_col = [40, 25, 30, 75]
    phase_headers = ["Phase", "Months", "Monthly Fee", "Focus"]
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(255, 255, 255)
    pdf.set_fill_color(*BLUE)
    for i, h in enumerate(phase_headers):
        pdf.cell(phase_col[i], 7, h, border=1, fill=True, align="C")
    pdf.ln()

    phases = [
        ("Phase 1", "M+0 to M+3", "$10,000", "Pre-Sub prep, IP transfer, Corp formation"),
        ("Phase 2", "M+3 to M+9", "$12,500", "510(k) drafting, investor outreach ramp"),
        ("Phase 3", "M+9 to M+15", "$15,000", "FDA submission, Series A fundraising"),
        ("Phase 4", "M+15 to M+18", "$12,500", "FDA review period, investor close"),
    ]
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(*TEXT)
    for i, (phase, months, fee, focus) in enumerate(phases):
        pdf.set_fill_color(250, 250, 255) if i % 2 == 0 else pdf.set_fill_color(255, 255, 255)
        pdf.cell(phase_col[0], 6, phase, border=1, fill=True)
        pdf.cell(phase_col[1], 6, months, border=1, fill=True, align="C")
        pdf.cell(phase_col[2], 6, fee, border=1, fill=True, align="C")
        pdf.cell(phase_col[3], 6, focus, border=1, fill=True)
        pdf.ln()

    pdf.ln(2)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(*TEXT)
    pdf.txt(
        "Total cash over 18 months at phased rates: ~$216,000\n"
        "This is 52-64% below market rate for equivalent services, with the\n"
        "gap compensated by the 15% equity stake.")

    # Legal structure
    pdf.ln(2)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(*BLUE)
    pdf.cell(0, 6, "Legal Structure", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(*TEXT)
    pdf.txt(
        "  Contracting Entity:   510k Bridge, Inc. (Delaware)\n"
        "  Engagement Type:      Independent contractor (Master Services Agreement)\n"
        "  Equity Grant:         Restricted Stock Agreement (Company B USA -> Lon Dailey)\n"
        "  IP Assignment:        All work product created under the MSA is assigned to\n"
        "                        Company B USA (standard work-for-hire clause)\n"
        "  Non-Compete:          None (PMP retains ability to take other contracts)\n"
        "  Confidentiality:      Mutual NDA covering all proprietary information\n"
        "  Termination:          Either party, 30-day written notice. Vested shares\n"
        "                        are retained; unvested shares are forfeited.")

    # Negotiation points
    pdf.ln(2)
    pdf.set_draw_color(*BLUE)
    pdf.set_fill_color(240, 243, 255)
    y = pdf.get_y()
    box_h = 42
    pdf.rect(pdf.l_margin, y, pdf.w - pdf.l_margin - pdf.r_margin, box_h, style="DF")
    pdf.set_xy(pdf.l_margin + 4, y + 3)
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(*BLUE)
    pdf.cell(0, 6, "Points to Discuss With Dr. Dai & Lawrence")
    pdf.set_xy(pdf.l_margin + 4, y + 11)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(*TEXT)
    comp_items = [
        "1. Is the 15% equity / $10-15K monthly blended model acceptable?",
        "2. Should contractor fees start immediately or after Lawrence invests?",
        "3. Does the phased fee schedule align with projected cash availability?",
        "4. Is Dr. Dai comfortable with a PMP who has equity (aligned incentives)?",
        "5. Does Lawrence want input on the PMP engagement terms?",
    ]
    for item in comp_items:
        pdf.set_x(pdf.l_margin + 6)
        pdf.cell(0, 5.5, f"  {item}", new_x="LMARGIN", new_y="NEXT")
    pdf.set_y(y + box_h + 4)
    pdf.notes_area()

    # ═══════════════════════════════════════
    # SECTION 7: Summary & Next Steps
    # ═══════════════════════════════════════
    pdf.add_page()
    pdf.sec(7, "Meeting Wrap-Up & Next Steps")
    pdf.txt(
        "Review the answers collected and confirm immediate action items.")

    pdf.sub("Key Decisions Needed After This Meeting:")
    items = [
        "1. Delaware C-Corp formation timeline and registered agent selection",
        "2. IP assignment agreement drafting (Oregon law, per R8 plan)",
        "3. Cap table / equity allocation term sheet",
        "4. Lawrence Liu's investment terms (amount, valuation, instrument)",
        "5. Dr. Dai employment/consulting agreement structure",
        "6. PMP engagement terms: equity grant + contractor fee schedule",
        "7. Communication cadence (weekly sync? Async via Q&A Board?)",
        "8. CFIUS considerations if Chinese investors take significant equity",
    ]
    for item in items:
        pdf.txt(item)

    pdf.ln(4)
    pdf.sub("Immediate Action Items:")
    pdf.txt("(Fill in during meeting)")
    pdf.notes_area()
    pdf.notes_area()
    pdf.notes_area()

    pdf.ln(4)
    pdf.sub("Notes:")
    pdf.notes_area()
    pdf.notes_area()
    pdf.notes_area()
    pdf.notes_area()

    path = os.path.join(OUT_DIR, "Meeting_Prep_DrDai_2026-03-23.pdf")
    pdf.output(path)
    return path


if __name__ == "__main__":
    p = build()
    print(f"Generated: {p}")
