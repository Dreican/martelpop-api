import hashlib
from html import escape

def generate_avatar(display_name: str) -> str:
    words = display_name.strip().split()

    initials = (
        words[0][0] if len(words) == 1
        else words[0][0] + words[-1][0]
    ).upper()

    colors = ["#2563EB", "#7C3AED", "#DB2777", "#DC2626", "#059669"]
    index = int(hashlib.sha256(display_name.encode()).hexdigest(), 16)
    background = colors[index % len(colors)]

    return f"""
    <svg xmlns="http://www.w3.org/2000/svg" width="256" height="256">
      <rect width="256" height="256" rx="128" fill="{background}"/>
      <text
        x="50%"
        y="50%"
        dominant-baseline="central"
        text-anchor="middle"
        font-family="Arial, sans-serif"
        font-size="96"
        font-weight="600"
        fill="white"
      >{escape(initials)}</text>
    </svg>
    """