import matplotlib.pyplot as plt

_, ax = plt.subplots()

midpoint = lambda p1, p2: ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)

draw = lambda p: ax.fill([p[0][0], p[1][0], p[2][0]], [p[0][1], p[1][1], p[2][1]], color = 'blue')

def sierpinski_trianlges_gen(points, depth, callback):
    if depth == 0:
        callback(points)
        return

    sierpinski_trianlges_gen([points[2], midpoint(points[2], points[0]), midpoint(points[1], points[2])], depth - 1, callback)
    sierpinski_trianlges_gen([points[1], midpoint(points[1], points[0]), midpoint(points[1], points[2])], depth - 1, callback)
    sierpinski_trianlges_gen([points[0], midpoint(points[1], points[0]), midpoint(points[0], points[2])], depth - 1, callback)


if __name__ == "__main__":
    sierpinski_trianlges_gen([(0.5, 1), (0, 0), (1, 0)], 3, draw)
    plt.show() 
