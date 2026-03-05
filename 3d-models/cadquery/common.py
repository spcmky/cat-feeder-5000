# Cat Feeder 5000 — Common CadQuery Modules
# Shared primitives used by multiple parts. Equivalent to the modules in params.scad.

import cadquery as cq
from params import INSERT_BORE, M3_CLEAR


def fillet_box(w: float, d: float, h: float, r: float = 2) -> cq.Workplane:
    """Rectangular box with filleted vertical edges.

    Origin at min corner (0,0,0) matching OpenSCAD convention.
    """
    r = min(r, w / 2 - 0.01, d / 2 - 0.01)
    return (
        cq.Workplane("XY")
        .box(w, d, h, centered=False)
        .edges("|Z")
        .fillet(r)
    )


def m3_insert(h: float = 8) -> cq.Workplane:
    """M3 heat-set insert pocket (cylinder). Origin at base center."""
    return cq.Workplane("XY").circle(INSERT_BORE / 2).extrude(h)


def m3_clear(h: float = 8) -> cq.Workplane:
    """M3 clearance hole (cylinder). Origin at base center."""
    return cq.Workplane("XY").circle(M3_CLEAR / 2).extrude(h)


def boss(d: float = 10, h: float = 4, pocket: bool = True) -> cq.Workplane:
    """Raised circular pad with M3 clearance hole.

    Origin at base center.
    """
    result = cq.Workplane("XY").circle(d / 2).extrude(h)
    if pocket:
        result = result.faces(">Z").workplane().circle(M3_CLEAR / 2).cutThruAll()
    return result
