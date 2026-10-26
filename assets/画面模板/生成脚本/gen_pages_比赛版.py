# -*- coding: utf-8 -*-
"""生成比赛版画面模板(9:16 竖版 1080x1920) —— 全场集锦过场体系
输出到 共享资产\画面模板\比赛版\{01_片头,02_节数据过场,03_全场数据,04_趋势图,05_片尾}
用法: 新比赛日拷贝模板目录 → 改日期/占位数据 → 重新运行本脚本(或改html) → 出图
数据均为占位(--)，比赛后按剪辑表数据填入"""
import os, subprocess, time

BASE = r'D:\视频剪辑\00_流程与规范\共享资产\画面模板\比赛版'
os.makedirs(BASE, exist_ok=True)
EDGE = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'

# ---------- 比赛信息占位 ----------
G = dict(
    org='常青藤篮球训练中心',
    season='2026 赛季',
    date='2026.__.__ 队内训练赛',
    teamA='常青藤 A 队',
    teamB='常青藤 B 队',
)

CSS = """
* { margin:0; padding:0; box-sizing:border-box; }
body { width:1080px; height:1920px; font-family:"Microsoft YaHei",sans-serif;
  background:linear-gradient(160deg,#101b33 0%,#16294d 55%,#1b3564 100%); color:#fff; overflow:hidden; }
.wrap { width:1080px; height:1920px; padding:64px 60px; position:relative; }
.deco { position:absolute; border:6px solid rgba(255,170,60,.45); border-radius:50%; }
.d1 { width:340px; height:340px; top:-130px; right:-115px; }
.d2 { width:210px; height:210px; bottom:-75px; left:-65px; border-color:rgba(255,255,255,.08); }
.topbar { text-align:center; }
.topbar .org { font-size:26px; color:#9fb4d8; letter-spacing:2px; }
.topbar .date { font-size:22px; color:#6f85ab; margin-top:6px; }
.page-flag { position:absolute; top:64px; right:60px; font-size:20px; color:#ff8a3d; font-weight:700; letter-spacing:2px; }
.section-t { font-size:44px; font-weight:800; color:#fff; text-align:center; margin-top:18px; letter-spacing:1px; }
.section-s { font-size:24px; color:#9fb4d8; text-align:center; margin-top:8px; }
.card { background:rgba(255,255,255,.06); border:1.5px solid rgba(255,255,255,.12); border-radius:14px; }
"""

def head(flag):
    return f"""<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8"><title>比赛集锦画面模板</title><style>{CSS}</style></head>
<body><div class="wrap"><div class="deco d1"></div><div class="deco d2"></div>
<div class="page-flag">{flag}</div>
<div class="topbar"><div class="org">{G['org']}</div><div class="date">{G['date']} · {G['season']}</div></div>"""

def tail():
    return "</div></body></html>"

def stat_card(t, v, color='#ffb84d', fsize=40):
    return f'<div class="card" style="flex:1 1 130px;padding:16px 8px;text-align:center;"><div style="font-size:{fsize}px;font-weight:800;color:{color};">{v}</div><div style="font-size:22px;color:#9fb4d8;margin-top:4px;">{t}</div></div>'

