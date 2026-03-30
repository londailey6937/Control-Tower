// ============================================================
// DATA MODEL — 510(k) Medical Device PM Dashboard
// Sourced from FDA 510(k) Pre-Submission Package (March 2026)
// PMP is overriding authority; accepts input from biz & tech
// ============================================================

import type {
  Project,
  Tracks,
  Gate,
  Risk,
  Standard,
  TimelineEvent,
  StakeholderInput,
  CashRunway,
  ChangeRequest,
  UserRole,
  AuditEntry,
  DHFDocument,
  CAPAItem,
  ActionItem,
  BudgetCategory,
  TeamMember,
  Supplier,
  QASection,
} from "./types.ts";

export const PROJECT: Project = {
  name: {
    en: "510(k) Medical Device Project",
    cn: "510(k)医疗器械项目",
  },
  subtitle: {
    en: "FDA 510(k) Clearance Program",
    cn: "FDA 510(k)审批项目",
  },
  submissionType:
    "510(k) (pathway pending Pre-Sub confirmation)",
  applicant: {
    en: "US Operating Entity",
    cn: "美国运营实体",
  },
  manufacturer: {
    en: "Contract Manufacturer",
    cn: "合同制造商",
  },
  preparedDate: "March 2026",
  currentMonth: 0,
};

// ============================================================
// DUAL-TRACK: Technical + Regulatory milestones
// ============================================================

