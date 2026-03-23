// ============================================================
// Type Definitions — Medical Device Development Control Tower
// ============================================================

export type Lang = "en" | "cn";

export interface LocalizedString {
  en: string;
  cn: string;
}

// ── Project ─────────────────────────────────────
export interface Project {
  name: LocalizedString;
  subtitle: LocalizedString;
  submissionType: string;
  applicant: LocalizedString;
  manufacturer: LocalizedString;
  preparedDate: string;
  currentMonth: number;
}

// ── Milestones & Tracks ─────────────────────────
export type MilestoneStatus = "complete" | "in-progress" | "not-started";
export type Owner = "tech" | "regulatory" | "business";

export interface Milestone {
  id: string;
  month: number;
  title: LocalizedString;
  description: LocalizedString;
  detail?: LocalizedString;
  status: MilestoneStatus;
  owner: Owner;
  category: string;
}

export interface Track {
  label: LocalizedString;
  icon: string;
  milestones: Milestone[];
}

export interface Tracks {
  technical: Track;
  regulatory: Track;
}

// ── Gate System ─────────────────────────────────
export type GateDecision = "proceed" | "more-data" | "stop" | null;
export type GateStatus =
  | "not-started"
  | "pending-review"
  | "approved"
  | "blocked"
  | "needs-data";

export interface GateCriteria extends LocalizedString {
  met: boolean;
}

export interface GateNote {
  date: string;
  text: string;
}

export interface Gate {
  id: string;
  number: number;
  title: LocalizedString;
  month: number;
  status: GateStatus;
  criteria: GateCriteria[];
  decision: GateDecision;
  decisionBy: string | null;
  decisionDate: string | null;
  notes: GateNote[];
  inputBusiness: string[];
  inputTech: string[];
}

// ── Risks ───────────────────────────────────────
export type RiskLevel = "red" | "yellow" | "green";
export type Severity = "high" | "medium" | "low";
export type Probability = "very-low" | "low" | "medium" | "high";
export type MitigationStatus = "complete" | "in-progress" | "not-started";

export interface Risk {
  id: string;
  title: LocalizedString;
  severity: Severity;
  probability: Probability;
  riskLevel: RiskLevel;
  controls: LocalizedString;
  residual: LocalizedString;
  mitigationStatus: MitigationStatus;
  module: string;
  standard: string;
}

// ── Timeline ────────────────────────────────────
export type TimelineImpact = "neutral" | "warning" | "critical";

export interface TimelineEvent {
  month: number;
  technical: LocalizedString;
  business: LocalizedString;
  impact: TimelineImpact;
}

// ── Standards ───────────────────────────────────
export interface Standard {
  id: string;
  code: string;
  title: LocalizedString;
  applies: string;
  status: MilestoneStatus;
  progress: number;
}

// ── Cash / Runway ───────────────────────────────
export interface FundingRound {
  id: string;
  label: LocalizedString;
  amount: number;
  date: string;
  status: "received" | "committed" | "pipeline";
}

export interface MonthlyBurn {
  month: number;
  burn: number;
  note: LocalizedString;
}

export interface CashRunway {
  cashOnHand: number;
  monthlyBurn: number;
  runwayMonths: number;
  fundingRounds: FundingRound[];
  burnHistory: MonthlyBurn[];
  currency: string;
}

// ── Stakeholder Inputs ──────────────────────────
export type InputFrom = "tech" | "business";
export type InputStatus = "pending-review" | "accepted" | "rejected" | "noted";

export interface StakeholderInput {
  id: string;
  from: InputFrom;
  date: string;
  gate: string;
  content: LocalizedString;
  status: InputStatus;
  pmpResponse: LocalizedString | null;
}

// ── Change Requests (PMP Approval Workflow) ─────
export type ChangeRequestType =
  | "milestone-status"
  | "risk-field"
  | "standard-status"
  | "standard-progress"
  | "funding-status";
export type ChangeRequestStatus = "pending" | "approved" | "rejected";

export interface CRDocument {
  name: string;
  size: number;
  key: string;
  type: string;
}

export interface ChangeRequest {
  id: string;
  type: ChangeRequestType;
  from: InputFrom;
  date: string;
  targetId: string;
  field: string;
  oldValue: string;
  newValue: string;
  justification: string;
  evidence: string;
  documents: CRDocument[];
  status: ChangeRequestStatus;
  pmpNote: string | null;
}

// ── Audit Trail ─────────────────────────────────
export type AuditAction =
  | "milestone-status"
  | "risk-field"
  | "gate-decision"
  | "gate-criteria"
  | "standard-status"
  | "standard-progress"
  | "funding-status"
  | "funding-added"
  | "cr-submitted"
  | "cr-approved"
  | "cr-rejected"
  | "gate-note"
  | "action-item"
  | "dhf-status"
  | "capa-status"
  | "budget-entry"
  | "resource-change"
  | "supplier-status"
  | "cash-field";

export interface AuditEntry {
  id: string;
  timestamp: string;
  user: string;
  action: AuditAction;
  targetId: string;
  field: string;
  oldValue: string;
  newValue: string;
  detail: string;
}

// ── DHF Document Tracker ────────────────────────
export type DHFDocStatus = "draft" | "in-review" | "approved" | "not-started";

