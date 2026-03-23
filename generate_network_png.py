#!/usr/bin/env python3
"""
Network Diagram -- ICU Respiratory Digital Twin System
High-quality PNG with AON boxes, CPM Total Float, critical path.
"""

import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

OUT = os.path.dirname(os.path.abspath(__file__))

# ================================================================
# 1.  ACTIVITIES
# ================================================================
activities = {
    # -- Technical --
    "T1": {"name": "Prototype Final\nsEMG Module",     "dur": 1, "preds": [],              "month": 0,  "st": "complete",    "trk": "T"},
    "T2": {"name": "ECG-Gating\nAlgorithm Valid.",     "dur": 1, "preds": ["T1"],           "month": 1,  "st": "in-progress", "trk": "T"},
    "T8": {"name": "MyoBus Protocol\nIntegration",     "dur": 2, "preds": ["T1"],           "month": 2,  "st": "in-progress", "trk": "T"},
    "T3": {"name": "Bench & Perf\nTesting sEMG",       "dur": 1, "preds": ["T2","T8","R2"], "month": 3,  "st": "not-started", "trk": "T"},
    "T4": {"name": "sEMG Sensitivity\n& Specificity",  "dur": 3, "preds": ["T3"],           "month": 6,  "st": "not-started", "trk": "T"},
    "T5": {"name": "EIT Prototype\n32-Elec Belt",      "dur": 2, "preds": ["T4"],           "month": 8,  "st": "not-started", "trk": "T"},
    "T6": {"name": "V/Q Algorithm\nValidation",        "dur": 4, "preds": ["T5"],           "month": 12, "st": "not-started", "trk": "T"},
    "T7": {"name": "EIT Biocompat\nTesting",           "dur": 6, "preds": ["T5"],           "month": 14, "st": "not-started", "trk": "T"},
    # -- Regulatory --
    "R1": {"name": "Pre-Sub Q-Meeting\nRequest Filed",  "dur": 1, "preds": [],              "month": 0,  "st": "complete",    "trk": "R"},
    "R8": {"name": "IP Buyout &\nUS Legal Structure",   "dur": 2, "preds": [],              "month": 1,  "st": "in-progress", "trk": "R"},
    "R2": {"name": "FDA Pre-Sub\nMeeting",              "dur": 1, "preds": ["R1","R8"],      "month": 2,  "st": "not-started", "trk": "R"},
    "R9": {"name": "ISO 13485 Audit\nSilan Technology", "dur": 1, "preds": ["R8"],           "month": 2,  "st": "not-started", "trk": "R"},
    "R3": {"name": "510(k) Submit\nsEMG Module",        "dur": 1, "preds": ["T4","R9"],      "month": 6,  "st": "not-started", "trk": "R"},
    "R4": {"name": "510(k) Clearance\nsEMG",            "dur": 3, "preds": ["R3"],           "month": 9,  "st": "not-started", "trk": "R"},
    "R5": {"name": "Begin EIT\n510(k) Prep",            "dur": 2, "preds": ["T6","R4"],      "month": 12, "st": "not-started", "trk": "R"},
    "R6": {"name": "510(k) Submit\nEIT System",         "dur": 1, "preds": ["R5","T7"],      "month": 17, "st": "not-started", "trk": "R"},
    "R7": {"name": "510(k) Clearance\nEIT System",      "dur": 6, "preds": ["R6"],           "month": 23, "st": "not-started", "trk": "R"},
}

# ================================================================
# 2.  CPM
# ================================================================
def topo(acts):
    indeg = {a: 0 for a in acts}
    succ = {a: [] for a in acts}
    for a, d in acts.items():
        for p in d["preds"]:
            succ[p].append(a)
            indeg[a] += 1
    q = sorted(a for a in acts if indeg[a] == 0)
    out = []
    while q:
        n = q.pop(0); out.append(n)
        for s in succ[n]:
            indeg[s] -= 1
            if indeg[s] == 0:
                q.append(s); q.sort()
    return out, succ

