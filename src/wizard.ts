// ============================================================
// PROJECT SETUP WIZARD — Interactive onboarding questionnaire
// Fully bilingual: EN / CN based on user's first selection
// ============================================================

import {
  seed,
  type WizardAnswers,
  type TeamEntry,
  type BudgetEntry,
  type SupplierEntry,
} from "./seed.ts";
import { TEMPLATE_LIST, type DeviceTemplate } from "./templates.ts";

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
  width: 90vw; max-width: 720px; max-height: 90vh; overflow-y: auto;
  box-shadow: 0 25px 50px rgba(0,0,0,0.5); color: #e2e8f0;
}
.wizard-card h1 { margin: 0 0 8px; font-size: 1.6rem; color: #38bdf8; }
.wizard-card .wiz-sub { color: #94a3b8; font-size: 0.9rem; margin-bottom: 24px; }
.wizard-card .wiz-progress { display: flex; gap: 6px; margin-bottom: 28px; }
.wizard-card .wiz-dot { width: 10px; height: 10px; border-radius: 50%; background: #334155; transition: background 0.3s; }
.wizard-card .wiz-dot.active { background: #38bdf8; }
.wizard-card .wiz-dot.done { background: #22c55e; }
.wiz-step h2 { font-size: 1.15rem; color: #f1f5f9; margin: 0 0 16px; }
.wiz-step p.hint { color: #94a3b8; font-size: 0.82rem; margin: -10px 0 16px; }
.wiz-field { margin-bottom: 18px; }
.wiz-field label { display: block; font-size: 0.85rem; color: #cbd5e1; margin-bottom: 5px; font-weight: 500; }
.wiz-field input, .wiz-field select, .wiz-field textarea {
  width: 100%; padding: 10px 12px; border-radius: 8px;
  border: 1px solid #475569; background: #0f172a;
  color: #e2e8f0; font-size: 0.9rem; font-family: inherit;
  outline: none; transition: border-color 0.2s; box-sizing: border-box;
}
.wiz-field input:focus, .wiz-field select:focus, .wiz-field textarea:focus { border-color: #38bdf8; }
.wiz-field textarea { resize: vertical; min-height: 72px; }
.wiz-row { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
.wiz-row-3 { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 12px; }
.wiz-actions { display: flex; justify-content: space-between; margin-top: 28px; }
.wiz-btn { padding: 10px 24px; border-radius: 8px; border: none; font-size: 0.9rem; font-weight: 600; cursor: pointer; transition: background 0.2s, transform 0.1s; }
.wiz-btn:active { transform: scale(0.97); }
.wiz-btn-back { background: #334155; color: #cbd5e1; }
.wiz-btn-back:hover { background: #475569; }
.wiz-btn-next { background: #2563eb; color: white; }
.wiz-btn-next:hover { background: #3b82f6; }
.wiz-btn-finish { background: #16a34a; color: white; }
.wiz-btn-finish:hover { background: #22c55e; }
.wiz-btn-skip { background: transparent; color: #64748b; text-decoration: underline; padding: 10px 12px; }
.wiz-btn-skip:hover { color: #94a3b8; }
.wiz-btn-add { background: #1e3a5f; color: #38bdf8; border: 1px dashed #38bdf8; padding: 6px 14px; border-radius: 6px; font-size: 0.82rem; cursor: pointer; margin-top: 8px; }
.wiz-btn-add:hover { background: #1e4976; }
.wiz-btn-remove { background: transparent; color: #ef4444; border: none; cursor: pointer; font-size: 0.85rem; padding: 2px 8px; }
.wiz-entry { background: #0f172a; border: 1px solid #334155; border-radius: 8px; padding: 12px; margin-bottom: 10px; position: relative; }
.wiz-entry .wiz-btn-remove { position: absolute; top: 6px; right: 6px; }
.wiz-lang-choice { display: flex; gap: 16px; justify-content: center; margin: 40px 0; }
.wiz-lang-btn { padding: 20px 40px; border-radius: 12px; border: 2px solid #475569; background: #0f172a; color: #e2e8f0; font-size: 1.1rem; cursor: pointer; transition: all 0.2s; min-width: 200px; text-align: center; }
.wiz-lang-btn:hover { border-color: #38bdf8; background: #1e293b; }
.wiz-lang-btn .flag { font-size: 2rem; display: block; margin-bottom: 8px; }
.wiz-doc-row { margin-bottom: 6px; }
.wiz-doc-row label { display: flex; align-items: center; gap: 8px; cursor: pointer; }
.wiz-doc-row input[type=checkbox] { width: auto; }
.wiz-doc-row .doc-code { color: #94a3b8; font-size: 0.8rem; min-width: 70px; }
.wiz-tmpl-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin: 20px 0; }
.wiz-tmpl-card { background: #0f172a; border: 2px solid #334155; border-radius: 12px; padding: 18px; cursor: pointer; transition: all 0.2s; text-align: left; color: #e2e8f0; }
.wiz-tmpl-card:hover { border-color: #38bdf8; background: #1e293b; transform: translateY(-2px); }
.wiz-tmpl-card .tmpl-icon { font-size: 2rem; margin-bottom: 8px; display: block; }
.wiz-tmpl-card .tmpl-name { font-size: 1rem; font-weight: 600; color: #f1f5f9; margin-bottom: 4px; }
.wiz-tmpl-card .tmpl-desc { font-size: 0.78rem; color: #94a3b8; line-height: 1.4; }
.wiz-tmpl-scratch { background: transparent; border: 2px dashed #475569; border-radius: 12px; padding: 18px; cursor: pointer; transition: all 0.2s; text-align: center; color: #94a3b8; grid-column: 1 / -1; }
.wiz-tmpl-scratch:hover { border-color: #38bdf8; color: #e2e8f0; }
`;

// ── Bilingual helpers ────────────────────────────
type L = { en: string; cn: string };
function tx(label: L, lang: "en" | "cn"): string {
  return lang === "cn" ? label.cn : label.en;
}

const TXT = {
  wizTitle: {
    en: "⚕ Control Tower — Project Setup",
    cn: "⚕ 控制塔 — 项目设置",
  },
  stepOf: { en: "Step {0} of {1}", cn: "第 {0} 步，共 {1} 步" },
  back: { en: "← Back", cn: "← 返回" },
  next: { en: "Next →", cn: "下一步 →" },
  finish: { en: "✓ Generate Dashboard", cn: "✓ 生成仪表板" },
  skipStep: { en: "Skip →", cn: "跳过 →" },
  addAnother: { en: "+ Add Another", cn: "+ 添加" },
  remove: { en: "✕", cn: "✕" },

  tmplTitle: { en: "Choose a Device Category", cn: "选择设备类别" },
  tmplHint: {
    en: "Select a template to pre-fill regulatory, risk, and standards data — or start from scratch.",
    cn: "选择模板预填法规、风险和标准数据，或从头开始。",
  },
  tmplScratch: { en: "✎ Start from Scratch", cn: "✎ 从头开始" },
  tmplScratchDesc: {
    en: "Enter all project details manually without a template.",
    cn: "不使用模板，手动输入所有项目信息。",
  },

  s1Title: { en: "Project Basics", cn: "项目基本信息" },
  s1Hint: {
    en: "Tell us about the medical device project.",
    cn: "请介绍医疗器械项目。",
  },
  projectName: { en: "Project / Device Name *", cn: "项目 / 设备名称 *" },
  projectNamePh: {
    en: "e.g. TiO₂ Medical Air Purification System",
    cn: "例: TiO₂医用空气净化系统",
  },
  projectNameCn: { en: "Project Name (Chinese)", cn: "项目名称（中文）" },
  subtitle: { en: "Project Subtitle / Description", cn: "项目副标题 / 描述" },
  subtitlePh: {
    en: "e.g. UV-C Photocatalytic Air Cleaning Platform",
    cn: "例: UV-C光催化空气清洁平台",
  },
  preparedDate: { en: "Prepared Date", cn: "准备日期" },
  preparedDatePh: { en: "e.g. March 2026", cn: "例: 2026年3月" },
  contactEmail: { en: "Primary Contact Email *", cn: "主要联系人邮箱 *" },
  contactEmailPh: {
    en: "e.g. project@company.com",
    cn: "例: project@company.com",
  },

  s2Title: { en: "Regulatory Classification", cn: "法规分类" },
  s2Hint: {
    en: "FDA submission pathway and classification details.",
    cn: "FDA提交途径和分类详情。",
  },
  submissionType: { en: "Submission Type", cn: "提交类型" },
  deviceClass: { en: "Device Class", cn: "设备分类" },
  productCode: { en: "Product Code", cn: "产品代码" },
  productCodePh: { en: "e.g. FRA, IKN, QEI", cn: "例: FRA, IKN, QEI" },
  regulationSection: { en: "Regulation Section (CFR)", cn: "法规章节 (CFR)" },
  regulationSectionPh: { en: "e.g. § 880.6500", cn: "例: § 880.6500" },
  predicateDevices: { en: "Predicate Device(s)", cn: "前置器械" },
  predicateDevicesPh: {
    en: "One per line: Name (K-number)\ne.g. AiroCide TiO2 (K023830)",
    cn: "每行一个: 名称 (K编号)\n例: AiroCide TiO2 (K023830)",
  },

  s3Title: { en: "Applicant & Manufacturer", cn: "申请人和制造商" },
  s3Hint: {
    en: "Who is filing and who is building?",
    cn: "谁在申请？谁在制造？",
  },
  applicantName: {
    en: "Applicant / Sponsor Name *",
    cn: "申请人 / 发起人名称 *",
  },
  applicantNamePh: {
    en: "e.g. Titania Labs, LLC",
    cn: "例: Titania Labs, LLC",
  },
  applicantNameCn: { en: "Applicant Name (Chinese)", cn: "申请人名称（中文）" },
  manufacturerName: {
    en: "Manufacturer Name & Location",
    cn: "制造商名称和地点",
  },
  manufacturerNamePh: {
    en: "e.g. Titania Labs, LLC (Gresham, OR)",
    cn: "例: Titania Labs, LLC (Gresham, OR)",
  },
  manufacturerNameCn: {
    en: "Manufacturer Name (Chinese)",
    cn: "制造商名称（中文）",
  },

  s4Title: { en: "Team & Resource Allocation", cn: "团队和资源分配" },
  s4Hint: {
    en: "Add team members with roles, emails, and workstream allocations.",
    cn: "添加团队成员及其角色、邮箱和工作流分配。",
  },
  memberName: { en: "Name", cn: "姓名" },
  memberRole: { en: "Role", cn: "角色" },
  memberEmail: { en: "Email", cn: "邮箱" },
  memberWorkstreams: {
    en: "Workstreams (one per line: name: %)",
    cn: "工作流（每行一个: 名称: %）",
  },
  memberWorkstreamsPh: {
    en: "e.g.\nProject Management: 40\nRegulatory: 30\nEngineering: 30",
    cn: "例:\n项目管理: 40\n法规: 30\n工程: 30",
  },

  s5Title: { en: "Budget Categories", cn: "预算类别" },
  s5Hint: {
    en: "Set planned budget amounts per category. Actual spend tracked in dashboard.",
    cn: "设置每个类别的计划预算。实际支出在仪表板中跟踪。",
  },
  budgetLabel: { en: "Category", cn: "类别" },
  budgetPlanned: { en: "Planned ($)", cn: "计划 ($)" },
  cashOnHand: { en: "Cash On Hand ($)", cn: "现金余额 ($)" },
  cashOnHandPh: { en: "e.g. 165000", cn: "例: 165000" },
  currency: { en: "Currency", cn: "货币" },

  s6Title: { en: "Probable Timeline", cn: "预计时间线" },
  s6Hint: {
    en: "Estimate project duration and key technical workstreams.",
    cn: "估计项目工期和关键技术工作流。",
  },
  projectDuration: {
    en: "Total Project Duration (months)",
    cn: "项目总工期（月）",
  },
  projectDurationPh: { en: "e.g. 12", cn: "例: 12" },
  currentMonth: { en: "Current Month (M+?)", cn: "当前月份 (M+?)" },
  currentMonthPh: { en: "e.g. 0", cn: "例: 0" },
  techAreas: { en: "Key Technical Workstreams", cn: "关键技术工作流" },
  techAreasPh: {
    en: "One per line, e.g.:\nUV-C Reactor Design\nHEPA Filtration\nElectrical Safety",
    cn: "每行一个，例:\nUV-C反应器设计\nHEPA过滤\n电气安全",
  },

  s7Title: { en: "Suppliers / Vendors (optional)", cn: "供应商（可选）" },
  s7Hint: {
    en: "Add key suppliers. You can skip this and add them later.",
    cn: "添加关键供应商。可跳过，稍后在仪表板中添加。",
  },
  supplierName: { en: "Supplier Name", cn: "供应商名称" },
  supplierComponent: { en: "Component / Service", cn: "组件 / 服务" },
  supplierLead: { en: "Lead Time (days)", cn: "交货期（天）" },

  s8Title: { en: "DHF Documents (Pre-loaded)", cn: "设计历史文件 (预加载)" },
  s8Hint: {
    en: "Standard regulatory documents are pre-loaded. Uncheck any that don't apply.",
    cn: "标准法规文件已预加载。取消勾选不适用的文件。",
  },
};

const DEFAULT_BUDGET_CATS: L[] = [
  { en: "Prototype & Materials", cn: "原型和材料" },
  { en: "Lab Testing & Validation", cn: "实验室测试和验证" },
  { en: "Regulatory & Legal", cn: "法规和法律" },
  { en: "Personnel", cn: "人员" },
  { en: "Clinical Studies", cn: "临床研究" },
  { en: "Equipment & Software", cn: "设备和软件" },
  { en: "Manufacturing Setup", cn: "生产线建设" },
  { en: "Travel & Conferences", cn: "差旅和会议" },
];

export const DEFAULT_DHF_DOCS = [
  { code: "DHF-DP", en: "Design Plan", cn: "设计计划" },
  { code: "DHF-DI", en: "Design Inputs", cn: "设计输入" },
  { code: "DHF-DO", en: "Design Outputs", cn: "设计输出" },
  { code: "DHF-DV", en: "Design Verification Report", cn: "设计验证报告" },
  { code: "DHF-VAL", en: "Design Validation Report", cn: "设计确认报告" },
  {
    code: "DHF-RA",
    en: "Risk Analysis (ISO 14971)",
    cn: "风险分析 (ISO 14971)",
  },
  {
    code: "DHF-SW",
    en: "Software Documentation (IEC 62304)",
    cn: "软件文档 (IEC 62304)",
  },
  { code: "DHF-BIO", en: "Biocompatibility Report", cn: "生物相容性报告" },
  {
    code: "DHF-EMC",
    en: "EMC Test Report (IEC 60601-1-2)",
    cn: "EMC测试报告 (IEC 60601-1-2)",
  },
  {
    code: "DHF-LBL",
    en: "Labeling & IFU (21 CFR 801)",
    cn: "标签和IFU (21 CFR 801)",
  },
  { code: "DHF-CL", en: "Submission Cover Letter", cn: "提交附信" },
  { code: "DHF-DD", en: "Device Description", cn: "设备描述" },
];

// ── HTML helpers ─────────────────────────────────
function fld(label: string, html: string): string {
  return `<div class="wiz-field"><label>${label}</label>${html}</div>`;
}
function inp(
  key: string,
  v: string,
  ph: string,
  type = "text",
  req = false,
): string {
  return `<input type="${type}" data-key="${key}" value="${esc(v)}" placeholder="${esc(ph)}" ${req ? "required" : ""}>`;
}
function sel(key: string, v: string, opts: { v: string; l: string }[]): string {
  return `<select data-key="${key}">${opts.map((o) => `<option value="${o.v}" ${v === o.v ? "selected" : ""}>${o.l}</option>`).join("")}</select>`;
}
function ta(key: string, v: string, ph: string, rows = 3): string {
  return `<textarea data-key="${key}" placeholder="${esc(ph)}" rows="${rows}">${escH(v)}</textarea>`;
}
function esc(s: string): string {
  return s.replace(/&/g, "&amp;").replace(/"/g, "&quot;").replace(/</g, "&lt;");
}
function escH(s: string): string {
  return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}
function gv(data: Record<string, unknown>, key: string): string {
  const v = data[key];
  return v != null ? String(v) : "";
}

// ── Step renderers ──────────────────────────────
type WizData = Record<string, unknown>;

function renderBasics(el: HTMLElement, d: WizData, lang: "en" | "cn"): void {
  el.innerHTML = `<h2>${tx(TXT.s1Title, lang)}</h2><p class="hint">${tx(TXT.s1Hint, lang)}</p>
  ${fld(tx(TXT.projectName, lang), inp("projectName", gv(d, "projectName"), tx(TXT.projectNamePh, lang), "text", true))}
  ${lang === "cn" ? fld(tx(TXT.projectNameCn, lang), inp("projectNameCn", gv(d, "projectNameCn"), "")) : ""}
  ${fld(tx(TXT.subtitle, lang), inp("subtitle", gv(d, "subtitle"), tx(TXT.subtitlePh, lang)))}
  ${fld(tx(TXT.preparedDate, lang), inp("preparedDate", gv(d, "preparedDate"), tx(TXT.preparedDatePh, lang)))}
  ${fld(tx(TXT.contactEmail, lang), inp("contactEmail", gv(d, "contactEmail"), tx(TXT.contactEmailPh, lang), "email", true))}`;
}

function renderRegulatory(
  el: HTMLElement,
  d: WizData,
  lang: "en" | "cn",
): void {
  el.innerHTML = `<h2>${tx(TXT.s2Title, lang)}</h2><p class="hint">${tx(TXT.s2Hint, lang)}</p>
  ${fld(
    tx(TXT.submissionType, lang),
    sel("submissionType", gv(d, "submissionType"), [
      { v: "510k-standard", l: "510(k) Standard" },
      { v: "510k-special", l: "510(k) Special" },
      { v: "510k-abbreviated", l: "510(k) Abbreviated" },
      { v: "de-novo", l: "De Novo" },
      { v: "pma", l: "PMA" },
      { v: "other", l: lang === "cn" ? "其他 / 待定" : "Other / TBD" },
    ]),
  )}
  ${fld(
    tx(TXT.deviceClass, lang),
    sel("deviceClass", gv(d, "deviceClass"), [
      { v: "I", l: lang === "cn" ? "I类" : "Class I" },
      { v: "II", l: lang === "cn" ? "II类" : "Class II" },
      { v: "III", l: lang === "cn" ? "III类" : "Class III" },
    ]),
  )}
  ${fld(tx(TXT.productCode, lang), inp("productCode", gv(d, "productCode"), tx(TXT.productCodePh, lang)))}
  ${fld(tx(TXT.regulationSection, lang), inp("regulationSection", gv(d, "regulationSection"), tx(TXT.regulationSectionPh, lang)))}
  ${fld(tx(TXT.predicateDevices, lang), ta("predicateDevices", gv(d, "predicateDevices"), tx(TXT.predicateDevicesPh, lang)))}`;
}

function renderApplicant(el: HTMLElement, d: WizData, lang: "en" | "cn"): void {
  el.innerHTML = `<h2>${tx(TXT.s3Title, lang)}</h2><p class="hint">${tx(TXT.s3Hint, lang)}</p>
  ${fld(tx(TXT.applicantName, lang), inp("applicantName", gv(d, "applicantName"), tx(TXT.applicantNamePh, lang), "text", true))}
  ${lang === "cn" ? fld(tx(TXT.applicantNameCn, lang), inp("applicantNameCn", gv(d, "applicantNameCn"), "")) : ""}
  ${fld(tx(TXT.manufacturerName, lang), inp("manufacturerName", gv(d, "manufacturerName"), tx(TXT.manufacturerNamePh, lang)))}
  ${lang === "cn" ? fld(tx(TXT.manufacturerNameCn, lang), inp("manufacturerNameCn", gv(d, "manufacturerNameCn"), "")) : ""}`;
}

function renderTeam(el: HTMLElement, d: WizData, lang: "en" | "cn"): void {
  const team = (d.team as TeamEntry[] | undefined) || [];
  if (!team.length) {
    team.push({ name: "", role: "", email: "", workstreams: "" });
    d.team = team;
  }
  let h = `<h2>${tx(TXT.s4Title, lang)}</h2><p class="hint">${tx(TXT.s4Hint, lang)}</p>`;
  team.forEach((m, i) => {
    h += `<div class="wiz-entry"><button class="wiz-btn-remove" data-remove-team="${i}">${tx(TXT.remove, lang)}</button>
    <div class="wiz-row">${fld(
      tx(TXT.memberName, lang),
      `<input data-team="name" data-idx="${i}" value="${esc(m.name)}">`,
    )}${fld(tx(TXT.memberRole, lang), `<input data-team="role" data-idx="${i}" value="${esc(m.role)}">`)}
    </div>${fld(tx(TXT.memberEmail, lang), `<input type="email" data-team="email" data-idx="${i}" value="${esc(m.email)}">`)}
    ${fld(tx(TXT.memberWorkstreams, lang), `<textarea data-team="workstreams" data-idx="${i}" placeholder="${esc(tx(TXT.memberWorkstreamsPh, lang))}" rows="3">${escH(m.workstreams)}</textarea>`)}
    </div>`;
  });
  h += `<button class="wiz-btn-add" id="wiz-add-team">${tx(TXT.addAnother, lang)}</button>`;
  el.innerHTML = h;
}

function collectTeam(ov: HTMLElement, d: WizData): void {
  const team = (d.team as TeamEntry[]) || [];
  ov.querySelectorAll<HTMLInputElement | HTMLTextAreaElement>(
    "[data-team]",
  ).forEach((e) => {
    const i = parseInt(e.dataset.idx!, 10);
    if (team[i]) team[i][e.dataset.team as keyof TeamEntry] = e.value.trim();
  });
}

function renderBudgetStep(
  el: HTMLElement,
  d: WizData,
  lang: "en" | "cn",
): void {
  const budgets =
    (d.budgets as BudgetEntry[] | undefined) ||
    DEFAULT_BUDGET_CATS.map((c) => ({ label: tx(c, lang), planned: 0 }));
  d.budgets = budgets;
  let h = `<h2>${tx(TXT.s5Title, lang)}</h2><p class="hint">${tx(TXT.s5Hint, lang)}</p>
  <div class="wiz-row">${fld(tx(TXT.cashOnHand, lang), inp("cashOnHand", gv(d, "cashOnHand"), tx(TXT.cashOnHandPh, lang), "number"))}
  ${fld(
    tx(TXT.currency, lang),
    sel("currency", gv(d, "currency") || "USD", [
      { v: "USD", l: "USD ($)" },
      { v: "CNY", l: "CNY (¥)" },
      { v: "EUR", l: "EUR (€)" },
      { v: "GBP", l: "GBP (£)" },
    ]),
  )}</div><div style="margin-top:12px">`;
  budgets.forEach((b, i) => {
    h += `<div class="wiz-row" style="margin-bottom:8px;align-items:end">
    ${fld(tx(TXT.budgetLabel, lang), `<input data-bud="label" data-idx="${i}" value="${esc(b.label)}">`)}
    ${fld(tx(TXT.budgetPlanned, lang), `<input type="number" data-bud="planned" data-idx="${i}" value="${b.planned || ""}" placeholder="0">`)}
    </div>`;
  });
  h += `<button class="wiz-btn-add" id="wiz-add-budget">${tx(TXT.addAnother, lang)}</button></div>`;
  el.innerHTML = h;
}

function collectBudget(ov: HTMLElement, d: WizData): void {
  const budgets = d.budgets as BudgetEntry[];
  ov.querySelectorAll<HTMLInputElement>("[data-bud]").forEach((e) => {
    const i = parseInt(e.dataset.idx!, 10);
    if (!budgets[i]) return;
    if (e.dataset.bud === "planned")
      budgets[i].planned = parseFloat(e.value) || 0;
    else budgets[i].label = e.value.trim();
  });
  collectSimple(ov, d);
}

function renderTimelineStep(
  el: HTMLElement,
  d: WizData,
  lang: "en" | "cn",
): void {
  el.innerHTML = `<h2>${tx(TXT.s6Title, lang)}</h2><p class="hint">${tx(TXT.s6Hint, lang)}</p>
  <div class="wiz-row">${fld(tx(TXT.projectDuration, lang), inp("projectDurationMonths", gv(d, "projectDurationMonths"), tx(TXT.projectDurationPh, lang), "number"))}
  ${fld(tx(TXT.currentMonth, lang), inp("currentMonth", gv(d, "currentMonth"), tx(TXT.currentMonthPh, lang), "number"))}</div>
  ${fld(tx(TXT.techAreas, lang), ta("techAreas", gv(d, "techAreas"), tx(TXT.techAreasPh, lang), 5))}`;
}

function renderSuppliersStep(
  el: HTMLElement,
  d: WizData,
  lang: "en" | "cn",
): void {
  const suppliers = (d.suppliers as SupplierEntry[] | undefined) || [];
  if (!suppliers.length) {
    suppliers.push({ name: "", component: "", leadTimeDays: 0 });
    d.suppliers = suppliers;
  }
  let h = `<h2>${tx(TXT.s7Title, lang)}</h2><p class="hint">${tx(TXT.s7Hint, lang)}</p>`;
  suppliers.forEach((s, i) => {
    h += `<div class="wiz-entry"><button class="wiz-btn-remove" data-remove-sup="${i}">${tx(TXT.remove, lang)}</button>
    <div class="wiz-row-3">${fld(tx(TXT.supplierName, lang), `<input data-sup="name" data-idx="${i}" value="${esc(s.name)}">`)}
    ${fld(tx(TXT.supplierComponent, lang), `<input data-sup="component" data-idx="${i}" value="${esc(s.component)}">`)}
    ${fld(tx(TXT.supplierLead, lang), `<input type="number" data-sup="leadTimeDays" data-idx="${i}" value="${s.leadTimeDays || ""}" placeholder="0">`)}</div></div>`;
  });
  h += `<button class="wiz-btn-add" id="wiz-add-supplier">${tx(TXT.addAnother, lang)}</button>`;
  el.innerHTML = h;
}

function collectSuppliers(ov: HTMLElement, d: WizData): void {
  const suppliers = d.suppliers as SupplierEntry[];
  ov.querySelectorAll<HTMLInputElement>("[data-sup]").forEach((e) => {
    const i = parseInt(e.dataset.idx!, 10);
    if (!suppliers[i]) return;
    const f = e.dataset.sup!;
    if (f === "leadTimeDays")
      suppliers[i].leadTimeDays = parseInt(e.value) || 0;
    else if (f === "name") suppliers[i].name = e.value.trim();
    else if (f === "component") suppliers[i].component = e.value.trim();
  });
}

function renderDocsStep(el: HTMLElement, d: WizData, lang: "en" | "cn"): void {
  const flags = (d.docFlags as boolean[]) || DEFAULT_DHF_DOCS.map(() => true);
  d.docFlags = flags;
  let h = `<h2>${tx(TXT.s8Title, lang)}</h2><p class="hint">${tx(TXT.s8Hint, lang)}</p>`;
  DEFAULT_DHF_DOCS.forEach((doc, i) => {
    h += `<div class="wiz-doc-row"><label>
      <input type="checkbox" data-doc="${i}" ${flags[i] !== false ? "checked" : ""}>
      <span class="doc-code">${doc.code}</span><span>${tx(doc, lang)}</span>
    </label></div>`;
  });
  el.innerHTML = h;
}

function collectDocs(ov: HTMLElement, d: WizData): void {
  const flags: boolean[] = DEFAULT_DHF_DOCS.map(() => true);
  ov.querySelectorAll<HTMLInputElement>("[data-doc]").forEach((e) => {
    flags[parseInt(e.dataset.doc!, 10)] = e.checked;
  });
  d.docFlags = flags;
}

function collectSimple(ov: HTMLElement, d: WizData): void {
  ov.querySelectorAll<
    HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement
  >("[data-key]").forEach((e) => {
    const v = e.value.trim();
    if (e.type === "number" && v) d[e.dataset.key!] = parseFloat(v);
    else if (v) d[e.dataset.key!] = v;
  });
}

// Step definitions
type Renderer = (el: HTMLElement, d: WizData, lang: "en" | "cn") => void;
type Collector = (ov: HTMLElement, d: WizData) => void;
const RENDERERS: Renderer[] = [
  renderBasics,
  renderRegulatory,
  renderApplicant,
  renderTeam,
  renderBudgetStep,
  renderTimelineStep,
  renderSuppliersStep,
  renderDocsStep,
];
const COLLECTORS: Collector[] = [
  collectSimple,
  collectSimple,
  collectSimple,
  collectTeam,
  collectBudget,
  collectSimple,
  collectSuppliers,
  collectDocs,
];
const SKIPPABLE = new Set([6]); // suppliers

// ── Public API ───────────────────────────────────
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

export function showWizard(onComplete: (answers: WizardAnswers) => void): void {
  if (!document.getElementById("wizard-styles")) {
    const s = document.createElement("style");
    s.id = "wizard-styles";
    s.textContent = WIZARD_CSS;
    document.head.appendChild(s);
  }

  let phase: "lang" | "template" | "steps" = "lang";
  let step = 0;
  const data: WizData = { lang: "en" };

  function applyTemplate(tmpl: DeviceTemplate, lang: "en" | "cn"): void {
    data.templateId = tmpl.id;
    data.submissionType = tmpl.submissionType;
    data.deviceClass = tmpl.deviceClass;
    data.productCode = tmpl.productCodes;
    data.regulationSection = tmpl.regulationSection;
    data.predicateDevices = tmpl.predicateExamples;
    data.techAreas = lang === "cn" ? tmpl.techAreas.cn : tmpl.techAreas.en;
    data.projectDurationMonths = tmpl.estimatedDuration;
    data.budgets = tmpl.budgetCategories.map((c) => ({
      label: lang === "cn" ? c.cn : c.en,
      planned: 0,
    }));
  }

  function render(): void {
    document.getElementById("wizard-overlay")?.remove();
    const ov = document.createElement("div");
    ov.id = "wizard-overlay";
    ov.className = "wizard-overlay";

    if (phase === "lang") {
      ov.innerHTML = `<div class="wizard-card">
        <h1>${TXT.wizTitle.en}</h1>
        <div class="wiz-step" style="display:block">
          <h2>${TXT.s1Title.en} / ${TXT.s1Title.cn}</h2>
          <p class="hint">Choose your preferred language for the wizard and dashboard.<br>为向导和仪表板选择您的首选语言。</p>
          <div class="wiz-lang-choice">
            <button class="wiz-lang-btn" data-lang="en"><span class="flag">🇺🇸</span>English</button>
            <button class="wiz-lang-btn" data-lang="cn"><span class="flag">🇨🇳</span>中文</button>
          </div>
          <div class="wiz-actions"><div><button class="wiz-btn wiz-btn-skip" id="wiz-demo">Load Demo Data / 加载演示数据</button></div><div></div></div>
        </div></div>`;
      document.body.appendChild(ov);
      ov.querySelectorAll<HTMLButtonElement>("[data-lang]").forEach((b) => {
        b.addEventListener("click", () => {
          data.lang = b.dataset.lang!;
          phase = "template";
          render();
        });
      });
      ov.querySelector("#wiz-demo")?.addEventListener("click", () => {
        ov.remove();
        onComplete(null as unknown as WizardAnswers);
      });
      return;
    }

    if (phase === "template") {
      const lang = data.lang as "en" | "cn";
      let cards = "";
      TEMPLATE_LIST.forEach((t) => {
        cards += `<button class="wiz-tmpl-card" data-tmpl="${t.id}">
          <span class="tmpl-icon">${t.icon}</span>
          <div class="tmpl-name">${lang === "cn" ? t.name.cn : t.name.en}</div>
          <div class="tmpl-desc">${lang === "cn" ? t.description.cn : t.description.en}</div>
        </button>`;
      });
      cards += `<button class="wiz-tmpl-scratch" id="wiz-scratch">
        <div class="tmpl-name">${tx(TXT.tmplScratch, lang)}</div>
        <div class="tmpl-desc">${tx(TXT.tmplScratchDesc, lang)}</div>
      </button>`;

      ov.innerHTML = `<div class="wizard-card">
        <h1>${tx(TXT.wizTitle, lang)}</h1>
        <div class="wiz-step" style="display:block">
          <h2>${tx(TXT.tmplTitle, lang)}</h2>
          <p class="hint">${tx(TXT.tmplHint, lang)}</p>
          <div class="wiz-tmpl-grid">${cards}</div>
          <div class="wiz-actions"><div><button class="wiz-btn wiz-btn-back" id="wiz-tmpl-back">← Language</button></div><div></div></div>
        </div></div>`;
      document.body.appendChild(ov);

      ov.querySelectorAll<HTMLButtonElement>("[data-tmpl]").forEach((b) => {
        b.addEventListener("click", () => {
          const tmpl = TEMPLATE_LIST.find((t) => t.id === b.dataset.tmpl!);
          if (tmpl) applyTemplate(tmpl, lang);
          phase = "steps";
          step = 0;
          render();
        });
      });
      ov.querySelector("#wiz-scratch")?.addEventListener("click", () => {
        data.templateId = "";
        phase = "steps";
        step = 0;
        render();
      });
      ov.querySelector("#wiz-tmpl-back")?.addEventListener("click", () => {
        phase = "lang";
        render();
      });
      return;
    }

    const lang = data.lang as "en" | "cn";
    const total = RENDERERS.length;
    const isLast = step === total - 1;
    const dots = RENDERERS.map(
      (_, i) =>
        `<div class="${i < step ? "wiz-dot done" : i === step ? "wiz-dot active" : "wiz-dot"}"></div>`,
    ).join("");
    const label = tx(TXT.stepOf, lang)
      .replace("{0}", String(step + 1))
      .replace("{1}", String(total));

    ov.innerHTML = `<div class="wizard-card">
      <h1>${tx(TXT.wizTitle, lang)}</h1>
      <div class="wiz-sub">${label}</div>
      <div class="wiz-progress">${dots}</div>
      <div class="wiz-step" id="wiz-body" style="display:block"></div>
      <div class="wiz-actions">
        <div>${
          step === 0
            ? `<button class="wiz-btn wiz-btn-back" id="wiz-tolang">← Template</button>`
            : `<button class="wiz-btn wiz-btn-back" id="wiz-back">${tx(TXT.back, lang)}</button>`
        }</div>
        <div style="display:flex;gap:8px">${SKIPPABLE.has(step) ? `<button class="wiz-btn wiz-btn-skip" id="wiz-skip">${tx(TXT.skipStep, lang)}</button>` : ""}
        ${isLast ? `<button class="wiz-btn wiz-btn-finish" id="wiz-finish">${tx(TXT.finish, lang)}</button>` : `<button class="wiz-btn wiz-btn-next" id="wiz-next">${tx(TXT.next, lang)}</button>`}</div>
      </div></div>`;
    document.body.appendChild(ov);

    const body = ov.querySelector("#wiz-body") as HTMLElement;
    RENDERERS[step](body, data, lang);
    bindDynamic(ov, body, lang);

    ov.querySelector("#wiz-tolang")?.addEventListener("click", () => {
      COLLECTORS[step](ov, data);
      phase = "template";
      render();
    });
    ov.querySelector("#wiz-back")?.addEventListener("click", () => {
      COLLECTORS[step](ov, data);
      step--;
      render();
    });
    ov.querySelector("#wiz-next")?.addEventListener("click", () => {
      COLLECTORS[step](ov, data);
      step++;
      render();
    });
    ov.querySelector("#wiz-skip")?.addEventListener("click", () => {
      step++;
      render();
    });
    ov.querySelector("#wiz-finish")?.addEventListener("click", () => {
      COLLECTORS[step](ov, data);
      if (!data.projectName) {
        step = 0;
        render();
        return;
      }
      localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
      ov.remove();
      onComplete(data as unknown as WizardAnswers);
    });
  }

  function bindDynamic(
    ov: HTMLElement,
    body: HTMLElement,
    lang: "en" | "cn",
  ): void {
    const rebind = () => {
      RENDERERS[step](body, data, lang);
      bindDynamic(ov, body, lang);
    };

    ov.querySelector("#wiz-add-team")?.addEventListener("click", () => {
      collectTeam(ov, data);
      (data.team as TeamEntry[]).push({
        name: "",
        role: "",
        email: "",
        workstreams: "",
      });
      rebind();
    });
    ov.querySelector("#wiz-add-budget")?.addEventListener("click", () => {
      collectBudget(ov, data);
      (data.budgets as BudgetEntry[]).push({ label: "", planned: 0 });
      rebind();
    });
    ov.querySelector("#wiz-add-supplier")?.addEventListener("click", () => {
      collectSuppliers(ov, data);
      (data.suppliers as SupplierEntry[]).push({
        name: "",
        component: "",
        leadTimeDays: 0,
      });
      rebind();
    });
    ov.querySelectorAll<HTMLButtonElement>("[data-remove-team]").forEach(
      (b) => {
        b.addEventListener("click", () => {
          collectTeam(ov, data);
          const t = data.team as TeamEntry[];
          t.splice(parseInt(b.dataset.removeTeam!, 10), 1);
          if (!t.length)
            t.push({ name: "", role: "", email: "", workstreams: "" });
          rebind();
        });
      },
    );
    ov.querySelectorAll<HTMLButtonElement>("[data-remove-sup]").forEach((b) => {
      b.addEventListener("click", () => {
        collectSuppliers(ov, data);
        const s = data.suppliers as SupplierEntry[];
        s.splice(parseInt(b.dataset.removeSup!, 10), 1);
        if (!s.length) s.push({ name: "", component: "", leadTimeDays: 0 });
        rebind();
      });
    });
  }

  render();
}

export function applyProjectData(answers: WizardAnswers): void {
  seed(answers);
}
