// ============================================================
// DATA MODEL — TiO2 Medical Air Purification System
// Based on FDA 510(k) Submission (Product Code FRA)
// PMP is overriding authority; accepts input from biz & tech
// ============================================================

import type {
  Project,
  Tracks,
  Gate,
  Risk,
  Standard,
  TimelineEvent,
  StakeholderInput,
  CashRunway,
  ChangeRequest,
  UserRole,
  AuditEntry,
  DHFDocument,
  CAPAItem,
  ActionItem,
  BudgetCategory,
  TeamMember,
  Supplier,
  QASection,
} from "./types.ts";

export const PROJECT: Project = {
  name: {
    en: "TiO2 Medical Air Purification System",
    cn: "TiO2医用空气净化系统",
  },
  subtitle: {
    en: "UV-C Photocatalytic Reactor + HEPA + Activated Carbon Platform",
    cn: "UV-C光催化反应器 + HEPA + 活性炭平台",
  },
  submissionType: "510(k) Standard — Class II (§ 880.6500, Product Code FRA)",
  applicant: {
    en: "Titania Labs, LLC",
    cn: "Titania Labs有限责任公司",
  },
  manufacturer: {
    en: "Titania Labs, LLC (Gresham, OR)",
    cn: "Titania Labs有限责任公司（俄勒冈州格雷舍姆）",
  },
  preparedDate: "March 2026",
  currentMonth: 0,
};

// ============================================================
// DUAL-TRACK: Technical + Regulatory milestones
// ============================================================

