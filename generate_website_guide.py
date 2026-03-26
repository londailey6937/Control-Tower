#!/usr/bin/env python3
"""
Generate a client-facing 510(k) Pathway Guide PDF (EN + CN).
This is a marketing asset for 510kbridge.com — demonstrates expertise
without exposing internal IP or project-specific details.
"""

import os
from fpdf import FPDF

OUT = os.path.dirname(os.path.abspath(__file__))

_MAP = str.maketrans({
    "\u2014": "--", "\u2013": "-", "\u2019": "'", "\u201c": '"', "\u201d": '"',
    "\u2018": "'", "\u2265": ">=", "\u2264": "<=", "\u00b5": "u", "\u00d7": "x",
    "\u2022": "-", "\u2026": "...", "\u00ae": "(R)",
})


def _a(s):
    return s.translate(_MAP)


# ═══════════════════════════════════════════
#  ENGLISH GUIDE
# ═══════════════════════════════════════════

class GuideEN(FPDF):
    CARDINAL = (140, 21, 21)
    DARK = (35, 35, 40)
    GRAY = (110, 110, 120)
    ACCENT = (0, 98, 71)
    BLUE = (30, 90, 200)
    WHITE = (255, 255, 255)

    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(*self.GRAY)
        self.cell(0, 4, _a("510k Bridge  |  510(k) Pathway Guide for Chinese Medical Device Companies"), align="R")
        self.ln(5)

    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(*self.GRAY)
        self.cell(0, 4, f"Page {self.page_no()}/{{nb}}", align="C")

    def sec(self, title):
        if self.get_y() > self.h - self.b_margin - 30:
            self.add_page()
        self.ln(3)
        self.set_fill_color(*self.CARDINAL)
        w = self.w - self.l_margin - self.r_margin
        self.rect(self.l_margin, self.get_y(), w, 10, style="F")
        self.set_font("Helvetica", "B", 12)
        self.set_text_color(*self.WHITE)
        self.set_x(self.l_margin + 3)
        self.cell(0, 10, _a(title))
        self.ln(12)

    def sub(self, title):
        if self.get_y() > self.h - self.b_margin - 25:
            self.add_page()
        self.ln(1)
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(*self.ACCENT)
        self.cell(0, 6, _a(title), new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(*self.ACCENT)
        self.set_line_width(0.3)
        self.line(self.l_margin, self.get_y(), self.l_margin + 50, self.get_y())
        self.ln(2)

    def txt(self, text):
        self.set_font("Helvetica", "", 9.5)
        self.set_text_color(*self.DARK)
        self.multi_cell(0, 5, _a(text), align="L")
        self.ln(2)

    def bul(self, text):
        self.set_font("Helvetica", "", 9.5)
        self.set_text_color(*self.DARK)
        self.cell(5, 5, "-")
        self.multi_cell(0, 5, _a(text), align="L")
        self.ln(0.5)

    def kv(self, key, val):
        self.set_font("Helvetica", "B", 9.5)
        self.set_text_color(*self.BLUE)
        self.cell(42, 5, _a(key))
        self.set_font("Helvetica", "", 9.5)
        self.set_text_color(*self.DARK)
        self.multi_cell(0, 5, _a(val), align="L")
        self.ln(0.5)

    def callout(self, text):
        self.set_fill_color(240, 250, 245)
        self.set_draw_color(*self.ACCENT)
        self.set_line_width(0.5)
        x0, y0, w = self.l_margin, self.get_y(), self.w - self.l_margin - self.r_margin
        self.set_font("Helvetica", "I", 9)
        self.set_text_color(*self.ACCENT)
        self.set_x(x0 + 3)
        self.multi_cell(w - 6, 5, _a(text), align="L", fill=True)
        y1 = self.get_y()
        self.line(x0, y0, x0, y1)
        self.ln(3)


def build_en():
    pdf = GuideEN()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.add_page()

    # ── Cover ──
    pdf.ln(30)
    pdf.set_font("Helvetica", "B", 28)
    pdf.set_text_color(*GuideEN.CARDINAL)
    pdf.cell(0, 14, "510(k) Pathway Guide", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)
    pdf.set_font("Helvetica", "", 16)
    pdf.set_text_color(*GuideEN.DARK)
    pdf.cell(0, 8, "For Chinese Medical Device Companies", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 8, "Entering the US Market", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)
    pdf.set_font("Helvetica", "I", 11)
    pdf.set_text_color(*GuideEN.GRAY)
    pdf.cell(0, 7, "Presented by 510k Bridge", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 7, "info@510kbridge.com  |  510kbridge.com", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(6)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(*GuideEN.GRAY)
    pdf.cell(0, 6, "March 2026  |  Version 1.0", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(15)
    pdf.set_font("Helvetica", "I", 9)
    pdf.set_text_color(*GuideEN.GRAY)
    pdf.multi_cell(0, 5,
        _a("This guide provides a practical overview of the FDA 510(k) clearance pathway "
           "for Chinese medical device companies. It covers key concepts, timelines, "
           "common pitfalls, and strategic recommendations to help you plan your US "
           "market entry successfully."),
        align="C")

    # ── 1. Is 510(k) Right for You? ──
    pdf.add_page()
    pdf.sec("1.  Is 510(k) Right for You?")
    pdf.txt(
        "The FDA classifies medical devices into three classes based on risk. "
        "Your regulatory pathway depends on your device classification:")
    pdf.kv("Class I", "Low risk (e.g., bandages, tongue depressors). Most are exempt from 510(k). Simple registration.")
    pdf.kv("Class II", "Moderate risk (e.g., powered wheelchairs, infusion pumps, patient monitors). "
           "Most require 510(k) clearance by demonstrating 'substantial equivalence' to a predicate device.")
    pdf.kv("Class III", "High risk (e.g., implantable pacemakers, heart valves). Requires Pre-Market Approval (PMA) -- "
           "a much longer and more expensive process.")
    pdf.ln(2)
    pdf.callout(
        "Most Chinese medical device companies entering the US market have Class II devices. "
        "If your device is Class II, the 510(k) pathway is almost certainly the right choice.")
    pdf.sub("How to Confirm Your Classification")
    pdf.txt("Steps to verify your device's FDA classification:")
    pdf.bul("Search the FDA Product Classification Database (accessdata.fda.gov)")
    pdf.bul("Identify your device's product code (e.g., IKN for sEMG, DQS for EIT)")
    pdf.bul("Check the regulation number and classification panel")
    pdf.bul("If uncertain, submit a Pre-Submission (Q-Sub) request to FDA for guidance")

    # ── 2. The 510(k) Timeline ──
    pdf.add_page()
    pdf.sec("2.  The 510(k) Timeline: What to Expect")
    pdf.txt(
        "A realistic 510(k) timeline for a non-invasive Class II device is 12-18 months "
        "from project start to FDA clearance. Here is a typical breakdown:")
    pdf.kv("Months 0-2", "Regulatory Strategy: Identify predicates, product codes, and applicable "
           "standards. Prepare and submit the Pre-Submission (Q-Sub) request to FDA.")
    pdf.kv("Months 2-4", "FDA Pre-Sub Meeting: Receive FDA feedback on your testing strategy, "
           "predicate selection, and intended use statement.")
    pdf.kv("Months 3-8", "Design Controls & Testing: Complete bench testing, biocompatibility "
           "(if applicable), software validation, electrical safety (IEC 60601), and EMC testing.")
    pdf.kv("Months 6-10", "Clinical Evidence: Compile clinical data -- literature review, bench "
           "study reports, and/or clinical studies (often not required for non-invasive devices).")
    pdf.kv("Months 10-13", "Submission Preparation: Compile the 510(k) package including "
           "performance data, substantial equivalence arguments, labeling, and software documentation.")
    pdf.kv("Months 13-18", "FDA Review: Submit to FDA. Respond to any Additional Information (AI) "
           "requests. Average review time is 90-120 days for a traditional 510(k).")
    pdf.ln(2)
    pdf.callout(
        "Key insight: The Pre-Submission meeting (Q-Sub) at months 2-4 is the single "
        "most important step. It lets you align with FDA before investing in expensive testing.")

    # ── 3. Pre-Submission Strategy ──
    pdf.add_page()
    pdf.sec("3.  Pre-Submission Strategy: Engage FDA Early")
    pdf.txt(
        "A Pre-Submission (Q-Sub) is a formal request to meet with FDA and discuss your "
        "regulatory strategy before filing the actual 510(k). It is optional but strongly "
        "recommended -- especially for first-time submissions from companies new to the US market.")
    pdf.sub("What to Include in Your Q-Sub")
    pdf.bul("Device description and intended use")
    pdf.bul("Proposed predicate device(s) with substantial equivalence rationale")
    pdf.bul("Proposed testing plan (bench, biocompatibility, clinical)")
    pdf.bul("Specific questions for FDA (e.g., 'Is this predicate acceptable?', "
            "'Do you agree with our testing approach?')")
    pdf.sub("Q-Sub Process")
    pdf.bul("Submit the Q-Sub package to CDRH (Center for Devices and Radiological Health)")
    pdf.bul("FDA sends a response letter within 75 days (often with written answers)")
    pdf.bul("If a meeting is requested, it typically occurs at day 70-75")
    pdf.bul("The meeting is teleconference-based (no need to travel to the US)")
    pdf.sub("Benefits")
    pdf.bul("Reduces risk of RTA (Refuse to Accept) on your actual submission")
    pdf.bul("Confirms that your predicate selection is acceptable to FDA")
    pdf.bul("Identifies any testing gaps before you invest in expensive lab work")
    pdf.bul("Creates an FDA record that demonstrates proactive regulatory engagement")

    # ── 4. Key Regulatory Standards ──
    pdf.add_page()
    pdf.sec("4.  Key Regulatory Standards")
    pdf.txt(
        "FDA expects Class II devices to comply with recognized consensus standards. "
        "The specific standards depend on your device type, but most non-invasive "
        "medical electrical equipment needs the following:")
    pdf.kv("IEC 60601-1", "General requirements for basic safety and essential performance of medical "
           "electrical equipment. This is the foundation standard.")
    pdf.kv("IEC 60601-1-2", "Electromagnetic compatibility (EMC) -- immunity and emissions testing. "
           "Essential for any device with electronic components.")
    pdf.kv("ISO 14971", "Risk management. Required for all medical devices. Demonstrates systematic "
           "identification and mitigation of hazards.")
    pdf.kv("IEC 62304", "Software lifecycle processes. Required if your device contains software "
           "(standalone or embedded). Defines software development class (A, B, or C) based on risk.")
    pdf.kv("ISO 10993", "Biocompatibility testing. Required if any component contacts the patient. "
           "Non-invasive surface-contact devices typically need a subset of tests.")
    pdf.kv("IEC 62366-1", "Usability engineering. Demonstrates that the user interface is safe "
           "and effective through formative and summative usability studies.")
    pdf.ln(2)
    pdf.callout(
        "Tip: You do not need to test against every standard on the FDA list. The Q-Sub "
        "meeting (Section 3) helps you identify exactly which standards FDA expects for "
        "your specific device.")

    # ── 5. Common Pitfalls ──
    pdf.add_page()
    pdf.sec("5.  Common Pitfalls & How to Avoid Them")
    pdf.sub("5.1 RTA (Refuse to Accept)")
    pdf.txt(
        "FDA screens every 510(k) submission within 15 days of receipt using an RTA checklist. "
        "If critical elements are missing, the submission is refused before substantive review "
        "even begins. Common RTA triggers:")
    pdf.bul("Missing or incomplete Indications for Use statement")
    pdf.bul("Inadequate predicate comparison (technological characteristics)")
    pdf.bul("Missing software documentation (if applicable)")
    pdf.bul("Incomplete performance testing summaries")
    pdf.bul("Labeling deficiencies")

    pdf.sub("5.2 Predicate Selection Errors")
    pdf.txt("Choosing the wrong predicate device is one of the most expensive mistakes:")
    pdf.bul("Predicate must have the same intended use as your device")
    pdf.bul("Technological differences must not raise new safety or effectiveness questions")
    pdf.bul("Avoid 'predicate creep' -- chaining through multiple predicates weakens your argument")
    pdf.bul("FDA may disagree with your predicate -- the Q-Sub resolves this early")

    pdf.sub("5.3 Testing Gaps")
    pdf.txt("Insufficient test data is the #1 reason for Additional Information (AI) requests:")
    pdf.bul("Ensure bench testing matches the testing plan discussed in the Q-Sub")
    pdf.bul("Software validation must follow IEC 62304 classification rigor")
    pdf.bul("EMC testing must use the latest IEC 60601-1-2 edition")
    pdf.bul("If clinical data is needed, start early -- clinical studies add 6-12 months")

    pdf.sub("5.4 Translation & Cultural Gaps")
    pdf.txt(
        "FDA submissions must be in English. Technical accuracy in translation is critical -- "
        "mistranslated terminology can cause rejection or misunderstanding. "
        "Work with a regulatory team that is fluent in both languages and FDA terminology.")

    # ── 6. US Entity Requirements ──
    pdf.add_page()
    pdf.sec("6.  US Entity Requirements")
    pdf.txt(
        "To sell a medical device in the United States, your company must meet "
        "several establishment and registration requirements:")
    pdf.sub("6.1 FDA Establishment Registration")
    pdf.bul("Every establishment that manufactures, distributes, or imports medical devices "
            "must register with FDA annually")
    pdf.bul("Registration is done through the FDA Unified Registration and Listing System (FURLS)")
    pdf.bul("A US Agent must be designated if the manufacturer is located outside the US")

    pdf.sub("6.2 US Agent")
    pdf.bul("Required for all foreign manufacturers selling into the US market")
    pdf.bul("The US Agent acts as the FDA's point of contact for your company")
    pdf.bul("Must be located in the United States and available during business hours")
    pdf.bul("Can be a company or individual -- several firms specialize in this service")

    pdf.sub("6.3 Device Listing")
    pdf.bul("Each device must be listed with FDA, including product code and device class")
    pdf.bul("Listing must be updated when devices are added, removed, or modified")

    pdf.sub("6.4 US Entity Formation (Optional)")
    pdf.txt(
        "While not required by FDA, many Chinese companies form a US subsidiary (typically a "
        "Delaware LLC or C-Corp) for business, legal, and investor-relations purposes. "
        "This simplifies contracts, banking, and demonstrates commitment to the US market.")

    # ── 7. Cost Planning ──
    pdf.add_page()
    pdf.sec("7.  Cost Planning")
    pdf.txt(
        "Budget planning is essential. Here are typical cost ranges for a Class II "
        "non-invasive 510(k) submission (all figures in USD):")
    pdf.kv("FDA User Fee", "$22,000-$23,000 (standard 510(k), updated annually; small business "
           "exemptions may apply)")
    pdf.kv("Testing (IEC 60601)", "$30,000-$80,000 depending on device complexity and number "
           "of applicable particular standards")
    pdf.kv("EMC Testing", "$15,000-$30,000 for IEC 60601-1-2 compliance")
    pdf.kv("Software (IEC 62304)", "$10,000-$40,000 for documentation and validation, depending "
           "on software safety class")
    pdf.kv("Biocompatibility", "$10,000-$50,000 depending on patient-contact characterization")
    pdf.kv("Regulatory Consulting", "$50,000-$150,000 for end-to-end project management, "
           "strategy, submission preparation, and FDA liaison")
    pdf.kv("US Agent", "$3,000-$6,000 per year")
    pdf.kv("US Entity Formation", "$2,000-$5,000 (one-time, if applicable)")
    pdf.ln(2)
    pdf.callout(
        "Total budget: Plan for $150,000-$400,000 for a typical Class II 510(k) submission. "
        "The largest variable is testing -- the Q-Sub meeting helps define exactly what "
        "testing is needed, so you avoid over-testing or under-testing.")

    # ── 8. How 510k Bridge Can Help ──
    pdf.add_page()
    pdf.sec("8.  How 510k Bridge Can Help")
    pdf.txt(
        "510k Bridge specializes in helping Chinese medical device companies navigate "
        "the FDA 510(k) process. Our bilingual team bridges the language, regulatory, "
        "and business culture gap between China and the US market.")

    pdf.sub("Control Tower License -- From $500/mo")
    pdf.bul("Dedicated project dashboard with 15-tab Control Tower platform")
    pdf.bul("Bilingual setup wizard (EN/CN) for rapid project onboarding")
    pdf.bul("Dual-track milestone tracking (regulatory + engineering)")
    pdf.bul("Regulatory document control and risk monitoring")
    pdf.bul("Real-time bilingual team messaging")

    pdf.sub("Professional PM -- $10-25K/mo")
    pdf.bul("Everything in SaaS, plus dedicated PMP project manager")
    pdf.bul("FDA Communications Center with Q-Sub automation")
    pdf.bul("Gate review management and regulatory submission oversight")
    pdf.bul("Supplier coordination and stakeholder management")

    pdf.sub("Enterprise -- Project-Based Pricing")
    pdf.bul("Everything in Professional, plus end-to-end 510(k) management")
    pdf.bul("Regulatory strategy and pathway development")
    pdf.bul("Automated RTA self-check and DHF readiness assessment")
    pdf.bul("US entity formation assistance")
    pdf.bul("Investor-ready documentation")

    pdf.ln(4)
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(*GuideEN.CARDINAL)
    pdf.cell(0, 8, "Ready to start your 510(k) journey?", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(*GuideEN.DARK)
    pdf.cell(0, 6, "info@510kbridge.com", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 6, "510kbridge.com", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 6, "Schedule a free consultation today.", align="C", new_x="LMARGIN", new_y="NEXT")

    path = os.path.join(OUT, "510k_Pathway_Guide_EN.pdf")
    pdf.output(path)
    return path


# ═══════════════════════════════════════════
#  CHINESE GUIDE
# ═══════════════════════════════════════════

class GuideCN(FPDF):
    CARDINAL = (140, 21, 21)
    DARK = (35, 35, 40)
    GRAY = (110, 110, 120)
    ACCENT = (0, 98, 71)
    BLUE = (30, 90, 200)
    WHITE = (255, 255, 255)

    def __init__(self):
        super().__init__()
        font_path = "/Library/Fonts/Arial Unicode.ttf"
        self.add_font("ARUNI", "", font_path, uni=True)
        self.add_font("ARUNI", "B", font_path, uni=True)
        self.add_font("ARUNI", "I", font_path, uni=True)

    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("ARUNI", "I", 7)
        self.set_text_color(*self.GRAY)
        self.cell(0, 4, "510k Bridge  |  中国医疗器械企业510(k)通关指南", align="R")
        self.ln(5)

    def footer(self):
        self.set_y(-12)
        self.set_font("ARUNI", "I", 7)
        self.set_text_color(*self.GRAY)
        self.cell(0, 4, f"第 {self.page_no()}/{{nb}} 页", align="C")

    def sec(self, title):
        if self.get_y() > self.h - self.b_margin - 30:
            self.add_page()
        self.ln(3)
        self.set_fill_color(*self.CARDINAL)
        w = self.w - self.l_margin - self.r_margin
        self.rect(self.l_margin, self.get_y(), w, 10, style="F")
        self.set_font("ARUNI", "B", 12)
        self.set_text_color(*self.WHITE)
        self.set_x(self.l_margin + 3)
        self.cell(0, 10, title)
        self.ln(12)

    def sub(self, title):
        if self.get_y() > self.h - self.b_margin - 25:
            self.add_page()
        self.ln(1)
        self.set_font("ARUNI", "B", 10)
        self.set_text_color(*self.ACCENT)
        self.cell(0, 6, title, new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(*self.ACCENT)
        self.set_line_width(0.3)
        self.line(self.l_margin, self.get_y(), self.l_margin + 50, self.get_y())
        self.ln(2)

    def txt(self, text):
        self.set_font("ARUNI", "", 9.5)
        self.set_text_color(*self.DARK)
        self.multi_cell(0, 5, text, align="L")
        self.ln(2)

    def bul(self, text):
        self.set_font("ARUNI", "", 9.5)
        self.set_text_color(*self.DARK)
        self.cell(5, 5, "- ")
        self.multi_cell(0, 5, text, align="L")
        self.ln(0.5)

    def kv(self, key, val):
        self.set_font("ARUNI", "B", 9.5)
        self.set_text_color(*self.BLUE)
        self.cell(42, 5, key)
        self.set_font("ARUNI", "", 9.5)
        self.set_text_color(*self.DARK)
        self.multi_cell(0, 5, val, align="L")
        self.ln(0.5)

    def callout(self, text):
        self.set_fill_color(240, 250, 245)
        self.set_draw_color(*self.ACCENT)
        self.set_line_width(0.5)
        x0, y0, w = self.l_margin, self.get_y(), self.w - self.l_margin - self.r_margin
        self.set_font("ARUNI", "I", 9)
        self.set_text_color(*self.ACCENT)
        self.set_x(x0 + 3)
        self.multi_cell(w - 6, 5, text, align="L", fill=True)
        y1 = self.get_y()
        self.line(x0, y0, x0, y1)
        self.ln(3)


def build_cn():
    pdf = GuideCN()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.add_page()

    # ── Cover ──
    pdf.ln(30)
    pdf.set_font("ARUNI", "B", 28)
    pdf.set_text_color(*GuideCN.CARDINAL)
    pdf.cell(0, 14, "510(k) 通关指南", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)
    pdf.set_font("ARUNI", "", 16)
    pdf.set_text_color(*GuideCN.DARK)
    pdf.cell(0, 8, "中国医疗器械企业进入美国市场", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 8, "实用手册", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)
    pdf.set_font("ARUNI", "I", 11)
    pdf.set_text_color(*GuideCN.GRAY)
    pdf.cell(0, 7, "510k Bridge 出品", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 7, "info@510kbridge.com  |  510kbridge.com", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(6)
    pdf.set_font("ARUNI", "", 10)
    pdf.set_text_color(*GuideCN.GRAY)
    pdf.cell(0, 6, "2026年3月  |  版本 1.0", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(15)
    pdf.set_font("ARUNI", "I", 9)
    pdf.set_text_color(*GuideCN.GRAY)
    pdf.multi_cell(0, 5,
        "本指南为中国医疗器械企业提供FDA 510(k)审批流程的实用概览。"
        "涵盖关键概念、时间规划、常见陷阱及策略建议，"
        "帮助您成功规划美国市场准入。",
        align="C")

    # ── 1 ──
    pdf.add_page()
    pdf.sec("1.  510(k)适合您的产品吗？")
    pdf.txt(
        "FDA根据风险等级将医疗器械分为三类。"
        "您的注册路径取决于产品分类：")
    pdf.kv("I类", "低风险（如绷带、压舌板）。大多数免于510(k)，只需简单注册。")
    pdf.kv("II类", "中等风险（如电动轮椅、输液泵、患者监护仪）。"
           "大多数需要通过510(k)途径，证明与已上市\"等效器械\"（predicate）的\"实质等效性\"。")
    pdf.kv("III类", "高风险（如植入式起搏器、心脏瓣膜）。需要上市前批准(PMA)——"
           "流程更长、费用更高。")
    pdf.ln(2)
    pdf.callout(
        "大多数进入美国市场的中国医疗器械企业拥有II类产品。"
        "如果您的产品是II类，510(k)途径几乎是必然选择。")
    pdf.sub("如何确认您的产品分类")
    pdf.txt("确认产品FDA分类的步骤：")
    pdf.bul("在FDA产品分类数据库中搜索（accessdata.fda.gov）")
    pdf.bul("确定产品代码（如sEMG对应IKN，EIT对应DQS）")
    pdf.bul("查看适用法规编号和分类面板")
    pdf.bul("如不确定，向FDA提交Pre-Submission（Q-Sub）咨询请求")

    # ── 2 ──
    pdf.add_page()
    pdf.sec("2.  510(k)时间规划：预期时间表")
    pdf.txt(
        "非侵入式II类器械的510(k)从项目启动到FDA放行，通常需要12-18个月。"
        "典型阶段如下：")
    pdf.kv("第0-2个月", "法规策略：确定等效器械、产品代码和适用标准。"
           "准备并提交Pre-Submission（Q-Sub）请求。")
    pdf.kv("第2-4个月", "FDA Pre-Sub会议：获取FDA对测试策略、"
           "等效器械选择和预期用途声明的反馈。")
    pdf.kv("第3-8个月", "设计控制与测试：完成台架测试、生物兼容性（如适用）、"
           "软件验证、电气安全（IEC 60601）和EMC测试。")
    pdf.kv("第6-10个月", "临床证据：汇编临床数据——文献综述、台架研究报告"
           "和/或临床研究（非侵入式器械通常不需要）。")
    pdf.kv("第10-13个月", "提交准备：编制510(k)提交包，包含性能数据、"
           "实质等效性论证、标签和软件文档。")
    pdf.kv("第13-18个月", "FDA审查：提交至FDA。回复任何补充信息（AI）请求。"
           "传统510(k)平均审查时间为90-120天。")
    pdf.ln(2)
    pdf.callout(
        "关键洞察：第2-4个月的Pre-Submission（Q-Sub）会议是最重要的一步。"
        "它让您在投入昂贵测试之前与FDA达成一致。")

    # ── 3 ──
    pdf.add_page()
    pdf.sec("3.  Pre-Submission策略：提前与FDA沟通")
    pdf.txt(
        "Pre-Submission（Q-Sub）是向FDA正式申请会议，在提交正式510(k)之前"
        "讨论您的法规策略。Q-Sub是可选的，但强烈建议——"
        "特别是对于首次进入美国市场的企业。")
    pdf.sub("Q-Sub应包含的内容")
    pdf.bul("产品描述和预期用途")
    pdf.bul("建议的等效器械及实质等效性论证")
    pdf.bul("建议的测试计划（台架、生物兼容性、临床）")
    pdf.bul('向FDA提出的具体问题（如"该等效器械是否可接受？"、'
            '"您是否同意我们的测试方案？"）')
    pdf.sub("Q-Sub流程")
    pdf.bul("向CDRH（器械和辐射健康中心）提交Q-Sub文件包")
    pdf.bul("FDA在75天内发送回复函（通常包含书面答复）")
    pdf.bul("如请求会议，通常在第70-75天进行")
    pdf.bul("会议为远程电话会议形式（无需前往美国）")
    pdf.sub("核心优势")
    pdf.bul("降低正式提交时被RTA（拒绝接受）的风险")
    pdf.bul("确认等效器械选择是否被FDA接受")
    pdf.bul("在投入昂贵实验室测试之前发现测试缺口")
    pdf.bul("建立FDA记录，展示主动的法规沟通态度")

    # ── 4 ──
    pdf.add_page()
    pdf.sec("4.  关键法规标准")
    pdf.txt(
        "FDA期望II类器械符合公认的共识标准。具体标准取决于产品类型，"
        "但大多数非侵入性医用电气设备需要以下标准：")
    pdf.kv("IEC 60601-1", "医用电气设备基本安全和基本性能的通用要求。这是基础标准。")
    pdf.kv("IEC 60601-1-2", "电磁兼容性(EMC)——抗扰度和发射测试。"
           "所有含电子元件的器械必需。")
    pdf.kv("ISO 14971", "风险管理。所有医疗器械必需。要求系统性识别和缓解危害。")
    pdf.kv("IEC 62304", "软件生命周期过程。含软件的器械必需。根据风险定义软件开发等级(A/B/C)。")
    pdf.kv("ISO 10993", "生物兼容性测试。与患者接触的部件必需。"
           "非侵入性表面接触器械通常只需部分测试。")
    pdf.kv("IEC 62366-1", "可用性工程。通过形成性和总结性可用性研究，"
           "证明用户界面安全有效。")
    pdf.ln(2)
    pdf.callout(
        "提示：您不需要对FDA清单上的每一项标准都进行测试。"
        "Q-Sub会议（第3节）帮助您准确确定FDA对您特定产品期望的标准。")

    # ── 5 ──
    pdf.add_page()
    pdf.sec("5.  常见陷阱及规避方法")
    pdf.sub("5.1 RTA（拒绝接受）")
    pdf.txt(
        "FDA在收到510(k)提交后15天内使用RTA检查清单进行筛查。"
        "如果缺少关键要素，提交在实质性审查之前就会被拒绝。常见触发因素：")
    pdf.bul("预期用途声明缺失或不完整")
    pdf.bul("等效器械对比不充分（技术特性方面）")
    pdf.bul("软件文档缺失（如适用）")
    pdf.bul("性能测试摘要不完整")
    pdf.bul("标签缺陷")

    pdf.sub("5.2 等效器械选择错误")
    pdf.txt("选择错误的等效器械是最昂贵的错误之一：")
    pdf.bul("等效器械必须与您的产品有相同的预期用途")
    pdf.bul("技术差异不得引起新的安全性或有效性问题")
    pdf.bul("避免\"等效器械链\"——通过多个等效器械链式引用会削弱论证")
    pdf.bul("FDA可能不同意您的等效器械选择——Q-Sub可以提前解决此问题")

    pdf.sub("5.3 测试缺口")
    pdf.txt("测试数据不足是补充信息（AI）请求的首要原因：")
    pdf.bul("确保台架测试与Q-Sub讨论的测试计划一致")
    pdf.bul("软件验证必须遵循IEC 62304分级严格性")
    pdf.bul("EMC测试必须使用最新版IEC 60601-1-2")
    pdf.bul("如需临床数据，尽早启动——临床研究增加6-12个月")

    pdf.sub("5.4 翻译与文化差异")
    pdf.txt(
        "FDA提交文件必须使用英文。翻译的技术准确性至关重要——"
        "术语翻译错误可能导致被拒或误解。"
        "与精通双语和FDA术语的法规团队合作。")

    # ── 6 ──
    pdf.add_page()
    pdf.sec("6.  美国实体要求")
    pdf.txt("要在美国销售医疗器械，您的公司必须满足多项注册要求：")
    pdf.sub("6.1 FDA场所注册")
    pdf.bul("每个制造、分销或进口医疗器械的场所必须每年向FDA注册")
    pdf.bul("通过FDA统一注册和上市系统（FURLS）完成注册")
    pdf.bul("如制造商位于美国境外，必须指定美国代理人")

    pdf.sub("6.2 美国代理人（US Agent）")
    pdf.bul("所有在美国销售产品的外国制造商必须指定")
    pdf.bul("美国代理人作为FDA联系贵公司的接口")
    pdf.bul("必须位于美国境内，在工作时间可联系")
    pdf.bul("可以是公司或个人——有专门提供此服务的公司")

    pdf.sub("6.3 产品上市")
    pdf.bul("每个器械必须在FDA上市登记，包含产品代码和器械分类")
    pdf.bul("在添加、删除或修改器械后必须更新上市信息")

    pdf.sub("6.4 美国实体设立（可选）")
    pdf.txt(
        "虽然FDA不要求，但许多中国公司会成立美国子公司（通常为Delaware LLC或C-Corp），"
        "用于商业、法律和投资者关系目的。"
        "这简化了合同、银行业务，并展示对美国市场的承诺。")

    # ── 7 ──
    pdf.add_page()
    pdf.sec("7.  费用规划")
    pdf.txt(
        "预算规划至关重要。以下是II类非侵入式510(k)提交的典型费用范围（单位：美元）：")
    pdf.kv("FDA用户费", "$22,000-$23,000（标准510(k)，每年更新；可能适用小企业豁免）")
    pdf.kv("测试(IEC 60601)", "$30,000-$80,000，取决于器械复杂度和适用特定标准数量")
    pdf.kv("EMC测试", "$15,000-$30,000，IEC 60601-1-2合规")
    pdf.kv("软件(IEC 62304)", "$10,000-$40,000，文档和验证，取决于软件安全等级")
    pdf.kv("生物兼容性", "$10,000-$50,000，取决于患者接触特性")
    pdf.kv("法规咨询", "$50,000-$150,000，全流程项目管理、策略、提交准备和FDA联络")
    pdf.kv("美国代理人", "$3,000-$6,000/年")
    pdf.kv("美国实体设立", "$2,000-$5,000（一次性，如适用）")
    pdf.ln(2)
    pdf.callout(
        "总预算：典型II类510(k)提交计划$150,000-$400,000。"
        "最大变量是测试——Q-Sub会议帮助准确定义所需测试，"
        "避免测试不足或过度测试。")

    # ── 8 ──
    pdf.add_page()
    pdf.sec("8.  510k Bridge 如何帮助您")
    pdf.txt(
        "510k Bridge专注于帮助中国医疗器械企业导航FDA 510(k)流程。"
        "我们的双语团队弥合中美之间的语言、法规和商业文化差距。")

    pdf.sub("Control Tower 许可 -- 起步价$500/月")
    pdf.bul("专属项目仪表盘，15个选项卡的控制塔平台")
    pdf.bul("双语设置向导（中英文）快速项目入驻")
    pdf.bul("双轨里程碑跟踪（法规+工程）")
    pdf.bul("法规文档控制和风险监控")
    pdf.bul("实时双语团队消息")

    pdf.sub("专业PM服务 -- $10,000-$25,000/月")
    pdf.bul("SaaS全部功能，外加专属PMP项目经理")
    pdf.bul("FDA通信中心及Q-Sub自动化")
    pdf.bul("门控评审管理和法规提交监督")
    pdf.bul("供应商协调和利益相关者管理")

    pdf.sub("企业级服务 -- 按项目定价")
    pdf.bul("专业版全部功能，外加端到端510(k)管理")
    pdf.bul("法规策略和路径开发")
    pdf.bul("自动化RTA自检和DHF就绪评估")
    pdf.bul("美国实体设立协助")
    pdf.bul("面向投资者的文档支持")

    pdf.ln(4)
    pdf.set_font("ARUNI", "B", 12)
    pdf.set_text_color(*GuideCN.CARDINAL)
    pdf.cell(0, 8, "准备好开始您的510(k)之旅了吗？", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)
    pdf.set_font("ARUNI", "", 11)
    pdf.set_text_color(*GuideCN.DARK)
    pdf.cell(0, 6, "info@510kbridge.com", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 6, "510kbridge.com", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 6, "立即预约免费咨询。", align="C", new_x="LMARGIN", new_y="NEXT")

    path = os.path.join(OUT, "510k_Pathway_Guide_CN.pdf")
    pdf.output(path)
    return path


if __name__ == "__main__":
    en = build_en()
    print(f"EN Guide: {en}")
    cn = build_cn()
    print(f"CN Guide: {cn}")
    print("Done.")
