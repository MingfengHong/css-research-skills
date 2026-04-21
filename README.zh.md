# Claude 计算社会科学技能

为计算社会科学所需的 coding 而设计的 Claude 技能，提供严谨、可复现、符合发表标准的研究软件工程规范。涵盖因果推断、自然语言处理、基于主体的建模以及社会网络分析四大领域。

---

## 功能概览

这款技能将 Claude 转变为兼具社会理论与代码能力的研究软件工程师。它不只是生成 Python 脚本——而是强制执行研究级标准：固定随机种子、结构化日志、防御性断言、算法复杂度标注，以及符合学术惯例的可视化。

在编写任何代码之前，技能会自动将用户的请求路由至正确的分析领域，并加载该领域特有的约束、工具链和验证协议。

## 仓库结构

```
css-research-skills/
│
├── README.md
├── LICENSE
│
└── css-research-assistant/
    ├── SKILL.md
    └── references/
        ├── packages.md
        ├── causal_inference.md
        ├── nlp_text_analysis.md
        ├── abm_simulation.md
        └── network_analysis.md
```

**注意：** 根据 [Claude 官方技能开发指南](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md)，技能文件夹内部**不得**包含 `README.md`。所有面向人类的文档应放在仓库根目录。

## 工作原理

### 渐进式加载

该技能采用三级加载机制，避免上下文过载：

1. **SKILL.md**（约 160 行）—— 始终加载。包含领域路由器、通用编码标准和完成度检查清单。
2. **领域参考资料**（约 140–165 行）—— 当路由器识别出用户的分析领域后按需加载。
3. **包参考**（约 90 行）—— 当某个特定包成为任务核心时加载。

### 领域路由

在编写代码之前，Claude 会将请求分类到以下四个领域之一，并加载对应的参考资料：

| 领域 | 触发条件 | 参考资料 |
|---|---|---|
| **因果推断** | 回归、DiD、RDD、IV、固定效应、匹配 | `references/causal_inference.md` |
| **文本分析 / NLP** | 主题建模、情感分析、嵌入、句法分析、分类 | `references/nlp_text_analysis.md` |
| **ABM / 模拟** | 基于主体的模型、Mesa、扩散、意见动态 | `references/abm_simulation.md` |
| **网络分析** | 图、中心性、社区发现、ERGM | `references/network_analysis.md` |

### 通用标准（所有领域）

- **理论先行**：在编码之前，先说明识别策略或理论机制。
- **可复现性**：固定所有随机种子（`seed=42`）并记录。
- **防御性编程**：断言领域约束条件（例如 `assert 0 <= p <= 1.0`）。
- **复杂度意识**：为循环密集型操作标注 Big-O；若为 O(N²) 或更差则发出警告。
- **管道完整性**：将所有路径集中在一个 `PATHS` 字典中；验证下游兼容性。
- **输出持久化**：每张表格、每幅图、每份报告都保存到 `output/` 目录，而非仅打印到控制台。
- **发可视化**：Nature/Science 风格，使用 Okabe-Ito 或 Viridis 配色，`dpi=300`。
- **错误处理**：禁止裸 `except:`；使用 `raise ... from e` 保留异常链。
- **无表情 / 无填充**：仅使用结构化日志（`[INFO] YYYY-MM-DD HH:MM:SS - message`）。

## 安装

### 前置要求

