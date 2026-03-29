// ============================================================
// 510(k) CATEGORY TEMPLATES — Pre-built project configurations
// for common medical device categories
// ============================================================

export interface DeviceTemplate {
  id: string;
  name: { en: string; cn: string };
  icon: string;
  description: { en: string; cn: string };
  submissionType: string;
  deviceClass: string;
  productCodes: string;
  regulationSection: string;
  predicateExamples: string;
  estimatedDuration: number;
  techAreas: { en: string; cn: string };
  risks: Array<{
    title: { en: string; cn: string };
    severity: "high" | "medium" | "low";
    probability: "very-low" | "low" | "medium" | "high";
    riskLevel: "red" | "yellow" | "green";
    controls: { en: string; cn: string };
    module: string;
    standard: string;
  }>;
  standards: Array<{
    code: string;
    title: { en: string; cn: string };
    applies: string;
  }>;
  budgetCategories: Array<{ en: string; cn: string }>;
}

function ls(en: string, cn: string): { en: string; cn: string } {
  return { en, cn };
}

// ── RESPIRATORY DEVICES ─────────────────────────
const respiratory: DeviceTemplate = {
  id: "respiratory",
  name: ls("Respiratory Devices", "呼吸设备"),
  icon: "🫁",
  description: ls(
    "Ventilators, CPAP/BiPAP, nebulizers, airway management, respiratory monitors, air purification systems",
    "呼吸机、CPAP/BiPAP、雾化器、气道管理、呼吸监测仪、空气净化系统",
  ),
  submissionType: "510k-standard",
  deviceClass: "II",
  productCodes: "BZD, CBK, BTT, FRA",
  regulationSection: "§ 868",
  predicateExamples:
    "Maquet NAVA Edi catheter (K082437)\nPhilips Respironics DreamStation (K142954)\nAiroCide TiO2 (K023830)",
  estimatedDuration: 18,
  techAreas: ls(
    "Airflow & Pressure Control\nHumidification System\nAlarm & Safety Systems\nPatient Interface Design\nElectrical Safety (IEC 60601-1)\nEMC Testing (IEC 60601-1-2)\nSoftware Validation (IEC 62304)\nBiocompatibility (ISO 10993)",
    "气流与压力控制\n加湿系统\n报警与安全系统\n患者接口设计\n电气安全 (IEC 60601-1)\nEMC测试 (IEC 60601-1-2)\n软件验证 (IEC 62304)\n生物相容性 (ISO 10993)",
  ),
  risks: [
    {
      title: ls("Inadequate ventilation delivery", "通气量不足"),
      severity: "high",
      probability: "low",
      riskLevel: "red",
      controls: ls(
        "Pressure/flow sensors, alarm systems, redundant controls",
        "压力/流量传感器、报警系统、冗余控制",
      ),
      module: "Respiratory",
      standard: "ISO 80601-2-12",
    },
    {
      title: ls("Oxygen concentration error", "氧浓度误差"),
      severity: "high",
      probability: "low",
      riskLevel: "red",
      controls: ls(
        "O2 sensor calibration, dual-sensor cross-check",
        "O2传感器校准、双传感器交叉验证",
      ),
      module: "Respiratory",
      standard: "IEC 60601-1",
    },
    {
      title: ls("Patient circuit leak / disconnect", "患者回路泄漏/断开"),
      severity: "high",
      probability: "medium",
      riskLevel: "red",
      controls: ls(
        "Disconnect alarm, leak compensation algorithm",
        "断开报警、泄漏补偿算法",
      ),
      module: "Respiratory",
      standard: "ISO 80601-2-12",
    },
    {
      title: ls(
        "Biocompatibility of patient-contact materials",
        "患者接触材料的生物相容性",
      ),
      severity: "medium",
      probability: "low",
      riskLevel: "yellow",
      controls: ls(
        "ISO 10993 testing, material selection per FDA guidance",
        "ISO 10993测试、按FDA指南选择材料",
      ),
      module: "Materials",
      standard: "ISO 10993",
    },
    {
      title: ls("EMC interference with ICU equipment", "与ICU设备的EMC干扰"),
      severity: "medium",
      probability: "low",
      riskLevel: "yellow",
      controls: ls(
        "IEC 60601-1-2 Ed.4 testing, shielding design",
        "IEC 60601-1-2第4版测试、屏蔽设计",
      ),
      module: "Electrical",
      standard: "IEC 60601-1-2",
    },
    {
      title: ls("Software malfunction in alarm system", "报警系统软件故障"),
      severity: "high",
      probability: "low",
      riskLevel: "red",
      controls: ls(
        "IEC 62304 Class B/C lifecycle, unit + integration testing",
        "IEC 62304 B/C类生命周期、单元+集成测试",
      ),
      module: "Software",
      standard: "IEC 62304",
    },
  ],
  standards: [
    {
      code: "IEC 60601-1",
      title: ls(
        "Medical Electrical Equipment -- General",
        "医用电气设备——通用",
      ),
      applies: "All",
    },
    {
      code: "IEC 60601-1-2",
      title: ls("EMC Requirements", "EMC要求"),
      applies: "All",
    },
    {
      code: "ISO 80601-2-12",
      title: ls("Ventilators -- Critical Care", "呼吸机——重症监护"),
      applies: "Ventilators",
    },
    {
      code: "ISO 80601-2-70",
      title: ls("Sleep Apnea Breathing Therapy", "睡眠呼吸暂停治疗"),
      applies: "CPAP/BiPAP",
    },
    {
      code: "IEC 62304",
      title: ls("Medical Device Software Lifecycle", "医疗器械软件生命周期"),
      applies: "Software",
    },
    {
      code: "ISO 14971",
      title: ls("Risk Management", "风险管理"),
      applies: "All",
    },
    {
      code: "ISO 10993",
      title: ls("Biocompatibility", "生物相容性"),
      applies: "Patient-contact",
    },
    {
      code: "21 CFR 820",
      title: ls("Quality System Regulation", "质量体系法规"),
      applies: "All",
    },
    {
      code: "ISO 13485",
      title: ls("Quality Management Systems", "质量管理体系"),
      applies: "All",
    },
  ],
  budgetCategories: [
    ls("Prototype & Materials", "原型和材料"),
    ls("Bench & Performance Testing", "台架与性能测试"),
    ls("Biocompatibility Testing", "生物相容性测试"),
    ls("EMC/Safety Testing", "EMC/安全测试"),
    ls("Software V&V", "软件V&V"),
    ls("Regulatory & Legal", "法规和法律"),
    ls("Personnel", "人员"),
    ls("Clinical Studies", "临床研究"),
  ],
};

