# Cat Feeder 5000 — Part 05: Auger Screw
# Rotates inside auger tube. Motor-driven. True helix via CadQuery sweep.
# Print: PETG, 0.15mm layers, 60% infill, supports YES.
# Print vertically (coupler end down) for thread layer integrity.

import cadquery as cq
import math
import sys; sys.path.insert(0, "..")
from params import AUGER_TUBE_L, AUGER_PITCH, TOLERANCE


# Screw dimensions
SCREW_OD = 30       # 1mm clearance to tube ID=32
PITCH = AUGER_PITCH
TURNS = math.floor(AUGER_TUBE_L / PITCH) - 1
SCREW_L = TURNS * PITCH
THREAD_D = 12       # Thread fin depth (radial)
THREAD_T = PITCH * 0.3   # Thread thickness (axial)
SHAFT_D = 5         # Motor shaft bore
COUPLER_L = 15
SET_D = 3           # Set screw hole diameter
CORE_D = SCREW_OD * 0.4  # 12mm core rod


def auger_screw() -> cq.Workplane:
    """Auger screw with true helical flights, coupler, and shaft bore.

    Origin at coupler bottom center. Screw extends upward.
    """
    # Core rod (full length from coupler bottom to screw top)
    total_h = COUPLER_L + SCREW_L
    core = cq.Workplane("XY").circle(CORE_D / 2).extrude(total_h)

    # Motor coupler (wider base section)
    coupler = (
        cq.Workplane("XY")
        .circle(SCREW_OD * 0.5 / 2)
        .extrude(COUPLER_L)
    )
    result = core.union(coupler)

    # Helical thread flights — true helix sweep
    # Profile: rectangular cross-section of the flight
    # Sweep along helix path
    helix_height = SCREW_L
    helix_wire = cq.Wire.makeHelix(
        pitch=PITCH,
        height=helix_height,
        radius=CORE_D / 2 + THREAD_D / 2,
        center=cq.Vector(0, 0, COUPLER_L),
        lefthand=True,
    )

    # Flight cross-section: rectangle centered on helix radius
    flight_profile = (
        cq.Workplane("XZ")
        .center(CORE_D / 2 + THREAD_D / 2, COUPLER_L)
        .rect(THREAD_D, THREAD_T)
    )
    flight = flight_profile.sweep(cq.Workplane().add(helix_wire), isFrenet=True)
    result = result.union(flight)

    # Shaft bore (through coupler and into core)
    shaft_hole = (
        cq.Workplane("XY")
        .circle((SHAFT_D + TOLERANCE) / 2)
        .extrude(COUPLER_L + 5)
        .translate((0, 0, -0.1))
    )
    result = result.cut(shaft_hole)

    # Set screw hole (M3, through side of coupler at mid-height)
    set_hole = (
        cq.Workplane("YZ")
        .workplane(offset=0)
        .center(0, COUPLER_L / 2)
        .circle(SET_D / 2)
        .extrude(SCREW_OD, both=True)
    )
    result = result.cut(set_hole)

    return result


if __name__ == "__main__":
    result = auger_screw()
    bb = result.val().BoundingBox()
    print(f"Auger screw: {bb.xlen:.1f} x {bb.ylen:.1f} x {bb.zlen:.1f} mm")
    print(f"Volume: {result.val().Volume():.1f} mm^3")
    print(f"Turns: {TURNS}, Screw length: {SCREW_L}mm")
    cq.exporters.export(result, "p05_auger_screw.step")
    cq.exporters.export(result, "p05_auger_screw.stl")
    print("Exported p05_auger_screw.step and p05_auger_screw.stl")
