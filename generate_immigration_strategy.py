#!/usr/bin/env python3
"""
Generate a dual-path immigration strategy PDF:
  Path A: Danielle Liu as EB-5 investor (with Malei as derivative)
  Path B: Lawrence & Lisa Liu via EB-1C Multinational Manager transfer
"""

import os
from datetime import date
from fpdf import FPDF

OUT_DIR = os.path.dirname(os.path.abspath(__file__))

NAVY = (10, 40, 100)
TEXT = (40, 40, 45)
GRAY = (120, 120, 130)
WHITE = (255, 255, 255)
LIGHT_BG = (245, 247, 252)
GREEN = (20, 120, 60)


class StrategyPDF(FPDF):

    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(*GRAY)
        self.cell(0, 5, "CONFIDENTIAL", align="R")
        self.ln(7)

    def footer(self):
        self.set_y(-13)
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(*GRAY)
        self.cell(0, 5, f"Page {self.page_no()}/{{nb}}", align="C")

    def sec(self, title):
        if self.get_y() > self.h - 40:
            self.add_page()
        self.ln(3)
        self.set_font("Helvetica", "B", 12)
        self.set_text_color(*NAVY)
        self.cell(0, 7, title, new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(*NAVY)
        self.set_line_width(0.4)
        self.line(self.l_margin, self.get_y(),
                  self.w - self.r_margin, self.get_y())
        self.ln(4)

    def sub(self, title):
        self.set_font("Helvetica", "B", 10.5)
        self.set_text_color(*NAVY)
        self.cell(0, 6, title, new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def txt(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*TEXT)
        self.multi_cell(0, 5.5, text, new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def green_txt(self, text):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(*GREEN)
        self.multi_cell(0, 5.5, text, new_x="LMARGIN", new_y="NEXT")
        self.set_text_color(*TEXT)
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

    def table(self, headers, rows, col_w):
        # Check if table fits on current page
        needed = 7 + len(rows) * 6 + 10
        if self.get_y() + needed > self.h - 20:
            self.add_page()
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*WHITE)
        self.set_fill_color(*NAVY)
        for i, h in enumerate(headers):
            self.cell(col_w[i], 7, h, border=1, fill=True, align="C")
        self.ln()
        self.set_text_color(*TEXT)
        for ri, row in enumerate(rows):
            self.set_font("Helvetica", "", 9)
            bg = LIGHT_BG if ri % 2 == 0 else WHITE
            self.set_fill_color(*bg)
            for ci, val in enumerate(row):
                align = "L" if ci == 0 else "C"
                self.cell(col_w[ci], 6, val, border=1, fill=True, align=align)
            self.ln()
        self.ln(3)


def build():
    pdf = StrategyPDF("P", "mm", "Letter")
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.set_margins(22, 18, 22)

    # ── PAGE 1: LETTERHEAD ────────────────────────
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 18)
    pdf.set_text_color(*NAVY)
    pdf.cell(0, 10, "510kBridge", align="L", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(*GRAY)
    pdf.cell(0, 4, "A Delaware Corporation", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 4, "510kbridge.com  |  info@510kbridge.com",
             new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)
    pdf.set_draw_color(*NAVY)
    pdf.set_line_width(0.6)
    pdf.line(pdf.l_margin, pdf.get_y(), pdf.w - pdf.r_margin, pdf.get_y())
    pdf.ln(6)

    # Title
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(*NAVY)
    pdf.cell(0, 10, "Family Immigration Strategy", align="C",
             new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(*GRAY)
    pdf.cell(0, 5, "Dual-Path Approach for the Liu Family", align="C",
             new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)
    today = date.today().strftime("%B %d, %Y")
    pdf.cell(0, 5, f"Prepared {today}", align="C",
             new_x="LMARGIN", new_y="NEXT")
    pdf.ln(8)

    # ── SUMMARY ───────────────────────────────────
    pdf.sec("Executive Summary")

    pdf.txt(
        "This document outlines a two-path immigration strategy that brings "
        "the entire Liu family to the United States through 510kBridge. Rather "
        "than a single EB-5 petition for Lawrence, this approach puts Danielle "
        "in the investor seat -- solving her immediate need for permanent status "
        "-- and brings Lawrence and Lisa through a separate EB-1C Multinational "
        "Manager transfer that requires no additional investment capital."
    )

    pdf.green_txt(
        "Result: All four adults receive green cards. Claire is already a US citizen."
    )

    pdf.table(
        ["Family Member", "Path", "Status"],
        [
            ["Danielle Liu", "EB-5 (principal investor)", "Green card"],
            ["Malei", "EB-5 (derivative spouse)", "Green card"],
            ["Claire", "N/A", "US citizen (born here)"],
            ["Lawrence Liu", "EB-1C (multinational manager)", "Green card"],
            ["Lisa Liu", "EB-1C (derivative spouse)", "Green card"],
        ],
        [50, 60, 50]
    )

    # ── PATH A: DANIELLE EB-5 ─────────────────────
    pdf.sec("Path A: Danielle Liu -- EB-5 Investor")

    pdf.sub("How It Works")
    pdf.txt(
        "Danielle files Form I-526E as the principal EB-5 investor. She invests "
        "$800,000 into 510kBridge, which is registered in Gresham, Oregon -- a "
        "designated Targeted Employment Area (TEA) qualifying for the reduced "
        "investment threshold. The company must create at least 10 full-time US "
        "jobs within two years."
    )

    pdf.sub("Source of Funds")
    pdf.txt(
        "USCIS accepts parental gifts as a lawful source of investment capital. "
        "Lawrence can gift the $800,000 to Danielle with proper documentation: "
        "a gift letter, proof of Lawrence's lawful earnings in China, and bank "
        "transfer records showing the clear path of funds. This is a well-established "
        "practice in EB-5 cases."
    )

    pdf.sub("Who Gets a Green Card")
    pdf.bold_bullet("Danielle Liu: ", "Principal investor -- conditional green card "
                    "upon I-526E approval")
    pdf.bold_bullet("Malei: ", "Derivative beneficiary (Danielle's spouse) -- "
                    "automatic conditional green card on the same petition")
    pdf.bold_bullet("Claire: ", "Already a US citizen -- no immigration action needed")

    pdf.sub("Timeline")
    pdf.table(
        ["Step", "Timeframe", "Notes"],
        [
            ["Prepare I-526E petition", "2-4 months", "Business plan, source of funds docs"],
            ["USCIS processes I-526E", "12-18 months", "Current processing times"],
            ["Adjustment of Status or consular", "3-6 months", "If Danielle is in US: AOS"],
            ["Conditional green card", "Month 18-24", "Valid for 2 years"],
            ["File I-829 (remove conditions)", "Month 42-48", "Prove jobs created, capital at risk"],
            ["Permanent green card", "Month 48-54", "Full permanent residency"],
        ],
        [55, 35, 70]
    )

    pdf.sub("Why Danielle as Investor (Not Lawrence)")
    pdf.txt(
        "Lawrence told us his primary concern is giving Danielle and her family "
        "something to do in the US. By making Danielle the investor:"
    )
    pdf.bullet("She gets her own green card directly -- not dependent on Lawrence")
    pdf.bullet("Malei gets a green card as her derivative spouse")
    pdf.bullet("She runs the US operation daily -- addressing Lawrence's concern about "
               "being far away with weak control")
    pdf.bullet("Lawrence avoids the EB-5 requirement to relocate permanently -- he can "
               "stay in China and travel as needed")
    pdf.bullet("The $800K investment is in a company the family controls, not in "
               "someone else's venture at a valuation Lawrence doesn't like")

    # ── PATH B: LAWRENCE EB-1C ────────────────────
    pdf.sec("Path B: Lawrence & Lisa Liu -- EB-1C Multinational Manager")

    pdf.sub("How It Works")
    pdf.txt(
        "The EB-1C visa is for multinational managers and executives. It allows a "
        "US company to transfer a manager or executive from an affiliated foreign "
        "office. Unlike EB-5, no investment is required. Unlike EB-2/EB-3, no labor "
        "certification (PERM) is needed."
    )

    pdf.sub("Requirements")
    pdf.bold_bullet("Foreign company: ", "Lawrence must work for a qualifying company "
                    "in China for at least 1 year in a managerial or executive capacity "
                    "within the 3 years before transfer")
    pdf.bold_bullet("US company: ", "510kBridge (US) must have an affiliate, subsidiary, "
                    "or parent relationship with the Chinese entity")
    pdf.bold_bullet("US role: ", "Lawrence must be coming to a managerial or executive "
                    "position at 510kBridge")
    pdf.bold_bullet("Both entities active: ", "Both the US and foreign companies must "
                    "be doing business (not just a shell)")

    pdf.sub("How to Structure It")
    pdf.txt(
        "510kBridge establishes a Chinese subsidiary or affiliated entity -- "
        "for example, '510kBridge Consulting (Shanghai) Co., Ltd.' Lawrence serves "
        "as its CEO, and Jialun Li serves as General Manager handling day-to-day "
        "operations. Together they manage Chinese client relationships, business "
        "development, and the China-side operations. After the qualifying period, "
        "510kBridge (US) files an I-140 petition to transfer Lawrence to the US as CEO."
    )

    pdf.txt(
        "Lawrence is already a CEO of a major company in China -- he has the exact "
        "executive experience that EB-1C requires. The Shanghai entity is not a "
        "demotion; it is a natural extension of his abilities. Jialun, as General "
        "Manager, ensures continuity of daily operations. When Lawrence transfers "
        "to the US, Jialun steps up to CEO of the Shanghai entity, maintaining "
        "the China pipeline without interruption."
    )

    pdf.txt(
        "This structure is natural, not manufactured: 510kBridge already needs a "
        "China-side presence to acquire Chinese medical device clients. Lawrence's "
        "existing network and Jialun's medical industry experience make them the "
        "ideal leadership team for that office. The transfer to a US executive role "
        "is a genuine business need."
    )

    pdf.sub("Who Gets a Green Card")
    pdf.bold_bullet("Lawrence Liu: ", "Principal -- green card as multinational manager/executive")
    pdf.bold_bullet("Lisa Liu: ", "Derivative spouse -- automatic green card on the same petition")

    pdf.sub("Timeline")
    pdf.table(
        ["Step", "Timeframe", "Notes"],
        [
            ["Establish China entity", "2-3 months", "WFOE or JV registration"],
            ["Lawrence as CEO, Jialun as GM", "12 months min", "Builds qualifying period"],
            ["File I-140 (EB-1C)", "Month 14-15", "No PERM/labor cert needed"],
            ["USCIS processes I-140", "4-8 months", "Premium processing available"],
            ["Consular processing", "3-6 months", "Interview at US consulate in China"],
            ["Green card issued", "Month 22-30", "Permanent from day one (no conditions)"],
        ],
        [55, 35, 70]
    )

    pdf.sub("Key Advantages of EB-1C")
    pdf.bullet("No investment capital required -- Lawrence keeps his money")
    pdf.bullet("No labor certification (PERM) -- faster, no DOL audit risk")
    pdf.bullet("No China EB-2/EB-3 backlog -- EB-1 is current or near-current for China")
    pdf.bullet("Green card is permanent from day one -- no 2-year conditional period")
    pdf.bullet("Lisa is covered automatically as derivative spouse")
    pdf.bullet("Lawrence stays in China initially -- builds the pipeline while qualifying")
    pdf.bullet("Jialun as GM provides operational continuity when Lawrence transfers to the US")

    # ── HOW BOTH PATHS WORK TOGETHER ──────────────
    pdf.sec("How Both Paths Work Together")

    pdf.sub("Parallel Timeline")
    pdf.table(
        ["Month", "Path A (Danielle EB-5)", "Path B (Lawrence EB-1C)"],
        [
            ["0-3", "Prepare I-526E, file petition", "Register China entity"],
            ["3-12", "USCIS processing", "Lawrence (CEO) & Jialun (GM) run China"],
            ["12-15", "Awaiting approval", "File I-140 for Lawrence"],
            ["15-18", "I-526E approved, file AOS", "I-140 processing"],
            ["18-24", "Conditional green cards", "Consular processing"],
            ["24-30", "Danielle & Malei in US", "Lawrence & Lisa arrive in US"],
            ["42-48", "File I-829 (remove conditions)", "Already permanent"],
        ],
        [20, 70, 70]
    )

    pdf.txt(
        "Both paths can run simultaneously. Danielle's EB-5 petition is filed "
        "immediately while the China entity is being set up. By the time Lawrence "
        "completes his 1-year qualifying period in China, Danielle may already have "
        "her conditional green card. Within 2-3 years, the entire family has permanent "
        "US residency."
    )

    # ── FAMILY ROLES ──────────────────────────────
    pdf.sec("Family Roles at 510kBridge")

    pdf.table(
        ["Person", "Title", "Responsibility", "Immigration Path"],
        [
            ["Danielle Liu", "COO / Investor", "US operations, accounting", "EB-5 principal"],
            ["Malei", "Operations Mgr", "Office, logistics, training", "EB-5 derivative"],
            ["Claire", "N/A", "N/A (minor, US citizen)", "US citizen"],
            ["Lawrence Liu", "CEO (Shanghai)", "China BD, client pipeline", "EB-1C principal"],
            ["Lisa Liu", "Advisory", "Family support", "EB-1C derivative"],
            ["Jialun Li", "GM (Shanghai)", "China ops, medical content", "Separate path"],
            ["Chensy Li", "Sr. Acct Manager", "Marketing, sales", "Separate path"],
            ["Lon Dailey", "Founder/Principal", "Regulatory, PM, US ops", "US citizen"],
        ],
        [33, 33, 52, 42]
    )

    # ── FINANCIAL STRUCTURE ───────────────────────
    pdf.sec("Financial Structure")

    pdf.sub("Investment")
    pdf.txt(
        "Total EB-5 capital required: $800,000 (TEA rate). This is Lawrence's gift "
        "to Danielle, documented for USCIS. No additional investment is required for "
        "the EB-1C path -- Lawrence earns a salary from the China entity and later "
        "from 510kBridge (US)."
    )

    pdf.sub("Ownership")
    pdf.txt(
        "Danielle holds the investor equity stake from her $800,000 EB-5 investment. "
        "Lawrence holds preferred shares as CEO (no cash investment required). "
        "Lon holds founder equity. This structure keeps Lawrence's ownership minimal "
        "enough that the EB-1C transfer is a genuine employer-employee relationship, "
        "not self-petitioning."
    )

    pdf.sub("Revenue Model")
    pdf.table(
        ["Tier", "What We Provide", "Monthly Fee"],
        [
            ["Starter", "Control Tower SaaS license", "$500-$2,000"],
            ["Professional", "Full PM, gates & submissions", "$10K-$25K"],
            ["Enterprise", "End-to-end regulatory + PM", "$50K+/project"],
        ],
        [40, 75, 45]
    )

    pdf.txt(
        "With 3-5 Professional clients, the company generates $500K-$900K annually "
        "-- enough to pay competitive salaries for the entire team and fund both "
        "the US and China operations."
    )

    # ── WHY GRESHAM ─────────────────────────────────────
    pdf.sec("Why Gresham, Oregon")

    pdf.txt(
        "Gresham is just east of Portland -- 20 minutes from the airport. "
        "It qualifies as a Targeted Employment Area, which means the EB-5 investment "
        "threshold is $800,000 instead of $1,050,000."
    )

    pdf.txt(
        "For the family: sell the current home at $800K or more and buy new in Gresham. "
        "Beautiful homes are available -- some listed at $2M. The family would be close "
        "together, close to Portland International Airport, and in a great community "
        "with excellent schools for Claire."
    )

    # ── COMPARISON TABLE ──────────────────────────
    pdf.sec("Why This Dual-Path Approach")

    pdf.table(
        ["Factor", "Dual Path (EB-5 + EB-1C)", "Lawrence-Only EB-5"],
        [
            ["Green cards", "All 4 adults + Claire (citizen)", "Lawrence + Lisa only"],
            ["Danielle status", "Permanent (her own petition)", "Must find separate path"],
            ["Malei status", "Permanent (derivative)", "No path"],
            ["Lawrence cost", "$0 (EB-1C has no investment)", "$800K out of pocket"],
            ["Total investment", "$800K (gift to Danielle)", "$800K (Lawrence direct)"],
            ["Lawrence in China", "Yes, runs China office", "Must relocate to US"],
            ["Control concern", "Danielle runs US daily", "Lawrence far away, uneasy"],
            ["PERM required", "No", "No"],
            ["Backlog risk", "EB-1 current for China", "EB-5 current"],
            ["Family covered", "Everyone", "Only Lawrence + Lisa"],
        ],
        [38, 60, 62]
    )

    # ── RISKS AND CONSIDERATIONS ──────────────────
    pdf.sec("Risks and Considerations")

    pdf.bold_bullet("China entity must be real: ", "The Chinese subsidiary needs actual "
                    "operations -- office space, employees, revenue. A paper entity will "
                    "not satisfy USCIS. 510kBridge genuinely needs China-side business "
                    "development, so this is naturally fulfilled.")
    pdf.bold_bullet("1-year qualifying period: ", "Lawrence must work in an executive "
                    "capacity (CEO) at the China entity for a minimum of 1 continuous year "
                    "before the transfer petition is filed. Jialun as GM ensures operations "
                    "continue seamlessly after Lawrence's departure.")
    pdf.bold_bullet("Lawrence's ownership stake: ", "Must be structured carefully. If "
                    "Lawrence owns too much of 510kBridge (US), USCIS may view the EB-1C "
                    "as self-petitioning. Preferred shares with limited voting rights, "
                    "combined with Danielle's majority investor equity, maintains the "
                    "employer-employee relationship.")
    pdf.bold_bullet("Source of funds documentation: ", "Lawrence's $800K gift to Danielle "
                    "requires thorough documentation of lawful source. Bank records, tax "
                    "returns, and business income records going back several years.")
    pdf.bold_bullet("Immigration counsel: ", "Both paths require experienced EB-5 and EB-1C "
                    "attorneys. The dual structure is well-established but must be properly "
                    "documented.")

    # ── NEXT STEPS ────────────────────────────────
    pdf.sec("Next Steps")

    pdf.bold_bullet("1. ", "Engage immigration attorney experienced in both EB-5 and EB-1C")
    pdf.bold_bullet("2. ", "Begin Danielle's I-526E preparation (source of funds, business plan)")
    pdf.bold_bullet("3. ", "Register 510kBridge China subsidiary (WFOE in Shanghai or Shenzhen)")
    pdf.bold_bullet("4. ", "Lawrence assumes CEO role, Jialun assumes GM role at China entity")
    pdf.bold_bullet("5. ", "File Danielle's I-526E petition")
    pdf.bold_bullet("6. ", "After 12 months, file Lawrence's I-140 (EB-1C)")
    pdf.bold_bullet("7. ", "Coordinate consular processing for both families")

    # ── CLOSING ─────────────────────────────────
    pdf.ln(4)
    pdf.txt(
        "This approach solves every concern Lawrence raised: Danielle and Malei have "
        "meaningful work and permanent status. Lawrence keeps control through the China "
        "entity where he is comfortable. The investment goes into a family company, not "
        "someone else's venture. And the entire family ends up in the United States."
    )

    pdf.ln(2)
    pdf.txt("Talk soon,")
    pdf.ln(6)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(*TEXT)
    pdf.cell(0, 5, "Lon", new_x="LMARGIN", new_y="NEXT")

    # ── DISCLAIMER ──────────────────────────────
    pdf.ln(10)
    pdf.set_draw_color(*GRAY)
    pdf.set_line_width(0.3)
    pdf.line(pdf.l_margin, pdf.get_y(), pdf.w - pdf.r_margin, pdf.get_y())
    pdf.ln(3)
    pdf.set_font("Helvetica", "I", 7.5)
    pdf.set_text_color(*GRAY)
    pdf.multi_cell(0, 4,
        "This document is for discussion purposes only and does not constitute legal, "
        "tax, or immigration advice. EB-5 and EB-1C eligibility must be confirmed by "
        "qualified immigration counsel. Financial projections are estimates, not guarantees. "
        "Immigration timelines are approximate and subject to USCIS processing conditions.",
        new_x="LMARGIN", new_y="NEXT")

    # ── SAVE ────────────────────────────────────
    out = os.path.join(OUT_DIR, "510kBridge_Immigration_Strategy.pdf")
    pdf.output(out)
    sz = os.path.getsize(out)
    print(f"Created {out}  ({sz:,} bytes, {pdf.pages_count} pages)")


if __name__ == "__main__":
    build()
