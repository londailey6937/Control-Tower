// ============================================================
// SEED.TS — Generate all CT data from wizard answers
// Mutates the live exported arrays/objects from data.ts in-place
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
} from "./data.ts";

export interface WizardAnswers {
  // Step 1 — Project basics
  projectName: string;
  projectNameCn?: string;
  subtitle?: string;
  preparedDate?: string;
  // Step 2 — Regulatory
  submissionType?: string;
  deviceClass?: string;
  productCode?: string;
  regulationSection?: string;
  predicateDevices?: string;
  // Step 3 — Applicant
  applicantName: string;
  applicantNameCn?: string;
  manufacturerName?: string;
  manufacturerNameCn?: string;
  // Step 4 — Timeline & budget
  projectDurationMonths?: number;
  currentMonth?: number;
  cashOnHand?: number;
  monthlyBurn?: number;
  currency?: string;
  // Step 5 — Team & areas
  techAreas?: string;
  teamLead?: string;
  teamSize?: number;
}

const SUBMISSION_LABELS: Record<string, string> = {
  "510k-standard": "510(k) Standard",
  "510k-special": "510(k) Special",
  "510k-abbreviated": "510(k) Abbreviated",
  "de-novo": "De Novo Classification",
  pma: "Premarket Approval (PMA)",
  other: "Other / TBD",
};

function ls(en: string, cn?: string) {
  return { en, cn: cn || en };
}

function clearArray<T>(arr: T[]): void {
  arr.length = 0;
}

function parseTechAreas(raw?: string): string[] {
  if (!raw) return ["Design & Engineering", "Testing & Validation", "Regulatory Compliance"];
  return raw
    .split("\n")
    .map((s) => s.trim())
    .filter(Boolean);
}

function parsePredicates(raw?: string): string[] {
  if (!raw) return [];
  return raw
    .split("\n")
    .map((s) => s.trim())
    .filter(Boolean);
}

/**
 * Populate all live data exports from wizard answers.
 * Mutates in-place so existing app.ts references stay valid.
 */