# ============ 1. 片头页 ============
cover = head('COVER · 片头')
cover += f"""
<div style="text-align:center;margin-top:150px;">
  <img src="../../../logo/LOGO.png" style="width:220px;height:220px;object-fit:contain;" alt="LOGO">
</div>
<div class="section-t" style="margin-top:36px;">队内训练赛</div>
<div style="text-align:center;margin-top:10px;font-size:26px;color:#9fb4d8;letter-spacing:3px;">全场集锦 · 过场体系</div>
<!-- A vs B -->
<div style="display:flex;justify-content:center;align-items:center;gap:30px;margin-top:70px;">
  <div style="text-align:center;"><div style="font-size:34px;font-weight:800;color:#b8a8ff;">{G['teamA']}</div></div>
  <div style="font-size:56px;font-weight:800;background:linear-gradient(90deg,#ffb84d,#ff8a3d);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">VS</div>
  <div style="text-align:center;"><div style="font-size:34px;font-weight:800;color:#ffb84d;">{G['teamB']}</div></div>
</div>
<!-- 最终比分占位 -->
<div style="text-align:center;margin-top:40px;background:rgba(255,255,255,.06);border:2px solid rgba(255,255,255,.14);border-radius:18px;padding:26px 24px;margin-left:60px;margin-right:60px;">
  <div style="font-size:24px;color:#9fb4d8;letter-spacing:2px;">最终比分</div>
  <div style="display:flex;justify-content:center;align-items:center;gap:26px;margin-top:12px;font-size:64px;font-weight:800;">
    <span style="color:#b8a8ff;">--</span><span style="color:#6f85ab;font-size:36px;">:</span><span style="color:#ffb84d;">--</span>
  </div>
  <div style="font-size:20px;color:#6f85ab;margin-top:8px;">（赛后填入）</div>
</div>
<div style="text-align:center;margin-top:60px;font-size:22px;color:#6f85ab;letter-spacing:2px;">第 1 ~ 8 节 · 每节过场 · 趋势汇总</div>
"""
cover += tail()

# ============ 2. 节数据过场页（第1~8节） ============
def quarter(n):
    q = head(f'QUARTER {n} · 节数据')
    q += f"""
<div class="section-t">第 {n} 节</div>
<div class="section-s">本节集锦 · 过场定格</div>
<!-- 比分核对条 -->
<div style="margin-top:30px;background:rgba(255,255,255,.06);border:2px solid rgba(255,255,255,.14);border-radius:18px;padding:26px 24px;">
  <div style="font-size:24px;color:#9fb4d8;text-align:center;letter-spacing:2px;">本节比分核对（家长核对用）</div>
  <div style="display:flex;justify-content:center;align-items:center;gap:22px;margin-top:16px;font-size:44px;font-weight:800;">
    <div style="text-align:center;"><div style="font-size:22px;color:#9fb4d8;">开始</div><div style="color:#b8a8ff;">0</div><div style="color:#ffb84d;font-size:24px;">0</div></div>
    <div style="color:#ff8a3d;">→</div>
    <div style="text-align:center;"><div style="font-size:22px;color:#9fb4d8;">结束</div><div style="color:#b8a8ff;">--</div><div style="color:#ffb84d;font-size:24px;">--</div></div>
  </div>
  <div style="text-align:center;font-size:20px;color:#6f85ab;margin-top:10px;">（比分由教练/剪辑表提供后填入）</div>
</div>
<!-- 本节球队数据 -->
<div style="margin-top:24px;font-size:26px;color:#9fb4d8;text-align:center;letter-spacing:2px;">本节球队数据</div>
<div style="display:flex;flex-wrap:wrap;gap:14px;margin-top:14px;">
  {stat_card('A队得分', '--', '#b8a8ff')}{stat_card('B队得分', '--', '#ffb84d')}{stat_card('本节总投篮', '--')}{stat_card('本节三分', '--')}{stat_card('本节篮板', '--')}{stat_card('本节抢断', '--')}
</div>
<!-- 本节高光 -->
<div style="margin-top:24px;background:rgba(255,138,61,.10);border:2px solid rgba(255,138,61,.40);border-radius:16px;padding:20px 26px;">
  <div style="font-size:26px;color:#ffd9b8;line-height:1.6;"><b style="color:#ffb84d;">本节高光：</b>待节次统计生成后自动填写（命中三分 / 关键抢断 / 精彩助攻）</div>
</div>
"""
    q += tail()
    return q

