# 圖片轉可編輯 Blender 場景：設定與驗證

## GitHub 雲端路線

在 Actions 執行 Build editable Blender scene。CPU runner 安裝固定版本 bpy，從 scenes/example.json 組裝並驗證，將 scene.blend、四個視角預覽及 validation.json 保存為 7 天 artifact。範例是煙霧測試，不包含圖片辨識模型。下一步將參考圖片與尺寸資料交給 Codex 分析，生成 scene plan，加入經許可的 GLB 單體資產，再替換範例計畫。建場景腳本支援方塊結構及 GLB 資產，並非任意造型的完整建模器。

一般 runner 沒有預設 GPU。GitHub GPU larger runner 需要適用的組織與方案，且應另查顯存是否足夠，不能假設它滿足 WorldBuilder。若採自行託管 Linux GPU runner，先由使用者配置 >=24GB VRAM、足夠 RAM/磁碟、Conda、SAM 權重及其存取授權。重建完成後把獨立物件 GLB 與場景布局交給本套件組裝。尚未配置或執行 GPU runner；不會默默啟動付費推論。

## 候選專案核實

| 專案 | 核實結果與選擇 |
|---|---|
| Top3d-ai/world-builder | 真實存在，commit 9f37da563ae6ec3a86755df536489d0d52991c09。包含 6 個 Codex 適配 skill，但依賴專案內 .claude 腳本、fal 金鑰與 GUI MCP；定位為風格化場景組裝。未找到根目錄明確 LICENSE，未直接安裝或再散布其 Skill。 |
| scpli/blender-mcp | 真實存在，commit 50a37a0dcf9898d86044398295d5097eab8ffa6b，MIT；package 1.8.7 的 metadata 指向 ahujasid/blender-mcp。已檢查 pyproject、server、telemetry 與啟動設定並從該 checkout 安裝，非 Blender 官方工具。它可執行任意 bpy；配置關閉 telemetry，維持 localhost。 |
| AdamRolander/WorldBuilder | 真實存在，commit c34b6d92642f0d386cf71cc0e6f1f9f9570650ca；主程式 MIT，Blender addon GPL-3.0-or-later。完整推論要求 Linux x86-64、24GB+ VRAM（24GB 尚未實測）、約60GB磁碟、Conda 及兩個受限 SAM 權重。8GB Windows 不相容；僅下載原始碼作評估，未安裝模型。 |
| microsoft/TRELLIS.2 | 官方原始專案可用，單體物件生成而非完整場景。依 upstream Linux/CUDA 與顯存要求選擇遠端環境；未安裝權重。 |
| Tencent-Hunyuan/Hunyuan3D-2 | 官方單體幾何與貼圖生成專案。不同幾何/貼圖階段需求不同，不能因8GB卡便宣稱完整高精度流程可跑；未安裝權重。 |

單張圖無法提供精確背面、遮擋區域或真實尺寸。高精度應補多視角與尺寸；AI 補全須標示推測。NeRF/3DGS 可自由觀看，但不等於獨立可編輯 Mesh。

## Skill 安裝

本庫已在 .agents/skills/ 安裝兩個專案 Skill。以此庫作為 Codex 工作目錄，或複製至 ~/.codex/skills/，下個回合重新載入。GitHub Actions 本身不會執行 Codex Skill；Skill 是給 Codex 使用的工作指引。沒有安裝任何壓縮代理、付費模型、全域 hooks 或停用權限的設定。

## 可選 GUI / MCP 設定

雲端批次採 bpy，不依賴 MCP。若要本機互動編修，另從 Blender 官方下載 GUI，從上述固定 commit 取得 addon.py，在 Preferences 安裝並啟用 Interface: Blender MCP。關閉 addon telemetry，再從側欄啟動 localhost:9876。只連一個 MCP client，勿公開 socket。新增的 MCP 工具通常要重載工作階段才會出現。

把 config/blender-mcp.toml 中 command 換成實際安裝的 blender-mcp.exe 絕對路徑，併入 Codex 設定並在 addon 可連線後改 enabled=true。此設定範本預設關閉，未改寫使用者全域設定，未宣稱已與 GUI 連線。未來搬移工作目錄時需更新路徑。不要使用未固定版本的 uvx blender-mcp 作為已審閱版本的替代。

雲端服務若用 fal/Tripo/Rodin/Hunyuan API，需要使用者自行開通、設定 GitHub Secrets 與預算，確認圖片可上傳。不要把金鑰寫入 JSON、Skill 或公開庫。Hugging Face gated 權重須自行同意其條款並申請。

## 來源

- https://github.com/Top3d-ai/world-builder
- https://github.com/scpli/blender-mcp
- https://github.com/AdamRolander/WorldBuilder/blob/main/docs/SETUP.md
- https://github.com/microsoft/TRELLIS.2
- https://github.com/Tencent-Hunyuan/Hunyuan3D-2
- https://docs.github.com/en/actions/concepts/runners/larger-runners
- https://docs.github.com/en/actions/tutorials/store-and-share-data
- https://developers.openai.com/codex/mcp
