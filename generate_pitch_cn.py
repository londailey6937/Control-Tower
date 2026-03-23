#!/usr/bin/env python3
"""
Generate the Chinese-language PMP Engagement Pitch PDF.
Mirror of generate_pitch.py with all content translated to Chinese.
Uses Arial Unicode MS for CJK support.
"""

import os
from fpdf import FPDF

OUT = os.path.dirname(os.path.abspath(__file__))
CJK_FONT = "/Library/Fonts/Arial Unicode.ttf"

_MAP = str.maketrans({
    "\u2014": "--", "\u2013": "-", "\u2019": "'", "\u201c": '"', "\u201d": '"',
    "\u2018": "'", "\u2265": ">=", "\u2264": "<=", "\u00b5": "u", "\u00d7": "x",
    "\u2022": "-", "\u2026": "...", "\u00ae": "(R)",
})
def _a(s):
    return s.translate(_MAP)


class PitchPDF(FPDF):
    CARDINAL = (140, 21, 21)
    DARK = (35, 35, 40)
    GRAY = (110, 110, 120)
    SANDSTONE = (210, 194, 149)
    ACCENT = (0, 98, 71)
    WHITE = (255, 255, 255)

    def __init__(self):
        super().__init__()
        self.add_font("CJK", "", CJK_FONT)
        self.add_font("CJK", "B", CJK_FONT)
        self.add_font("CJK", "I", CJK_FONT)

    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("CJK", "I", 7)
        self.set_text_color(*self.GRAY)
        self.cell(0, 4, "机密 -- Lon Dailey  |  斯坦福SCPM  |  PMP聘用提案", align="R")
        self.ln(5)

    def footer(self):
        self.set_y(-12)
        self.set_font("CJK", "I", 7)
        self.set_text_color(*self.GRAY)
        self.cell(0, 4, f"第 {self.page_no()}/{{nb}} 页", align="C")

    def section(self, num, title, page_break=True):
        page_body_bottom = self.h - self.b_margin
        if page_break and self.get_y() > (page_body_bottom - 25):
            self.add_page()
        self.set_font("CJK", "B", 12)
        self.set_text_color(*self.CARDINAL)
        self.cell(0, 7, f"{num}.  {title}" if num else title, new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(*self.CARDINAL)
        self.set_line_width(0.4)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(3)

    def body(self, text):
        self.set_font("CJK", "", 10)
        self.set_text_color(*self.DARK)
        self.multi_cell(0, 5.2, text, align="L")
        self.ln(2)

    def bullet(self, text, bold_prefix="", dash=True):
        self.set_font("CJK", "", 10)
        self.set_text_color(*self.DARK)
        if dash:
            self.cell(6, 5.2, "-")
        if bold_prefix:
            self.set_font("CJK", "B", 10)
            self.cell(self.get_string_width(bold_prefix) + 1, 5.2, bold_prefix)
            self.set_font("CJK", "", 10)
        self.multi_cell(0, 5.2, text, align="L")
        self.ln(0.5)

    def bullet_aligned(self, label, text, dash=True):
        """Bold label + body text, optionally with dash prefix."""
        indent = 6
        label_w = 50  # wider for Chinese characters
        self.set_font("CJK", "", 10)
        self.set_text_color(*self.DARK)
        if dash:
            self.cell(indent, 5.2, "-")
            self.set_font("CJK", "B", 10)
            self.cell(label_w, 5.2, label)
            body_w = self.w - self.l_margin - self.r_margin - indent - label_w
            self.set_font("CJK", "", 10)
            self.multi_cell(body_w, 5.2, text, align="L")
        else:
            self.set_font("CJK", "B", 10)
            self.cell(0, 5.5, label, new_x="LMARGIN", new_y="NEXT")
            self.set_font("CJK", "", 10)
            body_indent = 8
            self.set_x(self.l_margin + body_indent)
            body_w = self.w - self.l_margin - self.r_margin - body_indent
            self.multi_cell(body_w, 5.2, text, align="L")
        self.ln(0.8)

    def quote_box(self, text):
        self.set_fill_color(255, 245, 245)
        self.set_draw_color(*self.CARDINAL)
        self.set_line_width(0.5)
        x = self.l_margin + 3
        y = self.get_y()
        self.set_xy(x + 2, y + 2)
        self.set_font("CJK", "I", 10)
        self.set_text_color(*self.CARDINAL)
        self.multi_cell(self.w - self.l_margin - self.r_margin - 10, 5.2, text, align="L")
        h = self.get_y() - y + 2
        self.rect(x, y, self.w - self.l_margin - self.r_margin - 6, h, style="D")
        self.ln(4)


def build():
    pdf = PitchPDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.add_page()

    # ── Cover banner ──
    pdf.set_fill_color(*PitchPDF.CARDINAL)
    pdf.rect(0, 0, 210, 52, style="F")
    pdf.set_font("CJK", "B", 22)
    pdf.set_text_color(*PitchPDF.WHITE)
    pdf.set_y(10)
    pdf.cell(0, 10, "项目管理聘用提案", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("CJK", "", 12)
    pdf.cell(0, 7, "ICU呼吸数字孪生系统", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("CJK", "I", 10)
    pdf.cell(0, 6, "sEMG神经驱动 + EIT通气/灌注监测平台", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(1)
    pdf.set_draw_color(*PitchPDF.WHITE)
    pdf.set_line_width(0.3)
    pdf.line(40, pdf.get_y(), 170, pdf.get_y())
    pdf.ln(2)
    pdf.set_font("CJK", "B", 10)
    pdf.cell(0, 5, "编制人：Lon Dailey  |  斯坦福项目管理证书 (SCPM)",
             align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("CJK", "", 9)
    pdf.cell(0, 5, "呈送：ICU数字孪生项目利益相关者", align="C", new_x="LMARGIN", new_y="NEXT")

    pdf.ln(8)
    pdf.set_text_color(*PitchPDF.DARK)

    # ── 1. 执行摘要 ──
    pdf.section("1", "执行摘要", page_break=False)
    pdf.body(
        "根据您的PPT演示内容，该项目显然需要专职项目管理来引导从概念到完成的全过程执行。"
        "我已开始使用所提供的信息对项目进行建模，同时也认识到部分假设可能需要根据当前数据进行调整。"
        "我的目标是将这些输入与我开发的控制塔平台及其配套文档进行同步，以建立统一且可操作的项目框架。\n\n"
        "我提议担任ICU呼吸数字孪生系统的项目管理专业人员(PMP)——该系统是一个双轨、23个月的FDA 510(k)项目，"
        "涵盖sEMG神经驱动监测（模块A）和EIT通气与灌注成像（模块B）。\n\n"
        "我的斯坦福项目管理证书(SCPM)提供了一种严谨、基于研究的方法论，"
        "非常适合复杂的受监管医疗器械项目。这包括结构化进度管理、主动风险管理，"
        "以及工程、法规和商务职能之间的紧密协调，以确保按时合规执行。"
    )

    pdf.quote_box(
        "\"斯坦福SCPM课程专为技术密集型项目而设计，"
        "这类项目中范围不确定性、法规约束和多学科团队交汇——"
        "恰恰是我们数字孪生项目所面临的环境。\""
    )

    # ── 2. 为什么本项目需要专职PMP ──
    pdf.section("2", "为什么本项目需要专职PMP")
    pdf.body("数字孪生项目并非常规产品开发，它呈现出五种叠加的复杂性：")
    pdf.bullet(
        "技术轨道和法规轨道共17个相互依赖的里程碑，22个月关键路径，仅5项活动有浮动时间。",
        "双轨并行：  ", dash=False)
    pdf.bullet(
        "两次独立的510(k)申报（sEMG产品代码IKN，EIT产品代码DQS），"
        "各自需要严格的DHF、V&V、风险管理和FDA预申报沟通。",
        "连续FDA申报：  ", dash=False)
    pdf.bullet(
        "Arch Medical Management, LLC（PMP聘用实体，俄勒冈州）+ 思澜科技（成都）（研发/制造）"
        "——跨境协调、ISO 13485审核和CFIUS合规结构。",
        "双实体、跨境：  ", dash=False)
    pdf.bullet(
        "12项IEC/ISO标准、21 CFR 820 QSR合规、生物相容性测试、EMC测试——"
        "各项之间的依赖关系影响关键路径。",
        "法规负担：  ", dash=False)
    pdf.bullet(
        "这可能意味着，例如，现金储备$320K、月支出$45K、跑道7个月——"
        "每一次进度延误都直接侵蚀财务可行性。",
        "预算受限：  ", dash=False)

    pdf.body(
        "如果没有专职PMP运用CPM分析、挣值跟踪和主动风险管理，"
        "进度超期和预算耗尽的概率将急剧上升。"
    )

    # ── 3. 斯坦福SCPM资质 ──
    pdf.section("3", "斯坦福SCPM——为本项目带来什么")
    pdf.body(
        "斯坦福项目管理证书是一项研究生级别的专业资质，"
        "涵盖复杂技术项目的全生命周期。以下是每项核心能力与我们数字孪生项目的直接对应关系："
    )

    items = [
        ("关键路径法(CPM)与进度管理",
         "我已构建了包含正推/逆推分析的项目网络图。17项活动中有12项位于关键路径（TF=0）。"
         "我已识别出R9（ISO 13485审核）有6个月的浮动时间，R3/R4（sEMG 510(k)提交/批准）各有2个月，"
         "T2/R1各有1个月。该分析指导了哪些环节可以承受延误，哪些不能。"),
        ("风险管理与量化",
         "斯坦福的框架超越了定性风险登记。我运用期望货币值(EMV)分析、"
         "蒙特卡洛进度模拟和风险调整后的里程碑置信度——"
         "这对FDA时间线至关重要，因为一次AI（补充信息）请求就可能增加90天。"),
        ("挣值管理(EVM)",
         "拥有$320K预算和7个月跑道的情况下，我们无法承受事后才发现成本超支。"
         "我将从M+0开始实施CPI/SPI跟踪，以便对任何预算或进度偏差实现预警。"),
        ("利益相关者与沟通管理",
         "该项目涉及戴博士（技术总负责人）、Lawrence Liu、Lon Dailey——以及外部利益相关者"
         "（FDA、认证机构、投资者）。斯坦福的利益相关者管理模型确保每方在正确的节奏获得正确的信息。"),
        ("设计控制与法规整合",
         "斯坦福课程涵盖项目管理与设计控制流程（ISO 13485, 21 CFR 820）的整合。"
         "我理解DHF文档、设计评审和V&V关口如何必须作为硬依赖嵌入项目进度中——而非事后补充。"),
        ("变更控制与配置管理",
         "我们的仪表板已经实现了正式的变更请求工作流，包含审批链和审计追踪。"
         "我将确保每项范围变更在批准前都经过进度/成本/风险影响评估。"),
        ("沟通——项目经理最重要的技能",
         "沟通被广泛认为是项目经理最重要的核心能力。"
         "我在此方面具备独特优势：我的学位专业是技术传播（如简历所示）。"
         "这意味着我经过正规训练，能够将复杂的技术概念转化为针对不同受众的清晰、可操作的信息——"
         "无论受众是FDA、中国制造合作伙伴、投资者董事会，还是工程团队。"
         "每份状态报告、风险简报和利益相关者更新都受益于这一基础。"),
    ]
    for i, (title, desc) in enumerate(items):
        # Force page break before first item
        if i == 0:
            pdf.add_page()
        pdf.set_font("CJK", "B", 10)
        pdf.set_text_color(*PitchPDF.ACCENT)
        pdf.cell(0, 5.5, title, new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("CJK", "", 9.5)
        pdf.set_text_color(*PitchPDF.DARK)
        pdf.multi_cell(0, 5, desc, align="L")
        pdf.ln(2)

    # ── 4. 已交付成果 ──
    pdf.section("4", "已交付成果（能力证明）")
    pdf.body("在提出聘用请求之前，我已构建了相关工具和分析以证明能力：")
    pdf.bullet_aligned("PM仪表板：",
        "基于TypeScript + Vite + Tailwind CSS的全交互式仪表板，包含11个标签页："
        "概览、里程碑、关口、风险、标准、现金/跑道、预算、资源、供应商、CAPA、执行摘要。", dash=False)
    pdf.bullet_aligned("CPM网络分析：",
        "对全部17项活动进行正推/逆推分析。识别12项关键路径活动。"
        "量化5项浮动活动（R9: 6个月, R3: 2个月, R4: 2个月, T2: 1个月, R1: 1个月）。", dash=False)
    pdf.bullet_aligned("变更请求系统：",
        "基于IndexedDB存储的变更请求提交、审批工作流和完整审计追踪。", dash=False)
    pdf.bullet_aligned("基于角色的访问控制：",
        "基于角色的访问（PMP/技术/商务/会计），配备相应的可见性控制。", dash=False)
    pdf.bullet_aligned("现金与跑道跟踪：",
        "PMP可编辑的现金储备和月支出字段，自动重算跑道。", dash=False)
    pdf.bullet_aligned("法规合规工具：",
        "设计历史文件索引、CAPA日志、行动项目、供应商管理、通知系统。", dash=False)
    pdf.bullet_aligned("文档：",
        "中英文用户指南（各25节）、项目章程（中/英文）、发明人问答表。", dash=False)
    pdf.bullet_aligned("风险登记表：",
        "八项已定义风险，含概率/影响评分、缓解策略和触发条件。", dash=False)

    # ── 5. 拟议聘用结构 ──
    pdf.section("5", "拟议聘用结构")
    pdf.body("我为数字孪生项目提出以下PMP聘用方案：")

    # Table
    pdf.set_font("CJK", "B", 9)
    pdf.set_fill_color(255, 245, 245)
    pdf.set_text_color(*PitchPDF.CARDINAL)
    col_w = [38, 142]
    headers = ["要素", "详情"]
    for i, h in enumerate(headers):
        pdf.cell(col_w[i], 7, h, border=1, fill=True, align="C")
    pdf.ln()

    rows = [
        ("角色", "项目管理专业人员(PMP)——全面负责进度、成本、风险和质量管理"),
        ("范围", "双轨项目：sEMG（M+0至M+9批准）+ EIT（M+8至M+23批准）"),
        ("报告", "月度EVM仪表板、每周向利益相关者汇报、季度投资者摘要"),
        ("权限", "进度基线变更、变更请求批准/否决、资源分配调整"),
        ("交付物", "CPM更新、EVM报告、风险登记审查、关口就绪评估、DHF监管"),
        ("工具", "PM仪表板（在线）、网络图、风险蒙特卡洛、预算追踪器"),
        ("关系", "技术负责人保留完全技术权限；PMP管理进度、成本和流程"),
        ("实体", "Arch Medical Management, LLC"),
    ]
    pdf.set_font("CJK", "", 9)
    pdf.set_text_color(*PitchPDF.DARK)
    for lbl, val in rows:
        pdf.set_font("CJK", "B", 9)
        pdf.cell(col_w[0], 6.5, lbl, border=1)
        pdf.set_font("CJK", "", 9)
        pdf.cell(col_w[1], 6.5, val, border=1)
        pdf.ln()

    pdf.ln(4)

    # ── 6. 价值主张 ──
    pdf.section("6", "价值主张——为什么是我，为什么是现在")
    pdf.body(
        "您的专业领域在于科学——生物阻抗断层成像、sEMG信号处理以及使本设备具有变革性的临床算法。"
        "我的角色是确保这些专业技术按时、在预算内惠及患者。\n\n"
        "以下是我能带来的具体价值："
    )
    pdf.bullet_aligned("保护您的技术专注：",
        "您花在管理时间线、追踪审批或核对预算上的每一个小时，"
        "都是未花在科学研究上的时间。我来承担这些工作。", dash=False)
    pdf.bullet_aligned("降低时间线风险：",
        "仅有7个月跑道的情况下，2个月的进度延误可能是致命的。"
        "基于CPM的管理和每日关键路径监控能够防止这种情况。", dash=False)
    pdf.bullet_aligned("提升投资者信心：",
        "投资者和战略合作伙伴期望专业的项目治理。"
        "拥有斯坦福资质的PMP、在线仪表板和正式的EVM报告体现了项目成熟度。", dash=False)
    pdf.bullet_aligned("FDA就绪：",
        "FDA沟通（预申报、510(k)提交）从结构化项目管理中获益良多。"
        "我确保申报完整、准时、组织有序。", dash=False)
    pdf.bullet_aligned("已证明的交付能力：",
        "我已经构建了仪表板、网络分析、风险登记和文档。"
        "我不是提议从头开始——而是提议继续并正式化。", dash=False)

    pdf.ln(4)

    # ── 7. 下一步建议 ──
    pdf.section("7", "建议的下一步行动")
    pdf.body("如果您同意本聘用方案，我建议采取以下即时行动：")
    pdf.bullet("就PMP角色、权限边界和报告节奏达成正式协议。", "第1周：  ", dash=False)
    pdf.bullet("进度基线审查——共同走查CPM网络图，确认所有工期和依赖关系。", "第1周：  ", dash=False)
    pdf.bullet("EVM基线——使用当前预算分配建立绩效测量基线(PMB)。", "第2周：  ", dash=False)
    pdf.bullet("风险审查——对全部8项风险进行实时走查，更新概率，并确定缓解负责人。", "第2周：  ", dash=False)
    pdf.bullet("向全体利益相关者发出首份月度状态报告。", "第4周：  ", dash=False)

    pdf.ln(6)

    # ── Closing ──
    pdf.set_font("CJK", "", 10)
    pdf.set_text_color(*PitchPDF.DARK)
    pdf.multi_cell(0, 5.5,
        "我有信心，专职PMP职能将实质性地提高两个模块按时获得FDA批准的概率，"
        "并实现对有限资金的负责任管理。期待与您讨论本提案。",
        align="L"
    )
    pdf.ln(8)
    pdf.set_font("CJK", "B", 11)
    pdf.cell(0, 6, "Lon Dailey", new_x="LMARGIN", new_y="NEXT")

    path = os.path.join(OUT, "PMP_Engagement_Pitch_CN.pdf")
    pdf.output(path)
    return path


if __name__ == "__main__":
    p = build()
    print(f"PDF: {p}")
    print("Done.")