# ============ 3. 全场数据页 ============
spage = head('SUMMARY · 全场数据')
spage += f"""
<div class="section-t">全场数据汇总</div>
<div class="section-s">最终比分 · 两队数据对比</div>
<!-- 最终比分 -->
<div style="margin-top:28px;background:rgba(255,255,255,.06);border:2px solid rgba(255,255,255,.14);border-radius:18px;padding:22px 24px;">
  <div style="font-size:24px;color:#9fb4d8;text-align:center;letter-spacing:2px;">最终比分</div>
  <div style="display:flex;justify-content:center;align-items:center;gap:30px;margin-top:10px;">
    <div style="text-align:center;"><div style="font-size:26px;color:#b8a8ff;">{G['teamA']}</div><div style="font-size:72px;font-weight:800;color:#b8a8ff;">--</div></div>
    <div style="font-size:40px;color:#6f85ab;">:</div>
    <div style="text-align:center;"><div style="font-size:26px;color:#ffb84d;">{G['teamB']}</div><div style="font-size:72px;font-weight:800;color:#ffb84d;">--</div></div>
  </div>
</div>
<!-- 两队数据对比表 -->
<div style="margin-top:24px;font-size:26px;color:#9fb4d8;text-align:center;letter-spacing:2px;">两队全场数据</div>
<div style="margin-top:14px;background:rgba(255,255,255,.05);border-radius:16px;padding:18px 20px;">
  <table style="width:100%;border-collapse:collapse;text-align:center;">
    <tr style="font-size:22px;color:#9fb4d8;"><td style="padding:10px 0;width:18%;"></td><td style="width:20%;color:#b8a8ff;">A队</td><td style="width:20%;color:#ffb84d;">B队</td><td style="width:42%;"></td></tr>
    {''.join(f'<tr style="font-size:26px;color:#fff;"><td style="padding:9px 0;color:#9fb4d8;font-size:22px;">{t}</td><td style="font-weight:700;color:#b8a8ff;">--</td><td style="font-weight:700;color:#ffb84d;">--</td><td></td></tr>' for t in ['得分','投篮','三分','罚篮','篮板','助攻','抢断','盖帽'])}
  </table>
</div>
<!-- 教练点评占位 -->
<div style="margin-top:24px;background:rgba(255,138,61,.12);border:2px solid rgba(255,138,61,.45);border-radius:16px;padding:20px 24px;">
  <div style="font-size:25px;color:#ffd9b8;line-height:1.6;"><b style="color:#ffb84d;">教练点评：</b>待比赛数据统计完成后填写（球队整体表现 / 关键转折点 / 下一场改进方向）</div>
</div>
"""
spage += tail()

