# The Handy Controller

一个用于控制 The Handy 互动设备的 Python 库

[![Python](https://img.shields.io/badge/python-3.7%2B-blue)](https://www.python.org)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![GitHub](https://img.shields.io/badge/github-thehandy--controller-lightgrey)](https://github.com/ningzhongning97-cloud/thehandy-controller)

## 🚀 功能

- ✅ 完整的 The Handy API 客户端
- ✅ 设备连接和状态管理
- ✅ 速度和位置控制
- ✅ 脚本播放和管理
- ✅ 异常处理和错误管理
- ✅ 详细的日志记录
- ✅ 完整的单元测试

## 📋 系统要求

- Python 3.7 或更高版本
- pip 包管理器

## 📦 安装

### 从源代码安装

```bash
# 克隆仓库
git clone https://github.com/ningzhongning97-cloud/thehandy-controller.git
cd thehandy-controller

# 安装依赖
pip install -r requirements.txt

# 安装包
pip install -e .
```

### 使用 pip 安装（将来支持）

```bash
pip install thehandy-controller
```

## 🔧 配置

### 环境变量

创建 `.env` 文件来配置你的设备信息：

```bash
cp .env.example .env
```

编辑 `.env` 文件：

```ini
# The Handy API 配置
HANDY_API_URL=https://www.handyfeeling.com/api/v1
HANDY_CONNECTION_KEY=your_connection_key_here

# 请求配置
HANDY_REQUEST_TIMEOUT=10
HANDY_MAX_RETRIES=3

# 设备配置
HANDY_DEVICE_ID=your_device_id

# 日志配置
HANDY_LOG_LEVEL=INFO
HANDY_LOG_FILE=thehandy.log
```

**重要：** 获取你的 Connection Key
1. 访问 https://www.handyfeeling.com
2. 注册或登录你的账户
3. 在设备设置中找到 Connection Key
4. 复制 Connection Key 到 `.env` 文件

## 💻 使用方法

### 基础使用

```python
from thehandy import HandyController

# 创建控制器实例
controller = HandyController(connection_key='your_connection_key')

# 连接到设备
controller.connect()

# 获取设备信息
device_info = controller.get_device_info()
print(device_info)

# 设置速度 (0-100)
controller.set_speed(50)

# 设置位置 (0-100)
controller.set_position(75)

# 停止设备
controller.stop()

# 断开连接
controller.disconnect()
```

### API 参考

#### 连接管理

```python
# 连接到设备
controller.connect()

# 检查连接状态
is_connected = controller.is_connected()

# 断开连接
controller.disconnect()
```

#### 设备信息

```python
# 获取设备信息
device_info = controller.get_device_info()

# 获取设备状态
status = controller.get_status()
```

#### 设备控制

```python
# 设置速度 (范围: 0-100)
controller.set_speed(50)

# 设置位置 (范围: 0-100)
controller.set_position(75)

# 停止设备
controller.stop()
```

#### 脚本管理

```python
# 获取可用脚本列表
scripts = controller.get_scripts()

# 播放脚本
controller.play_script('script_id')

# 暂停脚本
controller.pause_script()

# 恢复脚本
controller.resume_script()
```

## 📚 示例

项目包含了三个完整的使用示例：

### 1. 基础控制 (basic_control.py)

演示如何连接设备、获取信息、控制速度和位置。

```bash
python examples/basic_control.py
```

### 2. 脚本播放 (script_player.py)

演示如何播放、暂停和恢复脚本。

```bash
python examples/script_player.py
```

### 3. 设备监控 (device_monitor.py)

演示如何监控设备状态。

```bash
python examples/device_monitor.py
```

## 🧪 测试

运行单元测试：

```bash
python -m pytest tests/
```

或使用 unittest：

```bash
python -m unittest discover tests/
```

## 🛠️ 异常处理

库提供了多个自定义异常类，用于不同的错误情况：

```python
from thehandy import (
    HandyException,           # 基础异常
    HandyConnectionError,     # 连接错误
    HandyAPIError,            # API 错误
    HandyTimeoutError,        # 超时错误
    HandyDeviceError,         # 设备错误
)

try:
    controller.connect()
except HandyConnectionError as e:
    print(f"连接错误: {e}")
except HandyAPIError as e:
    print(f"API 错误: {e}")
except HandyTimeoutError as e:
    print(f"超时错误: {e}")
except HandyException as e:
    print(f"其他错误: {e}")
```

## 📝 项目结构

```
thehandy-controller/
├── thehandy/
│   ├── __init__.py          # 包初始化和导出
│   ├── client.py            # 主 API 客户端
│   ├── config.py            # 配置管理
│   └── exceptions.py        # 自定义异常
├── examples/
│   ├── basic_control.py     # 基础控制示例
│   ├── script_player.py     # 脚本播放示例
│   └── device_monitor.py    # 设备监控示例
├── tests/
│   ├── __init__.py
│   └── test_client.py       # 单元测试
├── README.md                # 本文件
├── requirements.txt         # 项目依赖
├── setup.py                 # 包配置
├── .env.example             # 环境变量模板
├── .gitignore               # Git 忽略文件
├── LICENSE                  # MIT 许可证
└── CONTRIBUTING.md          # 贡献指南
```

## 🤝 贡献

欢迎提交 Pull Request！请参考 [CONTRIBUTING.md](CONTRIBUTING.md) 了解更多信息。

### 开发流程

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 开启 Pull Request

## 📄 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

## ⚠️ 免责声明

本项目为非官方 The Handy API 客户端。使用本库时请：

- 遵守 The Handy 的服务条款
- 对你的设备使用负责
- 仅在适当的情况下使用

## 🔗 相关链接

- [The Handy 官方网站](https://www.handyfeeling.com)
- [The Handy API 文档](https://www.handyfeeling.com/api/docs)
- [GitHub 仓库](https://github.com/ningzhongning97-cloud/thehandy-controller)

## 📧 联系方式

如有问题或建议，请：

1. 提交 Issue
2. 发起 Discussion
3. 创建 Pull Request

## 🎯 未来计划

- [ ] 发布到 PyPI
- [ ] 支持异步 API
- [ ] Web 仪表板
- [ ] CLI 工具
- [ ] 更多示例
- [ ] 完整的 API 文档

---

**最后更新**: 2026-05-02
