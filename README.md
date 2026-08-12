# Guided Local Workbench Template

這是一個讓一般使用者在 **LLM chatbot 引導下** 建立個人化本機工作台的模板；使用者不需要在公司環境取得 agent 能力。模板提供清楚的文件、資料契約與安全邊界，讓 chatbot 能協助使用者逐步完成一個可驗收的本機工具。

預設工具以本機方式運作：例如 Excel 經 ETL 轉成 JSON，再由 React 前端讀取。當需求成熟時，同一 repository 可逐步加入 API、資料庫、部署與正式的服務治理；不應因為這條升級路徑存在，就在原型階段預先加入它們。

## 為什麼需要模板，而不只是一份單檔 HTML

單檔 HTML 加上持續與 LLM 對話，很適合一次性、個人使用的小工具。這個模板處理的是另一種情境：工具會持續修改、使用真實資料、交給其他人，或有一天需要升級成正式服務。

模板的目的不是讓每個人變成 agent 工程師，而是讓更多有 LLM 經驗的使用者成為**有模板與引導的 LLM 工具建造者**。這一層使用者能將業務需求拆成可驗收的小改動，讓 chatbot 在明確邊界內協作，並知道何時該交給工程團隊。

| 面向 | 只有長對話與單檔 HTML | 有模板與引導的 LLM 工具建造者 |
| --- | --- | --- |
| 專案脈絡 | 留在聊天記錄或個人記憶中 | 留在 README、資料契約、決策與檔案清單中 |
| chatbot 判斷 | 從長文本推測目前狀態，容易猜錯或重寫既有功能 | 依指定文件與責任邊界做小而可檢查的變更 |
| 換人、換模型、換電腦 | 必須重新說明背景 | 提供同一份 repository context 即可接手 |
| 真實資料 | 容易混入 UI、手動修改或無法重跑 | 有輸入、驗證、生成資料與資料血緣的邊界 |
| 升級與交接 | 工程師需先反向理解原型 | 有資料來源、規則、例外、驗收與升級條件可接手 |

這些文件不會消除 chatbot 的錯誤或幻覺；它們將錯誤限制在較小、較明確、可驗證與可回退的範圍。專案的控制權不再依賴某一段聊天記錄或某一個模型，而在任何人都能檢查的檔案中。

## 對使用者、工程與組織的效益

對使用者而言，模板降低的是「持續做下去」的門檻：不需要理解完整軟體架構，也能知道資料放哪裡、哪些檔案不能手改、如何要求 chatbot 做小改動，以及如何驗證結果。

對工程團隊而言，模板提升接手品質。原型不只是畫面，而能帶著資料來源、資料定義、例外規則、可重現流程與已驗證的使用情境。工程師可將時間用在安全、整合、權限、可靠性與正式產品化，而非從零猜測原型意圖。

對主管與組織而言，這是一條能力擴散路徑：將大量會使用 LLM、但無法獨立維護工具的人，提升為能安全建立、驗證與交接本機工作流程的使用者。即使目前企業環境只允許 chatbot，未來一旦開放可控的 agent 環境，或由工程團隊接手繼續開發，明確的 repository context、契約與決策也能以低摩擦、低溝通成本延續工作。

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

## 模板契約與專案內容的邊界

同一個人可能會用這個模板建立不只一個本機工作台，clone 之間也會在同事間交接。若模板本身的契約文件被當成一般變動範圍隨手改掉，每份 clone 就會逐漸漂移成不同的樣子，交接時版本互不一致。

- **模板契約（不因建置單一工具而改動規則或結構）**：`README.md`、`AGENTS.md`、`ai/ARCHITECTURE_RULES.md`、`docs/FILE_MANIFEST.md` 的表格結構、`docs/UPGRADE_PATH.md` 的升級條件。
- **專案內容（建置這個工具時應持續填寫、修改）**：`ai/PROJECT_CONTEXT.md`、`docs/DATA_CONTRACT.md`、`docs/DECISIONS.md`、`config/*.example.json`，以及 `web/`, `server/`, `shared/`, `scripts/`, `data/`, `tests/`。

完整清單、判斷方式與「發現模板本身該改」時的處理流程，見 [docs/TEMPLATE_BOUNDARY.md](docs/TEMPLATE_BOUNDARY.md)。

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
