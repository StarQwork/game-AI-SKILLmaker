---
name: "game-plan-index"
description: "游戏策划案SKILL索引；作为Agent访问入口，引导调用对应专业策划SKILL"
priority: 100
---

# 游戏策划案 SKILL 索引

本知识库包含游戏策划案生成的专业SKILL，请根据用户需求选择对应的SKILL进行调用。

## SKILL 访问路径

| SKILL名称 | 文件路径 | 适用场景 |
|-----------|----------|----------|
| 程序员策划案 | [game-plan-programmer.md](./knowledge_base/game-plan-programmer.md) | 新建项目或迭代技术方案时调用 |
| 美术策划案 | [game-plan-artist.md](./knowledge_base/game-plan-artist.md) | 设定风格与资产规范时调用 |
| 音频策划案 | [game-plan-audio.md](./knowledge_base/game-plan-audio.md) | 确立音乐/音效方向与集成方案时调用 |
| 编剧策划案 | [game-plan-writer.md](./knowledge_base/game-plan-writer.md) | 确立世界观与任务线时调用 |

## 调用指南

### 1. 程序员策划案 (game-plan-programmer)

**触发条件：**
- 用户需要技术方案设计
- 涉及引擎选型、架构设计
- 需要系统模块划分
- 性能优化与工具链配置

**访问路径：** `knowledge_base/game-plan-programmer.md`

---

### 2. 美术策划案 (game-plan-artist)

**触发条件：**
- 用户需要美术风格定义
- 涉及资产生产规范
- 需要角色/场景/UI设计指导
- 引擎导入配置需求

**访问路径：** `knowledge_base/game-plan-artist.md`

---

### 3. 音频策划案 (game-plan-audio)

**触发条件：**
- 用户需要音乐/音效设计
- 涉及音频系统集成
- 需要事件表与混音配置
- 平台音频适配需求

**访问路径：** `knowledge_base/game-plan-audio.md`

---

### 4. 编剧策划案 (game-plan-writer)

**触发条件：**
- 用户需要世界观构建
- 涉及剧情与任务设计
- 需要角色设定与关系图
- 本地化文本规范需求

**访问路径：** `knowledge_base/game-plan-writer.md`

---

## 多SKILL协同

当用户需求涉及多个领域时，可按以下顺序依次调用：

1. **程序员策划案** - 确立技术基础
2. **美术策划案** - 定义视觉风格
3. **音频策划案** - 设计听觉体验
4. **编剧策划案** - 构建叙事框架

## 技术栈说明

所有SKILL均基于以下技术栈：
- **游戏引擎：** Godot
- **编程语言：** GDScript / C#
- **美术工具：** NanoBanana2
- **音频系统：** Godot Audio / FMOD
