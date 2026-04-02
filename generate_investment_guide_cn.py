#!/usr/bin/env python3
"""Generate Chinese version of the Investment & Fundraising Guide for Medical Device Startups."""

from fpdf import FPDF

FONT_PATH = "/Library/Fonts/Arial Unicode.ttf"

class PDF(FPDF):
    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("china", "", 8)
        self.set_text_color(100, 100, 100)
        self.cell(0, 8, "医疗器械初创企业投资指南 | 条款清单、融资轮次与筹资策略", align="R")
        self.ln(4)
        self.set_draw_color(0, 128, 100)
        self.set_line_width(0.5)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(6)

    def footer(self):
        self.set_y(-15)
        self.set_font("china", "", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"第 {self.page_no()} 页 / 共 {{nb}} 页", align="C")

    def section_banner(self, title):
        self.set_fill_color(0, 100, 80)
        self.rect(10, self.get_y(), 190, 12, "F")
        self.set_font("china", "", 14)
        self.set_text_color(255, 255, 255)
        self.set_xy(15, self.get_y() + 1)
        self.cell(0, 10, title)
        self.ln(16)

    def section_title(self, title):
        self.set_font("china", "", 14)
        self.set_text_color(0, 80, 60)
        self.ln(4)
        self.cell(0, 8, title)
        self.ln(10)

    def sub_title(self, title):
        self.set_font("china", "", 12)
        self.set_text_color(0, 100, 80)
        self.ln(2)
        self.cell(0, 7, title)
        self.ln(3)
        self.set_draw_color(0, 128, 100)
        self.set_line_width(0.4)
        self.line(self.get_x(), self.get_y(), self.get_x() + 50, self.get_y())
        self.ln(5)

    def body(self, text):
        self.set_font("china", "", 10)
        self.set_text_color(30, 30, 30)
        self.multi_cell(0, 5.5, text)
        self.ln(2)

    def bullet(self, text, indent=15):
        self.set_font("china", "", 10)
        self.set_text_color(30, 30, 30)
        x = self.get_x()
        self.set_x(x + indent)
        self.cell(5, 5.5, "-")
        self.multi_cell(0, 5.5, text)
        self.ln(1)

    def key_insight(self, text):
        self.set_fill_color(255, 248, 235)
        self.set_draw_color(200, 160, 60)
        x = self.get_x()
        y = self.get_y()
        self.set_font("china", "", 9)
        self.set_text_color(120, 80, 0)
        self.set_x(x + 10)
        self.multi_cell(170, 5, text, border=1, fill=True)
        self.ln(3)

    def warning_box(self, text):
        self.set_fill_color(255, 240, 240)
        self.set_draw_color(200, 80, 80)
        self.set_font("china", "", 9)
        self.set_text_color(160, 40, 40)
        self.set_x(self.get_x() + 10)
        self.multi_cell(170, 5, text, border=1, fill=True)
        self.ln(3)

    def tbl_row(self, cols, widths, header=False):
        self.set_font("china", "", 9)
        if header:
            self.set_fill_color(0, 100, 80)
            self.set_text_color(255, 255, 255)
        else:
            self.set_fill_color(240, 248, 245)
            self.set_text_color(30, 30, 30)
        h = 7
        x = self.get_x()
        y = self.get_y()
        cx = x
        for i, (col, w) in enumerate(zip(cols, widths)):
            self.rect(cx, y, w, h, "F")
            self.set_draw_color(200, 200, 200)
            self.rect(cx, y, w, h, "D")
            self.set_xy(cx + 2, y)
            self.cell(w - 4, h, col)
            cx += w
        self.set_xy(x, y + h)


pdf = PDF()
pdf.alias_nb_pages()
pdf.set_auto_page_break(auto=True, margin=20)
pdf.add_font("china", "", FONT_PATH, uni=True)
pdf.add_page()

# ============ TITLE PAGE ============
pdf.ln(30)
pdf.set_font("china", "", 28)
pdf.set_text_color(0, 80, 60)
pdf.cell(0, 14, "医疗器械初创企业", align="C")
pdf.ln(16)
pdf.cell(0, 14, "投资与融资指南", align="C")
pdf.ln(24)

pdf.set_draw_color(0, 128, 100)
pdf.set_line_width(1)
pdf.line(70, pdf.get_y(), 140, pdf.get_y())
pdf.ln(14)

pdf.set_font("china", "", 13)
pdf.set_text_color(100, 100, 100)
pdf.cell(0, 8, "条款清单、融资轮次、估值方法", align="C")
pdf.ln(9)
pdf.cell(0, 8, "及510(k)桥梁策略", align="C")
pdf.ln(24)

pdf.set_font("china", "", 11)
pdf.cell(0, 7, "Arch Medical Management", align="C")
pdf.ln(8)
pdf.cell(0, 7, "Pilot Software LLC dba Arch Medical Management", align="C")
pdf.ln(8)
pdf.cell(0, 7, "2026年3月", align="C")

# ============ SECTION 1: FUNDING ROUNDS ============
pdf.add_page()
pdf.section_banner("第一章：融资轮次")
pdf.set_font("china", "", 9)
pdf.set_text_color(80, 80, 80)
pdf.cell(0, 6, "从创意到IPO -- 初创企业融资如何演变")
pdf.ln(8)

