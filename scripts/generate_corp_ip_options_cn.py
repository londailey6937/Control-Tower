#!/usr/bin/env python3
"""
Generate Corporate Structure & IP Ownership Options PDF -- Chinese Version.
公司架构与知识产权所有权选项方案 -- 中文版
"""

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
WHITE = (255, 255, 255)


class OptionsReportCN(FPDF):
    def __init__(self):
        super().__init__()
        font_path = "/Library/Fonts/Arial Unicode.ttf"
        self.add_font("ARUNI", "", font_path, uni=True)
        self.add_font("ARUNI", "B", font_path, uni=True)
        self.add_font("ARUNI", "I", font_path, uni=True)

    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("ARUNI", "B", 8)
        self.set_text_color(*GRAY)
        self.cell(0, 5, "公司架构与知识产权所有权  |  Company B USA", align="R")
        self.ln(8)

    def footer(self):
        self.set_y(-15)
        self.set_font("ARUNI", "I", 8)
        self.set_text_color(*GRAY)
        self.cell(0, 10, f"第 {self.page_no()} 页 / 共 {{nb}} 页", align="C")

    # ── helpers ──
    def sec(self, num, title):
        self.set_font("ARUNI", "B", 15)
        self.set_text_color(*BLUE)
        self.cell(0, 10, f"{num}. {title}", new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(*BLUE)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(4)

    def sub(self, title, color=BLUE):
        self.set_font("ARUNI", "B", 11)
        self.set_text_color(*color)
        self.cell(0, 7, title, new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def txt(self, text):
        self.set_font("ARUNI", "", 10)
        self.set_text_color(*TEXT)
        self.multi_cell(0, 5.5, text, new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def bullet(self, text, indent=6):
        self.set_font("ARUNI", "", 10)
        self.set_text_color(*TEXT)
        self.set_x(self.l_margin + indent)
        self.multi_cell(self.w - self.l_margin - self.r_margin - indent, 5.5,
                        f"- {text}", new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def option_header(self, label, title, color):
        self.set_draw_color(*color)
        self.set_fill_color(*color)
        y = self.get_y()
        w = self.w - self.l_margin - self.r_margin
        self.rect(self.l_margin, y, w, 8, style="DF")
        self.set_xy(self.l_margin + 3, y + 1)
        self.set_font("ARUNI", "B", 11)
        self.set_text_color(*WHITE)
        self.cell(0, 6, f"{label}: {title}")
        self.set_y(y + 10)

    def pros_cons(self, pros, cons):
        x_mid = self.l_margin + (self.w - self.l_margin - self.r_margin) / 2
        y_start = self.get_y()

        self.set_xy(self.l_margin, y_start)
        self.set_font("ARUNI", "B", 9)
        self.set_text_color(*GREEN)
        self.cell(80, 5.5, "优势")
        self.set_xy(x_mid, y_start)
        self.set_text_color(*RED)
        self.cell(80, 5.5, "劣势")
        self.ln(6)

        self.set_font("ARUNI", "", 9)
        max_lines = max(len(pros), len(cons))
        for i in range(max_lines):
            y = self.get_y()
            if y > self.h - 25:
                self.add_page()
                y = self.get_y()
            if i < len(pros):
                self.set_xy(self.l_margin + 2, y)
                self.set_text_color(*TEXT)
                self.multi_cell(
                    x_mid - self.l_margin - 4, 4.5,
                    f"+ {pros[i]}", new_x="LMARGIN", new_y="NEXT")
            y_after_left = self.get_y()
            if i < len(cons):
                self.set_xy(x_mid + 2, y)
                self.set_text_color(*TEXT)
                self.multi_cell(
                    self.w - self.r_margin - x_mid - 4, 4.5,
                    f"- {cons[i]}", new_x="LMARGIN", new_y="NEXT")
            y_after_right = self.get_y()
            self.set_y(max(y_after_left, y_after_right) + 1)
        self.ln(2)

    def info_box(self, title, items, color=BLUE):
        self.set_draw_color(*color)
        bg = (240, 243, 255) if color == BLUE else (255, 240, 240) if color == RED else (240, 255, 240)
        self.set_fill_color(*bg)
        y = self.get_y()
        line_h = 5.5
        box_h = 10 + len(items) * line_h + 4
        if y + box_h > self.h - 20:
            self.add_page()
            y = self.get_y()
        self.rect(self.l_margin, y, self.w - self.l_margin - self.r_margin, box_h, style="DF")
        self.set_xy(self.l_margin + 4, y + 3)
        self.set_font("ARUNI", "B", 10)
        self.set_text_color(*color)
        self.cell(0, 5.5, title)
        self.set_xy(self.l_margin + 6, y + 10)
        self.set_font("ARUNI", "", 9)
        self.set_text_color(*TEXT)
        for item in items:
            self.set_x(self.l_margin + 6)
            self.cell(0, line_h, item, new_x="LMARGIN", new_y="NEXT")
        self.set_y(y + box_h + 4)

    def diagram(self, lines):
        self.set_font("ARUNI", "", 8)
        self.set_text_color(*TEXT)
        for line in lines:
            if self.get_y() > self.h - 20:
                self.add_page()
            self.cell(0, 4.2, line, new_x="LMARGIN", new_y="NEXT")
        self.ln(4)

    def table(self, headers, rows, col_w):
        self.set_font("ARUNI", "B", 9)
        self.set_text_color(*WHITE)
        self.set_fill_color(*BLUE)
        for i, h in enumerate(headers):
            self.cell(col_w[i], 7, h, border=1, fill=True, align="C")
        self.ln()
        self.set_font("ARUNI", "", 9)
        self.set_text_color(*TEXT)
        for ri, row in enumerate(rows):
            is_last = ri == len(rows) - 1
            if is_last:
                self.set_font("ARUNI", "B", 9)
                self.set_fill_color(230, 235, 250)
            else:
                self.set_font("ARUNI", "", 9)
                self.set_fill_color(250, 250, 255) if ri % 2 == 0 else self.set_fill_color(255, 255, 255)
            for ci, val in enumerate(row):
                align = "C" if ci > 0 else "L"
                self.cell(col_w[ci], 6, val, border=1, fill=True, align=align)
            self.ln()
        self.ln(3)

    def recommendation_badge(self, text):
        self.set_fill_color(*GREEN)
        y = self.get_y()
        self.rect(self.l_margin, y, 110, 7, style="DF")
        self.set_xy(self.l_margin + 2, y + 1)
        self.set_font("ARUNI", "B", 9)
        self.set_text_color(*WHITE)
        self.cell(106, 5, text)
        self.set_y(y + 9)

    def not_recommended_badge(self, text):
        self.set_fill_color(*RED)
        y = self.get_y()
        self.rect(self.l_margin, y, 110, 7, style="DF")
        self.set_xy(self.l_margin + 2, y + 1)
        self.set_font("ARUNI", "B", 9)
        self.set_text_color(*WHITE)
        self.cell(106, 5, text)
        self.set_y(y + 9)

    def conditional_badge(self, text):
        self.set_fill_color(*ORANGE)
        y = self.get_y()
        self.rect(self.l_margin, y, 110, 7, style="DF")
        self.set_xy(self.l_margin + 2, y + 1)
        self.set_font("ARUNI", "B", 9)
        self.set_text_color(*WHITE)
        self.cell(106, 5, text)
        self.set_y(y + 9)


# ═══════════════════════════════════════════════════════════════
#  BUILD
# ═══════════════════════════════════════════════════════════════
def build():
    pdf = OptionsReportCN()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)

    # ── 封面 ──
    pdf.add_page()
    pdf.ln(30)
    pdf.set_font("ARUNI", "B", 28)
    pdf.set_text_color(*BLUE)
    pdf.cell(0, 14, "公司架构与", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 14, "知识产权所有权方案", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(6)
    pdf.set_font("ARUNI", "", 14)
    pdf.set_text_color(*TEXT)
    pdf.cell(0, 8, "ICU呼吸数字孪生系统", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)
    pdf.set_font("ARUNI", "", 12)
    pdf.set_text_color(*GRAY)
    pdf.cell(0, 7, "Company B USA -- 特拉华州C型公司组建", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 7, "2026年3月23日", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(12)

    pdf.set_font("ARUNI", "I", 10)
    pdf.set_text_color(*GRAY)
    pdf.multi_cell(0, 5.5,
        "本文件介绍特拉华州C型公司组建及知识产权所有权策略的结构性方案。"
        "每个方案包含说明、优劣势分析、结构图和适用性评估。"
        "本文件旨在支持戴博士、刘劳伦斯及项目管理团队之间的决策讨论。",
        align="C")
    pdf.ln(10)

    pdf.info_box("项目背景", [
        "设备: sEMG神经驱动 + EIT通气/灌注ICU监护仪",
        "监管路径: FDA 510(k) II类器械许可 (18-23个月项目周期)",
        "当前知识产权持有方: 戴博士 / 思澜科技 (中国成都)",
        "拟设美国实体: 特拉华州C型公司 ('Company B USA')",
        "发明人: 戴博士 (CTO, 100%投入)",
        "投资人: 刘劳伦斯 (拟CEO或运营负责人, 领投人)",
        "PMP / 法规负责人: Lon Dailey (510k Bridge, Inc.)",
        "种子轮: 已融资$1.8M (直接股权) -- 资金可供部署",
        "月度支出: 约$45K  |  预计资金跑道: 种子轮约40个月",
    ])

    # ═══════════════════════════════════════
    # 第一部分: 公司架构
    # ═══════════════════════════════════════
    pdf.add_page()
    pdf.sec("I", "公司架构方案")
    pdf.txt(
        "公司架构决定了所有权、治理、责任、税务处理，以及对本项目至关重要的"
        "CFIUS审查风险和FDA申请人资格。以下评估三种主要方案，各有不同的利弊取舍。")

    # ─── 方案A ───
    pdf.add_page()
    pdf.option_header("方案A", "标准特拉华州C型公司 (单一实体)", GREEN)
    pdf.recommendation_badge("推荐方案")
    pdf.ln(2)

    pdf.sub("方案说明")
    pdf.txt(
        "组建一个单一的特拉华州C型公司('Company B USA')。所有知识产权、运营、FDA申报和"
        "投资者股权均在该实体内。成都思澜科技作为独立合同制造商运营，签订制造合同 -- "
        "不持有Company B USA的股权、董事会席位或所有权。")

    pdf.sub("架构图")
    pdf.diagram([
        "+===========================================================+",
        "|              COMPANY B USA (Delaware C-Corp)               |",
        "|                                                           |",
        "|  - 拥有全部知识产权 (专利, 软件, 商业秘密)               |",
        "|  - 510(k)申请人 & FDA设施注册持有人                       |",
        "|  - 发行普通股 + 优先股                                    |",
        "|  - 美国公民占多数的董事会                                 |",
        "+===========================================================+",
        "        |                                     |",
        "        | 雇佣/顾问协议                       | 制造合同",
        "        v                                     v",
        " +-----------------+              +------------------------+",
        " |  团队成员        |              |  思澜科技              |",
        " |  戴博士 (CTO)   |              |  (中国成都)            |",
        " |  Lon (PMP)      |              |  合同制造商             |",
        " |  未来员工        |              |  无股权或控制权         |",
        " +-----------------+              +------------------------+",
    ])

    pdf.sub("治理结构")
    pdf.txt(
        "董事会 (3个席位):\n"
        "  席位1 -- Lon Dailey (美国公民, 由普通股股东选举)\n"
        "  席位2 -- 戴博士 (发明人席位, 由普通股股东选举)\n"
        "  席位3 -- 独立董事 (双方同意, 优先选择美国公民)\n\n"
        "高管:\n"
        "  CEO -- 刘劳伦斯 (如担任运营角色; 发明人计划显示\n"
        "         创始人为CEO/CTO -- 角色分配待确认)\n"
        "  CTO -- 戴博士\n"
        "  秘书/财务 -- Lon Dailey\n\n"
        "刘劳伦斯持有董事会观察员席位(无投票权), 以避免触发CFIUS'外国控制'认定 -- "
        "他通过保护性条款(否决权)保留对重大决策的影响力, 但不占有投票席位。")

    pdf.sub("戴博士的移民身份 -- CFIUS关键变量")
    pdf.txt(
        "目前尚不清楚戴博士是否持有美国国籍或绿卡。"
        "他在美国有亲属, 可能持有美国国籍或永久居留权。"
        "这是董事会构成和CFIUS分析的关键变量:\n\n"
        "  情景A -- 戴博士是美国人 (公民或绿卡持有人):\n"
        "    董事会 = 2名美国人 (Lon + 戴博士) + 1名独立董事\n"
        "    CFIUS影响: 最有利。无需依赖独立董事即可确保美国人占多数。\n"
        "    若独立董事也是美国人, 则董事会3/3由美国人控制。\n\n"
        "  情景B -- 戴博士不是美国人 (外国公民):\n"
        "    董事会 = 1名确认美国人(Lon) + 1名外国人(戴博士) + 1名独立董事\n"
        "    CFIUS影响: 美国人多数取决于独立董事是否为美国人。\n"
        "    此方案仍可行, 但独立董事席位对CFIUS合规变得至关重要。\n\n"
        "  关于亲属的说明: 戴博士在美国的亲属不能作为其代理人持有股份\n"
        "  或董事席位 -- CFIUS审查穿透代持结构, 追溯至实际受益人。\n"
        "  但若戴博士有获得美国永久居留权的途径 (如亲属担保绿卡),\n"
        "  应将此纳入长期治理规划考虑。\n\n"
        "  行动事项: 在最终确定董事会结构和CFIUS申报策略之前,\n"
        "  必须确认戴博士的移民身份。")

    pdf.sub("股权分配 (示例)")
    pdf.table(
        ["各方", "股数", "持股比例", "类型", "贡献"],
        [
            ("戴博士", "4,000,000", "40%", "普通股", "知识产权+CTO"),
            ("刘劳伦斯", "3,000,000", "30%", "优先股", "现金投资"),
            ("Lon Dailey", "1,500,000", "15%", "普通股", "PMP+法规"),
            ("期权池", "1,500,000", "15%", "预留", "未来员工"),
            ("合计", "10,000,000", "100%", "", ""),
        ],
        [40, 25, 22, 22, 58],
    )

    pdf.pros_cons(
        [
            "最简单的结构 -- 一个实体, 一个股权表",
            "对FDA最有利: 申请人直接拥有知识产权",
            "最便于投资者评估和注资",
            "组建和维护成本最低 (约$2K)",
            "美国公民占多数的董事会满足CFIUS要求 (两种戴博士情景均可)",
            "标准的A轮融资结构",
            "特拉华州拥有最成熟的公司法体系",
        ],
        [
            "美国和中国运营之间无结构性隔离",
            "所有责任集中在一个实体 (可通过保险缓解)",
            "戴博士需以知识产权换取股权 (需要信任)",
            "如刘劳伦斯或戴博士是外国公民, 仍需CFIUS申报",
            "思澜除合同外无结构性激励",
        ],
    )

    pdf.info_box("方案A的CFIUS分析", [
        "知识产权归属美国实体: 是 (完全转让)",
        "美国公民控制董事会: 是 (若戴博士为美国人则占2/3,",
        "  若戴博士为外国人则通过Lon+独立董事占2/3)",
        "外国人拥有运营控制权: 否 (仅为观察员)",
        "关键技术在美国实体内: 是 (510(k)申请人)",
        "戴博士身份: 未知 -- 需确认国籍/绿卡状态",
        "可能的CFIUS结论: 建议主动自愿申报;",
        "  两种情景下该结构均可通过审查。",
    ])

    # ─── 方案B ───
    pdf.add_page()
    pdf.option_header("方案B", "美国母公司 + 中国子公司 (控股结构)", ORANGE)
    pdf.conditional_badge("有条件适用 -- 复杂度较高")
    pdf.ln(2)

    pdf.sub("方案说明")
    pdf.txt(
        "Company B USA (特拉华州C型公司)作为母公司组建。成都思澜科技成为Company B USA的"
        "全资子公司 (WFOE -- 外商独资企业)。所有知识产权仍转让给美国母公司, 但中国子公司"
        "正式纳入公司集团内部, 而非保持独立的合同关系。")

    pdf.sub("架构图")
    pdf.diagram([
        "+===========================================================+",
        "|              COMPANY B USA (Delaware C-Corp)               |",
        "|              母公司                                        |",
        "|  - 拥有全部知识产权                                       |",
        "|  - 510(k)申请人                                           |",
        "|  - 向戴博士、刘劳伦斯、Lon发行股权                       |",
        "+===========================================================+",
        "                          |",
        "                    100%控股",
        "                          |",
        "                          v",
        "+===========================================================+",
        "|              思澜科技 (成都)                               |",
        "|              WFOE -- 外商独资企业                          |",
        "|  - 制造运营                                               |",
        "|  - 员工 / 实验室 / 设备                                   |",
        "|  - 在Company B USA指导下运营                              |",
        "|  - 获得仅用于制造的知识产权许可                           |",
        "+===========================================================+",
    ])

    pdf.sub("适用场景")
    pdf.txt(
        "此结构适用于以下情况:\n"
        "  - 公司计划在中国直接雇佣员工 (不仅是合同制造)\n"
        "  - 中国有重大资产需要拥有 (实验室设备、设施)\n"
        "  - 未来计划在中国进行NMPA注册\n"
        "  - 刘劳伦斯或戴博士希望将中国运营正式纳入公司\n"
        "  - 长期计划为双市场 (美国+中国) 商业化")

    pdf.pros_cons(
        [
            "对中国制造运营拥有完全的控制权",
            "为投资者提供合并财务报表",
            "中国实体是子公司而非合作方 -- 更清晰",
            "可直接雇佣中国员工 (不仅是思澜员工)",
            "为后续NMPA (中国药监局) 申报做好准备",
            "知识产权仍归美国母公司 (与方案A对FDA同等有利)",
        ],
        [
            "WFOE在中国的组建费用$30K-$80K, 需3-6个月",
            "需要中国监管审批 (商务部、市场监管总局)",
            "持续的中国合规要求: 税务申报、年度审计、劳动法",
            "适用转让定价规则 (美中公司间交易)",
            "增加CFIUS审查力度 -- 美国公司拥有中国运营",
            "从中国汇回利润需缴纳预提税 (10%)",
            "每年增加$15K-$30K的会计和法律开支",
            "中国数据本地化法律可能适用于子公司数据",
        ],
    )

    pdf.info_box("方案B的CFIUS分析", [
        "知识产权归属美国实体: 是 (母公司持有知识产权)",
        "美国公民控制董事会: 是 (与方案A相同)",
        "是否有外国子公司: 是 -- 增加CFIUS审查复杂性",
        "可能的CFIUS结论: 比方案A审查更深入;",
        "  CFIUS可能要求签署缓解协议, 限制母子公司间数据流动。",
    ])

    pdf.info_box("与方案A的成本对比", [
        "组建成本: 多出$30K-$80K (中国WFOE注册)",
        "年度运营成本: 多出$15K-$30K (中国合规、审计、法律)",
        "组建时间: 3-6个月 (方案A仅需1-2周)",
        "净增: 第一年比方案A多$60K-$110K。",
    ])

    # ─── 方案C ───
    pdf.add_page()
    pdf.option_header("方案C", "平行实体 (合同联盟)", RED)
    pdf.not_recommended_badge("不推荐 -- 不适用于510(k)路径")
    pdf.ln(2)

    pdf.sub("方案说明")
    pdf.txt(
        "两个独立公司平行运营: Company B USA(特拉华州C型公司)在美国, 思澜科技(现有实体)"
        "在中国。两者仅通过合同连接 -- 制造合同、知识产权许可和交叉股权条款。"
        "两者之间不存在所有权关系。")

    pdf.sub("架构图")
    pdf.diagram([
        "+---------------------------+           +---------------------------+",
        "|    Company B USA          |           |    思澜科技              |",
        "|    (Delaware C-Corp)      |  许可证   |    (中国成都)            |",
        "|                           | <=======> |                           |",
        "|  - 510(k)申请人          |  制造合同 |  - 持有部分/全部IP       |",
        "|  - 美国市场运营          |           |  - 制造                   |",
        "|  - 美国投资者            |  收入分成 |  - 中国市场(独立)        |",
        "|  - Lon, 刘劳伦斯        |           |  - 戴博士的基础实体      |",
        "+---------------------------+           +---------------------------+",
        "",
        "        无所有权关系 -- 仅为合同关系",
    ])

    pdf.sub("变体")
    pdf.txt(
        "C1 -- 许可模式: 思澜持有IP, 许可给Company B USA\n"
        "C2 -- 分割模式: IP按地域分割 (美国权利归Company B, 中国归思澜)\n"
        "C3 -- 收入分成: 双方共有IP, 按市场分配收入")

    pdf.pros_cons(
        [
            "无需组建WFOE (思澜已存在)",
            "戴博士保留中国的IP控制权 (可能更倾向此方案)",
            "避免将中国运营纳入美国实体",
            "思澜可独立开拓中国/亚太市场",
            "中国方面合规更简单 (无外资所有权问题)",
        ],
        [
            "FDA关注: 申请人不拥有该技术",
            "投资者回避 -- 无法评估IP价值",
            "收购方必须与两个实体分别谈判",
            "CFIUS风险: 中国实体控制关键技术",
            "许可证可被撤销, 动摇美国公司根基",
            "转让定价和特许权使用费产生税务复杂性",
            "无合并财务报表 -- 两套独立损益表",
            "治理纠纷无内部解决机制",
            "IP纠纷跨越两个法律体系 (美国+中国)",
            "无IP所有权削弱510(k)对比器械策略",
        ],
    )

    pdf.info_box("方案C的FDA影响", [
        "510(k)申请人必须证明其控制所提交的技术。",
        "来自外国实体的许可构成依赖关系, FDA可能质疑。",
        "若许可被撤销, 已获批的器械将失去IP支撑。",
        "FDA审查员可能要求IP所有权证明 -- 许可证效力较弱。",
        "这不阻止510(k)批准, 但增加风险和审查时间。",
    ], RED)

    pdf.info_box("方案C的CFIUS分析", [
        "知识产权归属美国实体: 否 (或仅部分)",
        "中国实体控制关键技术: 是",
        "可能的CFIUS结论: 三个方案中风险最高;",
        "  可能导致强制申报和潜在阻止, 若中国实体",
        "  保留对医疗器械IP的控制权。",
    ], RED)

    # ─── 对比表 ───
    pdf.add_page()
    pdf.sub("公司架构 -- 对比一览")
    pdf.ln(2)

    comp_col = [48, 48, 48, 26]
    pdf.table(
        ["评估标准", "A: 单一公司", "B: 母公司+子公司", "C: 平行实体"],
        [
            ("组建成本", "$1.5K-$2K", "$30K-$80K", "$1.5K-$2K"),
            ("组建时间", "1-2周", "3-6个月", "1-2周"),
            ("年度运营成本", "$2K-$5K", "$20K-$35K", "$5K-$10K"),
            ("IP归属", "美国实体", "美国母公司", "分割/中国"),
            ("FDA有利程度", "最强", "强", "最弱"),
            ("投资者吸引力", "最高", "高", "低"),
            ("CFIUS风险", "低-中", "中等", "高"),
            ("中国市场", "通过合同", "通过子公司", "直接"),
            ("收购吸引力", "最高", "高", "复杂"),
            ("复杂度", "低", "高", "中等"),
            ("推荐", "是", "有条件", "否"),
        ],
        comp_col,
    )

    pdf.txt(
        "建议: 方案A是正确的起始架构。如果公司后续决定在中国直接雇佣员工或申请NMPA注册, "
        "可在当时组建WFOE转换为方案B。在公司组建阶段无需承担方案B的成本和复杂度。"
        "510(k)路径应避免采用方案C。")

    # ═══════════════════════════════════════
    # 第二部分: 知识产权所有权与转让
    # ═══════════════════════════════════════
    pdf.add_page()
    pdf.sec("II", "知识产权所有权与技术转让方案")
    pdf.txt(
        "知识产权是本项目的核心资产。IP策略决定了FDA申请人资格、投资者信心、"
        "CFIUS审查风险以及收购准备度。以下提出三个方案, 推荐方案排在首位。")

    pdf.ln(2)
    pdf.info_box("当前知识产权清单 (待与戴博士确认)", [
        "sEMG神经驱动算法和信号处理软件",
        "EIT通气/灌注重建算法",
        "MyoBus通信协议和固件",
        "硬件设计文件 (PCB, 传感器阵列, 电极配置)",
        "专利申请 (管辖区和状态待确认)",
        "商业秘密 (校准方法, 训练数据, 信号模型)",
        "软件版权 (嵌入式固件, 桌面分析工具)",
    ])

    pdf.info_box("重要: 两阶段IP转让 (按发明人商业计划v7)", [
        "第一阶段 (立即/种子轮): sEMG IP + MyoBus协议 + 相关软件",
        "  -- 在公司成立时转让给Company B USA, 对价为创始人股权",
        "  -- 须在FDA预申请会议(M+2)前完成",
        "",
        "第二阶段 (延后/A轮): EIT算法 + EIT硬件设计",
        "  -- EIT IP目前由中国A公司持有",
        "  -- A轮融资到位后启动转让谈判 (Year 1 Q2-Q4)",
        "  -- 可能为买断或独家许可, 视谈判情况而定",
        "  -- 不影响sEMG 510(k)提交 (模块A独立运作)",
        "",
        "40%股权对价IP的计算须明确: 40%是仅覆盖sEMG IP(第一阶段),",
        "还是包含未来EIT转让。",
    ], color=ORANGE)

    # ─── IP方案1 ───
    pdf.add_page()
    pdf.option_header("IP方案1", "全部转让给美国实体 + 回授许可", GREEN)
    pdf.recommendation_badge("推荐 -- 对FDA和投资者最有利")
    pdf.ln(2)

    pdf.sub("运作方式")
    pdf.txt(
        "这是一个两步法律交易:\n\n"
        "第一步 -- IP转让 (中国到美国)\n"
        "戴博士(或思澜科技, 视IP持有方而定)签署IP转让协议, 将专利、专利申请、"
        "软件版权、商业秘密和技术诀窍的全部权利、所有权和权益转让给Company B USA。"
        "这是永久性、不可撤销的转让。Company B USA成为合法所有人。\n\n"
        "第二步 -- 制造回授许可 (美国到中国)\n"
        "Company B USA授予思澜科技一项有限许可, 仅允许其代表Company B USA制造该设备。"
        "该许可:\n"
        "  - 非独占性 (Company B USA可在未来使用其他制造商)\n"
        "  - 可撤销 (如思澜表现不佳, Company B USA可终止)\n"
        "  - 范围有限 (仅限制造, 不得独立销售)\n"
        "  - 由美国实体全程控制\n\n"
        "第三步 (可选) -- 学术/科研回授许可\n"
        "向戴博士个人授予一项单独的永久性、免费许可, 用于学术研究、教学和论文发表 -- "
        "仅限非商业用途。保障戴博士继续开展学术工作的能力。")

    pdf.sub("结构图")
    pdf.diagram([
        "+---------------------------+     全部IP转让       +---------------------------+",
        "|   戴博士 / 思澜科技      | =====================>|    Company B USA           |",
        "|   (中国成都)              |  (永久, 全部权利)    |    (Delaware C-Corp)       |",
        "|                           |                      |                            |",
        "|   当前IP持有方            |                      |    新的合法IP所有人        |",
        "|   发明人                  |                      |    510(k)申请人            |",
        "+---------------------------+                      +----------------------------+",
        "            ^                                                    |",
        "            |          制造回授许可                              |",
        "            +<==================================================+",
        "              (非独占, 可撤销, 仅限制造, 美方控制)",
        "",
        "戴博士的价值交换:  IP所有权  --->  股权所有权 (40%)",
        "若Company B USA估值$20M:  40% = $8M (远超个人持有IP的价值)",
    ])

    pdf.sub("转让协议关键条款")
    pdf.txt(
        "  转让方:          戴博士 和/或 思澜科技\n"
        "  受让方:          Company B USA (特拉华州C型公司)\n"
        "  范围:            全部专利、专利申请、版权、商业秘密、\n"
        "                   技术诀窍及衍生作品\n"
        "  对价:            创始人股份 (4,000,000股普通股 = 40%)\n"
        "  适用法律:        特拉华州 (美国)\n"
        "  声明与保证:      转让方保证拥有清晰产权、无负担、\n"
        "                   无第三方主张、无高校所有权\n"
        "  登记备案:        在USPTO及相关外国专利局登记转让")

    pdf.sub("回授许可关键条款")
    pdf.txt(
        "  许可方:          Company B USA\n"
        "  被许可方:        思澜科技\n"
        "  范围:            按Company B USA规格制造ICU呼吸\n"
        "                   数字孪生设备及组件\n"
        "  独占性:          非独占\n"
        "  地域:            中国 (仅限制造, 不包括销售)\n"
        "  许可费:          $0 (成本含在制造协议定价中)\n"
        "  期限:            与制造协议同期\n"
        "  终止:            Company B USA可提前90天通知终止\n"
        "  分许可:          未经书面同意不得分许可")

    pdf.sub("此方案下戴博士的保护机制")
    pdf.info_box("发明人保护机制", [
        "1. 股权: 40%创始人股份 = 最大个人持股",
        "2. 加速归属: 若无故被终止, 100%立即归属",
        "3. IP否决权: 任何IP的出售、许可或分许可须经戴博士同意",
        "4. 回归条款: 若Company B USA放弃该设备 (12个月无商业活动",
        "   且无进行中的FDA申报), IP回归戴博士",
        "5. 学术许可: 永久性使用IP进行科研和教学的权利",
        "6. 董事会席位: 持股>10%期间保证董事席位",
        "7. 反稀释: 宽基加权平均反稀释保护条款",
    ], GREEN)

    pdf.pros_cons(
        [
            "FDA: 申请人直接拥有IP -- 最有利位置",
            "投资者: 美国实体下的清晰IP产权, 适用美国法律",
            "收购方: 单一实体拥有一切 -- 最简单的并购",
            "CFIUS: 美国实体拥有关键技术",
            "无需持续的许可费谈判或许可纠纷",
            "戴博士通过股权保留价值 (可能更大)",
            "回归条款在公司失败时保护戴博士",
            "数千家初创企业使用的标准结构",
        ],
        [
            "戴博士必须信任股权模式而非IP持有",
            "转让在法律上是永久性的 (回归条款为安全网)",
            "跨境IP转让需要审慎的法律起草",
            "中国专利局备案可能需要3-6个月",
            "若戴博士股权被稀释至10%以下, 将失去董事席位",
        ],
    )

    # ─── IP方案2 ───
    pdf.add_page()
    pdf.option_header("IP方案2", "独占许可给美国实体 (中国保留所有权)", ORANGE)
    pdf.conditional_badge("有条件适用 -- 对FDA效力较弱, 但可行")
    pdf.ln(2)

    pdf.sub("运作方式")
    pdf.txt(
        "戴博士或思澜科技保留全部IP的法律所有权。Company B USA获得一项独占性、"
        "全球范围的许可, 用于ICU呼吸数字孪生设备的开发、监管许可、制造和商业化。"
        "该许可在固定期限 (如20年) 内不可撤销, 或与基础专利的有效期挂钩。")

    pdf.sub("结构图")
    pdf.diagram([
        "+---------------------------+   独占许可           +---------------------------+",
        "|   戴博士 / 思澜科技      | =====================>|    Company B USA           |",
        "|   (中国成都)              | (全球, 不可撤销)     |    (Delaware C-Corp)       |",
        "|                           | (20年或专利有效期)   |                            |",
        "|   保留IP所有权            |                      |    独占被许可方            |",
        "|   许可方                  |                      |    510(k)申请人            |",
        "+---------------------------+                      +----------------------------+",
        "",
        "所有权留在中国。使用权归美国。",
    ])

    pdf.sub("许可关键条款")
    pdf.txt(
        "  许可方:          戴博士 / 思澜科技\n"
        "  被许可方:        Company B USA\n"
        "  范围:            与ICU呼吸数字孪生相关的所有用途\n"
        "  独占性:          全球独占 (许可方不得再许可他人)\n"
        "  不可撤销性:      除重大违约外不可撤销\n"
        "  许可费:          选项 -- (a) $0, 以股权为对价,\n"
        "                   (b) 净销售额的X%, (c) 年度固定费用\n"
        "  分许可:          Company B USA可分许可给合同制造商\n"
        "  改进:            双方的所有改进均纳入许可范围")

    pdf.pros_cons(
        [
            "戴博士保留正式的IP所有权 (心理上更安全)",
            "无需跨境转让手续 / 专利局备案",
            "戴博士可独立在中国/亚太市场使用IP",
            "许可可包含收入分成条款",
            "比全部转让更快执行",
        ],
        [
            "FDA: 申请人不拥有技术 -- 位置较弱",
            "FDA可能要求证明许可不可撤销",
            "投资者强烈反对 -- IP风险在公司之外",
            "收购方须与许可方另行谈判 (部分收购方的红线)",
            "CFIUS: 中国实体控制关键医疗器械技术",
            "若戴博士/思澜产生纠纷, 美国公司将面临风险",
            "许可费产生持续成本和转让定价问题",
            "保险 (D&O, E&O) 可能因IP结构更贵",
            "兴企后续融资 -- 风投可能要求转为方案1",
        ],
    )

    pdf.info_box("FDA影响", [
        "FDA不要求510(k)申请人拥有IP所有权。",
        "但FDA期望申请人控制该技术。",
        "独占性、不可撤销的许可可满足此要求 -- 但审查员",
        "可能就该安排提出后续问题。",
        "结论: 可行, 但可能增加1-3个月审查时间。",
    ], ORANGE)

    pdf.info_box("投资者影响", [
        "多数美国风投不会在此结构下投资。",
        "尽职调查会立即标记IP风险。",
        "若计划A轮融资, 投资者可能要求转换为",
        "方案1 (全部转让) 作为投资条件。",
        "结论: 适用于天使/种子轮, 但阻碍机构投资。",
    ], RED)

    # ─── IP方案3 ───
    pdf.add_page()
    pdf.option_header("IP方案3", "按地域分割所有权", RED)
    pdf.not_recommended_badge("不推荐")
    pdf.ln(2)

    pdf.sub("运作方式")
    pdf.txt(
        "知识产权按地域划分。Company B USA拥有美国(以及可选的欧盟/其他西方市场)的全部权利。"
        "戴博士或思澜保留中国、亚太及其他地区的全部权利。"
        "各实体可在其分配的地域内独立商业化。")

    pdf.sub("结构图")
    pdf.diagram([
        "+---------------------------+           +---------------------------+",
        "|    Company B USA          |           |    戴博士 / 思澜         |",
        "|    (Delaware C-Corp)      |           |    (中国成都)             |",
        "|                           |           |                           |",
        "|  拥有: 美国专利权         |           |  拥有: 中国/亚太专利权   |",
        "|  拥有: 美国软件版权       |           |  拥有: 中国软件版权      |",
        "|  市场: 美国, 欧盟, 加拿大 |           |  市场: 中国, 亚太        |",
        "|  510(k)申请人             |           |  NMPA申请人              |",
        "+---------------------------+           +---------------------------+",
        "",
        "        协调协议 (交叉改进, 按地域互不竞争)",
    ])

    pdf.pros_cons(
        [
            "两个实体完全独立 -- 无跨境控制问题",
            "戴博士可在中国/亚太自由商业化",
            "无需全部IP转让协议",
            "各实体可在各自市场独立融资",
            "思澜可同时申请NMPA注册",
        ],
        [
            "FDA: 不清楚谁拥有'该'技术 -- 分割令审查员困惑",
            "专利不易按地域分割 (尤其是美国实用新型专利)",
            "软件版权本质上是全球性的 -- 难以划分",
            "商业秘密无法'分割' -- 双方都知道",
            "投资者视为两个公司用同一技术竞争",
            "收购方仅获得一半IP -- 价值大幅降低",
            "CFIUS: 中国实体仍控制关键技术",
            "协调协议产生持续法律开支",
            "改进归属纠纷不可避免",
            "若一方修改技术, 衍生作品归属不明",
            "两套独立的监管申报 (FDA + NMPA) = 双倍成本",
        ],
    )

    pdf.info_box("为何此方案不适用于510(k)", [
        "FDA 510(k)申报要求清晰的IP所有权链。",
        "分割所有权造成技术控制权的模糊性。",
        "若中国实体独立修改设备, 美国510(k)可能不再",
        "代表实际销售的设备。",
        "结论: 理论上可行, 但实际上不适用于FDA路径。",
    ], RED)

    # ─── IP对比表 ───
    pdf.add_page()
    pdf.sub("IP方案 -- 对比一览")
    pdf.ln(2)

    pdf.table(
        ["评估标准", "1: 全部转让", "2: 独占许可", "3: 分割"],
        [
            ("IP法律所有人", "美国实体", "中国实体", "双方"),
            ("FDA有利程度", "最强", "可行", "最弱"),
            ("投资者吸引力", "最高", "低-中", "极低"),
            ("收购吸引力", "最高", "中等", "低"),
            ("CFIUS风险", "最低", "中-高", "高"),
            ("戴博士IP控制", "通过股权+否决权", "保留所有权", "保留中国权利"),
            ("组建复杂度", "中等", "低", "高"),
            ("持续法律成本", "低", "中等", "高"),
            ("融资影响", "无障碍", "阻碍风投", "阻碍全部"),
            ("回归可能性", "是(合同约定)", "不适用(仍拥有)", "不适用"),
            ("推荐", "是", "有条件", "否"),
        ],
        [42, 42, 42, 42],
    )

    # ═══════════════════════════════════════
    # 第三部分: IP转让操作流程
    # ═══════════════════════════════════════
    pdf.add_page()
    pdf.sec("III", "知识产权转让操作流程与时间表")
    pdf.txt(
        "若选择方案1(全部转让), 需执行以下步骤。"
        "注意: 按发明人商业计划(v7), 初始IP转让覆盖sEMG算法、"
        "MyoBus协议和相关软件。EIT IP转让是单独谈判, 推迟至A轮(Year 1 Q2-Q4)。\n\n"
        "sEMG IP转让应在FDA预申请会议(M+2)之前完成, "
        "以便Company B USA能向FDA审查员证明IP所有权。")

    pdf.sub("转让清单")
    pdf.txt(
        "  1. 知识产权盘点\n"
        "     清点全部IP: 专利、专利申请、版权、商业秘密、\n"
        "     技术诀窍、源代码、硬件设计、训练数据。\n"
        "     确认每项IP的当前法律所有人。\n"
        "     确认无高校、雇主或政府主张。\n\n"
        "  2. IP转让协议\n"
        "     由美国IP律师起草 (适用特拉华州法律)。\n"
        "     戴博士/思澜与Company B USA共同签署。\n"
        "     对价: 创始人股权 (4,000,000股) 在协议中注明。\n"
        "     公证并加注海牙认证以获国际认可。\n\n"
        "  3. 专利局备案登记\n"
        "     USPTO: 为任何美国专利申请登记转让。\n"
        "     CNIPA (中国): 为中国专利申请登记转让。\n"
        "     其他管辖区: PCT申请、EP申请等。\n"
        "     时间: 视管辖区而定, 1-6个月。\n\n"
        "  4. 软件版权登记\n"
        "     在美国版权局登记关键软件版权。\n"
        "     在美国法院提供所有权的法律推定。\n"
        "     费用: 每项登记约$65。\n\n"
        "  5. 商业秘密文档化\n"
        "     将商业秘密记录在保密登记册中。\n"
        "     实施访问控制 (谁可查看什么)。\n"
        "     Company B USA须证明采取了'合理措施'加以保护。\n\n"
        "  6. 制造回授许可签署\n"
        "     与转让协议同步起草。\n"
        "     界定范围、限制和终止权。\n"
        "     与思澜的总体制造协议挂钩。")

    pdf.sub("预计时间表 (从决策到完成)")
    pdf.table(
        ["步骤", "周期", "前置条件", "费用"],
        [
            ("IP盘点与审计", "2-3周", "戴博士配合", "$5K-$10K"),
            ("转让协议起草", "2-3周", "聘请IP律师", "$8K-$15K"),
            ("谈判与签署", "1-2周", "各方达成一致", "含在上项"),
            ("USPTO备案", "2-4周", "已签署协议", "$500-$1K"),
            ("CNIPA备案", "2-6个月", "中国专利代理人", "$2K-$5K"),
            ("回授许可签署", "1-2周", "转让完成", "$3K-$5K"),
            ("版权登记", "3-6个月", "向USCO提交", "$500-$1K"),
            ("合计", "3-4个月*", "* 多项并行", "$19K-$37K"),
        ],
        [48, 28, 48, 30],
    )

    pdf.set_font("ARUNI", "I", 9)
    pdf.set_text_color(*GRAY)
    pdf.txt(
        "* CNIPA备案和版权登记可与FDA预申请准备同步进行。"
        "关键里程碑是已签署的转让协议, 可在聘请律师后6-8周内完成。")

    # ═══════════════════════════════════════
    # 第四部分: 综合建议
    # ═══════════════════════════════════════
    pdf.add_page()
    pdf.sec("IV", "综合建议")

    pdf.sub("推荐结构", GREEN)
    pdf.txt(
        "基于FDA 510(k)路径、美国投资者预期、CFIUS风险管理和收购准备度, "
        "推荐的组合方案为:\n\n"
        "  公司架构:    方案A -- 标准特拉华州C型公司 (单一实体)\n"
        "  IP策略:      方案1 -- 全部转让给美国实体 + 回授许可\n\n"
        "这是美国医疗器械初创企业处理外国来源技术的标准、成熟路径。"
        "机构投资者、FDA审查员和潜在收购方均期望看到此结构。")

    pdf.sub("此组合方案的优势")
    pdf.txt(
        "  FDA: 510(k)申请人拥有技术。无IP控制问题。\n"
        "  投资者: 清晰的股权表, 单一实体, IP在美国管辖范围内。\n"
        "  CFIUS: 美国实体拥有IP, 美国人占多数的董事会, 无外国控制。\n"
        "  收购方: 一个收购对象, 一个IP组合, 一个股权表。\n"
        "  戴博士: 受股权(40%)、加速归属、IP否决权、回归条款保护。\n"
        "  刘劳伦斯: 受优先股、清算优先权、保护性条款保护。\n"
        "  Lon: 受股权(15%)、归属、双触发加速保护。\n"
        "  思澜: 受制造协议保护 (收入流持续)。")

    pdf.sub("今日讨论的决策要点")
    pdf.info_box("需要回答的问题", [
        "1. 谁目前持有IP? (戴博士个人? 思澜? 大学?)",
        "2. 戴博士是否愿意以创始人股权为对价转让IP?",
        "3. 刘劳伦斯是否同意IP归属美国实体?",
        "4. 是否有共同发明人、合作者或政府资助?",
        "5. 是否有任何第三方许可 (软件、算法、硬件)?",
        "6. 刘劳伦斯的国籍/居留状态? (影响CFIUS)",
        "7. 戴博士的国籍/居留状态? (美国公民、绿卡、签证,",
        "   还是无? 在美亲属是否持有相关身份?)",
        "8. 目标股权分配: 40/30/15/15作为起点是否可接受?",
        "9. 3人董事会 (2个美国席位 + 1个发明人席位) 是否可接受?",
    ])

    pdf.ln(2)
    pdf.sub("决策后的下一步行动")
    pdf.txt(
        "  1. 聘请特拉华州注册代理人 + 提交公司注册证书\n"
        "  2. 聘请美国IP律师起草IP转让协议\n"
        "  3. 起草刘劳伦斯投资的条款清单 (金额、估值、工具)\n"
        "  4. 起草限制性股票协议 (戴博士 + Lon)\n"
        "  5. 起草主服务协议 (510k Bridge, Inc.)\n"
        "  6. 起草与思澜科技的制造协议\n"
        "  7. 提交自愿CFIUS申报 (如刘劳伦斯或戴博士为外国人)\n"
        "  8. 准备FDA预申请资料包 (需附IP所有权文件)")

    pdf.ln(4)
    pdf.set_draw_color(*BLUE)
    mid = pdf.w / 2
    pdf.line(mid - 40, pdf.get_y(), mid + 40, pdf.get_y())
    pdf.ln(4)
    pdf.set_font("ARUNI", "I", 9)
    pdf.set_text_color(*GRAY)
    pdf.multi_cell(0, 5,
        "本文件仅供内部决策使用, 不构成法律建议。"
        "所有结构性决策在执行前应由合格的公司律师和知识产权顾问审核。",
        align="C")

    path = os.path.join(OUT_DIR, "Corporate_Structure_IP_Options_CN.pdf")
    pdf.output(path)
    return path


if __name__ == "__main__":
    p = build()
    print(f"Generated: {p}")
