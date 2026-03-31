// ============================================================
// SEED — Takes wizard answers → populates data.ts structures
// ============================================================

import {
  PROJECT,
  TRACKS,
  GATES,
  RISKS,
  STANDARDS,
  TIMELINE_EVENTS,
  CASH_RUNWAY,
  STAKEHOLDER_INPUTS,
  CHANGE_REQUESTS,
  AUDIT_LOG,
  DHF_DOCUMENTS,
  CAPA_LOG,
  ACTION_ITEMS,
  BUDGET_CATEGORIES,
  TEAM_MEMBERS,
  SUPPLIERS,
  QA_SECTIONS,
  TARGET_INVESTORS,
  IR_ACTIVITIES,
  INVESTOR_BRIDGE,
  SHAREHOLDERS,
  EQUITY_EVENTS,
  VESTING_SCHEDULES,
} from "./data.ts";

import { DEFAULT_DHF_DOCS } from "./wizard.ts";
import { DEVICE_TEMPLATES } from "./templates.ts";

// ── Public types ─────────────────────────────────
export interface TeamEntry {
  name: string;
  role: string;
  email: string;
  workstreams: string;
}
export interface BudgetEntry {
  label: string;
  planned: number;
}
export interface SupplierEntry {
  name: string;
  component: string;
  leadTimeDays: number;
}

export interface WizardAnswers {
  lang: string;
  templateId?: string;
  projectName: string;
  projectNameCn?: string;
  subtitle?: string;
  preparedDate?: string;
  contactEmail?: string;
  submissionType?: string;
  deviceClass?: string;
  productCode?: string;
  regulationSection?: string;
  predicateDevices?: string;
  applicantName?: string;
  applicantNameCn?: string;
  applicantAddress?: string;
  applicantPhone?: string;
  contactName?: string;
  manufacturerName?: string;
  manufacturerNameCn?: string;
  team?: TeamEntry[];
  budgets?: BudgetEntry[];
  cashOnHand?: number | string;
  currency?: string;
  projectDurationMonths?: number | string;
  currentMonth?: number | string;
  techAreas?: string;
  suppliers?: SupplierEntry[];
  docFlags?: boolean[];
}

// Helper to create offset dates from today
function offsetDate(days: number): string {
  const d = new Date();
  d.setDate(d.getDate() + days);
  return d.toISOString().slice(0, 10);
}

function ls(en: string, cn?: string): { en: string; cn: string } {
  return { en, cn: cn || en };
}

