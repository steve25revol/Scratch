"""Generate all SVG costumes for the Scratch stickman animation project."""


def _svg_wrap(inner, width=480, height=360):
    """Wrap SVG content in a standard SVG document."""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}">'
        f'{inner}</svg>'
    )


def _stickman(cx, cy, scale=1.0, arms="down", legs="stand",
              head_tilt=0, body_color="#000000", extra=""):
    """Draw a stickman at (cx, cy) with various poses.

    arms: "down", "typing1", "typing2", "up", "flail1", "flail2",
          "run1", "run2", "reach_up", "shrug", "thumbsup"
    legs: "stand", "sit", "run1", "run2", "fall", "landing", "bent"
    """
    s = scale
    head_r = 12 * s
    body_len = 40 * s
    arm_len = 30 * s
    leg_len = 35 * s
    sw = max(2, 3 * s)  # stroke width

    # Head
    hx = cx
    hy = cy - body_len - head_r
    parts = [
        f'<circle cx="{hx}" cy="{hy}" r="{head_r}" fill="none" '
        f'stroke="{body_color}" stroke-width="{sw}"/>'
    ]

    # Body
    neck_y = hy + head_r
    hip_y = neck_y + body_len
    parts.append(
        f'<line x1="{hx}" y1="{neck_y}" x2="{hx}" y2="{hip_y}" '
        f'stroke="{body_color}" stroke-width="{sw}"/>'
    )

    # Shoulder point
    sh_y = neck_y + 10 * s

    # Arms
    if arms == "down":
        parts.append(f'<line x1="{hx - arm_len}" y1="{sh_y + arm_len*0.7}" x2="{hx}" y2="{sh_y}" stroke="{body_color}" stroke-width="{sw}"/>')
        parts.append(f'<line x1="{hx}" y1="{sh_y}" x2="{hx + arm_len}" y2="{sh_y + arm_len*0.7}" stroke="{body_color}" stroke-width="{sw}"/>')
    elif arms == "typing1":
        # Arms forward and slightly down, hands close together
        parts.append(f'<line x1="{hx}" y1="{sh_y}" x2="{hx - 15*s}" y2="{sh_y + 20*s}" stroke="{body_color}" stroke-width="{sw}"/>')
        parts.append(f'<line x1="{hx - 15*s}" y1="{sh_y + 20*s}" x2="{hx - 5*s}" y2="{sh_y + 25*s}" stroke="{body_color}" stroke-width="{sw}"/>')
        parts.append(f'<line x1="{hx}" y1="{sh_y}" x2="{hx + 15*s}" y2="{sh_y + 20*s}" stroke="{body_color}" stroke-width="{sw}"/>')
        parts.append(f'<line x1="{hx + 15*s}" y1="{sh_y + 20*s}" x2="{hx + 8*s}" y2="{sh_y + 25*s}" stroke="{body_color}" stroke-width="{sw}"/>')
    elif arms == "typing2":
        parts.append(f'<line x1="{hx}" y1="{sh_y}" x2="{hx - 15*s}" y2="{sh_y + 20*s}" stroke="{body_color}" stroke-width="{sw}"/>')
        parts.append(f'<line x1="{hx - 15*s}" y1="{sh_y + 20*s}" x2="{hx - 8*s}" y2="{sh_y + 22*s}" stroke="{body_color}" stroke-width="{sw}"/>')
        parts.append(f'<line x1="{hx}" y1="{sh_y}" x2="{hx + 15*s}" y2="{sh_y + 20*s}" stroke="{body_color}" stroke-width="{sw}"/>')
        parts.append(f'<line x1="{hx + 15*s}" y1="{sh_y + 20*s}" x2="{hx + 5*s}" y2="{sh_y + 28*s}" stroke="{body_color}" stroke-width="{sw}"/>')
    elif arms == "up":
        parts.append(f'<line x1="{hx}" y1="{sh_y}" x2="{hx - 20*s}" y2="{sh_y - 25*s}" stroke="{body_color}" stroke-width="{sw}"/>')
        parts.append(f'<line x1="{hx}" y1="{sh_y}" x2="{hx + 20*s}" y2="{sh_y - 25*s}" stroke="{body_color}" stroke-width="{sw}"/>')
    elif arms == "flail1":
        parts.append(f'<line x1="{hx}" y1="{sh_y}" x2="{hx - 25*s}" y2="{sh_y - 15*s}" stroke="{body_color}" stroke-width="{sw}"/>')
        parts.append(f'<line x1="{hx}" y1="{sh_y}" x2="{hx + 20*s}" y2="{sh_y + 10*s}" stroke="{body_color}" stroke-width="{sw}"/>')
    elif arms == "flail2":
        parts.append(f'<line x1="{hx}" y1="{sh_y}" x2="{hx - 20*s}" y2="{sh_y + 10*s}" stroke="{body_color}" stroke-width="{sw}"/>')
        parts.append(f'<line x1="{hx}" y1="{sh_y}" x2="{hx + 25*s}" y2="{sh_y - 15*s}" stroke="{body_color}" stroke-width="{sw}"/>')
    elif arms == "run1":
        parts.append(f'<line x1="{hx}" y1="{sh_y}" x2="{hx - 25*s}" y2="{sh_y + 5*s}" stroke="{body_color}" stroke-width="{sw}"/>')
        parts.append(f'<line x1="{hx}" y1="{sh_y}" x2="{hx + 25*s}" y2="{sh_y - 5*s}" stroke="{body_color}" stroke-width="{sw}"/>')
    elif arms == "run2":
        parts.append(f'<line x1="{hx}" y1="{sh_y}" x2="{hx - 25*s}" y2="{sh_y - 5*s}" stroke="{body_color}" stroke-width="{sw}"/>')
        parts.append(f'<line x1="{hx}" y1="{sh_y}" x2="{hx + 25*s}" y2="{sh_y + 5*s}" stroke="{body_color}" stroke-width="{sw}"/>')
    elif arms == "reach_up":
        parts.append(f'<line x1="{hx}" y1="{sh_y}" x2="{hx}" y2="{sh_y - 30*s}" stroke="{body_color}" stroke-width="{sw}"/>')
        parts.append(f'<line x1="{hx}" y1="{sh_y}" x2="{hx + 20*s}" y2="{sh_y + 15*s}" stroke="{body_color}" stroke-width="{sw}"/>')
    elif arms == "shrug":
        parts.append(f'<line x1="{hx}" y1="{sh_y}" x2="{hx - 25*s}" y2="{sh_y - 10*s}" stroke="{body_color}" stroke-width="{sw}"/>')
        parts.append(f'<line x1="{hx - 25*s}" y1="{sh_y - 10*s}" x2="{hx - 20*s}" y2="{sh_y - 18*s}" stroke="{body_color}" stroke-width="{sw}"/>')
        parts.append(f'<line x1="{hx}" y1="{sh_y}" x2="{hx + 25*s}" y2="{sh_y - 10*s}" stroke="{body_color}" stroke-width="{sw}"/>')
        parts.append(f'<line x1="{hx + 25*s}" y1="{sh_y - 10*s}" x2="{hx + 20*s}" y2="{sh_y - 18*s}" stroke="{body_color}" stroke-width="{sw}"/>')
    elif arms == "thumbsup":
        parts.append(f'<line x1="{hx}" y1="{sh_y}" x2="{hx - 20*s}" y2="{sh_y + 15*s}" stroke="{body_color}" stroke-width="{sw}"/>')
        parts.append(f'<line x1="{hx}" y1="{sh_y}" x2="{hx + 20*s}" y2="{sh_y - 5*s}" stroke="{body_color}" stroke-width="{sw}"/>')
        parts.append(f'<line x1="{hx + 20*s}" y1="{sh_y - 5*s}" x2="{hx + 20*s}" y2="{sh_y - 18*s}" stroke="{body_color}" stroke-width="{sw}"/>')

    # Legs
    if legs == "stand":
        parts.append(f'<line x1="{hx}" y1="{hip_y}" x2="{hx - 15*s}" y2="{hip_y + leg_len}" stroke="{body_color}" stroke-width="{sw}"/>')
        parts.append(f'<line x1="{hx}" y1="{hip_y}" x2="{hx + 15*s}" y2="{hip_y + leg_len}" stroke="{body_color}" stroke-width="{sw}"/>')
    elif legs == "sit":
        # Legs bent at 90 degrees forward (sitting)
        knee_y = hip_y + 18 * s
        parts.append(f'<line x1="{hx}" y1="{hip_y}" x2="{hx - 8*s}" y2="{knee_y}" stroke="{body_color}" stroke-width="{sw}"/>')
        parts.append(f'<line x1="{hx - 8*s}" y1="{knee_y}" x2="{hx - 8*s}" y2="{knee_y + 18*s}" stroke="{body_color}" stroke-width="{sw}"/>')
        parts.append(f'<line x1="{hx}" y1="{hip_y}" x2="{hx + 8*s}" y2="{knee_y}" stroke="{body_color}" stroke-width="{sw}"/>')
        parts.append(f'<line x1="{hx + 8*s}" y1="{knee_y}" x2="{hx + 8*s}" y2="{knee_y + 18*s}" stroke="{body_color}" stroke-width="{sw}"/>')
    elif legs == "run1":
        parts.append(f'<line x1="{hx}" y1="{hip_y}" x2="{hx - 20*s}" y2="{hip_y + leg_len}" stroke="{body_color}" stroke-width="{sw}"/>')
        parts.append(f'<line x1="{hx}" y1="{hip_y}" x2="{hx + 20*s}" y2="{hip_y + leg_len - 10*s}" stroke="{body_color}" stroke-width="{sw}"/>')
    elif legs == "run2":
        parts.append(f'<line x1="{hx}" y1="{hip_y}" x2="{hx + 20*s}" y2="{hip_y + leg_len}" stroke="{body_color}" stroke-width="{sw}"/>')
        parts.append(f'<line x1="{hx}" y1="{hip_y}" x2="{hx - 20*s}" y2="{hip_y + leg_len - 10*s}" stroke="{body_color}" stroke-width="{sw}"/>')
    elif legs == "fall":
        parts.append(f'<line x1="{hx}" y1="{hip_y}" x2="{hx - 10*s}" y2="{hip_y + leg_len}" stroke="{body_color}" stroke-width="{sw}"/>')
        parts.append(f'<line x1="{hx}" y1="{hip_y}" x2="{hx + 10*s}" y2="{hip_y + leg_len}" stroke="{body_color}" stroke-width="{sw}"/>')
    elif legs == "landing":
        # Legs slightly bent on landing
        parts.append(f'<line x1="{hx}" y1="{hip_y}" x2="{hx - 18*s}" y2="{hip_y + 15*s}" stroke="{body_color}" stroke-width="{sw}"/>')
        parts.append(f'<line x1="{hx - 18*s}" y1="{hip_y + 15*s}" x2="{hx - 15*s}" y2="{hip_y + leg_len}" stroke="{body_color}" stroke-width="{sw}"/>')
        parts.append(f'<line x1="{hx}" y1="{hip_y}" x2="{hx + 18*s}" y2="{hip_y + 15*s}" stroke="{body_color}" stroke-width="{sw}"/>')
        parts.append(f'<line x1="{hx + 18*s}" y1="{hip_y + 15*s}" x2="{hx + 15*s}" y2="{hip_y + leg_len}" stroke="{body_color}" stroke-width="{sw}"/>')
    elif legs == "bent":
        # Slightly bent
        parts.append(f'<line x1="{hx}" y1="{hip_y}" x2="{hx - 12*s}" y2="{hip_y + 20*s}" stroke="{body_color}" stroke-width="{sw}"/>')
        parts.append(f'<line x1="{hx - 12*s}" y1="{hip_y + 20*s}" x2="{hx - 8*s}" y2="{hip_y + leg_len}" stroke="{body_color}" stroke-width="{sw}"/>')
        parts.append(f'<line x1="{hx}" y1="{hip_y}" x2="{hx + 12*s}" y2="{hip_y + 20*s}" stroke="{body_color}" stroke-width="{sw}"/>')
        parts.append(f'<line x1="{hx + 12*s}" y1="{hip_y + 20*s}" x2="{hx + 8*s}" y2="{hip_y + leg_len}" stroke="{body_color}" stroke-width="{sw}"/>')

    if extra:
        parts.append(extra)

    return "\n".join(parts)


