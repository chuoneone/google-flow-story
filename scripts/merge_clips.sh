#!/bin/sh
# 合併 Flow 片段（含聲音），統一縮放成 WxH、24fps、48kHz。
# 用法：sh merge_clips.sh <寬> <高> <輸出.mp4> <片段1> <片段2> ...
#   直式短影音：sh merge_clips.sh 720 1280 完整版.mp4 01.mp4 02.mp4 03.mp4
#   橫式長影音：sh merge_clips.sh 1280 720 完整版.mp4 01.mp4 02.mp4 03.mp4
# 不同解析度（例如混到一支 1080p）會自動縮放＋補邊，不會變形。
set -e
W=$1; H=$2; OUT=$3; shift 3
n=0; inputs=""; fc=""; pairs=""
for f in "$@"; do
  inputs="$inputs -i \"$f\""
  fc="$fc[$n:v]scale=$W:$H:force_original_aspect_ratio=decrease,pad=$W:$H:(ow-iw)/2:(oh-ih)/2,fps=24,setsar=1[v$n];[$n:a]aresample=48000[a$n];"
  pairs="$pairs[v$n][a$n]"
  n=$((n+1))
done
eval ffmpeg -y -hide_banner -loglevel error $inputs \
  -filter_complex "\"${fc}${pairs}concat=n=$n:v=1:a=1[v][a]\"" \
  -map "\"[v]\"" -map "\"[a]\"" -c:v libx264 -crf 18 -preset medium -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart "\"$OUT\""