pdf.body(
    "初创企业融资按顺序进行多轮，每轮有不同的目的、投资者类型和估值范围。"
    "对于医疗器械公司，监管路径（510(k)、De Novo、PMA）对每轮融资的时间和规模有重大影响。"
)

pdf.sub_title("种子前轮（Pre-Seed）")
pdf.body("最早期阶段。创始人使用个人储蓄、亲友资金或小额补助金来证明概念的可行性。")
pdf.bullet("金额：$25K - $500K（典型范围）")
pdf.bullet("来源：创始人、亲友、大学拨款、SBIR/STTR第一阶段")
pdf.bullet("估值：无或非常早期（产品前、仅概念阶段）")
pdf.bullet("资金用途：概念验证、初始知识产权申请、初步市场调研")
pdf.key_insight("关键洞察：对于医疗器械，种子前轮通常资助初始对比器械研究、可行性原型制作和临时专利申请。此阶段尚无FDA互动。")

pdf.sub_title("种子轮（Seed Round）")
pdf.body("第一轮'正式'融资。您已有可运作的原型或强大的技术数据，需要资金推进监管申报。")
pdf.bullet("金额：$500K - $3M（医疗器械典型范围）")
pdf.bullet("来源：天使投资人、天使团体、微型风投、加速器（Y Combinator、HAX、TMCx）")
pdf.bullet("估值：$2M - $10M 投前估值")
pdf.bullet("资金用途：设计验证测试、Pre-Submission会议（FDA）、台式测试、初步临床数据")
pdf.bullet("结构：SAFE协议、可转换票据或定价股权轮")
pdf.key_insight("关键洞察：这是510(k)器械公司的最佳时机。种子资金覆盖从Pre-Sub到提交申请的过程 -- 这是监管路径中资本效率最高的阶段。")

pdf.sub_title("A轮（Series A）")
pdf.body("第一轮机构风险投资。通常在重大风险降低之后融资 -- 对于医疗科技，这通常意味着FDA许可或提交申请。")
pdf.bullet("金额：$3M - $15M（典型范围）")
pdf.bullet("来源：风险投资公司（医疗科技专注：MedTech Ventures、Gilde Healthcare、Hatteras Venture Partners）")
pdf.bullet("估值：$10M - $40M 投前估值")
pdf.bullet("资金用途：商业化推出、销售团队建设、QMS实施、制造规模扩大")
pdf.bullet("关键条款：领投投资者获得董事会席位，优先股附带保护条款")

pdf.sub_title("B轮及以后（Series B and Beyond）")
pdf.body("成长阶段融资，适用于已证明产品市场契合度和收入增长的公司。")
pdf.bullet("金额：$15M - $50M+（典型范围）")
pdf.bullet("来源：成长阶段风投、战略投资者（J&J Innovation、Medtronic Ventures、GE Healthcare Ventures）")
pdf.bullet("资金用途：销售扩展、国际监管（CE标志、NMPA）、下一代产品开发")

pdf.sub_title("融资轮次总结表")
pdf.tbl_row(["轮次", "金额", "估值", "投资者", "医疗科技里程碑"],
            [30, 30, 30, 40, 55], header=True)
pdf.tbl_row(["种子前", "$25K-500K", "估值前", "亲友、拨款", "概念、IP申请"],
            [30, 30, 30, 40, 55])
pdf.tbl_row(["种子轮", "$500K-3M", "$2-10M投前", "天使、微VC", "Pre-Sub到510(k)申报"],
            [30, 30, 30, 40, 55])
pdf.tbl_row(["A轮", "$3-15M", "$10-40M投前", "VC公司", "FDA许可、上市"],
            [30, 30, 30, 40, 55])
pdf.tbl_row(["B轮", "$15-50M+", "$40-150M+", "成长VC", "规模化、国际市场"],
            [30, 30, 30, 40, 55])

# ============ SECTION 2: TERM SHEETS ============
pdf.add_page()
pdf.section_banner("第二章：条款清单（Term Sheet）")
pdf.set_font("china", "", 9)
pdf.set_text_color(80, 80, 80)
pdf.cell(0, 6, "交易蓝图 -- 每个条款的含义及其重要性")
pdf.ln(8)

pdf.body(
    "条款清单是一份非约束性文件，概述投资的关键财务和治理条款。通常由领投投资者在初步尽职调查后、"
    "最终法律文件起草前发出。可以将其视为投资的'意向书'。"
)

pdf.sub_title("经济条款")
pdf.body("这些条款决定公司的价值以及回报如何分配。")
pdf.bullet("投前估值（Pre-Money Valuation）：新投资资金注入前的公司价值。如果投前估值为$5M，投资者投入$1M，则投后估值为$6M，投资者拥有公司1/6（16.7%）。")
pdf.bullet("投后估值（Post-Money Valuation）：投前 + 新投资 = 投后。您的所有权百分比从投后数字计算。始终以投前估值进行谈判。")
pdf.bullet("每股价格（Price Per Share）：投资者支付的每股价格。计算方式为投前估值除以总流通股数（包括期权池）。")
pdf.bullet("期权池（Option Pool）：为未来员工股票期权预留的股份池（通常占投后的10-20%）。注意：投资者通常坚持期权池从投前估值中扣除，这实际上降低了创始人的真实投前估值。")
pdf.warning_box("警告：期权池调整是最需要理解的重要机制之一。$5M投前估值扣除20%期权池后，对创始人而言实际上是$4M投前估值。务必从两个角度计算稀释效应。")