# ============================================================
# BACKDROP SVGs
# ============================================================

def _backdrop_office_interior():
    """Office interior with walls, window, desks, lights."""
    parts = []
    # Floor
    parts.append('<rect x="0" y="0" width="480" height="360" fill="#E8E0D0"/>')
    # Floor line
    parts.append('<rect x="0" y="280" width="480" height="80" fill="#B0A090"/>')
    parts.append('<line x1="0" y1="280" x2="480" y2="280" stroke="#8B7D6B" stroke-width="2"/>')
    # Back wall
    parts.append('<rect x="0" y="0" width="480" height="280" fill="#D4CFC4"/>')
    # Window on right wall
    parts.append('<rect x="370" y="60" width="80" height="120" fill="#87CEEB" stroke="#6B5B4F" stroke-width="3"/>')
    parts.append('<line x1="410" y1="60" x2="410" y2="180" stroke="#6B5B4F" stroke-width="2"/>')
    parts.append('<line x1="370" y1="120" x2="450" y2="120" stroke="#6B5B4F" stroke-width="2"/>')
    # Fluorescent lights
    parts.append('<rect x="80" y="15" width="120" height="8" rx="3" fill="#FFFFFF" stroke="#CCC" stroke-width="1"/>')
    parts.append('<rect x="280" y="15" width="120" height="8" rx="3" fill="#FFFFFF" stroke="#CCC" stroke-width="1"/>')
    # Desk 1 (hero's desk, center-left)
    parts.append('<rect x="100" y="220" width="120" height="5" fill="#8B6914"/>')
    parts.append('<rect x="110" y="225" width="5" height="55" fill="#6B4914"/>')
    parts.append('<rect x="205" y="225" width="5" height="55" fill="#6B4914"/>')
    # Desk 2 (upper-left, coworker A)
    parts.append('<rect x="20" y="160" width="80" height="4" fill="#8B6914"/>')
    parts.append('<rect x="25" y="164" width="4" height="40" fill="#6B4914"/>')
    parts.append('<rect x="92" y="164" width="4" height="40" fill="#6B4914"/>')
    # Desk 3 (lower-left, coworker C)
    parts.append('<rect x="20" y="240" width="70" height="4" fill="#8B6914"/>')
    # Water cooler (right area)
    parts.append('<rect x="310" y="220" width="20" height="40" rx="3" fill="#DDEEFF" stroke="#99BBDD" stroke-width="1"/>')
    parts.append('<rect x="313" y="210" width="14" height="15" rx="5" fill="#AAD4FF" stroke="#88AACC" stroke-width="1"/>')
    # Plant in corner
    parts.append('<rect x="455" y="250" width="15" height="25" fill="#8B4513"/>')
    parts.append('<circle cx="462" cy="245" r="15" fill="#228B22"/>')
    parts.append('<circle cx="452" cy="238" r="10" fill="#2E8B2E"/>')
    parts.append('<circle cx="470" cy="240" r="10" fill="#1E7B1E"/>')
    return _svg_wrap("\n".join(parts))