order, succ_map = topo(activities)

for a in order:
    d = activities[a]
    d["ES"] = max((activities[p]["EF"] for p in d["preds"]), default=0)
    d["EF"] = d["ES"] + d["dur"]

proj_end = max(d["EF"] for d in activities.values())

for a in reversed(order):
    d = activities[a]
    d["LF"] = min((activities[s]["LS"] for s in succ_map[a]), default=proj_end)
    d["LS"] = d["LF"] - d["dur"]
    d["TF"] = d["LS"] - d["ES"]
    d["crit"] = d["TF"] == 0

hdr = f"{'ID':<4} {'M':>3} {'Dur':>3}  {'ES':>3} {'EF':>3} {'LS':>3} {'LF':>3}  {'TF':>3}  Crit"
print(hdr); print("-"*len(hdr))
for a in order:
    d = activities[a]
    print(f"{a:<4} {d['month']:>3} {d['dur']:>3}  {d['ES']:>3} {d['EF']:>3} {d['LS']:>3} {d['LF']:>3}  {d['TF']:>3}{'  ***' if d['crit'] else ''}")
print(f"\nCPM Project Duration: {proj_end} months")

# ================================================================
# 3.  LAYOUT
# ================================================================
BW, BH = 3.6, 3.0          # box size

# Four horizontal lanes
YT1, YT2 = 11.5, 7.5       # tech main / tech sub
YR1, YR2 = 3.0, -1.0        # reg main / reg sub

pos = {
    "T1": ( 2.5, YT1),  "T2": ( 7.5, YT1),  "T8": ( 7.5, YT2),
    "T3": (13.0, YT1),  "T4": (19.0, YT1),   "T5": (25.0, YT1),
    "T6": (31.0, YT1),  "T7": (31.0, YT2),
    "R1": ( 2.5, YR1),  "R8": ( 2.5, YR2),
    "R2": ( 7.5, YR1),  "R9": ( 7.5, YR2),
    "R3": (19.0, YR1),  "R4": (25.0, YR1),
    "R5": (37.0, YR1),  "R6": (43.0, YR1),  "R7": (49.0, YR1),
}

# ================================================================
# 4.  DRAW
# ================================================================
fig, ax = plt.subplots(figsize=(38, 15), dpi=180)
ax.set_xlim(-2.0, 53.5)
ax.set_ylim(-6.0, 16.0)
ax.set_aspect("equal"); ax.axis("off")
fig.patch.set_facecolor("white")

CR_c  = "#DC2626";  CB_c  = "#2563EB"
CG_c  = "#059669";  CO_c  = "#D97706"

# Swim lanes
ax.add_patch(FancyBboxPatch((-0.5, 5.5), 52, 9,
    boxstyle="round,pad=0.4", fc="#F0F5FF", ec="#CBD5E1", lw=0.7, zorder=0))
ax.text(0, 14.2, "TECHNICAL  TRACK   (T1 -- T8)",
    fontsize=12, fontweight="bold", color="#1E40AF", va="bottom")
ax.add_patch(FancyBboxPatch((-0.5, -3.0), 52, 8,
    boxstyle="round,pad=0.4", fc="#FFF8F0", ec="#FED7AA", lw=0.7, zorder=0))
ax.text(0, 4.7, "REGULATORY  TRACK   (R1 -- R9)",
    fontsize=12, fontweight="bold", color="#92400E", va="bottom")

# Title
ax.text(26, 15.8, "PROJECT  NETWORK  DIAGRAM  --  CPM  ANALYSIS  WITH  TOTAL  FLOAT",
    fontsize=16, fontweight="bold", color="#0F172A", ha="center", va="bottom")
ax.text(26, 15.1,
    "ICU Respiratory Digital Twin System  |  Dual-Track 23-Month Program  |  March 2026",
    fontsize=10, color="#64748B", ha="center", va="bottom")
ax.text(51, 15.8, "CONFIDENTIAL", fontsize=8, color=CR_c,
    ha="right", va="bottom", fontweight="bold")