export function seed(a: WizardAnswers): void {
  const name = a.projectName;
  const nameCn = a.projectNameCn || name;
  const duration = a.projectDurationMonths || 12;
  const month0 = a.currentMonth ?? 0;
  const areas = parseTechAreas(a.techAreas);
  const predicates = parsePredicates(a.predicateDevices);
  const submissionLabel = SUBMISSION_LABELS[a.submissionType || "other"] || a.submissionType || "TBD";
  const now = new Date().toISOString().slice(0, 10);

  // ── PROJECT ──────────────────────────────────
  Object.assign(PROJECT, {
    name: ls(name, nameCn),
    subtitle: ls(a.subtitle || name, a.subtitle || nameCn),
    submissionType: submissionLabel + (a.deviceClass ? ` (Class ${a.deviceClass})` : ""),
    applicant: ls(a.applicantName, a.applicantNameCn || a.applicantName),
    manufacturer: ls(
      a.manufacturerName || a.applicantName,
      a.manufacturerNameCn || a.manufacturerName || a.applicantName
    ),
    preparedDate: a.preparedDate || new Date().toLocaleDateString("en-US", { month: "long", year: "numeric" }),
    currentMonth: month0,
  });

  // ── TRACKS — Technical milestones from tech areas ─────
  const techMilestones = areas.map((area, i) => ({
    id: `T${i + 1}`,
    month: Math.round((i * duration) / Math.max(areas.length, 1)),
    title: ls(`${area} — Design & Development`),
    description: ls(`Complete design, development and documentation for ${area}.`),
    detail: ls(`Key workstream covering ${area}. Activities include design review, prototyping, testing, and documentation per applicable standards.`),
    status: i === 0 && month0 > 0 ? ("in-progress" as const) : ("not-started" as const),
    owner: "tech" as const,
    category: i === 0 ? "prototype" : i < areas.length / 2 ? "validation" : "testing",
  }));

  // Regulatory milestones (standard FDA pathway)
  const regMilestones = [
    {
      id: "R1",
      month: 0,
      title: ls("Regulatory Strategy & Pre-Submission Planning"),
      description: ls(`Define ${submissionLabel} pathway, identify predicates, prepare Pre-Sub questions.`),
      detail: ls(`Establish the regulatory strategy for ${name}. Identify predicate devices${predicates.length ? ": " + predicates.join(", ") : ""}. Prepare Pre-Submission package for FDA CDRH.`),
      status: month0 > 0 ? ("in-progress" as const) : ("not-started" as const),
      owner: "regulatory" as const,
      category: "submission",
    },
    {
      id: "R2",
      month: Math.round(duration * 0.15),
      title: ls("Pre-Submission Meeting (FDA)"),
      description: ls("Receive FDA feedback on predicate strategy, testing protocol, and classification."),
      detail: ls("Q-Meeting with CDRH review team to confirm substantial equivalence strategy through regulatory pathway."),
      status: "not-started" as const,
      owner: "regulatory" as const,
      category: "meeting",
    },
    {
      id: "R3",
      month: Math.round(duration * 0.6),
      title: ls(`${submissionLabel} Submission`),
      description: ls(`File ${submissionLabel} submission package with FDA.`),
      detail: ls(`Complete all submission sections and file with FDA. Includes device description, performance data, risk analysis, labeling, and clinical evidence.`),
      status: "not-started" as const,
      owner: "regulatory" as const,
      category: "submission",
    },
    {
      id: "R4",
      month: Math.round(duration * 0.85),
      title: ls("FDA Clearance / Approval"),
      description: ls("Target clearance date based on project timeline."),
      detail: ls(`Anticipated ${submissionLabel} clearance. Upon clearance, proceed to commercial launch preparation.`),
      status: "not-started" as const,
      owner: "regulatory" as const,
      category: "submission",
    },
  ];

  TRACKS.technical.label = ls("Technical Track", "技术路径");
  TRACKS.technical.icon = "🔬";
  TRACKS.technical.milestones.length = 0;
  TRACKS.technical.milestones.push(...techMilestones);

  TRACKS.regulatory.label = ls("Regulatory Track", "法规路径");
  TRACKS.regulatory.icon = "📋";
  TRACKS.regulatory.milestones.length = 0;
  TRACKS.regulatory.milestones.push(...regMilestones);

  // ── GATES ─────────────────────────────────────
  clearArray(GATES);
  const gatePoints = [
    { frac: 0.2, title: "Design Review Complete", criteria: ["Design inputs documented", "Risk analysis initiated", "Prototype ready for testing"] },
    { frac: 0.4, title: "Verification & Validation Ready", criteria: ["Testing protocols approved", "Test equipment qualified", "Predicate comparison documented"] },
    { frac: 0.6, title: "Submission Package Complete", criteria: ["All submission sections drafted", "Risk analysis finalized", "Labeling reviewed"] },
    { frac: 0.85, title: "Commercial Launch Ready", criteria: ["Regulatory clearance received", "Manufacturing validated", "Quality system audit passed"] },
  ];
  gatePoints.forEach((gp, i) => {
    GATES.push({
      id: `G${i + 1}`,
      number: i + 1,
      title: ls(gp.title),
      month: Math.round(duration * gp.frac),
      status: "not-started",
      criteria: gp.criteria.map((c) => ({ en: c, cn: c, met: false })),
      decision: null,
      decisionBy: null,
      decisionDate: null,
      notes: [],
      inputBusiness: [],
      inputTech: [],
    });
  });

  // ── RISKS ─────────────────────────────────────
  clearArray(RISKS);
  const defaultRisks = [
    { title: "Regulatory pathway rejection or reclassification", sev: "high" as const, prob: "low" as const, level: "yellow" as const, std: "21 CFR 807" },
    { title: "Design verification failure — performance targets not met", sev: "high" as const, prob: "medium" as const, level: "red" as const, std: "ISO 14971" },
    { title: "Supply chain disruption for critical components", sev: "medium" as const, prob: "medium" as const, level: "yellow" as const, std: "ISO 13485" },
    { title: "Cybersecurity vulnerability in device software", sev: "medium" as const, prob: "low" as const, level: "yellow" as const, std: "FDA Cybersecurity 2023" },
    { title: "Insufficient funding to complete regulatory pathway", sev: "high" as const, prob: "low" as const, level: "yellow" as const, std: "Business" },
  ];
  defaultRisks.forEach((r, i) => {
    RISKS.push({
      id: `RISK-${String(i + 1).padStart(3, "0")}`,
      title: ls(r.title),
      severity: r.sev,
      probability: r.prob,
      riskLevel: r.level,
      controls: ls("Controls to be defined"),
      residual: ls("TBD"),
      mitigationStatus: "not-started",
      module: "N/A",
      standard: r.std,
    });
  });

  // ── STANDARDS ─────────────────────────────────
  clearArray(STANDARDS);
  const stdList = [
    { code: "IEC 60601-1:2005+AMD1", title: "Medical Electrical Equipment — General Safety" },
    { code: "IEC 60601-1-2:2014", title: "Electromagnetic Compatibility (EMC)" },
    { code: "ISO 14971:2019", title: "Risk Management for Medical Devices" },
    { code: "IEC 62366-1:2015", title: "Usability Engineering" },
    { code: "IEC 62304:2006+AMD1", title: "Medical Device Software Lifecycle" },
    { code: "ISO 13485:2016", title: "Quality Management Systems" },
    { code: "21 CFR Part 820", title: "Quality System Regulation (QSR)" },
  ];
  if (a.regulationSection) {
    stdList.push({ code: a.regulationSection, title: `Device-Specific Regulation (${a.productCode || "TBD"})` });
  }
  stdList.forEach((s, i) => {
    STANDARDS.push({
      id: `STD-${String(i + 1).padStart(2, "0")}`,
      code: s.code,
      title: ls(s.title),
      applies: "All",
      status: "not-started",
      progress: 0,
    });
  });

  // ── TIMELINE EVENTS ───────────────────────────
  clearArray(TIMELINE_EVENTS);
  const tlPoints = [
    { frac: 0, tech: "Project kickoff — design planning", biz: "Project initiated — team mobilization" },
    { frac: 0.15, tech: "Pre-Submission meeting with FDA", biz: "Regulatory alignment — investor confidence checkpoint" },
    { frac: 0.3, tech: "Verification testing begins", biz: "Testing costs ramp — major spend phase" },
    { frac: 0.6, tech: `${submissionLabel} filed with FDA`, biz: "Submission milestone — key investor update" },
    { frac: 0.85, tech: "FDA clearance target", biz: "Clearance — commercial revenue pathway opens" },
    { frac: 1.0, tech: "Commercial launch", biz: "Market entry — ROI realization begins" },
  ];
  tlPoints.forEach((tp) => {
    TIMELINE_EVENTS.push({
      month: Math.round(duration * tp.frac),
      technical: ls(tp.tech),
      business: ls(tp.biz),
      impact: tp.frac === 0 ? "neutral" : tp.frac >= 0.6 ? "critical" : "warning",
    });
  });

  // ── CASH RUNWAY ───────────────────────────────
  const cash = a.cashOnHand || 0;
  const burn = a.monthlyBurn || 0;
  const runway = burn > 0 ? Math.round(cash / burn) : 0;
  Object.assign(CASH_RUNWAY, {
    cashOnHand: cash,
    monthlyBurn: burn,
    runwayMonths: runway,
    currency: a.currency || "USD",
  });
  CASH_RUNWAY.fundingRounds.length = 0;
  if (cash > 0) {
    CASH_RUNWAY.fundingRounds.push({
      id: "FR-001",
      label: ls("Initial Funding"),
      amount: cash,
      date: now,
      status: "received",
    });
  }
  CASH_RUNWAY.burnHistory.length = 0;
  if (burn > 0) {
    CASH_RUNWAY.burnHistory.push({
      month: 0,
      burn,
      note: ls("Project start"),
    });
  }

  // ── STAKEHOLDER INPUTS (empty) ────────────────
  clearArray(STAKEHOLDER_INPUTS);

  // ── CHANGE REQUESTS (empty) ───────────────────
  clearArray(CHANGE_REQUESTS);

  // ── AUDIT LOG (initial entry) ─────────────────
  clearArray(AUDIT_LOG);
  AUDIT_LOG.push({
    id: "AUD-001",
    timestamp: new Date().toISOString(),
    user: "System",
    action: "milestone-status",
    targetId: "PROJECT",
    field: "setup",
    oldValue: "",
    newValue: "initialized",
    detail: `Project "${name}" created via Setup Wizard`,
  });

  // ── DHF DOCUMENTS ─────────────────────────────
  clearArray(DHF_DOCUMENTS);
  const dhfDocs = [
    { code: "DHF-DP", title: "Design Plan", cat: "Design Controls", due: 0 },
    { code: "DHF-DI", title: "Design Inputs", cat: "Design Controls", due: 1 },
    { code: "DHF-DO", title: "Design Outputs", cat: "Design Controls", due: Math.round(duration * 0.25) },
    { code: "DHF-DV", title: "Design Verification Report", cat: "Verification", due: Math.round(duration * 0.35) },
    { code: "DHF-VAL", title: "Design Validation Report", cat: "Validation", due: Math.round(duration * 0.5) },
    { code: "DHF-RA", title: "Risk Analysis (ISO 14971)", cat: "Risk Management", due: Math.round(duration * 0.15) },
    { code: "DHF-SW", title: "Software Documentation (IEC 62304)", cat: "Software", due: Math.round(duration * 0.25) },
    { code: "DHF-BIO", title: "Biocompatibility Report", cat: "Biocompatibility", due: Math.round(duration * 0.4) },
    { code: "DHF-EMC", title: "EMC Test Report (IEC 60601-1-2)", cat: "Testing", due: Math.round(duration * 0.35) },
    { code: "DHF-LBL", title: "Labeling & IFU (21 CFR 801)", cat: "Labeling", due: Math.round(duration * 0.5) },
    { code: "DHF-CL", title: `${submissionLabel} Cover Letter`, cat: "Submission", due: Math.round(duration * 0.55) },
    { code: "DHF-DD", title: "Device Description", cat: "Submission", due: Math.round(duration * 0.5) },
  ];
  dhfDocs.forEach((d, i) => {
    DHF_DOCUMENTS.push({
      id: `DHF-${String(i + 1).padStart(3, "0")}`,
      code: d.code,
      title: ls(d.title),
      category: d.cat,
      owner: d.cat === "Submission" || d.cat === "Labeling" ? "regulatory" : "tech",
      status: "not-started",
      dueMonth: d.due,
      notes: "",
    });
  });

  // ── CAPA LOG (empty) ──────────────────────────
  clearArray(CAPA_LOG);

  // ── ACTION ITEMS ──────────────────────────────
  clearArray(ACTION_ITEMS);
  const leader = a.teamLead || "Project Lead";
  const initialActions = [
    { title: "Define design inputs & user needs", assignee: leader, pri: "high" as const, gate: "G1", due: 1 },
    { title: "Establish quality management system", assignee: leader, pri: "high" as const, gate: null, due: 2 },
    { title: "Conduct initial risk analysis (ISO 14971)", assignee: leader, pri: "high" as const, gate: "G1", due: 2 },
    { title: "Prepare Pre-Submission questions for FDA", assignee: leader, pri: "medium" as const, gate: "G2", due: 1 },
    { title: "Set up design history file structure", assignee: leader, pri: "medium" as const, gate: null, due: 1 },
  ];
  initialActions.forEach((act, i) => {
    ACTION_ITEMS.push({
      id: `ACT-${String(i + 1).padStart(3, "0")}`,
      title: ls(act.title),
      assignee: act.assignee,
      owner: "tech",
      priority: act.pri,
      status: "todo",
      dueDate: offsetDate(now, act.due * 30),
      linkedGate: act.gate,
      notes: "",
    });
  });

  // ── BUDGET CATEGORIES ─────────────────────────
  clearArray(BUDGET_CATEGORIES);
  const budgetItems = [
    "Prototype & Materials",
    "Lab Testing & Validation",
    "Regulatory & Legal",
    "Personnel",
    "Clinical Studies",
    "Equipment & Software",
    "Manufacturing Setup",
    "Travel & Conferences",
  ];
  budgetItems.forEach((label, i) => {
    BUDGET_CATEGORIES.push({
      id: `BUD-${String(i + 1).padStart(3, "0")}`,
      label: ls(label),
      planned: 0,
      actual: 0,
      notes: "",
    });
  });

  // ── TEAM MEMBERS ──────────────────────────────
  clearArray(TEAM_MEMBERS);
  if (leader) {
    TEAM_MEMBERS.push({
      id: "TM-001",
      name: leader,
      role: ls("Project Lead"),
      allocation: [
        { workstream: "Project Management", pct: 40 },
        { workstream: "Regulatory", pct: 30 },
        { workstream: "Engineering", pct: 30 },
      ],
      capacity: 100,
    });
  }

  // ── SUPPLIERS (empty) ─────────────────────────
  clearArray(SUPPLIERS);

  // ── QA SECTIONS ───────────────────────────────
  clearArray(QA_SECTIONS);
  QA_SECTIONS.push(
    {
      num: 1,
      title: ls("Design & Architecture Decisions"),
      context: ls(`Discussion space for ${name} design decisions and technical architecture.`),
      questions: [
        {
          num: 1,
          question: ls("What are the key design decisions that need to be documented?"),
          why: ls("Design decisions must be traceable in the DHF for regulatory review."),
          followUps: [ls("Are there any design constraints from the regulatory pathway?")],
        },
      ],
    },
    {
      num: 2,
      title: ls("Regulatory Strategy"),
      context: ls(`Regulatory pathway planning and FDA interactions for ${name}.`),
      questions: [
        {
          num: 1,
          question: ls("What is the regulatory submission strategy and timeline?"),
          why: ls("Clear regulatory strategy drives the entire project schedule."),
          followUps: [ls("Are there any predicate device concerns?")],
        },
      ],
    },
    {
      num: 3,
      title: ls("Risk Management"),
      context: ls("Risk identification, assessment, and mitigation tracking."),
      questions: [
        {
          num: 1,
          question: ls("What are the top risks to project success?"),
          why: ls("ISO 14971 requires systematic risk management throughout the device lifecycle."),
          followUps: [ls("What mitigation strategies are in place?")],
        },
      ],
    }
  );
}

function offsetDate(base: string, days: number): string {
  const d = new Date(base);
  d.setDate(d.getDate() + days);
  return d.toISOString().slice(0, 10);
}