pdf.sub_title("清算优先权（Liquidation Preference）")
pdf.body("清算优先权决定公司被出售、合并或清算时谁先获得支付（以及多少）。这是除估值外最重要的经济条款。")
pdf.bullet("1倍非参与型（1x Non-Participating）：投资者收回投资金额或转换为普通股按比例分配。这是对创始人最友好的版本。")
pdf.bullet("1倍参与型（1x Participating）：投资者先收回投资金额，然后还按比例分享剩余收益。这是'双重获利' -- 投资者被支付两次。")
pdf.bullet("多倍优先权（Multiple Preferences）：2倍或3倍优先权意味着投资者在普通股东获得任何回报之前，先收回2倍或3倍投资金额。应尽量避免。")
pdf.key_insight("关键洞察示例：投资者以1倍参与型优先股投入$2M获得20%。公司以$10M出售。投资者获得$2M（优先权）+ 剩余$8M的20%（$1.6M）= 总计$3.6M。创始人/普通股获得$6.4M。若为1倍非参与型，在$50M退出时参与型投资者获得$2M + 20%($48M) = $11.6M，而非参与型仅获得$10M。")

pdf.sub_title("反稀释保护（Anti-Dilution Protection）")
pdf.bullet("加权平均（广基）：使用加权平均公式重新计算转换价格，考虑低价轮相对于总股数的规模。这是标准且对创始人更友好的方式。")
pdf.bullet("完全棘轮（Full Ratchet）：转换价格降至新的更低价格 -- 如同投资者以更低估值投资。对创始人非常不利。现代交易中罕见。")

pdf.sub_title("治理与控制条款")
pdf.bullet("董事会席位（Board Seats）：投资者（尤其是A轮领投）通常获得一个董事会席位。常见结构：2名创始人 + 1名投资者 + 1名独立董事 = 4人董事会。警惕投资者获得董事会多数席位。")
pdf.bullet("保护性条款（Protective Provisions）：需要投资者批准的特定行为，无论董事会投票结果如何。典型条款包括：新股发行、公司出售、章程修改、超过阈值的借债、聘用/解雇CEO。")
pdf.bullet("拖带权（Drag-Along Rights）：如果多数投资者希望出售公司，他们可以强制所有股东（包括创始人）同意。通常需要50-67%优先股触发。")
pdf.bullet("按比例权（Pro-Rata Rights）：投资者可以在未来轮次中参与投资以维持其所有权百分比。标准且通常无争议。")

pdf.sub_title("创始人特定条款")
pdf.bullet("创始人股份归属（Founder Vesting）：投资者通常即使创始人已'拥有'股份也要求其受归属约束（通常4年，1年悬崖期）。常见折中：为创始人已投入的时间给予归属学分。")
pdf.bullet("竞业禁止/禁止招揽（Non-Compete / Non-Solicit）：创始人承诺全职工作于公司，且在任职期间及离职后一定时期内不与公司竞争。离职后1-2年为标准；更长则过于激进。")
pdf.bullet("知识产权转让（IP Assignment）：创始人创造的与公司业务相关的所有知识产权转让给公司。必要且不可协商。")
pdf.bullet("优先购买权（ROFR）：防止股东（创始人和投资者）未经公司/董事会批准出售股份。私有公司标准做法。")

pdf.sub_title("条款清单危险信号")
pdf.tbl_row(["危险信号", "为何重要"], [65, 120], header=True)
pdf.tbl_row(["完全棘轮反稀释", "在任何低价轮次中严重惩罚创始人"], [65, 120])
pdf.tbl_row(["参与型优先权 >1倍", "双重获利：投资者收回本金+分享收益"], [65, 120])
pdf.tbl_row(["投资者董事会多数", "创始人失去战略决策控制权"], [65, 120])
pdf.tbl_row(["过多保护性条款", "投资者对日常运营拥有否决权"], [65, 120])
pdf.tbl_row(["排他条款 >60天", "过长时间锁定你不得与其他投资者接触"], [65, 120])
pdf.tbl_row(["累积股息", "投资在创始人获得回报前每年增长8%+"], [65, 120])
pdf.tbl_row(["多倍清算优先权（2倍+）", "投资者在普通股东获得任何回报前收回2-3倍"], [65, 120])

# ============ SECTION 3: VALUATION METHODS ============
pdf.add_page()
pdf.section_banner("第三章：估值方法")
pdf.set_font("china", "", 9)
pdf.set_text_color(80, 80, 80)
pdf.cell(0, 6, "医疗器械初创企业在各阶段的估值方法")
pdf.ln(8)

pdf.body(
    "早期医疗器械公司的估值更多是艺术而非科学。与具有可预测MRR指标的SaaS初创企业不同，"
    "医疗科技估值主要受监管里程碑和临床风险驱动。"
)

