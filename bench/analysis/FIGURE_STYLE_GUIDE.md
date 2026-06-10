# Figure Style Guide

## General

- **Font**: DejaVu Sans (sans-serif), base size **9pt** for everything
- **Title**: 9pt, normal weight (no bold)
- **Axis labels**: 9pt
- **Tick labels**: 8.5pt
- **Legend**: 9pt, matching body text
- **Annotations/numbers on figures**: 9pt, matching body text
- **DPI**: 300 for saved figures

## Borders & Axes

- Four-sided borders (all spines enabled: top, bottom, left, right)
- Spine linewidth: 0.6
- No default grid; add custom gridlines only when needed (e.g., denser in interesting ranges, sparser elsewhere)

## Colors

Muted, lower-saturation palette:

| Name | Hex | Usage |
|---|---|---|
| Soft blue | `#77B1F2` | Primary / docs / agent-side |
| Soft red | `#F08D8D` | Secondary / no-docs / env bugs |
| Muted green | `#8BC7A3` | Easy tasks / post-audit |
| Muted amber | `#F2CB6C` | Medium tasks / ambiguous |
| Muted orange | `#E8956A` | Original hard tasks |
| Muted pink | `#D98BA3` | Hardened R1 |
| Muted purple | `#A68BBF` | Hardened R2 / impossible tasks |
| Muted indigo | `#7A8FBF` | Hardened R3 |
| Muted cyan | `#72BFC7` | Hardened R4 |
| Muted brown | `#A68F7D` | Infrastructure |
| Muted red | `#E07A7A` | App bugs |
| Muted orange (alt) | `#E8A85C` | Verifier bugs |

For multi-line plots, cycle through: `#77B1F2`, `#E8A85C`, `#8BC7A3`, `#E07A7A`, `#A68BBF`, `#72BFC7`, `#D98BA3`, `#A68F7D`, `#F2CB6C`, `#7A8FBF`.

## Layout

- Figures should be compact; avoid excess whitespace
- Bar chart numbers go inside/near the bar tops, not above error bars
- Error bars: thin lines (`elinewidth=1`, `capthick=1`, color `#555`)
- Bar edge color: white, linewidth 0.5

## Legends

- Use a legend box (with `frameon=True`, `framealpha=0.9`, `edgecolor='#DDD'`) when there are many series
- Place legend to the side (`bbox_to_anchor=(1.02, 1)`) if it would occlude data
- For donut/pie charts: no legend; use leader lines to centered labels outside the wedge, percentages inside the wedge (white, bold)

## Labels & Annotations

- Multi-word labels should be split across lines and centered (e.g., `"Verifier\nBug\n(27)"`)
- For line plots with clustered endpoints, annotate deltas or values next to the points, nudging to avoid overlap
- When a figure doesn't communicate well due to crowded data, prefer a table in the text instead

## Donut/Pie Charts

- Ring width: 0.48
- White edge between wedges (linewidth 1.5)
- Percentages inside wedges: white, bold, 9pt
- Category labels outside with thin leader lines (color `#999`, linewidth 0.8)
- Labels centered, count on its own line: e.g., `"Verifier\nBug\n(27)"`

## rcParams Reference

```python
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['DejaVu Sans'],
    'font.size': 9,
    'axes.titlesize': 9,
    'axes.titleweight': 'normal',
    'axes.titlepad': 10,
    'axes.labelsize': 9,
    'axes.labelpad': 6,
    'axes.linewidth': 0.6,
    'axes.grid': False,
    'axes.spines.top': True,
    'axes.spines.right': True,
    'xtick.labelsize': 8.5,
    'ytick.labelsize': 8.5,
    'xtick.major.width': 0.6,
    'ytick.major.width': 0.6,
    'xtick.major.size': 3,
    'ytick.major.size': 3,
    'legend.fontsize': 9,
    'legend.frameon': False,
    'figure.dpi': 100,
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.08,
})
```
