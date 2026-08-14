# 把單檔 HTML 原型遷移進這個模板

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](../LICENSE)
[![Status: Public](https://img.shields.io/badge/status-public-brightgreen.svg)](https://github.com/HankHub777/guided-local-workbench-template)
[![Read in English](https://img.shields.io/badge/lang-English-blue.svg)](MIGRATION_FROM_SINGLE_FILE.md)
[![閱讀中文版](https://img.shields.io/badge/lang-繁體中文-lightgrey.svg)](MIGRATION_FROM_SINGLE_FILE.zh-TW.md)

你已經在跟 chatbot 對話的過程中，累積出一個真正有內容的大型 HTML 檔案——CSS 寫在裡面、JavaScript 也寫在裡面、資料直接寫死在 markup 裡。你想把這些東西接進這個模板的結構，而不是從頭重來。

這是一次性的銜接流程，不是平常持續在用的工作方式。遷移完成後，回到 [README.zh-TW.md](../README.zh-TW.md)「LLM chatbot 工作方式」那段講的小步變動流程。

## 為什麼這需要專門的流程

把一個大檔案拆成 `web/` 元件、`shared/` 型別、`data/`、`config/`，需要判斷每一段內容到底是什麼——這不是靠固定規則的腳本就能可靠處理的事。但這正好適合交給 chatbot 做，只要有文件化的流程、中間再加一個人工檢查點：你審核的是一份提案，不是自己動手拆。

## 我該用哪一份 prompt？

| 你的情況 | 使用 |
| --- | --- |
| 第一次遷移、檔案不大不小、你可以接受一次審核完整份分類清單 | **Prompt 1 — 完整盤點** |
| 檔案很大、很複雜，或你比較想一次一個功能／頁面慢慢遷移以降低風險 | **Prompt 2 — 分段盤點** |
| 你已經有一份審核通過的分類（來自 Prompt 1 或 2），準備實際產生檔案 | **Prompt 3 — 拆分與打包** |
| 你剛套用完遷移更新，想確認沒有東西壞掉 | **Prompt 4 — 一致性檢查** |

## 整體流程

1. 照平常一樣產生 context bundle：`python3 scripts/build_context_bundle.py`。
2. 依上面的表格選擇執行 **Prompt 1** 或 **Prompt 2**，把你的單檔 HTML 附加或貼上。chatbot 會提出一份分類提案——這一步還不會產生任何檔案。
3. **你審核這份分類**——見下方檢查清單。這是唯一需要你自己判斷的步驟，而且是審核，不是重寫。
4. 拿審核通過的分類執行 **Prompt 3**。chatbot 會產生 `update_YYYYMMDD_HHMMSS.zip`（內含 `manifest.json`），跟平常的更新包完全一樣。
5. 套用它：先執行 `python3 scripts/apply_update.py --dry-run`——遷移這種規模的變動一定要先預覽——確認計畫沒問題後再正式執行。需要終端機操作步驟的話見 [updates/README.md](../updates/README.md)。
6. 執行 **Prompt 4**，請 chatbot 協助確認新結構的行為跟原本檔案一致，然後自己動手把流程都點過一遍，確認沒問題才算遷移完成。

## 審核分類（第 3 步）：要檢查什麼

- **任何標記 `contains_real_data: yes` 的項目，目標位置一定要在 `data/input/` 底下。** 絕對不要讓它落到 `data/fixtures/`、`config/*.example.json`，或任何其他會被 commit 進 Git 的地方。如果 chatbot 把真實資料提案放到會被追蹤的位置，先在表格裡改過來，不要讓 Prompt 3 拿著沒改過的表格去執行。
- **沒有任何一項的目標應該是 canonical 路徑**（`README.md`、`AGENTS.md`、`docs/TEMPLATE_BOUNDARY.md`，以及 [docs/TEMPLATE_BOUNDARY.md](TEMPLATE_BOUNDARY.md) 清單裡的其他檔案）。如果你的原型真的需要改動其中一份，那是另一個獨立、需要謹慎決定的模板層級決策——不屬於一般遷移的一部分。
- **留意同一段邏輯在多個 UI 區塊裡重複出現的情況。** 如果同一段商業邏輯因為在原始檔案裡被貼了好幾次，而在分類裡出現好幾個獨立項目，請 chatbot 把它整合成 `shared/` 底下的單一位置，而不是把每一份重複的內容各自遷移一次。
- **如果表格長到你只能快速掃過、沒辦法真的逐行看，改用 Prompt 2**，改成一段一段遷移，不要硬啃一張巨大的表格。

## Prompt 1 — 完整盤點

複製下面這段，附加或貼上你的單檔 HTML 跟 `LLM_CONTEXT_BUNDLE.md`，原封不動送出。

```
我有一個用單一 HTML 檔案做出來的既有原型（附加／貼在下面）。
我想把它遷移成結構化的專案，但先不要產生任何檔案——
這一步只做分類。

請先讀附加的 LLM_CONTEXT_BUNDLE.md，了解目標專案結構與規則，
特別是哪些檔案是 canonical——不應該有任何項目被分類成要放進
canonical 檔案。

逐一檢視這份單檔 HTML，把每一段獨立的內容分類進一張表格，欄位如下：
- id：這段內容的簡短標籤（例如 "header-nav"、"sales-table-data"）
- category：以下其中一種：`ui-component`、`styling`、`business-logic`、
  `static-config`、`real-data`
- description：一句話說明這是什麼
- proposed_target：這段內容在模板結構裡應該變成的檔案路徑
  （例如 `web/src/components/Header.tsx`、`shared/types.ts`、
  `data/input/sales.csv`、`config/app.config.example.json`）
- contains_real_data：yes/no——只要看起來像真實的營運數字、真實的
  客戶或個人資訊、真實姓名、綁定實際事件的真實日期，或任何不是
  佔位符／範例值的內容，都標成 "yes"。不確定的話，一律標 yes。

只需要輸出這張分類表格。不要寫程式碼、不要產生任何檔案——
我需要先審核這張表格。
```

## Prompt 2 — 分段盤點

概念跟 Prompt 1 一樣，但一次只處理檔案的一部分——當檔案大到沒辦法一次審完的時候用這個。

```
我有一個用單一 HTML 檔案做出來的既有原型。它大到我想一次遷移一個
功能／區塊，而不是整份一次處理。

請先讀附加的 LLM_CONTEXT_BUNDLE.md，了解目標專案結構與規則。

這一輪，我只給你這個區塊：[描述這個區塊——例如「儀表板摘要面板，
大概在第 120 到 340 行」]。用跟完整遷移一樣的表格格式，只分類
這個區塊：
- id、category（ui-component / styling / business-logic /
  static-config / real-data）、description、proposed_target、
  contains_real_data（yes/no）

不要參照或假設任何我還沒給你的部分。不要產生任何檔案——
只要分類表格。

這個區塊審核通過並遷移完成後，我會再拿下一個區塊回來。
```

## Prompt 3 — 拆分與打包

分類表格（來自 Prompt 1 或 Prompt 2）審核通過後，用這個。

```
以下是這次遷移這一輪、已經審核通過的分類表格：

[貼上審核通過的表格]

請依照 LLM_CONTEXT_BUNDLE.md 裡的目標專案結構與規則，
為表格裡的每一列產生實際檔案：
- 把所有東西打包成一個 zip，檔名用今天的日期時間，
  命名為 `update_YYYYMMDD_HHMMSS.zip`。
- zip 根目錄放一份 `manifest.json`，列出每個檔案的
  `path`、`type: "added"`，以及一句話的 `reason`
  （註明這是來自分類表格的哪個 id）。
- 任何標記 `contains_real_data: yes` 的項目，一定要放進
  `data/input/` 底下——絕對不要放進會被追蹤的路徑。
- 不要產生或修改任何 canonical 路徑上的內容
  （見 bundle 裡的 docs/TEMPLATE_BOUNDARY.md）。如果某一列的
  proposed_target 是 canonical 路徑，請停下來告訴我，不要直接產生。
- 每個產生出來的檔案要保持專注——不要把不相關的項目合併成同一個檔案。

把 zip 給我下載。
```

## Prompt 4 — 一致性檢查

套用遷移更新之後用這個，協助確認沒有東西遺漏。

```
我已經套用了遷移更新。以下是實際發生的結果：

[貼上 apply_update.py 印出的 sync note，或
updates/applied/.../apply_log.json 的內容]

以下是原始單檔 HTML，供你參考：

[貼上或附加它]

請協助我確認遷移過程沒有遺漏任何東西：
1. 列出你在原始檔案裡看得出來的每一個使用者可見的流程或互動功能
   （例如「點擊 X 會篩選表格」、「表單送出後會顯示 Y」）。
2. 針對每一項，告訴我根據分類結果，它現在應該落在哪個／哪些新檔案裡。
3. 標出原始檔案裡有、但在新結構裡完全看不到對應內容的部分——
   這是潛在的遺漏，不要假設沒問題。

我會自己把新版本裡的每個流程都手動點過一遍，確認過才會把
這次遷移當作完成。
```

## 遷移完成之後

- 原始的單檔 HTML 不會自動被刪除。要留著當存檔參考、還是確認一致後刪掉，由你自己決定——這個流程不會替你做這個決定。
- 從這裡開始，回到平常的小步變動流程：一次一個可驗收的需求，透過同一套 `apply_update.py` 流程套用，詳見 [README.zh-TW.md](../README.zh-TW.md)。
