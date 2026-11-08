# Image to editable Blender scene

圖片轉可編輯 Blender 場景的 Codex Skills 與 GitHub Actions 工作流程。

目前提供可執行的 CPU bpy 組裝、獨立 Mesh/材質/Collection、四視角預覽與重新開檔驗證。範例為環境測試，並非自動照片重建；高精度推論需另行配置足夠顯存的 Linux GPU 或授權雲端服務。

請讀 [設定、限制與專案評估](docs/setup.md)。在 Actions 手動執行 **Build editable Blender scene**，完成後下載 **editable-blender-scene** artifact。

兩個 Skill：image-to-blender-scene、token-saver。Token Saver 為原創指引型 Skill，不修改模型或帳戶限制。
