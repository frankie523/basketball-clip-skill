# -*- coding: utf-8 -*-
"""生成 4 类个人版页面模板(9:16 竖版 1080x1920), 示例球员=施柏宇(10.17真实累计)
输出到 共享资产\画面模板\个人版\{01_封面,02_节数据,03_汇总,04_封底}
用法: 改 P 字典数据 → 运行 → 各子目录刷新 html/png"""
import math, os, subprocess, time

BASE = r'D:\视频剪辑\00_流程与规范\共享资产\画面模板\个人版'
OUT_MAP = {'1_封面页': '01_封面', '2_每节数据页': '02_节数据', '3_汇总数据页': '03_汇总', '4_封底页': '04_封底'}
os.makedirs(BASE, exist_ok=True)

# ---- 施柏宇 10.17 真实累计(来源 summary_1017.json) ----
P = dict(
    name='施柏宇', team='A队', date='2026.10.17 队内训练赛',
    season='2026 赛季',
    position='内线', level='U14', trainingYears='2',
    height='___', weight='___', age='___',  # 待小程序档案数据
    under=8, mid=5, three=6, ft=1,
    under_hit=6, mid_hit=3, three_hit=2, ft_hit=0,
    pts=24, oreb=2, dreb=9, ast=1, stl=0, blk=2,
)
P['treb'] = P['oreb'] + P['dreb']
P['fga'] = P['under'] + P['mid'] + P['three'] + P['ft']
P['fgm'] = P['under_hit'] + P['mid_hit'] + P['three_hit'] + P['ft_hit']
P['fgp'] = round(100 * P['fgm'] / P['fga'], 1)
P['three_p'] = round(100 * P['three_hit'] / P['three'], 1) if P['three'] else 0

# 雷达图 6 维(归一化基准=全队该维度最高值)
RADAR = [
    ('得分', P['pts'], 24),
    ('篮板', P['treb'], 18),
    ('助攻', P['ast'], 6),
    ('抢断', P['stl'], 3),
    ('盖帽', P['blk'], 6),
    ('命中率', P['fgp'], 55.0),
]

