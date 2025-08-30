import colorsys

def n_gon_to_hex(dominance, angle, brightness=0.95):
    """
    Convert dominance & angle to pastel HEX color.
    - dominance: 0-1 (strength, mapped to saturation)
    - angle: degrees (-180 to 180 or 0-360)
    - brightness: value for HSV (0-1)
    """
    hue = (angle % 360) / 360.0  # 0-1 range
    saturation = min(max(dominance * 0.5, 0), 1)
    r, g, b = colorsys.hsv_to_rgb(hue, saturation, brightness)
    return '#%02x%02x%02x' % (int(r*255), int(g*255), int(b*255))

hex_color_0 = n_gon_to_hex(0.199643, -107.783651) 
hex_color_1 = n_gon_to_hex(0.067558, 150.245350) 

print("Row 0 HEX:", hex_color_0)
print("Row 1 HEX:", hex_color_1)