# ============ 4. 趋势图页（每节得分曲线） ============
def trend_svg(width=900, height=560, dataA=None, dataB=None, labels=None):
    dataA = dataA or [16, 23, 32, 22, 18, 25, 20, 27]
    dataB = dataB or [28, 15, 30, 24, 21, 26, 23, 29]
    labels = labels or [f'第{i}节' for i in range(1, 9)]
    n = len(labels)
    maxv = max(max(dataA), max(dataB), 1)
    top, bottom = 60, height - 70
    plot_h = bottom - top
    slot = width / n
    bar_w = min(slot * 0.28, 46)
    parts = [f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg" style="overflow:visible;display:block;">']
    for g in (0, 0.25, 0.5, 0.75, 1.0):
        gy = bottom - plot_h * g
        parts.append(f'<line x1="20" y1="{gy:.1f}" x2="{width-20}" y2="{gy:.1f}" stroke="rgba(255,255,255,.08)" stroke-width="1"/>')
        parts.append(f'<text x="14" y="{gy+7:.1f}" fill="#6f85ab" font-size="18">{int(maxv*g)}</text>')
    for i in range(n):
        cx = 20 + (i + 0.5) * slot
        # A队柱
        hA = plot_h * dataA[i] / maxv
        parts.append(f'<rect x="{cx-bar_w-2:.1f}" y="{bottom-hA:.1f}" width="{bar_w:.1f}" height="{hA:.1f}" rx="8" fill="rgba(184,168,255,.85)"/>')
        parts.append(f'<text x="{cx-bar_w-2+bar_w/2:.1f}" y="{bottom-hA-8:.1f}" fill="#b8a8ff" font-size="17" font-weight="700" text-anchor="middle">{dataA[i]}</text>')
        # B队柱
        hB = plot_h * dataB[i] / maxv
        parts.append(f'<rect x="{cx+2:.1f}" y="{bottom-hB:.1f}" width="{bar_w:.1f}" height="{hB:.1f}" rx="8" fill="rgba(255,184,77,.85)"/>')
        parts.append(f'<text x="{cx+2+bar_w/2:.1f}" y="{bottom-hB-8:.1f}" fill="#ffb84d" font-size="17" font-weight="700" text-anchor="middle">{dataB[i]}</text>')
        parts.append(f'<text x="{cx:.1f}" y="{bottom+34:.1f}" fill="#e8eefb" font-size="19" font-weight="700" text-anchor="middle">{labels[i]}</text>')
    parts.append('</svg>')
    return ''.join(parts)

tpage = head('TREND · 趋势图')
tpage += f"""
<div class="section-t">每节得分趋势</div>
<div class="section-s">第 1 ~ 8 节 · 两队对比（示意数据，赛后按剪辑表替换）</div>
<!-- 图例 -->
<div style="display:flex;justify-content:center;gap:40px;margin-top:20px;font-size:22px;">
  <span style="color:#b8a8ff;">■ {G['teamA']}</span>
  <span style="color:#ffb84d;">■ {G['teamB']}</span>
</div>
<div style="display:flex;justify-content:center;margin-top:16px;">{trend_svg(940, 660)}</div>
<div style="text-align:center;font-size:20px;color:#6f85ab;margin-top:30px;">数据来源：全场剪辑表 · 分节统计</div>
"""
tpage += tail()

# ============ 5. 片尾页 ============
epage = head('END · 片尾')
epage += f"""
<div style="margin-top:170px;text-align:center;">
  <div style="font-size:56px;font-weight:800;color:#fff;letter-spacing:2px;">本场集锦 · 完</div>
  <div style="margin-top:14px;font-size:24px;color:#9fb4d8;letter-spacing:2px;">第 1 ~ 8 节 · 全场集锦</div>
</div>
<!-- 最终比分核对 -->
<div style="margin-top:60px;background:rgba(255,255,255,.06);border:2px solid rgba(255,255,255,.14);border-radius:18px;padding:28px 24px;margin-left:60px;margin-right:60px;">
  <div style="font-size:24px;color:#9fb4d8;text-align:center;letter-spacing:2px;">最终比分核对</div>
  <div style="display:flex;justify-content:center;align-items:center;gap:26px;margin-top:16px;font-size:56px;font-weight:800;">
    <span style="color:#b8a8ff;">--</span><span style="color:#6f85ab;font-size:32px;">:</span><span style="color:#ffb84d;">--</span>
  </div>
  <div style="text-align:center;font-size:20px;color:#6f85ab;margin-top:10px;">（比分由教练提供后填入）</div>
</div>
<div style="text-align:center;margin-top:80px;font-size:26px;color:#9fb4d8;letter-spacing:3px;">感谢观看</div>
<div style="text-align:center;margin-top:10px;font-size:24px;color:#6f85ab;">{G['org']} · {G['date']}</div>
"""
epage += tail()

# ---------- 输出 ----------
out_files = {
    '01_片头/片头页': cover,
    '03_全场数据/全场数据页': spage,
    '04_趋势图/每节得分趋势': tpage,
    '05_片尾/片尾页': epage,
}
for n in range(1, 9):
    out_files[f'02_节数据过场/第{n}节'] = quarter(n)

for rel, html in out_files.items():
    hp = os.path.join(BASE, rel + '.html')
    os.makedirs(os.path.dirname(hp), exist_ok=True)
    with open(hp, 'w', encoding='utf-8') as f:
        f.write(html)
    png = hp.replace('.html', '.png')
    subprocess.run([EDGE, '--headless', '--disable-gpu', '--hide-scrollbars',
                    '--user-data-dir=' + os.path.join(os.path.dirname(hp), '_edge_prof'),
                    '--window-size=1080,1920', f'--screenshot={png}',
                    'file:///' + hp.replace('\\', '/')],
                   capture_output=True)
    time.sleep(1.2)
    print(rel, os.path.exists(png), os.path.getsize(png) if os.path.exists(png) else 0)
