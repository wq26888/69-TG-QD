# 69yun 自动签到脚本

运行效果（进行了多账户区分）
<img width="386" alt="image" src="https://github.com/user-attachments/assets/ad8df3bc-0f49-4fba-b05c-3bb76005527e" />


**声明：**

本脚本原版 fork 地址：[https://github.com/yixiu001/69yuncheckin](https://github.com/yixiu001/69yuncheckin)。本仓库版本基于这个作者的脚本，感谢原作者开源，本版本也不会收费。

对专业玩家，您可以得心应手的使用脚本的内容。

对新手玩家，您要明白提问的智慧，要描述清楚你的问题，否则不会回复。

对伸手党，建议你可以滚蛋。

本脚本请严格根据 readme 文档进行操作，不懂要问，要查资料，学会使用搜索引擎。

---

本项目旨在实现一个自动化的 69yun 签到脚本，并将签到结果通过 Telegram 和邮件发送给用户。

## 准备工作

在开始之前，请确保您拥有以下账号：

*   GitHub 账号
*   69yun 账号
*   Telegram 账号 (可选，用于接收 Telegram 通知)
*   Gmail 账号 (用于发送邮件)

## 使用方法

1.  **Fork 仓库：** 点击 GitHub 页面右上角的 "Fork" 按钮，将本项目 Fork 到您的 GitHub 账号下。

2.  **启用 Actions：** 在您的 Fork 仓库的 "Settings" -> "Actions" -> "General" 中，确保 Actions 处于启用状态。如果显示 "Actions are disabled on this repository"，请选择 "Allow all actions and reusable workflows" 或 "Allow select actions"，然后点击 "Save"。

3.  **设置 GitHub Secrets (环境变量)：**

    在您的 Fork 仓库的 "Settings" -> "Secrets" -> "Actions" 中，添加以下 Secrets：

    *   **`DOMAIN`：** 您的 69yun 域名 (例如：`https://69yun69.com`)。
    *   **`BOT_TOKEN`：** 您的 Telegram Bot Token (如果您想使用 Telegram 通知)。  
        *   获取方式：向 [BotFather](https://t.me/BotFather) 发送 `/newbot` 指令创建 Bot。
    *   **`CHAT_ID`：** 您的 Telegram Chat ID (如果您想使用 Telegram 通知)。 
        *   获取方式：将 Bot 加入您的频道/群组，然后使用 [get_id_bot](https://t.me/get_id_bot) 获取 Chat ID。
    *   **`GMAIL_SENDER_EMAIL`：** 您的 Gmail 发送邮箱地址 (用于发送邮件)。
    *   **`GMAIL_SENDER_PASSWORD`：** 您的 Gmail 发送邮箱密码或应用专用密码 (用于发送邮件)。
    *   **`GMAIL_RECEIVER_EMAIL`：** 您的 Gmail 初始接收邮箱地址 (用于接收未设置 `C_EMAIL` 的用户的邮件)。
    *   **`USER1`：** 第一个 69yun 账号的用户名 (邮箱地址)。
    *   **`PASS1`：** 第一个 69yun 账号的密码。
    *   **`C_EMAIL1`：** 第一个 69yun 账号的自定义接收邮箱地址 (可选，如果未设置，将发送到 `GMAIL_RECEIVER_EMAIL`)。
    *   **`USER2`：** 第二个 69yun 账号的用户名 (邮箱地址)。
    *   **`PASS2`：** 第二个 69yun 账号的密码。
    *   **`C_EMAIL2`：** 第二个 69yun 账号的自定义接收邮箱地址 (可选，如果未设置，将发送到 `GMAIL_RECEIVER_EMAIL`)。
    *   **以此类推，添加更多账号的 `USER(序号)`、`PASS(序号)` 和 `C_EMAIL(序号)` Secrets。**

    **重要说明：**

    *   **`GMAIL_SENDER_EMAIL`：** 所有邮件都将使用此邮箱作为发件人。
    *   **`GMAIL_RECEIVER_EMAIL`：** 如果某个账号没有设置 `C_EMAIL(序号)`，则该账号的签到结果将发送到此邮箱。
    *   **`C_EMAIL(序号)`：** 如果您希望某个账号的签到结果发送到特定的邮箱，请设置此 Secret。

4.  **配置 GitHub Actions 工作流：**

    *   本项目使用 GitHub Actions 实现自动化签到。
    *   您无需修改工作流文件 (`.github/workflows/your_workflow_name.yml`)，除非您需要更改签到频率。
    *   默认情况下，脚本每天早上 8:00 UTC 执行。  您可以修改 `cron` 表达式来调整执行时间。

5.  **启用 Gmail "允许安全性较低的应用访问" 或设置应用专用密码：**

    *   如果您使用 Gmail 发送邮件，您需要在您的 Gmail 账号中启用 "允许安全性较低的应用访问" (不推荐，存在安全风险) 或设置应用专用密码 (推荐)。
        *   **启用 "允许安全性较低的应用访问"：** 登录您的 Gmail 账号，访问 [https://myaccount.google.com/lesssecureapps](https://myaccount.google.com/lesssecureapps)，然后启用 "允许安全性较低的应用访问"。
        *   **设置应用专用密码：** 登录您的 Gmail 账号，访问 [https://myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)，选择 "邮件" 和 "其他设备"，然后生成一个应用专用密码。

6.  **运行脚本：**

    *   您可以手动触发 GitHub Actions 工作流，或者等待定时任务自动触发。
        *   **手动触发：** 在您的 Fork 仓库的 "Actions" 页面，选择您的工作流，然后点击 "Run workflow"。

## 脚本运行逻辑

1.  脚本会读取您在 GitHub Secrets 中设置的配置信息。
2.  脚本会循环执行每个账号的签到任务。
3.  脚本会将每个账号的签到结果发送到 Telegram (如果配置了 `BOT_TOKEN` 和 `CHAT_ID`)。
4.  脚本会将每个账号的签到结果发送到对应的邮箱：
    *   如果设置了 `C_EMAIL(序号)`，则发送到 `C_EMAIL(序号)` 指定的邮箱。
    *   否则，发送到 `GMAIL_RECEIVER_EMAIL` 指定的邮箱。
5.  所有邮件都将使用 `GMAIL_SENDER_EMAIL` 作为发件人。

## 建议和攻略

[点击查看 Gmail 邮箱申请和使用建议](opinion.md)


## 注意事项

*   请务必保护好您的 GitHub Secrets，不要泄露您的账号密码和 Telegram Bot Token。
*   请确保您的 69yun 账号密码正确。
*   如果遇到任何问题，请查看 GitHub Actions 的运行日志，或者提交 Issue。

## 贡献

欢迎提交 Issue 和 Pull Request！

## License

[MIT](LICENSE)

## 感谢

感谢所有为本项目做出贡献的人！
