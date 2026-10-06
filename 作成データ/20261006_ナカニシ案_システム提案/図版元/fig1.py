"""Figure for page 1: overall system concept (schematic; layout and sizes are not decided).

Outputs fig1.svg and fig1_anchors.json (SVG user units; 10 units = 1 mm on the slide).
Same camera orientation as fig2 so the rotary unit points the same way on both pages.
"""
import json
import math
import sys

from iso import (Cam, Svg, axial, axial_z, box, grooves, shadow, ring_pts, arrow_marker, bezier,
                 METAL, DARK, BLUEMETAL, GOLD)

W, H = 2850, 1250
NAVY, BLUE, ORANGE, RED = "#1F3A5F", "#2E6DB4", "#D9822B", "#E53935"

# ---- auto-fit: project the scene bounding points with a unit camera ----
probe = Cam(a=1.0, b=1.7, c=1.05, scale=1.0)
pts = []
for (x0, x1, y0, y1, z0, z1) in ((0, 900, 0, 600, 0, 1000), (-700, -250, 350, 950, 0, 900),
                                 (1000, 1400, -400, 0, 0, 1010), (600, 800, 350, 450, 1000, 1200)):
    for x in (x0, x1):
        for y in (y0, y1):
            for z in (z0, z1):
                pts.append(probe.p(x, y, z))
minx, maxx = min(p[0] for p in pts), max(p[0] for p in pts)
miny, maxy = min(p[1] for p in pts), max(p[1] for p in pts)
FX0, FX1, FY0, FY1 = 300, 2440, 25, 1225
s = min((FX1 - FX0) / (maxx - minx), (FY1 - FY0) / (maxy - miny))
ox = FX0 + ((FX1 - FX0) - s * (maxx - minx)) / 2 - s * minx
oy = FY0 + ((FY1 - FY0) - s * (maxy - miny)) / 2 - s * miny
cam = Cam(a=1.0, b=1.7, c=1.05, scale=s, ox=ox, oy=oy)
P = cam.p
svg = Svg(W, H)
A = {}

# ---------------- floor shadows ----------------
shadow(svg, cam, 0, 0, 900, 600, 0, dx=10, dy=14, sd=16, opacity=0.22)
shadow(svg, cam, -700, 350, -250, 950, 0, dx=10, dy=14, sd=14, opacity=0.2)
shadow(svg, cam, 1000, -400, 1400, 0, 0, dx=10, dy=14, sd=14, opacity=0.2)

# ================= ① laser oscillator rack (TRUMPF, left-back) =================
box(svg, cam, -700, 350, 0, 450, 600, 900, top="#e6eaee", front="#c9d0d7", side="#b7c0c8", stroke="#56606a")
# 19-inch style front units (schematic)
def rf(x, z):
    return P(x, 350, z)
for (z0, z1, col) in ((640, 860, "#2f3a46"), (430, 620, "#3b4754"), (230, 410, "#46525f")):
    svg.poly([rf(-680, z0), rf(-270, z0), rf(-270, z1), rf(-680, z1)], col, "#1f262d", 1.2)
    svg.poly([rf(-650, z1 - 50), rf(-560, z1 - 50), rf(-560, z1 - 25), rf(-650, z1 - 25)], "#7fb2e5", "none")
    for i in range(4):
        c = rf(-420 + i * 32, (z0 + z1) / 2)
        svg.circle(c, 3.2, "#9fb0c0", "none")
A["rack"] = P(-475, 350, 760)
A["rack_top"] = P(-475, 650, 900)

# ================= control cabinet + touch panel (right-front) =================
box(svg, cam, 1000, -400, 0, 400, 400, 800, top="#e9edf1", front="#d3dae0", side="#bfc8d0", stroke="#56606a")
def cf(x, z):
    return P(x, -400, z)
svg.poly([cf(1030, 40), cf(1370, 40), cf(1370, 760), cf(1030, 760)], "none", "#7d8893", 1.6)
svg.line([cf(1340, 360), cf(1340, 460)], "#4b5560", 6.0)
# emergency stop on the cabinet front
es = cf(1110, 690)
svg.circle(es, 26, "#F2C200", "#7a6400", 1.2)
svg.circle(es, 15, "#D32F2F", "#7f1d1d", 1.2)
A["estop"] = es
# touch panel on the cabinet top (schematic)
box(svg, cam, 1080, -380, 800, 240, 40, 30, top="#c4ccd3", front="#aeb7c0", side="#9aa4ae", stroke="#4b5560")
box(svg, cam, 1060, -392, 830, 280, 22, 180, top="#3a424b", front="#2a3037", side="#20262c", stroke="#14181c")
scr = [P(1078, -392.5, 846), P(1322, -392.5, 846), P(1322, -392.5, 994), P(1078, -392.5, 994)]
svg.poly(scr, svg.lin_grad(scr[3], scr[1], [(0, "#5f8fc4"), (1, "#bcd4ee")]), "#14181c", 1.0)
for i in range(3):
    svg.poly([P(1100 + i * 72, -393, 870), P(1160 + i * 72, -393, 870), P(1160 + i * 72, -393, 905), P(1100 + i * 72, -393, 905)],
             "#e8f0fa", "none", opacity=0.85)
