#!/usr/bin/env python3
"""Generate Project Charter PDFs (English + Chinese) for the
ICU Respiratory Digital Twin System."""

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

# ── ASCII-safe helper for Helvetica ──
_CHAR_MAP = str.maketrans({
    "\u2014": "--", "\u2013": "-", "\u2022": "*",
    "\u2018": "'", "\u2019": "'", "\u201c": '"', "\u201d": '"',
    "\u2265": ">=", "\u2264": "<=", "\u00b5": "u", "\u00d7": "x",
})
def _a(s: str) -> str:
    return s.translate(_CHAR_MAP)


# ════════════════════════════════════════
#  ENGLISH VERSION (Helvetica)
# ════════════════════════════════════════

class EnglishCharter(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(*GRAY)
        self.cell(0, 5, _a("ICU Respiratory Digital Twin -- Project Charter  |  CONFIDENTIAL"), align="R")
        self.ln(7)

    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(*GRAY)
        self.cell(0, 5, f"Page {self.page_no()}/{{nb}}", align="C")

    def sec(self, title):
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(*BLUE)
        self.cell(0, 7, _a(title), new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(*BLUE)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(2)

    def txt(self, text, bold=False):
        self.set_font("Helvetica", "B" if bold else "", 9)
        self.set_text_color(*TEXT)
        self.multi_cell(0, 4.5, _a(text), new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def bul(self, text):
        self.set_font("Helvetica", "", 9)
        self.set_text_color(*TEXT)
        x = self.get_x()
        self.cell(5, 4.5, _a("*"))
        self.multi_cell(0, 4.5, _a(text), new_x="LMARGIN", new_y="NEXT")

    def table_row(self, cols, widths, bold=False, header=False):
        line_h = 5.5
        if header:
            self.set_font("Helvetica", "B", 8)
            self.set_text_color(255, 255, 255)
            self.set_fill_color(*BLUE)
        elif bold:
            self.set_font("Helvetica", "B", 8)
            self.set_text_color(*TEXT)
            self.set_fill_color(245, 245, 248)
        else:
            self.set_font("Helvetica", "", 8)
            self.set_text_color(*TEXT)
            self.set_fill_color(255, 255, 255)
        # Calculate row height based on longest wrapped cell
        row_lines = 1
        for c, w in zip(cols, widths):
            n = self.multi_cell(w, line_h, _a(c), dry_run=True, output="LINES")
            if len(n) > row_lines:
                row_lines = len(n)
        row_h = line_h * row_lines
        # Page break if needed
        if self.get_y() + row_h > self.h - self.b_margin:
            self.add_page()
        x0 = self.get_x()
        y0 = self.get_y()
        for c, w in zip(cols, widths):
            x = self.get_x()
            self.rect(x, y0, w, row_h)
            self.set_fill_color(*([30, 90, 200] if header else [245, 245, 248] if bold else [255, 255, 255]))
            self.rect(x, y0, w, row_h, "F")
            self.rect(x, y0, w, row_h, "D")
            self.set_xy(x, y0)
            self.multi_cell(w, line_h, _a(c), border=0, fill=False)
            self.set_xy(x + w, y0)
        self.set_xy(x0, y0 + row_h)


def build_english():
    pdf = EnglishCharter()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=14)
    pdf.add_page()

    # ── Title block ──
    pdf.set_font("Helvetica", "B", 18)
    pdf.set_text_color(*BLUE)
    pdf.cell(0, 9, "PROJECT CHARTER", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(*TEXT)
    pdf.cell(0, 6, "ICU Respiratory Digital Twin System", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "I", 9)
    pdf.set_text_color(*GRAY)
    pdf.cell(0, 5, "sEMG Neural Drive + EIT Ventilation/Perfusion Monitoring Platform", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)

    # Meta info
    meta = [
        ("Project Sponsor:", "Company B USA"),
        ("Project Manager:", "Lon Dailey, PMP"),
        ("Date:", "March 21, 2026"),
        ("Document Version:", "1.0"),
    ]
    for label, val in meta:
        pdf.set_font("Helvetica", "B", 8)
        pdf.set_text_color(*GRAY)
        pdf.cell(35, 4.5, _a(label))
        pdf.set_font("Helvetica", "", 8)
        pdf.set_text_color(*TEXT)
        pdf.cell(0, 4.5, _a(val), new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)

    # ═══════════════════════════════════
    #  1. PROJECT PURPOSE / JUSTIFICATION
    # ═══════════════════════════════════
    pdf.sec("1. Project Purpose / Business Justification")
    pdf.txt(
        "Develop and obtain FDA 510(k) clearance for a novel ICU respiratory monitoring "
        "platform that combines surface electromyography (sEMG) neural respiratory drive "
        "measurement with electrical impedance tomography (EIT) ventilation/perfusion "
        "imaging. The system addresses a critical unmet clinical need: real-time, non-invasive "
        "assessment of patient-ventilator interaction to reduce ventilator-induced lung injury "
        "(VILI), shorten ventilator weaning time, and improve ICU outcomes.")
    pdf.txt(
        "The sEMG-first modular strategy enables early market entry (Module A, product code "
        "IKN) while the EIT module (Module B, product code DQS) undergoes parallel development, "
        "generating revenue to fund continued R&D. Company B USA holds all IP; Silan Technology "
        "(Chengdu) is the contract manufacturer.")

    # ═══════════════════════════════════
    #  2. MEASURABLE PROJECT OBJECTIVES
    # ═══════════════════════════════════
    pdf.sec("2. Measurable Project Objectives")
    objectives = [
        "Achieve FDA 510(k) clearance for sEMG module (Module A) by M+9 (Dec 2026)",
        "Achieve FDA 510(k) clearance for EIT module (Module B) by M+23 (Feb 2028)",
        "NRD detection sensitivity >= 92%, asynchrony specificity >= 88%, signal latency < 50 ms",
        "V/Q separation accuracy > 85% vs. DCE-CT reference for EIT module",
        "ECG artifact suppression > 98% via proprietary ECG-gating algorithm",
        "Secure $2M Phase 1 seed funding by M+3 (Jun 2026)",
        "Complete IP transfer to Company B USA by M+2 (May 2026)",
        "Achieve ISO 13485 audit readiness at Silan Technology by M+2",
    ]
    for o in objectives:
        pdf.bul(o)
    pdf.ln(2)

    # ═══════════════════════════════════
    #  3. HIGH-LEVEL REQUIREMENTS
    # ═══════════════════════════════════
    pdf.sec("3. High-Level Requirements")
    reqs = [
        "sEMG module: 4-8 electrode array, 24-bit ADC (ADS1298), 2000 Hz, Bluetooth wireless isolation",
        "EIT module: 32-electrode thoracic belt, 50 kHz AC injection, 50 Hz frame rate",
        "MyoBus protocol: < 1 ms timestamp alignment, AES-256 encryption, RBAC, HL7 FHIR",
        "Compliance: IEC 60601-1, IEC 60601-1-2 (EMC), IEC 62304 (software), ISO 14971 (risk), "
        "ISO 10993 (biocompatibility), FDA Cybersecurity 2023 guidance",
        "Modular 510(k) submission: sEMG first (M+6), EIT second (M+17)",
        "Quality system: ISO 13485 at Silan Technology; US-based DHF per 21 CFR 820",
        "Data security: No cloud storage; all patient data local with audit trail",
    ]
    for r in reqs:
        pdf.bul(r)
    pdf.ln(2)

    # ═══════════════════════════════════
    #  4. HIGH-LEVEL PROJECT DESCRIPTION
    # ═══════════════════════════════════
    pdf.sec("4. High-Level Project Description / Key Deliverables")
    pdf.txt(
        "The project follows a dual-track approach: Technical Track (8 milestones: T1-T8) and "
        "Regulatory Track (9 milestones: R1-R9). Six decision gates (G1-G6) provide go/no-go "
        "checkpoints. The project spans 23 months from March 2026 to February 2028.")
    pdf.txt("Key Deliverables:", bold=True)
    deliverables = [
        "Finalized sEMG prototype with locked BOM and design specifications",
        "Complete 510(k) submission package for sEMG (Module A)",
        "EIT 32-electrode belt prototype with V/Q imaging capability",
        "Complete 510(k) submission package for EIT (Module B)",
        "MyoBus integrated platform with synchronized sEMG + EIT data streams",
        "Design History File (DHF) per 21 CFR 820 for both modules",
        "ISO 14971 risk management file with 8 tracked risks",
        "ISO 13485 compliant manufacturing at Silan Technology (Chengdu)",
    ]
    for d in deliverables:
        pdf.bul(d)
    pdf.ln(2)

    # ═══════════════════════════════════
    #  5. HIGH-LEVEL RISKS
    # ═══════════════════════════════════
    pdf.sec("5. High-Level Risks")
    w = [8, 82, 15, 65]
    pdf.table_row(["#", "Risk", "Level", "Mitigation"], w, header=True)
    risks = [
        ("R-004", "V/Q image misinterpretation -- wrong ventilator adjustment", "RED",
         "Label as investigational adjunct; clinician training"),
        ("R-007", "510(k) rejected -- predicate not accepted by FDA", "RED",
         "Pre-Sub meeting; De Novo fallback (+60 days)"),
        ("R-008", "Funding runway insufficient before sEMG clearance", "RED",
         "Phased funding; sEMG-first for early revenue"),
        ("R-001", "False-negative sEMG (missed apnea)", "YELLOW",
         "Dual-threshold algorithm + alarm; adjunct label"),
        ("R-005", "Cybersecurity breach / unauthorized access", "YELLOW",
         "AES-256; RBAC; FDA Cyber 2023 compliance"),
        ("R-002", "ECG artifact false positive", "YELLOW",
         "ECG-gating >98% suppression; visual verification"),
    ]
    for i, (rid, desc, lvl, mit) in enumerate(risks):
        pdf.table_row([rid, desc, lvl, mit], w, bold=(i < 3))
    pdf.ln(2)

    # ═══════════════════════════════════
    #  6. SUMMARY MILESTONE SCHEDULE
    # ═══════════════════════════════════
    pdf.sec("6. Summary Milestone Schedule")
    mw = [16, 70, 22, 62]
    pdf.table_row(["Month", "Milestone", "Track", "Key Criteria"], mw, header=True)
    milestones = [
        ("M+0", "Prototype finalized -- sEMG module", "Technical", "BOM locked; specs match Pre-Sub"),
        ("M+0", "Pre-Sub Q-Meeting request filed", "Regulatory", "Q-Sub to FDA CDRH"),
        ("M+1", "IP buyout & US legal structure", "Regulatory", "Patents transferred to Co. B USA"),
        ("M+2", "FDA Pre-Submission meeting", "Regulatory", "FDA feedback on SE strategy"),
        ("M+2", "ISO 13485 audit -- Silan Technology", "Regulatory", "Gap remediation complete"),
        ("M+3", "Bench & performance testing -- sEMG", "Technical", "IEC 60601-1, EMC, n>=30"),
        ("M+6", "510(k) submission -- sEMG (Module A)", "Regulatory", "Complete submission package"),
        ("M+8", "EIT prototype -- 32-electrode belt", "Technical", "50 kHz, 50 Hz frame rate"),
        ("M+9", "Expected 510(k) clearance -- sEMG", "Regulatory", "IKN product code clearance"),
        ("M+12", "V/Q algorithm validation", "Technical", ">85% accuracy vs. DCE-CT"),
        ("M+17", "510(k) submission -- EIT (Module B)", "Regulatory", "DQS product code"),
        ("M+23", "Expected 510(k) clearance -- EIT", "Regulatory", "Full platform commercial"),
    ]
    for m in milestones:
        pdf.table_row(list(m), mw)
    pdf.ln(3)

    # ── Signature block ──
    pdf.set_draw_color(*BLUE)
    pdf.set_line_width(0.4)
    pdf.line(pdf.l_margin, pdf.get_y(), pdf.w - pdf.r_margin, pdf.get_y())
    pdf.ln(3)
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(*TEXT)
    pdf.cell(0, 5, "AUTHORIZATION", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(1)
    pdf.set_font("Helvetica", "", 8)

    sigs = [
        ("Project Sponsor:", "________________________", "Company B USA"),
        ("Project Manager:", "________________________", "Lon Dailey, PMP"),
        ("Chief Technologist:", "________________________", "Dr. Dai"),
        ("CEO:", "________________________", "Lawrence Liu"),
    ]
    for role, line, name in sigs:
        pdf.set_font("Helvetica", "B", 8)
        pdf.set_text_color(*GRAY)
        pdf.cell(32, 4.5, _a(role))
        pdf.set_font("Helvetica", "", 8)
        pdf.set_text_color(*TEXT)
        pdf.cell(45, 4.5, _a(line))
        pdf.set_font("Helvetica", "I", 8)
        pdf.set_text_color(*GRAY)
        pdf.cell(40, 4.5, _a(name))
        pdf.set_text_color(*TEXT)
        pdf.cell(0, 4.5, _a("Date: ___________"), new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)

    path = os.path.join(OUT_DIR, "Project_Charter_EN.pdf")
    pdf.output(path)
    return path


# ════════════════════════════════════════
#  CHINESE VERSION (Arial Unicode / ARUNI)
# ════════════════════════════════════════

class ChineseCharter(FPDF):
    def __init__(self):
        super().__init__()
        font_path = "/Library/Fonts/Arial Unicode.ttf"
        self.add_font("ARUNI", "", font_path, uni=True)
        self.add_font("ARUNI", "B", font_path, uni=True)
        self.add_font("ARUNI", "I", font_path, uni=True)

    def header(self):
        self.set_font("ARUNI", "B", 8)
        self.set_text_color(*GRAY)
        self.cell(0, 5, "ICU呼吸监护数字孪生系统 — 项目章程  |  机密", align="R")
        self.ln(7)

    def footer(self):
        self.set_y(-12)
        self.set_font("ARUNI", "I", 7)
        self.set_text_color(*GRAY)
        self.cell(0, 5, f"第 {self.page_no()}/{{nb}} 页", align="C")

    def sec(self, title):
        self.set_font("ARUNI", "B", 11)
        self.set_text_color(*BLUE)
        self.cell(0, 7, title, new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(*BLUE)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(2)

    def txt(self, text, bold=False):
        self.set_font("ARUNI", "B" if bold else "", 9)
        self.set_text_color(*TEXT)
        self.multi_cell(0, 4.5, text, new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def bul(self, text):
        self.set_font("ARUNI", "", 9)
        self.set_text_color(*TEXT)
        self.cell(5, 4.5, "\u2022")
        self.multi_cell(0, 4.5, text, new_x="LMARGIN", new_y="NEXT")

    def table_row(self, cols, widths, bold=False, header=False):
        line_h = 5.5
        if header:
            self.set_font("ARUNI", "B", 8)
            self.set_text_color(255, 255, 255)
            self.set_fill_color(*BLUE)
        elif bold:
            self.set_font("ARUNI", "B", 8)
            self.set_text_color(*TEXT)
            self.set_fill_color(245, 245, 248)
        else:
            self.set_font("ARUNI", "", 8)
            self.set_text_color(*TEXT)
            self.set_fill_color(255, 255, 255)
        # Calculate row height based on longest wrapped cell
        row_lines = 1
        for c, w in zip(cols, widths):
            n = self.multi_cell(w, line_h, c, dry_run=True, output="LINES")
            if len(n) > row_lines:
                row_lines = len(n)
        row_h = line_h * row_lines
        # Page break if needed
        if self.get_y() + row_h > self.h - self.b_margin:
            self.add_page()
        x0 = self.get_x()
        y0 = self.get_y()
        for c, w in zip(cols, widths):
            x = self.get_x()
            self.set_fill_color(*([30, 90, 200] if header else [245, 245, 248] if bold else [255, 255, 255]))
            self.rect(x, y0, w, row_h, "F")
            self.rect(x, y0, w, row_h, "D")
            self.set_xy(x, y0)
            self.multi_cell(w, line_h, c, border=0, fill=False)
            self.set_xy(x + w, y0)
        self.set_xy(x0, y0 + row_h)


def build_chinese():
    pdf = ChineseCharter()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=14)
    pdf.add_page()

    # ── Title block ──
    pdf.set_font("ARUNI", "B", 18)
    pdf.set_text_color(*BLUE)
    pdf.cell(0, 9, "项 目 章 程", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("ARUNI", "", 11)
    pdf.set_text_color(*TEXT)
    pdf.cell(0, 6, "ICU呼吸监护数字孪生系统", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("ARUNI", "I", 9)
    pdf.set_text_color(*GRAY)
    pdf.cell(0, 5, "sEMG神经驱动 + EIT通气/灌注监测平台", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)

    meta = [
        ("项目发起人：", "B公司美国（Company B USA）"),
        ("项目经理：", "Lon Dailey, PMP"),
        ("日期：", "2026年3月21日"),
        ("文档版本：", "1.0"),
    ]
    for label, val in meta:
        pdf.set_font("ARUNI", "B", 8)
        pdf.set_text_color(*GRAY)
        pdf.cell(30, 4.5, label)
        pdf.set_font("ARUNI", "", 8)
        pdf.set_text_color(*TEXT)
        pdf.cell(0, 4.5, val, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)

    # ═══════════════════════════════════
    #  1. 项目目的/商业论证
    # ═══════════════════════════════════
    pdf.sec("1. 项目目的 / 商业论证")
    pdf.txt(
        "开发并获得FDA 510(k)许可，用于一款新型ICU呼吸监护平台。"
        "该平台结合表面肌电图(sEMG)神经呼吸驱动测量与电阻抗断层成像(EIT)"
        "通气/灌注成像。该系统解决了一个关键的未满足临床需求：实时、无创地评估"
        "患者-呼吸机交互，以减少呼吸机引起的肺损伤(VILI)，缩短呼吸机脱机时间，"
        "改善ICU治疗结果。")
    pdf.txt(
        "sEMG优先的模块化策略实现早期市场准入（模块A，产品代码IKN），"
        "同时EIT模块（模块B，产品代码DQS）并行开发，"
        "产生收入以资助持续研发。B公司美国持有所有知识产权；"
        "思澜科技（成都）为合同制造商。")

    # ═══════════════════════════════════
    #  2. 可量化的项目目标
    # ═══════════════════════════════════
    pdf.sec("2. 可量化的项目目标")
    objectives = [
        "在M+9（2026年12月）前获得sEMG模块（模块A）FDA 510(k)许可",
        "在M+23（2028年2月）前获得EIT模块（模块B）FDA 510(k)许可",
        "NRD检测灵敏度 ≥ 92%，异步特异性 ≥ 88%，信号延迟 < 50ms",
        "EIT模块V/Q分离准确度 > 85%（对比DCE-CT参考）",
        "通过专有ECG门控算法实现ECG伪影抑制 > 98%",
        "在M+3（2026年6月）前获得200万美元第一阶段种子融资",
        "在M+2（2026年5月）前完成知识产权转让至B公司美国",
        "在M+2前实现思澜科技ISO 13485审核就绪",
    ]
    for o in objectives:
        pdf.bul(o)
    pdf.ln(2)

    # ═══════════════════════════════════
    #  3. 高层级需求
    # ═══════════════════════════════════
    pdf.sec("3. 高层级需求")
    reqs = [
        "sEMG模块：4-8电极阵列，24位ADC(ADS1298)，2000Hz，蓝牙无线隔离",
        "EIT模块：32电极胸带，50kHz交流注入，50Hz帧率",
        "MyoBus协议：< 1ms时间戳对齐，AES-256加密，RBAC，HL7 FHIR",
        "合规：IEC 60601-1、IEC 60601-1-2(EMC)、IEC 62304(软件)、ISO 14971(风险)、"
        "ISO 10993(生物相容性)、FDA网络安全2023指南",
        "模块化510(k)提交：sEMG优先(M+6)，EIT其次(M+17)",
        "质量体系：思澜科技ISO 13485；美国DHF符合21 CFR 820",
        "数据安全：无云存储；所有患者数据本地化，带审计追踪",
    ]
    for r in reqs:
        pdf.bul(r)
    pdf.ln(2)

    # ═══════════════════════════════════
    #  4. 高层级项目描述
    # ═══════════════════════════════════
    pdf.sec("4. 高层级项目描述 / 关键可交付成果")
    pdf.txt(
        "项目采用双轨制：技术路径（8个里程碑：T1-T8）和法规路径（9个里程碑：R1-R9）。"
        "六个决策门（G1-G6）提供通过/不通过检查点。项目跨度23个月，"
        "从2026年3月至2028年2月。")
    pdf.txt("关键可交付成果：", bold=True)
    deliverables = [
        "完成sEMG原型定型，锁定BOM和设计规范",
        "完整的sEMG 510(k)提交包（模块A）",
        "EIT 32电极带原型，具备V/Q成像能力",
        "完整的EIT 510(k)提交包（模块B）",
        "MyoBus集成平台，同步sEMG + EIT数据流",
        "符合21 CFR 820的两个模块设计历史文件(DHF)",
        "ISO 14971风险管理文件，追踪8项风险",
        "思澜科技（成都）ISO 13485合规制造",
    ]
    for d in deliverables:
        pdf.bul(d)
    pdf.ln(2)

    # ═══════════════════════════════════
    #  5. 高层级风险
    # ═══════════════════════════════════
    pdf.sec("5. 高层级风险")
    w = [9, 75, 14, 72]
    pdf.table_row(["编号", "风险", "等级", "缓解措施"], w, header=True)
    risks = [
        ("R-004", "V/Q灌注图像误判→呼吸机设置错误", "红",
         "标注为研究辅助工具；强制临床培训"),
        ("R-007", "510(k)被拒—FDA不接受前置器械", "红",
         "预提交会议策略；De Novo备用(+60天)"),
        ("R-008", "sEMG获批前资金跑道不足", "红",
         "分阶段资金；sEMG优先实现早期收入"),
        ("R-001", "sEMG假阴性（漏检呼吸暂停）", "黄",
         "双阈值算法+报警；辅助设备标签"),
        ("R-005", "网络安全破坏/未授权访问", "黄",
         "AES-256；RBAC；FDA网络安全2023"),
        ("R-002", "ECG伪影假阳性", "黄",
         "ECG门控>98%抑制；可视波形验证"),
    ]
    for i, (rid, desc, lvl, mit) in enumerate(risks):
        pdf.table_row([rid, desc, lvl, mit], w, bold=(i < 3))
    pdf.ln(2)

    # ═══════════════════════════════════
    #  6. 里程碑摘要
    # ═══════════════════════════════════
    pdf.sec("6. 里程碑摘要时间表")
    mw = [14, 68, 18, 70]
    pdf.table_row(["月份", "里程碑", "路径", "关键标准"], mw, header=True)
    milestones = [
        ("M+0", "原型定型 — sEMG模块", "技术", "BOM锁定；规格匹配Pre-Sub"),
        ("M+0", "预提交Q会议申请已提交", "法规", "向FDA CDRH提交Q-Sub"),
        ("M+1", "知识产权收购和美国法律结构", "法规", "专利转让至B公司美国"),
        ("M+2", "FDA预提交会议", "法规", "FDA反馈SE策略"),
        ("M+2", "ISO 13485审核—思澜科技", "法规", "差距修复完成"),
        ("M+3", "台架和性能测试—sEMG", "技术", "IEC 60601-1, EMC, n≥30"),
        ("M+6", "510(k)提交—sEMG（模块A）", "法规", "完整提交包"),
        ("M+8", "EIT原型—32电极带", "技术", "50kHz, 50Hz帧率"),
        ("M+9", "预计510(k)批准—sEMG", "法规", "IKN产品代码批准"),
        ("M+12", "V/Q算法验证", "技术", ">85%准确度vs DCE-CT"),
        ("M+17", "510(k)提交—EIT（模块B）", "法规", "DQS产品代码"),
        ("M+23", "预计510(k)批准—EIT", "法规", "完整平台商业化"),
    ]
    for m in milestones:
        pdf.table_row(list(m), mw)
    pdf.ln(3)

    # ── Signature block ──
    pdf.set_draw_color(*BLUE)
    pdf.set_line_width(0.4)
    pdf.line(pdf.l_margin, pdf.get_y(), pdf.w - pdf.r_margin, pdf.get_y())
    pdf.ln(3)
    pdf.set_font("ARUNI", "B", 9)
    pdf.set_text_color(*TEXT)
    pdf.cell(0, 5, "授权签署", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(1)

    sigs = [
        ("项目发起人：", "________________________", "B公司美国"),
        ("项目经理：", "________________________", "Lon Dailey, PMP"),
        ("首席技术官：", "________________________", "戴博士 (Dr. Dai)"),
        ("首席执行官：", "________________________", "Lawrence Liu"),
    ]
    for role, line, name in sigs:
        pdf.set_font("ARUNI", "B", 8)
        pdf.set_text_color(*GRAY)
        pdf.cell(28, 4.5, role)
        pdf.set_font("ARUNI", "", 8)
        pdf.set_text_color(*TEXT)
        pdf.cell(45, 4.5, line)
        pdf.set_font("ARUNI", "I", 8)
        pdf.set_text_color(*GRAY)
        pdf.cell(40, 4.5, name)
        pdf.set_text_color(*TEXT)
        pdf.cell(0, 4.5, "日期：___________", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)

    path = os.path.join(OUT_DIR, "Project_Charter_CN.pdf")
    pdf.output(path)
    return path


# ────────────────────────────────────
if __name__ == "__main__":
    en = build_english()
    print(f"English Charter: {en}")
    cn = build_chinese()
    print(f"Chinese Charter: {cn}")
    print("Done.")