export const TRACKS: Tracks = {
  technical: {
    label: { en: "Technical Track", cn: "技术路径" },
    icon: "🔬",
    milestones: [
      {
        id: "T1",
        month: 0,
        title: {
          en: "UV-C Reactor Prototype Finalization",
          cn: "UV-C反应器原型定型",
        },
        description: {
          en: "2½-inch fluorescent UV-C lamp (254 nm), TiO2 nanocoating, activated carbon chamber, fan assembly",
          cn: "2½英寸荧光UV-C灯（254nm），TiO2纳米涂层，活性炭反应室，风扇组件",
        },
        detail: {
          en: "The UV-C Reactor is the core technology of the TiO2 Air Cleaner. This milestone locks the production-intent design:\n\n- UV-C Lamp: 2½-inch fluorescent tube operating at 254 nm wavelength — the optimal germicidal range. The lamp is coated with a nano-thin layer of titanium dioxide (TiO2).\n- Photocatalytic Mechanism: When UV light energizes the TiO2 crystal, an energy band gap is created that pulls hydrogen atoms off H2O molecules in ambient humidity, producing hydroxyl radicals (OH⁻) — the strongest non-poisonous oxidizing agent in nature.\n- Activated Carbon Chamber: The lamp is enclosed in an activated carbon chamber derived from coconut shells. As air passes through, the carbon adsorbs volatile organic compounds (VOCs), formaldehyde, and chemical gases.\n- Fan Assembly: A variable-speed fan draws ambient air through an input pre-filter, past the reactor chamber, and exhausts purified air into the room.\n- Kill Mechanism: Hydroxyl radicals break carbon-hydrogen bonds in organic compounds (bacteria, mold, viruses), decomposing them safely into H2O and CO2 in nanoseconds. TiO2 acts as a catalyst — it is not consumed in the reaction.\n\nCompletion of T1 means the reactor assembly, housing, fan motor, and electrical circuitry are frozen for performance testing (T4).",
          cn: "UV-C反应器是TiO2空气净化器的核心技术。此里程碑锁定生产级设计：\n\n- UV-C灯：2½英寸荧光管工作在254nm波长——最佳杀菌范围。灯管涂覆纳米级二氧化钛（TiO2）涂层。\n- 光催化机制：当紫外线激发TiO2晶体时，产生能带间隙，从空气湿度中的H2O分子拉出氢原子，生成羟基自由基（OH⁻）——自然界中最强的无毒氧化剂。\n- 活性炭反应室：灯管封装在由椰壳制成的活性炭室中。空气通过时，活性炭吸附挥发性有机化合物（VOCs）、甲醛和化学气体。\n- 风扇组件：变速风扇将环境空气通过输入预过滤器、反应室，然后将净化空气排入室内。\n- 杀灭机制：羟基自由基断裂有机化合物（细菌、霉菌、病毒）中的碳氢键，在纳秒内安全分解为H2O和CO2。TiO2作为催化剂——不在反应中消耗。\n\n完成T1意味着反应器组件、外壳、风扇电机和电气电路已冻结，可进入性能测试（T4）。",
        },
        status: "complete",
        owner: "tech",
        category: "prototype",
      },
      {
        id: "T2",
        month: 1,
        title: {
          en: "TiO2 Photocatalytic Efficiency Validation",
          cn: "TiO2光催化效率验证",
        },
        description: {
          en: "Hydroxyl radical generation rate, TiO2 coating uniformity, UV-C intensity at reactor surface ≥40 µW/cm²",
          cn: "羟基自由基生成速率，TiO2涂层均匀性，反应器表面UV-C强度≥40 µW/cm²",
        },
        detail: {
          en: "This milestone validates the photocatalytic core — the TiO2-coated UV-C lamp — meets minimum performance thresholds:\n\n- Hydroxyl Radical Generation: Measured using methylene blue degradation assay. The reactor must achieve a minimum degradation rate indicating sufficient radical production for the target air volume.\n- TiO2 Coating Uniformity: Scanning electron microscopy (SEM) verification that the nano-thin TiO2 layer is uniformly deposited on the lamp surface. Non-uniform coating leads to hotspots and dead zones.\n- UV-C Intensity ≥40 µW/cm²: Measured at the inner wall of the activated carbon chamber using a calibrated UV-C radiometer. Below this threshold, photocatalytic activation of TiO2 is insufficient.\n- Lamp Lifetime Testing: Accelerated aging test to verify the UV-C lamp maintains ≥80% output intensity after 8,000 hours of continuous operation.\n- Secondary Reaction: UV-C also produces super-oxide anions (O2*) that react with NOx and SOx, reducing smog-forming pollutants to harmless nitrates and sulfates.\n\nT2 is validated by laboratory testing at an independent environmental testing facility. Results feed directly into the 510(k) performance data package.",
          cn: "此里程碑验证光催化核心——TiO2涂覆UV-C灯——满足最低性能阈值：\n\n- 羟基自由基生成：使用亚甲蓝降解试验测量。反应器必须达到最低降解率，表明目标空气体积的自由基产量充足。\n- TiO2涂层均匀性：扫描电子显微镜（SEM）验证纳米级TiO2层在灯管表面均匀沉积。不均匀涂层导致热点和死区。\n- UV-C强度≥40 µW/cm²：使用校准UV-C辐射计在活性炭室内壁测量。低于此阈值，TiO2的光催化激活不充分。\n- 灯管寿命测试：加速老化测试验证UV-C灯在8000小时连续运行后保持≥80%输出强度。\n- 次级反应：UV-C还产生超氧阴离子（O2*），与NOx和SOx反应，将形成烟雾的污染物还原为无害的硝酸盐和硫酸盐。\n\nT2由独立环境测试机构的实验室测试验证。结果直接纳入510(k)性能数据包。",
        },
        status: "in-progress",
        owner: "tech",
        category: "validation",
      },
      {
        id: "T3",
        month: 2,
        title: {
          en: "HEPA & Activated Carbon Filtration Integration",
          cn: "HEPA与活性炭过滤集成",
        },
        description: {
          en: "HEPA filter (99.97% @ 0.3µm), coconut-shell activated carbon, pre-filter, filter housing sealed assembly",
          cn: "HEPA过滤器（99.97% @ 0.3µm），椰壳活性炭，预过滤器，过滤器外壳密封组装",
        },
        detail: {
          en: "The TiO2 reactor handles gaseous contaminants and biological organisms, but particulate matter requires mechanical filtration. This milestone integrates the multi-stage filtration system:\n\n- HEPA Filter: True HEPA rated per DOE standards — removes 99.97% of airborne particles ≥0.3 µm. This captures PM2.5, pollen, dust mites, and aerosolized droplets.\n- Activated Carbon Filter: Coconut-shell derived, oxygen-treated to maximize porosity. Adsorbs formaldehyde, benzene, toluene, and hundreds of other VOCs via chemical bonding to the porous carbon surface.\n- Pre-Filter: Washable mesh pre-filter captures large particles (hair, lint, pet dander) to extend HEPA filter life.\n- Sealed Assembly: The filter stack must be sealed against bypass leakage — unfiltered air must not shortcut around the HEPA element. Gasket design and pressure drop testing verify seal integrity.\n- Filter Change Indicator: Electronic sensor monitors differential pressure across the filter stack. When pressure drop exceeds threshold (indicating clogging), a LED indicator alerts the user to replace filters.\n\nT3 completion means the complete three-stage filtration stack (pre-filter → activated carbon → HEPA) is integrated with the UV-C reactor module and ready for airflow performance testing (T4).",
          cn: "TiO2反应器处理气态污染物和生物有机体，但颗粒物需要机械过滤。此里程碑集成多级过滤系统：\n\n- HEPA过滤器：按DOE标准的真正HEPA级别——去除99.97%的≥0.3µm空气颗粒。捕获PM2.5、花粉、尘螨和气溶胶飞沫。\n- 活性炭过滤器：椰壳来源，氧处理以最大化孔隙率。通过化学键合到多孔碳表面吸附甲醛、苯、甲苯和数百种其他VOCs。\n- 预过滤器：可清洗网状预过滤器捕获大颗粒（毛发、纤维、宠物皮屑）以延长HEPA过滤器寿命。\n- 密封组装：过滤器组必须密封防止旁路泄漏——未过滤空气不得绕过HEPA元件。垫圈设计和压降测试验证密封完整性。\n- 滤芯更换指示器：电子传感器监测过滤器组两端的差压。当压降超过阈值（表示堵塞）时，LED指示灯提醒用户更换过滤器。\n\n完成T3意味着完整的三级过滤组（预过滤器→活性炭→HEPA）已与UV-C反应器模块集成，可进行气流性能测试（T4）。",
        },
        status: "in-progress",
        owner: "tech",
        category: "integration",
      },
      {
        id: "T4",
        month: 3,
        title: {
          en: "Airflow & CFM Performance Testing",
          cn: "气流与CFM性能测试",
        },
        description: {
          en: "Clean Air Delivery Rate (CADR) measurement, airflow CFM at each speed, noise level (dBA), power consumption",
          cn: "洁净空气输出率（CADR）测量，各速度下气流CFM，噪声水平（dBA），功耗",
        },
        detail: {
          en: "Airflow performance determines the device's practical effectiveness in real-world room sizes. This milestone quantifies all key aerodynamic parameters:\n\n- CADR (Clean Air Delivery Rate): Tested per ANSI/AHAM AC-1 standard in a sealed 1,008 ft³ test chamber. CADR is measured separately for smoke, dust, and pollen particles. Target: CADR ≥100 CFM for rooms up to 200 sq ft.\n- CFM at Each Speed: The variable-speed fan has 3 settings (Low, Medium, High). Airflow measured with a calibrated anemometer at the outlet. Target: Low 80 CFM, Med 150 CFM, High 250 CFM.\n- Noise Level: Sound pressure measurement per IEC 60704 at 1 meter distance. Target: Low ≤35 dBA (whisper quiet), High ≤55 dBA (normal conversation).\n- Power Consumption: Measured at each speed setting. Target: ≤45W at high speed. Energy Star certification considered for marketing advantage.\n- Pressure Drop: Static pressure across the complete filter stack + reactor. Must not exceed fan capability at minimum speed or the device cannot maintain adequate airflow with loaded filters.\n\nCADR testing is performed at an AHAM-certified laboratory. Results are printed on the device packaging per FTC labeling requirements.",
          cn: "气流性能决定设备在实际房间尺寸中的实用效果。此里程碑量化所有关键空气动力学参数：\n\n- CADR（洁净空气输出率）：按ANSI/AHAM AC-1标准在密封1008立方英尺测试室中测试。CADR分别测量烟雾、灰尘和花粉颗粒。目标：CADR≥100 CFM，适用于200平方英尺以下房间。\n- 各速度CFM：变速风扇有3档设置（低、中、高）。使用校准风速计在出口测量气流。目标：低档80 CFM，中档150 CFM，高档250 CFM。\n- 噪声水平：按IEC 60704在1米距离处测量声压。目标：低档≤35 dBA（耳语安静），高档≤55 dBA（正常对话）。\n- 功耗：在各速度设置下测量。目标：高速≤45W。考虑Energy Star认证以获得营销优势。\n- 压降：完整过滤器组+反应器的静压。不得超过最低速度下的风扇能力，否则设备在过滤器满载时无法维持足够气流。\n\nCADR测试在AHAM认证实验室进行。结果按FTC标签要求印在设备包装上。",
        },
        status: "not-started",
        owner: "tech",
        category: "testing",
      },
      {
        id: "T5",
        month: 4,
        title: {
          en: "Microbial Kill Rate Testing",
          cn: "微生物杀灭率测试",
        },
        description: {
          en: "Aerosolized bacteria (S. aureus, E. coli) reduction ≥99%, mold spore reduction ≥95%, single-pass kill rate",
          cn: "气溶胶细菌（金黄色葡萄球菌、大肠杆菌）减少≥99%，霉菌孢子减少≥95%，单次通过杀灭率",
        },
        detail: {
          en: "Microbial efficacy testing is the critical performance validation for the 510(k) — this is what makes the device a 'medical' air purifier rather than a consumer appliance:\n\n- Bacterial Reduction: Aerosolized S. aureus and E. coli are introduced into a sealed test chamber. The device operates for defined time intervals and viable colony counts are measured using impaction sampling. Target: ≥99% reduction (2-log) within 60 minutes in a 1,008 ft³ chamber.\n- Mold Spore Reduction: Aspergillus niger spores (highly resistant to UV) are aerosolized. Target: ≥95% reduction, demonstrating that the TiO2 photocatalytic mechanism adds germicidal capability beyond UV-C alone.\n- Single-Pass Efficiency: Air is sampled immediately before and after passing through the reactor+filter assembly in a duct configuration. This measures the device's instantaneous kill/capture rate independent of room mixing.\n- Comparator Benchmark: Results are compared to predicate device published data (AiroCide TiO2 K023830, ABRACAIR K050257) to support substantial equivalence.\n- Independent Lab: All microbial testing is performed at an ISO 17025-accredited microbiology lab (e.g., RTI, Aerobiology Laboratory).\n\nMicrobial kill data is the centerpiece of the 510(k) performance section and the primary evidence for substantial equivalence to the predicate devices.",
          cn: "微生物效能测试是510(k)的关键性能验证——这使设备成为'医用'空气净化器而非消费类家电：\n\n- 细菌减少：将气溶胶化的金黄色葡萄球菌和大肠杆菌引入密封测试室。设备运行规定时间间隔，使用撞击采样测量活菌落计数。目标：在1008立方英尺室内60分钟内减少≥99%（2-log）。\n- 霉菌孢子减少：将黑曲霉孢子（对UV高度耐受）气溶胶化。目标：减少≥95%，证明TiO2光催化机制提供超越单独UV-C的杀菌能力。\n- 单次通过效率：在管道配置中，在空气通过反应器+过滤器组前后立即采样。测量设备的瞬时杀灭/捕获率，独立于房间混合。\n- 对标基准：结果与前置设备公开数据（AiroCide TiO2 K023830, ABRACAIR K050257）比较，支持实质等效性。\n- 独立实验室：所有微生物测试在ISO 17025认证的微生物学实验室进行（如RTI、Aerobiology Laboratory）。\n\n微生物杀灭数据是510(k)性能部分的核心和与前置设备实质等效性的主要证据。",
        },
        status: "not-started",
        owner: "tech",
        category: "validation",
      },
      {
        id: "T6",
        month: 5,
        title: {
          en: "Electrical Safety & UL Testing",
          cn: "电气安全与UL测试",
        },
        description: {
          en: "UL 507 (fans), UL 867 (electrostatic air cleaners), IEC 60335 electrical safety, ground fault, leakage current",
          cn: "UL 507（风扇），UL 867（静电空气净化器），IEC 60335电气安全，接地故障，漏电流",
        },
        detail: {
          en: "Electrical safety testing verifies the device meets UL and IEC standards for consumer/medical electrical equipment operating in inhabited spaces:\n\n- UL 507 (Electric Fans): Fan motor safety — overload protection, thermal cutoff, blade guard clearance, cord strain relief, and grounding continuity.\n- UL 867 (Electrostatic Air Cleaners): Specific to air cleaning devices with electrical discharge elements. Covers high-voltage circuit safety for the UV-C lamp ballast, ozone emission limits, and enclosure temperature rise.\n- IEC 60335-2-65: International standard for air cleaning appliances. Electrical safety, mechanical stability, moisture resistance, and abnormal operation tests.\n- Ground Fault Testing: Leakage current measurement under normal and single-fault conditions. Class II double-insulated design intended to eliminate ground fault risk.\n- UV-C Containment: Verification that no UV-C radiation escapes the sealed reactor chamber during normal operation. UV measurements at all exterior surfaces must be below detectable limits (0.1 µW/cm² at 10 cm).\n- Thermal Testing: Component and enclosure surface temperatures under continuous maximum-speed operation for 7 days. No external surface shall exceed 65°C.\n\nAll electrical safety testing is performed at a Nationally Recognized Testing Laboratory (NRTL) such as Intertek, UL, or CSA. Reports are included in the 510(k) submission.",
          cn: "电气安全测试验证设备满足用于居住空间的消费/医用电气设备的UL和IEC标准：\n\n- UL 507（电风扇）：风扇电机安全——过载保护、热切断、叶片护罩间隙、电线应力释放和接地连续性。\n- UL 867（静电空气净化器）：特定于带有放电元件的空气净化设备。涵盖UV-C灯镇流器的高压电路安全、臭氧排放限值和外壳温升。\n- IEC 60335-2-65：空气净化器具的国际标准。电气安全、机械稳定性、防潮和异常运行测试。\n- 接地故障测试：正常和单一故障条件下的漏电流测量。II类双重绝缘设计旨在消除接地故障风险。\n- UV-C密封验证：验证正常运行期间无UV-C辐射从密封反应器室逸出。所有外部表面的UV测量必须低于可检测限（10cm处0.1 µW/cm²）。\n- 热测试：7天连续最高速运行下的元件和外壳表面温度。任何外部表面不得超过65°C。\n\n所有电气安全测试在国家认可测试实验室（NRTL）进行，如Intertek、UL或CSA。报告纳入510(k)提交。",
        },
        status: "not-started",
        owner: "tech",
        category: "testing",
      },
      {
        id: "T7",
        month: 4,
        title: {
          en: "Ozone Emission Testing",
          cn: "臭氧排放测试",
        },
        description: {
          en: "Ozone output &lt;50 ppb per FDA/EPA limits, UV-C wavelength verification (254nm not 185nm), chamber leak test",
          cn: "臭氧输出 &lt;50 ppb符合FDA/EPA限值，UV-C波长验证（254nm非185nm），反应室泄漏测试",
        },
        detail: {
          en: "Ozone is a critical safety concern for any device using UV-C light. This milestone verifies the TiO2 Air Cleaner meets EPA and FDA ozone limits:\n\n- Ozone Limit: FDA 21 CFR 801.415 requires indoor medical devices generating ozone to produce no more than 0.05 ppm (50 ppb) by volume of ozone. EPA indoor air quality guidelines concur.\n- UV-C Wavelength: The UV-C lamp operates at 254 nm (germicidal UV). A lamp emitting at 185 nm would generate ozone from oxygen (O2 → O3). Spectral analysis confirms the lamp output is 254 nm with no significant 185 nm emission.\n- Ozone Measurement: Continuous ozone monitoring (UV absorption method, 0-100 ppb resolution) in a sealed test chamber during 8-hour continuous operation at maximum fan speed. Samples taken at device outlet and at 1 meter distance.\n- TiO2 Ozone Effect: Photocatalytic TiO2 actually helps decompose ozone (O3 → O2) on the catalyst surface. Testing verifies that ozone levels at the device outlet are LOWER than ambient — a beneficial side effect.\n- Activated Carbon Contribution: The activated carbon stage further adsorbs any trace ozone before exhaust. Carbon breakthrough testing confirms ozone removal capacity over rated filter life.\n\nOzone compliance is a pass/fail gate for FDA clearance. Any reading above 50 ppb requires design changes before submission.",
          cn: "臭氧是使用UV-C光的任何设备的关键安全问题。此里程碑验证TiO2空气净化器满足EPA和FDA臭氧限值：\n\n- 臭氧限值：FDA 21 CFR 801.415要求产生臭氧的室内医疗设备体积臭氧产量不超过0.05 ppm（50 ppb）。EPA室内空气质量指南一致。\n- UV-C波长：UV-C灯在254nm（杀菌UV）运行。发射185nm的灯会从氧气生成臭氧（O2→O3）。光谱分析确认灯管输出为254nm，无显著185nm发射。\n- 臭氧测量：在最大风扇速度下8小时连续运行期间，在密封测试室中进行连续臭氧监测（UV吸收法，0-100 ppb分辨率）。在设备出口和1米距离处取样。\n- TiO2臭氧效应：光催化TiO2实际上帮助在催化剂表面分解臭氧（O3→O2）。测试验证设备出口的臭氧水平低于环境——一种有益的副效应。\n- 活性炭贡献：活性炭阶段在排气前进一步吸附任何痕量臭氧。碳穿透测试确认在额定过滤器寿命内的臭氧去除能力。\n\n臭氧合规是FDA批准的通过/失败门槛。任何超过50 ppb的读数需要在提交前进行设计更改。",
        },
        status: "not-started",
        owner: "tech",
        category: "testing",
      },
      {
        id: "T8",
        month: 7,
        title: {
          en: "Production Unit Assembly & Final QC",
          cn: "生产单元组装与最终质检",
        },
        description: {
          en: "Production-equivalent units (n=10), final assembly SOP, QC inspection checklist, packaging & labeling verification",
          cn: "生产等效单元（n=10），最终组装SOP，质检检查清单，包装和标签验证",
        },
        detail: {
          en: "T8 transitions from prototype to production-equivalent units that will be submitted to FDA as representative of the commercial device:\n\n- Production Run (n=10): Build 10 units using production-intent tooling, materials from qualified suppliers, and documented assembly procedures. These units serve as the 510(k) test articles.\n- Assembly SOP: Standard Operating Procedure for device assembly, covering reactor installation, filter stack mounting, wiring harness, final enclosure sealing, and QC checkpoints.\n- QC Inspection Checklist: Incoming material inspection, in-process checks (UV-C lamp orientation, TiO2 coating intact, HEPA seal integrity), and final functional test (fan at all speeds, UV-C lamp ignition, filter indicator).\n- Packaging & Labeling: Final package design including 21 CFR 801 required labeling, Instructions for Use (IFU), quick-start guide, and CADR label per FTC/AHAM requirements.\n- Environmental Stress Screening: Drop test (30 inches onto concrete), vibration test (per ISTA 3A for parcel shipping), and temperature cycling (-20°C to +60°C storage) on 3 units from the production run.\n\nT8 completion provides the test articles for the 510(k) submission and confirms manufacturing repeatability.",
          cn: "T8从原型过渡到生产等效单元，将作为商业设备的代表提交FDA：\n\n- 生产运行（n=10）：使用生产级工装、合格供应商材料和文档化组装程序建造10台设备。这些单元作为510(k)测试品。\n- 组装SOP：设备组装标准操作程序，涵盖反应器安装、过滤器组安装、线束、最终外壳密封和质检检查点。\n- 质检检查清单：进料检验、过程检查（UV-C灯方向、TiO2涂层完整、HEPA密封完整性），最终功能测试（所有速度风扇、UV-C灯点火、过滤器指示器）。\n- 包装和标签：最终包装设计，包括21 CFR 801要求的标签、使用说明（IFU）、快速入门指南和按FTC/AHAM要求的CADR标签。\n- 环境应力筛选：跌落测试（30英寸落到混凝土上）、振动测试（按ISTA 3A包裹运输）和温度循环（-20°C到+60°C存储），对生产运行中的3台设备进行。\n\nT8完成提供510(k)提交的测试品并确认制造可重复性。",
        },
        status: "not-started",
        owner: "tech",
        category: "prototype",
      },
    ],
  },
  regulatory: {
    label: { en: "Regulatory Track", cn: "法规路径" },
    icon: "📋",
    milestones: [
      {
        id: "R1",
        month: 0,
        title: {
          en: "Predicate Device Research & SE Strategy",
          cn: "前置设备研究与SE策略",
        },
        description: {
          en: "FDA 510(k) database search: AiroCide TiO2 (K023830), Air Purifier 3707 UVC (K033448), ABRACAIR (K050257)",
          cn: "FDA 510(k)数据库搜索：AiroCide TiO2 (K023830)，Air Purifier 3707 UVC (K033448)，ABRACAIR (K050257)",
        },
        detail: {
          en: "The 510(k) pathway requires demonstrating substantial equivalence to a legally marketed predicate device. This milestone locks the SE strategy:\n\n- Primary Predicate: AiroCide TiO2 (K023830) — the closest match. AiroCide uses TiO2 photocatalysis with UV light to destroy airborne pathogens. Same technology principle, same intended use, same product code (FRA).\n- Secondary Predicate: Air Purifier 3707 UVC (K033448) — a UV-C based medical air purifier. Establishes that UV-C germicidal technology is an accepted mechanism for this product classification.\n- Tertiary Predicate: ABRACAIR Air Cleaner (K050257, QTZ300-60 and QTZ100-24) — uses a xenon flash lamp doped with titanium in a reflecting chamber. Similar photocatalytic mechanism, tested by Research Triangle Institute (RTI) for bacterial and fungal reduction.\n- SE Discussion Framework: Device comparison table mapping our device specifications against each predicate across: intended use, technology, performance, materials, energy source, and safety features.\n- Classification: § 880.6500 Medical Ultraviolet Air Purifier, Class II, Product Code FRA, regulated by General Hospital Devices branch at CDRH.\n\nR1 is complete when the SE strategy document is finalized and approved by the regulatory team.",
          cn: "510(k)路径要求证明与合法上市的前置设备的实质等效性。此里程碑锁定SE策略：\n\n- 主要前置设备：AiroCide TiO2 (K023830)——最接近的匹配。AiroCide使用TiO2光催化与紫外光摧毁空气中的病原体。相同技术原理、相同预期用途、相同产品代码（FRA）。\n- 次要前置设备：Air Purifier 3707 UVC (K033448)——基于UV-C的医用空气净化器。确立UV-C杀菌技术是该产品分类的公认机制。\n- 第三前置设备：ABRACAIR Air Cleaner (K050257, QTZ300-60和QTZ100-24)——在反射室中使用掺钛氙闪光灯。类似光催化机制，由研究三角研究所（RTI）测试细菌和真菌减少。\n- SE讨论框架：设备对照表将我们的设备规格与每个前置设备在以下方面进行映射：预期用途、技术、性能、材料、能源和安全功能。\n- 分类：§ 880.6500医用紫外线空气净化器，II类，产品代码FRA，由CDRH通用医院设备分支监管。\n\nSE策略文件最终确定并经法规团队批准后，R1完成。",
        },
        status: "complete",
        owner: "regulatory",
        category: "preparation",
      },
      {
        id: "R2",
        month: 1,
        title: {
          en: "510(k) Summary Drafted",
          cn: "510(k)摘要起草",
        },
        description: {
          en: "510(k) Summary per 21 CFR 807.92: device description, intended use, SE discussion, performance standards",
          cn: "按21 CFR 807.92的510(k)摘要：设备描述，预期用途，SE讨论，性能标准",
        },
        detail: {
          en: "The 510(k) Summary is a mandatory document per the Safe Medical Devices Act of 1990 (21 CFR 807.92). This milestone produces the draft:\n\n- Submitter: Titania Labs, LLC, Gresham, OR\n- Proprietary Name: TiO2 Air Cleaner, Model 1\n- Common/Usual Name: Air Purifier\n- Classification: § 880.6500 Medical Ultraviolet Air Purifier, Class II, Product Code FRA, reviewed by General Hospital Devices\n- Predicate Devices: AiroCide TiO2 (K023830), Air Purifier 3707 UVC (K033448), ABRACAIR Air Cleaner (QTZ300-60 and QTZ100-24)\n- Device Description: Fan-powered device using a 2½-inch fluorescent UV-C lamp (254 nm) coated with titanium dioxide. The lamp is contained in an activated carbon chamber to irradiate air as it passes through and out of the device into ambient air.\n- Intended Use: Used to reduce the concentration of viable airborne bacteria, mold and spores within inhabited spaces. Not intended to treat a specific disease or medical condition. Used as part of a comprehensive air quality program.\n- Performance Standards: No mandatory performance standards under Section 514 of the FD&C Act. Berkeley Lab DOE research supports TiO2 photo-catalytic feasibility.\n- Substantial Equivalence: SE to predicates in intended use, characteristics, and device description.\n\nThe Summary is reviewed by legal counsel before finalization.",
          cn: "510(k)摘要是根据1990年安全医疗器械法（21 CFR 807.92）的强制性文件。此里程碑产出草稿：\n\n- 提交人：Titania Labs, LLC，俄勒冈州格雷舍姆\n- 专有名称：TiO2 Air Cleaner, Model 1\n- 通用名称：空气净化器\n- 分类：§ 880.6500医用紫外线空气净化器，II类，产品代码FRA，通用医院设备部门审查\n- 前置设备：AiroCide TiO2 (K023830)，Air Purifier 3707 UVC (K033448)，ABRACAIR Air Cleaner (QTZ300-60和QTZ100-24)\n- 设备描述：风扇驱动设备，使用涂覆二氧化钛的2½英寸荧光UV-C灯（254nm）。灯管封装在活性炭室中，在空气通过并排出设备进入环境空气时对其进行辐照。\n- 预期用途：用于减少居住空间中可存活的空气传播细菌、霉菌和孢子的浓度。不用于治疗特定疾病或医学状况。作为综合空气质量计划的一部分使用。\n- 性能标准：FD&C法第514条未建立强制性能标准。Berkeley Lab DOE研究支持TiO2光催化可行性。\n- 实质等效：在预期用途、特征和设备描述方面与前置设备实质等效。\n\n摘要在最终确定前经法律顾问审查。",
        },
        status: "complete",
        owner: "regulatory",
        category: "submission",
      },
      {
        id: "R3",
        month: 3,
        title: {
          en: "Device Description & SE Discussion",
          cn: "设备描述与SE讨论",
        },
        description: {
          en: "Detailed comparison to predicates: technology, intended use, performance, materials. Block diagrams, photos, specifications.",
          cn: "与前置设备详细比较：技术、预期用途、性能、材料。框图、照片、规格。",
        },
        detail: {
          en: "The SE Discussion is the heart of the 510(k) submission — where we prove our device is substantially equivalent to the predicate devices:\n\n- Intended Use Comparison: Side-by-side table showing our device and each predicate share the same intended use — reducing airborne microorganisms in inhabited spaces.\n- Technology Comparison: All devices use UV-based photocatalytic/germicidal mechanisms. Our device uses UV-C + TiO2 coating (same as AiroCide K023830). ABRACAIR uses xenon + titanium (similar but different UV source). Air Purifier 3707 uses UV-C without TiO2.\n- Performance Comparison: Comparative table of bacterial reduction rates, room coverage (CFM), and noise levels. Where predicates published performance data, we benchmark against it.\n- Materials Comparison: All devices use similar materials — UV lamp (quartz glass), electronic ballast, fan motor, and filtration media. Our activated carbon and HEPA stages are additions that enhance performance without raising new safety questions.\n- Block Diagram: Complete system diagram showing air path from intake → pre-filter → TiO2 reactor → activated carbon → HEPA → fan → exhaust.\n- Photographs: Labeled photos of the device exterior, reactor interior, filter assembly, control panel, and labeling location.\n\nThe SE Discussion must withstand FDA reviewer scrutiny. Any claimed difference from predicates must be explained as a performance enhancement, not a new intended use.",
          cn: "SE讨论是510(k)提交的核心——我们在此证明设备与前置设备实质等效：\n\n- 预期用途比较：并列表格显示我们的设备和每个前置设备共享相同的预期用途——减少居住空间中的空气传播微生物。\n- 技术比较：所有设备使用基于UV的光催化/杀菌机制。我们的设备使用UV-C + TiO2涂层（与AiroCide K023830相同）。ABRACAIR使用氙灯+钛（类似但不同的UV来源）。Air Purifier 3707使用不含TiO2的UV-C。\n- 性能比较：细菌减少率、房间覆盖面积（CFM）和噪声水平的对照表。前置设备公开性能数据时，我们以此为基准。\n- 材料比较：所有设备使用相似材料——UV灯（石英玻璃）、电子镇流器、风扇电机和过滤介质。我们的活性炭和HEPA阶段是增强性能的补充，不引入新的安全问题。\n- 框图：完整系统图显示气流路径：进气口→预过滤器→TiO2反应器→活性炭→HEPA→风扇→排气。\n- 照片：设备外部、反应器内部、过滤器组件、控制面板和标签位置的标注照片。\n\nSE讨论必须经得起FDA审查员审查。与前置设备的任何声称差异必须解释为性能增强而非新预期用途。",
        },
        status: "not-started",
        owner: "regulatory",
        category: "submission",
      },
      {
        id: "R4",
        month: 5,
        title: {
          en: "510(k) Cover Letter & Administrative Package",
          cn: "510(k)附信与行政包",
        },
        description: {
          en: "Cover letter, truthful & accuracy statement, indications for use, 510(k) summary, user fees, eSTAR format",
          cn: "附信，真实性和准确性声明，适应症，510(k)摘要，用户费，eSTAR格式",
        },
        detail: {
          en: "The administrative package wraps all technical and regulatory deliverables into the formal FDA submission format:\n\n- Cover Letter: Identifies the device, classification, product code, applicant, and contact person. Requests 510(k) clearance.\n- Truthful & Accuracy Statement: Per 21 CFR 807.87(j), a signed statement that all data and information submitted are truthful and accurate.\n- Indications for Use (IFU) Statement: FDA Form 3881 — the official intended use statement that will appear on the clearance letter.\n- 510(k) Summary or Statement: We chose to submit a 510(k) Summary (public document) per 21 CFR 807.92.\n- User Fee: FDA 510(k) user fee (~$21,760 for FY2026 for small business). Payment submitted via pay.gov.\n- eSTAR Format: FDA's electronic submission format. All documents compiled into the structured eSTAR template with hyperlinked sections.\n- Establishment Registration: Titania Labs, LLC registered as a device establishment per 21 CFR 807.\n- Device Listing: TiO2 Air Cleaner, Model 1 listed under product code FRA.\n\nR4 is the final assembly step before eCopy preparation (R5). All technical reports from T1–T7 must be complete before R4 can close.",
          cn: "行政包将所有技术和法规交付物打包成正式的FDA提交格式：\n\n- 附信：标识设备、分类、产品代码、申请人和联系人。请求510(k)批准。\n- 真实性和准确性声明：按21 CFR 807.87(j)，签署声明所有提交的数据和信息真实准确。\n- 适应症声明：FDA Form 3881——将出现在批准信上的官方预期用途声明。\n- 510(k)摘要或声明：我们选择按21 CFR 807.92提交510(k)摘要（公共文件）。\n- 用户费：FDA 510(k)用户费（FY2026小企业约$21,760）。通过pay.gov提交付款。\n- eSTAR格式：FDA的电子提交格式。所有文件编译成结构化eSTAR模板并带有超链接章节。\n- 机构注册：Titania Labs, LLC按21 CFR 807注册为设备机构。\n- 设备列表：TiO2 Air Cleaner, Model 1在产品代码FRA下列出。\n\nR4是eCopy准备（R5）之前的最终组装步骤。R4关闭前T1-T7的所有技术报告必须完成。",
        },
        status: "not-started",
        owner: "regulatory",
        category: "submission",
      },
      {
        id: "R5",
        month: 6,
        title: {
          en: "eCopy Preparation & FDA Submission",
          cn: "eCopy准备与FDA提交",
        },
        description: {
          en: "eCopy disk preparation, pre-submission validation check, CDRH Document Control Center submission",
          cn: "eCopy光盘准备，提交前验证检查，CDRH文件控制中心提交",
        },
        detail: {
          en: "The eCopy is the physical submission medium for FDA 510(k) filings. This milestone covers final preparation and delivery:\n\n- eCopy Format: FDA requires an electronic copy (eCopy) on CD/DVD/USB drive containing all submission documents in PDF format, organized per the eSTAR structure.\n- eCopy Validation: Before shipping, the eCopy is validated using FDA's eCopy validation tool to ensure: all files open correctly, no corrupted PDFs, hyperlinks work, file sizes within limits, and required sections present.\n- Pre-Submission Checklist: Final review against FDA's Refuse to Accept (RTA) checklist — the 48-item list of reasons FDA will reject a submission without review. Common RTA triggers: missing user fee, unsigned truthful/accuracy statement, incomplete device description, missing predicate comparison.\n- CDRH Submission: Physical eCopy shipped to FDA Center for Devices and Radiological Health (CDRH), Document Control Center, Silver Spring, MD.\n- Acknowledgment: FDA issues an acknowledgment letter with the 510(k) K-number within ~15 business days of receipt. The 90-day review clock starts upon acceptance (not receipt).\n\nNote: The original submission in 2018 received an eCopy hold letter from FDA due to formatting issues. The resubmission addresses all eCopy deficiencies identified in the hold letter.",
          cn: "eCopy是FDA 510(k)提交的物理提交介质。此里程碑涵盖最终准备和交付：\n\n- eCopy格式：FDA要求在CD/DVD/USB驱动器上提供电子副本（eCopy），包含按eSTAR结构组织的PDF格式的所有提交文件。\n- eCopy验证：发送前，使用FDA的eCopy验证工具验证eCopy：所有文件正确打开，无损坏PDF，超链接有效，文件大小在限制内，必需章节存在。\n- 提交前检查清单：按FDA的拒绝受理（RTA）检查清单进行最终审查——FDA不经审查即拒绝提交的48项理由清单。常见RTA触发因素：缺少用户费、未签署真实性/准确性声明、设备描述不完整、缺少前置设备比较。\n- CDRH提交：物理eCopy寄送至FDA器械和放射健康中心（CDRH），文件控制中心，马里兰州Silver Spring。\n- 确认：FDA在收到后约15个工作日内发出确认信和510(k) K编号。90天审查时钟在受理（非收到）后开始。\n\n注：2018年的原始提交因格式问题收到FDA的eCopy暂停信。重新提交解决了暂停信中确认的所有eCopy不足。",
        },
        status: "not-started",
        owner: "regulatory",
        category: "submission",
      },
      {
        id: "R6",
        month: 7,
        title: {
          en: "FDA Review Period",
          cn: "FDA审查期",
        },
        description: {
          en: "90-day standard 510(k) review. Respond to any Additional Information (AI) requests. Product code FRA review team.",
          cn: "90天标准510(k)审查。回应任何补充信息（AI）请求。产品代码FRA审查团队。",
        },
        detail: {
          en: "During the FDA review period, the CDRH review team evaluates the complete 510(k) package:\n\n- Review Timeline: MDUFA V goal is 90% of standard 510(k)s reviewed within 90 days of acceptance. FRA product code is reviewed by the General Hospital Devices branch.\n- Review Focus Areas: SE discussion strength, microbial kill data, ozone emissions compliance, electrical safety reports, and labeling accuracy.\n- AI Requests: FDA may issue Additional Information (AI) requests if they need clarification. Common AI topics for air purifiers: test methodology details, CADR testing conditions, ozone measurement protocol, predicate comparison gaps.\n- AI Response Window: Typically 60–180 days to respond. Review clock pauses during this time. A well-prepared submission minimizes AI likelihood.\n- Interactive Review: FDA may request a teleconference to discuss specific technical questions. This is an opportunity to address concerns before a formal AI letter.\n- Possible Outcomes: Clearance (SE Order), AI request, or Not Substantially Equivalent (NSE). NSE is rare for well-prepared FRA submissions with strong predicate alignment.\n\nDuring this period, the team continues post-clearance preparation — manufacturing ramp, distribution planning, and marketing materials.",
          cn: "在FDA审查期间，CDRH审查团队评估完整的510(k)包：\n\n- 审查时间线：MDUFA V目标是90%的标准510(k)在受理后90天内审查完成。FRA产品代码由通用医院设备分支审查。\n- 审查重点领域：SE讨论力度、微生物杀灭数据、臭氧排放合规、电气安全报告和标签准确性。\n- AI请求：如果需要澄清，FDA可能发出补充信息（AI）请求。空气净化器常见AI话题：测试方法细节、CADR测试条件、臭氧测量协议、前置设备比较差距。\n- AI响应窗口：通常60-180天回应。审查时钟在此期间暂停。准备充分的提交可最小化AI可能性。\n- 交互式审查：FDA可能请求电话会议讨论特定技术问题。这是在正式AI信之前解决关切的机会。\n- 可能结果：批准（SE令）、AI请求或非实质等效（NSE）。对于与前置设备良好对齐的FRA提交，NSE很少见。\n\n在此期间，团队继续批准后准备——制造提升、分销规划和营销材料。",
        },
        status: "not-started",
        owner: "regulatory",
        category: "clearance",
      },
      {
        id: "R7",
        month: 10,
        title: {
          en: "Expected 510(k) Clearance",
          cn: "预计510(k)批准",
        },
        description: {
          en: "FDA clearance letter with K-number. Product code FRA clearance → commercial launch authorized.",
          cn: "FDA批准信和K编号。产品代码FRA批准→授权商业发布。",
        },
        detail: {
          en: "R7 marks the expected FDA 510(k) clearance — the go-to-market authorization for the TiO2 Air Cleaner:\n\n- Clearance Letter: FDA issues a Substantially Equivalent (SE) determination letter with the assigned K-number. This letter authorizes commercial distribution of the TiO2 Air Cleaner, Model 1.\n- Post-Clearance Requirements: Establishment registration renewal, device listing confirmation, and complaint handling procedures activated per 21 CFR 803 (MDR).\n- Quality System: 21 CFR 820 Quality System Regulation compliance verification. Design History File (DHF) is complete and under document control.\n- Labeling: Final commercial labeling printed with K-number and 'cleared by FDA' language (per FDA labeling guidance — cannot say 'FDA approved' for 510(k) devices).\n- Manufacturing: Production line qualified, incoming material inspection procedures active, and initial production run scheduled.\n- Distribution: First commercial shipments to launch customers — healthcare facilities, hospitals, dental offices, and veterinary clinics.\n\nR7 at M+10 assumes no AI requests. A 30-day AI buffer brings the worst-case clearance to M+13.",
          cn: "R7标志着预期的FDA 510(k)批准——TiO2空气净化器的上市授权：\n\n- 批准信：FDA发出实质等效（SE）确定信和指定的K编号。此信授权TiO2 Air Cleaner, Model 1的商业分销。\n- 批准后要求：机构注册续期、设备列表确认和按21 CFR 803（MDR）的投诉处理程序启动。\n- 质量体系：21 CFR 820质量体系法规合规验证。设计历史文件（DHF）完成并在文件控制下。\n- 标签：最终商业标签印上K编号和'经FDA批准'语言（按FDA标签指南——510(k)设备不能说'FDA approved'）。\n- 制造：生产线已验证，进料检验程序已启动，初始生产运行已安排。\n- 分销：首批商业发货给启动客户——医疗保健设施、医院、牙科诊所和兽医诊所。\n\nM+10的R7假设无AI请求。30天AI缓冲将最坏情况批准推至M+13。",
        },
        status: "not-started",
        owner: "regulatory",
        category: "clearance",
      },
      {
        id: "R8",
        month: 1,
        title: {
          en: "IP & Trademark Filing",
          cn: "知识产权与商标申请",
        },
        description: {
          en: "Provisional patent application for reactor design, trademark 'TiO2 Air Cleaner', trade dress protection",
          cn: "反应器设计临时专利申请，'TiO2 Air Cleaner'商标，外观设计保护",
        },
        detail: {
          en: "R8 establishes the intellectual property foundation for the TiO2 Air Cleaner product line:\n\n- Provisional Patent: File a US provisional patent application covering the novel combination of UV-C lamp with TiO2 nanocoating integrated into an activated carbon chamber. While TiO2 photocatalysis is known, our specific reactor geometry and coating process are proprietary.\n- Trademark: File 'TiO2 Air Cleaner' and 'Titania Air' as registered trademarks with the USPTO for Class 11 (air purification apparatus). Also consider 'Titania Reactor' as a brand for the core technology.\n- Trade Dress: Document the distinctive product design elements (housing shape, control panel layout, reactor viewing window) for trade dress protection.\n- Patent Landscape Review: Freedom-to-operate analysis ensuring no infringement on existing TiO2/UV photocatalysis patents. Key patents to review: KenkoAir/AiroCide patents (expired), Synlabs/ABRACAIR patents.\n- IP Assignment: All IP rights formally assigned to Titania Labs, LLC with inventor assignment agreements.\n\nR8 at M+1 runs in parallel with technical development. IP protection before public disclosure (510(k) submission is a public document) is critical.",
          cn: "R8建立TiO2空气净化器产品线的知识产权基础：\n\n- 临时专利：提交涵盖UV-C灯与TiO2纳米涂层集成到活性炭室中的新颖组合的美国临时专利申请。虽然TiO2光催化已知，但我们的特定反应器几何形状和涂覆工艺是专有的。\n- 商标：向USPTO提交'TiO2 Air Cleaner'和'Titania Air'作为第11类（空气净化装置）注册商标。也考虑'Titania Reactor'作为核心技术品牌。\n- 外观设计：记录独特的产品设计元素（外壳形状、控制面板布局、反应器观察窗）用于外观设计保护。\n- 专利全景审查：自由实施分析确保不侵犯现有TiO2/UV光催化专利。需审查的关键专利：KenkoAir/AiroCide专利（已过期）、Synlabs/ABRACAIR专利。\n- IP转让：所有IP权利通过发明人转让协议正式转让给Titania Labs, LLC。\n\nM+1的R8与技术开发并行运行。在公开披露前的IP保护（510(k)提交是公共文件）至关重要。",
        },
        status: "in-progress",
        owner: "business",
        category: "legal",
      },
      {
        id: "R9",
        month: 2,
        title: {
          en: "Quality System Establishment",
          cn: "质量体系建立",
        },
        description: {
          en: "21 CFR 820 QSR framework: design controls, CAPA, document control, complaint handling, DHF structure",
          cn: "21 CFR 820 QSR框架：设计控制、CAPA、文件控制、投诉处理、DHF结构",
        },
        detail: {
          en: "R9 establishes the Quality Management System required for FDA-regulated medical device manufacturing:\n\n- 21 CFR 820 Framework: Implement the minimum QMS elements required by the Quality System Regulation:\n  • Design Controls (820.30): Design plan, inputs, outputs, verification, validation, transfer, and change control\n  • Document Controls (820.40): SOPs for creation, review, approval, and revision of quality documents\n  • CAPA (820.90): Corrective and Preventive Action procedures for addressing nonconformities\n  • Complaint Handling (820.198): Process for receiving, evaluating, and investigating customer complaints\n  • Production & Process Controls (820.70): Manufacturing procedures, environmental controls, equipment calibration\n  • Records (820.180): Retention of DHR (Device History Record) for each production unit\n- Design History File (DHF): Compile all design control evidence — design plan, inputs, outputs, verification records, validation records, design review minutes, and design transfer documentation.\n- Supplier Controls: Procedures for evaluating and qualifying suppliers, incoming material inspection, and supplier audit program.\n- Training: Quality system training for all personnel involved in design, manufacturing, testing, and complaint handling.\n\nR9 is a prerequisite for 510(k) filing — FDA reviewers verify that the applicant has an adequate quality system during submission review.",
          cn: "R9建立FDA监管医疗器械制造所需的质量管理体系：\n\n- 21 CFR 820框架：实施质量体系法规要求的最低QMS元素：\n  • 设计控制（820.30）：设计计划、输入、输出、验证、确认、转移和变更控制\n  • 文件控制（820.40）：质量文件的创建、审查、批准和修订SOP\n  • CAPA（820.90）：处理不符合项的纠正和预防措施程序\n  • 投诉处理（820.198）：接收、评估和调查客户投诉的流程\n  • 生产和过程控制（820.70）：制造程序、环境控制、设备校准\n  • 记录（820.180）：每个生产单元的DHR（设备历史记录）保留\n- 设计历史文件（DHF）：编译所有设计控制证据——设计计划、输入、输出、验证记录、确认记录、设计评审会议记录和设计转移文档。\n- 供应商控制：评估和验证供应商、进料检验和供应商审核计划的程序。\n- 培训：所有参与设计、制造、测试和投诉处理人员的质量体系培训。\n\nR9是510(k)提交的先决条件——FDA审查员在提交审查时验证申请人具有充分的质量体系。",
        },
        status: "not-started",
        owner: "regulatory",
        category: "audit",
      },
    ],
  },
};

