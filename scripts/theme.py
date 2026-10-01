import html

USER = "numunun"
TZ = "Asia/Seoul"

BG_TOP, BG_BOTTOM = "#111722", "#0d1117"
BORDER = "#30363d"
MUTED = "#7d8590"
TEXT = "#c9d1d9"
BRIGHT = "#e6edf3"
GREEN = "#39d353"
CYAN = "#22d3ee"
BLUE = "#58a6ff"
ORANGE = "#ffa657"
PURPLE = "#bc8cff"
PINK = "#ff7b9c"
HEAT = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]

MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"

esc = html.escape


def window(w, h, title, extra_defs=""):
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" font-family="{MONO}">',
        '<defs>'
        f'<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{BG_TOP}"/><stop offset="1" stop-color="{BG_BOTTOM}"/></linearGradient>'
        f'<linearGradient id="edge" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{GREEN}" stop-opacity="0"/><stop offset=".5" stop-color="{GREEN}" stop-opacity=".9"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></linearGradient>'
        f'{extra_defs}</defs>',
        f'<rect width="{w}" height="{h}" rx="12" fill="url(#bg)"/>',
        f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="12" fill="none" stroke="{BORDER}"/>',
        f'<line x1="0" y1="30" x2="{w}" y2="30" stroke="{BORDER}"/>',
        # 창 윗선을 따라 흐르는 빛
        f'<rect x="-200" y="0" width="200" height="1.5" fill="url(#edge)">'
        f'<animate attributeName="x" from="-200" to="{w}" dur="6s" repeatCount="indefinite"/></rect>',
        '<circle cx="20" cy="15" r="5" fill="#ff5f56"/><circle cx="36" cy="15" r="5" fill="#ffbd2e"/><circle cx="52" cy="15" r="5" fill="#27c93f"/>',
        f'<text x="{w/2}" y="19" fill="{MUTED}" font-size="12" text-anchor="middle">{esc(title)}</text>',
    ]


def fade_in(inner, delay, dy=6):
    return (f'<g opacity="0" transform="translate(0,{dy})">{inner}'
            f'<animate attributeName="opacity" from="0" to="1" begin="{delay:.2f}s" dur=".45s" fill="freeze"/>'
            f'<animateTransform attributeName="transform" type="translate" from="0 {dy}" to="0 0" begin="{delay:.2f}s" dur=".45s" fill="freeze"/></g>')