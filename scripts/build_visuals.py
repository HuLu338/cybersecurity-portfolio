"""Generate original decorative SVG artwork; no external images or libraries."""
from pathlib import Path
import math

ROOT = Path(__file__).resolve().parents[1]

def point(u, v):
    x = 510 + 1190 * u + 105 * math.sin(v * math.pi)
    ridge = math.exp(-((u - .47) / .24) ** 2)
    y = 115 + 700 * v - 230 * ridge * math.sin(v * math.pi) + 54 * math.sin(u * 4.2 + v * 2)
    return x, y

def line(points):
    return 'M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in points)

paths=[]
for row in range(34):
    v=row/33
    paths.append(f'<path d="{line(point(i/66,v) for i in range(67))}"/>')
for column in range(38):
    u=column/37
    paths.append(f'<path d="{line(point(u,i/42) for i in range(43))}"/>')

svg='''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 900" fill="none">
<title>Original abstract gradient and contour field</title>
<defs>
<radialGradient id="blue"><stop stop-color="#9CAEEB" stop-opacity=".9"/><stop offset="1" stop-color="#BAC8EF" stop-opacity="0"/></radialGradient>
<radialGradient id="mint"><stop stop-color="#A9D8BA" stop-opacity=".95"/><stop offset="1" stop-color="#C5E4C9" stop-opacity="0"/></radialGradient>
<radialGradient id="peach"><stop stop-color="#EDBDAC" stop-opacity=".75"/><stop offset="1" stop-color="#EED2C4" stop-opacity="0"/></radialGradient>
<linearGradient id="ink" x1="600" y1="100" x2="1550" y2="850" gradientUnits="userSpaceOnUse"><stop stop-color="#3B8981"/><stop offset=".52" stop-color="#6A7CB8"/><stop offset="1" stop-color="#25766C"/></linearGradient>
<linearGradient id="reveal"><stop stop-color="white" stop-opacity="0"/><stop offset=".3" stop-color="white" stop-opacity=".2"/><stop offset=".62" stop-color="white"/><stop offset="1" stop-color="white" stop-opacity=".8"/></linearGradient>
<mask id="right"><rect width="1600" height="900" fill="url(#reveal)"/></mask>
</defs>
<ellipse cx="1210" cy="275" rx="510" ry="440" fill="url(#blue)"/>
<ellipse cx="1060" cy="650" rx="580" ry="400" fill="url(#mint)"/>
<ellipse cx="1530" cy="585" rx="400" ry="330" fill="url(#peach)"/>
<g stroke="url(#ink)" stroke-width=".85" opacity=".42" mask="url(#right)">'''+''.join(paths)+'''</g>
<g stroke="#3A726B" opacity=".3" stroke-width="1"><path d="M1383 120h20m-10-10v20M890 693h20m-10-10v20M1480 766h20m-10-10v20"/><circle cx="1178" cy="422" r="5"/></g>
</svg>'''
out=ROOT/'assets/images/signal-field.svg'
out.write_text(svg,encoding='utf-8',newline='\n')
print(f'Generated {out.name}: {len(paths)} original paths, {out.stat().st_size} bytes')