// ── CARDIOVASCULAR DEVICES ──────────────────────
const cardiovascular: DeviceTemplate = {
  id: "cardiovascular",
  name: ls("Cardiovascular Devices", "心血管设备"),
  icon: "❤️",
  description: ls(
    "ECG monitors, blood pressure devices, cardiac catheters, vascular stents, pacemaker accessories, hemodynamic monitors",
    "心电监护仪、血压设备、心导管、血管支架、起搏器附件、血流动力学监测仪",
  ),
  submissionType: "510k-standard",
  deviceClass: "II",
  productCodes: "DRX, DXH, MHX, DSQ",
  regulationSection: "§ 870",
  predicateExamples:
    "GE CARESCAPE B850 (K193628)\nPhilips IntelliVue MX800 (K180136)\nMedtronic CareLink (K162572)",
  estimatedDuration: 18,
  techAreas: ls(
    "Signal Acquisition (ECG/BP)\nArrhythmia Detection Algorithm\nPatient Safety Isolation\nDisplay & Alarm System\nElectrical Safety (IEC 60601-1)\nEMC Testing (IEC 60601-1-2)\nSoftware Validation (IEC 62304)\nClinical Performance Validation",
    "信号采集 (ECG/BP)\n心律失常检测算法\n患者安全隔离\n显示与报警系统\n电气安全 (IEC 60601-1)\nEMC测试 (IEC 60601-1-2)\n软件验证 (IEC 62304)\n临床性能验证",
  ),
  risks: [
    {
      title: ls("False negative arrhythmia detection", "心律失常检测假阴性"),
      severity: "high",
      probability: "low",
      riskLevel: "red",
      controls: ls(
        "Algorithm validation with MIT-BIH database, clinical testing",
        "使用MIT-BIH数据库验证算法、临床测试",
      ),
      module: "Algorithm",
      standard: "IEC 60601-2-27",
    },
    {
      title: ls("Electrical leakage to patient", "对患者的电气泄漏"),
      severity: "high",
      probability: "very-low",
      riskLevel: "yellow",
      controls: ls(
        "Type CF isolation, <10uA leakage, double insulation",
        "CF型隔离、<10uA泄漏、双重绝缘",
      ),
      module: "Electrical",
      standard: "IEC 60601-1",
    },
    {
      title: ls("Blood pressure measurement inaccuracy", "血压测量不准确"),
      severity: "medium",
      probability: "medium",
      riskLevel: "yellow",
      controls: ls(
        "ISO 81060-2 validation, clinical study with AAMI/ESH protocol",
        "ISO 81060-2验证、按AAMI/ESH协议进行临床研究",
      ),
      module: "Measurement",
      standard: "ISO 81060-2",
    },
    {
      title: ls(
        "EMC interference in ICU/OR environment",
        "ICU/手术室环境中的EMC干扰",
      ),
      severity: "medium",
      probability: "low",
      riskLevel: "yellow",
      controls: ls(
        "IEC 60601-1-2 Ed.4 testing, professional healthcare environment",
        "IEC 60601-1-2第4版测试、专业医疗环境",
      ),
      module: "Electrical",
      standard: "IEC 60601-1-2",
    },
    {
      title: ls("Software failure in monitoring algorithm", "监测算法软件故障"),
      severity: "high",
      probability: "low",
      riskLevel: "red",
      controls: ls(
        "IEC 62304 Class C lifecycle, SOUP analysis, regression testing",
        "IEC 62304 C类生命周期、SOUP分析、回归测试",
      ),
      module: "Software",
      standard: "IEC 62304",
    },
    {
      title: ls("Data loss during patient transport", "患者转运期间数据丢失"),
      severity: "medium",
      probability: "medium",
      riskLevel: "yellow",
      controls: ls(
        "Local storage buffer, battery backup, auto-reconnect",
        "本地存储缓冲区、电池备份、自动重连",
      ),
      module: "System",
      standard: "IEC 60601-1",
    },
  ],
  standards: [
    {
      code: "IEC 60601-1",
      title: ls(
        "Medical Electrical Equipment -- General",
        "医用电气设备——通用",
      ),
      applies: "All",
    },
    {
      code: "IEC 60601-1-2",
      title: ls("EMC Requirements", "EMC要求"),
      applies: "All",
    },
    {
      code: "IEC 60601-2-27",
      title: ls("ECG Monitoring Equipment", "心电监护设备"),
      applies: "ECG",
    },
    {
      code: "IEC 60601-2-34",
      title: ls("Invasive Blood Pressure Monitoring", "有创血压监测"),
      applies: "IBP",
    },
    {
      code: "ISO 81060-2",
      title: ls("Non-Invasive BP Clinical Validation", "无创血压临床验证"),
      applies: "NIBP",
    },
    {
      code: "IEC 62304",
      title: ls("Medical Device Software Lifecycle", "医疗器械软件生命周期"),
      applies: "Software",
    },
    {
      code: "ISO 14971",
      title: ls("Risk Management", "风险管理"),
      applies: "All",
    },
    {
      code: "21 CFR 820",
      title: ls("Quality System Regulation", "质量体系法规"),
      applies: "All",
    },
    {
      code: "ISO 13485",
      title: ls("Quality Management Systems", "质量管理体系"),
      applies: "All",
    },
  ],
  budgetCategories: [
    ls("Prototype & Materials", "原型和材料"),
    ls("Bench & Performance Testing", "台架与性能测试"),
    ls("Clinical Validation Study", "临床验证研究"),
    ls("EMC/Safety Testing", "EMC/安全测试"),
    ls("Software V&V", "软件V&V"),
    ls("Regulatory & Legal", "法规和法律"),
    ls("Personnel", "人员"),
    ls("Manufacturing Setup", "生产线建设"),
  ],
};

