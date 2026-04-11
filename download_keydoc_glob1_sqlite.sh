#!/usr/bin/env bash

set -e

REPO="sanskrit-lexicon/csl-sqlite"
API="https://api.github.com/repos/$REPO/releases/latest"

FILES=(
  "keydoc_glob1.sqlite.zip"
)

TAG_FILE=".csl_sqlite_release_tag"

echo "🔍 Checking latest release..."

RELEASE_JSON=$(curl -s $API)
LATEST_TAG=$(echo "$RELEASE_JSON" | grep '"tag_name"' | cut -d '"' -f 4)

if [ -f "$TAG_FILE" ]; then
  LOCAL_TAG=$(cat "$TAG_FILE")
else
  LOCAL_TAG=""
fi

if [ "$LATEST_TAG" = "$LOCAL_TAG" ]; then
  echo "✅ Already up-to-date ($LATEST_TAG)"
  exit 0
fi

echo "⬇️ New version detected: $LATEST_TAG (old: $LOCAL_TAG)"

for FILE in "${FILES[@]}"; do
  URL="https://github.com/$REPO/releases/download/$LATEST_TAG/$FILE"

  echo "📥 Downloading $FILE ..."
  curl -L -o "$FILE" "$URL"
done

# Extract and organize files
echo "📦 Extracting keydoc_glob1.sqlite..."
unzip -o keydoc_glob1.sqlite.zip
mkdir -p keydoc
echo "Put sqlite in keydoc/keydoc_glob1.sqlite..."
mv keydoc_glob1.sqlite keydoc/keydoc_glob1.sqlite
rm -f keydoc_glob1.sqlite.zip

# Save new tag
echo "$LATEST_TAG" > "$TAG_FILE"

echo "🎉 Update complete!"

