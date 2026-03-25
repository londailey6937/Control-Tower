// ============================================================
// APP.TS — Medical Device Development Control Tower
// Dashboard logic, rendering, and interactivity
// ============================================================

import {
  PROJECT,
  TRACKS,
  GATES,
  RISKS,
  STANDARDS,
  TIMELINE_EVENTS,
  STAKEHOLDER_INPUTS,
  CASH_RUNWAY,
  CHANGE_REQUESTS,
  ACTIVE_ROLE,
  setActiveRole,
  AUDIT_LOG,
  DHF_DOCUMENTS,
  CAPA_LOG,
  ACTION_ITEMS,
  BUDGET_CATEGORIES,
  TEAM_MEMBERS,
  SUPPLIERS,
  QA_SECTIONS,
} from "./data.ts";
import { t, localizedText, getLang, setLang, applyLanguage } from "./i18n.ts";
import type {
  Gate,
  Milestone,
  ChangeRequest,
  CRDocument,
  UserRole,
  AuditEntry,
  DocLibItem,
  DocStatus,
  QAMessage,
  QASettings,
  MBThread,
  MBDecision,
  MBView,
  MBWorkstream,
  MBMessageIntent,
  MBLinkedItem,
  MBPriority,
} from "./types.ts";
import { storeDocument, getDocument } from "./docstore.ts";
import {
  isOnline,
  fetchMessages,
  insertMessage,
  markMessageRead,
  deleteMessages,
  subscribeMessages,
  fetchAuditLog,
  insertAuditEntry,
  insertAuditBatch,
  type DbMessage,
  type DbAuditEntry,
} from "./supabase.ts";

// ── STATE ─────────────────────────────────────
const USD_CNY_RATE = 7.25;
function fmtCurrency(n: number): string {
  const isCN = getLang() === "cn";
  const converted = isCN ? Math.round(n * USD_CNY_RATE) : n;
  return t("currencySymbol") + converted.toLocaleString();
}

let activeTab = "dual-track";
let activeRiskFilter = "all";
let crQueuedFiles: File[] = [];
let dismissedNotifs: Set<string> = new Set();

const CR_STORAGE_KEY = "ctower_change_requests";
const INPUT_STORAGE_KEY = "ctower_stakeholder_inputs";
const AUDIT_QUEUE_KEY = "ctower_audit_queue";

function loadCRs(): void {
  try {
    const raw = localStorage.getItem(CR_STORAGE_KEY);
    if (raw) {
      const parsed = JSON.parse(raw) as ChangeRequest[];
      CHANGE_REQUESTS.length = 0;
      parsed.forEach((cr) => CHANGE_REQUESTS.push(cr));
    }
  } catch {
    /* ignore corrupt data */
  }
}

function saveCRs(): void {
  localStorage.setItem(CR_STORAGE_KEY, JSON.stringify(CHANGE_REQUESTS));
}

function loadInputs(): void {
  try {
    const raw = localStorage.getItem(INPUT_STORAGE_KEY);
    if (raw) {
      const parsed = JSON.parse(raw) as typeof STAKEHOLDER_INPUTS;
      STAKEHOLDER_INPUTS.length = 0;
      parsed.forEach((inp) => STAKEHOLDER_INPUTS.push(inp));
    }
  } catch {
    /* ignore corrupt data */
  }
}

function saveInputs(): void {
  localStorage.setItem(INPUT_STORAGE_KEY, JSON.stringify(STAKEHOLDER_INPUTS));
}

// ── GLOBAL EVENT DELEGATION ────────────────────
// Replaces inline onclick/onchange with data-action/data-change attributes
function setupEventDelegation(): void {
  document.addEventListener("click", (e) => {
    const el = (e.target as HTMLElement).closest<HTMLElement>("[data-action]");
    if (!el) return;
    const a = el.dataset;
    switch (a.action) {
      case "openMilestone":
        window._openMilestone(a.track!, a.mid!);
        break;
      case "cycleMilestoneStatus":
        e.stopPropagation();
        window._cycleMilestoneStatus(a.track!, a.mid!);
        break;
      case "openGate":
        window._openGate(a.gid!);
        break;
      case "toggleCriteria":
        e.stopPropagation();
        window._toggleCriteria(a.gid!, Number(a.ci));
        break;
      case "setDecision":
        window._setDecision(a.gid!, a.decision!);
        break;
      case "addGateNote":
        window._addGateNote(a.gid!);
        break;
      case "openRiskEditor":
        window._openRiskEditor(a.rid!);
        break;
      case "cycleStandardStatus":
        window._cycleStandardStatus(a.sid!);
        break;
      case "editCashField":
        window._editCashField(a.field! as "cashOnHand" | "monthlyBurn");
        break;
      case "editBudgetField":
        window._editBudgetField(a.budgetid!, a.field! as "planned" | "actual");
        break;
      case "toggleFundingStatus":
        window._toggleFundingStatus(a.frid!);
        break;
      case "addFundingRound":
        window._addFundingRound();
        break;
      case "removeApiIntegration":
        window._removeApiIntegration(a.apikey!);
        break;
      case "restoreApiIntegrations":
        window._restoreApiIntegrations();
        break;
      case "closeRiskEditor":
        window._closeRiskEditor();
        break;
      case "closeChangeRequestForm":
        window._closeChangeRequestForm();
        break;
      case "submitChangeRequest": {
        const val =
          (document.getElementById("crNewValue") as HTMLInputElement)?.value ??
          "";
        window._submitChangeRequest(
          a.crtype!,
          a.crtarget!,
          a.crfield!,
          a.crold!,
          val,
        );
        break;
      }
      case "removeQueuedDocument":
        window._removeQueuedDocument(Number(a.idx!));
        break;
      case "approveChangeRequest":
        window._approveChangeRequest(a.crid!);
        break;
      case "rejectChangeRequest":
        window._rejectChangeRequest(a.crid!);
        break;
      case "downloadDocument":
        e.preventDefault();
        window._downloadDocument(a.dkey!, a.dname!);
        break;
      case "cycleActionStatus":
        window._cycleActionStatus(a.aid!);
        break;
      case "cycleDHFStatus":
        window._cycleDHFStatus(a.did!);
        break;
      case "cycleCAPAStatus":
        window._cycleCAPAStatus(a.cid!);
        break;
      case "cycleSupplierStatus":
        window._cycleSupplierStatus(a.supid!);
        break;
      case "dismissNotification":
        window._dismissNotification(Number(a.nidx!));
        break;
      case "exportReport":
        window._exportReport();
        break;
      case "logStakeholderInput":
        window._logStakeholderInput();
        break;
      case "editBurnEntry":
        window._editBurnEntry(Number(a.burnmonth!));
        break;
      case "addBurnEntry":
        window._addBurnEntry();
        break;
      case "deleteBurnEntry":
        window._deleteBurnEntry(Number(a.burnmonth!));
        break;
      case "addSupplier":
        window._addSupplier();
        break;
      case "deleteSupplier":
        window._deleteSupplier(a.supid!);
        break;
      case "openAddSupplierForm":
        window._openAddSupplierForm();
        break;
      case "addBudgetCategory":
        window._addBudgetCategory();
        break;
      case "deleteBudgetCategory":
        window._deleteBudgetCategory(a.budgetid!);
        break;
      case "openAddBudgetForm":
        window._openAddBudgetForm();
        break;
    }
  });
  document.addEventListener("change", (e) => {
    const el = e.target as HTMLElement;
    if (!el.dataset.change) return;
    const val = (el as HTMLInputElement | HTMLSelectElement).value;
    switch (el.dataset.change) {
      case "setStandardProgress":
        window._setStandardProgress(el.dataset.sid!, val);
        break;
      case "setRiskField":
        window._setRiskField(el.dataset.rid!, el.dataset.rfield!, val);
        break;
    }
  });
}

// ── INIT ──────────────────────────────────────
document.addEventListener("DOMContentLoaded", () => {
  setupEventDelegation();
  loadCRs();
  loadInputs();
  initTabs();
  initLangToggle();
  initFab();
  initRoleSwitcher();
  applyLanguage(getLang());

  // Bootstrap Supabase data, then render
  Promise.all([initQaMessages(), initAuditLog()]).then(() => {
    renderAll();
    setupRealtimeMessages();
  });

  // When connection restored, flush queued audit entries
  window.addEventListener("online", () => {
    flushAuditQueue().then(() => {
      initAuditLog().then(renderAuditTrail);
    });
  });
});

// ── TAB NAVIGATION ────────────────────────────
function initTabs(): void {
  document.querySelectorAll<HTMLButtonElement>(".tab-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      const tab = btn.dataset.tab;
      if (!tab || tab === activeTab) return;
      activeTab = tab;

      document
        .querySelectorAll(".tab-btn")
        .forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");

      document
        .querySelectorAll(".tab-panel")
        .forEach((p) => p.classList.remove("active"));
      const panel = document.getElementById("panel-" + tab);
      if (panel) panel.classList.add("active");
    });
  });
}

// ── LANGUAGE TOGGLE ───────────────────────────
function initLangToggle(): void {
  const btn = document.getElementById("langToggle")!;
  const label = document.getElementById("langLabel")!;
  function updateLangBtn(lang: "en" | "cn"): void {
    label.textContent = lang === "en" ? "EN" : "中";
    btn.title =
      lang === "en"
        ? "Switch to Chinese / 切换中文"
        : "Switch to English / 切换英文";
  }
  updateLangBtn(getLang());
  btn.addEventListener("click", () => {
    const newLang = getLang() === "en" ? ("cn" as const) : ("en" as const);
    setLang(newLang);
    updateLangBtn(newLang);
    applyLanguage(newLang);
    renderAll();
  });
}

// ── FAB / INPUT PANEL ─────────────────────────
function initFab(): void {
  const fab = document.getElementById("fabInputs")!;
  const overlay = document.getElementById("inputPanelOverlay")!;
  const closeBtn = document.getElementById("inputPanelClose")!;

  fab.addEventListener("click", () => {
    renderInputPanel();
    overlay.classList.add("open");
  });
  closeBtn.addEventListener("click", () => overlay.classList.remove("open"));
  overlay.addEventListener("click", (e) => {
    if (e.target === overlay) overlay.classList.remove("open");
  });
}

// ── RENDER ALL ────────────────────────────────
function renderAll(): void {
  applyRoleRestrictions();
  renderSummary();
  renderDualTrack();
  renderGates();
  renderRisks();
  renderTimeline();
  renderStandards();
  renderCashRunway();
  renderApiIntegrations();
  renderUsApiIntegrations();
  renderActionBoard();
  renderDHFTable();
  renderCAPALog();
  renderBudget();
  renderResources();
  renderSuppliers();
  renderAuditTrail();
  renderUsInvestment();
  renderDocLibrary();
  renderQaSheet();
  renderNotifications();
  updateFabBadge();
}

// ── SUMMARY BAR ───────────────────────────────
function renderSummary(): void {
  const redCount = RISKS.filter((r) => r.riskLevel === "red").length;
  document.getElementById("redRiskCount")!.textContent = String(redCount);

  const pending = STAKEHOLDER_INPUTS.filter(
    (i) => i.status === "pending-review",
  ).length;
  document.getElementById("pendingInputCount")!.textContent = String(pending);

  const nextGate = GATES.find(
    (g) =>
      g.status !== "approved" &&
      g.decision !== "proceed" &&
      !g.criteria.every((c) => c.met),
  );
  if (nextGate) {
    document.getElementById("nextGate")!.textContent =
      "G" + nextGate.number + " (M+" + nextGate.month + ")";
  }

  const statusEl = document.getElementById("overallStatus")!;
  if (redCount >= 3) {
    statusEl.textContent = t("statusBlocked");
    statusEl.className = "summary-value status-blocked";
  } else if (redCount >= 1) {
    statusEl.textContent = t("statusAtRisk");
    statusEl.className = "summary-value status-at-risk";
  } else {
    statusEl.textContent = t("statusOnTrack");
    statusEl.className = "summary-value status-on-track";
  }

  const currentM = PROJECT.currentMonth;
  const allMilestones = [
    ...TRACKS.technical.milestones,
    ...TRACKS.regulatory.milestones,
  ].filter((m) => m.month > currentM && m.status !== "complete");
  allMilestones.sort((a, b) => a.month - b.month);
  if (allMilestones.length > 0) {
    const monthsAway = allMilestones[0].month - currentM;
    document.getElementById("daysToMilestone")!.textContent =
      "~" + monthsAway * 30 + "d";
  }

  document.getElementById("currentMonthNum")!.textContent = String(currentM);

  // Runway in summary bar
  const runwayEl = document.getElementById("summaryRunway")!;
  runwayEl.textContent = CASH_RUNWAY.runwayMonths + " " + t("runwayMonths");
  runwayEl.className =
    "summary-value " +
    (CASH_RUNWAY.runwayMonths <= 3
      ? "runway-critical"
      : CASH_RUNWAY.runwayMonths <= 6
        ? "runway-warning"
        : "runway-ok");
}

// ── DUAL-TRACK DASHBOARD ──────────────────────
function renderDualTrack(): void {
  const techContainer = document.getElementById("techMilestones")!;
  const regContainer = document.getElementById("regMilestones")!;
  const timelineContainer = document.getElementById("centerTimeline")!;

  const techItems = [...TRACKS.technical.milestones].sort(
    (a, b) => a.month - b.month,
  );
  const regItems = [...TRACKS.regulatory.milestones].sort(
    (a, b) => a.month - b.month,
  );

  techContainer.innerHTML = techItems.map((m) => milestoneCard(m)).join("");
  regContainer.innerHTML = regItems.map((m) => milestoneCard(m)).join("");

  const allMonths = new Set([
    ...techItems.map((m) => m.month),
    ...regItems.map((m) => m.month),
  ]);
  const sortedMonths = [...allMonths].sort((a, b) => a - b);
  timelineContainer.innerHTML = sortedMonths
    .map((month, i) => {
      const isActive = month <= PROJECT.currentMonth;
      return `
        <div class="timeline-dot ${isActive ? "active" : ""}" title="M+${month}"></div>
        ${i < sortedMonths.length - 1 ? '<div class="timeline-line"></div>' : ""}
      `;
    })
    .join("");
}

function milestoneCard(m: Milestone): string {
  const statusClass = "status-" + m.status.replace(" ", "-");
  const badgeClass =
    m.status === "complete"
      ? "badge-complete"
      : m.status === "in-progress"
        ? "badge-in-progress"
        : "badge-not-started";
  const statusText =
    m.status === "complete"
      ? t("complete")
      : m.status === "in-progress"
        ? t("inProgress")
        : t("notStarted");

  // Determine which track this milestone belongs to
  const trackKey = TRACKS.technical.milestones.some((tm) => tm.id === m.id)
    ? "technical"
    : "regulatory";

  return `
    <div class="milestone-card ${statusClass}" data-action="openMilestone" data-track="${trackKey}" data-mid="${m.id}" style="cursor:pointer;">
      <div class="ms-header">
        <span class="ms-id" style="font-weight:700;color:#6366f1;margin-right:4px;">${m.id}</span>
        <span class="ms-title">${localizedText(m.title)}</span>
        <span class="ms-month">M+${m.month}</span>
      </div>
      <div class="ms-desc">${localizedText(m.description)}</div>
      <span class="ms-status-badge ${badgeClass} clickable-badge"
            data-action="cycleMilestoneStatus" data-track="${trackKey}" data-mid="${m.id}"
            title="${ACTIVE_ROLE === "pmp" ? t("clickToChangeStatus") : t("clickToSubmitCR")}">
        ${statusText}
      </span>
    </div>
  `;
}

// ── GATE SYSTEM ───────────────────────────────
function renderGates(): void {
  const container = document.getElementById("gatesPipeline")!;
  const items: string[] = [];

  GATES.forEach((gate, i) => {
    const metCount = gate.criteria.filter((c) => c.met).length;
    const totalCount = gate.criteria.length;
    const pct = totalCount > 0 ? Math.round((metCount / totalCount) * 100) : 0;

    let gateClass = "gate-not-started";
    if (gate.decision === "proceed") gateClass = "gate-approved";
    else if (gate.decision === "stop") gateClass = "gate-blocked";
    else if (gate.status === "pending-review" || gate.decision === "more-data")
      gateClass = "gate-pending";

    items.push(`
      <div class="gate-card ${gateClass}" data-gate-id="${gate.id}" data-action="openGate" data-gid="${gate.id}" style="cursor:pointer">
        <div class="gate-top">
          <div class="gate-number">G${gate.number}</div>
          <div class="gate-title">${localizedText(gate.title)}</div>
          <div class="gate-month">${t("gateMonthPrefix")}${gate.month}</div>
        </div>
        <div class="gate-status-strip"></div>
        <div class="gate-criteria-summary">
          <div class="criteria-progress">
            <span>${metCount}/${totalCount} ${t("gateCriteriaMet")}</span>
            <div class="criteria-bar">
              <div class="criteria-bar-fill" style="width:${pct}%"></div>
            </div>
          </div>
        </div>
      </div>
    `);

    if (i < GATES.length - 1) {
      items.push(`<div class="gate-connector">→</div>`);
    }
  });

  container.innerHTML = items.join("");
}

// Gate detail modal
window._openGate = function (gateId: string): void {
  const gate = GATES.find((g) => g.id === gateId);
  if (!gate) return;

  const overlay = document.getElementById("gateDetailOverlay")!;
  const content = document.getElementById("gateDetailContent")!;

  const metCount = gate.criteria.filter((c) => c.met).length;

  const criteriaHtml = gate.criteria
    .map(
      (c, ci) => `
      <li class="criteria-item">
        <div class="criteria-check ${c.met ? "checked" : ""}"
             data-action="toggleCriteria" data-gid="${gateId}" data-ci="${ci}">
          ${c.met ? "✓" : ""}
        </div>
        <span>${localizedText(c)}</span>
      </li>
    `,
    )
    .join("");

  const relatedInputs = STAKEHOLDER_INPUTS.filter((inp) => inp.gate === gateId);
  const inputsHtml =
    relatedInputs.length > 0
      ? relatedInputs
          .map((inp) => {
            const fromClass =
              inp.from === "tech" ? "from-tech" : "from-business";
            const fromLabel =
              inp.from === "tech" ? t("inputFromTech") : t("inputFromBusiness");
            const statusBadge =
              inp.status === "pending-review"
                ? `<span class="input-status-badge input-status-pending">${t("pendingReview")}</span>`
                : `<span class="input-status-badge input-status-accepted">${t("accepted")}</span>`;

            let responseHtml = "";
            if (inp.pmpResponse) {
              responseHtml = `<div class="pmp-response">${localizedText(inp.pmpResponse)}</div>`;
            }

            return `
              <div class="input-entry ${fromClass}">
                <div class="input-meta">${fromLabel} · ${inp.date} ${statusBadge}</div>
                <div>${localizedText(inp.content)}</div>
                ${responseHtml}
              </div>
            `;
          })
          .join("")
      : `<p style="color:var(--text-muted);font-size:0.8rem;">No inputs yet.</p>`;

  const proceedSel = gate.decision === "proceed" ? "selected" : "";
  const dataSel = gate.decision === "more-data" ? "selected" : "";
  const stopSel = gate.decision === "stop" ? "selected" : "";

  content.innerHTML = `
    <div class="gate-detail-header">
      <h2>G${gate.number} — ${localizedText(gate.title)}</h2>
      <div class="gate-detail-meta">${t("gateMonthPrefix")}${gate.month} · ${metCount}/${gate.criteria.length} ${t("gateCriteriaMet")}</div>
    </div>

    <ul class="criteria-list">${criteriaHtml}</ul>

    <div class="gate-decision-section">
      <h4>${t("gateDecisionTitle")}</h4>
      <div class="decision-buttons">
        <button class="decision-btn btn-proceed ${proceedSel}" data-action="setDecision" data-gid="${gateId}" data-decision="proceed">${t("gateProceed")}</button>
        <button class="decision-btn btn-data ${dataSel}" data-action="setDecision" data-gid="${gateId}" data-decision="more-data">${t("gateNeedData")}</button>
        <button class="decision-btn btn-stop ${stopSel}" data-action="setDecision" data-gid="${gateId}" data-decision="stop">${t("gateStop")}</button>
      </div>
    </div>

    <div class="gate-inputs-section">
      <h4>${t("gateInputsTitle")}</h4>
      ${inputsHtml}
    </div>

    <div class="gate-inputs-section">
      <h4>${t("gateNotesTitle")}</h4>
      ${gate.notes.map((n) => `<div class="input-entry from-tech"><div class="input-meta">PMP · ${n.date}</div>${n.text}</div>`).join("")}
      <div class="add-note-area">
        <textarea id="gateNoteInput" placeholder="${t("addNotePlaceholder")}"></textarea>
        <button data-action="addGateNote" data-gid="${gateId}">${t("addNoteBtn")}</button>
      </div>
    </div>
  `;

  overlay.classList.add("open");
  document.getElementById("gateModalClose")!.onclick = () =>
    overlay.classList.remove("open");
  overlay.onclick = (e) => {
    if (e.target === overlay) overlay.classList.remove("open");
  };
};

window._toggleCriteria = function (gateId: string, index: number): void {
  const gate = GATES.find((g) => g.id === gateId);
  if (!gate) return;
  const old = String(gate.criteria[index].met);
  gate.criteria[index].met = !gate.criteria[index].met;
  logAudit(
    "gate-criteria",
    gateId,
    `criteria[${index}].met`,
    old,
    String(gate.criteria[index].met),
    "Gate criteria toggled",
  );
  renderGates();
  renderSummary();
  window._openGate(gateId);
};

window._setDecision = function (gateId: string, decision: string): void {
  const gate = GATES.find((g) => g.id === gateId);
  if (!gate) return;
  const old = String(gate.decision);
  gate.decision = decision as Gate["decision"];
  gate.decisionBy = "PMP";
  gate.decisionDate = new Date().toISOString().split("T")[0];
  logAudit(
    "gate-decision",
    gateId,
    "decision",
    old,
    decision,
    `Gate G${gate.number} decision set`,
  );
  renderGates();
  renderSummary();
  window._openGate(gateId);
};

window._addGateNote = function (gateId: string): void {
  const gate = GATES.find((g) => g.id === gateId);
  const input = document.getElementById(
    "gateNoteInput",
  ) as HTMLTextAreaElement | null;
  if (!gate || !input || !input.value.trim()) return;
  gate.notes.push({
    date: new Date().toISOString().split("T")[0],
    text: input.value.trim(),
  });
  window._openGate(gateId);
};

// ── MILESTONE DETAIL MODAL ────────────────────
window._openMilestone = function (trackKey: string, milestoneId: string): void {
  const track = trackKey === "technical" ? TRACKS.technical : TRACKS.regulatory;
  const milestone = track.milestones.find((m) => m.id === milestoneId);
  if (!milestone) return;

  const overlay = document.getElementById("milestoneDetailOverlay")!;
  const content = document.getElementById("milestoneDetailContent")!;

  const statusLabel =
    milestone.status === "complete"
      ? t("complete")
      : milestone.status === "in-progress"
        ? t("inProgress")
        : t("notStarted");
  const badgeClass =
    milestone.status === "complete"
      ? "badge-complete"
      : milestone.status === "in-progress"
        ? "badge-in-progress"
        : "badge-not-started";
  const trackLabel =
    trackKey === "technical"
      ? "🔬 " + t("techTrackTitle")
      : "📋 " + t("regTrackTitle");

  const detailHtml = milestone.detail
    ? localizedText(milestone.detail)
        .split("\n\n")
        .map((para) => {
          if (para.includes("\n- ")) {
            const parts = para.split("\n- ");
            const intro = parts[0] ? `<p>${parts[0]}</p>` : "";
            const items = parts
              .slice(1)
              .map((item) => `<li>${item}</li>`)
              .join("");
            return `${intro}<ul>${items}</ul>`;
          }
          return `<p>${para}</p>`;
        })
        .join("")
    : `<p style="color:var(--text-muted);">${localizedText(milestone.description)}</p>`;

  content.innerHTML = `
    <div class="gate-detail-header">
      <h2>${milestone.id} — ${localizedText(milestone.title)}</h2>
      <div class="gate-detail-meta">${trackLabel} · M+${milestone.month} · <span class="ms-status-badge ${badgeClass}" style="font-size:0.75rem;">${statusLabel}</span></div>
    </div>
    <div class="milestone-detail-body">${detailHtml}</div>
  `;

  overlay.classList.add("open");
  document.getElementById("milestoneModalClose")!.onclick = () =>
    overlay.classList.remove("open");
  overlay.onclick = (e) => {
    if (e.target === overlay) overlay.classList.remove("open");
  };
};

