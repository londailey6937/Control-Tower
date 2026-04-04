#!/usr/bin/env python3
"""
Generate Sales Playbook PDF — 510k Bridge
EN + CN bilingual sales pitch deck for the Control Tower + Predicate Finder product suite.
"""

import os
from fpdf import FPDF

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
CJK_FONT = "/Library/Fonts/Arial Unicode.ttf"

BLUE = (30, 90, 200)
DARK = (15, 17, 23)
GRAY = (120, 120, 130)
TEXT = (40, 40, 45)
GREEN = (16, 120, 80)
AMBER = (180, 120, 10)
RED = (200, 40, 40)

_MAP = str.maketrans({
    "\u2014": "--", "\u2013": "-", "\u2019": "'", "\u2018": "'",
    "\u201c": '"', "\u201d": '"', "\u2026": "...", "\u00a0": " ",
    "\u2022": "-", "\u2192": "->",
})

def _s(t):
    return t.translate(_MAP)


# ═══════════════════════════════════════════
# English Sales Playbook
# ═══════════════════════════════════════════
class SalesEN(FPDF):
    def header(self):
        if self.page_no() <= 2:
            return
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(*GRAY)
        self.cell(0, 8, _s("510k Bridge -- Sales Playbook"), align="R", ln=True)
        self.ln(2)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(*GRAY)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")

    def sec(self, num, title):
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(*BLUE)
        self.cell(0, 10, _s(f"{num}. {title}"), new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(*BLUE)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(4)

    def sub(self, title):
        self.set_font("Helvetica", "B", 12)
        self.set_text_color(*TEXT)
        self.cell(0, 8, _s(title), new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def txt(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*TEXT)
        self.multi_cell(0, 5.5, _s(text), new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def bul(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*TEXT)
        self.multi_cell(0, 5.5, _s("  - " + text), new_x="LMARGIN", new_y="NEXT")

    def kv(self, key, val):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(*BLUE)
        self.cell(0, 5.5, _s(key), new_x="LMARGIN", new_y="NEXT")
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*TEXT)
        self.multi_cell(0, 5.5, _s("  " + val), new_x="LMARGIN", new_y="NEXT")
        self.ln(1)


def build_english():
    pdf = SalesEN()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()

    # Cover
    pdf.ln(30)
    pdf.set_font("Helvetica", "B", 28)
    pdf.set_text_color(*BLUE)
    pdf.cell(0, 14, "Sales Playbook", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 14)
    pdf.set_text_color(*TEXT)
    pdf.cell(0, 9, "510k Bridge", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(6)
    pdf.set_font("Helvetica", "I", 11)
    pdf.set_text_color(*GRAY)
    pdf.cell(0, 7, "Version 1.0 | March 2026", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 7, "510k Bridge, Inc.", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(20)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(*TEXT)
    pdf.multi_cell(0, 5.5, _s(
        "This playbook equips the sales team with positioning, pricing, objection handling, "
        "and demo scripts for the complete 510k Bridge product suite: "
        "Control Tower, Predicate Finder, QMS-Lite, Entity Setup Tracker, "
        "and professional services."
    ), align="C")

    # 1. Ideal Customer Profile
    pdf.add_page()
    pdf.sec(1, "Ideal Customer Profile (ICP)")
    pdf.txt(
        "Our ideal customer is a Chinese medical device company preparing to enter the "
        "US market through the FDA 510(k) pathway. Key characteristics:")
    pdf.bul("Company size: 50-500 employees, $10M-$100M revenue")
    pdf.bul("Has an existing NMPA-approved product they want to bring to the US")
    pdf.bul("Budget: $50K-$500K allocated for US market entry")
    pdf.bul("Decision maker: VP Regulatory, CEO, or Head of International Business")
    pdf.bul("Pain: Unfamiliar with FDA process, no US regulatory team, language barrier")
    pdf.bul("Timeline: 12-24 months to FDA clearance")

    pdf.sub("1.1 Secondary Personas")
    pdf.txt(
        "  US Regulatory Consultant -- Uses Predicate Finder for client work, upgrades "
        "to Control Tower for project management across multiple clients.\n\n"
        "  Chinese Entrepreneur (EB-1/E-2) -- Building a US medical device startup. "
        "Needs everything: entity formation, FDA strategy, PM tooling, investor relations.")

    # 2. Product Positioning
    pdf.add_page()
    pdf.sec(2, "Product Positioning")

    pdf.sub("2.1 Elevator Pitch (30 seconds)")
    pdf.txt(
        "'510k Bridge is the only bilingual platform that combines AI-powered "
        "predicate device research, a 16-tab project management dashboard, lightweight QMS, "
        "and FDA communications automation -- purpose-built "
        "for Chinese medical device companies pursuing 510(k) clearance. Our Predicate "
        "Finder tool is included free with all service tiers.'")

    pdf.sub("2.2 Value Proposition")
    pdf.txt(
        "  For the CEO: 'See your entire 510(k) program in one dashboard -- milestones, "
        "gates, risks, budget, and investor relations -- in Chinese or English.'\n\n"
        "  For the VP Regulatory: 'Find the right predicate device in minutes, not days. "
        "Auto-generate your SE argument draft and trace the predicate chain.'\n\n"
        "  For the CFO: 'Track burn rate, runway, and investor pipeline alongside the "
        "regulatory timeline. Know exactly when you'll need the next funding round.'")

    pdf.sub("2.3 Competitive Differentiators")
    pdf.txt(
        "  1. Bilingual (EN/CN) -- Only platform with full Chinese language support\n"
        "  2. Predicate Finder -- AI-powered predicate search + SE argument tool (included)\n"
        "  3. End-to-end -- From predicate research to clearance management in one platform\n"
        "  4. QMS-Lite -- Lightweight quality system for startups, not enterprise-grade overkill\n"
        "  5. FDA Comms Center -- Q-Sub generator, RTA self-check, MDUFA tracking built in\n"
        "  6. Entity Setup -- Delaware C-Corp, state registration, EIN, FDA establishment\n"
        "  7. China market expertise -- WeChat, Shanghai office, accelerator partnerships\n"
        "  8. PMP authority model -- FDA-grade decision traceability in the dashboard")

    # 3. Product Suite & Pricing
    pdf.add_page()
    pdf.sec(3, "Product Suite & Pricing")

    pdf.sub("3.1 510(k) Predicate Finder")
    pdf.txt(
        "  INCLUDED WITH ALL SERVICES\n"
        "    AI-powered search of FDA's openFDA database\n"
        "    Predicate chain tracing, multi-device comparison\n"
        "    SE argument generator, PDF export\n"
        "    Bilingual interface (EN/CN)\n"
        "    Purpose: Lead generation and client research accelerator")

    pdf.sub("3.2 Control Tower PM Dashboard")
    pdf.txt(
        "  STARTER ($500/mo)\n"
        "    1 project, read-only dashboard, basic tabs\n"
        "    Best for: Companies just beginning their 510(k) strategy\n\n"
        "  GROWTH ($1,000/mo)\n"
        "    2 projects, full dashboard, message board, document control\n"
        "    Best for: Active 510(k) submissions\n\n"
        "  SCALE ($2,000/mo)\n"
        "    Unlimited projects, full FDA comms center,\n"
        "    advanced analytics\n"
        "    Best for: Companies managing multiple submissions or devices")

    pdf.sub("3.3 QMS-Lite")
    pdf.txt(
        "  $200-500/mo\n"
        "    Lightweight QMS aligned to 21 CFR 820 & ISO 13485\n"
        "    Document control & CAPA tracking\n"
        "    Training records, supplier qualification, complaint handling\n"
        "    Integrates with Control Tower\n"
        "    Best for: Startups who need QMS without enterprise complexity")

    pdf.sub("3.4 Cross-Border Entity Setup Tracker")
    pdf.txt(
        "  $1K-5K one-time or $200/mo\n"
        "    Delaware C-Corp formation\n"
        "    Oregon state registration\n"
        "    Registered agent, EIN, US bank account coordination\n"
        "    FDA establishment registration, US Agent, labeling compliance\n"
        "    Best for: Chinese companies establishing US legal presence")

    pdf.sub("3.5 Professional Services")
    pdf.txt(
        "  Regulatory Consulting: $250-500/hr\n"
        "  Project Management Retainer: $10-25K/mo\n"
        "  Enterprise Engagement: $50-200K+ per project\n\n"
        "  Services include: predicate device strategy, 510(k) submission preparation, "
        "project management, supplier management, US entity setup, investor relations\n\n"
        "  US Agent representation included with Professional and Enterprise tiers")

    # 4. Sales Process
    pdf.add_page()
    pdf.sec(4, "Sales Process")

    pdf.sub("4.1 Lead Generation")
    pdf.txt(
        "  Inbound: Predicate Finder email gate -> nurture sequence -> demo request\n"
        "  Outbound: WeChat content -> accelerator introductions -> direct outreach\n"
        "  Referral: Immigration attorneys, CROs, testing labs\n"
        "  Events: Mandarin webinars, trade shows (CBIA, AdvaMed), biotech park visits")

    pdf.sub("4.2 Qualification (BANT)")
    pdf.txt(
        "  Budget: Can they invest $500-2,000/mo in SaaS + $10K+/mo in services?\n"
        "  Authority: Are we speaking to the decision maker (CEO, VP Regulatory)?\n"
        "  Need: Do they have a specific device they want to bring to the US?\n"
        "  Timeline: Are they active within the next 6-12 months?")

    pdf.sub("4.3 Demo Script")
    pdf.txt(
        "  1. Open Predicate Finder (free tool, live)\n"
        "     -- Search for their product code or device name\n"
        "     -- Show predicate chain tracing (their eyes light up here)\n"
        "     -- Generate SE argument draft\n"
        "     'This tool is included with every service tier.'\n\n"
        "  2. Switch to Control Tower demo (control-tower-bmx.pages.dev)\n"
        "     -- Show dual-track milestones in Chinese\n"
        "     -- Toggle to English to demonstrate bilingual\n"
        "     -- Open Gate System, show PMP decision flow\n"
        "     -- Show FDA Comms tab (Q-Sub letter, RTA 17-item checklist, SE flowchart)\n"
        "     -- Show Cash/Runway with investor pipeline\n"
        "     -- Show QMS-Lite: CAPA, training records, supplier qualification\n"
        "     'This is your command center from Day 1 to FDA clearance.'\n\n"
        "  3. Close with services pitch\n"
        "     -- 'You can run this yourself, or we can run it for you.'\n"
        "     -- Reference the retainer model\n"
        "     -- Mention Entity Setup if they need US presence\n"
        "     -- Offer a free 30-day Control Tower Starter trial")

    # 5. Objection Handling
    pdf.add_page()
    pdf.sec(5, "Objection Handling")

    pdf.kv("'We already have a consultant'",
           "Great -- we complement consultants. We provide the PM platform and "
           "predicate research tools. Your consultant can log into the dashboard too.")
    pdf.kv("'It's too expensive'",
           "A failed 510(k) costs $200K+ to redo. Our platform is a fraction of that. "
           "Start with the free Predicate Finder and upgrade when you're ready.")
    pdf.kv("'We'll use Excel/Project'",
           "Excel can't generate an SE argument, trace a predicate chain, or give your "
           "investors a live dashboard view. This is purpose-built for 510(k).")
    pdf.kv("'We need to talk to our team'",
           "Absolutely. Can I send you a demo video in Chinese so your team can see it? "
           "I'll also share the Predicate Finder link -- it's free, no commitment.")
    pdf.kv("'We're not ready yet'",
           "The best time to plan your 510(k) is 12-18 months before submission. "
           "Start with Predicate Finder free -- research your predicates now.")
    pdf.kv("'Can we see references?'",
           "Our platform is built on real 510(k) project experience. I can walk you "
           "through a case study with our ICU respiratory device program.")

    # 6. Collateral & Resources
    pdf.add_page()
    pdf.sec(6, "Collateral & Resources")

    pdf.sub("6.1 Lead Magnets (Free)")
    pdf.bul("510(k) Predicate Finder -- AI-powered SaaS tool (included with services)")
    pdf.bul("FDA 510(k) Pathway Guide PDF -- Branded EN + CN")
    pdf.bul("Investment & Fundraising Guide PDF -- EN + CN")
    pdf.bul("Stanford PMP Course -- Free professional development")
    pdf.bul("Mandarin Webinar Replays -- Gated content")

    pdf.sub("6.2 Sales Collateral")
    pdf.bul("This Sales Playbook (EN + CN)")
    pdf.bul("510(k) Bridge Service Fact Sheet (EN + CN)")
    pdf.bul("Control Tower User Guide (EN + CN)")
    pdf.bul("PMP User Guide (EN + CN)")
    pdf.bul("Demo dashboard: control-tower-bmx.pages.dev")

    pdf.sub("6.3 Demo Links")
    pdf.kv("Predicate Finder", "predicate-finder.pages.dev (included with services)")
    pdf.kv("Control Tower Demo", "control-tower-bmx.pages.dev (read-only demo)")
    pdf.kv("510k Bridge Website", "510kbridge.com (bilingual landing page)")

    # 7. Metrics & Targets
    pdf.add_page()
    pdf.sec(7, "Metrics & Targets (Year 1)")
    pdf.txt(
        "  Predicate Finder free registrations: 500\n"
        "  Predicate Finder Pro conversions: 20 (4% rate)\n"
        "  Control Tower paying clients: 3\n"
        "  Professional services retainers: 1\n"
        "  Monthly Recurring Revenue: $15K by Q4\n"
        "  Average deal size: $35K/yr\n"
        "  Sales cycle: 30-60 days (SaaS) / 60-90 days (services)\n"
        "  Demo-to-close rate: 30%")

    path = os.path.join(OUT_DIR, "Sales_Playbook_EN.pdf")
    pdf.output(path)
    return path


# ═══════════════════════════════════════════
# Chinese Sales Playbook
# ═══════════════════════════════════════════
class SalesCN(FPDF):
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
        self.cell(0, 8, _s("510k Bridge -- \u9500\u552e\u624b\u518c"), align="R", ln=True)
        self.ln(2)

    def footer(self):
        self.set_y(-15)
        self.set_font("CJK", "I", 8)
        self.set_text_color(*GRAY)
        self.cell(0, 10, _s(f"\u7b2c {self.page_no()}/{{nb}} \u9875"), align="C")

    def sec(self, num, title):
        self.set_font("CJK", "B", 16)
        self.set_text_color(*BLUE)
        self.cell(0, 10, _s(f"{num}. {title}"), new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(*BLUE)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(4)

    def sub(self, title):
        self.set_font("CJK", "B", 12)
        self.set_text_color(*TEXT)
        self.cell(0, 8, _s(title), new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def txt(self, text):
        self.set_font("CJK", "", 10)
        self.set_text_color(*TEXT)
        self.multi_cell(0, 6, _s(text), new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def bul(self, text):
        self.set_font("CJK", "", 10)
        self.set_text_color(*TEXT)
        self.multi_cell(0, 6, _s("  - " + text), new_x="LMARGIN", new_y="NEXT")

    def kv(self, key, val):
        self.set_font("CJK", "B", 10)
        self.set_text_color(*BLUE)
        self.cell(0, 6, _s(key), new_x="LMARGIN", new_y="NEXT")
        self.set_font("CJK", "", 10)
        self.set_text_color(*TEXT)
        self.multi_cell(0, 6, _s("  " + val), new_x="LMARGIN", new_y="NEXT")
        self.ln(1)


def build_chinese():
    pdf = SalesCN()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()

    # \u5c01\u9762
    pdf.ln(30)
    pdf.set_font("CJK", "B", 28)
    pdf.set_text_color(*BLUE)
    pdf.cell(0, 14, _s("\u9500\u552e\u624b\u518c"), align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("CJK", "", 14)
    pdf.set_text_color(*TEXT)
    pdf.cell(0, 9, "510k Bridge", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(6)
    pdf.set_font("CJK", "I", 11)
    pdf.set_text_color(*GRAY)
    pdf.cell(0, 7, _s("\u7248\u672c 2.0 | 2026\u5e744\u6708"), align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 7, "510k Bridge, Inc.", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(20)
    pdf.set_font("CJK", "", 10)
    pdf.set_text_color(*TEXT)
    pdf.multi_cell(0, 6, _s(
        "\u672c\u624b\u518c\u4e3a\u9500\u552e\u56e2\u961f\u63d0\u4f9b\u5b9a\u4f4d\u3001\u5b9a\u4ef7\u3001\u5f02\u8bae\u5904\u7406\u548c\u6f14\u793a\u811a\u672c\uff0c"
        "\u6db5\u76d6510k Bridge\u5b8c\u6574\u4ea7\u54c1\u5957\u4ef6\uff1a"
        "Control Tower\u3001510(k) Predicate Finder\u3001QMS-Lite\u3001"
        "\u8de8\u5883\u5b9e\u4f53\u8bbe\u7acb\u8ffd\u8e2a\u5668\u548c\u4e13\u4e1a\u670d\u52a1\u3002"
    ), align="C")

    # 1. \u7406\u60f3\u5ba2\u6237\u753b\u50cf
    pdf.add_page()
    pdf.sec(1, "\u7406\u60f3\u5ba2\u6237\u753b\u50cf (ICP)")
    pdf.txt(
        "\u6211\u4eec\u7684\u7406\u60f3\u5ba2\u6237\u662f\u51c6\u5907\u901a\u8fc7FDA 510(k)\u9014\u5f84\u8fdb\u5165\u7f8e\u56fd\u5e02\u573a\u7684"
        "\u4e2d\u56fd\u533b\u7597\u5668\u68b0\u4f01\u4e1a\u3002\u5173\u952e\u7279\u5f81:")
    pdf.bul("\u4f01\u4e1a\u89c4\u6a21: 50-500\u4eba\uff0c\u6536\u5165$10M-$100M")
    pdf.bul("\u5df2\u6709NMPA\u6279\u51c6\u7684\u4ea7\u54c1\uff0c\u5e0c\u671b\u5e26\u5230\u7f8e\u56fd")
    pdf.bul("\u9884\u7b97: $50K-$500K\u7528\u4e8e\u7f8e\u56fd\u5e02\u573a\u8fdb\u5165")
    pdf.bul("\u51b3\u7b56\u8005: \u6cd5\u89c4VP\u3001CEO\u6216\u56fd\u9645\u4e1a\u52a1\u8d1f\u8d23\u4eba")
    pdf.bul("\u75db\u70b9: \u4e0d\u719f\u6089FDA\u6d41\u7a0b\uff0c\u65e0\u7f8e\u56fd\u6cd5\u89c4\u56e2\u961f\uff0c\u8bed\u8a00\u969c\u788d")
    pdf.bul("\u65f6\u95f4\u7ebf: 12-24\u4e2a\u6708\u83b7\u5f97FDA\u6279\u51c6")

    # 2. \u4ea7\u54c1\u5b9a\u4f4d
    pdf.add_page()
    pdf.sec(2, "\u4ea7\u54c1\u5b9a\u4f4d")

    pdf.sub("2.1 \u7535\u68af\u6f14\u8bf4 (30\u79d2)")
    pdf.txt(
        "'510k Bridge\u662f\u552f\u4e00\u5c06AI\u9a71\u52a8\u7684\u5148\u5bfc\u5668\u68b0\u7814\u7a76\u3001"
        "16\u6807\u7b7ePM\u4eea\u8868\u677f\u3001\u8f7b\u91cf\u7ea7QMS\u548cFDA\u901a\u4fe1\u81ea\u52a8\u5316"
        "\u7ed3\u5408\u7684\u53cc\u8bed\u5e73\u53f0\uff0c\u4e13\u4e3a\u4e2d\u56fd\u533b\u7597\u5668\u68b0"
        "\u4f01\u4e1a\u8ffd\u6c42510(k)\u6279\u51c6\u800c\u6253\u9020\u3002'")

    pdf.sub("2.2 \u4ef7\u503c\u4e3b\u5f20")
    pdf.txt(
        "  \u5bf9CEO: '\u5728\u4e00\u4e2a\u4eea\u8868\u677f\u4e2d\u67e5\u770b\u60a8\u7684\u6574\u4e2a510(k)\u9879\u76ee -- "
        "\u91cc\u7a0b\u7891\u3001\u95e8\u7981\u3001\u98ce\u9669\u3001\u9884\u7b97\u548c\u6295\u8d44\u8005\u5173\u7cfb -- \u4e2d\u82f1\u6587\u5747\u53ef\u3002'\n\n"
        "  \u5bf9\u6cd5\u89c4VP: '\u51e0\u5206\u949f\u5185\u627e\u5230\u6b63\u786e\u7684\u5148\u5bfc\u5668\u68b0\u3002"
        "\u81ea\u52a8\u751f\u6210SE\u8bba\u8bc1\u8349\u7a3f\u5e76\u8ffd\u6eaf\u5148\u5bfc\u94fe\u3002'\n\n"
        "  \u5bf9CFO: '\u5c06\u71c3\u70e7\u7387\u3001\u8dd1\u9053\u548c\u6295\u8d44\u8005\u7ba1\u9053\u4e0e\u6cd5\u89c4\u65f6\u95f4\u7ebf\u4e00\u8d77\u8ddf\u8e2a\u3002"
        "\u786e\u5207\u77e5\u9053\u4f55\u65f6\u9700\u8981\u4e0b\u4e00\u8f6e\u878d\u8d44\u3002'")

    pdf.sub("2.3 \u5dee\u5f02\u5316\u4f18\u52bf")
    pdf.bul("\u53cc\u8bed\u5e73\u53f0 -- \u4e2d\u82f1\u6587\u5b8c\u6574\u652f\u6301")
    pdf.bul("AI\u5148\u5bfc\u5668\u68b0\u7814\u7a76 -- \u670d\u52a1\u5305\u542b\uff0c\u975e\u53e6\u884c\u6536\u8d39")
    pdf.bul("QMS-Lite -- \u4e13\u4e3a\u521d\u521b\u4f01\u4e1a\u8bbe\u8ba1\u7684\u8f7b\u91cf\u7ea7\u8d28\u91cf\u7ba1\u7406\u7cfb\u7edf")
    pdf.bul("FDA\u901a\u4fe1\u4e2d\u5fc3 -- Q-Sub\u3001RTA 17\u9879\u81ea\u68c0\u3001SE\u51b3\u7b56\u6d41\u7a0b")
    pdf.bul("\u8de8\u5883\u5b9e\u4f53\u8bbe\u7acb -- Delaware\u516c\u53f8\u3001\u94f6\u884c\u5f00\u6237\u3001\u7f8e\u56fd\u4ee3\u7406\u4eba")
    pdf.bul("16\u6807\u7b7e\u4eea\u8868\u677f -- \u53cc\u8f68\u3001\u95e8\u7981\u3001\u98ce\u9669\u3001\u9884\u7b97\u3001\u6295\u8d44\u8005")
    pdf.bul("\u4e0a\u6d77\u529e\u4e8b\u5904 -- \u672c\u5730\u652f\u6301\u548c\u5546\u52a1\u62d3\u5c55")
    pdf.bul("PMP\u8ba4\u8bc1\u9879\u76ee\u7ecf\u7406 -- \u4e0d\u662f\u5355\u7eaf\u7684\u8f6f\u4ef6")

    # 3. \u4ea7\u54c1\u5957\u4ef6\u4e0e\u5b9a\u4ef7
    pdf.add_page()
    pdf.sec(3, "\u4ea7\u54c1\u5957\u4ef6\u4e0e\u5b9a\u4ef7")

    pdf.sub("3.1 510(k) Predicate Finder (\u670d\u52a1\u5305\u542b)")
    pdf.txt(
        "  \u6240\u6709\u670d\u52a1\u5305\u542b Predicate Finder\u3002\n"
        "  AI\u9a71\u52a8\u7684\u5148\u5bfc\u5668\u68b0\u641c\u7d22\u3001\u5148\u5bfc\u94fe\u8ffd\u6eaf\u3001\n"
        "  \u591a\u5668\u68b0\u5bf9\u6bd4\u3001SE\u8bba\u8bc1\u751f\u6210\u5668\u3001PDF\u5bfc\u51fa\u3002\n"
        "  \u76ee\u7684: \u5f15\u6d41\u3002\u514d\u8d39\u5de5\u5177\u5438\u5f15\u5ba2\u6237\u4f53\u9a8c\u5e73\u53f0\u3002")

    pdf.sub("3.2 Control Tower PM \u4eea\u8868\u677f")
    pdf.txt(
        "  Starter ($500/\u6708) -- 1\u4e2a\u9879\u76ee\uff0c\u53ea\u8bfb\u4eea\u8868\u677f\n"
        "  Growth ($1,000/\u6708) -- 2\u4e2a\u9879\u76ee\uff0c\u5b8c\u6574\u4eea\u8868\u677f\uff0c\u6d88\u606f\u677f\n"
        "  Scale ($2,000/\u6708) -- \u65e0\u9650\u9879\u76ee\uff0c\u5d4c\u5165Predicate Finder\uff0c\u80a1\u6743\u8868\uff0cFDA\u901a\u4fe1")

    pdf.sub("3.3 QMS-Lite \u521d\u521b\u7248")
    pdf.txt(
        "  \u57fa\u7840\u7248 ($200/\u6708) -- CAPA/DMR\u6a21\u677f\uff0cISO 13485\u68c0\u67e5\u8868\n"
        "  \u4e13\u4e1a\u7248 ($500/\u6708) -- DHF\u5c55\u793a\uff0c\u6280\u672f\u6587\u4ef6\u5b58\u50a8\uff0c\u5ba1\u8ba1\u5c31\u7eea\u8bc4\u5206")

    pdf.sub("3.4 \u8de8\u5883\u5b9e\u4f53\u8bbe\u7acb\u8ffd\u8e2a\u5668")
    pdf.txt(
        "  \u9879\u76ee\u5236 ($1K-5K) \u6216 \u8ba2\u9605 ($200/\u6708)\n"
        "  Delaware\u516c\u53f8\u8bbe\u7acb\u3001EIN\u3001\u94f6\u884c\u5f00\u6237\u3001\u7f8e\u56fd\u4ee3\u7406\u4eba\u8bbe\u7f6e")

    pdf.sub("3.5 \u4e13\u4e1a\u670d\u52a1")
    pdf.txt(
        "  \u6cd5\u89c4\u54a8\u8be2: $250-500/\u5c0f\u65f6\n"
        "  \u9879\u76ee\u7ba1\u7406\u6708\u8d39: $10-25K/\u6708 (\u542b\u7f8e\u56fd\u4ee3\u7406\u4eba)\n"
        "  \u4f01\u4e1a\u7ea7\u53c2\u4e0e: $50-200K+ \u6bcf\u4e2a\u9879\u76ee")

    # 4. \u9500\u552e\u6d41\u7a0b
    pdf.add_page()
    pdf.sec(4, "\u9500\u552e\u6d41\u7a0b")

    pdf.sub("4.1 \u6f14\u793a\u811a\u672c")
    pdf.txt(
        "  1. \u6253\u5f00Predicate Finder\uff08\u670d\u52a1\u5305\u542b\u5de5\u5177\uff0c\u5b9e\u65f6\uff09\n"
        "     -- \u641c\u7d22\u5ba2\u6237\u7684\u4ea7\u54c1\u4ee3\u7801\u6216\u5668\u68b0\u540d\u79f0\n"
        "     -- \u5c55\u793a\u5148\u5bfc\u94fe\u8ffd\u6eaf\uff08\u8fd9\u91cc\u5ba2\u6237\u773c\u524d\u4e00\u4eae\uff09\n"
        "     -- \u751f\u6210SE\u8bba\u8bc1\u8349\u7a3f\n"
        "     '\u8fd9\u5df2\u5305\u542b\u5728\u670d\u52a1\u4e2d\u3002\u60f3\u8c61\u4e00\u4e0b\u5b8c\u6574\u5e73\u53f0\u80fd\u505a\u4ec0\u4e48\u3002'\n\n"
        "  2. \u5207\u6362\u5230Control Tower\u6f14\u793a\n"
        "     -- \u7528\u4e2d\u6587\u5c55\u793a\u53cc\u8f68\u91cc\u7a0b\u7891\n"
        "     -- \u5207\u6362\u82f1\u6587\u5c55\u793a\u53cc\u8bed\n"
        "     -- \u6253\u5f00FDA\u901a\u4fe1\u6807\u7b7e\uff0c\u5c55\u793aQ-Sub\u3001RTA 17\u9879\u81ea\u68c0\u3001SE\u51b3\u7b56\u6d41\u7a0b\n"
        "     -- \u6253\u5f00\u95e8\u7981\u7cfb\u7edf\uff0c\u5c55\u793aPMP\u51b3\u7b56\u6d41\u7a0b\n"
        "     '\u8fd9\u662f\u60a8\u4ece\u7b2c\u4e00\u5929\u5230FDA\u6279\u51c6\u7684\u6307\u6325\u4e2d\u5fc3\u3002'\n\n"
        "  3. \u5c55\u793aQMS-Lite\n"
        "     -- CAPA/DMR\u6a21\u677f\uff0cISO 13485\u68c0\u67e5\u8868\n"
        "     -- '\u5f88\u591a\u521d\u521b\u4f01\u4e1a\u7528Excel\u7ba1\u7406\u8d28\u91cf\u3002\u8fd9\u662f\u4e13\u4e3a510(k)\u8bbe\u8ba1\u7684\u3002'\n\n"
        "  4. \u670d\u52a1\u63a8\u4ecb\n"
        "     -- '\u60a8\u53ef\u4ee5\u81ea\u5df1\u8fd0\u884c\uff0c\u4e5f\u53ef\u4ee5\u8ba9\u6211\u4eec\u4e3a\u60a8\u8fd0\u884c\u3002'\n"
        "     -- \u63d0\u53ca\u8de8\u5883\u5b9e\u4f53\u8bbe\u7acb\u670d\u52a1\n"
        "     -- \u63d0\u4f9b\u514d\u8d3930\u5929Control Tower Starter\u8bd5\u7528")

    # 5. \u5f02\u8bae\u5904\u7406
    pdf.add_page()
    pdf.sec(5, "\u5f02\u8bae\u5904\u7406")

    pdf.kv("'\u6211\u4eec\u5df2\u7ecf\u6709\u987e\u95ee\u4e86'",
           "\u5f88\u597d -- \u6211\u4eec\u8865\u5145\u987e\u95ee\u3002\u6211\u4eec\u63d0\u4f9bPM\u5e73\u53f0\u3001QMS\u548c\u5148\u5bfc\u7814\u7a76\u5de5\u5177\u3002"
           "\u60a8\u7684\u987e\u95ee\u4e5f\u53ef\u4ee5\u767b\u5f55\u4eea\u8868\u677f\u3002")
    pdf.kv("'\u592a\u8d35\u4e86'",
           "\u5931\u8d25\u7684510(k)\u91cd\u65b0\u63d0\u4ea4\u8d39\u7528\u8d85\u8fc7$200K\u3002\u6211\u4eec\u7684\u5e73\u53f0\u53ea\u662f\u5176\u4e2d\u4e00\u5c0f\u90e8\u5206\u3002"
           "QMS-Lite\u4ece$200/\u6708\u8d77\u3002Predicate Finder\u5df2\u5305\u542b\u5728\u670d\u52a1\u4e2d\u3002")
    pdf.kv("'\u6211\u4eec\u7528Excel'",
           "Excel\u65e0\u6cd5\u751f\u6210SE\u8bba\u8bc1\u3001\u8ffd\u6eaf\u5148\u5bfc\u94fe\u3001\u7ba1\u7406CAPA/DMR\u6216\u7ed9\u6295\u8d44\u8005\u63d0\u4f9b\u5b9e\u65f6\u4eea\u8868\u677f\u3002"
           "\u8fd9\u662f\u4e13\u4e3a510(k)\u6253\u9020\u7684\u3002")
    pdf.kv("'\u8fd8\u6ca1\u51c6\u5907\u597d'",
           "\u8ba1\u5212510(k)\u7684\u6700\u4f73\u65f6\u95f4\u662f\u63d0\u4ea4\u524d12-18\u4e2a\u6708\u3002"
           "Predicate Finder\u5df2\u5305\u542b\u5728\u670d\u52a1\u4e2d -- \u73b0\u5728\u5c31\u7814\u7a76\u60a8\u7684\u5148\u5bfc\u5668\u68b0\u3002")

    # 6. \u6307\u6807\u4e0e\u76ee\u6807
    pdf.add_page()
    pdf.sec(6, "\u6307\u6807\u4e0e\u76ee\u6807\uff08\u7b2c1\u5e74\uff09")
    pdf.txt(
        "  Predicate Finder\u6ce8\u518c\u7528\u6237: 500\n"
        "  Control Tower\u4ed8\u8d39\u5ba2\u6237: 5\n"
        "  QMS-Lite\u8ba2\u9605: 10\n"
        "  \u4e13\u4e1a\u670d\u52a1\u6708\u8d39: 2\n"
        "  \u6708\u5ea6\u7ecf\u5e38\u6027\u6536\u5165: Q4\u8fbe$25K\n"
        "  \u5e73\u5747\u4ea4\u6613\u89c4\u6a21: $50K/\u5e74\n"
        "  \u9500\u552e\u5468\u671f: 30-60\u5929\uff08SaaS\uff09/ 60-90\u5929\uff08\u670d\u52a1\uff09\n"
        "  \u6f14\u793a\u5230\u6210\u4ea4\u7387: 30%")

    path = os.path.join(OUT_DIR, "Sales_Playbook_CN.pdf")
    pdf.output(path)
    return path


if __name__ == "__main__":
    en = build_english()
    print(f"Generated: {en}")
    cn = build_chinese()
    print(f"Generated: {cn}")
