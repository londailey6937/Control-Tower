#!/usr/bin/env python3
"""Generate a Project Network Diagram PDF for the Digital Twin project."""

import os
from fpdf import FPDF

OUT_DIR = os.path.dirname(os.path.abspath(__file__))

BLUE = (30, 90, 200)
GRAY = (120, 120, 130)
TEXT = (40, 40, 45)
WHITE = (255, 255, 255)

# Node colors
C_COMPLETE = (5, 150, 105)
C_INPROG = (217, 119, 6)
C_NOTSTART = (99, 102, 241)
C_GATE = (220, 38, 38)
C_MILESTONE = (2, 132, 199)

_CHAR_MAP = str.maketrans({
    "\u2014": "--", "\u2013": "-", "\u2265": ">=", "\u2264": "<=",
    "\u00b5": "u", "\u00d7": "x",
})
def _a(s): return s.translate(_CHAR_MAP)


class NetDiagram(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(*GRAY)
        self.cell(0, 5, _a("ICU Respiratory Digital Twin -- Project Network Diagram  |  CONFIDENTIAL"), align="R")
        self.ln(7)

    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(*GRAY)
        self.cell(0, 5, f"Page {self.page_no()}/{{nb}}", align="C")


def _box(pdf, x, y, w, h, fill, label_lines, border_color=None):
    """Draw a rounded-ish colored box with centered text lines."""
    bc = border_color or fill
    pdf.set_draw_color(*bc)
    pdf.set_fill_color(*fill)
    pdf.set_line_width(0.4)
    pdf.rect(x, y, w, h, style="DF")
    pdf.set_text_color(*WHITE)
    pdf.set_font("Helvetica", "B", 6.5)
    line_h = 3.5
    total_h = len(label_lines) * line_h
    start_y = y + (h - total_h) / 2
    for i, line in enumerate(label_lines):
        pdf.set_xy(x, start_y + i * line_h)
        pdf.cell(w, line_h, _a(line), align="C")


def _diamond(pdf, cx, cy, rw, rh, fill, label_lines):
    """Draw a diamond (gate) as a rotated square approximation using a filled rect with border."""
    # Use a slightly different box style for gates
    x = cx - rw/2
    y = cy - rh/2
    pdf.set_draw_color(*fill)
    pdf.set_fill_color(*fill)
    pdf.set_line_width(0.6)
    # Draw hexagonal shape using polygon-like approach — simplified as a box with thick border
    pdf.rect(x, y, rw, rh, style="DF")
    # Inner highlight border
    pdf.set_draw_color(255, 255, 255)
    pdf.set_line_width(0.3)
    pdf.rect(x + 1, y + 1, rw - 2, rh - 2, style="D")
    pdf.set_text_color(*WHITE)
    pdf.set_font("Helvetica", "B", 6)
    line_h = 3.2
    total_h = len(label_lines) * line_h
    start_y = cy - total_h / 2
    for i, line in enumerate(label_lines):
        pdf.set_xy(x, start_y + i * line_h)
        pdf.cell(rw, line_h, _a(line), align="C")


def _arrow(pdf, x1, y1, x2, y2, color=GRAY):
    """Draw a line with a small arrowhead."""
    pdf.set_draw_color(*color)
    pdf.set_line_width(0.35)
    pdf.line(x1, y1, x2, y2)
    # small arrowhead
    import math
    angle = math.atan2(y2 - y1, x2 - x1)
    alen = 1.8
    pdf.line(x2, y2, x2 - alen * math.cos(angle - 0.4), y2 - alen * math.sin(angle - 0.4))
    pdf.line(x2, y2, x2 - alen * math.cos(angle + 0.4), y2 - alen * math.sin(angle + 0.4))


def build():
    pdf = NetDiagram()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=False)
    pdf.add_page("L")  # Landscape for diagram

    # Title
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(*BLUE)
    pdf.cell(0, 7, "Project Network Diagram", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(*TEXT)
    pdf.cell(0, 5, "ICU Respiratory Digital Twin System", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(*GRAY)
    pdf.cell(0, 4, _a("Dual-Track: Technical (T1-T8) + Regulatory (R1-R9) | Gates (G1-G6) | 23-month timeline"), align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)

    # ── Layout coordinates ──
    # Landscape A4: 297 x 210 mm, margins ~10mm
    # We'll lay out nodes in columns by month groups
    bw = 28  # box width
    bh = 14  # box height
    gw = 26  # gate width
    gh = 14  # gate height

    # Y lanes
    y_tech = 42     # Technical track
    y_reg = 72      # Regulatory track
    y_gate = 102    # Gate row
    y_eit_tech = 132 # EIT technical
    y_eit_reg = 162  # EIT regulatory

    # X positions by column (month groups)
    x_start = 14
    x_m0 = 42
    x_m1 = 72
    x_m2 = 102
    x_m3 = 136
    x_m6 = 166
    x_m8 = 186
    x_m9 = 206
    x_m12 = 226
    x_m14 = 240
    x_m17 = 256
    x_m23 = 276

    # ═══════════════════════════════════
    # DRAW SWIM LANE BACKGROUNDS
    # ═══════════════════════════════════
    pdf.set_fill_color(245, 247, 250)
    pdf.rect(10, 35, 277, 22, style="F")  # Tech lane
    pdf.set_fill_color(250, 247, 245)
    pdf.rect(10, 62, 277, 22, style="F")  # Reg lane
    pdf.set_fill_color(255, 245, 245)
    pdf.rect(10, 94, 277, 22, style="F")  # Gate lane
    pdf.set_fill_color(245, 247, 250)
    pdf.rect(10, 124, 277, 22, style="F")  # EIT Tech lane
    pdf.set_fill_color(250, 247, 245)
    pdf.rect(10, 152, 277, 22, style="F")  # EIT Reg lane

    # Lane labels
    pdf.set_font("Helvetica", "B", 6.5)
    pdf.set_text_color(*GRAY)
    for lbl, yy in [("TECH (sEMG)", 36), ("REGULATORY", 63), ("GATES", 95),
                     ("TECH (EIT)", 125), ("REG (EIT)", 153)]:
        pdf.set_xy(11, yy)
        pdf.cell(25, 4, lbl)

    # ═══════════════════════════════════
    # DRAW NODES
    # ═══════════════════════════════════

    # --- START ---
    pdf.set_draw_color(*C_COMPLETE)
    pdf.set_fill_color(*C_COMPLETE)
    pdf.ellipse(x_start - 6, (y_tech + y_reg) / 2 - 6, 12, 12, style="DF")
    pdf.set_text_color(*WHITE)
    pdf.set_font("Helvetica", "B", 6)
    pdf.set_xy(x_start - 6, (y_tech + y_reg) / 2 - 3)
    pdf.cell(12, 3, "START", align="C")
    pdf.set_xy(x_start - 6, (y_tech + y_reg) / 2)
    pdf.cell(12, 3, "M+0", align="C")
    start_cx = x_start
    start_cy = (y_tech + y_reg) / 2

    # Technical Track — sEMG
    nodes = {}
    def node(nid, x, y, lines, color):
        _box(pdf, x - bw/2, y - bh/2, bw, bh, color, lines)
        nodes[nid] = (x, y)

    node("T1", x_m0, y_tech, ["T1 (M+0)", "Prototype Final", "sEMG Module"], C_COMPLETE)
    node("T2", x_m1, y_tech, ["T2 (M+1)", "ECG-Gating", "Algorithm"], C_INPROG)
    node("T8", x_m2, y_tech - 2, ["T8 (M+2)", "MyoBus Protocol", "Integration"], C_INPROG)
    node("T3", x_m3, y_tech, ["T3 (M+3)", "Bench & Perf", "Testing sEMG"], C_NOTSTART)
    node("T4", x_m6, y_tech, ["T4 (M+6)", "sEMG Sensitivity", "Specificity"], C_NOTSTART)

    # Regulatory Track
    node("R1", x_m0, y_reg, ["R1 (M+0)", "Pre-Sub Q-Meeting", "Request Filed"], C_COMPLETE)
    node("R8", x_m1, y_reg, ["R8 (M+1)", "IP Buyout &", "US Legal"], C_INPROG)
    node("R2", x_m2, y_reg + 2, ["R2 (M+2)", "FDA Pre-Sub", "Meeting"], C_NOTSTART)
    node("R9", x_m3 - 6, y_reg, ["R9 (M+2)", "ISO 13485 Audit", "Silan Tech"], C_NOTSTART)
    node("R3", x_m6, y_reg, ["R3 (M+6)", "510(k) Submit", "sEMG"], C_NOTSTART)
    node("R4", x_m9, y_reg, ["R4 (M+9)", "510(k) Clearance", "sEMG"], C_MILESTONE)

    # Gates
    def gate(gid, x, y, lines):
        _diamond(pdf, x, y, gw, gh, C_GATE, lines)
        nodes[gid] = (x, y)

    gate("G1", x_m3, y_gate, ["G1 (M+3)", "sEMG Design", "Verification"])
    gate("G2", x_m2, y_gate, ["G2 (M+2)", "FDA Feedback", "Received"])
    gate("G3", x_m6, y_gate, ["G3 (M+6)", "510(k) sEMG", "Ready"])
    gate("G4", x_m9, y_gate, ["G4 (M+9)", "sEMG Commercial", "Launch"])

    # EIT Technical
    node("T5", x_m8, y_eit_tech, ["T5 (M+8)", "EIT Prototype", "32-Elec Belt"], C_NOTSTART)
    node("T6", x_m12, y_eit_tech, ["T6 (M+12)", "V/Q Algorithm", "Validation"], C_NOTSTART)
    node("T7", x_m14, y_eit_tech, ["T7 (M+14)", "EIT Biocompat", "Testing"], C_NOTSTART)

    # EIT Regulatory
    node("R5", x_m12, y_eit_reg, ["R5 (M+12)", "Begin EIT", "510(k) Prep"], C_NOTSTART)
    gate("G5", x_m17, y_eit_reg, ["G5 (M+17)", "EIT 510(k)", "Ready"])
    node("R6", x_m17, y_eit_tech, ["R6 (M+17)", "510(k) Submit", "EIT"], C_NOTSTART)
    node("R7", x_m23, y_eit_reg, ["R7 (M+23)", "510(k) Clearance", "EIT"], C_MILESTONE)
    gate("G6", x_m23, y_eit_tech, ["G6 (M+23)", "Full Platform", "Launch"])

    # ═══════════════════════════════════
    # DRAW ARROWS (dependencies)
    # ═══════════════════════════════════
    def arrow(frm, to, color=GRAY):
        x1, y1 = nodes[frm]
        x2, y2 = nodes[to]
        # Compute edge points
        dx = x2 - x1
        dy = y2 - y1
        import math
        dist = math.sqrt(dx*dx + dy*dy)
        if dist == 0:
            return
        # offset from center by half-box
        ox1 = (bw/2) * (dx/dist) if abs(dx) > abs(dy) else 0
        oy1 = (bh/2) * (dy/dist) if abs(dy) >= abs(dx) else 0
        ox2 = (bw/2) * (dx/dist) if abs(dx) > abs(dy) else 0
        oy2 = (bh/2) * (dy/dist) if abs(dy) >= abs(dx) else 0
        _arrow(pdf, x1 + ox1, y1 + oy1, x2 - ox2, y2 - oy2, color)

    # Start to first nodes
    _arrow(pdf, start_cx + 6, start_cy - 3, nodes["T1"][0] - bw/2, nodes["T1"][1], GRAY)
    _arrow(pdf, start_cx + 6, start_cy + 3, nodes["R1"][0] - bw/2, nodes["R1"][1], GRAY)
    _arrow(pdf, start_cx + 4, start_cy + 2, nodes["R8"][0] - bw/2, nodes["R8"][1], GRAY)

    # sEMG technical chain
    arrow("T1", "T2")
    arrow("T1", "T8")
    arrow("T2", "T3")
    arrow("T8", "T3")
    arrow("T3", "G1")
    arrow("G1", "T4")
    arrow("T4", "G3")

    # Regulatory chain
    arrow("R1", "R2")
    arrow("R8", "R2")
    arrow("R8", "R9")
    arrow("R2", "G2")
    arrow("G2", "T3", C_GATE)
    arrow("R9", "R3")
    arrow("R2", "G3")
    arrow("G3", "R3")
    arrow("R3", "R4")
    arrow("R4", "G4")

    # EIT branch
    arrow("R4", "T5")
    arrow("T5", "T6")
    arrow("T5", "T7")
    arrow("T6", "R5")
    arrow("T7", "R5")
    arrow("R5", "G5")
    arrow("G5", "R6")
    arrow("R6", "R7")
    arrow("R7", "G6")
    arrow("T8", "R5", C_INPROG)

    # ═══════════════════════════════════
    # LEGEND
    # ═══════════════════════════════════
    ly = 176
    lx = 14
    pdf.set_font("Helvetica", "B", 7)
    pdf.set_text_color(*TEXT)
    pdf.set_xy(lx, ly)
    pdf.cell(20, 4, "LEGEND:")

    legend = [
        (C_COMPLETE, "Complete"),
        (C_INPROG, "In Progress"),
        (C_NOTSTART, "Not Started"),
        (C_GATE, "Decision Gate"),
        (C_MILESTONE, "Key Milestone"),
    ]
    lx2 = lx + 22
    for color, label in legend:
        pdf.set_fill_color(*color)
        pdf.rect(lx2, ly + 0.5, 8, 3, style="F")
        pdf.set_xy(lx2 + 9, ly)
        pdf.set_font("Helvetica", "", 6.5)
        pdf.set_text_color(*TEXT)
        pdf.cell(20, 4, label)
        lx2 += 32

    # Critical path note
    pdf.set_xy(14, ly + 6)
    pdf.set_font("Helvetica", "B", 7)
    pdf.set_text_color(*C_GATE)
    pdf.cell(0, 4, _a("CRITICAL PATH: START -> T1 -> T2 -> T3 -> G1 -> T4 -> G3 -> R3 -> R4 -> G4 -> T5 -> T6/T7 -> R5 -> G5 -> R6 -> R7 -> G6"))

    # Date/author
    pdf.set_xy(14, ly + 12)
    pdf.set_font("Helvetica", "I", 7)
    pdf.set_text_color(*GRAY)
    pdf.cell(0, 4, "Prepared: March 21, 2026  |  PM: Lon Dailey  |  Company B USA  |  23-month program (M+0 to M+23)")

    path = os.path.join(OUT_DIR, "Network_Diagram.pdf")
    pdf.output(path)
    return path


if __name__ == "__main__":
    p = build()
    print(f"PDF: {p}")
    print("Done.")
