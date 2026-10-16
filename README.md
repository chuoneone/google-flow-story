# google-flow-story（Google Flow 社會性故事與教學動畫穩定工作流 Skill）

讓 AI 幫你把任何「特教社會性故事、情緒教育劇本、教學短片腳本」一鍵轉換成 **Google Flow (Veo)** 最穩定、零亂碼、聲音清楚的分鏡指令與 **YouTube `.srt` 字幕檔**。

適用於 Claude Code、Antigravity、Cursor 等支援 `SKILL.md` 的 AI 工具，也可直接將 `SKILL.md` 內容貼進 Gemini Gem / ChatGPT GPTs 使用。

---

## 解決什麼問題？

直接把劇本丟進 Google Flow 自動拆鏡時，常遇到 4 大災情。本工作流透過 **5 大實測黃金鐵則** 徹底解決：

| 常見災情 | 原因 | 本工作流解法 |
| :--- | :--- | :--- |
| **1. 畫面出現亂碼假中文字** | AI 看到劇本有台詞，誤以為要在畫面上「畫出字幕」或球衣號碼 | 全域鎖定 **零文字／零數字**（連計分板、情緒溫度計都改為純光影圖示），字幕改用自動生成的 `.srt` 檔上傳 YouTube CC 字幕 |
| **2. 語音前半段清楚、後半段變外星語** | 單一鏡頭（8 秒）超過 15 字，或 AI 試圖讓角色邊動邊開口對嘴（Lip-sync），導致後半段語音失焦 | ① 強制設定**「角色閉嘴只演動作，人聲用純畫外音旁白（Voiceover）」**<br>② **每鏡台詞濃縮至 10～14 字內，且中間用句號 `。` 斷開**（強迫模型在 3～4 秒處停頓換氣、重新聚焦咬字） |
| **3. 十個場景畫面長得幾乎一樣** | 劇本多為心理狀態描述（例：覺得很生氣、決定冷靜），且都在同一地點 | 強制每鏡交替切換**「景別（遠景／中景／特寫／過肩／微仰角）」**，並將抽象情緒全部轉譯為**具體可見的肢體動作** |
| **4. 每個鏡頭主角變臉、換衣服** | 直接生影片未鎖定角色資產 | 第一步先在左側「🧍 角色」建立穿著素面無字衣服的主角，10 個場景統一綁定該角色 |

---

## 安裝方式

### 1. Antigravity / Claude Code 安裝（複製整個 repo 到 skills 資料夾）

**Claude Code**：
```bash
git clone https://github.com/chuoneone/google-flow-story.git .claude/skills/google-flow-story
```

**Antigravity**：
```bash
git clone https://github.com/chuoneone/google-flow-story.git .agent/skills/google-flow-story
```

要所有專案通用，改放使用者層級資料夾（Claude Code：`~/.claude/skills/`；Antigravity：`~/.gemini/config/skills/`）。

### 2. Gemini Gem / ChatGPT 專案安裝（免寫程式分享給同事）
直接打開 `SKILL.md`，把裡面的文字複製貼到 **Gemini 的「Gem 指令」** 或 **ChatGPT 的「自訂指令」** 中儲存即可！

---

## 怎麼使用？

直接把你的劇本或故事主題貼給 AI，例如：
> 「幫我用 Google Flow 做這支社會性故事動畫：球賽輸了，我覺得裁判不公平……」

AI 就會自動幫你產出：
1. **第一步（左欄「🧍 角色」設定指令）**
2. **第二步（右欄「📜 製作分鏡腳本」一鍵貼上防呆總指令）**
3. **第三步（3x4 分鏡預覽圖出來後的分批生成影片指令）**
4. **第四步（直接存好的 `.srt` 時間軸字幕檔，供上傳 YouTube）**
