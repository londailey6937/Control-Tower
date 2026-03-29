#!/usr/bin/env python3
"""
Generate Chinese translation of the dual-path immigration strategy PDF.
510kBridge 家庭移民策略 -- 中文版
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

    def __init__(self):
        super().__init__("P", "mm", "Letter")
        font_path = "/Library/Fonts/Arial Unicode.ttf"
        self.add_font("ARUNI", "", font_path, uni=True)
        self.add_font("ARUNI", "B", font_path, uni=True)
        self.add_font("ARUNI", "I", font_path, uni=True)

    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("ARUNI", "I", 7)
        self.set_text_color(*GRAY)
        self.cell(0, 5, "机密文件", align="R")
        self.ln(7)

    def footer(self):
        self.set_y(-13)
        self.set_font("ARUNI", "I", 7)
        self.set_text_color(*GRAY)
        self.cell(0, 5, f"第 {self.page_no()}/{{nb}} 页", align="C")

    def sec(self, title):
        if self.get_y() > self.h - 40:
            self.add_page()
        self.ln(3)
        self.set_font("ARUNI", "B", 12)
        self.set_text_color(*NAVY)
        self.cell(0, 7, title, new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(*NAVY)
        self.set_line_width(0.4)
        self.line(self.l_margin, self.get_y(),
                  self.w - self.r_margin, self.get_y())
        self.ln(4)

    def sub(self, title):
        self.set_font("ARUNI", "B", 10.5)
        self.set_text_color(*NAVY)
        self.cell(0, 6, title, new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def txt(self, text):
        self.set_font("ARUNI", "", 10)
        self.set_text_color(*TEXT)
        self.multi_cell(0, 5.5, text, new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def green_txt(self, text):
        self.set_font("ARUNI", "B", 10)
        self.set_text_color(*GREEN)
        self.multi_cell(0, 5.5, text, new_x="LMARGIN", new_y="NEXT")
        self.set_text_color(*TEXT)
        self.ln(2)

    def bullet(self, text, indent=6):
        self.set_font("ARUNI", "", 10)
        self.set_text_color(*TEXT)
        self.set_x(self.l_margin + indent)
        self.multi_cell(self.w - self.l_margin - self.r_margin - indent, 5.5,
                        f"· {text}", new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def bold_bullet(self, label, text, indent=6):
        self.set_x(self.l_margin + indent)
        self.set_font("ARUNI", "B", 10)
        self.set_text_color(*TEXT)
        lw = self.get_string_width(label) + 1
        self.cell(lw, 5.5, label)
        self.set_font("ARUNI", "", 10)
        self.multi_cell(0, 5.5, text, new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def table(self, headers, rows, col_w):
        needed = 7 + len(rows) * 6 + 10
        if self.get_y() + needed > self.h - 20:
            self.add_page()
        self.set_font("ARUNI", "B", 9)
        self.set_text_color(*WHITE)
        self.set_fill_color(*NAVY)
        for i, h in enumerate(headers):
            self.cell(col_w[i], 7, h, border=1, fill=True, align="C")
        self.ln()
        self.set_text_color(*TEXT)
        for ri, row in enumerate(rows):
            self.set_font("ARUNI", "", 9)
            bg = LIGHT_BG if ri % 2 == 0 else WHITE
            self.set_fill_color(*bg)
            for ci, val in enumerate(row):
                align = "L" if ci == 0 else "C"
                self.cell(col_w[ci], 6, val, border=1, fill=True, align=align)
            self.ln()
        self.ln(3)


def build():
    pdf = StrategyPDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.set_margins(22, 18, 22)

    # ── 第一页：抬头 ──────────────────────────────
    pdf.add_page()
    pdf.set_font("ARUNI", "B", 18)
    pdf.set_text_color(*NAVY)
    pdf.cell(0, 10, "510kBridge", align="L", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("ARUNI", "", 9)
    pdf.set_text_color(*GRAY)
    pdf.cell(0, 4, "特拉华州注册公司", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 4, "510kbridge.com  |  info@510kbridge.com",
             new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)
    pdf.set_draw_color(*NAVY)
    pdf.set_line_width(0.6)
    pdf.line(pdf.l_margin, pdf.get_y(), pdf.w - pdf.r_margin, pdf.get_y())
    pdf.ln(6)

    # 标题
    pdf.set_font("ARUNI", "B", 16)
    pdf.set_text_color(*NAVY)
    pdf.cell(0, 10, "家庭移民策略", align="C",
             new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("ARUNI", "", 10)
    pdf.set_text_color(*GRAY)
    pdf.cell(0, 5, "刘家双通道移民方案", align="C",
             new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)
    today = date.today().strftime("%Y年%m月%d日")
    pdf.cell(0, 5, f"编制日期：{today}", align="C",
             new_x="LMARGIN", new_y="NEXT")
    pdf.ln(8)

    # ── 摘要 ──────────────────────────────────────
    pdf.sec("方案摘要")

    pdf.txt(
        "本文件为刘家制定了一个双通道移民策略，通过510kBridge实现全家赴美。"
        "方案不再以宗刚作为EB-5投资人，而是让Danielle担任投资人——"
        "直接解决她的永久身份需求——同时通过EB-1C跨国经理人调动的方式，"
        "为宗刚和Lisa获得绿卡，无需额外投资。"
    )

    pdf.green_txt(
        "结果：四位成年人均获绿卡。Claire已是美国公民。"
    )

    pdf.table(
        ["家庭成员", "移民通道", "身份"],
        [
            ["Danielle Liu（刘小鸟）", "EB-5（主申请人）", "绿卡"],
            ["Malei（马磊）", "EB-5（配偶附属）", "绿卡"],
            ["Claire", "不适用", "美国公民（在美出生）"],
            ["Lawrence Liu（刘宗刚）", "EB-1C（跨国经理人）", "绿卡"],
            ["Lisa Liu", "EB-1C（配偶附属）", "绿卡"],
        ],
        [50, 60, 50]
    )

    # ── 通道A：Danielle EB-5 ──────────────────────
    pdf.sec("通道A：Danielle Liu — EB-5投资移民")

    pdf.sub("运作方式")
    pdf.txt(
        "Danielle以EB-5主申请人身份提交I-526E申请。她向510kBridge投资80万美元，"
        "公司注册在华盛顿州Camas——一个符合目标就业区（TEA）条件的地区，"
        "投资门槛从105万美元降至80万美元。公司须在两年内创造至少10个全职美国就业岗位。"
    )

    pdf.sub("资金来源")
    pdf.txt(
        "美国移民局（USCIS）接受父母赠与作为合法投资资金来源。"
        "宗刚可以将80万美元赠与Danielle，需提供完整文件：赠与信、"
        "宗刚在中国的合法收入证明、以及清晰的银行转账记录。"
        "这在EB-5案例中是成熟且常见的做法。"
    )

    pdf.sub("谁能获得绿卡")
    pdf.bold_bullet("Danielle Liu：", "主申请人——I-526E获批后获得有条件绿卡")
    pdf.bold_bullet("Malei（马磊）：", "附属受益人（Danielle的配偶）——"
                    "同一申请自动获得有条件绿卡")
    pdf.bold_bullet("Claire：", "已是美国公民——无需任何移民手续")

    pdf.sub("时间线")
    pdf.table(
        ["步骤", "时间", "说明"],
        [
            ["准备I-526E申请", "2-4个月", "商业计划、资金来源文件"],
            ["USCIS审理I-526E", "12-18个月", "当前审理周期"],
            ["调整身份或领事处理", "3-6个月", "如Danielle在美国：AOS"],
            ["有条件绿卡", "第18-24个月", "有效期2年"],
            ["提交I-829（解除条件）", "第42-48个月", "证明就业创造、资金在险"],
            ["永久绿卡", "第48-54个月", "正式永久居民"],
        ],
        [50, 30, 80]
    )

    pdf.sub("为何由Danielle而非宗刚作为投资人")
    pdf.txt(
        "宗刚明确表示，他最关心的是\u201c给Danielle他们在美国有个事情做\u201d。"
        "由Danielle作为投资人："
    )
    pdf.bullet("她直接获得自己的绿卡——不依赖宗刚")
    pdf.bullet("Malei作为附属配偶自动获得绿卡")
    pdf.bullet("她在美国每天管理公司运营——解决宗刚\u201c控制能力太弱\u201d的顾虑")
    pdf.bullet("宗刚无需满足EB-5的永久迁居要求——他可以留在中国，按需往来")
    pdf.bullet("80万投资进入家族企业，而非以不满意的估值投入别人的公司")

    # ── 通道B：Lawrence EB-1C ─────────────────────
    pdf.sec("通道B：宗刚 & Lisa — EB-1C跨国经理人")

    pdf.sub("运作方式")
    pdf.txt(
        "EB-1C签证面向跨国经理人和高管。它允许美国公司从关联的海外公司"
        "调动经理或高管。与EB-5不同，不需要投资。与EB-2/EB-3不同，"
        "不需要劳工证（PERM）。"
    )

    pdf.sub("基本要求")
    pdf.bold_bullet("海外公司：", "宗刚须在中国的关联公司以经理或高管身份"
                    "连续工作至少1年（在调动前3年内）")
    pdf.bold_bullet("美国公司：", "510kBridge（美国）须与中国实体存在关联、"
                    "子公司或母公司关系")
    pdf.bold_bullet("美国职位：", "宗刚须以经理或高管身份入职510kBridge")
    pdf.bold_bullet("双方均需运营：", "美国和中国公司都须处于正常经营状态"
                    "（不能是空壳公司）")

    pdf.sub("具体架构")
    pdf.txt(
        "510kBridge在中国设立子公司或关联实体——例如"
        "\u201c510kBridge咨询（上海）有限公司\u201d。宗刚担任CEO，"
        "佳伦担任总经理负责日常运营。两人共同管理中国客户关系、"
        "业务拓展和中国区运营。资格期满后，"
        "510kBridge（美国）提交I-140申请，将宗刚调至美国担任CEO。"
    )

    pdf.txt(
        "宗刚目前已是中国一家大型企业的CEO——他具备EB-1C所要求的"
        "高管经验。上海实体并非降级，而是他能力的自然延伸。"
        "佳伦作为总经理确保日常运营的连续性。当宗刚调至美国后，"
        "佳伦升任上海实体CEO，确保中国业务渠道不中断。"
    )

    pdf.txt(
        "这个架构是自然的，不是人为制造的：510kBridge确实需要中国方面的"
        "业务存在来获取中国医疗器械客户。宗刚现有的商业网络和佳伦的"
        "医疗行业经验使他们成为该办事处理想的领导团队。"
        "调任美国高管职位是真实的业务需要。"
    )

    pdf.sub("谁能获得绿卡")
    pdf.bold_bullet("宗刚（Lawrence Liu）：", "主申请人——以跨国经理人/高管身份获得绿卡")
    pdf.bold_bullet("Lisa Liu：", "附属配偶——同一申请自动获得绿卡")

    pdf.sub("时间线")
    pdf.table(
        ["步骤", "时间", "说明"],
        [
            ["设立中国实体", "2-3个月", "外商独资企业（WFOE）注册"],
            ["宗刚任CEO，佳伦任总经理", "至少12个月", "积累资格期"],
            ["提交I-140（EB-1C）", "第14-15个月", "无需PERM/劳工证"],
            ["USCIS审理I-140", "4-8个月", "可选加急处理"],
            ["领事处理", "3-6个月", "在中国美领馆面谈"],
            ["绿卡发放", "第22-30个月", "直接永久绿卡（无条件期）"],
        ],
        [55, 30, 75]
    )

    pdf.sub("EB-1C的核心优势")
    pdf.bullet("无需投资——宗刚保留自己的资金")
    pdf.bullet("无需劳工证（PERM）——更快、无DOL审计风险")
    pdf.bullet("无中国EB-2/EB-3排期问题——EB-1类别对中国基本无排期")
    pdf.bullet("绿卡从第一天起就是永久的——没有2年有条件期")
    pdf.bullet("Lisa作为附属配偶自动获得绿卡")
    pdf.bullet("宗刚初期留在中国——在资格期内建设客户渠道")
    pdf.bullet("佳伦担任总经理确保运营连续性，宗刚调美后佳伦接任CEO")

    # ── 双通道协同 ────────────────────────────────
    pdf.sec("双通道如何协同运作")

    pdf.sub("并行时间线")
    pdf.table(
        ["月份", "通道A（Danielle EB-5）", "通道B（宗刚 EB-1C）"],
        [
            ["0-3", "准备I-526E，提交申请", "注册中国实体"],
            ["3-12", "USCIS审理中", "宗刚（CEO）和佳伦（GM）管理中国"],
            ["12-15", "等待审批", "为宗刚提交I-140"],
            ["15-18", "I-526E获批，提交AOS", "I-140审理中"],
            ["18-24", "有条件绿卡到手", "领事处理"],
            ["24-30", "Danielle和Malei已在美国", "宗刚和Lisa抵达美国"],
            ["42-48", "提交I-829（解除条件）", "已是永久绿卡"],
        ],
        [18, 71, 71]
    )

    pdf.txt(
        "两条通道可以同时推进。Danielle的EB-5申请立即提交，同时着手设立中国实体。"
        "当宗刚完成在中国1年的资格期时，Danielle可能已经拿到有条件绿卡。"
        "2-3年内，全家均可获得美国永久居留权。"
    )

    # ── 家庭角色 ──────────────────────────────────
    pdf.sec("家庭成员在510kBridge的角色")

    pdf.table(
        ["成员", "职位", "职责", "移民通道"],
        [
            ["Danielle Liu", "COO/投资人", "美国运营、财务", "EB-5主申请"],
            ["Malei（马磊）", "运营经理", "行政、后勤、培训", "EB-5附属"],
            ["Claire", "不适用", "不适用（未成年，美国公民）", "美国公民"],
            ["宗刚", "CEO（上海）", "中国业务拓展、客户", "EB-1C主申请"],
            ["Lisa Liu", "顾问", "家庭支持", "EB-1C附属"],
            ["李佳伦", "总经理（上海）", "中国运营、医疗内容", "另行安排"],
            ["Chensy Li", "高级客户经理", "市场营销、销售", "另行安排"],
            ["Lon Dailey", "创始人/首席顾问", "法规、项目管理", "美国公民"],
        ],
        [30, 35, 50, 45]
    )

    # ── 财务结构 ──────────────────────────────────
    pdf.sec("财务结构")

    pdf.sub("投资")
    pdf.txt(
        "EB-5所需投资总额：80万美元（TEA优惠门槛）。这是宗刚赠与Danielle的资金，"
        "需为USCIS提供完整文件。EB-1C通道无需额外投资——宗刚从中国实体领取薪资，"
        "之后从510kBridge（美国）领取薪资。"
    )

    pdf.sub("股权结构")
    pdf.txt(
        "Danielle凭80万美元EB-5投资持有投资人股权。宗刚以CEO身份持有优先股"
        "（无需现金投资）。Lon持有创始人股权。这一结构确保宗刚的持股比例"
        "足够低，使EB-1C调动是真正的雇主-雇员关系，而非自我申请。"
    )

    pdf.sub("营收模式")
    pdf.table(
        ["层级", "服务内容", "月费"],
        [
            ["入门级", "Control Tower SaaS许可", "$500-$2,000"],
            ["专业级", "全面PM、审批管理", "$10K-$25K"],
            ["企业级", "端到端法规+项目管理", "$50K+/项目"],
        ],
        [30, 80, 50]
    )

    pdf.txt(
        "拥有3-5个专业级客户后，公司年收入可达50万-90万美元——"
        "足以为整个团队支付有竞争力的薪资，并支撑美国和中国的运营。"
    )

    # ── 为何选择Camas ─────────────────────────────
    pdf.sec("为何选择华盛顿州Camas")

    pdf.txt(
        "Camas就在波特兰对岸——距机场20分钟车程。"
        "它符合目标就业区（TEA）条件，EB-5投资门槛为80万美元"
        "而非标准的105万美元。"
    )

    pdf.txt(
        "对家庭而言：可以卖掉现有房产（80万美元或以上），在Camas购置新居。"
        "那里有漂亮的房子——有的标价200万美元。全家可以住在一起，"
        "靠近波特兰国际机场，社区环境优美，Claire的学校也很好。"
    )

    # ── 对比分析 ──────────────────────────────────
    pdf.sec("为何选择双通道方案")

    pdf.table(
        ["对比项", "双通道（EB-5+EB-1C）", "仅宗刚EB-5"],
        [
            ["绿卡人数", "4位成年人+Claire（公民）", "仅宗刚+Lisa"],
            ["Danielle身份", "永久（独立申请）", "需另找途径"],
            ["Malei身份", "永久（附属）", "无途径"],
            ["宗刚开支", "$0（EB-1C无需投资）", "80万美元自掏"],
            ["总投资额", "80万（赠与Danielle）", "80万（宗刚直投）"],
            ["宗刚在中国", "可以，管理中国办公室", "必须迁居美国"],
            ["控制力顾虑", "Danielle每天管理美国", "宗刚远在中国，不安"],
            ["需要PERM吗", "不需要", "不需要"],
            ["排期风险", "EB-1基本无排期", "EB-5暂无排期"],
            ["家庭覆盖", "所有人", "仅宗刚+Lisa"],
        ],
        [35, 63, 62]
    )

    # ── 风险与注意事项 ────────────────────────────
    pdf.sec("风险与注意事项")

    pdf.bold_bullet("中国实体必须真实运营：", "中国子公司需有实际运营——"
                    "办公场所、员工、收入。空壳公司不能满足USCIS要求。"
                    "510kBridge确实需要中国方面的业务拓展，因此这是自然满足的。")
    pdf.bold_bullet("1年资格期：", "宗刚必须在中国实体以CEO/高管身份"
                    "连续工作至少1年后，才能提交调动申请。")
    pdf.bold_bullet("宗刚的股权比例：", "必须谨慎设计。如果宗刚在510kBridge"
                    "（美国）持股过多，USCIS可能认定EB-1C为自我申请。"
                    "优先股加上有限投票权，配合Danielle的多数投资人股权，"
                    "可以维持雇主-雇员关系。")
    pdf.bold_bullet("资金来源文件：", "宗刚赠与Danielle的80万美元需要"
                    "全面的合法来源证明：银行记录、纳税申报表、"
                    "近几年的商业收入记录。")
    pdf.bold_bullet("移民律师：", "两条通道都需要有经验的EB-5和EB-1C律师。"
                    "双通道结构成熟可行，但文件必须规范完备。")

    # ── 下一步 ────────────────────────────────────
    pdf.sec("下一步行动")

    pdf.bold_bullet("1. ", "聘请同时擅长EB-5和EB-1C的移民律师")
    pdf.bold_bullet("2. ", "开始Danielle的I-526E申请准备（资金来源、商业计划）")
    pdf.bold_bullet("3. ", "在上海或深圳注册510kBridge中国子公司（WFOE）")
    pdf.bold_bullet("4. ", "宗刚就任中国实体CEO，佳伦就任总经理")
    pdf.bold_bullet("5. ", "提交Danielle的I-526E申请")
    pdf.bold_bullet("6. ", "满12个月后，提交宗刚的I-140（EB-1C）申请")
    pdf.bold_bullet("7. ", "协调两个家庭的领事处理")

    # ── 结尾 ──────────────────────────────────────
    pdf.ln(4)
    pdf.txt(
        "这个方案回应了宗刚提出的每一个顾虑：Danielle和Malei有了有意义的工作"
        "和永久身份；宗刚通过中国实体保持控制力，在他熟悉的环境里运作；"
        "投资进入家族企业，而非以不满意的估值投入别人的公司；"
        "最终全家都来到美国。"
    )

    pdf.ln(2)
    pdf.txt("随时聊，")
    pdf.ln(6)
    pdf.set_font("ARUNI", "", 10)
    pdf.set_text_color(*TEXT)
    pdf.cell(0, 5, "Lon", new_x="LMARGIN", new_y="NEXT")

    # ── 免责声明 ──────────────────────────────────
    pdf.ln(10)
    pdf.set_draw_color(*GRAY)
    pdf.set_line_width(0.3)
    pdf.line(pdf.l_margin, pdf.get_y(), pdf.w - pdf.r_margin, pdf.get_y())
    pdf.ln(3)
    pdf.set_font("ARUNI", "I", 7.5)
    pdf.set_text_color(*GRAY)
    pdf.multi_cell(0, 4,
        "本文件仅供讨论参考，不构成法律、税务或移民建议。EB-5和EB-1C的资格"
        "须由具备资质的移民律师确认。财务预测为估算值，非保证。"
        "移民时间线为近似值，取决于USCIS审理情况。",
        new_x="LMARGIN", new_y="NEXT")

    # ── 保存 ──────────────────────────────────────
    out = os.path.join(OUT_DIR, "510kBridge_Immigration_Strategy_CN.pdf")
    pdf.output(out)
    sz = os.path.getsize(out)
    print(f"Created {out}  ({sz:,} bytes, {pdf.pages_count} pages)")


if __name__ == "__main__":
    build()
