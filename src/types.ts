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
export interface StandardClause {
  id: string;
  clause: string;
  title: LocalizedString;
  checked: boolean;
  evidenceDoc?: string;
}

export interface Standard {
  id: string;
  code: string;
  title: LocalizedString;
  applies: string;
  status: MilestoneStatus;
  progress: number;
  clauses: StandardClause[];
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
  | "funding-status"
  | "action-status"
  | "dhf-status"
  | "capa-status"
  | "supplier-status";
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
  | "cash-field"
  | "doc-status"
  | "api-remove"
  | "api-restore"
  | "budget-field"
  | "budget-add"
  | "budget-delete"
  | "supplier-add"
  | "supplier-delete"
  | "burn-edit"
  | "burn-add"
  | "burn-delete"
  | "qa-topic"
  | "investor-add"
  | "investor-delete"
  | "investor-status"
  | "ir-activity-add"
  | "ir-activity-delete"
  | "ir-activity-status"
  | "shareholder-add"
  | "shareholder-delete"
  | "equity-event-add"
  | "equity-event-delete"
  | "equity-event-status"
  | "vesting-add"
  | "vesting-delete"
  | "vesting-status"
  | "team-add"
  | "team-delete";

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
  email?: string;
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
    _removeApiIntegration: (apiKey: string) => void;
    _restoreApiIntegrations: () => void;
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
    _sendQaMessage: (threadId: number) => void;
    _exportQaThread: () => void;
    _deleteDocLibItem: (id: string) => void;
    _openAddDocForm: () => void;
    _addDocLibItem: () => void;
    _cycleDocStatus: (id: string) => void;
    _openDocHistory: (id: string) => void;
    _closeDocHistory: () => void;
    _openQaSettings: () => void;
    _saveQaSettings: () => void;
    _markQaRead: (msgId: string) => void;
    _archiveQaMessages: (threadId: number) => void;
    _viewQaArchive: () => void;
    _closeQaArchive: () => void;
    _deleteQaArchive: (idx: number) => void;
    _autoMarkVisibleAsRead: () => void;
    _logStakeholderInput: () => void;
    _editBudgetField: (budgetId: string, field: "planned" | "actual") => void;
    _createQaTopic: () => void;
    _deleteQaTopic: (threadId: number) => void;
    _mbCreateThread: () => void;
    _mbResolveThread: (threadId: number) => void;
    _mbReopenThread: (threadId: number) => void;
    _mbDeleteThread: (threadId: number) => void;
    _mbSetView: (view: string) => void;
    _mbSetWorkstreamFilter: (ws: string) => void;
    _mbLogDecision: (threadId: number) => void;
    _mbCreateAction: (threadId: number) => void;
    _mbToggleActionStatus: (threadId: number) => void;
    _mbLinkItem: (threadId: number) => void;
    _addSupplier: () => void;
    _deleteSupplier: (supplierId: string) => void;
    _openAddSupplierForm: () => void;
    _addBudgetCategory: () => void;
    _deleteBudgetCategory: (budgetId: string) => void;
    _openAddBudgetForm: () => void;
    _editBurnEntry: (month: number) => void;
    _addBurnEntry: () => void;
    _deleteBurnEntry: (month: number) => void;
    _toggleQaTestMode: (checked: boolean) => void;
    _toggleStandardClauses: (standardId: string) => void;
    _toggleClause: (standardId: string, clauseId: string) => void;
    _openAddInvestorForm: () => void;
    _addInvestor: () => void;
    _deleteInvestor: (investorId: string) => void;
    _cycleInvestorStatus: (investorId: string) => void;
    _openAddIRActivityForm: () => void;
    _addIRActivity: () => void;
    _deleteIRActivity: (activityId: string) => void;
    _cycleIRActivityStatus: (activityId: string) => void;
    _openAddShareholderForm: () => void;
    _addShareholder: () => void;
    _deleteShareholder: (shareholderId: string) => void;
    _openAddEquityEventForm: () => void;
    _addEquityEvent: () => void;
    _deleteEquityEvent: (eventId: string) => void;
    _cycleEquityEventStatus: (eventId: string) => void;
    _openAddVestingForm: () => void;
    _addVesting: () => void;
    _deleteVesting: (vestingId: string) => void;
    _cycleVestingStatus: (vestingId: string) => void;
    _openAddTeamMemberForm: () => void;
    _addTeamMember: () => void;
    _deleteTeamMember: (tmId: string) => void;
  }
}

