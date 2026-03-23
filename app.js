// ============================================================
// APP.JS — Medical Device Development Control Tower
// Dashboard logic, rendering, and interactivity
// ============================================================

(function () {
  "use strict";

  // ── STATE ─────────────────────────────────────
  let activeTab = "dual-track";
  let activeRiskFilter = "all";
  let selectedGateId = null;

  // ── INIT ──────────────────────────────────────
  document.addEventListener("DOMContentLoaded", () => {
    initTabs();
    initLangToggle();
    initFab();
    renderAll();
  });

  // ── TAB NAVIGATION ────────────────────────────
  function initTabs() {
    document.querySelectorAll(".tab-btn").forEach((btn) => {
      btn.addEventListener("click", () => {
        const tab = btn.dataset.tab;
        if (tab === activeTab) return;
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
  function initLangToggle() {
    const btn = document.getElementById("langToggle");
    const label = document.getElementById("langLabel");
    btn.addEventListener("click", () => {
      currentLang = currentLang === "en" ? "cn" : "en";
      label.textContent = currentLang === "en" ? "EN" : "中";
      applyLanguage(currentLang);
      renderAll();
    });
  }

  // ── FAB / INPUT PANEL ─────────────────────────
  function initFab() {
    const fab = document.getElementById("fabInputs");
    const overlay = document.getElementById("inputPanelOverlay");
    const closeBtn = document.getElementById("inputPanelClose");

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
  function renderAll() {
    renderSummary();
    renderDualTrack();
    renderGates();
    renderRisks();
    renderTimeline();
    renderStandards();
    updateFabBadge();
  }

  // ── SUMMARY BAR ───────────────────────────────
  function renderSummary() {
    // Red risk count
    const redCount = RISKS.filter((r) => r.riskLevel === "red").length;
    document.getElementById("redRiskCount").textContent = redCount;

    // Pending inputs
    const pending = STAKEHOLDER_INPUTS.filter(
      (i) => i.status === "pending-review",
    ).length;
    document.getElementById("pendingInputCount").textContent = pending;

    // Next gate
    const nextGate = GATES.find(
      (g) => g.status !== "approved" && g.decision !== "proceed",
    );
    if (nextGate) {
      document.getElementById("nextGate").textContent =
        "G" + nextGate.number + " (M+" + nextGate.month + ")";
    }

    // Overall status
    const statusEl = document.getElementById("overallStatus");
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

    // Days to next milestone
    const currentM = PROJECT.currentMonth;
    const allMilestones = [
      ...TRACKS.technical.milestones,
      ...TRACKS.regulatory.milestones,
    ].filter((m) => m.month > currentM && m.status !== "complete");
    allMilestones.sort((a, b) => a.month - b.month);
    if (allMilestones.length > 0) {
      const monthsAway = allMilestones[0].month - currentM;
      document.getElementById("daysToMilestone").textContent =
        "~" + monthsAway * 30 + "d";
    }

    document.getElementById("currentMonthNum").textContent = currentM;
  }

  // ── DUAL-TRACK DASHBOARD ──────────────────────
  function renderDualTrack() {
    const techContainer = document.getElementById("techMilestones");
    const regContainer = document.getElementById("regMilestones");
    const timelineContainer = document.getElementById("centerTimeline");

    const techItems = [...TRACKS.technical.milestones].sort(
      (a, b) => a.month - b.month,
    );
    const regItems = [...TRACKS.regulatory.milestones].sort(
      (a, b) => a.month - b.month,
    );

    techContainer.innerHTML = techItems.map((m) => milestoneCard(m)).join("");
    regContainer.innerHTML = regItems.map((m) => milestoneCard(m)).join("");

    // Center timeline dots
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

  function milestoneCard(m) {
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

    return `
      <div class="milestone-card ${statusClass}">
        <div class="ms-header">
          <span class="ms-title">${localizedText(m.title)}</span>
          <span class="ms-month">M+${m.month}</span>
        </div>
        <div class="ms-desc">${localizedText(m.description)}</div>
        <span class="ms-status-badge ${badgeClass}">${statusText}</span>
      </div>
    `;
  }

  // ── GATE SYSTEM ───────────────────────────────
  function renderGates() {
    const container = document.getElementById("gatesPipeline");
    const items = [];

    GATES.forEach((gate, i) => {
      const metCount = gate.criteria.filter((c) => c.met).length;
      const totalCount = gate.criteria.length;
      const pct =
        totalCount > 0 ? Math.round((metCount / totalCount) * 100) : 0;

      let gateClass = "gate-not-started";
      if (gate.decision === "proceed") gateClass = "gate-approved";
      else if (gate.decision === "stop") gateClass = "gate-blocked";
      else if (
        gate.status === "pending-review" ||
        gate.decision === "more-data"
      )
        gateClass = "gate-pending";

      items.push(`
        <div class="gate-card ${gateClass}" data-gate-id="${gate.id}" onclick="window._openGate('${gate.id}')">
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
  window._openGate = function (gateId) {
    selectedGateId = gateId;
    const gate = GATES.find((g) => g.id === gateId);
    if (!gate) return;

    const overlay = document.getElementById("gateDetailOverlay");
    const content = document.getElementById("gateDetailContent");

    const metCount = gate.criteria.filter((c) => c.met).length;

    // Criteria list
    const criteriaHtml = gate.criteria
      .map(
        (c, ci) => `
      <li class="criteria-item">
        <div class="criteria-check ${c.met ? "checked" : ""}"
             onclick="event.stopPropagation(); window._toggleCriteria('${gateId}', ${ci})">
          ${c.met ? "✓" : ""}
        </div>
        <span>${localizedText(c)}</span>
      </li>
    `,
      )
      .join("");

    // Related inputs
    const relatedInputs = STAKEHOLDER_INPUTS.filter(
      (inp) => inp.gate === gateId,
    );
    const inputsHtml =
      relatedInputs.length > 0
        ? relatedInputs
            .map((inp) => {
              const fromClass =
                inp.from === "tech" ? "from-tech" : "from-business";
              const fromLabel =
                inp.from === "tech"
                  ? t("inputFromTech")
                  : t("inputFromBusiness");
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

    // Decision buttons
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
          <button class="decision-btn btn-proceed ${proceedSel}" onclick="window._setDecision('${gateId}','proceed')">${t("gateProceed")}</button>
          <button class="decision-btn btn-data ${dataSel}" onclick="window._setDecision('${gateId}','more-data')">${t("gateNeedData")}</button>
          <button class="decision-btn btn-stop ${stopSel}" onclick="window._setDecision('${gateId}','stop')">${t("gateStop")}</button>
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
          <button onclick="window._addGateNote('${gateId}')">${t("addNoteBtn")}</button>
        </div>
      </div>
    `;

    overlay.classList.add("open");
    document.getElementById("gateModalClose").onclick = () =>
      overlay.classList.remove("open");
    overlay.onclick = (e) => {
      if (e.target === overlay) overlay.classList.remove("open");
    };
  };

  window._toggleCriteria = function (gateId, index) {
    const gate = GATES.find((g) => g.id === gateId);
    if (!gate) return;
    gate.criteria[index].met = !gate.criteria[index].met;
    renderGates();
    renderSummary();
    window._openGate(gateId); // refresh modal
  };

  window._setDecision = function (gateId, decision) {
    const gate = GATES.find((g) => g.id === gateId);
    if (!gate) return;
    gate.decision = decision;
    gate.decisionBy = "PMP";
    gate.decisionDate = new Date().toISOString().split("T")[0];
    renderGates();
    renderSummary();
    window._openGate(gateId);
  };

  window._addGateNote = function (gateId) {
    const gate = GATES.find((g) => g.id === gateId);
    const input = document.getElementById("gateNoteInput");
    if (!gate || !input || !input.value.trim()) return;
    gate.notes.push({
      date: new Date().toISOString().split("T")[0],
      text: input.value.trim(),
    });
    window._openGate(gateId);
  };

  // ── RISK DASHBOARD ────────────────────────────
  function renderRisks() {
    // Filter buttons
    document.querySelectorAll(".filter-btn").forEach((btn) => {
      btn.classList.toggle("active", btn.dataset.filter === activeRiskFilter);
      btn.onclick = () => {
        activeRiskFilter = btn.dataset.filter;
        renderRisks();
      };
    });

    const filtered =
      activeRiskFilter === "all"
        ? RISKS
        : RISKS.filter((r) => r.riskLevel === activeRiskFilter);

    const grid = document.getElementById("riskGrid");
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
        <div class="risk-card risk-level-${r.riskLevel}">
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

    // Top 5 risks
    const sorted = [...RISKS].sort((a, b) => {
      const levelOrder = { red: 0, yellow: 1, green: 2 };
      const sevOrder = { high: 0, medium: 1, low: 2 };
      return (
        levelOrder[a.riskLevel] - levelOrder[b.riskLevel] ||
        sevOrder[a.severity] - sevOrder[b.severity]
      );
    });

    const top5 = sorted.slice(0, 5);
    const topList = document.getElementById("topRisksList");
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
  function renderTimeline() {
    const container = document.getElementById("timelineVisual");
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
  function renderStandards() {
    const tbody = document.getElementById("standardsBody");
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
          <td><span class="std-status-badge ${badgeClass}">${statusText}</span></td>
          <td>
            <div class="progress-cell">
              <div class="progress-bar">
                <div class="progress-bar-fill" style="width:${s.progress}%"></div>
              </div>
              <span class="progress-pct">${s.progress}%</span>
            </div>
          </td>
        </tr>
      `;
    }).join("");
  }

  // ── INPUT PANEL ───────────────────────────────
  function renderInputPanel() {
    const content = document.getElementById("inputPanelContent");
    content.innerHTML =
      STAKEHOLDER_INPUTS.map((inp) => {
        const fromClass = inp.from === "tech" ? "from-tech" : "from-business";
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
        <div class="input-entry ${fromClass}" style="margin-bottom:var(--sp-md)">
          <div class="input-meta">${fromLabel} · ${inp.date} · Gate ${inp.gate} ${statusBadge}</div>
          <div style="margin-top:var(--sp-xs)">${localizedText(inp.content)}</div>
          ${responseHtml}
        </div>
      `;
      }).join("") || `<p style="color:var(--text-muted)">No inputs.</p>`;
  }

  function updateFabBadge() {
    const pending = STAKEHOLDER_INPUTS.filter(
      (i) => i.status === "pending-review",
    ).length;
    const badge = document.getElementById("fabBadge");
    badge.textContent = pending;
    badge.classList.toggle("hidden", pending === 0);
  }

  // ── HELPERS ───────────────────────────────────
  function capitalize(str) {
    if (!str) return "";
    return str.charAt(0).toUpperCase() + str.slice(1).replace(/-/g, " ");
  }
})();
