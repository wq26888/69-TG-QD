# 项目配置教程

## 1. 点击 Star 和 Fork 这个项目

视频教程：https://youtu.be/HjECaEIH4_s

### 1.1 点击 Star

点个Star支持一下，非常感谢！

### 1.2 Fork 项目

- **步骤**：
    1. 打开该项目的 GitHub 页面。
    2. 在页面右上角，点击 **Fork** 按钮。
    3. 选择你要 Fork 到的 GitHub 账户或组织。

---

## 2. 配置环境变量

### 2.1 在 GitHub 中设置 Secrets（环境变量）

为了让 CI/CD 流程使用敏感信息（如 `BOT_TOKEN`, `CHAT_ID`, `USER1`, `PASS1` 等），我们使用 GitHub 的 **Secrets** 功能存储环境变量，这样可以安全地管理配置。

- **步骤**：
    1. 打开你的 GitHub 仓库页面。
    2. 点击页面右上角的 **Settings** 按钮。
    3. 在左侧菜单栏找到 **Secrets and variables**，点击 **Actions**。
    4. 点击 **New repository secret** 按钮，添加以下 Secrets：
        - `BOT_TOKEN`：你的 Bot Token。
        - `CHAT_ID`：你的 Chat ID。
        - `USER1`, `USER2`, `USER3`（根据需要添加）：第一个、第二个、第三个用户的用户名（如邮件地址）。
        - `PASS1`, `PASS2`, `PASS3`（根据需要添加）：与上述用户对应的密码。

> **注意**：Secrets 一旦设置好后，GitHub Actions 会自动读取它们，无需手动在每次提交时修改代码，但是在工作流中只配置了2个账户，所以需要添加更多账户的话，请手动修改yaml文件。

### 2.2 在 GitHub Actions 中引用环境变量

GitHub Actions 会自动加载你设置在 **Secrets** 中的环境变量，你可以在 `.yaml` 文件中通过 `${{ secrets.<secret_name> }}` 的方式引用这些环境变量。

#### 如果需要添加更多账户请手动修改.github/workflows/69yuncheckin.yaml文件的如下内容

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    env:
      BOT_TOKEN: ${{ secrets.BOT_TOKEN }}
      CHAT_ID: ${{ secrets.CHAT_ID }}        # 这里设置可以用于多个账户
      USER1: ${{ secrets.USER1 }}            # 用户1
      PASS1: ${{ secrets.PASS1 }}            # 密码1
      USER2: ${{ secrets.USER2 }}            # 用户2
      PASS2: ${{ secrets.PASS2 }}            # 密码2
      # 可以继续扩展更多用户和密码，例如
      USER3: ${{ secrets.USER3 }}            # 用户3
      PASS3: ${{ secrets.PASS3 }}            # 密码3
      USER4: ${{ secrets.USER4 }}            # 用户4
      PASS4: ${{ secrets.PASS4 }}            # 密码4
```

### 2.3 手动运行工作流，后续每天都会自动运行

--- 

# 二次修改

- 加入“邮箱通知功能”
- 需要设置环境变量或机密如下
    - EMAIL_SENDER: 你的邮箱账号
    - EMAIL_PASSWORD: 你的邮箱专用密码（请主动查询教程配置，小白勿动）
    - EMAIL_RECEIVER: 接收邮件的账号（可以和邮箱账号设置为同一个）
    