export const TRACKS: Tracks = {
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
        detail: {
          en: "The sEMG Module (Module A) is the first hardware product in the ICU Respiratory Digital Twin platform. This milestone locks the production-intent design:\n\n- Electrode Array: 4–8 surface electrodes placed on the chest and intercostal muscles to capture neural respiratory drive (NRD) — the brain's command to breathe.\n- 24-bit ADC: High-resolution analog-to-digital conversion ensures micro-volt level EMG signals are captured without quantization noise.\n- 2000 Hz Sampling: Nyquist-compliant rate for EMG bandwidth (10–500 Hz), with headroom for the proprietary ECG-gating filter.\n- BT Wireless Isolation: Bluetooth Low Energy link provides galvanic isolation between patient-contact electrodes and the bedside display, satisfying IEC 60601-1-2 EMC requirements.\n- FDA Product Code: IKN (Electromyograph, diagnostic). Primary predicate: Maquet NAVA Edi catheter (K082437). Pathway: standard 510(k).\n\nCompletion of T1 means the PCB layout, enclosure, and firmware are frozen for verification testing (T3).",
          cn: "sEMG模块（A模块）是ICU呼吸数字孪生平台的首个硬件产品。此里程碑锁定生产级设计：\n\n- 电极阵列：4-8个表面电极布置于胸壁和肋间肌，捕获神经呼吸驱动（NRD）— 大脑的呼吸指令。\n- 24位ADC：高分辨率模数转换确保微伏级EMG信号无量化噪声捕获。\n- 2000Hz采样：符合EMG带宽（10-500Hz）的奈奎斯特率，为专有ECG门控滤波预留空间。\n- 蓝牙无线隔离：低功耗蓝牙链路在患者接触电极与床旁显示器之间提供电气隔离，满足IEC 60601-1-2 EMC要求。\n- FDA产品代码：IKN（诊断用肌电描记器）。标准510(k)前置器械途径。\n\n完成T1意味着PCB布局、外壳和固件已冻结，可进入验证测试（T3）。",
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
        detail: {
          en: "Surface EMG electrodes on the chest inevitably pick up the heart's QRS complex, which can be 10–100× larger than the diaphragm EMG signal. The ECG-gating algorithm is the core IP that makes bedside NRD monitoring viable:\n\n- Adaptive Filtering: A real-time filter detects each R-wave peak and subtracts a template of the cardiac artifact, preserving the underlying EMG waveform.\n- SNR >20 dB: After gating, the respiratory EMG signal stands ≥20 dB above residual noise — enough for reliable NRD amplitude and timing extraction.\n- Suppression >98%: The QRS artifact energy is reduced by at least 98%, validated against simultaneous esophageal catheter EMG (gold standard).\n- Latency: Processing pipeline adds &lt;5 ms end-to-end, ensuring real-time breath-by-breath display.\n\nThis milestone is validated by running the algorithm on a dataset of ≥30 ICU patients and comparing surface NRD indices against esophageal EMG reference values.",
          cn: "胸壁表面EMG电极不可避免地会拾取心脏QRS波群，其幅值是膈肌EMG信号的10-100倍。ECG门控算法是使床旁NRD监测实现的核心知识产权：\n\n- 自适应滤波：实时滤波器检测每个R波峰值，减去心脏伪影模板，保留底层EMG波形。\n- 信噪比>20dB：门控后呼吸EMG信号高出残余噪声≥20dB，足以可靠提取NRD幅值和时序。\n- 抑制>98%：QRS伪影能量降低至少98%，通过同步食管导管EMG（金标准）验证。\n- 延迟：处理管道端到端增加&lt;5ms，确保实时逐次呼吸显示。\n\n此里程碑通过在≥30名ICU患者数据集上运行算法并将表面NRD指标与食管EMG参考值进行比较来验证。",
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
        detail: {
          en: "Bench and performance testing is the most comprehensive verification milestone for the sEMG module. It generates the data package that will form the backbone of the 510(k) submission:\n\n- IEC 60601-1 Electrical Safety: Leakage current, dielectric strength, protective earth, creepage/clearance distance measurements performed at an accredited NRTL (e.g., Intertek, TÜV).\n- EMC Testing (IEC 60601-1-2): Radiated emissions, conducted emissions, ESD immunity, radiated immunity, and surge immunity. The BT radio module must coexist with ICU infusion pumps and ventilators.\n- Usability Study (IEC 62366): Formative usability evaluation with ≥15 clinicians — electrode placement, display interpretation, alarm response. Task success rate, use errors, and hazardous use scenarios documented.\n- Algorithm Validation: Head-to-head comparison of surface sEMG NRD vs. esophageal catheter EMG in ≥30 mechanically ventilated patients. Statistical analysis (Bland-Altman, ICC) for sensitivity ≥92% and specificity ≥88%.\n\nAll test reports feed into the Design History File (DHF) and are cross-referenced in the 510(k) summary.",
          cn: "台架和性能测试是sEMG模块最全面的验证里程碑，生成的数据包将构成510(k)提交的骨干：\n\n- IEC 60601-1电气安全：漏电流、介电强度、保护接地、爬电/间隙距离测量，由认可的NRTL（如Intertek、TÜV）执行。\n- EMC测试（IEC 60601-1-2）：辐射发射、传导发射、ESD抗扰度、辐射抗扰度和浪涌抗扰度。蓝牙射频模块必须与ICU输液泵和呼吸机共存。\n- 可用性研究（IEC 62366）：与≥15名临床医生进行形成性可用性评估——电极放置、显示解读、报警响应。记录任务成功率、使用错误和危险使用场景。\n- 算法验证：在≥30名机械通气患者中进行表面sEMG NRD与食管导管EMG的头对头比较。统计分析（Bland-Altman、ICC）确认灵敏度≥92%、特异性≥88%。\n\n所有测试报告纳入设计历史文件（DHF），并在510(k)摘要中交叉引用。",
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
          en: "NRD detection sensitivity ≥92%, asynchrony specificity ≥88%, signal latency &lt;50ms",
          cn: "NRD检测灵敏度≥92%, 异步特异性≥88%, 信号延迟&lt;50ms",
        },
        detail: {
          en: "This milestone confirms the sEMG module meets its three key performance acceptance criteria — the numbers that will appear in the 510(k) Performance Testing section:\n\n- NRD Detection Sensitivity ≥92%: Of all true neural inspiratory efforts (confirmed by esophageal EMG), the surface device correctly identifies ≥92%. Missed breaths below this threshold would pose a clinical safety risk for weaning assessment.\n- Asynchrony Specificity ≥88%: When the system flags a patient-ventilator asynchrony event (trigger delay, double-trigger, ineffective effort), it is correct ≥88% of the time. False alarms waste clinician attention; false negatives miss dangerous dyssynchrony.\n- Signal Latency &lt;50 ms: From electrode pickup to on-screen NRD waveform, total pipeline delay is under 50 ms — enabling real-time overlay with the ventilator pressure/flow waveform.\n\nThese targets were derived from the clinical literature on esophageal EMG monitoring and from FDA reviewer expectations documented in similar device clearances (e.g., Maquet NAVA K082437, product code IKN).",
          cn: "此里程碑确认sEMG模块满足三个关键性能验收标准——这些数字将出现在510(k)性能测试部分：\n\n- NRD检测灵敏度≥92%：在所有真实神经吸气努力中（由食管EMG确认），表面设备正确识别≥92%。低于此阈值的漏检在脱机评估中构成临床安全风险。\n- 异步特异性≥88%：当系统标记患者-呼吸机异步事件（触发延迟、双触发、无效努力）时，≥88%的情况是正确的。误报浪费临床医生注意力；漏报错过危险的不同步。\n- 信号延迟&lt;50ms：从电极拾取到屏幕NRD波形，总管道延迟低于50ms——可与呼吸机压力/流量波形实时叠加。\n\n这些目标源自食管EMG监测临床文献和类似设备清许（如Maquet NAVA K082437, 产品代码IKN）中记录的FDA审评员期望。",
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
        detail: {
          en: "The EIT module (Module B) is the second cornerstone of the Digital Twin. Electrical Impedance Tomography creates real-time cross-sectional images of the lungs without radiation:\n\n- 32-Electrode Belt: A flexible silicone belt wraps around the thorax at the 5th–6th intercostal space. 32 equispaced Ag/AgCl electrodes inject tiny AC currents and measure resulting boundary voltages.\n- 50 kHz AC Injection: A safe, sub-milliamp alternating current at 50 kHz. At this frequency, impedance contrasts between air-filled lung, collapsed lung, fluid, and blood are maximized.\n- 50 Hz Frame Rate: 50 complete impedance images per second — fast enough to track ventilation and cardiac-related perfusion in real time, breath-by-breath.\n- 32×32 Reconstruction: A regularized inverse solver converts 32-electrode boundary voltages into a 32×32 pixel conductivity map of the chest cross-section. Regional ventilation and perfusion are quantified per pixel.\n\nThe prototype uses the Timpel Enlight 2100 (K250464) as the predicate device (FDA product code DQS). T5 freezes the hardware for biocompatibility testing (T7) and V/Q algorithm validation (T6).",
          cn: "EIT模块（B模块）是数字孪生的第二个基石。电阻抗断层成像可在无辐射情况下实时创建肺部横截面图像：\n\n- 32电极带：柔性硅胶带环绕胸廓第5-6肋间隙。32个等距Ag/AgCl电极注入微小交流电流并测量边界电压。\n- 50kHz交流注入：安全的亚毫安级50kHz交流电流。在此频率下，充气肺、塌陷肺、液体和血液之间的阻抗对比最大化。\n- 50Hz帧率：每秒50幅完整阻抗图像——足以实时逐次呼吸追踪通气和心脏相关灌注。\n- 32×32重建：正则化逆求解器将32电极边界电压转换为胸部横截面的32×32像素电导率图。按像素量化区域通气和灌注。\n\n原型以Timpel Enlight作为前置设备（FDA产品代码DQS）。T5冻结硬件以进行生物相容性测试（T7）和V/Q算法验证（T6）。",
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
        detail: {
          en: "The V/Q (ventilation/perfusion) algorithm is the software innovation that differentiates our EIT system from basic impedance imaging. It separates the impedance signal into two physiological components:\n\n- Ventilation Map: Impedance changes synchronized with breathing (tidal variation). Shows regional air distribution — where the lung is being ventilated and where it is not.\n- Perfusion Map: Impedance changes synchronized with the cardiac cycle (pulsatile blood flow). Shows regional blood flow distribution — critical for detecting V/Q mismatch.\n- Accuracy >85% vs. DCE-CT: Dynamic contrast-enhanced CT is the clinical gold standard for V/Q imaging. Our algorithm must achieve >85% spatial agreement (Dice coefficient) with DCE-CT maps across ≥20 patients.\n- Ventilation Sensitivity ≥90%: In regions confirmed as ventilated by CT, the EIT algorithm correctly classifies ≥90% of them.\n- Perfusion SNR >15 dB: The cardiac-related impedance pulsation (perfusion signal) must stand ≥15 dB above noise floor after cardiac-gated averaging.\n\nThis validation is the 510(k) performance data centerpiece for the EIT submission — it establishes substantial equivalence to the Timpel Enlight predicate.",
          cn: "V/Q（通气/灌注）算法是使我们EIT系统区别于基础阻抗成像的软件创新。它将阻抗信号分离为两个生理成分：\n\n- 通气图：与呼吸同步的阻抗变化（潮气变化）。显示区域空气分布——哪里被通气，哪里没有。\n- 灌注图：与心脏周期同步的阻抗变化（搏动性血流）。显示区域血流分布——对检测V/Q失配至关重要。\n- 准确度>85%对比DCE-CT：动态增强CT是V/Q成像的临床金标准。我们的算法必须在≥20名患者中实现>85%的空间一致性（Dice系数）。\n- 通气灵敏度≥90%：在CT确认通气的区域中，EIT算法正确分类≥90%。\n- 灌注信噪比>15dB：心脏相关阻抗搏动（灌注信号）经心脏门控平均后必须高出噪声基底≥15dB。\n\n此验证是EIT提交510(k)性能数据的核心——它建立与Timpel Enlight前置设备的实质等效性。",
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
        detail: {
          en: "Any device component that contacts the patient's skin requires biocompatibility evaluation per ISO 10993. For the EIT belt and electrodes:\n\n- ISO 10993-5 Cytotoxicity: In-vitro test exposing mammalian cell cultures to belt/electrode material extracts. Verifies the silicone belt, Ag/AgCl electrodes, and conductive gel do not release toxic leachables that kill or damage cells.\n- ISO 10993-10 Sensitization: Guinea pig maximization test (GPMT) or local lymph node assay (LLNA) to confirm electrode materials do not trigger delayed-type allergic reactions after repeated skin contact (24-hour wear cycles in ICU).\n- ISO 10993-10 Irritation: Dermal irritation study verifying no erythema, edema, or skin breakdown from prolonged belt wear (up to 72 hours continuous, typical ICU monitoring duration).\n\nBiocompatibility testing is outsourced to an ISO 17025-accredited lab (e.g., Nelson Labs, NAMSA). Results are included in the EIT 510(k) submission (R6) and filed in the DHF. Test samples are taken from production-equivalent materials, not lab prototypes.",
          cn: "任何接触患者皮肤的设备组件都需要按ISO 10993进行生物相容性评估。对于EIT带和电极：\n\n- ISO 10993-5细胞毒性：体外测试，将哺乳动物细胞培养物暴露于带/电极材料提取物。验证硅胶带、Ag/AgCl电极和导电凝胶不释放杀死或损伤细胞的有毒可浸出物。\n- ISO 10993-10致敏：豚鼠最大化试验（GPMT）或局部淋巴结试验（LLNA），确认电极材料在反复皮肤接触后不触发迟发型过敏反应（ICU中24小时佩戴周期）。\n- ISO 10993-10刺激：皮肤刺激研究，验证长时间佩戴带不出现红斑、水肿或皮肤破损（最长72小时连续佩戴，典型ICU监测时长）。\n\n生物相容性测试外包给ISO 17025认可实验室（如Nelson Labs、NAMSA）。结果纳入EIT 510(k)提交（R6）并归入DHF。测试样品取自生产等效材料，非实验室原型。",
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
          en: "&lt;1ms timestamp alignment between sEMG and EIT. AES-256 encryption, RBAC, HL7 FHIR output",
          cn: "&lt;1ms时间戳对齐sEMG和EIT。AES-256加密, RBAC, HL7 FHIR输出",
        },
        detail: {
          en: "MyoBus is the proprietary middleware protocol that fuses the two hardware modules into a single Digital Twin data stream. It solves four critical integration challenges:\n\n- Timestamp Synchronization (&lt;1 ms): sEMG and EIT sample at different rates (2000 Hz vs. 50 Hz). MyoBus uses a shared PTP (Precision Time Protocol) clock to align every sample pair to within 1 ms, so clinicians see a unified respiratory picture — muscle effort and lung image in perfect register.\n- AES-256 Encryption: All data in transit between modules and the bedside display is encrypted with AES-256-GCM. PHI never travels in the clear, satisfying HIPAA technical safeguards (§164.312(e)(1)).\n- Role-Based Access Control (RBAC): MyoBus enforces user roles — attending physician (full access), respiratory therapist (waveform + alerts), nurse (alerts only), biomedical engineer (configuration). Mapped to the hospital's Active Directory / LDAP.\n- HL7 FHIR Output: The fused data stream is also published as HL7 FHIR Observation resources, enabling integration with the hospital's EHR (Epic, Cerner) and third-party clinical decision support systems.\n\nMyoBus is classified as Software in a Medical Device (SiMD) by the FDA. Its software architecture, cybersecurity risk assessment, and SBOM are documented per FDA's 2023 cybersecurity guidance.",
          cn: "MyoBus是将两个硬件模块融合为单一数字孪生数据流的专有中间件协议。它解决四个关键集成挑战：\n\n- 时间戳同步（&lt;1ms）：sEMG和EIT以不同速率采样（2000Hz vs 50Hz）。MyoBus使用共享PTP（精密时间协议）时钟将每对样本对齐到1ms以内，使临床医生看到统一的呼吸图景——肌肉努力和肺部图像完美配准。\n- AES-256加密：模块间及床旁显示器之间所有传输数据均用AES-256-GCM加密。PHI从不以明文传输，满足HIPAA技术保障要求（§164.312(e)(1)）。\n- 基于角色的访问控制（RBAC）：MyoBus强制执行用户角色——主治医生（完全访问）、呼吸治疗师（波形+警报）、护士（仅警报）、生物医学工程师（配置）。映射到医院的Active Directory/LDAP。\n- HL7 FHIR输出：融合数据流同时发布为HL7 FHIR Observation资源，实现与医院EHR（Epic、Cerner）和第三方临床决策支持系统的集成。\n\nMyoBus被FDA归类为医疗器械中的软件（SiMD）。其软件架构、网络安全风险评估和SBOM按FDA 2023年网络安全指南编制。",
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
        detail: {
          en: "A Pre-Submission (Pre-Sub) is a formal mechanism under 21 CFR for requesting FDA feedback before filing a 510(k). The Q-Meeting (Question-based) format is the most common type:\n\n- Purpose: Present our proposed regulatory strategy to the FDA's Center for Devices and Radiological Health (CDRH) and get written feedback before committing resources to testing.\n- Key Questions Filed:\n  1. Predicate Selection — Is the Maquet NAVA Edi catheter (K082437, product code IKN) an appropriate predicate for our surface sEMG NRD monitor? Are there other predicates FDA recommends?\n  2. Testing Protocol — Does FDA agree our proposed bench and clinical validation protocol (n≥30 patients, esophageal EMG reference) is sufficient for substantial equivalence?\n  3. SiMD Classification — Should the MyoBus software and NRD algorithms be classified as Software in a Medical Device (SiMD) or Software as a Medical Device (SaMD)? This affects the software documentation requirements.\n- Format: We submit a Pre-Sub package (device description, proposed testing, specific questions) and receive written feedback within 75 days, typically followed by a teleconference.\n\nFiling R1 at M+0 enables us to get FDA alignment early, avoiding costly rework later in the testing phase.",
          cn: "预提交（Pre-Sub）是21 CFR下在提交510(k)之前请求FDA反馈的正式机制。基于问题的Q会议格式最为常见：\n\n- 目的：向FDA器械和放射健康中心（CDRH）展示我们提议的监管策略，在投入测试资源前获得书面反馈。\n- 提交的关键问题：\n  1. 前置器械选择 — Maquet NAVA Edi导管（K082437, 产品代码IKN）是否适合作为我们表面sEMG NRD监测器的前置器械？FDA是否推荐其他前置器械？\n  2. 测试方案 — FDA是否同意我们提议的台架和临床验证方案（n≥30名患者，食管EMG参考）足以证明实质等效？\n  3. SiMD分类 — MyoBus软件和NRD算法应归类为医疗器械中的软件（SiMD）还是作为医疗器械的软件（SaMD）？这影响软件文档要求。\n- 格式：提交Pre-Sub包（设备描述、拟议测试、具体问题），75天内收到书面反馈，通常随后进行电话会议。\n\n在M+0提交R1使我们能尽早获得FDA一致意见，避免测试阶段后期的高成本返工。",
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
        detail: {
          en: "The Pre-Submission meeting is the interactive follow-up to the Q-Sub filing (R1). This is where we receive and discuss FDA's written feedback:\n\n- Meeting Format: Typically a 60-minute teleconference with the CDRH review team (lead reviewer, branch chief, software specialist). Sometimes in-person at FDA White Oak campus.\n- Written Feedback: FDA issues a formal letter responding to each question from R1. This letter becomes a binding reference document we can cite in the 510(k) submission.\n- SE Strategy Discussion: FDA confirms or challenges our substantial equivalence strategy — which predicate(s) are acceptable, what comparative testing they expect, and whether the technology raises any new safety/effectiveness questions.\n- Testing Protocol Agreement: The most critical outcome. If FDA agrees to our proposed test protocol, we can proceed with confidence. If they request additional tests or a larger sample size, we adjust the timeline and budget now, not after spending months on testing.\n- Software Classification: FDA clarifies SiMD vs. SaMD classification and the software documentation level (Basic, Enhanced, or Comprehensive) per the 2023 Content of Premarket Submissions guidance.\n\nHaving clear FDA alignment from R2 de-risks the entire regulatory timeline from R3 through R4.",
          cn: "预提交会议是Q-Sub提交（R1）后的互动跟进。在此处我们接收并讨论FDA的书面反馈：\n\n- 会议格式：通常与CDRH审查团队（主审员、分支主管、软件专家）进行60分钟电话会议。有时在FDA White Oak园区面对面。\n- 书面反馈：FDA就R1中的每个问题发出正式信函。此信成为我们可在510(k)提交中引用的约束性参考文件。\n- SE策略讨论：FDA确认或质疑我们的实质等效策略——哪些前置器械可接受，他们期望什么比较测试，以及该技术是否引发新的安全性/有效性问题。\n- 测试方案协议：最关键成果。如果FDA同意拟议测试方案，我们可信心十足地推进。如果他们要求额外测试或更大样本量，我们现在调整时间线和预算，而非测试数月后再调整。\n- 软件分类：FDA明确SiMD vs. SaMD分类和软件文档级别（基础、增强或综合），按2023年上市前提交内容指南。\n\n从R2获得明确的FDA一致意见可降低从R3到R4整个监管时间线的风险。",
        },
        status: "not-started",
        owner: "regulatory",
        category: "meeting",
      },
      {
        id: "R3",
        month: 6,
        title: {
          en: "510(k) Submission — sEMG Module",
          cn: "510(k)提交 — sEMG模块",
        },
        description: {
          en: "Complete package: Cover letter, Device Description, SE Discussion, Performance Testing, Risk Analysis, Biocompatibility, Software, Labeling",
          cn: "完整包: 附信、设备描述、SE讨论、性能测试、风险分析、生物相容性、软件、标签",
        },
        detail: {
          en: "The 510(k) submission is the culmination of all prior technical and regulatory milestones for the sEMG module. The complete package includes:\n\n- Cover Letter & Administrative: Device name, applicant (Company B USA), classification (product code IKN), establishment registration.\n- Device Description: Detailed hardware/software architecture — electrode array, ADC, BT module, firmware, and MyoBus protocol. Block diagrams, photos, and component specifications.\n- Substantial Equivalence Discussion: Side-by-side comparison with the predicate device (as confirmed in R2). Covers intended use, technology, performance characteristics, and biocompatibility.\n- Performance Testing Report: All data from T3 (bench testing) and T4 (sensitivity/specificity). Includes IEC 60601-1 safety, EMC, usability, and clinical validation results.\n- Risk Analysis: ISO 14971 risk management file — hazard identification, risk estimation, risk evaluation, and risk control measures. Top risks: electrode detachment, ECG mis-gating, wireless interference.\n- Software Documentation: Per FDA guidance — software requirements, architecture, verification testing, cybersecurity (AES-256, SBOM), and SOUP/OTS documentation.\n- Biocompatibility: Electrode materials testing per ISO 10993 (surface contact &lt;24 hours category).\n- Labeling: Instructions for Use (IFU), clinician quick-start guide, package labeling per 21 CFR 801.\n\nThe submission is filed through FDA's eSTAR electronic system. Standard review timeline is ~90 days to clearance (R4).",
          cn: "510(k)提交是sEMG模块所有先前技术和监管里程碑的结晶。完整包包括：\n\n- 附信和行政文件：设备名称、申请人（Company B USA）、分类（产品代码IKN）、机构注册。\n- 设备描述：详细的硬件/软件架构——电极阵列、ADC、蓝牙模块、固件和MyoBus协议。框图、照片和组件规格。\n- 实质等效讨论：与前置设备（R2中确认）的逐项比较。涵盖预期用途、技术、性能特征和生物相容性。\n- 性能测试报告：T3（台架测试）和T4（灵敏度/特异性）的所有数据。包括IEC 60601-1安全、EMC、可用性和临床验证结果。\n- 风险分析：ISO 14971风险管理文件——危害识别、风险估计、风险评价和风险控制措施。主要风险：电极脱落、ECG误门控、无线干扰。\n- 软件文档：按FDA指南——软件需求、架构、验证测试、网络安全（AES-256、SBOM）和SOUP/OTS文档。\n- 生物相容性：电极材料按ISO 10993测试（表面接触&lt;24小时类别）。\n- 标签：使用说明（IFU）、临床医生快速入门指南、按21 CFR 801的包装标签。\n\n通过FDA的eSTAR电子系统提交。标准审查时间约90天到获批（R4）。",
        },
        status: "not-started",
        owner: "regulatory",
        category: "submission",
      },
      {
        id: "R4",
        month: 9,
        title: {
          en: "Expected 510(k) Clearance — sEMG",
          cn: "预计510(k)批准 — sEMG",
        },
        description: {
          en: "Standard 510(k) review ~90 days. IKN product code clearance → Module A commercial launch",
          cn: "标准510(k)审查约90天。IKN产品代码批准 → A模块商业发布",
        },
        detail: {
          en: "This milestone marks the expected FDA clearance of the sEMG module — the go-to-market gate for Module A:\n\n- Review Timeline: Standard 510(k) reviews average ~90 calendar days from acceptance to decision. The FDA MDUFA V user fee goal is 90 days for 90% of standard 510(k)s.\n- Possible Outcomes:\n  1. Clearance (SE Order) — FDA determines substantial equivalence. We receive a clearance letter and K-number. Commercial sales can begin immediately.\n  2. Additional Information (AI) Request — FDA requests clarification or additional testing data. Clock stops while we respond (typically 30–60 days to prepare response). Common AI topics: labeling clarification, additional performance data breakdowns, software documentation updates.\n  3. Not Substantially Equivalent (NSE) — Rare for well-prepared Pre-Sub-aligned submissions. Would require either a de novo pathway or redesign.\n- Post-Clearance Actions: Upon clearance, we register the device establishment, list the device with FDA, begin Quality System compliance monitoring (21 CFR 820), and initiate Module A commercial launch with KOL sites.\n- Revenue Impact: Module A clearance enables Phase 1 revenue — the sEMG NRD monitor as a standalone clinical device, generating cash flow while Module B (EIT) continues development.\n\nThe 90-day window from R3 to R4 assumes no AI requests. A 30-day AI buffer is built into the project risk register.",
          cn: "此里程碑标志着sEMG模块的预期FDA批准——A模块的上市门槛：\n\n- 审查时间线：标准510(k)审查从受理到决定平均约90个日历天。FDA MDUFA V用户费目标为90%的标准510(k)在90天内完成。\n- 可能结果：\n  1. 批准（SE令）——FDA确定实质等效。收到批准信和K编号。可立即开始商业销售。\n  2. 补充信息（AI）请求——FDA要求澄清或额外测试数据。时钟暂停直到我们回复（通常30-60天准备响应）。常见AI话题：标签澄清、额外性能数据细分、软件文档更新。\n  3. 非实质等效（NSE）——对于经过良好Pre-Sub对齐的提交罕见。需要走de novo途径或重新设计。\n- 批准后行动：获批后注册设备机构、在FDA列出设备、开始质量体系合规监测（21 CFR 820），并与KOL站点启动A模块商业发布。\n- 收入影响：A模块获批启动第一阶段收入——sEMG NRD监测器作为独立临床设备，在B模块（EIT）继续开发期间产生现金流。\n\n从R3到R4的90天窗口假设无AI请求。项目风险登记册中已包含30天AI缓冲。",
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
        detail: {
          en: "R5 marks the kickoff of the second 510(k) regulatory package — for the EIT system (Module B). This preparation phase runs in parallel with EIT technical milestones:\n\n- V/Q Validation Data Package: Compile all results from T6 (V/Q algorithm validation vs. DCE-CT). Structure the performance testing report to match the format agreed with FDA in the Pre-Sub (R2).\n- Belt Biocompatibility: Compile ISO 10993-5 and -10 test reports from T7. The EIT belt has prolonged skin contact (>24 hours continuous in ICU), which places it in a higher biocompatibility risk category than the sEMG electrodes.\n- EIT-Specific EMC: The EIT system injects AC current — it is both an emitter (50 kHz injection) and a receiver (boundary voltages). EMC testing must verify the belt's injection signal does not interfere with nearby medical devices (ventilators, infusion pumps, patient monitors) and that external EMI does not corrupt impedance measurements.\n- Predicate Alignment: Finalize the substantial equivalence discussion for the Timpel Enlight (product code DQS). Map our V/Q imaging capabilities to the predicate's functional claims.\n- DHF Assembly: Consolidate all design inputs, verification outputs, risk analysis updates, and traceability matrices into the EIT section of the Design History File.\n\nR5 runs for approximately 5 months (M+12 to M+17) before the EIT 510(k) is filed at R6.",
          cn: "R5标志着第二个510(k)监管包——EIT系统（B模块）——准备工作的启动。此准备阶段与EIT技术里程碑并行运行：\n\n- V/Q验证数据包：编译T6（V/Q算法验证对比DCE-CT）的所有结果。按Pre-Sub（R2）中与FDA协议的格式组织性能测试报告。\n- 带生物相容性：编译T7的ISO 10993-5和-10测试报告。EIT带为长时间皮肤接触（ICU中>24小时连续），属于比sEMG电极更高的生物相容性风险类别。\n- EIT专用EMC：EIT系统注入交流电——它既是发射器（50kHz注入）又是接收器（边界电压）。EMC测试必须验证带的注入信号不干扰附近医疗设备（呼吸机、输液泵、患者监护仪），且外部EMI不损坏阻抗测量。\n- 前置器械对齐：确定与Timpel Enlight（产品代码DQS）的实质等效讨论。将V/Q成像能力映射到前置器械的功能声明。\n- DHF组装：将所有设计输入、验证输出、风险分析更新和追溯矩阵整合到设计历史文件的EIT部分。\n\nR5运行约5个月（M+12到M+17），之后在R6提交EIT 510(k)。",
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
          en: "DQS product code, Timpel Enlight K250464 as primary predicate. V/Q imaging as performance enhancement",
          cn: "DQS产品代码, Timpel Enlight K250464作为主要前置器械。V/Q成像作为性能增强",
        },
        detail: {
          en: "The EIT 510(k) submission is the second major regulatory filing — for Module B (EIT system with V/Q imaging). It follows the same structure as R3 but with EIT-specific content:\n\n- Product Code DQS: Impedance plethysmograph classification. The predicate device is the Timpel Enlight, the only FDA-cleared EIT system for lung imaging.\n- V/Q Imaging Claim: Our key differentiator. The Timpel Enlight provides ventilation imaging only. We claim both ventilation AND perfusion imaging via the proprietary V/Q separation algorithm. This is positioned as a performance enhancement over the predicate, not a new intended use.\n- Performance Data: T6 validation results (V/Q accuracy >85% vs. DCE-CT), T7 biocompatibility reports, EIT-specific EMC testing, and the 32-electrode belt mechanical testing.\n- Software Documentation: The V/Q algorithm is SiMD Level of Concern: Enhanced (per FDA 2023 guidance). Full software architecture, verification, SBOM, and cybersecurity documentation.\n- Integrated Platform Statement: While the EIT module is cleared independently, the submission includes a description of the MyoBus integration for the combined sEMG+EIT Digital Twin platform. This lays groundwork for the future integrated platform claim.\n\nThe EIT 510(k) represents the highest regulatory risk in the project because of the novel V/Q perfusion imaging claim. The Pre-Sub feedback (R2) is critical for de-risking this submission.",
          cn: "EIT 510(k)提交是第二个主要监管申报——针对B模块（带V/Q成像的EIT系统）。结构与R3相同，但包含EIT特定内容：\n\n- 产品代码DQS：阻抗体积描记器分类。前置设备是Timpel Enlight，唯一FDA批准的肺部成像EIT系统。\n- V/Q成像声明：我们的关键差异化。Timpel Enlight仅提供通气成像。我们通过专有V/Q分离算法声明通气和灌注成像。这被定位为对前置器械的性能增强，而非新的预期用途。\n- 性能数据：T6验证结果（V/Q准确度>85%对比DCE-CT）、T7生物相容性报告、EIT专用EMC测试和32电极带机械测试。\n- 软件文档：V/Q算法为SiMD关注级别：增强（按FDA 2023指南）。完整的软件架构、验证、SBOM和网络安全文档。\n- 集成平台声明：虽然EIT模块独立获批，提交中包含MyoBus集成描述用于组合sEMG+EIT数字孪生平台。为未来集成平台声明奠定基础。\n\nEIT 510(k)代表项目中最高的监管风险，因为新颖的V/Q灌注成像声明。Pre-Sub反馈（R2）对降低此提交风险至关重要。",
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
        detail: {
          en: "R7 is the program's culminating regulatory milestone — FDA clearance of the EIT system, completing the dual-module Digital Twin platform:\n\n- Full Platform Available: With both sEMG (cleared at R4) and EIT (cleared at R7) on the market, hospitals can deploy the complete ICU Respiratory Digital Twin — real-time muscle drive monitoring plus lung impedance imaging on a single bedside display via MyoBus.\n- Integrated Platform Claim: Upon EIT clearance, we file a 510(k) amendment or supplement to formally claim the integrated sEMG+EIT platform as a single system. This unified labeling enables marketing the combined solution.\n- Clinical Deployment: Initial deployment at 3–5 KOL academic medical centers for clinical validation and publication generation. Target: peer-reviewed publications demonstrating improved weaning success rates and reduced ventilator days.\n- Post-Market Surveillance: Both modules enter the post-market phase. Complaint handling, medical device reporting (MDR per 21 CFR 803), and annual registration renewal procedures activated.\n- Revenue Milestone: Module B clearance unlocks the premium pricing tier — the combined Digital Twin system commands significantly higher value than the standalone sEMG monitor.\n\nR7 at M+23 marks the end of the 23-month regulatory timeline and the beginning of the commercial growth phase.",
          cn: "R7是项目的最终监管里程碑——EIT系统FDA批准，完成双模块数字孪生平台：\n\n- 完整平台可用：sEMG（R4获批）和EIT（R7获批）均上市后，医院可部署完整的ICU呼吸数字孪生——通过MyoBus在单一床旁显示器上实现实时肌肉驱动监测加肺阻抗成像。\n- 集成平台声明：EIT获批后，提交510(k)修正或补充，正式声明集成sEMG+EIT平台为单一系统。统一标签可营销组合解决方案。\n- 临床部署：在3-5所KOL学术医疗中心初始部署，进行临床验证和发表论文。目标：同行评审出版物证明改善脱机成功率和减少呼吸机天数。\n- 上市后监督：两个模块进入上市后阶段。投诉处理、医疗器械报告（按21 CFR 803的MDR）和年度注册更新程序启动。\n- 收入里程碑：B模块获批解锁高级定价层——组合数字孪生系统的价值远高于独立sEMG监测器。\n\nM+23的R7标志着23个月监管时间线的结束和商业增长阶段的开始。",
        },
        status: "not-started",
        owner: "regulatory",
        category: "clearance",
      },
      {
        id: "R8",
        month: 1,
        title: {
          en: "sEMG IP Assignment & US Legal Structure",
          cn: "sEMG知识产权转让和美国法律结构",
        },
        description: {
          en: "Transfer sEMG patents, software copyrights, MyoBus IP to Company B USA. EIT IP deferred to Series A. US-based DHF.",
          cn: "将sEMG专利、软件版权、MyoBus知识产权转让给B公司美国。EIT知识产权推迟至A轮。在美建立DHF。",
        },
        detail: {
          en: "R8 establishes the legal and intellectual property foundation required for a US-based FDA submission. Phase 1 transfers sEMG-related technology assets from the China R&D entity to the US regulatory entity. EIT IP (reconstruction methods, V/Q separation algorithms) remains with Company A and is deferred to Series A negotiation.\n\n- Patent Transfer (sEMG only): All filed and pending patents related to sEMG electrode design and ECG-gating algorithm are assigned to Company B USA (Delaware C-Corp). EIT reconstruction and V/Q separation patents remain with Company A pending Series A IP negotiation.\n- Software Copyrights: Source code, firmware, MyoBus protocol specification, and all software documentation copyrights transfer to Company B USA. This ensures the 510(k) applicant owns the IP it is submitting.\n- MyoBus IP: The proprietary middleware protocol — including its timestamp synchronization, encryption, RBAC, and FHIR output modules — is included in the IP package.\n- US-Based Design History File (DHF): A compliant DHF per 21 CFR 820.30 is established under Company B USA. All design inputs, outputs, reviews, verification, and validation records are maintained under US quality system control.\n- Transfer Agreement: A formal IP assignment agreement with consideration, executed under Delaware law, with representations and warranties regarding IP ownership, freedom to operate, and absence of encumbrances.\n\nR8 at M+1 must be completed before the Pre-Sub meeting (R2) at M+2, as FDA expects the submitting entity to demonstrate IP ownership.",
          cn: "R8建立基于美国的FDA提交所需的法律和知识产权基础。第一阶段将sEMG相关技术资产从中国研发实体转让给美国监管实体。EIT知识产权（重建方法、V/Q分离算法）保留在A公司，推迟至A轮谈判。\n\n- 专利转让（仅sEMG）：所有与sEMG电极设计和ECG门控算法相关的已申请和待审专利转让给Company B USA（特拉华州C-Corp）。EIT重建和V/Q分离专利保留在A公司，待A轮IP谈判。\n- 软件版权：源代码、固件、MyoBus协议规范和所有软件文档版权转让给Company B USA。确保510(k)申请人拥有所提交的知识产权。\n- MyoBus IP：专有中间件协议——包括时间戳同步、加密、RBAC和FHIR输出模块——纳入IP包。\n- 美国设计历史文件（DHF）：在Company B USA下建立符合21 CFR 820.30的DHF。所有设计输入、输出、评审、验证和确认记录在美国质量体系控制下维护。\n- 转让协议：正式的IP转让协议含对价，依特拉华州法律执行，包含关于IP所有权、自由运营和无负担的陈述和保证。\n\nM+1的R8必须在M+2的Pre-Sub会议（R2）前完成，因为FDA期望提交实体证明IP所有权。",
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
          cn: "ISO 13485审核 — 思澜科技",
        },
        description: {
          en: "Readiness assessment vs. 21 CFR 820 QSR and ISO 13485:2016. Gap remediation before FDA registration.",
          cn: "对比21 CFR 820 QSR和ISO 13485:2016进行准备评估。FDA注册前差距修复。",
        },
        detail: {
          en: "R9 ensures the manufacturing quality system at Silan Technology (思澜科技, Chengdu) meets both international and US FDA standards before device production begins:\n\n- ISO 13485:2016 Audit: A third-party registrar (e.g., BSI, TÜV, SGS) performs a Stage 1 (documentation review) and Stage 2 (on-site) audit of Silan's QMS. Key areas: management responsibility, resource management, product realization, measurement/analysis/improvement.\n- 21 CFR 820 QSR Alignment: The US Quality System Regulation has additional requirements beyond ISO 13485 — particularly in design controls (820.30), CAPA (820.90), and complaint handling (820.198). The gap assessment maps Silan's existing processes to both standards.\n- Gap Remediation: Any nonconformities or gaps identified are remediated before FDA registration. Typical gaps for China-based manufacturers: design control documentation format, English-language DHF maintenance, complaint handling timelines, and CAPA effectiveness verification.\n- FDA Establishment Registration: Once the QMS is compliant, we register Silan as a contract manufacturer with FDA (21 CFR 807) and list both the sEMG and EIT devices.\n- Ongoing Compliance: After initial certification, annual surveillance audits maintain ISO 13485 certification. FDA may also conduct unannounced inspections of registered establishments.\n\nR9 at M+2 runs in parallel with R2 (Pre-Sub Meeting). QMS compliance is a prerequisite for any 510(k) filing — FDA reviewers verify establishment registration during submission acceptance.",
          cn: "R9确保思澜科技（成都）的制造质量体系在设备生产开始前同时满足国际和美国FDA标准：\n\n- ISO 13485:2016审核：第三方注册机构（如BSI、TÜV、SGS）对思澜的QMS进行第一阶段（文件审核）和第二阶段（现场）审核。关键领域：管理职责、资源管理、产品实现、测量/分析/改进。\n- 21 CFR 820 QSR对齐：美国质量体系法规有超出ISO 13485的额外要求——特别是设计控制（820.30）、CAPA（820.90）和投诉处理（820.198）。差距评估将思澜现有流程映射到两个标准。\n- 差距修复：识别的任何不符合项或差距在FDA注册前修复。中国制造商的典型差距：设计控制文档格式、英文DHF维护、投诉处理时限和CAPA有效性验证。\n- FDA机构注册：QMS合规后，将思澜注册为FDA合同制造商（21 CFR 807）并列出sEMG和EIT设备。\n- 持续合规：初始认证后，年度监督审核维持ISO 13485认证。FDA也可能对注册机构进行不预先通知的检查。\n\nM+2的R9与R2（Pre-Sub会议）并行运行。QMS合规是任何510(k)提交的先决条件——FDA审查员在提交受理期间验证机构注册。",
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

export const GATES: Gate[] = [
  {
    id: "G1",
    number: 1,
    title: { en: "sEMG Design Verification Complete", cn: "sEMG设计验证完成" },
    month: 3,
    status: "not-started",
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
    decision: null,
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
    month: 6,
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
    month: 9,
    status: "not-started",
    criteria: [
      {
        en: "510(k) clearance received (IKN)",
        cn: "510(k)批准已获得(IKN)",
        met: false,
      },
      {
        en: "Manufacturing scaled — Silan production ready",
        cn: "制造已扩展 — 思澜生产就绪",
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
        en: "Timpel predicate comparison documented (K250464)",
        cn: "Timpel前置器械比较文档完成（K250464）",
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

export const RISKS: Risk[] = [
  {
    id: "RISK-001",
    title: {
      en: "False-negative sEMG signal (missed apnea / low-effort breath)",
      cn: "sEMG信号假阴性（漏检呼吸暂停/低努力呼吸）",
    },
    severity: "high",
    probability: "low",
    riskLevel: "yellow",
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
      en: "IEC 60601-1 Type BF; &lt;10 µA patient leakage; Bluetooth wireless isolation",
      cn: "IEC 60601-1 BF型; &lt;10µA患者泄漏; 蓝牙无线隔离",
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
      en: "Two risk scenarios: (A) Predicate rejection per module — sEMG K082437 uses esophageal catheter vs. our surface electrodes (different transducer technology); EIT K250464 is ventilation-only vs. our V/Q perfusion claim (potentially new intended use). Mitigation: Pre-Sub Q-Meeting at M+0 to get FDA written concurrence before committing test resources; identify 2-3 alternative predicates per module. (B) De Novo for combined platform — FDA may view integrated sEMG+EIT Digital Twin as a novel device with no predicate. Mitigation: describe each module as standalone in 510(k) filings; decouple Digital Twin language from primary submission; prepare De Novo contingency package. De Novo impact: +$130K user fee, +6-12 months timeline, may require prospective clinical study, +$200K-$400K total. Silver lining: De Novo creates the product code — device becomes the predicate for all future competitors, increasing acquisition value.",
      cn: "两个风险场景：(A) 各模块前置器械被拒 — sEMG K082437使用食管导管vs我们的表面电极（不同传感器技术）；EIT K250464仅通气vs我们的V/Q灌注声明（可能构成新预期用途）。缓解：M+0的Pre-Sub Q会议获取FDA书面认可后再投入测试资源；每个模块准备2-3个替代前置器械。(B) 组合平台De Novo — FDA可能认为集成sEMG+EIT数字孪生是无前置器械的新型器械。缓解：510(k)申报中将各模块描述为独立设备；将数字孪生语言与主要提交脱钩；准备De Novo备用方案。De Novo影响：+$130K用户费、+6-12个月时间线、可能需要前瞻性临床研究、总计+$200K-$400K。积极面：De Novo创建产品代码——设备成为所有未来竞争对手的前置器械，增加收购价值。",
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
      en: "Funding deployment risk — $1.8M seed raised, ~40-month runway at current burn",
      cn: "资金部署风险 — $1.8M种子轮已完成，当前消耗率下约40个月跑道",
    },
    severity: "medium",
    probability: "low",
    riskLevel: "yellow",
    controls: {
      en: "$1.8M seed closed; phased milestone-based deployment; sEMG-first strategy enables earlier revenue; investor gate reviews",
      cn: "$1.8M种子轮已完成; 分阶段里程碑部署; sEMG优先策略实现更早收入; 投资者门控评审",
    },
    residual: { en: "Low", cn: "低" },
    mitigationStatus: "complete",
    module: "N/A",
    standard: "Business",
  },
];

// ============================================================
// REGULATORY STANDARDS TRACKER
// ============================================================

export const STANDARDS: Standard[] = [
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
    clauses: [
      {
        id: "STD-01-C1",
        clause: "§4.7",
        title: { en: "ME Equipment classification", cn: "ME设备分类" },
        checked: false,
      },
      {
        id: "STD-01-C2",
        clause: "§8.4",
        title: { en: "Protective earth continuity", cn: "保护接地连续性" },
        checked: true,
      },
      {
        id: "STD-01-C3",
        clause: "§8.7",
        title: { en: "Leakage current measurements", cn: "漏电流测量" },
        checked: false,
        evidenceDoc: "DHF-DV",
      },
      {
        id: "STD-01-C4",
        clause: "§8.8",
        title: { en: "Dielectric strength test", cn: "介电强度测试" },
        checked: false,
      },
      {
        id: "STD-01-C5",
        clause: "§11",
        title: { en: "Temperature limits & controls", cn: "温度限制与控制" },
        checked: true,
      },
      {
        id: "STD-01-C6",
        clause: "§13",
        title: {
          en: "Hazardous situations & fault conditions",
          cn: "危险情况与故障条件",
        },
        checked: false,
      },
      {
        id: "STD-01-C7",
        clause: "§15",
        title: { en: "Construction requirements", cn: "结构要求" },
        checked: false,
      },
    ],
  },
  {
    id: "STD-02",
    code: "IEC 60601-1-2:2014 Ed.4.1",
    title: { en: "Electromagnetic Compatibility (EMC)", cn: "电磁兼容性(EMC)" },
    applies: "Both",
    status: "not-started",
    progress: 0,
    clauses: [
      {
        id: "STD-02-C1",
        clause: "§4",
        title: { en: "General EMC requirements", cn: "通用EMC要求" },
        checked: false,
      },
      {
        id: "STD-02-C2",
        clause: "§7",
        title: { en: "Immunity test configuration", cn: "抗扰度测试配置" },
        checked: false,
        evidenceDoc: "DHF-EMC",
      },
      {
        id: "STD-02-C3",
        clause: "§8",
        title: { en: "Emissions requirements", cn: "发射要求" },
        checked: false,
      },
      {
        id: "STD-02-C4",
        clause: "§9",
        title: { en: "Immunity requirements", cn: "抗扰度要求" },
        checked: false,
      },
      {
        id: "STD-02-C5",
        clause: "§10",
        title: { en: "Rationale for test levels", cn: "测试水平依据" },
        checked: false,
      },
      {
        id: "STD-02-C6",
        clause: "§11",
        title: { en: "Test plan documentation", cn: "测试计划文档" },
        checked: false,
      },
    ],
  },
  {
    id: "STD-03",
    code: "IEC 60601-1-6:2010+AMD1",
    title: { en: "Usability Engineering", cn: "可用性工程" },
    applies: "Both",
    status: "not-started",
    progress: 0,
    clauses: [
      {
        id: "STD-03-C1",
        clause: "§5.1",
        title: { en: "Use specification", cn: "使用规范" },
        checked: false,
      },
      {
        id: "STD-03-C2",
        clause: "§5.3",
        title: { en: "User interface specification", cn: "用户界面规范" },
        checked: false,
      },
      {
        id: "STD-03-C3",
        clause: "§5.7",
        title: { en: "Formative evaluation", cn: "形成性评估" },
        checked: false,
      },
      {
        id: "STD-03-C4",
        clause: "§5.8",
        title: { en: "Summative evaluation", cn: "总结性评估" },
        checked: false,
      },
      {
        id: "STD-03-C5",
        clause: "§5.9",
        title: { en: "Residual use risk assessment", cn: "残余使用风险评估" },
        checked: false,
      },
    ],
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
    clauses: [
      {
        id: "STD-04-C1",
        clause: "§4.1",
        title: { en: "Risk management plan", cn: "风险管理计划" },
        checked: true,
        evidenceDoc: "DHF-RA",
      },
      {
        id: "STD-04-C2",
        clause: "§5.2",
        title: {
          en: "Hazard identification (FTA/FMEA)",
          cn: "危害识别(FTA/FMEA)",
        },
        checked: true,
      },
      {
        id: "STD-04-C3",
        clause: "§5.4",
        title: { en: "Risk estimation", cn: "风险估计" },
        checked: true,
      },
      {
        id: "STD-04-C4",
        clause: "§5.5",
        title: { en: "Risk evaluation", cn: "风险评价" },
        checked: false,
      },
      {
        id: "STD-04-C5",
        clause: "§6",
        title: { en: "Risk control measures", cn: "风险控制措施" },
        checked: false,
        evidenceDoc: "DHF-RA",
      },
      {
        id: "STD-04-C6",
        clause: "§7",
        title: { en: "Residual risk evaluation", cn: "残余风险评价" },
        checked: false,
      },
      {
        id: "STD-04-C7",
        clause: "§8",
        title: { en: "Risk management report", cn: "风险管理报告" },
        checked: false,
      },
    ],
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
    clauses: [
      {
        id: "STD-05-C1",
        clause: "§4",
        title: { en: "General principles for evaluation", cn: "评价通用原则" },
        checked: false,
      },
      {
        id: "STD-05-C2",
        clause: "§5",
        title: { en: "Material characterization", cn: "材料表征" },
        checked: false,
      },
      {
        id: "STD-05-C3",
        clause: "§6",
        title: { en: "Biological evaluation plan", cn: "生物学评价计划" },
        checked: false,
        evidenceDoc: "DHF-BIO",
      },
      {
        id: "STD-05-C4",
        clause: "§7",
        title: { en: "Endpoints selection", cn: "终点选择" },
        checked: false,
      },
      {
        id: "STD-05-C5",
        clause: "§8",
        title: { en: "Risk assessment integration", cn: "风险评估整合" },
        checked: false,
      },
    ],
  },
  {
    id: "STD-06",
    code: "ISO 10993-5",
    title: { en: "Cytotoxicity", cn: "细胞毒性" },
    applies: "sEMG Electrodes",
    status: "not-started",
    progress: 0,
    clauses: [
      {
        id: "STD-06-C1",
        clause: "§5",
        title: { en: "Test methods", cn: "测试方法" },
        checked: false,
      },
      {
        id: "STD-06-C2",
        clause: "§6",
        title: { en: "Extract preparation", cn: "提取物制备" },
        checked: false,
      },
      {
        id: "STD-06-C3",
        clause: "§8",
        title: { en: "Results interpretation", cn: "结果解读" },
        checked: false,
      },
    ],
  },
  {
    id: "STD-07",
    code: "ISO 10993-10",
    title: { en: "Sensitization & Irritation", cn: "致敏和刺激" },
    applies: "sEMG + EIT Belt",
    status: "not-started",
    progress: 0,
    clauses: [
      {
        id: "STD-07-C1",
        clause: "§5",
        title: { en: "Irritation tests", cn: "刺激测试" },
        checked: false,
      },
      {
        id: "STD-07-C2",
        clause: "§6",
        title: { en: "Sensitization tests", cn: "致敏测试" },
        checked: false,
      },
      {
        id: "STD-07-C3",
        clause: "§7",
        title: { en: "Results documentation", cn: "结果文档化" },
        checked: false,
      },
    ],
  },
  {
    id: "STD-08",
    code: "FDA Cybersecurity 2023",
    title: { en: "Medical Device Cybersecurity", cn: "医疗器械网络安全" },
    applies: "Both",
    status: "in-progress",
    progress: 25,
    clauses: [
      {
        id: "STD-08-C1",
        clause: "SBOM",
        title: { en: "Software Bill of Materials", cn: "软件物料清单" },
        checked: true,
      },
      {
        id: "STD-08-C2",
        clause: "TM",
        title: { en: "Threat modeling", cn: "威胁建模" },
        checked: false,
      },
      {
        id: "STD-08-C3",
        clause: "SA",
        title: { en: "Security architecture review", cn: "安全架构审查" },
        checked: false,
      },
      {
        id: "STD-08-C4",
        clause: "VT",
        title: { en: "Vulnerability testing", cn: "漏洞测试" },
        checked: false,
      },
      {
        id: "STD-08-C5",
        clause: "PM",
        title: { en: "Patch/update mechanism", cn: "补丁/更新机制" },
        checked: false,
      },
    ],
  },
  {
    id: "STD-09",
    code: "21 CFR Part 820",
    title: { en: "Quality System Regulation (QSR)", cn: "质量体系法规(QSR)" },
    applies: "Both",
    status: "in-progress",
    progress: 40,
    clauses: [
      {
        id: "STD-09-C1",
        clause: "§820.30",
        title: { en: "Design Controls", cn: "设计控制" },
        checked: true,
        evidenceDoc: "DHF-DP",
      },
      {
        id: "STD-09-C2",
        clause: "§820.40",
        title: { en: "Document Controls", cn: "文件控制" },
        checked: true,
      },
      {
        id: "STD-09-C3",
        clause: "§820.50",
        title: { en: "Purchasing Controls", cn: "采购控制" },
        checked: false,
      },
      {
        id: "STD-09-C4",
        clause: "§820.75",
        title: { en: "Process Validation", cn: "过程确认" },
        checked: false,
      },
      {
        id: "STD-09-C5",
        clause: "§820.90",
        title: { en: "Nonconforming Product", cn: "不合格品" },
        checked: false,
      },
      {
        id: "STD-09-C6",
        clause: "§820.184",
        title: { en: "Device History Record", cn: "设备历史记录" },
        checked: false,
      },
    ],
  },
  {
    id: "STD-10",
    code: "21 CFR Part 11",
    title: { en: "Electronic Records & Signatures", cn: "电子记录和签名" },
    applies: "Software",
    status: "not-started",
    progress: 0,
    clauses: [
      {
        id: "STD-10-C1",
        clause: "§11.10",
        title: { en: "Closed system controls", cn: "封闭系统控制" },
        checked: false,
      },
      {
        id: "STD-10-C2",
        clause: "§11.30",
        title: { en: "Open system controls", cn: "开放系统控制" },
        checked: false,
      },
      {
        id: "STD-10-C3",
        clause: "§11.50",
        title: { en: "Signature manifestation", cn: "签名表现形式" },
        checked: false,
      },
      {
        id: "STD-10-C4",
        clause: "§11.70",
        title: { en: "Signature linking", cn: "签名关联" },
        checked: false,
      },
    ],
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
    clauses: [
      {
        id: "STD-11-C1",
        clause: "§4",
        title: { en: "General requirements", cn: "通用要求" },
        checked: true,
      },
      {
        id: "STD-11-C2",
        clause: "§5.1",
        title: { en: "Software development planning", cn: "软件开发计划" },
        checked: false,
        evidenceDoc: "DHF-SW",
      },
      {
        id: "STD-11-C3",
        clause: "§5.3",
        title: { en: "Software architecture design", cn: "软件架构设计" },
        checked: false,
      },
      {
        id: "STD-11-C4",
        clause: "§5.5",
        title: { en: "Software integration & testing", cn: "软件集成与测试" },
        checked: false,
      },
      {
        id: "STD-11-C5",
        clause: "§6",
        title: { en: "Software maintenance process", cn: "软件维护过程" },
        checked: false,
      },
      {
        id: "STD-11-C6",
        clause: "§7",
        title: { en: "Software risk management", cn: "软件风险管理" },
        checked: false,
      },
    ],
  },
  {
    id: "STD-12",
    code: "ISO 13485:2016",
    title: { en: "QMS for Medical Devices", cn: "医疗器械质量管理体系" },
    applies: "Silan Manufacturing",
    status: "in-progress",
    progress: 60,
    clauses: [
      {
        id: "STD-12-C1",
        clause: "§4.2",
        title: { en: "Documentation requirements", cn: "文件要求" },
        checked: true,
      },
      {
        id: "STD-12-C2",
        clause: "§7.1",
        title: { en: "Planning of product realization", cn: "产品实现策划" },
        checked: true,
      },
      {
        id: "STD-12-C3",
        clause: "§7.3",
        title: { en: "Design and development", cn: "设计和开发" },
        checked: true,
      },
      {
        id: "STD-12-C4",
        clause: "§8.2",
        title: { en: "Monitoring and measurement", cn: "监视和测量" },
        checked: false,
      },
      {
        id: "STD-12-C5",
        clause: "§8.5",
        title: { en: "Improvement", cn: "改进" },
        checked: false,
      },
    ],
  },
];

// ============================================================
// TIMELINE — Business-term translations
// ============================================================

export const TIMELINE_EVENTS: TimelineEvent[] = [
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
    month: 6,
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
    month: 9,
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
// CASH / RUNWAY — Financial tracking
// ============================================================

export const CASH_RUNWAY: CashRunway = {
  cashOnHand: 1800000,
  monthlyBurn: 45000,
  runwayMonths: 40,
  currency: "USD",
  fundingRounds: [
    {
      id: "FR-001",
      label: { en: "Founder Seed", cn: "\u521b\u59cb\u79cd\u5b50\u8f6e" },
      amount: 150000,
      date: "2025-09",
      status: "received",
    },
    {
      id: "FR-002",
      label: { en: "Angel Round", cn: "\u5929\u4f7f\u8f6e" },
      amount: 250000,
      date: "2026-01",
      status: "received",
    },
    {
      id: "FR-003",
      label: {
        en: "Phase 1 Seed Round ($1.8M raised — direct equity)",
        cn: "\u7b2c\u4e00\u9636\u6bb5\u79cd\u5b50\u8f6e\uff08$1.8M\u5df2\u52df\u96c6 — \u76f4\u63a5\u80a1\u6743\uff09",
      },
      amount: 1800000,
      date: "2026-03",
      status: "received",
    },
    {
      id: "FR-004",
      label: {
        en: "Phase 2 Growth (PPT total: $5M)",
        cn: "\u7b2c\u4e8c\u9636\u6bb5\u589e\u957f\u8f6e\uff08PPT\u603b\u989d: $5M\uff09",
      },
      amount: 3000000,
      date: "2027-06",
      status: "pipeline",
    },
  ],
  burnHistory: [
    {
      month: -3,
      burn: 35000,
      note: { en: "Setup & legal", cn: "\u8bbe\u7acb\u4e0e\u6cd5\u5f8b" },
    },
    {
      month: -2,
      burn: 38000,
      note: { en: "Prototype materials", cn: "\u539f\u578b\u6750\u6599" },
    },
    {
      month: -1,
      burn: 42000,
      note: {
        en: "Lab + early testing",
        cn: "\u5b9e\u9a8c\u5ba4+\u65e9\u671f\u6d4b\u8bd5",
      },
    },
    {
      month: 0,
      burn: 45000,
      note: {
        en: "Q-Sub prep + bench testing",
        cn: "Q-Sub\u51c6\u5907+\u53f0\u67b6\u6d4b\u8bd5",
      },
    },
  ],
};

// ============================================================
// INPUT TRACKING — Business & Tech stakeholder inputs
// ============================================================

export const STAKEHOLDER_INPUTS: StakeholderInput[] = [
  {
    id: "INP-001",
    from: "tech",
    date: "2026-03-15",
    gate: "G1",
    content: {
      en: "ECG-gating algorithm showing 97.5% suppression in latest bench test — close to 98% target. Requesting 2 additional weeks for optimization.",
      cn: "ECG门控算法在最新台架测试中显示97.5%抑制 — 接近98%目标。请求额外2周进行优化。",
    },
    status: "pending-review",
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

// ============================================================
// CHANGE REQUEST QUEUE — PMP approval workflow
// ============================================================

export const CHANGE_REQUESTS: ChangeRequest[] = [];

// ============================================================
// AUDIT TRAIL — All actions logged for DHF traceability
// ============================================================

export const AUDIT_LOG: AuditEntry[] = [
  {
    id: "AUD-001",
    timestamp: "2026-03-15T09:30:00Z",
    user: "PMP",
    action: "gate-criteria",
    targetId: "G1",
    field: "criteria[0].met",
    oldValue: "false",
    newValue: "true",
    detail: "Marked ECG-gating criterion as met based on bench test results",
  },
  {
    id: "AUD-002",
    timestamp: "2026-03-14T14:15:00Z",
    user: "PMP",
    action: "milestone-status",
    targetId: "T1",
    field: "status",
    oldValue: "in-progress",
    newValue: "complete",
    detail: "sEMG prototype finalization confirmed complete",
  },
  {
    id: "AUD-003",
    timestamp: "2026-03-12T11:00:00Z",
    user: "PMP",
    action: "risk-field",
    targetId: "RISK-005",
    field: "mitigationStatus",
    oldValue: "not-started",
    newValue: "in-progress",
    detail: "Cybersecurity mitigation work started per FDA 2023 guidance",
  },
];

// ============================================================
// DHF DOCUMENT TRACKER — Design History File
// ============================================================

export const DHF_DOCUMENTS: DHFDocument[] = [
  {
    id: "DHF-001",
    code: "DHF-DP",
    title: { en: "Design Plan", cn: "设计计划" },
    category: "Design Controls",
    owner: "tech",
    status: "approved",
    dueMonth: 0,
    notes: "",
  },
  {
    id: "DHF-002",
    code: "DHF-DI",
    title: { en: "Design Inputs", cn: "设计输入" },
    category: "Design Controls",
    owner: "tech",
    status: "in-review",
    dueMonth: 1,
    notes: "",
  },
  {
    id: "DHF-003",
    code: "DHF-DO",
    title: { en: "Design Outputs", cn: "设计输出" },
    category: "Design Controls",
    owner: "tech",
    status: "draft",
    dueMonth: 3,
    notes: "",
  },
  {
    id: "DHF-004",
    code: "DHF-DV",
    title: { en: "Design Verification Report", cn: "设计验证报告" },
    category: "Verification",
    owner: "tech",
    status: "not-started",
    dueMonth: 4,
    notes: "",
  },
  {
    id: "DHF-005",
    code: "DHF-VAL",
    title: { en: "Design Validation Report", cn: "设计确认报告" },
    category: "Validation",
    owner: "tech",
    status: "not-started",
    dueMonth: 6,
    notes: "",
  },
  {
    id: "DHF-006",
    code: "DHF-RA",
    title: { en: "Risk Analysis (ISO 14971)", cn: "风险分析(ISO 14971)" },
    category: "Risk Management",
    owner: "tech",
    status: "in-review",
    dueMonth: 2,
    notes: "",
  },
  {
    id: "DHF-007",
    code: "DHF-SW",
    title: {
      en: "Software Documentation (IEC 62304)",
      cn: "软件文档(IEC 62304)",
    },
    category: "Software",
    owner: "tech",
    status: "draft",
    dueMonth: 3,
    notes: "",
  },
  {
    id: "DHF-008",
    code: "DHF-BIO",
    title: {
      en: "Biocompatibility Report (ISO 10993)",
      cn: "生物相容性报告(ISO 10993)",
    },
    category: "Biocompatibility",
    owner: "tech",
    status: "not-started",
    dueMonth: 5,
    notes: "",
  },
  {
    id: "DHF-009",
    code: "DHF-EMC",
    title: {
      en: "EMC Test Report (IEC 60601-1-2)",
      cn: "EMC测试报告(IEC 60601-1-2)",
    },
    category: "Testing",
    owner: "tech",
    status: "not-started",
    dueMonth: 4,
    notes: "",
  },
  {
    id: "DHF-010",
    code: "DHF-LBL",
    title: { en: "Labeling & IFU (21 CFR 801)", cn: "标签和IFU(21 CFR 801)" },
    category: "Labeling",
    owner: "regulatory",
    status: "draft",
    dueMonth: 5,
    notes: "",
  },
  {
    id: "DHF-011",
    code: "DHF-CL",
    title: { en: "510(k) Cover Letter", cn: "510(k)附信" },
    category: "Submission",
    owner: "regulatory",
    status: "not-started",
    dueMonth: 6,
    notes: "",
  },
  {
    id: "DHF-012",
    code: "DHF-DD",
    title: { en: "Device Description", cn: "设备描述" },
    category: "Submission",
    owner: "regulatory",
    status: "draft",
    dueMonth: 5,
    notes: "",
  },
];

// ============================================================
// CAPA LOG — Corrective & Preventive Actions
// ============================================================

export const CAPA_LOG: CAPAItem[] = [
  {
    id: "CAPA-001",
    type: "corrective",
    title: {
      en: "ECG Artifact Suppression Below Target",
      cn: "ECG伪影抑制低于目标",
    },
    linkedRiskId: "RISK-002",
    description: {
      en: "ECG-gating algorithm achieved 97.5% but target is 98%. Corrective action: add secondary adaptive filter stage.",
      cn: "ECG门控算法达到97.5%但目标是98%。纠正措施：增加二级自适应滤波阶段。",
    },
    owner: "Tech Lead",
    status: "in-progress",
    openedDate: "2026-03-10",
    dueDate: "2026-04-15",
    closedDate: null,
  },
  {
    id: "CAPA-002",
    type: "preventive",
    title: { en: "V/Q Misinterpretation Safeguard", cn: "V/Q误判预防措施" },
    linkedRiskId: "RISK-004",
    description: {
      en: "Preventive action for V/Q image misinterpretation risk: develop mandatory clinical training module and add on-screen confidence indicator.",
      cn: "V/Q图像误判风险的预防措施：开发强制临床培训模块并添加屏幕置信度指示器。",
    },
    owner: "Clinical Affairs",
    status: "open",
    openedDate: "2026-03-05",
    dueDate: "2026-07-01",
    closedDate: null,
  },
  {
    id: "CAPA-003",
    type: "corrective",
    title: {
      en: "Cybersecurity Penetration Test Findings",
      cn: "网络安全渗透测试发现",
    },
    linkedRiskId: "RISK-005",
    description: {
      en: "Penetration test revealed weak session token handling. Corrective: implement token rotation and session timeout per FDA Cyber 2023.",
      cn: "渗透测试发现会话令牌处理薄弱。纠正：按FDA网络安全2023实施令牌轮换和会话超时。",
    },
    owner: "Security Engineer",
    status: "in-progress",
    openedDate: "2026-02-20",
    dueDate: "2026-04-01",
    closedDate: null,
  },
  {
    id: "CAPA-004",
    type: "preventive",
    title: {
      en: "Predicate & De Novo Contingency Strategy",
      cn: "前置器械与De Novo备用策略",
    },
    linkedRiskId: "RISK-007",
    description: {
      en: "Three-pronged mitigation: (1) Identify 2-3 alternative IKN predicates for sEMG beyond K082437 (surface EMG devices, not catheter-based). (2) Prepare SE argument for EIT V/Q claim as performance enhancement vs. new intended use. (3) Draft De Novo pre-submission package for combined platform if FDA rejects modular 510(k) strategy. Budget reserve: $130K De Novo fee + $200K clinical study contingency.",
      cn: "三管齐下缓解：(1) 为sEMG识别2-3个K082437之外的替代IKN前置器械（表面EMG设备而非导管类）。(2) 准备EIT V/Q声明作为性能增强而非新预期用途的SE论证。(3) 如FDA拒绝模块化510(k)策略，起草组合平台De Novo预提交包。预算储备：$130K De Novo费用 + $200K临床研究备用金。",
    },
    owner: "Regulatory Affairs",
    status: "open",
    openedDate: "2026-03-01",
    dueDate: "2026-05-15",
    closedDate: null,
  },
];

// ============================================================
// ACTION ITEMS / TASK BOARD
// ============================================================

export const ACTION_ITEMS: ActionItem[] = [
  {
    id: "ACT-001",
    title: {
      en: "Complete ECG-gating optimization (98% target)",
      cn: "完成ECG门控优化（98%目标）",
    },
    assignee: "Dr. Dai",
    owner: "tech",
    priority: "high",
    status: "in-progress",
    dueDate: "2026-04-01",
    linkedGate: "G1",
    notes: "",
  },
  {
    id: "ACT-002",
    title: {
      en: "Prepare Pre-Sub meeting presentation",
      cn: "准备预提交会议报告",
    },
    assignee: "Regulatory Lead",
    owner: "regulatory",
    priority: "high",
    status: "in-progress",
    dueDate: "2026-04-10",
    linkedGate: "G2",
    notes: "",
  },
  {
    id: "ACT-003",
    title: {
      en: "Draft risk analysis report (ISO 14971)",
      cn: "起草风险分析报告(ISO 14971)",
    },
    assignee: "Quality Mgr",
    owner: "tech",
    priority: "high",
    status: "in-progress",
    dueDate: "2026-04-15",
    linkedGate: "G1",
    notes: "",
  },
  {
    id: "ACT-004",
    title: {
      en: "Source EIT electrode belt supplier",
      cn: "寻找EIT电极带供应商",
    },
    assignee: "Procurement",
    owner: "tech",
    priority: "medium",
    status: "todo",
    dueDate: "2026-05-01",
    linkedGate: null,
    notes: "",
  },
  {
    id: "ACT-005",
    title: {
      en: "Set up investor monthly reporting template",
      cn: "建立投资者月度报告模板",
    },
    assignee: "PM Analyst",
    owner: "business",
    priority: "medium",
    status: "done",
    dueDate: "2026-03-15",
    linkedGate: null,
    notes: "",
  },
  {
    id: "ACT-006",
    title: {
      en: "Schedule ISO 13485 gap assessment audit",
      cn: "安排ISO 13485差距评估审核",
    },
    assignee: "Quality Mgr",
    owner: "regulatory",
    priority: "high",
    status: "todo",
    dueDate: "2026-04-20",
    linkedGate: "G3",
    notes: "",
  },
  {
    id: "ACT-007",
    title: {
      en: "Order biocompatibility test samples",
      cn: "订购生物相容性测试样品",
    },
    assignee: "Lab Tech",
    owner: "tech",
    priority: "low",
    status: "blocked",
    dueDate: "2026-06-01",
    linkedGate: null,
    notes: "Waiting for supplier qualification",
  },
  {
    id: "ACT-008",
    title: { en: "MyoBus protocol security review", cn: "MyoBus协议安全审查" },
    assignee: "Security Engineer",
    owner: "tech",
    priority: "high",
    status: "in-progress",
    dueDate: "2026-04-05",
    linkedGate: "G1",
    notes: "",
  },
];

// ============================================================
// BUDGET vs ACTUAL — Category-level tracking
// ============================================================

export const BUDGET_CATEGORIES: BudgetCategory[] = [
  {
    id: "BUD-001",
    label: { en: "Prototype & Materials", cn: "原型和材料" },
    planned: 85000,
    actual: 78000,
    notes: "",
  },
  {
    id: "BUD-002",
    label: { en: "Lab Testing & Validation", cn: "实验室测试和验证" },
    planned: 120000,
    actual: 45000,
    notes: "Ramp expected M+3",
  },
  {
    id: "BUD-003",
    label: { en: "Regulatory & Legal", cn: "法规和法律" },
    planned: 95000,
    actual: 62000,
    notes: "",
  },
  {
    id: "BUD-004",
    label: { en: "Personnel", cn: "人员" },
    planned: 250000,
    actual: 135000,
    notes: "Annualized — 6 FTE",
  },
  {
    id: "BUD-005",
    label: { en: "Clinical Studies", cn: "临床研究" },
    planned: 80000,
    actual: 0,
    notes: "Begins at M+3",
  },
  {
    id: "BUD-006",
    label: { en: "Equipment & Software", cn: "设备和软件" },
    planned: 60000,
    actual: 42000,
    notes: "",
  },
  {
    id: "BUD-007",
    label: { en: "Manufacturing Setup", cn: "生产线建设" },
    planned: 100000,
    actual: 15000,
    notes: "Silan facility upgrades",
  },
  {
    id: "BUD-008",
    label: { en: "Travel & Conferences", cn: "差旅和会议" },
    planned: 25000,
    actual: 8000,
    notes: "",
  },
];

// ============================================================
// RESOURCE ALLOCATION — Team capacity view
// ============================================================

export const TEAM_MEMBERS: TeamMember[] = [
  {
    id: "TM-001",
    name: "Project Lead",
    role: {
      en: "Regulatory & Project Management",
      cn: "法规及项目管理",
    },
    allocation: [
      { workstream: "510(k) Prep", pct: 40 },
      { workstream: "Standards Compliance", pct: 20 },
      { workstream: "Project Management", pct: 40 },
    ],
    capacity: 100,
  },
  {
    id: "TM-002",
    name: "Technical Lead",
    role: { en: "Chief Technology Officer", cn: "首席技术官" },
    allocation: [
      { workstream: "Device Development", pct: 50 },
      { workstream: "V&V Testing", pct: 30 },
      { workstream: "Documentation", pct: 20 },
    ],
    capacity: 100,
  },
  {
    id: "TM-003",
    name: "Business Lead",
    role: {
      en: "Business Development",
      cn: "商务拓展",
    },
    allocation: [
      { workstream: "Investor Relations", pct: 40 },
      { workstream: "Business Strategy", pct: 35 },
      { workstream: "Operations", pct: 25 },
    ],
    capacity: 100,
  },
];

// ============================================================
// SUPPLIER / VENDOR TRACKER
// ============================================================

export const SUPPLIERS: Supplier[] = [
  {
    id: "SUP-001",
    name: "TechElec Components",
    component: {
      en: "sEMG Electrode Arrays (Ag/AgCl)",
      cn: "sEMG电极阵列(Ag/AgCl)",
    },
    status: "active",
    leadTimeDays: 21,
    poStatus: "PO-2026-014 Delivered",
    contractMfgMilestone: "M+0",
    notes: "",
  },
  {
    id: "SUP-002",
    name: "FlexBelt Medical",
    component: { en: "EIT 32-Electrode Thoracic Belt", cn: "EIT 32电极胸带" },
    status: "under-review",
    leadTimeDays: 45,
    poStatus: "RFQ Sent",
    contractMfgMilestone: "M+6",
    notes: "Biocompatibility cert required",
  },
  {
    id: "SUP-003",
    name: "NordicSemi",
    component: { en: "Bluetooth SoC (nRF52840)", cn: "蓝牙SoC(nRF52840)" },
    status: "active",
    leadTimeDays: 14,
    poStatus: "PO-2026-009 In Transit",
    contractMfgMilestone: "M+0",
    notes: "",
  },
  {
    id: "SUP-004",
    name: "Texas Instruments",
    component: { en: "24-bit ADC (ADS1298)", cn: "24位ADC(ADS1298)" },
    status: "active",
    leadTimeDays: 28,
    poStatus: "PO-2026-011 Delivered",
    contractMfgMilestone: "M+0",
    notes: "",
  },
  {
    id: "SUP-005",
    name: "Silan Technology",
    component: {
      en: "Contract Manufacturing (Assembly)",
      cn: "合同生产(组装)",
    },
    status: "qualified",
    leadTimeDays: 60,
    poStatus: "Framework Agreement",
    contractMfgMilestone: "M+8",
    notes: "ISO 13485 audit pending",
  },
  {
    id: "SUP-006",
    name: "CeramTec",
    component: { en: "Medical-grade Ceramic Substrates", cn: "医用级陶瓷基板" },
    status: "under-review",
    leadTimeDays: 35,
    poStatus: "Samples Requested",
    contractMfgMilestone: "M+4",
    notes: "Alternative to current PCB substrate",
  },
];

// ============================================================
// US INVESTMENT & INVESTOR RELATIONS
// ============================================================

import type { TargetInvestor, IRActivity } from "./types.ts";

export const TARGET_INVESTORS: TargetInvestor[] = [
  {
    id: "INV-001",
    name: "MedTech Ventures",
    type: "VC",
    stage: "Seed",
    contact: "contacted",
    amount: 500000,
    notes: "Focus on FDA-cleared devices",
  },
  {
    id: "INV-002",
    name: "BioStar Capital",
    type: "Angel Group",
    stage: "Seed",
    contact: "prospect",
    amount: 250000,
    notes: "Pacific NW health-tech syndicate",
  },
  {
    id: "INV-003",
    name: "Cascade Health Fund",
    type: "VC",
    stage: "Series A",
    contact: "prospect",
    amount: 1000000,
    notes: "Portland-based, med-device focus",
  },
  {
    id: "INV-004",
    name: "Oregon Angel Fund",
    type: "Angel Group",
    stage: "Seed",
    contact: "contacted",
    amount: 200000,
    notes: "Local angel network",
  },
  {
    id: "INV-005",
    name: "Digital Health Partners",
    type: "VC",
    stage: "Seed",
    contact: "in-dd",
    amount: 500000,
    notes: "ICU/respiratory portfolio",
  },
];

export const IR_ACTIVITIES: IRActivity[] = [
  {
    id: "IRA-001",
    date: "2026-03-18",
    activity:
      "Initial outreach to MedTech Ventures — sent executive summary & pitch deck",
    status: "done",
  },
  {
    id: "IRA-002",
    date: "2026-03-20",
    activity:
      "Oregon Angel Fund intro meeting — presented 510(k) regulatory strategy",
    status: "done",
  },
  {
    id: "IRA-003",
    date: "2026-03-25",
    activity: "Digital Health Partners — due diligence data room setup",
    status: "in-progress",
  },
  {
    id: "IRA-004",
    date: "2026-04-01",
    activity:
      "Prepare Phase 1 Seed Round investor update ($1.8M raised — deployment plan)",
    status: "todo",
  },
  {
    id: "IRA-005",
    date: "2026-04-10",
    activity: "BioStar Capital — schedule intro call",
    status: "todo",
  },
  {
    id: "IRA-006",
    date: "2026-04-15",
    activity: "Cascade Health Fund — warm introduction via Oregon Bio network",
    status: "todo",
  },
];

// ============================================================
// 510(k) BRIDGE — INVESTOR OUTREACH TIMING
// ============================================================

export interface InvestorBridgeMilestone {
  regulatoryId: string;
  month: number;
  milestone: { en: string; cn: string };
  investorAction: { en: string; cn: string };
  signal: "warm" | "active" | "peak" | "close";
}

export const INVESTOR_BRIDGE: InvestorBridgeMilestone[] = [
  {
    regulatoryId: "R1",
    month: 0,
    milestone: {
      en: "Pre-Sub Filed",
      cn: "预提交已递交",
    },
    investorAction: {
      en: "Build relationships, warm intros — FDA engagement signals credibility",
      cn: "建立关系、暖引荐 — FDA参与证明可信度",
    },
    signal: "warm",
  },
  {
    regulatoryId: "R2",
    month: 2,
    milestone: {
      en: "Pre-Sub Meeting (FDA Feedback)",
      cn: "预提交会议（FDA反馈）",
    },
    investorAction: {
      en: "Active outreach & pitch meetings — FDA feedback de-risks the pathway",
      cn: "主动接触和路演 — FDA反馈降低了监管风险",
    },
    signal: "active",
  },
  {
    regulatoryId: "T3",
    month: 3,
    milestone: {
      en: "Bench & Performance Testing Complete",
      cn: "台架和性能测试完成",
    },
    investorAction: {
      en: "Share performance data with prospects — hard data proves technical viability",
      cn: "与潜在投资者分享性能数据 — 硬数据证明技术可行性",
    },
    signal: "active",
  },
  {
    regulatoryId: "R3",
    month: 6,
    milestone: {
      en: "510(k) Submitted — sEMG Module",
      cn: "510(k)已提交 — sEMG模块",
    },
    investorAction: {
      en: "Push for term sheets — submission is the inflection point",
      cn: "推动条款清单 — 提交是拐点",
    },
    signal: "peak",
  },
  {
    regulatoryId: "R4",
    month: 9,
    milestone: {
      en: "510(k) Clearance — sEMG",
      cn: "510(k)批准 — sEMG",
    },
    investorAction: {
      en: "Close rounds, Series A positioning — cleared device, maximum leverage",
      cn: "完成融资轮次、Series A定位 — 已获批设备、最大谈判筹码",
    },
    signal: "close",
  },
];

// ============================================================
// CAP TABLE MANAGEMENT
// ============================================================

import type { Shareholder, EquityEvent, VestingSchedule } from "./types.ts";

export const SHAREHOLDERS: Shareholder[] = [
  {
    id: "SH-001",
    name: "Lon Dailey",
    role: "Founder / CEO",
    shareClass: "common",
    shares: 1_000_000,
    notes: "CEO, PMP — project management & investor relations",
  },
  {
    id: "SH-002",
    name: "Dr. Dai",
    role: "Founder / CTO",
    shareClass: "common",
    shares: 1_000_000,
    notes: "CTO — device engineering & R&D (China)",
  },
  {
    id: "SH-003",
    name: "Lawrence Liu",
    role: "Founder / COO",
    shareClass: "common",
    shares: 1_000_000,
    notes: "COO — China operations & manufacturing",
  },
  {
    id: "SH-004",
    name: "Option Pool",
    role: "Reserved",
    shareClass: "options",
    shares: 400_000,
    notes: "10% post-money ESOP for future employees & advisors",
  },
  {
    id: "SH-005",
    name: "Angel Investors (Group)",
    role: "Investor",
    shareClass: "safe",
    shares: 150_000,
    notes: "SAFE notes at $5M cap, 20% discount — converts at Series A",
  },
  {
    id: "SH-006",
    name: "Phase 1 Seed (510(k) Bridge)",
    role: "Investor",
    shareClass: "preferred-seed",
    shares: 500_000,
    notes: "$1.8M seed at $3M pre-money — timed to Pre-Sub meeting",
  },
];

export const EQUITY_EVENTS: EquityEvent[] = [
  {
    id: "EQ-001",
    date: "2025-09-01",
    event: "Company Formation",
    shareClass: "common",
    shares: 3_000_000,
    pricePerShare: 0.001,
    totalValue: 3_000,
    status: "issued",
    notes: "3-way founder split — 1M shares each at par value",
  },
  {
    id: "EQ-002",
    date: "2025-11-15",
    event: "SAFE Note — Angel Round",
    shareClass: "safe",
    shares: 0,
    pricePerShare: 0,
    totalValue: 150_000,
    status: "pending",
    notes: "SAFE with $5M cap, 20% discount. Converts at next priced round.",
  },
  {
    id: "EQ-003",
    date: "2026-01-10",
    event: "Option Pool Creation",
    shareClass: "options",
    shares: 400_000,
    pricePerShare: 0,
    totalValue: 0,
    status: "issued",
    notes: "10% post-money ESOP — carved from pre-money per investor request",
  },
  {
    id: "EQ-004",
    date: "2026-03-01",
    event: "Phase 1 Seed Round",
    shareClass: "preferred-seed",
    shares: 500_000,
    pricePerShare: 3.6,
    totalValue: 1_800_000,
    status: "issued",
    notes: "$1.8M at $3M pre-money ($4.8M post). Timed to Pre-Sub milestone.",
  },
  {
    id: "EQ-005",
    date: "2026-09-01",
    event: "SAFE Conversion (projected)",
    shareClass: "preferred-seed",
    shares: 150_000,
    pricePerShare: 1.0,
    totalValue: 150_000,
    status: "pending",
    notes: "Angel SAFEs convert at Series A trigger — estimated 150K shares",
  },
  {
    id: "EQ-006",
    date: "2027-03-01",
    event: "Series A (projected)",
    shareClass: "preferred-a",
    shares: 1_200_000,
    pricePerShare: 8.33,
    totalValue: 10_000_000,
    status: "pending",
    notes: "$10M at $25M pre-money — post-510(k) clearance timing",
  },
];

export const VESTING_SCHEDULES: VestingSchedule[] = [
  {
    id: "VS-001",
    holder: "Lon Dailey",
    shares: 1_000_000,
    startDate: "2025-09-01",
    cliffMonths: 12,
    totalMonths: 48,
    vestedShares: 125_000,
    status: "vesting",
    notes:
      "4-year vest, 1-year cliff. 6 months credited for pre-formation work.",
  },
  {
    id: "VS-002",
    holder: "Dr. Dai",
    shares: 1_000_000,
    startDate: "2025-09-01",
    cliffMonths: 12,
    totalMonths: 48,
    vestedShares: 125_000,
    status: "vesting",
    notes: "4-year vest, 1-year cliff. 6 months credited for IP development.",
  },
  {
    id: "VS-003",
    holder: "Lawrence Liu",
    shares: 1_000_000,
    startDate: "2025-09-01",
    cliffMonths: 12,
    totalMonths: 48,
    vestedShares: 125_000,
    status: "vesting",
    notes: "4-year vest, 1-year cliff. 6 months credited for mfg sourcing.",
  },
];

// ============================================================
// MESSAGE BOARD SECTIONS
// ============================================================

export const QA_SECTIONS: QASection[] = [
  {
    num: 1,
    title: {
      en: "Device Architecture & Design Decisions",
      cn: "设备架构与设计决策",
    },
    context: {
      en: "We need to validate every specification in the Pre-Sub package. Discrepancies between what was filed and what exists will delay FDA review.",
      cn: "我们需要验证Pre-Sub提交包中的每一项规格。已提交内容与实际情况之间的差异将延迟FDA审查。",
    },
    questions: [
      {
        num: 1,
        question: {
          en: "Walk me through the current sEMG module hardware. Is the 4-8 electrode array configuration final, or are you still iterating?",
          cn: "请介绍当前sEMG模块硬件。4-8电极阵列配置是最终版本还是仍在迭代？",
        },
        why: {
          en: "The Pre-Sub states 4-8 electrodes. FDA will ask which it is -- we need a locked design.",
          cn: "Pre-Sub声明了4-8个电极。FDA会问具体是几个——我们需要锁定设计。",
        },
        followUps: [
          {
            en: "What drove the electrode count choice?",
            cn: "电极数量选择的驱动因素是什么？",
          },
          {
            en: "Are there any alternative array geometries under consideration?",
            cn: "是否有其他替代阵列几何形状在考虑中？",
          },
          {
            en: "What material are the electrodes? Ag/AgCl confirmed?",
            cn: "电极材料是什么？确认是Ag/AgCl吗？",
          },
        ],
      },
      {
        num: 2,
        question: {
          en: "The ADC is spec'd as 24-bit (ADS1298) at 2000 Hz sampling. Is this the production design or a bench prototype?",
          cn: "ADC规格为24位（ADS1298），2000Hz采样。这是量产设计还是台式原型？",
        },
        why: {
          en: "TI ADS1298 is in our supplier tracker as delivered. Need to confirm it's the final BOM part.",
          cn: "TI ADS1298在我们的供应商跟踪器中显示已交付。需确认这是最终BOM零件。",
        },
        followUps: [
          {
            en: "Any plans to change the ADC? If so, it triggers a new EMC cycle.",
            cn: "是否有更换ADC的计划？如果有，将触发新的EMC测试周期。",
          },
          {
            en: "What is the actual measured SNR at 2000 Hz?",
            cn: "2000Hz下实际测量的SNR是多少？",
          },
          {
            en: "Is the sampling rate configurable, or fixed at 2000 Hz?",
            cn: "采样率可配置还是固定在2000Hz？",
          },
        ],
      },
      {
        num: 3,
        question: {
          en: "Describe the Bluetooth wireless isolation. Which BT standard -- BLE 5.x? What is the measured patient leakage current?",
          cn: "描述蓝牙无线隔离。哪种BT标准——BLE 5.x？测量的患者漏电流是多少？",
        },
        why: {
          en: "IEC 60601-1 Type BF requires <10 uA patient leakage. This is a pass/fail gate.",
          cn: "IEC 60601-1 BF型要求患者漏电流<10 uA。这是通过/失败门槛。",
        },
        followUps: [
          {
            en: "NordicSemi nRF52840 is in our BOM -- confirmed?",
            cn: "NordicSemi nRF52840在我们的BOM中——确认了吗？",
          },
          {
            en: "What is the maximum transmission range needed in an ICU setting?",
            cn: "ICU环境中需要的最大传输距离是多少？",
          },
          {
            en: "How is the device paired to the bedside monitor?",
            cn: "设备如何与床旁监护仪配对？",
          },
        ],
      },
      {
        num: 4,
        question: {
          en: "Explain the ECG-gating algorithm. You claim >98% artifact suppression -- current bench tests show 97.5%. What's the path to 98%?",
          cn: "请解释ECG门控算法。你声称伪影抑制率>98%——当前台式测试显示97.5%。达到98%的路径是什么？",
        },
        why: {
          en: "CAPA-001 is open for this. G1 criteria requires 98%. We need a realistic timeline.",
          cn: "CAPA-001对此尚未关闭。G1标准要求98%。我们需要一个切实可行的时间线。",
        },
        followUps: [
          {
            en: "Is the algorithm proprietary or based on published literature?",
            cn: "算法是专有的还是基于已发表文献？",
          },
          {
            en: "What is the computational load? Can it run on the nRF52840?",
            cn: "计算负载是多少？能在nRF52840上运行吗？",
          },
          {
            en: "How was the 98% target derived -- clinical requirement or engineering margin?",
            cn: "98%的目标是怎么得出的——临床需求还是工程余量？",
          },
          {
            en: "What happens if 98% is not achievable? Is 97.5% clinically acceptable?",
            cn: "如果98%无法达到会怎样？97.5%在临床上可接受吗？",
          },
        ],
      },
      {
        num: 5,
        question: {
          en: "Describe the EIT Belt -- 32-electrode, 50 kHz AC injection, 50 Hz frame rate. What stage is the physical prototype at?",
          cn: "描述EIT腰带——32电极、50kHz交流注入、50Hz帧率。物理原型处于什么阶段？",
        },
        why: {
          en: "T5 (EIT Prototype) is NOT STARTED, targeted M+8. Need to understand actual readiness.",
          cn: "T5（EIT原型）尚未开始，目标M+8。需要了解实际准备情况。",
        },
        followUps: [
          {
            en: "Do we have a working 32-electrode prototype or only simulation?",
            cn: "我们有可工作的32电极原型还是只有仿真？",
          },
          {
            en: "Who manufactured the prototype belt? FlexBelt Medical?",
            cn: "谁制造了原型腰带？FlexBelt Medical？",
          },
          {
            en: "What is the spatial resolution of the 32x32 pixel reconstruction?",
            cn: "32x32像素重建的空间分辨率是多少？",
          },
          {
            en: "Is 50 Hz frame rate sufficient for real-time ventilator feedback?",
            cn: "50Hz帧率是否足以提供实时呼吸机反馈？",
          },
        ],
      },
      {
        num: 6,
        question: {
          en: "MyoBus protocol -- explain the <1ms timestamp alignment. How is this achieved across two wireless modules?",
          cn: "MyoBus协议——解释<1ms时间戳对齐。这是如何在两个无线模块之间实现的？",
        },
        why: {
          en: "RISK-006 (sync failure) is rated GREEN -- need to verify that's justified.",
          cn: "RISK-006（同步失败）评级为绿色——需验证是否合理。",
        },
        followUps: [
          {
            en: "Is MyoBus a hardware clock sync or software post-processing alignment?",
            cn: "MyoBus是硬件时钟同步还是软件后处理对齐？",
          },
          {
            en: "What happens during a sync loss event? Describe the fallback mode.",
            cn: "同步丢失时会发生什么？描述回退模式。",
          },
          {
            en: "Has the <1ms claim been verified in a multi-patient ICU environment?",
            cn: "<1ms的声明是否在多患者ICU环境中得到验证？",
          },
        ],
      },
    ],
  },
  {
    num: 2,
    title: {
      en: "Performance Claims & Validation Evidence",
      cn: "性能声明与验证证据",
    },
    context: {
      en: "Every performance number in the 510(k) must be backed by test data. FDA will issue an Additional Information (AI) request if claims are unsupported.",
      cn: "510(k)中的每个性能数据都必须有测试数据支持。如果声明无依据，FDA将发出补充信息请求。",
    },
    questions: [
      {
        num: 7,
        question: {
          en: "NRD detection sensitivity is claimed at >=92%. What test protocol was used, and what is the current measured value?",
          cn: "NRD检测灵敏度声称>=92%。使用了什么测试协议？当前测量值是多少？",
        },
        why: {
          en: "T4 targets are sensitivity >=92%, specificity >=88%, latency <50ms. All three are 510(k) submission claims.",
          cn: "T4目标为灵敏度>=92%、特异性>=88%、延迟<50ms。三者均为510(k)提交声明。",
        },
        followUps: [
          {
            en: "Was this tested against esophageal EMG as reference?",
            cn: "是否以食道EMG作为参考进行测试？",
          },
          {
            en: "What is the sample size so far? The Pre-Sub mentions n>=30.",
            cn: "目前样本量是多少？Pre-Sub提到n>=30。",
          },
          {
            en: "How does performance degrade with obese patients or high BMI?",
            cn: "肥胖患者或高BMI时性能如何下降？",
          },
        ],
      },
      {
        num: 8,
        question: {
          en: "V/Q separation algorithm -- you claim >85% accuracy vs. DCE-CT. Where does this number come from?",
          cn: "V/Q分离算法——你说与DCE-CT相比准确度>85%。这个数字从何而来？",
        },
        why: {
          en: "This is an EIT module claim (T6, M+12). If it's unvalidated, the EIT 510(k) timeline may need adjustment.",
          cn: "这是EIT模块声明（T6, M+12）。如果未验证，EIT 510(k)时间线可能需要调整。",
        },
        followUps: [
          {
            en: "Is there published literature supporting this accuracy threshold?",
            cn: "是否有已发表文献支持该准确度阈值？",
          },
          {
            en: "How many comparison studies have been done?",
            cn: "已进行了多少比较研究？",
          },
          {
            en: "Is there a predicate device that uses the same V/Q imaging approach?",
            cn: "是否有使用相同V/Q成像方法的对照设备？",
          },
        ],
      },
      {
        num: 9,
        question: {
          en: "Signal latency claim: <50ms end-to-end. Is this sensor-to-screen or sensor-to-algorithm-output?",
          cn: "信号延迟声明：端到端<50ms。这是传感器到屏幕还是传感器到算法输出？",
        },
        why: {
          en: "Clinicians making ventilator adjustments need real-time data. The definition of 'latency' matters for the IFU.",
          cn: "进行呼吸机调整的临床医生需要实时数据。'延迟'的定义对IFU很重要。",
        },
        followUps: [
          {
            en: "What are the individual latency contributions (acquisition, processing, display)?",
            cn: "各环节延迟贡献是多少（采集、处理、显示）？",
          },
          {
            en: "Is this measured or theoretical?",
            cn: "这是测量值还是理论值？",
          },
          {
            en: "Does BLE transmission add variable latency?",
            cn: "BLE传输是否增加可变延迟？",
          },
        ],
      },
      {
        num: 10,
        question: {
          en: "What clinical evidence exists today? Any IRB-approved studies, published abstracts, or case reports?",
          cn: "目前有哪些临床证据？有IRB批准的研究、已发表摘要或病例报告吗？",
        },
        why: {
          en: "510(k) Section 9 requires clinical evidence. If we have none, we need a clinical evidence strategy before M+3.",
          cn: "510(k)第9节要求临床证据。如果我们没有，需要在M+3之前制定临床证据策略。",
        },
        followUps: [
          {
            en: "Are there plans for a clinical validation study? If so, at which hospital?",
            cn: "是否有临床验证研究计划？如果有，在哪家医院？",
          },
          {
            en: "Has the device been used on human subjects (even informally)?",
            cn: "设备是否曾在人体受试者上使用过（即使非正式）？",
          },
          {
            en: "Are there any conference presentations or posters?",
            cn: "是否有会议报告或海报？",
          },
        ],
      },
    ],
  },
  {
    num: 3,
    title: { en: "Intellectual Property & Ownership", cn: "知识产权与所有权" },
    context: {
      en: "R8 (sEMG IP Assignment & US Legal Structure) is IN PROGRESS. Phase 1 covers sEMG IP only; EIT IP deferred to Series A. The 510(k) applicant must be Company B USA.",
      cn: "R8（sEMG知识产权转让和美国法律结构）正在进行中。第一阶段仅涉及sEMG知识产权；EIT知识产权推迟至A轮。510(k)申请人必须是Company B USA。",
    },
    questions: [
      {
        num: 11,
        question: {
          en: "List every patent, patent application, and provisional filing related to this device. Include application numbers and jurisdictions.",
          cn: "列出与该设备相关的每项专利、专利申请和临时申请。包括申请号和管辖区。",
        },
        why: {
          en: "We need a complete IP inventory for the DHF and investor due diligence.",
          cn: "我们需要完整的IP清单用于DHF和投资者尽职调查。",
        },
        followUps: [
          {
            en: "Who is the named inventor on each filing?",
            cn: "每项申请中的具名发明人是谁？",
          },
          {
            en: "Are any patents jointly owned with a university or employer?",
            cn: "是否有专利与大学或雇主共同拥有？",
          },
          {
            en: "Are there any freedom-to-operate concerns?",
            cn: "是否有自由实施的顾虑？",
          },
        ],
      },
      {
        num: 12,
        question: {
          en: "Is there any third-party IP embedded in the device -- licensed algorithms, open-source code, or university technology?",
          cn: "设备中是否嵌入了第三方IP——许可算法、开源代码或大学技术？",
        },
        why: {
          en: "Software containing GPL or university-licensed code can create ownership disputes and FDA submission complications.",
          cn: "包含GPL或大学许可代码的软件可能产生所有权纠纷和FDA提交并发症。",
        },
        followUps: [
          {
            en: "List all software libraries used, with license types.",
            cn: "列出所有使用的软件库及其许可类型。",
          },
          {
            en: "Is the ECG-gating algorithm entirely original work?",
            cn: "ECG门控算法是否完全是原创作品？",
          },
          {
            en: "Any research agreements, CRADA, or SBIR grants involved?",
            cn: "是否涉及任何研究协议、CRADA或SBIR资助？",
          },
        ],
      },
      {
        num: 13,
        question: {
          en: "What is the status of the IP transfer to Company B USA? Has a formal assignment agreement been executed?",
          cn: "IP转让给Company B USA的状态如何？是否已签署正式的转让协议？",
        },
        why: {
          en: "R8 milestone depends on this. Cannot file 510(k) until Company B USA holds or has irrevocable license to all IP.",
          cn: "R8里程碑取决于此。在Company B USA持有或获得所有IP的不可撤销许可之前，不能提交510(k)。",
        },
        followUps: [
          {
            en: "Is the inventor willing to assign all IP, or does he want to retain any rights?",
            cn: "发明人是否愿意转让所有IP，还是想保留部分权利？",
          },
          {
            en: "Is Silan Technology a co-owner of any IP?",
            cn: "思澜科技是否共同拥有任何IP？",
          },
          {
            en: "Are there any prior encumbrances (liens, pledges, prior licenses)?",
            cn: "是否有任何在先负担（留置权、质押、在先许可）？",
          },
        ],
      },
    ],
  },
  {
    num: 4,
    title: { en: "Regulatory & Standards Readiness", cn: "法规与标准准备情况" },
    context: {
      en: "12 regulatory standards are being tracked. Several are at 0% progress. The inventor's cooperation on test readiness is critical.",
      cn: "正在跟踪12项法规标准。多项进度为0%。发明人在测试准备方面的配合至关重要。",
    },
    questions: [
      {
        num: 14,
        question: {
          en: "Has the device undergone ANY formal IEC 60601-1 electrical safety testing? Even preliminary?",
          cn: "设备是否进行过任何正式的IEC 60601-1电气安全测试？即使是初步测试？",
        },
        why: {
          en: "STD-01 is at 30% progress. Need to know what's been done.",
          cn: "STD-01进度为30%。需要了解已完成的内容。",
        },
        followUps: [
          {
            en: "Which test lab was used? Is it NVLAP-accredited?",
            cn: "使用了哪个测试实验室？是否有NVLAP认证？",
          },
          {
            en: "Do we have any test reports we can share with FDA at Pre-Sub?",
            cn: "我们是否有可以在Pre-Sub时与FDA共享的测试报告？",
          },
        ],
      },
      {
        num: 15,
        question: {
          en: "EMC testing (IEC 60601-1-2) -- any testing done? ICU environments have extreme electromagnetic interference.",
          cn: "EMC测试（IEC 60601-1-2）——做过任何测试吗？ICU环境有极强的电磁干扰。",
        },
        why: {
          en: "STD-02 is at 0%. EMC is a common 510(k) failure point. G1 requires EMC compliance verified.",
          cn: "STD-02进度为0%。EMC是510(k)常见失败点。G1要求验证EMC合规性。",
        },
        followUps: [
          {
            en: "Has the device been tested in an actual ICU environment?",
            cn: "设备是否在实际ICU环境中进行过测试？",
          },
          {
            en: "Any known interference issues (ventilators, infusion pumps, defibrillators)?",
            cn: "是否有已知的干扰问题（呼吸机、输液泵、除颤器）？",
          },
        ],
      },
      {
        num: 16,
        question: {
          en: "Software classification -- do you agree this is IEC 62304 Class B? Or could FDA classify it as Class C given it influences ventilator decisions?",
          cn: "软件分类——你同意这是IEC 62304 B级吗？还是FDA会因其影响呼吸机决策而将其归为C级？",
        },
        why: {
          en: "G2 criteria includes software classification confirmation from FDA. Class C would significantly increase documentation requirements.",
          cn: "G2标准包括FDA确认软件分类。C级将大幅增加文档要求。",
        },
        followUps: [
          {
            en: "Does the software make autonomous decisions, or only display data?",
            cn: "软件是自主决策还是仅显示数据？",
          },
          {
            en: "Is there a Software Development Plan per IEC 62304?",
            cn: "是否有符合IEC 62304的软件开发计划？",
          },
          {
            en: "What programming languages and RTOS are used?",
            cn: "使用了什么编程语言和RTOS？",
          },
        ],
      },
      {
        num: 17,
        question: {
          en: "Cybersecurity -- the Pre-Sub mentions AES-256 and RBAC. Is this implemented or planned?",
          cn: "网络安全——Pre-Sub提到了AES-256和RBAC。这是已实施还是计划中？",
        },
        why: {
          en: "RISK-005 (cybersecurity) is YELLOW. CAPA-003 found weak session tokens. FDA Cybersecurity 2023 guidance is mandatory.",
          cn: "RISK-005（网络安全）为黄色。CAPA-003发现弱会话令牌。FDA 2023年网络安全指南是必须的。",
        },
        followUps: [
          {
            en: "Has a threat model been created (per FDA guidance)?",
            cn: "是否创建了威胁模型（按照FDA指南）？",
          },
          {
            en: "SBOM (Software Bill of Materials) -- do we have one?",
            cn: "SBOM（软件物料清单）——我们有吗？",
          },
          {
            en: "How are firmware updates delivered? Over-the-air?",
            cn: "固件更新如何交付？空中升级？",
          },
          {
            en: "What vulnerability disclosure process exists?",
            cn: "存在什么漏洞披露流程？",
          },
        ],
      },
    ],
  },
  {
    num: 5,
    title: { en: "Manufacturing & Supply Chain", cn: "制造与供应链" },
    context: {
      en: "Silan Technology (Chengdu) is the contract manufacturer. ISO 13485 audit is pending (R9, M+2). 6 suppliers are tracked.",
      cn: "思澜科技（成都）是合同制造商。ISO 13485审核待定（R9, M+2）。正在跟踪6家供应商。",
    },
    questions: [
      {
        num: 18,
        question: {
          en: "Describe Silan's current manufacturing capability for this device. Assembly line? Clean room? Soldering? Final test?",
          cn: "描述思澜目前的设备制造能力。装配线？洁净室？焊接？最终测试？",
        },
        why: {
          en: "G4 criteria requires 'Manufacturing scaled -- Silan production ready.' We need to understand the starting point.",
          cn: "G4标准要求'制造扩展——思澜生产就绪。'我们需要了解起点。",
        },
        followUps: [
          {
            en: "What is the current production capacity (units/month)?",
            cn: "目前的产能是多少（每月单位数）？",
          },
          {
            en: "What capital equipment upgrades are needed?",
            cn: "需要哪些资本设备升级？",
          },
          {
            en: "Is there a Device Master Record (DMR)?",
            cn: "是否有设备主记录（DMR）？",
          },
        ],
      },
      {
        num: 19,
        question: {
          en: "Are there any single-source components that have no alternate supplier?",
          cn: "是否有无替代供应商的单一来源组件？",
        },
        why: {
          en: "Supply chain risk. If NordicSemi or TI has allocation issues, we could miss milestones.",
          cn: "供应链风险。如果NordicSemi或TI有分配问题，我们可能会错过里程碑。",
        },
        followUps: [
          {
            en: "Can we qualify a second source for the ADC?",
            cn: "我们能否为ADC认证第二供应源？",
          },
          {
            en: "ADS1298 is a mature part -- any EOL concerns?",
            cn: "ADS1298是成熟部件——有任何停产顾虑吗？",
          },
          {
            en: "What is the longest lead-time component in the BOM?",
            cn: "BOM中交货时间最长的组件是什么？",
          },
        ],
      },
      {
        num: 20,
        question: {
          en: "Biocompatibility -- have ANY ISO 10993 tests been done on the electrode materials or the EIT belt materials?",
          cn: "生物相容性——电极材料或EIT腰带材料是否进行过任何ISO 10993测试？",
        },
        why: {
          en: "Three biocompatibility standards (STD-05/06/07) are at 0%. ACT-007 (order biocompat samples) is BLOCKED waiting on supplier.",
          cn: "三项生物相容性标准（STD-05/06/07）进度为0%。ACT-007（订购生物相容性样品）因等待供应商而被阻塞。",
        },
        followUps: [
          {
            en: "Material Safety Data Sheets (MSDS) for all patient-contact materials?",
            cn: "所有患者接触材料的材料安全数据表（MSDS）？",
          },
          {
            en: "Any history of skin reactions in prototype testing?",
            cn: "原型测试中是否有皮肤反应的历史？",
          },
          {
            en: "Who will perform ISO 10993 testing -- in-house or contract lab?",
            cn: "谁将进行ISO 10993测试——内部还是合同实验室？",
          },
        ],
      },
    ],
  },
  {
    num: 6,
    title: {
      en: "Predicate Devices & Competitive Landscape",
      cn: "对照设备与竞争格局",
    },
    context: {
      en: "The 510(k) pathway depends on demonstrating substantial equivalence. RISK-007 (510(k) rejection -- predicate not accepted) is rated RED.",
      cn: "510(k)路径取决于证明实质等价。RISK-007（510(k)拒绝——对照设备未被接受）评级为红色。",
    },
    questions: [
      {
        num: 21,
        question: {
          en: "What is the specific predicate device for the sEMG module? Provide the 510(k) K-number.",
          cn: "sEMG模块的具体对照设备是什么？提供510(k) K编号。",
        },
        why: {
          en: "Product code IKN. The Pre-Sub Q-meeting will specifically ask about predicate selection. We need K-numbers before M+2.",
          cn: "产品代码IKN。Pre-Sub Q会议将专门询问对照设备选择。我们需要在M+2之前获取K编号。",
        },
        followUps: [
          {
            en: "Has this predicate been verified as still active (not recalled)?",
            cn: "是否已验证该对照设备仍然有效（未召回）？",
          },
          {
            en: "What are the key differences between our device and the predicate?",
            cn: "我们的设备与对照设备有哪些关键差异？",
          },
          {
            en: "Do we have the predicate's Summary of Safety and Effectiveness (SSED)?",
            cn: "我们是否有对照设备的安全有效性摘要（SSED）？",
          },
        ],
      },
      {
        num: 22,
        question: {
          en: "For the EIT module -- the Pre-Sub mentions Timpel Enlight as predicate. Do you have the Timpel K-number? Is it cleared for V/Q imaging?",
          cn: "对于EIT模块——Pre-Sub提到Timpel Enlight作为对照设备。你有Timpel的K编号吗？它是否获批用于V/Q成像？",
        },
        why: {
          en: "CAPA-004 (Predicate Backup Strategy) is OPEN. If Timpel is not a valid predicate, we may need De Novo (+60 days).",
          cn: "CAPA-004（对照设备备选策略）未关闭。如果Timpel不是有效对照设备，我们可能需要De Novo（+60天）。",
        },
        followUps: [
          {
            en: "Are there any other EIT-based cleared devices in the FDA database?",
            cn: "FDA数据库中是否有其他基于EIT的已批准设备？",
          },
          {
            en: "If no valid predicate exists, are you prepared for a De Novo pathway?",
            cn: "如果没有有效的对照设备，你是否准备好走De Novo路径？",
          },
          {
            en: "What is Timpel's intended use statement vs. ours?",
            cn: "Timpel的预期用途声明与我们的相比如何？",
          },
        ],
      },
      {
        num: 23,
        question: {
          en: "Who are the direct competitors in bedside respiratory monitoring? What is our differentiation?",
          cn: "床旁呼吸监护的直接竞争对手是谁？我们的差异化是什么？",
        },
        why: {
          en: "Investor pitch and 510(k) Section 4 (Device Description) both need a clear competitive positioning.",
          cn: "投资者推介和510(k)第4节（设备描述）都需要清晰的竞争定位。",
        },
        followUps: [
          {
            en: "Draeger, Getinge, Magnamed -- any of these doing combined sEMG+EIT?",
            cn: "Draeger、Getinge、Magnamed——其中任何一家在做联合sEMG+EIT吗？",
          },
          {
            en: "Is there a published market size for ICU respiratory monitoring?",
            cn: "ICU呼吸监护是否有已发布的市场规模？",
          },
          {
            en: "What is our target price point vs. competitors?",
            cn: "我们的目标价格点与竞争对手相比如何？",
          },
        ],
      },
    ],
  },
  {
    num: 7,
    title: { en: "Risk & Clinical Safety Concerns", cn: "风险与临床安全关切" },
    context: {
      en: "8 risks tracked in ISO 14971 register. 3 RED risks. The inventor's input is needed to assess residual risk accuracy.",
      cn: "ISO 14971登记册中跟踪了8项风险。3项红色风险。需要发明人的输入来评估剩余风险准确性。",
    },
    questions: [
      {
        num: 24,
        question: {
          en: "RISK-004 is rated RED: V/Q perfusion image misinterpretation leading to incorrect ventilator adjustment. How do you prevent this?",
          cn: "RISK-004评级为红色：V/Q灌注图像误解导致不正确的呼吸机调整。你如何防止这种情况？",
        },
        why: {
          en: "This is the highest clinical risk. 'Investigational adjunct' labeling reduces but does not eliminate risk.",
          cn: "这是最高的临床风险。'研究性辅助设备'标签降低但不消除风险。",
        },
        followUps: [
          {
            en: "Should perfusion imaging be excluded from the initial 510(k)?",
            cn: "灌注成像是否应从初始510(k)中排除？",
          },
          {
            en: "What training do clinicians need to interpret V/Q images correctly?",
            cn: "临床医生需要什么培训才能正确解读V/Q图像？",
          },
          {
            en: "Is there an on-screen confidence score or quality indicator?",
            cn: "是否有屏幕上的置信度评分或质量指标？",
          },
        ],
      },
      {
        num: 25,
        question: {
          en: "RISK-007 is RED: 510(k) rejection. What is your honest assessment of the probability that FDA accepts our predicate strategy?",
          cn: "RISK-007为红色：510(k)拒绝。你对FDA接受我们对照设备策略的概率的真实评估是什么？",
        },
        why: {
          en: "A De Novo adds ~60 days and $50-100K. If this is likely, we need to budget and plan now, not at M+6.",
          cn: "De Novo增加约60天和5-10万美元。如果可能性大，我们需要现在预算和计划，而不是在M+6。",
        },
        followUps: [
          {
            en: "Have you spoken with any regulatory consultants about predicate viability?",
            cn: "你是否与法规顾问讨论过对照设备的可行性？",
          },
          {
            en: "Is there a published FDA guidance document for our device type?",
            cn: "是否有针对我们设备类型的已发布FDA指南文件？",
          },
        ],
      },
      {
        num: 26,
        question: {
          en: "RISK-008 is YELLOW: $1.8M seed raised with ~40-month runway. What is the minimum viable hardware cost to reach 510(k) submission?",
          cn: "RISK-008为黄色：$1.8M种子轮已完成，约40个月跑道。达到510(k)提交的最低可行硬件成本是多少？",
        },
        why: {
          en: "$1.8M seed raised, $45K/mo burn, ~40-month runway. Submission is at M+6. We need to know if the budget is realistic.",
          cn: "$1.8M种子轮已完成，月消耗4.5万美元，约40个月跑道。提交在M+6。我们需要知道预算是否现实。",
        },
        followUps: [
          {
            en: "What are the largest unfunded cost items between now and M+6?",
            cn: "从现在到M+6之间最大的未资助成本项目是什么？",
          },
          {
            en: "Can any testing be deferred past sEMG submission?",
            cn: "是否有任何测试可以推迟到sEMG提交之后？",
          },
          {
            en: "What is the minimum team size to keep the project on track?",
            cn: "保持项目正常运行的最少团队规模是多少？",
          },
        ],
      },
    ],
  },
  {
    num: 8,
    title: {
      en: "Inventor Relationship & Ongoing Role",
      cn: "发明人关系与后续角色",
    },
    context: {
      en: "Clarifying the inventor's role going forward is essential for both the IP structure and the team resource plan.",
      cn: "明确发明人未来的角色对IP结构和团队资源计划至关重要。",
    },
    questions: [
      {
        num: 27,
        question: {
          en: "How is the $45K/month burn rate composed? Walk me through the major cost buckets that make up monthly operating expenses.",
          cn: "每月4.5万美元的消耗率是如何构成的？请介绍构成月度运营费用的主要成本类别。",
        },
        why: {
          en: "The burn rate drives runway calculations and investor reporting. Currently it is a static number -- we need the actual breakdown to forecast accurately.",
          cn: "消耗率驱动跑道计算和投资者报告。目前是静态数字——我们需要实际分解以准确预测。",
        },
        followUps: [
          {
            en: "Which costs are fixed (salaries, rent) vs. variable (materials, testing)?",
            cn: "哪些费用是固定的（工资、租金）与可变的（材料、测试）？",
          },
          {
            en: "How will the burn rate change at each project phase (M+3, M+6, M+9)?",
            cn: "每个项目阶段（M+3、M+6、M+9）消耗率将如何变化？",
          },
          {
            en: "Is Silan charging a monthly retainer, or cost-plus per milestone?",
            cn: "思澜是按月收费还是按里程碑成本加成？",
          },
          {
            en: "Are there any upcoming step-function cost increases?",
            cn: "是否有即将到来的阶跃成本增加？",
          },
          {
            en: "What is the minimum monthly spend to keep the project alive if funding is delayed?",
            cn: "如果资金延迟，维持项目存续的最低月支出是多少？",
          },
        ],
      },
      {
        num: 28,
        question: {
          en: "What is your expected role after IP transfer to Company B USA? CTO? Consultant? Advisory board?",
          cn: "IP转让给Company B USA后你期望的角色是什么？CTO？顾问？顾问委员会？",
        },
        why: {
          en: "Resource allocation planning. Dr. Dai is currently at 100% allocation across 3 workstreams.",
          cn: "资源配置规划。戴博士目前在3个工作流中分配了100%。",
        },
        followUps: [
          {
            en: "Are you willing to be the named technical contact for FDA communications?",
            cn: "你是否愿意担任FDA通信的指定技术联系人？",
          },
          {
            en: "What is your availability commitment (hours/week)?",
            cn: "你的可用性承诺是多少（小时/周）？",
          },
          {
            en: "Employment agreement or consulting agreement?",
            cn: "雇佣协议还是咨询协议？",
          },
        ],
      },
      {
        num: 29,
        question: {
          en: "Are there any co-inventors, research collaborators, or students who contributed to the technology?",
          cn: "是否有共同发明人、研究合作者或学生对该技术做出了贡献？",
        },
        why: {
          en: "Unnamed contributors can surface as IP claimants later.",
          cn: "未提及的贡献者可能会在后续成为IP索赔人。",
        },
        followUps: [
          {
            en: "Any university affiliations that might claim IP rights?",
            cn: "是否有可能主张IP权利的大学关联？",
          },
          {
            en: "Were any government grants (NIH, NSF, DARPA) used in development?",
            cn: "开发中是否使用了政府资助（NIH、NSF、DARPA）？",
          },
        ],
      },
      {
        num: 30,
        question: {
          en: "Is there anything about this device -- technical limitations, failed experiments, known issues -- that I should know about but hasn't been disclosed yet?",
          cn: "关于该设备——技术限制、失败的实验、已知问题——有什么我应该知道但尚未披露的吗？",
        },
        why: {
          en: "The PMP needs a complete picture. Undisclosed issues found during FDA review are far more damaging than issues disclosed upfront.",
          cn: "PMP需要完整的信息。FDA审查期间发现的未披露问题比提前披露的问题危害更大。",
        },
        followUps: [
          {
            en: "Any regulatory interactions in other countries (CE, NMPA)?",
            cn: "在其他国家是否有法规互动（CE、NMPA）？",
          },
          {
            en: "Any adverse events or near-misses during prototype testing?",
            cn: "原型测试期间是否有不良事件或险情？",
          },
          {
            en: "Any previous FDA submissions (for any device) by the inventor?",
            cn: "发明人是否曾为任何设备提交过FDA申请？",
          },
        ],
      },
    ],
  },
];

// ============================================================
// ACTIVE ROLE — Controls UI permissions
// ============================================================

// Password-based auth: password determines role at login
export let IS_ADMIN: boolean = false;
export let ACTIVE_ROLE: UserRole = "business";

const CREDENTIAL_HASHES: Record<string, { role: UserRole; admin: boolean }> = {
  "135c73edb7cca493ebfa47115cc3015addde7165d14974954b1e125e55a13785": {
    role: "pmp",
    admin: true,
  },
  "4b355cd6cc19844a3c8fd44cf16c6c168a2eb81eba0fb74bec0f5f21687c2acc": {
    role: "business",
    admin: false,
  },
};

async function sha256(message: string): Promise<string> {
  const data = new TextEncoder().encode(message);
  const hashBuffer = await crypto.subtle.digest("SHA-256", data);
  const hashArray = Array.from(new Uint8Array(hashBuffer));
  return hashArray.map((b) => b.toString(16).padStart(2, "0")).join("");
}

export async function authenticatePassword(password: string): Promise<boolean> {
  const hash = await sha256(password);
  const cred = CREDENTIAL_HASHES[hash];
  if (!cred) return false;
  IS_ADMIN = cred.admin;
  ACTIVE_ROLE = cred.role;
  return true;
}

export function setActiveRole(role: UserRole): void {
  ACTIVE_ROLE = role;
}