// ============================================================
// GATE SYSTEM — Decision checkpoints
// ============================================================

export const GATES: Gate[] = [
  {
    id: "G1",
    number: 1,
    title: { en: "Prototype Design Freeze", cn: "原型设计冻结" },
    month: 2,
    status: "pending-review",
    criteria: [
      {
        en: "UV-C reactor prototype finalized (T1)",
        cn: "UV-C反应器原型定型（T1）",
        met: true,
      },
      {
        en: "TiO2 photocatalytic efficiency validated (T2)",
        cn: "TiO2光催化效率已验证（T2）",
        met: false,
      },
      {
        en: "HEPA/carbon filtration integrated (T3)",
        cn: "HEPA/活性炭过滤已集成（T3）",
        met: false,
      },
      {
        en: "Predicate research & SE strategy complete (R1)",
        cn: "前置设备研究与SE策略完成（R1）",
        met: true,
      },
    ],
    decision: null,
    decisionBy: null,
    decisionDate: null,
    notes: [],
    inputBusiness: [],
    inputTech: [],
  },
  {
    id: "G2",
    number: 2,
    title: { en: "Performance Testing Complete", cn: "性能测试完成" },
    month: 5,
    status: "not-started",
    criteria: [
      {
        en: "Airflow & CADR testing passed (T4)",
        cn: "气流与CADR测试通过（T4）",
        met: false,
      },
      {
        en: "Microbial kill rate ≥99% bacteria confirmed (T5)",
        cn: "微生物杀灭率≥99%细菌确认（T5）",
        met: false,
      },
      {
        en: "Ozone emissions <50 ppb verified (T7)",
        cn: "臭氧排放<50 ppb已验证（T7）",
        met: false,
      },
      {
        en: "Electrical safety UL/IEC testing passed (T6)",
        cn: "电气安全UL/IEC测试通过（T6）",
        met: false,
      },
    ],
    decision: null,
    decisionBy: null,
    decisionDate: null,
    notes: [],
    inputBusiness: [],
    inputTech: [],
  },
  {
    id: "G3",
    number: 3,
    title: { en: "510(k) Submission Ready", cn: "510(k)提交就绪" },
    month: 6,
    status: "not-started",
    criteria: [
      {
        en: "All submission sections complete (eSTAR format)",
        cn: "全部提交章节完成（eSTAR格式）",
        met: false,
      },
      {
        en: "Risk analysis (ISO 14971) finalized",
        cn: "风险分析（ISO 14971）定稿",
        met: false,
      },
      {
        en: "SE discussion & predicate comparison documented",
        cn: "SE讨论与前置设备比较文档完成",
        met: false,
      },
      {
        en: "Labeling & IFU reviewed (21 CFR 801)",
        cn: "标签和IFU审核（21 CFR 801）",
        met: false,
      },
      { en: "Quality system audit passed", cn: "质量体系审核通过", met: false },
    ],
    decision: null,
    decisionBy: null,
    decisionDate: null,
    notes: [],
    inputBusiness: [],
    inputTech: [],
  },
  {
    id: "G4",
    number: 4,
    title: { en: "eCopy Submitted to FDA", cn: "eCopy已提交FDA" },
    month: 7,
    status: "not-started",
    criteria: [
      {
        en: "eCopy validated and shipped to CDRH",
        cn: "eCopy已验证并寄送CDRH",
        met: false,
      },
      {
        en: "User fee payment confirmed",
        cn: "用户费支付已确认",
        met: false,
      },
      {
        en: "Production-equivalent units (n=10) assembled (T8)",
        cn: "生产等效单元（n=10）已组装（T8）",
        met: false,
      },
    ],
    decision: null,
    decisionBy: null,
    decisionDate: null,
    notes: [],
    inputBusiness: [],
    inputTech: [],
  },
  {
    id: "G5",
    number: 5,
    title: { en: "FDA 510(k) Clearance", cn: "FDA 510(k)批准" },
    month: 10,
    status: "not-started",
    criteria: [
      {
        en: "510(k) SE determination received (product code FRA)",
        cn: "510(k) SE决定已收到（产品代码FRA）",
        met: false,
      },
      {
        en: "K-number assigned",
        cn: "K编号已分配",
        met: false,
      },
      {
        en: "No outstanding AI requests",
        cn: "无未完成的AI补充信息请求",
        met: false,
      },
    ],
    decision: null,
    decisionBy: null,
    decisionDate: null,
    notes: [],
    inputBusiness: [],
    inputTech: [],
  },
  {
    id: "G6",
    number: 6,
    title: {
      en: "Commercial Launch Authorization",
      cn: "商业发布授权",
    },
    month: 12,
    status: "not-started",
    criteria: [
      {
        en: "FDA clearance letter in hand",
        cn: "FDA批准信已收到",
        met: false,
      },
      {
        en: "Manufacturing line qualified & first production run complete",
        cn: "生产线已验证且首次生产运行完成",
        met: false,
      },
      {
        en: "Distribution & marketing plan finalized",
        cn: "分销和营销计划已定稿",
        met: false,
      },
    ],
    decision: null,
    decisionBy: null,
    decisionDate: null,
    notes: [],
    inputBusiness: [],
    inputTech: [],
  },
];

