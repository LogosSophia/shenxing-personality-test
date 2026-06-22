# 神性论人格王国底盘测评 v0.3

这是一个 Streamlit 原型，用于部署“神性论人格王国底盘测评”。

## 功能

- 120 题 v0.3 题库
- 16 型底盘分
- 低位 / 高位判定
- 帝师气质
- 元帅反相
- 护卫过高异型风险提示
- 子民刺痛过载提示
- 元帅过激提示
- MBTI 对照非计分题
- 默认后台记录答卷与结果

## 本地运行

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Streamlit Community Cloud 部署

1. 打开 Streamlit Community Cloud。
2. Create app。
3. 选择仓库 `LogosSophia/shenxing-personality-test`。
4. Branch 选择 `main`。
5. Main file path 填 `app.py`。
6. Deploy。

## 后台保存逻辑

生成结果时，应用会默认保存本次答卷与结果。

优先级：

1. 如果配置了 Google Sheets secrets，则写入 Google Sheets。
2. 如果未配置 Google Sheets，则写入本地 `submissions/submissions.csv` 作为开发 fallback。

注意：Streamlit Community Cloud 的本地文件不适合长期保存数据。正式收集样本时应配置 Google Sheets。

## Google Sheets 后台配置

推荐创建一个 Google Sheet，建立名为 `Submissions` 的工作表，然后把该表共享给 Google Cloud service account 的 `client_email`。

在 Streamlit Community Cloud 里打开：

```text
App → Settings → Secrets
```

填入类似内容：

```toml
[gsheets]
spreadsheet_id = "你的 Google Sheets 文件 ID"
worksheet_name = "Submissions"

[gcp_service_account]
type = "service_account"
project_id = "your-project-id"
private_key_id = "your-private-key-id"
private_key = "-----BEGIN PRIVATE KEY-----\n你的私钥内容\n-----END PRIVATE KEY-----\n"
client_email = "your-service-account@your-project-id.iam.gserviceaccount.com"
client_id = "your-client-id"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/your-service-account%40your-project-id.iam.gserviceaccount.com"
universe_domain = "googleapis.com"
```

仓库中有 `.streamlit/secrets.example.toml` 示例。不要把真实 `secrets.toml` 提交到 GitHub。

## 后台记录字段

后台会保存：

- 提交时间
- submission_id
- 最终类型与低位/高位
- 16 型底盘分
- 君主、宰相、护卫、子民、帝师、元帅分
- 风险提示
- 全部题目答案 JSON
- 可选 MBTI 对照

## 说明

本测评只用于人格结构研究与自我理解，不是医学或心理诊断。
