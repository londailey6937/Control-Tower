#!/usr/bin/env python3
"""
Generate a comprehensive Investment & Fundraising Guide PDF
for medical device startups navigating the 510(k) pathway.
Covers term sheets, funding rounds, investor types, and timing.
"""

import os
from fpdf import FPDF

OUT = os.path.dirname(os.path.abspath(__file__))

_MAP = str.maketrans({
    "\u2014": "--", "\u2013": "-", "\u2019": "'", "\u201c": '"', "\u201d": '"',
    "\u2018": "'", "\u2265": ">=", "\u2264": "<=", "\u00b5": "u", "\u00d7": "x",
    "\u2022": "-", "\u2026": "...", "\u00ae": "(R)", "\u2192": "->",
})
def _a(s):
    return s.translate(_MAP)


class GuidePDF(FPDF):
    CARDINAL = (20, 60, 120)
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
        self.cell(0, 4, _a("Medical Device Startup Investment Guide  |  Term Sheets, Rounds & Fundraising Strategy"), align="R")
        self.ln(5)

    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(*self.GRAY)
        self.cell(0, 4, f"Page {self.page_no()}/{{nb}}", align="C")

    def section_heading(self, num, title, subtitle=""):
        self.add_page()
        self.set_fill_color(*self.CARDINAL)
        self.rect(self.l_margin, self.get_y(), self.w - self.l_margin - self.r_margin, 14, style="F")
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(*self.WHITE)
        self.set_x(self.l_margin + 4)
        self.cell(0, 14, _a(f"Section {num}:  {title}"))
        self.ln(16)
        if subtitle:
            self.set_font("Helvetica", "I", 9)
            self.set_text_color(*self.GRAY)
            self.cell(0, 5, _a(subtitle), new_x="LMARGIN", new_y="NEXT")
            self.ln(2)

    def sub_heading(self, text):
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

    def callout_box(self, text, style="key"):
        if style == "warn":
            self.set_fill_color(*self.WARN_BG)
            self.set_draw_color(*self.WARN_BORDER)
            self.set_text_color(160, 90, 0)
            prefix = "WARNING:  "
        else:
            self.set_fill_color(240, 250, 245)
            self.set_draw_color(*self.ACCENT)
            self.set_text_color(*self.ACCENT)
            prefix = "KEY INSIGHT:  "
        self.set_line_width(0.5)
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

    def table_row(self, cells, widths, bold_first=False, header=False):
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
    pdf = GuidePDF(orientation="P", unit="mm", format="Letter")
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.alias_nb_pages()

    # ── COVER PAGE ──────────────────────────────────
    pdf.add_page()
    pdf.ln(35)
    pdf.set_font("Helvetica", "B", 28)
    pdf.set_text_color(*GuidePDF.CARDINAL)
    pdf.cell(0, 12, _a("Investment & Fundraising"), align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 12, _a("Guide for Medical Device"), align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 12, _a("Startups"), align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(8)
    pdf.set_draw_color(*GuidePDF.CARDINAL)
    pdf.set_line_width(0.8)
    pdf.line(60, pdf.get_y(), 155, pdf.get_y())
    pdf.ln(8)
    pdf.set_font("Helvetica", "", 13)
    pdf.set_text_color(*GuidePDF.GRAY)
    pdf.cell(0, 7, _a("Term Sheets, Funding Rounds, Valuation,"), align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 7, _a("and the 510(k) Bridge Strategy"), align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(30)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(*GuidePDF.DARK)
    pdf.cell(0, 6, _a("Arch Medical Management"), align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 6, _a("Pilot Software LLC dba Arch Medical Management"), align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 6, _a("March 2026"), align="C", new_x="LMARGIN", new_y="NEXT")

    # ── SECTION 1: FUNDING ROUNDS ──────────────────
    pdf.section_heading(1, "Funding Rounds", "How startup financing evolves from idea to IPO")

    pdf.body("Startup fundraising happens in sequential 'rounds,' each with a distinct purpose, investor type, and typical valuation range. For medical device companies, the regulatory pathway (510(k), De Novo, PMA) heavily influences timing and size of each round.")

    pdf.sub_heading("Pre-Seed")
    pdf.body("The earliest stage. Founders use personal savings, friends & family money, or small grants to prove the concept is worth pursuing.")
    pdf.bullet("$25K - $500K typical", "Amount: ")
    pdf.bullet("Founders, friends & family, university grants, SBIR/STTR Phase I", "Sources: ")
    pdf.bullet("None or very early (pre-product, concept only)", "Valuation: ")
    pdf.bullet("Proof of concept, initial IP filing, preliminary market research", "Use of Funds: ")
    pdf.callout_box("For medical devices, pre-seed often funds the initial predicate device research, feasibility prototyping, and provisional patent filings. No FDA interaction yet.")

    pdf.sub_heading("Seed Round")
    pdf.body("The first 'real' fundraising round. You have a working prototype or strong technical data and need capital to advance toward regulatory submission.")
    pdf.bullet("$500K - $3M typical for medical devices", "Amount: ")
    pdf.bullet("Angel investors, angel groups, micro-VCs, accelerators (Y Combinator, HAX, TMCx)", "Sources: ")
    pdf.bullet("$2M - $10M pre-money valuation", "Valuation: ")
    pdf.bullet("Design verification testing, Pre-Submission meeting (FDA), bench testing, initial clinical data", "Use of Funds: ")
    pdf.bullet("SAFE notes, convertible notes, or priced equity rounds", "Structure: ")
    pdf.callout_box("This is the sweet spot for 510(k) device companies. Seed capital funds the Pre-Sub through submission -- the most capital-efficient stretch of the regulatory pathway.")

    pdf.sub_heading("Series A")
    pdf.body("The first institutional venture capital round. Typically raised after significant de-risking -- for medtech, this often means FDA clearance or submission.")
    pdf.bullet("$3M - $15M typical", "Amount: ")
    pdf.bullet("Venture capital firms (medtech-focused: MedTech Ventures, Gilde Healthcare, Hatteras Venture Partners)", "Sources: ")
    pdf.bullet("$10M - $40M pre-money valuation", "Valuation: ")
    pdf.bullet("Commercial launch, sales team buildout, QMS implementation, manufacturing scale-up", "Use of Funds: ")
    pdf.bullet("Board seat for lead investor, preferred stock with protective provisions", "Key Term: ")

    pdf.sub_heading("Series B and Beyond")
    pdf.body("Growth-stage financing for companies with proven product-market fit and revenue traction.")
    pdf.bullet("$15M - $50M+ typical", "Amount: ")
    pdf.bullet("Growth-stage VCs, strategic investors (J&J Innovation, Medtronic Ventures, GE Healthcare Ventures)", "Sources: ")
    pdf.bullet("Sales expansion, international regulatory (CE marking, NMPA), next-gen product development", "Use of Funds: ")

    pdf.sub_heading("Funding Rounds Summary Table")
    w = [30, 28, 40, 40, 52]
    pdf.table_row(["Round", "Amount", "Valuation", "Investors", "MedTech Milestone"], w, header=True)
    pdf.table_row(["Pre-Seed", "$25K-500K", "Pre-valuation", "F&F, Grants", "Concept, IP filing"], w, bold_first=True)
    pdf.table_row(["Seed", "$500K-3M", "$2-10M pre", "Angels, Micro-VC", "Pre-Sub to 510(k) filing"], w, bold_first=True)
    pdf.table_row(["Series A", "$3-15M", "$10-40M pre", "VC firms", "FDA clearance, launch"], w, bold_first=True)
    pdf.table_row(["Series B", "$15-50M+", "$40-150M+", "Growth VC", "Scale, international"], w, bold_first=True)

    # ── SECTION 2: TERM SHEETS ─────────────────────
    pdf.section_heading(2, "Term Sheets", "The blueprint of a deal -- what every clause means and why it matters")

    pdf.body("A term sheet is a non-binding document that outlines the key financial and governance terms of an investment. It is typically issued by the lead investor after initial due diligence and before the definitive legal documents are drafted. Think of it as a 'letter of intent' for investment.")

    pdf.sub_heading("Economics Terms")
    pdf.body("These terms determine how much the company is worth and how returns are distributed.")

    pdf.bullet("The company's worth before new investment money comes in. If your pre-money valuation is $5M and an investor puts in $1M, the post-money valuation is $6M and the investor owns 1/6 (16.7%) of the company.", "Pre-Money Valuation: ")
    pdf.bullet("Pre-money + new investment = post-money. Your ownership percentage is calculated from the post-money number. Always negotiate on pre-money.", "Post-Money Valuation: ")
    pdf.bullet("The price per share the investor pays. Calculated as pre-money valuation divided by total shares outstanding (including the option pool).", "Price Per Share: ")
    pdf.bullet("A reserved pool of shares (typically 10-20% of post-money) set aside for future employee stock options. CRITICAL: Investors usually insist the option pool comes from the pre-money valuation, which effectively lowers the true pre-money for founders.", "Option Pool: ")

    pdf.callout_box("The option pool shuffle is one of the most important dynamics to understand. A $5M pre-money with a 20% option pool carved from pre-money is effectively a $4M pre-money valuation for the founders. Always model the dilution both ways.", style="warn")

    pdf.sub_heading("Liquidation Preference")
    pdf.body("Liquidation preference determines who gets paid first (and how much) when the company is sold, merged, or liquidated. This is the single most important economic term besides valuation.")

    pdf.bullet("1x non-participating preferred: The investor gets their money back OR converts to common stock and shares pro-rata. This is the most founder-friendly version.", "1x Non-Participating: ")
    pdf.bullet("1x participating preferred: The investor gets their money back FIRST, then also shares in the remaining proceeds pro-rata. This is a 'double dip' -- the investor gets paid twice.", "1x Participating: ")
    pdf.bullet("2x or 3x preference means the investor gets 2x or 3x their investment back before common shareholders see a penny. Avoid if possible.", "Multiple Preferences: ")

    pdf.callout_box("Example: Investor puts in $2M for 20% at 1x participating preferred. Company sells for $10M. Investor gets $2M back (preference) + 20% of remaining $8M ($1.6M) = $3.6M total. Founders/common get $6.4M. With 1x non-participating, investor would choose to convert: 20% of $10M = $2M. Same result here, but at a $50M exit the participating preferred investor gets $2M + 20%($48M) = $11.6M vs. just $10M non-participating.")

    pdf.sub_heading("Anti-Dilution Protection")
    pdf.body("Protects investors if the company raises a future round at a lower valuation (a 'down round'). The investor's conversion price is adjusted downward, giving them more shares.")

    pdf.bullet("The conversion price is recalculated using a weighted average formula that accounts for the size of the down round relative to total shares. This is the standard and more founder-friendly approach.", "Weighted Average (Broad-Based): ")
    pdf.bullet("The conversion price drops to the new lower price -- as if the investor had invested at the lower valuation. Very investor-friendly and punitive to founders. Rare in modern deals.", "Full Ratchet: ")

    pdf.sub_heading("Governance & Control Terms")

    pdf.bullet("Investors (especially Series A leads) typically get one board seat. Common structure: 2 founders + 1 investor + 1 independent = 4-member board. Be cautious about giving investors board majority.", "Board Seats: ")
    pdf.bullet("Specific actions that require investor approval regardless of board vote. Typical protective provisions: new share issuance, sale of company, changes to charter, taking on debt above a threshold, hiring/firing CEO.", "Protective Provisions: ")
    pdf.bullet("If a majority of investors want to sell the company, they can force all shareholders (including founders) to agree. Usually requires 50-67% of preferred to trigger.", "Drag-Along Rights: ")
    pdf.bullet("Investors can participate in future rounds to maintain their ownership percentage. Standard and generally non-controversial.", "Pro-Rata Rights: ")
    pdf.bullet("In a future IPO or acquisition, investors with registration rights can require the company to include their shares in the registration. Standard provision.", "Registration Rights: ")

    pdf.sub_heading("Founder-Specific Terms")

    pdf.bullet("Even though founders already 'own' their shares, investors often require founder shares to be subject to vesting (typically 4 years with a 1-year cliff). This protects against a founder leaving early. Common compromise: credit founders for time already spent (e.g., 1 year of vesting already earned).", "Founder Vesting: ")
    pdf.bullet("Founders commit to work full-time on the company and not compete with it during or for some period after employment. 1-2 years post-departure is standard; longer is aggressive.", "Non-Compete / Non-Solicit: ")
    pdf.bullet("All intellectual property created by founders related to the company's business is assigned to the company. Essential and non-negotiable.", "IP Assignment: ")
    pdf.bullet("Prevents shareholders (founders and investors) from selling shares without company/board approval. Typical for private companies until IPO.", "Right of First Refusal (ROFR): ")

    pdf.sub_heading("Term Sheet Red Flags")
    w2 = [55, 135]
    pdf.table_row(["Red Flag", "Why It Matters"], w2, header=True)
    pdf.table_row(["Full ratchet anti-dilution", "Severely punishes founders in any down round"], w2, bold_first=True)
    pdf.table_row(["Participating preferred >1x", "Double-dip: investor gets money back + share of upside"], w2, bold_first=True)
    pdf.table_row(["Investor board majority", "Founders lose control of strategic decisions"], w2, bold_first=True)
    pdf.table_row(["Excessive protective provisions", "Investor has veto power over routine operations"], w2, bold_first=True)
    pdf.table_row(["No-shop clause >60 days", "Locks you out of talking to other investors too long"], w2, bold_first=True)
    pdf.table_row(["Cumulative dividends", "Investment grows at 8%+ annually before founders see returns"], w2, bold_first=True)
    pdf.table_row(["Multiple liquidation pref (2x+)", "Investors recover 2-3x before common shareholders receive anything"], w2, bold_first=True)

    # ── SECTION 3: VALUATION ───────────────────────
    pdf.section_heading(3, "Valuation Methods", "How medical device startups are valued at each stage")

    pdf.body("Valuation is more art than science for early-stage medical device companies. Unlike SaaS startups with predictable MRR metrics, medtech valuations are heavily driven by regulatory milestones and clinical risk.")

    pdf.sub_heading("Pre-Revenue Valuation Approaches")

    pdf.bullet("Value = total addressable market for the device category, discounted by probability of FDA clearance, time to market, and competition. A $1B TAM with 70% probability of clearance and 24-month timeline might support a $5-10M pre-money at seed.", "Risk-Adjusted Market Approach: ")
    pdf.bullet("Compare to similar medtech companies at the same stage. Recent public data from similar 510(k) device companies that raised seed rounds. Adjust for your specific indication and market size.", "Comparable Transactions: ")
    pdf.bullet("What would a strategic acquirer pay for this technology? For 510(k) devices, acquirers typically pay 3-8x revenue (post-clearance) or $20-50M+ for cleared devices with initial revenue. Work backward from exit to determine a fair entry valuation.", "Acquisition Comps / Exit Analysis: ")
    pdf.bullet("Investors target a specific return (e.g., 10x in 7 years). If they expect a $100M exit and want 10x, they'll invest $1M-$2M at a $10M post-money for 10-20% ownership.", "VC Method: ")

    pdf.sub_heading("Valuation Step-Ups by Milestone")
    pdf.body("Medical device valuations increase in a staircase pattern, with each regulatory milestone creating a 'step-up' in value:")
    w3 = [50, 40, 48, 52]
    pdf.table_row(["Milestone", "Typical Step-Up", "Pre-Money Range", "Why"], w3, header=True)
    pdf.table_row(["Concept/Patent", "Baseline", "$1-3M", "Idea risk, no FDA contact"], w3, bold_first=True)
    pdf.table_row(["Pre-Sub Filed", "+30-50%", "$2-5M", "FDA engagement signal"], w3, bold_first=True)
    pdf.table_row(["Pre-Sub Feedback", "+50-80%", "$4-8M", "Regulatory de-risked"], w3, bold_first=True)
    pdf.table_row(["510(k) Submitted", "+100-200%", "$6-15M", "Submission = inflection"], w3, bold_first=True)
    pdf.table_row(["510(k) Cleared", "+200-400%", "$10-30M", "Market-ready device"], w3, bold_first=True)
    pdf.table_row(["First Revenue", "+300-500%", "$15-50M", "Product-market fit"], w3, bold_first=True)

    pdf.callout_box("The single biggest valuation jump in medtech is from '510(k) Submitted' to '510(k) Cleared.' This is why strategic fundraising BEFORE clearance gives investors the best return and gives founders the most favorable entry point for their cap table.")

    # ── SECTION 4: INVESTMENT VEHICLES ─────────────
    pdf.section_heading(4, "Investment Vehicles", "SAFEs, convertible notes, and priced rounds explained")

    pdf.sub_heading("SAFE (Simple Agreement for Future Equity)")
    pdf.body("Created by Y Combinator. A SAFE is not debt -- it's a contract that gives the investor the right to receive equity in a future priced round. No interest, no maturity date.")
    pdf.bullet("Investor gets equity at the lower of: (a) the valuation cap, or (b) a discount to the next round's price", "How it works: ")
    pdf.bullet("The maximum valuation at which the SAFE converts. Example: $5M cap means no matter how high the Series A valuation, the SAFE investor converts at $5M.", "Valuation Cap: ")
    pdf.bullet("Typically 15-25%. If the Series A is at $10M pre-money and the SAFE has a 20% discount, the SAFE investor converts at $8M.", "Discount Rate: ")
    pdf.bullet("Simple, fast (one document), no interest accrual, no maturity date pressure. Standard for pre-seed and seed.", "Pros: ")
    pdf.bullet("No investor rights until conversion, dilution is uncertain until priced round, can stack up multiple SAFEs creating a 'SAFE pile' problem.", "Cons: ")

    pdf.sub_heading("Convertible Notes")
    pdf.body("Convertible notes are short-term debt that converts to equity. Unlike SAFEs, they accrue interest and have a maturity date.")
    pdf.bullet("Typically 4-8% annually. Interest converts to equity along with principal.", "Interest Rate: ")
    pdf.bullet("Typically 18-24 months. If no priced round occurs by maturity, the note is technically due -- creating potential for conflict.", "Maturity Date: ")
    pdf.bullet("Same as SAFEs: valuation cap and/or discount to the next priced round.", "Conversion: ")
    pdf.bullet("More investor protection than SAFEs (it's debt). Some investors prefer the forced conversion timeline.", "Pros: ")
    pdf.bullet("Interest accrual costs you equity. Maturity date creates pressure. More complex legally than a SAFE.", "Cons: ")
    pdf.callout_box("For medical device startups, convertible notes can be risky because FDA timelines are unpredictable. If your 510(k) review takes longer than expected and the note matures before your priced round, you may face a forced repayment or unfavorable renegotiation.", style="warn")

    pdf.sub_heading("Priced Equity Round (Preferred Stock)")
    pdf.body("A priced round sets a specific valuation, price per share, and creates a new class of preferred stock with defined rights. This is the standard structure for Series A and beyond.")
    pdf.bullet("Definitive legal documents: Stock Purchase Agreement, Investors' Rights Agreement, Right of First Refusal, Voting Agreement, Certificate of Incorporation amendment.", "Key Documents: ")
    pdf.bullet("$15K-$50K+ in legal fees for a standard Series A. Both sides typically have counsel.", "Legal Costs: ")
    pdf.bullet("Clean cap table, clear governance, investor rights codified. Required for institutional VC investment.", "Pros: ")
    pdf.bullet("Expensive, time-consuming (4-8 weeks to close), requires board approval and shareholder consent.", "Cons: ")

    pdf.sub_heading("Vehicle Comparison")
    w4 = [35, 45, 45, 65]
    pdf.table_row(["Feature", "SAFE", "Conv. Note", "Priced Round"], w4, header=True)
    pdf.table_row(["Legal Cost", "$0-2K", "$2-5K", "$15-50K+"], w4, bold_first=True)
    pdf.table_row(["Time to Close", "Days", "1-2 weeks", "4-8 weeks"], w4, bold_first=True)
    pdf.table_row(["Interest", "None", "4-8%/yr", "N/A"], w4, bold_first=True)
    pdf.table_row(["Maturity Date", "None", "18-24 months", "N/A"], w4, bold_first=True)
    pdf.table_row(["Valuation Set?", "Deferred", "Deferred", "Yes, fixed"], w4, bold_first=True)
    pdf.table_row(["Board Seat", "No", "Sometimes", "Yes (lead)"], w4, bold_first=True)
    pdf.table_row(["Best For", "Pre-Seed/Seed", "Seed/Bridge", "Series A+"], w4, bold_first=True)

    # ── SECTION 5: INVESTOR TYPES ──────────────────
    pdf.section_heading(5, "Investor Types", "Who invests in medical devices and what they expect")

    pdf.sub_heading("Angel Investors")
    pdf.body("High-net-worth individuals who invest their own money. Often former executives, physicians, or entrepreneurs with domain expertise.")
    pdf.bullet("$25K - $250K per investment", "Check Size: ")
    pdf.bullet("Pre-seed and seed", "Stage: ")
    pdf.bullet("Personal experience, mentor relationship, belief in the founder. Often invest on less formal terms.", "Motivation: ")
    pdf.bullet("Can be slow decision-makers, limited follow-on capital, may not add strategic value.", "Watch Out: ")

    pdf.sub_heading("Angel Groups / Syndicates")
    pdf.body("Organized groups of angels who pool capital and share due diligence. Examples: Oregon Angel Fund, Alliance of Angels, Tech Coast Angels, Life Science Angels.")
    pdf.bullet("$100K - $1M per investment (pooled)", "Check Size: ")
    pdf.bullet("Seed", "Stage: ")
    pdf.bullet("Formal pitch process, group vote, more structured terms than individual angels.", "Process: ")
    pdf.bullet("Usually one representative on the board or as observer.", "Governance: ")

    pdf.sub_heading("Venture Capital (VC)")
    pdf.body("Professional investment firms that manage pools of capital (funds) from limited partners (LPs). Medtech-focused VCs understand FDA timelines and regulatory risk.")
    pdf.bullet("$1M - $25M+ per investment", "Check Size: ")
    pdf.bullet("Series A and beyond (some do seed)", "Stage: ")
    pdf.bullet("Board seat, active governance, follow-on investment, exit-focused (5-7 year horizon)", "Expectations: ")
    pdf.bullet("High return expectations (3-5x fund return). Will push for growth, sometimes at expense of founder control.", "Watch Out: ")

    pdf.sub_heading("Strategic Investors (Corporate VC)")
    pdf.body("Investment arms of large medical device companies: J&J Innovation, Medtronic Ventures, GE Healthcare Ventures, Philips Health Technology Ventures, Baxter Ventures.")
    pdf.bullet("$2M - $20M per investment", "Check Size: ")
    pdf.bullet("Series A-B, sometimes seed for highly strategic technologies", "Stage: ")
    pdf.bullet("Access to distribution channels, clinical sites, regulatory expertise, potential acquisition path.", "Upside: ")
    pdf.bullet("May want technology access rights, right of first refusal on acquisition, or exclusive licensing. Can scare off other acquirers.", "Watch Out: ")
    pdf.callout_box("Strategic investors can be a double-edged sword. A Medtronic Ventures investment signals validation but may discourage J&J or Abbott from acquiring you. Negotiate carefully around ROFR and information rights.")

    pdf.sub_heading("Government / Non-Dilutive Funding")
    pdf.bullet("Phase I ($275K, 6-9 months) for feasibility, Phase II ($1-2M, 2 years) for development. Highly competitive but non-dilutive.", "NIH SBIR/STTR: ")
    pdf.bullet("Phase I ($200K), Phase II ($1.1M). Good for dual-use medical technologies.", "NSF SBIR: ")
    pdf.bullet("BARDA and ASPR for medical countermeasures. Large awards ($5-25M) but very specific use cases.", "BARDA: ")
    pdf.bullet("Oregon SBIR matching grants, Oregon Innovation Council, state venture funds.", "State Programs: ")
    pdf.callout_box("Non-dilutive funding should always be pursued in parallel with equity fundraising. An SBIR grant does not dilute your cap table and signals government validation of the technology.")

    # ── SECTION 6: 510(k) BRIDGE ───────────────────
    pdf.section_heading(6, "The 510(k) Bridge Strategy", "When to engage investors relative to your regulatory milestones")

    pdf.body("The 510(k) regulatory pathway creates natural inflection points that directly impact your fundraising leverage. Understanding when to engage investors relative to each milestone is crucial for optimizing valuation and terms.")

    pdf.sub_heading("The Investor Outreach Timeline")
    pdf.body("Not all months are created equal for fundraising. Here is the optimal engagement cadence mapped to a standard 510(k) timeline:")

    pdf.ln(2)
    w5 = [14, 33, 12, 45, 86]
    pdf.table_row(["Month", "Milestone", "Signal", "Investor Action", "Why This Timing"], w5, header=True)
    pdf.table_row(["M+0", "Pre-Sub Filed", "Warm", "Build relationships", "FDA engagement proves you're serious -- not just ideas"], w5, bold_first=True)
    pdf.table_row(["M+2", "Pre-Sub Meeting", "Active", "Pitch meetings", "FDA feedback letter is your best fundraising asset"], w5, bold_first=True)
    pdf.table_row(["M+3", "Bench Testing", "Active", "Share data", "IEC 60601, EMC, usability data proves technical viability"], w5, bold_first=True)
    pdf.table_row(["M+6", "510(k) Filed", "Peak", "Push term sheets", "Submission is the inflection -- clearance is 'when' not 'if'"], w5, bold_first=True)
    pdf.table_row(["M+9", "510(k) Cleared", "Close", "Close rounds", "Maximum leverage -- cleared, market-ready device"], w5, bold_first=True)

    pdf.sub_heading("Why M+2 to M+6 is the Sweet Spot")
    pdf.body("The period between your FDA Pre-Submission meeting feedback (M+2) and 510(k) filing (M+6) is the optimal fundraising window for three reasons:")
    pdf.bullet("The FDA feedback letter from R2 is a tangible, third-party validation that your regulatory strategy is sound. This is the single most persuasive document you can show investors.", "1. Regulatory De-Risking: ")
    pdf.bullet("Before clearance, your valuation is still 'pre-event.' Investors who come in before the 510(k) is cleared get the pre-clearance price -- typically 40-60% lower than post-clearance. This is the return they're buying.", "2. Favorable Valuation: ")
    pdf.bullet("At M+6 when the 510(k) is submitted, you're 90 days from clearance (standard review). This is close enough that investors can see the finish line but early enough to get in at pre-clearance terms.", "3. Visible Finish Line: ")

    pdf.callout_box("The #1 mistake medtech founders make is waiting until AFTER clearance to fundraise. Post-clearance fundraising gives you better terms but costs 6-12 months of commercial runway. The capital you need for launch should be committed BEFORE the clearance letter arrives.")

    pdf.sub_heading("What Investors Want to See at Each Stage")

    pdf.body("Your pitch materials should evolve as you progress through the regulatory timeline:")

    pdf.bullet("Vision + technical approach, IP landscape, team credentials, TAM/SAM analysis. Pre-Sub filing shows FDA engagement.", "M+0 (Pre-Sub Filed): ")
    pdf.bullet("ALL of the above + FDA feedback letter (the 'de-risking document'), proposed testing protocol with FDA agreement, competitive landscape with predicate device comparison.", "M+2 (Pre-Sub Meeting): ")
    pdf.bullet("ALL of the above + IEC 60601 test reports, EMC data, clinical validation protocol/early results, design freeze documentation.", "M+3 (Bench Testing): ")
    pdf.bullet("ALL of the above + complete 510(k) submission summary, timeline to clearance (90 days), launch plan, revenue projections, first KOL commitments.", "M+6 (510(k) Filed): ")
    pdf.bullet("ALL of the above + clearance letter, K-number, post-market plan, commercial traction, first purchase orders or LOIs.", "M+9 (Cleared): ")

    # ── SECTION 7: DUE DILIGENCE ───────────────────
    pdf.section_heading(7, "Investor Due Diligence", "What investors investigate before writing a check")

    pdf.body("Due diligence ('DD') is the investigation process investors conduct before finalizing an investment. For medical devices, DD is more rigorous than typical tech startups because of regulatory, clinical, and manufacturing risks.")

    pdf.sub_heading("Technical / Product DD")
    pdf.bullet("Working prototype vs. concept? Design freeze status? Verification and validation testing complete?", "Product Maturity: ")
    pdf.bullet("Patents (filed vs. granted), trade secrets, freedom-to-operate analysis. Has an FTO search been done?", "IP Portfolio: ")
    pdf.bullet("Is it cleared/approved? What pathway? What did FDA say in the Pre-Sub? Any known issues?", "Regulatory Status: ")
    pdf.bullet("Bill of materials, contract manufacturer identified? Can this be manufactured at scale? What are the COGS?", "Manufacturing: ")

    pdf.sub_heading("Market DD")
    pdf.bullet("Total addressable market with credible bottom-up analysis, not just top-down TAM numbers.", "Market Size: ")
    pdf.bullet("Reimbursement pathway (CPT codes, hospital budget vs. physician preference item), willingness to pay.", "Reimbursement: ")
    pdf.bullet("Existing devices, emerging competitors, barrier to entry analysis.", "Competition: ")
    pdf.bullet("Clinician and hospital interest, letters of intent, KOL relationships.", "Clinical Champions: ")

    pdf.sub_heading("Team DD")
    pdf.bullet("Regulatory affairs experience, prior FDA submissions, clinical/engineering depth.", "Domain Expertise: ")
    pdf.bullet("Full-time commitment, vesting schedules, founder agreement in place.", "Founder Commitment: ")
    pdf.bullet("Key hires needed, advisory board composition, gaps in expertise.", "Team Gaps: ")

    pdf.sub_heading("Financial DD")
    pdf.bullet("Existing cap table, prior investments, outstanding SAFEs/notes.", "Cap Table: ")
    pdf.bullet("Monthly burn rate, runway at current spend, detailed use-of-proceeds for this round.", "Burn Rate & Runway: ")
    pdf.bullet("Revenue model, pricing strategy, path to profitability, unit economics.", "Financial Projections: ")

    pdf.sub_heading("Legal DD")
    pdf.bullet("Clean corporate structure, no outstanding litigation, proper entity formation.", "Corporate: ")
    pdf.bullet("IP assignment agreements, employee invention agreements, NDA/NCA obligations.", "IP Ownership: ")
    pdf.bullet("QMS in place (ISO 13485), complaint handling, MDR reporting procedures.", "Regulatory Compliance: ")

    # ── SECTION 8: NEGOTIATION ─────────────────────
    pdf.section_heading(8, "Negotiation Strategy", "Practical tactics for medical device founders")

    pdf.sub_heading("Before the Negotiation")
    pdf.bullet("Talk to 15-25 investors simultaneously. Competition creates leverage. Never negotiate with a single interested party.", "Create Competition: ")
    pdf.bullet("Research the investor's portfolio, fund size, and recent deals. A $50M fund writing $1M checks behaves differently than a $500M fund.", "Know Your Investor: ")
    pdf.bullet("Be clear on your BATNA (Best Alternative to Negotiated Agreement). What happens if this deal falls through? More options = more power.", "Know Your BATNA: ")

    pdf.sub_heading("Key Negotiation Points (Prioritized)")
    pdf.body("Not all terms are equally important. Focus your negotiation energy on the terms that matter most:")
    pdf.bullet("This directly determines your ownership. Fight hardest here.", "1. Valuation (highest priority): ")
    pdf.bullet("1x non-participating is standard. Push back hard on participating preferred or >1x multiples.", "2. Liquidation Preference: ")
    pdf.bullet("Maintain founder-friendly board composition. 2 founders + 1 investor + 1 independent is ideal.", "3. Board Composition: ")
    pdf.bullet("Insist on broad-based weighted average. Reject full ratchet.", "4. Anti-Dilution: ")
    pdf.bullet("Ensure the option pool is the right size but push for it to come from post-money, not pre-money.", "5. Option Pool: ")
    pdf.bullet("Standard and not worth fighting. Accept reasonable protective provisions.", "6. Pro-Rata Rights (lower priority): ")

    pdf.sub_heading("Common Mistakes")
    pdf.bullet("The first investor to see your deal should not be your top-choice lead. Practice your pitch with lower-priority investors first.", "Showing Your Best Card First: ")
    pdf.bullet("Fundraising takes 3-6 months for medtech. Start early, especially around regulatory milestones.", "Waiting Too Long to Start: ")
    pdf.bullet("Get startup-experienced legal counsel (not your family attorney). Wilson Sonsini, Cooley, Fenwick -- or local equivalents.", "Skipping Legal Counsel: ")
    pdf.bullet("In medtech, a credible 510(k) timeline is more persuasive than hockey-stick revenue projections. Lead with regulatory progress.", "Overemphasizing Revenue Projections: ")

    pdf.callout_box("The best fundraising position is when you don't desperately need the money. Start fundraising with 6+ months of runway remaining. Negotiating from a position of need always leads to worse terms.")

    # ── SECTION 9: CAP TABLE ───────────────────────
    pdf.section_heading(9, "Cap Table Management", "Understanding ownership dilution through multiple rounds")

    pdf.body("Your capitalization table ('cap table') tracks who owns what percentage of the company. Understanding how it evolves is essential for making informed fundraising decisions.")

    pdf.sub_heading("Example: 510(k) Medical Device Startup Cap Table Evolution")

    pdf.body("Starting point: Two co-founders, 50/50 split, 10M authorized shares.")

    w6 = [50, 30, 30, 30, 50]
    pdf.table_row(["Shareholder", "Founding", "Post-Seed", "Post-Series A", "Notes"], w6, header=True)
    pdf.table_row(["Founder A", "50.0%", "37.5%", "28.1%", "CEO - full vesting"], w6, bold_first=True)
    pdf.table_row(["Founder B", "50.0%", "37.5%", "28.1%", "CTO - full vesting"], w6, bold_first=True)
    pdf.table_row(["Seed Investors", "--", "15.0%", "11.3%", "SAFE, $1M at $6M cap"], w6, bold_first=True)
    pdf.table_row(["Option Pool", "--", "10.0%", "12.5%", "Refreshed at Series A"], w6, bold_first=True)
    pdf.table_row(["Series A Lead", "--", "--", "20.0%", "$3M at $12M pre-money"], w6, bold_first=True)
    pdf.table_row(["Total", "100%", "100%", "100%", ""], w6, bold_first=True)

    pdf.body("Key observations:")
    pdf.bullet("Founders go from 100% to 56.2% combined after two rounds. This is normal and healthy.", "Dilution is expected: ")
    pdf.bullet("56.2% of a $15M company ($8.4M) is better than 100% of a $2M company.", "Dilution is not loss: ")
    pdf.bullet("Each round dilutes all previous shareholders proportionally (unless they exercise pro-rata rights).", "Every round dilutes everyone: ")

    pdf.callout_box("A useful mental model: founders who keep 40-60% after seed and 25-40% after Series A are in a strong position. If you're below 20% combined before Series B, you may have given up too much too early.")

    # ── SECTION 10: GLOSSARY ───────────────────────
    pdf.section_heading(10, "Glossary", "Essential investment terminology")

    terms = [
        ("Anti-Dilution", "Protection for investors against lower-valuation future rounds. Adjusts conversion price."),
        ("BATNA", "Best Alternative to Negotiated Agreement. Your fallback if the deal falls through."),
        ("Bridge Round", "Small round of financing between major rounds, often using convertible notes."),
        ("Burn Rate", "Monthly cash expenditure. Gross burn = total spend. Net burn = spend minus revenue."),
        ("Cap Table", "Capitalization table showing all equity ownership, options, warrants, and convertible instruments."),
        ("Cliff", "Minimum time (usually 1 year) before any shares vest."),
        ("Convertible Note", "Short-term debt that converts to equity at a future priced round."),
        ("Down Round", "A financing round at a lower valuation than the previous round."),
        ("Drag-Along", "Right allowing majority shareholders to force minority shareholders into a sale."),
        ("Due Diligence", "Investigation conducted by investors before finalizing investment."),
        ("Equity", "Ownership in the company, represented by shares of stock."),
        ("Exit", "Liquidity event: acquisition, IPO, or secondary sale."),
        ("Fully Diluted", "Total shares counting all options, warrants, and convertible instruments as if exercised."),
        ("Lead Investor", "The investor who sets terms, does primary DD, and often takes a board seat."),
        ("Liquidation Preference", "Order and amount of payout to shareholders in a sale or liquidation."),
        ("Lock-Up Period", "Time after IPO during which insiders cannot sell shares (typically 180 days)."),
        ("Non-Dilutive", "Funding (grants, revenue) that doesn't give up equity."),
        ("Option Pool", "Shares reserved for future employee equity grants."),
        ("Pari Passu", "Equal treatment -- investors in the same class share proceeds equally."),
        ("Post-Money", "Company valuation including the new investment."),
        ("Pre-Money", "Company valuation before the new investment."),
        ("Preferred Stock", "Stock class with additional rights (liquidation pref, anti-dilution, etc.) over common."),
        ("Pro-Rata Right", "Right to invest in future rounds to maintain ownership percentage."),
        ("ROFR", "Right of First Refusal -- company can match any outside offer for shares."),
        ("Runway", "Months of operation remaining at current burn rate."),
        ("SAFE", "Simple Agreement for Future Equity. Converts to stock at a future priced round."),
        ("Secondary Sale", "Sale of existing shares (not new issuance) between shareholders."),
        ("Tag-Along", "Right of minority shareholders to join a sale on the same terms."),
        ("Term Sheet", "Non-binding outline of key investment terms."),
        ("Vesting", "Gradual earning of equity over time (typically 4 years for employees/founders)."),
    ]

    for label, definition in terms:
        pdf.bullet(definition, f"{label}: ")

    # ── WRITE FILE ─────────────────────────────────
    path = os.path.join(OUT, "Investment_Fundraising_Guide.pdf")
    pdf.output(path)
    print(f"PDF generated: {path}")
    return path


if __name__ == "__main__":
    build()
