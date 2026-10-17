#!/bin/sh
# 認片段用：每支片段抽 1.5 / 4 / 6.5 秒三張畫面，依參數順序左到右拼成一張圖，
# 用 Read 看圖即可判斷每支是哪一場（Flow 下載的英文檔名常常看不出場次）。
# 用法：sh contact_sheet.sh <輸出.png> <片段1> <片段2> ...
# 片段很多時分兩三張圖做，每張 4 支左右最清楚。
set -e
OUT=$1; shift
TMP=$(mktemp -d)
i=0; rows=""; n=0
for f in "$@"; do
  i=$((i+1))
  for t in 1.5 4 6.5; do
    ffmpeg -v error -y -ss $t -i "$f" -frames:v 1 -vf scale=150:-2 "$TMP/r${i}_$t.png"
  done
  ffmpeg -v error -y -i "$TMP/r${i}_1.5.png" -i "$TMP/r${i}_4.png" -i "$TMP/r${i}_6.5.png" -filter_complex hstack=3 "$TMP/row$i.png"
  rows="$rows -i $TMP/row$i.png"; n=$((n+1))
done
if [ $n -eq 1 ]; then cp "$TMP/row1.png" "$OUT"; else ffmpeg -v error -y $rows -filter_complex hstack=$n "$OUT"; fi
rm -rf "$TMP"