pdf.sub_title("收入前估值方法")
pdf.bullet("风险调整市场法：价值 = 器械品类的总可寻址市场(TAM)，根据FDA许可概率、上市时间和竞争进行折扣。$1B TAM、70%许可概率、24个月时间线可在种子轮支持$5-10M投前估值。")
pdf.bullet("可比交易法：与同阶段的类似医疗科技公司进行比较。参考类似510(k)器械公司在种子轮的近期公开数据。根据您的具体适应症和市场规模调整。")
pdf.bullet("收购可比/退出分析：战略收购者会为这项技术支付多少？对于510(k)器械，收购者通常支付3-8倍收入（许可后）或$20-50M+用于已获许可且有初始收入的器械。从退出价值倒推确定合理的进入估值。")
pdf.bullet("VC方法：投资者设定特定回报目标（如7年10倍）。如果预期$100M退出并希望10倍回报，他们将以$10M投后估值投入$1M-$2M，获得10-20%所有权。")

pdf.sub_title("按里程碑的估值阶梯式增长")
pdf.body("医疗器械估值以阶梯形式增长，每个监管里程碑创造一次'估值跳升'：")
pdf.tbl_row(["里程碑", "典型增幅", "投前估值范围", "原因"],
            [40, 35, 40, 70], header=True)
pdf.tbl_row(["概念/专利", "基线", "$1-3M", "创意风险，无FDA接触"],
            [40, 35, 40, 70])
pdf.tbl_row(["Pre-Sub已提交", "+30-50%", "$2-5M", "FDA参与信号"],
            [40, 35, 40, 70])
pdf.tbl_row(["Pre-Sub反馈", "+50-80%", "$4-8M", "监管风险已降低"],
            [40, 35, 40, 70])
pdf.tbl_row(["510(k)已提交", "+100-200%", "$6-15M", "提交 = 拐点"],
            [40, 35, 40, 70])
pdf.tbl_row(["510(k)已获许可", "+200-400%", "$10-30M", "可上市器械"],
            [40, 35, 40, 70])
pdf.tbl_row(["首笔收入", "+300-500%", "$15-50M", "产品市场契合"],
            [40, 35, 40, 70])
pdf.ln(3)
pdf.key_insight("关键洞察：医疗科技中最大的单次估值跃升是从'510(k)已提交'到'510(k)已获许可'。这就是为什么在许可前进行战略融资可为投资者提供最佳回报，并为创始人的股权表提供最有利的进入点。")

# ============ SECTION 4: INVESTMENT VEHICLES ============
pdf.add_page()
pdf.section_banner("第四章：投资工具")
pdf.set_font("china", "", 9)
pdf.set_text_color(80, 80, 80)
pdf.cell(0, 6, "SAFE、可转换票据和定价轮次详解")
pdf.ln(8)

pdf.sub_title("SAFE（未来股权简单协议）")
pdf.body("由Y Combinator创建。SAFE不是债务 -- 它是一份合同，赋予投资者在未来定价轮次中获取股权的权利。无利息，无到期日。")
pdf.bullet("运作方式：投资者以以下两者中较低者获得股权：(a) 估值上限，或 (b) 下一轮价格的折扣")
pdf.bullet("估值上限（Valuation Cap）：SAFE转换的最高估值。例：$5M上限意味着无论A轮估值多高，SAFE投资者均按$5M转换。")
pdf.bullet("折扣率（Discount Rate）：通常15-25%。如果A轮投前估值$10M且SAFE有20%折扣，SAFE投资者按$8M转换。")
pdf.bullet("优点：简单、快速（一份文件）、无利息累积、无到期日压力。种子前和种子轮的标准。")
pdf.bullet("缺点：转换前无投资者权利，稀释不确定直到定价轮，可能堆叠多个SAFE造成'SAFE堆积'问题。")

pdf.sub_title("可转换票据（Convertible Notes）")
pdf.body("可转换票据是转换为股权的短期债务。与SAFE不同，它们产生利息并有到期日。")
pdf.bullet("利率：通常每年4-8%。利息随本金一起转换为股权。")
pdf.bullet("到期日：通常18-24个月。如果到期前未进行定价轮，票据在技术上到期应偿还 -- 可能造成冲突。")
pdf.bullet("转换方式：与SAFE相同：估值上限和/或下一轮定价轮的折扣。")
pdf.bullet("优点：比SAFE更多的投资者保护（是债务）。部分投资者偏好强制转换时间线。")
pdf.bullet("缺点：利息累积消耗您的股权。到期日产生压力。法律上比SAFE更复杂。")
pdf.warning_box("警告：对于医疗器械初创企业，可转换票据可能有风险，因为FDA时间线不可预测。如果您的510(k)审查时间超过预期且票据在定价轮之前到期，您可能面临被迫偿还或不利的重新谈判。")

