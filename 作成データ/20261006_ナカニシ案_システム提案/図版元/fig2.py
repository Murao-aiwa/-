"""Figure for page 2: Nakanishi rotary unit concept (schematic, not to scale).

Outputs fig2.svg and fig2_anchors.json (screen coordinates in SVG user units, 10 units = 1 mm on the slide).
"""
import json
import math
import random
import sys

from iso import (Cam, Svg, axial, axial_z, box, grooves, shadow, ring_pts, arrow_marker, bezier,
                 METAL, DARK, BLUEMETAL, GOLD)

W, H = 2850, 1240
NAVY, BLUE, ORANGE, RED = "#1F3A5F", "#2E6DB4", "#D9822B", "#E53935"

svg = Svg(W, H)
cam = Cam(a=1.0, b=1.7, c=1.05, scale=5.2, ox=760, oy=990)
P = cam.p
ZC = 46.0  # axis height (mm, schematic)
A = {}

# ---------------- shadows ----------------
shadow(svg, cam, -45, -55, 290, 55, 0, dx=14, dy=20, sd=18, opacity=0.22)
shadow(svg, cam, 320, -20, 420, 60, 0, dx=10, dy=16, sd=14, opacity=0.22)

# ---------------- E2280 controller (separate box) ----------------
box(svg, cam, 320, -20, 0, 100, 80, 62, top="#eef1f4", front="#d9dee3", side="#c3cad1", stroke="#59636d")
# front panel (y = -20 face)
def fp(x, z):
    return P(x, -20, z)
panel = [fp(328, 10), fp(412, 10), fp(412, 54), fp(328, 54)]
svg.poly(panel, "#3a434d", "#2a3038", 1.2)
disp = [fp(350, 34), fp(372, 34), fp(372, 48), fp(350, 48)]
svg.poly(disp, "#0f1a14", "#202a24", 1.0)
for i, x in enumerate((354, 362)):
    seg = [fp(x, 37), fp(x + 6, 37), fp(x + 6, 45), fp(x, 45)]
    svg.poly(seg, "none", "#5fe08a", 2.2)
for x in (384, 396):
    c = fp(x, 41)
    svg.circle(c, 9, "#c8cfd6", "#20262c", 1.2)
conn = fp(337, 22)
svg.circle(conn, 11, "#9aa3ad", "#20262c", 1.4)
svg.circle(conn, 5, "#2b3036", "none")
svg.poly([fp(386, 16), fp(406, 16), fp(406, 26), fp(386, 26)], "#c8cfd6", "#20262c", 1.0)
A["e2280"] = P(370, -20, 62)
A["e2280_conn"] = conn

# ---------------- base plate ----------------
box(svg, cam, -45, -55, 0, 335, 110, 12, top="#e4e8ec", front="#c5ccd3", side="#b2bbc4", stroke="#69737d")
for (x, y) in ((-30, -40), (275, -40), (-30, 40), (275, 40)):
    c = P(x, y, 12)
    svg.circle(c, 7, "#9aa4ae", "#69737d", 1.0)
    svg.circle(c, 3.5, "#59636d", "none")
A["plate"] = P(250, -55, 6)

# ---------------- holders (③, shape/position undecided) ----------------
HOLD_FILL, HOLD_ST = "#9DB9DA", BLUE
for (hx0, hx1, rr) in ((118, 148, 11.4), (205, 240, 12.0)):
    box(svg, cam, hx0, -16, 12, hx1 - hx0, 32, ZC - rr - 12 + 1.5, top="#c9d9ec", front="#a9c1de", side="#93afd2",
        stroke=HOLD_ST, sw=2.0, opacity=0.78, dash="10 7")

# ---------------- EM-2350J motor (far) ----------------
# cable leaving the rear first (behind the motor body)
axial(svg, cam, 268, 280, 10.5, 9.5, 0, ZC, stops=DARK, cap="#2c3238", stroke="#15191d")
axial(svg, cam, 168, 268, 12.0, 12.0, 0, ZC, stops=DARK, cap="#4a525b", stroke="#15191d")
grooves(svg, cam, (176, 182), 12.0, 0, ZC, color="#9aa3ad", sw=1.6, opacity=0.55)
A["motor"] = P(225, 0, ZC + 12)
A["motor_rear"] = P(280, 0, ZC)

