// ============================================================
// DATA MODEL — ICU Respiratory Digital Twin System
// Sourced from FDA 510(k) Pre-Submission Package (March 2026)
// PMP is overriding authority; accepts input from biz & tech
// ============================================================

const PROJECT = {
  name: {
    en: "ICU Respiratory Digital Twin System",
    cn: "ICU呼吸数字孪生系统",
  },
  subtitle: {
    en: "sEMG Neural Drive + EIT Ventilation/Perfusion Monitoring Platform",
    cn: "sEMG神经驱动 + EIT通气/灌注监测平台",
  },
  submissionType: "510(k) — Two Modular Devices",
  applicant: {
    en: "Company B USA (Global IP Holder)",
    cn: "B公司美国（全球知识产权持有方）",
  },
  manufacturer: {
    en: "Silan Technology (Chengdu) Co., Ltd.",
    cn: "思岚科技（成都）有限公司",
  },
  preparedDate: "March 2026",
  currentMonth: 0, // M+0 starting point
};

// ============================================================
// DUAL-TRACK: Technical + Regulatory milestones
// ============================================================

const TRACKS = {
  technical: {
    label: { en: "Technical Track", cn: "技术路径" },
    icon: "🔬",
    milestones: [
      {
        id: "T1",
        month: 0,
        title: {
          en: "Prototype Finalization — sEMG Module",
          cn: "原型定型 — sEMG模块",
        },
        description: {
          en: "4–8 surface EMG electrode array, 24-bit ADC, 2000 Hz sampling, BT wireless isolation per IEC 60601-1-2",
          cn: "4-8表面EMG电极阵列, 24位ADC, 2000Hz采样, 蓝牙无线隔离符合IEC 60601-1-2",
        },
        status: "complete",
        owner: "tech",
        category: "prototype",
      },
      {
        id: "T2",
        month: 1,
        title: { en: "ECG-Gating Algorithm Validation", cn: "ECG门控算法验证" },
        description: {
          en: "Proprietary adaptive filtering: SNR improvement >20 dB, ECG artifact suppression >98%",
          cn: "专有自适应滤波: 信噪比改善>20dB, ECG伪影抑制>98%",
        },
        status: "in-progress",
        owner: "tech",
        category: "validation",
      },
      {
        id: "T3",
        month: 3,
        title: {
          en: "Bench & Performance Testing — sEMG",
          cn: "台架和性能测试 — sEMG",
        },
        description: {
          en: "IEC 60601-1 electrical safety, EMC testing, usability study (IEC 62366), algorithm validation vs. esophageal reference (n≥30)",
          cn: "IEC 60601-1电气安全, EMC测试, 可用性研究(IEC 62366), 算法验证对比食管参考(n≥30)",
        },
        status: "not-started",
        owner: "tech",
        category: "testing",
      },
      {
        id: "T4",
        month: 6,
        title: {
          en: "sEMG Sensitivity/Specificity Targets",
          cn: "sEMG灵敏度/特异性目标",
        },
        description: {
          en: "NRD detection sensitivity ≥92%, asynchrony specificity ≥88%, signal latency <50ms",
          cn: "NRD检测灵敏度≥92%, 异步特异性≥88%, 信号延迟<50ms",
        },
        status: "not-started",
        owner: "tech",
        category: "validation",
      },
      {
        id: "T5",
        month: 8,
        title: {
          en: "EIT Prototype — 32-Electrode Belt",
          cn: "EIT原型 — 32电极带",
        },
        description: {
          en: "32-electrode thoracic belt, 50 kHz AC injection, 50 Hz frame rate, 32×32 pixel cross-section reconstruction",
          cn: "32电极胸带, 50kHz交流注入, 50Hz帧率, 32×32像素截面重建",
        },
        status: "not-started",
        owner: "tech",
        category: "prototype",
      },
      {
        id: "T6",
        month: 12,
        title: {
          en: "V/Q Algorithm Validation (vs. DCE-CT)",
          cn: "V/Q算法验证（对比DCE-CT）",
        },
        description: {
          en: "V/Q separation accuracy >85% vs. DCE-CT reference, ventilation sensitivity ≥90%, perfusion SNR >15 dB",
          cn: "V/Q分离准确度>85%对比DCE-CT参考, 通气灵敏度≥90%, 灌注信噪比>15dB",
        },
        status: "not-started",
        owner: "tech",
        category: "validation",
      },
      {
        id: "T7",
        month: 14,
        title: { en: "EIT Biocompatibility Testing", cn: "EIT生物相容性测试" },
        description: {
          en: "ISO 10993-5 cytotoxicity, ISO 10993-10 sensitization/irritation for belt & electrode materials",
          cn: "ISO 10993-5细胞毒性, ISO 10993-10致敏/刺激测试（带和电极材料）",
        },
        status: "not-started",
        owner: "tech",
        category: "testing",
      },
      {
        id: "T8",
        month: 2,
        title: { en: "MyoBus Protocol Integration", cn: "MyoBus协议集成" },
        description: {
          en: "<1ms timestamp alignment between sEMG and EIT. AES-256 encryption, RBAC, HL7 FHIR output",
          cn: "<1ms时间戳对齐sEMG和EIT。AES-256加密, RBAC, HL7 FHIR输出",
        },
        status: "in-progress",
        owner: "tech",
        category: "integration",
      },
    ],
  },
  regulatory: {
    label: { en: "Regulatory Track", cn: "法规路径" },
    icon: "📋",
    milestones: [
      {
        id: "R1",
        month: 0,
        title: {
          en: "Pre-Sub Q-Meeting Request Filed",
          cn: "预提交Q会议申请已提交",
        },
        description: {
          en: "Q-Sub to FDA (CDRH) for sEMG module: predicate selection, testing protocol, SiMD classification",
          cn: "向FDA(CDRH)提交sEMG模块Q-Sub: 前置器械选择, 测试方案, SiMD分类",
        },
        status: "complete",
        owner: "regulatory",
        category: "submission",
      },
      {
        id: "R2",
        month: 2,
        title: { en: "Pre-Submission Meeting (FDA)", cn: "预提交会议（FDA）" },
        description: {
          en: "FDA written feedback on: SE strategy, performance testing protocol, software classification",
          cn: "FDA书面反馈: SE策略, 性能测试方案, 软件分类",
        },
        status: "not-started",
        owner: "regulatory",
        category: "meeting",
      },
      {
        id: "R3",
        month: 5,
        title: {
          en: "510(k) Submission — sEMG Module",
          cn: "510(k)提交 — sEMG模块",
        },
        description: {
          en: "Complete package: Cover letter, Device Description, SE Discussion, Performance Testing, Risk Analysis, Biocompatibility, Software, Labeling",
          cn: "完整包: 附信、设备描述、SE讨论、性能测试、风险分析、生物相容性、软件、标签",
        },
        status: "not-started",
        owner: "regulatory",
        category: "submission",
      },
      {
        id: "R4",
        month: 11,
        title: {
          en: "Expected 510(k) Clearance — sEMG",
          cn: "预计510(k)批准 — sEMG",
        },
        description: {
          en: "Standard 510(k) review ~90 days. IKN product code clearance → Module A commercial launch",
          cn: "标准510(k)审查约90天。IKN产品代码批准 → A模块商业发布",
        },
        status: "not-started",
        owner: "regulatory",
        category: "clearance",
      },
      {
        id: "R5",
        month: 12,
        title: { en: "Begin EIT 510(k) Preparation", cn: "开始EIT 510(k)准备" },
        description: {
          en: "EIT system testing: V/Q validation, belt biocompatibility (ISO 10993-5/10), EIT-specific EMC",
          cn: "EIT系统测试: V/Q验证, 带生物相容性(ISO 10993-5/10), EIT专用EMC",
        },
        status: "not-started",
        owner: "regulatory",
        category: "preparation",
      },
      {
        id: "R6",
        month: 17,
        title: {
          en: "510(k) Submission — EIT System",
          cn: "510(k)提交 — EIT系统",
        },
        description: {
          en: "DQS product code, Timpel Enlight K250464 as primary predicate, V/Q imaging as performance enhancement",
          cn: "DQS产品代码, Timpel Enlight K250464作为主要前置器械, V/Q成像作为性能增强",
        },
        status: "not-started",
        owner: "regulatory",
        category: "submission",
      },
      {
        id: "R7",
        month: 23,
        title: {
          en: "Expected 510(k) Clearance — EIT System",
          cn: "预计510(k)批准 — EIT系统",
        },
        description: {
          en: "Full platform commercially available. Integrated MyoBus system clinical deployment. File for integrated platform claim.",
          cn: "完整平台商业可用。集成MyoBus系统临床部署。申请集成平台声明。",
        },
        status: "not-started",
        owner: "regulatory",
        category: "clearance",
      },
      {
        id: "R8",
        month: 1,
        title: {
          en: "IP Buyout & US Legal Structure",
          cn: "知识产权收购和美国法律结构",
        },
        description: {
          en: "Transfer patents, software copyrights, MyoBus IP to Company B USA. US-based DHF.",
          cn: "将专利、软件版权、MyoBus知识产权转让给B公司美国。在美建立DHF。",
        },
        status: "in-progress",
        owner: "business",
        category: "legal",
      },
      {
        id: "R9",
        month: 2,
        title: {
          en: "ISO 13485 Audit — Silan Technology",
          cn: "ISO 13485审核 — 思岚科技",
        },
        description: {
          en: "Readiness assessment vs. 21 CFR 820 QSR and ISO 13485:2016. Gap remediation before FDA registration.",
          cn: "对比21 CFR 820 QSR和ISO 13485:2016进行准备评估。FDA注册前差距修复。",
        },
        status: "not-started",
        owner: "regulatory",
        category: "audit",
      },
    ],
  },
};