// ── MILESTONE STATUS CYCLING ──────────────────
window._cycleMilestoneStatus = function (
  trackKey: string,
  milestoneId: string,
): void {
  const track = trackKey === "technical" ? TRACKS.technical : TRACKS.regulatory;
  const milestone = track.milestones.find((m) => m.id === milestoneId);
  if (!milestone) return;

  const cycle: Record<string, "in-progress" | "complete" | "not-started"> = {
    "not-started": "in-progress",
    "in-progress": "complete",
    complete: "not-started",
  };
  const newStatus = cycle[milestone.status];

  // Non-PMP roles must submit a change request
  if (ACTIVE_ROLE !== "pmp") {
    window._openChangeRequestForm(
      "milestone-status",
      milestoneId,
      "status",
      milestone.status,
    );
    return;
  }

  milestone.status = newStatus;
  logAudit(
    "milestone-status",
    milestoneId,
    "status",
    milestone.status === "in-progress"
      ? "not-started"
      : milestone.status === "complete"
        ? "in-progress"
        : "complete",
    newStatus,
    `Milestone ${milestoneId} status changed`,
  );
  renderAll();
};

// ── RISK DASHBOARD ────────────────────────────
function renderRisks(): void {
  document.querySelectorAll<HTMLButtonElement>(".filter-btn").forEach((btn) => {
    btn.classList.toggle("active", btn.dataset.filter === activeRiskFilter);
    btn.onclick = () => {
      activeRiskFilter = btn.dataset.filter || "all";
      renderRisks();
    };
  });

  const filtered =
    activeRiskFilter === "all"
      ? RISKS
      : RISKS.filter((r) => r.riskLevel === activeRiskFilter);

  const grid = document.getElementById("riskGrid")!;
  grid.innerHTML = filtered
    .map((r) => {
      const mitigationClass =
        "mitigation-" + r.mitigationStatus.replace(" ", "-");
      const mitigationText =
        r.mitigationStatus === "complete"
          ? t("complete")
          : r.mitigationStatus === "in-progress"
            ? t("inProgress")
            : t("notStarted");
      return `
        <div class="risk-card risk-level-${r.riskLevel}" data-action="openRiskEditor" data-rid="${r.id}" style="cursor:pointer">
          <div class="risk-card-header">
            <span class="risk-id">${r.id}</span>
            <span class="risk-level-badge badge-${r.riskLevel}">${r.riskLevel.toUpperCase()}</span>
          </div>
          <div class="risk-title">${localizedText(r.title)}</div>
          <div class="risk-detail-row">
            <span class="risk-detail-label">${t("riskSeverity")}:</span>
            <span>${capitalize(r.severity)}</span>
          </div>
          <div class="risk-detail-row">
            <span class="risk-detail-label">${t("riskProbability")}:</span>
            <span>${capitalize(r.probability)}</span>
          </div>
          <div class="risk-detail-row">
            <span class="risk-detail-label">${t("riskModule")}:</span>
            <span>${r.module}</span>
          </div>
          <div class="risk-detail-row">
            <span class="risk-detail-label">${t("riskControls")}:</span>
            <span>${localizedText(r.controls)}</span>
          </div>
          <div class="risk-mitigation-bar ${mitigationClass}">
            <span>${t("riskMitigation")}: ${mitigationText}</span>
            <div class="mitigation-bar"><div class="mitigation-bar-fill"></div></div>
          </div>
        </div>
      `;
    })
    .join("");

  const sorted = [...RISKS].sort((a, b) => {
    const levelOrder: Record<string, number> = { red: 0, yellow: 1, green: 2 };
    const sevOrder: Record<string, number> = { high: 0, medium: 1, low: 2 };
    return (
      levelOrder[a.riskLevel] - levelOrder[b.riskLevel] ||
      sevOrder[a.severity] - sevOrder[b.severity]
    );
  });

  const top5 = sorted.slice(0, 5);
  const topList = document.getElementById("topRisksList")!;
  topList.innerHTML = top5
    .map(
      (r, i) => `
      <div class="top-risk-item">
        <span class="top-risk-rank">${i + 1}</span>
        <span class="top-risk-indicator" style="background:var(--${r.riskLevel})"></span>
        <span class="top-risk-text">${localizedText(r.title)}</span>
        <span class="top-risk-module">${r.module}</span>
      </div>
    `,
    )
    .join("");
}

// ── TIMELINE ──────────────────────────────────
function renderTimeline(): void {
  const container = document.getElementById("timelineVisual")!;
  container.innerHTML = TIMELINE_EVENTS.map(
    (ev) => `
      <div class="timeline-event impact-${ev.impact}">
        <span class="tl-month-badge">M+${ev.month}</span>
        <div class="tl-columns">
          <div class="tl-col tl-tech">
            <h4>${t("tlTechnical")}</h4>
            <p>${localizedText(ev.technical)}</p>
          </div>
          <div class="tl-col tl-biz">
            <h4>${t("tlBusiness")}</h4>
            <p>${localizedText(ev.business)}</p>
          </div>
        </div>
      </div>
    `,
  ).join("");
}

// ── REGULATORY STANDARDS TABLE ────────────────
function renderStandards(): void {
  const tbody = document.getElementById("standardsBody")!;
  tbody.innerHTML = STANDARDS.map((s) => {
    const badgeClass =
      s.status === "complete"
        ? "badge-complete"
        : s.status === "in-progress"
          ? "badge-in-progress"
          : "badge-not-started";
    const statusText =
      s.status === "complete"
        ? t("complete")
        : s.status === "in-progress"
          ? t("inProgress")
          : t("notStarted");

    return `
      <tr>
        <td><span class="std-code">${s.code}</span></td>
        <td>${localizedText(s.title)}</td>
        <td>${s.applies}</td>
        <td>
          <span class="std-status-badge ${badgeClass}${ACTIVE_ROLE === "pmp" ? " clickable-badge" : ""}"
                ${ACTIVE_ROLE === "pmp" ? `data-action="cycleStandardStatus" data-sid="${s.id}" title="${t("clickToChangeStatus")}"` : ""}>
            ${statusText}
          </span>
        </td>
        <td>
          <div class="progress-cell">
            <div class="progress-bar">
              <div class="progress-bar-fill" style="width:${s.progress}%"></div>
            </div>
            ${
              ACTIVE_ROLE === "pmp"
                ? `<input type="number" class="progress-input" min="0" max="100" value="${s.progress}"
                   data-change="setStandardProgress" data-sid="${s.id}"
                   title="${t("progressLabel")}" />`
                : `<span class="progress-text">${s.progress}%</span>`
            }
          </div>
        </td>
      </tr>
    `;
  }).join("");
}

// ── CASH / RUNWAY ─────────────────────────────
function renderCashRunway(): void {
  const cr = CASH_RUNWAY;

  // Summary cards
  const cards = document.getElementById("cashSummaryCards")!;
  const runwayClass =
    cr.runwayMonths <= 3
      ? "runway-critical"
      : cr.runwayMonths <= 6
        ? "runway-warning"
        : "runway-ok";
  const canEditCash = ["pmp", "business", "technology"].includes(ACTIVE_ROLE);
  cards.innerHTML = `
    <div class="cash-card">
      <div class="cash-card-label">${t("cashOnHand")}</div>
      <div class="cash-card-value">${fmtCurrency(cr.cashOnHand)}
        ${canEditCash ? `<button class="cash-edit-btn" data-action="editCashField" data-field="cashOnHand" title="${t("editCashHint")}">✎</button>` : ""}
      </div>
    </div>
    <div class="cash-card">
      <div class="cash-card-label">${t("monthlyBurnLabel")}</div>
      <div class="cash-card-value burn-value">${fmtCurrency(cr.monthlyBurn)}/mo
        ${canEditCash ? `<button class="cash-edit-btn" data-action="editCashField" data-field="monthlyBurn" title="${t("editBurnHint")}">✎</button>` : ""}
      </div>
    </div>
    <div class="cash-card">
      <div class="cash-card-label">${t("runwayLabel")}</div>
      <div class="cash-card-value ${runwayClass}">${cr.runwayMonths} ${t("runwayMonths")}</div>
    </div>
  `;

  // Funding rounds
  const frContainer = document.getElementById("fundingRoundsContainer")!;
  frContainer.innerHTML = cr.fundingRounds
    .map((fr) => {
      const statusKey =
        fr.status === "received"
          ? "frReceived"
          : fr.status === "committed"
            ? "frCommitted"
            : "frPipeline";
      const statusClass = `fr-${fr.status}`;
      return `
      <div class="funding-round-row">
        <div class="fr-label">${localizedText(fr.label)}</div>
        <div class="fr-amount">${fmtCurrency(fr.amount)}</div>
        <div class="fr-date">${fr.date}</div>
        <div class="fr-status ${statusClass} clickable-badge"
             data-action="toggleFundingStatus" data-frid="${fr.id}"
             title="${t("clickToChangeStatus")}">
          ${t(statusKey)}
        </div>
      </div>
    `;
    })
    .join("");

  // Add funding form
  frContainer.innerHTML += `
    <div class="add-funding-form">
      <h4>${t("addFundingTitle")}</h4>
      <div class="funding-form-row">
        <input type="text" id="newFundingLabel" placeholder="${t("fundingLabelPlaceholder")}" />
        <input type="number" id="newFundingAmount" placeholder="${t("fundingAmountPlaceholder")}" min="0" />
        <input type="text" id="newFundingDate" placeholder="${t("fundingDatePlaceholder")}" />
        <button class="btn-add-funding" data-action="addFundingRound">${t("addFundingBtn")}</button>
      </div>
      <p class="funding-note">${t("fundingNote")}</p>
    </div>
  `;

  // Burn history (editable for PMP/Business/Technology)
  const bhContainer = document.getElementById("burnHistoryContainer")!;
  const maxBurn = Math.max(...cr.burnHistory.map((b) => b.burn));
  bhContainer.innerHTML = cr.burnHistory
    .map((b) => {
      const pct = Math.round((b.burn / maxBurn) * 100);
      const monthLabel = b.month < 0 ? `M${b.month}` : `M+${b.month}`;
      return `
      <div class="burn-row">
        <span class="burn-month">${monthLabel}</span>
        <div class="burn-bar-wrap">
          <div class="burn-bar" style="width:${pct}%"></div>
        </div>
        <span class="burn-amount">${fmtCurrency(b.burn)}${canEditCash ? ` <button class="cash-edit-btn" data-action="editBurnEntry" data-burnmonth="${b.month}" title="${t("burnEditHint")}">✎</button>` : ""}</span>
        <span class="burn-note">${localizedText(b.note)}</span>
        ${canEditCash ? `<button class="cash-edit-btn burn-delete-btn" data-action="deleteBurnEntry" data-burnmonth="${b.month}" title="✕">✕</button>` : ""}
      </div>
    `;
    })
    .join("");

  if (canEditCash) {
    bhContainer.innerHTML += `
      <div class="burn-add-row">
        <button class="btn-add-funding" data-action="addBurnEntry">${t("burnAddBtn")}</button>
      </div>`;
  }

  // Exchange rate note (CN only)
  const rateNote = t("exchangeRateNote");
  if (rateNote) {
    bhContainer.innerHTML += `<p class="exchange-rate-note">${rateNote}</p>`;
  }
}

// ── INPUT PANEL ───────────────────────────────
function renderInputPanel(): void {
  const content = document.getElementById("inputPanelContent")!;
  const isPMP = ACTIVE_ROLE === "pmp";

  // PMP-only form to log new stakeholder inputs
  let formHtml = "";
  if (isPMP) {
    const gateOptions = GATES.map(
      (g) =>
        `<option value="G${g.number}">G${g.number} — ${localizedText(g.title)}</option>`,
    ).join("");
    formHtml = `
      <div class="log-input-form">
        <h4>${t("logInputTitle")}</h4>
        <div class="cr-form-row">
          <label>${t("logInputFrom")}</label>
          <select id="logInputFrom" class="cr-select">
            <option value="tech">${t("inputFromTech")}</option>
            <option value="business">${t("inputFromBusiness")}</option>
          </select>
        </div>
        <div class="cr-form-row">
          <label>${t("logInputGate")}</label>
          <select id="logInputGate" class="cr-select">${gateOptions}</select>
        </div>
        <div class="cr-form-row">
          <label>${t("logInputContent")}</label>
          <textarea id="logInputContent" placeholder="${t("logInputContentPlaceholder")}"></textarea>
        </div>
        <div class="cr-form-row">
          <label>${t("logInputStatus")}</label>
          <select id="logInputStatus" class="cr-select">
            <option value="pending-review">${t("pendingReview")}</option>
            <option value="accepted">${t("accepted")}</option>
            <option value="noted">${t("noted")}</option>
          </select>
        </div>
        <button class="btn-add-funding" data-action="logStakeholderInput">${t("logInputSubmit")}</button>
      </div>
      <hr style="border-color:var(--border);margin:var(--sp-md) 0" />
    `;
  }

  const entries = STAKEHOLDER_INPUTS.slice()
    .reverse()
    .map((inp) => {
      const fromClass = inp.from === "tech" ? "from-tech" : "from-business";
      const fromLabel =
        inp.from === "tech" ? t("inputFromTech") : t("inputFromBusiness");
      const statusMap: Record<string, { key: string; cls: string }> = {
        "pending-review": { key: "pendingReview", cls: "input-status-pending" },
        accepted: { key: "accepted", cls: "input-status-accepted" },
        rejected: { key: "rejected", cls: "input-status-accepted" },
        noted: { key: "noted", cls: "input-status-accepted" },
      };
      const si = statusMap[inp.status] || statusMap["pending-review"];
      const statusBadge = `<span class="input-status-badge ${si.cls}">${t(si.key as Parameters<typeof t>[0])}</span>`;

      let responseHtml = "";
      if (inp.pmpResponse) {
        responseHtml = `<div class="pmp-response">${localizedText(inp.pmpResponse)}</div>`;
      }

      return `
      <div class="input-entry ${fromClass}" style="margin-bottom:var(--sp-md)">
        <div class="input-meta">${fromLabel} · ${inp.date} · Gate ${inp.gate} ${statusBadge}</div>
        <div style="margin-top:var(--sp-xs)">${localizedText(inp.content)}</div>
        ${responseHtml}
      </div>
    `;
    })
    .join("");

  content.innerHTML =
    formHtml + (entries || `<p style="color:var(--text-muted)">No inputs.</p>`);
}

function updateFabBadge(): void {
  const pending = STAKEHOLDER_INPUTS.filter(
    (i) => i.status === "pending-review",
  ).length;
  const badge = document.getElementById("fabBadge")!;
  badge.textContent = String(pending);
  badge.classList.toggle("hidden", pending === 0);
}

// ── LOG STAKEHOLDER INPUT (PMP only) ──────────
window._logStakeholderInput = function (): void {
  if (ACTIVE_ROLE !== "pmp") return;
  const fromEl = document.getElementById("logInputFrom") as HTMLSelectElement;
  const gateEl = document.getElementById("logInputGate") as HTMLSelectElement;
  const contentEl = document.getElementById(
    "logInputContent",
  ) as HTMLTextAreaElement;
  const statusEl = document.getElementById(
    "logInputStatus",
  ) as HTMLSelectElement;

  const text = contentEl?.value?.trim();
  if (!text) return;

  const from = fromEl.value as "tech" | "business";
  const gate = gateEl.value;
  const status = statusEl.value as "pending-review" | "accepted" | "noted";

  const id = "INP-" + String(STAKEHOLDER_INPUTS.length + 1).padStart(3, "0");
  const lang = getLang();
  STAKEHOLDER_INPUTS.push({
    id,
    from,
    date: new Date().toISOString().split("T")[0],
    gate,
    content: { en: lang === "en" ? text : "", cn: lang === "cn" ? text : "" },
    status,
    pmpResponse: null,
  });
  saveInputs();
  renderInputPanel();
  updateFabBadge();
  renderSummary();
};

// ── HELPERS ───────────────────────────────────
function capitalize(str: string): string {
  if (!str) return "";
  return str.charAt(0).toUpperCase() + str.slice(1).replace(/-/g, " ");
}

function showCrToast(crId: string): void {
  const existing = document.getElementById("crToast");
  if (existing) existing.remove();
  const toast = document.createElement("div");
  toast.id = "crToast";
  toast.className = "cr-toast";
  toast.textContent = `${crId}: ${t("crSubmitted")}`;
  document.body.appendChild(toast);
  requestAnimationFrame(() => toast.classList.add("cr-toast-show"));
  setTimeout(() => {
    toast.classList.remove("cr-toast-show");
    setTimeout(() => toast.remove(), 400);
  }, 4000);
}

// ── RISK EDITOR MODAL ─────────────────────────
window._openRiskEditor = function (riskId: string): void {
  const risk = RISKS.find((r) => r.id === riskId);
  if (!risk) return;

  // Remove existing overlay if any
  const existing = document.getElementById("riskEditorOverlay");
  if (existing) existing.remove();

  const severities = ["high", "medium", "low"];
  const probabilities = ["high", "medium", "low", "very-low"];
  const levels = ["red", "yellow", "green"];
  const mitigations = ["not-started", "in-progress", "complete"];

  const makeOptions = (opts: string[], current: string) =>
    opts
      .map(
        (o) =>
          `<option value="${o}" ${o === current ? "selected" : ""}>${capitalize(o)}</option>`,
      )
      .join("");

  const overlay = document.createElement("div");
  overlay.id = "riskEditorOverlay";
  overlay.className = "gate-detail-overlay open";

  const isPmp = ACTIVE_ROLE === "pmp";

  const fieldsHtml = isPmp
    ? `<div class="risk-editor-fields">
        <label>${t("riskFieldSeverity")}
          <select data-change="setRiskField" data-rid="${riskId}" data-rfield="severity">
            ${makeOptions(severities, risk.severity)}
          </select>
        </label>
        <label>${t("riskFieldProbability")}
          <select data-change="setRiskField" data-rid="${riskId}" data-rfield="probability">
            ${makeOptions(probabilities, risk.probability)}
          </select>
        </label>
        <label>${t("riskFieldLevel")}
          <select data-change="setRiskField" data-rid="${riskId}" data-rfield="riskLevel">
            ${makeOptions(levels, risk.riskLevel)}
          </select>
        </label>
        <label>${t("riskMitigation")}
          <select data-change="setRiskField" data-rid="${riskId}" data-rfield="mitigationStatus">
            ${makeOptions(mitigations, risk.mitigationStatus)}
          </select>
        </label>
      </div>`
    : `<div class="risk-editor-fields risk-readonly">
        <label>${t("riskFieldSeverity")}<span class="readonly-value">${capitalize(risk.severity)}</span></label>
        <label>${t("riskFieldProbability")}<span class="readonly-value">${capitalize(risk.probability)}</span></label>
        <label>${t("riskFieldLevel")}<span class="readonly-value">${capitalize(risk.riskLevel)}</span></label>
        <label>${t("riskMitigation")}<span class="readonly-value">${capitalize(risk.mitigationStatus)}</span></label>
      </div>`;

  overlay.innerHTML = `
    <div class="gate-detail-modal" style="max-width:500px">
      <button class="modal-close" data-action="closeRiskEditor">&times;</button>
      <div class="gate-detail-header">
        <h2>${risk.id} — ${isPmp ? t("riskEditTitle") : localizedText(risk.title)}</h2>
        <div class="gate-detail-meta">${isPmp ? localizedText(risk.title) : risk.id}</div>
      </div>
      ${fieldsHtml}
    </div>
  `;
  document.body.appendChild(overlay);
  overlay.addEventListener("click", (e) => {
    if (e.target === overlay) window._closeRiskEditor();
  });
};

window._setRiskField = function (
  riskId: string,
  field: string,
  value: string,
): void {
  const risk = RISKS.find((r) => r.id === riskId);
  if (!risk) return;

  const oldValue = String(
    (risk as unknown as Record<string, unknown>)[field] ?? "",
  );

  if (ACTIVE_ROLE !== "pmp") {
    window._closeRiskEditor();
    window._openChangeRequestForm("risk-field", riskId, field, oldValue);
    return;
  }

  (risk as unknown as Record<string, unknown>)[field] = value;
  renderRisks();
  renderSummary();
};

window._closeRiskEditor = function (): void {
  const overlay = document.getElementById("riskEditorOverlay");
  if (overlay) overlay.remove();
};

// ── STANDARD STATUS CYCLING ───────────────────
window._cycleStandardStatus = function (standardId: string): void {
  const std = STANDARDS.find((s) => s.id === standardId);
  if (!std) return;

  if (ACTIVE_ROLE !== "pmp") {
    window._openChangeRequestForm(
      "standard-status",
      standardId,
      "status",
      std.status,
    );
    return;
  }

  const cycle: Record<string, "in-progress" | "complete" | "not-started"> = {
    "not-started": "in-progress",
    "in-progress": "complete",
    complete: "not-started",
  };
  std.status = cycle[std.status];

  // Auto-adjust progress to match status
  if (std.status === "complete") std.progress = 100;
  else if (std.status === "not-started") std.progress = 0;
  else if (std.progress === 0 || std.progress === 100) std.progress = 50;

  renderStandards();
  renderSummary();
};

window._setStandardProgress = function (
  standardId: string,
  value: string,
): void {
  const std = STANDARDS.find((s) => s.id === standardId);
  if (!std) return;
  if (ACTIVE_ROLE !== "pmp") {
    window._openChangeRequestForm(
      "standard-progress",
      standardId,
      "progress",
      String(std.progress),
    );
    return;
  }
  const num = Math.max(0, Math.min(100, parseInt(value, 10) || 0));
  std.progress = num;

  // Auto-adjust status to match progress
  if (num === 100) std.status = "complete";
  else if (num === 0) std.status = "not-started";
  else std.status = "in-progress";

  renderStandards();
  renderSummary();
};

// ── FUNDING MANAGEMENT ────────────────────────
window._editCashField = function (field: "cashOnHand" | "monthlyBurn"): void {
  if (!["pmp", "business", "technology"].includes(ACTIVE_ROLE)) return;
  const label =
    field === "cashOnHand" ? t("cashOnHand") : t("monthlyBurnLabel");
  const current =
    field === "cashOnHand" ? CASH_RUNWAY.cashOnHand : CASH_RUNWAY.monthlyBurn;
  const input = prompt(`${label} (USD):`, String(current));
  if (input === null) return;
  const val = parseFloat(input.replace(/[^0-9.]/g, ""));
  if (isNaN(val) || val < 0) return;
  const prev = current;
  if (field === "cashOnHand") {
    CASH_RUNWAY.cashOnHand = val;
  } else {
    CASH_RUNWAY.monthlyBurn = val;
  }
  CASH_RUNWAY.runwayMonths =
    CASH_RUNWAY.monthlyBurn > 0
      ? Math.floor(CASH_RUNWAY.cashOnHand / CASH_RUNWAY.monthlyBurn)
      : 0;
  logAudit(
    "cash-field",
    "CASH_RUNWAY",
    field,
    t("currencySymbol") + prev.toLocaleString(),
    t("currencySymbol") + val.toLocaleString(),
    `Runway recalculated: ${CASH_RUNWAY.runwayMonths} months`,
  );
  renderCashRunway();
  renderAll();
};

window._editBudgetField = function (
  budgetId: string,
  field: "planned" | "actual",
): void {
  if (!["pmp", "business", "technology"].includes(ACTIVE_ROLE)) return;
  const cat = BUDGET_CATEGORIES.find((b) => b.id === budgetId);
  if (!cat) return;
  const label = `${localizedText(cat.label)} — ${field === "planned" ? t("budgetPlanned") : t("budgetActual")}`;
  const current = field === "planned" ? cat.planned : cat.actual;
  const input = prompt(`${label} (USD):`, String(current));
  if (input === null) return;
  const val = parseFloat(input.replace(/[^0-9.]/g, ""));
  if (isNaN(val) || val < 0) return;
  const prev = current;
  if (field === "planned") {
    cat.planned = val;
  } else {
    cat.actual = val;
  }
  logAudit(
    "budget-field",
    budgetId,
    field,
    t("currencySymbol") + prev.toLocaleString(),
    t("currencySymbol") + val.toLocaleString(),
    localizedText(cat.label),
  );
  renderBudget();
  renderAll();
};