def _backdrop_building_exterior():
    """Tall building with sky."""
    parts = []
    # Sky
    parts.append('<rect x="0" y="0" width="480" height="360" fill="#87CEEB"/>')
    # Gradient sky effect
    parts.append('<rect x="0" y="0" width="480" height="60" fill="#6BB8E0" opacity="0.5"/>')
    # Clouds
    parts.append('<ellipse cx="350" cy="50" rx="50" ry="20" fill="white" opacity="0.8"/>')
    parts.append('<ellipse cx="380" cy="45" rx="35" ry="18" fill="white" opacity="0.7"/>')
    parts.append('<ellipse cx="120" cy="80" rx="40" ry="15" fill="white" opacity="0.7"/>')
    # Building on left
    parts.append('<rect x="20" y="20" width="180" height="340" fill="#A0937D"/>')
    parts.append('<rect x="20" y="20" width="180" height="340" fill="none" stroke="#7D7060" stroke-width="2"/>')
    # Windows grid (6 cols, many rows)
    for row in range(12):
        for col in range(5):
            wx = 32 + col * 34
            wy = 30 + row * 28
            fill = "#FFFFCC" if (row + col) % 3 != 0 else "#FFD700"
            parts.append(f'<rect x="{wx}" y="{wy}" width="22" height="18" fill="{fill}" stroke="#6B5B4F" stroke-width="1"/>')
    # Smoke from one window
    parts.append('<circle cx="100" cy="55" r="8" fill="#555" opacity="0.4"/>')
    parts.append('<circle cx="105" cy="45" r="10" fill="#666" opacity="0.3"/>')
    parts.append('<circle cx="110" cy="35" r="12" fill="#777" opacity="0.2"/>')
    return _svg_wrap("\n".join(parts))


