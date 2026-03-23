// ============================================================
// INTERNATIONALIZATION (i18n) — English / 中文
// ============================================================

const I18N = {
  en: {
    // Top bar
    appTitle: "Control Tower",
    appSubtitle: "ICU Respiratory Digital Twin",
    masterQuestion:
      "Are we still on track to FDA clearance — and what is at risk?",
    pmpBadge: "PMP Authority",
    currentMonth: "Current",

    // Tabs
    tabDualTrack: "Dual-Track",
    tabGates: "Gate System",
    tabRisks: "Risk Dashboard",
    tabTimeline: "Timeline",
    tabRegulatory: "Regulatory Tracker",

    // Summary bar
    summaryOverall: "Overall Status",
    summaryNextGate: "Next Gate",
    summaryRedRisks: "Red Risks",
    summaryPendingInputs: "Pending Inputs",
    summaryDaysToMilestone: "Days to Next Milestone",
    statusOnTrack: "ON TRACK",
    statusAtRisk: "AT RISK",
    statusBlocked: "BLOCKED",

    // Dual-track
    dualTrackTitle: "Dual-Track Dashboard",
    dualTrackDesc:
      "Technical progress and regulatory milestones — side by side",
    techTrackTitle: "Technical Track",
    regTrackTitle: "Regulatory Track",

    // Gates
    gatesTitle: "Gate System",
    gatesDesc: "Decision checkpoints — Proceed / Need Data / Stop",
    gateMonthPrefix: "Target: M+",
    gateCriteriaMet: "criteria met",
    gateDecisionTitle: "PMP Decision (Authority)",
    gateProceed: "✓ Proceed",
    gateNeedData: "⟳ Need More Data",
    gateStop: "✕ Stop",
    gateInputsTitle: "Stakeholder Inputs",
    gateNotesTitle: "Gate Notes",
    addNotePlaceholder: "Add a note (PMP authority)...",
    addNoteBtn: "Add Note",

    // Risks
    risksTitle: "Risk Dashboard",
    risksDesc:
      "ISO 14971 — Top risks, mitigation status, and residual assessment",
    filterAll: "All",
    filterRed: "Red",
    filterYellow: "Yellow",
    filterGreen: "Green",
    topRisksTitle: "Top 5 Risks This Week",
    riskSeverity: "Severity",
    riskProbability: "Probability",
    riskControls: "Controls",
    riskResidual: "Residual",
    riskMitigation: "Mitigation",
    riskModule: "Module",

    // Timeline
    timelineTitle: "Timeline — Business Translation",
    timelineDesc:
      "Technical milestones translated into investor and business language",
    tlTechnical: "Technical",
    tlBusiness: "Business Impact",

    // Regulatory
    regulatoryTitle: "Regulatory Standards Tracker",
    regulatoryDesc: "IEC 60601, ISO 10993, 21 CFR compliance matrix",
    colCode: "Standard",
    colTitle: "Description",
    colApplies: "Applies To",
    colStatus: "Status",
    colProgress: "Progress",

    // Input panel
    inputPanelTitle: "Stakeholder Inputs",
    inputFromTech: "Technology Team",
    inputFromBusiness: "Business / Investors",

    // Statuses
    complete: "Complete",
    inProgress: "In Progress",
    notStarted: "Not Started",
    pendingReview: "Pending Review",
    accepted: "Accepted",
    rejected: "Rejected",
    noted: "Noted",
  },

  cn: {
    // Top bar
    appTitle: "控制塔",
    appSubtitle: "ICU呼吸数字孪生",
    masterQuestion: "我们是否仍在FDA批准的正轨上——有什么风险？",
    pmpBadge: "PMP权限",
    currentMonth: "当前",

    // Tabs
    tabDualTrack: "双轨视图",
    tabGates: "门控系统",
    tabRisks: "风险仪表盘",
    tabTimeline: "时间线",
    tabRegulatory: "法规追踪",

    // Summary bar
    summaryOverall: "总体状态",
    summaryNextGate: "下一门控",
    summaryRedRisks: "红色风险",
    summaryPendingInputs: "待处理输入",
    summaryDaysToMilestone: "距下一里程碑",
    statusOnTrack: "正轨",
    statusAtRisk: "有风险",
    statusBlocked: "受阻",

    // Dual-track
    dualTrackTitle: "双轨仪表盘",
    dualTrackDesc: "技术进展与法规里程碑——并排显示",
    techTrackTitle: "技术路径",
    regTrackTitle: "法规路径",

    // Gates
    gatesTitle: "门控系统",
    gatesDesc: "决策检查点 — 通过 / 需更多数据 / 停止",
    gateMonthPrefix: "目标: M+",
    gateCriteriaMet: "标准已满足",
    gateDecisionTitle: "PMP决策（权限）",
    gateProceed: "✓ 通过",
    gateNeedData: "⟳ 需更多数据",
    gateStop: "✕ 停止",
    gateInputsTitle: "利益相关方输入",
    gateNotesTitle: "门控备注",
    addNotePlaceholder: "添加备注（PMP权限）...",
    addNoteBtn: "添加备注",

    // Risks
    risksTitle: "风险仪表盘",
    risksDesc: "ISO 14971 — 主要风险、缓解状态和残余评估",
    filterAll: "全部",
    filterRed: "红色",
    filterYellow: "黄色",
    filterGreen: "绿色",
    topRisksTitle: "本周前5大风险",
    riskSeverity: "严重性",
    riskProbability: "可能性",
    riskControls: "控制措施",
    riskResidual: "残余风险",
    riskMitigation: "缓解措施",
    riskModule: "模块",

    // Timeline
    timelineTitle: "时间线 — 商业翻译",
    timelineDesc: "技术里程碑转化为投资者和商业语言",
    tlTechnical: "技术方面",
    tlBusiness: "商业影响",

    // Regulatory
    regulatoryTitle: "法规标准追踪器",
    regulatoryDesc: "IEC 60601, ISO 10993, 21 CFR合规矩阵",
    colCode: "标准",
    colTitle: "描述",
    colApplies: "适用于",
    colStatus: "状态",
    colProgress: "进度",

    // Input panel
    inputPanelTitle: "利益相关方输入",
    inputFromTech: "技术团队",
    inputFromBusiness: "商业/投资方",

    // Statuses
    complete: "已完成",
    inProgress: "进行中",
    notStarted: "未开始",
    pendingReview: "待审核",
    accepted: "已接受",
    rejected: "已拒绝",
    noted: "已记录",
  },
};

// Active language state
let currentLang = "en";

function t(key) {
  return I18N[currentLang][key] || I18N.en[key] || key;
}

function localizedText(obj) {
  if (!obj) return "";
  return obj[currentLang] || obj.en || "";
}

function applyLanguage(lang) {
  currentLang = lang;
  document.querySelectorAll("[data-i18n]").forEach((el) => {
    const key = el.getAttribute("data-i18n");
    if (I18N[lang][key]) {
      el.textContent = I18N[lang][key];
    }
  });
  document.documentElement.lang = lang === "cn" ? "zh-CN" : "en";
}
