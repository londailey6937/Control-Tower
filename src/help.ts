// ============================================================
// HELP — In-App User Guide (EN + CN), searchable HTML overlay
// ============================================================

import { localizedText } from "./i18n";
import type { LocalizedString } from "./types";

// ── Guide content structure ────────────────────
interface HelpSection {
  num: number;
  title: LocalizedString;
  content: LocalizedString; // HTML string
}

const GUIDE: HelpSection[] = [
  {
    num: 1,
    title: { en: "Getting Started", cn: "入门指南" },
    content: {
      en: `<p>The Control Tower PM Dashboard is a comprehensive project management platform designed specifically for FDA 510(k) medical device development. It provides real-time visibility across regulatory, technical, and business workstreams.</p>
<h4>System Requirements</h4>
<ul><li>Modern web browser (Chrome, Firefox, Safari, Edge)</li><li>Internet connection for Supabase sync (offline mode available)</li><li>Screen resolution 1280x720 or higher recommended</li></ul>
<h4>First Launch</h4>
<p>When you first open the dashboard, the Setup Wizard will guide you through project configuration. You can choose from 7 device templates (Respiratory, Cardiovascular, Orthopedic, IVD, Imaging, Rehabilitation, SaMD) or start from scratch. Alternatively, click 'Load Demo Data' to explore with sample data.</p>
<h4>Login &amp; Authentication</h4>
<p>The dashboard uses a role-based login. Enter the password provided by your project administrator. After authentication, you will see the dashboard with tabs appropriate for your assigned role and subscription tier.</p>
<div class="help-tip">💡 Bookmark the dashboard URL for quick access. Your project data is saved automatically.</div>`,
      cn: `<p>Control Tower PM仪表板是专为FDA 510(k)医疗器械开发设计的综合项目管理平台。它提供跨法规、技术和业务工作流的实时可见性。</p>
<h4>系统要求</h4>
<ul><li>现代Web浏览器（Chrome、Firefox、Safari、Edge）</li><li>用于Supabase同步的互联网连接（支持离线模式）</li><li>建议屏幕分辨率1280x720或更高</li></ul>
<h4>首次启动</h4>
<p>首次打开仪表板时，设置向导将引导您完成项目配置。您可以从7个设备模板中选择（呼吸、心血管、骨科、IVD、影像、康复、SaMD），或从头开始。也可以点击"加载演示数据"使用示例数据探索。</p>
<h4>登录与身份验证</h4>
<p>仪表板使用基于角色的登录。输入项目管理员提供的密码。认证后，您将看到与您分配的角色和订阅层级相对应的标签页。</p>
<div class="help-tip">💡 收藏仪表板URL以便快速访问。您的项目数据会自动保存。</div>`,
    },
  },
  {
    num: 2,
    title: { en: "Dashboard Overview", cn: "仪表板概览" },
    content: {
      en: `<p>The dashboard consists of a header bar with role/tier selectors, a horizontal tab navigation bar with 16 functional tabs, and a main content area. Each tab focuses on a specific aspect of the 510(k) project lifecycle.</p>
<h4>Header Bar</h4>
<ul><li>Project name and subtitle (bilingual EN/CN)</li><li>Role selector: Switch between PMP, Technology, Business, and Accounting views</li><li>Tier indicator: Shows your current subscription tier (Starter/Growth/Scale)</li><li>Language toggle: Switch between English and Chinese interface</li></ul>
<h4>The 16 Tabs</h4>
<table class="help-table"><thead><tr><th>Tab</th><th>Description</th></tr></thead><tbody>
<tr><td><strong>Dual-Track</strong></td><td>Technical and regulatory milestone tracking</td></tr>
<tr><td><strong>Gate System</strong></td><td>Phase-gate reviews with criteria checklists</td></tr>
<tr><td><strong>Regulatory Tracker</strong></td><td>Standards compliance and progress monitoring</td></tr>
<tr><td><strong>Risk Dashboard</strong></td><td>ISO 14971 risk matrix with severity/probability</td></tr>
<tr><td><strong>Audit Trail</strong></td><td>Timestamped log of all dashboard changes</td></tr>
<tr><td><strong>Document Control</strong></td><td>ISO 13485-aligned document lifecycle management</td></tr>
<tr><td><strong>Actions</strong></td><td>Task board, DHF Tracker, DMR Tracker, CAPA Log</td></tr>
<tr><td><strong>Timeline</strong></td><td>Month-by-month project timeline view</td></tr>
<tr><td><strong>Budget</strong></td><td>Budget categories with planned vs. actual tracking</td></tr>
<tr><td><strong>Cash / Runway</strong></td><td>Cash position, burn rate, and runway forecast</td></tr>
<tr><td><strong>US Investment</strong></td><td>Investor pipeline and IR activity tracking</td></tr>
<tr><td><strong>Cap Table</strong></td><td>Shareholder registry, equity events, vesting</td></tr>
<tr><td><strong>Resources</strong></td><td>Team allocation and utilization monitoring</td></tr>
<tr><td><strong>Suppliers</strong></td><td>Supplier qualification and lead-time tracking</td></tr>
<tr><td><strong>Message Board</strong></td><td>Threaded discussions with decisions and actions</td></tr>
<tr><td><strong>FDA Comms</strong></td><td>Q-Sub generator, RTA checklist, regulatory timelines (PMP only)</td></tr>
</tbody></table>
<div class="help-warn">⚠️ Some tabs may be restricted based on your role or subscription tier.</div>`,
      cn: `<p>仪表板由带有角色/层级选择器的标题栏、带有16个功能标签页的水平导航栏和主内容区域组成。每个标签页专注于510(k)项目生命周期的特定方面。</p>
<h4>标题栏</h4>
<ul><li>项目名称和副标题（中英双语）</li><li>角色选择器：在PMP、技术、商务和财务视图之间切换</li><li>层级指示器：显示当前订阅层级（入门/成长/规模）</li><li>语言切换：在中英文界面之间切换</li></ul>
<h4>16个标签页</h4>
<table class="help-table"><thead><tr><th>标签页</th><th>说明</th></tr></thead><tbody>
<tr><td><strong>双轨制</strong></td><td>技术和法规里程碑跟踪</td></tr>
<tr><td><strong>门控系统</strong></td><td>带标准清单的阶段门控评审</td></tr>
<tr><td><strong>法规跟踪</strong></td><td>标准合规性和进度监控</td></tr>
<tr><td><strong>风险看板</strong></td><td>ISO 14971风险矩阵，含严重性/概率</td></tr>
<tr><td><strong>审计追踪</strong></td><td>所有仪表板更改的时间戳日志</td></tr>
<tr><td><strong>文档控制</strong></td><td>ISO 13485对齐的文档生命周期管理</td></tr>
<tr><td><strong>行动项</strong></td><td>任务板、DHF跟踪器、DMR跟踪器、CAPA日志</td></tr>
<tr><td><strong>时间线</strong></td><td>按月份的项目时间线视图</td></tr>
<tr><td><strong>预算</strong></td><td>按类别的计划与实际预算跟踪</td></tr>
<tr><td><strong>现金/跑道</strong></td><td>现金状况、燃烧率和跑道预测</td></tr>
<tr><td><strong>美国投资</strong></td><td>投资者管道和IR活动跟踪</td></tr>
<tr><td><strong>股权表</strong></td><td>股东登记、股权事件、归属计划</td></tr>
<tr><td><strong>资源</strong></td><td>团队分配和利用率监控</td></tr>
<tr><td><strong>供应商</strong></td><td>供应商资质审核和交期跟踪</td></tr>
<tr><td><strong>消息板</strong></td><td>带决策和行动跟踪的线程讨论</td></tr>
<tr><td><strong>FDA通讯</strong></td><td>Q-Sub生成器、RTA清单、法规时间线（仅PMP）</td></tr>
</tbody></table>
<div class="help-warn">⚠️ 部分标签页可能因您的角色或订阅层级而受限。</div>`,
    },
  },
  {
    num: 3,
    title: {
      en: "Role-Based Access & Tier System",
      cn: "基于角色的访问与层级系统",
    },
    content: {
      en: `<h4>User Roles</h4>
<p>The dashboard supports four primary roles, each with different access levels:</p>
<table class="help-table"><thead><tr><th>Role</th><th>Access</th></tr></thead><tbody>
<tr><td><strong>PMP (Project Manager)</strong></td><td>Full access to all tabs. Can edit milestones, gates, risks, budgets, documents, and team. Only role that can see FDA Communications.</td></tr>
<tr><td><strong>Technology</strong></td><td>Can view and update technical milestones, risks, and documents. Can participate in Message Board. Cannot access financial tabs.</td></tr>
<tr><td><strong>Business</strong></td><td>Access to business milestones, budget, investment, and cap table. Can participate in Message Board.</td></tr>
<tr><td><strong>Accounting</strong></td><td>Read-only access to Budget, Cash/Runway, and Cap Table. Limited editing capabilities.</td></tr>
</tbody></table>
<h4>Subscription Tiers</h4>
<p>Tab access is server-controlled via Supabase RLS. The tier determines which tabs are available:</p>
<table class="help-table"><thead><tr><th>Tier</th><th>Price</th><th>Seats</th><th>Tabs</th></tr></thead><tbody>
<tr><td><strong>Starter</strong></td><td>$500/mo</td><td>2</td><td>Dual-Track, Gates, Timeline, Budget</td></tr>
<tr><td><strong>Growth</strong></td><td>$1,000/mo</td><td>5</td><td>All except Cap Table, FDA Comms, US Investment</td></tr>
<tr><td><strong>Scale</strong></td><td>$2,000/mo</td><td>10</td><td>All 16 tabs including FDA Comms and Cap Table</td></tr>
</tbody></table>
<div class="help-tip">💡 Your tier is managed server-side and cannot be changed from the dashboard UI.</div>`,
      cn: `<h4>用户角色</h4>
<p>仪表板支持四种主要角色，每种角色具有不同的访问级别：</p>
<table class="help-table"><thead><tr><th>角色</th><th>访问权限</th></tr></thead><tbody>
<tr><td><strong>PMP（项目经理）</strong></td><td>对所有标签页的完全访问。可以编辑里程碑、门控、风险、预算、文档和团队。唯一能看到FDA通讯的角色。</td></tr>
<tr><td><strong>技术</strong></td><td>可以查看和更新技术里程碑、风险和文档。可以参与消息板。无法访问财务标签页。</td></tr>
<tr><td><strong>商务</strong></td><td>可以访问商务里程碑、预算、投资和股权表。可以参与消息板。</td></tr>
<tr><td><strong>财务</strong></td><td>对预算、现金/跑道和股权表的只读访问。有限的编辑能力。</td></tr>
</tbody></table>
<h4>订阅层级</h4>
<p>标签页访问通过Supabase RLS进行服务器端控制。层级决定可用的标签页：</p>
<table class="help-table"><thead><tr><th>层级</th><th>价格</th><th>席位</th><th>标签页</th></tr></thead><tbody>
<tr><td><strong>入门</strong></td><td>$500/月</td><td>2</td><td>双轨制、门控、时间线、预算</td></tr>
<tr><td><strong>成长</strong></td><td>$1,000/月</td><td>5</td><td>除股权表、FDA通讯、美国投资外全部</td></tr>
<tr><td><strong>规模</strong></td><td>$2,000/月</td><td>10</td><td>全部16个标签页，包括FDA通讯和股权表</td></tr>
</tbody></table>
<div class="help-tip">💡 您的层级由服务器端管理，无法从仪表板UI更改。</div>`,
    },
  },
  {
    num: 4,
    title: { en: "Dual-Track Milestones", cn: "双轨制里程碑" },
    content: {
      en: `<p>The Dual-Track tab displays parallel regulatory and technical milestone tracks. This mirrors the actual FDA 510(k) process where engineering development and regulatory preparation run concurrently.</p>
<h4>Technical Milestones</h4>
<p>Technical milestones track engineering deliverables: design freeze, prototype testing, verification and validation activities, and design transfer. Each milestone shows its month, status, owner, and category.</p>
<h4>Regulatory Milestones</h4>
<p>Regulatory milestones track FDA deliverables: Pre-Submission meeting, 510(k) preparation, and submission filing. These are auto-generated based on your project duration.</p>
<h4>Editing Milestones</h4>
<p>Click on a milestone status badge to cycle through: Not Started, In Progress, Complete, and Blocked. Only PMP and the owning role can change status. All changes are logged in the Audit Trail.</p>`,
      cn: `<p>双轨制标签页显示并行的法规和技术里程碑轨道。这反映了实际的FDA 510(k)流程，其中工程开发和法规准备同步进行。</p>
<h4>技术里程碑</h4>
<p>技术里程碑跟踪工程交付成果：设计冻结、原型测试、验证和确认活动以及设计转移。每个里程碑显示其月份、状态、负责人和类别。</p>
<h4>法规里程碑</h4>
<p>法规里程碑跟踪FDA交付成果：Pre-Submission会议、510(k)准备和提交申报。这些基于项目持续时间自动生成。</p>
<h4>编辑里程碑</h4>
<p>点击里程碑状态徽章可循环切换：未开始、进行中、完成和阻塞。只有PMP和对应角色可以更改状态。所有更改都记录在审计追踪中。</p>`,
    },
  },
  {
    num: 5,
    title: { en: "Gate System", cn: "门控系统" },
    content: {
      en: `<p>The Gate System implements a phase-gate review process. Gates are automatically generated based on project duration (2-6 gates). Each gate has criteria that must be met before the project can proceed.</p>
<h4>Gate Criteria</h4>
<p>Each gate has a checklist of criteria (e.g., 'Technical deliverables complete', 'Budget on track', 'Risk mitigations confirmed'). Check criteria individually by clicking them. The gate status updates based on criteria completion.</p>
<h4>Gate Decisions</h4>
<p>PMP can record gate decisions: Go, No-Go, or Conditional Go. Decisions are timestamped and attributed. Gate notes can capture discussion points and conditions for conditional approvals.</p>
<h4>Stakeholder Inputs</h4>
<p>Technical and Business stakeholders can submit gate inputs. These appear in the gate review panel, providing a complete picture for the gate decision.</p>`,
      cn: `<p>门控系统实施阶段门控评审流程。门控基于项目持续时间自动生成（2-6个门控）。每个门控都有在项目继续之前必须满足的标准。</p>
<h4>门控标准</h4>
<p>每个门控都有标准清单（例如"技术交付成果完成"、"预算正常"、"风险缓解已确认"）。通过点击逐项检查标准。门控状态根据标准完成情况更新。</p>
<h4>门控决定</h4>
<p>PMP可以记录门控决定：通过、不通过或有条件通过。决定带有时间戳和归属。门控备注可以记录讨论要点和有条件批准的条件。</p>
<h4>利益相关方输入</h4>
<p>技术和商务利益相关方可以提交门控输入。这些出现在门控评审面板中，为门控决定提供完整的信息。</p>`,
    },
  },
  {
    num: 6,
    title: { en: "Regulatory Tracker", cn: "法规跟踪" },
    content: {
      en: `<p>The Regulatory Tracker monitors compliance with applicable standards. Standards are pre-populated based on your device template (e.g., IEC 60601-1 for electrical devices, ISO 10993 for biocompatibility) or entered manually.</p>
<h4>Tracking Standards</h4>
<ul><li>Status: Not Started, In Progress, Complete</li><li>Progress bar: 0-100% completion percentage</li><li>Clause-level tracking for detailed compliance</li></ul>
<p>Click the status badge to cycle through states. Update the progress slider to reflect actual completion. The FDA Comms tab uses these values to auto-populate the RTA checklist.</p>`,
      cn: `<p>法规跟踪器监控适用标准的合规性。标准基于您的设备模板预填充（例如电气设备的IEC 60601-1、生物相容性的ISO 10993），也可手动输入。</p>
<h4>标准跟踪</h4>
<ul><li>状态：未开始、进行中、完成</li><li>进度条：0-100%完成百分比</li><li>条款级别跟踪，实现详细合规</li></ul>
<p>点击状态徽章可循环切换状态。更新进度滑块以反映实际完成情况。FDA通讯标签页使用这些值自动填充RTA清单。</p>`,
    },
  },
  {
    num: 7,
    title: { en: "Risk Dashboard", cn: "风险看板" },
    content: {
      en: `<p>The Risk Dashboard implements ISO 14971 risk management. Risks are displayed in a color-coded matrix showing severity, probability, and risk level. Template-specific risks are auto-populated from your device category.</p>
<h4>Risk Fields</h4>
<table class="help-table"><thead><tr><th>Field</th><th>Description</th></tr></thead><tbody>
<tr><td><strong>Severity</strong></td><td>How serious the harm would be (Low/Medium/High)</td></tr>
<tr><td><strong>Probability</strong></td><td>How likely the hazardous situation occurs (Low/Medium/High)</td></tr>
<tr><td><strong>Risk Level</strong></td><td>Color-coded: Green (acceptable), Yellow (ALARP), Red (unacceptable)</td></tr>
<tr><td><strong>Controls</strong></td><td>Risk control measures implemented</td></tr>
<tr><td><strong>Residual Risk</strong></td><td>Remaining risk after controls</td></tr>
<tr><td><strong>Mitigation Status</strong></td><td>Not Started, In Progress, Complete</td></tr>
</tbody></table>
<div class="help-tip">💡 Red risks trigger alerts in the FDA Comms panel and should be addressed before 510(k) submission.</div>`,
      cn: `<p>风险看板实施ISO 14971风险管理。风险以颜色编码的矩阵显示，展示严重性、概率和风险级别。基于设备类别的特定风险自动填充。</p>
<h4>风险字段</h4>
<table class="help-table"><thead><tr><th>字段</th><th>说明</th></tr></thead><tbody>
<tr><td><strong>严重性</strong></td><td>危害的严重程度（低/中/高）</td></tr>
<tr><td><strong>概率</strong></td><td>危险情况发生的可能性（低/中/高）</td></tr>
<tr><td><strong>风险级别</strong></td><td>颜色编码：绿色（可接受）、黄色（ALARP）、红色（不可接受）</td></tr>
<tr><td><strong>控制措施</strong></td><td>已实施的风险控制措施</td></tr>
<tr><td><strong>残余风险</strong></td><td>控制后的剩余风险</td></tr>
<tr><td><strong>缓解状态</strong></td><td>未开始、进行中、完成</td></tr>
</tbody></table>
<div class="help-tip">💡 红色风险会在FDA通讯面板中触发警报，应在510(k)提交前解决。</div>`,
    },
  },
  {
    num: 8,
    title: { en: "Audit Trail", cn: "审计追踪" },
    content: {
      en: `<p>Every change made in the dashboard is recorded in the Audit Trail with a timestamp, user role, action type, field changed, old value, new value, and detail description. This supports 21 CFR Part 11 traceability requirements.</p>
<h4>Supabase Sync</h4>
<p>Audit entries are automatically synced to the Supabase backend. If you are offline, entries queue locally and flush when connectivity is restored.</p>
<h4>Filtering</h4>
<p>The audit trail supports filtering by action type and searching by keyword. Recent entries appear first. Export functionality allows downloading the complete audit history.</p>`,
      cn: `<p>仪表板中的每次更改都会记录在审计追踪中，包含时间戳、用户角色、操作类型、更改的字段、旧值、新值和详细描述。这支持21 CFR Part 11的可追溯性要求。</p>
<h4>Supabase同步</h4>
<p>审计条目自动同步到Supabase后端。如果您离线，条目会在本地排队，并在连接恢复时刷新。</p>
<h4>筛选</h4>
<p>审计追踪支持按操作类型筛选和按关键字搜索。最近的条目优先显示。导出功能允许下载完整的审计历史记录。</p>`,
    },
  },
  {
    num: 9,
    title: { en: "Document Control", cn: "文档控制" },
    content: {
      en: `<p>Document Control provides ISO 13485-aligned document lifecycle management. Documents are tracked locally in the browser to protect intellectual property, with server sync available for approved/effective documents.</p>
<h4>Document Lifecycle</h4>
<ul><li><strong>Draft</strong> — Initial document creation</li><li><strong>In Review</strong> — Under stakeholder review</li><li><strong>Approved</strong> — Formally approved by designated authority</li><li><strong>Effective</strong> — Active and controlling (effective date set automatically)</li><li><strong>Obsolete</strong> — Superseded or withdrawn</li></ul>
<p>Click the status badge to cycle through the lifecycle. Only PMP can change document status.</p>
<h4>Document Fields</h4>
<table class="help-table"><thead><tr><th>Field</th><th>Description</th></tr></thead><tbody>
<tr><td><strong>DCN</strong></td><td>Document Control Number (auto-generated, e.g., DCN-REG-001)</td></tr>
<tr><td><strong>Category</strong></td><td>Regulatory, Technical, Business, Legal, Finance, Templates</td></tr>
<tr><td><strong>Version</strong></td><td>Version number with revision history</td></tr>
<tr><td><strong>Owner</strong></td><td>Responsible person or role</td></tr>
<tr><td><strong>Source Ref</strong></td><td>External reference (GitHub commit, SVN revision, etc.)</td></tr>
<tr><td><strong>Linked</strong></td><td>Linked milestone or gate (e.g., R8, T2)</td></tr>
</tbody></table>
<h4>Sync to Server</h4>
<p>When documents reach 'Approved' or 'Effective' status, use the 'Sync to Server' button to upload them to the Supabase dhf_documents table. The FDA Communications tab shows an alert when approved documents have not been synced.</p>
<div class="help-warn">⚠️ Documents are stored in browser localStorage. Clear browser data = lose documents. Sync critical documents to the server.</div>`,
      cn: `<p>文档控制提供符合ISO 13485的文档生命周期管理。文档在浏览器中本地跟踪以保护知识产权，已批准/生效的文档可通过服务器同步。</p>
<h4>文档生命周期</h4>
<ul><li><strong>草稿</strong> — 初始文档创建</li><li><strong>审核中</strong> — 利益相关方审核中</li><li><strong>已批准</strong> — 由指定权威正式批准</li><li><strong>生效</strong> — 活跃且具有控制力（自动设置生效日期）</li><li><strong>废止</strong> — 被取代或撤回</li></ul>
<p>点击状态徽章可循环切换生命周期。只有PMP可以更改文档状态。</p>
<h4>文档字段</h4>
<table class="help-table"><thead><tr><th>字段</th><th>说明</th></tr></thead><tbody>
<tr><td><strong>DCN</strong></td><td>文档控制编号（自动生成，如DCN-REG-001）</td></tr>
<tr><td><strong>类别</strong></td><td>法规、技术、商务、法律、财务、模板</td></tr>
<tr><td><strong>版本</strong></td><td>版本号及修订历史</td></tr>
<tr><td><strong>负责人</strong></td><td>责任人或角色</td></tr>
<tr><td><strong>来源参考</strong></td><td>外部参考（GitHub提交、SVN修订等）</td></tr>
<tr><td><strong>关联</strong></td><td>关联的里程碑或门控（如R8、T2）</td></tr>
</tbody></table>
<h4>同步到服务器</h4>
<p>当文档达到"已批准"或"生效"状态时，使用"同步到服务器"按钮将其上传到Supabase dhf_documents表。FDA通讯标签页会在已批准的文档未同步时显示警报。</p>
<div class="help-warn">⚠️ 文档存储在浏览器localStorage中。清除浏览器数据=丢失文档。请将关键文档同步到服务器。</div>`,
    },
  },
  {
    num: 10,
    title: { en: "Actions", cn: "行动项" },
    content: {
      en: `<p>The Actions tab tracks action items arising from gate reviews, risk mitigation, and general project management.</p>
<h4>Action Fields</h4>
<table class="help-table"><thead><tr><th>Field</th><th>Description</th></tr></thead><tbody>
<tr><td><strong>Assignee</strong></td><td>Team member responsible</td></tr>
<tr><td><strong>Priority</strong></td><td>High, Medium, Low</td></tr>
<tr><td><strong>Status</strong></td><td>Todo, In Progress, Done, Blocked</td></tr>
<tr><td><strong>Due Date</strong></td><td>Target completion date</td></tr>
<tr><td><strong>Linked Gate</strong></td><td>Associated gate review (e.g., G1, G2)</td></tr>
</tbody></table>
<h4>DHF Document Tracker</h4>
<p>The Design History File (DHF) Document Tracker appears within the Actions tab. It tracks all design-phase documents required by 21 CFR 820.30. Click a document's status badge to cycle through: Not Started, Draft, In Review, Approved.</p>
<h4>DMR Document Tracker</h4>
<p>The Device Master Record (DMR) Document Tracker is also within the Actions tab. It tracks 12 documents required by 21 CFR 820.181 covering device specifications, production processes, quality procedures, and packaging/labeling.</p>
<h4>CAPA Log</h4>
<p>The Corrective and Preventive Action (CAPA) Log tracks CAPA items with type (Corrective or Preventive), status, owner, and linked gate.</p>`,
      cn: `<p>行动项标签页跟踪来自门控评审、风险缓解和一般项目管理的行动项。</p>
<h4>行动项字段</h4>
<table class="help-table"><thead><tr><th>字段</th><th>说明</th></tr></thead><tbody>
<tr><td><strong>负责人</strong></td><td>负责的团队成员</td></tr>
<tr><td><strong>优先级</strong></td><td>高、中、低</td></tr>
<tr><td><strong>状态</strong></td><td>待办、进行中、完成、阻塞</td></tr>
<tr><td><strong>截止日期</strong></td><td>目标完成日期</td></tr>
<tr><td><strong>关联门控</strong></td><td>关联的门控评审（如G1、G2）</td></tr>
</tbody></table>
<h4>DHF文档跟踪器</h4>
<p>设计历史文件(DHF)文档跟踪器位于行动项标签页内。它跟踪21 CFR 820.30要求的所有设计阶段文档。点击文档的状态徽章可循环切换：未开始、草稿、审核中、已批准。</p>
<h4>DMR文档跟踪器</h4>
<p>设备主记录(DMR)文档跟踪器也在行动项标签页内。它跟踪21 CFR 820.181要求的12份文档，涵盖设备规格、生产过程、质量程序和包装/标签。</p>
<h4>CAPA日志</h4>
<p>纠正和预防措施(CAPA)日志跟踪CAPA项目，包含类型（纠正或预防）、状态、负责人和关联门控。</p>`,
    },
  },
  {
    num: 11,
    title: { en: "Timeline", cn: "时间线" },
    content: {
      en: `<p>The Timeline provides a month-by-month view of project events. Each entry shows technical and business activities with an impact indicator (positive/neutral/negative). Timeline events are auto-generated during wizard setup and can be edited.</p>`,
      cn: `<p>时间线提供按月份的项目事件视图。每个条目显示技术和业务活动，并带有影响指标（正面/中性/负面）。时间线事件在向导设置期间自动生成，可以编辑。</p>`,
    },
  },
  {
    num: 12,
    title: { en: "Budget", cn: "预算" },
    content: {
      en: `<p>The Budget tab tracks spending against planned budgets by category. Categories are defined during wizard setup (or from template budget lines). Each category shows planned amount, actual spend, and variance.</p>
<h4>Budget Management</h4>
<ul><li>Add, edit, or delete budget categories</li><li>Update actual spend values to track variance</li><li>Currency display toggles between USD and CNY</li><li>All changes logged in Audit Trail</li></ul>`,
      cn: `<p>预算标签页按类别跟踪支出与计划预算的对比。类别在向导设置期间定义（或来自模板预算行）。每个类别显示计划金额、实际支出和差异。</p>
<h4>预算管理</h4>
<ul><li>添加、编辑或删除预算类别</li><li>更新实际支出值以跟踪差异</li><li>货币显示在USD和CNY之间切换</li><li>所有更改记录在审计追踪中</li></ul>`,
    },
  },
  {
    num: 13,
    title: { en: "Cash / Runway", cn: "现金/跑道" },
    content: {
      en: `<p>Cash/Runway provides financial health visibility: current cash position, monthly burn rate, and projected runway in months. It includes funding round tracking and burn history charts.</p>
<h4>Key Metrics</h4>
<table class="help-table"><thead><tr><th>Metric</th><th>Description</th></tr></thead><tbody>
<tr><td><strong>Cash on Hand</strong></td><td>Current available cash balance</td></tr>
<tr><td><strong>Monthly Burn</strong></td><td>Average monthly expenditure rate</td></tr>
<tr><td><strong>Runway</strong></td><td>Months of operation at current burn rate</td></tr>
</tbody></table>
<h4>Funding Rounds</h4>
<p>Track funding rounds with status (Planned, In Progress, Received). Each round records amount, date, and funding source.</p>`,
      cn: `<p>现金/跑道提供财务健康可见性：当前现金状况、月度燃烧率和预计跑道月数。包括融资轮次跟踪和燃烧历史图表。</p>
<h4>关键指标</h4>
<table class="help-table"><thead><tr><th>指标</th><th>说明</th></tr></thead><tbody>
<tr><td><strong>手头现金</strong></td><td>当前可用现金余额</td></tr>
<tr><td><strong>月度燃烧</strong></td><td>平均月度支出率</td></tr>
<tr><td><strong>跑道</strong></td><td>以当前燃烧率可运营的月数</td></tr>
</tbody></table>
<h4>融资轮次</h4>
<p>跟踪融资轮次状态（计划中、进行中、已到账）。每轮记录金额、日期和资金来源。</p>`,
    },
  },
  {
    num: 14,
    title: { en: "US Investment", cn: "美国投资" },
    content: {
      en: `<p>The US Investment tab manages investor relations for medical device ventures seeking US market entry.</p>
<h4>Target Investors</h4>
<table class="help-table"><thead><tr><th>Field</th><th>Options</th></tr></thead><tbody>
<tr><td><strong>Type</strong></td><td>VC, Angel Group, Strategic, PE, Government</td></tr>
<tr><td><strong>Stage</strong></td><td>Seed, Series A, Series B, Growth</td></tr>
<tr><td><strong>Contact Status</strong></td><td>Prospect, Contacted, In Discussions, Term Sheet, Committed</td></tr>
</tbody></table>
<h4>IR Activities</h4>
<p>Log investor relations activities: meetings, presentations, due diligence sessions, term sheet negotiations. Each activity has a date, type, and status.</p>`,
      cn: `<p>美国投资标签页管理寻求进入美国市场的医疗器械企业的投资者关系。</p>
<h4>目标投资者</h4>
<table class="help-table"><thead><tr><th>字段</th><th>选项</th></tr></thead><tbody>
<tr><td><strong>类型</strong></td><td>VC、天使集团、战略、PE、政府</td></tr>
<tr><td><strong>阶段</strong></td><td>种子、A轮、B轮、成长</td></tr>
<tr><td><strong>联系状态</strong></td><td>潜在、已联系、讨论中、条款清单、已承诺</td></tr>
</tbody></table>
<h4>IR活动</h4>
<p>记录投资者关系活动：会议、演示、尽职调查、条款谈判。每项活动都有日期、类型和状态。</p>`,
    },
  },
  {
    num: 15,
    title: { en: "Cap Table", cn: "股权表" },
    content: {
      en: `<p>The Cap Table tracks equity ownership, equity events, and vesting schedules.</p>
<h4>Shareholders</h4>
<ul><li>Name, share class (Common, Preferred A/B/C, Options, Warrants)</li><li>Share count and ownership percentage</li><li>Board seat, vesting status, and notes</li></ul>
<h4>Equity Events</h4>
<ul><li>Track funding rounds, stock splits, option grants, conversions</li><li>Each event records shares issued, price per share, and total raised</li></ul>
<h4>Vesting Schedules</h4>
<ul><li>Standard 4-year vest with 1-year cliff, or custom schedules</li><li>Track cliff date, total shares, vested shares, and next vest date</li></ul>`,
      cn: `<p>股权表跟踪股权所有权、股权事件和归属计划。</p>
<h4>股东</h4>
<ul><li>姓名、股份类别（普通、优先A/B/C、期权、认股权证）</li><li>股份数量和所有权百分比</li><li>董事会席位、归属状态和备注</li></ul>
<h4>股权事件</h4>
<ul><li>跟踪融资轮次、股票分割、期权授予、转换</li><li>每个事件记录发行的股份、每股价格和总融资额</li></ul>
<h4>归属计划</h4>
<ul><li>标准4年归属，1年悬崖期，或自定义计划</li><li>跟踪悬崖日期、总股份、已归属股份和下次归属日期</li></ul>`,
    },
  },
  {
    num: 16,
    title: { en: "Resources", cn: "资源" },
    content: {
      en: `<p>The Resources tab displays team members with their role, allocation across workstreams, and utilization percentage.</p>
<h4>Managing Team Members</h4>
<ul><li>Add team members with name, role, email, and workstream allocation</li><li>Click allocation percentages to edit them inline (PMP/Tech/Business roles)</li><li>Utilization gauge: Green (&lt;85%), Yellow (85-100%), Red (&gt;100% over-allocated)</li><li>Delete team members via the X button on each card</li></ul>
<h4>Workstream Allocation</h4>
<p>Each team member can be allocated across multiple workstreams. Percentages are editable inline. The utilization gauge updates automatically. Changes are audit-logged.</p>
<div class="help-tip">💡 Keep total allocation at or below 100% to avoid burnout. The dashboard flags over-allocation in red.</div>`,
      cn: `<p>资源标签页显示团队成员及其角色、跨工作流的分配和利用率百分比。</p>
<h4>管理团队成员</h4>
<ul><li>添加团队成员，包含姓名、角色、邮箱和工作流分配</li><li>点击分配百分比可内联编辑（PMP/技术/商务角色）</li><li>利用率指示：绿色（&lt;85%）、黄色（85-100%）、红色（&gt;100%过度分配）</li><li>通过每张卡片上的X按钮删除团队成员</li></ul>
<h4>工作流分配</h4>
<p>每个团队成员可以分配到多个工作流。百分比可内联编辑。利用率指示自动更新。更改被审计记录。</p>
<div class="help-tip">💡 将总分配保持在100%或以下以避免过劳。仪表板用红色标记过度分配。</div>`,
    },
  },
  {
    num: 17,
    title: { en: "Suppliers", cn: "供应商" },
    content: {
      en: `<p>The Suppliers tab tracks supplier qualification status, lead times, purchase order status, and contract manufacturing milestones. This supports 21 CFR 820 supplier controls.</p>
<h4>Supplier Status</h4>
<ul><li><strong>Under Review</strong> — Initial evaluation</li><li><strong>Qualified</strong> — Approved for use</li><li><strong>Active</strong> — Currently supplying</li><li><strong>On Hold</strong> — Temporarily suspended</li><li><strong>Rejected</strong> — Failed qualification</li></ul>`,
      cn: `<p>供应商标签页跟踪供应商资质审核状态、交期、采购订单状态和代工里程碑。这支持21 CFR 820供应商控制要求。</p>
<h4>供应商状态</h4>
<ul><li><strong>审核中</strong> — 初始评估</li><li><strong>已资质</strong> — 批准使用</li><li><strong>活跃</strong> — 当前供货中</li><li><strong>暂停</strong> — 临时暂停</li><li><strong>拒绝</strong> — 资质审核未通过</li></ul>`,
    },
  },
  {
    num: 18,
    title: { en: "Message Board", cn: "消息板" },
    content: {
      en: `<p>The Message Board is a purpose-driven messaging system for cross-functional communication. It supports threaded discussions with lifecycle management, decisions tracking, and action item creation.</p>
<h4>Threads</h4>
<p>Create threads with a title, workstream assignment, priority level, and intent (Discuss, Decide, Inform, Escalate). Threads flow through an Open &rarr; Resolved lifecycle.</p>
<h4>Posting Messages</h4>
<p>Select your posting role from the role picker toolbar. Type your message and press Send. Use [DECISION] or [ACTION] prefixes to tag messages with special intent.</p>
<h4>Settings</h4>
<p>Click the Settings gear icon to configure email addresses for each role. Toggle Test Mode for development. Click Settings again to close the panel.</p>
<h4>Views &amp; Filters</h4>
<ul><li>All Threads: Complete thread list</li><li>My Items: Threads where you are owner or assignee</li><li>Decisions: Threads with active decisions</li><li>Executive: High-priority and decision threads</li><li>Workstream filter: Filter by workstream category</li><li>Lifecycle filter: Open, Resolved, or All</li></ul>`,
      cn: `<p>消息板是跨职能沟通的专用消息系统。它支持带生命周期管理、决策跟踪和行动项创建的线程讨论。</p>
<h4>线程</h4>
<p>创建线程时设置标题、工作流分配、优先级和意图（讨论、决定、通知、升级）。线程经历 打开 → 已解决 的生命周期。</p>
<h4>发送消息</h4>
<p>从角色选择工具栏中选择您的发布角色。输入消息并按发送。使用[DECISION]或[ACTION]前缀标记具有特殊意图的消息。</p>
<h4>设置</h4>
<p>点击设置齿轮图标配置每个角色的电子邮件地址。切换测试模式用于开发。再次点击设置关闭面板。</p>
<h4>视图与筛选</h4>
<ul><li>所有线程：完整线程列表</li><li>我的项目：您是所有者或负责人的线程</li><li>决策：有活跃决策的线程</li><li>高管：高优先级和决策线程</li><li>工作流筛选：按工作流类别筛选</li><li>生命周期筛选：打开、已解决或全部</li></ul>`,
    },
  },
  {
    num: 19,
    title: { en: "FDA Communications Center", cn: "FDA通讯中心" },
    content: {
      en: `<p>The FDA Comms tab is PMP-only and provides tools for FDA regulatory interactions.</p>
<h4>Q-Sub Cover Letter Generator</h4>
<p>Select from 5 Q-Sub types (Pre-Sub Meeting, Pre-Sub Written, SIR, Informational Meeting, Study Risk Determination) to auto-generate a cover letter with your company letterhead. Export as HTML for final formatting.</p>
<h4>Q-Submission Types Reference</h4>
<p>Overview of all 5 FDA CDRH Q-Sub types with purpose, timeline, and "When to Use" guidance. Includes a "How to Choose the Right Q-Sub Type" decision guide.</p>
<h4>Refuse-to-Accept (RTA) Checklist</h4>
<p>Self-check against FDA's 17-item RTA checklist. Items auto-populate from your DHF documents and standards compliance data. The progress bar shows overall readiness percentage.</p>
<h4>Document Sync Alert</h4>
<p>An amber alert banner appears when approved or effective documents in Document Control have not been synced to the server. Click "Go to Document Control" to navigate and sync.</p>
<h4>MDUFA Review Timeline</h4>
<p>Tracks 510(k) MDUFA review milestones: submission received, K-number assignment (Day 7), RTA screening (Day 15), substantive review (Day 60), and MDUFA decision goal (Day 90).</p>
<h4>SE Decision Flowchart</h4>
<p>Visual decision flow for FDA's Substantial Equivalence determination: predicate identification, intended use comparison, technological characteristics analysis, and safety/effectiveness evaluation.</p>`,
      cn: `<p>FDA通讯标签页仅限PMP使用，提供FDA法规互动工具。</p>
<h4>Q-Sub附信生成器</h4>
<p>从5种Q-Sub类型中选择（Pre-Sub会议、Pre-Sub书面、SIR、信息会议、研究风险判定），自动生成带公司抬头的附信。导出为HTML进行最终格式化。</p>
<h4>Q-Sub类型参考</h4>
<p>全部5种FDA CDRH Q-Sub类型概览，包含用途、时间线和"何时使用"指南。包括"如何选择正确的Q-Sub类型"决策指南。</p>
<h4>RTA自检清单</h4>
<p>对照FDA的17项RTA清单进行自检。项目从您的DHF文档和标准合规数据中自动填充。进度条显示整体就绪百分比。</p>
<h4>文档同步警报</h4>
<p>当文档控制中已批准或生效的文档未同步到服务器时，会出现琥珀色警报横幅。点击"前往文档控制"导航并同步。</p>
<h4>MDUFA审查时间线</h4>
<p>跟踪510(k) MDUFA审查里程碑：提交收到、K编号分配（第7天）、RTA筛选（第15天）、实质性审查（第60天）和MDUFA决定目标（第90天）。</p>
<h4>SE决策流程</h4>
<p>FDA实质等效判定的可视化决策流程：前置器械识别、预期用途比较、技术特征分析和安全性/有效性评估。</p>`,
    },
  },
  {
    num: 20,
    title: { en: "Setup Wizard & Templates", cn: "设置向导与模板" },
    content: {
      en: `<p>The Setup Wizard launches on first visit (or when no project data exists). It guides you through a 3-phase setup process.</p>
<h4>Phase 1: Language Selection</h4>
<p>Choose English or Chinese for the wizard and dashboard interface.</p>
<h4>Phase 2: Device Template</h4>
<p>Select from 7 pre-configured device templates or start from scratch:</p>
<ul><li>Respiratory Devices (ventilators, CPAP, nebulizers)</li><li>Cardiovascular (stents, pacemakers, monitors)</li><li>Orthopedic (implants, instruments, fixation)</li><li>IVD (in-vitro diagnostics, assays, analyzers)</li><li>Imaging (X-ray, ultrasound, MRI accessories)</li><li>Rehabilitation (therapy devices, mobility aids)</li><li>SaMD (Software as a Medical Device)</li></ul>
<p>Templates pre-populate: submission type, device class, product codes, regulation section, predicate examples, tech areas, budget categories, standards, and template-specific risks.</p>
<h4>Phase 3: Project Details (8 Steps)</h4>
<ul><li>Step 1: Project name and subtitle</li><li>Step 2: Regulatory details (submission type, device class, predicate devices)</li><li>Step 3: Applicant and manufacturer information</li><li>Step 4: Team members with roles and workstream allocation</li><li>Step 5: Budget categories and amounts</li><li>Step 6: Cash on hand and project duration</li><li>Step 7: Suppliers and components</li><li>Step 8: DHF document selection</li></ul>`,
      cn: `<p>设置向导在首次访问时启动（或当不存在项目数据时）。它引导您完成3阶段设置过程。</p>
<h4>阶段1：语言选择</h4>
<p>为向导和仪表板界面选择英文或中文。</p>
<h4>阶段2：设备模板</h4>
<p>从7个预配置的设备模板中选择或从头开始：</p>
<ul><li>呼吸设备（呼吸机、CPAP、雾化器）</li><li>心血管（支架、起搏器、监护仪）</li><li>骨科（植入物、器械、固定）</li><li>IVD（体外诊断、检测、分析仪）</li><li>影像（X射线、超声、MRI附件）</li><li>康复（治疗设备、助行器）</li><li>SaMD（软件即医疗器械）</li></ul>
<p>模板预填充：提交类型、设备分类、产品代码、法规段落、前置器械示例、技术领域、预算类别、标准和特定模板风险。</p>
<h4>阶段3：项目详情（8个步骤）</h4>
<ul><li>步骤1：项目名称和副标题</li><li>步骤2：法规详情（提交类型、设备分类、前置器械）</li><li>步骤3：申请人和制造商信息</li><li>步骤4：团队成员及角色和工作流分配</li><li>步骤5：预算类别和金额</li><li>步骤6：手头现金和项目持续时间</li><li>步骤7：供应商和组件</li><li>步骤8：DHF文档选择</li></ul>`,
    },
  },
  {
    num: 21,
    title: { en: "Keyboard Shortcuts & Tips", cn: "快捷操作与技巧" },
    content: {
      en: `<h4>General Tips</h4>
<ul><li>All data saves automatically to browser localStorage -- including full dashboard state</li><li>Dashboard state survives browser crashes and power outages</li><li>Supabase sync happens in real-time when online</li><li>Offline changes queue and sync when connection is restored</li><li>Currency display toggles between USD and CNY based on language setting</li><li>The floating action button (bottom-right) provides quick actions</li></ul>
<h4>URL Parameters</h4>
<table class="help-table"><thead><tr><th>Parameter</th><th>Effect</th></tr></thead><tbody>
<tr><td><code>?test=respiratory</code></td><td>Load test data for the respiratory template</td></tr>
<tr><td><code>?test=cardiovascular</code></td><td>Load test data for the cardiovascular template</td></tr>
<tr><td><code>?test=&lt;templateId&gt;</code></td><td>Load pre-built test data for any of the 7 templates</td></tr>
</tbody></table>
<h4>Data Persistence</h4>
<ul><li><code>ctower_project_data</code> — Project configuration</li><li><code>ctower_live_state</code> — Full dashboard state (milestones, gates, risks, budget, etc.)</li><li><code>ctower_mb_threads</code> — Message Board threads</li><li><code>ctower_doclib_docs</code> — Documents</li><li>Supabase <code>messages</code> table — Synced messages</li><li>Supabase <code>audit_log</code> table — Synced audit entries</li></ul>
<div class="help-tip">💡 All dashboard state is automatically saved to localStorage after every change. If power is lost or the browser crashes, your data is preserved.</div>`,
      cn: `<h4>常用技巧</h4>
<ul><li>所有数据自动保存到浏览器localStorage——包括完整的仪表板状态</li><li>仪表板状态在浏览器崩溃和断电后仍保留</li><li>在线时Supabase同步实时进行</li><li>离线更改排队并在连接恢复时同步</li><li>货币显示根据语言设置在USD和CNY之间切换</li><li>浮动操作按钮（右下角）提供快捷操作</li></ul>
<h4>URL参数</h4>
<table class="help-table"><thead><tr><th>参数</th><th>效果</th></tr></thead><tbody>
<tr><td><code>?test=respiratory</code></td><td>加载呼吸模板的测试数据</td></tr>
<tr><td><code>?test=cardiovascular</code></td><td>加载心血管模板的测试数据</td></tr>
<tr><td><code>?test=&lt;templateId&gt;</code></td><td>加载7个模板中任意一个的预建测试数据</td></tr>
</tbody></table>
<h4>数据持久化</h4>
<ul><li><code>ctower_project_data</code> — 项目配置</li><li><code>ctower_live_state</code> — 完整仪表板状态（里程碑、门控、风险、预算等）</li><li><code>ctower_mb_threads</code> — 消息板线程</li><li><code>ctower_doclib_docs</code> — 文档</li><li>Supabase <code>messages</code>表 — 同步的消息</li><li>Supabase <code>audit_log</code>表 — 同步的审计条目</li></ul>
<div class="help-tip">💡 所有仪表板状态在每次更改后自动保存到localStorage。如果断电或浏览器崩溃，您的数据会被保留。</div>`,
    },
  },
  {
    num: 22,
    title: { en: "Troubleshooting", cn: "故障排除" },
    content: {
      en: `<h4>Dashboard won't load</h4>
<ul><li>Check internet connection for initial Supabase authentication</li><li>Clear browser cache and reload</li><li>Verify the deployment URL is correct</li></ul>
<h4>Tabs are grayed out</h4>
<p>Tab access is controlled by your subscription tier. Grayed-out tabs with strikethrough text indicate they are not included in your tier. Contact your administrator to upgrade.</p>
<h4>Messages not syncing</h4>
<ul><li>Verify internet connectivity (green indicator)</li><li>Check browser console for Supabase errors</li><li>Messages sync automatically when connection is restored</li></ul>
<h4>Settings panel not visible</h4>
<p>On the Message Board, click the Settings gear icon. The panel appears above the thread list and scrolls into view. Click Settings again to close.</p>
<h4>Stale demo data</h4>
<p>If you see data from a previous project, the wizard's 'Load Demo Data' will clear all existing data and generate fresh sample data.</p>
<h4>Resetting the Dashboard</h4>
<p>To completely reset, clear the following localStorage keys: ctower_project_data, ctower_live_state, ctower_mb_threads, ctower_mb_decisions, ctower_doclib_docs, ctower_qa_messages, ctower_qa_settings, ctower_qa_archive. Or clear all site data in browser settings.</p>`,
      cn: `<h4>仪表板无法加载</h4>
<ul><li>检查初始Supabase身份验证的互联网连接</li><li>清除浏览器缓存并重新加载</li><li>验证部署URL是否正确</li></ul>
<h4>标签页变灰</h4>
<p>标签页访问由您的订阅层级控制。灰色带删除线文本的标签页表示不包含在您的层级中。联系管理员升级。</p>
<h4>消息未同步</h4>
<ul><li>验证互联网连接（绿色指示器）</li><li>检查浏览器控制台的Supabase错误</li><li>消息在连接恢复时自动同步</li></ul>
<h4>设置面板不可见</h4>
<p>在消息板上，点击设置齿轮图标。面板出现在线程列表上方并滚动到视图中。再次点击设置关闭。</p>
<h4>过时的演示数据</h4>
<p>如果您看到以前项目的数据，向导的"加载演示数据"将清除所有现有数据并生成新的示例数据。</p>
<h4>重置仪表板</h4>
<p>要完全重置，清除以下localStorage键：ctower_project_data、ctower_live_state、ctower_mb_threads、ctower_mb_decisions、ctower_doclib_docs、ctower_qa_messages、ctower_qa_settings、ctower_qa_archive。或在浏览器设置中清除所有站点数据。</p>`,
    },
  },
  {
    num: 23,
    title: { en: "510(k) Predicate Finder", cn: "510(k) Predicate Finder" },
    content: {
      en: `<p>The 510(k) Predicate Finder is a companion SaaS tool that connects to the FDA openFDA database. It helps PMPs and regulatory teams identify predicate devices, trace predicate chains, and draft Substantial Equivalence arguments.</p>
<h4>Free vs Pro</h4>
<p>The Predicate Finder is available free with daily limits (5 searches, 1 chain trace, 2-device comparison). Pro ($99/month) unlocks unlimited searches, unlimited chain tracing, 4-device comparison, SE argument generation, and PDF export.</p>
<h4>Integration with Control Tower (Scale Tier)</h4>
<p>On the Scale tier ($2,000/mo), the Predicate Finder is embedded directly in the Control Tower dashboard. Predicate research informs:</p>
<ul><li>Regulatory Tracker -- predicate device references and SE strategy</li><li>Risk Dashboard -- risks identified during predicate comparison</li><li>FDA Communications Center -- Pre-Sub discussion points based on predicate analysis</li><li>Document Control -- predicate comparison reports as DHF artifacts</li></ul>
<h4>PMP Workflow</h4>
<ol><li>Use Predicate Finder to search for candidate predicate devices by product code or keyword</li><li>Trace the predicate chain to understand the regulatory lineage</li><li>Compare up to 4 devices side-by-side (Pro) to select the strongest predicate</li><li>Generate a draft SE argument (Pro) as a starting point for the regulatory team</li><li>Export results to PDF and attach to the 510(k) submission package in Document Control</li></ol>`,
      cn: `<p>510(k) Predicate Finder是连接FDA openFDA数据库的配套SaaS工具。它帮助PMP和法规团队识别前置器械、追踪前置器械链并起草实质等效论证。</p>
<h4>免费版 vs Pro版</h4>
<p>Predicate Finder免费提供每日限制（5次搜索、1次链追踪、2设备比较）。Pro版（$99/月）解锁无限搜索、无限链追踪、4设备比较、SE论证生成和PDF导出。</p>
<h4>与Control Tower的集成（Scale层级）</h4>
<p>在Scale层级（$2,000/月），Predicate Finder直接嵌入Control Tower仪表板。前置器械研究为以下提供信息：</p>
<ul><li>法规跟踪器——前置器械参考和SE策略</li><li>风险看板——前置器械比较中识别的风险</li><li>FDA通讯中心——基于前置器械分析的Pre-Sub讨论要点</li><li>文档控制——前置器械比较报告作为DHF产出</li></ul>
<h4>PMP工作流程</h4>
<ol><li>使用Predicate Finder通过产品代码或关键字搜索候选前置器械</li><li>追踪前置器械链以了解法规谱系</li><li>并排比较最多4个设备（Pro）以选择最强的前置器械</li><li>生成SE论证草稿（Pro）作为法规团队的起点</li><li>将结果导出为PDF并附加到文档控制中的510(k)提交包</li></ol>`,
    },
  },
  {
    num: 24,
    title: { en: "Glossary of FDA & Regulatory Terms", cn: "FDA与法规术语表" },
    content: {
      en: `<table class="help-table help-glossary"><thead><tr><th>Term</th><th>Definition</th></tr></thead><tbody>
<tr><td><strong>510(k)</strong></td><td>Premarket Notification submitted to FDA to demonstrate a Class II device is substantially equivalent to a legally marketed predicate device.</td></tr>
<tr><td><strong>PMA</strong></td><td>Premarket Approval. The most stringent FDA pathway, required for Class III devices.</td></tr>
<tr><td><strong>De Novo</strong></td><td>FDA classification pathway for novel low-to-moderate risk devices with no predicate.</td></tr>
<tr><td><strong>SE</strong></td><td>Substantial Equivalence. The legal standard for 510(k) clearance.</td></tr>
<tr><td><strong>Predicate Device</strong></td><td>A legally marketed device used as the comparison basis for a new 510(k) submission.</td></tr>
<tr><td><strong>RTA</strong></td><td>Refuse to Accept. FDA's initial administrative screening of a 510(k) submission.</td></tr>
<tr><td><strong>Pre-Sub (Q-Sub)</strong></td><td>Formal FDA meeting request to discuss regulatory strategy before filing.</td></tr>
<tr><td><strong>DICE</strong></td><td>Division of Industry and Consumer Education. Handles Pre-Sub logistics.</td></tr>
<tr><td><strong>MDUFA</strong></td><td>Medical Device User Fee Amendments. Sets review timeline goals (90-day target for 510(k)).</td></tr>
<tr><td><strong>21 CFR 820</strong></td><td>Quality System Regulation (QSR). FDA's cGMP requirements for medical devices.</td></tr>
<tr><td><strong>ISO 13485</strong></td><td>International standard for medical device quality management systems.</td></tr>
<tr><td><strong>ISO 14971</strong></td><td>International standard for medical device risk management.</td></tr>
<tr><td><strong>IEC 60601-1</strong></td><td>Basic safety and essential performance of medical electrical equipment.</td></tr>
<tr><td><strong>IEC 62304</strong></td><td>Medical device software lifecycle processes.</td></tr>
<tr><td><strong>DHF</strong></td><td>Design History File. Complete collection of design and development records (21 CFR 820.30).</td></tr>
<tr><td><strong>DMR</strong></td><td>Device Master Record. Documentation specifying the finished device.</td></tr>
<tr><td><strong>CAPA</strong></td><td>Corrective and Preventive Action (21 CFR 820.90).</td></tr>
<tr><td><strong>V&amp;V</strong></td><td>Verification and Validation. Confirms design meets inputs (built right) and user needs (built the right thing).</td></tr>
<tr><td><strong>UDI</strong></td><td>Unique Device Identification. FDA-mandated identifier on device labels.</td></tr>
<tr><td><strong>eSTAR</strong></td><td>FDA's standardized electronic submission format for 510(k) applications.</td></tr>
<tr><td><strong>openFDA</strong></td><td>FDA's public API providing searchable access to 510(k) clearances, adverse events, and recalls.</td></tr>
</tbody></table>`,
      cn: `<table class="help-table help-glossary"><thead><tr><th>术语</th><th>定义</th></tr></thead><tbody>
<tr><td><strong>510(k)</strong></td><td>提交给FDA的上市前通知，证明II类器械与已合法上市的前置器械实质等效。</td></tr>
<tr><td><strong>PMA</strong></td><td>上市前批准。FDA最严格的路径，适用于III类器械。</td></tr>
<tr><td><strong>De Novo</strong></td><td>FDA分类路径，适用于没有前置器械的新型低至中等风险器械。</td></tr>
<tr><td><strong>SE</strong></td><td>实质等效。510(k)许可的法律标准。</td></tr>
<tr><td><strong>前置器械</strong></td><td>作为新510(k)提交比较基础的已合法上市器械。</td></tr>
<tr><td><strong>RTA</strong></td><td>拒绝接受。FDA对510(k)提交的初始行政筛选。</td></tr>
<tr><td><strong>Pre-Sub (Q-Sub)</strong></td><td>正式的FDA会议请求，在申报前讨论法规策略。</td></tr>
<tr><td><strong>DICE</strong></td><td>工业和消费者教育部。处理Pre-Sub后勤事务。</td></tr>
<tr><td><strong>MDUFA</strong></td><td>医疗器械用户费修正案。设定审查时间线目标（510(k)的90天目标）。</td></tr>
<tr><td><strong>21 CFR 820</strong></td><td>质量体系法规(QSR)。FDA对医疗器械的cGMP要求。</td></tr>
<tr><td><strong>ISO 13485</strong></td><td>医疗器械质量管理体系国际标准。</td></tr>
<tr><td><strong>ISO 14971</strong></td><td>医疗器械风险管理国际标准。</td></tr>
<tr><td><strong>IEC 60601-1</strong></td><td>医用电气设备基本安全和基本性能。</td></tr>
<tr><td><strong>IEC 62304</strong></td><td>医疗器械软件生命周期过程。</td></tr>
<tr><td><strong>DHF</strong></td><td>设计历史文件。设计和开发记录的完整集合(21 CFR 820.30)。</td></tr>
<tr><td><strong>DMR</strong></td><td>设备主记录。规定成品器械的文档。</td></tr>
<tr><td><strong>CAPA</strong></td><td>纠正和预防措施(21 CFR 820.90)。</td></tr>
<tr><td><strong>V&amp;V</strong></td><td>验证和确认。确认设计满足输入（正确构建）和用户需求（构建正确的东西）。</td></tr>
<tr><td><strong>UDI</strong></td><td>唯一器械标识。FDA要求的器械标签上的标识符。</td></tr>
<tr><td><strong>eSTAR</strong></td><td>FDA标准化电子提交格式，用于510(k)申请。</td></tr>
<tr><td><strong>openFDA</strong></td><td>FDA的公共API，提供对510(k)许可、不良事件和召回的可搜索访问。</td></tr>
</tbody></table>`,
    },
  },
];

