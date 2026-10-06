"""Minimal axonometric drawing helpers that emit SVG (schematic concept figures).

World axes: x = rotary-unit axis (toward the back-right), y = depth (toward the back),
z = up. The camera looks from the front-left-above, so faces -x, -y and +z are visible.
"""
import math


def _norm(v):
    n = math.sqrt(sum(c * c for c in v))
    return tuple(c / n for c in v)


def _cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def _dot(a, b):
    return sum(x * y for x, y in zip(a, b))


class Cam:
    def __init__(self, a=1.0, b=1.7, c=1.05, scale=1.0, ox=0.0, oy=0.0):
        f = _norm((a, b, -c))
        r = _norm(_cross(f, (0, 0, 1)))
        u = _cross(r, f)
        self.f, self.r, self.u = f, r, u
        self.s, self.ox, self.oy = scale, ox, oy

    def v(self, x, y, z):
        p = (x, y, z)
        return (self.s * _dot(self.r, p), -self.s * _dot(self.u, p))

    def p(self, x, y, z):
        vx, vy = self.v(x, y, z)
        return (self.ox + vx, self.oy + vy)


def fmt(pts):
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)


def path_d(pts, close=True):
    d = "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in pts)
    return d + (" Z" if close else "")


def convex_hull(points):
    pts = sorted(set((round(x, 2), round(y, 2)) for x, y in points))
    if len(pts) <= 2:
        return pts

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    lower = []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    upper = []
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


class Svg:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.defs = []
        self.body = []
        self._gid = 0

    def gid(self, prefix="g"):
        self._gid += 1
        return f"{prefix}{self._gid}"

    def lin_grad(self, p1, p2, stops):
        gid = self.gid("lg")
        parts = []
        for s in stops:
            o, c = s[0], s[1]
            a = s[2] if len(s) > 2 else None
            op = f' stop-opacity="{a}"' if a is not None else ""
            parts.append(f'<stop offset="{o}" stop-color="{c}"{op}/>')
        st = "".join(parts)
        self.defs.append(
            f'<linearGradient id="{gid}" gradientUnits="userSpaceOnUse" x1="{p1[0]:.1f}" y1="{p1[1]:.1f}" '
            f'x2="{p2[0]:.1f}" y2="{p2[1]:.1f}">{st}</linearGradient>'
        )
        return f"url(#{gid})"

    def rad_grad(self, c, r, stops):
        gid = self.gid("rg")
        st = "".join(f'<stop offset="{o}" stop-color="{col}"/>' for o, col in stops)
        self.defs.append(
            f'<radialGradient id="{gid}" gradientUnits="userSpaceOnUse" cx="{c[0]:.1f}" cy="{c[1]:.1f}" r="{r:.1f}">{st}</radialGradient>'
        )
        return f"url(#{gid})"

    def blur(self, sd):
        gid = self.gid("bl")
        self.defs.append(
            f'<filter id="{gid}" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="{sd}"/></filter>'
        )
        return f"url(#{gid})"

    def add(self, s):
        self.body.append(s)

    def poly(self, pts, fill, stroke="none", sw=1.0, opacity=None, dash=None, extra=""):
        o = f' opacity="{opacity}"' if opacity is not None else ""
        da = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(
            f'<path d="{path_d(pts)}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" '
            f'stroke-linejoin="round"{da}{o} {extra}/>'
        )

    def line(self, pts, stroke, sw=2.0, dash=None, opacity=None, cap="round", extra=""):
        o = f' opacity="{opacity}"' if opacity is not None else ""
        da = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(
            f'<path d="{path_d(pts, close=False)}" fill="none" stroke="{stroke}" stroke-width="{sw}" '
            f'stroke-linecap="{cap}" stroke-linejoin="round"{da}{o} {extra}/>'
        )

    def raw_path(self, d, fill="none", stroke="none", sw=1.0, extra=""):
        self.add(f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>')

    def circle(self, c, r, fill, stroke="none", sw=1.0, extra=""):
        self.add(f'<circle cx="{c[0]:.1f}" cy="{c[1]:.1f}" r="{r:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>')

    def text(self, xy, s, size, fill="#1F3A5F", weight="normal", anchor="start", extra=""):
        self.add(
            f'<text x="{xy[0]:.1f}" y="{xy[1]:.1f}" font-family="BIZ UDPGothic" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" {extra}>{s}</text>'
        )

    def svg(self, bg="#FFFFFF"):
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" '
            f'viewBox="0 0 {self.w} {self.h}">'
            f'<defs>{"".join(self.defs)}</defs>'
            f'<rect width="{self.w}" height="{self.h}" fill="{bg}"/>' + "".join(self.body) + "</svg>"
        )


