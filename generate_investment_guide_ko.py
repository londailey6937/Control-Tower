#!/usr/bin/env python3
"""
Generate a comprehensive Investment & Fundraising Guide PDF (Korean)
for medical device startups navigating the 510(k) pathway.
Covers term sheets, funding rounds, investor types, and timing.
"""

import os
from fpdf import FPDF

OUT = os.path.dirname(os.path.abspath(__file__))
CJK_FONT = "/Library/Fonts/Arial Unicode.ttf"

_MAP = str.maketrans({
    "\u2014": "--", "\u2013": "-", "\u2019": "'", "\u201c": '"', "\u201d": '"',
    "\u2018": "'", "\u2265": ">=", "\u2264": "<=", "\u00b5": "u", "\u00d7": "x",
    "\u2022": "-", "\u2026": "...", "\u00ae": "(R)", "\u2192": "->",
})
def _a(s):
    return s.translate(_MAP)


class GuidePDF(FPDF):
    CARDINAL = (20, 60, 120)
    DARK = (35, 35, 40)
    GRAY = (110, 110, 120)
    ACCENT = (0, 98, 71)
    WHITE = (255, 255, 255)
    LIGHT_BG = (248, 248, 252)
    WARN_BG = (255, 248, 240)
    WARN_BORDER = (200, 120, 20)
    SCENARIO_BG = (235, 238, 255)
    SCENARIO_BORDER = (60, 60, 180)

    def __init__(self):
        super().__init__(orientation="P", unit="mm", format="Letter")
        self.add_font("CJK", "", CJK_FONT)
        self.add_font("CJK", "B", CJK_FONT)
        self.add_font("CJK", "I", CJK_FONT)

    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("CJK", "I", 7)
        self.set_text_color(*self.GRAY)
        self.cell(0, 4, _a("의료기기 스타트업 투자 가이드  |  텀시트, 라운드 & 자금조달 전략"), align="R")
        self.ln(5)

    def footer(self):
        self.set_y(-12)
        self.set_font("CJK", "I", 7)
        self.set_text_color(*self.GRAY)
        self.cell(0, 4, f"{self.page_no()}/{{nb}} 페이지", align="C")

    def section_heading(self, num, title, subtitle=""):
        self.add_page()
        self.set_fill_color(*self.CARDINAL)
        self.rect(self.l_margin, self.get_y(), self.w - self.l_margin - self.r_margin, 14, style="F")
        self.set_font("CJK", "B", 14)
        self.set_text_color(*self.WHITE)
        self.set_x(self.l_margin + 4)
        self.cell(0, 14, _a(f"섹션 {num}:  {title}"))
        self.ln(16)
        if subtitle:
            self.set_font("CJK", "I", 9)
            self.set_text_color(*self.GRAY)
            self.cell(0, 5, _a(subtitle), new_x="LMARGIN", new_y="NEXT")
            self.ln(2)

    def sub_heading(self, text):
        page_body_bottom = self.h - self.b_margin
        if self.get_y() > (page_body_bottom - 30):
            self.add_page()
        self.ln(2)
        self.set_font("CJK", "B", 11)
        self.set_text_color(*self.ACCENT)
        self.cell(0, 6, _a(text), new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(*self.ACCENT)
        self.set_line_width(0.3)
        self.line(self.l_margin, self.get_y(), self.l_margin + 60, self.get_y())
        self.ln(2)

    def body(self, text):
        self.set_font("CJK", "", 10)
        self.set_text_color(*self.DARK)
        self.multi_cell(0, 5.2, _a(text), align="L")
        self.ln(2)

    def bullet(self, text, bold_prefix=""):
        self.set_font("CJK", "", 10)
        self.set_text_color(*self.DARK)
        self.cell(6, 5.2, _a("-"))
        if bold_prefix:
            self.set_font("CJK", "B", 10)
            self.cell(self.get_string_width(_a(bold_prefix)) + 1, 5.2, _a(bold_prefix))
            self.set_font("CJK", "", 10)
        self.multi_cell(0, 5.2, _a(text), align="L")
        self.ln(0.5)

    def callout_box(self, text, style="key"):
        if style == "warn":
            self.set_fill_color(*self.WARN_BG)
            self.set_draw_color(*self.WARN_BORDER)
            self.set_text_color(160, 90, 0)
            prefix = "경고:  "
        elif style == "scenario":
            self.set_fill_color(*self.SCENARIO_BG)
            self.set_draw_color(*self.SCENARIO_BORDER)
            self.set_text_color(40, 40, 150)
            prefix = "시나리오:  "
        else:
            self.set_fill_color(240, 250, 245)
            self.set_draw_color(*self.ACCENT)
            self.set_text_color(*self.ACCENT)
            prefix = "핵심 인사이트:  "
        self.set_line_width(0.5)
        if self.get_y() > self.page_break_trigger - 35:
            self.add_page()
        x = self.l_margin + 2
        y = self.get_y()
        page_before = self.page
        self.set_xy(x + 3, y + 2)
        self.set_font("CJK", "B", 9)
        self.cell(self.get_string_width(_a(prefix)) + 1, 5, _a(prefix))
        self.set_font("CJK", "", 9)
        box_w = self.w - self.l_margin - self.r_margin - 7
        text_w = box_w - self.get_string_width(_a(prefix)) - 1
        self.multi_cell(text_w, 5, _a(text), align="L")
        if self.page == page_before:
            h = self.get_y() - y + 2
            self.rect(x, y, box_w + 3, h, style="D")
        self.ln(4)

    def table_row(self, cells, widths, bold_first=False, header=False):
        h = 6.5
        if header:
            self.set_font("CJK", "B", 9)
            self.set_fill_color(*self.CARDINAL)
            self.set_text_color(*self.WHITE)
            for i, cell in enumerate(cells):
                self.cell(widths[i], h, _a(cell), border=1, fill=True, align="C")
            self.ln()
            return
        self.set_text_color(*self.DARK)
        for i, cell in enumerate(cells):
            if i == 0 and bold_first:
                self.set_font("CJK", "B", 9)
            else:
                self.set_font("CJK", "", 9)
            self.cell(widths[i], h, _a(cell), border=1)
        self.ln()


def build():
    pdf = GuidePDF()
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.alias_nb_pages()

    # ── 표지 ──────────────────────────────────────
    pdf.add_page()
    pdf.ln(35)
    pdf.set_font("CJK", "B", 28)
    pdf.set_text_color(*GuidePDF.CARDINAL)
    pdf.cell(0, 12, _a("의료기기 스타트업을 위한"), align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 12, _a("투자 및 자금조달"), align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 12, _a("가이드"), align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(8)
    pdf.set_draw_color(*GuidePDF.CARDINAL)
    pdf.set_line_width(0.8)
    pdf.line(60, pdf.get_y(), 155, pdf.get_y())
    pdf.ln(8)
    pdf.set_font("CJK", "", 13)
    pdf.set_text_color(*GuidePDF.GRAY)
    pdf.cell(0, 7, _a("텀시트, 투자 라운드, 기업가치 평가,"), align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 7, _a("그리고 510(k) Bridge 전략"), align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(30)
    pdf.set_font("CJK", "", 10)
    pdf.set_text_color(*GuidePDF.DARK)
    pdf.cell(0, 6, _a("510k Bridge"), align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 6, _a("510k Bridge, Inc."), align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 6, _a("2026년 3월"), align="C", new_x="LMARGIN", new_y="NEXT")

    # ── 섹션 1: 투자 라운드 ──────────────────────
    pdf.section_heading(1, "투자 라운드", "아이디어에서 IPO까지 스타트업 자금조달의 진화")

    pdf.body("스타트업 자금조달은 순차적인 '라운드'로 이루어지며, 각 라운드는 고유한 목적, 투자자 유형, 일반적인 기업가치 범위를 가집니다. 의료기기 기업의 경우 규제 경로(510(k), De Novo, PMA)가 각 라운드의 시기와 규모에 큰 영향을 미칩니다.")

    pdf.sub_heading("프리시드(Pre-Seed)")
    pdf.body("가장 초기 단계입니다. 창업자가 개인 자금, 지인 투자, 소규모 보조금으로 사업 개념의 타당성을 입증합니다.")
    pdf.bullet("일반적으로 $25K - $500K", "금액: ")
    pdf.bullet("창업자, 지인, 대학 보조금, SBIR/STTR Phase I", "자금원: ")
    pdf.bullet("없음 또는 매우 초기 (제품 이전, 개념 단계)", "기업가치: ")
    pdf.bullet("개념 증명, 초기 IP 출원, 예비 시장 조사", "자금 용도: ")
    pdf.callout_box("의료기기의 경우, 프리시드 단계에서는 주로 초기 등가기기 조사, 타당성 시제품 제작, 임시 특허 출원에 자금이 사용됩니다. 아직 FDA와의 접촉은 없습니다.")

    pdf.sub_heading("시드 라운드(Seed Round)")
    pdf.body("첫 번째 '본격적인' 자금조달 라운드입니다. 작동하는 시제품이나 강력한 기술 데이터가 있으며, 규제 제출을 향해 발전하기 위한 자금이 필요합니다.")
    pdf.bullet("의료기기 기준 일반적으로 $500K - $3M", "금액: ")
    pdf.bullet("엔젤 투자자, 엔젤 그룹, 마이크로 VC, 액셀러레이터 (Y Combinator, HAX, TMCx)", "자금원: ")
    pdf.bullet("프리머니 기업가치 $2M - $10M", "기업가치: ")
    pdf.bullet("설계 검증 테스트, Pre-Submission 회의(FDA), 벤치 테스트, 초기 임상 데이터", "자금 용도: ")
    pdf.bullet("SAFE, 전환사채, 프라이스드 에퀴티 라운드", "구조: ")
    pdf.callout_box("510(k) 기기 기업에게 이것이 최적 시점입니다. 시드 자금은 Pre-Sub부터 제출까지를 지원합니다 -- 규제 경로에서 자본 효율성이 가장 높은 구간입니다.")

    pdf.sub_heading("시리즈 A(Series A)")
    pdf.body("첫 번째 기관 벤처캐피탈 라운드입니다. 일반적으로 상당한 리스크 제거 이후에 진행됩니다 -- 의료기기의 경우 보통 FDA 인허가 또는 제출 이후입니다.")
    pdf.bullet("일반적으로 $3M - $15M", "금액: ")
    pdf.bullet("벤처캐피탈 (의료기기 전문: MedTech Ventures, Gilde Healthcare, Hatteras Venture Partners)", "자금원: ")
    pdf.bullet("프리머니 기업가치 $10M - $40M", "기업가치: ")
    pdf.bullet("상업적 출시, 영업팀 구축, QMS 구현, 제조 스케일업", "자금 용도: ")
    pdf.bullet("리드 투자자 이사회 의석, 보호 조항이 포함된 우선주", "핵심 조건: ")

    pdf.sub_heading("시리즈 B 및 후속 라운드")
    pdf.body("제품-시장 적합성과 매출 성장이 입증된 기업을 위한 성장 단계 자금조달입니다.")
    pdf.bullet("일반적으로 $15M - $50M+", "금액: ")
    pdf.bullet("성장 단계 VC, 전략적 투자자 (J&J Innovation, Medtronic Ventures, GE Healthcare Ventures)", "자금원: ")
    pdf.bullet("판매 확대, 국제 규제 (CE 마킹, NMPA), 차세대 제품 개발", "자금 용도: ")

    pdf.sub_heading("투자 라운드 요약표")
    w = [30, 28, 40, 40, 52]
    pdf.table_row(["라운드", "금액", "기업가치", "투자자", "의료기기 마일스톤"], w, header=True)
    pdf.table_row(["프리시드", "$25K-500K", "프리밸류에이션", "지인, 보조금", "개념, IP 출원"], w, bold_first=True)
    pdf.table_row(["시드", "$500K-3M", "$2-10M 프리", "엔젤, 마이크로VC", "Pre-Sub~510(k) 제출"], w, bold_first=True)
    pdf.table_row(["시리즈 A", "$3-15M", "$10-40M 프리", "VC 펀드", "FDA 인허가, 출시"], w, bold_first=True)
    pdf.table_row(["시리즈 B", "$15-50M+", "$40-150M+", "성장 VC", "스케일업, 해외 진출"], w, bold_first=True)

    # ── 섹션 2: 텀시트 ─────────────────────────────
    pdf.section_heading(2, "텀시트(Term Sheet)", "투자 계약의 청사진 -- 모든 조항의 의미와 중요성")

    pdf.body("텀시트는 투자의 핵심 재무 및 거버넌스 조건을 정리한 비구속력 문서입니다. 일반적으로 초기 실사 이후, 최종 법률 문서 작성 전에 리드 투자자가 발행합니다. 투자를 위한 '의향서(LOI)'로 생각하시면 됩니다.")

    pdf.sub_heading("경제적 조건")
    pdf.body("기업의 가치와 수익 분배 방식을 결정하는 조건입니다.")

    pdf.bullet("새로운 투자금이 들어오기 전 기업의 가치입니다. 프리머니 기업가치가 $5M이고 투자자가 $1M을 투자하면, 포스트머니 기업가치는 $6M이며 투자자는 1/6(16.7%)을 소유합니다.", "프리머니 기업가치: ")
    pdf.bullet("프리머니 + 신규 투자 = 포스트머니. 지분율은 포스트머니 기준으로 계산합니다. 항상 프리머니 기준으로 협상하세요.", "포스트머니 기업가치: ")
    pdf.bullet("투자자가 지불하는 주당 가격입니다. 프리머니 기업가치를 총 발행주식수(옵션풀 포함)로 나누어 산출합니다.", "주당 가격: ")
    pdf.bullet("향후 직원 스톡옵션을 위해 예약된 주식 풀(일반적으로 포스트머니의 10-20%)입니다. 중요: 투자자들은 보통 옵션풀이 프리머니 기업가치에서 차감되도록 요구하며, 이는 실질적으로 창업자의 프리머니를 낮추는 효과가 있습니다.", "옵션풀: ")

    pdf.callout_box("옵션풀 셔플은 이해해야 할 가장 중요한 메커니즘 중 하나입니다. $5M 프리머니에서 20% 옵션풀을 프리머니에서 차감하면 실질적으로 창업자에게는 $4M 프리머니가 됩니다. 항상 양쪽 방식으로 희석을 모델링하세요.", style="warn")

    pdf.callout_box("시드 투자자가 $5M 기업가치에서 프리머니 기준 20% 옵션풀을 요구하지만, 실제로는 10%만 필요합니다. 20% 풀에서는 실질 프리머니가 $4M으로 떨어져 투자자의 $1M이 16.7% 대신 20%를 차지합니다. 10% 풀에서는 실질 프리머니가 $4.5M이고 투자자는 18.2%를 받습니다. 이 10%포인트 차이는 창업자에게 약 $500K의 암묵적 가치를 의미합니다. 어떤 직책을 채용할 것인지 보여주는 상향식 채용 계획으로 항상 풀 규모를 협상하세요.", style="scenario")

    pdf.sub_heading("청산우선권(Liquidation Preference)")
    pdf.body("회사가 매각, 합병 또는 청산될 때 누가 먼저 (얼마나) 지급받는지를 결정합니다. 기업가치 다음으로 가장 중요한 경제적 조건입니다.")

    pdf.bullet("투자자가 투자금을 회수하거나 보통주로 전환하여 비례배분합니다. 가장 창업자-친화적입니다.", "1배 비참여형 우선주: ")
    pdf.bullet("투자자가 먼저 투자금을 회수한 후, 나머지 수익도 비례배분합니다. '이중 이익' 구조로 투자자가 두 번 지급받습니다.", "1배 참여형 우선주: ")
    pdf.bullet("2배 또는 3배 우선권은 보통주주가 한 푼도 받기 전에 투자자가 2~3배를 회수합니다. 가능하면 피하세요.", "다중 우선권: ")

    pdf.callout_box("예시: 투자자가 1배 참여형 우선주로 20%에 $2M 투자. 회사가 $10M에 매각. 투자자는 $2M(우선권) + 나머지 $8M의 20%($1.6M) = 총 $3.6M. 창업자/보통주주는 $6.4M. 1배 비참여형이라면 투자자는 전환 선택: 20% x $10M = $2M. 동일한 결과이지만, $50M 엑시트에서는 참여형 투자자가 $2M + 20%($48M) = $11.6M, 비참여형은 $10M.")

    pdf.callout_box("510(k) 기기 회사가 $30M 인수 제안을 받습니다. 투자자는 1배 참여형 우선주로 25%에 $3M 투자. 참여형: 투자자가 $3M 우선권 + 나머지 $27M의 25%($6.75M) = $9.75M. 창업자는 $20.25M. 비참여형: 투자자 전환 -- 25% x $30M = $7.5M. 창업자는 $22.5M. 참여형 우선권이 이 엑시트에서 창업자에게 $2.25M 비용 발생. 이제 실망스러운 $6M 엑시트를 상상해보세요: 참여형 투자자는 $3M + 25%($3M) = $3.75M, 창업자는 $2.25M. 비참여형 투자자는 $3M 우선권 선택(25% x $6M = $1.5M보다 유리). 창업자는 $3M. 낮은 엑시트에서 참여형 우선주가 가장 큰 피해를 줍니다.", style="scenario")

    pdf.sub_heading("희석방지 보호(Anti-Dilution)")
    pdf.body("향후 라운드에서 낮은 기업가치로 자금 조달(다운 라운드)할 경우 투자자를 보호합니다. 투자자의 전환 가격이 하향 조정되어 더 많은 주식을 받습니다.")

    pdf.bullet("다운 라운드의 규모를 총 주식 대비 가중 평균 공식으로 재산출합니다. 표준적이며 더 창업자-친화적입니다.", "광의 가중평균(Broad-Based Weighted Average): ")
    pdf.bullet("전환 가격이 새로운 낮은 가격으로 떨어집니다 -- 투자자가 낮은 기업가치에 투자한 것처럼 됩니다. 매우 투자자-친화적이며 창업자에게 불리합니다. 현대 거래에서는 드뭅니다.", "완전 래칫(Full Ratchet): ")

    pdf.callout_box("시드 투자자가 $10M 프리머니에서 20%를 매수합니다. 6개월 후 임상시험이 혼합 결과를 내놓고 $5M 프리머니(다운 라운드)로 시리즈 A를 진행해야 합니다. 완전 래칫: 시드 투자자의 주식이 $5M 기업가치로 재조정되어 소유 비율이 20%에서 약 35%로 증가 -- 창업자 지분 15%포인트 소멸. 광의 가중평균: 다운 라운드의 상대적 규모를 반영하여 시드 투자자가 약 24%로 증가. 두 메커니즘의 차이는 창업자 희석 11%포인트입니다. $50M 엑시트에서 이 차이는 창업자에게 $5.5M의 가치입니다.", style="scenario")

    pdf.sub_heading("거버넌스 및 통제 조건")

    pdf.bullet("투자자(특히 시리즈 A 리드)는 일반적으로 이사회 의석 1석을 받습니다. 일반적 구성: 창업자 2 + 투자자 1 + 독립이사 1 = 4인 이사회. 투자자 과반 의석 부여에 주의하세요.", "이사회 의석: ")
    pdf.bullet("이사회 투표와 관계없이 투자자 승인이 필요한 특정 사안. 일반적 보호 조항: 신주 발행, 회사 매각, 정관 변경, 임계치 초과 부채, CEO 채용/해고.", "보호 조항: ")
    pdf.bullet("투자자 다수가 회사 매각을 원하면 모든 주주(창업자 포함)에게 동의를 강제할 수 있습니다. 보통 우선주의 50-67%가 동의해야 발동됩니다.", "동반매도청구권(Drag-Along): ")
    pdf.bullet("투자자가 향후 라운드에 참여하여 지분율을 유지할 수 있습니다. 표준적이며 논쟁의 여지가 적습니다.", "비례참여권(Pro-Rata): ")
    pdf.bullet("향후 IPO 또는 인수 시, 등록 권한을 가진 투자자는 자신의 주식을 등록에 포함하도록 요구할 수 있습니다. 표준 조항입니다.", "등록권(Registration Rights): ")

    pdf.callout_box("이사회가 창업자 2 + 투자자 2로 구성됩니다. 전략적 인수자가 인허가된 510(k) 기기에 $30M을 제안하며, 각 창업자에게 우선권 후 $8M이 돌아갑니다. 투자자는 3년 후 $100M을 노리고 보류합니다. 이사회가 교착되어 거래가 무산되고 인수자는 경쟁사로 갑니다. 6개월 후 새로운 경쟁사가 진입하며 회사 가치가 하락합니다. 항상 교착을 해결할 수 있는 독립이사를 최소 1명 두고, 시리즈 B 이전에 투자자 과반 의석 부여에 주의하세요.", style="scenario")

    pdf.sub_heading("창업자 관련 조건")

    pdf.bullet("창업자가 이미 주식을 '소유'하고 있더라도 투자자들은 보통 창업자 주식에 베스팅(일반적으로 1년 클리프가 포함된 4년)을 요구합니다. 이는 창업자의 조기 이탈을 방지합니다. 일반적 타협: 이미 투입된 시간에 대한 크레딧(예: 1년 베스팅 이미 적립).", "창업자 베스팅: ")
    pdf.bullet("창업자가 전일제로 근무하고 재직 중 또는 퇴직 후 일정 기간 경쟁하지 않겠다는 약속. 퇴직 후 1-2년이 표준이며, 그 이상은 공격적입니다.", "경쟁금지/인재유인금지: ")
    pdf.bullet("창업자가 만든 기업 관련 모든 지적 재산은 기업에 양도됩니다. 필수적이고 협상 불가입니다.", "IP 양도: ")
    pdf.bullet("주주(창업자 및 투자자)가 회사/이사회 승인 없이 주식을 판매하는 것을 방지합니다. IPO 전까지 비상장 기업의 표준입니다.", "우선매수권(ROFR): ")

    pdf.callout_box("40% 지분을 가진 CTO 공동창업자가 4년 베스팅(1년 클리프 통과 후) 18개월차에 퇴사합니다. 베스팅 있음: CTO는 18/48 = 15%를 보유(할당량의 37.5%). 나머지 25%는 재배분을 위해 회사로 반환. 베스팅 없음: CTO는 40% 전체를 가지고 떠남 -- 회사를 거의 투자 불가능하게 만드는 대규모 '유령 지분'이 생깁니다. 어떤 투자자도 40%가 퇴사자에게 있는 회사에 투자하지 않습니다. 이것이 투자자가 이미 '보유한' 주식에도 창업자 베스팅을 요구하는 이유입니다.", style="scenario")

    pdf.callout_box("경쟁금지 조항이 퇴직 후 2년, '모든 의료기기 회사'에 적용됩니다. 투자자와 의견 불일치로 퇴사합니다. 2년간 자신의 분야에서 일할 수 없습니다 -- 컨설팅, 경쟁사 합류, 새 의료기기 벤처 창업 포함. 대부분의 유효한 경쟁금지는 12개월이며 특정 기기 카테고리로 좁게 범위가 정해집니다. 12개월 초과 또는 특정 제품 영역보다 넓은 것에는 반드시 반대하세요. 참고: 캘리포니아 및 여러 주에서는 경쟁금지를 전혀 시행하지 않습니다.", style="scenario")

    pdf.sub_heading("텀시트 적신호")
    w2 = [55, 135]
    pdf.table_row(["적신호", "중요한 이유"], w2, header=True)
    pdf.table_row(["완전 래칫 희석방지", "다운 라운드 시 창업자에게 심각한 피해"], w2, bold_first=True)
    pdf.table_row(["1배 초과 참여형 우선주", "이중 이익: 투자금 회수 + 잔여 수익 배분"], w2, bold_first=True)
    pdf.table_row(["투자자 이사회 과반", "전략적 결정에 대한 창업자 통제력 상실"], w2, bold_first=True)
    pdf.table_row(["과도한 보호 조항", "일상 운영에 대한 투자자 거부권"], w2, bold_first=True)
    pdf.table_row(["60일 초과 독점협상 조항", "너무 오래 다른 투자자와 대화 차단"], w2, bold_first=True)
    pdf.table_row(["누적 배당금", "창업자 수익 전 연 8%+ 투자금 증가"], w2, bold_first=True)
    pdf.table_row(["다중 청산우선권(2배+)", "보통주주 수령 전 투자자 2-3배 회수"], w2, bold_first=True)

    # ── 섹션 3: 기업가치 평가 ────────────────────
    pdf.section_heading(3, "기업가치 평가 방법", "각 단계별 의료기기 스타트업 기업가치 평가")

    pdf.body("초기 단계 의료기기 기업의 기업가치 평가는 과학보다 예술에 가깝습니다. 예측 가능한 MRR 메트릭이 있는 SaaS 스타트업과 달리, 의료기기 기업가치는 규제 마일스톤과 임상 리스크에 크게 좌우됩니다.")

    pdf.sub_heading("매출 전 기업가치 평가 방식")

    pdf.bullet("가치 = 기기 카테고리의 TAM(전체 시장 규모)에서 FDA 인허가 확률, 시장 진입 시간, 경쟁을 할인하여 산출. $1B TAM에 70% 인허가 확률, 24개월 타임라인이면 시드 시 $5-10M 프리머니를 지지할 수 있습니다.", "리스크 조정 시장 접근법: ")
    pdf.bullet("같은 단계의 유사한 의료기기 기업과 비교. 유사한 510(k) 기기 기업의 시드 라운드 공개 데이터 참조. 적응증과 시장 규모에 따라 조정합니다.", "비교거래법: ")
    pdf.bullet("전략적 인수자가 이 기술에 얼마를 지불할까? 510(k) 기기의 경우, 인수자들은 일반적으로 매출의 3-8배(인허가 후) 또는 초기 매출이 있는 인허가 기기에 $20-50M+를 지불합니다. 엑시트에서 역산하여 적정 진입 기업가치를 결정합니다.", "인수 비교/엑시트 분석: ")
    pdf.bullet("투자자가 특정 수익률(예: 7년에 10배)을 목표로 합니다. $100M 엑시트에서 10배를 기대하면, $10M 포스트머니에 $1M-$2M을 투자하여 10-20% 소유합니다.", "VC 방법론: ")

    pdf.sub_heading("마일스톤별 기업가치 상승")
    pdf.body("의료기기 기업가치는 계단식으로 상승하며, 각 규제 마일스톤이 가치 '스텝업'을 만듭니다:")
    w3 = [50, 40, 48, 52]
    pdf.table_row(["마일스톤", "일반적 상승폭", "프리머니 범위", "이유"], w3, header=True)
    pdf.table_row(["개념/특허", "기준선", "$1-3M", "아이디어 리스크, FDA 미접촉"], w3, bold_first=True)
    pdf.table_row(["Pre-Sub 제출", "+30-50%", "$2-5M", "FDA 접촉 신호"], w3, bold_first=True)
    pdf.table_row(["Pre-Sub 피드백", "+50-80%", "$4-8M", "규제 리스크 해소"], w3, bold_first=True)
    pdf.table_row(["510(k) 제출", "+100-200%", "$6-15M", "제출 = 변곡점"], w3, bold_first=True)
    pdf.table_row(["510(k) 인허가", "+200-400%", "$10-30M", "시장 준비 완료"], w3, bold_first=True)
    pdf.table_row(["첫 매출", "+300-500%", "$15-50M", "제품-시장 적합성"], w3, bold_first=True)

    pdf.callout_box("의료기기에서 가장 큰 기업가치 도약은 '510(k) 제출'에서 '510(k) 인허가' 사이입니다. 인허가 전 전략적 자금조달이 투자자에게 최고의 수익을, 창업자에게 캡테이블 상 가장 유리한 진입점을 제공하는 이유입니다.")

    # ── 섹션 4: 투자 수단 ─────────────────────────
    pdf.section_heading(4, "투자 수단", "SAFE, 전환사채, 프라이스드 라운드 설명")

    pdf.sub_heading("SAFE (미래 지분에 대한 간단한 합의)")
    pdf.body("Y Combinator가 만든 구조입니다. SAFE는 부채가 아니며, 향후 프라이스드 라운드에서 지분을 받을 권리를 투자자에게 부여하는 계약입니다. 이자도, 만기일도 없습니다.")
    pdf.bullet("투자자가 (a) 밸류에이션 캡 또는 (b) 다음 라운드 가격에 대한 할인 중 낮은 가격으로 지분을 받습니다", "작동 방식: ")
    pdf.bullet("SAFE가 전환되는 최대 기업가치. 예: $5M 캡이면 시리즈 A 기업가치가 아무리 높아도 SAFE 투자자는 $5M에서 전환합니다.", "밸류에이션 캡: ")
    pdf.bullet("일반적으로 15-25%. 시리즈 A가 $10M 프리머니이고 SAFE에 20% 할인이 있으면, SAFE 투자자는 $8M에서 전환합니다.", "할인율: ")
    pdf.bullet("단순, 빠름(문서 하나), 이자 누적 없음, 만기일 압박 없음. 프리시드와 시드에 표준적.", "장점: ")
    pdf.bullet("전환 시까지 투자자 권한 없음, 프라이스드 라운드까지 희석 불확실, 여러 SAFE가 쌓이는 'SAFE 파일' 문제 가능.", "단점: ")

    pdf.callout_box("$5M 캡으로 $500K SAFE를 조달한 후, $8M 캡으로 $300K 두 번째 SAFE를 조달하고, $12M 프리머니로 $2M 시리즈 A를 진행합니다. 첫 SAFE는 $5M에서 전환(매우 유리 -- $500K로 10% 소유). 두 번째는 $8M(3.75%). 시리즈 A 투자자는 $12M으로 가격 책정. 전환 후 SAFE 스택이 시리즈 A 투자자 지분 전에 합계 13.75% 소유. $800K로 약 6% 희석을 예상했지만 13.75%가 됩니다. 각 SAFE는 자체 캡에서 독립적으로 전환되며 희석이 복리됩니다. 가능하면 단일 SAFE 캡으로 제한하세요.", style="scenario")

    pdf.sub_heading("전환사채(Convertible Notes)")
    pdf.body("전환사채는 지분으로 전환되는 단기 부채입니다. SAFE와 달리 이자가 발생하고 만기일이 있습니다.")
    pdf.bullet("일반적으로 연 4-8%. 이자는 원금과 함께 지분으로 전환됩니다.", "이자율: ")
    pdf.bullet("일반적으로 18-24개월. 만기까지 프라이스드 라운드가 없으면 기술적으로 상환 의무 발생 -- 갈등의 소지.", "만기일: ")
    pdf.bullet("SAFE와 동일: 밸류에이션 캡 및/또는 다음 프라이스드 라운드 할인.", "전환: ")
    pdf.bullet("SAFE보다 투자자 보호 강함(부채). 일부 투자자는 강제 전환 일정을 선호합니다.", "장점: ")
    pdf.bullet("이자 누적이 지분 비용 발생. 만기일이 압박 생성. SAFE보다 법적으로 복잡.", "단점: ")
    pdf.callout_box("의료기기 스타트업의 경우, FDA 일정의 불확실성 때문에 전환사채는 위험할 수 있습니다. 510(k) 심사가 예상보다 길어지고 프라이스드 라운드 전에 사채가 만기되면, 강제 상환이나 불리한 재협상에 직면할 수 있습니다.", style="warn")

    pdf.callout_box("6% 이자, 24개월 만기, $5M 캡으로 $500K 전환사채를 발행합니다. 510(k) 심사가 예상 6개월 대신 14개월 소요 -- FDA 추가정보요청(AI)으로 8개월 추가. 24개월차에 만기 도래, 누적 이자 $60K($560K 합계). 아직 인허가가 없어 시리즈 A를 진행하지 못했습니다. 투자자가 보유하지 않은 $560K 현금 상환을 요구하거나, 훨씬 낮은 캡($5M 대신 $3M)으로 전환 재협상을 할 수 있습니다 -- 실질적으로 투자자 소유비율이 두 배. SAFE(만기일 없음, 이자 없음)였다면 시간 압박도 재협상 레버리지도 없었을 것입니다.", style="scenario")

    pdf.sub_heading("프라이스드 에퀴티 라운드(우선주)")
    pdf.body("프라이스드 라운드는 특정 기업가치, 주당 가격을 설정하고 정의된 권리를 가진 새로운 우선주 클래스를 생성합니다. 시리즈 A 이상의 표준 구조입니다.")
    pdf.bullet("확정적 법률 문서: 주식매매계약서, 투자자 권리 계약서, 우선매수권, 의결권 계약서, 정관 수정.", "핵심 문서: ")
    pdf.bullet("표준 시리즈 A에 $15K-$50K+ 법률 비용. 양측 모두 법률 자문 필요.", "법률 비용: ")
    pdf.bullet("깨끗한 캡테이블, 명확한 거버넌스, 투자자 권한 확정. 기관 VC 투자에 필수.", "장점: ")
    pdf.bullet("비용이 많이 들고, 시간 소요(클로징까지 4-8주), 이사회 승인과 주주 동의 필요.", "단점: ")

    pdf.callout_box("SAFE 대신 $5M 프리머니로 프라이스드 시드 라운드를 진행합니다. 법률 비용 $35K와 6주 소요. 3개월 후, 긍정적 FDA Pre-Sub 피드백으로 규제 리스크가 크게 해소됩니다. 회사 가치가 이제 $8-10M입니다. 전체 가치 상승이 $5M에 참여한 시드 투자자에게 귀속됩니다. $7M 캡 SAFE였다면 기업가치가 시리즈 A까지 이연되어 마일스톤 혜택을 받을 수 있었습니다. 반대 시나리오: Pre-Sub 피드백이 부정적이고 기업 가치가 $3M으로 하락했다면, $5M 프라이스드 라운드가 고통스러운 다운라운드 재협상으로부터 보호했을 것입니다. 프라이스드 라운드는 양방향 불확실성을 제거합니다.", style="scenario")

    pdf.sub_heading("투자 수단 비교")
    w4 = [35, 45, 45, 65]
    pdf.table_row(["특성", "SAFE", "전환사채", "프라이스드 라운드"], w4, header=True)
    pdf.table_row(["법률 비용", "$0-2K", "$2-5K", "$15-50K+"], w4, bold_first=True)
    pdf.table_row(["클로징 소요", "수일", "1-2주", "4-8주"], w4, bold_first=True)
    pdf.table_row(["이자", "없음", "연 4-8%", "해당없음"], w4, bold_first=True)
    pdf.table_row(["만기일", "없음", "18-24개월", "해당없음"], w4, bold_first=True)
    pdf.table_row(["기업가치 확정?", "이연", "이연", "확정"], w4, bold_first=True)
    pdf.table_row(["이사회 의석", "없음", "가끔", "있음(리드)"], w4, bold_first=True)
    pdf.table_row(["최적 시기", "프리시드/시드", "시드/브릿지", "시리즈 A+"], w4, bold_first=True)

    # ── 섹션 5: 투자자 유형 ──────────────────────
    pdf.section_heading(5, "투자자 유형", "의료기기에 투자하는 주체와 기대사항")

    pdf.sub_heading("엔젤 투자자")
    pdf.body("자기 자금으로 투자하는 고액자산가 개인입니다. 종종 전직 경영자, 의사, 또는 해당 분야 전문성을 가진 기업가입니다.")
    pdf.bullet("투자당 $25K - $250K", "투자규모: ")
    pdf.bullet("프리시드 및 시드", "단계: ")
    pdf.bullet("개인 경험, 멘토 관계, 창업자에 대한 신뢰. 비공식적 조건으로 투자하는 경우가 많습니다.", "동기: ")
    pdf.bullet("의사결정이 느릴 수 있고, 후속 투자 여력 제한, 전략적 가치를 추가하지 못할 수 있음.", "주의사항: ")

    pdf.sub_heading("엔젤 그룹 / 신디케이트")
    pdf.body("자본을 모으고 실사를 공유하는 조직화된 엔젤 그룹입니다. 예: Oregon Angel Fund, Alliance of Angels, Tech Coast Angels, Life Science Angels.")
    pdf.bullet("투자당 $100K - $1M (공동)", "투자규모: ")
    pdf.bullet("시드", "단계: ")
    pdf.bullet("공식 피칭 프로세스, 그룹 투표, 개인 엔젤보다 구조화된 조건.", "프로세스: ")
    pdf.bullet("보통 대표 1명이 이사 또는 옵서버 역할.", "거버넌스: ")

    pdf.sub_heading("벤처캐피탈(VC)")
    pdf.body("유한파트너(LP)의 자본 풀(펀드)을 관리하는 전문 투자 회사입니다. 의료기기 전문 VC는 FDA 일정과 규제 리스크를 이해합니다.")
    pdf.bullet("투자당 $1M - $25M+", "투자규모: ")
    pdf.bullet("시리즈 A 이상 (일부는 시드도 참여)", "단계: ")
    pdf.bullet("이사회 의석, 적극적 거버넌스, 후속 투자, 엑시트 중심 (5-7년 투자기간)", "기대사항: ")
    pdf.bullet("높은 수익률 기대(펀드 수익률 3-5배). 성장을 밀어붙이며, 때로 창업자 통제를 희생할 수 있음.", "주의사항: ")

    pdf.sub_heading("전략적 투자자(Corporate VC)")
    pdf.body("대형 의료기기 기업의 투자 부문: J&J Innovation, Medtronic Ventures, GE Healthcare Ventures, Philips Health Technology Ventures, Baxter Ventures.")
    pdf.bullet("투자당 $2M - $20M", "투자규모: ")
    pdf.bullet("시리즈 A-B, 전략적으로 중요한 기술의 경우 시드도 가능", "단계: ")
    pdf.bullet("유통 채널, 임상 시험기관, 규제 전문성, 인수 경로 접근.", "장점: ")
    pdf.bullet("기술 접근권, 인수 우선권, 독점 라이선스를 원할 수 있음. 다른 인수자를 저해할 수 있음.", "주의사항: ")
    pdf.callout_box("전략적 투자자는 양날의 검입니다. Medtronic Ventures 투자는 검증 신호가 되지만 J&J이나 Abbott의 인수 관심을 저해할 수 있습니다. ROFR과 정보 접근권을 신중하게 협상하세요.")

    pdf.callout_box("Medtronic Ventures가 인수 우선매수권(ROFR)과 함께 시드 라운드에 $2M 투자합니다. 2년 후, Abbott이 $50M 인수를 제안합니다. Medtronic이 ROFR을 행사하여 제안을 매칭하지만 90일이 소요되어 Abbott의 관심이 식습니다. 또는 Medtronic이 매칭을 거부해도, Abbott은 Medtronic이 거래를 보고 패스한 것을 알고 제안을 낮출 수 있습니다. 어느 경우든 ROFR은 레버리지를 줄입니다. 반대 시나리오: Medtronic의 투자로 임상시험기관, 유통망, 규제팀에 접근할 수 있었고 -- 인허가를 6개월 앞당기고 최종 인수 가격을 $15M 높였습니다. ROFR은 레버리지를 잃었지만 전략적 가치가 그 이상으로 보상했습니다.", style="scenario")

    pdf.sub_heading("정부 / 비희석적 자금조달")
    pdf.bullet("Phase I ($275K, 6-9개월) 타당성 연구, Phase II ($1-2M, 2년) 개발. 경쟁이 치열하지만 비희석적.", "NIH SBIR/STTR: ")
    pdf.bullet("Phase I ($200K), Phase II ($1.1M). 이중 용도 의료 기술에 적합.", "NSF SBIR: ")
    pdf.bullet("의료 대응 기술을 위한 BARDA 및 ASPR. 대규모 지원($5-25M) 그러나 매우 특정한 용도.", "BARDA: ")
    pdf.bullet("오리건 SBIR 매칭 보조금, Oregon Innovation Council, 주 벤처 펀드.", "주 프로그램: ")
    pdf.callout_box("비희석적 자금은 항상 지분 자금조달과 병행 추진해야 합니다. SBIR 보조금은 캡테이블을 희석하지 않으며 정부의 기술 검증 신호가 됩니다.")

    pdf.callout_box("$5M 캡 SAFE로 $1M 시드 라운드를 조달하면서 동시에 SBIR Phase I($275K)을 수상합니다. SBIR이 필요한 지분 조달액을 줄여줍니다 -- 이제 $1M 대신 $725K만 조달하면 되어 희석이 20%에서 14.5%로 감소. 세 라운드에 걸쳐 이 복리 효과가 창업자 지분을 추가 5-8% 보존합니다. 또는: SBIR로 핵심 마일스톤(Pre-Sub 피드백) 대기 동안 런웨이를 연장하여, 더 높은 기업가치($5M 대신 $7M)로 시드를 조달할 수 있습니다. 비희석적 자금은 단순히 지분만 절약한 것이 아니라 기업가치를 높일 시간을 벌어준 것입니다.", style="scenario")

    # ── 섹션 6: 510(k) Bridge 전략 ──────────────
    pdf.section_heading(6, "510(k) Bridge 전략", "규제 마일스톤 대비 투자자 접촉 시점")

    pdf.body("510(k) 규제 경로는 자금조달 레버리지에 직접 영향을 미치는 자연스러운 변곡점을 만듭니다. 각 마일스톤 대비 투자자 접촉 시점을 이해하는 것이 기업가치와 조건 최적화에 핵심입니다.")

    pdf.sub_heading("투자자 접촉 타임라인")
    pdf.body("자금조달에 있어 모든 달이 동일하지 않습니다. 표준 510(k) 타임라인에 매핑된 최적 접촉 케이던스입니다:")

    pdf.ln(2)
    w5 = [14, 33, 12, 45, 86]
    pdf.table_row(["월", "마일스톤", "신호", "투자자 액션", "이 시점인 이유"], w5, header=True)
    pdf.table_row(["M+0", "Pre-Sub 제출", "웜", "관계 구축", "FDA 접촉이 진지함을 증명 -- 아이디어만이 아님"], w5, bold_first=True)
    pdf.table_row(["M+2", "Pre-Sub 회의", "활발", "피칭 미팅", "FDA 피드백 레터가 최고의 자금조달 자산"], w5, bold_first=True)
    pdf.table_row(["M+3", "벤치 테스트", "활발", "데이터 공유", "IEC 60601, EMC, 사용성 데이터가 기술 타당성 증명"], w5, bold_first=True)
    pdf.table_row(["M+6", "510(k) 제출", "피크", "텀시트 추진", "제출이 변곡점 -- 인허가는 '언제'의 문제"], w5, bold_first=True)
    pdf.table_row(["M+9", "510(k) 인허가", "클로즈", "라운드 클로징", "최대 레버리지 -- 인허가, 시장 준비 완료"], w5, bold_first=True)

    pdf.sub_heading("M+2에서 M+6이 최적 시점인 이유")
    pdf.body("FDA Pre-Submission 회의 피드백(M+2)과 510(k) 제출(M+6) 사이가 최적의 자금조달 기간인 세 가지 이유:")
    pdf.bullet("R2의 FDA 피드백 레터가 규제 전략이 건전하다는 구체적인 제3자 검증입니다. 투자자에게 보여줄 수 있는 가장 설득력 있는 문서입니다.", "1. 규제 리스크 해소: ")
    pdf.bullet("인허가 전이므로 기업가치가 아직 '이벤트 전'입니다. 510(k) 인허가 전에 참여하는 투자자들은 인허가 전 가격 -- 일반적으로 인허가 후보다 40-60% 낮은 가격을 받습니다. 이것이 투자자들이 구매하는 수익률입니다.", "2. 유리한 기업가치: ")
    pdf.bullet("M+6에서 510(k)가 제출되면 인허가까지 90일(표준 심사)입니다. 투자자가 결승선을 볼 수 있을 만큼 가깝지만, 인허가 전 조건을 받을 수 있을 만큼 이른 시점입니다.", "3. 가시적인 결승선: ")

    pdf.callout_box("의료기기 창업자들이 가장 많이 하는 실수는 인허가 이후까지 자금조달을 미루는 것입니다. 인허가 후 자금조달은 더 나은 조건을 주지만 6-12개월의 상업적 런웨이를 잃게 됩니다. 출시에 필요한 자금은 인허가 레터 도착 전에 확약받아야 합니다.")

    pdf.callout_box("기업 A는 M+3(Pre-Sub 피드백 후)에 $6M 프리머니로 $2M 조달. 510(k) 제출 전 자금 확보 완료. 인허가 도착 시 즉시 출시 -- 영업사원 채용, 전시회 참가, 30일 내 첫 출하. 기업 B는 인허가 후 자금조달 시작. 더 나은 조건($12M 프리머니에 $2M -- 절반의 희석) 확보하지만 조달에 5개월 소요. 그동안 경쟁사가 유사 기기를 출시하고 2개 병원 시스템과 계약. 기업 A의 희석 '과다 지불'이 5개월의 시장 독점과 선점자 우위를 가져왔습니다. 의료기기에서 인허가 후 시장 출시 속도가 종종 기업가치 차이보다 더 가치있습니다.", style="scenario")

    pdf.sub_heading("각 단계에서 투자자가 보고 싶어하는 것")

    pdf.body("피칭 자료는 규제 타임라인을 따라 진화해야 합니다:")

    pdf.bullet("비전 + 기술 접근법, IP 현황, 팀 역량, TAM/SAM 분석. Pre-Sub 제출이 FDA 접촉을 증명.", "M+0 (Pre-Sub 제출): ")
    pdf.bullet("위의 모든 것 + FDA 피드백 레터('리스크 해소 문서'), FDA 합의한 시험 프로토콜, 등가기기 비교를 포함한 경쟁 환경.", "M+2 (Pre-Sub 회의): ")
    pdf.bullet("위의 모든 것 + IEC 60601 시험 보고서, EMC 데이터, 임상 검증 프로토콜/초기 결과, 설계 동결 문서.", "M+3 (벤치 테스트): ")
    pdf.bullet("위의 모든 것 + 완전한 510(k) 제출 요약서, 인허가까지 타임라인(90일), 출시 계획, 매출 전망, 첫 KOL 약정.", "M+6 (510(k) 제출): ")
    pdf.bullet("위의 모든 것 + 인허가 레터, K-번호, 시판 후 계획, 상업적 성과, 첫 구매 주문 또는 LOI.", "M+9 (인허가): ")

    # ── 섹션 7: 실사 ─────────────────────────────
    pdf.section_heading(7, "투자자 실사(Due Diligence)", "투자 전 투자자가 조사하는 항목")

    pdf.body("실사(DD)는 투자 확정 전 투자자가 수행하는 조사 과정입니다. 의료기기의 경우, 규제, 임상, 제조 리스크로 인해 일반 기술 스타트업보다 더 엄격합니다.")

    pdf.sub_heading("기술 / 제품 실사")
    pdf.bullet("시제품 작동 vs. 개념? 설계 동결 상태? 검증 및 밸리데이션 테스트 완료?", "제품 성숙도: ")
    pdf.bullet("특허(출원 vs. 등록), 영업비밀, 자유실시 분석. FTO 조사 완료 여부?", "IP 포트폴리오: ")
    pdf.bullet("인허가/승인 여부? 어떤 경로? Pre-Sub에서 FDA 의견? 알려진 이슈?", "규제 현황: ")
    pdf.bullet("BOM, 계약 제조업체 확보? 대량 생산 가능? COGS는?", "제조: ")

    pdf.sub_heading("시장 실사")
    pdf.bullet("신뢰할 수 있는 상향식 분석의 전체 시장 규모. 하향식 TAM 수치만이 아닙니다.", "시장 규모: ")
    pdf.bullet("보험 급여 경로(CPT 코드, 병원 예산 vs. 의사 선호 품목), 지불 의향.", "보험 급여: ")
    pdf.bullet("기존 기기, 신규 경쟁사, 진입장벽 분석.", "경쟁: ")
    pdf.bullet("임상의 및 병원 관심, 의향서, KOL 관계.", "임상 챔피언: ")

    pdf.sub_heading("팀 실사")
    pdf.bullet("규제 업무 경험, 이전 FDA 제출 이력, 임상/엔지니어링 역량.", "도메인 전문성: ")
    pdf.bullet("전일제 근무 약정, 베스팅 일정, 창업자 계약서 체결 여부.", "창업자 약정: ")
    pdf.bullet("필요한 핵심 채용, 자문단 구성, 전문성 공백.", "팀 공백: ")

    pdf.sub_heading("재무 실사")
    pdf.bullet("기존 캡테이블, 이전 투자, 미전환 SAFE/사채.", "캡테이블: ")
    pdf.bullet("월간 소각율, 현재 지출 기준 런웨이, 이번 라운드 자금 사용처 상세.", "소각율 & 런웨이: ")
    pdf.bullet("수익 모델, 가격 전략, 흑자 경로, 단위 경제학.", "재무 전망: ")

    pdf.sub_heading("법률 실사")
    pdf.bullet("깨끗한 기업 구조, 계류 소송 없음, 적절한 법인 설립.", "법인: ")
    pdf.bullet("IP 양도 계약, 직원 발명 계약, NDA/경쟁금지 의무.", "IP 소유권: ")
    pdf.bullet("QMS 구축(ISO 13485), 불만 처리, MDR 보고 절차.", "규제 준수: ")

    # ── 섹션 8: 협상 전략 ────────────────────────
    pdf.section_heading(8, "협상 전략", "의료기기 창업자를 위한 실전 전술")

    pdf.sub_heading("협상 전")
    pdf.bullet("15-25명의 투자자와 동시에 대화하세요. 경쟁이 레버리지를 만듭니다. 관심 있는 단일 당사자와만 협상하지 마세요.", "경쟁 환경 조성: ")
    pdf.bullet("투자자의 포트폴리오, 펀드 규모, 최근 거래를 조사하세요. $50M 펀드의 $1M 체크와 $500M 펀드의 $1M 체크는 다릅니다.", "투자자 파악: ")
    pdf.bullet("BATNA(협상 결렬 시 최선의 대안)를 명확히 하세요. 이 거래가 무산되면 어떻게 되나? 선택지가 많을수록 = 더 많은 파워.", "BATNA 파악: ")

    pdf.sub_heading("핵심 협상 포인트 (우선순위)")
    pdf.body("모든 조건이 동등하게 중요한 것은 아닙니다. 가장 중요한 조건에 협상 에너지를 집중하세요:")
    pdf.bullet("이것이 직접적으로 지분을 결정합니다. 여기서 가장 강하게 싸우세요.", "1. 기업가치 (최고 우선순위): ")
    pdf.bullet("1배 비참여형이 표준입니다. 참여형 우선주나 1배 초과에 강하게 반대하세요.", "2. 청산우선권: ")
    pdf.bullet("창업자-친화적 이사회 구성 유지. 창업자 2 + 투자자 1 + 독립이사 1이 이상적.", "3. 이사회 구성: ")
    pdf.bullet("광의 가중평균을 주장하세요. 완전 래칫은 거부하세요.", "4. 희석방지: ")
    pdf.bullet("옵션풀 규모가 적정한지 확인하되, 프리머니가 아닌 포스트머니에서 차감하도록 주장하세요.", "5. 옵션풀: ")
    pdf.bullet("표준적이며 싸울 가치가 없습니다. 합리적인 보호 조항은 수용하세요.", "6. 비례참여권 (낮은 우선순위): ")

    pdf.sub_heading("흔한 실수")
    pdf.bullet("첫 번째 투자자가 1순위 리드여서는 안 됩니다. 우선순위가 낮은 투자자들로 먼저 피치를 연습하세요.", "최선의 카드를 먼저 보여주기: ")
    pdf.bullet("의료기기 자금조달은 3-6개월 소요됩니다. 규제 마일스톤에 맞춰 일찍 시작하세요.", "너무 늦게 시작하기: ")
    pdf.bullet("스타트업 경험이 있는 법률 자문을 구하세요(가족 변호사가 아닌). Wilson Sonsini, Cooley, Fenwick -- 또는 동급.", "법률 자문 건너뛰기: ")
    pdf.bullet("의료기기에서는 신뢰할 수 있는 510(k) 타임라인이 하키스틱 매출 전망보다 설득력 있습니다. 규제 진행 상황을 리드하세요.", "매출 전망 과대강조: ")

    pdf.callout_box("가장 좋은 자금조달 포지션은 돈이 절실히 필요하지 않을 때입니다. 6개월 이상의 런웨이가 남아 있을 때 자금조달을 시작하세요. 필요에 의한 포지션에서의 협상은 항상 불리한 조건으로 귀결됩니다.")

    # ── 섹션 9: 캡테이블 ─────────────────────────
    pdf.section_heading(9, "캡테이블 관리", "복수 라운드에 걸친 지분 희석 이해")

    pdf.body("캡테이블은 누가 회사의 몇 퍼센트를 소유하는지를 추적합니다. 캡테이블의 진화를 이해하는 것은 정보에 기반한 자금조달 결정에 필수적입니다.")

    pdf.sub_heading("예시: 510(k) 의료기기 스타트업 캡테이블 진화")

    pdf.body("시작점: 공동 창업자 2인, 50/50 배분, 발행 가능 주식 10M주.")

    w6 = [50, 30, 30, 30, 50]
    pdf.table_row(["주주", "설립 시", "시드 후", "시리즈A 후", "비고"], w6, header=True)
    pdf.table_row(["창업자 A", "50.0%", "37.5%", "28.1%", "CEO - 풀 베스팅"], w6, bold_first=True)
    pdf.table_row(["창업자 B", "50.0%", "37.5%", "28.1%", "CTO - 풀 베스팅"], w6, bold_first=True)
    pdf.table_row(["시드 투자자", "--", "15.0%", "11.3%", "SAFE, $1M/$6M 캡"], w6, bold_first=True)
    pdf.table_row(["옵션풀", "--", "10.0%", "12.5%", "시리즈A에서 보충"], w6, bold_first=True)
    pdf.table_row(["시리즈A 리드", "--", "--", "20.0%", "$3M/$12M 프리머니"], w6, bold_first=True)
    pdf.table_row(["합계", "100%", "100%", "100%", ""], w6, bold_first=True)

    pdf.body("핵심 관찰:")
    pdf.bullet("창업자는 두 라운드 후 100%에서 56.2%(합산)로 감소합니다. 이것은 정상적이고 건강한 것입니다.", "희석은 예상됨: ")
    pdf.bullet("$15M 기업의 56.2%($8.4M)은 $2M 기업의 100%보다 낫습니다.", "희석은 손실이 아님: ")
    pdf.bullet("모든 라운드가 이전 주주를 비례적으로 희석합니다(비례참여권을 행사하지 않는 한).", "모든 라운드가 모든 사람을 희석: ")

    pdf.callout_box("유용한 기준: 시드 후 40-60%, 시리즈 A 후 25-40%를 유지하는 창업자는 강한 포지션에 있습니다. 시리즈 B 전에 합산 20% 미만이면 너무 많이 양보한 것일 수 있습니다.")

    pdf.callout_box("두 창업자가 시드 후 각 40%(합산 80%) 소유, 옵션풀 10%, 시드 투자자 10%. 강한 포지션입니다. 이제 시리즈 A 투자자가 30% 지분과 15% 옵션풀 보충(프리머니에서)을 요구합니다. 시리즈A 후: 창업자는 80% x (1 - 0.30 - 0.075) = 합산 50%(각 25%)로 감소. 여전히 건강합니다. 하지만 시드 라운드가 과도하게 희석적이었다면(시드 후 합산 55%), 같은 시리즈 A로 창업자가 55% x 0.625 = 합산 34.4%(각 17.2%). 시리즈 B까지 각 10% 미만이 될 수 있습니다 -- 동기와 통제력 상실. 초기 라운드에서 지분을 적극적으로 보호하세요; 희석은 후속 조달마다 복리됩니다.", style="scenario")

    # ── 섹션 10: 용어집 ──────────────────────────
    pdf.section_heading(10, "용어집", "필수 투자 용어")

    terms = [
        ("희석방지(Anti-Dilution)", "낮은 기업가치의 향후 라운드에 대한 투자자 보호. 전환 가격을 조정합니다."),
        ("BATNA", "협상 결렬 시 최선의 대안. 거래가 무산될 경우의 대안책."),
        ("브릿지 라운드(Bridge Round)", "주요 라운드 사이의 소규모 자금조달, 보통 전환사채 사용."),
        ("소각율(Burn Rate)", "월간 현금 지출. 총 소각 = 총 지출. 순 소각 = 지출 - 수익."),
        ("캡테이블(Cap Table)", "모든 지분, 옵션, 워런트, 전환 수단을 보여주는 자본 구성표."),
        ("클리프(Cliff)", "주식이 베스팅되기 전 최소 기간(보통 1년)."),
        ("전환사채(Convertible Note)", "향후 프라이스드 라운드에서 지분으로 전환되는 단기 부채."),
        ("다운 라운드(Down Round)", "이전 라운드보다 낮은 기업가치의 자금조달 라운드."),
        ("동반매도청구권(Drag-Along)", "다수 주주가 소수 주주를 매각에 강제할 수 있는 권리."),
        ("실사(Due Diligence)", "투자 확정 전 투자자가 수행하는 조사 과정."),
        ("지분(Equity)", "주식으로 대표되는 회사 소유권."),
        ("엑시트(Exit)", "유동성 이벤트: 인수, IPO, 또는 세컨더리 매각."),
        ("완전 희석(Fully Diluted)", "모든 옵션, 워런트, 전환 수단이 행사된 것으로 간주한 총 주식수."),
        ("리드 투자자(Lead Investor)", "조건을 설정하고 주요 DD를 수행하며 보통 이사 의석을 차지하는 투자자."),
        ("청산우선권(Liquidation Preference)", "매각 또는 청산 시 주주에 대한 지급 순서와 금액."),
        ("보호예수 기간(Lock-Up Period)", "IPO 후 내부자가 주식을 매각할 수 없는 기간(보통 180일)."),
        ("비희석적(Non-Dilutive)", "지분을 포기하지 않는 자금(보조금, 수익)."),
        ("옵션풀(Option Pool)", "향후 직원 지분 보상을 위해 예약된 주식."),
        ("동순위(Pari Passu)", "동등한 대우 -- 같은 클래스의 투자자가 수익을 동등하게 배분."),
        ("포스트머니(Post-Money)", "신규 투자를 포함한 기업 기치."),
        ("프리머니(Pre-Money)", "신규 투자 이전의 기업가치."),
        ("우선주(Preferred Stock)", "보통주 대비 추가 권리(청산우선권, 희석방지 등)가 있는 주식 클래스."),
        ("비례참여권(Pro-Rata Right)", "지분율 유지를 위해 향후 라운드에 참여할 수 있는 권리."),
        ("우선매수권(ROFR)", "주식에 대한 외부 제안을 회사가 매칭할 수 있는 권리."),
        ("런웨이(Runway)", "현재 소각율 기준 운영 가능한 잔여 개월수."),
        ("SAFE", "미래 지분에 대한 간단한 합의. 향후 프라이스드 라운드에서 주식으로 전환."),
        ("세컨더리 매각(Secondary Sale)", "주주 간 기존 주식(신규 발행 아닌)의 매각."),
        ("동반매도참여권(Tag-Along)", "소수 주주가 동일 조건으로 매각에 참여할 수 있는 권리."),
        ("텀시트(Term Sheet)", "핵심 투자 조건의 비구속력 개요."),
        ("베스팅(Vesting)", "시간에 걸친 점진적 지분 획득(보통 직원/창업자 4년)."),
    ]

    for label, definition in terms:
        pdf.bullet(definition, f"{label}: ")

    # ── 파일 저장 ─────────────────────────────────
    path = os.path.join(OUT, "Investment_Fundraising_Guide_KO.pdf")
    pdf.output(path)
    print(f"PDF 생성 완료: {path}")
    return path


if __name__ == "__main__":
    build()
