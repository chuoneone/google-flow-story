"""從一個 JSON 同時產生「短影音燒錄字幕 .ass」與「YouTube CC 字幕 .srt」。

用法：python -I make_captions.py captions.json out.ass out.srt
燒錄：ffmpeg -i 完整版.mp4 -vf "subtitles=out.ass" -c:v libx264 -crf 18 -pix_fmt yuv420p -c:a copy 字幕版.mp4
     （在 out.ass 所在資料夾執行、用相對檔名，避免 Windows 路徑的冒號跳脫問題）

captions.json 範例：
{
  "width": 720, "height": 1280,
  "title": "老師和學生靈魂交換了？！", "title_keywords": ["靈魂交換"],
  "scenes": [
    {"dur": 8, "a": "陳老師和小安", "b": "在走廊撞在一起！", "keywords": ["撞在一起"]},
    {"dur": 8, "a": "上課鐘響了", "b": "老師卻在轉椅子？！", "keywords": ["轉椅子"]}
  ],
  "ending": "下一集待續", "ending_seconds": 2
}
- dur 用 ffprobe 量到的實際秒數（Flow 有時給 10 秒）。
- a / b 是旁白句號前後兩半；keywords 會變黃色。
- title / ending 可省略（橫式長影音通常不放標題，只出 .srt）。
"""
import json
import sys

YELLOW = r"{\c&H0000FFFF&}"
WHITE = r"{\c&H00FFFFFF&}"
POP = r"{\fscx70\fscy70\t(0,120,\fscx110\fscy110)\t(120,220,\fscx100\fscy100)}"
TITLE_POP = r"{\fscx60\fscy60\t(0,200,\fscx115\fscy115)\t(200,350,\fscx100\fscy100)}"
END_POP = r"{\fad(150,0)\fscx50\fscy50\t(0,250,\fscx115\fscy115)\t(250,400,\fscx100\fscy100)}"


def ass_time(s):
    return f"{int(s // 3600)}:{int(s % 3600 // 60):02d}:{s % 60:05.2f}"


def srt_time(s):
    ms = int(round(s * 1000))
    return f"{ms // 3600000:02d}:{ms % 3600000 // 60000:02d}:{ms % 60000 // 1000:02d},{ms % 1000:03d}"


def mark(text, keywords, on, off):
    for k in keywords:
        text = text.replace(k, f"{on}{k}{off}")
    return text


def main(cfg_path, ass_path, srt_path):
    cfg = json.load(open(cfg_path, encoding="utf-8"))
    w, h = cfg.get("width", 720), cfg.get("height", 1280)
    vertical = h > w
    total = sum(s["dur"] for s in cfg["scenes"])
    ending = cfg.get("ending")
    end_at = total - cfg.get("ending_seconds", 2) if ending else total

    if vertical:
        title_size, sub_size, end_size, title_mv, sub_mv = 62, 74, 96, 120, 330
    else:
        title_size, sub_size, end_size, title_mv, sub_mv = 50, 58, 90, 40, 70

    out = [
        "[Script Info]", "ScriptType: v4.00+", f"PlayResX: {w}", f"PlayResY: {h}",
        "WrapStyle: 2", "ScaledBorderAndShadow: yes", "",
        "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
        f"Style: Title,Microsoft JhengHei,{title_size},&H0000FFFF,&H000000FF,&H00000000,&H96000000,-1,0,0,0,100,100,2,0,1,7,3,8,30,30,{title_mv},1",
        f"Style: Sub,Microsoft JhengHei,{sub_size},&H00FFFFFF,&H000000FF,&H00000000,&HA0000000,-1,0,0,0,100,100,2,0,1,7,4,2,30,30,{sub_mv},1",
        f"Style: End,Microsoft JhengHei,{end_size},&H0000FFFF,&H000000FF,&H00000000,&H64000000,-1,0,0,0,100,100,4,0,1,8,5,5,30,30,0,1",
        "", "[Events]",
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
    ]
    if cfg.get("title"):
        title = mark(cfg["title"], cfg.get("title_keywords", []), WHITE, YELLOW)
        out.append(f"Dialogue: 2,{ass_time(0)},{ass_time(total)},Title,,0,0,0,,{TITLE_POP}{title}")

    srt, start = [], 0.0
    for i, sc in enumerate(cfg["scenes"], 1):
        d, kw = sc["dur"], sc.get("keywords", [])
        half = start + min(3.6, d / 2)
        a_end = min(half, end_at)
        b_end = min(start + d - 0.1, end_at)
        if start + 0.2 < a_end:
            out.append(f"Dialogue: 1,{ass_time(start + 0.2)},{ass_time(a_end)},Sub,,0,0,0,,{POP}{mark(sc['a'], kw, YELLOW, WHITE)}")
        if half < b_end:
            out.append(f"Dialogue: 1,{ass_time(half)},{ass_time(b_end)},Sub,,0,0,0,,{POP}{mark(sc['b'], kw, YELLOW, WHITE)}")
        plain = f"{sc['a'].rstrip('！？!?。')}，{sc['b'].rstrip('！？!?。…')}"
        srt.append(f"{i}\n{srt_time(start + 0.5)} --> {srt_time(start + d - 0.5)}\n{plain}\n")
        start += d
    if ending:
        out.append(f"Dialogue: 3,{ass_time(end_at)},{ass_time(total)},End,,0,0,0,,{END_POP}{ending}")

    with open(ass_path, "w", encoding="utf-8-sig", newline="\n") as f:
        f.write("\n".join(out) + "\n")
    with open(srt_path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(srt))


if __name__ == "__main__":
    main(*sys.argv[1:4])