// ── Budget Category CRUD ───────────────────────
window._openAddBudgetForm = function (): void {
  const form = document.getElementById("budgetAddForm");
  if (!form) return;
  form.innerHTML = `
    <div class="funding-form-row">
      <input type="text" id="budgetFormLabel" placeholder="${t("budgetFormLabel")}" />
      <input type="text" id="budgetFormLabelCn" placeholder="${t("budgetFormLabelCn")}" />
      <input type="number" id="budgetFormPlanned" placeholder="${t("budgetFormPlanned")}" min="0" />
      <input type="number" id="budgetFormActual" placeholder="${t("budgetFormActual")}" min="0" value="0" />
      <button class="btn-add-funding" data-action="addBudgetCategory">${t("budgetFormAdd")}</button>
      <button class="btn-secondary" onclick="document.getElementById('budgetAddForm').innerHTML=''">${t("budgetFormCancel")}</button>
    </div>
  `;
};

window._addBudgetCategory = function (): void {
  if (!["pmp", "business", "technology"].includes(ACTIVE_ROLE)) return;
  const labelEl = document.getElementById(
    "budgetFormLabel",
  ) as HTMLInputElement;
  const labelCnEl = document.getElementById(
    "budgetFormLabelCn",
  ) as HTMLInputElement;
  const plannedEl = document.getElementById(
    "budgetFormPlanned",
  ) as HTMLInputElement;
  const actualEl = document.getElementById(
    "budgetFormActual",
  ) as HTMLInputElement;
  const label = labelEl?.value?.trim();
  if (!label) return;
  const planned = parseFloat(plannedEl?.value || "0");
  const actual = parseFloat(actualEl?.value || "0");
  const id = "BUD-" + String(BUDGET_CATEGORIES.length + 1).padStart(3, "0");
  BUDGET_CATEGORIES.push({
    id,
    label: { en: label, cn: labelCnEl?.value?.trim() || label },
    planned: isNaN(planned) ? 0 : planned,
    actual: isNaN(actual) ? 0 : actual,
    notes: "",
  });
  logAudit("budget-add", id, "add", "", label, "");
  const form = document.getElementById("budgetAddForm");
  if (form) form.innerHTML = "";
  renderBudget();
  renderAll();
};

window._deleteBudgetCategory = function (budgetId: string): void {
  if (!["pmp", "business", "technology"].includes(ACTIVE_ROLE)) return;
  if (!confirm(t("budgetDeleteConfirm"))) return;
  const idx = BUDGET_CATEGORIES.findIndex((b) => b.id === budgetId);
  if (idx < 0) return;
  const cat = BUDGET_CATEGORIES[idx];
  BUDGET_CATEGORIES.splice(idx, 1);
  logAudit(
    "budget-delete",
    budgetId,
    "delete",
    localizedText(cat.label),
    "",
    "",
  );
  renderBudget();
  renderAll();
};

window._addFundingRound = function (): void {
  const labelEl = document.getElementById(
    "newFundingLabel",
  ) as HTMLInputElement;
  const amountEl = document.getElementById(
    "newFundingAmount",
  ) as HTMLInputElement;
  const dateEl = document.getElementById("newFundingDate") as HTMLInputElement;

  const label = labelEl?.value?.trim();
  const amount = parseFloat(amountEl?.value || "0");
  const date = dateEl?.value?.trim();
  if (!label || !amount || !date) return;

  const id =
    "FR-" + String(CASH_RUNWAY.fundingRounds.length + 1).padStart(3, "0");
  CASH_RUNWAY.fundingRounds.push({
    id,
    label: { en: label, cn: label },
    amount,
    date,
    status: "pipeline",
  });

  renderCashRunway();
};

window._toggleFundingStatus = function (roundId: string): void {
  const round = CASH_RUNWAY.fundingRounds.find((fr) => fr.id === roundId);
  if (!round) return;
  if (!["pmp", "business", "technology"].includes(ACTIVE_ROLE)) {
    window._openChangeRequestForm(
      "funding-status",
      roundId,
      "status",
      round.status,
    );
    return;
  }

  const cycle: Record<string, "committed" | "received" | "pipeline"> = {
    pipeline: "committed",
    committed: "received",
    received: "pipeline",
  };
  const prevStatus = round.status;
  round.status = cycle[round.status];

  // When a round transitions to "received", update cash on hand and runway
  if (round.status === "received" && prevStatus !== "received") {
    CASH_RUNWAY.cashOnHand += round.amount;
    CASH_RUNWAY.runwayMonths = Math.floor(
      CASH_RUNWAY.cashOnHand / CASH_RUNWAY.monthlyBurn,
    );
  }
  // When cycling away from "received", reverse the adjustment
  if (prevStatus === "received" && round.status !== "received") {
    CASH_RUNWAY.cashOnHand -= round.amount;
    CASH_RUNWAY.runwayMonths = Math.floor(
      CASH_RUNWAY.cashOnHand / CASH_RUNWAY.monthlyBurn,
    );
  }

  renderCashRunway();
  renderSummary();
};

// ── Burn History CRUD ───────────────────────────
window._editBurnEntry = function (month: number): void {
  if (!["pmp", "business", "technology"].includes(ACTIVE_ROLE)) return;
  const entry = CASH_RUNWAY.burnHistory.find((b) => b.month === month);
  if (!entry) return;
  const input = prompt(
    `${month < 0 ? `M${month}` : `M+${month}`} — ${t("burnFormAmount")}:`,
    String(entry.burn),
  );
  if (input === null) return;
  const val = parseFloat(input.replace(/[^0-9.]/g, ""));
  if (isNaN(val) || val < 0) return;
  const prev = entry.burn;
  entry.burn = val;
  logAudit(
    "burn-edit",
    `M${month}`,
    "burn",
    fmtCurrency(prev),
    fmtCurrency(val),
    "",
  );
  renderCashRunway();
};

window._addBurnEntry = function (): void {
  if (!["pmp", "business", "technology"].includes(ACTIVE_ROLE)) return;
  const monthStr = prompt(t("burnFormMonth"), "M+1");
  if (!monthStr) return;
  const m = parseInt(monthStr.replace(/[Mm+]/g, ""), 10);
  if (isNaN(m)) return;
  if (CASH_RUNWAY.burnHistory.some((b) => b.month === m)) return;
  const amtStr = prompt(t("burnFormAmount"), "45000");
  if (!amtStr) return;
  const amt = parseFloat(amtStr.replace(/[^0-9.]/g, ""));
  if (isNaN(amt) || amt < 0) return;
  const note = prompt(t("burnFormNote"), "") || "";
  CASH_RUNWAY.burnHistory.push({
    month: m,
    burn: amt,
    note: { en: note, cn: note },
  });
  CASH_RUNWAY.burnHistory.sort((a, b) => a.month - b.month);
  logAudit(
    "burn-add",
    `M${m >= 0 ? "+" : ""}${m}`,
    "add",
    "",
    fmtCurrency(amt),
    note,
  );
  renderCashRunway();
};

window._deleteBurnEntry = function (month: number): void {
  if (!["pmp", "business", "technology"].includes(ACTIVE_ROLE)) return;
  if (!confirm(t("burnDeleteConfirm"))) return;
  const entry = CASH_RUNWAY.burnHistory.find((b) => b.month === month);
  CASH_RUNWAY.burnHistory = CASH_RUNWAY.burnHistory.filter(
    (b) => b.month !== month,
  );
  logAudit(
    "burn-delete",
    `M${month}`,
    "delete",
    entry ? fmtCurrency(entry.burn) : "",
    "",
    "",
  );
  renderCashRunway();
};

// ══════════════════════════════════════════════════
// ROLE SWITCHER
// ══════════════════════════════════════════════════
function initRoleSwitcher(): void {
  const container = document.getElementById("roleSwitcher");
  if (!container) return;
  container.addEventListener("change", (e) => {
    const select = e.target as HTMLSelectElement;
    if (select?.id === "roleSelect") {
      window._setRole(select.value);
    }
  });
}

window._setRole = function (role: string): void {
  setActiveRole(role as UserRole);
  renderAll();
};

// Accounting: read-only access to Cash/Runway, Timeline, Gate statuses only
// Tech/Business: can view all, but changes go through CR workflow
function applyRoleRestrictions(): void {
  const role = ACTIVE_ROLE;
  const tabs = document.querySelectorAll<HTMLButtonElement>(".tab-btn");
  const accountingTabs = new Set([
    "cash-runway",
    "timeline",
    "gates",
    "budget",
  ]);

  tabs.forEach((btn) => {
    const tab = btn.dataset.tab || "";
    if (role === "accounting") {
      const allowed = accountingTabs.has(tab);
      btn.classList.toggle("tab-restricted", !allowed);
      btn.disabled = !allowed;
    } else {
      btn.classList.remove("tab-restricted");
      btn.disabled = false;
    }
  });

  // If accounting is on a restricted tab, switch to cash-runway
  if (role === "accounting" && !accountingTabs.has(activeTab)) {
    const cashBtn = document.querySelector<HTMLButtonElement>(
      '.tab-btn[data-tab="cash-runway"]',
    );
    if (cashBtn) cashBtn.click();
  }

  // Show/hide role badge
  const roleBadge = document.getElementById("roleBadgeText");
  if (roleBadge) {
    const labels: Record<string, string> = {
      pmp: t("rolePmp"),
      tech: t("roleTech"),
      business: t("roleBusiness"),
      accounting: t("roleAccounting"),
    };
    roleBadge.textContent = labels[role] || role;
  }

  // Show accounting notice
  const notice = document.getElementById("accountingNotice");
  if (notice) {
    notice.style.display = role === "accounting" ? "block" : "none";
    notice.textContent = t("roleAccountingAccess");
  }
}

// ══════════════════════════════════════════════════
// CHANGE REQUEST WORKFLOW
// ══════════════════════════════════════════════════
window._openChangeRequestForm = function (
  type: string,
  targetId: string,
  field: string,
  oldVal: string,
): void {
  const isStatusField = field === "status";
  const oldLabel = isStatusField ? t("crOldStatus") : t("crOldValue");
  const newLabel = isStatusField ? t("crNewStatus") : t("crNewValue");

  // Build proposed value input — dropdown for status fields, text for others
  let proposedInput: string;
  if (type === "milestone-status" || type === "standard-status") {
    const isCN = getLang() === "cn";
    const opts = [
      { value: "not-started", label: isCN ? "未开始" : "Not Started" },
      { value: "in-progress", label: isCN ? "进行中" : "In Progress" },
      { value: "complete", label: isCN ? "完成" : "Complete" },
    ];
    const options = opts
      .filter((o) => o.value !== oldVal)
      .map((o) => `<option value="${o.value}">${o.label}</option>`)
      .join("");
    proposedInput = `<select id="crNewValue" class="cr-select">${options}</select>`;
  } else if (type === "funding-status") {
    const isCN = getLang() === "cn";
    const opts = [
      { value: "pipeline", label: isCN ? "洽谈中" : "Pipeline" },
      { value: "committed", label: isCN ? "已承诺" : "Committed" },
      { value: "received", label: isCN ? "已到账" : "Received" },
    ];
    const options = opts
      .filter((o) => o.value !== oldVal)
      .map((o) => `<option value="${o.value}">${o.label}</option>`)
      .join("");
    proposedInput = `<select id="crNewValue" class="cr-select">${options}</select>`;
  } else if (type === "action-status") {
    const isCN = getLang() === "cn";
    const opts = [
      { value: "todo", label: isCN ? "待办" : "Todo" },
      { value: "in-progress", label: isCN ? "进行中" : "In Progress" },
      { value: "blocked", label: isCN ? "受阻" : "Blocked" },
      { value: "done", label: isCN ? "完成" : "Done" },
    ];
    const options = opts
      .filter((o) => o.value !== oldVal)
      .map((o) => `<option value="${o.value}">${o.label}</option>`)
      .join("");
    proposedInput = `<select id="crNewValue" class="cr-select">${options}</select>`;
  } else if (type === "dhf-status") {
    const isCN = getLang() === "cn";
    const opts = [
      { value: "not-started", label: isCN ? "未开始" : "Not Started" },
      { value: "draft", label: isCN ? "草稿" : "Draft" },
      { value: "in-review", label: isCN ? "审核中" : "In Review" },
      { value: "approved", label: isCN ? "已批准" : "Approved" },
    ];
    const options = opts
      .filter((o) => o.value !== oldVal)
      .map((o) => `<option value="${o.value}">${o.label}</option>`)
      .join("");
    proposedInput = `<select id="crNewValue" class="cr-select">${options}</select>`;
  } else if (type === "capa-status") {
    const isCN = getLang() === "cn";
    const opts = [
      { value: "open", label: isCN ? "开放" : "Open" },
      { value: "in-progress", label: isCN ? "进行中" : "In Progress" },
      { value: "closed", label: isCN ? "关闭" : "Closed" },
      { value: "verified", label: isCN ? "已验证" : "Verified" },
    ];
    const options = opts
      .filter((o) => o.value !== oldVal)
      .map((o) => `<option value="${o.value}">${o.label}</option>`)
      .join("");
    proposedInput = `<select id="crNewValue" class="cr-select">${options}</select>`;
  } else if (type === "supplier-status") {
    const isCN = getLang() === "cn";
    const opts = [
      { value: "under-review", label: isCN ? "审核中" : "Under Review" },
      { value: "qualified", label: isCN ? "合格" : "Qualified" },
      { value: "active", label: isCN ? "活跃" : "Active" },
      { value: "risk", label: isCN ? "风险" : "Risk" },
    ];
    const options = opts
      .filter((o) => o.value !== oldVal)
      .map((o) => `<option value="${o.value}">${o.label}</option>`)
      .join("");
    proposedInput = `<select id="crNewValue" class="cr-select">${options}</select>`;
  } else {
    proposedInput = `<input type="text" id="crNewValue" placeholder="${t("crNewValuePlaceholder")}" />`;
  }

  const existing = document.getElementById("crFormOverlay");
  if (existing) existing.remove();

  const role = ACTIVE_ROLE;
  const fromLabel =
    role === "tech" ? t("inputFromTech") : t("inputFromBusiness");

  const overlay = document.createElement("div");
  overlay.id = "crFormOverlay";
  overlay.className = "gate-detail-overlay open";
  overlay.innerHTML = `
    <div class="gate-detail-modal cr-modal">
      <button class="modal-close" data-action="closeChangeRequestForm">&times;</button>
      <div class="gate-detail-header">
        <h2>${t("crSubmitTitle")}</h2>
        <div class="gate-detail-meta">${t("crRequiresApproval")}</div>
      </div>
      <div class="cr-form">
        <div class="cr-form-row">
          <label>${t("crFrom")}</label>
          <span class="cr-value">${fromLabel}</span>
        </div>
        <div class="cr-form-row">
          <label>${t("crField")}</label>
          <span class="cr-value">${targetId} → ${field}</span>
        </div>
        <div class="cr-form-row">
          <label>${oldLabel}</label>
          <span class="cr-value cr-old">${capitalize(oldVal)}</span>
        </div>
        <div class="cr-form-row">
          <label>${newLabel}</label>
          ${proposedInput}
        </div>
        <div class="cr-form-row">
          <label>${t("crJustification")}</label>
          <textarea id="crJustification" placeholder="${t("crJustPlaceholder")}"></textarea>
        </div>
        <div class="cr-form-row">
          <label>${t("crEvidence")}</label>
          <input type="text" id="crEvidence" placeholder="${t("crEvidencePlaceholder")}" />
        </div>
        <div class="cr-form-row">
          <label>${t("crDocuments")}</label>
          <div class="cr-file-upload">
            <input type="file" id="crFileInput" multiple class="cr-file-input" />
            <label for="crFileInput" class="cr-file-label">${t("crChooseFiles")}</label>
            <div id="crFileList" class="cr-file-list"></div>
          </div>
        </div>
        <button class="btn-add-funding cr-submit-btn"
                data-action="submitChangeRequest" data-crtype="${type}" data-crtarget="${targetId}" data-crfield="${field}" data-crold="${oldVal}">
          ${t("crSubmit")}
        </button>
      </div>
    </div>
  `;
  crQueuedFiles = [];
  document.body.appendChild(overlay);
  overlay.addEventListener("click", (e) => {
    if (e.target === overlay) window._closeChangeRequestForm();
  });

  // File upload handling
  const fileInput = document.getElementById("crFileInput") as HTMLInputElement;
  fileInput?.addEventListener("change", () => {
    if (fileInput.files) {
      for (const f of Array.from(fileInput.files)) {
        crQueuedFiles.push(f);
      }
      fileInput.value = "";
      renderQueuedFiles();
    }
  });
};

window._removeQueuedDocument = function (index: number): void {
  crQueuedFiles.splice(index, 1);
  renderQueuedFiles();
};

function renderQueuedFiles(): void {
  const list = document.getElementById("crFileList");
  if (!list) return;
  list.innerHTML = crQueuedFiles
    .map(
      (f, i) =>
        `<div class="cr-file-item">
          <span class="cr-file-name">${f.name}</span>
          <span class="cr-file-size">(${formatFileSize(f.size)})</span>
          <button class="cr-file-remove" data-action="removeQueuedDocument" data-idx="${i}">&times;</button>
        </div>`,
    )
    .join("");
}

function formatFileSize(bytes: number): string {
  if (bytes < 1024) return bytes + " B";
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + " KB";
  return (bytes / (1024 * 1024)).toFixed(1) + " MB";
}

window._closeChangeRequestForm = function (): void {
  crQueuedFiles = [];
  const overlay = document.getElementById("crFormOverlay");
  if (overlay) overlay.remove();
};

window._submitChangeRequest = function (
  type: string,
  targetId: string,
  field: string,
  oldVal: string,
  newVal: string,
): void {
  const justEl = document.getElementById(
    "crJustification",
  ) as HTMLTextAreaElement;
  const evidEl = document.getElementById("crEvidence") as HTMLInputElement;

  const justification = justEl?.value?.trim() || "";
  const evidence = evidEl?.value?.trim() || "";

  if (!newVal?.trim() || !justification) return;

  const id = "CR-" + String(CHANGE_REQUESTS.length + 1).padStart(3, "0");

  // Build document metadata and store files
  const docs: CRDocument[] = crQueuedFiles.map((f, i) => ({
    name: f.name,
    size: f.size,
    type: f.type,
    key: `${id}-doc-${i}`,
  }));

  // Store each file in IndexedDB (fire-and-forget is fine here)
  crQueuedFiles.forEach((f, i) => {
    storeDocument(`${id}-doc-${i}`, f);
  });

  const cr: ChangeRequest = {
    id,
    type: type as ChangeRequest["type"],
    from: ACTIVE_ROLE === "tech" ? "tech" : "business",
    date: new Date().toISOString().split("T")[0],
    targetId,
    field,
    oldValue: oldVal,
    newValue: newVal.trim(),
    justification,
    evidence,
    documents: docs,
    status: "pending",
    pmpNote: null,
  };
  CHANGE_REQUESTS.push(cr);
  saveCRs();
  window._closeChangeRequestForm();
  updateFabBadge();
  showCrToast(cr.id);
};

window._approveChangeRequest = function (crId: string): void {
  const cr = CHANGE_REQUESTS.find((c) => c.id === crId);
  if (!cr || cr.status !== "pending") return;

  cr.status = "approved";
  cr.pmpNote = "Approved by PMP on " + new Date().toISOString().split("T")[0];
  logAudit(
    "cr-approved",
    crId,
    "status",
    "pending",
    "approved",
    `CR ${crId} approved`,
  );

  // Apply the change
  applyChangeRequest(cr);
  saveCRs();
  renderAll();
};

window._rejectChangeRequest = function (crId: string): void {
  const cr = CHANGE_REQUESTS.find((c) => c.id === crId);
  if (!cr || cr.status !== "pending") return;

  cr.status = "rejected";
  cr.pmpNote = "Rejected by PMP on " + new Date().toISOString().split("T")[0];
  logAudit(
    "cr-rejected",
    crId,
    "status",
    "pending",
    "rejected",
    `CR ${crId} rejected`,
  );
  saveCRs();
  renderAll();
};

window._downloadDocument = function (key: string, filename: string): void {
  getDocument(key).then((file) => {
    if (!file) return;
    const url = URL.createObjectURL(file);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  });
};

function applyChangeRequest(cr: ChangeRequest): void {
  switch (cr.type) {
    case "milestone-status": {
      const allMs = [
        ...TRACKS.technical.milestones,
        ...TRACKS.regulatory.milestones,
      ];
      const ms = allMs.find((m) => m.id === cr.targetId);
      if (ms) ms.status = cr.newValue as Milestone["status"];
      break;
    }
    case "risk-field": {
      const risk = RISKS.find((r) => r.id === cr.targetId);
      if (risk)
        (risk as unknown as Record<string, unknown>)[cr.field] = cr.newValue;
      break;
    }
    case "standard-status": {
      const std = STANDARDS.find((s) => s.id === cr.targetId);
      if (std) {
        std.status = cr.newValue as Milestone["status"];
        if (std.status === "complete") std.progress = 100;
        else if (std.status === "not-started") std.progress = 0;
        else if (std.progress === 0 || std.progress === 100) std.progress = 50;
      }
      break;
    }
    case "standard-progress": {
      const std2 = STANDARDS.find((s) => s.id === cr.targetId);
      if (std2) {
        const num = Math.max(0, Math.min(100, parseInt(cr.newValue, 10) || 0));
        std2.progress = num;
        if (num === 100) std2.status = "complete";
        else if (num === 0) std2.status = "not-started";
        else std2.status = "in-progress";
      }
      break;
    }
    case "funding-status": {
      const fr = CASH_RUNWAY.fundingRounds.find((f) => f.id === cr.targetId);
      if (fr) {
        const prev = fr.status;
        fr.status = cr.newValue as "received" | "committed" | "pipeline";
        if (fr.status === "received" && prev !== "received") {
          CASH_RUNWAY.cashOnHand += fr.amount;
          CASH_RUNWAY.runwayMonths = Math.floor(
            CASH_RUNWAY.cashOnHand / CASH_RUNWAY.monthlyBurn,
          );
        }
      }
      break;
    }
    case "action-status": {
      const act = ACTION_ITEMS.find((a) => a.id === cr.targetId);
      if (act) act.status = cr.newValue as typeof act.status;
      break;
    }
    case "dhf-status": {
      const dhf = DHF_DOCUMENTS.find((d) => d.id === cr.targetId);
      if (dhf) dhf.status = cr.newValue as typeof dhf.status;
      break;
    }
    case "capa-status": {
      const capa = CAPA_LOG.find((c) => c.id === cr.targetId);
      if (capa) {
        capa.status = cr.newValue as typeof capa.status;
        if (capa.status === "closed" && !capa.closedDate) {
          capa.closedDate = new Date().toISOString().split("T")[0];
        }
      }
      break;
    }
    case "supplier-status": {
      const sup = SUPPLIERS.find((s) => s.id === cr.targetId);
      if (sup) sup.status = cr.newValue as typeof sup.status;
      break;
    }
  }
}

// ── HIDDEN API PERSISTENCE ─────────────────────
const HIDDEN_APIS_KEY = "ctower_hidden_apis";
function loadHiddenApis(): Set<string> {
  try {
    const raw = localStorage.getItem(HIDDEN_APIS_KEY);
    return raw ? new Set(JSON.parse(raw)) : new Set();
  } catch {
    return new Set();
  }
}
function saveHiddenApis(hidden: Set<string>): void {
  localStorage.setItem(HIDDEN_APIS_KEY, JSON.stringify([...hidden]));
}

window._removeApiIntegration = function (apiKey: string): void {
  if (!["pmp", "business", "technology"].includes(ACTIVE_ROLE)) return;
  if (!confirm(t("apiRemoveConfirm"))) return;
  const hidden = loadHiddenApis();
  hidden.add(apiKey);
  saveHiddenApis(hidden);
  logAudit(
    "api-remove",
    "API",
    apiKey,
    "visible",
    "hidden",
    "Integration removed",
  );
  renderApiIntegrations();
  renderUsApiIntegrations();
};