pdf.sub_title("定价股权轮（优先股）")
pdf.body("定价轮设定具体的估值、每股价格，并创建一类新的优先股，具有明确的权利。这是A轮及以后的标准结构。")
pdf.bullet("关键文件：股份购买协议、投资者权利协议、优先购买权、投票协议、公司章程修订。")
pdf.bullet("法律费用：标准A轮$15K-$50K+法律费用。双方通常各有律师。")
pdf.bullet("优点：清晰的股权表、明确的治理、投资者权利有据可依。机构VC投资的必要条件。")
pdf.bullet("缺点：昂贵、耗时（4-8周完成交割）、需要董事会批准和股东同意。")

pdf.sub_title("投资工具对比表")
pdf.tbl_row(["特征", "SAFE", "可转换票据", "定价轮"],
            [40, 40, 50, 55], header=True)
pdf.tbl_row(["法律费用", "$0-2K", "$2-5K", "$15-50K+"],
            [40, 40, 50, 55])
pdf.tbl_row(["完成时间", "数天", "1-2周", "4-8周"],
            [40, 40, 50, 55])
pdf.tbl_row(["利息", "无", "4-8%/年", "不适用"],
            [40, 40, 50, 55])
pdf.tbl_row(["到期日", "无", "18-24个月", "不适用"],
            [40, 40, 50, 55])
pdf.tbl_row(["估值确定？", "延后", "延后", "是，固定"],
            [40, 40, 50, 55])
pdf.tbl_row(["董事会席位", "否", "有时", "是（领投）"],
            [40, 40, 50, 55])
pdf.tbl_row(["最适合", "种子前/种子", "种子/过桥", "A轮+"],
            [40, 40, 50, 55])

# ============ SECTION 5: INVESTOR TYPES ============
pdf.add_page()
pdf.section_banner("第五章：投资者类型")
pdf.set_font("china", "", 9)
pdf.set_text_color(80, 80, 80)
pdf.cell(0, 6, "谁投资医疗器械以及他们的期望")
pdf.ln(8)

pdf.sub_title("天使投资人（Angel Investors）")
pdf.body("高净值个人使用自有资金投资。通常是前高管、医生或具有行业专业知识的企业家。")
pdf.bullet("投资规模：每笔投资$25K - $250K")
pdf.bullet("阶段：种子前和种子轮")
pdf.bullet("动机：个人经验、导师关系、对创始人的信任。通常以较非正式的条款投资。")
pdf.bullet("注意：可能决策缓慢，后续资金有限，可能不增加战略价值。")

pdf.sub_title("天使团体/辛迪加（Angel Groups / Syndicates）")
pdf.body("有组织的天使团体，汇集资金并共享尽职调查。例如：Oregon Angel Fund、Alliance of Angels、Tech Coast Angels、Life Science Angels。")
pdf.bullet("投资规模：每笔投资$100K - $1M（汇集）")
pdf.bullet("阶段：种子轮")
pdf.bullet("流程：正式路演流程，集体投票，条款比个人天使更结构化。")

pdf.sub_title("风险投资（VC）")
pdf.body("管理有限合伙人（LP）资金池（基金）的专业投资公司。医疗科技专注VC了解FDA时间线和监管风险。")
pdf.bullet("投资规模：每笔投资$1M - $25M+")
pdf.bullet("阶段：A轮及以后（部分做种子轮）")
pdf.bullet("期望：董事会席位、主动治理、后续追加投资、以退出为导向（5-7年视野）")
pdf.bullet("注意：高回报期望（3-5倍基金回报）。会推动增长，有时以牺牲创始人控制权为代价。")

pdf.sub_title("战略投资者（企业VC）")
pdf.body("大型医疗器械公司的投资部门：J&J Innovation、Medtronic Ventures、GE Healthcare Ventures、Philips Health Technology Ventures、Baxter Ventures。")
pdf.bullet("投资规模：每笔投资$2M - $20M")
pdf.bullet("阶段：A-B轮，对高度战略性技术有时做种子轮")
pdf.bullet("优势：获取分销渠道、临床站点、监管专业知识、潜在收购路径。")
pdf.bullet("注意：可能要求技术访问权、收购优先拒绝权或独家许可。可能吓退其他收购方。")
pdf.key_insight("关键洞察：战略投资者是一把双刃剑。Medtronic Ventures的投资意味着验证，但可能阻止J&J或Abbott收购您。在ROFR和信息权方面谨慎谈判。")

pdf.sub_title("政府/非稀释性资金")
pdf.bullet("NIH SBIR/STTR：第一阶段（$275K，6-9个月）用于可行性研究，第二阶段（$1-2M，2年）用于开发。竞争激烈但非稀释性。")
pdf.bullet("NSF SBIR：第一阶段（$200K），第二阶段（$1.1M）。适合双用途医疗技术。")
pdf.bullet("BARDA：用于医疗对策。大额资助（$5-25M），但用途非常特定。")
pdf.bullet("州级计划：Oregon SBIR配套拨款、Oregon Innovation Council、州级风险基金。")
pdf.key_insight("关键洞察：非稀释性资金应始终与股权融资并行追求。SBIR拨款不稀释您的股权表，并且意味着政府对技术的认可。")

# ============ SECTION 6: 510(k) BRIDGE STRATEGY ============
pdf.add_page()
pdf.section_banner("第六章：510(k)桥梁策略")
pdf.set_font("china", "", 9)
pdf.set_text_color(80, 80, 80)
pdf.cell(0, 6, "何时相对于监管里程碑与投资者接触")
pdf.ln(8)