// ── Document Control ────────────────────────────
export type DocStatus =
  | "draft"
  | "in-review"
  | "approved"
  | "effective"
  | "obsolete";

export interface DocRevision {
  rev: string;
  date: string;
  author: string;
  change: LocalizedString;
}

export interface DocLibItem {
  id: string;
  dcn: string;
  cat: string;
  name: LocalizedString;
  version: string;
  date: string;
  owner: string;
  status: DocStatus;
  effectiveDate: string;
  nextReview: string;
  linkedMilestone: string;
  sourceRef?: string;
  revisions: DocRevision[];
}

// ── Message Board ────────────────────────────────
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
  sender: string;
  text: string;
  timestamp: string;
  readBy?: string[];
}

export interface QASettings {
  pmpEmail: string;
  technologyEmail: string;
  businessEmail: string;
  accountingEmail: string;
}

// ── Message Board v2 — Purpose-Driven Threads ────
export type MBWorkstream =
  | "project"
  | "regulatory"
  | "engineering"
  | "clinical"
  | "business"
  | "operations";
export type MBMessageIntent = "inform" | "decide" | "act";
export type MBThreadLifecycle = "open" | "resolved" | "archived";
export type MBPriority = "normal" | "urgent" | "escalated";
export type MBActionStatus = "open" | "blocked" | "done";

export interface MBLinkedItem {
  type: "milestone" | "risk" | "task" | "document" | "gate" | "standard";
  id: string;
  label: string;
}

export interface MBThread {
  id: number;
  title: string;
  workstream: MBWorkstream;
  intent: MBMessageIntent;
  owner: string;
  objective: string;
  lifecycle: MBThreadLifecycle;
  priority: MBPriority;
  assignee?: string;
  dueDate?: string;
  linkedItems: MBLinkedItem[];
  sourceRef?: string;
  createdAt: string;
  resolvedAt?: string;
  resolutionSummary?: string;
}

export interface MBDecision {
  id: string;
  threadId: number;
  text: string;
  rationale: string;
  madeBy: string;
  date: string;
  linkedItems: MBLinkedItem[];
  status: "active" | "superseded";
}

export type MBView =
  | "all"
  | "my-items"
  | "decisions"
  | "executive"
  | "workstream";

// ── US Investment & Investor Relations ──────────
export type InvestorContactStatus =
  | "prospect"
  | "contacted"
  | "in-dd"
  | "term-sheet"
  | "closed"
  | "passed";

export type IRActivityStatus = "done" | "in-progress" | "todo";

export interface TargetInvestor {
  id: string;
  name: string;
  type: string;
  stage: string;
  contact: InvestorContactStatus;
  amount: number;
  notes: string;
}

export interface IRActivity {
  id: string;
  date: string;
  activity: string;
  status: IRActivityStatus;
}

// ── Cap Table Management ────────────────────────

export type ShareClass =
  | "common"
  | "preferred-seed"
  | "preferred-a"
  | "safe"
  | "options";

export type EquityEventStatus = "issued" | "pending" | "converted";

export type VestingStatus = "vesting" | "fully-vested" | "cancelled";

export interface Shareholder {
  id: string;
  name: string;
  role: string;
  shareClass: ShareClass;
  shares: number;
  notes: string;
}

export interface EquityEvent {
  id: string;
  date: string;
  event: string;
  shareClass: ShareClass;
  shares: number;
  pricePerShare: number;
  totalValue: number;
  status: EquityEventStatus;
  notes: string;
}

export interface VestingSchedule {
  id: string;
  holder: string;
  shares: number;
  startDate: string;
  cliffMonths: number;
  totalMonths: number;
  vestedShares: number;
  status: VestingStatus;
  notes: string;
}
