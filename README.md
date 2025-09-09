# Flask 2FA 认证项目文档

## 项目概述
本项目是一个基于 Flask 实现的双因素认证（2FA）系统。它提供用户注册、登录以及通过 Google Authenticator 或其他兼容 TOTP（基于时间的一次性密码）的应用进行 2FA 认证的功能。

## 技术栈
- **后端**: Python (Flask)
- **前端**: HTML, JavaScript, DaisyUI (CSS 框架), Tailwind CSS (通过 DaisyUI 引入)
- **2FA 库**: `pyotp` 用于生成和验证 TOTP
- **二维码生成**: `qrcode` 用于生成 2FA 设置二维码

## 文件结构
- `main.py`: Flask 后端应用的核心逻辑，包括路由定义、用户注册、登录和 2FA 验证。
- `templates/index.html`: 前端页面，包含用户注册和登录的表单以及显示 2FA 二维码的区域。
- `.gitignore`: Git 忽略文件配置。
- `.python-version`: Python 版本管理文件。
- `pyproject.toml`: Python 项目配置。
- `uv.lock`: 依赖锁定文件。
- `README.md`: 项目的 README 文件。

## 功能模块

### 1. 用户注册 (`/register`)
- **方法**: `POST`
- **请求体**: `JSON` 格式，包含 `username` 和 `password`。
- **逻辑**:
    - 接收用户提供的用户名和密码。
    - 使用 `pyotp.random_base32()` 生成一个随机的 TOTP 密钥。
    - 生成一个 TOTP provisioning URI (otpauth://) 用于 Google Authenticator。
    - 使用 `qrcode` 库将 provisioning URI 转换为二维码图像。
    - 将二维码图像编码为 Base64 字符串，并作为数据 URI 返回给前端。
    - 注册成功后，前端会显示该二维码供用户扫描。
- **响应**: `JSON` 格式，包含 `status` (0 为成功), `msg` 和 `qrcode` (Base64 编码的二维码数据 URI)。

### 2. 用户登录 (`/login`)
- **方法**: `POST`
- **请求体**: `JSON` 格式，包含 `username`, `password` 和 `code` (用户输入的 TOTP 验证码)。
- **逻辑**:
    - 接收用户提供的用户名、密码和 2FA 验证码。
    - 验证用户名和密码是否与预设的 `admin:admin` 匹配。
    - 如果匹配，使用存储的 TOTP 密钥 (`data["secret"]`) 创建 `pyotp.TOTP` 对象。
    - 调用 `totp.verify(code, valid_window=1)` 验证用户输入的验证码。`valid_window=1` 表示允许当前时间戳前后各一个时间步的验证码。
    - 根据验证结果返回登录成功或失败信息。
- **响应**: `JSON` 格式，包含 `status` (0 为成功) 和 `msg`。

### 3. 首页 (`/index`)
- **方法**: `GET`
- **逻辑**: 渲染 `templates/index.html` 页面。

## 前端交互 (`templates/index.html`)
- **UI 框架**: DaisyUI (基于 Tailwind CSS)。
- **页面切换**: 通过 `tab_switch` JavaScript 函数在注册和登录界面之间切换。
- **注册表单**:
    - 收集用户名、密码和确认密码。
    - 客户端验证：检查用户名是否为空，两次密码是否一致。
    - 通过 `fetch` API 向 `/register` 接口发送 POST 请求。
    - 注册成功后，隐藏注册容器，显示二维码容器，并将返回的 Base64 二维码显示在 `img` 标签中。
- **登录表单**:
    - 收集用户名、密码和 2FA 验证码。
    - 客户端验证：检查用户名、密码和验证码是否为空，验证码长度是否为 6 位。
    - 通过 `fetch` API 向 `/login` 接口发送 POST 请求。
    - 根据服务器响应显示登录成功或失败的提示。

## 运行项目
1. **安装依赖**:
   ```bash
   pip install Flask pyotp qrcode Flask-Cors
   ```
2. **运行应用**:
   ```bash
   python main.py
   ```
   应用将在 `http://127.0.0.1:5000` 上运行。

## 注意事项
- 默认的用户名为 `admin`，密码为 `admin`。
- 注册时生成的 TOTP 密钥是随机的，并且在后端 `main.py` 的 `data` 字典中硬编码了一个示例密钥 `IM6YOMCQSOFLQLEGX3W5UEGGATZSDFKN`。实际应用中应将密钥安全存储（例如数据库），并与特定用户关联。
- 本项目仅为演示目的，未实现用户数据持久化。