pdf.body(
    "510(k)监管路径创造了自然的拐点，直接影响您的融资杠杆。了解何时相对于每个里程碑与投资者接触，"
    "对于优化估值和条款至关重要。"
)

pdf.sub_title("投资者对接时间线")
pdf.body("并非所有月份对融资都是平等的。以下是映射到标准510(k)时间线的最佳对接节奏：")
pdf.tbl_row(["月份", "里程碑", "信号", "投资者行动", "此时机的原因"],
            [20, 32, 18, 32, 83], header=True)
pdf.tbl_row(["M+0", "Pre-Sub已提交", "预热", "建立关系", "FDA参与证明你是认真的"],
            [20, 32, 18, 32, 83])
pdf.tbl_row(["M+2", "Pre-Sub会议", "活跃", "安排路演", "FDA反馈信是最佳融资资产"],
            [20, 32, 18, 32, 83])
pdf.tbl_row(["M+3", "台式测试", "活跃", "分享数据", "IEC 60601、EMC、可用性数据"],
            [20, 32, 18, 32, 83])
pdf.tbl_row(["M+6", "510(k)已提交", "高峰", "推动条款清单", "提交是拐点 -- 许可只是'时间问题'"],
            [20, 32, 18, 32, 83])
pdf.tbl_row(["M+9", "510(k)已获许可", "收尾", "完成融资轮", "最大杠杆 -- 已获许可、可上市"],
            [20, 32, 18, 32, 83])
pdf.ln(4)

pdf.sub_title("为什么M+2到M+6是最佳窗口期")
pdf.body("在FDA Pre-Submission会议反馈（M+2）和510(k)提交（M+6）之间的时期，是最佳融资窗口，原因有三：")
pdf.bullet("1. 监管风险降低：FDA反馈信是有形的第三方验证，证明您的监管策略是合理的。这是您能向投资者展示的最具说服力的文件。")
pdf.bullet("2. 有利估值：在许可前，您的估值仍处于'事件前'水平。在510(k)获许可前进入的投资者获得许可前价格 -- 通常比许可后低40-60%。这是他们购买的回报。")
pdf.bullet("3. 可见的终点线：在M+6提交510(k)时，您距离许可还有90天（标准审查）。足够接近让投资者看到终点，但又足够早以获得许可前条款。")
pdf.key_insight("关键洞察：医疗科技创始人犯的第一大错误是等到许可后才融资。许可后融资给您更好的条款，但会消耗6-12个月的商业化跑道。您需要用于上市的资金应在许可函到达前已承诺到位。")

pdf.sub_title("各阶段投资者希望看到的内容")
pdf.body("您的路演材料应随着监管时间线的推进而演变：")
pdf.bullet("M+0（Pre-Sub已提交）：愿景 + 技术方案、IP格局、团队资历、TAM/SAM分析。Pre-Sub提交展示FDA参与。")
pdf.bullet("M+2（Pre-Sub会议）：以上全部 + FDA反馈信（'风险降低文件'）、经FDA同意的拟议测试方案、带对比器械比较的竞争格局。")
pdf.bullet("M+3（台式测试）：以上全部 + IEC 60601测试报告、EMC数据、临床验证方案/初步结果、设计冻结文档。")
pdf.bullet("M+6（510(k)已提交）：以上全部 + 完整510(k)提交摘要、许可时间线（90天）、上市计划、收入预测、首批KOL承诺。")
pdf.bullet("M+9（已获许可）：以上全部 + 许可函、K编号、上市后计划、商业化进展、首批采购订单或意向书。")

# ============ SECTION 7: INVESTOR DUE DILIGENCE ============
pdf.add_page()
pdf.section_banner("第七章：投资者尽职调查")
pdf.set_font("china", "", 9)
pdf.set_text_color(80, 80, 80)
pdf.cell(0, 6, "投资者在出资前调查什么")
pdf.ln(8)

pdf.body(
    "尽职调查（'DD'）是投资者在最终完成投资前进行的调查过程。"
    "对于医疗器械，DD比典型的科技初创企业更为严格，因为存在监管、临床和制造风险。"
)

pdf.sub_title("技术/产品尽职调查")
pdf.bullet("产品成熟度：可运作原型还是概念？设计冻结状态？验证和确认测试是否完成？")
pdf.bullet("知识产权组合：专利（已申请 vs. 已授权）、商业秘密、自由运营分析。是否已进行FTO检索？")
pdf.bullet("监管状态：是否已获许可/批准？什么路径？FDA在Pre-Sub中说了什么？已知问题？")
pdf.bullet("制造：物料清单、代工厂是否已确定？能否规模化制造？成本（COGS）是多少？")

pdf.sub_title("市场尽职调查")
pdf.bullet("市场规模：具有可信自下而上分析的总可寻址市场，而非仅自上而下的TAM数字。")
pdf.bullet("报销：报销路径（CPT代码、医院预算 vs. 医生偏好项目）、支付意愿。")
pdf.bullet("竞争：现有器械、新兴竞争者、进入壁垒分析。")
pdf.bullet("临床拥护者：临床医生和医院兴趣、意向书、关键意见领袖（KOL）关系。")

