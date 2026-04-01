(function(){const t=document.createElement("link").relList;if(t&&t.supports&&t.supports("modulepreload"))return;for(const c of document.querySelectorAll('link[rel="modulepreload"]'))a(c);new MutationObserver(c=>{for(const i of c)if(i.type==="childList")for(const l of i.addedNodes)l.tagName==="LINK"&&l.rel==="modulepreload"&&a(l)}).observe(document,{childList:!0,subtree:!0});function n(c){const i={};return c.integrity&&(i.integrity=c.integrity),c.referrerPolicy&&(i.referrerPolicy=c.referrerPolicy),c.crossOrigin==="use-credentials"?i.credentials="include":c.crossOrigin==="anonymous"?i.credentials="omit":i.credentials="same-origin",i}function a(c){if(c.ep)return;c.ep=!0;const i=n(c);fetch(c.href,i)}})();const q="https://api.fda.gov/device/510k.json";function le(e){const t=[],n=e.query.trim();if(!n)return"";switch(e.field){case"product_code":t.push(`product_code:"${n.toUpperCase()}"`);break;case"applicant":t.push(`applicant:"${n}"`);break;case"device_name":t.push(`device_name:"${n}"`);break;case"knumber":t.push(`k_number:"${n.toUpperCase()}"`);break;default:t.push(`(device_name:"${n}"+applicant:"${n}"+product_code:"${n.toUpperCase()}"+k_number:"${n.toUpperCase()}")`)}if(e.yearFrom||e.yearTo){const a=e.yearFrom?`${e.yearFrom}0101`:"19760101",c=e.yearTo?`${e.yearTo}1231`:"20261231";t.push(`decision_date:[${a}+TO+${c}]`)}return e.decision&&t.push(`decision_code:"${e.decision}"`),e.reviewType&&t.push(`clearance_type:"${e.reviewType}"`),t.join("+AND+")}async function de(e){const t=le(e);if(!t)throw new Error("Empty search query");const n=`${q}?search=${t}&sort=decision_date:desc&skip=${e.skip}&limit=${e.limit}`,a=await fetch(n);if(!a.ok){if(a.status===404)return{meta:{disclaimer:"",terms:"",license:"",last_updated:"",results:{skip:0,limit:e.limit,total:0}},results:[]};throw new Error(`FDA API returned ${a.status}`)}return a.json()}async function A(e){const t=e.trim().toUpperCase(),n=`${q}?search=k_number:"${t}"&limit=1`,a=await fetch(n);if(!a.ok)return null;const c=await a.json();return c.results.length>0?c.results[0]:null}async function te(e){var i;if(e.predicate_devices&&e.predicate_devices.length>0){const l=[];for(const u of e.predicate_devices){const R=await A(u.k_number);R&&l.push(R)}return l}const t=(i=e.decision_date)==null?void 0:i.replace(/-/g,"");if(!t||!e.product_code)return[];const n=`${q}?search=product_code:"${e.product_code}"+AND+decision_code:"SESE"+AND+decision_date:[19760101+TO+${t}]&sort=decision_date:desc&limit=5`,a=await fetch(n);return a.ok?(await a.json()).results.filter(l=>l.k_number!==e.k_number):[]}async function pe(e,t=5){const n=[];let a=e;for(let c=0;c<t;c++){const i=await A(a);if(!i)break;n.push(i);const l=await te(i);if(l.length===0||(a=l[0].k_number,n.some(u=>u.k_number===a)))break}return n}const N={appTitle:{en:"510(k) Predicate Finder",cn:"510(k) 先导器械查找器"},searchTitle:{en:"Find Your Predicate Device",cn:"查找您的先导器械"},searchDesc:{en:"Search FDA's 510(k) database by product code, applicant, device name, or K-number.",cn:"按产品代码、申请人、器械名称或K编号搜索FDA 510(k)数据库。"},searchBtn:{en:"Search",cn:"搜索"},fieldAll:{en:"All Fields",cn:"所有字段"},filterYear:{en:"Year Range:",cn:"年份范围："},filterDecision:{en:"Decision:",cn:"决定："},filterType:{en:"Review Type:",cn:"审查类型："},results:{en:"Results",cn:"结果"},compareSelected:{en:"Compare Selected",cn:"对比选中项"},comparison:{en:"Device Comparison",cn:"器械对比"},closeCompare:{en:"✕ Close",cn:"✕ 关闭"},predicateChain:{en:"Predicate Chain",cn:"先导链"},chainDesc:{en:"Trace the predicate lineage backward from any cleared device.",cn:"从任意已通过器械向前追溯先导谱系。"},seGenerator:{en:"Substantial Equivalence Argument Draft",cn:"实质性等同论证草稿"},copySE:{en:"Copy to Clipboard",cn:"复制到剪贴板"},exportSE:{en:"Export as PDF",cn:"导出PDF"},colKNumber:{en:"K-Number",cn:"K编号"},colDevice:{en:"Device Name",cn:"器械名称"},colApplicant:{en:"Applicant",cn:"申请人"},colProductCode:{en:"Product Code",cn:"产品代码"},colDecision:{en:"Decision",cn:"决定"},colDate:{en:"Decision Date",cn:"决定日期"},colType:{en:"Type",cn:"类型"},noResults:{en:"No results found. Try a different search term.",cn:"未找到结果。请尝试其他搜索词。"},searching:{en:"Searching FDA database...",cn:"正在搜索FDA数据库..."},errorApi:{en:"FDA API error. Please try again.",cn:"FDA API错误，请重试。"},deviceDetail:{en:"Device Detail",cn:"器械详情"},reviewPanel:{en:"Review Panel",cn:"审查委员会"},dateReceived:{en:"Date Received",cn:"接收日期"},summaryType:{en:"Summary/Statement",cn:"概要/声明"},thirdParty:{en:"Third Party Review",cn:"第三方审查"},expedited:{en:"Expedited Review",cn:"加速审查"},advisory:{en:"Advisory Committee",cn:"咨询委员会"},predicates:{en:"Referenced Predicates",cn:"引用先导器械"},traceChain:{en:"Trace Predicate Chain",cn:"追溯先导链"},generateSE:{en:"Generate SE Argument",cn:"生成SE论证"},ofTotal:{en:"of",cn:"共"},page:{en:"Page",cn:"页"},prev:{en:"← Prev",cn:"← 上页"},next:{en:"Next →",cn:"下页 →"},selectForCompare:{en:"Select 2–4 devices to compare",cn:"选择2-4个器械进行对比"},seIntro:{en:"Substantial Equivalence Comparison",cn:"实质性等同比较"},seSubject:{en:"Subject Device",cn:"目标器械"},sePredicate:{en:"Predicate Device",cn:"先导器械"},seConclusion:{en:"Based on the comparison above, the subject device shares the same intended use, technological characteristics, and product classification as the predicate device.",cn:"基于以上对比，目标器械与先导器械具有相同的预期用途、技术特征和产品分类。"},gateTitle:{en:"Unlock Premium Features",cn:"解锁高级功能"},gateSubmit:{en:"Unlock Free — No Credit Card",cn:"免费解锁 — 无需信用卡"},gateFooter:{en:"We'll send you the 510(k) Pathway Guide + PMP Course link.",cn:"我们将向您发送510(k)通路指南 + PMP课程链接。"}};let w="en";function ne(e){w=e,document.querySelectorAll("[data-i18n]").forEach(t=>{const n=t.dataset.i18n;N[n]&&(t.textContent=N[n][w])}),document.documentElement.lang=e==="cn"?"zh-CN":"en"}function s(e){var t;return((t=N[e])==null?void 0:t[w])??e}function G(){return w}function ue(){ne(w==="en"?"cn":"en")}const ae="pf_gate",P=5,me=1,ye=2,fe=4;function y(){return new Date().toISOString().slice(0,10)}function x(){try{const e=localStorage.getItem(ae);if(e)return JSON.parse(e)}catch{}return{email:null,tier:"free",searches:{date:y(),count:0},chains:{date:y(),count:0}}}function H(e){localStorage.setItem(ae,JSON.stringify(e))}function b(){return x().tier==="pro"}function ge(){if(b())return!0;const e=x();return e.searches.date!==y()?!0:e.searches.count<P}function he(){const e=x();e.searches.date!==y()?e.searches={date:y(),count:1}:e.searches.count++,H(e),U()}function ve(){if(b())return!0;const e=x();return e.chains.date!==y()?!0:e.chains.count<me}function xe(){const e=x();e.chains.date!==y()?e.chains={date:y(),count:1}:e.chains.count++,H(e)}function K(){return b()?fe:ye}function $e(e){const t=x();t.email=e,t.tier="pro",H(t),M(),U()}let p=null,$=null,C=null;function be(){p=document.getElementById("gateModal"),$=document.getElementById("tierBadge");const e=document.getElementById("gateForm"),t=document.getElementById("gateEmail");e==null||e.addEventListener("submit",a=>{a.preventDefault();const c=t==null?void 0:t.value.trim();c&&($e(c),C&&(C(),C=null))});const n=document.getElementById("closeGateModal");n==null||n.addEventListener("click",M),p==null||p.addEventListener("click",a=>{a.target===p&&M()}),U()}function I(e,t){var a;if(!p)return;C=t??null;const n=document.getElementById("gateFeatureDesc");if(n){const c=G(),l=((a={search:{en:"unlimited searches",cn:"无限搜索"},chain:{en:"unlimited predicate chain tracing",cn:"无限先导链追溯"},compare:{en:"compare up to 4 devices",cn:"对比最多4个器械"},se:{en:"SE argument generation",cn:"SE论证生成"},pdf:{en:"PDF export",cn:"PDF导出"}}[e])==null?void 0:a[c])??e;n.textContent=c==="cn"?`输入您的邮箱即可解锁 ${l} 等高级功能。`:`Enter your email to unlock ${l} and all premium features.`}p.classList.remove("hidden")}function M(){p==null||p.classList.add("hidden")}function U(){if($)if(b())$.textContent="PRO",$.className="text-xs px-2 py-0.5 rounded-full bg-emerald-600 text-white font-semibold";else{const e=x(),t=e.searches.date===y()?Math.max(0,P-e.searches.count):P;$.textContent=`FREE (${t}/${P})`,$.className="text-xs px-2 py-0.5 rounded-full bg-gray-700 text-gray-300 font-semibold"}}const o=e=>document.getElementById(e),B=o("searchInput"),_e=o("searchField"),ke=o("searchBtn"),z=o("yearFrom"),V=o("yearTo"),we=o("decisionFilter"),Ee=o("typeFilter"),se=o("statusBar"),Se=o("statusText"),J=o("resultsSection"),_=o("resultsBody"),Q=o("resultCount"),T=o("compareBtn"),O=o("compareSection"),W=o("compareGrid"),Pe=o("closeCompare"),Z=o("chainSection"),Ce=o("chainViz"),X=o("seSection"),ce=o("seContent"),k=o("pagination"),h=o("detailModal"),Te=o("detailTitle"),De=o("detailContent"),Ae=o("closeDetail"),Le=o("langToggle"),ee=o("selectAll"),Fe=o("copySeBtn");let v=[],E=0,L=0;const g=25,d=new Set;function f(e){e.classList.remove("hidden")}function m(e){e.classList.add("hidden")}function F(e){Se.textContent=e,f(se)}function Y(){m(se)}function S(e){return`<span class="${e==="SESE"||e==="SESP"||e==="SEST"?"badge-se":e==="NSE"?"badge-nse":"badge-pend"} text-xs px-2 py-0.5 rounded-full">${e}</span>`}function r(e){return e?e.replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;"):""}async function D(e=0){const t={query:B.value.trim(),field:_e.value,yearFrom:z.value?parseInt(z.value):void 0,yearTo:V.value?parseInt(V.value):void 0,decision:we.value||void 0,reviewType:Ee.value||void 0,skip:e,limit:g};if(!t.query){B.focus();return}if(!ge()){I("search",()=>D(e));return}F(s("searching")),d.clear(),j();try{const n=await de(t);v=n.results,E=n.meta.results.total,L=e,he(),re(),Y()}catch{F(s("errorApi"))}}function re(){if(v.length===0){_.innerHTML=`<tr><td colspan="8" class="px-4 py-8 text-center text-gray-500">${r(s("noResults"))}</td></tr>`,Q.textContent="(0)",m(k),f(J);return}Q.textContent=`(${L+1}–${Math.min(L+g,E)} ${s("ofTotal")} ${E.toLocaleString()})`,_.innerHTML=v.map(e=>`
      <tr data-k="${r(e.k_number)}">
        <td class="px-3 py-2"><input type="checkbox" class="row-check accent-blue-500" value="${r(e.k_number)}" ${d.has(e.k_number)?"checked":""} /></td>
        <td class="px-3 py-2 font-mono text-blue-400 whitespace-nowrap">${r(e.k_number)}</td>
        <td class="px-3 py-2 max-w-xs truncate">${r(e.device_name)}</td>
        <td class="px-3 py-2 max-w-[180px] truncate">${r(e.applicant)}</td>
        <td class="px-3 py-2 font-mono">${r(e.product_code)}</td>
        <td class="px-3 py-2">${S(e.decision_code)}</td>
        <td class="px-3 py-2 whitespace-nowrap">${r(e.decision_date)}</td>
        <td class="px-3 py-2">${r(e.clearance_type)}</td>
      </tr>`).join(""),Ie(),f(J)}function Ie(){if(E<=g){m(k);return}const e=Math.ceil(E/g),t=Math.floor(L/g)+1;let n="";t>1&&(n+=`<button class="page-btn px-3 py-1 rounded bg-gray-800 hover:bg-gray-700" data-skip="${(t-2)*g}">${s("prev")}</button>`),n+=`<span class="text-gray-500">${s("page")} ${t} / ${e}</span>`,t<e&&(n+=`<button class="page-btn px-3 py-1 rounded bg-gray-800 hover:bg-gray-700" data-skip="${t*g}">${s("next")}</button>`),k.innerHTML=n,f(k)}async function Re(e){Te.textContent=`${e.k_number} — ${e.device_name}`;const t=await te(e);De.innerHTML=`
    <div class="grid grid-cols-2 gap-3 text-sm mb-6">
      <div><span class="text-gray-500">${s("colApplicant")}:</span> ${r(e.applicant)}</div>
      <div><span class="text-gray-500">${s("colProductCode")}:</span> <span class="font-mono">${r(e.product_code)}</span></div>
      <div><span class="text-gray-500">${s("colDecision")}:</span> ${S(e.decision_code)} ${r(e.decision_description)}</div>
      <div><span class="text-gray-500">${s("colDate")}:</span> ${r(e.decision_date)}</div>
      <div><span class="text-gray-500">${s("dateReceived")}:</span> ${r(e.date_received)}</div>
      <div><span class="text-gray-500">${s("colType")}:</span> ${r(e.clearance_type)}</div>
      <div><span class="text-gray-500">${s("reviewPanel")}:</span> ${r(e.review_panel)}</div>
      <div><span class="text-gray-500">${s("summaryType")}:</span> ${r(e.statement_or_summary)}</div>
      <div><span class="text-gray-500">${s("thirdParty")}:</span> ${e.third_party_flag==="Y"?"Yes":"No"}</div>
      <div><span class="text-gray-500">${s("expedited")}:</span> ${e.expedited_review_flag==="Y"?"Yes":"No"}</div>
      <div class="col-span-2"><span class="text-gray-500">${s("advisory")}:</span> ${r(e.advisory_committee_description)}</div>
    </div>

    ${t.length>0?`
      <h4 class="text-sm font-semibold mb-2 text-gray-300">${s("predicates")}</h4>
      <div class="space-y-2 mb-4">
        ${t.map(n=>`
          <div class="bg-gray-800 rounded-lg p-3 text-xs flex items-center justify-between">
            <div>
              <span class="font-mono text-blue-400">${r(n.k_number)}</span>
              <span class="mx-2 text-gray-600">|</span>
              <span>${r(n.device_name)}</span>
              <span class="mx-2 text-gray-600">|</span>
              <span class="text-gray-400">${r(n.applicant)}</span>
            </div>
            <span class="text-gray-500">${r(n.decision_date)}</span>
          </div>`).join("")}
      </div>`:""}

    <div class="flex gap-3 mt-4">
      <button class="bg-blue-600 hover:bg-blue-500 text-white text-xs px-4 py-2 rounded-lg transition" onclick="window._traceChain('${e.k_number}')">${s("traceChain")}</button>
      ${t.length>0?`<button class="bg-emerald-600 hover:bg-emerald-500 text-white text-xs px-4 py-2 rounded-lg transition" onclick="window._generateSE('${e.k_number}','${t[0].k_number}')">${s("generateSE")}</button>`:""}
    </div>
  `,f(h)}async function ie(e){if(!ve()){I("chain",()=>ie(e));return}m(h),F(s("searching"));const t=await pe(e);xe(),Y(),t.length!==0&&(Ce.innerHTML=`
    <div class="flex items-center overflow-x-auto gap-1 py-2">
      ${t.map((n,a)=>`
        <div class="chain-node ${a===0?"active":""} flex-shrink-0">
          <div class="font-mono text-blue-400 font-semibold">${r(n.k_number)}</div>
          <div class="text-gray-300 mt-1 truncate max-w-[160px]">${r(n.device_name)}</div>
          <div class="text-gray-500 mt-1">${r(n.applicant)}</div>
          <div class="text-gray-600 mt-1">${r(n.decision_date)}</div>
          <div class="mt-1">${S(n.decision_code)}</div>
        </div>
        ${a<t.length-1?'<div class="chain-arrow flex-shrink-0">→</div>':""}
      `).join("")}
    </div>
    <p class="text-xs text-gray-600 mt-3">${t.length} ${G()==="cn"?"个器械在先导链中":"devices in predicate chain"}</p>
  `,f(Z),Z.scrollIntoView({behavior:"smooth"}))}function j(){d.size>=2?(T.textContent=`${s("compareSelected")} (${d.size})`,f(T)):m(T)}function Ne(){const e=v.filter(c=>d.has(c.k_number));if(e.length<2)return;const t=[{key:"product_code",label:s("colProductCode")},{key:"review_panel",label:s("reviewPanel")},{key:"clearance_type",label:s("colType")},{key:"decision_code",label:s("colDecision")},{key:"advisory_committee_description",label:s("advisory")},{key:"third_party_flag",label:s("thirdParty")},{key:"statement_or_summary",label:s("summaryType")}],n=e.length;W.style.gridTemplateColumns=`180px repeat(${n}, 1fr)`;let a="";a+='<div class="text-xs text-gray-500 uppercase tracking-wider py-2 font-semibold"></div>';for(const c of e)a+=`<div class="compare-card">
      <div class="font-mono text-blue-400 font-semibold">${r(c.k_number)}</div>
      <div class="text-sm text-gray-200 truncate mt-1">${r(c.device_name)}</div>
      <div class="text-xs text-gray-500 mt-1">${r(c.applicant)}</div>
    </div>`;for(const c of t){a+=`<div class="text-xs text-gray-500 py-2 flex items-center">${c.label}</div>`;const i=e.map(u=>String(u[c.key]??"")),l=i.every(u=>u===i[0]);for(const u of i)a+=`<div class="compare-card"><span class="${l?"compare-match":"compare-differ"} text-sm">${r(u)}</span></div>`}W.innerHTML=a,f(O),O.scrollIntoView({behavior:"smooth"})}async function oe(e,t){if(!b()){I("se",()=>oe(e,t));return}m(h),F(s("searching"));const[n,a]=await Promise.all([A(e),A(t)]);if(Y(),!n||!a)return;const c=G(),i=n.product_code===a.product_code,l=n.review_panel===a.review_panel;ce.innerHTML=`
    <h4 class="text-base font-bold mb-4">${s("seIntro")}</h4>

    <div class="grid grid-cols-2 gap-6 mb-6">
      <div>
        <h5 class="text-sm font-semibold text-blue-400 mb-2">${s("seSubject")}</h5>
        <div class="space-y-1 text-sm">
          <div><span class="text-gray-500">K-Number:</span> ${r(n.k_number)}</div>
          <div><span class="text-gray-500">${s("colDevice")}:</span> ${r(n.device_name)}</div>
          <div><span class="text-gray-500">${s("colApplicant")}:</span> ${r(n.applicant)}</div>
          <div><span class="text-gray-500">${s("colProductCode")}:</span> <span class="font-mono">${r(n.product_code)}</span></div>
          <div><span class="text-gray-500">${s("reviewPanel")}:</span> ${r(n.review_panel)}</div>
        </div>
      </div>
      <div>
        <h5 class="text-sm font-semibold text-emerald-400 mb-2">${s("sePredicate")}</h5>
        <div class="space-y-1 text-sm">
          <div><span class="text-gray-500">K-Number:</span> ${r(a.k_number)}</div>
          <div><span class="text-gray-500">${s("colDevice")}:</span> ${r(a.device_name)}</div>
          <div><span class="text-gray-500">${s("colApplicant")}:</span> ${r(a.applicant)}</div>
          <div><span class="text-gray-500">${s("colProductCode")}:</span> <span class="font-mono">${r(a.product_code)}</span></div>
          <div><span class="text-gray-500">${s("reviewPanel")}:</span> ${r(a.review_panel)}</div>
        </div>
      </div>
    </div>

    <h5 class="text-sm font-semibold mb-2">${c==="cn"?"对比分析":"Comparison Analysis"}</h5>
    <table class="w-full text-sm border border-gray-800 rounded mb-6">
      <thead class="bg-gray-800 text-gray-400 text-xs">
        <tr>
          <th class="px-3 py-2 text-left">${c==="cn"?"特征":"Characteristic"}</th>
          <th class="px-3 py-2 text-left">${s("seSubject")}</th>
          <th class="px-3 py-2 text-left">${s("sePredicate")}</th>
          <th class="px-3 py-2 text-left">${c==="cn"?"匹配":"Match"}</th>
        </tr>
      </thead>
      <tbody class="divide-y divide-gray-800">
        <tr>
          <td class="px-3 py-2 text-gray-400">${s("colProductCode")}</td>
          <td class="px-3 py-2 font-mono">${r(n.product_code)}</td>
          <td class="px-3 py-2 font-mono">${r(a.product_code)}</td>
          <td class="px-3 py-2">${i?'<span class="text-emerald-400">✓</span>':'<span class="text-amber-400">✗</span>'}</td>
        </tr>
        <tr>
          <td class="px-3 py-2 text-gray-400">${s("reviewPanel")}</td>
          <td class="px-3 py-2">${r(n.review_panel)}</td>
          <td class="px-3 py-2">${r(a.review_panel)}</td>
          <td class="px-3 py-2">${l?'<span class="text-emerald-400">✓</span>':'<span class="text-amber-400">✗</span>'}</td>
        </tr>
        <tr>
          <td class="px-3 py-2 text-gray-400">${s("colType")}</td>
          <td class="px-3 py-2">${r(n.clearance_type)}</td>
          <td class="px-3 py-2">${r(a.clearance_type)}</td>
          <td class="px-3 py-2">${n.clearance_type===a.clearance_type?'<span class="text-emerald-400">✓</span>':'<span class="text-gray-500">—</span>'}</td>
        </tr>
        <tr>
          <td class="px-3 py-2 text-gray-400">${s("colDecision")}</td>
          <td class="px-3 py-2">${S(n.decision_code)}</td>
          <td class="px-3 py-2">${S(a.decision_code)}</td>
          <td class="px-3 py-2"></td>
        </tr>
      </tbody>
    </table>

    <div class="bg-gray-800/50 rounded-lg p-4 border border-gray-700">
      <h5 class="text-sm font-semibold mb-2">${c==="cn"?"初步结论":"Preliminary Conclusion"}</h5>
      <p class="text-sm text-gray-300">${s("seConclusion")}</p>
      ${i?"":`<p class="text-sm text-amber-400 mt-2">${c==="cn"?"⚠ 产品代码不同——需要额外论证来证明相同的预期用途和技术特征。":"⚠ Product codes differ — additional argumentation needed to demonstrate same intended use and technological characteristics."}</p>`}
    </div>
  `,f(X),X.scrollIntoView({behavior:"smooth"})}function Me(){ne("en"),be(),ke.addEventListener("click",()=>D(0)),B.addEventListener("keydown",e=>{e.key==="Enter"&&D(0)}),Le.addEventListener("click",()=>{ue(),v.length&&re()}),_.addEventListener("click",e=>{const t=e.target;if(t.tagName==="INPUT")return;const n=t.closest("tr");if(!n)return;const a=n.dataset.k,c=v.find(i=>i.k_number===a);c&&Re(c)}),_.addEventListener("change",e=>{const t=e.target;if(t.classList.contains("row-check")){if(t.checked){if(d.size>=K()){b()||I("compare"),t.checked=!1;return}d.add(t.value)}else d.delete(t.value);j()}}),ee.addEventListener("change",()=>{d.clear(),ee.checked&&v.slice(0,K()).forEach(e=>d.add(e.k_number)),_.querySelectorAll(".row-check").forEach(e=>{e.checked=d.has(e.value)}),j()}),T.addEventListener("click",Ne),Pe.addEventListener("click",()=>m(O)),k.addEventListener("click",e=>{const t=e.target.closest(".page-btn");t&&D(parseInt(t.dataset.skip??"0"))}),Ae.addEventListener("click",()=>m(h)),h.addEventListener("click",e=>{e.target===h&&m(h)}),Fe.addEventListener("click",()=>{const e=ce.innerText;navigator.clipboard.writeText(e)}),window._traceChain=ie,window._generateSE=oe}Me();