export interface DHFDocument {
  id: string;
  code: string;
  title: LocalizedString;
  category: string;
  owner: Owner;
  status: DHFDocStatus;
  dueMonth: number;
  notes: string;
}

// ── CAPA Log ────────────────────────────────────
export type CAPAStatus = "open" | "in-progress" | "closed" | "verified";
export type CAPAType = "corrective" | "preventive";

export interface CAPAItem {
  id: string;
  type: CAPAType;
  title: LocalizedString;
  linkedRiskId: string;
  description: LocalizedString;
  owner: string;
  status: CAPAStatus;
  openedDate: string;
  dueDate: string;
  closedDate: string | null;
}

// ── Action Items / Task Board ───────────────────
export type ActionStatus = "todo" | "in-progress" | "done" | "blocked";
export type ActionPriority = "high" | "medium" | "low";

export interface ActionItem {
  id: string;
  title: LocalizedString;
  assignee: string;
  owner: Owner;
  priority: ActionPriority;
  status: ActionStatus;
  dueDate: string;
  linkedGate: string | null;
  notes: string;
}

// ── Budget vs Actual ────────────────────────────
export interface BudgetCategory {
  id: string;
  label: LocalizedString;
  planned: number;
  actual: number;
  notes: string;
}

// ── Resource Allocation ─────────────────────────
export interface TeamMember {
  id: string;
  name: string;
  role: LocalizedString;
  allocation: { workstream: string; pct: number }[];
  capacity: number;
}

// ── Supplier / Vendor Tracker ───────────────────
export type SupplierStatus = "active" | "qualified" | "under-review" | "risk";

export interface Supplier {
  id: string;
  name: string;
  component: LocalizedString;
  status: SupplierStatus;
  leadTimeDays: number;
  poStatus: string;
  contractMfgMilestone: string;
  notes: string;
}

// ── User Roles ──────────────────────────────────
export type UserRole = "pmp" | "tech" | "business" | "accounting";

// ── i18n ────────────────────────────────────────
export type I18nKey = string;
export type I18nDict = Record<I18nKey, string>;
export type I18nMessages = Record<Lang, I18nDict>;

// ── Window augmentation for global handlers ─────
declare global {
  interface Window {
    _openGate: (gateId: string) => void;
    _openMilestone: (trackKey: string, milestoneId: string) => void;
    _toggleCriteria: (gateId: string, index: number) => void;
    _setDecision: (gateId: string, decision: string) => void;
    _addGateNote: (gateId: string) => void;
    _cycleMilestoneStatus: (trackKey: string, milestoneId: string) => void;
    _openRiskEditor: (riskId: string) => void;
    _setRiskField: (riskId: string, field: string, value: string) => void;
    _closeRiskEditor: () => void;
    _cycleStandardStatus: (standardId: string) => void;
    _setStandardProgress: (standardId: string, value: string) => void;
    _editCashField: (field: "cashOnHand" | "monthlyBurn") => void;
    _addFundingRound: () => void;
    _toggleFundingStatus: (roundId: string) => void;
    _submitChangeRequest: (
      type: string,
      targetId: string,
      field: string,
      oldVal: string,
      newVal: string,
    ) => void;
    _approveChangeRequest: (crId: string) => void;
    _rejectChangeRequest: (crId: string) => void;
    _openChangeRequestForm: (
      type: string,
      targetId: string,
      field: string,
      oldVal: string,
    ) => void;
    _closeChangeRequestForm: () => void;
    _setRole: (role: string) => void;
    _downloadDocument: (key: string, filename: string) => void;
    _removeQueuedDocument: (index: number) => void;
    _cycleDHFStatus: (docId: string) => void;
    _cycleCAPAStatus: (capaId: string) => void;
    _cycleActionStatus: (actionId: string) => void;
    _cycleSupplierStatus: (supplierId: string) => void;
    _dismissNotification: (index: number) => void;
    _exportReport: () => void;
    _sendQaMessage: (qNum: number) => void;
    _exportQaThread: () => void;
    _deleteDocLibItem: (id: string) => void;
    _openAddDocForm: () => void;
    _addDocLibItem: () => void;
    _openQaSettings: () => void;
    _saveQaSettings: () => void;
    _markQaRead: (msgId: string) => void;
    _archiveQaMessages: (qNum: number) => void;
    _viewQaArchive: () => void;
    _closeQaArchive: () => void;
    _deleteQaArchive: (idx: number) => void;
    _logStakeholderInput: () => void;
  }
}

// ── Document Library ────────────────────────────
export interface DocLibItem {
  id: string;
  cat: string;
  name: LocalizedString;
  version: string;
  date: string;
  owner: string;
  status: string;
}

// ── Inventor Q&A ────────────────────────────────
export interface QASection {
  num: number;
  title: LocalizedString;
  context: LocalizedString;
  questions: QAQuestion[];
}

export interface QAQuestion {
  num: number;
  question: LocalizedString;
  why?: LocalizedString;
  followUps?: LocalizedString[];
}

export interface QAMessage {
  id: string;
  qNum: number;
  sender: "pmp" | "inventor";
  text: string;
  timestamp: string;
  readBy?: string[];
}

export interface QASettings {
  pmpEmail: string;
  inventorEmail: string;
}