// ── ORTHOPEDIC DEVICES ──────────────────────────
const orthopedic: DeviceTemplate = {
  id: "orthopedic",
  name: ls("Orthopedic Devices", "骨科设备"),
  icon: "🦴",
  description: ls(
    "Joint implants, bone plates/screws, spinal devices, external fixation, orthopedic instruments, rehabilitation devices",
    "关节植入物、骨板/螺钉、脊柱器械、外固定、骨科器械、康复设备",
  ),
  submissionType: "510k-standard",
  deviceClass: "II",
  productCodes: "HRS, HSJ, MAX, NQG",
  regulationSection: "§ 888",
  predicateExamples:
    "Stryker Triathlon Knee System (K191286)\nZimmer Biomet Taperloc Hip (K182109)\nDePuy Synthes Plate System (K171452)",
  estimatedDuration: 24,
  techAreas: ls(
    "Biomechanical Design & FEA\nMaterial Characterization (Ti, CoCr, UHMWPE)\nBiocompatibility Testing (ISO 10993)\nMechanical Testing (ASTM F-series)\nFatigue & Wear Testing\nSterilization Validation\nPackaging Validation (ASTM D4169)\nClinical Performance Data",
    "生物力学设计与有限元分析\n材料表征 (Ti, CoCr, UHMWPE)\n生物相容性测试 (ISO 10993)\n力学测试 (ASTM F系列)\n疲劳与磨损测试\n灭菌验证\n包装验证 (ASTM D4169)\n临床性能数据",
  ),
  risks: [
    {
      title: ls("Implant fatigue fracture", "植入物疲劳断裂"),
      severity: "high",
      probability: "low",
      riskLevel: "red",
      controls: ls(
        "ASTM F2077 fatigue testing, FEA stress analysis, material certs",
        "ASTM F2077疲劳测试、有限元应力分析、材料证书",
      ),
      module: "Mechanical",
      standard: "ASTM F2077",
    },
    {
      title: ls(
        "Biocompatibility reaction (metal sensitivity)",
        "生物相容性反应（金属过敏）",
      ),
      severity: "high",
      probability: "low",
      riskLevel: "red",
      controls: ls(
        "ISO 10993 full panel, material composition per ASTM F75/F136",
        "ISO 10993全套测试、按ASTM F75/F136材料成分",
      ),
      module: "Materials",
      standard: "ISO 10993",
    },
    {
      title: ls("Wear debris generation", "磨损颗粒生成"),
      severity: "medium",
      probability: "medium",
      riskLevel: "yellow",
      controls: ls(
        "ASTM F2025 wear testing, bearing surface optimization",
        "ASTM F2025磨损测试、承载面优化",
      ),
      module: "Tribology",
      standard: "ASTM F2025",
    },
    {
      title: ls("Sterilization residual (EtO)", "灭菌残留（环氧乙烷）"),
      severity: "medium",
      probability: "low",
      riskLevel: "yellow",
      controls: ls(
        "ISO 11135 EtO validation, aeration cycle optimization",
        "ISO 11135 EtO验证、通风周期优化",
      ),
      module: "Sterilization",
      standard: "ISO 11135",
    },
    {
      title: ls(
        "Surgical instrument failure during procedure",
        "手术中器械故障",
      ),
      severity: "high",
      probability: "very-low",
      riskLevel: "yellow",
      controls: ls(
        "Dynamic testing per ASTM, IFU torque limits, QC inspection",
        "按ASTM进行动态测试、IFU扭矩限制、QC检查",
      ),
      module: "Instruments",
      standard: "21 CFR 820",
    },
    {
      title: ls(
        "Packaging breach compromising sterility",
        "包装破损影响无菌性",
      ),
      severity: "high",
      probability: "low",
      riskLevel: "red",
      controls: ls(
        "ASTM D4169 transport simulation, seal integrity testing",
        "ASTM D4169运输模拟、密封完整性测试",
      ),
      module: "Packaging",
      standard: "ISO 11607",
    },
  ],
  standards: [
    {
      code: "ISO 13485",
      title: ls("Quality Management Systems", "质量管理体系"),
      applies: "All",
    },
    {
      code: "ISO 14971",
      title: ls("Risk Management", "风险管理"),
      applies: "All",
    },
    {
      code: "21 CFR 820",
      title: ls("Quality System Regulation", "质量体系法规"),
      applies: "All",
    },
    {
      code: "ISO 10993",
      title: ls("Biocompatibility", "生物相容性"),
      applies: "Implants",
    },
    {
      code: "ASTM F2077",
      title: ls("Spinal Implant Fatigue Testing", "脊柱植入物疲劳测试"),
      applies: "Spinal",
    },
    {
      code: "ASTM F1264",
      title: ls("Intramedullary Fixation Devices", "髓内固定器械"),
      applies: "Trauma",
    },
    {
      code: "ISO 11607",
      title: ls(
        "Packaging for Terminally Sterilized Devices",
        "终端灭菌器械包装",
      ),
      applies: "Sterile",
    },
    {
      code: "ISO 11135",
      title: ls("EtO Sterilization", "环氧乙烷灭菌"),
      applies: "Sterile",
    },
    {
      code: "ASTM D4169",
      title: ls("Transport Package Testing", "运输包装测试"),
      applies: "All",
    },
  ],
  budgetCategories: [
    ls("Prototype & Materials", "原型和材料"),
    ls("Mechanical / Fatigue Testing", "力学/疲劳测试"),
    ls("Biocompatibility Testing", "生物相容性测试"),
    ls("Sterilization Validation", "灭菌验证"),
    ls("Packaging Validation", "包装验证"),
    ls("Regulatory & Legal", "法规和法律"),
    ls("Personnel", "人员"),
    ls("Clinical Studies", "临床研究"),
  ],
};