// ── Main seed function ──────────────────────────
export function seed(a: WizardAnswers): void {
  const lang = (a.lang as "en" | "cn") || "en";
  const isCn = lang === "cn";
  const nm = a.projectName || "Untitled Project";
  const nmCn = a.projectNameCn || nm;
  const sub = a.subtitle || "";
  const subCn = sub; // user can overwrite later

  // ── PROJECT ──────────────────────────────────
  Object.assign(PROJECT, {
    name: ls(nm, nmCn),
    subtitle: ls(sub, subCn),
    submissionType: a.submissionType || "510k-standard",
    applicant: ls(
      a.applicantName || "TBD",
      a.applicantNameCn || a.applicantName || "TBD",
    ),
    applicantAddress: a.applicantAddress || "",
    applicantPhone: a.applicantPhone || "",
    contactName: a.contactName || "",
    contactEmail: a.contactEmail || "",
    manufacturer: ls(
      a.manufacturerName || "TBD",
      a.manufacturerNameCn || a.manufacturerName || "TBD",
    ),
    preparedDate:
      a.preparedDate ||
      new Date().toLocaleDateString("en-US", {
        month: "long",
        year: "numeric",
      }),
    currentMonth: Number(a.currentMonth) || 0,
  });

  const dur = Number(a.projectDurationMonths) || 12;

  // ── TRACKS ───────────────────────────────────
  // Parse tech areas for technical milestones
  const techLines = (a.techAreas || "")
    .split("\n")
    .map((s) => s.trim())
    .filter(Boolean);
  const techMilestones = techLines.map((line, i) => ({
    id: `MS-T-${String(i + 1).padStart(3, "0")}`,
    month: Math.round(((i + 1) * dur) / (techLines.length + 1)),
    title: ls(line),
    description: ls(`Technical workstream: ${line}`),
    status: "not-started" as const,
    owner: "tech" as const,
    category: "Engineering",
  }));
  if (!techMilestones.length) {
    techMilestones.push({
      id: "MS-T-001",
      month: 1,
      title: ls(isCn ? "设计冻结" : "Design Freeze"),
      description: ls(isCn ? "锁定设计规格" : "Lock design specifications"),
      status: "not-started",
      owner: "tech",
      category: "Engineering",
    });
  }

  const regMilestones = [
    {
      id: "MS-R-001",
      month: 1,
      title: ls("Pre-Sub Meeting", "Pre-Sub会议"),
      description: ls("FDA Pre-Submission meeting", "FDA预提交会议"),
      status: "not-started" as const,
      owner: "regulatory" as const,
      category: "Regulatory",
    },
    {
      id: "MS-R-002",
      month: Math.round(dur * 0.5),
      title: ls("510(k) Preparation", "510(k)准备"),
      description: ls("Prepare submission package", "准备提交包"),
      status: "not-started" as const,
      owner: "regulatory" as const,
      category: "Regulatory",
    },
    {
      id: "MS-R-003",
      month: Math.round(dur * 0.8),
      title: ls("510(k) Submitted", "510(k)已提交"),
      description: ls("File with FDA", "向FDA提交"),
      status: "not-started" as const,
      owner: "regulatory" as const,
      category: "Regulatory",
    },
  ];

  TRACKS.technical.milestones.length = 0;
  techMilestones.forEach((m) => TRACKS.technical.milestones.push(m));
  TRACKS.regulatory.milestones.length = 0;
  regMilestones.forEach((m) => TRACKS.regulatory.milestones.push(m));

  // ── GATES ────────────────────────────────────
  GATES.length = 0;
  const gateCount = Math.min(Math.max(Math.floor(dur / 3), 2), 6);
  for (let i = 0; i < gateCount; i++) {
    GATES.push({
      id: `G${i + 1}`,
      number: i + 1,
      title: ls(
        `Gate ${i + 1}: ${i === 0 ? "Feasibility" : i === gateCount - 1 ? "Launch Readiness" : `Phase ${i + 1} Review`}`,
      ),
      month: Math.round(((i + 1) * dur) / (gateCount + 1)),
      status: "not-started",
      criteria: [
        {
          en: "Technical deliverables complete",
          cn: "技术交付物完成",
          met: false,
        },
        { en: "Budget on track", cn: "预算正常", met: false },
        { en: "Risk mitigations confirmed", cn: "风险缓解已确认", met: false },
      ],
      decision: null,
      decisionBy: null,
      decisionDate: null,
      notes: [],
      inputBusiness: [],
      inputTech: [],
    });
  }

  // ── RISKS ────────────────────────────────────
  RISKS.length = 0;
  RISKS.push(
    {
      id: "RISK-001",
      title: ls("Schedule Delay", "进度延迟"),
      severity: "high",
      probability: "medium",
      riskLevel: "yellow",
      controls: ls("Weekly tracking, buffer time", "每周跟踪，缓冲时间"),
      residual: ls("Moderate", "中等"),
      mitigationStatus: "in-progress",
      module: "PM",
      standard: "ISO 14971",
    },
    {
      id: "RISK-002",
      title: ls("Regulatory Gap", "法规差距"),
      severity: "high",
      probability: "low",
      riskLevel: "yellow",
      controls: ls("Pre-Sub feedback, RA consultant", "Pre-Sub反馈，RA顾问"),
      residual: ls("Low", "低"),
      mitigationStatus: "not-started",
      module: "Regulatory",
      standard: "21 CFR 820",
    },
    {
      id: "RISK-003",
      title: ls("Budget Overrun", "预算超支"),
      severity: "medium",
      probability: "medium",
      riskLevel: "yellow",
      controls: ls("Monthly reviews, contingency", "每月审查，应急储备"),
      residual: ls("Moderate", "中等"),
      mitigationStatus: "not-started",
      module: "Finance",
      standard: "",
    },
  );
  // Merge template-specific risks
  const tmpl = a.templateId ? DEVICE_TEMPLATES[a.templateId] : null;
  if (tmpl) {
    tmpl.risks.forEach((r) => {
      RISKS.push({
        id: `RISK-${String(RISKS.length + 1).padStart(3, "0")}`,
        title: ls(r.title.en, r.title.cn),
        severity: r.severity,
        probability: r.probability,
        riskLevel: r.riskLevel,
        controls: ls(r.controls.en, r.controls.cn),
        residual: ls(
          r.riskLevel === "red"
            ? "High"
            : r.riskLevel === "yellow"
              ? "Moderate"
              : "Low",
          r.riskLevel === "red"
            ? "高"
            : r.riskLevel === "yellow"
              ? "中等"
              : "低",
        ),
        mitigationStatus: "not-started",
        module: r.module,
        standard: r.standard,
      });
    });
  }

  // ── STANDARDS ─────────────────────────────────
  STANDARDS.length = 0;
  // Use template standards if available, otherwise use generic defaults
  const stdList = tmpl
    ? tmpl.standards.map((s) => ({
        code: s.code,
        title: ls(s.title.en, s.title.cn),
        applies: s.applies,
      }))
    : [
        {
          code: "IEC 60601-1",
          title: ls(
            "Medical Electrical Equipment — General",
            "医用电气设备——通用",
          ),
          applies: "All",
        },
        {
          code: "IEC 62304",
          title: ls(
            "Medical Device Software — Lifecycle",
            "医疗器械软件——生命周期",
          ),
          applies: "All",
        },
        {
          code: "ISO 14971",
          title: ls("Risk Management for Medical Devices", "医疗器械风险管理"),
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
      ];
  stdList.forEach((s, i) => {
    STANDARDS.push({
      id: `STD-${String(i + 1).padStart(3, "0")}`,
      code: s.code,
      title: s.title,
      applies: s.applies || "All",
      status: "not-started",
      progress: 0,
      clauses: [],
    });
  });

  // ── TIMELINE_EVENTS ──────────────────────────
  TIMELINE_EVENTS.length = 0;
  for (let m = 0; m <= dur; m += 3) {
    TIMELINE_EVENTS.push({
      month: m,
      technical: ls(m === 0 ? "Project Kickoff" : `Technical Review M+${m}`),
      business: ls(
        m === 0 ? "Team Mobilization" : `Business Checkpoint M+${m}`,
      ),
      impact: "neutral",
    });
  }

  // ── CASH_RUNWAY ──────────────────────────────
  const cash = Number(a.cashOnHand) || 0;
  const totalBudget = (a.budgets || []).reduce(
    (s, b) => s + (b.planned || 0),
    0,
  );
  const monthlyBurn = totalBudget > 0 ? Math.round(totalBudget / dur) : 0;
  Object.assign(CASH_RUNWAY, {
    cashOnHand: cash,
    monthlyBurn,
    runwayMonths: monthlyBurn > 0 ? Math.round(cash / monthlyBurn) : 0,
    currency: a.currency || "USD",
    fundingRounds:
      cash > 0
        ? [
            {
              id: "FR-001",
              label: ls("Initial Funding", "初始资金"),
              amount: cash,
              date: offsetDate(0),
              status: "received" as const,
            },
          ]
        : [],
    burnHistory: (() => {
      const hist = [];
      const months = Math.min(dur, 6);
      for (let m = 0; m < months; m++) {
        hist.push({
          month: m,
          burn: monthlyBurn,
          note: ls(
            m === 0 ? "Project start" : `Month ${m}`,
            m === 0 ? "项目启动" : `第${m}月`,
          ),
        });
      }
      return hist;
    })(),
  });

  // ── STAKEHOLDER_INPUTS ───────────────────────
  STAKEHOLDER_INPUTS.length = 0;

  // ── CHANGE_REQUESTS ──────────────────────────
  CHANGE_REQUESTS.length = 0;

  // ── AUDIT_LOG ────────────────────────────────
  AUDIT_LOG.length = 0;
  AUDIT_LOG.push({
    id: "AUD-001",
    timestamp: new Date().toISOString(),
    user: "Wizard",
    action: "milestone-status",
    targetId: "SYSTEM",
    field: "init",
    oldValue: "",
    newValue: "Project created via Setup Wizard",
    detail: `Project "${nm}" initialized`,
  });

  // ── DHF_DOCUMENTS ────────────────────────────
  DHF_DOCUMENTS.length = 0;
  const flags = a.docFlags || DEFAULT_DHF_DOCS.map(() => true);
  DEFAULT_DHF_DOCS.forEach((doc, i) => {
    if (flags[i] === false) return;
    DHF_DOCUMENTS.push({
      id: `DHF-${String(i + 1).padStart(3, "0")}`,
      code: doc.code,
      title: ls(doc.en, doc.cn),
      category: "Design Control",
      owner: "regulatory",
      status: "not-started",
      dueMonth: Math.round(((i + 1) * dur) / (DEFAULT_DHF_DOCS.length + 1)),
      notes: "",
    });
  });

  // ── CAPA_LOG ─────────────────────────────────
  CAPA_LOG.length = 0;

  // ── ACTION_ITEMS ─────────────────────────────
  ACTION_ITEMS.length = 0;
  ACTION_ITEMS.push(
    {
      id: "ACT-001",
      title: ls("Define Design Inputs", "定义设计输入"),
      assignee: a.team?.[0]?.name || "PM",
      owner: "tech",
      priority: "high",
      status: "todo",
      dueDate: offsetDate(14),
      linkedGate: "G1",
      notes: "",
    },
    {
      id: "ACT-002",
      title: ls("Draft Risk Analysis", "起草风险分析"),
      assignee: a.team?.[0]?.name || "PM",
      owner: "regulatory",
      priority: "high",
      status: "todo",
      dueDate: offsetDate(30),
      linkedGate: "G1",
      notes: "",
    },
    {
      id: "ACT-003",
      title: ls("Identify Predicate Devices", "识别前置器械"),
      assignee: a.team?.[0]?.name || "PM",
      owner: "regulatory",
      priority: "medium",
      status: "todo",
      dueDate: offsetDate(21),
      linkedGate: "G1",
      notes: "",
    },
  );

  // ── BUDGET_CATEGORIES ────────────────────────
  BUDGET_CATEGORIES.length = 0;
  const budgets = a.budgets || [];
  if (budgets.length) {
    budgets.forEach((b, i) => {
      if (!b.label) return;
      BUDGET_CATEGORIES.push({
        id: `BUD-${String(i + 1).padStart(3, "0")}`,
        label: ls(b.label),
        planned: b.planned || 0,
        actual: 0,
        notes: "",
      });
    });
  } else {
    BUDGET_CATEGORIES.push({
      id: "BUD-001",
      label: ls("General", "一般"),
      planned: 0,
      actual: 0,
      notes: "",
    });
  }

  // ── TEAM_MEMBERS ─────────────────────────────
  TEAM_MEMBERS.length = 0;
  const team = a.team || [];
  team.forEach((m, i) => {
    if (!m.name) return;
    const alloc = m.workstreams
      .split("\n")
      .map((line) => {
        const parts = line.split(":");
        if (parts.length < 2) return null;
        return { workstream: parts[0].trim(), pct: parseInt(parts[1]) || 0 };
      })
      .filter(Boolean) as { workstream: string; pct: number }[];
    TEAM_MEMBERS.push({
      id: `TM-${String(i + 1).padStart(3, "0")}`,
      name: m.name,
      role: ls(m.role),
      email: m.email || undefined,
      allocation: alloc.length
        ? alloc
        : [{ workstream: m.role || "General", pct: 100 }],
      capacity: 100,
    });
  });
  if (!TEAM_MEMBERS.length) {
    TEAM_MEMBERS.push({
      id: "TM-001",
      name: "Project Lead",
      role: ls("Project Manager", "项目经理"),
      allocation: [{ workstream: "Project Management", pct: 100 }],
      capacity: 100,
    });
  }

  // ── SUPPLIERS ────────────────────────────────
  SUPPLIERS.length = 0;
  const suppliers = a.suppliers || [];
  suppliers.forEach((s, i) => {
    if (!s.name) return;
    SUPPLIERS.push({
      id: `SUP-${String(i + 1).padStart(3, "0")}`,
      name: s.name,
      component: ls(s.component),
      status: "under-review",
      leadTimeDays: s.leadTimeDays || 0,
      poStatus: "Pending",
      contractMfgMilestone: "TBD",
      notes: "",
    });
  });
  if (!SUPPLIERS.length) {
    SUPPLIERS.push({
      id: "SUP-001",
      name: isCn ? "供应商 (待定)" : "Supplier (TBD)",
      component: ls(isCn ? "待定" : "TBD"),
      status: "under-review",
      leadTimeDays: 0,
      poStatus: "Pending",
      contractMfgMilestone: "TBD",
      notes: "",
    });
  }

  // ── QA_SECTIONS ──────────────────────────────
  QA_SECTIONS.length = 0;
  QA_SECTIONS.push({
    num: 1,
    title: ls("General Discussion", "综合讨论"),
    context: ls(`Discussion thread for ${nm}`, `${nmCn}讨论线程`),
    questions: [
      {
        num: 1,
        question: ls(
          "What are the immediate priorities?",
          "当前的优先事项是什么？",
        ),
        why: ls("Align team on first actions", "统一团队首要行动"),
        followUps: [],
      },
    ],
  });

  // ── TARGET_INVESTORS ─────────────────────────
  TARGET_INVESTORS.length = 0;
  TARGET_INVESTORS.push(
    {
      id: "INV-001",
      name: isCn ? "投资方1 (待定)" : "Investor 1 (TBD)",
      type: "VC",
      stage: "Seed",
      contact: "prospect",
      amount: 0,
      notes: isCn ? "待联系" : "Pending outreach",
    },
    {
      id: "INV-002",
      name: isCn ? "投资方2 (待定)" : "Investor 2 (TBD)",
      type: "Angel Group",
      stage: "Seed",
      contact: "prospect",
      amount: 0,
      notes: "",
    },
  );

  // ── IR_ACTIVITIES ────────────────────────────
  IR_ACTIVITIES.length = 0;
  IR_ACTIVITIES.push({
    id: "IRA-001",
    date: offsetDate(0),
    activity: isCn
      ? "项目启动——准备投资者资料"
      : "Project kickoff — prepare investor materials",
    status: "todo",
  });

  // ── INVESTOR_BRIDGE ──────────────────────────
  INVESTOR_BRIDGE.length = 0;
  // Seed default bridge milestones aligned to project duration
  INVESTOR_BRIDGE.push(
    {
      regulatoryId: "R1",
      month: 0,
      milestone: ls("Pre-Sub Filed", "预提交已递交"),
      investorAction: ls(
        "Build relationships, warm intros — FDA engagement signals credibility",
        "建立关系、暖引荐 — FDA参与证明可信度",
      ),
      signal: "warm",
    },
    {
      regulatoryId: "R2",
      month: Math.round(dur * 0.15),
      milestone: ls("Pre-Sub Meeting (FDA Feedback)", "预提交会议（FDA反馈）"),
      investorAction: ls(
        "Active outreach & pitch meetings — FDA feedback de-risks the pathway",
        "主动接触和路演 — FDA反馈降低了监管风险",
      ),
      signal: "active",
    },
    {
      regulatoryId: "T3",
      month: Math.round(dur * 0.25),
      milestone: ls(
        "Bench & Performance Testing Complete",
        "台架和性能测试完成",
      ),
      investorAction: ls(
        "Share performance data with prospects — hard data proves technical viability",
        "与潜在投资者分享性能数据 — 硬数据证明技术可行性",
      ),
      signal: "active",
    },
    {
      regulatoryId: "R3",
      month: Math.round(dur * 0.5),
      milestone: ls("510(k) Submitted", "510(k)已提交"),
      investorAction: ls(
        "Push for term sheets — submission is the inflection point",
        "推动条款清单 — 提交是拐点",
      ),
      signal: "peak",
    },
    {
      regulatoryId: "R4",
      month: Math.round(dur * 0.75),
      milestone: ls("510(k) Clearance", "510(k)批准"),
      investorAction: ls(
        "Close rounds, Series A positioning — cleared device, maximum leverage",
        "完成融资轮次、Series A定位 — 已获批设备、最大谈判筹码",
      ),
      signal: "close",
    },
  );

  // ── SHAREHOLDERS (Cap Table) ─────────────────
  const founderName = a.applicantName || (isCn ? "创始人" : "Founder");
  SHAREHOLDERS.length = 0;
  SHAREHOLDERS.push(
    {
      id: "SH-001",
      name: founderName,
      role: isCn ? "创始人" : "Founder",
      shareClass: "common",
      shares: 0,
      notes: isCn ? "创始人普通股" : "Founder common shares",
    },
    {
      id: "SH-002",
      name: isCn ? "期权池" : "Option Pool",
      role: isCn ? "预留" : "Reserved",
      shareClass: "options",
      shares: 0,
      notes: isCn ? "员工期权预留 (ESOP)" : "Employee stock option pool (ESOP)",
    },
  );

  // ── EQUITY_EVENTS ────────────────────────────
  EQUITY_EVENTS.length = 0;
  EQUITY_EVENTS.push({
    id: "EQ-001",
    date: offsetDate(0),
    event: isCn ? "公司成立" : "Company Formation",
    shareClass: "common",
    shares: 0,
    pricePerShare: 0,
    totalValue: 0,
    status: "pending",
    notes: isCn ? "待分配股份" : "Shares pending allocation",
  });

  // ── VESTING_SCHEDULES ────────────────────────
  VESTING_SCHEDULES.length = 0;
  VESTING_SCHEDULES.push({
    id: "VS-001",
    holder: founderName,
    shares: 0,
    startDate: offsetDate(0),
    cliffMonths: 12,
    totalMonths: 48,
    vestedShares: 0,
    status: "vesting",
    notes: isCn ? "4年归属, 1年悬崖期" : "4-year vest, 1-year cliff",
  });
}