# connection gap marker 2 (ARG-01 / EM-2350J)
axial(svg, cam, 163, 168, 13.6, 13.6, 0, ZC, stops=[(0, "#FFE2BF"), (1, "#FFC98A")], cap="#FFE7C9",
      stroke=ORANGE, sw=2.2, opacity=0.55)
gap2 = ring_pts(cam, "x", (165.5, 0, ZC), 16.5)
svg.line(gap2, ORANGE, 3.2, dash="12 9")
A["gap2"] = P(165.5, 0, ZC + 16.5)

# ---------------- ARG-01 reducer ----------------
axial(svg, cam, 103, 163, 11.4, 11.4, 0, ZC, stops=BLUEMETAL, cap="#d4dde6", stroke="#4f5f70")
grooves(svg, cam, (110, 156), 11.4, 0, ZC, color="#4f5f70", sw=1.6, opacity=0.6)
A["arg"] = P(133, 0, ZC + 11.4)

# connection gap marker 1 (IH-300 / ARG-01)
axial(svg, cam, 98, 103, 13.0, 13.0, 0, ZC, stops=[(0, "#FFE2BF"), (1, "#FFC98A")], cap="#FFE7C9",
      stroke=ORANGE, sw=2.2, opacity=0.55)
gap1 = ring_pts(cam, "x", (100.5, 0, ZC), 16.0)
svg.line(gap1, ORANGE, 3.2, dash="12 9")
A["gap1"] = P(100.5, 0, ZC + 16)

# ---------------- holder bands (translucent, drawn over the cylinders) ----------------
for (hx0, hx1, rr) in ((118, 148, 11.4), (205, 240, 12.0)):
    axial(svg, cam, hx0, hx1, rr + 3.0, rr + 3.0, 0, ZC, stops=[(0, "#d6e4f3"), (0.5, "#b4cbe6"), (1, "#8fb0d8")],
          cap="#c5d7ee", stroke=HOLD_ST, sw=2.0, opacity=0.55)
    band = ring_pts(cam, "x", (hx0, 0, ZC), rr + 3.0)
    svg.line(band, HOLD_ST, 2.0, dash="10 7")
A["holder"] = P(225, 16, 22)
A["holder2"] = P(133, -16, 22)

# ---------------- IH-300 attachment ----------------
axial(svg, cam, 92, 98, 8.6, 8.6, 0, ZC, stops=METAL, cap="#cfd6dc")
axial(svg, cam, 14, 92, 9.6, 9.6, 0, ZC, stops=METAL, cap="#dfe5ea")
grooves(svg, cam, [24 + 3.2 * i for i in range(7)], 9.6, 0, ZC, color="#59636d", sw=1.3, opacity=0.55)
axial(svg, cam, 0, 14, 4.2, 7.8, 0, ZC, stops=METAL, cap="#c3ccd4")
# collet nose ring
axial(svg, cam, -1.5, 0.5, 3.0, 3.6, 0, ZC, stops=DARK, cap="#3b434b", stroke="#15191d", sw=1.0)
A["ih300"] = P(60, 0, ZC + 9.6)
# lever (schematic)
lv_y = 0.0
box(svg, cam, 34, -2.6, ZC + 9.4, 44, 5.2, 3.2, top="#3a424b", front="#2a3037", side="#20262c", stroke="#14181c", sw=1.0)
pivot = axial(svg, cam, 76, 80, 3.4, 3.4, 0, ZC + 10.5, stops=DARK, cap="#3a424b", stroke="#14181c", sw=1.0)
A["lever"] = P(48, 0, ZC + 12.6)

# ---------------- workpiece (dental diamond tool) ----------------
axial(svg, cam, -14, -1.5, 1.175, 1.175, 0, ZC, stops=METAL, cap="#e6ebef", stroke="#6c7680", sw=0.8)
axial(svg, cam, -16.5, -14, 0.9, 1.175, 0, ZC, stops=METAL, cap="#e6ebef", stroke="#6c7680", sw=0.8)
axial(svg, cam, -24.5, -16.5, 1.05, 1.05, 0, ZC, stops=GOLD, cap="#d6bd6c", stroke="#7c6220", sw=0.8)
A["work_tip"] = P(-20.5, 0, ZC)
A["work_shank"] = P(-8, 0, ZC)

# rotation arrow around the shank
marker = arrow_marker(svg, BLUE, 26)
arc = ring_pts(cam, "x", (-7.0, 0, ZC), 6.2, n=60, t0=math.radians(200), t1=math.radians(470))
svg.line(arc, BLUE, 4.0, extra=f'marker-end="{marker}"')
A["rotation"] = P(-7, 0, ZC + 6.2)