A["panel"] = P(1200, -392, 1010)
A["cabinet"] = P(1200, -400, 560)

# ================= machine stand =================
box(svg, cam, 0, 0, 0, 900, 600, 420, top="#eef2f5", front="#d6dde3", side="#c3cbd3", stroke="#56606a")
def sf(x, z):
    return P(x, 0, z)
for (x0, x1) in ((40, 440), (460, 860)):
    svg.poly([sf(x0, 40), sf(x1, 40), sf(x1, 380), sf(x0, 380)], "none", "#8a959f", 1.4)
svg.line([sf(420, 170), sf(420, 250)], "#4b5560", 5.0)
svg.line([sf(480, 170), sf(480, 250)], "#4b5560", 5.0)

# ================= enclosure (back faces first) =================
EZ0, EZ1 = 420, 1000
back = [P(0, 600, EZ0), P(900, 600, EZ0), P(900, 600, EZ1), P(0, 600, EZ1)]
right = [P(900, 0, EZ0), P(900, 600, EZ0), P(900, 600, EZ1), P(900, 0, EZ1)]
svg.poly(back, "#dde7f1", "#7f93a8", 1.4, opacity=0.9)
svg.poly(right, "#cfdbe8", "#7f93a8", 1.4, opacity=0.9)
for (x, y) in ((0, 600), (900, 600)):
    box(svg, cam, x - (24 if x else 0), y - 24, EZ0, 24, 24, EZ1 - EZ0, top="#9aa5b0", front="#8693a0", side="#76838f", stroke="#4b5763", sw=1.0)

# ---------------- interior ----------------
# ③ inner base plate
box(svg, cam, 110, 110, EZ0, 680, 380, 14, top="#e2e6ea", front="#c3cad1", side="#b1bac3", stroke="#69737d")
A["base"] = P(700, 110, EZ0 + 7)
# laser head column (behind)
box(svg, cam, 470, 420, EZ0 + 14, 50, 50, 460, top="#aab5c0", front="#95a2ae", side="#84919d", stroke="#4f5b67")
# ④ adjustment stage (stacked blocks + knob)
box(svg, cam, 200, 200, EZ0 + 14, 330, 200, 30, top="#d7dde3", front="#b9c2cb", side="#a6b0ba", stroke="#56606a")
box(svg, cam, 230, 215, EZ0 + 44, 270, 170, 26, top="#c8d6e6", front="#a9bdd3", side="#97adc6", stroke="#4f6274")
axial(svg, cam, 160, 200, 11, 11, 300, EZ0 + 30, stops=DARK, cap="#59626d", stroke="#15191d", sw=1.0)
A["stage"] = P(365, 215, EZ0 + 57)
ZC = EZ0 + 70 + 38  # rotary axis height
# ② rotary unit (simplified version of page 2) + ③ holders
for (hx0, hx1, rr) in ((360, 392, 11.4), (450, 488, 12.0)):
    box(svg, cam, hx0, 284, EZ0 + 70, hx1 - hx0, 32, ZC - rr - (EZ0 + 70) + 1, top="#c9d9ec", front="#a9c1de",
        side="#93afd2", stroke=BLUE, sw=1.2, opacity=0.85, dash="6 4")
axial(svg, cam, 520, 532, 10.5, 9.5, 300, ZC, stops=DARK, cap="#2c3238", stroke="#15191d", sw=0.8)
axial(svg, cam, 420, 520, 12.0, 12.0, 300, ZC, stops=DARK, cap="#4a525b", stroke="#15191d", sw=0.8)
axial(svg, cam, 355, 415, 11.4, 11.4, 300, ZC, stops=BLUEMETAL, cap="#d4dde6", stroke="#4f5f70", sw=0.8)
axial(svg, cam, 266, 350, 9.6, 9.6, 300, ZC, stops=METAL, cap="#dfe5ea", sw=0.8)
axial(svg, cam, 252, 266, 4.2, 7.8, 300, ZC, stops=METAL, cap="#c3ccd4", sw=0.8)
axial(svg, cam, 228, 252, 1.4, 1.4, 300, ZC, stops=GOLD, cap="#d6bd6c", stroke="#7c6220", sw=0.6)
box(svg, cam, 286, 297.4, ZC + 9.4, 44, 5.2, 3.2, top="#3a424b", front="#2a3037", side="#20262c", stroke="#14181c", sw=0.6)
A["rotary"] = P(400, 300, ZC + 12)
A["holder"] = P(470, 284, EZ0 + 80)
A["work"] = P(236, 300, ZC)
# ① laser head: arm, scanner box, lens
box(svg, cam, 300, 270, 850, 220, 60, 36, top="#aab5c0", front="#95a2ae", side="#84919d", stroke="#4f5b67")
box(svg, cam, 160, 230, 800, 190, 140, 110, top="#5d6773", front="#3f4852", side="#353d46", stroke="#1d232a")
axial_z(svg, cam, 735, 800, 22, 22, 240, 300, stops=DARK, cap="#59626d", stroke="#15191d", sw=1.0)
A["head"] = P(255, 230, 880)
beam_top = P(240, 300, 735)
beam_bot = P(240, 300, ZC + 1.4)
svg.add(f'<path d="M {beam_top[0]:.1f} {beam_top[1]:.1f} L {beam_bot[0]:.1f} {beam_bot[1]:.1f}" stroke="{RED}" '
        f'stroke-width="9" opacity="0.35" filter="{svg.blur(4)}"/>')