def _backdrop_building_with_ground():
    """Building exterior with ground level visible."""
    parts = []
    # Sky
    parts.append('<rect x="0" y="0" width="480" height="360" fill="#87CEEB"/>')
    parts.append('<ellipse cx="400" cy="40" rx="45" ry="18" fill="white" opacity="0.7"/>')
    parts.append('<ellipse cx="100" cy="60" rx="35" ry="14" fill="white" opacity="0.6"/>')
    # Building
    parts.append('<rect x="20" y="10" width="160" height="310" fill="#A0937D"/>')
    parts.append('<rect x="20" y="10" width="160" height="310" fill="none" stroke="#7D7060" stroke-width="2"/>')
    # Windows
    for row in range(10):
        for col in range(4):
            wx = 30 + col * 36
            wy = 20 + row * 30
            fill = "#FFFFCC"
            parts.append(f'<rect x="{wx}" y="{wy}" width="24" height="18" fill="{fill}" stroke="#6B5B4F" stroke-width="1"/>')
    # Ground/street
    parts.append('<rect x="0" y="320" width="480" height="40" fill="#808080"/>')
    # Sidewalk
    parts.append('<rect x="0" y="310" width="480" height="15" fill="#C0C0C0"/>')
    # Sidewalk lines
    for x in range(0, 480, 40):
        parts.append(f'<line x1="{x}" y1="310" x2="{x}" y2="325" stroke="#A0A0A0" stroke-width="1"/>')
    # Tree
    parts.append('<rect x="300" y="270" width="8" height="45" fill="#8B4513"/>')
    parts.append('<circle cx="304" cy="260" r="22" fill="#228B22"/>')
    parts.append('<circle cx="294" cy="255" r="16" fill="#2E8B2E"/>')
    parts.append('<circle cx="314" cy="258" r="16" fill="#1E7B1E"/>')
    # Smoke from building
    parts.append('<circle cx="85" cy="25" r="6" fill="#555" opacity="0.4"/>')
    parts.append('<circle cx="90" cy="15" r="8" fill="#666" opacity="0.3"/>')
    return _svg_wrap("\n".join(parts))