// ============================================================
// RISK DASHBOARD — ISO 14971
// ============================================================

export const RISKS: Risk[] = [
  {
    id: "RISK-001",
    title: {
      en: "Ozone generation exceeds 50 ppb limit (FDA 21 CFR 801.415)",
      cn: "臭氧生成超过50 ppb限值（FDA 21 CFR 801.415）",
    },
    severity: "high",
    probability: "low",
    riskLevel: "yellow",
    controls: {
      en: "254nm UV-C only (no 185nm); TiO2 catalyzes O3→O2 decomposition; activated carbon adsorption; continuous ozone monitoring in test protocol",
      cn: "仅254nm UV-C（无185nm）；TiO2催化O3→O2分解；活性炭吸附；测试方案中连续臭氧监测",
    },
    residual: { en: "Acceptable", cn: "可接受" },
    mitigationStatus: "in-progress",
    module: "A",
    standard: "FDA 21 CFR 801.415",
  },
  {
    id: "RISK-002",
    title: {
      en: "UV-C radiation leakage from reactor chamber (user skin/eye exposure)",
      cn: "UV-C辐射从反应器室泄漏（用户皮肤/眼睛暴露）",
    },
    severity: "high",
    probability: "very-low",
    riskLevel: "green",
    controls: {
      en: "Sealed reactor enclosure; UV measurements at all exterior surfaces <0.1 µW/cm²; interlock switch cuts UV lamp on enclosure open",
      cn: "密封反应器外壳；所有外部表面UV测量<0.1 µW/cm²；互锁开关在外壳打开时切断UV灯",
    },
    residual: { en: "Acceptable", cn: "可接受" },
    mitigationStatus: "complete",
    module: "A",
    standard: "IEC 60335-2-65",
  },
  {
    id: "RISK-003",
    title: {
      en: "TiO2 nanoparticle release into airstream (inhalation hazard)",
      cn: "TiO2纳米颗粒释放到气流中（吸入危害）",
    },
    severity: "high",
    probability: "very-low",
    riskLevel: "yellow",
    controls: {
      en: "TiO2 bonded to lamp surface (not aerosolized); HEPA downstream captures any particles ≥0.3µm; nano-release testing per ISO 10808",
      cn: "TiO2结合在灯面上（非气溶胶化）；下游HEPA捕获任何≥0.3µm颗粒；按ISO 10808进行纳米释放测试",
    },
    residual: { en: "Acceptable", cn: "可接受" },
    mitigationStatus: "in-progress",
    module: "A",
    standard: "ISO 14971",
  },
  {
    id: "RISK-004",
    title: {
      en: "Insufficient microbial kill rate — below ≥99% threshold for SE claim",
      cn: "微生物杀灭率不足——低于SE声明所需≥99%阈值",
    },
    severity: "high",
    probability: "medium",
    riskLevel: "red",
    controls: {
      en: "Single-pass efficiency testing at accredited lab; UV-C intensity optimization; reactor dwell time adjustment; predicate benchmarking against AiroCide (K023830)",
      cn: "在认可实验室进行单次通过效率测试；UV-C强度优化；反应器停留时间调整；与AiroCide (K023830)前置设备基准比较",
    },
    residual: {
      en: "Manageable with design iteration",
      cn: "通过设计迭代可控",
    },
    mitigationStatus: "not-started",
    module: "A",
    standard: "ISO 14971",
  },
  {
    id: "RISK-005",
    title: {
      en: "Electrical safety failure — fan motor overload or UV ballast malfunction",
      cn: "电气安全故障——风扇电机过载或UV镇流器故障",
    },
    severity: "medium",
    probability: "low",
    riskLevel: "yellow",
    controls: {
      en: "UL 507 fan safety compliance; UL 867 UV ballast testing; thermal cutoff; over-current protection circuit; Class II double insulation",
      cn: "UL 507风扇安全合规；UL 867 UV镇流器测试；热切断；过流保护电路；II类双重绝缘",
    },
    residual: { en: "Acceptable", cn: "可接受" },
    mitigationStatus: "in-progress",
    module: "A",
    standard: "UL 507 / UL 867",
  },
  {
    id: "RISK-006",
    title: {
      en: "Filter replacement indicator malfunction — clogged filter undetected",
      cn: "滤芯更换指示器故障——堵塞过滤器未被检测",
    },
    severity: "medium",
    probability: "low",
    riskLevel: "yellow",
    controls: {
      en: "Redundant differential pressure sensor; timed maximum-use reminder (secondary); user manual filter inspection instructions",
      cn: "冗余差压传感器；定时最大使用量提醒（辅助）；用户手册过滤器检查说明",
    },
    residual: { en: "Low", cn: "低" },
    mitigationStatus: "not-started",
    module: "A",
    standard: "ISO 14971",
  },
  {
    id: "RISK-007",
    title: {
      en: "510(k) rejection — predicate comparison insufficient or SE not established",
      cn: "510(k)被拒——前置设备比较不充分或SE未建立",
    },
    severity: "high",
    probability: "low",
    riskLevel: "yellow",
    controls: {
      en: "Three strong predicates identified (AiroCide K023830, Air Purifier 3707 K033448, ABRACAIR K050257); comprehensive SE discussion; performance data benchmarked against predicate published results",
      cn: "已确定三个强前置设备（AiroCide K023830，Air Purifier 3707 K033448，ABRACAIR K050257）；全面SE讨论；性能数据与前置设备公开结果基准比较",
    },
    residual: { en: "Acceptable", cn: "可接受" },
    mitigationStatus: "in-progress",
    module: "N/A",
    standard: "21 CFR 807",
  },
  {
    id: "RISK-008",
    title: {
      en: "Funding deployment risk — limited seed capital for testing, regulatory fees, and prototype tooling",
      cn: "资金部署风险——测试、监管费用和原型工装的种子资金有限",
    },
    severity: "medium",
    probability: "medium",
    riskLevel: "yellow",
    controls: {
      en: "Phased milestone deployment; UL/microbial testing prioritized by cost; small business FDA fee discount; bootstrap production tooling",
      cn: "分阶段里程碑部署；UL/微生物测试按成本优先级排序；小企业FDA费用折扣；自主生产工装",
    },
    residual: { en: "Manageable", cn: "可控" },
    mitigationStatus: "in-progress",
    module: "N/A",
    standard: "Business",
  },
];

// ============================================================
// REGULATORY STANDARDS TRACKER
// ============================================================

