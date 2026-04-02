// ============================================================
// HELP — In-App User Guide (EN + CN + KO), searchable HTML overlay
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
    title: { en: "Getting Started", cn: "入门指南", ko: "시작하기" },
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
      ko: `<p>Control Tower PM 대시보드는 FDA 510(k) 의료기기 개발을 위해 특별히 설계된 종합 프로젝트 관리 플랫폼입니다. 규제, 기술 및 비즈니스 워크스트림 전반에 대한 실시간 가시성을 제공합니다.</p>
<h4>시스템 요구사항</h4>
<ul><li>최신 웹 브라우저 (Chrome, Firefox, Safari, Edge)</li><li>Supabase 동기화를 위한 인터넷 연결 (오프라인 모드 가능)</li><li>화면 해상도 1280x720 이상 권장</li></ul>
<h4>첫 실행</h4>
<p>대시보드를 처음 열면 설정 마법사가 프로젝트 구성을 안내합니다. 7개의 기기 템플릿(호흡기, 심혈관, 정형외과, IVD, 영상, 재활, SaMD) 중에서 선택하거나 처음부터 시작할 수 있습니다. 또는 '데모 데이터 로드'를 클릭하여 샘플 데이터로 탐색할 수 있습니다.</p>
<h4>로그인 및 인증</h4>
<p>대시보드는 역할 기반 로그인을 사용합니다. 프로젝트 관리자가 제공한 비밀번호를 입력하세요. 인증 후 할당된 역할과 구독 등급에 적합한 탭이 있는 대시보드가 표시됩니다.</p>
<div class="help-tip">💡 빠른 접근을 위해 대시보드 URL을 북마크하세요. 프로젝트 데이터는 자동으로 저장됩니다.</div>`,
    },
  },
  {
    num: 2,
    title: { en: "Dashboard Overview", cn: "仪表板概览", ko: "대시보드 개요" },
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
      ko: `<p>대시보드는 역할/등급 선택기가 있는 헤더 바, 16개의 기능 탭이 있는 수평 탭 내비게이션 바, 그리고 메인 콘텐츠 영역으로 구성됩니다. 각 탭은 510(k) 프로젝트 수명주기의 특정 측면에 중점을 둡니다.</p>
<h4>헤더 바</h4>
<ul><li>프로젝트 이름 및 부제목 (다국어 EN/CN/KO)</li><li>역할 선택기: PMP, 기술, 비즈니스, 회계 뷰 간 전환</li><li>등급 표시기: 현재 구독 등급 표시 (Starter/Growth/Scale)</li><li>언어 전환: 영어, 중국어, 한국어 인터페이스 간 전환</li></ul>
<h4>16개 탭</h4>
<table class="help-table"><thead><tr><th>탭</th><th>설명</th></tr></thead><tbody>
<tr><td><strong>듀얼 트랙</strong></td><td>기술 및 규제 마일스톤 추적</td></tr>
<tr><td><strong>게이트 시스템</strong></td><td>기준 체크리스트를 포함한 단계별 게이트 심사</td></tr>
<tr><td><strong>규제 추적기</strong></td><td>표준 준수 및 진행 상황 모니터링</td></tr>
<tr><td><strong>위험 대시보드</strong></td><td>심각도/발생확률을 포함한 ISO 14971 위험 매트릭스</td></tr>
<tr><td><strong>감사 추적</strong></td><td>모든 대시보드 변경의 타임스탬프 로그</td></tr>
<tr><td><strong>문서 관리</strong></td><td>ISO 13485 기반 문서 수명주기 관리</td></tr>
<tr><td><strong>조치 항목</strong></td><td>작업 보드, DHF 추적기, DMR 추적기, CAPA 로그</td></tr>
<tr><td><strong>타임라인</strong></td><td>월별 프로젝트 타임라인 뷰</td></tr>
<tr><td><strong>예산</strong></td><td>계획 대비 실제 예산 범주별 추적</td></tr>
<tr><td><strong>현금/런웨이</strong></td><td>현금 보유 현황, 소진율, 런웨이 예측</td></tr>
<tr><td><strong>미국 투자</strong></td><td>투자자 파이프라인 및 IR 활동 추적</td></tr>
<tr><td><strong>지분 현황표</strong></td><td>주주 등록, 지분 이벤트, 베스팅</td></tr>
<tr><td><strong>리소스</strong></td><td>팀 배정 및 활용도 모니터링</td></tr>
<tr><td><strong>공급업체</strong></td><td>공급업체 자격 심사 및 리드타임 추적</td></tr>
<tr><td><strong>게시판</strong></td><td>의사결정 및 조치 추적이 포함된 스레드 토론</td></tr>
<tr><td><strong>FDA 커뮤니케이션</strong></td><td>Q-Sub 생성기, RTA 체크리스트, 규제 타임라인 (PMP 전용)</td></tr>
</tbody></table>
<div class="help-warn">⚠️ 일부 탭은 역할 또는 구독 등급에 따라 제한될 수 있습니다.</div>`,
    },
  },
  {
    num: 3,
    title: {
      en: "Role-Based Access & Tier System",
      cn: "基于角色的访问与层级系统",
      ko: "역할 기반 접근 및 구독 등급",
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
      ko: `<h4>사용자 역할</h4>
<p>대시보드는 각기 다른 접근 수준을 가진 네 가지 주요 역할을 지원합니다:</p>
<table class="help-table"><thead><tr><th>역할</th><th>접근 권한</th></tr></thead><tbody>
<tr><td><strong>PMP (프로젝트 매니저)</strong></td><td>모든 탭에 대한 전체 접근. 마일스톤, 게이트, 위험, 예산, 문서, 팀을 편집할 수 있습니다. FDA 커뮤니케이션을 볼 수 있는 유일한 역할입니다.</td></tr>
<tr><td><strong>기술</strong></td><td>기술 마일스톤, 위험, 문서를 조회 및 업데이트할 수 있습니다. 게시판 참여 가능. 재무 탭 접근 불가.</td></tr>
<tr><td><strong>비즈니스</strong></td><td>비즈니스 마일스톤, 예산, 투자, 지분 현황표에 접근할 수 있습니다. 게시판 참여 가능.</td></tr>
<tr><td><strong>회계</strong></td><td>예산, 현금/런웨이, 지분 현황표에 대한 읽기 전용 접근. 제한된 편집 기능.</td></tr>
</tbody></table>
<h4>구독 등급</h4>
<p>탭 접근은 Supabase RLS를 통해 서버에서 제어됩니다. 등급에 따라 사용 가능한 탭이 결정됩니다:</p>
<table class="help-table"><thead><tr><th>등급</th><th>가격</th><th>사용자 수</th><th>탭</th></tr></thead><tbody>
<tr><td><strong>Starter</strong></td><td>$500/월</td><td>2</td><td>듀얼 트랙, 게이트, 타임라인, 예산</td></tr>
<tr><td><strong>Growth</strong></td><td>$1,000/월</td><td>5</td><td>지분 현황표, FDA 커뮤니케이션, 미국 투자 제외 전체</td></tr>
<tr><td><strong>Scale</strong></td><td>$2,000/월</td><td>10</td><td>FDA 커뮤니케이션 및 지분 현황표를 포함한 전체 16개 탭</td></tr>
</tbody></table>
<div class="help-tip">💡 구독 등급은 서버에서 관리되며 대시보드 UI에서 변경할 수 없습니다.</div>`,
    },
  },
  {
    num: 4,
    title: {
      en: "Dual-Track Milestones",
      cn: "双轨制里程碑",
      ko: "듀얼 트랙 마일스톤",
    },
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
      ko: `<p>듀얼 트랙 탭은 규제와 기술 마일스톤 트랙을 병렬로 표시합니다. 이는 엔지니어링 개발과 규제 준비가 동시에 진행되는 실제 FDA 510(k) 절차를 반영합니다.</p>
<h4>기술 마일스톤</h4>
<p>기술 마일스톤은 엔지니어링 산출물을 추적합니다: 설계 동결, 프로토타입 테스트, 검증 및 확인 활동, 설계 이전. 각 마일스톤은 월별, 상태, 담당자 및 카테고리를 표시합니다.</p>
<h4>규제 마일스톤</h4>
<p>규제 마일스톤은 FDA 산출물을 추적합니다: Pre-Submission 미팅, 510(k) 준비, 제출 신청. 이들은 프로젝트 기간에 따라 자동 생성됩니다.</p>
<h4>마일스톤 편집</h4>
<p>마일스톤 상태 배지를 클릭하면 순차적으로 전환됩니다: 미시작, 진행 중, 완료, 차단. PMP와 해당 역할의 담당자만 상태를 변경할 수 있습니다. 모든 변경 사항은 감사 추적에 기록됩니다.</p>`,
    },
  },
  {
    num: 5,
    title: { en: "Gate System", cn: "门控系统", ko: "게이트 시스템" },
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
      ko: `<p>게이트 시스템은 단계별 게이트 심사 프로세스를 구현합니다. 게이트는 프로젝트 기간에 따라 자동으로 생성됩니다(2~6개 게이트). 각 게이트에는 프로젝트가 진행되기 전에 충족해야 하는 기준이 있습니다.</p>
<h4>게이트 기준</h4>
<p>각 게이트에는 기준 체크리스트가 있습니다(예: '기술 산출물 완료', '예산 정상', '위험 완화 확인'). 기준을 클릭하여 개별적으로 확인합니다. 게이트 상태는 기준 완료에 따라 업데이트됩니다.</p>
<h4>게이트 결정</h4>
<p>PMP는 게이트 결정을 기록할 수 있습니다: 진행(Go), 중단(No-Go), 또는 조건부 진행(Conditional Go). 결정에는 타임스탬프와 귀속 정보가 포함됩니다. 게이트 노트에 논의 사항과 조건부 승인 조건을 기록할 수 있습니다.</p>
<h4>이해관계자 입력</h4>
<p>기술 및 비즈니스 이해관계자가 게이트 입력을 제출할 수 있습니다. 이는 게이트 심사 패널에 표시되어 게이트 결정을 위한 완전한 정보를 제공합니다.</p>`,
    },
  },
  {
    num: 6,
    title: { en: "Regulatory Tracker", cn: "法规跟踪", ko: "규제 추적기" },
    content: {
      en: `<p>The Regulatory Tracker monitors compliance with applicable standards. Standards are pre-populated based on your device template (e.g., IEC 60601-1 for electrical devices, ISO 10993 for biocompatibility) or entered manually.</p>
<h4>Tracking Standards</h4>
<ul><li>Status: Not Started, In Progress, Complete</li><li>Progress bar: 0-100% completion percentage</li><li>Clause-level tracking for detailed compliance</li></ul>
<p>Click the status badge to cycle through states. Update the progress slider to reflect actual completion. The FDA Comms tab uses these values to auto-populate the RTA checklist.</p>`,
      cn: `<p>法规跟踪器监控适用标准的合规性。标准基于您的设备模板预填充（例如电气设备的IEC 60601-1、生物相容性的ISO 10993），也可手动输入。</p>
<h4>标准跟踪</h4>
<ul><li>状态：未开始、进行中、完成</li><li>进度条：0-100%完成百分比</li><li>条款级别跟踪，实现详细合规</li></ul>
<p>点击状态徽章可循环切换状态。更新进度滑块以反映实际完成情况。FDA通讯标签页使用这些值自动填充RTA清单。</p>`,
      ko: `<p>규제 추적기는 적용 가능한 표준의 준수 여부를 모니터링합니다. 표준은 기기 템플릿(예: 전기 기기용 IEC 60601-1, 생체적합성용 ISO 10993)에 따라 자동으로 입력되거나 수동으로 입력할 수 있습니다.</p>
<h4>표준 추적</h4>
<ul><li>상태: 미시작, 진행 중, 완료</li><li>진행률 바: 0-100% 완료 백분율</li><li>세부 준수를 위한 조항 수준 추적</li></ul>
<p>상태 배지를 클릭하여 상태를 순차적으로 전환합니다. 진행률 슬라이더를 업데이트하여 실제 완료 상황을 반영하세요. FDA 커뮤니케이션 탭에서 이 값을 사용하여 RTA 체크리스트를 자동으로 채웁니다.</p>`,
    },
  },
  {
    num: 7,
    title: { en: "Risk Dashboard", cn: "风险看板", ko: "위험 대시보드" },
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
      ko: `<p>위험 대시보드는 ISO 14971 위험 관리를 구현합니다. 위험은 심각도, 발생확률, 위험 수준을 보여주는 색상 코드 매트릭스로 표시됩니다. 템플릿별 위험은 기기 카테고리에서 자동으로 채워집니다.</p>
<h4>위험 필드</h4>
<table class="help-table"><thead><tr><th>필드</th><th>설명</th></tr></thead><tbody>
<tr><td><strong>심각도</strong></td><td>위해의 심각한 정도 (낮음/중간/높음)</td></tr>
<tr><td><strong>발생확률</strong></td><td>위험 상황이 발생할 가능성 (낮음/중간/높음)</td></tr>
<tr><td><strong>위험 수준</strong></td><td>색상 코드: 녹색 (허용 가능), 노란색 (ALARP), 빨간색 (허용 불가)</td></tr>
<tr><td><strong>통제 조치</strong></td><td>구현된 위험 통제 조치</td></tr>
<tr><td><strong>잔여 위험</strong></td><td>통제 후 남은 위험</td></tr>
<tr><td><strong>완화 상태</strong></td><td>미시작, 진행 중, 완료</td></tr>
</tbody></table>
<div class="help-tip">💡 빨간색 위험은 FDA 커뮤니케이션 패널에서 경고를 트리거하며 510(k) 제출 전에 해결해야 합니다.</div>`,
    },
  },
  {
    num: 8,
    title: { en: "Audit Trail", cn: "审计追踪", ko: "감사 추적" },
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
      ko: `<p>대시보드에서 이루어진 모든 변경 사항은 타임스탬프, 사용자 역할, 작업 유형, 변경된 필드, 이전 값, 새 값 및 상세 설명과 함께 감사 추적에 기록됩니다. 이는 21 CFR Part 11 추적성 요구사항을 지원합니다.</p>
<h4>Supabase 동기화</h4>
<p>감사 항목은 Supabase 백엔드에 자동으로 동기화됩니다. 오프라인 상태인 경우 항목이 로컬에 대기열로 저장되고 연결이 복원되면 전송됩니다.</p>
<h4>필터링</h4>
<p>감사 추적은 작업 유형별 필터링과 키워드 검색을 지원합니다. 최근 항목이 먼저 표시됩니다. 내보내기 기능을 통해 전체 감사 이력을 다운로드할 수 있습니다.</p>`,
    },
  },
  {
    num: 9,
    title: { en: "Document Control", cn: "文档控制", ko: "문서 관리" },
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
      ko: `<p>문서 관리는 ISO 13485에 맞춘 문서 수명주기 관리를 제공합니다. 지적 재산을 보호하기 위해 문서는 브라우저에서 로컬로 추적되며, 승인/발효된 문서에 대해 서버 동기화가 가능합니다.</p>
<h4>문서 수명주기</h4>
<ul><li><strong>초안</strong> — 초기 문서 생성</li><li><strong>검토 중</strong> — 이해관계자 검토 중</li><li><strong>승인됨</strong> — 지정된 권한자에 의해 공식 승인</li><li><strong>발효</strong> — 활성 상태 및 관리 중 (발효일 자동 설정)</li><li><strong>폐기</strong> — 대체되었거나 철회됨</li></ul>
<p>상태 배지를 클릭하여 수명주기를 순차적으로 전환합니다. PMP만 문서 상태를 변경할 수 있습니다.</p>
<h4>문서 필드</h4>
<table class="help-table"><thead><tr><th>필드</th><th>설명</th></tr></thead><tbody>
<tr><td><strong>DCN</strong></td><td>문서 관리 번호 (자동 생성, 예: DCN-REG-001)</td></tr>
<tr><td><strong>카테고리</strong></td><td>규제, 기술, 비즈니스, 법률, 재무, 템플릿</td></tr>
<tr><td><strong>버전</strong></td><td>개정 이력을 포함한 버전 번호</td></tr>
<tr><td><strong>담당자</strong></td><td>책임자 또는 역할</td></tr>
<tr><td><strong>출처 참조</strong></td><td>외부 참조 (GitHub 커밋, SVN 리비전 등)</td></tr>
<tr><td><strong>연결</strong></td><td>연결된 마일스톤 또는 게이트 (예: R8, T2)</td></tr>
</tbody></table>
<h4>서버에 동기화</h4>
<p>문서가 '승인됨' 또는 '발효' 상태에 도달하면 '서버에 동기화' 버튼을 사용하여 Supabase dhf_documents 테이블에 업로드합니다. FDA 커뮤니케이션 탭에서 승인된 문서가 동기화되지 않은 경우 경고를 표시합니다.</p>
<div class="help-warn">⚠️ 문서는 브라우저 localStorage에 저장됩니다. 브라우저 데이터 삭제 = 문서 손실. 중요한 문서는 서버에 동기화하세요.</div>`,
    },
  },
  {
    num: 10,
    title: { en: "Actions", cn: "行动项", ko: "조치 항목" },
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
      ko: `<p>조치 항목 탭은 게이트 심사, 위험 완화 및 일반 프로젝트 관리에서 발생하는 조치 항목을 추적합니다.</p>
<h4>조치 항목 필드</h4>
<table class="help-table"><thead><tr><th>필드</th><th>설명</th></tr></thead><tbody>
<tr><td><strong>담당자</strong></td><td>책임 팀원</td></tr>
<tr><td><strong>우선순위</strong></td><td>높음, 중간, 낮음</td></tr>
<tr><td><strong>상태</strong></td><td>할 일, 진행 중, 완료, 차단</td></tr>
<tr><td><strong>마감일</strong></td><td>목표 완료일</td></tr>
<tr><td><strong>연결된 게이트</strong></td><td>관련 게이트 심사 (예: G1, G2)</td></tr>
</tbody></table>
<h4>DHF 문서 추적기</h4>
<p>설계 이력 파일(DHF) 문서 추적기는 조치 항목 탭 내에 있습니다. 21 CFR 820.30에서 요구하는 모든 설계 단계 문서를 추적합니다. 문서의 상태 배지를 클릭하면 순차적으로 전환됩니다: 미시작, 초안, 검토 중, 승인됨.</p>
<h4>DMR 문서 추적기</h4>
<p>장치 마스터 레코드(DMR) 문서 추적기도 조치 항목 탭 내에 있습니다. 21 CFR 820.181에서 요구하는 12개 문서를 추적하며, 기기 사양, 생산 공정, 품질 절차, 포장/라벨링을 포함합니다.</p>
<h4>CAPA 로그</h4>
<p>시정 및 예방 조치(CAPA) 로그는 유형(시정 또는 예방), 상태, 담당자 및 연결된 게이트와 함께 CAPA 항목을 추적합니다.</p>`,
    },
  },
  {
    num: 11,
    title: { en: "Timeline", cn: "时间线", ko: "타임라인" },
    content: {
      en: `<p>The Timeline provides a month-by-month view of project events. Each entry shows technical and business activities with an impact indicator (positive/neutral/negative). Timeline events are auto-generated during wizard setup and can be edited.</p>`,
      cn: `<p>时间线提供按月份的项目事件视图。每个条目显示技术和业务活动，并带有影响指标（正面/中性/负面）。时间线事件在向导设置期间自动生成，可以编辑。</p>`,
      ko: `<p>타임라인은 프로젝트 이벤트의 월별 뷰를 제공합니다. 각 항목은 영향 지표(긍정적/중립/부정적)와 함께 기술 및 비즈니스 활동을 표시합니다. 타임라인 이벤트는 마법사 설정 중에 자동 생성되며 편집할 수 있습니다.</p>`,
    },
  },
  {
    num: 12,
    title: { en: "Budget", cn: "预算", ko: "예산" },
    content: {
      en: `<p>The Budget tab tracks spending against planned budgets by category. Categories are defined during wizard setup (or from template budget lines). Each category shows planned amount, actual spend, and variance.</p>
<h4>Budget Management</h4>
<ul><li>Add, edit, or delete budget categories</li><li>Update actual spend values to track variance</li><li>Currency display toggles between USD and CNY</li><li>All changes logged in Audit Trail</li></ul>`,
      cn: `<p>预算标签页按类别跟踪支出与计划预算的对比。类别在向导设置期间定义（或来自模板预算行）。每个类别显示计划金额、实际支出和差异。</p>
<h4>预算管理</h4>
<ul><li>添加、编辑或删除预算类别</li><li>更新实际支出值以跟踪差异</li><li>货币显示在USD和CNY之间切换</li><li>所有更改记录在审计追踪中</li></ul>`,
      ko: `<p>예산 탭은 카테고리별로 계획 예산 대비 지출을 추적합니다. 카테고리는 마법사 설정 중에 정의되거나 템플릿 예산 항목에서 가져옵니다. 각 카테고리는 계획 금액, 실제 지출 및 차이를 표시합니다.</p>
<h4>예산 관리</h4>
<ul><li>예산 카테고리 추가, 편집 또는 삭제</li><li>실제 지출 값을 업데이트하여 차이 추적</li><li>통화 표시를 USD와 CNY 간 전환</li><li>모든 변경 사항은 감사 추적에 기록</li></ul>`,
    },
  },
  {
    num: 13,
    title: { en: "Cash / Runway", cn: "现金/跑道", ko: "현금/런웨이" },
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
      ko: `<p>현금/런웨이는 재무 건전성 가시성을 제공합니다: 현재 현금 보유 현황, 월간 소진율, 예상 런웨이 개월 수. 펀딩 라운드 추적 및 소진 이력 차트를 포함합니다.</p>
<h4>핵심 지표</h4>
<table class="help-table"><thead><tr><th>지표</th><th>설명</th></tr></thead><tbody>
<tr><td><strong>보유 현금</strong></td><td>현재 사용 가능한 현금 잔액</td></tr>
<tr><td><strong>월간 소진율</strong></td><td>평균 월간 지출률</td></tr>
<tr><td><strong>런웨이</strong></td><td>현재 소진율로 운영 가능한 개월 수</td></tr>
</tbody></table>
<h4>펀딩 라운드</h4>
<p>펀딩 라운드를 상태별로 추적합니다 (계획, 진행 중, 수령). 각 라운드는 금액, 날짜 및 자금 출처를 기록합니다.</p>`,
    },
  },
  {
    num: 14,
    title: { en: "US Investment", cn: "美国投资", ko: "미국 투자" },
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
      ko: `<p>미국 투자 탭은 미국 시장 진출을 추진하는 의료기기 벤처의 투자자 관계를 관리합니다.</p>
<h4>대상 투자자</h4>
<table class="help-table"><thead><tr><th>필드</th><th>옵션</th></tr></thead><tbody>
<tr><td><strong>유형</strong></td><td>VC, 엔젤 그룹, 전략적, PE, 정부</td></tr>
<tr><td><strong>단계</strong></td><td>시드, 시리즈 A, 시리즈 B, 성장</td></tr>
<tr><td><strong>연락 상태</strong></td><td>잠재, 연락 완료, 논의 중, 텀시트, 확약</td></tr>
</tbody></table>
<h4>IR 활동</h4>
<p>투자자 관계 활동을 기록합니다: 미팅, 프레젠테이션, 실사 세션, 텀시트 협상. 각 활동에는 날짜, 유형 및 상태가 있습니다.</p>`,
    },
  },
  {
    num: 15,
    title: { en: "Cap Table", cn: "股权表", ko: "지분 현황표" },
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
      ko: `<p>지분 현황표는 지분 소유권, 지분 이벤트 및 베스팅 일정을 추적합니다.</p>
<h4>주주</h4>
<ul><li>이름, 주식 클래스 (보통주, 우선주 A/B/C, 옵션, 워런트)</li><li>주식 수 및 소유권 백분율</li><li>이사회 석, 베스팅 상태 및 메모</li></ul>
<h4>지분 이벤트</h4>
<ul><li>펀딩 라운드, 주식 분할, 옵션 부여, 전환 추적</li><li>각 이벤트는 발행 주식 수, 주당 가격, 총 조달 금액을 기록</li></ul>
<h4>베스팅 일정</h4>
<ul><li>1년 클리프가 포함된 4년 표준 베스팅, 또는 맞춤형 일정</li><li>클리프 날짜, 총 주식, 베스팅된 주식, 다음 베스팅 날짜 추적</li></ul>`,
    },
  },
  {
    num: 16,
    title: { en: "Resources", cn: "资源", ko: "리소스" },
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
      ko: `<p>리소스 탭은 팀원의 역할, 워크스트림 배정 및 활용률을 표시합니다.</p>
<h4>팀원 관리</h4>
<ul><li>이름, 역할, 이메일, 워크스트림 배정과 함께 팀원 추가</li><li>배정 백분율을 클릭하여 인라인 편집 (PMP/기술/비즈니스 역할)</li><li>활용도 게이지: 녹색 (&lt;85%), 노란색 (85-100%), 빨간색 (&gt;100% 과배정)</li><li>각 카드의 X 버튼으로 팀원 삭제</li></ul>
<h4>워크스트림 배정</h4>
<p>각 팀원은 여러 워크스트림에 배정할 수 있습니다. 백분율은 인라인 편집 가능합니다. 활용도 게이지가 자동으로 업데이트됩니다. 변경 사항은 감사 로그에 기록됩니다.</p>
<div class="help-tip">💡 번아웃을 방지하려면 총 배정을 100% 이하로 유지하세요. 대시보드에서 과배정을 빨간색으로 표시합니다.</div>`,
    },
  },
  {
    num: 17,
    title: { en: "Suppliers", cn: "供应商", ko: "공급업체" },
    content: {
      en: `<p>The Suppliers tab tracks supplier qualification status, lead times, purchase order status, and contract manufacturing milestones. This supports 21 CFR 820 supplier controls.</p>
<h4>Supplier Status</h4>
<ul><li><strong>Under Review</strong> — Initial evaluation</li><li><strong>Qualified</strong> — Approved for use</li><li><strong>Active</strong> — Currently supplying</li><li><strong>On Hold</strong> — Temporarily suspended</li><li><strong>Rejected</strong> — Failed qualification</li></ul>`,
      cn: `<p>供应商标签页跟踪供应商资质审核状态、交期、采购订单状态和代工里程碑。这支持21 CFR 820供应商控制要求。</p>
<h4>供应商状态</h4>
<ul><li><strong>审核中</strong> — 初始评估</li><li><strong>已资质</strong> — 批准使用</li><li><strong>活跃</strong> — 当前供货中</li><li><strong>暂停</strong> — 临时暂停</li><li><strong>拒绝</strong> — 资质审核未通过</li></ul>`,
      ko: `<p>공급업체 탭은 공급업체 자격 심사 상태, 리드타임, 구매 주문 상태 및 위탁 제조 마일스톤을 추적합니다. 이는 21 CFR 820 공급업체 관리 요구사항을 지원합니다.</p>
<h4>공급업체 상태</h4>
<ul><li><strong>심사 중</strong> — 초기 평가</li><li><strong>자격 충족</strong> — 사용 승인됨</li><li><strong>활성</strong> — 현재 공급 중</li><li><strong>보류</strong> — 일시적으로 중단</li><li><strong>거절</strong> — 자격 심사 미통과</li></ul>`,
    },
  },
  {
    num: 18,
    title: { en: "Message Board", cn: "消息板", ko: "게시판" },
    content: {
      en: `<p>The Message Board is a purpose-driven messaging system for cross-functional communication. It supports threaded discussions with lifecycle management, decisions tracking, and action item creation.</p>
<h4>Threads</h4>
<p>Create threads with a title, workstream assignment, priority level, and intent (Discuss, Decide, Inform, Escalate). Threads flow through an Open &rarr; Resolved lifecycle.</p>
<h4>Pre-Sub Questions Workstream</h4>
<p>Use the <strong>Pre-Sub Questions</strong> workstream to author questions for your FDA Pre-Submission package. Any team member can create threads under this workstream &mdash; each thread becomes one question in the exported package. Use the thread objective field for context/rationale, and add messages to discuss the question with your team.</p>
<p>Once questions are finalized, the PMP exports them from the FDA Comms tab using the <em>Export Question Package</em> button. The export includes the question title, context, and any discussion messages.</p>
<h4>Posting Messages</h4>
<p>Select your posting role from the role picker toolbar. Type your message and press Send. Use [DECISION] or [ACTION] prefixes to tag messages with special intent.</p>
<h4>Settings</h4>
<p>Click the Settings gear icon to configure email addresses for each role. Toggle Test Mode for development. Click Settings again to close the panel.</p>
<h4>Views &amp; Filters</h4>
<ul><li>All Threads: Complete thread list</li><li>My Items: Threads where you are owner or assignee</li><li>Decisions: Threads with active decisions</li><li>Executive: High-priority and decision threads</li><li>Workstream filter: Filter by workstream category (including Pre-Sub Questions)</li><li>Lifecycle filter: Open, Resolved, or All</li></ul>`,
      cn: `<p>消息板是跨职能沟通的专用消息系统。它支持带生命周期管理、决策跟踪和行动项创建的线程讨论。</p>
<h4>线程</h4>
<p>创建线程时设置标题、工作流分配、优先级和意图（讨论、决定、通知、升级）。线程经历 打开 → 已解决 的生命周期。</p>
<h4>Pre-Sub问题工作流</h4>
<p>使用<strong>Pre-Sub问题</strong>工作流来撰写FDA Pre-Submission包的问题。任何团队成员都可以在此工作流下创建线程——每个线程成为导出包中的一个问题。使用线程目标字段填写背景/理由，并添加消息与团队讨论问题。</p>
<p>问题确定后，PMP从FDA通信标签页使用<em>导出问题包</em>按钮导出。导出内容包括问题标题、背景和所有讨论消息。</p>
<h4>发送消息</h4>
<p>从角色选择工具栏中选择您的发布角色。输入消息并按发送。使用[DECISION]或[ACTION]前缀标记具有特殊意图的消息。</p>
<h4>设置</h4>
<p>点击设置齿轮图标配置每个角色的电子邮件地址。切换测试模式用于开发。再次点击设置关闭面板。</p>
<h4>视图与筛选</h4>
<ul><li>所有线程：完整线程列表</li><li>我的项目：您是所有者或负责人的线程</li><li>决策：有活跃决策的线程</li><li>高管：高优先级和决策线程</li><li>工作流筛选：按工作流类别筛选（包括Pre-Sub问题）</li><li>生命周期筛选：打开、已解决或全部</li></ul>`,
      ko: `<p>게시판은 부서 간 커뮤니케이션을 위한 목적 지향 메시징 시스템입니다. 수명주기 관리, 의사결정 추적 및 조치 항목 생성이 포함된 스레드 토론을 지원합니다.</p>
<h4>스레드</h4>
<p>제목, 워크스트림 배정, 우선순위 및 의도(토론, 결정, 알림, 에스컬레이션)를 설정하여 스레드를 생성합니다. 스레드는 열림 → 해결됨 수명주기를 따릅니다.</p>
<h4>Pre-Sub 질문 워크스트림</h4>
<p><strong>Pre-Sub 질문</strong> 워크스트림을 사용하여 FDA Pre-Submission 패키지용 질문을 작성합니다. 모든 팀원이 이 워크스트림 아래에 스레드를 생성할 수 있으며, 각 스레드가 내보낸 패키지의 하나의 질문이 됩니다. 스레드 목표 필드에 배경/근거를 작성하고 메시지를 추가하여 팀과 질문을 논의합니다.</p>
<p>질문이 확정되면 PMP가 FDA 커뮤니케이션 탭에서 <em>질문 패키지 내보내기</em> 버튼을 사용하여 내보냅니다. 내보내기에는 질문 제목, 맥락 및 모든 토론 메시지가 포함됩니다.</p>
<h4>메시지 작성</h4>
<p>역할 선택 도구 모음에서 작성 역할을 선택합니다. 메시지를 입력하고 보내기를 누릅니다. [DECISION] 또는 [ACTION] 접두사를 사용하여 특별한 의도를 가진 메시지를 태그합니다.</p>
<h4>설정</h4>
<p>설정 기어 아이콘을 클릭하여 각 역할의 이메일 주소를 설정합니다. 개발용 테스트 모드를 전환합니다. 설정을 다시 클릭하면 패널이 닫힙니다.</p>
<h4>보기 및 필터</h4>
<ul><li>모든 스레드: 전체 스레드 목록</li><li>내 항목: 소유자 또는 담당자인 스레드</li><li>결정: 활성 결정이 있는 스레드</li><li>경영진: 높은 우선순위 및 결정 스레드</li><li>워크스트림 필터: 워크스트림 카테고리별 필터 (Pre-Sub 질문 포함)</li><li>수명주기 필터: 열림, 해결됨, 또는 전체</li></ul>`,
    },
  },
  {
    num: 19,
    title: {
      en: "FDA Communications Center",
      cn: "FDA通讯中心",
      ko: "FDA 커뮤니케이션 센터",
    },
    content: {
      en: `<p>The FDA Comms tab is PMP-only and provides tools for FDA regulatory interactions.</p>
<h4>Q-Sub Cover Letter Generator</h4>
<p>Select from 5 Q-Sub types (Pre-Sub Meeting, Pre-Sub Written, SIR, Informational Meeting, Study Risk Determination) to auto-generate a cover letter with your company letterhead. Export as HTML for final formatting.</p>
<h4>Export Question Package</h4>
<p>Exports all open <strong>Pre-Sub Questions</strong> threads from the Message Board into a formatted HTML document. Each thread becomes a numbered question. The thread title is the question text, the objective field provides context, and any discussion messages are included below.</p>
<p><strong>Workflow:</strong> Team members author questions on the Message Board (Pre-Sub Questions workstream) &rarr; PMP reviews and curates &rarr; PMP exports the final package from FDA Comms.</p>
<p>If no Pre-Sub Questions threads exist, the export will prompt you to create them on the Message Board first.</p>
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
<h4>导出问题包</h4>
<p>将消息板上所有打开的<strong>Pre-Sub问题</strong>线程导出为格式化HTML文档。每个线程成为一个编号问题。线程标题为问题文本，目标字段提供背景，所有讨论消息包含在下方。</p>
<p><strong>工作流：</strong>团队成员在消息板上撰写问题（Pre-Sub问题工作流）→ PMP审核和整理 → PMP从FDA通信导出最终包。</p>
<p>如果没有Pre-Sub问题线程，导出时会提示您先在消息板上创建。</p>
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
      ko: `<p>FDA 커뮤니케이션 탭은 PMP 전용이며 FDA 규제 상호작용을 위한 도구를 제공합니다.</p>
<h4>Q-Sub 커버 레터 생성기</h4>
<p>5가지 Q-Sub 유형(Pre-Sub 미팅, Pre-Sub 서면, SIR, 정보 미팅, 연구 위험 판정) 중 선택하여 회사 레터헤드가 포함된 커버 레터를 자동 생성합니다. 최종 서식을 위해 HTML로 내보냅니다.</p>
<h4>질문 패키지 내보내기</h4>
<p>게시판의 모든 열린 <strong>Pre-Sub 질문</strong> 스레드를 형식화된 HTML 문서로 내보냅니다. 각 스레드가 번호가 매겨진 질문이 됩니다. 스레드 제목이 질문 텍스트이고, 목표 필드가 맥락을 제공하며, 모든 토론 메시지가 아래에 포함됩니다.</p>
<p><strong>워크플로:</strong> 팀원이 게시판에서 질문을 작성 (Pre-Sub 질문 워크스트림) → PMP가 검토 및 정리 → PMP가 FDA 커뮤니케이션에서 최종 패키지를 내보냅니다.</p>
<p>Pre-Sub 질문 스레드가 없으면 내보내기 시 게시판에서 먼저 생성하라는 안내가 표시됩니다.</p>
<h4>Q-Submission 유형 참조</h4>
<p>모든 5가지 FDA CDRH Q-Sub 유형 개요, 목적, 타임라인 및 "언제 사용" 가이드를 포함합니다. "올바른 Q-Sub 유형 선택 방법" 결정 가이드가 포함되어 있습니다.</p>
<h4>접수 거부(RTA) 체크리스트</h4>
<p>FDA의 17개 항목 RTA 체크리스트에 대한 자체 점검. 항목은 DHF 문서 및 표준 준수 데이터에서 자동으로 채워집니다. 진행률 바가 전체 준비 상태 백분율을 표시합니다.</p>
<h4>문서 동기화 알림</h4>
<p>문서 관리에서 승인 또는 발효된 문서가 서버에 동기화되지 않은 경우 황색 알림 배너가 표시됩니다. "문서 관리로 이동"을 클릭하여 이동 후 동기화합니다.</p>
<h4>MDUFA 심사 타임라인</h4>
<p>510(k) MDUFA 심사 마일스톤을 추적합니다: 제출 접수, K번호 할당(7일차), RTA 스크리닝(15일차), 실질 심사(60일차), MDUFA 결정 목표(90일차).</p>
<h4>SE 결정 흐름도</h4>
<p>FDA의 실질적 동등성 판정을 위한 시각적 결정 흐름: 선행기기 식별, 사용 목적 비교, 기술적 특성 분석, 안전성/유효성 평가.</p>`,
    },
  },
  {
    num: 20,
    title: {
      en: "Setup Wizard & Templates",
      cn: "设置向导与模板",
      ko: "설정 마법사 및 템플릿",
    },
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
      ko: `<p>설정 마법사는 처음 방문 시(또는 프로젝트 데이터가 없을 때) 실행됩니다. 3단계 설정 프로세스를 안내합니다.</p>
<h4>1단계: 언어 선택</h4>
<p>마법사 및 대시보드 인터페이스의 언어를 영어, 중국어 또는 한국어 중에서 선택합니다.</p>
<h4>2단계: 기기 템플릿</h4>
<p>7개의 사전 구성된 기기 템플릿 중에서 선택하거나 처음부터 시작합니다:</p>
<ul><li>호흡기 기기 (인공호흡기, CPAP, 네뷸라이저)</li><li>심혈관 (스텐트, 페이스메이커, 모니터)</li><li>정형외과 (임플란트, 기구, 고정장치)</li><li>IVD (체외진단, 분석키트, 분석기)</li><li>영상 (X선, 초음파, MRI 부속품)</li><li>재활 (치료기기, 보행보조기)</li><li>SaMD (의료기기 소프트웨어)</li></ul>
<p>템플릿 자동 입력 항목: 제출 유형, 기기 등급, 제품 코드, 규제 조항, 선행기기 예시, 기술 영역, 예산 카테고리, 표준 및 템플릿별 위험.</p>
<h4>3단계: 프로젝트 세부사항 (8단계)</h4>
<ul><li>단계 1: 프로젝트 이름 및 부제목</li><li>단계 2: 규제 세부사항 (제출 유형, 기기 등급, 선행기기)</li><li>단계 3: 신청자 및 제조업체 정보</li><li>단계 4: 역할 및 워크스트림 배정이 포함된 팀원</li><li>단계 5: 예산 카테고리 및 금액</li><li>단계 6: 보유 현금 및 프로젝트 기간</li><li>단계 7: 공급업체 및 부품</li><li>단계 8: DHF 문서 선택</li></ul>`,
    },
  },
  {
    num: 21,
    title: {
      en: "Keyboard Shortcuts & Tips",
      cn: "快捷操作与技巧",
      ko: "단축키 및 팁",
    },
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
      ko: `<h4>일반 팁</h4>
<ul><li>모든 데이터는 브라우저 localStorage에 자동 저장됩니다 — 전체 대시보드 상태 포함</li><li>대시보드 상태는 브라우저 충돌 및 정전 후에도 유지됩니다</li><li>온라인 상태에서 Supabase 동기화가 실시간으로 이루어집니다</li><li>오프라인 변경 사항은 대기열에 저장되어 연결이 복원되면 동기화됩니다</li><li>통화 표시는 언어 설정에 따라 USD와 CNY 간 전환됩니다</li><li>플로팅 액션 버튼(우측 하단)이 빠른 조치를 제공합니다</li></ul>
<h4>URL 매개변수</h4>
<table class="help-table"><thead><tr><th>매개변수</th><th>효과</th></tr></thead><tbody>
<tr><td><code>?test=respiratory</code></td><td>호흡기 템플릿의 테스트 데이터 로드</td></tr>
<tr><td><code>?test=cardiovascular</code></td><td>심혈관 템플릿의 테스트 데이터 로드</td></tr>
<tr><td><code>?test=&lt;templateId&gt;</code></td><td>7개 템플릿 중 하나의 사전 빌드된 테스트 데이터 로드</td></tr>
</tbody></table>
<h4>데이터 지속성</h4>
<ul><li><code>ctower_project_data</code> — 프로젝트 구성</li><li><code>ctower_live_state</code> — 전체 대시보드 상태 (마일스톤, 게이트, 위험, 예산 등)</li><li><code>ctower_mb_threads</code> — 게시판 스레드</li><li><code>ctower_doclib_docs</code> — 문서</li><li>Supabase <code>messages</code> 테이블 — 동기화된 메시지</li><li>Supabase <code>audit_log</code> 테이블 — 동기화된 감사 항목</li></ul>
<div class="help-tip">💡 모든 대시보드 상태는 매 변경 후 자동으로 localStorage에 저장됩니다. 정전이나 브라우저 충돌 시에도 데이터가 보존됩니다.</div>`,
    },
  },
  {
    num: 22,
    title: { en: "Troubleshooting", cn: "故障排除", ko: "문제 해결" },
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
      ko: `<h4>대시보드가 로드되지 않음</h4>
<ul><li>초기 Supabase 인증을 위한 인터넷 연결 확인</li><li>브라우저 캐시를 지우고 새로고침</li><li>배포 URL이 올바른지 확인</li></ul>
<h4>탭이 회색으로 표시됨</h4>
<p>탭 접근은 구독 등급에 의해 제어됩니다. 취소선 텍스트가 있는 회색 탭은 현재 등급에 포함되지 않음을 나타냅니다. 업그레이드하려면 관리자에게 문의하세요.</p>
<h4>메시지가 동기화되지 않음</h4>
<ul><li>인터넷 연결 확인 (녹색 표시기)</li><li>브라우저 콘솔에서 Supabase 오류 확인</li><li>연결이 복원되면 메시지가 자동으로 동기화됩니다</li></ul>
<h4>설정 패널이 표시되지 않음</h4>
<p>게시판에서 설정 기어 아이콘을 클릭하세요. 패널이 스레드 목록 위에 나타나고 화면에 스크롤됩니다. 설정을 다시 클릭하면 닫힙니다.</p>
<h4>오래된 데모 데이터</h4>
<p>이전 프로젝트의 데이터가 표시되면 마법사의 '데모 데이터 로드'가 모든 기존 데이터를 지우고 새로운 샘플 데이터를 생성합니다.</p>
<h4>대시보드 초기화</h4>
<p>완전히 초기화하려면 다음 localStorage 키를 지우세요: ctower_project_data, ctower_live_state, ctower_mb_threads, ctower_mb_decisions, ctower_doclib_docs, ctower_qa_messages, ctower_qa_settings, ctower_qa_archive. 또는 브라우저 설정에서 모든 사이트 데이터를 지우세요.</p>`,
    },
  },
  {
    num: 23,
    title: {
      en: "510(k) Predicate Finder",
      cn: "510(k) Predicate Finder",
      ko: "510(k) 선행기기 검색기",
    },
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
      ko: `<p>510(k) 선행기기 검색기는 FDA openFDA 데이터베이스에 연결되는 동반 SaaS 도구입니다. PMP 및 규제 팀이 선행기기를 식별하고, 선행기기 체인을 추적하며, 실질적 동등성 논증 초안을 작성하는 데 도움을 줍니다.</p>
<h4>무료 vs Pro</h4>
<p>선행기기 검색기는 일일 제한(5회 검색, 1회 체인 추적, 2기기 비교)으로 무료 이용 가능합니다. Pro ($99/월)는 무제한 검색, 무제한 체인 추적, 4기기 비교, SE 논증 생성 및 PDF 내보내기를 이용할 수 있습니다.</p>
<h4>Control Tower와의 통합 (Scale 등급)</h4>
<p>Scale 등급($2,000/월)에서 선행기기 검색기는 Control Tower 대시보드에 직접 내장됩니다. 선행기기 연구는 다음에 정보를 제공합니다:</p>
<ul><li>규제 추적기 — 선행기기 참조 및 SE 전략</li><li>위험 대시보드 — 선행기기 비교 중 식별된 위험</li><li>FDA 커뮤니케이션 센터 — 선행기기 분석에 기반한 Pre-Sub 논의 사항</li><li>문서 관리 — DHF 산출물로서의 선행기기 비교 보고서</li></ul>
<h4>PMP 워크플로</h4>
<ol><li>선행기기 검색기를 사용하여 제품 코드 또는 키워드로 후보 선행기기 검색</li><li>규제 계보를 이해하기 위해 선행기기 체인 추적</li><li>최대 4개 기기를 나란히 비교(Pro)하여 가장 강력한 선행기기 선택</li><li>규제 팀의 출발점으로 SE 논증 초안 생성(Pro)</li><li>결과를 PDF로 내보내고 문서 관리의 510(k) 제출 패키지에 첨부</li></ol>`,
    },
  },
  {
    num: 24,
    title: {
      en: "Glossary of FDA & Regulatory Terms",
      cn: "FDA与法规术语表",
      ko: "FDA 및 규제 용어 사전",
    },
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
      ko: `<table class="help-table help-glossary"><thead><tr><th>용어</th><th>정의</th></tr></thead><tbody>
<tr><td><strong>510(k)</strong></td><td>Class II 기기가 합법적으로 판매 중인 선행기기와 실질적으로 동등함을 입증하기 위해 FDA에 제출하는 시판 전 통지서.</td></tr>
<tr><td><strong>PMA</strong></td><td>시판 전 승인. Class III 기기에 필요한 FDA의 가장 엄격한 경로.</td></tr>
<tr><td><strong>De Novo</strong></td><td>선행기기가 없는 신규 저~중위험 기기를 위한 FDA 분류 경로.</td></tr>
<tr><td><strong>SE</strong></td><td>실질적 동등성. 510(k) 허가의 법적 기준.</td></tr>
<tr><td><strong>선행기기</strong></td><td>새로운 510(k) 제출의 비교 근거로 사용되는 합법적으로 판매 중인 기기.</td></tr>
<tr><td><strong>RTA</strong></td><td>접수 거부. 510(k) 제출에 대한 FDA의 초기 행정 심사.</td></tr>
<tr><td><strong>Pre-Sub (Q-Sub)</strong></td><td>제출 전 규제 전략을 논의하기 위한 공식 FDA 미팅 요청.</td></tr>
<tr><td><strong>DICE</strong></td><td>산업 및 소비자 교육과. Pre-Sub 관련 행정을 처리.</td></tr>
<tr><td><strong>MDUFA</strong></td><td>의료기기 사용자 수수료 수정안. 심사 타임라인 목표를 설정 (510(k)의 90일 목표).</td></tr>
<tr><td><strong>21 CFR 820</strong></td><td>품질 시스템 규정(QSR). 의료기기에 대한 FDA의 cGMP 요구사항.</td></tr>
<tr><td><strong>ISO 13485</strong></td><td>의료기기 품질 관리 시스템 국제 표준.</td></tr>
<tr><td><strong>ISO 14971</strong></td><td>의료기기 위험 관리 국제 표준.</td></tr>
<tr><td><strong>IEC 60601-1</strong></td><td>의료용 전기 기기의 기본 안전성 및 필수 성능.</td></tr>
<tr><td><strong>IEC 62304</strong></td><td>의료기기 소프트웨어 수명주기 프로세스.</td></tr>
<tr><td><strong>DHF</strong></td><td>설계 이력 파일. 설계 및 개발 기록의 전체 모음 (21 CFR 820.30).</td></tr>
<tr><td><strong>DMR</strong></td><td>장치 마스터 레코드. 완제품 기기를 명시하는 문서.</td></tr>
<tr><td><strong>CAPA</strong></td><td>시정 및 예방 조치 (21 CFR 820.90).</td></tr>
<tr><td><strong>V&amp;V</strong></td><td>검증 및 확인. 설계가 입력 사항을 충족하는지(올바르게 구축) 및 사용자 요구를 충족하는지(올바른 것을 구축) 확인.</td></tr>
<tr><td><strong>UDI</strong></td><td>고유 기기 식별. 기기 라벨에 FDA가 요구하는 식별자.</td></tr>
<tr><td><strong>eSTAR</strong></td><td>510(k) 신청을 위한 FDA의 표준화된 전자 제출 형식.</td></tr>
<tr><td><strong>openFDA</strong></td><td>510(k) 허가, 이상사례 및 리콜에 대한 검색 가능한 접근을 제공하는 FDA의 공개 API.</td></tr>
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

  const docLang = document.documentElement.lang;
  const isCN =
    docLang === "zh" || docLang === "zh-CN" || docLang.startsWith("zh");
  const isKO = docLang === "ko";

  const guideTitle = isKO ? "사용자 가이드" : isCN ? "用户指南" : "User Guide";
  const searchPlaceholder = isKO
    ? "가이드 검색..."
    : isCN
      ? "搜索指南..."
      : "Search guide...";
  const closeLabel = isKO ? "닫기" : isCN ? "关闭" : "Close";

  overlay.innerHTML = `
  <div class="help-backdrop" id="helpBackdrop"></div>
  <div class="help-panel">
    <div class="help-header">
      <h2>📖 ${guideTitle}</h2>
      <div class="help-search-wrap">
        <input type="text" id="helpSearch" class="help-search" placeholder="${searchPlaceholder}" />
      </div>
      <button class="help-close" id="helpClose">${closeLabel}</button>
    </div>
    <div class="help-body">
      <nav class="help-toc" id="helpToc">
        ${GUIDE.map(
          (s) =>
            `<a class="help-toc-item ${s.num === helpSection ? "active" : ""}" data-sec="${s.num}">${s.num}. ${localizedText(s.title)}</a>`,
        ).join("")}
      </nav>
      <article class="help-content" id="helpContent">
        ${renderSection(helpSection)}
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
      content.innerHTML = renderSection(helpSection);
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

    const matchLabel = isKO
      ? "개 매칭 섹션"
      : isCN
        ? "个匹配章节"
        : "matching section(s)";
    const noMatchLabel = isKO
      ? "일치하는 결과 없음"
      : isCN
        ? "未找到匹配项"
        : "No matches found";

    content.innerHTML = results.length
      ? `<div class="help-search-count">${results.length} ${matchLabel}</div>${results.join("")}`
      : `<div class="help-search-empty">${noMatchLabel}</div>`;

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

function renderSection(num: number): string {
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
