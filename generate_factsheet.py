#!/usr/bin/env python3
"""
Generate a 510k Bridge Service Fact Sheet PDF (EN + CN).
1-2 page marketing asset for 510kbridge.com.
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
#  ENGLISH FACT SHEET
# ═══════════════════════════════════════════

class FactEN(FPDF):
    CARDINAL = (140, 21, 21)
    DARK = (35, 35, 40)
    GRAY = (110, 110, 120)
    ACCENT = (0, 98, 71)
    WHITE = (255, 255, 255)
    LIGHT_BG = (248, 248, 252)

    def header(self):
        pass

    def footer(self):
        self.set_y(-10)
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(*self.GRAY)
        self.cell(0, 4, "510k Bridge  |  info@510kbridge.com  |  510kbridge.com", align="C")

    def section_bar(self, title):
        self.set_fill_color(*self.CARDINAL)
        w = self.w - self.l_margin - self.r_margin
        self.rect(self.l_margin, self.get_y(), w, 7, style="F")
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*self.WHITE)
        self.set_x(self.l_margin + 2)
        self.cell(0, 7, _a(title))
        self.ln(9)

    def txt(self, text, sz=8.5):
        self.set_font("Helvetica", "", sz)
        self.set_text_color(*self.DARK)
        self.multi_cell(0, 4.2, _a(text), align="L")
        self.ln(1.5)

    def bul(self, text, sz=8.5):
        self.set_font("Helvetica", "", sz)
        self.set_text_color(*self.DARK)
        x0 = self.get_x()
        self.cell(4, 4.2, "-")
        self.multi_cell(0, 4.2, _a(text), align="L")
        self.ln(0.3)

    def kv_line(self, key, val, sz=8.5):
        self.set_font("Helvetica", "B", sz)
        self.set_text_color(*self.ACCENT)
        self.cell(38, 4.2, _a(key))
        self.set_font("Helvetica", "", sz)
        self.set_text_color(*self.DARK)
        self.multi_cell(0, 4.2, _a(val), align="L")
        self.ln(0.5)


def build_factsheet_en():
    pdf = FactEN()
    pdf.set_auto_page_break(auto=True, margin=14)
    pdf.add_page()

    # ── Banner ──
    pdf.set_fill_color(*FactEN.CARDINAL)
    pdf.rect(0, 0, pdf.w, 28, style="F")
    pdf.set_y(6)
    pdf.set_font("Helvetica", "B", 20)
    pdf.set_text_color(*FactEN.WHITE)
    pdf.cell(0, 8, "510k Bridge", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 6, _a("Service Overview & Capabilities"), align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_y(32)

    # ── Who We Serve ──
    pdf.section_bar("WHO WE SERVE")
    pdf.txt(
        "Chinese medical device companies seeking FDA 510(k) clearance to enter "
        "the US market. We specialize in Class II non-invasive devices: patient "
        "monitors, imaging systems, rehabilitation equipment, diagnostic tools, "
        "and software-as-a-medical-device (SaMD).")

    # ── The Problem ──
    pdf.section_bar("THE PROBLEM")
    pdf.bul("Language & regulatory culture gap between NMPA and FDA processes")
    pdf.bul("No visibility into project status across distributed teams (China + US)")
    pdf.bul("Difficulty coordinating testing labs, US agents, and regulatory consultants")
    pdf.bul("High failure rates: ~30% of 510(k) submissions receive AI requests")
    pdf.bul("Costly delays from preventable errors (wrong predicate, missing test data, RTA)")

    # ── Our Solution ──
    pdf.section_bar("OUR SOLUTION")
    pdf.txt(
        "A bilingual (EN/CN) 510(k) project management platform paired with "
        "experienced regulatory professionals. From strategy through clearance, "
        "we bridge the language, process, and compliance gap.")

    # ── Platform Highlights ──
    pdf.section_bar("PLATFORM HIGHLIGHTS")
    col_w = (pdf.w - pdf.l_margin - pdf.r_margin) / 2 - 2
    x_left = pdf.l_margin
    x_right = pdf.l_margin + col_w + 4
    y0 = pdf.get_y()
    pdf.set_font("Helvetica", "", 8.5)
    pdf.set_text_color(*FactEN.DARK)
    items_left = [
        "16-tab Control Tower dashboard",
        "Bilingual 9-step setup wizard",
        "Dual-track milestone tracking",
        "FDA Communications Center",
        "Q-Sub generation automation",
    ]
    items_right = [
        "Document control with version history",
        "Risk & budget monitoring",
        "Thread-based team messaging (EN/CN)",
        "Automated RTA self-check",
        "Data Source Ref for audit traceability",
    ]
    for i, (l, r) in enumerate(zip(items_left, items_right)):
        pdf.set_xy(x_left, y0 + i * 4.5)
        pdf.cell(col_w, 4.5, _a("  -  " + l))
        pdf.set_xy(x_right, y0 + i * 4.5)
        pdf.cell(col_w, 4.5, _a("  -  " + r))
    pdf.set_y(y0 + len(items_left) * 4.5 + 2)

    # ── By The Numbers ──
    pdf.section_bar("BY THE NUMBERS")
    col3_w = (pdf.w - pdf.l_margin - pdf.r_margin) / 3
    y0 = pdf.get_y()
    stats = [
        ("12-18 mo", "Typical clearance timeline"),
        ("90-120 days", "Average FDA review period"),
        ("$150K-$400K", "End-to-end budget range"),
    ]
    for i, (big, small) in enumerate(stats):
        cx = pdf.l_margin + col3_w * i + col3_w / 2
        pdf.set_xy(pdf.l_margin + col3_w * i, y0)
        pdf.set_font("Helvetica", "B", 16)
        pdf.set_text_color(*FactEN.CARDINAL)
        pdf.cell(col3_w, 8, _a(big), align="C", new_x="LMARGIN", new_y="NEXT")
        pdf.set_xy(pdf.l_margin + col3_w * i, y0 + 8)
        pdf.set_font("Helvetica", "", 7.5)
        pdf.set_text_color(*FactEN.GRAY)
        pdf.cell(col3_w, 4, _a(small), align="C")
    pdf.set_y(y0 + 16)

    # ── Service Tiers ──
    pdf.section_bar("SERVICE TIERS")
    tiers = [
        ("SaaS Platform", "From $500/mo",
         ["Control Tower dashboard", "Bilingual setup wizard", "Dual-track milestones",
          "Document control", "Team messaging", "Risk & budget tracking"]),
        ("Professional PM", "$10-25K/mo",
         ["All SaaS features", "Dedicated PMP project manager", "FDA Comms Center",
          "US Agent representation", "Gate review management", "Submission oversight",
          "Supplier coordination"]),
        ("Enterprise", "Project-Based",
         ["All Professional features", "End-to-end 510(k) management", "Regulatory strategy",
          "RTA self-check & DHF readiness", "US Agent representation",
          "US entity formation", "Investor documentation"]),
    ]
    col_w = (pdf.w - pdf.l_margin - pdf.r_margin - 6) / 3
    y0 = pdf.get_y()
    for idx, (name, price, features) in enumerate(tiers):
        x = pdf.l_margin + idx * (col_w + 3)
        pdf.set_xy(x, y0)
        pdf.set_fill_color(*FactEN.LIGHT_BG)
        box_h = 4.5 + 5 + len(features) * 4 + 2
        pdf.rect(x, y0, col_w, box_h, style="F")
        pdf.set_xy(x + 1, y0 + 1)
        pdf.set_font("Helvetica", "B", 8.5)
        pdf.set_text_color(*FactEN.CARDINAL)
        pdf.cell(col_w - 2, 4.5, _a(name), align="C", new_x="LMARGIN", new_y="NEXT")
        pdf.set_xy(x + 1, y0 + 5)
        pdf.set_font("Helvetica", "B", 8)
        pdf.set_text_color(*FactEN.ACCENT)
        pdf.cell(col_w - 2, 4.5, _a(price), align="C", new_x="LMARGIN", new_y="NEXT")
        for j, feat in enumerate(features):
            pdf.set_xy(x + 2, y0 + 10 + j * 4)
            pdf.set_font("Helvetica", "", 7.5)
            pdf.set_text_color(*FactEN.DARK)
            pdf.cell(col_w - 4, 4, _a("- " + feat))
    pdf.set_y(y0 + 4.5 + 5 + max(len(t[2]) for t in tiers) * 4 + 5)

    # ── Contact ──
    pdf.section_bar("GET STARTED")
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(*FactEN.DARK)
    pdf.cell(0, 5, _a("info@510kbridge.com  |  510kbridge.com  |  Schedule a free consultation today."), align="C")

    path = os.path.join(OUT, "510k_Bridge_Factsheet_EN.pdf")
    pdf.output(path)
    return path


# ═══════════════════════════════════════════
#  CHINESE FACT SHEET
# ═══════════════════════════════════════════

class FactCN(FPDF):
    CARDINAL = (140, 21, 21)
    DARK = (35, 35, 40)
    GRAY = (110, 110, 120)
    ACCENT = (0, 98, 71)
    WHITE = (255, 255, 255)
    LIGHT_BG = (248, 248, 252)

    def __init__(self):
        super().__init__()
        font_path = "/Library/Fonts/Arial Unicode.ttf"
        self.add_font("ARUNI", "", font_path, uni=True)
        self.add_font("ARUNI", "B", font_path, uni=True)
        self.add_font("ARUNI", "I", font_path, uni=True)

    def header(self):
        pass

    def footer(self):
        self.set_y(-10)
        self.set_font("ARUNI", "I", 7)
        self.set_text_color(*self.GRAY)
        self.cell(0, 4, "510k Bridge  |  info@510kbridge.com  |  510kbridge.com", align="C")

    def section_bar(self, title):
        self.set_fill_color(*self.CARDINAL)
        w = self.w - self.l_margin - self.r_margin
        self.rect(self.l_margin, self.get_y(), w, 7, style="F")
        self.set_font("ARUNI", "B", 9)
        self.set_text_color(*self.WHITE)
        self.set_x(self.l_margin + 2)
        self.cell(0, 7, title)
        self.ln(9)

    def txt(self, text, sz=8.5):
        self.set_font("ARUNI", "", sz)
        self.set_text_color(*self.DARK)
        self.multi_cell(0, 4.2, text, align="L")
        self.ln(1.5)

    def bul(self, text, sz=8.5):
        self.set_font("ARUNI", "", sz)
        self.set_text_color(*self.DARK)
        self.cell(4, 4.2, "- ")
        self.multi_cell(0, 4.2, text, align="L")
        self.ln(0.3)

    def kv_line(self, key, val, sz=8.5):
        self.set_font("ARUNI", "B", sz)
        self.set_text_color(*self.ACCENT)
        self.cell(38, 4.2, key)
        self.set_font("ARUNI", "", sz)
        self.set_text_color(*self.DARK)
        self.multi_cell(0, 4.2, val, align="L")
        self.ln(0.5)


def build_factsheet_cn():
    pdf = FactCN()
    pdf.set_auto_page_break(auto=True, margin=14)
    pdf.add_page()

    # ── Banner ──
    pdf.set_fill_color(*FactCN.CARDINAL)
    pdf.rect(0, 0, pdf.w, 28, style="F")
    pdf.set_y(6)
    pdf.set_font("ARUNI", "B", 20)
    pdf.set_text_color(*FactCN.WHITE)
    pdf.cell(0, 8, "510k Bridge", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("ARUNI", "", 10)
    pdf.cell(0, 6, "服务概览与能力介绍", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_y(32)

    # ── Who We Serve ──
    pdf.section_bar("我们的客户")
    pdf.txt(
        "寻求FDA 510(k)许可进入美国市场的中国医疗器械企业。"
        "我们专注于II类非侵入式器械：患者监护仪、影像系统、"
        "康复设备、诊断工具和医疗器械软件(SaMD)。")

    # ── The Problem ──
    pdf.section_bar("行业痛点")
    pdf.bul("NMPA与FDA流程之间的语言和法规文化差异")
    pdf.bul("跨地区团队（中国+美国）项目状态不透明")
    pdf.bul("测试实验室、美国代理人和法规顾问协调困难")
    pdf.bul("高失败率：约30%的510(k)提交收到补充信息请求")
    pdf.bul("可避免的错误（错误的等效器械、缺失测试数据、RTA）导致高昂延误")

    # ── Our Solution ──
    pdf.section_bar("我们的解决方案")
    pdf.txt(
        "双语(中英文)510(k)项目管理平台，配合经验丰富的法规专业人员。"
        "从策略制定到获批放行，我们弥合语言、流程和合规差距。")

    # ── Platform Highlights ──
    pdf.section_bar("平台亮点")
    col_w = (pdf.w - pdf.l_margin - pdf.r_margin) / 2 - 2
    x_left = pdf.l_margin
    x_right = pdf.l_margin + col_w + 4
    y0 = pdf.get_y()
    items_left = [
        "15选项卡控制塔仪表盘",
        "双语9步设置向导",
        "双轨里程碑跟踪",
        "FDA通信中心",
        "Q-Sub生成自动化",
    ]
    items_right = [
        "版本化文档控制",
        "风险与预算监控",
        "线程式团队消息(中英文)",
        "自动化RTA自检",
        "数据源引用审计追踪",
    ]
    pdf.set_font("ARUNI", "", 8.5)
    pdf.set_text_color(*FactCN.DARK)
    for i, (l, r) in enumerate(zip(items_left, items_right)):
        pdf.set_xy(x_left, y0 + i * 4.5)
        pdf.cell(col_w, 4.5, "  -  " + l)
        pdf.set_xy(x_right, y0 + i * 4.5)
        pdf.cell(col_w, 4.5, "  -  " + r)
    pdf.set_y(y0 + len(items_left) * 4.5 + 2)

    # ── By The Numbers ──
    pdf.section_bar("关键数据")
    col3_w = (pdf.w - pdf.l_margin - pdf.r_margin) / 3
    y0 = pdf.get_y()
    stats = [
        ("12-18个月", "典型审批周期"),
        ("90-120天", "平均FDA审查时间"),
        ("$15万-$40万", "端到端预算范围"),
    ]
    for i, (big, small) in enumerate(stats):
        pdf.set_xy(pdf.l_margin + col3_w * i, y0)
        pdf.set_font("ARUNI", "B", 16)
        pdf.set_text_color(*FactCN.CARDINAL)
        pdf.cell(col3_w, 8, big, align="C", new_x="LMARGIN", new_y="NEXT")
        pdf.set_xy(pdf.l_margin + col3_w * i, y0 + 8)
        pdf.set_font("ARUNI", "", 7.5)
        pdf.set_text_color(*FactCN.GRAY)
        pdf.cell(col3_w, 4, small, align="C")
    pdf.set_y(y0 + 16)

    # ── Service Tiers ──
    pdf.section_bar("服务层级")
    tiers = [
        ("SaaS 平台", "起步价$500/月",
         ["控制塔仪表盘", "双语设置向导", "双轨里程碑",
          "文档控制", "团队消息", "风险与预算跟踪"]),
        ("专业PM服务", "$10,000-$25,000/月",
         ["SaaS全部功能", "专属PMP项目经理", "FDA通信中心",
          "美国代理人服务", "门控评审管理", "提交监督",
          "供应商协调"]),
        ("企业级服务", "按项目定价",
         ["专业版全部功能", "端到端510(k)管理", "法规策略",
          "RTA自检与DHF就绪", "美国代理人服务",
          "美国实体设立", "投资者文档"]),
    ]
    col_w = (pdf.w - pdf.l_margin - pdf.r_margin - 6) / 3
    y0 = pdf.get_y()
    for idx, (name, price, features) in enumerate(tiers):
        x = pdf.l_margin + idx * (col_w + 3)
        pdf.set_xy(x, y0)
        pdf.set_fill_color(*FactCN.LIGHT_BG)
        box_h = 4.5 + 5 + len(features) * 4 + 2
        pdf.rect(x, y0, col_w, box_h, style="F")
        pdf.set_xy(x + 1, y0 + 1)
        pdf.set_font("ARUNI", "B", 8.5)
        pdf.set_text_color(*FactCN.CARDINAL)
        pdf.cell(col_w - 2, 4.5, name, align="C", new_x="LMARGIN", new_y="NEXT")
        pdf.set_xy(x + 1, y0 + 5)
        pdf.set_font("ARUNI", "B", 8)
        pdf.set_text_color(*FactCN.ACCENT)
        pdf.cell(col_w - 2, 4.5, price, align="C", new_x="LMARGIN", new_y="NEXT")
        for j, feat in enumerate(features):
            pdf.set_xy(x + 2, y0 + 10 + j * 4)
            pdf.set_font("ARUNI", "", 7.5)
            pdf.set_text_color(*FactCN.DARK)
            pdf.cell(col_w - 4, 4, "- " + feat)
    pdf.set_y(y0 + 4.5 + 5 + max(len(t[2]) for t in tiers) * 4 + 5)

    # ── Contact ──
    pdf.section_bar("立即开始")
    pdf.set_font("ARUNI", "", 9)
    pdf.set_text_color(*FactCN.DARK)
    pdf.cell(0, 5, "info@510kbridge.com  |  510kbridge.com  |  立即预约免费咨询", align="C")

    path = os.path.join(OUT, "510k_Bridge_Factsheet_CN.pdf")
    pdf.output(path)
    return path


if __name__ == "__main__":
    en = build_factsheet_en()
    print(f"EN Factsheet: {en}")
    cn = build_factsheet_cn()
    print(f"CN Factsheet: {cn}")
    print("Done.")
