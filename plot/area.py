import math

def triangle_analysis(weights, A=(0,0), B=(1,0), C=(0.5, math.sqrt(3)/2)):
    """
    Compute triangle properties from barycentric weights.
    
    :param weights: tuple/list of three percentages (wA, wB, wC)
    :param A,B,C: vertices of the triangle as (x,y)
    """
    # 1. Normalize weights
    total_w = sum(weights)
    wA, wB, wC = [w/total_w for w in weights]

    # 2. Compute total area using shoelace formula
    def area_triangle(A, B, C):
        return 0.5 * abs(A[0]*(B[1]-C[1]) + B[0]*(C[1]-A[1]) + C[0]*(A[1]-B[1]))
    T = area_triangle(A,B,C)

    # 3. Compute barycentric point P
    Px = wA*A[0] + wB*B[0] + wC*C[0]
    Py = wA*A[1] + wB*B[1] + wC*C[1]
    P = (Px, Py)

    # 4. Compute centroid G
    Gx = (A[0]+B[0]+C[0])/3
    Gy = (A[1]+B[1]+C[1])/3
    G = (Gx, Gy)

    # 5. Dominance metric
    PG = math.dist(P, G)
    VGmax = max(math.dist(A,G), math.dist(B,G), math.dist(C,G))
    dominance = PG / VGmax

    # 6. Angle from centroid to P
    theta = math.degrees(math.atan2(P[1]-G[1], P[0]-G[0]))

    # 7. Subtriangle areas (weights × total area)
    sub_areas = {
        'Not A': f"{wA*T:.8f}",
        'Not B': f"{wB*T:.8f}",
        'Not C': f"{wC*T:.8f}" }

    return {
        'Total area': T,
        'Point Px': Px,
        'Point Py': Py,
        'Centroid G': G,
        'Dominance': dominance,
        'Angle from centroid': theta,
        'Sub-areas': "\n".join([f"{k}: {v}" for k, v in sub_areas.items()])
    }

weights = (17, 67, 14)
result = triangle_analysis(weights)
for k,v in result.items():
    print(f"{k}: {v}")