# ============================================================
# STICKMAN HERO COSTUMES
# ============================================================

def _hero_costumes():
    """Return dict of {name: svg_string} for StickmanHero."""
    costumes = {}
    cx, cy = 240, 260  # center position in SVG space

    # Typing frames (sitting at desk)
    costumes["typing-1"] = _svg_wrap(_stickman(cx, cy, arms="typing1", legs="sit"))
    costumes["typing-2"] = _svg_wrap(_stickman(cx, cy, arms="typing2", legs="sit"))

    # Surprised (leaning back)
    costumes["surprised"] = _svg_wrap(_stickman(cx - 5, cy, arms="up", legs="sit"))

    # Knocked back
    costumes["knocked-back"] = _svg_wrap(_stickman(cx - 20, cy + 5, arms="flail1", legs="bent"))

    # Running frames
    costumes["running-1"] = _svg_wrap(_stickman(cx, cy, arms="run1", legs="run1"))
    costumes["running-2"] = _svg_wrap(_stickman(cx, cy, arms="run2", legs="run2"))
    costumes["running-3"] = _svg_wrap(_stickman(cx, cy, arms="run1", legs="run2"))

    # Jumping
    costumes["jumping"] = _svg_wrap(_stickman(cx, cy - 10, arms="up", legs="bent"))

    # Falling frames
    costumes["falling-1"] = _svg_wrap(_stickman(cx, cy, arms="flail1", legs="fall"))
    costumes["falling-2"] = _svg_wrap(_stickman(cx, cy, arms="flail2", legs="fall"))
    costumes["falling-3"] = _svg_wrap(_stickman(cx, cy, arms="up", legs="fall"))

    # Parachute hold
    costumes["parachute-hold"] = _svg_wrap(_stickman(cx, cy, arms="reach_up", legs="fall"))

    # Landing
    costumes["landing"] = _svg_wrap(_stickman(cx, cy + 5, arms="down", legs="landing"))

    # Standing final
    costumes["standing-final"] = _svg_wrap(_stickman(cx, cy, arms="down", legs="stand"))

    # Shrug
    costumes["shrug"] = _svg_wrap(_stickman(cx, cy, arms="shrug", legs="stand"))

    return costumes


# ============================================================
# COWORKER COSTUMES
# ============================================================

def _coworker_costumes(name_prefix, cx, cy, scale=0.7):
    """Return dict of costumes for a coworker sprite."""
    costumes = {}
    costumes[f"{name_prefix}-idle-1"] = _svg_wrap(
        _stickman(cx, cy, scale=scale, arms="down", legs="stand", body_color="#333333"))
    costumes[f"{name_prefix}-idle-2"] = _svg_wrap(
        _stickman(cx, cy - 2, scale=scale, arms="down", legs="stand", body_color="#333333"))
    costumes[f"{name_prefix}-panic-1"] = _svg_wrap(
        _stickman(cx, cy, scale=scale, arms="up", legs="stand", body_color="#333333"))
    costumes[f"{name_prefix}-panic-2"] = _svg_wrap(
        _stickman(cx + 5, cy, scale=scale, arms="flail1", legs="run1", body_color="#333333"))
    return costumes


# ============================================================
# COMPUTER/MONITOR COSTUMES
# ============================================================