window._restoreApiIntegrations = function (): void {
  if (!["pmp", "business", "technology"].includes(ACTIVE_ROLE)) return;
  const hidden = loadHiddenApis();
  if (hidden.size === 0) return;
  hidden.clear();
  saveHiddenApis(hidden);
  logAudit(
    "api-restore",
    "API",
    "all",
    "hidden",
    "visible",
    "All integrations restored",
  );
  renderApiIntegrations();
  renderUsApiIntegrations();
};

// ══════════════════════════════════════════════════
// CHINA INVESTOR API INTEGRATIONS PANEL
// ══════════════════════════════════════════════════
function renderApiIntegrations(): void {
  const container = document.getElementById("apiIntegrationsContainer");
  if (!container) return;
  const hidden = loadHiddenApis();
  const canEdit = ["pmp", "business", "technology"].includes(ACTIVE_ROLE);

  const apis = [
    {
      key: "cn-alipay",
      name: t("apiAlipay"),
      desc: t("apiAlipayDesc"),
      status: "planned",
      docs: "Alipay Global Merchant API",
    },
    {
      key: "cn-wechat",
      name: t("apiWechat"),
      desc: t("apiWechatDesc"),
      status: "planned",
      docs: "WeChat Pay API v3",
    },
    {
      key: "cn-unionpay",
      name: t("apiUnionpay"),
      desc: t("apiUnionpayDesc"),
      status: "planned",
      docs: "UnionPay Online Payment API",
    },
    {
      key: "cn-cmbchina",
      name: t("apiCmbchina"),
      desc: t("apiCmbchinaDesc"),
      status: "available",
      docs: "CMB Open Banking API",
    },
    {
      key: "cn-pingpong",
      name: t("apiPingpong"),
      desc: t("apiPingpongDesc"),
      status: "available",
      docs: "PingPong Global API",
    },
    {
      key: "cn-xe",
      name: t("apiXe"),
      desc: t("apiXeDesc"),
      status: "active",
      docs: "XE Currency Data API",
    },
    {
      key: "cn-swift",
      name: t("apiSwift"),
      desc: t("apiSwiftDesc"),
      status: "available",
      docs: "SWIFT gpi Tracker API",
    },
  ].filter((api) => !hidden.has(api.key));

  const statusLabel = (s: string) =>
    s === "active"
      ? t("apiActive")
      : s === "available"
        ? t("apiAvailable")
        : t("apiPlanned");

  container.innerHTML =
    apis
      .map(
        (api) => `
    <div class="api-card api-${api.status}">
      <div class="api-card-header">
        <span class="api-name">${api.name}</span>
        <span class="api-status-badge api-badge-${api.status}">${statusLabel(api.status)}</span>
        ${canEdit ? `<button class="cash-edit-btn" data-action="removeApiIntegration" data-apikey="${api.key}" title="${t("apiRemove")}">✕</button>` : ""}
      </div>
      <div class="api-desc">${api.desc}</div>
      <div class="api-meta">
        <span><strong>${t("apiDocs")}:</strong> ${api.docs}</span>
      </div>
    </div>
  `,
      )
      .join("") +
    (canEdit && hidden.size > 0
      ? `<button class="btn-add-funding" data-action="restoreApiIntegrations">${t("apiRestoreAll")}</button>`
      : "");
}

// ══════════════════════════════════════════════════
// US-SPECIFIC API INTEGRATIONS
// ══════════════════════════════════════════════════
function renderUsApiIntegrations(): void {
  const container = document.getElementById("usApiIntegrationsContainer");
  if (!container) return;
  const hidden = loadHiddenApis();
  const canEdit = ["pmp", "business", "technology"].includes(ACTIVE_ROLE);

  const apis = [
    {
      key: "us-plaid",
      name: t("usApiPlaid"),
      desc: t("usApiPlaidDesc"),
      status: "available",
      docs: "Plaid Link + Balance API",
    },
    {
      key: "us-mercury",
      name: t("usApiMercury"),
      desc: t("usApiMercuryDesc"),
      status: "active",
      docs: "Mercury Banking API v2",
    },
    {
      key: "us-stripe",
      name: t("usApiStripe"),
      desc: t("usApiStripeDesc"),
      status: "available",
      docs: "Stripe Payments API",
    },
    {
      key: "us-svb",
      name: t("usApiSvb"),
      desc: t("usApiSvbDesc"),
      status: "planned",
      docs: "SVB API Gateway",
    },
    {
      key: "us-angellist",
      name: t("usApiAngellist"),
      desc: t("usApiAngellistDesc"),
      status: "planned",
      docs: "AngelList Stack API",
    },
    {
      key: "us-carta",
      name: t("usApiCarta"),
      desc: t("usApiCartaDesc"),
      status: "planned",
      docs: "Carta Connect API",
    },
    {
      key: "us-sec",
      name: t("usApiSec"),
      desc: t("usApiSecDesc"),
      status: "available",
      docs: "SEC EDGAR XBRL API",
    },
  ].filter((api) => !hidden.has(api.key));

  const statusLabel = (s: string) =>
    s === "active"
      ? t("apiActive")
      : s === "available"
        ? t("apiAvailable")
        : t("apiPlanned");

  container.innerHTML =
    apis
      .map(
        (api) => `
    <div class="api-card api-${api.status}">
      <div class="api-card-header">
        <span class="api-name">${api.name}</span>
        <span class="api-status-badge api-badge-${api.status}">${statusLabel(api.status)}</span>
        ${canEdit ? `<button class="cash-edit-btn" data-action="removeApiIntegration" data-apikey="${api.key}" title="${t("apiRemove")}">✕</button>` : ""}
      </div>
      <div class="api-desc">${api.desc}</div>
      <div class="api-meta">
        <span><strong>${t("apiDocs")}:</strong> ${api.docs}</span>
      </div>
    </div>
  `,
      )
      .join("") +
    (canEdit && hidden.size > 0
      ? `<button class="btn-add-funding" data-action="restoreApiIntegrations">${t("apiRestoreAll")}</button>`
      : "");
}

// ══════════════════════════════════════════════════
// US INVESTMENT & INVESTOR RELATIONS
// ══════════════════════════════════════════════════
function renderUsInvestment(): void {
  // Metrics cards
  const metrics = document.getElementById("usInvestMetrics");
  if (metrics) {
    metrics.innerHTML = `
      <div class="cash-card">
        <div class="cash-card-label">${t("usInvestMeetings")}</div>
        <div class="cash-card-value">8</div>
      </div>
      <div class="cash-card">
        <div class="cash-card-label">${t("usInvestPipeline")}</div>
        <div class="cash-card-value">$2.5M</div>
      </div>
      <div class="cash-card">
        <div class="cash-card-label">${t("usInvestConverted")}</div>
        <div class="cash-card-value">$0</div>
      </div>
      <div class="cash-card">
        <div class="cash-card-label">${t("usInvestIrRole")}</div>
        <div class="cash-card-value" style="font-size:0.9rem">Lon Dailey</div>
      </div>
    `;
  }

  // Target investors table
  const tbody = document.getElementById("usInvestBody");
  if (tbody) {
    const targets = [
      {
        name: "MedTech Ventures",
        type: "VC",
        stage: "Seed",
        contact: "contacted",
        amount: "$500K",
        notes: "Focus on FDA-cleared devices",
      },
      {
        name: "BioStar Capital",
        type: "Angel Group",
        stage: "Seed",
        contact: "prospect",
        amount: "$250K",
        notes: "Pacific NW health-tech syndicate",
      },
      {
        name: "Cascade Health Fund",
        type: "VC",
        stage: "Series A",
        contact: "prospect",
        amount: "$1M",
        notes: "Portland-based, med-device focus",
      },
      {
        name: "Oregon Angel Fund",
        type: "Angel Group",
        stage: "Seed",
        contact: "contacted",
        amount: "$200K",
        notes: "Local angel network",
      },
      {
        name: "Digital Health Partners",
        type: "VC",
        stage: "Seed",
        contact: "in-dd",
        amount: "$500K",
        notes: "ICU/respiratory portfolio",
      },
    ];

    const contactLabel = (s: string) => {
      switch (s) {
        case "contacted":
          return `<span class="fr-committed">${t("usInvestContacted")}</span>`;
        case "in-dd":
          return `<span class="fr-received">${t("usInvestInDD")}</span>`;
        case "term-sheet":
          return `<span class="fr-received">${t("usInvestTermSheet")}</span>`;
        case "closed":
          return `<span class="fr-received">${t("usInvestClosed")}</span>`;
        default:
          return `<span class="fr-pipeline">${t("usInvestProspect")}</span>`;
      }
    };

    tbody.innerHTML = targets
      .map(
        (inv) => `
      <tr>
        <td>${inv.name}</td>
        <td>${inv.type}</td>
        <td>${inv.stage}</td>
        <td>${contactLabel(inv.contact)}</td>
        <td>${inv.amount}</td>
        <td>${inv.notes}</td>
      </tr>
    `,
      )
      .join("");
  }

  // IR Activities
  const activities = document.getElementById("usInvestActivities");
  if (activities) {
    const items = [
      {
        date: "2026-03-18",
        activity:
          "Initial outreach to MedTech Ventures — sent executive summary & pitch deck",
        status: "done",
      },
      {
        date: "2026-03-20",
        activity:
          "Oregon Angel Fund intro meeting — presented 510(k) regulatory strategy",
        status: "done",
      },
      {
        date: "2026-03-25",
        activity: "Digital Health Partners — due diligence data room setup",
        status: "in-progress",
      },
      {
        date: "2026-04-01",
        activity:
          "Prepare Phase 1 Seed Round investor update ($1.8M raised — deployment plan)",
        status: "todo",
      },
      {
        date: "2026-04-10",
        activity: "BioStar Capital — schedule intro call",
        status: "todo",
      },
      {
        date: "2026-04-15",
        activity:
          "Cascade Health Fund — warm introduction via Oregon Bio network",
        status: "todo",
      },
    ];

    const statusBadge = (s: string) => {
      switch (s) {
        case "done":
          return `<span class="std-complete">${t("complete")}</span>`;
        case "in-progress":
          return `<span class="std-in-progress">${t("inProgress")}</span>`;
        default:
          return `<span class="std-not-started">${t("notStarted")}</span>`;
      }
    };

    activities.innerHTML = items
      .map(
        (item) => `
      <div class="input-entry" style="margin-bottom:var(--sp-sm)">
        <div class="input-meta">${item.date} ${statusBadge(item.status)}</div>
        <div style="margin-top:var(--sp-xs)">${item.activity}</div>
      </div>
    `,
      )
      .join("");
  }
}

// ══════════════════════════════════════════════════
// DOCUMENT CONTROL
// ══════════════════════════════════════════════════

const DOCLIB_STORAGE_KEY = "ctower_doclib_docs";

const DEFAULT_DOCS: DocLibItem[] = [
  {
    id: "doc-1",
    dcn: "DCN-REG-001",
    cat: "regulatory",
    name: { en: "510(k) Pre-Submission Package", cn: "510(k)预提交包" },
    version: "2.0",
    date: "2026-03-15",
    owner: "Lon Dailey",
    status: "effective",
    effectiveDate: "2026-03-15",
    nextReview: "2026-06-15",
    linkedMilestone: "R1",
    revisions: [
      {
        rev: "1.0",
        date: "2026-02-01",
        author: "Lon Dailey",
        change: { en: "Initial draft", cn: "初稿" },
      },
      {
        rev: "2.0",
        date: "2026-03-15",
        author: "Lon Dailey",
        change: {
          en: "Revised per FDA Pre-Sub guidance; updated predicate strategy",
          cn: "根据FDA Pre-Sub指南修订；更新前置器械策略",
        },
      },
    ],
  },
  {
    id: "doc-2",
    dcn: "DCN-REG-002",
    cat: "regulatory",
    name: { en: "FDA Pre-Sub Q-Meeting Minutes", cn: "FDA预提交Q会议纪要" },
    version: "1.0",
    date: "2026-03-01",
    owner: "Lon Dailey",
    status: "draft",
    effectiveDate: "",
    nextReview: "2026-04-01",
    linkedMilestone: "R2",
    revisions: [
      {
        rev: "1.0",
        date: "2026-03-01",
        author: "Lon Dailey",
        change: { en: "Draft pending meeting", cn: "待会议草稿" },
      },
    ],
  },
  {
    id: "doc-3",
    dcn: "DCN-REG-003",
    cat: "regulatory",
    name: { en: "Predicate Device Comparison (IKN)", cn: "前置器械对比(IKN)" },
    version: "1.1",
    date: "2026-03-10",
    owner: "Lon Dailey",
    status: "in-review",
    effectiveDate: "",
    nextReview: "2026-04-10",
    linkedMilestone: "R3",
    revisions: [
      {
        rev: "1.0",
        date: "2026-02-20",
        author: "Lon Dailey",
        change: { en: "Initial comparison K082437", cn: "初始比较K082437" },
      },
      {
        rev: "1.1",
        date: "2026-03-10",
        author: "Lon Dailey",
        change: {
          en: "Added Timpel Enlight DQS for EIT module",
          cn: "添加Timpel Enlight DQS用于EIT模块",
        },
      },
    ],
  },
  {
    id: "doc-4",
    dcn: "DCN-TECH-001",
    cat: "technical",
    name: { en: "sEMG Module Design Specification", cn: "sEMG模块设计规格" },
    version: "3.0",
    date: "2026-03-12",
    owner: "Dr. Dai",
    status: "effective",
    effectiveDate: "2026-03-12",
    nextReview: "2026-06-12",
    linkedMilestone: "T1",
    revisions: [
      {
        rev: "1.0",
        date: "2025-10-01",
        author: "Dr. Dai",
        change: { en: "Initial design spec", cn: "初始设计规格" },
      },
      {
        rev: "2.0",
        date: "2026-01-15",
        author: "Dr. Dai",
        change: {
          en: "Updated electrode array (4→8 channel option)",
          cn: "更新电极阵列（4→8通道选项）",
        },
      },
      {
        rev: "3.0",
        date: "2026-03-12",
        author: "Dr. Dai",
        change: { en: "Production-intent design freeze", cn: "生产级设计冻结" },
      },
    ],
  },
  {
    id: "doc-5",
    dcn: "DCN-TECH-002",
    cat: "technical",
    name: {
      en: "ECG-Gating Algorithm Technical Report",
      cn: "ECG门控算法技术报告",
    },
    version: "1.2",
    date: "2026-03-18",
    owner: "Dr. Dai",
    status: "in-review",
    effectiveDate: "",
    nextReview: "2026-04-18",
    linkedMilestone: "T2",
    revisions: [
      {
        rev: "1.0",
        date: "2026-02-01",
        author: "Dr. Dai",
        change: {
          en: "Algorithm description and bench data",
          cn: "算法描述和台架数据",
        },
      },
      {
        rev: "1.2",
        date: "2026-03-18",
        author: "Dr. Dai",
        change: {
          en: "Updated suppression to 97.5%; added 30-patient dataset results",
          cn: "更新抑制率至97.5%；添加30例患者数据集结果",
        },
      },
    ],
  },
  {
    id: "doc-6",
    dcn: "DCN-TECH-003",
    cat: "technical",
    name: { en: "MyoBus Protocol Specification", cn: "MyoBus协议规范" },
    version: "2.1",
    date: "2026-03-05",
    owner: "Dr. Dai",
    status: "effective",
    effectiveDate: "2026-03-05",
    nextReview: "2026-06-05",
    linkedMilestone: "T8",
    revisions: [
      {
        rev: "1.0",
        date: "2025-11-01",
        author: "Dr. Dai",
        change: { en: "Initial protocol design", cn: "初始协议设计" },
      },
      {
        rev: "2.1",
        date: "2026-03-05",
        author: "Dr. Dai",
        change: {
          en: "Added FHIR output module; AES-256 encryption spec",
          cn: "添加FHIR输出模块；AES-256加密规范",
        },
      },
    ],
  },
  {
    id: "doc-7",
    dcn: "DCN-TECH-004",
    cat: "technical",
    name: { en: "EIT Belt Hardware Design Doc", cn: "EIT电极带硬件设计文档" },
    version: "1.0",
    date: "2026-02-28",
    owner: "Dr. Dai",
    status: "draft",
    effectiveDate: "",
    nextReview: "2026-05-28",
    linkedMilestone: "T5",
    revisions: [
      {
        rev: "1.0",
        date: "2026-02-28",
        author: "Dr. Dai",
        change: {
          en: "Initial 32-electrode belt design",
          cn: "初始32电极带设计",
        },
      },
    ],
  },
  {
    id: "doc-10",
    dcn: "DCN-BIZ-001",
    cat: "business",
    name: {
      en: "Phase 1 Seed Round Term Sheet Template",
      cn: "第一阶段种子轮条款清单模板",
    },
    version: "1.0",
    date: "2026-03-08",
    owner: "Lawrence Liu",
    status: "approved",
    effectiveDate: "",
    nextReview: "2026-06-08",
    linkedMilestone: "",
    revisions: [
      {
        rev: "1.0",
        date: "2026-03-08",
        author: "Lawrence Liu",
        change: { en: "Template for $1.8M seed round", cn: "$1.8M种子轮模板" },
      },
    ],
  },
  {
    id: "doc-11",
    dcn: "DCN-LEG-001",
    cat: "legal",
    name: {
      en: "sEMG IP Assignment Agreement (CN→US)",
      cn: "sEMG IP转让协议(中国→美国)",
    },
    version: "2.0",
    date: "2026-02-15",
    owner: "Lawrence Liu",
    status: "effective",
    effectiveDate: "2026-02-15",
    nextReview: "2026-08-15",
    linkedMilestone: "R8",
    revisions: [
      {
        rev: "1.0",
        date: "2025-12-01",
        author: "Lawrence Liu",
        change: { en: "Initial IP transfer framework", cn: "初始IP转让框架" },
      },
      {
        rev: "2.0",
        date: "2026-02-15",
        author: "Lawrence Liu",
        change: {
          en: "Scoped to sEMG only; EIT deferred to Series A",
          cn: "范围限sEMG；EIT推迟至A轮",
        },
      },
    ],
  },
  {
    id: "doc-12",
    dcn: "DCN-LEG-002",
    cat: "legal",
    name: {
      en: "Company B USA — Delaware C-Corp Filing",
      cn: "B公司美国 — 特拉华州C-Corp注册",
    },
    version: "1.0",
    date: "2025-09-01",
    owner: "Lon Dailey",
    status: "effective",
    effectiveDate: "2025-09-01",
    nextReview: "2026-09-01",
    linkedMilestone: "R8",
    revisions: [
      {
        rev: "1.0",
        date: "2025-09-01",
        author: "Lon Dailey",
        change: { en: "Incorporation filing", cn: "公司注册" },
      },
    ],
  },
  {
    id: "doc-13",
    dcn: "DCN-FIN-001",
    cat: "finance",
    name: {
      en: "Monthly Burn Report — March 2026",
      cn: "月度燃烧报告 — 2026年3月",
    },
    version: "1.0",
    date: "2026-03-22",
    owner: "Danielle Liu",
    status: "effective",
    effectiveDate: "2026-03-22",
    nextReview: "2026-04-22",
    linkedMilestone: "",
    revisions: [
      {
        rev: "1.0",
        date: "2026-03-22",
        author: "Danielle Liu",
        change: {
          en: "March actuals: $45K burn, $1.8M cash",
          cn: "3月实际：$45K消耗，$1.8M现金",
        },
      },
    ],
  },
  {
    id: "doc-14",
    dcn: "DCN-FIN-002",
    cat: "finance",
    name: { en: "Budget vs. Actual YTD", cn: "预算vs实际 年初至今" },
    version: "3.0",
    date: "2026-03-20",
    owner: "Danielle Liu",
    status: "in-review",
    effectiveDate: "",
    nextReview: "2026-04-20",
    linkedMilestone: "",
    revisions: [
      {
        rev: "1.0",
        date: "2026-01-15",
        author: "Danielle Liu",
        change: { en: "Q1 initial budget", cn: "Q1初始预算" },
      },
      {
        rev: "3.0",
        date: "2026-03-20",
        author: "Danielle Liu",
        change: {
          en: "Updated with $1.8M seed inflow",
          cn: "更新$1.8M种子资金流入",
        },
      },
    ],
  },
  {
    id: "doc-15",
    dcn: "DCN-TPL-001",
    cat: "templates",
    name: { en: "Monthly Investor Update Template", cn: "月度投资者更新模板" },
    version: "1.0",
    date: "2026-02-01",
    owner: "Lon Dailey",
    status: "effective",
    effectiveDate: "2026-02-01",
    nextReview: "2026-08-01",
    linkedMilestone: "",
    revisions: [
      {
        rev: "1.0",
        date: "2026-02-01",
        author: "Lon Dailey",
        change: { en: "Standardized template", cn: "标准化模板" },
      },
    ],
  },
  {
    id: "doc-16",
    dcn: "DCN-TPL-002",
    cat: "templates",
    name: { en: "Gate Review Checklist", cn: "门控审查清单" },
    version: "1.0",
    date: "2026-01-15",
    owner: "Lon Dailey",
    status: "effective",
    effectiveDate: "2026-01-15",
    nextReview: "2026-07-15",
    linkedMilestone: "",
    revisions: [
      {
        rev: "1.0",
        date: "2026-01-15",
        author: "Lon Dailey",
        change: {
          en: "6-gate checklist per ISO 13485 design controls",
          cn: "按ISO 13485设计控制的6门控清单",
        },
      },
    ],
  },
  {
    id: "doc-17",
    dcn: "DCN-REG-004",
    cat: "regulatory",
    name: { en: "Dashboard Users Guide (EN)", cn: "仪表盘用户指南(英文)" },
    version: "1.1",
    date: "2026-03-22",
    owner: "Lon Dailey",
    status: "draft",
    effectiveDate: "",
    nextReview: "2026-04-22",
    linkedMilestone: "",
    revisions: [
      {
        rev: "1.0",
        date: "2026-03-15",
        author: "Lon Dailey",
        change: { en: "Initial guide", cn: "初始指南" },
      },
      {
        rev: "1.1",
        date: "2026-03-22",
        author: "Lon Dailey",
        change: {
          en: "Added document control tab instructions",
          cn: "添加文档控制页签说明",
        },
      },
    ],
  },
  {
    id: "doc-18",
    dcn: "DCN-REG-005",
    cat: "regulatory",
    name: { en: "Dashboard Users Guide (CN)", cn: "仪表盘用户指南(中文)" },
    version: "1.1",
    date: "2026-03-22",
    owner: "Lon Dailey",
    status: "draft",
    effectiveDate: "",
    nextReview: "2026-04-22",
    linkedMilestone: "",
    revisions: [
      {
        rev: "1.0",
        date: "2026-03-15",
        author: "Lon Dailey",
        change: { en: "Initial guide (CN)", cn: "初始指南（中文）" },
      },
      {
        rev: "1.1",
        date: "2026-03-22",
        author: "Lon Dailey",
        change: {
          en: "Added document control tab instructions (CN)",
          cn: "添加文档控制页签说明（中文）",
        },
      },
    ],
  },
];

let docActiveFilter = "all";

function loadDocLibDocs(): DocLibItem[] {
  try {
    const raw = localStorage.getItem(DOCLIB_STORAGE_KEY);
    if (!raw) return [...DEFAULT_DOCS];
    const parsed = JSON.parse(raw) as DocLibItem[];
    // Migrate old format: add missing fields
    return parsed.map((d) => ({
      ...{
        dcn: "",
        effectiveDate: "",
        nextReview: "",
        linkedMilestone: "",
        revisions: [] as any[],
      },
      ...d,
    }));
  } catch {
    return [...DEFAULT_DOCS];
  }
}

function saveDocLibDocs(docs: DocLibItem[]): void {
  localStorage.setItem(DOCLIB_STORAGE_KEY, JSON.stringify(docs));
}

function deleteDocLibItem(id: string): void {
  if (ACTIVE_ROLE !== "pmp") return;
  if (!confirm(t("docLibConfirmRemove"))) return;
  const docs = loadDocLibDocs().filter((d) => d.id !== id);
  saveDocLibDocs(docs);
  renderDocLibTable();
}

const DOC_STATUS_ORDER: DocStatus[] = [
  "draft",
  "in-review",
  "approved",
  "effective",
  "obsolete",
];

