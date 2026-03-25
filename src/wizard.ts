// ============================================================
// PROJECT SETUP WIZARD — Interactive onboarding questionnaire
// Collects project information and generates all CT data
// ============================================================

import { seed, type WizardAnswers } from "./seed.ts";

const STORAGE_KEY = "ctower_project_data";
const WIZARD_CSS = `
.wizard-overlay {
  position: fixed; inset: 0; z-index: 9999;
  background: rgba(15, 23, 42, 0.85);
  display: flex; align-items: center; justify-content: center;
  font-family: 'Inter', -apple-system, sans-serif;
}
.wizard-card {
  background: #1e293b; border-radius: 16px; padding: 40px;
  width: 90vw; max-width: 680px; max-height: 90vh; overflow-y: auto;
  box-shadow: 0 25px 50px rgba(0,0,0,0.5);
  color: #e2e8f0;
}
.wizard-card h1 {
  margin: 0 0 8px; font-size: 1.6rem; color: #38bdf8;
}
.wizard-card .wiz-sub {
  color: #94a3b8; font-size: 0.9rem; margin-bottom: 24px;
}
.wizard-card .wiz-progress {
  display: flex; gap: 6px; margin-bottom: 28px;
}
.wizard-card .wiz-dot {
  width: 10px; height: 10px; border-radius: 50%;
  background: #334155; transition: background 0.3s;
}
.wizard-card .wiz-dot.active { background: #38bdf8; }
.wizard-card .wiz-dot.done { background: #22c55e; }
.wiz-step { display: none; }
.wiz-step.active { display: block; }
.wiz-step h2 {
  font-size: 1.15rem; color: #f1f5f9; margin: 0 0 16px;
}
.wiz-step p.hint {
  color: #94a3b8; font-size: 0.82rem; margin: -10px 0 16px;
}
.wiz-field { margin-bottom: 18px; }
.wiz-field label {
  display: block; font-size: 0.85rem; color: #cbd5e1;
  margin-bottom: 5px; font-weight: 500;
}
.wiz-field input, .wiz-field select, .wiz-field textarea {
  width: 100%; padding: 10px 12px; border-radius: 8px;
  border: 1px solid #475569; background: #0f172a;
  color: #e2e8f0; font-size: 0.9rem; font-family: inherit;
  outline: none; transition: border-color 0.2s;
  box-sizing: border-box;
}
.wiz-field input:focus, .wiz-field select:focus, .wiz-field textarea:focus {
  border-color: #38bdf8;
}
.wiz-field textarea { resize: vertical; min-height: 72px; }
.wiz-field .wiz-row {
  display: grid; grid-template-columns: 1fr 1fr; gap: 12px;
}
.wiz-actions {
  display: flex; justify-content: space-between; margin-top: 28px;
}
.wiz-btn {
  padding: 10px 24px; border-radius: 8px; border: none;
  font-size: 0.9rem; font-weight: 600; cursor: pointer;
  transition: background 0.2s, transform 0.1s;
}
.wiz-btn:active { transform: scale(0.97); }
.wiz-btn-back {
  background: #334155; color: #cbd5e1;
}
.wiz-btn-back:hover { background: #475569; }
.wiz-btn-next {
  background: #2563eb; color: white;
}
.wiz-btn-next:hover { background: #3b82f6; }
.wiz-btn-finish {
  background: #16a34a; color: white;
}
.wiz-btn-finish:hover { background: #22c55e; }
.wiz-btn-skip {
  background: transparent; color: #64748b; text-decoration: underline;
  padding: 10px 12px;
}
.wiz-btn-skip:hover { color: #94a3b8; }
`;

interface StepDef {
  title: string;
  hint?: string;
  fields: FieldDef[];
}

interface FieldDef {
  key: keyof WizardAnswers;
  label: string;
  type: "text" | "textarea" | "select" | "number";
  placeholder?: string;
  required?: boolean;
  options?: { value: string; label: string }[];
  half?: boolean; // for 2-col layout pairing
}

