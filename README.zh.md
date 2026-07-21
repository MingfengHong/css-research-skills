<div align="center">

# CSS Research Skills

**面向计算社会科学 Agent 的研究设计优先型 Skill**

把社会科学问题转化为可检查的分析流程，覆盖因果推断、计算文本分析、基于主体的建模与网络科学，而不是把“代码能运行”误当作“结论有证据”。

[![版本](https://img.shields.io/badge/version-2.0.0-7A8B64)](css-research-skills/SKILL.md)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-compatible-C6D0B4)](https://agentskills.io/)
[![许可](https://img.shields.io/badge/license-CC%20BY--NC%204.0-7A8B64)](LICENSE)

[English](README.md) · [快速开始](#快速开始) · [Benchmark](#benchmark)

</div>

## 为什么需要这个 Skill？

通用编程 Agent 很容易生成看似合理的分析，却在过程中悄悄改变估计目标、跳过构念效度、调用过时 API，或因为设置了固定随机种子就宣称“可复现”。`css-research-skills` 补上从研究问题到经验结论之间所需的研究契约与效度检查。

它帮助 Agent：

- 区分描述、预测、测量、因果识别与模拟解释；
- 让混合型项目同时进入多个相关领域，而不是被迫选择一个方法标签；
- 把代码、诊断、稳健性、来源追踪、伦理与最终主张连接起来；
- 只在任务需要时加载详细规则，控制上下文占用。

这个 Skill 用于增强研究者判断，不能代替领域知识、伦理审查或识别论证。

## 快速开始

克隆仓库后，复制直接包含 `SKILL.md` 的内层目录：

```bash
git clone https://github.com/MingfengHong/css-research-skills.git
cp -R css-research-skills/css-research-skills ~/.claude/skills/css-research-skills
```

其他兼容 Agent Skills 目录规范的工具也可以直接使用该内层目录，只需替换安装位置。

然后给 Agent 一个真实研究任务，例如：

```text
审计我的错位处理 DiD 设计：定义估计目标，识别无效比较，提出诊断，
并给出可以在 R 中实现的分析方案。
```

```text
为一项因果研究设计多语言文本测量流程，包括标注、效度证据、
预处理敏感性分析和样本切分。
```

```text
审查这个 Mesa 模型与网络分析管线的 API 兼容性、ODD 文档、
模拟验证、社区发现稳健性与数据来源记录。
```

## 能做什么

| 领域 | 覆盖内容 |
|---|---|
| 因果推断 | 目标试验、DAG、实验、回归调整、面板设计、现代 DiD/事件研究、RDD、IV、匹配/加权、纵向分析 |
| 计算文本分析 / NLP | 语料构建、表示、发现、构念测量、标注、分类、嵌入、LLM 编码、文本进入因果流程 |
| 基于主体的建模 | ODD 2020、Mesa 版本门控、概念模型、校准、验证、不变量、敏感性与 Monte Carlo 不确定性 |
| 网络分析 | 网络构建、中心性、社区、二模与时序网络、零模型、幂律、ERGM/TERGM |
| 可复现研究 | 来源追踪、原始/派生/分析数据分层、环境记录、可执行流程、受限数据与责任计算 |

## 2.0.0 更新

- 用依赖研究设计的判断与显式效度门槛替代僵化默认值。
- 纳入现代错位处理 DiD、文本测量效度与样本切分、ODD 2020、Mesa 版本门控、Leiden 稳定性、规范的幂律判断和 ERGM 4。
- 将可复现性从“随机种子 + 输出目录”扩展到来源、元数据、环境、主入口、输出映射和受限数据说明。
- 增加利益相关者、隐私、可预见伤害、双重用途与风险缓解检查。

## Benchmark

扩展后的 benchmark 包括 8 类任务：错位处理 DiD、跨语言 IV、多语言文本测量、不平衡文本分类、空间 ABM、二模网络、含缺失 dyad 的 valued ERGM，以及受限数据复现包。每份回答按 6 个维度评测：研究框架、方法匹配、实现、诊断、可复现性与负责任的主张。

![无 Skill、Skill 1.0.0 与 Skill 2.0.0 的综合 benchmark](assets/benchmark-comparison.png)

| 条件 | 通过检查 | 通过率 | 相对无 Skill |
|---|---:|---:|---:|
| 无 Skill | 28/48 | 58.3% | — |
| Skill 1.0.0 | 31/48 | 64.6% | +6.3 个百分点 |
| Skill 2.0.0 | 42/48 | 87.5% | +29.2 个百分点 |

更完整的任务组合纳入了 1.0.0 重点覆盖的能力。Skill 2.0.0 总体领先，而 1.0.0 在不平衡文本分类任务上得分更高（5/6 对 4/6）。

查看[完整任务与维度结果](benchmarks/README.md)。

## 致谢

社区化呈现参考了 [nuwa-skill](https://github.com/alchaincyf/nuwa-skill) 与 [academic-research-skills](https://github.com/Imbad0202/academic-research-skills)。

## 许可协议

[CC BY-NC 4.0](LICENSE)：允许在署名与非商业条件下分享和改编。