# ---------- solids ----------

def ring_pts(cam, axis, c, r, n=144, t0=0.0, t1=2 * math.pi):
    if axis == "x":
        U, V = (0, 1, 0), (0, 0, 1)
    elif axis == "y":
        U, V = (1, 0, 0), (0, 0, 1)
    else:
        U, V = (1, 0, 0), (0, 1, 0)
    out = []
    for i in range(n + 1):
        t = t0 + (t1 - t0) * i / n
        ct, stt = math.cos(t), math.sin(t)
        out.append(cam.p(c[0] + r * (ct * U[0] + stt * V[0]),
                         c[1] + r * (ct * U[1] + stt * V[1]),
                         c[2] + r * (ct * U[2] + stt * V[2])))
    return out


METAL = [(0, "#7d8893"), (0.10, "#c9d1d8"), (0.24, "#f6f8fa"), (0.34, "#dfe5ea"),
         (0.58, "#a9b3bc"), (0.84, "#6f7a85"), (1, "#8c98a3")]
DARK = [(0, "#2a2f36"), (0.10, "#59626d"), (0.22, "#9aa3ad"), (0.32, "#5b646e"),
        (0.60, "#30363d"), (0.88, "#1b1f24"), (1, "#3a414a")]
BLUEMETAL = [(0, "#6f8193"), (0.10, "#b9c8d6"), (0.24, "#eef3f8"), (0.34, "#cbd7e3"),
             (0.58, "#93a5b7"), (0.84, "#5f7184"), (1, "#7b8da0")]
GOLD = [(0, "#8a6d1f"), (0.12, "#d9bb63"), (0.26, "#fff0b8"), (0.36, "#e3c56f"),
        (0.62, "#b8922f"), (0.86, "#7d6018"), (1, "#9b7a25")]


def axial(svg, cam, x0, x1, r0, r1, yc=0.0, zc=0.0, stops=METAL, cap="#d7dde3",
          stroke="#56606a", sw=1.2, opacity=None, cap_visible=True):
    """Solid of revolution about the x axis from x0 (near) to x1 (far)."""
    e0 = ring_pts(cam, "x", (x0, yc, zc), r0)
    e1 = ring_pts(cam, "x", (x1, yc, zc), r1)
    hull = convex_hull(e0 + e1)
    dx, dy = cam.v(1, 0, 0)
    L = math.hypot(dx, dy)
    nx, ny = -dy / L, dx / L
    if ny > 0:
        nx, ny = -nx, -ny
    c0 = cam.p(x0, yc, zc)
    proj = [(px - c0[0]) * nx + (py - c0[1]) * ny for px, py in hull]
    hi, lo = max(proj), min(proj)
    g1 = (c0[0] + nx * hi, c0[1] + ny * hi)
    g2 = (c0[0] + nx * lo, c0[1] + ny * lo)
    fill = svg.lin_grad(g1, g2, stops)
    svg.poly(hull, fill, stroke, sw, opacity)
    if cap_visible:
        svg.poly(e0, cap, stroke, sw * 0.9, opacity)
    return hull


def grooves(svg, cam, xs, r, yc=0.0, zc=0.0, color="#4b5560", sw=1.4, opacity=0.65):
    """Visible half-ring lines (grip grooves / seams) on a cylinder."""
    for x in xs:
        pts = ring_pts(cam, "x", (x, yc, zc), r, n=72, t0=-0.5 * math.pi - 0.15, t1=0.5 * math.pi + 1.25)
        svg.line(pts, color, sw, opacity=opacity)