# ---------------- laser head nose (①) and beam ----------------
tip_top = P(-20.5, 0, ZC + 1.05)
lens_bot_z = 150
axial_z(svg, cam, lens_bot_z, 180, 12, 12, -20.5, 0, stops=[(0, "#4b545e"), (0.25, "#8d97a2"), (0.45, "#c3cbd3"), (0.7, "#6b7580"), (1, "#3d454e")], cap="#7a848f", stroke="#2b3138")
axial_z(svg, cam, lens_bot_z - 4, lens_bot_z, 8, 10.5, -20.5, 0, stops=DARK, cap="#3a414a", stroke="#15191d")
beam_top = P(-20.5, 0, lens_bot_z - 4)
glow = svg.blur(6)
svg.add(f'<path d="M {beam_top[0]:.1f} {beam_top[1]:.1f} L {tip_top[0]:.1f} {tip_top[1]:.1f}" stroke="{RED}" '
        f'stroke-width="12" opacity="0.35" filter="{glow}"/>')
svg.line([beam_top, tip_top], RED, 4.2)
svg.circle(tip_top, 9, RED, extra=f'opacity="0.55" filter="{svg.blur(4)}"')
A["head"] = P(-20.5, 0, 165)
A["beam"] = ((beam_top[0] + tip_top[0]) / 2, (beam_top[1] + tip_top[1]) / 2)

# ---------------- motor cord (electric) and signal line ----------------
mr = A["motor_rear"]
cp = A["e2280_conn"]
cord = bezier(mr, (mr[0] + 160, mr[1] + 10), (cp[0] - 160, cp[1] + 140), cp, n=64)
svg.line(cord, "#1b1f24", 9.0)
svg.line(cord, "#4a525b", 3.0, opacity=0.8)
A["cord"] = cord[30]
sig_start = P(420, -20, 34)
sig = [sig_start, (W - 40, sig_start[1])]
svg.line(sig, BLUE, 4.0, dash="16 10", extra=f'marker-end="{arrow_marker(svg, BLUE, 26)}"')
A["signal"] = ((sig_start[0] + W - 40) / 2, sig_start[1])

# ---------------- magnified inset (2D side view, schematic) ----------------
C = (330.0, 420.0)
R = 270.0
clip = svg.gid("clip")
svg.defs.append(f'<clipPath id="{clip}"><circle cx="{C[0]}" cy="{C[1]}" r="{R}"/></clipPath>')
tip = A["work_tip"]
# leader cone from inset to the real tip
ang = math.atan2(tip[1] - C[1], tip[0] - C[0])
for s in (-1, 1):
    a2 = ang + s * 0.42
    svg.line([(C[0] + R * math.cos(a2), C[1] + R * math.sin(a2)), (tip[0] + 30 * math.cos(ang + s * 1.9), tip[1] + 30 * math.sin(ang + s * 1.9))],
             "#8aa2bf", 2.0, dash="8 6")
svg.circle(tip, 30, "none", "#8aa2bf", 2.4)
svg.circle(C, R + 6, "#ffffff", "none", extra='opacity="0.9"')
g = [f'<g clip-path="url(#{clip})">']
g.append(f'<rect x="{C[0]-R}" y="{C[1]-R}" width="{2*R}" height="{2*R}" fill="#F7FAFD"/>')
k = 22.0  # px per mm in the inset
cy = C[1] + 30
x_hd = C[0] - 232          # head tip (left)
x_nk = x_hd + 8.0 * k       # head / neck boundary
x_sh0 = x_nk + 2.0 * k      # neck / shank boundary
x_collet = x_sh0 + 7.0 * k  # collet nose face
sh_r, hd_r = 1.175 * k, 1.05 * k
# collet nose (cut, schematic)
g.append(f'<path d="M {x_collet} {cy-3.6*k} L {x_collet+300} {cy-8.4*k} L {x_collet+300} {cy+8.4*k} L {x_collet} {cy+3.6*k} Z" '
         f'fill="#c9d1d8" stroke="#56606a" stroke-width="2"/>')
