#!/bin/bash
# Claudeの応答完了時にプラグインの変更をcommitする
# push は .githooks/post-commit が自動で行う
PLUGIN_DIR="${CLAUDE_PLUGIN_ROOT:-$(dirname "$(dirname "$(dirname "$0")")")}"

cd "$PLUGIN_DIR" || exit 0

# gitリポジトリでなければスキップ
if [ ! -d .git ]; then
  echo '{"decision":"approve","reason":"gitリポジトリではありません"}'
  exit 0
fi

# .githooksをgitのhooksディレクトリに設定（初回のみ効く）
git config core.hooksPath .githooks 2>/dev/null

# 変更がなければスキップ
if git diff --quiet && git diff --cached --quiet && [ -z "$(git ls-files --others --exclude-standard)" ]; then
  echo '{"decision":"approve","reason":"変更なし"}'
  exit 0
fi

# ステージ → コミット（post-commitフックが自動pushする）
git add -A
git commit -m "auto: プラグイン更新 $(date '+%Y-%m-%d %H:%M')" --no-verify 2>&1

echo '{"decision":"approve","reason":"変更をコミットしました"}'
