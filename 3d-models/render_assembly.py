#!/usr/bin/env python3
"""Cat Feeder 5000 — Assembly Renderer (matplotlib)

Generates 4 views: front, side, top, and isometric corner.
All dimensions match params.scad. Run: python3 render_assembly.py
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.colors as mcolors

# ── Dimensions (from params.scad) ──────────────────────────────────────────────
UNIT_W, UNIT_D, UNIT_H = 160, 240, 160
WALL, FLOOR_T = 3, 4
APPROACH_W, APPROACH_H = 130, 130
GATE_W, GATE_H, GATE_T = 118, 90, 3
GATE_SETBACK = 40
HALO_CLEAR_W = 130
HALO_TUBE_OD = 16
HALO_LEG_H = 77
HALO_TILT = 18  # degrees
HALO_TOTAL_W = HALO_CLEAR_W + HALO_TUBE_OD  # 146
HOPPER_W, HOPPER_D, HOPPER_H = 130, 130, 130
AUGER_TUBE_OD = 38
BOWL_FLOOR_W, BOWL_FLOOR_D = 100, 90
BOWL_OVERHANG = 15
BOWL_SIDE_H, BOWL_BACK_H = 25, 30
BOWL_FLOOR_T = 3

# ── Colors ─────────────────────────────────────────────────────────────────────
COL_BODY = (0.65, 0.65, 0.65, 0.55)
COL_BODY_EDGE = (0.4, 0.4, 0.4, 0.7)
COL_RFID = (0.85, 0.2, 0.2, 0.85)
COL_RFID_EDGE = (0.6, 0.1, 0.1, 0.9)
COL_GATE = (0.2, 0.5, 0.85, 0.85)
COL_GATE_EDGE = (0.1, 0.3, 0.6, 0.9)
COL_FOOD = (0.92, 0.75, 0.35, 0.7)
COL_FOOD_EDGE = (0.7, 0.5, 0.15, 0.9)
COL_TPU = (0.4, 0.72, 0.3, 0.8)
COL_TPU_EDGE = (0.25, 0.5, 0.15, 0.9)


def box_faces(x0, y0, z0, w, d, h):
    """Return 6 faces of a box as vertex lists."""
    x1, y1, z1 = x0 + w, y0 + d, z0 + h
    return [
        [(x0,y0,z0),(x1,y0,z0),(x1,y1,z0),(x0,y1,z0)],  # bottom
        [(x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)],  # top
        [(x0,y0,z0),(x1,y0,z0),(x1,y0,z1),(x0,y0,z1)],  # front
        [(x0,y1,z0),(x1,y1,z0),(x1,y1,z1),(x0,y1,z1)],  # back
        [(x0,y0,z0),(x0,y1,z0),(x0,y1,z1),(x0,y0,z1)],  # left
        [(x1,y0,z0),(x1,y1,z0),(x1,y1,z1),(x1,y0,z1)],  # right
    ]


def tube_faces(p0, p1, radius, n=12):
    """Return faces for a tube/cylinder between two 3D points."""
    p0, p1 = np.array(p0), np.array(p1)
    axis = p1 - p0
    length = np.linalg.norm(axis)
    if length < 1e-6:
        return []
    axis_n = axis / length

    # Find perpendicular vectors
    if abs(axis_n[2]) < 0.9:
        perp1 = np.cross(axis_n, [0, 0, 1])
    else:
        perp1 = np.cross(axis_n, [1, 0, 0])
    perp1 /= np.linalg.norm(perp1)
    perp2 = np.cross(axis_n, perp1)

    angles = np.linspace(0, 2*np.pi, n+1)
    faces = []
    for i in range(n):
        a0, a1 = angles[i], angles[i+1]
        c0 = p0 + radius*(np.cos(a0)*perp1 + np.sin(a0)*perp2)
        c1 = p0 + radius*(np.cos(a1)*perp1 + np.sin(a1)*perp2)
        c2 = p1 + radius*(np.cos(a1)*perp1 + np.sin(a1)*perp2)
        c3 = p1 + radius*(np.cos(a0)*perp1 + np.sin(a0)*perp2)
        faces.append([tuple(c0), tuple(c1), tuple(c2), tuple(c3)])
    return faces


def arc_tube_faces(center, radius_arc, radius_tube, start_angle, end_angle,
                   n_arc=24, n_tube=8, axis='z', tilt_deg=0):
    """Return faces for a tube swept along an arc."""
    angles = np.linspace(start_angle, end_angle, n_arc+1)
    faces = []
    cx, cy, cz = center

    def arc_point(a):
        # Arc in XZ plane (front view), then optionally tilt
        x = cx + radius_arc * np.cos(a)
        z = cz + radius_arc * np.sin(a)
        y = cy
        return np.array([x, y, z])

    def tangent(a):
        tx = -np.sin(a)
        tz = np.cos(a)
        return np.array([tx, 0, tz])

    tube_angles = np.linspace(0, 2*np.pi, n_tube+1)

    for i in range(n_arc):
        a0, a1 = angles[i], angles[i+1]
        p0 = arc_point(a0)
        p1 = arc_point(a1)
        t0 = tangent(a0)
        t1 = tangent(a1)

        # Perpendiculars for tube cross-section
        up = np.array([0, 1, 0])
        n0_1 = np.cross(t0, up); n0_1 /= np.linalg.norm(n0_1)
        n0_2 = np.cross(t0, n0_1); n0_2 /= np.linalg.norm(n0_2)
        n1_1 = np.cross(t1, up); n1_1 /= np.linalg.norm(n1_1)
        n1_2 = np.cross(t1, n1_1); n1_2 /= np.linalg.norm(n1_2)

        for j in range(n_tube):
            ta0, ta1 = tube_angles[j], tube_angles[j+1]
            v0 = p0 + radius_tube*(np.cos(ta0)*n0_1 + np.sin(ta0)*n0_2)
            v1 = p0 + radius_tube*(np.cos(ta1)*n0_1 + np.sin(ta1)*n0_2)
            v2 = p1 + radius_tube*(np.cos(ta1)*n1_1 + np.sin(ta1)*n1_2)
            v3 = p1 + radius_tube*(np.cos(ta0)*n1_1 + np.sin(ta0)*n1_2)
            faces.append([tuple(v0), tuple(v1), tuple(v2), tuple(v3)])
    return faces


def frustum_faces(x0, y0, z0, w_bot, d_bot, w_top, d_top, h, n_side=1):
    """Return faces for a frustum (tapered box)."""
    # Bottom corners
    bx0, by0 = x0, y0
    bx1, by1 = x0 + w_bot, y0 + d_bot
    # Top corners (centered)
    tx0 = x0 + (w_bot - w_top)/2
    ty0 = y0 + (d_bot - d_top)/2
    tx1 = tx0 + w_top
    ty1 = ty0 + d_top
    z1 = z0 + h

    faces = [
        [(bx0,by0,z0),(bx1,by0,z0),(bx1,by1,z0),(bx0,by1,z0)],  # bottom
        [(tx0,ty0,z1),(tx1,ty0,z1),(tx1,ty1,z1),(tx0,ty1,z1)],  # top
        [(bx0,by0,z0),(bx1,by0,z0),(tx1,ty0,z1),(tx0,ty0,z1)],  # front
        [(bx0,by1,z0),(bx1,by1,z0),(tx1,ty1,z1),(tx0,ty1,z1)],  # back
        [(bx0,by0,z0),(bx0,by1,z0),(tx0,ty1,z1),(tx0,ty0,z1)],  # left
        [(bx1,by0,z0),(bx1,by1,z0),(tx1,ty1,z1),(tx1,ty0,z1)],  # right
    ]
    return faces


def add_part(ax, faces, facecolor, edgecolor, linewidth=0.3):
    """Add a Poly3DCollection to an axes."""
    pc = Poly3DCollection(faces, facecolors=facecolor, edgecolors=edgecolor,
                          linewidths=linewidth, zsort='average')
    ax.add_collection3d(pc)


def build_halo():
    """Build the round halo antenna arch geometry."""
    # Assembly position: translate([(160-154)/2, -HALO_TUBE_OD/2, 0])
    # But HALO_TOTAL_W in the SCAD is 146 (130+16), params.scad says 24 OD but
    # the part file uses 16. The assembly uses 154 for centering calc.
    # Let's match the actual part: 16mm OD, 130mm clear.
    r_tube = HALO_TUBE_OD / 2  # 8mm
    r_arc = HALO_CLEAR_W / 2   # 65mm (center-to-center)

    # Halo origin in assembly coords
    halo_ox = (UNIT_W - HALO_TOTAL_W) / 2  # centering
    halo_oy = -HALO_TUBE_OD / 2
    halo_oz = 0

    tilt_rad = np.radians(HALO_TILT)

    all_faces = []

    # Build in local coords then transform
    # Left leg: from (r_tube, 0, 0) up to (r_tube, 0, HALO_LEG_H)
    # Right leg: from (HALO_TOTAL_W - r_tube, 0, 0) up to same height

    def tilt_point(x, y, z):
        """Tilt around X axis at Z=0, then translate to assembly position."""
        # Rotate around X: y' = y*cos - z*sin, z' = y*sin + z*cos
        yr = y * np.cos(-tilt_rad) - z * np.sin(-tilt_rad)
        zr = y * np.sin(-tilt_rad) + z * np.cos(-tilt_rad)
        return (x + halo_ox, yr + halo_oy, zr + halo_oz)

    def tilt_faces(faces):
        return [
            [tilt_point(*v) for v in face]
            for face in faces
        ]

    # Left leg
    left_leg = tube_faces(
        (r_tube, 0, 0),
        (r_tube, 0, HALO_LEG_H),
        r_tube, n=10
    )
    all_faces.extend(tilt_faces(left_leg))

    # Right leg
    right_leg = tube_faces(
        (HALO_TOTAL_W - r_tube, 0, 0),
        (HALO_TOTAL_W - r_tube, 0, HALO_LEG_H),
        r_tube, n=10
    )
    all_faces.extend(tilt_faces(right_leg))

    # Semicircular arch at top of legs
    # Arc center is at (HALO_TOTAL_W/2, 0, HALO_LEG_H)
    # Arc radius = r_arc = 65mm, sweeps from 0 to pi in XZ plane
    arch_center = np.array([HALO_TOTAL_W/2, 0, HALO_LEG_H])
    arch_faces = arc_tube_faces(
        arch_center, r_arc, r_tube,
        start_angle=0, end_angle=np.pi,
        n_arc=20, n_tube=8
    )
    all_faces.extend(tilt_faces(arch_faces))

    # Feet (simplified as flat boxes)
    foot_w, foot_d, foot_h = 30, 30, 5
    for leg_x in [r_tube, HALO_TOTAL_W - r_tube]:
        fx = leg_x - foot_w/2 + halo_ox
        fy = -foot_d + r_tube + halo_oy
        fz = 0
        all_faces.extend(box_faces(fx, fy, fz, foot_w, foot_d, foot_h))

    return all_faces


def build_assembly(ax):
    """Build all parts and add them to the axes."""

    # ── Main body (semi-transparent to show interior) ──────────────────────
    # Outer shell
    body_faces = box_faces(0, 0, 0, UNIT_W, UNIT_D, UNIT_H)
    add_part(ax, body_faces, COL_BODY, COL_BODY_EDGE, linewidth=0.5)

    # Approach opening (dark rectangle on front face to show the cutout)
    opening_x = (UNIT_W - APPROACH_W) / 2
    opening_faces = [
        [(opening_x, -0.5, 0), (opening_x + APPROACH_W, -0.5, 0),
         (opening_x + APPROACH_W, -0.5, APPROACH_H), (opening_x, -0.5, APPROACH_H)]
    ]
    add_part(ax, opening_faces, (0.15, 0.15, 0.2, 0.6), (0.1, 0.1, 0.1, 0.8), linewidth=0.8)

    # ── Round halo antenna arch ────────────────────────────────────────────
    halo_faces = build_halo()
    add_part(ax, halo_faces, COL_RFID, COL_RFID_EDGE, linewidth=0.2)

    # ── Hopper (on top of body) ────────────────────────────────────────────
    hop_x, hop_y, hop_z = 15, 80, UNIT_H
    hopper_faces = frustum_faces(
        hop_x, hop_y, hop_z,
        HOPPER_W, HOPPER_D,       # bottom (sits on body)
        AUGER_TUBE_OD + 10, AUGER_TUBE_OD + 10,  # top outlet
        -HOPPER_H                   # negative = tapers downward...
    )
    # Actually: hopper tapers from wide top to narrow bottom outlet
    hopper_faces = frustum_faces(
        hop_x, hop_y, hop_z,
        HOPPER_W, HOPPER_D,         # bottom face (wide, sits on body top)
        HOPPER_W, HOPPER_D,         # same width at bottom
        HOPPER_H                     # goes up
    )
    # The hopper is a funnel: wide at top, narrow outlet at bottom
    # In assembly: bottom at Z=UNIT_H, opens upward. Wide at top.
    # Let me do it properly: narrow at Z=UNIT_H, wide at Z=UNIT_H+HOPPER_H
    outlet_size = AUGER_TUBE_OD + 10  # ~48mm
    hopper_faces = frustum_faces(
        hop_x, hop_y, hop_z,
        HOPPER_W, HOPPER_D,
        HOPPER_W, HOPPER_D,
        HOPPER_H
    )
    # Simplify: just show it as a tapered box
    # Bottom (outlet) centered on the wide footprint
    hopper_faces = []
    bx0, by0 = hop_x, hop_y
    bw, bd = HOPPER_W, HOPPER_D
    tw, td = HOPPER_W, HOPPER_D
    # Outlet at bottom center
    ox = hop_x + HOPPER_W/2 - outlet_size/2
    oy = hop_y + HOPPER_D/2 - outlet_size/2
    z_bot = hop_z
    z_top = hop_z + HOPPER_H

    # Build as frustum: narrow bottom, wide top
    hopper_faces = frustum_faces(
        ox, oy, z_bot,
        outlet_size, outlet_size,
        HOPPER_W, HOPPER_D,
        HOPPER_H
    )
    # Lid on top
    hopper_faces.extend(box_faces(hop_x - 3, hop_y - 3, z_top, HOPPER_W + 6, HOPPER_D + 6, 3))
    add_part(ax, hopper_faces, COL_FOOD, COL_FOOD_EDGE, linewidth=0.3)

    # ── Gate flap ──────────────────────────────────────────────────────────
    gate_x = (UNIT_W - GATE_W) / 2
    gate_faces = box_faces(gate_x, GATE_SETBACK, FLOOR_T, GATE_W, GATE_T, GATE_H)
    add_part(ax, gate_faces, COL_GATE, COL_GATE_EDGE, linewidth=0.4)

    # ── Bowl ───────────────────────────────────────────────────────────────
    bowl_x = (UNIT_W - BOWL_FLOOR_W) / 2
    bowl_y = GATE_SETBACK + 15
    bowl_z = FLOOR_T
    bowl_total_d = BOWL_FLOOR_D + BOWL_OVERHANG

    # Bowl floor
    bowl_faces = box_faces(bowl_x, bowl_y, bowl_z, BOWL_FLOOR_W, bowl_total_d, BOWL_FLOOR_T)
    # Bowl back wall
    bowl_faces.extend(box_faces(bowl_x, bowl_y + BOWL_OVERHANG, bowl_z + BOWL_FLOOR_T,
                                 BOWL_FLOOR_W, 2.5, BOWL_BACK_H))
    # Bowl left wall
    bowl_faces.extend(box_faces(bowl_x, bowl_y, bowl_z + BOWL_FLOOR_T,
                                 2.5, bowl_total_d, BOWL_SIDE_H))
    # Bowl right wall
    bowl_faces.extend(box_faces(bowl_x + BOWL_FLOOR_W - 2.5, bowl_y, bowl_z + BOWL_FLOOR_T,
                                 2.5, bowl_total_d, BOWL_SIDE_H))
    add_part(ax, bowl_faces, COL_FOOD, COL_FOOD_EDGE, linewidth=0.3)

    # ── Feet (4 corners) ──────────────────────────────────────────────────
    foot_d = 12
    foot_h = 4
    for x in [15, UNIT_W - 15]:
        for y in [15, UNIT_D - 15]:
            foot_faces = []
            # Simple cylinder approximation as octagonal prism
            n = 10
            angles = np.linspace(0, 2*np.pi, n+1)
            r = 6
            for i in range(n):
                a0, a1 = angles[i], angles[i+1]
                v0 = (x + r*np.cos(a0), y + r*np.sin(a0), -foot_h)
                v1 = (x + r*np.cos(a1), y + r*np.sin(a1), -foot_h)
                v2 = (x + r*np.cos(a1), y + r*np.sin(a1), 0)
                v3 = (x + r*np.cos(a0), y + r*np.sin(a0), 0)
                foot_faces.append([v0, v1, v2, v3])
            add_part(ax, foot_faces, COL_TPU, COL_TPU_EDGE, linewidth=0.2)


def setup_axes(ax, title=""):
    """Configure axes appearance."""
    ax.set_xlabel('X (width) mm', fontsize=7, labelpad=2)
    ax.set_ylabel('Y (depth) mm', fontsize=7, labelpad=2)
    ax.set_zlabel('Z (height) mm', fontsize=7, labelpad=2)
    ax.set_title(title, fontsize=10, fontweight='bold', pad=8)
    ax.tick_params(labelsize=6)

    # Equal aspect ratio
    ax.set_xlim(-40, 200)
    ax.set_ylim(-50, 260)
    ax.set_zlim(-20, 310)

    # Make axes equal
    ax.set_box_aspect([240, 310, 330])
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    ax.xaxis.pane.set_edgecolor('lightgray')
    ax.yaxis.pane.set_edgecolor('lightgray')
    ax.zaxis.pane.set_edgecolor('lightgray')
    ax.grid(True, alpha=0.2)


# ── Views ──────────────────────────────────────────────────────────────────────
VIEWS = {
    'front':  {'elev': 5,  'azim': -90, 'title': 'Front View (Cat Approach Side)'},
    'side':   {'elev': 5,  'azim': 0,   'title': 'Right Side View'},
    'top':    {'elev': 89, 'azim': -90, 'title': 'Top View'},
    'corner': {'elev': 25, 'azim': -55, 'title': 'Isometric (Corner View)'},
}


def render_single(view_name, save=True):
    """Render a single view."""
    v = VIEWS[view_name]
    fig = plt.figure(figsize=(10, 8), dpi=150)
    ax = fig.add_subplot(111, projection='3d')
    build_assembly(ax)
    setup_axes(ax, v['title'])
    ax.view_init(elev=v['elev'], azim=v['azim'])
    fig.suptitle('Cat Feeder 5000 — Assembly', fontsize=12, y=0.98,
                 fontstyle='italic', color='gray')
    plt.tight_layout()
    if save:
        path = f'3d-models/renders/assembly_{view_name}.png'
        fig.savefig(path, dpi=150, bbox_inches='tight',
                    facecolor='white', edgecolor='none')
        print(f'  Saved: {path}')
    plt.close(fig)


def render_all():
    """Render all 4 views as individual files + one combined 2x2 sheet."""
    import os
    os.makedirs('3d-models/renders', exist_ok=True)

    # Individual views
    for name in VIEWS:
        render_single(name)

    # Combined 2×2 sheet
    fig = plt.figure(figsize=(18, 14), dpi=150)
    fig.suptitle('Cat Feeder 5000 — Assembly Views', fontsize=16,
                 fontweight='bold', y=0.98)

    layout = [('front', 1), ('side', 2), ('top', 3), ('corner', 4)]
    for name, pos in layout:
        v = VIEWS[name]
        ax = fig.add_subplot(2, 2, pos, projection='3d')
        build_assembly(ax)
        setup_axes(ax, v['title'])
        ax.view_init(elev=v['elev'], azim=v['azim'])

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    path = '3d-models/renders/assembly_all_views.png'
    fig.savefig(path, dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    print(f'  Saved: {path}')
    plt.close(fig)


# ── Legend helper ──────────────────────────────────────────────────────────────
def add_legend(ax):
    """Add a color legend for part groups."""
    from matplotlib.patches import Patch
    legend_items = [
        Patch(facecolor=COL_BODY[:3], edgecolor=COL_BODY_EDGE[:3], label='Body / Structure'),
        Patch(facecolor=COL_RFID[:3], edgecolor=COL_RFID_EDGE[:3], label='RFID Halo Antenna'),
        Patch(facecolor=COL_GATE[:3], edgecolor=COL_GATE_EDGE[:3], label='Gate Mechanism'),
        Patch(facecolor=COL_FOOD[:3], edgecolor=COL_FOOD_EDGE[:3], label='Hopper / Bowl (Food)'),
        Patch(facecolor=COL_TPU[:3], edgecolor=COL_TPU_EDGE[:3], label='TPU Feet'),
    ]
    ax.legend(handles=legend_items, loc='upper left', fontsize=7, framealpha=0.8)


if __name__ == '__main__':
    print('Rendering Cat Feeder 5000 assembly views...')
    render_all()
    print('Done!')
