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
        "and software-as-a-medical-device (SaMD). Offices in Gresham, Oregon & Shanghai, China.")

    # ── The Problem ──
    pdf.section_bar("THE PROBLEM")
    pdf.bul("Language & regulatory culture gap between NMPA and FDA processes")
    pdf.bul("No visibility into project status across distributed teams (China + US)")
    pdf.bul("Difficulty coordinating testing labs, US agents, and regulatory consultants")
    pdf.bul("High failure rates: ~30% of 510(k) submissions receive AI requests")
    pdf.bul("Costly delays from preventable errors (wrong predicate, missing test data, RTA)")
    pdf.bul("No lightweight QMS for startups -- enterprise systems are overkill")

    # ── Our Solution ──
    pdf.section_bar("OUR SOLUTION")
    pdf.txt(
        "A trilingual (EN/KO/CN) 510(k) project management platform paired with "
        "experienced regulatory professionals. From predicate device research through "
        "FDA clearance, we bridge the language, process, and compliance gap -- "
        "including QMS, entity formation, and investor relations.")

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
        "Multilingual 9-step setup wizard",
        "AI-powered Predicate Finder",
        "FDA Communications Center",
        "Q-Sub generation & RTA self-check",
        "QMS-Lite (21 CFR 820 / ISO 13485)",
        "Cross-border Entity Setup Tracker",
    ]
    items_right = [
        "Dual-track milestone tracking",
        "Document control with version history",
        "Risk & budget monitoring (USD/CNY)",
        "Thread-based team messaging (EN/CN)",
        "SE decision flowchart & DHF readiness",
        "CAPA, DMR & supplier qualification",
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
        ("Control Tower", "From $500/mo",
         ["16-tab PM dashboard", "Multilingual setup wizard", "Dual-track milestones",
          "Document control & messaging", "Risk & budget tracking", "Predicate Finder included"]),
        ("QMS-Lite", "$200-500/mo (included in Professional & Enterprise)",
         ["21 CFR 820 & ISO 13485 aligned", "Document control & CAPA",
          "Training records mgmt", "Supplier qualification",
          "Complaint handling", "Integrates with Control Tower"]),
        ("Professional PM", "$10-25K/mo",
         ["All SaaS features + QMS-Lite included", "Dedicated PMP project manager", "FDA Comms Center & Q-Sub",
          "US Agent representation", "Gate review management", "Submission oversight"]),
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

    # ── Additional Products ──
    pdf.section_bar("ADDITIONAL PRODUCTS")
    pdf.bul("Predicate Finder -- AI-powered search of openFDA database for predicate devices, SE analysis, comparison reports (included with services)")
    pdf.bul("Entity Setup Tracker -- Delaware C-Corp formation, state registration, EIN, bank account, FDA establishment registration ($1K-5K or $200/mo)")
    pdf.bul("Enterprise -- End-to-end: regulatory strategy + PM + QMS-Lite + RTA/DHF readiness + US entity formation + investor documentation (project-based pricing)")

    # ── Contact ──
    pdf.section_bar("GET STARTED")
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(*FactEN.DARK)
    pdf.cell(0, 5, _a("info@510kbridge.com  |  510kbridge.com  |  Gresham, Oregon & Shanghai, China"), align="C")
    pdf.ln(3)
    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(*FactEN.GRAY)
    pdf.cell(0, 4, _a("510kBridge, a Delaware corporation. Schedule a free 30-minute consultation today."), align="C")

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
        "多语言(中英韩文)510(k)项目管理平台，配合经验丰富的法规专业人员。"
        "从策略制定到获批放行，我们弥合语言、流程和合规差距。")

    # ── Platform Highlights ──
    pdf.section_bar("平台亮点")
    col_w = (pdf.w - pdf.l_margin - pdf.r_margin) / 2 - 2
    x_left = pdf.l_margin
    x_right = pdf.l_margin + col_w + 4
    y0 = pdf.get_y()
    items_left = [
        "16选项卡控制塔仪表盘",
        "多语言9步设置向导",
        "7大设备类别模板",
        "双轨里程碑跟踪",
        "FDA通信中心",
        "Q-Sub生成自动化",
    ]
    items_right = [
        "版本化文档控制",
        "风险与预算监控",
        "自动配置标准与风险",
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
        ("Control Tower", "起步价$500/月",
         ["16选项卡PM仪表板", "多语言设置向导", "双轨里程碑",
          "文档控制与消息", "风险与预算跟踪", "Predicate Finder包含"]),
        ("QMS-Lite", "$200-500/月 (专业版和企业版已包含)",
         ["21 CFR 820 & ISO 13485对齐", "文档控制与CAPA",
          "培训记录管理", "供应商资质",
          "投诉处理", "与Control Tower集成"]),
        ("专业PM服务", "$10,000-$25,000/月",
         ["SaaS全部功能 + QMS-Lite包含", "专属PMP项目经理", "FDA通信中心与Q-Sub",
          "美国代理人服务", "门控评审管理", "提交监督"]),
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

    # ── Additional Products ──
    pdf.section_bar("额外产品")
    pdf.bul("Predicate Finder -- AI驱动的openFDA数据库先导器械搜索、SE分析、比较报告（服务包含）")
    pdf.bul("跨境实体设立追踪器 -- 特拉华C-Corp注册、州登记、EIN、银行账户、FDA机构注册 ($1K-5K或$200/月)")
    pdf.bul("企业级 -- 端到端: 法规策略 + PM + QMS-Lite + RTA/DHF就绪 + 美国实体设立 + 投资者文档 (项目定价)")

    # ── Contact ──
    pdf.section_bar("立即开始")
    pdf.set_font("ARUNI", "", 9)
    pdf.set_text_color(*FactCN.DARK)
    pdf.cell(0, 5, "info@510kbridge.com  |  510kbridge.com  |  美国格雷舍姆(俄勒冈州) & 中国上海", align="C")
    pdf.ln(3)
    pdf.set_font("ARUNI", "", 8)
    pdf.set_text_color(*FactCN.GRAY)
    pdf.cell(0, 4, "510kBridge, 特拉华公司。立即预约免费30分钟咨询。", align="C")

    path = os.path.join(OUT, "510k_Bridge_Factsheet_CN.pdf")
    pdf.output(path)
    return path


# ═══════════════════════════════════════════
#  KOREAN FACT SHEET
# ═══════════════════════════════════════════

class FactKO(FPDF):
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


def build_factsheet_ko():
    pdf = FactKO()
    pdf.set_auto_page_break(auto=True, margin=14)
    pdf.add_page()

    # ── Banner ──
    pdf.set_fill_color(*FactKO.CARDINAL)
    pdf.rect(0, 0, pdf.w, 28, style="F")
    pdf.set_y(6)
    pdf.set_font("ARUNI", "B", 20)
    pdf.set_text_color(*FactKO.WHITE)
    pdf.cell(0, 8, "510k Bridge", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("ARUNI", "", 10)
    pdf.cell(0, 6, "\uc11c\ube44\uc2a4 \uac1c\uc694 \ubc0f \ud575\uc2ec \uc5ed\ub7c9", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_y(32)

    # ── Who We Serve ──
    pdf.section_bar("\ub300\uc0c1 \uace0\uac1d")
    pdf.txt(
        "FDA 510(k) \uc778\ud5c8\uac00\ub97c \ud1b5\ud574 \ubbf8\uad6d \uc2dc\uc7a5\uc5d0 \uc9c4\ucd9c\ud558\ub824\ub294 \ud55c\uad6d \uc758\ub8cc\uae30\uae30 \uae30\uc5c5. "
        "Class II \ube44\uce68\uc2b5\uc801 \uae30\uae30 \uc804\ubb38: \ud658\uc790 \ubaa8\ub2c8\ud130, \uc601\uc0c1 \uc2dc\uc2a4\ud15c, "
        "\uc7ac\ud65c \uc7a5\ube44, \uc9c4\ub2e8 \ub3c4\uad6c \ubc0f SaMD(\uc758\ub8cc\uae30\uae30 \uc18c\ud504\ud2b8\uc6e8\uc5b4). "
        "\ubbf8\uad6d \uadf8\ub808\uc14c(\uc624\ub808\uac74\uc8fc) \ubc0f \uc911\uad6d \uc0c1\ud558\uc774 \uc624\ud53c\uc2a4.")

    # ── The Problem ──
    pdf.section_bar("\uc5c5\uacc4 \ubb38\uc81c\uc810")
    pdf.bul("\uad6d\ub0b4 \uaddc\uc81c\uc640 FDA \ud504\ub85c\uc138\uc2a4 \uac04\uc758 \uc5b8\uc5b4 \ubc0f \uaddc\uc81c \ubb38\ud654 \ucc28\uc774")
    pdf.bul("\ubd84\uc0b0\ub41c \ud300(\ud55c\uad6d + \ubbf8\uad6d) \uac04 \ud504\ub85c\uc81d\ud2b8 \uc0c1\ud0dc \ubd88\ud22c\uba85")
    pdf.bul("\uc2dc\ud5d8 \uc5f0\uad6c\uc18c, \ubbf8\uad6d \ub300\ub9ac\uc778, \uaddc\uc81c \ucee8\uc124\ud134\ud2b8 \uc870\uc728 \uc5b4\ub824\uc6c0")
    pdf.bul("\ub192\uc740 \uc2e4\ud328\uc728: 510(k) \uc81c\ucd9c\uc758 \uc57d 30%\uac00 AI(Additional Information) \uc694\uccad \uc218\uc2e0")
    pdf.bul("\uc608\ubc29 \uac00\ub2a5\ud55c \uc624\ub958(\uc798\ubabb\ub41c \ub4f1\uac00\uae30\uae30, \ub204\ub77d\ub41c \uc2dc\ud5d8 \ub370\uc774\ud130, RTA)\ub85c \uc778\ud55c \uace0\ube44\uc6a9 \uc9c0\uc5f0")
    pdf.bul("\uc2a4\ud0c0\ud2b8\uc5c5\uc744 \uc704\ud55c \uacbd\ub7c9 QMS \ubd80\uc7ac -- \uc5d4\ud130\ud504\ub77c\uc774\uc988 \uc2dc\uc2a4\ud15c\uc740 \uacfc\ub3c4")

    # ── Our Solution ──
    pdf.section_bar("\uc6b0\ub9ac\uc758 \uc194\ub8e8\uc158")
    pdf.txt(
        "\ub2e4\uad6d\uc5b4(EN/KO/CN) 510(k) \ud504\ub85c\uc81d\ud2b8 \uad00\ub9ac \ud50c\ub7ab\ud3fc\uacfc "
        "\uacbd\ud5d8 \ud48d\ubd80\ud55c \uaddc\uc81c \uc804\ubb38\uac00 \ud300. "
        "\ub4f1\uac00\uae30\uae30 \uc870\uc0ac\ubd80\ud130 FDA \uc778\ud5c8\uae30\uae30\uac00\uc9c0, \uc5b8\uc5b4, \ud504\ub85c\uc138\uc2a4, "
        "\ucef4\ud50c\ub77c\uc774\uc5b8\uc2a4 \uaca9\ucc28\ub97c \ud574\uc18c\ud569\ub2c8\ub2e4 -- "
        "QMS, \ubc95\uc778 \uc124\ub9bd, \ud22c\uc790\uc790 \uad00\uacc4 \ud3ec\ud568.")

    # ── Platform Highlights ──
    pdf.section_bar("\ud50c\ub7ab\ud3fc \ud558\uc774\ub77c\uc774\ud2b8")
    col_w = (pdf.w - pdf.l_margin - pdf.r_margin) / 2 - 2
    x_left = pdf.l_margin
    x_right = pdf.l_margin + col_w + 4
    y0 = pdf.get_y()
    items_left = [
        "16\ud0ed Control Tower \ub300\uc2dc\ubcf4\ub4dc",
        "\ub2e4\uad6d\uc5b4 9\ub2e8\uacc4 \uc124\uc815 \ub9c8\ubc95\uc0ac",
        "AI \uae30\ubc18 \ub4f1\uac00\uae30\uae30 \uac80\uc0c9\uae30",
        "FDA \ucee4\ubba4\ub2c8\ucf00\uc774\uc158 \uc13c\ud130",
        "Q-Sub \uc0dd\uc131 \ubc0f RTA \uc790\uac00\uc810\uac80",
        "QMS-Lite (21 CFR 820 / ISO 13485)",
        "\uad6d\uacbd\uac04 \ubc95\uc778 \uc124\ub9bd \ud2b8\ub798\ucee4",
    ]
    items_right = [
        "\ub4c0\uc5bc\ud2b8\ub799 \ub9c8\uc77c\uc2a4\ud1a4 \ucd94\uc801",
        "\ubc84\uc804 \uad00\ub9ac \ubb38\uc11c \ud1b5\uc81c",
        "\ub9ac\uc2a4\ud06c \ubc0f \uc608\uc0b0 \ubaa8\ub2c8\ud130\ub9c1 (USD/KRW)",
        "\uc2a4\ub808\ub4dc \uae30\ubc18 \ud300 \uba54\uc2dc\uc9d5 (EN/KO/CN)",
        "SE \uc758\uc0ac\uacb0\uc815 \ubc0f DHF \uc900\ube44 \uc0c1\ud0dc",
        "CAPA, DMR \ubc0f \uacf5\uae09\uc5c5\uccb4 \uc790\uaca9 \uad00\ub9ac",
        "\uac10\uc0ac \ucd94\uc801\uc131 \ub370\uc774\ud130 \uc18c\uc2a4 \ucc38\uc870",
    ]
    pdf.set_font("ARUNI", "", 8.5)
    pdf.set_text_color(*FactKO.DARK)
    for i, (l, r) in enumerate(zip(items_left, items_right)):
        pdf.set_xy(x_left, y0 + i * 4.5)
        pdf.cell(col_w, 4.5, "  -  " + l)
        pdf.set_xy(x_right, y0 + i * 4.5)
        pdf.cell(col_w, 4.5, "  -  " + r)
    pdf.set_y(y0 + len(items_left) * 4.5 + 2)

    # ── By The Numbers ──
    pdf.section_bar("\ud575\uc2ec \uc218\uce58")
    col3_w = (pdf.w - pdf.l_margin - pdf.r_margin) / 3
    y0 = pdf.get_y()
    stats = [
        ("12-18\uac1c\uc6d4", "\uc77c\ubc18\uc801 \uc778\ud5c8\uae30\uae30 \ud0c0\uc784\ub77c\uc778"),
        ("90-120\uc77c", "\ud3c9\uade0 FDA \uc2ec\uc0ac \uae30\uac04"),
        ("$150K-$400K", "\uc5d4\ub4dc\ud22c\uc5d4\ub4dc \uc608\uc0b0 \ubc94\uc704"),
    ]
    for i, (big, small) in enumerate(stats):
        pdf.set_xy(pdf.l_margin + col3_w * i, y0)
        pdf.set_font("ARUNI", "B", 16)
        pdf.set_text_color(*FactKO.CARDINAL)
        pdf.cell(col3_w, 8, big, align="C", new_x="LMARGIN", new_y="NEXT")
        pdf.set_xy(pdf.l_margin + col3_w * i, y0 + 8)
        pdf.set_font("ARUNI", "", 7.5)
        pdf.set_text_color(*FactKO.GRAY)
        pdf.cell(col3_w, 4, small, align="C")
    pdf.set_y(y0 + 16)

    # ── Service Tiers ──
    pdf.section_bar("\uc11c\ube44\uc2a4 \ud2f0\uc5b4")
    tiers = [
        ("Control Tower", "\uc6d4 $500\ubd80\ud130",
         ["16\ud0ed PM \ub300\uc2dc\ubcf4\ub4dc", "\ub2e4\uad6d\uc5b4 \uc124\uc815 \ub9c8\ubc95\uc0ac", "\ub4c0\uc5bc\ud2b8\ub799 \ub9c8\uc77c\uc2a4\ud1a4",
          "\ubb38\uc11c \ud1b5\uc81c \ubc0f \uba54\uc2dc\uc9d5", "\ub9ac\uc2a4\ud06c \ubc0f \uc608\uc0b0 \ucd94\uc801", "\ub4f1\uac00\uae30\uae30 \uac80\uc0c9\uae30 \ud3ec\ud568"]),
        ("QMS-Lite", "\uc6d4 $200-500 (\uc804\ubb38\uac00/\uc5d4\ud130\ud504\ub77c\uc774\uc988 \ud3ec\ud568)",
         ["21 CFR 820 & ISO 13485 \uc815\ub82c", "\ubb38\uc11c \ud1b5\uc81c \ubc0f CAPA",
          "\uad50\uc721 \uae30\ub85d \uad00\ub9ac", "\uacf5\uae09\uc5c5\uccb4 \uc790\uaca9",
          "\ubd88\ub9cc \ucc98\ub9ac", "Control Tower \ud1b5\ud569"]),
        ("\uc804\ubb38 PM \uc11c\ube44\uc2a4", "\uc6d4 $10,000-$25,000",
         ["SaaS \uc804\uccb4 + QMS-Lite \ud3ec\ud568", "\uc804\ub2f4 PMP \ud504\ub85c\uc81d\ud2b8 \ub9e4\ub2c8\uc800", "FDA \ucee4\ubba4\ub2c8\ucf00\uc774\uc158 & Q-Sub",
          "\ubbf8\uad6d \ub300\ub9ac\uc778 \uc11c\ube44\uc2a4", "\uac8c\uc774\ud2b8 \ub9ac\ubdf0 \uad00\ub9ac", "\uc81c\ucd9c \uac10\ub3c5"]),
    ]
    col_w = (pdf.w - pdf.l_margin - pdf.r_margin - 6) / 3
    y0 = pdf.get_y()
    for idx, (name, price, features) in enumerate(tiers):
        x = pdf.l_margin + idx * (col_w + 3)
        pdf.set_xy(x, y0)
        pdf.set_fill_color(*FactKO.LIGHT_BG)
        box_h = 4.5 + 5 + len(features) * 4 + 2
        pdf.rect(x, y0, col_w, box_h, style="F")
        pdf.set_xy(x + 1, y0 + 1)
        pdf.set_font("ARUNI", "B", 8.5)
        pdf.set_text_color(*FactKO.CARDINAL)
        pdf.cell(col_w - 2, 4.5, name, align="C", new_x="LMARGIN", new_y="NEXT")
        pdf.set_xy(x + 1, y0 + 5)
        pdf.set_font("ARUNI", "B", 8)
        pdf.set_text_color(*FactKO.ACCENT)
        pdf.cell(col_w - 2, 4.5, price, align="C", new_x="LMARGIN", new_y="NEXT")
        for j, feat in enumerate(features):
            pdf.set_xy(x + 2, y0 + 10 + j * 4)
            pdf.set_font("ARUNI", "", 7.5)
            pdf.set_text_color(*FactKO.DARK)
            pdf.cell(col_w - 4, 4, "- " + feat)
    pdf.set_y(y0 + 4.5 + 5 + max(len(t[2]) for t in tiers) * 4 + 5)

    # ── Additional Products ──
    pdf.section_bar("\ucd94\uac00 \uc81c\ud488")
    pdf.bul("\ub4f1\uac00\uae30\uae30 \uac80\uc0c9\uae30 -- AI \uae30\ubc18 openFDA \ub370\uc774\ud130\ubca0\uc774\uc2a4 \uac80\uc0c9, SE \ubd84\uc11d, \ube44\uad50 \ubcf4\uace0\uc11c (\uc11c\ube44\uc2a4 \ud3ec\ud568)")
    pdf.bul("\uad6d\uacbd\uac04 \ubc95\uc778 \uc124\ub9bd \ud2b8\ub798\ucee4 -- Delaware C-Corp \uc124\ub9bd, \uc8fc \ub4f1\ub85d, EIN, \uc740\ud589 \uacc4\uc88c, FDA \uc2dc\uc124 \ub4f1\ub85d ($1K-5K \ub610\ub294 \uc6d4 $200)")
    pdf.bul("\uc5d4\ud130\ud504\ub77c\uc774\uc988 -- \uc5d4\ub4dc\ud22c\uc5d4\ub4dc: \uaddc\uc81c \uc804\ub7b5 + PM + QMS-Lite + RTA/DHF \uc900\ube44 + \ubbf8\uad6d \ubc95\uc778 \uc124\ub9bd + \ud22c\uc790\uc790 \ubb38\uc11c (\ud504\ub85c\uc81d\ud2b8 \uae30\ubc18 \uac00\uaca9)")

    # ── Contact ──
    pdf.section_bar("\uc2dc\uc791\ud558\uae30")
    pdf.set_font("ARUNI", "", 9)
    pdf.set_text_color(*FactKO.DARK)
    pdf.cell(0, 5, "info@510kbridge.com  |  510kbridge.com  |  \ubbf8\uad6d \uadf8\ub808\uc14c(OR) & \uc911\uad6d \uc0c1\ud558\uc774", align="C")
    pdf.ln(3)
    pdf.set_font("ARUNI", "", 8)
    pdf.set_text_color(*FactKO.GRAY)
    pdf.cell(0, 4, "510kBridge, Delaware \ubc95\uc778. \uc624\ub298 \ubb34\ub8cc 30\ubd84 \uc0c1\ub2f4\uc744 \uc608\uc57d\ud558\uc138\uc694.", align="C")

    path = os.path.join(OUT, "510k_Bridge_Factsheet_KO.pdf")
    pdf.output(path)
    return path


if __name__ == "__main__":
    en = build_factsheet_en()
    print(f"EN Factsheet: {en}")
    cn = build_factsheet_cn()
    print(f"CN Factsheet: {cn}")
    ko = build_factsheet_ko()
    print(f"KO Factsheet: {ko}")
    print("Done.")
