import matplotlib.pyplot as plt

# Функция поиска средней точки между p1 и p2
midpoint = lambda p1, p2: ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)

# Функция отрисовки треугольника по 3 точкам
# plot.fill принимает последовательность X и последовательность Y
draw = lambda p, plot: plot.fill([p[0][0], p[1][0], p[2][0]], [p[0][1], p[1][1], p[2][1]], color = 'blue')

# Рекурсивная функция поиска точек треугольника Серпинского
def sierpinski_trianlges_gen(points, depth, callback, plot):
    # Когда достигли самой глубокой точки - обратный вызов
    if depth == 0:
        callback(points, plot)
        return

    # Для каждого треугольника вычисляем координаты точек трех "подтреугольников"
    sierpinski_trianlges_gen([points[2], midpoint(points[2], points[0]), 
                              midpoint(points[1], points[2])], depth - 1, callback, plot)
    sierpinski_trianlges_gen([points[1], midpoint(points[1], points[0]), 
                              midpoint(points[1], points[2])], depth - 1, callback, plot)
    sierpinski_trianlges_gen([points[0], midpoint(points[1], points[0]), 
                              midpoint(points[0], points[2])], depth - 1, callback, plot)


if __name__ == "__main__":
    _, plot = plt.subplots()
    sierpinski_trianlges_gen([(0.5, 1), (0, 0), (1, 0)], 2, draw, plot)
    plt.show() 