def _computer_costumes():
    """Return costumes for the computer monitor sprite."""
    costumes = {}

    def _monitor(screen_color="#335577", screen_extra="", broken=False):
        parts = []
        # Monitor body
        parts.append('<rect x="200" y="170" width="70" height="55" rx="3" fill="#222" stroke="#444" stroke-width="2"/>')
        if not broken:
            parts.append(f'<rect x="205" y="175" width="60" height="40" rx="2" fill="{screen_color}"/>')
            if screen_extra:
                parts.append(screen_extra)
            # Screen glow lines
            parts.append('<line x1="210" y1="185" x2="255" y2="185" stroke="#88AACC" stroke-width="1" opacity="0.5"/>')
            parts.append('<line x1="210" y1="192" x2="250" y2="192" stroke="#88AACC" stroke-width="1" opacity="0.5"/>')
            parts.append('<line x1="210" y1="199" x2="248" y2="199" stroke="#88AACC" stroke-width="1" opacity="0.5"/>')
        else:
            # Broken screen with cracks
            parts.append(f'<rect x="205" y="175" width="60" height="40" rx="2" fill="#222"/>')
            parts.append('<line x1="220" y1="175" x2="250" y2="215" stroke="#555" stroke-width="2"/>')
            parts.append('<line x1="250" y1="180" x2="215" y2="210" stroke="#555" stroke-width="1"/>')
            # Smoke
            parts.append('<circle cx="235" cy="168" r="5" fill="#888" opacity="0.5"/>')
            parts.append('<circle cx="240" cy="160" r="7" fill="#888" opacity="0.3"/>')
        # Stand
        parts.append('<rect x="228" y="225" width="14" height="15" fill="#333"/>')
        parts.append('<rect x="218" y="238" width="34" height="4" rx="2" fill="#333"/>')
        # Keyboard
        parts.append('<rect x="205" y="248" width="60" height="8" rx="2" fill="#444" stroke="#555" stroke-width="1"/>')
        return "\n".join(parts)

    costumes["normal-1"] = _svg_wrap(_monitor("#335577"))
    costumes["normal-2"] = _svg_wrap(_monitor("#3A6088"))
    costumes["glitching"] = _svg_wrap(_monitor("#335577",
        '<rect x="210" y="185" width="50" height="5" fill="#FF5555" opacity="0.7"/>'
        '<rect x="215" y="200" width="40" height="3" fill="#55FF55" opacity="0.5"/>'))
    costumes["red-screen"] = _svg_wrap(_monitor("#AA2222"))
    costumes["destroyed"] = _svg_wrap(_monitor(broken=True))
    return costumes


# ============================================================
# EXPLOSION COSTUMES
# ============================================================

def _explosion_costumes():
    """Return explosion animation frame costumes."""
    costumes = {}
    cx, cy = 235, 200

    costumes["flash-small"] = _svg_wrap(
        f'<circle cx="{cx}" cy="{cy}" r="15" fill="#FFFF00" opacity="0.9"/>'
        f'<circle cx="{cx}" cy="{cy}" r="8" fill="#FFFFFF"/>',
        100, 100)

    costumes["fireball-1"] = _svg_wrap(
        f'<circle cx="{cx}" cy="{cy}" r="30" fill="#FF6600" opacity="0.8"/>'
        f'<circle cx="{cx}" cy="{cy}" r="20" fill="#FFAA00" opacity="0.9"/>'
        f'<circle cx="{cx}" cy="{cy}" r="10" fill="#FFFF00"/>',
        200, 200)

    costumes["fireball-2"] = _svg_wrap(
        f'<circle cx="{cx}" cy="{cy}" r="50" fill="#FF4400" opacity="0.7"/>'
        f'<circle cx="{cx}" cy="{cy}" r="35" fill="#FF6600" opacity="0.8"/>'
        f'<circle cx="{cx}" cy="{cy}" r="20" fill="#FFAA00"/>'
        f'<circle cx="{cx}" cy="{cy}" r="10" fill="#FFFF00" opacity="0.9"/>',
        300, 300)

    costumes["fireball-3"] = _svg_wrap(
        f'<circle cx="{cx}" cy="{cy}" r="70" fill="#CC3300" opacity="0.6"/>'
        f'<circle cx="{cx}" cy="{cy}" r="50" fill="#FF4400" opacity="0.7"/>'
        f'<circle cx="{cx}" cy="{cy}" r="30" fill="#FF8800" opacity="0.8"/>'
        f'<circle cx="{cx}" cy="{cy}" r="15" fill="#FFCC00"/>',
        350, 350)

    costumes["smoke-1"] = _svg_wrap(
        f'<circle cx="{cx}" cy="{cy}" r="60" fill="#555" opacity="0.5"/>'
        f'<circle cx="{cx - 20}" cy="{cy - 15}" r="30" fill="#666" opacity="0.6"/>'
        f'<circle cx="{cx + 25}" cy="{cy + 10}" r="25" fill="#777" opacity="0.5"/>'
        f'<circle cx="{cx}" cy="{cy}" r="20" fill="#FF6600" opacity="0.3"/>',
        350, 350)

    costumes["smoke-2"] = _svg_wrap(
        f'<circle cx="{cx}" cy="{cy}" r="70" fill="#666" opacity="0.4"/>'
        f'<circle cx="{cx - 25}" cy="{cy - 20}" r="35" fill="#777" opacity="0.4"/>'
        f'<circle cx="{cx + 30}" cy="{cy + 15}" r="30" fill="#888" opacity="0.3"/>',
        350, 350)

    costumes["smoke-3"] = _svg_wrap(
        f'<circle cx="{cx}" cy="{cy}" r="80" fill="#888" opacity="0.25"/>'
        f'<circle cx="{cx - 30}" cy="{cy - 25}" r="40" fill="#999" opacity="0.2"/>',
        350, 350)

    costumes["dissipate"] = _svg_wrap(
        f'<circle cx="{cx}" cy="{cy}" r="90" fill="#AAA" opacity="0.1"/>',
        350, 350)

    return costumes


