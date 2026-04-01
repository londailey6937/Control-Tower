#!/usr/bin/env python3
"""
Generate a personal letter to Lawrence Liu proposing 510kBridge as an EB-5
investment vehicle for his family.
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


class LetterPDF(FPDF):

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
    pdf = LetterPDF("P", "mm", "Letter")
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
    pdf.ln(8)

    today = date.today().strftime("%B %d, %Y")
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(*TEXT)
    pdf.cell(0, 5, today, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(8)

    # ── THE LETTER ────────────────────────────────
    pdf.txt("Hi Lawrence,")

    pdf.txt(
        "I think I understand your situation and needs better now. If your primary "
        "concern is for Danielle, Malei, and Claire, then invest in the family."
    )

    pdf.txt(
        "After building the Control Tower and doing exhaustive research into the FDA "
        "submission process, I see an opportunity that could benefit both of our "
        "families. I haven't discussed this with anyone yet, but I can see a company "
        "formed through the EB-5 program with shares for active company members and "
        "salaries paid from client services revenue."
    )

    pdf.txt(
        "We would have a strong team with educated and experienced family members. "
        "Let me tell you what I see:"
    )

    # ── OUR TEAM ──────────────────────────────────
    pdf.sec("Our Team")

    pdf.bold_bullet("Jialun Li -- Director of Client Services: ",
        "Jialun is doing really well with his company as Content Supervisor and "
        "Senior Medical Editor. He is involved with medical content planning, patient "
        "education content creation, and quality control. He knows many medical "
        "professionals in China and Europe -- he travels there regularly to participate "
        "in seminars and give speeches. He is a good salesman and wants to be a leader "
        "someday in his own company. This could be his path.")

    pdf.bold_bullet("Chensy Li -- Senior Account Manager: ",
        "Chensy, his wife, has a graduate degree from the UK and extensive marketing "
        "experience. She could help us find sources of clients. She currently works for "
        "a western company in Shanghai as a senior account manager where she manages "
        "projects and clients. She knows how to bring in business.")

    pdf.bold_bullet("Danielle Liu -- Accounting: ",
        "Danielle would be in charge of accounting. Her UCSB Master's in Accounting "
        "is exactly what we need -- real credentials for real responsibility.")

    pdf.bold_bullet("Malei & Jessica: ",
        "We could find roles for Malei and Jessica after some directed training. "
        "Already, Jessica has contacted me with her own business idea, which shows "
        "she has the entrepreneurial spirit. That kind of initiative is exactly what "
        "a startup needs.")

    pdf.bold_bullet("Lawrence Liu -- CEO: ",
        "Your title would be CEO. This comes with no financial investment requirement "
        "in the company, but you would hold preferred shares. Your business network in "
        "China is the client pipeline. You already know the people who need this service.")

    pdf.bold_bullet("Lon Dailey -- Founder & Principal Consultant: ",
        "I handle all US regulatory, legal, and operational matters. PMP certified, "
        "14 years of US corporate experience in regulated product development, and "
        "prior 510(k) submission experience. I am your US partner -- you focus on what "
        "you know best, and I handle the side you told me makes you uneasy.")

    # ── THE OPPORTUNITY ───────────────────────────
    pdf.sec("The Opportunity")

    pdf.txt(
        "510kBridge helps Chinese medical device companies get FDA 510(k) clearance "
        "to sell in the US market. We manage the entire process for them using the "
        "Control Tower platform I built. There are hundreds of Chinese companies that "
        "need this service every year, and the US medical device market is enormous."
    )

    pdf.txt(
        "Since we last talked, I have built a four-product technology suite:\n\n"
        "  Control Tower -- The 17-tab PM command dashboard for managing the entire "
        "510(k) pathway, from dual-track milestones through FDA submission.\n"
        "  Predicate Finder -- An FDA database search tool (embedded in Control Tower "
        "and available as a free standalone tool) that helps identify predicate devices "
        "for substantial equivalence arguments.\n"
        "  QMS-Lite -- A lightweight quality management system designed for 510(k)-stage "
        "startups who cannot afford enterprise QMS platforms like Greenlight Guru.\n"
        "  Entity Setup Tracker -- Helps Chinese companies form their US entity (Delaware "
        "C-Corp, EIN, registered agent, bank account) with step-by-step tracking.\n\n"
        "Each product generates recurring SaaS revenue and feeds clients into higher "
        "service tiers. The Predicate Finder alone is a lead-generation machine -- "
        "companies start with a free search and upgrade when they see the value."
    )

    pdf.txt(
        "Here is the additional benefit I want you to consider: as we onboard clients "
        "seeking FDA clearance, you can look through the client list and see if there "
        "are better valuations that you could be interested in. Instead of being locked "
        "into one company at a price you are not satisfied with, you would have a front-row "
        "seat to evaluate multiple companies at different stages -- and invest in the ones "
        "that make sense to you, on your terms."
    )

    pdf.txt(
        "You would be investing in your family, not in someone else's company."
    )

    # ── WHY CAMAS ─────────────────────────────────
    pdf.sec("Why Camas, Washington")

    pdf.txt(
        "Camas is just across the river from Portland -- 20 minutes from the airport. "
        "It qualifies as a Targeted Employment Area, which means the EB-5 investment "
        "threshold is $800,000 instead of $1,050,000."
    )

    pdf.txt(
        "I would suggest selling your house and buying new in Camas. There are beautiful "
        "homes available -- I found one listed at $2M right now. You could sell yours at "
        "$800K or more, and the difference puts you in a nicer home in a TEA-qualified "
        "area where the company is registered. The family would be close together, close "
        "to the airport, and in a great community."
    )

    # ── JIALUN & CHENSY ───────────────────────────
    pdf.sec("Jialun & Chensy")

    pdf.txt(
        "If you are interested in this, I would check with Jialun and Chensy to see "
        "what they think. They are already planning to move here at some point in the "
        "future. I think they would like to have better control of their lives, and "
        "having their own business would suit them. This could be the opportunity that "
        "brings that timeline forward."
    )

    # ── CLIENT FEES AND COMPENSATION ──────────────
    pdf.sec("How Client Fees Work")

    pdf.txt(
        "Our revenue comes from the companies we serve. Here is what a typical client "
        "engagement looks like and how the money flows:"
    )

    pdf.sub("Service Tiers")
    pdf.table(
        ["Tier", "What We Provide", "Monthly Fee"],
        [
            ["Predicate Finder Pro", "Unlimited searches, chain tracing, SE drafts", "$99"],
            ["QMS-Lite", "Quality system for FDA audit readiness", "$200-$500"],
            ["Starter", "Control Tower SaaS + Entity Setup Tracker", "$500-$2,000"],
            ["Professional", "Full PM engagement, manage gates & submissions", "$10,000-$25,000"],
            ["Enterprise", "End-to-end: regulatory + PM + suppliers + entity", "$50,000+/project"],
        ],
        [40, 75, 45]
    )

    pdf.txt(
        "Revenue comes from multiple streams. SaaS subscriptions (Predicate Finder Pro, "
        "QMS-Lite, Starter dashboards) provide predictable monthly recurring revenue. "
        "Professional and Enterprise clients bring in $10K-$50K+ per month each. A single "
        "Professional client at $15,000/month generates $180,000 per year. With SaaS "
        "subscribers plus 3-5 Professional clients, the company could reach $500K-$900K "
        "annually."
    )

    pdf.sub("How Fees Are Used")
    pdf.table(
        ["Category", "% of Revenue", "What It Covers"],
        [
            ["Salaries & Benefits", "45-50%", "Team compensation (everyone gets paid)"],
            ["Operations", "15-20%", "Office, legal, insurance, software tools"],
            ["Business Development", "10-15%", "Marketing, travel, client acquisition"],
            ["Technology", "5-10%", "Control Tower platform maintenance & upgrades"],
            ["Owner Distributions", "15-20%", "Profit sharing to shareholders"],
        ],
        [45, 35, 80]
    )

    pdf.txt(
        "The key point: client fees pay salaries first. Danielle, Jialun, Chensy, "
        "and everyone else draws a real salary from operations. On top of that, as "
        "the company becomes profitable, shareholders receive distributions. "
        "This is not speculative -- it is a services business where revenue begins "
        "with the first client."
    )

    pdf.sub("Example: Year 2 with SaaS + 5 Active PM Clients")
    pdf.table(
        ["Item", "Annual Amount"],
        [
            ["SaaS Revenue (PF Pro + QMS + Starter)", "$120,000"],
            ["PM Revenue (5 clients x $15K/mo avg)", "$900,000"],
            ["Total Revenue", "$1,020,000"],
            ["Salaries & Benefits (50%)", "$510,000"],
            ["Operations (15%)", "$153,000"],
            ["Business Development (10%)", "$102,000"],
            ["Technology (5%)", "$51,000"],
            ["Owner Distributions (20%)", "$204,000"],
        ],
        [95, 65]
    )

    pdf.txt(
        "At 5 PM clients plus SaaS subscribers, the company supports competitive "
        "salaries for the entire team and distributes over $200,000 to shareholders. "
        "As we add clients in Year 3-5, both salaries and distributions grow."
    )

    # ── EB-5 BASICS ──────────────────────────────
    pdf.sec("How the EB-5 Program Works")

    pdf.txt(
        "The EB-5 Immigrant Investor Program provides a pathway to US permanent "
        "residency (green card) for foreign investors who invest in a US business "
        "that creates jobs. Here are the basics:"
    )

    pdf.bold_bullet("Investment: ", "$800,000 in a Targeted Employment Area (TEA) "
                    "or $1,050,000 in a standard area. Camas, Washington qualifies "
                    "as a TEA -- it is outside the Portland metro MSA boundary and "
                    "meets the high-unemployment threshold at the census tract level.")
    pdf.bold_bullet("Job Creation: ", "The business must create at least 10 full-time "
                    "US jobs per investor")
    pdf.bold_bullet("Timeline: ", "Conditional green card (2 years), then file I-829 "
                    "to remove conditions and receive permanent residency")
    pdf.bold_bullet("At Risk: ", "The capital must be genuinely invested in the business "
                    "(not a guaranteed return)")

    pdf.txt(
        "510kBridge would be registered in Camas, Washington -- a designated "
        "TEA that qualifies for the reduced $800,000 investment threshold. Our hiring "
        "plan calls for 13+ full-time positions in the first 2-3 years -- well above "
        "the 10-job threshold. And because the EB-5 investment goes directly into an "
        "operating company that Danielle and the family work in every day, it is not "
        "just an investment on paper."
    )

    # ── JOB CREATION ─────────────────────────────
    pdf.sub("Planned Positions (Years 1-3)")
    pdf.table(
        ["Role", "Timeline", "Type"],
        [
            ["CEO (Lawrence Liu)", "Current", "Full-time"],
            ["Principal Consultant (Lon Dailey, PMP)", "Current", "Full-time"],
            ["Director of Client Services (Jialun Li)", "Current", "Full-time"],
            ["Senior Account Manager (Chensy Li)", "Current", "Full-time"],
            ["Accounting (Danielle Liu)", "Current", "Full-time"],
            ["Regulatory Specialist", "Year 1", "Full-time"],
            ["Business Development Rep", "Year 1", "Full-time"],
            ["Marketing / WeChat Specialist", "Year 1", "Full-time"],
            ["Office Administrator", "Year 1", "Full-time"],
            ["Project Manager", "Year 2", "Full-time"],
            ["Regulatory Specialist #2", "Year 2", "Full-time"],
            ["Clinical Affairs Manager", "Year 2", "Full-time"],
            ["Controller / CFO", "Year 2-3", "Full-time"],
        ],
        [80, 40, 40]
    )

    # ── SIDE-BY-SIDE ─────────────────────────────
    pdf.sec("Why This Is Different")

    pdf.table(
        ["Factor", "510kBridge (EB-5)", "External Investment"],
        [
            ["Your role", "CEO", "Minority investor"],
            ["Family roles", "Danielle, Jessica, Malei", "None guaranteed"],
            ["Capital required", "$800K (Camas TEA)", "$1M+ at set valuation"],
            ["Valuation", "You build it from zero", "Pre-set by others"],
            ["Control", "Full -- you are CEO", "Limited, makes you uneasy"],
            ["Technology IP", "4-product suite (CT, PF, QMS, EST)", "None"],
            ["US operations", "Lon handles it", "You navigate alone"],
            ["Revenue starts", "First client (Year 1)", "18-23 months (FDA wait)"],
            ["Risk", "Portfolio of clients", "Single product bet"],
            ["Green card", "Yes (EB-5)", "No"],
            ["Client deal flow", "See all valuations", "Locked into one company"],
        ],
        [38, 60, 62]
    )

    # ── CLOSING ─────────────────────────────────
    pdf.ln(4)
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
        "This letter is for discussion purposes only and does not constitute legal, "
        "tax, or immigration advice. EB-5 eligibility must be confirmed by qualified "
        "immigration counsel. Financial projections are estimates, not guarantees.",
        new_x="LMARGIN", new_y="NEXT")

    # ── SAVE ────────────────────────────────────
    out = os.path.join(OUT_DIR, "510kBridge_EB5_Proposal.pdf")
    pdf.output(out)
    sz = os.path.getsize(out)
    print(f"Created {out}  ({sz:,} bytes, {pdf.pages_count} pages)")


if __name__ == "__main__":
    build()
