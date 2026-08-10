# Guided Local Workbench Template

這是一個讓一般使用者在 **LLM chatbot 引導下** 建立個人化本機工作台的模板；使用者不需要在公司環境取得 agent 能力。模板提供清楚的文件、資料契約與安全邊界，讓 chatbot 能協助使用者逐步完成一個可驗收的本機工具。

預設工具以本機方式運作：例如 Excel 經 ETL 轉成 JSON，再由 React 前端讀取。當需求成熟時，同一 repository 可逐步加入 API、資料庫、部署與正式的服務治理；不應因為這條升級路徑存在，就在原型階段預先加入它們。

## 先選擇運作模式

| 模式 | 使用時機 | 必要目錄 |
| --- | --- | --- |
| Local | 單人／小組、讀多寫少、JSON 可重建 | `web/`, `data/`, `scripts/`, `shared/` |
| Managed | 需排程 ETL、多人共用或受控 API | 加入 `server/` 與 CI |
| Product | 帳號、權限、多人寫入、稽核或正式對外 | 啟用 `server/`, `config/database.*`, 部署與測試 |

不要因為目錄存在就啟用後端或資料庫。升級條件見 [docs/UPGRADE_PATH.md](docs/UPGRADE_PATH.md)。

## 快速規則

1. `data/input/` 是輸入；`data/generated/` 是 ETL 產物，禁止手改。
2. UI 不直接依賴 JSON 檔案路徑；只透過 `web/src/data/` 的資料 adapter 讀資料。
3. `shared/` 是資料契約的唯一來源：型別、schema、欄位名稱都由這裡定義。
4. 秘密資訊不進 Git；本機使用 `.env`，可分享的範例放在 `config/*.example.*`。
5. 每次改資料結構，要一併更新 schema、ETL、測試資料與 `docs/DATA_CONTRACT.md`。

## LLM chatbot 工作方式

在不能使用 agent 的環境中，把下列檔案一併提供給 chatbot，再提出**一個可驗收的需求**：

- `AGENTS.md`
- `ai/PROJECT_CONTEXT.md`
- `ai/ARCHITECTURE_RULES.md`
- `docs/FILE_MANIFEST.md`
- 對應的 `shared/` 資料契約

要求它先說明將修改哪些檔案、哪些驗收條件會通過，再產生 patch。不要要求它「做一個完整系統」。使用者仍應在本機檢查 patch、執行驗證步驟，並只把不含機密資訊的內容提供給 chatbot。

## 目錄摘要

完整定義見 [docs/FILE_MANIFEST.md](docs/FILE_MANIFEST.md)。第一次接手模板時，先從這份檔案開始。

```text
ai/        給 AI 的專案脈絡與變更規範
config/    可版本控制的設定範例
data/      輸入、測試 fixture、ETL 產物
docs/      人可讀的決策、契約與交接文件
scripts/   Excel/CSV → JSON 等可重複執行工作
shared/    前後端共用的型別、schema、常數
web/       React + TypeScript + Tailwind 前端
server/    API／背景工作的邊界（初期只保留 README）
```