# ============================================================
# PARACHUTE COSTUMES
# ============================================================

def _parachute_costumes():
    """Return parachute sprite costumes."""
    costumes = {}
    cx = 240

    # Packed (small bundle above head)
    costumes["packed"] = _svg_wrap(
        f'<rect x="{cx - 8}" y="140" width="16" height="12" rx="3" fill="#CC3300" stroke="#AA2200" stroke-width="1"/>',
        480, 360)

    # Deploying-1 (small chute emerging)
    costumes["deploying-1"] = _svg_wrap(
        f'<path d="M{cx} 120 Q{cx - 25} 110 {cx - 30} 130 L{cx} 160 L{cx + 30} 130 Q{cx + 25} 110 {cx} 120Z" '
        f'fill="#CC3300" stroke="#AA2200" stroke-width="1.5" opacity="0.8"/>'
        f'<line x1="{cx - 25}" y1="130" x2="{cx}" y2="180" stroke="#333" stroke-width="1"/>'
        f'<line x1="{cx + 25}" y1="130" x2="{cx}" y2="180" stroke="#333" stroke-width="1"/>',
        480, 360)

    # Deploying-2 (half inflated)
    costumes["deploying-2"] = _svg_wrap(
        f'<path d="M{cx - 60} 120 Q{cx} 60 {cx + 60} 120 L{cx} 180Z" '
        f'fill="#CC3300" stroke="#AA2200" stroke-width="1.5"/>'
        f'<line x1="{cx - 50}" y1="118" x2="{cx}" y2="180" stroke="#333" stroke-width="1"/>'
        f'<line x1="{cx}" y1="80" x2="{cx}" y2="180" stroke="#333" stroke-width="1"/>'
        f'<line x1="{cx + 50}" y1="118" x2="{cx}" y2="180" stroke="#333" stroke-width="1"/>',
        480, 360)

    # Full open
    costumes["full-open"] = _svg_wrap(
        f'<path d="M{cx - 80} 130 Q{cx} 40 {cx + 80} 130 L{cx} 200Z" '
        f'fill="#CC3300" stroke="#AA2200" stroke-width="2"/>'
        f'<path d="M{cx - 60} 128 Q{cx} 70 {cx + 60} 128" fill="none" stroke="#FF5533" stroke-width="1" opacity="0.5"/>'
        f'<line x1="{cx - 70}" y1="130" x2="{cx}" y2="200" stroke="#333" stroke-width="1.5"/>'
        f'<line x1="{cx - 35}" y1="110" x2="{cx}" y2="200" stroke="#333" stroke-width="1.5"/>'
        f'<line x1="{cx}" y1="100" x2="{cx}" y2="200" stroke="#333" stroke-width="1"/>'
        f'<line x1="{cx + 35}" y1="110" x2="{cx}" y2="200" stroke="#333" stroke-width="1.5"/>'
        f'<line x1="{cx + 70}" y1="130" x2="{cx}" y2="200" stroke="#333" stroke-width="1.5"/>',
        480, 360)

    # Drifting frames (slight asymmetry to show movement)
    costumes["drifting-1"] = _svg_wrap(
        f'<path d="M{cx - 85} 135 Q{cx - 5} 40 {cx + 75} 125 L{cx} 200Z" '
        f'fill="#CC3300" stroke="#AA2200" stroke-width="2"/>'
        f'<line x1="{cx - 75}" y1="133" x2="{cx}" y2="200" stroke="#333" stroke-width="1.5"/>'
        f'<line x1="{cx - 35}" y1="108" x2="{cx}" y2="200" stroke="#333" stroke-width="1.5"/>'
        f'<line x1="{cx + 30}" y1="105" x2="{cx}" y2="200" stroke="#333" stroke-width="1.5"/>'
        f'<line x1="{cx + 68}" y1="128" x2="{cx}" y2="200" stroke="#333" stroke-width="1.5"/>',
        480, 360)

    costumes["drifting-2"] = _svg_wrap(
        f'<path d="M{cx - 75} 125 Q{cx + 5} 40 {cx + 85} 135 L{cx} 200Z" '
        f'fill="#CC3300" stroke="#AA2200" stroke-width="2"/>'
        f'<line x1="{cx - 68}" y1="128" x2="{cx}" y2="200" stroke="#333" stroke-width="1.5"/>'
        f'<line x1="{cx - 30}" y1="105" x2="{cx}" y2="200" stroke="#333" stroke-width="1.5"/>'
        f'<line x1="{cx + 35}" y1="108" x2="{cx}" y2="200" stroke="#333" stroke-width="1.5"/>'
        f'<line x1="{cx + 75}" y1="133" x2="{cx}" y2="200" stroke="#333" stroke-width="1.5"/>',
        480, 360)

    # Collapsed
    costumes["collapsed"] = _svg_wrap(
        f'<path d="M{cx - 40} 170 Q{cx} 160 {cx + 40} 170 L{cx + 30} 185 Q{cx} 190 {cx - 30} 185Z" '
        f'fill="#CC3300" stroke="#AA2200" stroke-width="1" opacity="0.7"/>'
        f'<line x1="{cx - 30}" y1="175" x2="{cx}" y2="165" stroke="#333" stroke-width="1" opacity="0.5"/>'
        f'<line x1="{cx + 30}" y1="175" x2="{cx}" y2="165" stroke="#333" stroke-width="1" opacity="0.5"/>',
        480, 360)

    return costumes