function cycleDocStatus(id: string): void {
  if (ACTIVE_ROLE !== "pmp") return;
  const docs = loadDocLibDocs();
  const doc = docs.find((d) => d.id === id);
  if (!doc) return;
  const idx = DOC_STATUS_ORDER.indexOf(doc.status);
  const next = DOC_STATUS_ORDER[(idx + 1) % DOC_STATUS_ORDER.length];
  const prev = doc.status;
  doc.status = next;
  if (next === "effective" && !doc.effectiveDate) {
    doc.effectiveDate = new Date().toISOString().split("T")[0];
  }
  saveDocLibDocs(docs);
  logAudit(
    "doc-status" as AuditEntry["action"],
    id,
    "status",
    prev,
    next,
    `${localizedText(doc.name)}: ${prev} → ${next}`,
  );
  renderDocLibTable();
}

function openDocHistory(id: string): void {
  const docs = loadDocLibDocs();
  const doc = docs.find((d) => d.id === id);
  if (!doc) return;
  const overlay = document.getElementById("docHistoryOverlay");
  if (!overlay) return;
  overlay.innerHTML = `
    <div class="doc-history-panel">
      <div class="doc-history-header">
        <h3>${localizedText(doc.name)}</h3>
        <span class="doc-dcn-label">${doc.dcn}</span>
        <button class="modal-close" onclick="window._closeDocHistory()">✕</button>
      </div>
      <div class="doc-history-meta">
        <div><strong>${t("docLibOwner")}:</strong> ${doc.owner}</div>
        <div><strong>${t("docLibVersion")}:</strong> v${doc.version}</div>
        <div><strong>${t("docLibEffective")}:</strong> ${doc.effectiveDate || "—"}</div>
        <div><strong>${t("docLibNextReview")}:</strong> ${doc.nextReview || "—"}</div>
        <div><strong>${t("docLibLinked")}:</strong> ${doc.linkedMilestone || "—"}</div>
      </div>
      <h4 class="doc-history-subtitle">${t("docLibRevHistory")}</h4>
      <table class="standards-table doc-rev-table">
        <thead><tr>
          <th>${t("docLibRev")}</th>
          <th>${t("docLibDate")}</th>
          <th>${t("docLibAuthor")}</th>
          <th>${t("docLibChange")}</th>
        </tr></thead>
        <tbody>
          ${doc.revisions
            .map(
              (r) => `
            <tr>
              <td>v${r.rev}</td>
              <td>${r.date}</td>
              <td>${r.author}</td>
              <td>${localizedText(r.change)}</td>
            </tr>
          `,
            )
            .join("")}
          ${doc.revisions.length === 0 ? `<tr><td colspan="4" style="text-align:center; opacity:0.5">No revision history</td></tr>` : ""}
        </tbody>
      </table>
    </div>
  `;
  overlay.classList.add("open");
}

function closeDocHistory(): void {
  const overlay = document.getElementById("docHistoryOverlay");
  if (overlay) {
    overlay.classList.remove("open");
    overlay.innerHTML = "";
  }
}

function openAddDocForm(): void {
  const form = document.getElementById("docLibAddForm");
  if (!form) return;
  const cats = [
    "regulatory",
    "technical",
    "business",
    "legal",
    "finance",
    "templates",
  ];
  const catLabels: Record<string, string> = {
    regulatory: t("docLibCatRegulatory"),
    technical: t("docLibCatTechnical"),
    business: t("docLibCatBusiness"),
    legal: t("docLibCatLegal"),
    finance: t("docLibCatFinance"),
    templates: t("docLibCatTemplates"),
  };
  form.style.display = "block";
  form.innerHTML = `
    <h4 class="doc-form-title">${t("docLibFormTitle")}</h4>
    <div class="doc-form-grid">
      <label>${t("docLibFormName")}
        <input type="text" id="docFormName" class="doc-form-input" required />
      </label>
      <label>${t("docLibFormNameCn")}
        <input type="text" id="docFormNameCn" class="doc-form-input" />
      </label>
      <label>${t("docLibFormCat")}
        <select id="docFormCat" class="doc-form-input">
          ${cats.map((c) => `<option value="${c}">${catLabels[c]}</option>`).join("")}
        </select>
      </label>
      <label>${t("docLibFormVersion")}
        <input type="text" id="docFormVersion" class="doc-form-input" value="1.0" />
      </label>
      <label>${t("docLibFormOwner")}
        <input type="text" id="docFormOwner" class="doc-form-input" />
      </label>
      <label>${t("docLibLinked")}
        <input type="text" id="docFormLinked" class="doc-form-input" placeholder="e.g. R8, T2" />
      </label>
    </div>
    <div class="doc-form-actions">
      <button class="btn-primary" onclick="window._addDocLibItem()">${t("docLibFormAdd")}</button>
      <button class="btn-secondary" onclick="document.getElementById('docLibAddForm').style.display='none'">${t("docLibFormCancel")}</button>
    </div>
  `;
}

function addDocLibItem(): void {
  const nameEl = document.getElementById("docFormName") as HTMLInputElement;
  const nameCnEl = document.getElementById("docFormNameCn") as HTMLInputElement;
  const catEl = document.getElementById("docFormCat") as HTMLSelectElement;
  const versionEl = document.getElementById(
    "docFormVersion",
  ) as HTMLInputElement;
  const ownerEl = document.getElementById("docFormOwner") as HTMLInputElement;
  const linkedEl = document.getElementById("docFormLinked") as HTMLInputElement;

  if (!nameEl?.value.trim()) return;

  const docs = loadDocLibDocs();
  const cat = catEl.value;
  const catPrefixes: Record<string, string> = {
    regulatory: "REG",
    technical: "TECH",
    business: "BIZ",
    legal: "LEG",
    finance: "FIN",
    templates: "TPL",
  };
  const prefix = catPrefixes[cat] || "DOC";
  const catDocs = docs.filter((d) => d.dcn.includes(`-${prefix}-`));
  const nextNum = String(catDocs.length + 1).padStart(3, "0");
  const today = new Date().toISOString().split("T")[0];
  const ver = versionEl.value.trim() || "1.0";

  const newDoc: DocLibItem = {
    id: `doc-${Date.now()}-${Math.random().toString(36).slice(2, 6)}`,
    dcn: `DCN-${prefix}-${nextNum}`,
    cat,
    name: {
      en: nameEl.value.trim(),
      cn: nameCnEl?.value.trim() || nameEl.value.trim(),
    },
    version: ver,
    date: today,
    owner: ownerEl.value.trim() || "—",
    status: "draft",
    effectiveDate: "",
    nextReview: "",
    linkedMilestone: linkedEl?.value.trim() || "",
    revisions: [
      {
        rev: ver,
        date: today,
        author: ownerEl.value.trim() || "—",
        change: { en: "Initial draft", cn: "初稿" },
      },
    ],
  };
  docs.push(newDoc);
  saveDocLibDocs(docs);

  const form = document.getElementById("docLibAddForm");
  if (form) form.style.display = "none";
  renderDocLibTable();
}

function docStatusClass(s: string): string {
  switch (s) {
    case "effective":
      return "doc-status-effective";
    case "approved":
      return "doc-status-approved";
    case "in-review":
      return "doc-status-review";
    case "draft":
      return "doc-status-draft";
    default:
      return "doc-status-obsolete";
  }
}

function docStatusLabel(s: string): string {
  switch (s) {
    case "effective":
      return t("docLibEffectiveStatus");
    case "approved":
      return t("docLibApproved");
    case "in-review":
      return t("docLibInReview");
    case "draft":
      return t("docLibDraft");
    default:
      return t("docLibObsolete");
  }
}

function renderDocLibTable(): void {
  const tbody = document.getElementById("docLibBody");
  if (!tbody) return;

  const docs = loadDocLibDocs();
  const catLabel = (c: string) => {
    const map: Record<string, string> = {
      regulatory: t("docLibCatRegulatory"),
      technical: t("docLibCatTechnical"),
      business: t("docLibCatBusiness"),
      legal: t("docLibCatLegal"),
      finance: t("docLibCatFinance"),
      templates: t("docLibCatTemplates"),
    };
    return map[c] || c;
  };

  // Sort: effective first, then approved, in-review, draft, obsolete
  const statusOrder: Record<string, number> = {
    effective: 0,
    approved: 1,
    "in-review": 2,
    draft: 3,
    obsolete: 4,
  };
  const sorted = [...docs].sort((a, b) => {
    if (a.cat !== b.cat) return a.cat.localeCompare(b.cat);
    return (statusOrder[a.status] ?? 9) - (statusOrder[b.status] ?? 9);
  });

  // Check for overdue reviews
  const today = new Date().toISOString().split("T")[0];

  tbody.innerHTML = sorted
    .map((d) => {
      const overdue =
        d.nextReview && d.nextReview <= today && d.status !== "obsolete";
      return `
    <tr data-category="${d.cat}" class="${overdue ? "doc-overdue-row" : ""}">
      <td><span class="doc-cat-badge doc-cat-${d.cat}">${catLabel(d.cat)}</span></td>
      <td class="doc-dcn-cell">${d.dcn}</td>
      <td class="doc-name-cell">
        <button class="doc-name-link" onclick="window._openDocHistory('${d.id}')">${localizedText(d.name)}</button>
      </td>
      <td>v${d.version}</td>
      <td>${d.date}</td>
      <td>${d.owner}</td>
      <td>${d.linkedMilestone || "—"}</td>
      <td>
        <button class="doc-status-btn ${docStatusClass(d.status)}" onclick="window._cycleDocStatus('${d.id}')" title="${ACTIVE_ROLE === "pmp" ? t("clickToChangeStatus") : ""}">${docStatusLabel(d.status)}</button>
        ${overdue ? `<span class="doc-overdue-badge" title="${t("docLibOverdue")}">⚠</span>` : ""}
      </td>
      <td>${ACTIVE_ROLE === "pmp" ? `<button class="doc-remove-btn" onclick="window._deleteDocLibItem('${d.id}')" title="${t("docLibRemove")}">✕</button>` : ""}</td>
    </tr>`;
    })
    .join("");

  // Re-apply active filter
  if (docActiveFilter !== "all") {
    document
      .querySelectorAll<HTMLTableRowElement>("#docLibBody tr")
      .forEach((row) => {
        row.style.display =
          row.dataset.category === docActiveFilter ? "" : "none";
      });
  }

  // Update summary counters
  const summaryEl = document.getElementById("docControlSummary");
  if (summaryEl) {
    const total = docs.length;
    const eff = docs.filter((d) => d.status === "effective").length;
    const rev = docs.filter((d) => d.status === "in-review").length;
    const drafts = docs.filter((d) => d.status === "draft").length;
    const overdueCount = docs.filter(
      (d) => d.nextReview && d.nextReview <= today && d.status !== "obsolete",
    ).length;
    summaryEl.innerHTML = `
      <div class="doc-summary-item"><span class="doc-summary-num">${total}</span><span class="doc-summary-label">${t("docLibTotal")}</span></div>
      <div class="doc-summary-item doc-summary-effective"><span class="doc-summary-num">${eff}</span><span class="doc-summary-label">${t("docLibEffectiveStatus")}</span></div>
      <div class="doc-summary-item doc-summary-review"><span class="doc-summary-num">${rev}</span><span class="doc-summary-label">${t("docLibInReview")}</span></div>
      <div class="doc-summary-item doc-summary-draft"><span class="doc-summary-num">${drafts}</span><span class="doc-summary-label">${t("docLibDraft")}</span></div>
      ${overdueCount > 0 ? `<div class="doc-summary-item doc-summary-overdue"><span class="doc-summary-num">${overdueCount}</span><span class="doc-summary-label">${t("docLibOverdue")}</span></div>` : ""}
    `;
  }
}

function renderDocLibrary(): void {
  const filters = document.getElementById("docLibFilters");
  if (filters) {
    const cats = [
      "all",
      "regulatory",
      "technical",
      "business",
      "legal",
      "finance",
      "templates",
    ];
    const catLabels: Record<string, string> = {
      all: t("docLibFilterAll"),
      regulatory: t("docLibCatRegulatory"),
      technical: t("docLibCatTechnical"),
      business: t("docLibCatBusiness"),
      legal: t("docLibCatLegal"),
      finance: t("docLibCatFinance"),
      templates: t("docLibCatTemplates"),
    };
    filters.innerHTML = cats
      .map(
        (c) =>
          `<button class="filter-btn${c === docActiveFilter ? " active" : ""}" data-docfilter="${c}">${catLabels[c]}</button>`,
      )
      .join("");

    filters.addEventListener("click", (e) => {
      const btn = (e.target as HTMLElement).closest<HTMLButtonElement>(
        "[data-docfilter]",
      );
      if (!btn) return;
      const clicked = btn.dataset.docfilter!;
      // Toggle: clicking the active filter resets to "all"
      if (clicked === docActiveFilter && clicked !== "all") {
        docActiveFilter = "all";
      } else {
        docActiveFilter = clicked;
      }
      filters
        .querySelectorAll(".filter-btn")
        .forEach((b) => b.classList.remove("active"));
      const activeBtn = filters.querySelector(
        `[data-docfilter="${docActiveFilter}"]`,
      );
      if (activeBtn) activeBtn.classList.add("active");
      const rows =
        document.querySelectorAll<HTMLTableRowElement>("#docLibBody tr");
      rows.forEach((row) => {
        row.style.display =
          docActiveFilter === "all" || row.dataset.category === docActiveFilter
            ? ""
            : "none";
      });
    });
  }
  renderDocLibTable();
}

// Expose Document Control functions globally
(window as any)._deleteDocLibItem = deleteDocLibItem;
(window as any)._openAddDocForm = openAddDocForm;
(window as any)._addDocLibItem = addDocLibItem;
(window as any)._cycleDocStatus = cycleDocStatus;
(window as any)._openDocHistory = openDocHistory;
(window as any)._closeDocHistory = closeDocHistory;

// ══════════════════════════════════════════════════
// MESSAGE BOARD — Purpose-Driven Messaging Layer
// Threads with lifecycle, decisions, actions, accountability
// Supabase Realtime primary, localStorage fallback
// ══════════════════════════════════════════════════

const QA_STORAGE_KEY = "ctower_qa_messages";
const QA_SETTINGS_KEY = "ctower_qa_settings";
const MB_THREADS_KEY = "ctower_mb_threads";
const MB_DECISIONS_KEY = "ctower_mb_decisions";
let qaPostingRole: string = "pmp";
let qaCollapsed: Set<number> = new Set();
let qaTestMode = true;
let mbActiveView: MBView = "all";
let mbWorkstreamFilter: MBWorkstream | "all" = "all";
let mbLifecycleFilter: "open" | "all" | "resolved" = "open";

// ── Role display helpers ──────────────────────
function qaRoleLabel(role: string): string {
  switch (role) {
    case "pmp":
      return t("qaPmp");
    case "technology":
    case "inventor":
    case "tech":
      return t("qaInventor");
    case "business":
      return t("qaBusiness");
    case "accounting":
      return t("qaAccounting");
    default:
      return role;
  }
}
function qaRoleIcon(role: string): string {
  switch (role) {
    case "pmp":
      return "\ud83c\udfaf";
    case "technology":
    case "inventor":
    case "tech":
      return "\ud83d\udd2c";
    case "business":
      return "\ud83d\udcbc";
    case "accounting":
      return "\ud83d\udcca";
    default:
      return "\ud83d\udcac";
  }
}
function normalizeRole(role: string): string {
  return role === "inventor"
    ? "technology"
    : role === "tech"
      ? "technology"
      : role;
}

// ── Thread persistence ────────────────────────
function loadMBThreads(): MBThread[] {
  try {
    const raw = localStorage.getItem(MB_THREADS_KEY);
    return raw ? JSON.parse(raw) : [];
  } catch {
    return [];
  }
}
function saveMBThreads(threads: MBThread[]): void {
  localStorage.setItem(MB_THREADS_KEY, JSON.stringify(threads));
}

function loadMBDecisions(): MBDecision[] {
  try {
    const raw = localStorage.getItem(MB_DECISIONS_KEY);
    return raw ? JSON.parse(raw) : [];
  } catch {
    return [];
  }
}
function saveMBDecisions(decisions: MBDecision[]): void {
  localStorage.setItem(MB_DECISIONS_KEY, JSON.stringify(decisions));
}

// Migrate predefined Q1-Q30 + custom topics into threads if first run
function ensureDefaultThreads(): void {
  let threads = loadMBThreads();
  if (threads.length > 0) return;

  // Create default workstream threads from QA_SECTIONS
  const wsMap: Record<number, MBWorkstream> = {
    1: "engineering",
    2: "engineering",
    3: "business",
    4: "regulatory",
    5: "project",
    6: "operations",
    7: "clinical",
    8: "business",
  };
  QA_SECTIONS.forEach((sec) => {
    sec.questions.forEach((q) => {
      threads.push({
        id: q.num,
        title: localizedText(q.question),
        workstream: wsMap[sec.num] ?? "project",
        intent: "inform",
        owner: "pmp",
        objective: q.why ? localizedText(q.why) : "",
        lifecycle: "open",
        priority: "normal",
        linkedItems: [],
        createdAt: new Date().toISOString(),
      });
    });
  });

  // Migrate custom topics
  try {
    const raw = localStorage.getItem("ctower_qa_custom_topics");
    if (raw) {
      const topics: Array<{ qNum: number; title: string; createdAt: string }> =
        JSON.parse(raw);
      topics.forEach((tp) => {
        threads.push({
          id: tp.qNum,
          title: tp.title,
          workstream: "project",
          intent: "inform",
          owner: qaPostingRole,
          objective: "",
          lifecycle: "open",
          priority: "normal",
          linkedItems: [],
          createdAt: tp.createdAt,
        });
      });
    }
  } catch {
    /* ignore */
  }

  saveMBThreads(threads);
}

// ── Supabase ↔ localStorage message cache ─────────────
let _qaCache: QAMessage[] = [];

function dbToQa(db: DbMessage): QAMessage {
  return {
    id: db.id,
    qNum: db.q_num,
    sender: db.sender,
    text: db.text,
    timestamp: db.created_at,
    readBy: db.read_by ?? [],
  };
}

function loadQaMessagesLocal(): QAMessage[] {
  try {
    const raw = localStorage.getItem(QA_STORAGE_KEY);
    return raw ? JSON.parse(raw) : [];
  } catch {
    return [];
  }
}

function saveQaMessagesLocal(msgs: QAMessage[]): void {
  localStorage.setItem(QA_STORAGE_KEY, JSON.stringify(msgs));
}

async function initQaMessages(): Promise<void> {
  ensureDefaultThreads();
  if (isOnline()) {
    try {
      const rows = await fetchMessages();
      _qaCache = rows.map(dbToQa);
      saveQaMessagesLocal(_qaCache);
    } catch {
      _qaCache = loadQaMessagesLocal();
    }
  } else {
    _qaCache = loadQaMessagesLocal();
  }
}

async function syncOfflineMessages(): Promise<void> {
  if (!isOnline()) return;
  const localMsgs = loadQaMessagesLocal();
  const remoteIds = new Set(_qaCache.map((m) => m.id));
  for (const m of localMsgs) {
    if (!remoteIds.has(m.id)) {
      await insertMessage({
        q_num: m.qNum,
        sender: m.sender,
        text: m.text,
        read_by: m.readBy ?? [],
      });
    }
  }
}

// ── Settings ─────────────────────────────────
function loadQaSettings(): QASettings {
  try {
    const raw = localStorage.getItem(QA_SETTINGS_KEY);
    if (raw) {
      const parsed = JSON.parse(raw);
      return {
        pmpEmail: parsed.pmpEmail ?? "",
        technologyEmail:
          parsed.technologyEmail ??
          parsed.inventorEmail ??
          "uniquedai@gmail.com",
        businessEmail: parsed.businessEmail ?? "lawrenceliu@enzhi.org",
        accountingEmail: parsed.accountingEmail ?? "",
      };
    }
    return {
      pmpEmail: "",
      technologyEmail: "uniquedai@gmail.com",
      businessEmail: "lawrenceliu@enzhi.org",
      accountingEmail: "",
    };
  } catch {
    return {
      pmpEmail: "",
      technologyEmail: "uniquedai@gmail.com",
      businessEmail: "lawrenceliu@enzhi.org",
      accountingEmail: "",
    };
  }
}

function saveQaSettingsData(settings: QASettings): void {
  localStorage.setItem(QA_SETTINGS_KEY, JSON.stringify(settings));
}

function openQaSettings(): void {
  const panel = document.getElementById("qaSettingsPanel");
  if (!panel) return;
  const settings = loadQaSettings();
  panel.style.display = "block";
  panel.innerHTML = `
    <h4 class="qa-settings-title">${t("qaSettingsTitle")}</h4>
    <div class="qa-settings-grid">
      <label class="qa-settings-label">\ud83c\udfaf ${t("qaPmpEmail")}
        <input type="email" id="qaSettingsPmpEmail" class="qa-settings-input" value="${settings.pmpEmail.replace(/"/g, "&quot;")}" placeholder="pmp@example.com" />
      </label>
      <label class="qa-settings-label">\ud83d\udd2c ${t("qaTechnologyEmail")}
        <input type="email" id="qaSettingsTechnologyEmail" class="qa-settings-input" value="${settings.technologyEmail.replace(/"/g, "&quot;")}" placeholder="uniquedai@gmail.com" />
      </label>
      <label class="qa-settings-label">\ud83d\udcbc ${t("qaBusinessEmail")}
        <input type="email" id="qaSettingsBusinessEmail" class="qa-settings-input" value="${settings.businessEmail.replace(/"/g, "&quot;")}" placeholder="lawrenceliu@enzhi.org" />
      </label>
      <label class="qa-settings-label">\ud83d\udcca ${t("qaAccountingEmail")}
        <input type="email" id="qaSettingsAccountingEmail" class="qa-settings-input" value="${settings.accountingEmail.replace(/"/g, "&quot;")}" placeholder="" />
      </label>
    </div>
    <div class="qa-settings-actions">
      <button class="btn-primary" onclick="window._saveQaSettings()">${t("qaSettingsSave")}</button>
      <span class="qa-settings-separator">|</span>
      <button class="btn-secondary" onclick="document.getElementById('qaSettingsPanel').style.display='none'">${t("qaSettingsCancel")}</button>
    </div>
    <div class="qa-test-mode-row">
      <label class="qa-test-toggle">
        <input type="checkbox" id="qaTestModeToggle" ${qaTestMode ? "checked" : ""} onchange="window._toggleQaTestMode(this.checked)" />
        <span>${qaTestMode ? t("qaTestModeOn") : t("qaTestModeOff")}</span>
      </label>
      ${qaTestMode ? `<span class="qa-test-badge">${t("qaTestMode")}</span>` : ""}
    </div>
  `;
}

function saveQaSettingsUI(): void {
  const pmpEl = document.getElementById(
    "qaSettingsPmpEmail",
  ) as HTMLInputElement;
  const techEl = document.getElementById(
    "qaSettingsTechnologyEmail",
  ) as HTMLInputElement;
  const bizEl = document.getElementById(
    "qaSettingsBusinessEmail",
  ) as HTMLInputElement;
  const acctEl = document.getElementById(
    "qaSettingsAccountingEmail",
  ) as HTMLInputElement;
  if (!pmpEl || !techEl || !bizEl || !acctEl) return;
  saveQaSettingsData({
    pmpEmail: pmpEl.value.trim(),
    technologyEmail: techEl.value.trim(),
    businessEmail: bizEl.value.trim(),
    accountingEmail: acctEl.value.trim(),
  });
  const panel = document.getElementById("qaSettingsPanel");
  if (panel) panel.style.display = "none";
  showQaSaveStatus();
}

// ── Message operations ───────────────────────
function markQaRead(msgId: string): void {
  const msg = _qaCache.find((m) => m.id === msgId);
  if (!msg) return;
  if (!msg.readBy) msg.readBy = [];
  const role = normalizeRole(qaPostingRole);
  if (!msg.readBy.includes(role)) {
    msg.readBy.push(role);
    saveQaMessagesLocal(_qaCache);
    if (isOnline()) markMessageRead(msgId, role);
    renderQaThread(msg.qNum);
    updateQaUnreadBadge();
  }
}

