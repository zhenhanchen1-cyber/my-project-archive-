# 🚀 全景项目知识库与个人自研归档 (My Project Archive)

> 本仓库汇集了个人在日常研发、开源探索与 AI 协同开发中**搜过、调研过、使用过的全部 GitHub 开源项目**，以及**个人原创与自研的项目工程**。  
> 包含每个项目的核心功能定义与自研项目的极简复刻指南。

---

## 目录
- [一、搜过 / 用过的 GitHub 开源项目清单](#一搜过--用过的-github-开源项目清单)
  - [1. 逆向工程、网络与实用工具](#1-逆向工程网络与实用工具)
  - [2. 芯片微架构、3D-IC、EDA 与 RISC-V](#2-芯片微架构3d-ic-eda-与-risc-v)
  - [3. 大模型、分布式并行与 Agent 生态](#3-大模型分布式并行与-agent-生态)
  - [4. MiniMax H3 视频生成与 ComfyUI 加速](#4-minimax-h3-视频生成与-comfyui-加速)
  - [5. 创意动画、Web 3D 与生活工具](#5-创意动画web-3d-与生活工具)
- [二、个人原创 / 自研项目与极简复刻指南](#二个人原创--自研项目与极简复刻指南)

---

## 一、搜过 / 用过的 GitHub 开源项目清单

### 1. 逆向工程、网络与实用工具
| 项目仓库 | 做了什么 / 核心特性 |
| :--- | :--- |
| [morluto/rea](https://github.com/morluto/rea) | 全自动化智能逆向分析工具（REA），用 Agent 贯穿从应用层行为捕获、UI 动作追踪到底层 Native 二进制反编译与内存分析。 |
| [alsk1992/CloddsBot](https://github.com/alsk1992/CloddsBot) | 海外网盘与流媒体资源的自动化下载与中转机器人。 |
| [epiral/bb-sites](https://github.com/epiral/bb-sites) | `bb-browser` 爬取规则集合，预置了 Reddit、Twitter、GitHub 等站点的免登录数据提取适配器。 |
| [truelockmc/streambert](https://github.com/truelockmc/streambert) | 基于 Electron 的跨平台无广告电影、剧集与动漫流媒体聚合播放与下载器。 |
| [clash-verge-rev/clash-verge-rev](https://github.com/clash-verge-rev/clash-verge-rev) | 基于 Tauri 开发的现代跨平台 Clash 代理客户端 GUI。 |
| [2dust/v2rayN](https://github.com/2dust/v2rayN) | 经典 Windows GUI 代理工具，支持 Xray、V2Ray 与 sing-box 内核。 |
| [hmjz100/LinkSwift](https://github.com/hmjz100/LinkSwift) | 全网网盘免客户端直链解析脚本（支持百度、阿里云盘、夸克、迅雷、123云盘等）。 |
| [Accelerider/BaiduPanDownloadWinform](https://github.com/Accelerider/BaiduPanDownloadWinform) | Windows 客户端免官方限速的百度网盘下载辅助工具。 |
| [wuxx/openocd-toolbox](https://github.com/wuxx/openocd-toolbox) | 嵌入式 OpenOCD 烧录与离线调试工具箱。 |

### 2. 芯片微架构、3D-IC、EDA 与 RISC-V
| 项目仓库 | 做了什么 / 核心特性 |
| :--- | :--- |
| [OpenXiangShan/XiangShan](https://github.com/OpenXiangShan/XiangShan) | 中科院开源的高性能乱序执行 RISC-V 处理器核（“香山”处理器）。 |
| [pulp-platform/mempool](https://github.com/pulp-platform/mempool) | 苏黎世联邦理工开源的千核级（256/1024 核）可扩展 RISC-V 共享超低延迟 L1 内存多核片上系统架构。 |
| [THU-DSP-LAB/ventus-gpgpu](https://github.com/THU-DSP-LAB/ventus-gpgpu) | 清华大学开源的基于 RISC-V 向量扩展（RVV）的 GPGPU 处理器（Chisel HDL 实现）。 |
| [xjtuiair-cag/c910-fpga](https://github.com/xjtuiair-cag/c910-fpga) | 基于平头哥玄铁 C910/C906 的开源 FPGA SoC 软核实现系统。 |
| [PrincetonUniversity/openpiton](https://github.com/PrincetonUniversity/openpiton) | 普林斯顿大学开源的跨指令集众核/多核芯片协同设计与研究平台。 |
| [iCAS-SJTU/Cool-3D](https://github.com/iCAS-SJTU/Cool-3D) | 上海交大开源的微流控冷却 3D-IC 架构早期热感知设计空间探索框架。 |
| [FCAS-LAB/Chiplet_Heterogeneous_newVersion](https://github.com/FCAS-LAB/Chiplet_Heterogeneous_newVersion) | LegoSim 异构 Chiplet 与 3D 封装多核全系统协同仿真器。 |
| [FCAS-LAB/LEGOSIM_MICRO](https://github.com/FCAS-LAB/LEGOSIM_MICRO) | LegoSim 微体系结构仿真器分支。 |
| [liljz250090/ChipletPart_legosim](https://github.com/liljz250090/ChipletPart_legosim) | Chiplet 模块化切分与布局算法仿真扩展。 |
| [CMU-SAFARI/ramulator2](https://github.com/CMU-SAFARI/ramulator2) | 卡内基梅隆大学开源的周期精确 DRAM / HBM / 异构内存高保真仿真器。 |
| [aiiiii-creator/3d-systolic](https://github.com/aiiiii-creator/3d-systolic) | 3D 脉动阵列芯片架构硬件实现方案。 |
| [The-OpenROAD-Project/asap7](https://github.com/The-OpenROAD-Project/asap7) | 7nm FinFET 预测工艺的学术界开源 PDK 与标准单元库。 |

### 3. 大模型、分布式并行与 Agent 生态
| 项目仓库 | 做了什么 / 核心特性 |
| :--- | :--- |
| [PKU-DAIR/Hetu-Galvatron](https://github.com/PKU-DAIR/Hetu-Galvatron) | 北京大学开源的超大模型自动混合并行与 MoE（混合专家）分布式训练系统。 |
| [deepseek-ai/deepseek-harness](https://github.com/deepseek-ai/deepseek-harness) | DeepSeek 官方插件式智能体评测与模型运行框架。 |
| [JustVugg/colibri](https://github.com/JustVugg/colibri) | 支持在消费级单机硬件上直接部署运行 Frontier 级混合专家模型（MoE）的推理运行时。 |
| [Shubhamsaboo/awesome-llm-apps](https://github.com/Shubhamsaboo/awesome-llm-apps) | 涵盖前沿 LLM 应用、Agent Skills 与工作流的综合案例代码库。 |
| [openai/skills](https://github.com/openai/skills) | OpenAI 官方 Codex / Agent Skills 核心规范与技能定义参考集。 |

### 4. MiniMax H3 视频生成与 ComfyUI 加速
| 项目仓库 | 做了什么 / 核心特性 |
| :--- | :--- |
| [zhenhanchen1-cyber/minimax-h3-ascend](https://github.com/zhenhanchen1-cyber/minimax-h3-ascend) | MiniMax-H3 在华为昇腾 NPU（910B/910C）上的本地单卡/多卡部署与显存优化套件。 |
| [AtlasCloudAI/awesome-minimax-h3](https://github.com/AtlasCloudAI/awesome-minimax-h3) | MiniMax H3 权重、量化模型、LoRA 及工作流资源全景合集。 |
| [xmarre/ComfyUI-Spectrum-MiniMax-H3](https://github.com/xmarre/ComfyUI-Spectrum-MiniMax-H3) | 免训练的切比雪夫特征预测跳层加速插件，大幅压缩 H3 视频生成推理用时。 |
| [LBH-123-AI/Comfyui_Minimax_h3_latent_Upscaler](https://github.com/LBH-123-AI/Comfyui_Minimax_h3_latent_Upscaler) | 针对 H3 24 通道潜空间的神经超分辨率放大器，绕过高耗能 VAE 进行低潜空间直升放大。 |
| [Miiikuuu/minimax-h3-ascend-single-card](https://github.com/Miiikuuu/minimax-h3-ascend-single-card) | 华为昇腾单卡快速部署跑通 MiniMax H3 方案。 |
| [BHUHD/minixmax-h3](https://github.com/BHUHD/minixmax-h3) | 针对英伟达 GPU 与华为昇腾 NPU 双平台优化的 H3 联合部署脚本。 |
| [ssssssanjiu/minimax-h3-turbo](https://github.com/ssssssanjiu/minimax-h3-turbo) | 4 步 / 8 步极速输出 MiniMax H3 视频的 ComfyUI 加速方案。 |
| [SilenWang/comfy-h3-container](https://github.com/SilenWang/comfy-h3-container) | 12GB 显存显卡即可运行 ComfyUI + MiniMax H3 的 Docker 一键镜像。 |
| [Eanya-Tonic/2080ti-minimax-h3](https://github.com/Eanya-Tonic/2080ti-minimax-h3) | 魔改 22GB RTX 2080 Ti 四卡通过 Raylight FSDP 运行 MiniMax H3 的硬核部署方案。 |
| [neng320/minimax-h3-local-deployment](https://github.com/neng320/minimax-h3-local-deployment) | 基于 16GB 显存实现 300% 速度飞跃的 H3 全栈优化部署手册。 |
| [ethanfel/ComfyUI-MiniMax-H3-Guide](https://github.com/ethanfel/ComfyUI-MiniMax-H3-Guide) | 用于精准调优 MiniMax H3 镜头与动效的结构化 Prompt 预置节点。 |

### 5. 创意动画、Web 3D 与生活工具
| 项目仓库 | 做了什么 / 核心特性 |
| :--- | :--- |
| [oxomkbk/earth-migration](https://github.com/oxomkbk/earth-migration) | 基于 Three.js r160 制作的电影级流浪地球星际穿梭交互 Web 3D 页面。 |
| [Jehuge/prompt-collection](https://github.com/Jehuge/prompt-collection) | 高质量 3D/动效/交互高质量 Prompt 提示词集（含浅海、山谷、星盘等）。 |
| [lemomo-ai/lemo-opuscar](https://github.com/lemomo-ai/lemo-opuscar) | 通过纯代码由 AI 手绘生成的 43 套短片风格与动效展示。 |
| [athemeroy/awesome-claude-5-5-videos](https://github.com/athemeroy/awesome-claude-5-5-videos) | Claude 5.5 纯代码交互视频、手绘动效演示与提示词工程集。 |
| [bilawalsidhu/gods-eye-view](https://github.com/bilawalsidhu/gods-eye-view) | 基于地理信息与卫星航拍的“上帝视角”3D 空间动态渲染工程。 |
| [yushua0808-cpu/dragon-codex-boot](https://github.com/yushua0808-cpu/dragon-codex-boot) | 1080P 动漫龙娘启动开机动画外壳，利用 DWM 实时缩略图无缝融合到桌面客户端。 |
| [17madman/DiscordVerificationBot](https://github.com/17madman/DiscordVerificationBot) | 调用大学公开通讯录 API 自动核验学生身份并为 Discord 成员赋权的校园门禁 Bot。 |

---

## 二、个人原创 / 自研项目与极简复刻指南

| 项目名称 | 做了什么 | 下次怎么复刻（极简命令/步骤） |
| :--- | :--- | :--- |
| **微信欢乐斗地主·实时悬浮军师** | 针对微信小程序定制。OpenCV 自动定位裁剪手牌特征，实时精准识牌算牌并推演压牌建议。 | 1. `pip install opencv-python pillow pygetwindow pydirectinput`<br>2. 运行 `python 微信欢乐斗地主_实时悬浮军师.py`<br>3. 打开微信斗地主点“自动截屏识牌”。 |
| **Escape Friday（逃离星期五）** | 基于 Vite + Canvas 与 Kenney 1-bit 复古素材制作的 2D 独立像素冒险小游戏。 | 1. 进入游戏目录执行 `npm install`<br>2. `npm run dev` 即可本地浏览器试玩。 |
| **MetaApp 游戏逆向提取器** | 自动化爬虫与逆向分析工具，批量解析 MetaApp 游戏章节关卡与美术资源。 | 1. `pip install requests`<br>2. 运行 `python dump_chapters.py` 批量提取。 |
| **DJI Action 4 3D 交互拆解系统** | 基于 Three.js + WebGL 纯代码打造的运动相机 3D 爆炸图与工程结构多轴分解交互。 | 双击目录内的 `open.bat`（或用任何静态 Web 服务器打开 `index.html`）。 |
| **Dusk Till Dawn · 逐帧手绘 MV** | 纯 Canvas 脚本逐帧手绘的日出日落 60 秒动画 MV（纯数学算法绘制纸船、人物与猫咪）。 | 终端执行 `npm install` ➔ 浏览器直接打开 `index.html`。 |
| **层叠剪纸国风动效 MV** | 复刻抖音 Remotion 风格，纯代码手绘多图层剪纸、云雾与光晕的动态视差系统。 | 双击运行 `open.bat` 即可带背景音乐全屏播放。 |
| **Codex 认证助手 Chrome 扩展** | Chrome 扩展程序 + 引导落地页，解决 OpenAI Codex 跨域凭据认证与本地 token 注入。 | 打开 Chrome 扩展页面，开启开发者模式，点击“加载已解压的扩展程序”选择 `extension`。 |
| **抖音无水印原片与逐字稿归档** | 抖音下载 Skill。支持原片保存、语音转写校对 SRT、按点赞排序批量改写口播稿。 | 在具备 CDP 调试环境的 Python 环境下运行 `agents/` 中的主控脚本。 |
| **百度网盘免客户端下载助手** | 油猴脚本（Tampermonkey Userscript），免客户端解析提取百度网盘直链。 | 浏览器安装 Tampermonkey 扩展后导入安装 `.user.js` 脚本。 |
| **北京数字孪生 WebGIS** | 基于前端工程化搭建的 3D 城市园区级空间数字孪生地图可视化系统。 | 进入目录执行 `npm install` ➔ `npm run dev` 即可查看。 |
| **中微子 2026 物理动态演示** | 结合音频时间轴，用 WebGL 粒子模拟 2026 诺贝尔物理学奖中微子震荡的科幻演示。 | 双击 `open.bat` 或运行 `python serve.py`。 |
| **《寰宇坠落》《太阳系星历》《纪元山谷》** | 包含宇宙降落三日系统、太阳系天体时钟、公元前2万年到2100年悬浮沙盘的 3D 系列。 | 均为纯单页 WebGL，本地双击 `index.html` 或通过 `npx serve` 即可秒开。 |
| **MSPM0 平衡小车 / STM32 纯惯导系统** | TI MSPM0 巡线自平衡控制算法、STM32 纯惯性导航小车工程以及立创 EDA 拓展板 PCB。 | Keil MDK 打开 `.uvprojx` 工程文件 ➔ 连接 DAP-Link 点击下载烧录。 |