// ============================================================
// GATE SYSTEM — Decision checkpoints
// ============================================================

const GATES = [
  {
    id: "G1",
    number: 1,
    title: { en: "sEMG Design Verification Complete", cn: "sEMG设计验证完成" },
    month: 3,
    status: "not-started", // not-started | pending-review | approved | blocked | needs-data
    criteria: [
      {
        en: "ECG-gating algorithm validated (suppression >98%)",
        cn: "ECG门控算法已验证（抑制>98%）",
        met: false,
      },
      {
        en: "Bench testing per IEC 60601-1 passed",
        cn: "符合IEC 60601-1的台架测试通过",
        met: false,
      },
      {
        en: "sEMG sensitivity ≥92% confirmed",
        cn: "sEMG灵敏度≥92%确认",
        met: false,
      },
      {
        en: "EMC compliance (IEC 60601-1-2) verified",
        cn: "EMC合规性(IEC 60601-1-2)已验证",
        met: false,
      },
    ],
    decision: null, // null | "proceed" | "more-data" | "stop"
    decisionBy: null,
    decisionDate: null,
    notes: [],
    inputBusiness: [],
    inputTech: [],
  },
  {
    id: "G2",
    number: 2,
    title: { en: "Pre-Sub FDA Feedback Received", cn: "预提交FDA反馈已收到" },
    month: 2,
    status: "not-started",
    criteria: [
      {
        en: "FDA written feedback received",
        cn: "FDA书面反馈已收到",
        met: false,
      },
      {
        en: "Predicate device strategy accepted",
        cn: "前置器械策略被接受",
        met: false,
      },
      {
        en: "Testing protocol approved by FDA",
        cn: "测试方案获FDA批准",
        met: false,
      },
      {
        en: "Software classification confirmed (Class C / IEC 62304 Class B)",
        cn: "软件分类确认(C类 / IEC 62304 B类)",
        met: false,
      },
    ],
    decision: null,
    decisionBy: null,
    decisionDate: null,
    notes: [],
    inputBusiness: [],
    inputTech: [],
  },
  {
    id: "G3",
    number: 3,
    title: { en: "510(k) sEMG Submission Ready", cn: "510(k) sEMG提交就绪" },
    month: 5,
    status: "not-started",
    criteria: [
      {
        en: "All 15 submission sections complete",
        cn: "全部15个提交章节完成",
        met: false,
      },
      {
        en: "Risk analysis (ISO 14971) finalized",
        cn: "风险分析(ISO 14971)定稿",
        met: false,
      },
      {
        en: "Clinical evidence dossier compiled",
        cn: "临床证据档案汇编完成",
        met: false,
      },
      {
        en: "Labeling & IFU reviewed (21 CFR 801)",
        cn: "标签和IFU审核(21 CFR 801)",
        met: false,
      },
      { en: "Quality system audit passed", cn: "质量体系审核通过", met: false },
    ],
    decision: null,
    decisionBy: null,
    decisionDate: null,
    notes: [],
    inputBusiness: [],
    inputTech: [],
  },
  {
    id: "G4",
    number: 4,
    title: { en: "sEMG Module Commercial Launch", cn: "sEMG模块商业发布" },
    month: 11,
    status: "not-started",
    criteria: [
      {
        en: "510(k) clearance received (IKN)",
        cn: "510(k)批准已获得(IKN)",
        met: false,
      },
      {
        en: "Manufacturing scaled — Silan production ready",
        cn: "制造已扩展 — 思岚生产就绪",
        met: false,
      },
      {
        en: "Funding secured for commercial ops",
        cn: "商业运营资金已到位",
        met: false,
      },
    ],
    decision: null,
    decisionBy: null,
    decisionDate: null,
    notes: [],
    inputBusiness: [],
    inputTech: [],
  },
  {
    id: "G5",
    number: 5,
    title: { en: "EIT 510(k) Submission Ready", cn: "EIT 510(k)提交就绪" },
    month: 17,
    status: "not-started",
    criteria: [
      {
        en: "V/Q algorithm validated (>85% vs DCE-CT)",
        cn: "V/Q算法已验证(>85%对比DCE-CT)",
        met: false,
      },
      {
        en: "EIT biocompatibility testing complete",
        cn: "EIT生物相容性测试完成",
        met: false,
      },
      {
        en: "Timpel predicate comparison documented",
        cn: "Timpel前置器械比较文档完成",
        met: false,
      },
      {
        en: "EIT-specific EMC testing passed",
        cn: "EIT专用EMC测试通过",
        met: false,
      },
    ],
    decision: null,
    decisionBy: null,
    decisionDate: null,
    notes: [],
    inputBusiness: [],
    inputTech: [],
  },
  {
    id: "G6",
    number: 6,
    title: {
      en: "Full Platform Launch — FDA Cleared",
      cn: "完整平台发布 — FDA已批准",
    },
    month: 23,
    status: "not-started",
    criteria: [
      {
        en: "EIT 510(k) clearance (DQS)",
        cn: "EIT 510(k)批准(DQS)",
        met: false,
      },
      {
        en: "MyoBus integrated platform validated",
        cn: "MyoBus集成平台已验证",
        met: false,
      },
      {
        en: "Commercial deployment plan finalized",
        cn: "商业部署计划已定稿",
        met: false,
      },
    ],
    decision: null,
    decisionBy: null,
    decisionDate: null,
    notes: [],
    inputBusiness: [],
    inputTech: [],
  },
];