# ============================================================
# DEBRIS SPRITE
# ============================================================

def _debris_costumes():
    """Small debris particle costumes."""
    costumes = {}
    costumes["debris-1"] = _svg_wrap(
        '<polygon points="5,0 10,3 8,10 2,8 0,4" fill="#8B6914" stroke="#6B4914" stroke-width="1"/>', 15, 15)
    costumes["debris-2"] = _svg_wrap(
        '<polygon points="3,0 12,2 10,10 0,7" fill="#A07030" stroke="#6B4914" stroke-width="1"/>', 15, 15)
    costumes["debris-3"] = _svg_wrap(
        '<rect x="1" y="1" width="8" height="6" fill="#666" stroke="#444" stroke-width="1" transform="rotate(15 5 4)"/>', 15, 15)
    return costumes


# ============================================================
# THE END TEXT SPRITE
# ============================================================

def _theend_costumes():
    """THE END text costumes."""
    costumes = {}
    costumes["the-end"] = _svg_wrap(
        '<text x="240" y="190" text-anchor="middle" font-family="Arial, sans-serif" '
        'font-size="48" font-weight="bold" fill="white" stroke="black" stroke-width="2">'
        'THE END</text>', 480, 360)
    return costumes


# ============================================================
# MAIN FUNCTION
# ============================================================

def generate_all_svgs():
    """Return a dict of all SVGs organized by sprite/backdrop.

    Returns: {
        "backdrops": {name: svg_string, ...},
        "StickmanHero": {name: svg_string, ...},
        "CoworkerA": {name: svg_string, ...},
        "CoworkerB": {name: svg_string, ...},
        "CoworkerC": {name: svg_string, ...},
        "Computer": {name: svg_string, ...},
        "Explosion": {name: svg_string, ...},
        "Parachute": {name: svg_string, ...},
        "Debris": {name: svg_string, ...},
        "TheEnd": {name: svg_string, ...},
    }
    """
    return {
        "backdrops": {
            "office-interior": _backdrop_office_interior(),
            "building-exterior": _backdrop_building_exterior(),
            "building-with-ground": _backdrop_building_with_ground(),
        },
        "StickmanHero": _hero_costumes(),
        "CoworkerA": _coworker_costumes("coworkerA", 240, 260, 0.7),
        "CoworkerB": _coworker_costumes("coworkerB", 240, 260, 0.65),
        "CoworkerC": _coworker_costumes("coworkerC", 240, 260, 0.6),
        "Computer": _computer_costumes(),
        "Explosion": _explosion_costumes(),
        "Parachute": _parachute_costumes(),
        "Debris": _debris_costumes(),
        "TheEnd": _theend_costumes(),
    }


if __name__ == "__main__":
    svgs = generate_all_svgs()
    for category, items in svgs.items():
        print(f"{category}: {len(items)} costumes")
        for name in items:
            print(f"  - {name} ({len(items[name])} bytes)")