const STEPS: StepDef[] = [
  {
    title: "Project Basics",
    hint: "Tell us about the medical device project.",
    fields: [
      {
        key: "projectName",
        label: "Project / Device Name",
        type: "text",
        placeholder: "e.g. TiO₂ Medical Air Purification System",
        required: true,
      },
      {
        key: "projectNameCn",
        label: "Project Name (Chinese, optional)",
        type: "text",
        placeholder: "e.g. TiO₂医用空气净化系统",
      },
      {
        key: "subtitle",
        label: "Project Subtitle / Description",
        type: "text",
        placeholder: "e.g. UV-C Photocatalytic Air Cleaning Platform",
      },
      {
        key: "preparedDate",
        label: "Prepared Date",
        type: "text",
        placeholder: "e.g. March 2026",
      },
    ],
  },
  {
    title: "Regulatory Classification",
    hint: "FDA submission pathway and classification details.",
    fields: [
      {
        key: "submissionType",
        label: "Submission Type",
        type: "select",
        options: [
          { value: "510k-standard", label: "510(k) Standard" },
          { value: "510k-special", label: "510(k) Special" },
          { value: "510k-abbreviated", label: "510(k) Abbreviated" },
          { value: "de-novo", label: "De Novo" },
          { value: "pma", label: "PMA" },
          { value: "other", label: "Other / TBD" },
        ],
      },
      {
        key: "deviceClass",
        label: "Device Class",
        type: "select",
        options: [
          { value: "I", label: "Class I" },
          { value: "II", label: "Class II" },
          { value: "III", label: "Class III" },
        ],
      },
      {
        key: "productCode",
        label: "Product Code",
        type: "text",
        placeholder: "e.g. FRA, IKN, QEI",
      },
      {
        key: "regulationSection",
        label: "Regulation Section (CFR)",
        type: "text",
        placeholder: "e.g. § 880.6500",
      },
      {
        key: "predicateDevices",
        label: "Predicate Device(s)",
        type: "textarea",
        placeholder:
          "One per line: Device Name (K-number)\ne.g. AiroCide TiO2 (K023830)",
      },
    ],
  },
  {
    title: "Applicant & Manufacturer",
    hint: "Who is filing and who is building?",
    fields: [
      {
        key: "applicantName",
        label: "Applicant / Sponsor Name",
        type: "text",
        placeholder: "e.g. Titania Labs, LLC",
        required: true,
      },
      {
        key: "applicantNameCn",
        label: "Applicant Name (Chinese, optional)",
        type: "text",
        placeholder: "",
      },
      {
        key: "manufacturerName",
        label: "Manufacturer Name & Location",
        type: "text",
        placeholder: "e.g. Titania Labs, LLC (Gresham, OR)",
      },
      {
        key: "manufacturerNameCn",
        label: "Manufacturer (Chinese, optional)",
        type: "text",
        placeholder: "",
      },
    ],
  },
  {
    title: "Project Timeline & Budget",
    hint: "High-level project scope and financial parameters.",
    fields: [
      {
        key: "projectDurationMonths",
        label: "Total Project Duration (months)",
        type: "number",
        placeholder: "e.g. 12",
      },
      {
        key: "currentMonth",
        label: "Current Month (M+?)",
        type: "number",
        placeholder: "e.g. 0",
      },
      {
        key: "cashOnHand",
        label: "Cash On Hand ($)",
        type: "number",
        placeholder: "e.g. 165000",
      },
      {
        key: "monthlyBurn",
        label: "Monthly Burn Rate ($)",
        type: "number",
        placeholder: "e.g. 8500",
      },
      {
        key: "currency",
        label: "Currency",
        type: "select",
        options: [
          { value: "USD", label: "USD ($)" },
          { value: "CNY", label: "CNY (¥)" },
          { value: "EUR", label: "EUR (€)" },
          { value: "GBP", label: "GBP (£)" },
        ],
      },
    ],
  },
  {
    title: "Team & Key Areas",
    hint: "Key technology areas and team info. Keep it brief — you can add detail later in the dashboard.",
    fields: [
      {
        key: "techAreas",
        label: "Key Technical Areas / Workstreams",
        type: "textarea",
        placeholder:
          "One per line, e.g.:\nUV-C Reactor Design\nHEPA Filtration\nElectrical Safety\nMicrobial Testing",
      },
      {
        key: "teamLead",
        label: "Project Lead Name",
        type: "text",
        placeholder: "e.g. Alex Chen",
      },
      {
        key: "teamSize",
        label: "Approximate Team Size",
        type: "number",
        placeholder: "e.g. 3",
      },
    ],
  },
];

export function hasProjectData(): boolean {
  return localStorage.getItem(STORAGE_KEY) !== null;
}

export function clearProjectData(): void {
  localStorage.removeItem(STORAGE_KEY);
  localStorage.removeItem("ctower_change_requests");
  localStorage.removeItem("ctower_stakeholder_inputs");
  localStorage.removeItem("ctower_qa_messages");
}

export function getSavedAnswers(): WizardAnswers | null {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    return raw ? (JSON.parse(raw) as WizardAnswers) : null;
  } catch {
    return null;
  }
}

function saveAnswers(answers: WizardAnswers): void {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(answers));
}