export const STANDARDS: Standard[] = [
  {
    id: "STD-01",
    code: "UL 507",
    title: {
      en: "Electric Fans — Safety",
      cn: "电风扇 — 安全",
    },
    applies: "Fan Assembly",
    status: "not-started",
    progress: 0,
  },
  {
    id: "STD-02",
    code: "UL 867",
    title: {
      en: "Electrostatic Air Cleaners — Safety",
      cn: "静电空气净化器 — 安全",
    },
    applies: "UV-C Reactor",
    status: "not-started",
    progress: 0,
  },
  {
    id: "STD-03",
    code: "IEC 60335-2-65",
    title: {
      en: "Air Cleaning Appliances — Safety",
      cn: "空气净化器具 — 安全",
    },
    applies: "Complete Device",
    status: "not-started",
    progress: 0,
  },
  {
    id: "STD-04",
    code: "ISO 14971:2019",
    title: {
      en: "Risk Management for Medical Devices",
      cn: "医疗器械风险管理",
    },
    applies: "Complete Device",
    status: "in-progress",
    progress: 35,
  },
  {
    id: "STD-05",
    code: "21 CFR 801.415",
    title: {
      en: "FDA Ozone Emission Limits for Medical Devices",
      cn: "FDA医疗器械臭氧排放限值",
    },
    applies: "UV-C Reactor",
    status: "in-progress",
    progress: 20,
  },
  {
    id: "STD-06",
    code: "ANSI/AHAM AC-1",
    title: {
      en: "Clean Air Delivery Rate (CADR) Standard",
      cn: "洁净空气输出率（CADR）标准",
    },
    applies: "Complete Device",
    status: "not-started",
    progress: 0,
  },
  {
    id: "STD-07",
    code: "21 CFR Part 820",
    title: { en: "Quality System Regulation (QSR)", cn: "质量体系法规（QSR）" },
    applies: "Manufacturing",
    status: "in-progress",
    progress: 25,
  },
  {
    id: "STD-08",
    code: "21 CFR Part 801",
    title: {
      en: "Medical Device Labeling Requirements",
      cn: "医疗器械标签要求",
    },
    applies: "Labeling & IFU",
    status: "not-started",
    progress: 0,
  },
  {
    id: "STD-09",
    code: "ISO 10808",
    title: {
      en: "Nanoparticle Release — Characterization",
      cn: "纳米颗粒释放 — 表征",
    },
    applies: "TiO2 Coating",
    status: "not-started",
    progress: 0,
  },
  {
    id: "STD-10",
    code: "EPA Indoor Air Quality",
    title: {
      en: "EPA Indoor Air Quality Guidelines (Ozone)",
      cn: "EPA室内空气质量指南（臭氧）",
    },
    applies: "Complete Device",
    status: "in-progress",
    progress: 15,
  },
  {
    id: "STD-11",
    code: "IEC 60704",
    title: {
      en: "Household Appliances — Noise Measurement",
      cn: "家用电器 — 噪声测量",
    },
    applies: "Fan Assembly",
    status: "not-started",
    progress: 0,
  },
  {
    id: "STD-12",
    code: "21 CFR Part 807",
    title: {
      en: "Establishment Registration & Device Listing",
      cn: "机构注册与设备列表",
    },
    applies: "Applicant",
    status: "in-progress",
    progress: 50,
  },
];

// ============================================================
// TIMELINE — Business-term translations
// ============================================================

export const TIMELINE_EVENTS: TimelineEvent[] = [
  {
    month: 0,
    technical: {
      en: "Reactor prototype finalized; predicate research complete",
      cn: "反应器原型定型；前置设备研究完成",
    },
    business: {
      en: "Core technology locked — development clock starts",
      cn: "核心技术锁定——开发计时开始",
    },
    impact: "neutral",
  },
  {
    month: 2,
    technical: {
      en: "TiO2 efficiency validated; HEPA integrated",
      cn: "TiO2效率验证；HEPA集成",
    },
    business: {
      en: "Prototype design freeze — testing investment begins",
      cn: "原型设计冻结——测试投资开始",
    },
    impact: "critical",
  },
  {
    month: 4,
    technical: {
      en: "CADR testing & microbial kill rate testing",
      cn: "CADR测试与微生物杀灭率测试",
    },
    business: {
      en: "Performance validation — largest pre-submission expense",
      cn: "性能验证——提交前最大费用",
    },
    impact: "warning",
  },
  {
    month: 6,
    technical: {
      en: "510(k) package assembled; eCopy prepared",
      cn: "510(k)包组装；eCopy准备",
    },
    business: {
      en: "Submission milestone — regulatory pathway committed",
      cn: "提交里程碑——监管路径确定",
    },
    impact: "critical",
  },
  {
    month: 7,
    technical: {
      en: "eCopy submitted to CDRH",
      cn: "eCopy已提交CDRH",
    },
    business: {
      en: "FDA review period begins — 90-day clock",
      cn: "FDA审查期开始——90天计时",
    },
    impact: "critical",
  },
  {
    month: 10,
    technical: {
      en: "Expected 510(k) clearance (FRA)",
      cn: "预计510(k)批准（FRA）",
    },
    business: {
      en: "Market authorization — commercial launch enabled",
      cn: "上市授权——商业发布启动",
    },
    impact: "critical",
  },
  {
    month: 11,
    technical: {
      en: "Manufacturing ramp & first production run",
      cn: "制造提升与首批生产",
    },
    business: {
      en: "Revenue generation begins — distribution to healthcare facilities",
      cn: "收入产生开始——向医疗设施分销",
    },
    impact: "warning",
  },
  {
    month: 12,
    technical: {
      en: "Post-market surveillance active",
      cn: "上市后监督启动",
    },
    business: {
      en: "Full commercial operations — ROI realization",
      cn: "全面商业运营——ROI实现",
    },
    impact: "critical",
  },
];

// ============================================================
// CASH / RUNWAY — Financial tracking
// ============================================================

export const CASH_RUNWAY: CashRunway = {
  cashOnHand: 165000,
  monthlyBurn: 8500,
  runwayMonths: 19,
  currency: "USD",
  fundingRounds: [
    {
      id: "FR-001",
      label: { en: "Founder Investment", cn: "创始人投资" },
      amount: 75000,
      date: "2026-01",
      status: "received",
    },
    {
      id: "FR-002",
      label: { en: "SBIR Phase I Application", cn: "SBIR第一阶段申请" },
      amount: 275000,
      date: "2026-06",
      status: "pipeline",
    },
    {
      id: "FR-003",
      label: {
        en: "Angel Investor Commitment",
        cn: "天使投资人承诺",
      },
      amount: 100000,
      date: "2026-09",
      status: "pipeline",
    },
    {
      id: "FR-004",
      label: {
        en: "Seed Round (Post-Clearance)",
        cn: "种子轮（批准后）",
      },
      amount: 500000,
      date: "2027-03",
      status: "pipeline",
    },
  ],
  burnHistory: [
    {
      month: -3,
      burn: 6500,
      note: { en: "LLC setup & patent filing", cn: "LLC设立与专利申请" },
    },
    {
      month: -2,
      burn: 7200,
      note: { en: "Prototype materials & UV lamps", cn: "原型材料与UV灯" },
    },
    {
      month: -1,
      burn: 8000,
      note: {
        en: "TiO2 coating development",
        cn: "TiO2涂层开发",
      },
    },
    {
      month: 0,
      burn: 8500,
      note: {
        en: "Reactor assembly + 510(k) summary drafting",
        cn: "反应器组装+510(k)摘要起草",
      },
    },
  ],
};

// ============================================================
// INPUT TRACKING — Business & Tech stakeholder inputs
// ============================================================

export const STAKEHOLDER_INPUTS: StakeholderInput[] = [
  {
    id: "INP-001",
    from: "tech",
    date: "2026-03-15",
    gate: "G1",
    content: {
      en: "TiO2 coating uniformity on first batch of lamps shows 3 of 8 with patchy coverage per SEM analysis. Need to refine deposition process before efficiency validation.",
      cn: "首批灯管的TiO2涂层均匀性SEM分析显示8个中有3个覆盖不均。需在效率验证前改进沉积工艺。",
    },
    status: "pending-review",
    pmpResponse: null,
  },
  {
    id: "INP-002",
    from: "business",
    date: "2026-03-10",
    gate: "G3",
    content: {
      en: "FDA small business fee discount application submitted. Confirmed eligible for reduced 510(k) user fee (~$4,400 vs $21,760). Approval expected within 30 days.",
      cn: "FDA小企业费用折扣申请已提交。确认有资格获得减免510(k)用户费（约$4,400 vs $21,760）。预计30天内获批。",
    },
    status: "accepted",
    pmpResponse: {
      en: "Approved. Budget updated to reflect reduced FDA fee.",
      cn: "已批准。预算已更新以反映减免FDA费用。",
    },
  },
];

// ============================================================
// CHANGE REQUEST QUEUE — PMP approval workflow
// ============================================================

export const CHANGE_REQUESTS: ChangeRequest[] = [];

// ============================================================
// AUDIT TRAIL — All actions logged for DHF traceability
// ============================================================

export const AUDIT_LOG: AuditEntry[] = [
  {
    id: "AUD-001",
    timestamp: "2026-03-15T09:30:00Z",
    user: "PMP",
    action: "gate-criteria",
    targetId: "G1",
    field: "criteria[0].met",
    oldValue: "false",
    newValue: "true",
    detail: "Marked UV-C reactor prototype criterion as met — T1 complete",
  },
  {
    id: "AUD-002",
    timestamp: "2026-03-14T14:15:00Z",
    user: "PMP",
    action: "milestone-status",
    targetId: "T1",
    field: "status",
    oldValue: "in-progress",
    newValue: "complete",
    detail: "UV-C reactor prototype finalization confirmed complete",
  },
  {
    id: "AUD-003",
    timestamp: "2026-03-12T11:00:00Z",
    user: "PMP",
    action: "risk-field",
    targetId: "RISK-001",
    field: "mitigationStatus",
    oldValue: "not-started",
    newValue: "in-progress",
    detail:
      "Ozone emission mitigation work started — 254nm lamp spectrum verified",
  },
];

// ============================================================
// DHF DOCUMENT TRACKER — Design History File
// ============================================================

export const DHF_DOCUMENTS: DHFDocument[] = [
  {
    id: "DHF-001",
    code: "DHF-DP",
    title: { en: "Design Plan", cn: "设计计划" },
    category: "Design Controls",
    owner: "tech",
    status: "approved",
    dueMonth: 0,
    notes: "",
  },
  {
    id: "DHF-002",
    code: "DHF-DI",
    title: { en: "Design Inputs", cn: "设计输入" },
    category: "Design Controls",
    owner: "tech",
    status: "in-review",
    dueMonth: 1,
    notes: "UV-C intensity, airflow CFM, ozone limits, microbial kill targets",
  },
  {
    id: "DHF-003",
    code: "DHF-DO",
    title: { en: "Design Outputs", cn: "设计输出" },
    category: "Design Controls",
    owner: "tech",
    status: "draft",
    dueMonth: 3,
    notes: "Reactor drawings, filter stack layout, wiring schematic",
  },
  {
    id: "DHF-004",
    code: "DHF-DV",
    title: { en: "Design Verification Report", cn: "设计验证报告" },
    category: "Verification",
    owner: "tech",
    status: "not-started",
    dueMonth: 5,
    notes: "Covers T4 CADR, T5 microbial, T6 electrical, T7 ozone results",
  },
  {
    id: "DHF-005",
    code: "DHF-VAL",
    title: { en: "Design Validation Report", cn: "设计确认报告" },
    category: "Validation",
    owner: "tech",
    status: "not-started",
    dueMonth: 6,
    notes: "",
  },
  {
    id: "DHF-006",
    code: "DHF-RA",
    title: { en: "Risk Analysis (ISO 14971)", cn: "风险分析（ISO 14971）" },
    category: "Risk Management",
    owner: "tech",
    status: "in-review",
    dueMonth: 2,
    notes: "Ozone, UV leakage, TiO2 nanoparticle, electrical risks",
  },
  {
    id: "DHF-007",
    code: "DHF-SE",
    title: {
      en: "Substantial Equivalence Discussion",
      cn: "实质等效性讨论",
    },
    category: "Regulatory",
    owner: "regulatory",
    status: "draft",
    dueMonth: 3,
    notes: "vs AiroCide K023830, Air Purifier 3707 K033448, ABRACAIR K050257",
  },
  {
    id: "DHF-008",
    code: "DHF-DD",
    title: {
      en: "Device Description & Block Diagrams",
      cn: "设备描述与框图",
    },
    category: "Submission",
    owner: "regulatory",
    status: "draft",
    dueMonth: 3,
    notes: "Air path diagram, reactor cross-section, labeled photos",
  },
  {
    id: "DHF-009",
    code: "DHF-UL",
    title: {
      en: "Electrical Safety Report (UL 507/867)",
      cn: "电气安全报告（UL 507/867）",
    },
    category: "Testing",
    owner: "tech",
    status: "not-started",
    dueMonth: 5,
    notes: "NRTL testing lab TBD",
  },
  {
    id: "DHF-010",
    code: "DHF-LBL",
    title: { en: "Labeling & IFU (21 CFR 801)", cn: "标签和IFU（21 CFR 801）" },
    category: "Labeling",
    owner: "regulatory",
    status: "draft",
    dueMonth: 5,
    notes: "CADR label, filter replacement instructions, UV safety warnings",
  },
  {
    id: "DHF-011",
    code: "DHF-CL",
    title: { en: "510(k) Cover Letter", cn: "510(k)附信" },
    category: "Submission",
    owner: "regulatory",
    status: "not-started",
    dueMonth: 6,
    notes: "",
  },
  {
    id: "DHF-012",
    code: "DHF-510K",
    title: {
      en: "510(k) Summary (21 CFR 807.92)",
      cn: "510(k)摘要（21 CFR 807.92）",
    },
    category: "Submission",
    owner: "regulatory",
    status: "in-review",
    dueMonth: 1,
    notes: "Drafted — pending legal review",
  },
];

// ============================================================
// CAPA LOG — Corrective & Preventive Actions
// ============================================================

