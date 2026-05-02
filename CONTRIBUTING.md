# 贡献指南

感谢你有兴趣为 The Handy Controller 做贡献！

## 行为守则

我们承诺为所有贡献者提供友好、安全和欢迎的环境。

## 如何贡献

### 报告 Bug

如果你发现了 bug，请创建一个 Issue：

1. 使用清晰的标题描述问题
2. 提供详细的步骤来重现问题
3. 提供具体的示例来演示问题
4. 描述你观察到的行为和预期的行为

### 提交功能请求

功能请求欢迎！请：

1. 使用清晰的标题
2. 提供详细的描述
3. 解释为什么这个功能有用
4. 列出一些可能的实现方式（可选）

### 拉取请求 (Pull Request)

1. Fork 本仓库
2. 创建新的分支 (`git checkout -b feature/amazing-feature`)
3. 做出更改
4. 确保代码通过测试
5. 提交更改 (`git commit -am 'Add amazing feature'`)
6. 推送到分支 (`git push origin feature/amazing-feature`)
7. 创建 Pull Request

## 开发设置

### 环境要求

- Python 3.7 或更高版本
- pip
- git

### 设置开发环境

```bash
# 克隆仓库
git clone https://github.com/ningzhongning97-cloud/thehandy-controller.git
cd thehandy-controller

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # 在 Windows 上使用 venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
pip install -e .
```

### 运行测试

```bash
python -m pytest tests/
```

### 代码风格

We use:
- **Black** for code formatting
- **Flake8** for linting
- **isort** for import sorting

```bash
# 格式化代码
black thehandy/ tests/ examples/

# 检查代码风格
flake8 thehandy/ tests/ examples/

# 排序导入
isort thehandy/ tests/ examples/
```

## 提交信息规范

请使用有意义的提交信息。示例：

```
Add feature: device status monitoring
Fix: connection timeout issue
Docs: update README with examples
Test: add unit tests for API client
```

## Pull Request 检查清单

在提交 PR 之前，请确保：

- [ ] 代码遵循项目的代码风格
- [ ] 所有测试都通过
- [ ] 添加了新功能的测试
- [ ] 更新了文档（如果需要）
- [ ] 提交信息清晰明了
- [ ] 没有未解决的 merge conflicts

## 问题

如有任何问题，请：

1. 检查现有的 Issues
2. 创建新的 Issue 并提供详细信息
3. 参与 Discussions

## 许可证

通过贡献，你同意你的贡献将根据项目的 MIT 许可证进行许可。

---

感谢你的贡献！🎉
