#!/usr/bin/env python3
"""
Generate 510(k) Bridge 5-Year Business Strategy — Korean PDF
510k Bridge, Inc.
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

def _a(t):
    return t.translate(_MAP)


class StrategyKO(FPDF):
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
        self.cell(0, 8, _a("510(k) Bridge -- 5개년 사업 전략"), align="R", ln=True)
        self.ln(2)

    def footer(self):
        self.set_y(-15)
        self.set_font("CJK", "I", 8)
        self.set_text_color(*GRAY)
        self.cell(0, 10, _a(f"페이지 {self.page_no()}/{{nb}}"), align="C")

    def sec(self, num, title):
        self.set_font("CJK", "B", 16)
        self.set_text_color(*BLUE)
        self.cell(0, 10, _a(f"{num}. {title}"), new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(*BLUE)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(4)

    def sub(self, title):
        self.set_font("CJK", "B", 12)
        self.set_text_color(*TEXT)
        self.cell(0, 8, _a(title), new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def txt(self, text):
        self.set_font("CJK", "", 10)
        self.set_text_color(*TEXT)
        self.multi_cell(0, 6, _a(text), new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def bul(self, text):
        self.set_font("CJK", "", 10)
        self.set_text_color(*TEXT)
        self.multi_cell(0, 6, _a("  - " + text), new_x="LMARGIN", new_y="NEXT")

    def kv(self, key, val):
        self.set_font("CJK", "B", 10)
        self.set_text_color(*BLUE)
        self.cell(0, 6, _a(key), new_x="LMARGIN", new_y="NEXT")
        self.set_font("CJK", "", 10)
        self.set_text_color(*TEXT)
        self.multi_cell(0, 6, _a("  " + val), new_x="LMARGIN", new_y="NEXT")
        self.ln(1)


def build():
    pdf = StrategyKO()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()

    # -- 표지 --
    pdf.ln(30)
    pdf.set_font("CJK", "B", 28)
    pdf.set_text_color(*BLUE)
    pdf.cell(0, 14, "510(k) Bridge", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("CJK", "", 16)
    pdf.set_text_color(*TEXT)
    pdf.cell(0, 9, _a("5개년 사업 전략"), align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(6)
    pdf.set_font("CJK", "I", 11)
    pdf.set_text_color(*GRAY)
    pdf.cell(0, 7, "510k Bridge", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 7, "510k Bridge, Inc.", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 7, _a("버전 3.0 | 2026년 4월"), align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(20)
    pdf.set_font("CJK", "", 10)
    pdf.set_text_color(*TEXT)
    pdf.multi_cell(0, 6, _a(
        "본 문서는 510k Bridge가 미국 FDA 510(k) 인허가를 추진하는 "
        "중국 및 한국 의료기기 기업을 위한 선도적인 SaaS 플랫폼 및 "
        "전문 서비스 파트너로 성장하기 위한 5개년 전략을 개괄합니다."
    ), align="C")

    # -- 1. 경영 요약 --
    pdf.add_page()
    pdf.sec(1, "경영 요약")
    pdf.txt(
        "510k Bridge는 FDA 510(k) 경로를 통해 미국 시장에 진출하는 "
        "중국 및 한국 의료기기 기업을 대상으로 5개의 상호 보완적인 "
        "SaaS 제품과 전문 서비스를 운영합니다.\n\n"
        "핵심 제품:\n"
        "  1. Control Tower -- 510(k) 프로그램 프로젝트 관리 대시보드\n"
        "  2. 510(k) Predicate Finder -- FDA 데이터베이스 검색, "
        "선행기기 체인 추적, 실질적 동등성 논증 생성\n"
        "  3. FDA 가이던스 문서 라이브러리 -- 600개 이상의 CDRH "
        "가이던스 문서 검색 가능\n"
        "  4. QMS-Lite 스타트업용 -- 21 CFR 820 / ISO 13485에 "
        "부합하는 경량 품질관리 시스템\n"
        "  5. 국경간 법인 설립 추적기 -- 미국 시장 진출 체크리스트 대시보드\n\n"
        "통합 제품군은 규제 연구(가이던스 문서), 선행기기 전략(Predicate Finder), "
        "품질 관리(QMS-Lite), 실행 관리(Control Tower), "
        "미국 법인 설립(법인 설립 추적기)의 전체 라이프사이클을 커버합니다. "
        "전문 서비스는 직접적인 규제 및 프로젝트 관리 지원이 필요한 "
        "고객을 위한 부가가치 레이어입니다.")

    # -- 2. 시장 기회 --
    pdf.add_page()
    pdf.sec(2, "시장 기회")
    pdf.txt(
        "중국 의료기기 산업은 세계 2위(2025년 800억 달러 이상)이며 "
        "연 15-20% 성장 중입니다. 한국 의료기기 시장은 70억 달러를 "
        "초과하며 수출 성장이 강력합니다. 매년 300개 이상의 중국 기업과 "
        "100개 이상의 한국 기업이 미국 시장 진출을 시도하며, "
        "대부분 510(k) 경로를 FDA 인허가의 가장 빠른 루트로 선택합니다.\n\n"
        "이들 기업이 직면하는 주요 과제:\n"
        "  1. 미국 규제 프로세스 미숙 -- 510(k)는 NMPA/MFDS와 크게 다름\n"
        "  2. 선행기기 선택 -- 잘못된 선행기기가 FDA 거부의 1순위 원인\n"
        "  3. 언어 및 문화 장벽 -- 대부분의 FDA 가이던스는 영어 전용\n"
        "  4. 프로젝트 관리 공백 -- 다년간 규제 프로그램은 구조 없이 실패\n"
        "  5. 미국 법인 설립 및 투자자 관계 -- EB-1/E-2 비자, 델라웨어 LLC, 은행 업무")

    pdf.sub("2.1 서비스 가능 시장")
    pdf.txt(
        "  총 접근 가능 시장 (TAM): 42억 달러 (글로벌 규제 SaaS + 서비스)\n"
        "  서비스 가능 접근 시장 (SAM): 4.2억 달러 (중국/한국 기기 기업, 미국 510(k))\n"
        "  획득 가능 서비스 시장 (SOM): 5년차 840만 달러 (20 고객, 평균 3.5만 달러)")

    pdf.sub("2.2 경쟁 환경")
    pdf.txt(
        "  Greenlight Guru -- QMS + 설계 제어. $30K/년. 다국어 없음, 선행기기 도구 없음.\n"
        "  MasterControl -- 엔터프라이즈 QMS. $100K+/년. 510(k) 단계 스타트업에 과도함.\n"
        "  Qualio -- 클라우드 QMS. $20K/년. PM 대시보드 없음, 아시아 시장 미집중.\n"
        "  규제 컨설턴트 -- $300-500/시간. 분산적, 도구 없음.\n"
        "  이민/기업 변호사 -- 법인 설립당 $5-15K. 이메일 기반, 대시보드 없음.\n\n"
        "이 경쟁사들 중 3개 국어(EN/CN/KO) 플랫폼을 제공하며 "
        "PM 대시보드, 선행기기 연구, QMS, 법인 설립 추적, SE 논증 생성을 "
        "결합한 곳은 없습니다. 완전한 QMS 시스템은 연 $30K-$100K이며 "
        "구현에 수개월 소요 -- 스타트업은 FDA 감사를 통과할 정도의 QMS만 "
        "필요하며, 이것이 QMS-Lite의 기회입니다.")

    # -- 3. 제품 포트폴리오 --
    pdf.add_page()
    pdf.sec(3, "제품 포트폴리오")

    pdf.sub("3.1 Control Tower PM 대시보드")
    pdf.txt(
        "Vite + TypeScript 기반 SaaS 애플리케이션, Supabase 백엔드:\n\n"
        "  15개 탭: 이중 트랙 마일스톤, 게이트 시스템, 위험 대시보드, "
        "규제 추적기, 감사 추적, 문서 제어, 조치 항목(DHF/DMR/CAPA), "
        "타임라인, 예산, 현금/런웨이, 미국 투자, 리소스, "
        "공급업체, 메시지 보드, FDA 통신\n\n"
        "  Supabase RLS 멀티테넌트 아키텍처\n"
        "  3개 국어 EN/CN/KO 인터페이스, 원클릭 전환\n"
        "  역할 기반 접근 제어: PMP, 기술, 사업, 회계\n"
        "  7개 사전 구축 기기 카테고리 템플릿\n"
        "  설정 마법사로 가이드 프로젝트 구성")

    pdf.sub("3.2 510(k) Predicate Finder")
    pdf.txt(
        "독립형 SaaS 도구 (Vite + TypeScript, Tailwind CSS), "
        "FDA openFDA 510(k) 데이터베이스 검색:\n\n"
        "  데이터베이스 검색 -- 제품 코드, 신청자, 기기명, K-번호로 조회\n"
        "  고급 필터 -- 연도 범위, 결정 유형(SE/NSE), 심사 유형\n"
        "  기기 상세 -- 선행기기 참조가 포함된 완전한 510(k) 기록\n"
        "  선행기기 체인 -- 최대 5단계까지 역추적\n"
        "  기기 비교 -- 최대 4개 기기 병렬 비교\n"
        "  SE 논증 생성기 -- 실질적 동등성 논증 초안 자동 생성\n"
        "  3개 국어 EN/CN/KO -- 전체 인터페이스 번역\n\n"
        "프리미엄 모델:\n"
        "  무료 -- 일 5회 검색, 일 1회 체인 추적, 2기기 비교\n"
        "  Pro (이메일 게이트) -- 무제한 검색, 전체 체인, "
        "4기기 비교, SE 논증, PDF 내보내기\n\n"
        "Predicate Finder는 주요 리드 자석 역할: 무료 사용자가 "
        "이메일을 제공하여 프리미엄 기능을 해제하면 Control Tower 및 "
        "전문 서비스의 영업 퍼널에 진입합니다.")

    pdf.sub("3.3 QMS-Lite 스타트업용")
    pdf.txt(
        "510(k) 단계 스타트업을 위한 경량 품질관리 시스템으로, "
        "완전한 플랫폼의 연 $30K-$100K 비용 없이 FDA 감사를 통과할 수 "
        "있는 수준의 QMS를 제공합니다.\n\n"
        "모듈 (21 CFR 820 / ISO 13485 정렬):\n"
        "  문서 제어 -- 버전 관리 SOP, 작업 지시서, 양식\n"
        "  CAPA -- 시정 및 예방 조치 추적, 근본 원인 분석\n"
        "  교육 기록 -- 직원 교육 매트릭스, 서명 추적, 역량 로그\n"
        "  공급업체 자격 -- 승인 공급업체 목록, 감사 일정, 스코어카드\n"
        "  불만 처리 -- 고객 불만 접수, 조사, 추세 분석\n\n"
        "시장: 모든 510(k) 신청자에게 QMS가 필요하며 대부분 스프레드시트를 사용 중.\n"
        "가격: 회사당 $200-$500/월 (vs. Greenlight Guru / MasterControl의 $2.5K-$8K/월).\n"
        "모듈의 절반은 이미 Control Tower 탭으로 존재 (문서 제어, 조치/CAPA, 공급업체).")

    pdf.sub("3.4 국경간 법인 설립 추적기")
    pdf.txt(
        "미국 사업을 설립하는 중국/한국 기업을 위한 대시보드. "
        "현재 이러한 프로세스는 모두 변호사와의 이메일 체인으로 처리되며 "
        "전용 도구가 없습니다.\n\n"
        "체크리스트 모듈:\n"
        "  델라웨어 C-Corp 설립 -- 정관, 부속 정관, EIN\n"
        "  오레곤 주 등록 -- 외국 법인 등록, 사업 허가\n"
        "  등록 대리인 -- 임명 및 연간 갱신 추적\n"
        "  미국 은행 계좌 -- 신청 상태, 서명권자 요건\n"
        "  FDA 시설 등록 -- 시설 등록, 기기 목록\n"
        "  미국 대리인 임명 -- FDA 요구 미국 대리인 지정\n"
        "  라벨링 준수 -- 21 CFR 801 요건 체크리스트\n"
        "  주별 영업 허가 -- 주별 허가 및 갱신\n"
        "  보험 -- 제조물 책임, 일반 책임, D&O\n\n"
        "가격: $1K-$5K 일회성 설립 또는 $200/월 SaaS.\n"
        "수익 부스터: 이민 변호사, 법인 서비스 제공업체, 등록 대리인 "
        "회사와의 추천 파트너십.\n\n"
        "향후 확장: 중국 WFOE 체크리스트 모듈 -- 미국 운영을 설립하는 "
        "일부 중국 클라이언트는 중국 자회사도 필요로 하여 "
        "(미국 모회사에 중국 법인 필요) 중국 회사 설립 대행사와의 "
        "추천 파트너십 기회 창출.")

    pdf.sub("3.5 FDA 가이던스 문서 라이브러리")
    pdf.txt(
        "600개 이상의 CDRH(기기 및 방사선 건강 센터) 가이던스 문서에 "
        "즉시 접근할 수 있는 검색 가능한 싱글 페이지 애플리케이션.\n\n"
        "기능:\n"
        "  전체 가이던스 문서 제목 및 설명에 대한 전문 검색\n"
        "  최종본, 초안, 철회 상태별 필터\n"
        "  FDA 원본 문서 직접 링크\n"
        "  3개 국어 EN/CN/KO 인터페이스\n"
        "  510kbridge.com에 무료 리소스로 임베드\n\n"
        "전략적 가치: 510k Bridge를 규제 참고 플랫폼으로 포지셔닝. "
        "가이던스 문서를 탐색하는 모든 방문자는 Predicate Finder Pro, "
        "Control Tower 및 전문 서비스의 잠재 리드입니다. "
        "이 라이브러리는 높은 의도의 규제 키워드에 대한 유기적 SEO 트래픽을 주도합니다.")

    pdf.sub("3.6 리드 자석 및 콘텐츠")
    pdf.txt(
        "  스탠퍼드 PMP 과정 -- 무료 전문 역량 개발 제공 (EN + CN + KO)\n"
        "  FDA 510(k) 경로 가이드 -- 브랜드 PDF (EN + CN + KO)\n"
        "  미국 시장 진출 체크리스트 -- LLC 설립, FDA 등록, 라벨링, QSR\n"
        "  중국어 및 한국어 웨비나 -- Control Tower 라이브 데모, 게이트 리플레이\n"
        "  WeChat 공식 계정 -- 중국 시장 콘텐츠 배포\n"
        "  KakaoTalk / Naver -- 한국 시장 콘텐츠 배포")

    # -- 4. 수익 모델 --
    pdf.add_page()
    pdf.sec(4, "수익 모델")

    pdf.sub("4.1 SaaS 등급")
    pdf.txt(
        "  Predicate Finder 무료 -- $0 (리드 생성, 이메일 수집)\n"
        "  Predicate Finder Pro -- $99/월 (무제한 검색, SE 논증, PDF 내보내기)\n"
        "  Control Tower Starter -- $500/월 (프로젝트당 읽기 전용 대시보드)\n"
        "  Control Tower Growth -- $1,000/월 (전체 대시보드, 2 프로젝트, 메시지 보드)\n"
        "  Control Tower Scale -- $2,000/월 (멀티 프로젝트, Predicate Finder 임베드, "
        "FDA 통신)\n"
        "  QMS-Lite Starter -- $200/월 (문서 제어, CAPA, 교육 기록)\n"
        "  QMS-Lite Pro -- $500/월 (전체 제품군 포함 공급업체 자격, 불만 처리)\n"
        "  법인 설립 추적기 -- $200/월 SaaS 또는 $1K-$5K 일회성 설립")

    pdf.sub("4.2 전문 서비스")
    pdf.txt(
        "  규제 컨설팅 -- $250-500/시간 수시\n"
        "  프로젝트 관리 리테이너 -- $10-25K/월 (고객의 Control Tower 운영)\n"
        "  엔터프라이즈 참여 -- 프로젝트당 $50-200K+ "
        "(엔드투엔드: 규제 전략 + PM + 공급업체 관리 + 미국 법인 설립)")

    pdf.sub("4.3 5개년 매출 전망")
    pdf.txt(
        "  1년차 -- 제품 출시 + 3 고객 = $240K ARR\n"
        "    Predicate Finder: 500 무료 사용자, 20 Pro ($24K)\n"
        "    Control Tower: 3 Starter 고객 ($18K)\n"
        "    법인 설립: 5건 일회성 설립, 평균 $3K ($15K)\n"
        "    QMS-Lite: 3 Starter 고객 ($7K, 부분 연도)\n"
        "    서비스: 1건 리테이너 $10K/월 ($120K) + 수시 ($18K)\n"
        "    추천 수수료: 이민/법인 ($38K)\n\n"
        "  2년차 -- 시장 검증 + 8 고객 = $780K ARR\n"
        "    Predicate Finder: 2,000 무료 사용자, 80 Pro ($95K)\n"
        "    Control Tower: 3 Starter + 4 Growth + 1 Scale ($102K)\n"
        "    QMS-Lite: 15 고객 평균 $300/월 ($54K)\n"
        "    법인 설립: 20건 설립 + 10 SaaS ($86K)\n"
        "    서비스: 3건 리테이너 ($360K) + 수시 ($43K)\n"
        "    추천 수수료 ($40K)\n\n"
        "  3년차 -- 성장 단계 + 15 고객 = $2.1M ARR\n"
        "    Predicate Finder: 5,000 무료 사용자, 200 Pro ($238K)\n"
        "    Control Tower: 5 Starter + 6 Growth + 4 Scale ($198K)\n"
        "    QMS-Lite: 40 고객 평균 $350/월 ($168K)\n"
        "    법인 설립: 40건 설립 + 25 SaaS ($170K)\n"
        "    서비스: 6건 리테이너 ($900K) + 컨설팅 ($264K)\n"
        "    추천 수수료 ($62K)\n\n"
        "  4년차 -- 규모 확대 + 30 고객 = $4.5M ARR\n"
        "    Predicate Finder: 10,000 무료, 500 Pro ($594K)\n"
        "    Control Tower: 10 Starter + 12 Growth + 8 Scale ($396K)\n"
        "    QMS-Lite: 80 고객 평균 $400/월 ($384K)\n"
        "    법인 설립: 60건 설립 + 40 SaaS ($220K)\n"
        "    서비스: 10건 리테이너 ($1.8M) + 엔터프라이즈 ($710K)\n"
        "    추천 수수료 ($96K) + QMS 업셀 ($300K)\n\n"
        "  5년차 -- 시장 리더 + 50 고객 = $10.8M ARR\n"
        "    Predicate Finder: 20,000 무료, 1,000 Pro ($1.2M)\n"
        "    Control Tower: 15 Starter + 20 Growth + 15 Scale ($690K)\n"
        "    QMS-Lite: 150 고객 평균 $420/월 ($756K)\n"
        "    법인 설립: 100건 설립 + 60 SaaS ($360K)\n"
        "    서비스: 15건 리테이너 ($3.6M) + 엔터프라이즈 ($2.9M)\n"
        "    추천 수수료 ($150K) + QMS 업셀 ($1.1M)")

    # -- 5. 시장 진출 전략 --
    pdf.add_page()
    pdf.sec(5, "시장 진출 전략")

    pdf.sub("5.1 퍼널: 무료 -> SaaS -> 서비스")
    pdf.txt(
        "  1단계 -- Predicate Finder(무료)로 규제 전문가 유치\n"
        "  2단계 -- 이메일 게이트로 리드 확보, 510(k) 가이드 + PMP 과정 제공\n"
        "  3단계 -- 활발한 신청을 진행하는 파워 유저를 위한 Pro 업그레이드 ($99/월)\n"
        "  4단계 -- 다개월 프로그램을 관리하는 팀을 위한 Control Tower 데모\n"
        "  5단계 -- 직접 지원이 필요한 고객을 위한 전문 서비스 참여\n\n"
        "전환 목표: 무료 -> Pro: 5% | Pro -> CT 시험: 15% | 시험 -> 유료: 30%")

    pdf.sub("5.2 중국 및 한국 시장 채널")
    pdf.txt(
        "  WeChat 공식 계정 -- 주요 콘텐츠 배포(중국)\n"
        "  중국 의료기기 액셀러레이터 (선전, 쑤저우, 항저우 바이오파크)\n"
        "  한국 의료기기 클러스터 (원주, 대구, 판교)\n"
        "  미국 이민 변호사 (EB-1/E-2 비자 고객의 FDA 경로 필요)\n"
        "  CRO 및 시험 연구소 (UL, TUV, Intertek) -- 추천 파트너십\n"
        "  산업 협회: CBIA, AdvaMed, RAPS, KMDIA -- 강연 활동\n"
        "  LinkedIn + 3개 국어 블로그 콘텐츠\n"
        "  중국어 및 한국어 웨비나, 게이트 리플레이\n"
        "  KakaoTalk / Naver 블로그 -- 한국 시장 콘텐츠 배포")

    pdf.sub("5.3 SEO 및 디지털")
    pdf.txt(
        "  롱테일 EN: 'FDA 510(k) process for Chinese company'\n"
        "  롱테일 CN: 'FDA 510(k) shenqing liucheng' (신청 절차)\n"
        "  롱테일 KO: 'FDA 510(k) 신청 절차'\n"
        "  도메인: 510kbridge.com + .cn + .kr\n"
        "  3개 국어 랜딩 페이지, Control Tower 라이브 데모 임베드")

    # -- 6. 기술 로드맵 --
    pdf.add_page()
    pdf.sec(6, "기술 로드맵")

    pdf.sub("6.1 1년차 (2026)")
    pdf.txt(
        "  Q1 -- Control Tower v1.1: DMR 추적기, FDA 통신 탭, 메시지 보드\n"
        "  Q1 -- FDA 가이던스 문서 라이브러리 (600+ CDRH 문서, 3개 국어)\n"
        "  Q1 -- 모든 제품에 한국어 지원 추가\n"
        "  Q2 -- Predicate Finder 출시, 프리미엄 게이팅\n"
        "  Q2 -- 510k Bridge 웹사이트 출시 (510kbridge.com)\n"
        "  Q3 -- Control Tower 멀티테넌트 (Supabase RLS 고객별)\n"
        "  Q3 -- 국경간 법인 설립 추적기 v1 (DE C-Corp, OR, WA 등록)\n"
        "  Q4 -- Predicate Finder Pro: PDF 내보내기, 대량 비교, 저장 검색\n"
        "  Q4 -- QMS-Lite MVP: 문서 제어 + CAPA 모듈")

    pdf.sub("6.2 2년차 (2027)")
    pdf.txt(
        "  Q1 -- QMS-Lite: 교육 기록 + 공급업체 자격 모듈\n"
        "  Q1 -- 법인 설립 추적기: 은행 계좌 + FDA 등록 워크플로\n"
        "  Q2 -- QMS-Lite: 불만 처리 + 완전한 21 CFR 820 정렬\n"
        "  Q2 -- Predicate Finder를 Control Tower Scale 탭으로 임베드\n"
        "  Q3 -- AI 규제 갭 분석: generate_regulatory_analysis.py를 셀프서비스로 노출\n"
        "  Q3 -- 법인 설립 추천 파트너 포털 (변호사, CSP)\n"
        "  Q4 -- API 통합: Supabase Edge Functions 자동 알림\n"
        "  Q4 -- QMS-Lite + Control Tower 통합 대시보드")

    pdf.sub("6.3 3-5년차 (2028-2030)")
    pdf.txt(
        "  일반 선행기기 카테고리 템플릿 라이브러리 "
        "(호흡기, 심혈관, 정형외과, IVD, 영상, 재활, SaMD)\n"
        "  QMS-Lite ISO 13485 감사 준비 보고서 생성기\n"
        "  법인 설립 추적기: 자동 주별 신고 + 연간 갱신 알림\n"
        "  모바일 앱, 이동 중 프로젝트 모니터링\n"
        "  De Novo 및 PMA 경로 확장\n"
        "  EU MDR / CE 마킹 모듈 (FDA 이상 확장)\n"
        "  규제 컨설팅 회사를 위한 화이트 라벨 옵션")

    # -- 7. 조직 계획 --
    pdf.add_page()
    pdf.sec(7, "조직 계획")

    pdf.sub("7.1 회사 구조")
    pdf.txt(
        "  운영 법인: 510k Bridge, Inc. (델라웨어 법인)\n"
        "  계약 및 송장: '510k Bridge, Inc.'")

    pdf.sub("7.2 팀 (1년차)")
    pdf.txt(
        "  창립자 / CEO -- 사업 개발, 제품 비전, 규제 전략,\n"
        "    소프트웨어 개발, 프론트엔드/백엔드 유지보수\n"
        "  영업 / BD (중국 및 한국) -- WeChat, KakaoTalk, 액셀러레이터 관계")

    pdf.sub("7.3 채용 계획 (2-5년차)")
    pdf.txt(
        "  2년차: 전임 개발자, 규제 담당, 영업 리드\n"
        "  3년차: 제품 책임자, 추가 개발자 2명, 고객 성공\n"
        "  4년차: VP 영업, 규제 팀 (3명), 마케팅 리드\n"
        "  5년차: COO, 엔지니어링 확대 (8명), 엔터프라이즈 영업 팀")

    # -- 8. 재무 계획 --
    pdf.add_page()
    pdf.sec(8, "재무 계획")

    pdf.sub("8.1 창업 비용")
    pdf.txt(
        "  도메인 등록 (510kbridge.com) -- $10/년\n"
        "  CloudFlare Pages 호스팅 -- $0 (무료 티어)\n"
        "  Supabase -- $0 무료 티어 (규모 확대 시 $25/월)\n"
        "  개발 도구 -- $0 (오픈 소스 스택)\n"
        "  법률 (계약 템플릿, 중국에서 준비) -- $500\n"
        "  초기 마케팅 (WeChat, LinkedIn, 중국 기반) -- $1,500\n"
        "  1년차 총 창업 비용: ~$2,500")

    pdf.sub("8.2 운영 비용 (월간, 1년차)")
    pdf.txt(
        "  클라우드 호스팅 -- $25/월\n"
        "  SaaS 도구 (이메일, CRM) -- $50/월\n"
        "  마케팅 (중국 기반) -- $200/월\n"
        "  합계: ~$275/월 = $3,300/년")

    pdf.sub("8.3 손익분기점 분석")
    pdf.txt(
        "  월 비용: $275\n"
        "  필요 매출: 1개 CT Starter ($500) = $500/월로 운영비 커버\n"
        "  손익분기점: 첫 유료 고객으로 1-2개월차\n"
        "  목표 매출총이익률: 85% (SaaS) / 65% (서비스)")

    # -- 9. 위험 요인 --
    pdf.add_page()
    pdf.sec(9, "위험 요인")
    pdf.txt(
        "  1. 시장 수용 -- 중국 및 한국 기업이 현지 컨설턴트를 선호할 수 있음\n"
        "     완화: 3개 국어 플랫폼, WeChat/KakaoTalk 존재, 현지 BD\n\n"
        "  2. FDA 규제 변경 -- 새로운 제출 요건\n"
        "     완화: 모듈식 아키텍처, 빠른 템플릿 업데이트\n\n"
        "  3. 경쟁 -- Greenlight Guru 또는 Qualio가 아시아 언어 지원 추가\n"
        "     완화: 선발 주자 우위, 선행기기 도구 차별화\n\n"
        "  4. 단일 창업자 위험 -- 핵심 인물 의존\n"
        "     완화: 문서화된 코드베이스, 모듈식 아키텍처, 조기 채용\n\n"
        "  5. openFDA API 변경 -- 요율 제한 또는 데이터 형식 변경\n"
        "     완화: 로컬 캐싱, FDA 510(k) 데이터베이스 다운로드로 대체\n\n"
        "  6. QMS 규제 변화 -- 21 CFR 820과 ISO 13485 조화\n"
        "     완화: 모듈식 QMS 설계, 템플릿 기반 컴플라이언스 업데이트\n\n"
        "  7. 주 등록 복잡성 -- 50개 주의 상이한 요건\n"
        "     완화: DE/OR/WA에서 시작, 고객 수요에 따라 확장")

    # -- 10. 마일스톤 및 KPI --
    pdf.add_page()
    pdf.sec(10, "마일스톤 및 KPI")

    pdf.sub("10.1 1년차 마일스톤")
    pdf.txt(
        "  Q1 -- Control Tower v1.1 출시, Predicate Finder MVP\n"
        "  Q2 -- 510kbridge.com 오픈, 최초 100명 Predicate Finder 사용자\n"
        "  Q3 -- 첫 CT 유료 고객, 첫 전문 서비스 리테이너\n"
        "  Q3 -- 법인 설립 추적기 v1 오픈 (DE/OR/WA)\n"
        "  Q4 -- QMS-Lite MVP 오픈 (문서 제어 + CAPA)\n"
        "  Q4 -- 500 PF 무료 사용자, 3 CT 고객, $20K MRR")

    pdf.sub("10.2 핵심 성과 지표")
    pdf.txt(
        "  Predicate Finder 무료 등록 (목표: 1년차 500 / 5년차 20,000)\n"
        "  PF 무료 -> Pro 전환률 (목표: 5%)\n"
        "  Control Tower 유료 고객 (목표: 1년차 3 / 5년차 50)\n"
        "  QMS-Lite 유료 고객 (목표: 1년차 3 / 5년차 150)\n"
        "  법인 설립 완료 수 (목표: 1년차 5 / 5년차 100)\n"
        "  월간 반복 매출 (목표: 1년차 $20K / 5년차 $900K)\n"
        "  전문 서비스 매출 (목표: 1년차 $140K / 5년차 $6.5M)\n"
        "  순추천지수 (목표: 50+)\n"
        "  고객 유지율 (목표: 90%+)")

    pdf.sub("10.3 출구 전략")
    pdf.txt(
        "  QMS 벤더에 의한 전략적 인수 (Greenlight Guru, Qualio, MasterControl)\n"
        "  사모 펀드의 규제 기술 플랫폼 롤업\n"
        "  $5-11M ARR, 75% 매출총이익률의 라이프스타일 비즈니스로 지속")

    # -- 11. 중국 WFOE 전략 --
    pdf.add_page()
    pdf.sec(11, "중국 WFOE 전략")

    pdf.sub("11.1 중국 WFOE가 올바른 선택인가?")
    pdf.txt(
        "중국 WFOE(외상독자기업)는 초기 단계에서 명확한 필요가 아니며 "
        "1-2년차에는 시기상조일 수 있습니다. "
        "510k Bridge의 고객은 미국으로 진출하는 중국 기업이지 -- "
        "중국 국내에서 판매하는 미국 기업이 아닙니다. "
        "수익 모델은 달러 표시 SaaS + 전문 서비스 계약입니다. "
        "중국 고객에게 판매하거나, 위챗 계정을 운영하거나, "
        "중국 BD 인력을 고용하는 데 중국 법인이 필요하지 않습니다.\n\n"
        "WFOE가 관련되는 경우:\n"
        "  - 중국 급여에서 직접 직원 고용 희망 (EOR 대신)\n"
        "  - 회계상 발표(파피아오)가 필요한 기업 고객에게 "
        "중국 부가세 세금계산서 발행 필요\n"
        "  - 중국 정부 보조금, 바이오파크 보조금, 자유무역지대 혜택 추구\n"
        "  - 위안화 수금을 위한 중국 은행 계좌 개설 희망")

    pdf.sub("11.2 더 경제적인 대안 (1-2년차)")
    pdf.txt(
        "EOR/PEO (명의상 고용주)\n"
        "'영업 / BD (중국)' 채용의 경우, Velocity Global, Deel, Atlas 같은 "
        "EOR을 통해 법인 설립 없이 합법적으로 중국 직원을 고용할 수 있습니다. "
        "비용: 급여 외에 직원당 월 약 $300-$600 관리비. "
        "$2,500 창업 예산을 고려할 때 1년차에는 거의 확실히 올바른 선택입니다.\n\n"
        "WeChat 공식 계정\n"
        "WFOE 없이 외국 기업으로 등록 가능합니다. "
        "중국 사업 허가증 또는 외국 회사 등록 증명서가 필요합니다. "
        "델라웨어 C-corp 문서(아포스티유 인증)로 충분할 수 있으며, "
        "계정 유형에 따라 다릅니다.")

    pdf.sub("11.3 WFOE가 필요한 시점")
    pdf.txt(
        "아마도 3년차 이후, 파피아오를 요구하는 기업 고객, "
        "위안화 리테이너 수익, 또는 중국 내 3명 이상의 팀이 있을 때. "
        "그 시점에서 예산:\n\n"
        "  대행/설립 비용 (서비스형 WFOE):              $2,500 - $5,000\n"
        "  등록 주소 (가상, 경제 구역):                  $500 - $1,500/년\n"
        "  문서 공증 (DE C-corp 아포스티유):              $500 - $1,000\n"
        "  회사 도장:                                    ~$200\n"
        "  지속 회계/컴플라이언스:                        $2,000 - $4,000/년\n"
        "  WFOE 1년차 총계:                              ~$6,000 - $12,000\n\n"
        "등록 자본금 약정: 1선 도시 서비스형 WFOE에 적합한 금액으로 "
        "인민폐 50만-100만 (약 $70K-$140K), 5년에 걸쳐 납입.")

    pdf.sub("11.4 전략적 제품 기회")
    pdf.txt(
        "국경간 법인 설립 추적기(3.4절)는 이미 고객의 델라웨어 C-Corp, "
        "OR, WA 등록을 다루고 있습니다. 자연스러운 확장은 중국 WFOE "
        "체크리스트 모듈을 추가하는 것입니다 -- 미국 운영을 설립하는 일부 "
        "중국 클라이언트는 반대 질문도 가질 것입니다 "
        "(미국 모회사에 중국 자회사 필요). "
        "이는 중국 회사 설립 대행사와의 추천 파트너십 기회를 만들어, "
        "미국 이민 변호사 추천 모델을 미러링합니다.")

    path = os.path.join(OUT_DIR, "510kBridge_5Year_Business_Strategy_KO.pdf")
    pdf.output(path)
    return path


if __name__ == "__main__":
    p = build()
    print(f"Generated: {p}")