def trend_svg(width=900, height=320, cx=450, data=None, labels=None):
    """每节得分趋势柱状图(示意), data/labels 默认 3 节"""
    data = data or [8, 10, 6]
    labels = labels or ['第1节', '第2节', '第3节']
    n = len(data)
    maxv = max(data) if data else 10
    top, bottom = 40, height - 46
    plot_h = bottom - top
    slot = width / n
    bar_w = min(slot * 0.5, 120)
    parts = [f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg" style="overflow:visible;display:block;">']
    # 网格线
    for g in (0, 0.5, 1.0):
        gy = bottom - plot_h * g
        parts.append(f'<line x1="20" y1="{gy:.1f}" x2="{width-20}" y2="{gy:.1f}" stroke="rgba(255,255,255,.08)" stroke-width="1"/>')
        if g > 0:
            parts.append(f'<text x="12" y="{gy+7:.1f}" fill="#6f85ab" font-size="18" text-anchor="start">{int(maxv*g)}</text>')
    # 柱
    for i, (v, lab) in enumerate(zip(data, labels)):
        x0 = cx + (i - (n - 1) / 2) * slot - bar_w / 2
        h = plot_h * v / maxv
        y0 = bottom - h
        grad = f'<defs><linearGradient id="g{i}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffb84d"/><stop offset="1" stop-color="#ff8a3d"/></linearGradient></defs>' if i == 0 else ''
        if i == 0:
            parts.insert(1, grad)
        parts.append(f'<rect x="{x0:.1f}" y="{y0:.1f}" width="{bar_w:.1f}" height="{h:.1f}" rx="10" fill="url(#g{i})"/>')
        parts.append(f'<text x="{x0+bar_w/2:.1f}" y="{y0-10:.1f}" fill="#ffb84d" font-size="24" font-weight="700" text-anchor="middle">{v}分</text>')
        parts.append(f'<text x="{x0+bar_w/2:.1f}" y="{bottom+30:.1f}" fill="#e8eefb" font-size="20" font-weight="700" text-anchor="middle">{lab}</text>')
    parts.append('</svg>')
    return ''.join(parts)

def radar_svg(cx, cy, R, size, fill='rgba(255,138,61,.55)', stroke='#ff8a3d'):
    """六边形网格 + 数据多边形, 返回 svg 字符串"""
    n = len(RADAR)
    def pt(i, r, off=0.0):
        ang = -math.pi / 2 + 2 * math.pi * i / n + off
        return (cx + r * math.cos(ang), cy + r * math.sin(ang))
    parts = [f'<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}" xmlns="http://www.w3.org/2000/svg" style="overflow:visible">']
    # 网格(0.25/0.5/0.75/1.0)
    for f in (0.25, 0.5, 0.75, 1.0):
        pts = ' '.join(f'{pt(i, R*f)[0]:.1f},{pt(i, R*f)[1]:.1f}' for i in range(n))
        parts.append(f'<polygon points="{pts}" fill="none" stroke="rgba(255,255,255,.12)" stroke-width="1"/>')
    # 轴线
    for i in range(n):
        x, y = pt(i, R)
        parts.append(f'<line x1="{cx}" y1="{cy}" x2="{x:.1f}" y2="{y:.1f}" stroke="rgba(255,255,255,.10)" stroke-width="1"/>')
    # 数据多边形
    dp = []
    for i, (lab, v, base) in enumerate(RADAR):
        dp.append(pt(i, R * min(v / base, 1.0)))
    dpts = ' '.join(f'{x:.1f},{y:.1f}' for x, y in dp)
    parts.append(f'<polygon points="{dpts}" fill="{fill}" stroke="{stroke}" stroke-width="2.5" stroke-linejoin="round"/>')
    # 顶点圆点+标签
    for i, (lab, v, base) in enumerate(RADAR):
        x, y = pt(i, R * min(v / base, 1.0))
        parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4.5" fill="#ff8a3d"/>')
        lx, ly = pt(i, R + 30)
        anchor = 'middle'
        if abs(math.cos(2 * math.pi * i / n)) > 0.6:
            anchor = 'start' if math.cos(2 * math.pi * i / n) > 0 else 'end'
        parts.append(f'<text x="{lx:.1f}" y="{ly:.1f}" fill="#e8eefb" font-size="20" font-weight="700" text-anchor="{anchor}" dominant-baseline="middle">{lab}</text>')
        vx, vy = pt(i, R - 24)
        parts.append(f'<text x="{vx:.1f}" y="{vy:.1f}" fill="#ffb84d" font-size="19" font-weight="700" text-anchor="middle" dominant-baseline="middle">{v}</text>')
    parts.append('</svg>')
    return ''.join(parts)

CSS = """
* { margin:0; padding:0; box-sizing:border-box; }
body { width:1080px; height:1920px; font-family:"Microsoft YaHei",sans-serif;
  background:linear-gradient(160deg,#101b33 0%,#16294d 55%,#1b3564 100%); color:#fff; overflow:hidden; }
.wrap { width:1080px; height:1920px; padding:64px 60px; position:relative; }
.deco { position:absolute; border:6px solid rgba(255,170,60,.45); border-radius:50%; }
.d1 { width:320px; height:320px; top:-120px; right:-110px; }
.d2 { width:200px; height:200px; bottom:-70px; left:-60px; border-color:rgba(255,255,255,.08); }
.topbar { text-align:center; }
.topbar .org { font-size:26px; color:#9fb4d8; letter-spacing:2px; }
.topbar .date { font-size:22px; color:#6f85ab; margin-top:6px; }
.page-flag { position:absolute; top:64px; right:60px; font-size:20px; color:#ff8a3d; font-weight:700; letter-spacing:2px; }
.section-t { font-size:44px; font-weight:800; color:#fff; text-align:center; margin-top:18px; letter-spacing:1px; }
.section-s { font-size:24px; color:#9fb4d8; text-align:center; margin-top:8px; }
"""

def head(flag):
    return f"""<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8"><title>{P['name']}集锦页面模板</title><style>{CSS}</style></head>
<body><div class="wrap"><div class="deco d1"></div><div class="deco d2"></div>
<div class="page-flag">{flag}</div>
<div class="topbar"><div class="org">常青藤篮球训练中心</div><div class="date">{P['date']}</div></div>"""

def tail():
    return "</div></body></html>"

# ============ 1. 封面页 ============
cover = head('COVER · 封面')
cover += f"""
<div class="section-t">{P['name']}</div>
<div style="text-align:center;margin-top:12px;">
  <span style="display:inline-block;font-size:22px;color:#101b33;background:#ff8a3d;padding:6px 22px;border-radius:20px;font-weight:700;">{P['team']} · 内线 · 得分核心</span>
</div>
<div style="text-align:center;margin-top:26px;">
  <div style="font-size:24px;color:#9fb4d8;letter-spacing:4px;">本场得分</div>
  <div style="font-size:150px;font-weight:800;background:linear-gradient(90deg,#ffb84d,#ff8a3d);-webkit-background-clip:text;-webkit-text-fill-color:transparent;line-height:1;">{P['pts']}</div>
  <div style="font-size:26px;color:#6f85ab;">POINTS</div>
</div>
<!-- 登记照占位 + 档案 -->
<div style="display:flex;align-items:center;gap:26px;margin-top:34px;background:rgba(255,255,255,.06);border:2px solid rgba(255,255,255,.12);border-radius:20px;padding:24px 26px;">
  <div style="width:220px;height:270px;flex:none;border:3px dashed rgba(255,170,60,.7);border-radius:14px;display:flex;flex-direction:column;align-items:center;justify-content:center;background:rgba(255,170,60,.06);">
    <div style="font-size:52px;">📷</div>
    <div style="font-size:22px;color:#ffb84d;margin-top:8px;">贴登记照处</div>
  </div>
  <div style="font-size:30px;line-height:1.9;color:#e8eefb;">
    <div>身高 <span style="color:#ffb84d;font-weight:700;">___ cm</span></div>
    <div>体重 <span style="color:#ffb84d;font-weight:700;">___ kg</span></div>
    <div>年龄 <span style="color:#ffb84d;font-weight:700;">___ 岁</span></div>
  </div>
</div>
<!-- 雷达图 -->
<div style="margin-top:30px;text-align:center;">
  <div style="font-size:26px;color:#9fb4d8;letter-spacing:2px;margin-bottom:10px;">能力雷达图 · 本场累计</div>
  <div style="display:flex;justify-content:center;">{radar_svg(200,200,150,400)}</div>
</div>
<!-- AI 一句话 -->
<div style="margin-top:26px;background:rgba(255,138,61,.12);border:2px solid rgba(255,138,61,.45);border-radius:16px;padding:20px 26px;text-align:center;">
  <div style="font-size:26px;color:#ffd9b8;line-height:1.5;"><b style="color:#ffb84d;">教练点评：</b>得分终结核心 · 命中率全队第一，攻防两端都是内线支柱</div>
</div>
"""
cover += tail()

# ============ 2. 每节数据页 ============
qpage = head('QUARTER · 节数据')
qpage += f"""
<div class="section-t">第 1 节</div>
<div class="section-s">接力赛 · 本节集锦</div>
<!-- 比分核对条 -->
<div style="margin-top:30px;background:rgba(255,255,255,.06);border:2px solid rgba(255,255,255,.14);border-radius:18px;padding:26px 24px;">
  <div style="font-size:24px;color:#9fb4d8;text-align:center;letter-spacing:2px;">本节比分核对（家长核对用）</div>
  <div style="display:flex;justify-content:center;align-items:center;gap:22px;margin-top:14px;font-size:44px;font-weight:800;">
    <div style="text-align:center;"><div style="font-size:22px;color:#9fb4d8;">开始</div><div style="color:#fff;">{P['team']} 0</div></div>
    <div style="color:#ff8a3d;">→</div>
    <div style="text-align:center;"><div style="font-size:22px;color:#9fb4d8;">结束</div><div style="color:#ffb84d;">? : ?</div></div>
  </div>
  <div style="text-align:center;font-size:20px;color:#6f85ab;margin-top:10px;">（比分由教练提供后填入）</div>
</div>
<!-- 本节个人数据 -->
<div style="margin-top:22px;font-size:26px;color:#9fb4d8;text-align:center;letter-spacing:2px;">本节个人数据</div>
<div style="display:flex;flex-wrap:wrap;gap:14px;margin-top:12px;">
  {''.join(f'<div style="flex:1 1 150px;background:rgba(255,255,255,.06);border:1.5px solid rgba(255,255,255,.12);border-radius:14px;padding:16px 10px;text-align:center;"><div style="font-size:40px;font-weight:800;color:#ffb84d;">--</div><div style="font-size:22px;color:#9fb4d8;margin-top:4px;">{t}</div></div>' for t in ['得分','篮板','助攻','抢断'])}
</div>
<div style="margin-top:22px;background:rgba(255,255,255,.05);border-radius:14px;padding:16px 20px;text-align:center;font-size:22px;color:#9fb4d8;">本节高光事件：待节次统计生成后自动填写（命中三分/关键抢断）</div>
"""
qpage += tail()

# ============ 3. 汇总数据页 ============
spage = head('SUMMARY · 汇总')
spage += f"""
<div class="section-t">全场数据汇总</div>
<div class="section-s">累计统计 · 雷达图 · 特点解读</div>
<!-- 核心数据 -->
<div style="display:flex;flex-wrap:wrap;gap:14px;margin-top:26px;">
  {''.join(f'<div style="flex:1 1 130px;background:rgba(255,255,255,.06);border:1.5px solid rgba(255,255,255,.12);border-radius:14px;padding:16px 8px;text-align:center;"><div style="font-size:42px;font-weight:800;color:#ffb84d;">{v}</div><div style="font-size:22px;color:#9fb4d8;margin-top:4px;">{t}</div></div>' for t, v in [('得分',P['pts']),('篮板',P['treb']),('助攻',P['ast']),('抢断',P['stl']),('盖帽',P['blk']),('命中率',f"{P['fgp']}%")])}
</div>
<!-- 投篮明细 -->
<div style="display:flex;flex-wrap:wrap;gap:10px;margin-top:16px;">
  {''.join(f'<div style="flex:1 1 150px;background:rgba(255,255,255,.05);border-radius:12px;padding:12px 10px;text-align:center;"><div style="font-size:22px;color:#9fb4d8;">{t}</div><div style="font-size:30px;color:#fff;font-weight:700;margin-top:4px;">{v}</div></div>' for t, v in [('投篮',f"{P['fgm']}/{P['fga']}"),('篮下',f"{P['under_hit']}/{P['under']}"),('中投',f"{P['mid_hit']}/{P['mid']}"),('三分',f"{P['three_hit']}/{P['three']}"),('罚篮',f"{P['ft_hit']}/{P['ft']}")])}
</div>
<!-- 每节得分趋势 -->
<div style="margin-top:20px;background:rgba(255,255,255,.05);border-radius:16px;padding:18px 20px;">
  <div style="display:flex;justify-content:space-between;align-items:baseline;">
    <div style="font-size:26px;color:#9fb4d8;letter-spacing:2px;">每节得分趋势</div>
    <div style="font-size:18px;color:#6f85ab;">示意划分 · 待节次确认后校正</div>
  </div>
  <div style="display:flex;justify-content:center;margin-top:10px;">{trend_svg(900, 300, 450)}</div>
</div>
<!-- 雷达图大图 -->
<div style="margin-top:20px;text-align:center;">
  <div style="font-size:26px;color:#9fb4d8;letter-spacing:2px;margin-bottom:8px;">6 维能力雷达图 · 全队横向对比</div>
  <div style="display:flex;justify-content:center;">{radar_svg(250,250,185,500, fill='rgba(255,138,61,.45)')}</div>
</div>
<!-- AI 特点 -->
<div style="margin-top:20px;background:rgba(255,138,61,.12);border:2px solid rgba(255,138,61,.45);border-radius:16px;padding:20px 24px;">
  <div style="font-size:25px;color:#ffd9b8;line-height:1.6;">
    <b style="color:#ffb84d;">教练点评：</b>得分终结核心——全场 24 分领跑全队，命中率 55% 全队第一；11 个篮板镇守禁区，2 记盖帽护框，中投与篮下双终结手段兼备，是攻防两端都靠得住的内线支柱。
  </div>
</div>
"""
spage += tail()

# ============ 4. 封底页 ============
epage = head('END · 封底')
epage += f"""
<div style="margin-top:180px;text-align:center;">
  <div style="font-size:56px;font-weight:800;color:#fff;letter-spacing:2px;">本场集锦 · 完</div>
  <div style="margin-top:14px;font-size:24px;color:#9fb4d8;letter-spacing:2px;">第 1 节 · {P['name']}</div>
</div>
<!-- 比分核对 -->
<div style="margin-top:60px;background:rgba(255,255,255,.06);border:2px solid rgba(255,255,255,.14);border-radius:18px;padding:28px 24px;">
  <div style="font-size:24px;color:#9fb4d8;text-align:center;letter-spacing:2px;">本节比分核对</div>
  <div style="display:flex;justify-content:center;align-items:center;gap:22px;margin-top:16px;font-size:44px;font-weight:800;">
    <div style="text-align:center;"><div style="font-size:22px;color:#9fb4d8;">开始</div><div style="color:#fff;">0 : 0</div></div>
    <div style="color:#ff8a3d;">→</div>
    <div style="text-align:center;"><div style="font-size:22px;color:#9fb4d8;">结束</div><div style="color:#ffb84d;">? : ?</div></div>
  </div>
  <div style="text-align:center;font-size:20px;color:#6f85ab;margin-top:10px;">（比分由教练提供后填入）</div>
</div>
<div style="text-align:center;margin-top:70px;font-size:26px;color:#9fb4d8;letter-spacing:3px;">感谢观看</div>
<div style="text-align:center;margin-top:10px;font-size:24px;color:#6f85ab;">常青藤篮球训练中心 · 2026.10.17</div>
"""
epage += tail()

pages = {'1_封面页': cover, '2_每节数据页': qpage, '3_汇总数据页': spage, '4_封底页': epage}

edge = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
for name, html in pages.items():
    out_dir = os.path.join(BASE, OUT_MAP[name])
    os.makedirs(out_dir, exist_ok=True)
    hp = os.path.join(out_dir, name.replace('1_封面页', '封面页').replace('2_每节数据页', '节数据页').replace('3_汇总数据页', '汇总数据页').replace('4_封底页', '封底页') + '.html')
    with open(hp, 'w', encoding='utf-8') as f:
        f.write(html)
    png = hp.replace('.html', '.png')
    subprocess.run([edge, '--headless', '--disable-gpu', '--hide-scrollbars',
                    '--user-data-dir=' + os.path.join(out_dir, '_edge_prof'),
                    '--window-size=1080,1920', f'--screenshot={png}',
                    'file:///' + hp.replace('\\', '/')],
                   capture_output=True)
    time.sleep(1.2)
    print(name, '→', os.path.basename(hp), os.path.exists(png), os.path.getsize(png) if os.path.exists(png) else 0)
