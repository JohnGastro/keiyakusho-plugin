# keiyakusho プラグイン マーケットプレイス

全日本不動産協会（ラビーネット）の統一書式に準拠した不動産契約書の作成と、不動産調査ワークフローを支援するCoworkプラグインです。

## インストール

### マーケットプレイスから（推奨）

1. Coworkの「Customize」→「マーケットプレイスを追加」
2. URL: `https://github.com/JohnGastro/keiyakusho-plugin`
3. 「同期」をクリック

### .pluginファイルから

1. [GitHub Releases](https://github.com/JohnGastro/keiyakusho-plugin/releases) から `keiyakusho.plugin` をダウンロード
2. Coworkの「Customize」→ プラグインをアップロード

テンプレート（Excelファイル298個）はプラグインに同梱されています。インストール後すぐに使えます。

## 含まれるプラグイン

### keiyakusho

ラビーネット書式での契約書作成（売買、賃貸借、媒介契約、覚書、付帯書類）と不動産調査ガイドを提供します。

#### スキル

- **keiyakusho** — 契約書作成ワークフロー
- **fudosan-chosa** — 不動産調査ガイド、チェックリスト生成、物件フォルダ管理（大分市特化の窓口案内付き）

#### コマンド

| コマンド | 説明 |
|---------|------|
| `/shinki-bukken` | 新しい物件フォルダを作成 |
| `/chosa-checklist` | 不動産調査チェックリストを生成 |
| `/keiyakusho-sakusei` | ラビーネット書式で契約書を作成 |

## 対応エリア

現在は **大分市** に特化した窓口情報を提供しています。

## ライセンス

ラビーネットのテンプレートは全日本不動産協会会員のみ利用可能です。社外への再配布は禁止です。
