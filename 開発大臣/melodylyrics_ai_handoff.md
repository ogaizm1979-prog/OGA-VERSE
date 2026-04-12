# MelodyLyrics — AI引き継ぎ書

> **Purpose**: AIがこのプロジェクトに関して、毎回ゼロから説明を受けずに的確なサポートができるようにするための引き継ぎ書。

---

## 1. AI Instructions（AIへの行動指針）

- **コードは書けないユーザー**。Claude Codeとの会話で開発を進めているため、技術的な実装はAIが主導する
- 提案するときは「なぜそうするか」の理由を簡潔に添える
- 実装前に設計方針を確認し、合意してから進める
- 変更は必ず worktree → main へのマージというフローで行う
- **ビルドが通ることを確認してからコミット**する
- 日本語でコミュニケーションする

---

## 2. プロジェクト概要

| 項目 | 内容 |
|---|---|
| アプリ名 | **MelodyLyrics** |
| 種別 | macOS ネイティブアプリ |
| 目的 | MIDIメロディを読み込んでAIが歌詞を生成するツール |
| ターゲット | 作曲家・作詞家（自分用から始め、将来は配布も視野） |
| 位置づけ | 既存サービスにない独自プロダクト |

**ユニークな点**: メロディのスロット情報（音の長さ・アクセント・フレーズ区切り）をLLMに渡すことで、メロディに「乗る」歌詞を生成する仕組み。単なる歌詞生成ではなく、音楽的制約を守った生成が目標。

---

## 3. 技術スタック

```
言語       : Swift / SwiftUI
MIDIパース : MIDIKit (Swift Package Manager)
AI API     : Claude API（現在実装済み）
             ※将来：ChatGPT / Gemini にも対応予定
             　（月額プランに入っているユーザーがログインして使える形）
ストレージ : macOS Keychain（APIキー保存）
プロジェクト: .melodylyrics（JSON形式、MIDIデータをBase64埋め込み）
開発環境   : Claude Code + Cursor
```

---

## 4. 現在の実装状態（フェーズ2進行中）

### 完成済み ✅

| 機能 | 詳細 |
|---|---|
| MIDIパーサー | MIDIKit使用、19テスト通過、テンポ/拍子欠落時のtyped error |
| MIDIファイル読み込み | NSOpenPanel（常時ヘッダーボタン）+ ドラッグ&ドロップ |
| ピアノロール表示 | ノート描画・鍵盤・ズームスライダー・セクション色分け |
| プレイヘッド | 表示・スクロール同期・クリックシーク |
| トランスポートLCD | BPM・拍子・小節番号表示 |
| セクション/フレーズ表示 | RegionLane・左ペインのアコーディオン |
| セクション手動編集 | 右クリックでプリセット選択（Verse/Chorus等）+ 自由入力リネーム |
| フレーズ手動編集 | 分割・結合・移動（セクション間） |
| スロットシステム | 同音連続・装飾音を自動グルーピング、アクセント判定 |
| Claude APIクライアント | フレーズのスロット+ノートをJSONペイロードで送信、歌詞候補を返す |
| 設定シート | APIキー入力（Keychain保存）+ グローバル指示/スタイルシート |
| プロジェクトファイル | .melodylyrics（JSON）: 保存・読み込み・最近使った項目 |
| ファイルメニュー | 新規(⌘N) / 開く(⌘O) / 保存(⌘S) / 別名で保存(⇧⌘S) / MIDIを読み込む |

### 実装予定・検討中 🔲

| 機能 | 優先度 | 備考 |
|---|---|---|
| Canon（確定歌詞コンテキスト） | 高 | 採用済み歌詞をAPIペイロードに含めて一貫性向上 |
| Working Set | 高 | 生成対象セクションをチェックで選択、トークン節約 |
| バージョン履歴 | 中 | 生成結果を保存・比較・復元 |
| ChatGPT / Gemini 対応 | 中 | 月額プランのユーザーがログインして使える形 |
| フレーズ境界の手動マーカー | 低 | タイムライン上でフレーズ区切りを自由に配置 |
| エンドツーエンド動作確認 | - | 実MIDIファイル + APIキーで通し検証 |

---

## 5. ディレクトリ構成（主要ファイル）

