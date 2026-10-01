"""Builds the printable shadow-zone map (student) and its key (teacher) for Unit 3 Lesson 3."""
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Wedge


def draw(path, key):
    fig, ax = plt.subplots(figsize=(8.5, 11))
    ax.set_xlim(-1.45, 1.45); ax.set_ylim(-1.9, 1.5); ax.set_aspect("equal"); ax.axis("off")
    title = "Shadow Zone Map - TEACHER KEY" if key else "Shadow Zone Map"
    ax.text(0, 1.42, title, ha="center", fontsize=18, weight="bold")
    ax.text(0, 1.31, "Name: ____________________   Period: ____" if not key else "Unit 3, Lesson 3 (Days 40-41)",
            ha="center", fontsize=11)
    if key:
        # S-wave shadow (104-180 deg) and P-wave shadow (104-140 deg), both sides
        ax.add_patch(Wedge((0, 0), 1, 90 - 180, 90 - 104, color="#f6e7a1"))
        ax.add_patch(Wedge((0, 0), 1, 90 + 104, 90 + 180, color="#f6e7a1"))
        ax.add_patch(Wedge((0, 0), 1, 90 - 140, 90 - 104, color="#f2b8b5"))
        ax.add_patch(Wedge((0, 0), 1, 90 + 104, 90 + 140, color="#f2b8b5"))
        ax.add_patch(Circle((0, 0), 3480 / 6371, fill=True, color="#ffd9a8", ec="#c05621", lw=2))
        ax.add_patch(Circle((0, 0), 1220 / 6371, fill=True, color="#fbb36b", ec="#c05621", lw=1.5))
        ax.text(0, 0.30, "liquid outer core", ha="center", fontsize=10)
        ax.text(0, -0.03, "solid\ninner core", ha="center", fontsize=9)
    ax.add_patch(Circle((0, 0), 1, fill=False, lw=2.5))
    for d in range(0, 181, 10):
        for side in (1, -1):
            if side == -1 and d in (0, 180):
                continue
            a = math.radians(90 - side * d)
            x, y = math.cos(a), math.sin(a)
            ax.plot([x, 1.06 * x], [y, 1.06 * y], color="black", lw=1.2)
            ax.text(1.15 * x, 1.15 * y, f"{d}°", ha="center", va="center", fontsize=8.5)
    ax.plot(0, 1, marker="*", markersize=22, color="#c53030")
    ax.text(0.08, 0.86, "earthquake", fontsize=10, color="#c53030")
    legend = ["Color each station's dot on the edge of the circle (both sides):",
              "GREEN = P-waves and S-waves     YELLOW = P-waves only     RED = no waves"]
    if key:
        legend = ["Green: 0-103° (P and S).  Red/pink band: 104-140° (no direct waves = shadow zone).",
                  "Yellow: 141-180° (P only: S-waves stopped by the liquid outer core).",
                  "Core-mantle boundary drawn to scale: about 2,900 km deep (core radius about 3,480 km)."]
    for i, line in enumerate(legend):
        ax.text(0, -1.38 - 0.11 * i, line, ha="center", fontsize=10.5)
    if not key:
        ax.text(0, -1.75, "Then: draw a circle inside Earth that would block S-waves from reaching the yellow stations.",
                ha="center", fontsize=10.5, style="italic")
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)


draw("shadow-zone-map.pdf", key=False)
draw("shadow-zone-map-KEY.pdf", key=True)
draw("shadow-zone-map-KEY.png", key=True)
