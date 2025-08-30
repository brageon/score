import math
import pandas as pd

def ngon_analysis(weights, vertices=None):
    """
    Compute N-gon properties from barycentric weights.

    :param weights: list/tuple of N percentages (w1,...,wN)
    :param vertices: list of N (x,y) coordinates. Default: regular polygon on unit circle
    """
    N = len(weights)
    total_w = sum(weights)
    w_norm = [w/total_w for w in weights]

    # Default vertices: regular N-gon on unit circle
    if vertices is None:
        vertices = [(math.cos(2*math.pi*i/N), math.sin(2*math.pi*i/N)) for i in range(N)]

    # Centroid of polygon
    Gx = sum(v[0] for v in vertices)/N
    Gy = sum(v[1] for v in vertices)/N
    G = (Gx, Gy)

    # Weighted barycentric point
    Px = sum(w*v[0] for w,v in zip(w_norm, vertices))
    Py = sum(w*v[1] for w,v in zip(w_norm, vertices))
    P = (Px, Py)

    # Approximate total area using shoelace formula (for polygon)
    area = 0
    for i in range(N):
        x1, y1 = vertices[i]
        x2, y2 = vertices[(i+1)%N]
        area += (x1*y2 - x2*y1)
    area = 0.5*abs(area)

    # Dominance metric $
    PG = math.dist(P, G)
    VGmax = max(math.dist(v, G) for v in vertices)
    dominance = PG / VGmax

    # Angle $ from centroid to P
    theta = math.degrees(math.atan2(Py - Gy, Px - Gx))

    # Sub-areas approximation (weight × total area)
    sub_areas = {f'V{i+1}': w*area for i,w in enumerate(w_norm)}

    return {
        'Weights': weights,
        'Vertices': vertices,
        'Total area': area,
        'Px': Px,
        'Py': Py,
        'Centroid': G,
        'Dominance': dominance,
        'Angle': theta,
        'Sub-areas': sub_areas }

inputs = [
    (25, 14, 29, 17, 50, 29), 
    (14, 50, 67, 14, 75) ]

results = [ngon_analysis(w) for w in inputs]

df = pd.DataFrame(results)
print(df)