pdf.sub_title("团队尽职调查")
pdf.bullet("领域专业知识：监管事务经验、以往FDA申报、临床/工程深度。")
pdf.bullet("创始人承诺：全职承诺、股份归属计划、创始人协议是否到位。")
pdf.bullet("团队缺口：需要的关键招聘、顾问委员会构成、专业知识缺口。")

pdf.sub_title("财务尽职调查")
pdf.bullet("股权表：现有股权表、以往投资、未结算的SAFE/票据。")
pdf.bullet("燃烧率与跑道：月度燃烧率、当前支出下的跑道、本轮资金使用的详细计划。")
pdf.bullet("财务预测：收入模型、定价策略、盈利路径、单位经济学。")

pdf.sub_title("法律尽职调查")
pdf.bullet("公司架构：清晰的公司结构、无未决诉讼、合规的实体设立。")
pdf.bullet("知识产权所有权：IP转让协议、员工发明协议、NDA/NCA义务。")
pdf.bullet("监管合规：QMS是否到位（ISO 13485）、投诉处理、MDR报告程序。")

# ============ SECTION 8: NEGOTIATION STRATEGY ============
pdf.add_page()
pdf.section_banner("第八章：谈判策略")
pdf.set_font("china", "", 9)
pdf.set_text_color(80, 80, 80)
pdf.cell(0, 6, "医疗器械创始人的实用策略")
pdf.ln(8)

pdf.sub_title("谈判之前")
pdf.bullet("制造竞争：同时与15-25位投资者交流。竞争创造杠杆。永远不要只与一个感兴趣的方谈判。")
pdf.bullet("了解您的投资者：研究投资者的投资组合、基金规模和近期交易。$50M基金开出$1M支票与$500M基金的行为方式不同。")
pdf.bullet("了解您的BATNA：清楚您的BATNA（谈判替代方案的最佳选择）。如果这笔交易失败会怎样？选项越多 = 权力越大。")

pdf.sub_title("关键谈判要点（按优先级排列）")
pdf.body("并非所有条款同等重要。将谈判精力集中在最重要的条款上：")
pdf.bullet("1. 估值（最高优先级）：这直接决定您的所有权。在此处全力争取。")
pdf.bullet("2. 清算优先权：1倍非参与型是标准。对参与型优先股或>1倍的倍数强力推回。")
pdf.bullet("3. 董事会构成：保持对创始人友好的董事会构成。2名创始人 + 1名投资者 + 1名独立董事最为理想。")
pdf.bullet("4. 反稀释：坚持广基加权平均。拒绝完全棘轮。")
pdf.bullet("5. 期权池：确保期权池大小合适，但争取从投后估值而非投前估值中扣除。")
pdf.bullet("6. 按比例权（较低优先级）：标准且不值得争论。接受合理的保护性条款。")

pdf.sub_title("常见错误")
pdf.bullet("先亮最好的牌：第一个看到您交易的投资者不应是您的首选领投。先与低优先级投资者练习路演。")
pdf.bullet("启动太晚：医疗科技融资需要3-6个月。尽早开始，特别是在监管里程碑前后。")
pdf.bullet("跳过法律顾问：聘请有初创企业经验的法律顾问（不是您的家庭律师）。Wilson Sonsini、Cooley、Fenwick -- 或当地同等事务所。")
pdf.bullet("过度强调收入预测：在医疗科技中，可信的510(k)时间线比曲棍球棒式的收入预测更有说服力。以监管进展为先导。")
pdf.key_insight("关键洞察：最佳融资状态是您并不急需资金。在还剩6个月以上跑道时开始融资。从急需资金的立场谈判总是导致更差的条款。")

# ============ SECTION 9: CAP TABLE MANAGEMENT ============
pdf.add_page()
pdf.section_banner("第九章：股权表管理")
pdf.set_font("china", "", 9)
pdf.set_text_color(80, 80, 80)
pdf.cell(0, 6, "理解多轮融资中的所有权稀释")
pdf.ln(8)

pdf.body(
    "您的资本化表（'股权表'）追踪谁拥有公司的多少百分比。"
    "了解它如何演变对于做出明智的融资决策至关重要。"
)

pdf.sub_title("示例：510(k)医疗器械初创企业股权表演变")
pdf.body("起点：两位联合创始人，50/50分配，1000万授权股数。")
pdf.tbl_row(["股东", "创始时", "种子轮后", "A轮后", "说明"],
            [30, 28, 28, 28, 71], header=True)
pdf.tbl_row(["创始人A", "50.0%", "37.5%", "28.1%", "CEO - 完全归属"],
            [30, 28, 28, 28, 71])
pdf.tbl_row(["创始人B", "50.0%", "37.5%", "28.1%", "CTO - 完全归属"],
            [30, 28, 28, 28, 71])
pdf.tbl_row(["种子投资者", "--", "15.0%", "11.3%", "SAFE, $1M @ $6M上限"],
            [30, 28, 28, 28, 71])
