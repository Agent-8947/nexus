# 初學者數據科學課程綱要

[![在 GitHub Codespaces 開啟](https://github.com/codespaces/badge.svg)](https://github.com/codespaces/new?hide_repo_select=true&ref=main&repo=344191198)

[![GitHub 授權](https://img.shields.io/github/license/microsoft/Data-Science-For-Beginners.svg)](https://github.com/microsoft/Data-Science-For-Beginners/blob/master/LICENSE)
[![GitHub 貢獻者](https://img.shields.io/github/contributors/microsoft/Data-Science-For-Beginners.svg)](https://GitHub.com/microsoft/Data-Science-For-Beginners/graphs/contributors/)
[![GitHub 問題](https://img.shields.io/github/issues/microsoft/Data-Science-For-Beginners.svg)](https://GitHub.com/microsoft/Data-Science-For-Beginners/issues/)
[![GitHub 拉取請求](https://img.shields.io/github/issues-pr/microsoft/Data-Science-For-Beginners.svg)](https://GitHub.com/microsoft/Data-Science-For-Beginners/pulls/)
[![歡迎 PR](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)

[![GitHub 觀察者](https://img.shields.io/github/watchers/microsoft/Data-Science-For-Beginners.svg?style=social&label=Watch)](https://GitHub.com/microsoft/Data-Science-For-Beginners/watchers/)
[![GitHub 派生](https://img.shields.io/github/forks/microsoft/Data-Science-For-Beginners.svg?style=social&label=Fork)](https://GitHub.com/microsoft/Data-Science-For-Beginners/network/)
[![GitHub 星標](https://img.shields.io/github/stars/microsoft/Data-Science-For-Beginners.svg?style=social&label=Star)](https://GitHub.com/microsoft/Data-Science-For-Beginners/stargazers/)


[![Microsoft Foundry Discord](https://dcbadge.limes.pink/api/server/nTYy5BXMWG)](https://discord.gg/nTYy5BXMWG)

[![Microsoft Foundry 開發者論壇](https://img.shields.io/badge/GitHub-Microsoft_Foundry_Developer_Forum-blue?style=for-the-badge&logo=github&color=000000&logoColor=fff)](https://aka.ms/foundry/forum)

微軟的 Azure Cloud Advocates 很高興提供一個為期10週、共20課的數據科學課程。每課包含課前及課後小測驗、完成課程的書面指引、解決方案和作業。我們採用基於項目的教學法，讓你在實作中學習，是讓新技能「牢記」的有效方式。

**衷心感謝我們的作者們：** [Jasmine Greenaway](https://www.twitter.com/paladique), [Dmitry Soshnikov](http://soshnikov.com), [Nitya Narasimhan](https://twitter.com/nitya), [Jalen McGee](https://twitter.com/JalenMcG), [Jen Looper](https://twitter.com/jenlooper), [Maud Levy](https://twitter.com/maudstweets), [Tiffany Souterre](https://twitter.com/TiffanySouterre), [Christopher Harrison](https://www.twitter.com/geektrainer)。

**🙏 特別感謝 🙏 我們的 [Microsoft 學生大使](https://studentambassadors.microsoft.com/) 作者、審核者和內容貢獻者，** 尤其是 Aaryan Arora、[Aditya Garg](https://github.com/AdityaGarg00)、[Alondra Sanchez](https://www.linkedin.com/in/alondra-sanchez-molina/)、[Ankita Singh](https://www.linkedin.com/in/ankitasingh007)、[Anupam Mishra](https://www.linkedin.com/in/anupam--mishra/)、[Arpita Das](https://www.linkedin.com/in/arpitadas01/)、ChhailBihari Dubey、[Dibri Nsofor](https://www.linkedin.com/in/dibrinsofor)、[Dishita Bhasin](https://www.linkedin.com/in/dishita-bhasin-7065281bb)、[Majd Safi](https://www.linkedin.com/in/majd-s/)、[Max Blum](https://www.linkedin.com/in/max-blum-6036a1186/)、[Miguel Correa](https://www.linkedin.com/in/miguelmque/)、[Mohamma Iftekher (Iftu) Ebne Jalal](https://twitter.com/iftu119)、[Nawrin Tabassum](https://www.linkedin.com/in/nawrin-tabassum)、[Raymond Wangsa Putra](https://www.linkedin.com/in/raymond-wp/)、[Rohit Yadav](https://www.linkedin.com/in/rty2423)、Samridhi Sharma、[Sanya Sinha](https://www.linkedin.com/mwlite/in/sanya-sinha-13aab1200)、
[Sheena Narula](https://www.linkedin.com/in/sheena-narua-n/)、[Tauqeer Ahmad](https://www.linkedin.com/in/tauqeerahmad5201/)、Yogendrasingh Pawar 、[Vidushi Gupta](https://www.linkedin.com/in/vidushi-gupta07/)、[Jasleen Sondhi](https://www.linkedin.com/in/jasleen-sondhi/)

|![由 @sketchthedocs 繪製草圖筆記 https://sketchthedocs.dev](../../translated_images/zh-MO/00-Title.8af36cd35da1ac55.webp)|
|:---:|
| 初學者數據科學 - _草圖筆記由 [@nitya](https://twitter.com/nitya) 繪製_ |

### 🌐 多語言支援

#### 透過 GitHub Action 支援（自動及持續更新）

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[阿拉伯語](../ar/README.md) | [孟加拉語](../bn/README.md) | [保加利亞語](../bg/README.md) | [緬甸語](../my/README.md) | [中文（簡體）](../zh-CN/README.md) | [中文（繁體，香港）](../zh-HK/README.md) | [中文（繁體，澳門）](./README.md) | [中文（繁體，台灣）](../zh-TW/README.md) | [克羅地亞語](../hr/README.md) | [捷克語](../cs/README.md) | [丹麥語](../da/README.md) | [荷蘭語](../nl/README.md) | [愛沙尼亞語](../et/README.md) | [芬蘭語](../fi/README.md) | [法語](../fr/README.md) | [德語](../de/README.md) | [希臘語](../el/README.md) | [希伯來語](../he/README.md) | [印地語](../hi/README.md) | [匈牙利語](../hu/README.md) | [印度尼西亞語](../id/README.md) | [義大利語](../it/README.md) | [日語](../ja/README.md) | [坎納達語](../kn/README.md) | [韓語](../ko/README.md) | [立陶宛語](../lt/README.md) | [馬來語](../ms/README.md) | [馬拉雅拉姆語](../ml/README.md) | [馬拉地語](../mr/README.md) | [尼泊爾語](../ne/README.md) | [奈及利亞皮欽語](../pcm/README.md) | [挪威語](../no/README.md) | [波斯語（法爾西語）](../fa/README.md) | [波蘭語](../pl/README.md) | [葡萄牙語（巴西）](../pt-BR/README.md) | [葡萄牙語（葡萄牙）](../pt-PT/README.md) | [旁遮普語（古爾穆克希）](../pa/README.md) | [羅馬尼亞語](../ro/README.md) | [俄語](../ru/README.md) | [塞爾維亞語（西里爾字母）](../sr/README.md) | [斯洛伐克語](../sk/README.md) | [斯洛文尼亞語](../sl/README.md) | [西班牙語](../es/README.md) | [斯瓦希里語](../sw/README.md) | [瑞典語](../sv/README.md) | [他加祿語（菲律賓語）](../tl/README.md) | [泰米爾語](../ta/README.md) | [泰盧固語](../te/README.md) | [泰語](../th/README.md) | [土耳其語](../tr/README.md) | [烏克蘭語](../uk/README.md) | [烏爾都語](../ur/README.md) | [越南語](../vi/README.md)

> **想要本地端克隆？**
>
> 本儲存庫包含50餘種語言翻譯，會大幅增加下載大小。若想不帶翻譯檔案克隆，可使用稀疏檢出：
>
> **Bash / macOS / Linux：**
> ```bash
> git clone --filter=blob:none --sparse https://github.com/microsoft/Data-Science-For-Beginners.git
> cd Data-Science-For-Beginners
> git sparse-checkout set --no-cone '/*' '!translations' '!translated_images'
> ```
>
> **CMD（Windows）：**
> ```cmd
> git clone --filter=blob:none --sparse https://github.com/microsoft/Data-Science-For-Beginners.git
> cd Data-Science-For-Beginners
> git sparse-checkout set --no-cone "/*" "!translations" "!translated_images"
> ```
>
> 這樣讓你以更快的速度取得完成課程所需所有資源。
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

**如欲增加其他翻譯語言，請參閱此處列出的支援語言清單 [here](https://github.com/Azure/co-op-translator/blob/main/getting_started/supported-languages.md)**

#### 加入我們的社群  
[![Microsoft Foundry Discord](https://dcbadge.limes.pink/api/server/nTYy5BXMWG)](https://discord.gg/nTYy5BXMWG)

我們目前正在進行 Discord AI 學習系列，歡迎了解並於 2025 年 9 月 18 日至 30 日加入我們：[Learn with AI Series](https://aka.ms/learnwithai/discord)。你將學到使用 GitHub Copilot 進行數據科學的秘訣與技巧。

![Learn with AI 系列](../../translated_images/zh-MO/1.2b28cdc6205e26fe.webp)

# 你是學生嗎？

開始使用以下資源：

- [學生中心頁面](https://docs.microsoft.com/en-gb/learn/student-hub?WT.mc_id=academic-77958-bethanycheum) 在此頁面，你會找到初學者資源、學生包甚至免費證書兌換券的取得方式。這是你想要加入書籤並定期查看的頁面，因為我們至少每月更換內容一次。
- [Microsoft Learn 學生大使](https://studentambassadors.microsoft.com?WT.mc_id=academic-77958-bethanycheum) 加入全球學生大使社群，這可能是你進入微軟的橋樑。

# 入門指南

## 📚 文件資料

- **[安裝指南](INSTALLATION.md)** - 初學者的分步設定指引
- **[使用指南](USAGE.md)** - 範例與常用工作流程
- **[故障排除](TROUBLESHOOTING.md)** - 常見問題解決方案
- **[貢獻指南](CONTRIBUTING.md)** - 如何參與此專案
- **[教師專區](for-teachers.md)** - 教學指導與課堂資源

## 👨‍🎓 學生專區
> **完全初學者**：剛開始接觸數據科學？請先從我們的 [初學者範例](examples/README.md) 開始！這些簡單且附有良好註解的範例，將幫助你在深入完整課程前，理解基本概念。
> **[學生們](https://aka.ms/student-page)**：想要自行使用本課程，請複製整個倉庫，並自行完成練習，從課前小測驗開始。然後閱讀課程並完成其他活動。盡量透過理解課程來創建專案，而非直接複製解答程式碼；不過每個基於專案的課程都在 /solutions 目錄備有程式碼。另一個方式是和朋友組成學習小組，一同進行內容。進一步學習我們推薦使用 [Microsoft Learn](https://docs.microsoft.com/en-us/users/jenlooper-2911/collections/qprpajyoy3x0g7?WT.mc_id=academic-77958-bethanycheum)。

**快速開始：**
1. 查看 [安裝指南](INSTALLATION.md) 以設定你的環境
2. 閱讀 [使用指南](USAGE.md) 以學習如何使用課程
3. 從第一課開始，按順序完成各課
4. 加入我們的 [Discord 社群](https://aka.ms/ds4beginners/discord) 尋求支援

## 👩‍🏫 教師專區
> **教師**：我們已[包含一些建議](for-teachers.md)說明如何使用此課程。歡迎您在[討論區](https://github.com/microsoft/Data-Science-For-Beginners/discussions)留下您的意見！

## 認識團隊

[![宣傳影片](../../ds-for-beginners.gif)](https://youtu.be/8mzavjQSMM4 "宣傳影片")

**動圖由** [Mohit Jaisal](https://www.linkedin.com/in/mohitjaisal) 製作

> 🎥 點擊上方圖片觀看關於專案和創作者們的影片！

## 教學法

在設計本課程時，我們選擇了兩個教學原則：確保課程以專案為基礎，並包含頻繁的測驗。到本系列課程結束時，學生將學會資料科學的基本原理，包括倫理概念、資料準備、不同的資料處理方式、資料視覺化、資料分析、資料科學的實際應用案例等。

另外，課前的低壓力測驗可幫助學生設定學習主題的意圖，而課後的第二次測驗則確保持續記憶。此課程設計具彈性且有趣，可整體或部分學習。專案從簡單開始，並在十週的學習週期結束時逐漸增加難度。

> 請參閱我們的[行為準則](CODE_OF_CONDUCT.md)、[貢獻指南](CONTRIBUTING.md)、[翻譯指南](TRANSLATIONS.md)。歡迎您提供建設性的回饋！

## 每堂課包含：

- 選用的手繪筆記
- 選用的補充影片
- 課前暖身測驗
- 書面課程
- 專案課程包含的逐步專案建置指引
- 知識檢測
- 挑戰題
- 補充閱讀
- 作業
- [課後測驗](https://ff-quizzes.netlify.app/en/)

> **關於測驗的說明**：所有測驗均位於 Quiz-App 資料夾中，共有40個，每個包含三個問題。測驗連結嵌入於課程中，但測驗應用程式可本地執行或部署至 Azure；請參考 `quiz-app` 資料夾中的說明。測驗正在逐步本地化。

## 🎓 初學者友善範例

**剛接觸資料科學？** 我們建立了特殊的[範例目錄](examples/README.md)，包含簡單且詳盡註解的程式碼幫助您入門：

- 🌟 **Hello World** - 您的第一個資料科學程式
- 📂 **資料載入** - 學習讀取與探索資料集
- 📊 **簡單分析** - 計算統計並尋找模式
- 📈 **基礎視覺化** - 創建圖表與圖形
- 🔬 **實務專案** - 從頭到尾完整工作流程

每個範例均包含詳細註解解說每步驟，適合完全的新手！

👉 **[從範例開始](examples/README.md)** 👈

## 課程列表


|![ Sketchnote by @sketchthedocs https://sketchthedocs.dev](../../translated_images/zh-MO/00-Roadmap.4905d6567dff4753.webp)|
|:---:|
| 資料科學初學者：路線圖 - _手繪筆記由 [@nitya](https://twitter.com/nitya)_ |


| 課程編號 | 主題 | 課程分組 | 學習目標 | 連結課程 | 作者 |
| :-----------: | :----------------------------------------: | :--------------------------------------------------: | :-----------------------------------------------------------------------------------------------------------------------------------------------------------------------: | :---------------------------------------------------------------------: | :----: |
| 01 | 定義資料科學 | [介紹](1-Introduction/README.md) | 了解資料科學的基本概念及其與人工智慧、機器學習和大數據的關聯。 | [課程](1-Introduction/01-defining-data-science/README.md) [影片](https://youtu.be/beZ7Mb_oz9I) | [Dmitry](http://soshnikov.com) |
| 02 | 資料科學倫理 | [介紹](1-Introduction/README.md) | 資料倫理概念、挑戰與架構。 | [課程](1-Introduction/02-ethics/README.md) | [Nitya](https://twitter.com/nitya) |
| 03 | 定義資料 | [介紹](1-Introduction/README.md) | 資料的分類及其常見來源。 | [課程](1-Introduction/03-defining-data/README.md) | [Jasmine](https://www.twitter.com/paladique) |
| 04 | 統計與機率導論 | [介紹](1-Introduction/README.md) | 使用機率與統計的數學技術來了解資料。 | [課程](1-Introduction/04-stats-and-probability/README.md) [影片](https://youtu.be/Z5Zy85g4Yjw) | [Dmitry](http://soshnikov.com) |
| 05 | 使用關聯式資料 | [資料處理](2-Working-With-Data/README.md) | 關聯式資料介紹及使用結構化查詢語言（SQL，發音為 “see-quell”）探索和分析關聯式資料的基礎。 | [課程](2-Working-With-Data/05-relational-databases/README.md) | [Christopher](https://www.twitter.com/geektrainer) | | |
| 06 | 使用 NoSQL 資料 | [資料處理](2-Working-With-Data/README.md) | 非關聯式資料介紹、種類及探索和分析文件型資料庫的基礎。 | [課程](2-Working-With-Data/06-non-relational/README.md) | [Jasmine](https://twitter.com/paladique) |
| 07 | 使用 Python | [資料處理](2-Working-With-Data/README.md) | 使用 Python 進行資料探索的基礎，包含 Pandas 等函式庫。建議具備 Python 程式基礎。 | [課程](2-Working-With-Data/07-python/README.md) [影片](https://youtu.be/dZjWOGbsN4Y) | [Dmitry](http://soshnikov.com) |
| 08 | 資料準備 | [資料處理](2-Working-With-Data/README.md) | 資料清理與轉換技術，應對缺失、不準確或不完整資料的挑戰。 | [課程](2-Working-With-Data/08-data-preparation/README.md) | [Jasmine](https://www.twitter.com/paladique) |
| 09 | 量化視覺化 | [資料視覺化](3-Data-Visualization/README.md) | 學習使用 Matplotlib 來視覺化鳥類資料 🦆 | [課程](3-Data-Visualization/09-visualization-quantities/README.md) | [Jen](https://twitter.com/jenlooper) |
| 10 | 資料分佈視覺化 | [資料視覺化](3-Data-Visualization/README.md) | 在區間內視覺化觀察與趨勢。 | [課程](3-Data-Visualization/10-visualization-distributions/README.md) | [Jen](https://twitter.com/jenlooper) |
| 11 | 比例視覺化 | [資料視覺化](3-Data-Visualization/README.md) | 視覺化離散和分組百分比。 | [課程](3-Data-Visualization/11-visualization-proportions/README.md) | [Jen](https://twitter.com/jenlooper) |
| 12 | 關係視覺化 | [資料視覺化](3-Data-Visualization/README.md) | 視覺化資料集及其變量間的連結和相關性。 | [課程](3-Data-Visualization/12-visualization-relationships/README.md) | [Jen](https://twitter.com/jenlooper) |
| 13 | 有意義的視覺化 | [資料視覺化](3-Data-Visualization/README.md) | 創造有價值視覺化的技巧與指導，有助於有效解決問題和獲得見解。 | [課程](3-Data-Visualization/13-meaningful-visualizations/README.md) | [Jen](https://twitter.com/jenlooper) |
| 14 | 資料科學生命週期導論 | [生命週期](4-Data-Science-Lifecycle/README.md) | 資料科學生命週期介紹及其第一步驟：取得與提取資料。 | [課程](4-Data-Science-Lifecycle/14-Introduction/README.md) | [Jasmine](https://twitter.com/paladique) |
| 15 | 分析 | [生命週期](4-Data-Science-Lifecycle/README.md) | 資料科學生命週期中著重於資料分析的階段。 | [課程](4-Data-Science-Lifecycle/15-analyzing/README.md) | [Jasmine](https://twitter.com/paladique) | | |
| 16 | 溝通 | [生命週期](4-Data-Science-Lifecycle/README.md) | 資料科學生命週期中專注於以便於決策者理解的方式呈現資料洞見的階段。 | [課程](4-Data-Science-Lifecycle/16-communication/README.md) | [Jalen](https://twitter.com/JalenMcG) | | |
| 17 | 雲端資料科學 | [雲端資料](5-Data-Science-In-Cloud/README.md) | 介紹雲端資料科學及其好處。 | [課程](5-Data-Science-In-Cloud/17-Introduction/README.md) | [Tiffany](https://twitter.com/TiffanySouterre) 及 [Maud](https://twitter.com/maudstweets) |
| 18 | 雲端資料科學 | [雲端資料](5-Data-Science-In-Cloud/README.md) | 使用低碼工具訓練模型。 |[課程](5-Data-Science-In-Cloud/18-Low-Code/README.md) | [Tiffany](https://twitter.com/TiffanySouterre) 及 [Maud](https://twitter.com/maudstweets) |
| 19 | 雲端資料科學 | [雲端資料](5-Data-Science-In-Cloud/README.md) | 使用 Azure 機器學習工作室部署模型。 | [課程](5-Data-Science-In-Cloud/19-Azure/README.md)| [Tiffany](https://twitter.com/TiffanySouterre) 及 [Maud](https://twitter.com/maudstweets) |
| 20 | 實務資料科學 | [實務](6-Data-Science-In-Wild/README.md) | 實際世界中由資料科學驅動的專案。 | [課程](6-Data-Science-In-Wild/20-Real-World-Examples/README.md) | [Nitya](https://twitter.com/nitya) |

## GitHub Codespaces

按照以下步驟在 Codespace 中開啟此範例：
1. 點擊 Code 下拉選單，選擇 Open with Codespaces。
2. 在面板底部選擇 + New codespace。
欲了解更多，請參考[GitHub 文件](https://docs.github.com/en/codespaces/developing-in-codespaces/creating-a-codespace-for-a-repository#creating-a-codespace)。

## VSCode 遠端容器

使用您的本機電腦和 VSCode 搭配 VS Code Remote - Containers 擴充功能，在容器中打開此儲存庫，步驟如下：

1. 若您是首次使用開發容器，請確保系統符合先決條件（例如已安裝 Docker），請參考[入門文件](https://code.visualstudio.com/docs/devcontainers/containers#_getting-started)。

使用此儲存庫，您可以選擇在獨立 Docker 卷中開啟儲存庫：

**注意**：底層將使用 Remote-Containers 的 **Clone Repository in Container Volume...** 指令，將原始碼克隆到 Docker 卷中，而非本地檔案系統。 [卷](https://docs.docker.com/storage/volumes/) 是持久化容器資料的首選機制。

或是開啟本地克隆或下載的儲存庫副本：

- 將儲存庫克隆至本地檔案系統。
- 按 F1，選擇 **Remote-Containers: Open Folder in Container...** 指令。
- 選擇剛剛克隆的資料夾，等待容器啟動，開始嘗試。

## 離線存取

您可以使用 [Docsify](https://docsify.js.org/#/) 進行離線瀏覽此文件。將此儲存庫分叉，於本機安裝 [Docsify](https://docsify.js.org/#/quickstart)，然後在本儲存庫根目錄輸入 `docsify serve`，網站將於本地主機的3000端口執行：`localhost:3000`。

> 注意，筆記本不會透過 Docsify 呈現，當您需要執行筆記本時，請在 VS Code 中使用 Python 核心單獨執行。

## 其他課程

我們團隊也製作其他課程！歡迎參考：

<!-- CO-OP TRANSLATOR OTHER COURSES START -->
### LangChain
[![LangChain4j for Beginners](https://img.shields.io/badge/LangChain4j%20for%20Beginners-22C55E?style=for-the-badge&&labelColor=E5E7EB&color=0553D6)](https://aka.ms/langchain4j-for-beginners)
[![LangChain.js 入門](https://img.shields.io/badge/LangChain.js%20for%20Beginners-22C55E?style=for-the-badge&labelColor=E5E7EB&color=0553D6)](https://aka.ms/langchainjs-for-beginners?WT.mc_id=m365-94501-dwahlin)
[![LangChain 入門](https://img.shields.io/badge/LangChain%20for%20Beginners-22C55E?style=for-the-badge&labelColor=E5E7EB&color=0553D6)](https://github.com/microsoft/langchain-for-beginners?WT.mc_id=m365-94501-dwahlin)
---

### Azure / Edge / MCP / Agents
[![AZD 入門](https://img.shields.io/badge/AZD%20for%20Beginners-0078D4?style=for-the-badge&labelColor=E5E7EB&color=0078D4)](https://github.com/microsoft/AZD-for-beginners?WT.mc_id=academic-105485-koreyst)
[![Edge AI 入門](https://img.shields.io/badge/Edge%20AI%20for%20Beginners-00B8E4?style=for-the-badge&labelColor=E5E7EB&color=00B8E4)](https://github.com/microsoft/edgeai-for-beginners?WT.mc_id=academic-105485-koreyst)
[![MCP 入門](https://img.shields.io/badge/MCP%20for%20Beginners-009688?style=for-the-badge&labelColor=E5E7EB&color=009688)](https://github.com/microsoft/mcp-for-beginners?WT.mc_id=academic-105485-koreyst)
[![AI Agents 入門](https://img.shields.io/badge/AI%20Agents%20for%20Beginners-00C49A?style=for-the-badge&labelColor=E5E7EB&color=00C49A)](https://github.com/microsoft/ai-agents-for-beginners?WT.mc_id=academic-105485-koreyst)

---

### 生成式 AI 系列
[![生成式 AI 入門](https://img.shields.io/badge/Generative%20AI%20for%20Beginners-8B5CF6?style=for-the-badge&labelColor=E5E7EB&color=8B5CF6)](https://github.com/microsoft/generative-ai-for-beginners?WT.mc_id=academic-105485-koreyst)
[![生成式 AI (.NET)](https://img.shields.io/badge/Generative%20AI%20(.NET)-9333EA?style=for-the-badge&labelColor=E5E7EB&color=9333EA)](https://github.com/microsoft/Generative-AI-for-beginners-dotnet?WT.mc_id=academic-105485-koreyst)
[![生成式 AI (Java)](https://img.shields.io/badge/Generative%20AI%20(Java)-C084FC?style=for-the-badge&labelColor=E5E7EB&color=C084FC)](https://github.com/microsoft/generative-ai-for-beginners-java?WT.mc_id=academic-105485-koreyst)
[![生成式 AI (JavaScript)](https://img.shields.io/badge/Generative%20AI%20(JavaScript)-E879F9?style=for-the-badge&labelColor=E5E7EB&color=E879F9)](https://github.com/microsoft/generative-ai-with-javascript?WT.mc_id=academic-105485-koreyst)

---

### 核心學習
[![機器學習入門](https://img.shields.io/badge/ML%20for%20Beginners-22C55E?style=for-the-badge&labelColor=E5E7EB&color=22C55E)](https://aka.ms/ml-beginners?WT.mc_id=academic-105485-koreyst)
[![數據科學入門](https://img.shields.io/badge/Data%20Science%20for%20Beginners-84CC16?style=for-the-badge&labelColor=E5E7EB&color=84CC16)](https://aka.ms/datascience-beginners?WT.mc_id=academic-105485-koreyst)
[![人工智能入門](https://img.shields.io/badge/AI%20for%20Beginners-A3E635?style=for-the-badge&labelColor=E5E7EB&color=A3E635)](https://aka.ms/ai-beginners?WT.mc_id=academic-105485-koreyst)
[![網絡安全入門](https://img.shields.io/badge/Cybersecurity%20for%20Beginners-F97316?style=for-the-badge&labelColor=E5E7EB&color=F97316)](https://github.com/microsoft/Security-101?WT.mc_id=academic-96948-sayoung)
[![網頁開發入門](https://img.shields.io/badge/Web%20Dev%20for%20Beginners-EC4899?style=for-the-badge&labelColor=E5E7EB&color=EC4899)](https://aka.ms/webdev-beginners?WT.mc_id=academic-105485-koreyst)
[![物聯網入門](https://img.shields.io/badge/IoT%20for%20Beginners-14B8A6?style=for-the-badge&labelColor=E5E7EB&color=14B8A6)](https://aka.ms/iot-beginners?WT.mc_id=academic-105485-koreyst)
[![XR 開發入門](https://img.shields.io/badge/XR%20Development%20for%20Beginners-38BDF8?style=for-the-badge&labelColor=E5E7EB&color=38BDF8)](https://github.com/microsoft/xr-development-for-beginners?WT.mc_id=academic-105485-koreyst)

---

### Copilot 系列
[![Copilot 供 AI 配對編程](https://img.shields.io/badge/Copilot%20for%20AI%20Paired%20Programming-FACC15?style=for-the-badge&labelColor=E5E7EB&color=FACC15)](https://aka.ms/GitHubCopilotAI?WT.mc_id=academic-105485-koreyst)
[![Copilot 供 C#/.NET](https://img.shields.io/badge/Copilot%20for%20C%23/.NET-FBBF24?style=for-the-badge&labelColor=E5E7EB&color=FBBF24)](https://github.com/microsoft/mastering-github-copilot-for-dotnet-csharp-developers?WT.mc_id=academic-105485-koreyst)
[![Copilot 探險](https://img.shields.io/badge/Copilot%20Adventure-FDE68A?style=for-the-badge&labelColor=E5E7EB&color=FDE68A)](https://github.com/microsoft/CopilotAdventures?WT.mc_id=academic-105485-koreyst)
<!-- CO-OP TRANSLATOR OTHER COURSES END -->

## 尋求協助

**遇到問題嗎？** 請查看我們的 [疑難排解指南](TROUBLESHOOTING.md) 來尋找常見問題的解決方法。

如果你在建構 AI 應用程式時遇到阻礙或有任何疑問，歡迎加入 MCP 學習者與經驗豐富的開發者討論社群。這是一個支持性強的社區，任何問題都可提出，並且知識會自由分享。

[![Microsoft Foundry Discord](https://dcbadge.limes.pink/api/server/nTYy5BXMWG)](https://discord.gg/nTYy5BXMWG)

如果你有產品反饋或在建構過程中發現錯誤，請訪問：

[![Microsoft Foundry 開發者論壇](https://img.shields.io/badge/GitHub-Microsoft_Foundry_Developer_Forum-blue?style=for-the-badge&logo=github&color=000000&logoColor=fff)](https://aka.ms/foundry/forum)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免責聲明**：  
本文件係使用 AI 翻譯服務 [Co-op Translator](https://github.com/Azure/co-op-translator) 翻譯而成。雖然我們致力於確保準確性，但請注意，自動翻譯可能包含錯誤或不準確之處。原始文件的母語版本應被視為權威版本。對於重要資訊，建議採用專業人工翻譯。我們不對因使用此翻譯而引起的誤解或曲解承擔任何責任。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->