export const CAPA_LOG: CAPAItem[] = [
  {
    id: "CAPA-001",
    type: "corrective",
    title: {
      en: "TiO2 Coating Non-Uniformity on UV-C Lamps",
      cn: "UV-C灯管TiO2涂层不均匀",
    },
    linkedRiskId: "RISK-003",
    description: {
      en: "SEM analysis of first batch showed 3/8 lamps with patchy TiO2 coverage. Corrective action: refine sol-gel deposition parameters — dip speed, withdrawal rate, and curing temperature.",
      cn: "首批SEM分析显示8个灯管中3个TiO2覆盖不均。纠正措施：优化溶胶-凝胶沉积参数——浸入速度、抽出速率和固化温度。",
    },
    owner: "Materials Engineer",
    status: "in-progress",
    openedDate: "2026-03-10",
    dueDate: "2026-04-15",
    closedDate: null,
  },
  {
    id: "CAPA-002",
    type: "preventive",
    title: { en: "Ozone Emission Monitoring Protocol", cn: "臭氧排放监测协议" },
    linkedRiskId: "RISK-001",
    description: {
      en: "Preventive action: establish continuous ozone monitoring during all reactor testing. Document protocol for 8-hour test at max fan speed per FDA 21 CFR 801.415.",
      cn: "预防措施：在所有反应器测试期间建立连续臭氧监测。记录按FDA 21 CFR 801.415最大风扇速度8小时测试协议。",
    },
    owner: "Test Engineer",
    status: "open",
    openedDate: "2026-03-05",
    dueDate: "2026-05-01",
    closedDate: null,
  },
  {
    id: "CAPA-003",
    type: "corrective",
    title: {
      en: "eCopy Formatting Deficiencies (2018 FDA Hold)",
      cn: "eCopy格式缺陷（2018年FDA暂停）",
    },
    linkedRiskId: "RISK-007",
    description: {
      en: "Original 2018 submission received FDA eCopy hold letter. Corrective: address all formatting issues identified — use current eSTAR template, validate with FDA eCopy tool before resubmission.",
      cn: "2018年原始提交收到FDA eCopy暂停信。纠正：解决所有确认的格式问题——使用当前eSTAR模板，重新提交前用FDA eCopy工具验证。",
    },
    owner: "Regulatory Lead",
    status: "in-progress",
    openedDate: "2026-02-20",
    dueDate: "2026-06-01",
    closedDate: null,
  },
  {
    id: "CAPA-004",
    type: "preventive",
    title: {
      en: "HEPA Filter Bypass Leakage Prevention",
      cn: "HEPA过滤器旁路泄漏预防",
    },
    linkedRiskId: "RISK-006",
    description: {
      en: "Preventive action: design gasket seal around HEPA element to prevent unfiltered air bypass. Include pressure drop testing at filter end-of-life to verify seal integrity throughout rated filter lifespan.",
      cn: "预防措施：在HEPA元件周围设计垫圈密封以防止未过滤空气旁路。包括过滤器寿命终止时的压降测试，以验证整个额定过滤器寿命期间的密封完整性。",
    },
    owner: "Mechanical Engineer",
    status: "open",
    openedDate: "2026-03-01",
    dueDate: "2026-04-30",
    closedDate: null,
  },
];

// ============================================================
// ACTION ITEMS / TASK BOARD
// ============================================================

export const ACTION_ITEMS: ActionItem[] = [
  {
    id: "ACT-001",
    title: {
      en: "Refine TiO2 sol-gel deposition process",
      cn: "优化TiO2溶胶-凝胶沉积工艺",
    },
    assignee: "Materials Engineer",
    owner: "tech",
    priority: "high",
    status: "in-progress",
    dueDate: "2026-04-01",
    linkedGate: "G1",
    notes: "SEM verification after each batch",
  },
  {
    id: "ACT-002",
    title: {
      en: "Finalize SE comparison table (3 predicates)",
      cn: "完成SE比较表（3个前置设备）",
    },
    assignee: "Regulatory Lead",
    owner: "regulatory",
    priority: "high",
    status: "in-progress",
    dueDate: "2026-04-10",
    linkedGate: "G3",
    notes: "",
  },
  {
    id: "ACT-003",
    title: {
      en: "Draft risk analysis report (ISO 14971)",
      cn: "起草风险分析报告（ISO 14971）",
    },
    assignee: "Quality Mgr",
    owner: "tech",
    priority: "high",
    status: "in-progress",
    dueDate: "2026-04-15",
    linkedGate: "G1",
    notes: "",
  },
  {
    id: "ACT-004",
    title: {
      en: "Source HEPA filter & activated carbon suppliers",
      cn: "寻找HEPA过滤器和活性炭供应商",
    },
    assignee: "Procurement",
    owner: "tech",
    priority: "medium",
    status: "todo",
    dueDate: "2026-05-01",
    linkedGate: null,
    notes: "",
  },
  {
    id: "ACT-005",
    title: {
      en: "Submit FDA small business fee discount application",
      cn: "提交FDA小企业费用折扣申请",
    },
    assignee: "Admin",
    owner: "business",
    priority: "medium",
    status: "done",
    dueDate: "2026-03-15",
    linkedGate: null,
    notes: "",
  },
  {
    id: "ACT-006",
    title: {
      en: "Identify NRTL for UL 507/867 testing",
      cn: "确定UL 507/867测试的NRTL",
    },
    assignee: "Quality Mgr",
    owner: "regulatory",
    priority: "high",
    status: "todo",
    dueDate: "2026-04-20",
    linkedGate: "G2",
    notes: "Get quotes from Intertek, UL, CSA",
  },
  {
    id: "ACT-007",
    title: {
      en: "Order UV-C radiometer for reactor intensity testing",
      cn: "订购UV-C辐射计用于反应器强度测试",
    },
    assignee: "Lab Tech",
    owner: "tech",
    priority: "low",
    status: "blocked",
    dueDate: "2026-05-01",
    linkedGate: null,
    notes: "Waiting for equipment budget approval",
  },
  {
    id: "ACT-008",
    title: {
      en: "Provisional patent application — reactor design",
      cn: "临时专利申请——反应器设计",
    },
    assignee: "Patent Attorney",
    owner: "business",
    priority: "high",
    status: "in-progress",
    dueDate: "2026-04-05",
    linkedGate: null,
    notes: "",
  },
];

// ============================================================
// BUDGET vs ACTUAL — Category-level tracking
// ============================================================

export const BUDGET_CATEGORIES: BudgetCategory[] = [
  {
    id: "BUD-001",
    label: { en: "Prototype & Materials", cn: "原型和材料" },
    planned: 18000,
    actual: 14500,
    notes: "UV lamps, TiO2 powder, fan motors, enclosure",
  },
  {
    id: "BUD-002",
    label: {
      en: "Lab Testing (UL/Microbial/Ozone)",
      cn: "实验室测试（UL/微生物/臭氧）",
    },
    planned: 35000,
    actual: 5000,
    notes: "Major spend at M+4 (NRTL + microbiology lab)",
  },
  {
    id: "BUD-003",
    label: { en: "Regulatory & Legal", cn: "法规和法律" },
    planned: 15000,
    actual: 8500,
    notes: "FDA fee, patent attorney, trademark filing",
  },
  {
    id: "BUD-004",
    label: { en: "Personnel (Contract)", cn: "人员（合同）" },
    planned: 42000,
    actual: 22000,
    notes: "Part-time consultants — regulatory, materials, testing",
  },
  {
    id: "BUD-005",
    label: { en: "HEPA & Carbon Filters", cn: "HEPA和碳过滤器" },
    planned: 8000,
    actual: 3200,
    notes: "Filter media evaluation + production samples",
  },
  {
    id: "BUD-006",
    label: { en: "Equipment & Instruments", cn: "设备和仪器" },
    planned: 12000,
    actual: 7800,
    notes: "UV-C radiometer, ozone monitor, anemometer",
  },
  {
    id: "BUD-007",
    label: { en: "Production Tooling", cn: "生产工装" },
    planned: 20000,
    actual: 2000,
    notes: "Enclosure mold, assembly fixtures — starts M+7",
  },
  {
    id: "BUD-008",
    label: { en: "Miscellaneous & Contingency", cn: "杂项与应急" },
    planned: 10000,
    actual: 2000,
    notes: "Shipping, samples, unforeseen expenses",
  },
];

// ============================================================
// RESOURCE ALLOCATION — Team capacity view
// ============================================================

export const TEAM_MEMBERS: TeamMember[] = [
  {
    id: "TM-001",
    name: "Alex Chen",
    role: {
      en: "Project Lead & Regulatory Affairs",
      cn: "项目负责人与法规事务",
    },
    allocation: [
      { workstream: "510(k) Preparation", pct: 35 },
      { workstream: "Standards Compliance", pct: 20 },
      { workstream: "Business Development", pct: 20 },
      { workstream: "Project Management", pct: 25 },
    ],
    capacity: 100,
  },
  {
    id: "TM-002",
    name: "Maria Santos",
    role: { en: "Mechanical & Materials Engineer", cn: "机械与材料工程师" },
    allocation: [
      { workstream: "Reactor Design", pct: 40 },
      { workstream: "Filter Integration", pct: 25 },
      { workstream: "Production Tooling", pct: 20 },
      { workstream: "Documentation", pct: 15 },
    ],
    capacity: 100,
  },
  {
    id: "TM-003",
    name: "James Park",
    role: {
      en: "Photocatalysis & Testing Specialist",
      cn: "光催化与测试专家",
    },
    allocation: [
      { workstream: "TiO2 Coating Process", pct: 35 },
      { workstream: "Microbial Testing", pct: 30 },
      { workstream: "Ozone/Safety Testing", pct: 25 },
      { workstream: "Lab Operations", pct: 10 },
    ],
    capacity: 100,
  },
];

// ============================================================
// SUPPLIER / VENDOR TRACKER
// ============================================================

export const SUPPLIERS: Supplier[] = [
  {
    id: "SUP-001",
    name: "UVP Lighting",
    component: {
      en: '2½" Fluorescent UV-C Lamps (254nm)',
      cn: '2½"荧光UV-C灯管（254nm）',
    },
    status: "active",
    leadTimeDays: 14,
    poStatus: "PO-2026-001 Delivered",
    contractMfgMilestone: "M+0",
    notes: "Confirmed 254nm — no 185nm emission",
  },
  {
    id: "SUP-002",
    name: "NanoTech Coatings",
    component: {
      en: "TiO2 Nanoparticle Powder (Sol-Gel Grade)",
      cn: "TiO2纳米颗粒粉末（溶胶-凝胶级）",
    },
    status: "active",
    leadTimeDays: 21,
    poStatus: "PO-2026-003 Delivered",
    contractMfgMilestone: "M+0",
    notes: "Anatase phase, 25nm particle size",
  },
  {
    id: "SUP-003",
    name: "FilterPro Industries",
    component: {
      en: "HEPA Filter Media (H13 Grade)",
      cn: "HEPA过滤介质（H13级）",
    },
    status: "under-review",
    leadTimeDays: 28,
    poStatus: "Samples Received",
    contractMfgMilestone: "M+2",
    notes: "99.97% @ 0.3µm certified",
  },
  {
    id: "SUP-004",
    name: "CocoCarbon Ltd.",
    component: { en: "Activated Carbon (Coconut Shell)", cn: "活性炭（椰壳）" },
    status: "active",
    leadTimeDays: 14,
    poStatus: "PO-2026-005 Delivered",
    contractMfgMilestone: "M+0",
    notes: "Oxygen-treated for max porosity",
  },
  {
    id: "SUP-005",
    name: "MotorTech Asia",
    component: {
      en: "Variable-Speed DC Fan Motor",
      cn: "变速直流风扇电机",
    },
    status: "qualified",
    leadTimeDays: 35,
    poStatus: "RFQ Sent",
    contractMfgMilestone: "M+3",
    notes: "3-speed, ≤45W at max, UL listed",
  },
  {
    id: "SUP-006",
    name: "Pacific Enclosures",
    component: { en: "ABS Housing & Assembly", cn: "ABS外壳与组装" },
    status: "under-review",
    leadTimeDays: 45,
    poStatus: "Design Review",
    contractMfgMilestone: "M+6",
    notes: "Injection mold tooling quote pending",
  },
];

// ============================================================
// MESSAGE BOARD SECTIONS
// ============================================================