function sendQaMessage(threadId: number): void {
  const input = document.getElementById(
    `qa-input-${threadId}`,
  ) as HTMLTextAreaElement | null;
  if (!input || !input.value.trim()) return;

  const text = input.value.trim();
  const role = normalizeRole(qaPostingRole);

  // Detect intent markers: [DECISION] or [ACTION] prefix
  let intentTag = "";
  if (text.match(/^\[DECISION\]/i)) intentTag = "decision";
  else if (text.match(/^\[ACTION\]/i)) intentTag = "action";

  const localMsg: QAMessage = {
    id: `qm-${Date.now()}-${Math.random().toString(36).slice(2, 6)}`,
    qNum: threadId,
    sender: role,
    text,
    timestamp: new Date().toISOString(),
    readBy: [role],
  };

  _qaCache.push(localMsg);
  saveQaMessagesLocal(_qaCache);
  input.value = "";
  renderQaThread(threadId);
  showQaSaveStatus();
  updateQaUnreadBadge();

  // Auto-log decision if tagged
  if (intentTag === "decision") {
    const decisions = loadMBDecisions();
    decisions.push({
      id: `dec-${Date.now()}`,
      threadId,
      text: text.replace(/^\[DECISION\]\s*/i, ""),
      rationale: "",
      madeBy: role,
      date: new Date().toISOString(),
      linkedItems: [],
      status: "active",
    });
    saveMBDecisions(decisions);
    logAudit(
      "qa-topic",
      String(threadId),
      "decision",
      "",
      text.replace(/^\[DECISION\]\s*/i, ""),
      `Decision logged in thread ${threadId}`,
    );
  }

  if (isOnline()) {
    insertMessage({
      q_num: threadId,
      sender: role,
      text,
      read_by: [role],
    }).then((dbMsg) => {
      if (dbMsg) {
        const idx = _qaCache.findIndex((m) => m.id === localMsg.id);
        if (idx !== -1) {
          _qaCache[idx] = dbToQa(dbMsg);
          saveQaMessagesLocal(_qaCache);
          renderQaThread(threadId);
        }
      }
    });
  }
}

function showQaSaveStatus(): void {
  const status = document.getElementById("qaSaveStatus");
  if (status) {
    const now = new Date();
    const time = now.toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit",
    });
    status.textContent = `${t("qaSaved")} \u2014 ${time}`;
    status.classList.add("qa-status-flash");
    setTimeout(() => status.classList.remove("qa-status-flash"), 1500);
  }
}

function formatMsgTime(iso: string): string {
  const d = new Date(iso);
  const date = d.toLocaleDateString(undefined, {
    month: "short",
    day: "numeric",
  });
  const time = d.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
  return `${date}, ${time}`;
}

// ── Thread rendering ─────────────────────────
function renderQaThread(threadId: number): void {
  const container = document.getElementById(`qa-thread-${threadId}`);
  if (!container) return;

  const msgs = _qaCache.filter((m) => m.qNum === threadId);
  if (msgs.length === 0) {
    container.innerHTML = `<div class="qa-no-messages">${t("qaNoMessages")}</div>`;
    return;
  }

  container.innerHTML = msgs
    .map((m) => {
      const senderNorm = normalizeRole(m.sender);
      const isSelf = senderNorm === normalizeRole(qaPostingRole);
      const senderLabel = qaRoleLabel(m.sender);
      const icon = qaRoleIcon(m.sender);
      const isReadByViewer =
        m.readBy?.includes(normalizeRole(qaPostingRole)) ?? false;
      const isReadBySomeone =
        senderNorm === normalizeRole(qaPostingRole)
          ? (m.readBy ?? []).some(
              (r) => normalizeRole(r) !== normalizeRole(qaPostingRole),
            )
          : false;
      const readIndicator =
        senderNorm === normalizeRole(qaPostingRole)
          ? isReadBySomeone
            ? `<span class="qa-read-badge qa-read">\u2713\u2713 ${t("qaRead")}</span>`
            : `<span class="qa-read-badge qa-unread">\u2713 ${t("qaUnread")}</span>`
          : "";
      const unreadClass =
        !isReadByViewer && senderNorm !== normalizeRole(qaPostingRole)
          ? " qa-msg-unread"
          : "";
      const markReadBtn =
        !isReadByViewer && senderNorm !== normalizeRole(qaPostingRole)
          ? `<button class="qa-mark-read-btn" onclick="window._markQaRead('${m.id}')" title="${t("qaMarkRead")}">&#x2709;</button>`
          : "";

      // Highlight decisions and actions
      const isDecision = m.text.match(/^\[DECISION\]/i);
      const isAction = m.text.match(/^\[ACTION\]/i);
      const intentClass = isDecision
        ? " qa-msg-decision"
        : isAction
          ? " qa-msg-action"
          : "";
      const intentBadge = isDecision
        ? `<span class="mb-intent-badge mb-intent-decide">⚖️ ${t("mbDecision")}</span>`
        : isAction
          ? `<span class="mb-intent-badge mb-intent-act">⚡ ${t("mbAction")}</span>`
          : "";

      return `
    <div class="qa-msg ${isSelf ? "qa-msg-self" : "qa-msg-other"} qa-msg-${senderNorm}${unreadClass}${intentClass}">
      <div class="qa-msg-header">
        <span class="qa-msg-sender">${icon} ${senderLabel}</span>
        ${intentBadge}
        <span class="qa-msg-meta">${readIndicator}${markReadBtn}<span class="qa-msg-time">${formatMsgTime(m.timestamp)}</span></span>
      </div>
      <div class="qa-msg-body">${m.text.replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/\n/g, "<br>")}</div>
    </div>`;
    })
    .join("");

  container.scrollTop = container.scrollHeight;
}

// ── Thread card HTML ──────────────────────────
function threadCardHtml(thread: MBThread): string {
  const msgs = _qaCache.filter((m) => m.qNum === thread.id);
  const msgCount = msgs.length;
  const myRole = normalizeRole(qaPostingRole);
  const unreadCount = msgs.filter(
    (m) => normalizeRole(m.sender) !== myRole && !m.readBy?.includes(myRole),
  ).length;
  const isCollapsed = qaCollapsed.has(thread.id);
  const decisions = loadMBDecisions().filter(
    (d) => d.threadId === thread.id && d.status === "active",
  );

  const intentIcon =
    thread.intent === "decide" ? "⚖️" : thread.intent === "act" ? "⚡" : "📢";
  const priorityClass =
    thread.priority === "urgent"
      ? "mb-priority-urgent"
      : thread.priority === "escalated"
        ? "mb-priority-escalated"
        : "";
  const lifecycleClass = thread.lifecycle === "resolved" ? "mb-resolved" : "";
  const ownerLabel = qaRoleLabel(thread.owner);

  // Linked items badges
  const linkedHtml =
    thread.linkedItems.length > 0
      ? `<div class="mb-linked">${thread.linkedItems.map((li) => `<span class="mb-linked-badge" title="${li.label}">${li.type === "milestone" ? "🏁" : li.type === "risk" ? "⚠️" : li.type === "gate" ? "🚦" : li.type === "document" ? "📄" : li.type === "standard" ? "📋" : "📌"} ${li.label}</span>`).join("")}</div>`
      : "";

  // Action status indicator
  const actionHtml = thread.assignee
    ? `<div class="mb-action-meta">
        <span class="mb-assignee">👤 ${qaRoleLabel(thread.assignee)}</span>
        ${thread.dueDate ? `<span class="mb-due">📅 ${thread.dueDate}</span>` : ""}
      </div>`
    : "";

  // Decision summary
  const decisionHtml =
    decisions.length > 0
      ? `<div class="mb-decisions-list">${decisions
          .map(
            (d) =>
              `<div class="mb-decision-card"><span class="mb-decision-icon">⚖️</span> <strong>${d.text}</strong> <span class="mb-decision-by">— ${qaRoleLabel(d.madeBy)}, ${formatMsgTime(d.date)}</span></div>`,
          )
          .join("")}</div>`
      : "";

  // Thread actions row
  const isPmp = qaPostingRole === "pmp";
  const actionsHtml = `<div class="mb-thread-actions">
    ${thread.lifecycle === "open" ? `<button class="mb-action-btn mb-btn-resolve" onclick="window._mbResolveThread(${thread.id})" title="${t("mbResolve")}">✅ ${t("mbResolve")}</button>` : ""}
    ${thread.lifecycle === "resolved" ? `<button class="mb-action-btn" onclick="window._mbReopenThread(${thread.id})" title="${t("mbReopen")}">🔄 ${t("mbReopen")}</button>` : ""}
    <button class="mb-action-btn" onclick="window._mbLogDecision(${thread.id})" title="${t("mbLogDecision")}">⚖️ ${t("mbLogDecision")}</button>
    <button class="mb-action-btn" onclick="window._mbCreateAction(${thread.id})" title="${t("mbCreateAction")}">⚡ ${t("mbCreateAction")}</button>
    <button class="mb-action-btn" onclick="window._mbLinkItem(${thread.id})" title="${t("mbLinkArtifact")}">🔗 ${t("mbLinkArtifact")}</button>
    ${msgCount > 0 ? `<button class="mb-action-btn" onclick="window._archiveQaMessages(${thread.id})" title="${t("qaArchive")}">📦</button>` : ""}
    ${isPmp ? `<button class="mb-action-btn mb-btn-delete" onclick="window._mbDeleteThread(${thread.id})" title="${t("mbDelete")}">🗑️</button>` : ""}
  </div>`;

  return `
  <div class="mb-thread-card ${priorityClass} ${lifecycleClass}" id="qa-topic-${thread.id}">
    <div class="mb-thread-header">
      <div class="mb-thread-left">
        <span class="mb-intent-icon">${intentIcon}</span>
        <div class="mb-thread-title-group">
          <span class="mb-thread-title">${thread.title}</span>
          <div class="mb-thread-meta">
            <span class="mb-ws-badge mb-ws-${thread.workstream}">${t("mbWs_" + thread.workstream)}</span>
            <span class="mb-owner">${ownerLabel}</span>
            ${thread.priority !== "normal" ? `<span class="mb-priority-badge ${priorityClass}">${thread.priority === "urgent" ? "🔴 " + t("mbUrgent") : "🚨 " + t("mbEscalated")}</span>` : ""}
            ${thread.lifecycle === "resolved" ? `<span class="mb-lifecycle-badge mb-status-resolved">✅ ${t("mbResolved")}</span>` : `<span class="mb-lifecycle-badge mb-status-open">🟢 ${t("mbOpen")}</span>`}
          </div>
        </div>
      </div>
      <div class="mb-thread-right">
        <span class="qa-msg-count">${msgCount > 0 ? `💬 ${msgCount}${unreadCount > 0 ? ` (${unreadCount} ${t("qaUnread")})` : ""}` : ""}</span>
        <button class="qa-collapse-btn" data-qatoggle="${thread.id}">${isCollapsed ? t("qaExpand") : t("qaCollapse")}</button>
      </div>
    </div>
    ${thread.objective ? `<div class="mb-thread-objective">${thread.objective}</div>` : ""}
    ${linkedHtml}
    ${actionHtml}
    ${thread.resolutionSummary ? `<div class="mb-resolution">✅ <strong>${t("mbResolution")}:</strong> ${thread.resolutionSummary}</div>` : ""}
    ${decisionHtml}
    <div class="qa-thread-wrap${isCollapsed ? " collapsed" : ""}" id="qa-wrap-${thread.id}">
      <div class="qa-thread" id="qa-thread-${thread.id}"></div>
      ${
        thread.lifecycle === "open"
          ? `<div class="qa-compose">
        <div class="mb-compose-hints">${t("mbComposeHint")}</div>
        <textarea id="qa-input-${thread.id}" class="qa-compose-input" rows="2" placeholder="${t("qaAnswerPlaceholder")}"></textarea>
        <div class="qa-compose-actions">
          <button class="qa-send-btn" onclick="window._sendQaMessage(${thread.id})">${t("qaSend")} \u27a4</button>
        </div>
      </div>`
          : ""
      }
    </div>
    ${actionsHtml}
  </div>`;
}

// ── Summary cards ─────────────────────────────
function renderMBSummary(): void {
  const el = document.getElementById("mbSummary");
  if (!el) return;
  const threads = loadMBThreads();
  const decisions = loadMBDecisions();
  const myRole = normalizeRole(qaPostingRole);

  const openCount = threads.filter((th) => th.lifecycle === "open").length;
  const urgentCount = threads.filter(
    (th) => th.lifecycle === "open" && th.priority !== "normal",
  ).length;
  const decisionCount = decisions.filter((d) => d.status === "active").length;
  const myItems = threads.filter(
    (th) =>
      th.lifecycle === "open" &&
      (th.owner === myRole || th.assignee === myRole),
  ).length;
  const unreadMsgs = _qaCache.filter(
    (m) => normalizeRole(m.sender) !== myRole && !m.readBy?.includes(myRole),
  ).length;

  el.innerHTML = `
    <div class="mb-summary-card"><div class="mb-summary-value">${openCount}</div><div class="mb-summary-label">${t("mbOpen")} ${t("mbThreads")}</div></div>
    <div class="mb-summary-card ${urgentCount > 0 ? "mb-summary-urgent" : ""}"><div class="mb-summary-value">${urgentCount}</div><div class="mb-summary-label">${t("mbUrgent")} / ${t("mbEscalated")}</div></div>
    <div class="mb-summary-card"><div class="mb-summary-value">${decisionCount}</div><div class="mb-summary-label">${t("mbDecisions")}</div></div>
    <div class="mb-summary-card"><div class="mb-summary-value">${myItems}</div><div class="mb-summary-label">${t("mbViewMyItems")}</div></div>
    <div class="mb-summary-card ${unreadMsgs > 0 ? "mb-summary-unread" : ""}"><div class="mb-summary-value">${unreadMsgs}</div><div class="mb-summary-label">${t("qaUnread")}</div></div>
  `;
}