grad_sh = svg.lin_grad((0, cy - sh_r), (0, cy + sh_r), METAL)
g.append(f'<rect x="{x_sh0}" y="{cy-sh_r}" width="{x_collet + 9*k - x_sh0}" height="{2*sh_r}" fill="{grad_sh}" stroke="#6c7680" stroke-width="1.5"/>')
# collet jaws over the shank inside the nose
g.append(f'<path d="M {x_collet} {cy-2.9*k} L {x_collet+300} {cy-2.9*k} L {x_collet+300} {cy-sh_r} L {x_collet} {cy-sh_r} Z" fill="#8f9aa4" opacity="0.95"/>')
g.append(f'<path d="M {x_collet} {cy+sh_r} L {x_collet+300} {cy+sh_r} L {x_collet+300} {cy+2.9*k} L {x_collet} {cy+2.9*k} Z" fill="#8f9aa4" opacity="0.95"/>')
g.append(f'<rect x="{x_collet-3}" y="{cy-2.9*k}" width="6" height="{5.8*k}" fill="#3b434b"/>')
# neck
g.append(f'<path d="M {x_sh0} {cy-sh_r} L {x_nk} {cy-0.85*k} L {x_nk} {cy+0.85*k} L {x_sh0} {cy+sh_r} Z" fill="{grad_sh}" stroke="#6c7680" stroke-width="1.5"/>')
# diamond head
grad_hd = svg.lin_grad((0, cy - hd_r), (0, cy + hd_r), GOLD)
g.append(f'<rect x="{x_hd}" y="{cy-hd_r}" width="{x_nk-x_hd}" height="{2*hd_r}" rx="{0.45*k}" fill="{grad_hd}" stroke="#7c6220" stroke-width="1.5"/>')
rnd = random.Random(3)
for _ in range(150):
    px = x_hd + rnd.uniform(5, x_nk - x_hd - 5)
    py = cy + rnd.uniform(-hd_r + 3, hd_r - 3)
    g.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{rnd.uniform(1.2, 2.6):.1f}" fill="#fff6d6" opacity="{rnd.uniform(0.35, 0.8):.2f}"/>')
# graduation lines (0.5 mm wide): one finished, one being marked
xm_done, xb = x_nk - 2.0 * k, x_nk - 5.0 * k
g.append(f'<rect x="{xm_done-0.25*k}" y="{cy-hd_r}" width="{0.5*k}" height="{2*hd_r}" fill="#2b2f33" opacity="0.85"/>')
g.append(f'<rect x="{xb-0.25*k}" y="{cy-hd_r}" width="{0.5*k}" height="{2*hd_r}" fill="#2b2f33" opacity="0.4"/>')
g.append(f'<path d="M {xb} {C[1]-R} L {xb} {cy-hd_r}" stroke="{RED}" stroke-width="16" opacity="0.28"/>')
g.append(f'<path d="M {xb} {C[1]-R} L {xb} {cy-hd_r}" stroke="{RED}" stroke-width="4.5"/>')
g.append(f'<circle cx="{xb}" cy="{cy-hd_r}" r="10" fill="{RED}" opacity="0.6"/>')
# rotation arrow around the head (front arc)
rot_m = arrow_marker(svg, BLUE, 22)
ax0 = x_hd + 1.8 * k
g.append(f'<path d="M {ax0+14} {cy-hd_r-26} C {ax0-40} {cy-hd_r-26}, {ax0-40} {cy+hd_r+28}, {ax0+10} {cy+hd_r+28}" fill="none" stroke="{BLUE}" stroke-width="3.6" marker-end="{rot_m}"/>')
g.append("</g>")
svg.add("".join(g))
svg.circle(C, R, "none", NAVY, 4.0)
A["inset_shank"] = (x_sh0 + 0.5 * (x_collet - x_sh0), cy + sh_r)
A["inset_head"] = (x_hd + 0.5 * (x_nk - x_hd), cy + hd_r)
A["inset_beam"] = (xb, C[1] - R + 80)
A["inset_mark"] = (xm_done, cy - hd_r)
A["inset_center"] = C
A["inset_r"] = R

open(sys.argv[1] if len(sys.argv) > 1 else "fig2.svg", "w").write(svg.svg())
json.dump({k: [round(v[0], 1), round(v[1], 1)] if isinstance(v, tuple) else v for k, v in A.items() if k != "cord"} | {"cord": [round(A["cord"][0], 1), round(A["cord"][1], 1)]},
          open("fig2_anchors.json", "w"), ensure_ascii=False, indent=1)
print("ok")