// ── IN VITRO DIAGNOSTICS (IVD) ──────────────────
const ivd: DeviceTemplate = {
  id: "ivd",
  name: ls("In Vitro Diagnostics (IVD)", "体外诊断 (IVD)"),
  icon: "🧪",
  description: ls(
    "Clinical chemistry analyzers, immunoassay systems, hematology instruments, point-of-care tests, molecular diagnostics",
    "临床化学分析仪、免疫分析系统、血液学仪器、即时检测、分子诊断",
  ),
  submissionType: "510k-standard",
  deviceClass: "II",
  productCodes: "LLL, JJY, GGN, QMT",
  regulationSection: "§ 862-864",
  predicateExamples:
    "Roche cobas 6000 (K173893)\nAbbott i-STAT (K163542)\nBeckman Coulter AU680 (K140968)",
  estimatedDuration: 15,
  techAreas: ls(
    "Analytical Performance (Accuracy, Precision)\nLinearity & Reportable Range\nInterference Studies\nReference Range Establishment\nSample Stability Studies\nSoftware Validation (IEC 62304)\nElectrical Safety (IEC 61010-1)\nMethod Comparison & Clinical Correlation",
    "分析性能（准确度、精密度）\n线性与可报告范围\n干扰研究\n参考范围建立\n样本稳定性研究\n软件验证 (IEC 62304)\n电气安全 (IEC 61010-1)\n方法比较与临床相关性",
  ),
  risks: [
    {
      title: ls(
        "Erroneous test result leading to misdiagnosis",
        "错误检测结果导致误诊",
      ),
      severity: "high",
      probability: "low",
      riskLevel: "red",
      controls: ls(
        "CLSI EP-series validation, QC program, multi-site clinical study",
        "CLSI EP系列验证、QC项目、多中心临床研究",
      ),
      module: "Analytical",
      standard: "CLSI EP15-A3",
    },
    {
      title: ls("Cross-reactivity / interference", "交叉反应/干扰"),
      severity: "high",
      probability: "medium",
      riskLevel: "red",
      controls: ls(
        "CLSI EP07 interference testing, known interferent panel",
        "CLSI EP07干扰测试、已知干扰物质面板",
      ),
      module: "Analytical",
      standard: "CLSI EP07",
    },
    {
      title: ls("Reagent instability / degradation", "试剂不稳定/降解"),
      severity: "medium",
      probability: "medium",
      riskLevel: "yellow",
      controls: ls(
        "Real-time stability studies, shipping condition validation",
        "实时稳定性研究、运输条件验证",
      ),
      module: "Chemistry",
      standard: "CLSI EP25",
    },
    {
      title: ls("Biohazard exposure to operator", "操作人员生物危害暴露"),
      severity: "high",
      probability: "low",
      riskLevel: "red",
      controls: ls(
        "Closed-system design, splash guards, IFU PPE requirements",
        "封闭系统设计、防溅挡板、IFU个人防护要求",
      ),
      module: "Safety",
      standard: "IEC 61010-2-101",
    },
    {
      title: ls("Software error in result calculation", "结果计算软件错误"),
      severity: "high",
      probability: "low",
      riskLevel: "red",
      controls: ls(
        "IEC 62304 lifecycle, calculation verification, audit trail",
        "IEC 62304生命周期、计算验证、审计追踪",
      ),
      module: "Software",
      standard: "IEC 62304",
    },
    {
      title: ls(
        "Calibration drift between maintenance",
        "维护间隔期间校准漂移",
      ),
      severity: "medium",
      probability: "medium",
      riskLevel: "yellow",
      controls: ls(
        "Auto-calibration, daily QC checks, drift detection algorithm",
        "自动校准、每日QC检查、漂移检测算法",
      ),
      module: "Metrology",
      standard: "CLSI EP06",
    },
  ],
  standards: [
    {
      code: "IEC 61010-1",
      title: ls("Safety -- Laboratory Equipment", "安全——实验室设备"),
      applies: "All",
    },
    {
      code: "IEC 61010-2-101",
      title: ls("IVD Medical Equipment Safety", "IVD医疗设备安全"),
      applies: "All",
    },
    {
      code: "IEC 62304",
      title: ls("Medical Device Software Lifecycle", "医疗器械软件生命周期"),
      applies: "Software",
    },
    {
      code: "ISO 14971",
      title: ls("Risk Management", "风险管理"),
      applies: "All",
    },
    {
      code: "21 CFR 820",
      title: ls("Quality System Regulation", "质量体系法规"),
      applies: "All",
    },
    {
      code: "ISO 13485",
      title: ls("Quality Management Systems", "质量管理体系"),
      applies: "All",
    },
    {
      code: "CLSI EP15-A3",
      title: ls(
        "User Verification of Precision & Bias",
        "精密度与偏差用户验证",
      ),
      applies: "Analytical",
    },
    {
      code: "CLSI EP07",
      title: ls("Interference Testing", "干扰测试"),
      applies: "Analytical",
    },
    {
      code: "CLSI EP06",
      title: ls("Linearity & Reportable Range", "线性与可报告范围"),
      applies: "Analytical",
    },
  ],
  budgetCategories: [
    ls("Prototype & Materials", "原型和材料"),
    ls("Analytical Performance Studies", "分析性能研究"),
    ls("Reference Material & Reagents", "参考物质和试剂"),
    ls("Clinical Study (Method Comparison)", "临床研究（方法比较）"),
    ls("Electrical Safety Testing", "电气安全测试"),
    ls("Software V&V", "软件V&V"),
    ls("Regulatory & Legal", "法规和法律"),
    ls("Personnel", "人员"),
  ],
};