# ── Node drawing ──
def draw_node(aid, x, y):
    d = activities[aid]
    hw, hh = BW/2, BH/2
    if d["st"] == "complete":       bc, fc, tc = CG_c, "#ECFDF5", "#065F46"
    elif d["st"] == "in-progress":  bc, fc, tc = CO_c, "#FFFBEB", "#78350F"
    elif d["crit"]:                 bc, fc, tc = CR_c, "#FEF2F2", "#7F1D1D"
    else:                           bc, fc, tc = CB_c, "#EFF6FF", "#1E3A5F"
    lw = 3.0 if d["crit"] else 1.6

    # Main rect
    ax.add_patch(FancyBboxPatch((x-hw, y-hh), BW, BH,
        boxstyle="round,pad=0.12", fc=fc, ec=bc, lw=lw, zorder=3))

    # Header band
    hy = y + hh - 0.62
    ax.fill_between([x-hw+0.1, x+hw-0.1], hy, y+hh-0.06,
        color=bc, alpha=0.18, zorder=4)
    ax.text(x-hw+0.22, hy+0.28, aid, fontsize=11, fontweight="bold",
        color=bc, va="center", ha="left", zorder=5)
    ax.text(x+hw-0.22, hy+0.28, f"M+{d['month']}",
        fontsize=9, color=bc, va="center", ha="right", zorder=5)

    # Activity name
    ax.text(x, y+0.25, d["name"], fontsize=8, color=tc,
        va="center", ha="center", linespacing=1.15, zorder=5)

    # Duration
    ax.text(x, y-0.45, f"Dur: {d['dur']} mo", fontsize=6.5, color="#6B7280",
        va="center", ha="center", zorder=5)

    # CPM bottom band
    bby = y - hh + 0.08
    bbh = 0.82
    ax.fill_between([x-hw+0.1, x+hw-0.1], bby, bby+bbh,
        color=bc, alpha=0.10, zorder=4)
    cols = [("ES",d["ES"]),("EF",d["EF"]),("LS",d["LS"]),("LF",d["LF"]),("TF",d["TF"])]
    cw = (BW-0.44)/5
    cx0 = x - hw + 0.22
    for i,(lb,v) in enumerate(cols):
        cx = cx0 + i*cw + cw/2
        ax.text(cx, bby+bbh-0.08, lb, fontsize=5.5, color="#6B7280",
            va="top", ha="center", zorder=5)
        clr = CR_c if lb=="TF" and v==0 else (CB_c if lb=="TF" else tc)
        wt = "bold" if lb=="TF" else "normal"
        ax.text(cx, bby+0.12, str(v), fontsize=8, color=clr,
            va="bottom", ha="center", fontweight=wt, zorder=5)

    # Float badge
    if d["TF"] > 0:
        bx, by = x+hw+0.1, y+hh-0.1
        ax.add_patch(plt.Circle((bx,by), 0.42, fc=CB_c, ec="white", lw=1.5, zorder=6))
        ax.text(bx, by, str(d["TF"]), fontsize=9, color="white",
            fontweight="bold", va="center", ha="center", zorder=7)
        ax.text(bx, by-0.60, "float", fontsize=5, color=CB_c,
            va="top", ha="center", zorder=7)

for aid in activities:
    draw_node(aid, *pos[aid])