pdf.tbl_row(["期权池", "--", "10.0%", "12.5%", "A轮时刷新"],
            [30, 28, 28, 28, 71])
pdf.tbl_row(["A轮领投", "--", "--", "20.0%", "$3M @ $12M投前"],
            [30, 28, 28, 28, 71])
pdf.tbl_row(["合计", "100%", "100%", "100%", ""],
            [30, 28, 28, 28, 71])
pdf.ln(4)

pdf.body("关键观察：")
pdf.bullet("稀释是预期中的：创始人从100%降至两轮后合计56.2%。这是正常且健康的。")
pdf.bullet("稀释不是损失：$15M公司的56.2%（$8.4M）好过$2M公司的100%。")
pdf.bullet("每轮稀释所有人：每轮按比例稀释所有现有股东（除非他们行使按比例权）。")
pdf.key_insight("关键洞察：一个有用的心理模型：种子轮后保持40-60%、A轮后保持25-40%的创始人处于强势地位。如果在B轮前合计低于20%，您可能过早放弃了太多。")

# ============ SECTION 10: GLOSSARY ============
pdf.add_page()
pdf.section_banner("第十章：术语表")
pdf.set_font("china", "", 9)
pdf.set_text_color(80, 80, 80)
pdf.cell(0, 6, "必备投资术语")
pdf.ln(8)

glossary = [
    ("Anti-Dilution（反稀释）", "保护投资者免受未来低估值轮次影响。调整转换价格。"),
    ("BATNA（最佳替代方案）", "谈判替代方案的最佳选择。交易失败时的后备方案。"),
    ("Bridge Round（过桥轮）", "主要轮次之间的小额融资，通常使用可转换票据。"),
    ("Burn Rate（燃烧率）", "月度现金支出。总燃烧 = 总支出。净燃烧 = 支出减去收入。"),
    ("Cap Table（股权表）", "显示所有股权所有权、期权、认股权证和可转换工具的资本化表。"),
    ("Cliff（悬崖期）", "任何股份归属前的最短时间（通常1年）。"),
    ("Convertible Note（可转换票据）", "在未来定价轮中转换为股权的短期债务。"),
    ("Down Round（低价轮）", "估值低于前一轮的融资轮次。"),
    ("Drag-Along（拖带权）", "允许多数股东强制少数股东参与出售的权利。"),
    ("Due Diligence（尽职调查）", "投资者在最终投资前进行的调查。"),
    ("Equity（股权）", "公司所有权，以股份形式体现。"),
    ("Exit（退出）", "流动性事件：收购、IPO或二级销售。"),
    ("Fully Diluted（完全稀释）", "计入所有期权、认股权证和可转换工具（如已行使）的总股数。"),
    ("Lead Investor（领投投资者）", "设定条款、进行主要DD并通常获得董事会席位的投资者。"),
    ("Liquidation Preference（清算优先权）", "在出售或清算中向股东支付的顺序和金额。"),
    ("Lock-Up Period（锁定期）", "IPO后内部人不得出售股份的时期（通常180天）。"),
    ("Non-Dilutive（非稀释性）", "不放弃股权的资金（拨款、收入）。"),
    ("Option Pool（期权池）", "为未来员工股权授予预留的股份。"),
    ("Pari Passu（平等待遇）", "同类投资者平等分享收益。"),
    ("Post-Money（投后估值）", "包含新投资的公司估值。"),
    ("Pre-Money（投前估值）", "新投资前的公司估值。"),
    ("Preferred Stock（优先股）", "相对于普通股拥有额外权利（清算优先权、反稀释等）的股票类别。"),
    ("Pro-Rata Right（按比例权）", "在未来轮次中投资以维持所有权百分比的权利。"),
    ("ROFR（优先拒绝权）", "公司可以匹配任何外部股份报价。"),
    ("Runway（跑道）", "按当前燃烧率可运营的剩余月数。"),
    ("SAFE（未来股权简单协议）", "在未来定价轮中转换为股票的协议。"),
    ("Secondary Sale（二级销售）", "股东之间的现有股份（非新发行）销售。"),
    ("Tag-Along（跟随权）", "少数股东以相同条款参与出售的权利。"),
    ("Term Sheet（条款清单）", "关键投资条款的非约束性概述。"),
    ("Vesting（归属）", "随时间逐步获得股权（员工/创始人通常4年）。"),
]

for term, defn in glossary:
    pdf.bullet(f"{term}：{defn}")

# ============ CLOSING ============
pdf.ln(10)
pdf.set_draw_color(0, 128, 100)
pdf.set_line_width(0.5)
pdf.line(10, pdf.get_y(), 200, pdf.get_y())
pdf.ln(6)
pdf.set_font("china", "", 9)
pdf.set_text_color(100, 100, 100)
pdf.multi_cell(0, 5,
    "本指南由Arch Medical Management（Pilot Software LLC dba Arch Medical Management）于2026年3月编制。"
    "内容仅供参考，不构成法律、财务或监管建议。请咨询合格的专业人士以获取具体指导。"
)

output_path = "/Users/londailey/Control-Tower/Investment_Fundraising_Guide_CN.pdf"
pdf.output(output_path)
print(f"PDF generated: {output_path}")