// ── PATIENT MONITORING & IMAGING ────────────────
const imaging: DeviceTemplate = {
  id: "imaging",
  name: ls("Imaging & Monitoring", "影像与监测"),
  icon: "📡",
  description: ls(
    "Ultrasound, X-ray accessories, patient monitors, EEG, pulse oximeters, thermometers, SaMD imaging software",
    "超声、X射线附件、患者监护仪、脑电图、脉搏血氧仪、体温计、SaMD影像软件",
  ),
  submissionType: "510k-standard",
  deviceClass: "II",
  productCodes: "IYO, MUJ, DQA, DRT",
  regulationSection: "§ 892",
  predicateExamples:
    "Masimo MightySat (K200474)\nGE Vscan Air (K212984)\nNihon Kohden EEG-1200 (K163271)",
  estimatedDuration: 15,
  techAreas: ls(
    "Sensor / Transducer Design\nSignal Processing & Algorithms\nDisplay & User Interface\nImage Quality & Resolution\nElectrical Safety (IEC 60601-1)\nEMC Testing (IEC 60601-1-2)\nSoftware Validation (IEC 62304)\nUsability Testing (IEC 62366-1)",
    "传感器/换能器设计\n信号处理与算法\n显示与用户界面\n图像质量与分辨率\n电气安全 (IEC 60601-1)\nEMC测试 (IEC 60601-1-2)\n软件验证 (IEC 62304)\n可用性测试 (IEC 62366-1)",
  ),
  risks: [
    {
      title: ls("Inaccurate physiological measurement", "生理测量不准确"),
      severity: "high",
      probability: "low",
      riskLevel: "red",
      controls: ls(
        "AAMI/ISO standard testing, clinical validation study",
        "AAMI/ISO标准测试、临床验证研究",
      ),
      module: "Measurement",
      standard: "ISO 80601-2-61",
    },
    {
      title: ls("Image artifact causing misinterpretation", "图像伪影导致误判"),
      severity: "high",
      probability: "medium",
      riskLevel: "red",
      controls: ls(
        "Image quality testing, DICOM compliance, user training",
        "图像质量测试、DICOM合规、用户培训",
      ),
      module: "Imaging",
      standard: "IEC 60601-2-37",
    },
    {
      title: ls("Electrical safety -- patient contact", "电气安全——患者接触"),
      severity: "high",
      probability: "very-low",
      riskLevel: "yellow",
      controls: ls(
        "IEC 60601-1 Type BF/CF, leakage testing, isolation design",
        "IEC 60601-1 BF/CF型、泄漏测试、隔离设计",
      ),
      module: "Electrical",
      standard: "IEC 60601-1",
    },
    {
      title: ls(
        "Cybersecurity -- unauthorized data access",
        "网络安全——未授权数据访问",
      ),
      severity: "medium",
      probability: "medium",
      riskLevel: "yellow",
      controls: ls(
        "SBOM, encryption, RBAC, FDA Cyber Guidance 2023",
        "SBOM、加密、RBAC、FDA网络安全指南2023",
      ),
      module: "Cybersecurity",
      standard: "FDA Cyber Guidance",
    },
    {
      title: ls("Software failure in clinical algorithm", "临床算法软件故障"),
      severity: "high",
      probability: "low",
      riskLevel: "red",
      controls: ls(
        "IEC 62304 Class C, regression testing, SOUP management",
        "IEC 62304 C类、回归测试、SOUP管理",
      ),
      module: "Software",
      standard: "IEC 62304",
    },
    {
      title: ls(
        "Usability error in clinical workflow",
        "临床工作流程中的可用性错误",
      ),
      severity: "medium",
      probability: "medium",
      riskLevel: "yellow",
      controls: ls(
        "IEC 62366-1 formative & summative usability testing",
        "IEC 62366-1形成性和总结性可用性测试",
      ),
      module: "Usability",
      standard: "IEC 62366-1",
    },
  ],
  standards: [
    {
      code: "IEC 60601-1",
      title: ls(
        "Medical Electrical Equipment -- General",
        "医用电气设备——通用",
      ),
      applies: "All",
    },
    {
      code: "IEC 60601-1-2",
      title: ls("EMC Requirements", "EMC要求"),
      applies: "All",
    },
    {
      code: "IEC 62304",
      title: ls("Medical Device Software Lifecycle", "医疗器械软件生命周期"),
      applies: "Software",
    },
    {
      code: "IEC 62366-1",
      title: ls("Usability Engineering", "可用性工程"),
      applies: "All",
    },
    {
      code: "ISO 80601-2-61",
      title: ls("Pulse Oximeter Equipment", "脉搏血氧仪设备"),
      applies: "SpO2",
    },
    {
      code: "IEC 60601-2-37",
      title: ls("Ultrasound Diagnostic Equipment", "超声诊断设备"),
      applies: "Ultrasound",
    },
    {
      code: "ISO 14971",
      title: ls("Risk Management", "风险管理"),
      applies: "All",
    },
    {
      code: "21 CFR 820",
      title: ls("Quality System Regulation", "质量体系法规"),
      applies: "All",
    },
    {
      code: "ISO 13485",
      title: ls("Quality Management Systems", "质量管理体系"),
      applies: "All",
    },
  ],
  budgetCategories: [
    ls("Prototype & Materials", "原型和材料"),
    ls("Bench & Performance Testing", "台架与性能测试"),
    ls("EMC/Safety Testing", "EMC/安全测试"),
    ls("Software V&V", "软件V&V"),
    ls("Usability Testing", "可用性测试"),
    ls("Regulatory & Legal", "法规和法律"),
    ls("Personnel", "人员"),
    ls("Clinical Validation", "临床验证"),
  ],
};