```
MelodyLyrics/
├── MelodyLyricsApp.swift          # エントリーポイント + FileMenuCommands
├── ContentView.swift              # メインレイアウト（ヘッダー + 3ペイン）
├── Commands/
│   └── FileMenuCommands.swift     # ファイルメニュー実装
├── Models/
│   └── DataModels.swift           # MelodyNote, Slot, SlotBuilder 等
├── Services/
│   ├── MIDIParser.swift           # MIDIKitを使ったパーサー
│   ├── ClaudeClient.swift         # Claude API通信 + KeychainHelper
│   └── ProjectDocument.swift      # .melodylyrics形式の保存/読み込み
├── ViewModels/
│   └── AppState.swift             # @Observable 状態管理（全UI状態）
├── Views/
│   ├── CenterPane/
│   │   ├── PianoRollView.swift    # ピアノロール（Canvas描画）
│   │   ├── RegionLaneView.swift   # セクションブロック表示
│   │   ├── TransportLCDView.swift # トランスポートコントロール
│   │   ├── BreadcrumbBar.swift    # パンくずナビ
│   │   └── AIChatView.swift       # AIチャット入力/表示
│   ├── LeftPane/
│   │   ├── LeftInspectorView.swift
│   │   ├── SectionAccordion.swift
│   │   └── SlotsAccordion.swift
│   ├── RightPane/
│   │   └── RightLyricsView.swift  # 歌詞候補パネル
│   └── Shared/
│       ├── MIDIDropOverlay.swift   # ドラッグ&ドロップUI
│       ├── TrackPickerSheet.swift  # トラック選択
│       ├── ManualMetaInputSheet.swift # BPM/拍子手動入力
│       └── SettingsSheet.swift     # APIキー設定
└── Theme/
    └── DAWTheme.swift              # カラー・フォント定数
```

---

## 6. 重要な設計方針

### スロットシステム
- 1スロット = 1歌詞音節（モーラ）
- 同ピッチ連続 + 休符なし → 1スロットにまとめる（タイ）
- 32分音符以下（< 0.125 beats）の装飾音 → 直後ノートとマージ
- アクセント判定：beat 1.0 または 3.0 始まりが `.strong`

### JSONペイロード（Claude API送信形式）
```json
{
  "bpm": 120,
  "time_signature": "4/4",
  "section": "Chorus",
  "slot_count": 8,
  "slots": [
    { "slot_index": 0, "duration_beats_total": 1.0, "accent": "strong" },
    ...
  ],
  "melody_notes": [
    { "index": 0, "pitch": "C4", "bar": 1, "beat": 1.0, "duration_beats": 0.5 },
    ...
  ]
}
```

### プロジェクトファイル（.melodylyrics）
- JSON形式、MIDIデータをBase64で埋め込み（ファイル移動で壊れない）
- sections / phrases / slots / 歌詞 / BPM / 拍子 / グローバル指示を保存

### Gitワークフロー
- 機能ごとに `git worktree add .claude/worktrees/<name> -b claude/<name>` でブランチ作成
- ビルド確認 → コミット → mainへマージ

---

## 7. 基本情報

| 項目 | 内容 |
|---|---|
| 名前 | おがちん |
| 居住地 | 鎌倉 |
| 職業 | フリーランス広告音楽プロデューサー |
| 音楽パートナー | 妻・しおりさん |
| 意思決定の軸 | 家族最優先・面白いかどうか・流れに乗っているか |
| 最終目標 | Universe.com |
| 開発スタイル | コードは書かずClaudeとの会話で開発。実装はAI主導 |

---

## 8. 未対応・要検討事項

- [ ] **AI連携の拡張**: ChatGPT / Gemini への対応方法（OAuth? APIキー?）
- [ ] **フレーズ境界の自動提案**: MIDIの休符・音量変化から自動分割（Phase 3）
- [ ] **配布方法**: App Store vs 個人配布（サンドボックス制約が関係）
- [ ] **バージョン履歴UI**: 生成結果の比較ビューのデザイン
- [ ] **Canon実装**: 確定歌詞をどのUI操作で「Canon」にするか
- [ ] **Working Set**: セクション一覧でのチェックボックスUI

---

*最終更新: 2026-04-06*