svg.line([beam_top, beam_bot], RED, 3.0)
svg.circle(beam_bot, 6, RED, extra=f'opacity="0.6" filter="{svg.blur(3)}"')
# fiber/cable inside the enclosure (from roof to head)
svg.line([P(330, 330, EZ1), P(300, 330, 910)], "#1b1f24", 6.0)

# ================= enclosure front parts (translucent) =================
for (x, y) in ((0, 0), (900, 0)):
    box(svg, cam, x - (24 if x else 0), y, EZ0, 24, 24, EZ1 - EZ0, top="#9aa5b0", front="#8693a0", side="#76838f", stroke="#4b5763", sw=1.0)
left = [P(0, 0, EZ0), P(0, 0, EZ1), P(0, 600, EZ1), P(0, 600, EZ0)]
front = [P(0, 0, EZ0), P(900, 0, EZ0), P(900, 0, EZ1), P(0, 0, EZ1)]
top = [P(0, 0, EZ1), P(900, 0, EZ1), P(900, 600, EZ1), P(0, 600, EZ1)]
svg.poly(left, "#bcd3ea", "#5f7894", 2.0, opacity=0.22)
svg.poly(front, "#bcd3ea", "#5f7894", 2.0, opacity=0.14)
svg.poly(top, "#c9dcef", "#5f7894", 2.0, opacity=0.30)
for edge in ((P(0, 0, EZ1), P(900, 0, EZ1)), (P(0, 0, EZ1), P(0, 600, EZ1)), (P(900, 0, EZ1), P(900, 600, EZ1)),
             (P(0, 600, EZ1), P(900, 600, EZ1))):
    svg.line(list(edge), "#5f7894", 5.0)
# door outline + handle + interlock switch
door = [P(90, 0, EZ0 + 30), P(810, 0, EZ0 + 30), P(810, 0, EZ1 - 40), P(90, 0, EZ1 - 40)]
svg.poly(door, "none", "#41607f", 3.0, dash="18 10")
svg.line([P(780, -2, 620), P(780, -2, 760)], "#2b3a4a", 9.0)
box(svg, cam, 820, -14, 930, 50, 14, 34, top="#F2C200", front="#E0B000", side="#c79c00", stroke="#6b5600", sw=1.0)
A["door"] = P(450, 0, EZ1 - 40)
A["interlock"] = P(845, -14, 947)
A["enclosure"] = P(0, 300, EZ1 - 80)
A["door_tr"] = P(800, 0, EZ1 - 60)
A["enc_tr"] = P(900, 0, EZ1)
A["stand_fl_top"] = P(0, 0, 420)
A["stand_fr_top"] = P(900, 0, 420)
A["stand_fl_bot"] = P(0, 0, 0)
A["stand_fr_bot"] = P(900, 0, 0)
A["cab_tl"] = P(1000, -400, 800)
A["cab_fr_top"] = P(1400, -400, 800)

# ================= ⑦ exhaust duct (requirement undecided -> dashed) =================
dx = 700
hull = axial_z(svg, cam, EZ1, EZ1 + 150, 45, 45, dx, 400, stops=[(0, "#fbfcfd"), (1, "#eef2f6")], cap="#fbfcfd",
        stroke="none", sw=0, opacity=0.95)
svg.poly(hull, "none", ORANGE, 3.0, dash="12 8")
ring = ring_pts(cam, "z", (dx, 400, EZ1 + 150), 45)
svg.line(ring, ORANGE, 3.0, dash="12 8")
A["exhaust"] = P(dx, 400, EZ1 + 150)

# ================= cables (schematic) =================
rt = A["rack_top"]
et = P(330, 330, EZ1)
fiber = bezier(rt, (rt[0] + 40, rt[1] - 260), (et[0] - 260, et[1] - 300), et, n=60)
svg.line(fiber, "#1b1f24", 7.0)
A["fiber"] = fiber[22]
# wiring between control cabinet and machine stand
w0 = P(1000, -200, 300)
w1 = P(900, 300, 260)
svg.line(bezier(w0, (w0[0] - 60, w0[1] + 60), (w1[0] + 80, w1[1] + 70), w1, n=30), "#1b1f24", 6.0)

open(sys.argv[1] if len(sys.argv) > 1 else "fig1.svg", "w").write(svg.svg())
json.dump({k: [round(v[0], 1), round(v[1], 1)] for k, v in A.items()}, open("fig1_anchors.json", "w"),
          ensure_ascii=False, indent=1)
print("scale", round(s, 3))
