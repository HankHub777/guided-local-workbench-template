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

- **模板契約（不因建置單一工具而改動規則或結構）**：`README.md`、`AGENTS.md`、`ai/ARCHITECTURE_RULES.md`、`docs/FILE_MANIFEST.md` 的表格結構、`docs/UPGRADE_PATH.md` 的升級條件、`.gitignore`、`LICENSE`、`scripts/apply_update.py`、`updates/README.md`、`scripts/build_context_bundle.py`。
- **專案內容（建置這個工具時應持續填寫、修改）**：`ai/PROJECT_CONTEXT.md`、`docs/DATA_CONTRACT.md`、`docs/DECISIONS.md`、`config/*.example.json`，以及 `web/`, `server/`, `shared/`, `scripts/`（`apply_update.py`、`build_context_bundle.py` 除外）, `data/`, `tests/`。`CHANGELOG.md` 只由 `scripts/apply_update.py` 附加內容，任何更新包都不應直接覆寫它。`LLM_CONTEXT_BUNDLE.md` 是產物，不進 Git，由 `scripts/build_context_bundle.py` 重建。

完整清單、判斷方式與「發現模板本身該改」時的處理流程，見 [docs/TEMPLATE_BOUNDARY.md](docs/TEMPLATE_BOUNDARY.md)。

## LLM chatbot 工作方式

在不能使用 agent 的環境中，開始對話前先執行：

```bash
python3 scripts/build_context_bundle.py
```

會產生單一檔案 `LLM_CONTEXT_BUNDLE.md`（裡面依序放了 5 份文件，各自在做什麼都有一行說明：協作規則、哪些檔案不能隨便改、整個專案的檔案索引、這個工具是做什麼的、程式架構的邊界），把這一份整份上傳或貼給 chatbot，就不用逐一上傳五個檔案、也不容易撞到聊天工具的上傳限制。這份 bundle 是可重建的產物，不進 Git；每次開新對話前重新執行一次即可，不用擔心過期。

如果產生的檔案開頭出現「still template placeholder content」這樣的提醒，代表「這個工具是做什麼的」那份文件（`ai/PROJECT_CONTEXT.md`）你還沒填成自己專案的真實內容、還是模板出廠時的通用範例。看到這個提醒，代表 chatbot 現在拿到的還不是「你這個工具」的真實資訊——找時間把那份文件改成寫你自己的專案，chatbot 給的建議才會真的對你有用。

如果這次任務會動到特定的資料結構，另外把對應的 `shared/` 資料契約檔案附上——bundle 刻意不包含它，因為那是任務相關、不是每次都要給的。

給完 context 後，再提出**一個可驗收的需求**，要求 chatbot 先說明將修改哪些檔案、哪些驗收條件會通過，再產生 patch。不要要求它「做一個完整系統」。使用者仍應在本機檢查 patch、執行驗證步驟，並只把不含機密資訊的內容提供給 chatbot。

### 把 chatbot 的輸出套用到本機

如果 chatbot 只能整包匯出更新後的檔案（沒有 agent 能力、無法直接改本機檔案），不要手動整包覆蓋本機資料夾。改用：

1. 請 chatbot 把變更輸出成一個 zip，檔名照固定格式命名為 `update_YYYYMMDD_HHMMSS.zip`（例如 `update_20260811_153000.zip`），並盡量附上 `updates/README.md` 所定義的 `manifest.json`。
2. 把這個檔案放進 `updates/incoming/`。
3. 依你的作業系統（macOS Terminal 或 Windows PowerShell）執行 `scripts/apply_update.py` — 完整可直接複製貼上的指令、以及互動提示的說明，見 [updates/README.md](updates/README.md)。
4. 腳本跑完後，畫面上會印出一小段文字，開頭寫「Paste this back into the chatbot so it knows what actually happened」。**如果你還會在同一個對話裡繼續請 chatbot 做事，把這段話整段複製、貼回聊天室當作你的下一句話。** chatbot 只知道自己「建議」了什麼，不知道你實際上有沒有全部照做——如果你剛剛跳過了某個檔案的變更，不告訴它的話，它會誤以為那個檔案已經改好了，接下來給你的建議可能就會建立在錯誤的假設上。

這個腳本會自動套用一般專案內容，但遇到模板契約檔案或任何刪除都會停下來要求確認，並把每次結果記錄進 `CHANGELOG.md`。

## 目錄摘要

完整定義見 [docs/FILE_MANIFEST.md](docs/FILE_MANIFEST.md)。第一次接手模板時，先從這份檔案開始。

```text
ai/        給 AI 的專案脈絡與變更規範
config/    可版本控制的設定範例
data/      輸入、測試 fixture、ETL 產物
docs/      人可讀的決策、契約與交接文件
scripts/   Excel/CSV → JSON 等可重複執行工作
shared/    前後端共用的型別、schema、常數
updates/   套用 chatbot 整包更新的收件匣與腳本
web/       React + TypeScript + Tailwind 前端
server/    API／背景工作的邊界（初期只保留 README）
```