// ── Export ─────────────────────────────────────
function exportQaThread(): void {
  const threads = loadMBThreads();
  const decisions = loadMBDecisions();
  const lines: string[] = [
    "ICU Respiratory Digital Twin \u2014 Message Board Export",
    `Exported: ${new Date().toISOString().split("T")[0]}`,
    "=".repeat(60),
    "",
  ];

  // Decisions summary
  const activeDecisions = decisions.filter((d) => d.status === "active");
  if (activeDecisions.length > 0) {
    lines.push("DECISIONS LOG", "-".repeat(50));
    activeDecisions.forEach((d) => {
      const thread = threads.find((th) => th.id === d.threadId);
      lines.push(`  [${formatMsgTime(d.date)}] ${d.text}`);
      lines.push(
        `    Thread: ${thread?.title ?? "Unknown"} | By: ${qaRoleLabel(d.madeBy)}`,
      );
      if (d.rationale) lines.push(`    Rationale: ${d.rationale}`);
    });
    lines.push("");
  }

  // Threads
  threads.forEach((thread) => {
    const msgs = _qaCache.filter((m) => m.qNum === thread.id);
    if (msgs.length === 0) return;
    lines.push(
      `THREAD: ${thread.title} [${thread.workstream}] (${thread.lifecycle})`,
    );
    lines.push(
      `  Owner: ${qaRoleLabel(thread.owner)} | Intent: ${thread.intent} | Priority: ${thread.priority}`,
    );
    if (thread.objective) lines.push(`  Objective: ${thread.objective}`);
    lines.push("-".repeat(50));
    msgs.forEach((m) => {
      lines.push(
        `  [${qaRoleLabel(m.sender)} | ${formatMsgTime(m.timestamp)}] ${m.text}`,
      );
    });
    if (thread.resolutionSummary)
      lines.push(`  RESOLUTION: ${thread.resolutionSummary}`);
    lines.push("");
  });

  const blob = new Blob([lines.join("\n")], { type: "text/plain" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `Message_Board_Export_${new Date().toISOString().split("T")[0]}.txt`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

// ── Main render ───────────────────────────────
function renderQaSheet(): void {
  const body = document.getElementById("qaSheetBody");
  if (!body) return;

  renderMBSummary();

  let threads = loadMBThreads();
  const myRole = normalizeRole(qaPostingRole);

  // Apply lifecycle filter
  if (mbLifecycleFilter === "open") {
    threads = threads.filter((th) => th.lifecycle === "open");
  } else if (mbLifecycleFilter === "resolved") {
    threads = threads.filter((th) => th.lifecycle === "resolved");
  }

  // Apply workstream filter
  if (mbWorkstreamFilter !== "all") {
    threads = threads.filter((th) => th.workstream === mbWorkstreamFilter);
  }

  // Apply view filter
  switch (mbActiveView) {
    case "my-items":
      threads = threads.filter(
        (th) => th.owner === myRole || th.assignee === myRole,
      );
      break;
    case "decisions": {
      const decisionThreadIds = new Set(
        loadMBDecisions()
          .filter((d) => d.status === "active")
          .map((d) => d.threadId),
      );
      threads = threads.filter((th) => decisionThreadIds.has(th.id));
      break;
    }
    case "executive":
      threads = threads.filter(
        (th) =>
          th.priority !== "normal" ||
          th.intent === "decide" ||
          th.lifecycle === "resolved",
      );
      break;
  }

  // Sort: escalated > urgent > normal, then by most recent message
  threads.sort((a, b) => {
    const prio = { escalated: 0, urgent: 1, normal: 2 };
    const pa = prio[a.priority] ?? 2;
    const pb = prio[b.priority] ?? 2;
    if (pa !== pb) return pa - pb;
    const aMsgs = _qaCache.filter((m) => m.qNum === a.id);
    const bMsgs = _qaCache.filter((m) => m.qNum === b.id);
    const aLast =
      aMsgs.length > 0 ? aMsgs[aMsgs.length - 1].timestamp : a.createdAt;
    const bLast =
      bMsgs.length > 0 ? bMsgs[bMsgs.length - 1].timestamp : b.createdAt;
    return bLast.localeCompare(aLast);
  });

  if (threads.length === 0) {
    body.innerHTML = `<div class="mb-empty">${t("mbNoThreads")}</div>`;
  } else {
    body.innerHTML = threads.map(threadCardHtml).join("");
  }

  // Render all threads
  threads.forEach((th) => renderQaThread(th.id));
  updateQaUnreadBadge();

  // Wire export button
  const exportBtn = document.getElementById("qaExportBtn");
  if (exportBtn) exportBtn.onclick = exportQaThread;

  // Wire collapse/expand
  body.addEventListener("click", (e) => {
    const btn = (e.target as HTMLElement).closest<HTMLButtonElement>(
      "[data-qatoggle]",
    );
    if (!btn) return;
    const id = Number(btn.dataset.qatoggle);
    if (qaCollapsed.has(id)) qaCollapsed.delete(id);
    else qaCollapsed.add(id);
    const wrap = document.getElementById(`qa-wrap-${id}`);
    if (wrap) wrap.classList.toggle("collapsed");
    btn.textContent = qaCollapsed.has(id) ? t("qaExpand") : t("qaCollapse");
  });

  // Wire role picker
  const toolbar = document.getElementById("qaToolbar");
  if (toolbar) {
    toolbar.addEventListener("click", (e) => {
      const btn = (e.target as HTMLElement).closest<HTMLButtonElement>(
        "[data-qarole]",
      );
      if (!btn) return;
      qaPostingRole = btn.dataset.qarole!;
      toolbar
        .querySelectorAll(".qa-role-btn")
        .forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
      renderQaSheet();
      updateQaUnreadBadge();
    });
  }

  // Wire view switcher
  const views = document.getElementById("mbViews");
  if (views) {
    views.addEventListener("click", (e) => {
      const btn = (e.target as HTMLElement).closest<HTMLButtonElement>(
        "[data-mbview]",
      );
      if (!btn) return;
      mbActiveView = btn.dataset.mbview as MBView;
      views
        .querySelectorAll(".mb-view-btn")
        .forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
      renderQaSheet();
    });
  }

  // Wire filters
  const wsFilter = document.getElementById(
    "mbWorkstreamFilter",
  ) as HTMLSelectElement;
  if (wsFilter) {
    wsFilter.value = mbWorkstreamFilter;
    wsFilter.onchange = () => {
      mbWorkstreamFilter = wsFilter.value as MBWorkstream | "all";
      renderQaSheet();
    };
  }
  const lcFilter = document.getElementById(
    "mbLifecycleFilter",
  ) as HTMLSelectElement;
  if (lcFilter) {
    lcFilter.value = mbLifecycleFilter;
    lcFilter.onchange = () => {
      mbLifecycleFilter = lcFilter.value as "open" | "all" | "resolved";
      renderQaSheet();
    };
  }
}

// ── Archive ───────────────────────────────────
const QA_ARCHIVE_KEY = "ctower_qa_archive";

function loadQaArchive(): Array<{ archivedAt: string; messages: QAMessage[] }> {
  try {
    const raw = localStorage.getItem(QA_ARCHIVE_KEY);
    return raw ? JSON.parse(raw) : [];
  } catch {
    return [];
  }
}

function archiveQaMessages(threadId: number): void {
  const threadMsgs = _qaCache.filter((m) => m.qNum === threadId);
  if (threadMsgs.length === 0) return;
  if (!confirm(t("qaArchiveConfirm"))) return;

  const archive = loadQaArchive();
  archive.push({ archivedAt: new Date().toISOString(), messages: threadMsgs });
  localStorage.setItem(QA_ARCHIVE_KEY, JSON.stringify(archive));

  _qaCache = _qaCache.filter((m) => m.qNum !== threadId);
  saveQaMessagesLocal(_qaCache);
  if (isOnline()) deleteMessages(threadId);
  renderQaSheet();
  showQaSaveStatus();
}

function viewQaArchive(): void {
  const body = document.getElementById("qaSheetBody");
  if (!body) return;
  const archive = loadQaArchive();
  if (archive.length === 0) {
    body.innerHTML = `<div class="qa-archive-empty">${t("qaNoArchives")}</div>`;
    return;
  }
  body.innerHTML = `
    <div class="qa-archive-header">
      <h3>${t("qaArchiveTitle")}</h3>
      <button class="btn-secondary" onclick="window._closeQaArchive()">${t("qaArchiveBack")}</button>
    </div>
    ${archive
      .map((entry, idx) => {
        const dateStr = new Date(entry.archivedAt).toLocaleDateString(
          undefined,
          { year: "numeric", month: "short", day: "numeric" },
        );
        return `<div class="qa-archive-entry">
        <div class="qa-archive-entry-header">
          <span class="qa-archive-date">📦 ${dateStr} — ${entry.messages.length} ${t("qaMessages")}</span>
          <button class="doc-remove-btn" onclick="window._deleteQaArchive(${idx})" title="${t("docLibRemove")}">✕</button>
        </div>
        <div class="qa-archive-messages">
          ${entry.messages
            .slice(0, 5)
            .map(
              (m) =>
                `<div class="qa-archive-msg">T${m.qNum} · ${qaRoleLabel(m.sender)}: ${m.text.length > 80 ? m.text.slice(0, 80) + "…" : m.text}</div>`,
            )
            .join("")}
          ${entry.messages.length > 5 ? `<div class="qa-archive-more">+ ${entry.messages.length - 5} ${t("qaMessages")}…</div>` : ""}
        </div>
      </div>`;
      })
      .join("")}`;
}

function closeQaArchive(): void {
  renderQaSheet();
}
function deleteQaArchive(idx: number): void {
  if (!confirm(t("qaArchiveDeleteConfirm"))) return;
  const archive = loadQaArchive();
  archive.splice(idx, 1);
  localStorage.setItem(QA_ARCHIVE_KEY, JSON.stringify(archive));
  viewQaArchive();
}

// ── Unread badge ──────────────────────────────
function updateQaUnreadBadge(): void {
  const tabBtn = document.querySelector('.tab-btn[data-tab="qa-sheet"]');
  if (!tabBtn) return;
  const myRole = normalizeRole(qaPostingRole);
  const unread = _qaCache.filter(
    (m) => normalizeRole(m.sender) !== myRole && !m.readBy?.includes(myRole),
  ).length;
  let badge = tabBtn.querySelector(".qa-tab-badge") as HTMLElement | null;
  if (unread > 0) {
    if (!badge) {
      badge = document.createElement("span");
      badge.className = "qa-tab-badge";
      tabBtn.appendChild(badge);
    }
    badge.textContent = String(unread);
  } else if (badge) {
    badge.remove();
  }
}

// ── Cross-tab sync ────────────────────────────
window.addEventListener("storage", (e: StorageEvent) => {
  if (e.key !== QA_STORAGE_KEY) return;
  const newMsgs: QAMessage[] = e.newValue ? JSON.parse(e.newValue) : [];
  _qaCache = newMsgs;
  const panel = document.getElementById("panel-qa-sheet");
  if (panel && panel.style.display !== "none") {
    loadMBThreads().forEach((th) => renderQaThread(th.id));
  }
  updateQaUnreadBadge();
  const oldMsgs: QAMessage[] = e.oldValue ? JSON.parse(e.oldValue) : [];
  if (newMsgs.length > oldMsgs.length) {
    const latest = newMsgs[newMsgs.length - 1];
    if (latest.sender !== normalizeRole(qaPostingRole))
      showQaNotification(latest);
  }
});

// ── Toast notifications ───────────────────────
function showQaNotification(msg: QAMessage): void {
  const senderLabel = qaRoleLabel(msg.sender);
  const icon = qaRoleIcon(msg.sender);
  const preview = msg.text.length > 60 ? msg.text.slice(0, 60) + "…" : msg.text;
  const toast = document.createElement("div");
  toast.className = "qa-toast";
  toast.innerHTML = `
    <div class="qa-toast-header">${icon} ${senderLabel} — T${msg.qNum}</div>
    <div class="qa-toast-body">${preview.replace(/</g, "&lt;").replace(/>/g, "&gt;")}</div>
  `;
  document.body.appendChild(toast);
  requestAnimationFrame(() => toast.classList.add("qa-toast-show"));
  setTimeout(() => {
    toast.classList.remove("qa-toast-show");
    toast.addEventListener("transitionend", () => toast.remove());
  }, 4000);
}

// ── Auto-mark read ────────────────────────────
function autoMarkVisibleAsRead(): void {
  const myRole = normalizeRole(qaPostingRole);
  let changed = false;
  _qaCache.forEach((m) => {
    if (normalizeRole(m.sender) !== myRole && !m.readBy?.includes(myRole)) {
      const threadEl = document.getElementById(`qa-thread-${m.qNum}`);
      if (threadEl && threadEl.offsetParent !== null) {
        if (!m.readBy) m.readBy = [];
        m.readBy.push(myRole);
        if (isOnline()) markMessageRead(m.id, myRole);
        changed = true;
      }
    }
  });
  if (changed) {
    saveQaMessagesLocal(_qaCache);
    updateQaUnreadBadge();
  }
}

// ── Thread CRUD ───────────────────────────────
function mbCreateThread(): void {
  const title = prompt(t("mbNewThreadTitle"));
  if (!title || !title.trim()) return;

  const wsOptions: MBWorkstream[] = [
    "project",
    "regulatory",
    "engineering",
    "clinical",
    "business",
    "operations",
  ];
  const wsChoice = prompt(
    `${t("mbWorkstream")} (${wsOptions.join(", ")})`,
    "project",
  );
  const workstream: MBWorkstream = wsOptions.includes(wsChoice as MBWorkstream)
    ? (wsChoice as MBWorkstream)
    : "project";

  const intentOptions: MBMessageIntent[] = ["inform", "decide", "act"];
  const intentChoice = prompt(
    `${t("mbIntent")} (${intentOptions.join(", ")})`,
    "inform",
  );
  const intent: MBMessageIntent = intentOptions.includes(
    intentChoice as MBMessageIntent,
  )
    ? (intentChoice as MBMessageIntent)
    : "inform";

  const objective = prompt(t("mbObjective")) || "";

  const priorityOptions: MBPriority[] = ["normal", "urgent", "escalated"];
  const prioChoice = prompt(
    `${t("mbPriorityLabel")} (${priorityOptions.join(", ")})`,
    "normal",
  );
  const priority: MBPriority = priorityOptions.includes(
    prioChoice as MBPriority,
  )
    ? (prioChoice as MBPriority)
    : "normal";

  const threads = loadMBThreads();
  const maxId = threads.reduce((mx, th) => Math.max(mx, th.id), 999);
  const id = maxId + 1;

  const thread: MBThread = {
    id,
    title: title.trim(),
    workstream,
    intent,
    owner: normalizeRole(qaPostingRole),
    objective,
    lifecycle: "open",
    priority,
    linkedItems: [],
    createdAt: new Date().toISOString(),
  };
  threads.push(thread);
  saveMBThreads(threads);
  logAudit(
    "qa-topic",
    String(id),
    "create",
    "",
    title.trim(),
    `Thread created: ${workstream}/${intent}`,
  );
  renderQaSheet();
  setTimeout(() => {
    const el = document.getElementById(`qa-topic-${id}`);
    if (el) el.scrollIntoView({ behavior: "smooth", block: "start" });
  }, 100);
}

function mbResolveThread(threadId: number): void {
  const summary = prompt(t("mbResolutionPrompt"));
  if (summary === null) return;
  const threads = loadMBThreads();
  const thread = threads.find((th) => th.id === threadId);
  if (!thread) return;
  thread.lifecycle = "resolved";
  thread.resolvedAt = new Date().toISOString();
  thread.resolutionSummary = summary || "Resolved";
  saveMBThreads(threads);
  logAudit(
    "qa-topic",
    String(threadId),
    "resolve",
    "open",
    "resolved",
    summary || "",
  );
  renderQaSheet();
}

function mbReopenThread(threadId: number): void {
  const threads = loadMBThreads();
  const thread = threads.find((th) => th.id === threadId);
  if (!thread) return;
  thread.lifecycle = "open";
  thread.resolvedAt = undefined;
  thread.resolutionSummary = undefined;
  saveMBThreads(threads);
  logAudit("qa-topic", String(threadId), "reopen", "resolved", "open", "");
  renderQaSheet();
}

function mbDeleteThread(threadId: number): void {
  if (!confirm(t("mbDeleteConfirm"))) return;
  let threads = loadMBThreads();
  const thread = threads.find((th) => th.id === threadId);
  threads = threads.filter((th) => th.id !== threadId);
  saveMBThreads(threads);
  // Remove decisions
  let decisions = loadMBDecisions();
  decisions = decisions.filter((d) => d.threadId !== threadId);
  saveMBDecisions(decisions);
  // Remove messages
  _qaCache = _qaCache.filter((m) => m.qNum !== threadId);
  saveQaMessagesLocal(_qaCache);
  if (isOnline()) deleteMessages(threadId);
  logAudit("qa-topic", String(threadId), "delete", thread?.title ?? "", "", "");
  renderQaSheet();
}

function mbLogDecision(threadId: number): void {
  const text = prompt(t("mbDecisionText"));
  if (!text || !text.trim()) return;
  const rationale = prompt(t("mbDecisionRationale")) || "";
  const decisions = loadMBDecisions();
  const decision: MBDecision = {
    id: `dec-${Date.now()}`,
    threadId,
    text: text.trim(),
    rationale,
    madeBy: normalizeRole(qaPostingRole),
    date: new Date().toISOString(),
    linkedItems: [],
    status: "active",
  };
  decisions.push(decision);
  saveMBDecisions(decisions);
  logAudit(
    "qa-topic",
    String(threadId),
    "decision",
    "",
    text.trim(),
    rationale,
  );
  renderQaSheet();
}

function mbCreateAction(threadId: number): void {
  const threads = loadMBThreads();
  const thread = threads.find((th) => th.id === threadId);
  if (!thread) return;

  const roles = ["pmp", "technology", "business", "accounting"];
  const assignee = prompt(`${t("mbAssignee")} (${roles.join(", ")})`, "pmp");
  if (!assignee) return;
  const dueDate = prompt(
    t("mbDueDate"),
    new Date(Date.now() + 7 * 86400000).toISOString().split("T")[0],
  );

  thread.assignee = normalizeRole(assignee);
  thread.dueDate = dueDate || undefined;
  thread.intent = "act";
  saveMBThreads(threads);
  logAudit("qa-topic", String(threadId), "assign", "", assignee, dueDate || "");
  renderQaSheet();
}

function mbToggleActionStatus(threadId: number): void {
  const threads = loadMBThreads();
  const thread = threads.find((th) => th.id === threadId);
  if (!thread) return;
  // Cycle through action states via resolve/reopen
  if (thread.lifecycle === "open") {
    mbResolveThread(threadId);
  } else {
    mbReopenThread(threadId);
  }
}

function mbLinkItem(threadId: number): void {
  const threads = loadMBThreads();
  const thread = threads.find((th) => th.id === threadId);
  if (!thread) return;

  const types = ["milestone", "risk", "gate", "document", "standard", "task"];
  const type = prompt(`${t("mbLinkType")} (${types.join(", ")})`, "milestone");
  if (!type || !types.includes(type)) return;
  const id = prompt(t("mbLinkId"));
  if (!id) return;
  const label = prompt(t("mbLinkLabel")) || id;

  thread.linkedItems.push({ type: type as MBLinkedItem["type"], id, label });
  saveMBThreads(threads);
  logAudit("qa-topic", String(threadId), "link", "", `${type}:${id}`, label);
  renderQaSheet();
}

// Legacy compat
function createQaTopic(): void {
  mbCreateThread();
}
function deleteQaTopic(threadId: number): void {
  mbDeleteThread(threadId);
}

// ── Expose globals ────────────────────────────
(window as any)._sendQaMessage = sendQaMessage;
(window as any)._exportQaThread = exportQaThread;
(window as any)._openQaSettings = openQaSettings;
(window as any)._saveQaSettings = saveQaSettingsUI;
(window as any)._markQaRead = markQaRead;
(window as any)._archiveQaMessages = archiveQaMessages;
(window as any)._viewQaArchive = viewQaArchive;
(window as any)._closeQaArchive = closeQaArchive;
(window as any)._deleteQaArchive = deleteQaArchive;
(window as any)._autoMarkVisibleAsRead = autoMarkVisibleAsRead;
(window as any)._createQaTopic = createQaTopic;
(window as any)._deleteQaTopic = deleteQaTopic;
(window as any)._toggleQaTestMode = function (checked: boolean): void {
  qaTestMode = checked;
  renderQaSheet();
};
(window as any)._mbCreateThread = mbCreateThread;
(window as any)._mbResolveThread = mbResolveThread;
(window as any)._mbReopenThread = mbReopenThread;
(window as any)._mbDeleteThread = mbDeleteThread;
(window as any)._mbSetView = function (view: string): void {
  mbActiveView = view as MBView;
  renderQaSheet();
};
(window as any)._mbSetWorkstreamFilter = function (ws: string): void {
  mbWorkstreamFilter = ws as MBWorkstream | "all";
  renderQaSheet();
};
(window as any)._mbLogDecision = mbLogDecision;
(window as any)._mbCreateAction = mbCreateAction;
(window as any)._mbToggleActionStatus = mbToggleActionStatus;
(window as any)._mbLinkItem = mbLinkItem;

// ── Supabase Realtime Subscription ────────────────────
function setupRealtimeMessages(): void {
  subscribeMessages(
    (dbMsg) => {
      const msg = dbToQa(dbMsg);
      if (!_qaCache.some((m) => m.id === msg.id)) {
        _qaCache.push(msg);
        saveQaMessagesLocal(_qaCache);
        renderQaThread(msg.qNum);
        updateQaUnreadBadge();
        if (normalizeRole(msg.sender) !== normalizeRole(qaPostingRole))
          showQaNotification(msg);
      }
    },
    (dbMsg) => {
      const idx = _qaCache.findIndex((m) => m.id === dbMsg.id);
      if (idx !== -1) {
        _qaCache[idx].readBy = dbMsg.read_by ?? [];
        saveQaMessagesLocal(_qaCache);
        renderQaThread(_qaCache[idx].qNum);
        updateQaUnreadBadge();
      }
    },
  );
}

// Re-sync when coming back online
window.addEventListener("online", async () => {
  await syncOfflineMessages();
  const rows = await fetchMessages();
  _qaCache = rows.map(dbToQa);
  saveQaMessagesLocal(_qaCache);
  const panel = document.getElementById("panel-qa-sheet");
  if (panel && panel.style.display !== "none") {
    loadMBThreads().forEach((th) => renderQaThread(th.id));
  }
  updateQaUnreadBadge();
});

// ══════════════════════════════════════════════════
// AUDIT TRAIL HELPER
// ══════════════════════════════════════════════════

/** Queue of audit entries waiting to be sent to Supabase (offline buffer) */
function loadAuditQueue(): Omit<DbAuditEntry, "id">[] {
  try {
    const raw = localStorage.getItem(AUDIT_QUEUE_KEY);
    return raw ? (JSON.parse(raw) as Omit<DbAuditEntry, "id">[]) : [];
  } catch {
    return [];
  }
}
function saveAuditQueue(q: Omit<DbAuditEntry, "id">[]): void {
  localStorage.setItem(AUDIT_QUEUE_KEY, JSON.stringify(q));
}

async function flushAuditQueue(): Promise<void> {
  const q = loadAuditQueue();
  if (q.length === 0) return;
  const ok = await insertAuditBatch(q);
  if (ok) {
    localStorage.removeItem(AUDIT_QUEUE_KEY);
  }
}

function logAudit(
  action: AuditEntry["action"],
  targetId: string,
  field: string,
  oldValue: string,
  newValue: string,
  detail: string,
): void {
  const roleLabels: Record<string, string> = {
    pmp: "PMP",
    tech: "Tech",
    business: "Business",
    accounting: "Accounting",
  };
  const entry: Omit<DbAuditEntry, "id"> = {
    timestamp: new Date().toISOString(),
    user_role: roleLabels[ACTIVE_ROLE] || ACTIVE_ROLE,
    action,
    target_id: targetId,
    field,
    old_value: oldValue,
    new_value: newValue,
    detail,
  };

  // Push to in-memory cache for instant UI update
  AUDIT_LOG.unshift({
    id: "AUD-" + String(AUDIT_LOG.length + 1).padStart(3, "0"),
    timestamp: entry.timestamp,
    user: entry.user_role,
    action: action,
    targetId,
    field,
    oldValue,
    newValue,
    detail,
  });

  // Persist to Supabase (or queue offline)
  if (isOnline()) {
    insertAuditEntry(entry).catch(() => {
      const q = loadAuditQueue();
      q.push(entry);
      saveAuditQueue(q);
    });
  } else {
    const q = loadAuditQueue();
    q.push(entry);
    saveAuditQueue(q);
  }
}

// ══════════════════════════════════════════════════
// ACTION ITEMS / TASK BOARD
// ══════════════════════════════════════════════════
function renderActionBoard(): void {
  const container = document.getElementById("actionBoard");
  if (!container) return;

  const columns: { key: string; label: string; items: typeof ACTION_ITEMS }[] =
    [
      {
        key: "todo",
        label: t("actionTodo"),
        items: ACTION_ITEMS.filter((a) => a.status === "todo"),
      },
      {
        key: "in-progress",
        label: t("actionInProgress"),
        items: ACTION_ITEMS.filter((a) => a.status === "in-progress"),
      },
      {
        key: "blocked",
        label: t("actionBlocked"),
        items: ACTION_ITEMS.filter((a) => a.status === "blocked"),
      },
      {
        key: "done",
        label: t("actionDone"),
        items: ACTION_ITEMS.filter((a) => a.status === "done"),
      },
    ];

  container.innerHTML = columns
    .map(
      (col) => `
      <div class="action-column action-col-${col.key}">
        <h4 class="action-col-header">${col.label} (${col.items.length})</h4>
        ${col.items
          .map(
            (a) => `
          <div class="action-card priority-${a.priority}" data-action="cycleActionStatus" data-aid="${a.id}" style="cursor:pointer">
            <div class="action-card-top">
              <span class="action-id">${a.id}</span>
              <span class="action-priority-badge prio-${a.priority}">${a.priority === "high" ? t("actionHigh") : a.priority === "medium" ? t("actionMedium") : t("actionLow")}</span>
            </div>
            <div class="action-title">${localizedText(a.title)}</div>
            <div class="action-meta">
              <span>${t("actionAssignee")}: ${a.assignee}</span>
              <span>${t("actionDue")}: ${a.dueDate}</span>
              ${a.linkedGate ? `<span>${t("actionGate")}: ${a.linkedGate}</span>` : ""}
            </div>
            ${a.notes ? `<div class="action-notes">${a.notes}</div>` : ""}
          </div>`,
          )
          .join("")}
      </div>`,
    )
    .join("");
}

window._cycleActionStatus = function (actionId: string): void {
  const item = ACTION_ITEMS.find((a) => a.id === actionId);
  if (!item) return;
  if (ACTIVE_ROLE !== "pmp") {
    window._openChangeRequestForm(
      "action-status",
      actionId,
      "status",
      item.status,
    );
    return;
  }
  const cycle: Record<string, "in-progress" | "done" | "todo" | "blocked"> = {
    todo: "in-progress",
    "in-progress": "done",
    done: "todo",
    blocked: "in-progress",
  };
  const old = item.status;
  item.status = cycle[item.status];
  logAudit(
    "action-item",
    actionId,
    "status",
    old,
    item.status,
    `Action ${actionId} status changed`,
  );
  renderActionBoard();
};

// ══════════════════════════════════════════════════
// DHF DOCUMENT TRACKER
// ══════════════════════════════════════════════════
function renderDHFTable(): void {
  const tbody = document.getElementById("dhfBody");
  if (!tbody) return;

  tbody.innerHTML = DHF_DOCUMENTS.map((d) => {
    const statusLabels: Record<string, string> = {
      "not-started": t("notStarted"),
      draft: t("dhfDraft"),
      "in-review": t("dhfInReview"),
      approved: t("dhfApproved"),
    };
    const badgeClass =
      d.status === "approved"
        ? "badge-complete"
        : d.status === "in-review"
          ? "badge-in-progress"
          : d.status === "draft"
            ? "badge-draft"
            : "badge-not-started";

    return `
      <tr>
        <td><span class="std-code">${d.code}</span></td>
        <td>${localizedText(d.title)}</td>
        <td>${d.category}</td>
        <td>
          <span class="std-status-badge ${badgeClass} clickable-badge"
                data-action="cycleDHFStatus" data-did="${d.id}"
                title="${t("clickToChangeStatus")}">
            ${statusLabels[d.status] || d.status}
          </span>
        </td>
        <td>M+${d.dueMonth}</td>
      </tr>
    `;
  }).join("");
}

window._cycleDHFStatus = function (docId: string): void {
  const doc = DHF_DOCUMENTS.find((d) => d.id === docId);
  if (!doc) return;
  if (ACTIVE_ROLE !== "pmp") {
    window._openChangeRequestForm("dhf-status", docId, "status", doc.status);
    return;
  }
  const cycle: Record<
    string,
    "draft" | "in-review" | "approved" | "not-started"
  > = {
    "not-started": "draft",
    draft: "in-review",
    "in-review": "approved",
    approved: "not-started",
  };
  const old = doc.status;
  doc.status = cycle[doc.status];
  logAudit(
    "dhf-status",
    docId,
    "status",
    old,
    doc.status,
    `DHF ${doc.code} status changed`,
  );
  renderDHFTable();
};

// ══════════════════════════════════════════════════
// CAPA LOG
// ══════════════════════════════════════════════════
function renderCAPALog(): void {
  const container = document.getElementById("capaContainer");
  if (!container) return;

  container.innerHTML = CAPA_LOG.map((c) => {
    const typeLabel =
      c.type === "corrective" ? t("capaCorrective") : t("capaPreventive");
    const statusLabels: Record<string, string> = {
      open: t("capaOpen"),
      "in-progress": t("capaInProgress"),
      closed: t("capaDone"),
      verified: t("capaVerified"),
    };
    const statusClass = `capa-${c.status}`;

    return `
      <div class="capa-card ${statusClass}" data-action="cycleCAPAStatus" data-cid="${c.id}" style="cursor:pointer">
        <div class="capa-header">
          <span class="capa-id">${c.id}</span>
          <span class="capa-type-badge capa-type-${c.type}">${typeLabel}</span>
          <span class="capa-status-badge ${statusClass}">${statusLabels[c.status]}</span>
        </div>
        <div class="capa-title">${localizedText(c.title)}</div>
        <div class="capa-desc">${localizedText(c.description)}</div>
        <div class="capa-meta">
          <span>${t("capaLinkedRisk")}: ${c.linkedRiskId}</span>
          <span>${t("capaOwner")}: ${c.owner}</span>
          <span>${t("capaOpened")}: ${c.openedDate}</span>
          <span>${t("capaDue")}: ${c.dueDate}</span>
          ${c.closedDate ? `<span>${t("capaClosed")}: ${c.closedDate}</span>` : ""}
        </div>
      </div>
    `;
  }).join("");
}

window._cycleCAPAStatus = function (capaId: string): void {
  const capa = CAPA_LOG.find((c) => c.id === capaId);
  if (!capa) return;
  if (ACTIVE_ROLE !== "pmp") {
    window._openChangeRequestForm("capa-status", capaId, "status", capa.status);
    return;
  }
  const cycle: Record<string, "in-progress" | "closed" | "verified" | "open"> =
    {
      open: "in-progress",
      "in-progress": "closed",
      closed: "verified",
      verified: "open",
    };
  const old = capa.status;
  capa.status = cycle[capa.status];
  if (capa.status === "closed" && !capa.closedDate) {
    capa.closedDate = new Date().toISOString().split("T")[0];
  }
  logAudit(
    "capa-status",
    capaId,
    "status",
    old,
    capa.status,
    `CAPA ${capaId} status changed`,
  );
  renderCAPALog();
};

// ══════════════════════════════════════════════════
// BUDGET vs ACTUAL
// ══════════════════════════════════════════════════
function renderBudget(): void {
  const tbody = document.getElementById("budgetBody");
  if (!tbody) return;

  const canEditBudget = ["pmp", "business", "technology"].includes(ACTIVE_ROLE);
  let totalPlanned = 0;
  let totalActual = 0;

  const rows = BUDGET_CATEGORIES.map((b) => {
    totalPlanned += b.planned;
    totalActual += b.actual;
    const variance = b.planned - b.actual;
    const varianceClass =
      variance < 0 ? "budget-over" : variance === 0 ? "" : "budget-under";
    return `
      <tr>
        <td>${localizedText(b.label)}${canEditBudget ? ` <button class="cash-edit-btn burn-delete-btn" data-action="deleteBudgetCategory" data-budgetid="${b.id}" title="✕">✕</button>` : ""}</td>
        <td>${fmtCurrency(b.planned)}${canEditBudget ? ` <button class="cash-edit-btn" data-action="editBudgetField" data-budgetid="${b.id}" data-field="planned" title="${t("budgetEditPlanned")}">✎</button>` : ""}</td>
        <td>${fmtCurrency(b.actual)}${canEditBudget ? ` <button class="cash-edit-btn" data-action="editBudgetField" data-budgetid="${b.id}" data-field="actual" title="${t("budgetEditActual")}">✎</button>` : ""}</td>
        <td class="${varianceClass}">${variance >= 0 ? "+" : ""}${fmtCurrency(variance)}</td>
      </tr>
    `;
  }).join("");

  const totalVar = totalPlanned - totalActual;
  const totalVarClass = totalVar < 0 ? "budget-over" : "budget-under";
  tbody.innerHTML =
    rows +
    `<tr class="budget-total-row">
      <td><strong>${t("budgetTotal")}</strong></td>
      <td><strong>${fmtCurrency(totalPlanned)}</strong></td>
      <td><strong>${fmtCurrency(totalActual)}</strong></td>
      <td class="${totalVarClass}"><strong>${totalVar >= 0 ? "+" : ""}${fmtCurrency(totalVar)}</strong></td>
    </tr>`;

  // Add budget form placeholder
  const formEl = document.getElementById("budgetAddForm");
  if (formEl && canEditBudget) {
    formEl.style.display = "";
  }
}

// ══════════════════════════════════════════════════
// RESOURCE ALLOCATION
// ══════════════════════════════════════════════════
function renderResources(): void {
  const container = document.getElementById("resourceGrid");
  if (!container) return;

  container.innerHTML = TEAM_MEMBERS.map((m) => {
    const totalAlloc = m.allocation.reduce((s, a) => s + a.pct, 0);
    const utilPct = Math.round((totalAlloc / m.capacity) * 100);
    const utilClass =
      utilPct > 100 ? "util-over" : utilPct > 85 ? "util-high" : "util-ok";

    return `
      <div class="resource-card">
        <div class="resource-header">
          <span class="resource-name">${m.name}</span>
          <span class="resource-util ${utilClass}">${utilPct}%</span>
        </div>
        <div class="resource-role">${localizedText(m.role)}</div>
        ${m.email ? `<div class="resource-email">📧 <a href="mailto:${m.email}">${m.email}</a></div>` : ""}
        <div class="resource-alloc">
          ${m.allocation
            .map(
              (a) => `
            <div class="alloc-row">
              <span class="alloc-label">${a.workstream}</span>
              <div class="alloc-bar-wrap">
                <div class="alloc-bar" style="width:${a.pct}%"></div>
              </div>
              <span class="alloc-pct">${a.pct}%</span>
            </div>`,
            )
            .join("")}
        </div>
        <div class="resource-cap">${t("resourceCapacity")}: ${m.capacity}%</div>
      </div>
    `;
  }).join("");
}

// ══════════════════════════════════════════════════
// SUPPLIER / VENDOR TRACKER
// ══════════════════════════════════════════════════
function renderSuppliers(): void {
  const tbody = document.getElementById("supplierBody");
  if (!tbody) return;

  const canEdit = ["pmp", "business", "technology"].includes(ACTIVE_ROLE);

  tbody.innerHTML = SUPPLIERS.map((s) => {
    const statusLabels: Record<string, string> = {
      active: t("supplierActive"),
      qualified: t("supplierQualified"),
      "under-review": t("supplierUnderReview"),
      risk: t("supplierRisk"),
    };
    const statusClass = `sup-${s.status}`;

    return `
      <tr>
        <td>${s.name}</td>
        <td>${localizedText(s.component)}</td>
        <td>
          <span class="sup-status-badge ${statusClass} clickable-badge"
                data-action="cycleSupplierStatus" data-supid="${s.id}"
                title="${t("clickToChangeStatus")}">
            ${statusLabels[s.status]}
          </span>
        </td>
        <td>${s.leadTimeDays} ${t("supplierDays")}</td>
        <td>${s.poStatus}</td>
        <td>${s.contractMfgMilestone}</td>
        <td>${canEdit ? `<button class="doc-remove-btn" data-action="deleteSupplier" data-supid="${s.id}" title="✕">✕</button>` : ""}</td>
      </tr>
    `;
  }).join("");
}

window._cycleSupplierStatus = function (supplierId: string): void {
  const sup = SUPPLIERS.find((s) => s.id === supplierId);
  if (!sup) return;
  if (ACTIVE_ROLE !== "pmp") {
    window._openChangeRequestForm(
      "supplier-status",
      supplierId,
      "status",
      sup.status,
    );
    return;
  }
  const cycle: Record<
    string,
    "qualified" | "active" | "under-review" | "risk"
  > = {
    "under-review": "qualified",
    qualified: "active",
    active: "risk",
    risk: "under-review",
  };
  const old = sup.status;
  sup.status = cycle[sup.status];
  logAudit(
    "supplier-status",
    supplierId,
    "status",
    old,
    sup.status,
    `Supplier ${sup.name} status changed`,
  );
  renderSuppliers();
};

// ── Supplier CRUD ───────────────────────────
window._openAddSupplierForm = function (): void {
  const form = document.getElementById("supplierAddForm");
  if (!form) return;
  form.innerHTML = `
    <h4>${t("supplierAddBtn")}</h4>
    <div class="funding-form-row">
      <input type="text" id="supFormName" placeholder="${t("supplierFormName")}" />
      <input type="text" id="supFormComponent" placeholder="${t("supplierFormComponent")}" />
      <input type="text" id="supFormComponentCn" placeholder="${t("supplierFormComponentCn")}" />
      <input type="number" id="supFormLead" placeholder="${t("supplierFormLead")}" min="1" />
      <input type="text" id="supFormPO" placeholder="${t("supplierFormPO")}" />
      <input type="text" id="supFormMilestone" placeholder="${t("supplierFormMilestone")}" />
      <button class="btn-add-funding" data-action="addSupplier">${t("supplierFormAdd")}</button>
      <button class="btn-secondary" onclick="document.getElementById('supplierAddForm').innerHTML=''">${t("supplierFormCancel")}</button>
    </div>
  `;
};

window._addSupplier = function (): void {
  if (!["pmp", "business", "technology"].includes(ACTIVE_ROLE)) return;
  const nameEl = document.getElementById("supFormName") as HTMLInputElement;
  const compEl = document.getElementById(
    "supFormComponent",
  ) as HTMLInputElement;
  const compCnEl = document.getElementById(
    "supFormComponentCn",
  ) as HTMLInputElement;
  const leadEl = document.getElementById("supFormLead") as HTMLInputElement;
  const poEl = document.getElementById("supFormPO") as HTMLInputElement;
  const msEl = document.getElementById("supFormMilestone") as HTMLInputElement;
  const name = nameEl?.value?.trim();
  if (!name) return;
  const id = "SUP-" + String(SUPPLIERS.length + 1).padStart(3, "0");
  SUPPLIERS.push({
    id,
    name,
    component: {
      en: compEl?.value?.trim() || "",
      cn: compCnEl?.value?.trim() || compEl?.value?.trim() || "",
    },
    status: "under-review",
    leadTimeDays: parseInt(leadEl?.value || "30", 10) || 30,
    poStatus: poEl?.value?.trim() || "—",
    contractMfgMilestone: msEl?.value?.trim() || "—",
    notes: "",
  });
  logAudit("supplier-add", id, "add", "", name, "");
  const form = document.getElementById("supplierAddForm");
  if (form) form.innerHTML = "";
  renderSuppliers();
};

window._deleteSupplier = function (supplierId: string): void {
  if (!["pmp", "business", "technology"].includes(ACTIVE_ROLE)) return;
  if (!confirm(t("supplierDeleteConfirm"))) return;
  const idx = SUPPLIERS.findIndex((s) => s.id === supplierId);
  if (idx < 0) return;
  const sup = SUPPLIERS[idx];
  SUPPLIERS.splice(idx, 1);
  logAudit("supplier-delete", supplierId, "delete", sup.name, "", "");
  renderSuppliers();
};

// ══════════════════════════════════════════════════
// AUDIT TRAIL TABLE
// ══════════════════════════════════════════════════

/** Fetch audit log from Supabase on startup, merge with seed data */
async function initAuditLog(): Promise<void> {
  try {
    // First flush any queued offline entries
    await flushAuditQueue();

    const rows = await fetchAuditLog(200);
    if (rows.length > 0) {
      // Replace seed data with server data
      AUDIT_LOG.length = 0;
      rows.forEach((r) =>
        AUDIT_LOG.push({
          id: r.id ?? "",
          timestamp: r.timestamp,
          user: r.user_role,
          action: r.action as AuditEntry["action"],
          targetId: r.target_id,
          field: r.field,
          oldValue: r.old_value,
          newValue: r.new_value,
          detail: r.detail,
        }),
      );
    }
    // If no rows returned, keep the seed data for display
  } catch (err) {
    console.error("initAuditLog failed, using seed data:", err);
  }
}

function renderAuditTrail(): void {
  const tbody = document.getElementById("auditBody");
  if (!tbody) return;

  tbody.innerHTML = AUDIT_LOG.slice(0, 50)
    .map(
      (e) => `
      <tr>
        <td class="audit-ts">${new Date(e.timestamp).toLocaleString()}</td>
        <td>${e.user}</td>
        <td><span class="audit-action-badge">${e.action}</span></td>
        <td>${e.targetId}</td>
        <td class="audit-old">${e.oldValue}</td>
        <td class="audit-new">${e.newValue}</td>
        <td class="audit-detail">${e.detail}</td>
      </tr>
    `,
    )
    .join("");
}

// ══════════════════════════════════════════════════
// NOTIFICATIONS / ALERTS
// ══════════════════════════════════════════════════
function renderNotifications(): void {
  const bar = document.getElementById("notifBar");
  const container = document.getElementById("notifContainer");
  if (!bar || !container) return;

  const today = new Date().toISOString().split("T")[0];
  const alerts: { key: string; type: string; text: string }[] = [];

  // Pending CRs
  const pendingCrs = CHANGE_REQUESTS.filter((c) => c.status === "pending");
  pendingCrs.forEach((cr) => {
    const k = "cr-" + cr.id;
    if (!dismissedNotifs.has(k)) {
      alerts.push({
        key: k,
        type: "notifPendingCR",
        text: `${cr.id}: ${cr.targetId} → ${cr.field}`,
      });
    }
  });

  // Overdue action items
  ACTION_ITEMS.filter((a) => a.status !== "done" && a.dueDate < today).forEach(
    (a) => {
      const k = "act-" + a.id;
      if (!dismissedNotifs.has(k)) {
        alerts.push({
          key: k,
          type: "notifOverdueAction",
          text: `${a.id}: ${localizedText(a.title)}`,
        });
      }
    },
  );

  // Overdue CAPAs
  CAPA_LOG.filter(
    (c) =>
      c.status !== "closed" && c.status !== "verified" && c.dueDate < today,
  ).forEach((c) => {
    const k = "capa-" + c.id;
    if (!dismissedNotifs.has(k)) {
      alerts.push({
        key: k,
        type: "notifOverdueCapa",
        text: `${c.id}: ${localizedText(c.title)}`,
      });
    }
  });

  // Budget overruns
  BUDGET_CATEGORIES.filter((b) => b.actual > b.planned).forEach((b) => {
    const k = "bud-" + b.id;
    if (!dismissedNotifs.has(k)) {
      alerts.push({
        key: k,
        type: "notifBudgetOverrun",
        text: `${localizedText(b.label)}: ${fmtCurrency(b.actual - b.planned)} over`,
      });
    }
  });

  // Runway warning
  if (CASH_RUNWAY.runwayMonths <= 6 && !dismissedNotifs.has("runway")) {
    alerts.push({
      key: "runway",
      type: "notifRunwayWarning",
      text: `${CASH_RUNWAY.runwayMonths} months remaining`,
    });
  }

  bar.style.display = alerts.length > 0 ? "block" : "none";
  container.innerHTML = alerts
    .map(
      (a, i) => `
      <div class="notif-item notif-${a.type}">
        <span class="notif-type">${t(a.type)}</span>
        <span class="notif-text">${a.text}</span>
        <button class="notif-dismiss" data-action="dismissNotification" data-nidx="${i}" data-key="${a.key}">${t("notifDismiss")}</button>
      </div>`,
    )
    .join("");
}

window._dismissNotification = function (index: number): void {
  const btn =
    document.querySelectorAll<HTMLButtonElement>(".notif-dismiss")[index];
  if (btn) {
    const key = btn.dataset.key;
    if (key) dismissedNotifs.add(key);
  }
  renderNotifications();
};

// ══════════════════════════════════════════════════
// EXPORT / REPORT GENERATOR
// ══════════════════════════════════════════════════
window._exportReport = function (): void {
  const lang = getLang();
  const isCN = lang === "cn";
  const projectName = PROJECT.name[isCN ? "cn" : "en"];
  const dateStr = new Date().toISOString().split("T")[0];

  const redRisks = RISKS.filter((r) => r.riskLevel === "red");
  const yellowRisks = RISKS.filter((r) => r.riskLevel === "yellow");
  const pendingCrs = CHANGE_REQUESTS.filter(
    (c) => c.status === "pending",
  ).length;
  const nextGate = GATES.find(
    (g) =>
      g.status !== "approved" &&
      g.decision !== "proceed" &&
      !g.criteria.every((c) => c.met),
  );
  const allMilestones = [
    ...TRACKS.technical.milestones,
    ...TRACKS.regulatory.milestones,
  ];
  const completeMilestones = allMilestones.filter(
    (m) => m.status === "complete",
  ).length;
  const totalMilestones = allMilestones.length;
  const totalPlanned = BUDGET_CATEGORIES.reduce((s, b) => s + b.planned, 0);
  const totalActual = BUDGET_CATEGORIES.reduce((s, b) => s + b.actual, 0);
  const openCapa = CAPA_LOG.filter(
    (c) => c.status === "open" || c.status === "in-progress",
  ).length;
  const openActions = ACTION_ITEMS.filter((a) => a.status !== "done").length;
  const dhfApproved = DHF_DOCUMENTS.filter(
    (d) => d.status === "approved",
  ).length;
  const dhfTotal = DHF_DOCUMENTS.length;

  // Overall status
  const overallLabel =
    redRisks.length >= 3
      ? isCN
        ? "受阻"
        : "BLOCKED"
      : redRisks.length >= 1
        ? isCN
          ? "有风险"
          : "AT RISK"
        : isCN
          ? "正轨"
          : "ON TRACK";
  const overallColor =
    redRisks.length >= 3
      ? "#ef4444"
      : redRisks.length >= 1
        ? "#f59e0b"
        : "#22c55e";

  const esc = (s: string) =>
    s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");

  // Status badge helper
  const badge = (text: string, bg: string) =>
    `<span style="display:inline-block;padding:2px 10px;border-radius:4px;background:${bg};color:#fff;font-weight:600;font-size:13px">${esc(text)}</span>`;

  // Risk level badge
  const riskBadge = (level: string) => {
    const colors: Record<string, string> = {
      red: "#ef4444",
      yellow: "#f59e0b",
      green: "#22c55e",
    };
    const labels: Record<string, string> = isCN
      ? { red: "红色", yellow: "黄色", green: "绿色" }
      : { red: "RED", yellow: "YELLOW", green: "GREEN" };
    return badge(labels[level] || level, colors[level] || "#6b7280");
  };

  // Milestone status badge
  const msBadge = (status: string) => {
    const colors: Record<string, string> = {
      complete: "#22c55e",
      "in-progress": "#3b82f6",
      "not-started": "#6b7280",
    };
    const labels: Record<string, string> = isCN
      ? { complete: "完成", "in-progress": "进行中", "not-started": "未开始" }
      : {
          complete: "Complete",
          "in-progress": "In Progress",
          "not-started": "Not Started",
        };
    return badge(labels[status] || status, colors[status] || "#6b7280");
  };

  const budgetRows = BUDGET_CATEGORIES.map((b) => {
    const variance = b.planned - b.actual;
    const varColor = variance < 0 ? "#ef4444" : "#22c55e";
    return `<tr>
      <td style="padding:6px 12px;border-bottom:1px solid #e5e7eb">${esc(localizedText(b.label))}</td>
      <td style="padding:6px 12px;border-bottom:1px solid #e5e7eb;text-align:right">${esc(fmtCurrency(b.planned))}</td>
      <td style="padding:6px 12px;border-bottom:1px solid #e5e7eb;text-align:right">${esc(fmtCurrency(b.actual))}</td>
      <td style="padding:6px 12px;border-bottom:1px solid #e5e7eb;text-align:right;color:${varColor};font-weight:600">${variance >= 0 ? "+" : ""}${esc(fmtCurrency(variance))}</td>
    </tr>`;
  }).join("");

  const riskRows = [...redRisks, ...yellowRisks]
    .map(
      (r) => `<tr>
    <td style="padding:6px 12px;border-bottom:1px solid #e5e7eb;font-weight:600">${esc(r.id)}</td>
    <td style="padding:6px 12px;border-bottom:1px solid #e5e7eb">${esc(localizedText(r.title))}</td>
    <td style="padding:6px 12px;border-bottom:1px solid #e5e7eb;text-align:center">${riskBadge(r.riskLevel)}</td>
    <td style="padding:6px 12px;border-bottom:1px solid #e5e7eb">${esc(localizedText(r.controls))}</td>
  </tr>`,
    )
    .join("");

  const milestoneRows = allMilestones
    .filter((m) => m.status !== "not-started")
    .map(
      (m) => `<tr>
      <td style="padding:6px 12px;border-bottom:1px solid #e5e7eb;font-weight:600">${esc(m.id)}</td>
      <td style="padding:6px 12px;border-bottom:1px solid #e5e7eb">${esc(localizedText(m.title))}</td>
      <td style="padding:6px 12px;border-bottom:1px solid #e5e7eb;text-align:center">M+${m.month}</td>
      <td style="padding:6px 12px;border-bottom:1px solid #e5e7eb;text-align:center">${msBadge(m.status)}</td>
    </tr>`,
    )
    .join("");

  const actionRows = ACTION_ITEMS.filter((a) => a.status !== "done")
    .map((a) => {
      const prioColor =
        a.priority === "high"
          ? "#ef4444"
          : a.priority === "medium"
            ? "#f59e0b"
            : "#6b7280";
      return `<tr>
        <td style="padding:6px 12px;border-bottom:1px solid #e5e7eb;font-weight:600">${esc(a.id)}</td>
        <td style="padding:6px 12px;border-bottom:1px solid #e5e7eb">${esc(localizedText(a.title))}</td>
        <td style="padding:6px 12px;border-bottom:1px solid #e5e7eb">${esc(a.assignee)}</td>
        <td style="padding:6px 12px;border-bottom:1px solid #e5e7eb;text-align:center">${badge(a.priority.toUpperCase(), prioColor)}</td>
        <td style="padding:6px 12px;border-bottom:1px solid #e5e7eb">${esc(a.dueDate)}</td>
      </tr>`;
    })
    .join("");

  const th =
    "padding:8px 12px;border-bottom:2px solid #1e293b;text-align:left;background:#f1f5f9;font-size:13px";
  const thR = th + ";text-align:right";
  const thC = th + ";text-align:center";
  const metricCard = (label: string, value: string, color = "#1e293b") =>
    `<div style="flex:1;min-width:140px;background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px;padding:14px 18px;text-align:center">
      <div style="font-size:12px;color:#64748b;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:4px">${esc(label)}</div>
      <div style="font-size:22px;font-weight:700;color:${color}">${value}</div>
    </div>`;

  const sectionTitle = (text: string) =>
    `<h2 style="font-size:16px;font-weight:700;color:#1e293b;border-bottom:2px solid #3b82f6;padding-bottom:6px;margin:28px 0 14px">${esc(text)}</h2>`;

  const rateNote = t("exchangeRateNote");

  const html = `<!DOCTYPE html>
<html lang="${isCN ? "zh-CN" : "en"}">
<head>
<meta charset="UTF-8">
<title>${esc(t("exportTitle"))} — ${esc(projectName)}</title>
<style>
  body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 0; padding: 40px; color: #1e293b; background: #fff; line-height: 1.5; }
  table { width: 100%; border-collapse: collapse; font-size: 14px; }
  @media print { body { padding: 20px; } }
</style>
</head>
<body>

<div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:30px;border-bottom:3px solid #1e293b;padding-bottom:20px">
  <div>
    <h1 style="margin:0 0 4px;font-size:24px;color:#1e293b">${esc(projectName)}</h1>
    <div style="font-size:14px;color:#64748b">${esc(t("exportTitle"))}</div>
  </div>
  <div style="text-align:right;font-size:13px;color:#64748b">
    <div>${dateStr}</div>
    <div>${isCN ? "角色" : "Role"}: ${ACTIVE_ROLE.toUpperCase()}</div>
  </div>
</div>

<div style="display:flex;gap:12px;flex-wrap:wrap;margin-bottom:24px">
  ${metricCard(isCN ? "总体状态" : "Overall Status", `<span style="color:${overallColor}">${esc(overallLabel)}</span>`)}
  ${metricCard(isCN ? "下一门控" : "Next Gate", nextGate ? `G${nextGate.number} (M+${nextGate.month})` : isCN ? "无" : "None", "#3b82f6")}
  ${metricCard(isCN ? "红色风险" : "Red Risks", String(redRisks.length), redRisks.length > 0 ? "#ef4444" : "#22c55e")}
  ${metricCard(isCN ? "里程碑" : "Milestones", `${completeMilestones}/${totalMilestones}`, "#3b82f6")}
  ${metricCard(isCN ? "待处理CR" : "Pending CRs", String(pendingCrs), pendingCrs > 0 ? "#f59e0b" : "#22c55e")}
</div>

${sectionTitle(isCN ? "财务概览" : "Financial Overview")}
<div style="display:flex;gap:12px;flex-wrap:wrap;margin-bottom:16px">
  ${metricCard(t("cashOnHand"), esc(fmtCurrency(CASH_RUNWAY.cashOnHand)), "#0f766e")}
  ${metricCard(t("monthlyBurnLabel"), esc(fmtCurrency(CASH_RUNWAY.monthlyBurn)), "#dc2626")}
  ${metricCard(t("runwayLabel"), `${CASH_RUNWAY.runwayMonths} ${t("runwayMonths")}`, CASH_RUNWAY.runwayMonths <= 3 ? "#ef4444" : CASH_RUNWAY.runwayMonths <= 6 ? "#f59e0b" : "#22c55e")}
  ${metricCard(isCN ? "DHF文件" : "DHF Docs", `${dhfApproved}/${dhfTotal}`, "#3b82f6")}
</div>
${rateNote ? `<p style="font-size:12px;color:#94a3b8;margin:4px 0 12px;font-style:italic">${esc(rateNote)}</p>` : ""}

<table>
  <thead><tr>
    <th style="${th}">${isCN ? "类别" : "Category"}</th>
    <th style="${thR}">${isCN ? "计划" : "Planned"}</th>
    <th style="${thR}">${isCN ? "实际" : "Actual"}</th>
    <th style="${thR}">${isCN ? "差异" : "Variance"}</th>
  </tr></thead>
  <tbody>
    ${budgetRows}
    <tr style="font-weight:700;background:#f1f5f9">
      <td style="padding:8px 12px;border-top:2px solid #1e293b">${isCN ? "合计" : "Total"}</td>
      <td style="padding:8px 12px;border-top:2px solid #1e293b;text-align:right">${esc(fmtCurrency(totalPlanned))}</td>
      <td style="padding:8px 12px;border-top:2px solid #1e293b;text-align:right">${esc(fmtCurrency(totalActual))}</td>
      <td style="padding:8px 12px;border-top:2px solid #1e293b;text-align:right;color:${totalPlanned - totalActual < 0 ? "#ef4444" : "#22c55e"}">${totalPlanned - totalActual >= 0 ? "+" : ""}${esc(fmtCurrency(totalPlanned - totalActual))}</td>
    </tr>
  </tbody>
</table>

${
  riskRows
    ? `${sectionTitle(isCN ? "风险登记 (红色 & 黄色)" : "Risk Register (Red & Yellow)")}
<table>
  <thead><tr>
    <th style="${th}">ID</th>
    <th style="${th}">${isCN ? "标题" : "Title"}</th>
    <th style="${thC}">${isCN ? "等级" : "Level"}</th>
    <th style="${th}">${isCN ? "描述" : "Description"}</th>
  </tr></thead>
  <tbody>${riskRows}</tbody>
</table>`
    : ""
}

${
  milestoneRows
    ? `${sectionTitle(isCN ? "里程碑进展" : "Milestone Progress")}
<table>
  <thead><tr>
    <th style="${th}">ID</th>
    <th style="${th}">${isCN ? "标题" : "Title"}</th>
    <th style="${thC}">${isCN ? "目标月" : "Target"}</th>
    <th style="${thC}">${isCN ? "状态" : "Status"}</th>
  </tr></thead>
  <tbody>${milestoneRows}</tbody>
</table>`
    : ""
}

${
  actionRows
    ? `${sectionTitle(isCN ? "待办行动项" : "Open Action Items")}
<table>
  <thead><tr>
    <th style="${th}">ID</th>
    <th style="${th}">${isCN ? "标题" : "Title"}</th>
    <th style="${th}">${isCN ? "负责人" : "Assignee"}</th>
    <th style="${thC}">${isCN ? "优先级" : "Priority"}</th>
    <th style="${th}">${isCN ? "截止日期" : "Due Date"}</th>
  </tr></thead>
  <tbody>${actionRows}</tbody>
</table>`
    : ""
}

<div style="display:flex;gap:12px;margin-top:28px;flex-wrap:wrap">
  ${metricCard(isCN ? "开放CAPA" : "Open CAPAs", String(openCapa), openCapa > 0 ? "#f59e0b" : "#22c55e")}
  ${metricCard(isCN ? "开放行动项" : "Open Actions", String(openActions), openActions > 0 ? "#f59e0b" : "#22c55e")}
  ${metricCard(isCN ? "黄色风险" : "Yellow Risks", String(yellowRisks.length), yellowRisks.length > 0 ? "#f59e0b" : "#22c55e")}
</div>

<div style="margin-top:36px;padding-top:12px;border-top:1px solid #e2e8f0;font-size:11px;color:#94a3b8;text-align:center">
  ${isCN ? "由控制塔仪表盘自动生成" : "Generated by Control Tower Dashboard"} · ${dateStr}
</div>

</body>
</html>`;

  const blob = new Blob([html], { type: "text/html" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `Project_Status_Report_${dateStr}.html`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
};