// ============================================================
// RISK DASHBOARD — ISO 14971
// ============================================================

const RISKS = [
  {
    id: "RISK-001",
    title: {
      en: "False-negative sEMG signal (missed apnea / low-effort breath)",
      cn: "sEMG信号假阴性（漏检呼吸暂停/低努力呼吸）",
    },
    severity: "high",
    probability: "low",
    riskLevel: "yellow", // red | yellow | green
    controls: {
      en: "Dual-threshold algorithm + alarm; labeled as adjunct; clinical staff training",
      cn: "双阈值算法+报警; 标注为辅助设备; 临床人员培训",
    },
    residual: { en: "Acceptable", cn: "可接受" },
    mitigationStatus: "in-progress",
    module: "A",
    standard: "ISO 14971",
  },
  {
    id: "RISK-002",
    title: {
      en: "ECG artifact misidentified as neural drive signal (false positive)",
      cn: "ECG伪影被误识别为神经驱动信号（假阳性）",
    },
    severity: "medium",
    probability: "medium",
    riskLevel: "yellow",
    controls: {
      en: "Proprietary ECG-gating (>98% suppression, validated); visual waveform display for verification",
      cn: "专有ECG门控(>98%抑制, 已验证); 可视波形显示用于验证",
    },
    residual: { en: "Acceptable", cn: "可接受" },
    mitigationStatus: "in-progress",
    module: "A",
    standard: "ISO 14971",
  },
  {
    id: "RISK-003",
    title: {
      en: "EIT belt electrical leakage (patient contact current)",
      cn: "EIT带电气泄漏（患者接触电流）",
    },
    severity: "high",
    probability: "very-low",
    riskLevel: "green",
    controls: {
      en: "IEC 60601-1 Type BF; <10 µA patient leakage; Bluetooth wireless isolation",
      cn: "IEC 60601-1 BF型; <10µA患者泄漏; 蓝牙无线隔离",
    },
    residual: { en: "Acceptable", cn: "可接受" },
    mitigationStatus: "complete",
    module: "B",
    standard: "IEC 60601-1",
  },
  {
    id: "RISK-004",
    title: {
      en: "V/Q perfusion image misinterpretation → incorrect ventilator adjustment",
      cn: "V/Q灌注图像误判 → 呼吸机设置错误",
    },
    severity: "high",
    probability: "low",
    riskLevel: "red",
    controls: {
      en: "Perfusion labeled 'investigational adjunct' in initial 510(k); mandated clinical training program",
      cn: "灌注在初始510(k)中标注为'研究辅助工具'; 强制临床培训计划",
    },
    residual: { en: "Acceptable", cn: "可接受" },
    mitigationStatus: "not-started",
    module: "B",
    standard: "ISO 14971",
  },
  {
    id: "RISK-005",
    title: {
      en: "Cybersecurity breach / unauthorized data access or device tampering",
      cn: "网络安全破坏/未授权数据访问或设备篡改",
    },
    severity: "medium",
    probability: "low",
    riskLevel: "yellow",
    controls: {
      en: "AES-256 encryption; RBAC; isolated local network; FDA Cyber Guidance 2023; no remote FW update without auth",
      cn: "AES-256加密; RBAC; 隔离本地网络; FDA网络安全指南2023; 无认证不允许远程固件更新",
    },
    residual: { en: "Acceptable", cn: "可接受" },
    mitigationStatus: "in-progress",
    module: "Both",
    standard: "FDA Cybersecurity 2023",
  },
  {
    id: "RISK-006",
    title: {
      en: "MyoBus synchronization failure — misaligned neural-mechanical data",
      cn: "MyoBus同步故障 — 神经-机械数据不对齐",
    },
    severity: "medium",
    probability: "very-low",
    riskLevel: "green",
    controls: {
      en: "Hardware timestamp redundancy; loss-of-sync alarm; automatic fallback to independent module mode",
      cn: "硬件时间戳冗余; 同步丢失报警; 自动回退到独立模块模式",
    },
    residual: { en: "Acceptable", cn: "可接受" },
    mitigationStatus: "complete",
    module: "Both",
    standard: "ISO 14971",
  },
  {
    id: "RISK-007",
    title: {
      en: "510(k) rejection or De Novo reclassification — predicate not accepted or combined platform deemed novel",
      cn: "510(k)被拒或De Novo重分类 — 前置器械未被接受或组合平台被认定为新型器械",
    },
    severity: "high",
    probability: "medium",
    riskLevel: "red",
    controls: {
      en: "Two risk scenarios: (A) Predicate rejection — sEMG K082437 esophageal vs. surface electrodes, EIT K250464 ventilation-only vs. V/Q claim. (B) De Novo for combined platform — FDA views integrated Digital Twin as novel. Mitigation: Pre-Sub Q-Meeting at M+0; decouple modules in filings; prepare De Novo contingency (+$130K fee, +6-12 months, +$200K-$400K total). Silver lining: De Novo creates the product code for future competitors.",
      cn: "两个风险场景：(A) 前置器械被拒 — sEMG K082437食管vs表面电极, EIT K250464仅通气vs V/Q声明。(B) 组合平台De Novo — FDA认为集成数字孪生为新型器械。缓解：M+0的Pre-Sub Q会议；申报中模块脱钩；准备De Novo备用方案（+$130K费用, +6-12个月, 总计+$200K-$400K）。积极面：De Novo为未来竞争对手创建产品代码。",
    },
    residual: {
      en: "Manageable if detected at Pre-Sub (M+2)",
      cn: "如在Pre-Sub(M+2)发现则可控",
    },
    mitigationStatus: "in-progress",
    module: "Both",
    standard: "21 CFR 807",
  },
  {
    id: "RISK-008",
    title: {
      en: "Funding runway insufficient before sEMG clearance (M+11)",
      cn: "sEMG批准(M+11)前资金跑道不足",
    },
    severity: "high",
    probability: "medium",
    riskLevel: "red",
    controls: {
      en: "Phased milestone-based funding; sEMG-first strategy enables earlier revenue; investor gate reviews",
      cn: "分阶段里程碑资金; sEMG优先策略实现更早收入; 投资者门控评审",
    },
    residual: { en: "Manageable", cn: "可控" },
    mitigationStatus: "in-progress",
    module: "N/A",
    standard: "Business",
  },
];

