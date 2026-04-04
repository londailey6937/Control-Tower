#!/usr/bin/env python3
"""Generate a one-page PDF: Why Delaware Incorporation."""

import os
from fpdf import FPDF

OUT_DIR = os.path.dirname(os.path.abspath(__file__))

BLUE = (30, 90, 200)
GRAY = (120, 120, 130)
TEXT = (40, 40, 45)
DARK = (15, 17, 23)

_CHAR_MAP = str.maketrans({
    "\u2014": "--", "\u2013": "-", "\u2022": "*",
    "\u2018": "'", "\u2019": "'", "\u201c": '"', "\u201d": '"',
})
def _a(s): return s.translate(_CHAR_MAP)


class DelPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(*GRAY)
        self.cell(0, 5, _a("Company B USA -- Delaware Incorporation Reference  |  CONFIDENTIAL"), align="R")
        self.ln(7)

    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(*GRAY)
        self.cell(0, 5, f"Page {self.page_no()}/{{nb}}", align="C")

    def sec(self, title):
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(*BLUE)
        self.cell(0, 6, _a(title), new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(*BLUE)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(2)

    def sub(self, title):
        self.set_font("Helvetica", "B", 9.5)
        self.set_text_color(*DARK)
        self.cell(0, 5.5, _a(title), new_x="LMARGIN", new_y="NEXT")
        self.ln(0.5)

    def txt(self, text, bold=False, italic=False):
        style = "B" if bold else ("I" if italic else "")
        self.set_font("Helvetica", style, 9)
        self.set_text_color(*TEXT)
        self.multi_cell(0, 4.3, _a(text), new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def bul(self, text):
        self.set_font("Helvetica", "", 9)
        self.set_text_color(*TEXT)
        self.cell(5, 4.3, _a("*"))
        self.multi_cell(0, 4.3, _a(text), new_x="LMARGIN", new_y="NEXT")


def build():
    pdf = DelPDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=14)
    pdf.add_page()

    # Title
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(*BLUE)
    pdf.cell(0, 8, "Why Delaware Incorporation?", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "I", 9)
    pdf.set_text_color(*GRAY)
    pdf.cell(0, 5, _a("Reference for Company B USA -- Medical Device Venture"), align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)

    pdf.txt(
        "Delaware is the default choice for many U.S. companies -- especially startups and "
        "medical device ventures -- because it's optimized for investors, governance, and "
        "legal predictability.")
    pdf.ln(1)

    # ── 1-5 ──
    pdf.sec("Why Delaware Is So Commonly Used")

    pdf.sub("1) Investor Preference (Big One)")
    pdf.bul("Venture capital and institutional investors often require a Delaware C-Corp")
    pdf.bul("Familiar structure = faster due diligence and fewer negotiation issues")
    pdf.bul("Standardized terms for stock, options, and exits")
    pdf.ln(1)

    pdf.sub("2) Business-Friendly Legal System")
    pdf.bul("Delaware has a specialized court, the Court of Chancery, focused on business law")
    pdf.bul("No juries -- cases are decided by experienced judges")
    pdf.bul("Predictable outcomes based on extensive case history (this matters if disputes arise)")
    pdf.ln(1)

    pdf.sub("3) Flexible Corporate Structure")
    pdf.bul("Easy to set up multiple classes of stock (important for raising capital)")
    pdf.bul("Well-defined rules for boards, officers, and fiduciary duties")
    pdf.bul("Clean framework for equity, options, and future funding rounds")
    pdf.ln(1)

    pdf.sub("4) Privacy and Simplicity")
    pdf.bul("You don't have to publicly list all shareholders")
    pdf.bul("Minimal reporting requirements compared to some states")
    pdf.ln(1)

    pdf.sub("5) Tax Advantages (Situational)")
    pdf.bul("No Delaware state tax on income earned outside Delaware")
    pdf.bul("No sales tax")
    pdf.bul("But: you still pay taxes in the state where you actually operate (e.g., Oregon)")
    pdf.ln(2)

    # ── When it makes sense ──
    pdf.sec("When Delaware Makes the Most Sense")
    pdf.txt("Delaware is usually the right move if you plan to:")
    pdf.bul("Raise outside capital (angels, VC, private equity)")
    pdf.bul("Issue equity to multiple stakeholders")
    pdf.bul("Scale nationally or globally")
    pdf.bul("Eventually sell the company or go public")
    pdf.ln(2)

    # ── When it might not be necessary ──
    pdf.sec("When It Might Not Be Necessary")
    pdf.txt("If your company is:")
    pdf.bul("Small, local, and self-funded")
    pdf.bul("Not planning to raise capital")
    pdf.bul("Operating entirely in one state")
    pdf.ln(1)
    pdf.txt("Then registering directly in Oregon could be simpler and cheaper.")
    pdf.ln(2)

    # ── Medical device context ──
    pdf.sec("For a Medical Device Company (Your Context)")
    pdf.txt("Because you're dealing with:")
    pdf.bul("FDA regulatory timelines")
    pdf.bul("Investor involvement")
    pdf.bul("Potential high capital needs")
    pdf.ln(1)
    pdf.txt("Delaware aligns well with how investors and partners expect the company to be structured.")
    pdf.ln(2)

    # ── Bottom line ──
    pdf.set_draw_color(*BLUE)
    pdf.set_line_width(0.5)
    pdf.line(pdf.l_margin, pdf.get_y(), pdf.w - pdf.r_margin, pdf.get_y())
    pdf.ln(3)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(*BLUE)
    pdf.cell(0, 6, "Bottom Line", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(*TEXT)
    pdf.txt("Delaware isn't about location -- it's about credibility, flexibility, and investor readiness.", bold=True)

    path = os.path.join(OUT_DIR, "Delaware_Incorporation_Reference.pdf")
    pdf.output(path)
    return path


if __name__ == "__main__":
    p = build()
    print(f"PDF: {p}")
    print("Done.")