export function showWizard(onComplete: (answers: WizardAnswers) => void): void {
  // Inject styles
  if (!document.getElementById("wizard-styles")) {
    const style = document.createElement("style");
    style.id = "wizard-styles";
    style.textContent = WIZARD_CSS;
    document.head.appendChild(style);
  }

  let currentStep = 0;
  const answers: Record<string, string | number> = {};

  function render(): void {
    const existing = document.getElementById("wizard-overlay");
    if (existing) existing.remove();

    const overlay = document.createElement("div");
    overlay.id = "wizard-overlay";
    overlay.className = "wizard-overlay";

    const step = STEPS[currentStep];
    const isLast = currentStep === STEPS.length - 1;
    const isFirst = currentStep === 0;

    // Progress dots
    const dots = STEPS.map((_, i) => {
      const cls =
        i < currentStep
          ? "wiz-dot done"
          : i === currentStep
            ? "wiz-dot active"
            : "wiz-dot";
      return `<div class="${cls}"></div>`;
    }).join("");

    // Fields
    let fieldsHtml = "";
    step.fields.forEach((f) => {
      const val = answers[f.key] !== undefined ? String(answers[f.key]) : "";
      let input = "";
      if (f.type === "select" && f.options) {
        const opts = f.options
          .map(
            (o) =>
              `<option value="${o.value}" ${val === o.value ? "selected" : ""}>${o.label}</option>`,
          )
          .join("");
        input = `<select data-key="${f.key}">${opts}</select>`;
      } else if (f.type === "textarea") {
        input = `<textarea data-key="${f.key}" placeholder="${f.placeholder || ""}" rows="3">${val}</textarea>`;
      } else {
        input = `<input type="${f.type}" data-key="${f.key}" value="${val}" placeholder="${f.placeholder || ""}" ${f.required ? "required" : ""}>`;
      }
      fieldsHtml += `<div class="wiz-field"><label>${f.label}${f.required ? " *" : ""}</label>${input}</div>`;
    });

    overlay.innerHTML = `
      <div class="wizard-card">
        <h1>⚕ Control Tower — Project Setup</h1>
        <div class="wiz-sub">Step ${currentStep + 1} of ${STEPS.length}</div>
        <div class="wiz-progress">${dots}</div>
        <div class="wiz-step active">
          <h2>${step.title}</h2>
          ${step.hint ? `<p class="hint">${step.hint}</p>` : ""}
          ${fieldsHtml}
        </div>
        <div class="wiz-actions">
          <div>
            ${!isFirst ? '<button class="wiz-btn wiz-btn-back" id="wiz-back">← Back</button>' : '<button class="wiz-btn wiz-btn-skip" id="wiz-demo">Load Demo Data</button>'}
          </div>
          <div>
            ${isLast ? '<button class="wiz-btn wiz-btn-finish" id="wiz-finish">✓ Generate Dashboard</button>' : '<button class="wiz-btn wiz-btn-next" id="wiz-next">Next →</button>'}
          </div>
        </div>
      </div>
    `;

    document.body.appendChild(overlay);

    // Collect field values
    function collectFields(): void {
      overlay
        .querySelectorAll<
          HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement
        >("[data-key]")
        .forEach((el) => {
          const key = el.dataset.key!;
          const val = el.value.trim();
          if (el.type === "number" && val) {
            answers[key] = parseFloat(val);
          } else if (val) {
            answers[key] = val;
          }
        });
    }

    // Bind buttons
    overlay.querySelector("#wiz-back")?.addEventListener("click", () => {
      collectFields();
      currentStep--;
      render();
    });
    overlay.querySelector("#wiz-next")?.addEventListener("click", () => {
      collectFields();
      // Validate required fields
      const missing = step.fields.filter((f) => f.required && !answers[f.key]);
      if (missing.length) {
        const firstMissing = overlay.querySelector(
          `[data-key="${missing[0].key}"]`,
        ) as HTMLElement;
        firstMissing?.focus();
        firstMissing?.style.setProperty("border-color", "#ef4444");
        return;
      }
      currentStep++;
      render();
    });
    overlay.querySelector("#wiz-finish")?.addEventListener("click", () => {
      collectFields();
      const missing = STEPS[0].fields.filter(
        (f) => f.required && !answers[f.key],
      );
      if (missing.length) {
        currentStep = 0;
        render();
        return;
      }
      const wa = answers as unknown as WizardAnswers;
      saveAnswers(wa);
      overlay.remove();
      onComplete(wa);
    });
    overlay.querySelector("#wiz-demo")?.addEventListener("click", () => {
      overlay.remove();
      // Signal to load hardcoded defaults
      onComplete(null as unknown as WizardAnswers);
    });
  }

  render();
}

/**
 * Apply wizard answers to the live data arrays.
 * Called on boot (after wizard or from saved data).
 */
export function applyProjectData(answers: WizardAnswers): void {
  seed(answers);
}
