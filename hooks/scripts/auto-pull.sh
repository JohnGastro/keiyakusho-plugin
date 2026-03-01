#!/bin/bash
# セッション開始時にプラグインの最新版をpullする
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

# pull実行
result=$(git pull origin main 2>&1)

if echo "$result" | grep -q "Already up to date"; then
  echo '{"decision":"approve","reason":"プラグインは最新です"}'
elif echo "$result" | grep -q "Updating"; then
  echo '{"decision":"approve","reason":"プラグインを最新版に更新しました"}'
else
  echo '{"decision":"approve","reason":"git pull完了"}'
fi