// ============================================================
// REGULATORY STANDARDS TRACKER
// ============================================================

const STANDARDS = [
  {
    id: "STD-01",
    code: "IEC 60601-1:2005+AMD1",
    title: {
      en: "Medical Electrical Equipment — General Safety",
      cn: "医用电气设备 — 通用安全",
    },
    applies: "Both",
    status: "in-progress",
    progress: 30,
  },
  {
    id: "STD-02",
    code: "IEC 60601-1-2:2014 Ed.4.1",
    title: { en: "Electromagnetic Compatibility (EMC)", cn: "电磁兼容性(EMC)" },
    applies: "Both",
    status: "not-started",
    progress: 0,
  },
  {
    id: "STD-03",
    code: "IEC 60601-1-6:2010+AMD1",
    title: { en: "Usability Engineering", cn: "可用性工程" },
    applies: "Both",
    status: "not-started",
    progress: 0,
  },
  {
    id: "STD-04",
    code: "ISO 14971:2019",
    title: {
      en: "Risk Management for Medical Devices",
      cn: "医疗器械风险管理",
    },
    applies: "Both",
    status: "in-progress",
    progress: 45,
  },
  {
    id: "STD-05",
    code: "ISO 10993-1:2018",
    title: {
      en: "Biocompatibility — Evaluation Framework",
      cn: "生物相容性 — 评估框架",
    },
    applies: "sEMG Electrodes",
    status: "not-started",
    progress: 0,
  },
  {
    id: "STD-06",
    code: "ISO 10993-5",
    title: { en: "Cytotoxicity", cn: "细胞毒性" },
    applies: "sEMG Electrodes",
    status: "not-started",
    progress: 0,
  },
  {
    id: "STD-07",
    code: "ISO 10993-10",
    title: { en: "Sensitization & Irritation", cn: "致敏和刺激" },
    applies: "sEMG + EIT Belt",
    status: "not-started",
    progress: 0,
  },
  {
    id: "STD-08",
    code: "FDA Cybersecurity 2023",
    title: { en: "Medical Device Cybersecurity", cn: "医疗器械网络安全" },
    applies: "Both",
    status: "in-progress",
    progress: 25,
  },
  {
    id: "STD-09",
    code: "21 CFR Part 820",
    title: { en: "Quality System Regulation (QSR)", cn: "质量体系法规(QSR)" },
    applies: "Both",
    status: "in-progress",
    progress: 40,
  },
  {
    id: "STD-10",
    code: "21 CFR Part 11",
    title: { en: "Electronic Records & Signatures", cn: "电子记录和签名" },
    applies: "Software",
    status: "not-started",
    progress: 0,
  },
  {
    id: "STD-11",
    code: "IEC 62304",
    title: {
      en: "Medical Device Software Lifecycle",
      cn: "医疗器械软件生命周期",
    },
    applies: "Software",
    status: "in-progress",
    progress: 20,
  },
  {
    id: "STD-12",
    code: "ISO 13485:2016",
    title: { en: "QMS for Medical Devices", cn: "医疗器械质量管理体系" },
    applies: "Silan Manufacturing",
    status: "in-progress",
    progress: 60,
  },
];