export const QA_SECTIONS: QASection[] = [
  {
    num: 1,
    title: {
      en: "UV-C Reactor & Photocatalysis Design",
      cn: "UV-C反应器与光催化设计",
    },
    context: {
      en: "The core technology is a 254nm UV-C fluorescent lamp illuminating a TiO2-nanocoated substrate to generate hydroxyl radicals. Design freeze is targeted at G1 (M+2).",
      cn: "核心技术是254nm UV-C荧光灯照射TiO2纳米涂层基材以产生羟基自由基。设计冻结目标为G1（M+2）。",
    },
    questions: [
      {
        num: 1,
        question: {
          en: "Describe the current UV-C lamp specification. Is the 2½-inch fluorescent tube at 254nm the final production lamp, or are you evaluating alternatives?",
          cn: "描述当前UV-C灯规格。2½英寸254nm荧光灯管是最终生产灯还是仍在评估替代方案？",
        },
        why: {
          en: "The 510(k) device description must specify exact lamp model and wavelength. Changes after submission trigger an amendment.",
          cn: "510(k)设备描述必须指定确切灯型号和波长。提交后更改将触发修订。",
        },
        followUps: [
          {
            en: "What is the rated lamp life in hours? What is the replacement interval?",
            cn: "灯的额定寿命是多少小时？更换间隔是多少？",
          },
          {
            en: "Is the UV-C output measured in mW/cm² at the TiO2 surface? What is the current reading?",
            cn: "UV-C输出是否以mW/cm²在TiO2表面测量？当前读数是多少？",
          },
          {
            en: "Are UV-C LEDs being considered as a future alternative to fluorescent?",
            cn: "是否考虑将UV-C LED作为荧光灯的未来替代方案？",
          },
        ],
      },
      {
        num: 2,
        question: {
          en: "What is the TiO2 coating process? Anatase phase at 25nm particle size -- how is the coating applied to the substrate, and what is the uniformity spec?",
          cn: "TiO2涂层工艺是什么？锐钛矿相25nm粒径——涂层如何施加到基材上？均匀性规格是什么？",
        },
        why: {
          en: "CAPA-001 flagged TiO2 coating uniformity as a corrective action. Inconsistent coating directly impacts photocatalytic efficiency.",
          cn: "CAPA-001将TiO2涂层均匀性标记为纠正措施。涂层不一致直接影响光催化效率。",
        },
        followUps: [
          {
            en: "Is the coating applied by dip, spray, or sputtering?",
            cn: "涂层是浸渍、喷涂还是溅射？",
          },
          {
            en: "What is the acceptance criteria for coating thickness variation?",
            cn: "涂层厚度变化的验收标准是什么？",
          },
          {
            en: "How is coating quality verified in production -- visual inspection or instrument?",
            cn: "生产中如何验证涂层质量——目视检查还是仪器？",
          },
        ],
      },
      {
        num: 3,
        question: {
          en: "Explain the photocatalytic reaction mechanism. The 510(k) claims hydroxyl radical (OH⁻) generation decomposes organics to H₂O + CO₂. What evidence supports this claim?",
          cn: "解释光催化反应机制。510(k)声称羟基自由基（OH⁻）生成可将有机物分解为H₂O + CO₂。什么证据支持这一声明？",
        },
        why: {
          en: "FDA reviewers may question the mechanism of action. Published literature and bench test data will be needed for the SE discussion.",
          cn: "FDA审查人员可能质疑作用机制。实质等价讨论需要已发表文献和台架测试数据。",
        },
        followUps: [
          {
            en: "Have you measured radical generation rate under operating conditions?",
            cn: "是否在工作条件下测量了自由基生成速率？",
          },
          {
            en: "Does the predicate AiroCide (K023830) describe its mechanism similarly?",
            cn: "对照设备AiroCide（K023830）是否类似描述其机制？",
          },
          {
            en: "Are super-oxide anions (O₂*) also generated? If so, are they claimed in the submission?",
            cn: "是否也生成超氧阴离子（O₂*）？如果是，是否在提交中声明？",
          },
        ],
      },
      {
        num: 4,
        question: {
          en: "What is the reactor chamber geometry? What is the airflow path -- does air pass directly over the TiO2 surface, or through a separate reaction zone?",
          cn: "反应腔的几何形状是什么？气流路径如何——空气直接通过TiO2表面还是经过单独的反应区？",
        },
        why: {
          en: "Contact time between UV-activated TiO2 and airborne contaminants determines efficacy. Chamber design is critical for CADR claims.",
          cn: "UV激活的TiO2与空气污染物的接触时间决定了效能。腔室设计对CADR声明至关重要。",
        },
        followUps: [
          {
            en: "What is the calculated dwell time of air in the reactor at max fan speed?",
            cn: "在最大风速下空气在反应器中的计算停留时间是多少？",
          },
          {
            en: "Has CFD modeling been performed on the airflow path?",
            cn: "是否对气流路径进行了CFD建模？",
          },
          {
            en: "Is there any concern about UV-C degrading the ABS enclosure material over time?",
            cn: "是否担心UV-C会随时间降解ABS外壳材料？",
          },
        ],
      },
    ],
  },
  {
    num: 2,
    title: {
      en: "Filtration System & CADR Performance",
      cn: "过滤系统与CADR性能",
    },
    context: {
      en: "The device uses a multi-stage filtration approach: HEPA H13, activated carbon (coconut shell), and TiO2 photocatalysis. CADR testing per ANSI/AHAM AC-1 is planned for M+4.",
      cn: "设备采用多级过滤方法：HEPA H13、活性炭（椰壳）和TiO2光催化。按ANSI/AHAM AC-1标准的CADR测试计划在M+4进行。",
    },
    questions: [
      {
        num: 5,
        question: {
          en: "Is the HEPA filter a true H13 grade (99.97% at 0.3µm)? Has the filter media been independently tested and certified?",
          cn: "HEPA过滤器是否为真正的H13级（0.3µm处99.97%）？滤材是否经过独立测试和认证？",
        },
        why: {
          en: "FDA and FTC both scrutinize HEPA claims. FilterPro samples have been received -- need cert documentation.",
          cn: "FDA和FTC都严格审查HEPA声明。FilterPro样品已收到——需要认证文件。",
        },
        followUps: [
          {
            en: "What is the filter effective area and pleat count?",
            cn: "过滤器的有效面积和褶皱数是多少？",
          },
          {
            en: "What is the expected filter replacement interval?",
            cn: "预期的过滤器更换间隔是多少？",
          },
          {
            en: "Does the device include a filter replacement indicator?",
            cn: "设备是否包含过滤器更换指示器？",
          },
        ],
      },
      {
        num: 6,
        question: {
          en: "Describe the activated carbon stage. Coconut shell carbon -- what is the adsorption capacity for formaldehyde and VOCs?",
          cn: "描述活性炭阶段。椰壳炭——对甲醛和VOC的吸附能力是多少？",
        },
        why: {
          en: "If the 510(k) claims VOC reduction, specific adsorption data is required. This differentiates from HEPA-only predicates.",
          cn: "如果510(k)声明VOC减少，需要具体吸附数据。这与纯HEPA对照设备有所区分。",
        },
        followUps: [
          {
            en: "Is the carbon oxygen-treated? What is the BET surface area?",
            cn: "活性炭是否经过氧处理？BET比表面积是多少？",
          },
          {
            en: "How much carbon (grams) is in each filter cartridge?",
            cn: "每个过滤器滤芯中有多少克活性炭？",
          },
          {
            en: "What is the carbon saturation life at typical indoor VOC concentrations?",
            cn: "在典型室内VOC浓度下活性炭的饱和寿命是多少？",
          },
        ],
      },
      {
        num: 7,
        question: {
          en: "What CADR values are you targeting? Smoke, dust, and pollen -- or only microbial reduction?",
          cn: "你的目标CADR值是多少？烟雾、灰尘和花粉——还是仅微生物减少？",
        },
        why: {
          en: "T4 (Airflow/CFM Testing) is targeted M+4. ANSI/AHAM AC-1 testing needs clear performance targets before starting.",
          cn: "T4（气流/CFM测试）目标M+4。ANSI/AHAM AC-1测试在开始前需要明确性能目标。",
        },
        followUps: [
          {
            en: "What room size is the device rated for (sq ft)?",
            cn: "设备额定适用房间面积是多少（平方英尺）？",
          },
          {
            en: "What is the airflow rate at each fan speed setting?",
            cn: "每个风速设置下的气流速率是多少？",
          },
          {
            en: "Has any preliminary CADR testing been done, even informal?",
            cn: "是否进行过任何初步CADR测试，即使是非正式的？",
          },
        ],
      },
      {
        num: 8,
        question: {
          en: "What is the filtration sequence? Does air hit HEPA first, then carbon, then TiO2 reactor -- or a different order?",
          cn: "过滤顺序是什么？空气先到HEPA，然后是活性炭，再到TiO2反应器——还是不同的顺序？",
        },
        why: {
          en: "Filter sequence affects both performance and maintenance. HEPA first protects the TiO2 coating from particulate fouling.",
          cn: "过滤顺序影响性能和维护。HEPA在前可保护TiO2涂层免受颗粒污染。",
        },
        followUps: [
          {
            en: "Is there a pre-filter for large particles before the HEPA?",
            cn: "HEPA前是否有大颗粒预过滤器？",
          },
          {
            en: "Is the filter cartridge a single integrated unit or separate stages?",
            cn: "过滤器滤芯是单一集成单元还是分阶段？",
          },
        ],
      },
    ],
  },
  {
    num: 3,
    title: {
      en: "Ozone Safety & Emission Compliance",
      cn: "臭氧安全与排放合规",
    },
    context: {
      en: "UV-C photocatalysis can generate ozone as a byproduct. RISK-001 (ozone >50ppb) is rated RED. UL 867 and 21 CFR 801.415 set strict ozone limits.",
      cn: "UV-C光催化可能产生臭氧作为副产品。RISK-001（臭氧>50ppb）评级为红色。UL 867和21 CFR 801.415设定了严格的臭氧限值。",
    },
    questions: [
      {
        num: 9,
        question: {
          en: "What is the current measured ozone output at maximum fan speed? Has any formal ozone emission testing been performed?",
          cn: "最大风速下当前测量的臭氧输出是多少？是否进行过任何正式的臭氧排放测试？",
        },
        why: {
          en: "UL 867 limits ozone to 50 ppb for consumer devices. 21 CFR 801.415 mandates labeling for any device emitting ozone. This is a pass/fail gate.",
          cn: "UL 867将消费设备的臭氧限制在50ppb。21 CFR 801.415要求任何排放臭氧的设备进行标记。这是通过/失败门槛。",
        },
        followUps: [
          {
            en: "What instrument was used for ozone measurement? Calibrated?",
            cn: "使用什么仪器测量臭氧？是否校准？",
          },
          {
            en: "Is the 254nm wavelength optimal for minimizing ozone generation vs. 185nm?",
            cn: "254nm波长对比185nm是否最优减少臭氧生成？",
          },
          {
            en: "Does the activated carbon stage adequately scrub residual ozone?",
            cn: "活性炭阶段是否足以清除残余臭氧？",
          },
        ],
      },
      {
        num: 10,
        question: {
          en: "CAPA-002 established an ozone monitoring protocol. What does this protocol entail, and have test results been documented?",
          cn: "CAPA-002建立了臭氧监测协议。该协议包含什么内容？测试结果是否已记录？",
        },
        why: {
          en: "CAPA-002 is open with effectiveness checks pending. Need to verify the corrective action is actually working.",
          cn: "CAPA-002已开放但有效性检查待完成。需要验证纠正措施是否实际有效。",
        },
        followUps: [
          {
            en: "How frequently is ozone measured during testing -- continuous or spot-check?",
            cn: "测试期间臭氧测量频率是多少——连续还是抽查？",
          },
          {
            en: "What is the plan if ozone exceeds 50ppb under any operating condition?",
            cn: "如果在任何工作条件下臭氧超过50ppb，计划是什么？",
          },
        ],
      },
      {
        num: 11,
        question: {
          en: "Does the predicate AiroCide TiO2 (K023830) have any ozone-related labeling or warnings? How does their approach compare?",
          cn: "对照设备AiroCide TiO2（K023830）是否有与臭氧相关的标签或警告？他们的方法如何比较？",
        },
        why: {
          en: "Substantial equivalence requires comparison of safety profiles. If the predicate has ozone warnings, we likely need them too.",
          cn: "实质等价要求比较安全性。如果对照设备有臭氧警告，我们也可能需要。",
        },
        followUps: [
          {
            en: "Have you obtained the AiroCide SSED from the FDA database?",
            cn: "你是否从FDA数据库获取了AiroCide的SSED？",
          },
          {
            en: "Does the Air Purifier 3707 UVC (K033448) predicate have ozone data?",
            cn: "Air Purifier 3707 UVC（K033448）对照设备是否有臭氧数据？",
          },
        ],
      },
      {
        num: 12,
        question: {
          en: "Is there a hardware interlock that shuts off the UV-C lamp if the fan motor fails, preventing ozone accumulation?",
          cn: "是否有硬件联锁装置在风扇电机故障时关闭UV-C灯，防止臭氧积累？",
        },
        why: {
          en: "Risk mitigation for RISK-001. If the fan stops but UV stays on, confined ozone concentration could spike.",
          cn: "RISK-001的风险缓解。如果风扇停止但UV继续工作，密闭空间臭氧浓度可能飙升。",
        },
        followUps: [
          {
            en: "Is this interlock in the current prototype, or only planned?",
            cn: "该联锁装置是否在当前原型中？还是仅在计划中？",
          },
          {
            en: "Is the interlock tested as part of the electrical safety verification?",
            cn: "联锁装置是否作为电气安全验证的一部分进行测试？",
          },
        ],
      },
    ],
  },
  {
    num: 4,
    title: {
      en: "Microbial Efficacy & Testing Protocol",
      cn: "微生物效能与测试方案",
    },
    context: {
      en: "The intended use claims reduction of viable airborne bacteria, mold, and spores. T5 (Microbial Kill Rate Testing) is targeted M+5. Predicate comparison is key for SE.",
      cn: "预期用途声称减少可存活的空气中细菌、霉菌和孢子。T5（微生物杀灭率测试）目标M+5。对照设备比较是SE的关键。",
    },
    questions: [
      {
        num: 13,
        question: {
          en: "What test organisms are planned for microbial kill rate testing? ATCC reference strains? What log-reduction are you targeting?",
          cn: "微生物杀灭率测试计划使用什么测试微生物？ATCC参考菌株？目标对数减少是多少？",
        },
        why: {
          en: "FDA expects standard test organisms for air purifier claims. Minimum 3-log reduction is typical for 510(k) air purification devices.",
          cn: "FDA期望空气净化器声明使用标准测试微生物。510(k)空气净化设备通常要求最低3-log减少。",
        },
        followUps: [
          {
            en: "Staphylococcus aureus, Aspergillus niger -- confirmed as primary test organisms?",
            cn: "金黄色葡萄球菌、黑曲霉——确认为主要测试微生物？",
          },
          {
            en: "What chamber volume and exposure time will be used?",
            cn: "将使用什么腔室体积和暴露时间？",
          },
          {
            en: "Will testing be done at an accredited microbiology lab?",
            cn: "测试是否将在认可的微生物实验室进行？",
          },
        ],
      },
      {
        num: 14,
        question: {
          en: "RISK-004 flags insufficient microbial kill rate (<99% single-pass). What is the current prototype achieving on bench tests?",
          cn: "RISK-004标记微生物杀灭率不足（单次通过<99%）。当前原型在台架测试中达到了什么水平？",
        },
        why: {
          en: "If single-pass efficacy is low, we may need to recirculate or increase UV-C intensity. This affects CADR and power consumption.",
          cn: "如果单次通过效率低，我们可能需要再循环或增加UV-C强度。这影响CADR和功耗。",
        },
        followUps: [
          {
            en: "What is the relationship between fan speed and kill rate?",
            cn: "风速与杀灭率之间的关系是什么？",
          },
          {
            en: "Is there a minimum dwell time in the UV-C chamber for effective kill?",
            cn: "UV-C腔室中是否有有效杀灭的最短停留时间？",
          },
          {
            en: "How does kill rate vary between bacteria, mold, and spores?",
            cn: "杀灭率在细菌、霉菌和孢子之间如何变化？",
          },
        ],
      },
      {
        num: 15,
        question: {
          en: "How do the predicates' efficacy claims compare to ours? AiroCide K023830 specifically -- what organisms and reductions did they demonstrate?",
          cn: "对照设备的效能声明与我们的相比如何？特别是AiroCide K023830——他们展示了什么微生物和减少率？",
        },
        why: {
          en: "SE discussion Section 5 requires performance comparison. Our claims cannot exceed the predicate without additional clinical data.",
          cn: "SE讨论第5节要求性能比较。我们的声明不能超过对照设备，除非有额外的临床数据。",
        },
        followUps: [
          {
            en: "Have you reviewed the AiroCide 510(k) summary for test methodology?",
            cn: "你是否审查了AiroCide 510(k)摘要的测试方法？",
          },
          {
            en: "Does ABRACAIR (QTZ predicate) publish efficacy data?",
            cn: "ABRACAIR（QTZ对照设备）是否公布了效能数据？",
          },
        ],
      },
    ],
  },
  {
    num: 5,
    title: {
      en: "Electrical Safety & UL Compliance",
      cn: "电气安全与UL合规",
    },
    context: {
      en: "UL 507 (Electric Fans) and UL 867 (Electrostatic Air Cleaners) are primary safety standards. T6 (Electrical Safety/UL Testing) is targeted M+5. The device uses mains AC power.",
      cn: "UL 507（电风扇）和UL 867（静电空气净化器）是主要安全标准。T6（电气安全/UL测试）目标M+5。设备使用交流电源。",
    },
    questions: [
      {
        num: 16,
        question: {
          en: "Has the device undergone ANY formal UL 507 or UL 867 testing? Even preliminary bench checks?",
          cn: "设备是否进行过任何正式的UL 507或UL 867测试？即使是初步台架检查？",
        },
        why: {
          en: "STD-01 (UL 507) is at 20% progress. Need to understand what has actually been tested.",
          cn: "STD-01（UL 507）进度20%。需要了解实际测试了什么。",
        },
        followUps: [
          {
            en: "Which NRTL (Nationally Recognized Testing Lab) will perform UL testing?",
            cn: "哪个NRTL（国家认可测试实验室）将进行UL测试？",
          },
          {
            en: "What is the estimated cost and timeline for full UL certification?",
            cn: "全面UL认证的预计成本和时间是多少？",
          },
          {
            en: "Is UL listing required before 510(k) submission, or can it come after?",
            cn: "UL认证是否需要在510(k)提交前完成，还是可以在之后？",
          },
        ],
      },
      {
        num: 17,
        question: {
          en: "Describe the power supply design. Is the UV-C lamp ballast integrated or external? What are the input voltage/current specs?",
          cn: "描述电源设计。UV-C灯镇流器是集成的还是外置的？输入电压/电流规格是什么？",
        },
        why: {
          en: "IEC 60335-2-65 (air cleaning appliances) requires specific insulation and grounding. The ballast is a potential failure point.",
          cn: "IEC 60335-2-65（空气净化器具）要求特定绝缘和接地。镇流器是潜在故障点。",
        },
        followUps: [
          {
            en: "Is the device single-voltage (120V) or universal input?",
            cn: "设备是单电压（120V）还是通用输入？",
          },
          {
            en: "What fuse or circuit protection is included?",
            cn: "包含什么保险丝或电路保护？",
          },
          {
            en: "Is the power cord detachable? If so, what connector type?",
            cn: "电源线是否可拆卸？如果是，什么连接器类型？",
          },
        ],
      },
      {
        num: 18,
        question: {
          en: "RISK-002 flags UV-C radiation leakage. What shielding is in place, and has UV leakage been measured at the enclosure exterior?",
          cn: "RISK-002标记UV-C辐射泄漏。有什么屏蔽措施？是否在外壳外部测量了UV泄漏？",
        },
        why: {
          en: "UV-C at 254nm is harmful to skin and eyes. RISK-002 is rated YELLOW. An interlock on the access panel is listed as mitigation.",
          cn: "254nm UV-C对皮肤和眼睛有害。RISK-002评级为黄色。进入面板上的联锁装置被列为缓解措施。",
        },
        followUps: [
          {
            en: "Is there an interlock that kills UV-C power when the filter door is opened?",
            cn: "当过滤器门打开时是否有切断UV-C电源的联锁装置？",
          },
          {
            en: "What UV-C exposure limit standard is being followed (ACGIH TLV)?",
            cn: "遵循什么UV-C暴露限值标准（ACGIH TLV）？",
          },
          {
            en: "Is there a UV-C indicator light visible to the user?",
            cn: "是否有用户可见的UV-C指示灯？",
          },
        ],
      },
      {
        num: 19,
        question: {
          en: "Fan motor noise level -- IEC 60704 specifies measurement methods. What are the measured dB(A) levels at each speed setting?",
          cn: "风扇电机噪音水平——IEC 60704规定了测量方法。每个速度设置下测量的dB(A)水平是多少？",
        },
        why: {
          en: "Noise affects usability in medical settings. Predicate devices typically operate at <55 dB(A). Need comparative data.",
          cn: "噪音影响医疗环境中的可用性。对照设备通常在<55 dB(A)下运行。需要比较数据。",
        },
        followUps: [
          {
            en: "What is the target noise level for the production unit?",
            cn: "生产单元的目标噪音水平是多少？",
          },
          {
            en: "Is motor vibration isolation included in the design?",
            cn: "设计中是否包含电机振动隔离？",
          },
        ],
      },
    ],
  },
  {
    num: 6,
    title: {
      en: "510(k) Regulatory Strategy & Substantial Equivalence",
      cn: "510(k)法规策略与实质等价",
    },
    context: {
      en: "Three predicate devices identified: AiroCide TiO2 (K023830), Air Purifier 3707 UVC (K033448), and ABRACAIR (QTZ300-60/QTZ100-24). eCopy hold letter received July 2018 -- submission was incomplete.",
      cn: "已确定三个对照设备：AiroCide TiO2（K023830）、Air Purifier 3707 UVC（K033448）和ABRACAIR（QTZ300-60/QTZ100-24）。2018年7月收到eCopy暂停通知——提交不完整。",
    },
    questions: [
      {
        num: 20,
        question: {
          en: "The 2018 eCopy hold letter indicated the submission was incomplete. What specific deficiencies were cited, and have they been addressed?",
          cn: "2018年eCopy暂停通知指出提交不完整。引用了哪些具体缺陷？这些缺陷是否已解决？",
        },
        why: {
          en: "Understanding the prior rejection is critical to avoid repeating mistakes. CAPA-003 (eCopy formatting) addresses part of this.",
          cn: "了解先前的拒绝对避免重复错误至关重要。CAPA-003（eCopy格式）解决了部分问题。",
        },
        followUps: [
          {
            en: "Was the hold due to missing sections, formatting errors, or content deficiencies?",
            cn: "暂停是由于缺少章节、格式错误还是内容缺陷？",
          },
          {
            en: "Has a new eCopy been prepared with the corrected format?",
            cn: "是否已准备了更正格式的新eCopy？",
          },
          {
            en: "Was the eCopy hold letter the only FDA communication, or were there follow-up requests?",
            cn: "eCopy暂停通知是唯一的FDA通信，还是有后续请求？",
          },
        ],
      },
      {
        num: 21,
        question: {
          en: "Which of the three predicates is strongest for SE? AiroCide K023830 uses the same TiO2 photocatalysis mechanism. Is that the primary predicate?",
          cn: "三个对照设备中哪个对SE最有利？AiroCide K023830使用相同的TiO2光催化机制。它是主要对照设备吗？",
        },
        why: {
          en: "RISK-007 (510k rejection) is rated YELLOW. Predicate selection is the single most important regulatory decision.",
          cn: "RISK-007（510k拒绝）评级为黄色。对照设备选择是最重要的法规决定。",
        },
        followUps: [
          {
            en: "Have you obtained and reviewed the AiroCide SSED from the FDA database?",
            cn: "你是否从FDA数据库获取并审查了AiroCide的SSED？",
          },
          {
            en: "What are the key differences between our device and AiroCide? New technology claims?",
            cn: "我们的设备与AiroCide之间的关键差异是什么？新技术声明？",
          },
          {
            en: "Is the Air Purifier 3707 UVC (K033448) still listed as an active cleared device?",
            cn: "Air Purifier 3707 UVC（K033448）是否仍列为有效已批准设备？",
          },
        ],
      },
      {
        num: 22,
        question: {
          en: "The device is classified under § 880.6500 (Medical Device Air Purifier), product code FRA, Class II. Has this classification been confirmed with FDA?",
          cn: "设备分类为§ 880.6500（医用空气净化器），产品代码FRA，II类。是否已与FDA确认此分类？",
        },
        why: {
          en: "Incorrect classification leads to rejection. Some air purifiers are classified as consumer devices (EPA regulated) rather than FDA Class II.",
          cn: "分类错误导致拒绝。一些空气净化器被分类为消费设备（EPA监管）而非FDA II类。",
        },
        followUps: [
          {
            en: "Has an FDA classification request been submitted?",
            cn: "是否已提交FDA分类请求？",
          },
          {
            en: "Are there any special controls for product code FRA?",
            cn: "产品代码FRA是否有特殊控制？",
          },
          {
            en: "Does the intended use statement clearly establish medical device status?",
            cn: "预期用途声明是否明确确立了医疗器械身份？",
          },
        ],
      },
      {
        num: 23,
        question: {
          en: "What is the SE comparison table status? Have the side-by-side comparisons of intended use, technology, and performance been drafted?",
          cn: "SE比较表的状态如何？是否已起草预期用途、技术和性能的并排比较？",
        },
        why: {
          en: "R3 (Device Description & SE Discussion) is at M+4. The comparison table is the core of the 510(k) submission.",
          cn: "R3（设备描述和SE讨论）在M+4。比较表是510(k)提交的核心。",
        },
        followUps: [
          {
            en: "Is the comparison table bilingual or English-only for FDA?",
            cn: "比较表是双语还是仅英文提交FDA？",
          },
          {
            en: "Are there any technological differences that could trigger a 'new intended use' determination?",
            cn: "是否有任何技术差异可能触发'新预期用途'判定？",
          },
        ],
      },
    ],
  },
  {
    num: 7,
    title: {
      en: "Manufacturing & Quality System",
      cn: "制造与质量体系",
    },
    context: {
      en: "Titania Labs is a small startup in Gresham, OR. 21 CFR 820 QMS compliance is required for FDA submission. Production assembly planning (T8) is at M+10.",
      cn: "Titania Labs是位于俄勒冈州格雷沙姆的小型创业公司。FDA提交需要符合21 CFR 820 QMS。生产装配计划（T8）在M+10。",
    },
    questions: [
      {
        num: 24,
        question: {
          en: "What is the current state of the Quality Management System? Is there a Quality Manual? Any SOPs written?",
          cn: "质量管理体系的当前状态如何？是否有质量手册？是否编写了任何SOP？",
        },
        why: {
          en: "R9 (Quality System/ISO) targets M+3 for QMS design complete. 21 CFR 820 compliance is a 510(k) prerequisite.",
          cn: "R9（质量体系/ISO）目标M+3完成QMS设计。21 CFR 820合规是510(k)先决条件。",
        },
        followUps: [
          {
            en: "Has a regulatory consultant been engaged for QMS development?",
            cn: "是否聘请了法规顾问进行QMS开发？",
          },
          {
            en: "Have any internal quality audits been performed?",
            cn: "是否进行过内部质量审核？",
          },
          {
            en: "Is there a Corrective and Preventive Action (CAPA) procedure in place?",
            cn: "是否有纠正和预防措施（CAPA）程序？",
          },
        ],
      },
      {
        num: 25,
        question: {
          en: "Where will the device be manufactured? In-house at Gresham, or contract manufacturing? What is the production capacity plan?",
          cn: "设备将在哪里制造？格雷沙姆内部还是合同制造？生产能力计划是什么？",
        },
        why: {
          en: "T8 (Production Assembly Documentation) targets M+10. Need to understand whether Titania Labs has manufacturing space and equipment.",
          cn: "T8（生产装配文件）目标M+10。需要了解Titania Labs是否有制造空间和设备。",
        },
        followUps: [
          {
            en: "What assembly steps are required? Manual or automated?",
            cn: "需要哪些装配步骤？手动还是自动？",
          },
          {
            en: "Is there a Device Master Record (DMR)?",
            cn: "是否有器械主记录（DMR）？",
          },
          {
            en: "What is the target production volume for Year 1?",
            cn: "第一年的目标生产量是多少？",
          },
        ],
      },
      {
        num: 26,
        question: {
          en: "Are there any single-source components with no alternate supplier? What is the supply chain risk?",
          cn: "是否有无替代供应商的单一来源组件？供应链风险是什么？",
        },
        why: {
          en: "6 suppliers tracked. UVP Lighting for UV-C lamps and NanoTech Coatings for TiO2 are both specialized -- need backup sources.",
          cn: "跟踪了6家供应商。UVP Lighting的UV-C灯和NanoTech Coatings的TiO2都是专业的——需要备用来源。",
        },
        followUps: [
          {
            en: "What is the longest lead-time component in the BOM?",
            cn: "BOM中交货时间最长的组件是什么？",
          },
          {
            en: "Are there qualified second sources for the UV-C lamp and TiO2 powder?",
            cn: "UV-C灯和TiO2粉末是否有合格的第二供应源？",
          },
          {
            en: "Has a supplier quality agreement been signed with critical suppliers?",
            cn: "是否与关键供应商签署了供应商质量协议？",
          },
        ],
      },
    ],
  },
  {
    num: 8,
    title: {
      en: "Commercial Launch & Post-Market Planning",
      cn: "商业推出与上市后计划",
    },
    context: {
      en: "G6 (Commercial Launch Authorization) is at M+12. Cash runway is 19 months at current burn. Funding strategy is critical for sustainability.",
      cn: "G6（商业推出授权）在M+12。按当前消耗速率现金跑道为19个月。资金策略对可持续性至关重要。",
    },
    questions: [
      {
        num: 27,
        question: {
          en: "What is the go-to-market strategy after 510(k) clearance? Direct sales, distributors, or online?",
          cn: "510(k)通过后的上市策略是什么？直销、分销商还是在线？",
        },
        why: {
          en: "G6 criteria requires 'Distribution channel agreements finalized.' Need visibility into commercial planning.",
          cn: "G6标准要求'分销渠道协议已最终确定。'需要了解商业规划。",
        },
        followUps: [
          {
            en: "What is the target unit price? Is there market research to support it?",
            cn: "目标单价是多少？是否有市场研究支持？",
          },
          {
            en: "Are you targeting hospitals, clinics, or consumer markets?",
            cn: "你的目标是医院、诊所还是消费市场？",
          },
          {
            en: "What is the competitive pricing landscape for medical-grade air purifiers?",
            cn: "医疗级空气净化器的竞争定价格局如何？",
          },
        ],
      },
      {
        num: 28,
        question: {
          en: "RISK-008 rates funding risk as YELLOW. The $165K runway at $8.5K/mo burn gives ~19 months. Is this realistic through 510(k) clearance?",
          cn: "RISK-008将资金风险评级为黄色。$165K跑道在$8.5K/月消耗下约19个月。这到510(k)通过是否现实？",
        },
        why: {
          en: "510(k) clearance (G5) is at M+10. The budget must cover testing, submission fees, and potential FDA additional information requests.",
          cn: "510(k)通过（G5）在M+10。预算必须覆盖测试、提交费用和可能的FDA补充信息请求。",
        },
        followUps: [
          {
            en: "What are the largest unfunded cost items between now and M+10?",
            cn: "从现在到M+10之间最大的未资助成本项目是什么？",
          },
          {
            en: "Is the $275K SBIR grant application in progress? What is the expected timeline?",
            cn: "$275K SBIR资助申请是否在进行中？预期时间是什么？",
          },
          {
            en: "What is the minimum spend to reach 510(k) submission if funding is delayed?",
            cn: "如果资金延迟，达到510(k)提交的最低支出是多少？",
          },
        ],
      },
      {
        num: 29,
        question: {
          en: "What post-market surveillance plan exists? 21 CFR 803 (MDR reporting) and complaint handling need to be in place before launch.",
          cn: "存在什么上市后监测计划？21 CFR 803（MDR报告）和投诉处理需要在上市前就位。",
        },
        why: {
          en: "FDA can inspect at any time after clearance. A functional complaint system and MDR procedure must exist at launch.",
          cn: "FDA可以在通过后随时检查。功能性投诉系统和MDR程序必须在上市时就位。",
        },
        followUps: [
          {
            en: "Will you implement a customer feedback tracking system?",
            cn: "你会实施客户反馈跟踪系统吗？",
          },
          {
            en: "Who is responsible for MDR reporting within Titania Labs?",
            cn: "Titania Labs内谁负责MDR报告？",
          },
        ],
      },
      {
        num: 30,
        question: {
          en: "Is there anything about this device -- technical limitations, failed experiments, known issues -- that hasn't been disclosed to the project team?",
          cn: "关于该设备——技术限制、失败的实验、已知问题——是否有尚未向项目团队披露的信息？",
        },
        why: {
          en: "Undisclosed issues found during FDA review are far more damaging than issues disclosed upfront during project planning.",
          cn: "FDA审查期间发现的未披露问题比项目计划期间提前披露的问题危害更大。",
        },
        followUps: [
          {
            en: "Were there any earlier prototype versions that failed or were abandoned?",
            cn: "是否有更早的原型版本失败或被放弃？",
          },
          {
            en: "Any prior regulatory interactions besides the 2018 eCopy hold?",
            cn: "除了2018年eCopy暂停外，是否有其他法规互动？",
          },
          {
            en: "Are there any known material compatibility or degradation issues with extended UV-C exposure?",
            cn: "是否有已知的材料兼容性或长期UV-C暴露降解问题？",
          },
        ],
      },
    ],
  },
];

// ============================================================
// ACTIVE ROLE — Controls UI permissions
// ============================================================

const ADMIN_KEY = "arch2026";
export const IS_ADMIN: boolean =
  new URLSearchParams(window.location.search).get("admin") === ADMIN_KEY;

export let ACTIVE_ROLE: UserRole = IS_ADMIN ? "pmp" : "business";

export function setActiveRole(role: UserRole): void {
  ACTIVE_ROLE = role;
}