// ── REHABILITATION & PHYSICAL MEDICINE ──────────
const rehabilitation: DeviceTemplate = {
  id: "rehabilitation",
  name: ls("Rehabilitation Devices", "康复设备"),
  icon: "🦿",
  description: ls(
    "Powered exoskeletons, neurostimulators, EMG biofeedback, therapeutic ultrasound, physical therapy devices",
    "动力外骨骼、神经刺激器、肌电生物反馈、治疗超声、物理治疗设备",
  ),
  submissionType: "510k-standard",
  deviceClass: "II",
  productCodes: "IKN, IOZ, ILZ, ITX",
  regulationSection: "§ 890",
  predicateExamples:
    "Ekso GT (K183538)\nBioness L300 Go (K173014)\nChattanooga Intelect Focus (K170512)",
  estimatedDuration: 18,
  techAreas: ls(
    "Actuator & Motor Control\nSensor Integration (EMG, IMU, Force)\nControl Algorithm & Safety Logic\nBattery & Power Management\nElectrical Safety (IEC 60601-1)\nEMC Testing (IEC 60601-1-2)\nSoftware Validation (IEC 62304)\nHuman Factors / Usability (IEC 62366-1)",
    "执行器与电机控制\n传感器集成（EMG、IMU、力传感器）\n控制算法与安全逻辑\n电池与电源管理\n电气安全 (IEC 60601-1)\nEMC测试 (IEC 60601-1-2)\n软件验证 (IEC 62304)\n人因工程/可用性 (IEC 62366-1)",
  ),
  risks: [
    {
      title: ls(
        "Unintended actuator movement causing injury",
        "执行器意外动作导致损伤",
      ),
      severity: "high",
      probability: "low",
      riskLevel: "red",
      controls: ls(
        "Torque limiters, emergency stop, range-of-motion limits",
        "扭矩限制器、紧急停止、活动范围限制",
      ),
      module: "Mechanical",
      standard: "IEC 60601-1",
    },
    {
      title: ls(
        "Electrical stimulation at incorrect intensity",
        "电刺激强度不正确",
      ),
      severity: "high",
      probability: "low",
      riskLevel: "red",
      controls: ls(
        "Hardware current limiter, software checks, IEC 60601-2-10",
        "硬件电流限制器、软件检查、IEC 60601-2-10",
      ),
      module: "Electrical",
      standard: "IEC 60601-2-10",
    },
    {
      title: ls("Battery thermal event during charging", "充电期间电池热事件"),
      severity: "high",
      probability: "very-low",
      riskLevel: "yellow",
      controls: ls(
        "UN 38.3 battery testing, thermal cutoff, BMS monitoring",
        "UN 38.3电池测试、热切断、BMS监测",
      ),
      module: "Electrical",
      standard: "IEC 62133",
    },
    {
      title: ls(
        "Skin irritation from prolonged contact",
        "长时间接触引起皮肤刺激",
      ),
      severity: "low",
      probability: "medium",
      riskLevel: "green",
      controls: ls(
        "ISO 10993 biocompatibility, breathable materials, IFU duration limits",
        "ISO 10993生物相容性、透气材料、IFU使用时间限制",
      ),
      module: "Materials",
      standard: "ISO 10993",
    },
    {
      title: ls(
        "Software fault in motion control loop",
        "运动控制回路软件故障",
      ),
      severity: "high",
      probability: "low",
      riskLevel: "red",
      controls: ls(
        "IEC 62304 Class C, watchdog timer, independent safety observer",
        "IEC 62304 C类、看门狗定时器、独立安全监视器",
      ),
      module: "Software",
      standard: "IEC 62304",
    },
    {
      title: ls(
        "User error in device fitting or operation",
        "设备佩戴或操作中的用户错误",
      ),
      severity: "medium",
      probability: "medium",
      riskLevel: "yellow",
      controls: ls(
        "IEC 62366-1 usability study, training program, quick-fit design",
        "IEC 62366-1可用性研究、培训计划、快速佩戴设计",
      ),
      module: "Usability",
      standard: "IEC 62366-1",
    },
  ],
  standards: [
    {
      code: "IEC 60601-1",
      title: ls(
        "Medical Electrical Equipment -- General",
        "医用电气设备——通用",
      ),
      applies: "All",
    },
    {
      code: "IEC 60601-1-2",
      title: ls("EMC Requirements", "EMC要求"),
      applies: "All",
    },
    {
      code: "IEC 60601-2-10",
      title: ls("Nerve & Muscle Stimulators", "神经和肌肉刺激器"),
      applies: "NMES/FES",
    },
    {
      code: "IEC 62304",
      title: ls("Medical Device Software Lifecycle", "医疗器械软件生命周期"),
      applies: "Software",
    },
    {
      code: "IEC 62366-1",
      title: ls("Usability Engineering", "可用性工程"),
      applies: "All",
    },
    {
      code: "ISO 14971",
      title: ls("Risk Management", "风险管理"),
      applies: "All",
    },
    {
      code: "ISO 10993",
      title: ls("Biocompatibility", "生物相容性"),
      applies: "Patient-contact",
    },
    {
      code: "21 CFR 820",
      title: ls("Quality System Regulation", "质量体系法规"),
      applies: "All",
    },
    {
      code: "ISO 13485",
      title: ls("Quality Management Systems", "质量管理体系"),
      applies: "All",
    },
  ],
  budgetCategories: [
    ls("Prototype & Materials", "原型和材料"),
    ls("Bench & Performance Testing", "台架与性能测试"),
    ls("Biocompatibility Testing", "生物相容性测试"),
    ls("EMC/Safety Testing", "EMC/安全测试"),
    ls("Software V&V", "软件V&V"),
    ls("Usability Testing", "可用性测试"),
    ls("Regulatory & Legal", "法规和法律"),
    ls("Personnel", "人员"),
  ],
};

