#!/usr/bin/env python3
"""Fix y="NaN" in excalidraw-to-svg output.

excalidraw-to-svg wraps each text element in:
  <g transform="translate(x y) rotate(0 halfW halfH)">
    <text x="halfW" y="NaN" ...>text</text>
  </g>

The translate positions to the element's top-left. The text x is centered
at halfW. We need y to be the vertical baseline within the element height.
halfH = elementHeight / 2. For proper centering:
  y = halfH + fontSize * 0.35  (approximate ascent for middle alignment)
"""

import re, sys


def fix_svg(path):
    with open(path) as f:
        svg = f.read()

    def fix_text_y(m):
        full = m.group(0)
        # Extract halfH from the rotate transform in the parent <g>
        rotate_match = re.search(r'rotate\(0\s+[\d.]+\s+([\d.]+)\)', full)
        # Extract font-size
        fs_match = re.search(r'font-size="([\d.]+)px"', full)

        if rotate_match and fs_match:
            half_h = float(rotate_match.group(1))
            fs = float(fs_match.group(1))
            # Center text vertically: baseline at center + ~35% of font size
            y = half_h + fs * 0.35
        elif fs_match:
            fs = float(fs_match.group(1))
            y = fs * 0.85
        else:
            y = 12

        return full.replace('y="NaN"', f'y="{y:.1f}"')

    # Match each <g> containing text with y="NaN"
    # Handle both single-text and multi-text groups
    svg = re.sub(
        r'<g\s+transform="translate[^"]*"[^>]*>(?:<text[^<]*</text>\s*)+</g>',
        lambda m: fix_group(m.group(0)),
        svg
    )

    # Fallback: fix any remaining standalone y="NaN"
    svg = re.sub(
        r'(<text\s[^>]*?)y="NaN"([^>]*>)',
        lambda m: fix_standalone(m),
        svg
    )

    with open(path, 'w') as f:
        f.write(svg)
    print(f"Fixed {path}")


def fix_group(group_html):
    """Fix all y="NaN" text elements within a <g> group."""
    rotate_match = re.search(r'rotate\(0\s+[\d.]+\s+([\d.]+)\)', group_html)
    half_h = float(rotate_match.group(1)) if rotate_match else None

    # Find all text elements in this group
    texts = list(re.finditer(r'<text\s([^>]*?)y="NaN"([^>]*?)>([^<]*)</text>', group_html))
    if not texts:
        return group_html

    result = group_html
    n_texts = len(texts)

    for idx, tm in enumerate(texts):
        fs_match = re.search(r'font-size="([\d.]+)px"', tm.group(0))
        fs = float(fs_match.group(1)) if fs_match else 14

        if half_h is not None:
            if n_texts == 1:
                # Single text: center vertically using dominant-baseline
                y = half_h
            else:
                # Multiple texts (multiline): distribute evenly
                line_h = fs * 1.2
                total_h = n_texts * line_h
                start_y = half_h - total_h / 2 + fs * 0.5
                y = start_y + idx * line_h
        else:
            y = fs * 0.5

        old = tm.group(0)
        new = old.replace('y="NaN"', f'y="{y:.1f}" dominant-baseline="central"')
        result = result.replace(old, new, 1)

    return result


def fix_standalone(m):
    """Fix a standalone <text> y="NaN" not in a group."""
    prefix = m.group(1)
    suffix = m.group(2)
    fs_match = re.search(r'font-size="([\d.]+)px"', suffix)
    fs = float(fs_match.group(1)) if fs_match else 14
    y = fs * 0.5
    return f'{prefix}y="{y:.1f}" dominant-baseline="central"{suffix}'


if __name__ == "__main__":
    for p in sys.argv[1:]:
        fix_svg(p)
