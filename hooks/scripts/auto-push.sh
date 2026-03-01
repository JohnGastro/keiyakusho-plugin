#!/bin/bash
# ファイル編集後にプラグインの変更をcommit & pushする
PLUGIN_DIR="${CLAUDE_PLUGIN_ROOT:-$(dirname "$(dirname "$(dirname "$0")")")}"

cd "$PLUGIN_DIR" || exit 0

# gitリポジトリでなければスキップ
if [ ! -d .git ]; then
  exit 0
fi

# リモートがなければスキップ
if ! git remote get-url origin &>/dev/null; then
  exit 0
fi

# 変更がなければスキップ
if git diff --quiet && git diff --cached --quiet; then
  echo '{"decision":"approve","reason":"変更なし"}'
  exit 0
fi

# ステージ → コミット → プッシュ
git add -A
git commit -m "auto: プラグイン更新 $(date '+%Y-%m-%d %H:%M')" --no-verify
git push origin main --no-verify 2>&1

echo '{"decision":"approve","reason":"変更をGitHubにプッシュしました"}'