// ── Help overlay controller ────────────────────
let helpVisible = false;
let helpSection = 1;

export function toggleHelp(): void {
  helpVisible = !helpVisible;
  renderHelp();
}

export function renderHelp(): void {
  let overlay = document.getElementById("helpOverlay");
  if (!helpVisible) {
    overlay?.remove();
    return;
  }
  if (!overlay) {
    overlay = document.createElement("div");
    overlay.id = "helpOverlay";
    document.body.appendChild(overlay);
  }

  const isCN = document.documentElement.lang === "zh";

  overlay.innerHTML = `
  <div class="help-backdrop" id="helpBackdrop"></div>
  <div class="help-panel">
    <div class="help-header">
      <h2>📖 ${isCN ? "用户指南" : "User Guide"}</h2>
      <div class="help-search-wrap">
        <input type="text" id="helpSearch" class="help-search" placeholder="${isCN ? "搜索指南..." : "Search guide..."}" />
      </div>
      <button class="help-close" id="helpClose">${isCN ? "关闭" : "Close"}</button>
    </div>
    <div class="help-body">
      <nav class="help-toc" id="helpToc">
        ${GUIDE.map(
          (s) =>
            `<a class="help-toc-item ${s.num === helpSection ? "active" : ""}" data-sec="${s.num}">${s.num}. ${localizedText(s.title)}</a>`,
        ).join("")}
      </nav>
      <article class="help-content" id="helpContent">
        ${renderSection(helpSection, isCN)}
      </article>
    </div>
  </div>`;

  // Event listeners
  document.getElementById("helpBackdrop")?.addEventListener("click", () => {
    helpVisible = false;
    renderHelp();
  });
  document.getElementById("helpClose")?.addEventListener("click", () => {
    helpVisible = false;
    renderHelp();
  });

  // TOC navigation
  overlay.querySelectorAll(".help-toc-item").forEach((el) => {
    el.addEventListener("click", () => {
      helpSection = parseInt((el as HTMLElement).dataset.sec || "1", 10);
      renderHelp();
    });
  });

  // Search
  const searchInput = document.getElementById(
    "helpSearch",
  ) as HTMLInputElement | null;
  searchInput?.addEventListener("input", () => {
    const q = searchInput.value.trim().toLowerCase();
    const content = document.getElementById("helpContent");
    const toc = document.getElementById("helpToc");
    if (!content || !toc) return;

    if (!q) {
      // Reset to current section
      content.innerHTML = renderSection(helpSection, isCN);
      toc.querySelectorAll(".help-toc-item").forEach((el) => {
        (el as HTMLElement).style.display = "";
      });
      return;
    }

    // Search all sections
    const results: string[] = [];
    toc.querySelectorAll(".help-toc-item").forEach((el) => {
      (el as HTMLElement).style.display = "";
    });

    GUIDE.forEach((s) => {
      const title = localizedText(s.title).toLowerCase();
      const body = localizedText(s.content).toLowerCase();
      if (title.includes(q) || body.includes(q)) {
        results.push(`<div class="help-search-result" data-sec="${s.num}">
          <h3>${s.num}. ${localizedText(s.title)}</h3>
          ${highlightMatches(localizedText(s.content), q)}
        </div>`);
      } else {
        // Dim non-matching TOC items
        const tocItem = toc.querySelector(
          `[data-sec="${s.num}"]`,
        ) as HTMLElement | null;
        if (tocItem) tocItem.style.display = "none";
      }
    });

    content.innerHTML = results.length
      ? `<div class="help-search-count">${results.length} ${isCN ? "个匹配章节" : "matching section(s)"}</div>${results.join("")}`
      : `<div class="help-search-empty">${isCN ? "未找到匹配项" : "No matches found"}</div>`;

    // Click search result navigates to section
    content.querySelectorAll(".help-search-result").forEach((el) => {
      el.addEventListener("click", () => {
        helpSection = parseInt((el as HTMLElement).dataset.sec || "1", 10);
        searchInput.value = "";
        renderHelp();
      });
    });
  });

  searchInput?.focus();
}

function renderSection(num: number, _isCN: boolean): string {
  const sec = GUIDE.find((s) => s.num === num);
  if (!sec) return "";
  return `<h2>${sec.num}. ${localizedText(sec.title)}</h2>${localizedText(sec.content)}`;
}

function highlightMatches(html: string, query: string): string {
  // Strip HTML tags for snippet extraction, then show first 300 chars around match
  const plain = html.replace(/<[^>]+>/g, " ");
  const idx = plain.toLowerCase().indexOf(query);
  if (idx < 0) return "";
  const start = Math.max(0, idx - 80);
  const end = Math.min(plain.length, idx + query.length + 200);
  let snippet =
    (start > 0 ? "..." : "") +
    plain.slice(start, end) +
    (end < plain.length ? "..." : "");
  // Bold the match
  const re = new RegExp(
    `(${query.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")})`,
    "gi",
  );
  snippet = snippet.replace(re, "<mark>$1</mark>");
  return `<p class="help-snippet">${snippet}</p>`;
}