// ============================================================
// TIMELINE — Business-term translations
// ============================================================

const TIMELINE_EVENTS = [
  {
    month: 0,
    technical: {
      en: "Pre-Sub filed; prototype ready",
      cn: "预提交已提交; 原型就绪",
    },
    business: {
      en: "FDA engagement initiated — clock starts",
      cn: "FDA接触启动 — 计时开始",
    },
    impact: "neutral",
  },
  {
    month: 2,
    technical: { en: "FDA Pre-Sub meeting", cn: "FDA预提交会议" },
    business: {
      en: "Regulatory green light / red flag — pivotal investor signal",
      cn: "法规绿灯/红旗 — 关键投资者信号",
    },
    impact: "critical",
  },
  {
    month: 3,
    technical: {
      en: "Bench & performance testing begins",
      cn: "台架和性能测试开始",
    },
    business: {
      en: "Testing costs ramp — largest pre-submission spend",
      cn: "测试成本攀升 — 提交前最大支出",
    },
    impact: "warning",
  },
  {
    month: 5,
    technical: {
      en: "510(k) sEMG submitted to FDA",
      cn: "510(k) sEMG已提交FDA",
    },
    business: {
      en: "Submission milestone — investor confidence checkpoint",
      cn: "提交里程碑 — 投资者信心检查点",
    },
    impact: "critical",
  },
  {
    month: 11,
    technical: {
      en: "sEMG 510(k) clearance expected",
      cn: "sEMG 510(k)预计批准",
    },
    business: {
      en: "Module A revenue-ready — funding runway extended",
      cn: "A模块可产生收入 — 资金跑道延长",
    },
    impact: "critical",
  },
  {
    month: 12,
    technical: {
      en: "EIT testing & validation begins",
      cn: "EIT测试和验证开始",
    },
    business: {
      en: "Second major investment tranche needed",
      cn: "需要第二笔主要投资",
    },
    impact: "warning",
  },
  {
    month: 17,
    technical: { en: "510(k) EIT submitted", cn: "510(k) EIT已提交" },
    business: {
      en: "Full platform pathway visible — strategic partnerships viable",
      cn: "完整平台路径可见 — 战略合作可行",
    },
    impact: "critical",
  },
  {
    month: 23,
    technical: {
      en: "EIT clearance — full platform",
      cn: "EIT批准 — 完整平台",
    },
    business: {
      en: "Full commercial launch — ROI realization begins",
      cn: "全面商业发布 — ROI实现开始",
    },
    impact: "critical",
  },
];

// ============================================================
// INPUT TRACKING — Business & Tech stakeholder inputs
// ============================================================

const STAKEHOLDER_INPUTS = [
  {
    id: "INP-001",
    from: "tech",
    date: "2026-03-15",
    gate: "G1",
    content: {
      en: "ECG-gating algorithm showing 97.5% suppression in latest bench test — close to 98% target. Requesting 2 additional weeks for optimization.",
      cn: "ECG门控算法在最新台架测试中显示97.5%抑制 — 接近98%目标。请求额外2周进行优化。",
    },
    status: "pending-review", // pending-review | accepted | rejected | noted
    pmpResponse: null,
  },
  {
    id: "INP-002",
    from: "business",
    date: "2026-03-10",
    gate: "G4",
    content: {
      en: "Investor board requests monthly progress reports starting M+3. Need clear KPIs tied to each gate.",
      cn: "投资者委员会要求从M+3开始每月进度报告。需要与每个门控关联的明确KPI。",
    },
    status: "accepted",
    pmpResponse: {
      en: "Approved. Monthly reports will align with gate criteria.",
      cn: "已批准。月度报告将与门控标准对齐。",
    },
  },
];
