import pandas as pd
import colour
import numpy as np

# ---- Load CSV of HEX colors ----
# CSV should have a column named 'HEX'
df = pd.read_csv("hex.csv")

def hex_to_rgb(hex_color):
    hex_color = hex_color.strip('#')
    return tuple(int(hex_color[i:i+2], 16)/255.0 for i in (0, 2, 4))

def hex_to_lab(hex_color):
    rgb = hex_to_rgb(hex_color)
    xyz = colour.sRGB_to_XYZ(rgb)
    lab = colour.XYZ_to_Lab(xyz)
    return lab

df['Lab'] = df['HEX'].apply(hex_to_lab)
target_hex = "#eaf2ee"
target_lab = hex_to_lab(target_hex)

# ---- Compute DeltaE (CIE2000) ----
def delta_e(row):
    return colour.delta_E(row['Lab'], target_lab, method='CIE 2000')

df['DeltaE'] = df.apply(delta_e, axis=1)
closest = df.loc[df['DeltaE'].idxmin()]

print("Closest HEX:", closest['HEX'])
print("DeltaE:", closest['DeltaE'])