# ── Arrows ──
def draw_arrow(a_fr, a_to):
    x1,y1 = pos[a_fr]; x2,y2 = pos[a_to]
    hw, hh = BW/2, BH/2
    dx, dy = x2-x1, y2-y1

    # Pick connection points
    if abs(dx) >= abs(dy)*0.3:
        sx, sy = x1+hw, y1;  tx, ty = x2-hw, y2
        if dx < 0: sx, tx = x1-hw, x2+hw
    elif dy > 0:
        sx, sy = x1, y1+hh;  tx, ty = x2, y2-hh
    else:
        sx, sy = x1, y1-hh;  tx, ty = x2, y2+hh

    d1, d2 = activities[a_fr], activities[a_to]
    crit = d1["crit"] and d2["crit"]
    col = CR_c if crit else "#94A3B8"
    lw = 2.2 if crit else 1.0
    astyle = "Simple,tail_width=1.0,head_width=7,head_length=5" if crit \
        else "Simple,tail_width=0.5,head_width=4,head_length=3"
    rad = 0.12 if abs(dy) > 3 else 0.05

    ax.add_patch(FancyArrowPatch((sx,sy),(tx,ty),
        arrowstyle=astyle, color=col, lw=lw,
        connectionstyle=f"arc3,rad={rad}", zorder=2, alpha=0.85))

for aid, d in activities.items():
    for p in d["preds"]:
        draw_arrow(p, aid)

# ── Timeline ruler ──
tl_y = -3.8
ax.plot([-0.5, 52], [tl_y, tl_y], color="#CBD5E1", lw=1.5, zorder=1)
mx_map = {0:2.5, 1:5, 2:7.5, 3:13, 6:19, 8:25, 9:28, 12:34, 14:36, 17:43, 23:49}
for m, mx in mx_map.items():
    ax.plot([mx,mx],[tl_y-0.2,tl_y+0.2], color="#475569", lw=1, zorder=1)
    ax.text(mx, tl_y-0.5, f"M+{m}", fontsize=7.5, color="#475569", ha="center", va="top")
ax.text(-0.5, tl_y, "TIMELINE ", fontsize=7.5, fontweight="bold",
    color="#475569", ha="right", va="center")

# ── Legend ──
patches = [
    mpatches.Patch(fc="#FEF2F2", ec=CR_c, lw=2.5, label="Critical Path (TF = 0)"),
    mpatches.Patch(fc="#EFF6FF", ec=CB_c, lw=1.5, label="Has Float (TF > 0)"),
    mpatches.Patch(fc="#ECFDF5", ec=CG_c, lw=1.5, label="Complete"),
    mpatches.Patch(fc="#FFFBEB", ec=CO_c, lw=1.5, label="In Progress"),
]
ax.legend(handles=patches, loc="lower left", bbox_to_anchor=(0.0, -0.02),
    ncol=4, fontsize=9, frameon=True, framealpha=0.95,
    edgecolor="#CBD5E1", fancybox=True)

# Key text — same line as prepared date
ax.text(51, -5.3,
    "ES = Early Start  |  EF = Early Finish  |  LS = Late Start  |  LF = Late Finish  |  TF = Total Float (months)",
    fontsize=7, color="#94A3B8", ha="right", va="top")

# Critical path string
cp = [a for a in order if activities[a]["crit"]]
ax.text(0.5, -2.5,
    f"CRITICAL PATH:  {' -> '.join(cp)}",
    fontsize=8, fontweight="bold", color=CR_c, va="bottom")

# Float summary — placed inside the technical track area (upper right)
fsum = sorted(((a,d["TF"]) for a,d in activities.items() if d["TF"]>0),
              key=lambda x:-x[1])
fx = 40; fy = 13.8
ax.text(fx, fy, "FLOAT  SUMMARY", fontsize=9, fontweight="bold", color="#1E293B", va="bottom")
for i,(a,tf) in enumerate(fsum):
    ax.text(fx, fy - 0.55 - i*0.50,
        f"{a} ({activities[a]['name'].split(chr(10))[0]}):  {tf} mo",
        fontsize=7.5, color=CB_c, fontweight="bold", va="top")

ax.text(26, -5.3, "Prepared: March 21, 2026  |  PM: Lon Dailey, PMP  |  Company B USA",
    fontsize=7, color="#94A3B8", ha="center", va="top")

plt.tight_layout()
out = os.path.join(OUT, "Network_Diagram.png")
plt.savefig(out, dpi=180, bbox_inches="tight", facecolor="white", pad_inches=0.4)
plt.close()
print(f"\nPNG saved: {out}")
