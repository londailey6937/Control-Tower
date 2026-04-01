#!/usr/bin/env python3
"""
Generate Chinese translation of the EB-5 proposal letter to Lawrence Liu.
510kBridge EB-5 投资提案 -- 中文版
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
        self.cell(0, 5, f"第 {self.page_no()} 页 / 共 {{nb}} 页", align="C")

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
    pdf = LetterPDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.set_margins(22, 18, 22)

    # ── PAGE 1: LETTERHEAD ────────────────────────
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
    pdf.ln(8)

    today = date.today().strftime("%Y年%m月%d日")
    pdf.set_font("ARUNI", "", 10)
    pdf.set_text_color(*TEXT)
    pdf.cell(0, 5, today, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(8)

    # ── THE LETTER ────────────────────────────────
    pdf.txt("宗刚你好，")

    pdf.txt(
        "我觉得我现在更了解你的情况和需求了。如果你最关心的是Danielle、Malei和Claire，"
        "那就投资在家人身上。"
    )

    pdf.txt(
        "在搭建Control Tower并对FDA提交流程做了大量研究之后，我看到了一个对我们两个"
        "家庭都有益的机会。我还没有和任何人讨论过这个想法，但我可以想象通过EB-5项目"
        "成立一家公司，活跃的公司成员持有股份，薪酬来自客户服务收入。"
    )

    pdf.txt(
        "我们将拥有一支由受过教育、经验丰富的家庭成员组成的强大团队。"
        "让我告诉你我的想法："
    )

    # ── OUR TEAM ──────────────────────────────────
    pdf.sec("我们的团队")

    pdf.bold_bullet("李佳伦 -- 客户服务总监：",
        "佳伦在公司做内容主管和高级医学编辑，表现非常出色。他参与医学内容策划、"
        "患者教育内容创作和质量管控。他认识很多中国和欧洲的医学专家——他经常出差参加"
        "学术研讨会并发表演讲。他是一个优秀的销售人才，希望有一天能领导自己的公司。"
        "这可以是他的发展路径。")

    pdf.bold_bullet("Chensy Li -- 高级客户经理：",
        "Chensy是佳伦的妻子，拥有英国研究生学位和丰富的营销经验。她可以帮助我们"
        "开拓客户来源。她目前在上海一家西方公司担任高级客户经理，负责管理项目和客户。"
        "她知道如何拓展业务。")

    pdf.bold_bullet("刘小鸟 (Danielle) -- 财务会计：",
        "Danielle将负责公司财务会计工作。她在加州大学圣芭芭拉分校（UCSB）获得的"
        "会计硕士学位正是我们所需要的——真正的专业资质承担真正的责任。")

    pdf.bold_bullet("Malei 和 Jessica：",
        "经过一些定向培训后，我们可以为Malei和Jessica找到合适的岗位。Jessica已经"
        "主动联系我提出了她自己的商业想法，这说明她有创业精神。这种主动性正是初创"
        "公司所需要的。")

    pdf.bold_bullet("刘宗刚 (Lawrence) -- CEO：",
        "你的头衔是CEO。这不需要你向公司进行财务投资，但你将持有优先股。你在中国"
        "的商业人脉就是客户来源。你已经认识那些需要这项服务的人。")

    pdf.bold_bullet("Lon Dailey -- 创始人兼首席顾问：",
        "我负责所有美国监管、法律和运营事务。PMP认证，14年美国受监管产品开发企业"
        "经验，有510(k)提交经验。我是你的美国合伙人——你专注于你最擅长的领域，"
        "我来处理你说让你不安的那部分。")

    # ── THE OPPORTUNITY ───────────────────────────
    pdf.sec("商业机会")

    pdf.txt(
        "510kBridge帮助中国医疗器械公司获得FDA 510(k)许可，以便在美国市场销售。"
        "我们使用我搭建的Control Tower平台为客户管理整个流程。每年有数百家中国公司"
        "需要这项服务，而且美国医疗器械市场规模巨大。"
    )

    pdf.txt(
        "自从我们上次交谈以来，我已经搭建了一个四产品技术套件：\n\n"
        "  Control Tower -- 17个选项卡的项目管理中枢仪表板，管理从双轨里程碑"
        "到FDA提交的整个510(k)流程。\n"
        "  Predicate Finder -- FDA数据库搜索工具（嵌入Control Tower，"
        "也可作为独立免费工具使用），帮助识别先导器械用于实质等效性论证。\n"
        "  QMS-Lite -- 专为510(k)阶段初创企业设计的轻量级质量管理系统，"
        "无需承担Greenlight Guru等企业级QMS平台的高昂费用。\n"
        "  Entity Setup Tracker -- 帮助中国公司设立美国实体（特拉华州C-Corp、"
        "EIN、注册代理人、银行账户），提供逐步跟踪。\n\n"
        "每个产品都能产生持续的SaaS订阅收入，并将客户引导到更高的服务层级。"
        "仅Predicate Finder本身就是一个强大的获客引擎——"
        "客户从免费搜索开始，在看到价值后自然升级。"
    )

    pdf.txt(
        "我还想让你考虑一个额外的好处：当我们接收寻求FDA许可的客户时，你可以浏览"
        "客户名单，看看是否有你感兴趣的更好估值项目。不用被锁定在一家你对价格不满意"
        "的公司里，你将有机会近距离评估处于不同阶段的多家公司——按照你的条件，"
        "投资你认为合适的项目。"
    )

    pdf.txt(
        "你投资的是你的家人，而不是别人的公司。"
    )

    # ── WHY CAMAS ─────────────────────────────────
    pdf.sec("为什么选择Camas, Washington")

    pdf.txt(
        "Camas就在波特兰河对岸——离机场只有20分钟车程。它符合目标就业区（TEA）条件，"
        "这意味着EB-5投资门槛是$800,000而不是$1,050,000。"
    )

    pdf.txt(
        "我建议你卖掉现在的房子，在Camas买新房。那里有很漂亮的房子——我看到一套"
        "挂牌价$2M的在售房屋。你现在的房子可以卖到$800K以上，差价可以让你在公司"
        "注册所在的TEA地区住上更好的房子。全家人会住得很近，离机场很近，"
        "社区环境也非常好。"
    )

    # ── JIALUN & CHENSY ───────────────────────────
    pdf.sec("佳伦和Chensy")

    pdf.txt(
        "如果你对这个方案有兴趣，我会跟佳伦和Chensy聊聊，看看他们怎么想。他们本来"
        "就计划将来搬到美国来。我觉得他们希望对自己的生活有更多掌控，拥有自己的事业"
        "会很适合他们。这可能是促使他们提前行动的机会。"
    )

    # ── CLIENT FEES AND COMPENSATION ──────────────
    pdf.sec("客户费用模式")

    pdf.txt(
        "我们的收入来自我们服务的公司。以下是典型的客户合作模式和资金流向："
    )

    pdf.sub("服务层级")
    pdf.table(
        ["层级", "服务内容", "月费"],
        [
            ["Predicate Finder Pro", "无限搜索、链追溯、SE论证草稿", "$99"],
            ["QMS-Lite", "FDA审计就绪的质量管理系统", "$200-$500"],
            ["入门版", "Control Tower SaaS + Entity Setup Tracker", "$500-$2,000"],
            ["专业版", "全程项目管理，审批管理和提交", "$10,000-$25,000"],
            ["企业版", "端到端：监管+项目管理+供应商+实体设立", "$50,000+/项目"],
        ],
        [40, 75, 45]
    )

    pdf.txt(
        "收入来自多个渠道。SaaS订阅（Predicate Finder Pro、QMS-Lite、入门版仪表板）"
        "提供可预测的每月经常性收入。专业版和企业版客户每月带来$10K-$50K+。"
        "一个专业版客户每月$15,000，年收入$180,000。SaaS订阅加上3-5个专业版客户，"
        "公司年收入可达$500K-$900K。"
    )

    pdf.sub("费用用途")
    pdf.table(
        ["类别", "收入占比", "用途"],
        [
            ["薪酬福利", "45-50%", "团队薪资（每个人都有工资）"],
            ["运营", "15-20%", "办公、法律、保险、软件工具"],
            ["业务拓展", "10-15%", "营销、差旅、客户开发"],
            ["技术", "5-10%", "Control Tower平台维护和升级"],
            ["股东分红", "15-20%", "利润分配给股东"],
        ],
        [35, 30, 95]
    )

    pdf.txt(
        "关键点：客户费用优先支付薪酬。Danielle、佳伦、Chensy和其他所有人都从"
        "运营中获得实际工资。此外，随着公司盈利，股东将获得分红。这不是投机——"
        "这是一个服务型企业，从第一个客户开始就有收入。"
    )

    pdf.sub("示例：第二年，SaaS + 5个活跃项目管理客户")
    pdf.table(
        ["项目", "年度金额"],
        [
            ["SaaS收入（PF Pro + QMS + 入门版）", "$120,000"],
            ["项目管理收入（5个客户 x 月均$15K）", "$900,000"],
            ["总收入", "$1,020,000"],
            ["薪酬福利（50%）", "$510,000"],
            ["运营（15%）", "$153,000"],
            ["业务拓展（10%）", "$102,000"],
            ["技术（5%）", "$51,000"],
            ["股东分红（20%）", "$204,000"],
        ],
        [95, 65]
    )

    pdf.txt(
        "5个项目管理客户加上SaaS订阅用户，公司可以支撑整个团队有竞争力的薪酬，"
        "并向股东分配超过$200,000。随着第3-5年客户增加，薪资和分红都会增长。"
    )

    # ── EB-5 BASICS ──────────────────────────────
    pdf.sec("EB-5项目运作方式")

    pdf.txt(
        "EB-5投资移民项目为投资美国创造就业岗位的企业的外国投资者提供获得美国"
        "永久居留权（绿卡）的途径。以下是基本要点："
    )

    pdf.bold_bullet("投资金额：", "目标就业区（TEA）$800,000，或标准地区$1,050,000。"
                    "华盛顿州Camas符合TEA条件——它位于波特兰都会区MSA边界之外，"
                    "且在人口普查区层面达到高失业率门槛。")
    pdf.bold_bullet("创造就业：", "企业必须为每位投资者创造至少10个全职美国就业岗位")
    pdf.bold_bullet("时间线：", "有条件绿卡（2年），然后提交I-829申请解除条件，"
                    "获得永久居留权")
    pdf.bold_bullet("风险投资：", "资金必须真实投入企业运营（不是保本回报）")

    pdf.txt(
        "510kBridge将注册在华盛顿州Camas——一个符合条件的目标就业区（TEA），"
        "可享受降低至$800,000的投资门槛。我们的招聘计划在前2-3年将创造13个以上"
        "全职岗位——远超10个岗位的要求。而且EB-5投资直接进入一家Danielle和家人"
        "每天都在工作的运营公司，这不仅仅是纸面上的投资。"
    )

    # ── JOB CREATION ─────────────────────────────
    pdf.sub("计划岗位（第1-3年）")
    pdf.table(
        ["职位", "时间", "类型"],
        [
            ["CEO（刘宗刚）", "现有", "全职"],
            ["首席顾问（Lon Dailey, PMP）", "现有", "全职"],
            ["客户服务总监（李佳伦）", "现有", "全职"],
            ["高级客户经理（Chensy Li）", "现有", "全职"],
            ["财务会计（刘小鸟）", "现有", "全职"],
            ["法规专员", "第1年", "全职"],
            ["业务拓展代表", "第1年", "全职"],
            ["营销/微信运营专员", "第1年", "全职"],
            ["行政主管", "第1年", "全职"],
            ["项目经理", "第2年", "全职"],
            ["法规专员 #2", "第2年", "全职"],
            ["临床事务经理", "第2年", "全职"],
            ["财务总监 / CFO", "第2-3年", "全职"],
        ],
        [80, 40, 40]
    )

    # ── SIDE-BY-SIDE ─────────────────────────────
    pdf.sec("为什么这不一样")

    pdf.table(
        ["因素", "510kBridge (EB-5)", "外部投资"],
        [
            ["你的角色", "CEO", "少数股东"],
            ["家人的角色", "Danielle, Jessica, Malei", "没有保障"],
            ["所需资金", "$800K (Camas TEA)", "$1M+ 固定估值"],
            ["估值", "从零开始你自己建", "由别人预设"],
            ["控制权", "完全——你是CEO", "有限，让你不安"],
            ["技术IP", "4产品套件（CT、PF、QMS、EST）", "无"],
            ["美国运营", "Lon负责", "你自己摸索"],
            ["收入开始", "第一个客户（第1年）", "18-23个月（等FDA）"],
            ["风险", "多客户组合", "押注单一产品"],
            ["绿卡", "是（EB-5）", "没有"],
            ["客户投资机会", "浏览所有估值", "锁定一家公司"],
        ],
        [38, 60, 62]
    )

    # ── CLOSING ─────────────────────────────────
    pdf.ln(4)
    pdf.txt("随时聊，")
    pdf.ln(6)
    pdf.set_font("ARUNI", "", 10)
    pdf.set_text_color(*TEXT)
    pdf.cell(0, 5, "Lon", new_x="LMARGIN", new_y="NEXT")

    # ── DISCLAIMER ──────────────────────────────
    pdf.ln(10)
    pdf.set_draw_color(*GRAY)
    pdf.set_line_width(0.3)
    pdf.line(pdf.l_margin, pdf.get_y(), pdf.w - pdf.r_margin, pdf.get_y())
    pdf.ln(3)
    pdf.set_font("ARUNI", "I", 7.5)
    pdf.set_text_color(*GRAY)
    pdf.multi_cell(0, 4,
        "本函仅供讨论之用，不构成法律、税务或移民建议。EB-5资格须由合格的移民律师确认。"
        "财务预测为估算值，不构成保证。",
        new_x="LMARGIN", new_y="NEXT")

    # ── SAVE ────────────────────────────────────
    out = os.path.join(OUT_DIR, "510kBridge_EB5_Proposal_CN.pdf")
    pdf.output(out)
    sz = os.path.getsize(out)
    print(f"Created {out}  ({sz:,} bytes, {pdf.pages_count} pages)")


if __name__ == "__main__":
    build()