def box(svg, cam, x0, y0, z0, dx, dy, dz, top="#e9edf1", front="#c7cfd6", side="#aab4be",
        stroke="#5b6670", sw=1.2, opacity=None, dash=None, grad=True):
    P = lambda x, y, z: cam.p(x, y, z)
    x1, y1, z1 = x0 + dx, y0 + dy, z0 + dz
    topf = [P(x0, y0, z1), P(x1, y0, z1), P(x1, y1, z1), P(x0, y1, z1)]
    frontf = [P(x0, y0, z0), P(x1, y0, z0), P(x1, y0, z1), P(x0, y0, z1)]
    sidef = [P(x0, y0, z0), P(x0, y0, z1), P(x0, y1, z1), P(x0, y1, z0)]
    if grad:
        tf = svg.lin_grad(P(x0, y0, z1), P(x1, y1, z1), [(0, _shade(top, 1.04)), (1, _shade(top, 0.95))])
        ff = svg.lin_grad(P(x0, y0, z1), P(x1, y0, z0), [(0, _shade(front, 1.05)), (1, _shade(front, 0.92))])
        sf = svg.lin_grad(P(x0, y0, z1), P(x0, y1, z0), [(0, _shade(side, 1.03)), (1, _shade(side, 0.9))])
    else:
        tf, ff, sf = top, front, side
    for pts, fill in ((sidef, sf), (frontf, ff), (topf, tf)):
        svg.poly(pts, fill, stroke, sw, opacity, dash)
    return {"top": topf, "front": frontf, "side": sidef}


def _shade(hexcol, k):
    hexcol = hexcol.lstrip("#")
    r, g, b = (int(hexcol[i:i + 2], 16) for i in (0, 2, 4))
    f = lambda c: max(0, min(255, int(round(c * k))))
    return "#%02x%02x%02x" % (f(r), f(g), f(b))


def shadow(svg, cam, x0, y0, x1, y1, z, dx=10, dy=14, sd=14, opacity=0.28):
    pts = [cam.p(x0, y0, z), cam.p(x1, y0, z), cam.p(x1, y1, z), cam.p(x0, y1, z)]
    pts = [(x + dx, y + dy) for x, y in pts]
    svg.poly(pts, "#1b2633", opacity=opacity, extra=f'filter="{svg.blur(sd)}"')


def axial_z(svg, cam, z0, z1, r0, r1, xc=0.0, yc=0.0, stops=METAL, cap="#d7dde3",
            stroke="#56606a", sw=1.2, opacity=None):
    """Vertical solid of revolution from z0 (bottom) to z1 (top); the top cap is visible."""
    e0 = ring_pts(cam, "z", (xc, yc, z0), r0)
    e1 = ring_pts(cam, "z", (xc, yc, z1), r1)
    hull = convex_hull(e0 + e1)
    xs = [p[0] for p in hull]
    cy = cam.p(xc, yc, z1)[1]
    fill = svg.lin_grad((min(xs), cy), (max(xs), cy), stops)
    svg.poly(hull, fill, stroke, sw, opacity)
    svg.poly(e1, cap, stroke, sw * 0.9, opacity)
    return hull


def arrow_marker(svg, color, size=10):
    gid = svg.gid("ar")
    svg.defs.append(
        f'<marker id="{gid}" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="{size}" markerHeight="{size}" '
        f'markerUnits="userSpaceOnUse" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{color}"/></marker>'
    )
    return f"url(#{gid})"


def bezier(p0, p1, p2, p3, n=48):
    out = []
    for i in range(n + 1):
        t = i / n
        a, b, c, d = (1 - t) ** 3, 3 * (1 - t) ** 2 * t, 3 * (1 - t) * t ** 2, t ** 3
        out.append((a * p0[0] + b * p1[0] + c * p2[0] + d * p3[0], a * p0[1] + b * p1[1] + c * p2[1] + d * p3[1]))
    return out