// ── SOFTWARE AS MEDICAL DEVICE (SaMD) ───────────
const samd: DeviceTemplate = {
  id: "samd",
  name: ls("Software as Medical Device (SaMD)", "软件作为医疗器械 (SaMD)"),
  icon: "💻",
  description: ls(
    "Clinical decision support, diagnostic AI/ML, telehealth platforms, mobile health apps, PACS viewers",
    "临床决策支持、诊断AI/ML、远程医疗平台、移动健康应用、PACS浏览器",
  ),
  submissionType: "510k-standard",
  deviceClass: "II",
  productCodes: "QAS, QMT, QIH, LLZ",
  regulationSection: "§ 892.2020",
  predicateExamples:
    "Aidoc BriefCase AI (K201501)\nViz.ai ContaCT (K180647)\nCaption Health EF (K200980)",
  estimatedDuration: 12,
  techAreas: ls(
    "Algorithm Design & Training Data\nModel Validation (Sensitivity/Specificity)\nClinical Workflow Integration\nCybersecurity Architecture\nSoftware Architecture (IEC 62304)\nCloud/Edge Deployment Strategy\nInteroperability (HL7 FHIR, DICOM)\nReal-World Performance Monitoring",
    "算法设计与训练数据\n模型验证（灵敏度/特异度）\n临床工作流程集成\n网络安全架构\n软件架构 (IEC 62304)\n云/边缘部署策略\n互操作性 (HL7 FHIR, DICOM)\n真实世界性能监测",
  ),
  risks: [
    {
      title: ls("Algorithm bias in training data", "训练数据中的算法偏差"),
      severity: "high",
      probability: "medium",
      riskLevel: "red",
      controls: ls(
        "Diverse dataset, bias testing across demographics, GMLP practices",
        "多样化数据集、跨人口统计偏差测试、GMLP实践",
      ),
      module: "Algorithm",
      standard: "FDA AI/ML Guidance",
    },
    {
      title: ls(
        "Cybersecurity breach -- patient data",
        "网络安全漏洞——患者数据",
      ),
      severity: "high",
      probability: "medium",
      riskLevel: "red",
      controls: ls(
        "SBOM, penetration testing, HIPAA compliance, encryption at rest/transit",
        "SBOM、渗透测试、HIPAA合规、静态/传输加密",
      ),
      module: "Cybersecurity",
      standard: "FDA Cyber Guidance",
    },
    {
      title: ls(
        "False positive/negative clinical output",
        "假阳性/假阴性临床输出",
      ),
      severity: "high",
      probability: "low",
      riskLevel: "red",
      controls: ls(
        "Clinical validation study, ROC analysis, threshold optimization",
        "临床验证研究、ROC分析、阈值优化",
      ),
      module: "Algorithm",
      standard: "FDA AI/ML Guidance",
    },
    {
      title: ls("Software regression after update", "更新后的软件回归"),
      severity: "medium",
      probability: "medium",
      riskLevel: "yellow",
      controls: ls(
        "CI/CD pipeline, automated regression tests, change control",
        "CI/CD流水线、自动回归测试、变更控制",
      ),
      module: "Software",
      standard: "IEC 62304",
    },
    {
      title: ls(
        "Interoperability failure with EHR/PACS",
        "与EHR/PACS的互操作性故障",
      ),
      severity: "medium",
      probability: "medium",
      riskLevel: "yellow",
      controls: ls(
        "HL7 FHIR conformance testing, DICOM compliance, IHE profiles",
        "HL7 FHIR一致性测试、DICOM合规、IHE配置文件",
      ),
      module: "Integration",
      standard: "HL7 FHIR",
    },
    {
      title: ls(
        "Cloud service outage -- loss of availability",
        "云服务中断——可用性丧失",
      ),
      severity: "medium",
      probability: "low",
      riskLevel: "yellow",
      controls: ls(
        "Multi-region deployment, offline fallback, SLA monitoring",
        "多区域部署、离线回退、SLA监控",
      ),
      module: "Infrastructure",
      standard: "ISO 27001",
    },
  ],
  standards: [
    {
      code: "IEC 62304",
      title: ls("Medical Device Software Lifecycle", "医疗器械软件生命周期"),
      applies: "All",
    },
    {
      code: "IEC 62366-1",
      title: ls("Usability Engineering", "可用性工程"),
      applies: "All",
    },
    {
      code: "ISO 14971",
      title: ls("Risk Management", "风险管理"),
      applies: "All",
    },
    {
      code: "21 CFR 820",
      title: ls("Quality System Regulation", "质量体系法规"),
      applies: "All",
    },
    {
      code: "ISO 13485",
      title: ls("Quality Management Systems", "质量管理体系"),
      applies: "All",
    },
    {
      code: "FDA AI/ML",
      title: ls("AI/ML-Based SaMD Action Plan", "AI/ML SaMD行动计划"),
      applies: "AI/ML",
    },
    {
      code: "FDA Cyber",
      title: ls("Cybersecurity Guidance 2023", "网络安全指南2023"),
      applies: "All",
    },
    {
      code: "HIPAA",
      title: ls(
        "Health Insurance Portability & Accountability",
        "健康保险可携性和责任",
      ),
      applies: "PHI handling",
    },
    {
      code: "ISO 27001",
      title: ls("Information Security Management", "信息安全管理"),
      applies: "Cloud/SaaS",
    },
  ],
  budgetCategories: [
    ls("Algorithm Development", "算法开发"),
    ls("Training Data Acquisition", "训练数据采购"),
    ls("Clinical Validation Study", "临床验证研究"),
    ls("Cybersecurity Testing", "网络安全测试"),
    ls("Software V&V", "软件V&V"),
    ls("Cloud Infrastructure", "云基础设施"),
    ls("Regulatory & Legal", "法规和法律"),
    ls("Personnel", "人员"),
  ],
};

// ── EXPORT ALL TEMPLATES ────────────────────────
export const DEVICE_TEMPLATES: Record<string, DeviceTemplate> = {
  respiratory,
  cardiovascular,
  orthopedic,
  ivd,
  imaging,
  rehabilitation,
  samd,
};

export const TEMPLATE_LIST: DeviceTemplate[] = [
  respiratory,
  cardiovascular,
  orthopedic,
  ivd,
  imaging,
  rehabilitation,
  samd,
];