- 已安装 [Claude Code](https://claude.ai/code)
- 已导出 `ANTHROPIC_API_KEY`，或首次运行 Claude Code 时按提示输入

### 通过 GitHub（推荐）

**全局安装**（在所有项目中可用）：

```bash
mkdir -p ~/.claude/skills
git clone https://github.com/MingfengHong/css-research-skills.git ~/.claude/skills/css-research-skills
cp -r ~/.claude/skills/css-research-skills/css-research-assistant ~/.claude/skills/css-research-assistant
```

**项目安装**（推荐用于特定项目）：

```bash
cd /path/to/your/project
mkdir -p .claude/skills
git clone https://github.com/MingfengHong/css-research-skills.git .claude/skills/css-research-skills
cp -r .claude/skills/css-research-skills/css-research-assistant .claude/skills/css-research-assistant
```

> **没有 Git？** 访问 <https://github.com/MingfengHong/css-research-skills>，点击 **Code** → **Download ZIP**，解压后将 `css-research-assistant/` 文件夹复制到上述目标位置即可。

### 通过魔搭（ModelScope）

也可以通过魔搭安装：

**全局安装：**

```bash
npx skills add https://github.com/MingfengHong/css-research-skills
```

或通过 ModelScope SDK：

```bash
pip install --upgrade modelscope
modelscope skills add MingfengHong/css-research-skills
```

或通过 bash：

```bash
curl -fsSL https://modelscope.cn/skills/install.sh | bash -s -- MingfengHong/css-research-skills
```

**项目安装：**

```bash
cd /path/to/your/project
npx skills add https://github.com/MingfengHong/css-research-skills
```

### 安装后

重启 Claude Code。当你提及社会网络、回归、文本建模、主体模拟或因果推断等话题时，技能将自动触发。

## 使用示例

**用户**："我想在这个面板数据集上运行一个双重差分回归，标准误按聚类处理。"

**Claude（加载技能后）**：
1. 路由至**因果推断**领域。
2. 读取 `references/causal_inference.md`。
3. 询问："你的处理变量、结果变量、个体标识符和时间变量分别是什么？"
4. 编写 `did_analysis.py`，包含：
   - 注释中明确说明识别策略
   - `linearmodels.PanelOLS` 配合 `cov_type='clustered'`
   - 用于平行趋势检验的事件研究图
   - 多模型 Markdown 表格保存至 `output/regression_table.md`
   - 脚本末尾打印完成度检查清单

## 各领域亮点

### 因果推断
- **工具链锁定**：`statsmodels` / `linearmodels`（Python）；`fixest`（R，用于高维固定效应）。
- **标准误**：强制使用稳健/聚类/HAC 标准误；禁止使用球面标准误。
- **Cunningham 验证**：对基准模型进行跨语言系数核对（Python vs R）。

### NLP / 文本分析
- **预处理分野**：经典 NLP（停用词、词形还原）用于 LDA；Transformer 模型则采用最小化清洗。
- **基线要求**：在尝试 BERT 之前，必须先建立 TF-IDF + LinearSVC 基线。
- **构念效度**：对潜变量（如极化、框架）进行显式操作化。

### ABM / 模拟
- **OOP 严格性**：强制继承 `mesa.Model` / `mesa.Agent`。
- **随机性锁定**：使用 Mesa 的 `self.random`，禁止使用 Python 的 `random`。
- **性能保障**：通过 Mesa 原生方法进行空间查找；禁止 O(N²) 的邻居循环。

### 网络分析
- **复杂度关卡**：节点数 N > 10,000 时，对 O(N³) 的中介中心度发出警告。
- **二分图防御**：加权投影 + 信息损失警告。
- **语言锁定**：ERGM 切换至 R（`statnet` / `ergm`），并进行 MCMC 退化检查。

## 开发

本技能使用 Anthropic [Skill Creator](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md) 构建：
1. 基于领域专业知识和学术实践起草技能。
2. 在真实 CSS 任务上并行运行评估（加载技能 vs 不加载技能）。
3. 使用程序断言对输出进行评分（可复现性、路径规范、可视化质量）。
4. 基于量化基准和定性代码审查迭代改进。

## 许可协议

本作品采用 [Creative Commons Attribution-NonCommercial 4.0 International License](https://creativecommons.org/licenses/by-nc/4.0/)（知识共享署名-非商业性使用 4.0 国际许可协议）授权。

你可以出于**非商业**目的自由分享和改编本材料，前提是注明出处。完整法律文本请参见 `LICENSE` 文件。
