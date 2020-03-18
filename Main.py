from math import sqrt
from random import randint
import numpy as np
import scipy.stats


def r(x: float) -> float:
    """Точність округлення"""
    x = round(x, 4)
    if float(x) == int(x):
        return int(x)
    else:
        return x


def par(a: float) -> str:
    """Для вивіду. Негативні числа закидає в скобки и округлює"""
    if a < 0:
        return "(" + str(r(a)) + ")"
    else:
        return str(r(a))


def average(list: list, name: str) -> int or float:
    """Середнє значення з форматованним вивідом для будь-якого листа"""
    print("{} = ( ".format(name), end="")
    average = 0
    for i in range(len(list)):
        average += list[i]
        if i == 0:
            print(r(list[i]), end="")
        else:
            print(" + ", end="")
            print(par(list[i]), end="")
    average /= len(list)
    print(" ) / {} = {} ".format(len(list), r(average)))
    return average


def printf(name: str, value: int or float):
    """Форматованний вивід змінної з округленням"""
    print("{} = {}".format(name, r(value)))


def matrixplan(xn_factor: list, x_min: int, x_max: int) -> list:
    """Заповнює матрицю планування згідно нормованої"""
    xn_factor_experiment = []
    for i in range(len(xn_factor)):
        if xn_factor[i] == -1:
            xn_factor_experiment.append(x_min)
        elif xn_factor[i] == 1:
            xn_factor_experiment.append(x_max)
    return xn_factor_experiment


def MatrixExper(x_norm: list, x_min: list, x_max: list) -> list:
    """Генеруємо матрицю планування згідно нормованної"""
    x_factor_experiment = []
    for i in range(len(x_norm)):
        if i == 0:
            continue  # x0_factor = [1, 1, 1, 1] не використовується на першому этапы
            # стовпці матриці планування (эксперементальні)
        x_factor_experiment.append(matrixplan(x_norm[i], x_min[i - 1], x_max[i - 1]))
    return x_factor_experiment


def generate_y(y_min, y_max, n, m) -> list:
    """Генерує функції відгугу за вказанним діапозоном"""
    list = []
    for i in range(m):
        list.append([randint(y_min, y_max + 1) for i in range(n)])
    return list


def a_n_funct(xn_factor_experiment: list, y_average_list: list) -> list:
    """Рахує а1, а2, а3 з форматованним вивідом"""
    a_n = []
    for i in range(len(xn_factor_experiment)):
        a_n.append(0)
        print("a{} = ( ".format(i + 1), end="")
        for j in range(len(xn_factor_experiment[i])):
            a_n[i] += xn_factor_experiment[i][j] * y_average_list[j]
            if j == 0:
                print("{}*{}".format(r(xn_factor_experiment[i][j]), par(y_average_list[j])), end="")
            else:
                print(" + {}*{}".format(par(xn_factor_experiment[i][j]), par(y_average_list[j])), end="")
        a_n[i] /= len(xn_factor_experiment[i])
        print(" ) / {} = {} ".format(len(xn_factor_experiment[i]), r(a_n[i])))
    return a_n


def a_nn_funct(xn_factor_experiment: list) -> list:
    """Рахує а11, а22, а33 з форматованим вивідом"""
    a_nn = []
    for i in range(len(xn_factor_experiment)):
        a_nn.append(0)
        print("a{}{} = ( ".format(i + 1, i + 1), end="")
        for j in range(len(xn_factor_experiment[i])):
            a_nn[i] += xn_factor_experiment[i][j] ** 2
            if j == 0:
                print("{}^2".format(par(xn_factor_experiment[i][j])), end="")
            else:
                print(" + {}^2".format(par(xn_factor_experiment[i][j])), end="")
        a_nn[i] /= len(xn_factor_experiment[i])
        print(" ) / {} = {} ".format(len(xn_factor_experiment[i]), r(a_nn[i])))
    return a_nn


def a_mn_funct(x_factor_experiment: list) -> list:
    """Рахує a12, a21, a13, a31, a23, a32"""
    a_mn = []
    list_range = [[0, 1], [1, 2], [2, 0]]

    for i, j in list_range:
        a_mn.append(0)
        print("a{}{} = ( ".format(i + 1, j + 1), end="")
        for k in range(len(x_factor_experiment[i])):
            a_mn[i] += x_factor_experiment[i][k] * x_factor_experiment[j][k]
            if k == 0:
                print("{}*{}".format(r(x_factor_experiment[i][k]), par(x_factor_experiment[j][k])), end="")
            else:
                print(" + {}*{}".format(r(x_factor_experiment[i][k]), par(x_factor_experiment[j][k])), end="")
        a_mn[i] /= len(x_factor_experiment[i])
        print(" ) / {} = {} ".format(len(x_factor_experiment[i]), r(a_mn[i])))

    return a_mn


def dispers(y: list, y_average_list: list) -> list:
    """Рахує s2 для усіх рядоків. Повертає масив значень"""
    s2_y_row = []

    for i in range(len(y_average_list)):
        s2_y_row.append(0)
        print("s2_y_row{} = ( ".format(i + 1), end="")
        for j in range(3):
            s2_y_row[i] += (y[j][i] - y_average_list[i]) ** 2
            if j == 0:
                print("({} - {})^2".format(r(y[j][i]), par(y_average_list[i])), end="")
            else:
                print(" + ({} - {})^2".format(r(y[j][i]), par(y_average_list[i])), end="")
        s2_y_row[i] /= len(y_average_list) - 1
        print(" ) / {} = {} ".format(len(y_average_list) - 1, r(s2_y_row[i])))

    return s2_y_row


def beta(x_norm: list, y_average_list: list) -> list:
    """Рахує Бета критерия Стюдента. Повертає масив значень"""
    beta_list = []

    for i in range(len(x_norm)):
        beta_list.append(0)
        print("Beta{} = ( ".format(i + 1), end="")
        for j in range(len(x_norm[i])):
            beta_list[i] += y_average_list[j] * x_norm[i][j]
            if j == 0:
                print("{}*{}".format(r(y_average_list[j]), par(x_norm[i][j])), end="")
            else:
                print(" + {}*{}".format(r(y_average_list[j]), par(x_norm[i][j])), end="")
        beta_list[i] /= len(x_norm)
        print(" ) / {} = {} ".format(len(x_norm), r(beta_list[i])))

    return beta_list


def t(beta_list: list, s_BetaS) -> list:
    """Рахує t критерія Стюдента. Повертає масив значень"""
    t_list = []
    for i in range(len(beta_list)):
        t_list.append(abs(beta_list[i]) / s_BetaS)
        print("t{} = {}/{} = {}".format(i, r(abs(beta_list[i])), par(s_BetaS), par(t_list[i])))
    return t_list


def s2_od_func(y_average_list, y_average_row_Student, m, N, d):
    """Вираховує сігму в квадраті для критерія Фішера"""
    s2_od = 0
    print("s2_od = ( ", end="")
    for i in range(len(y_average_list)):
        s2_od += (y_average_row_Student[i] - y_average_list[i]) ** 2
        if i == 0:
            print("({} - {})^2".format(r(y_average_row_Student[i]), par(y_average_list[i])), end="")
        else:
            print(" + ({} - {})^2".format(r(y_average_row_Student[i]), par(y_average_list[i])), end="")
    s2_od *= m / (N - d)
    print(" ) * {}/({} - {}) = {} ".format(m, N, d, r(s2_od)))
    return s2_od


x_min = [10, -15, -15]  # Задані за умовою значення. Варіант 206
x_max = [40, 35, 5]

x_average_min = average(x_min, "X_average_min")  # Середнє Х макс и мин
x_average_max = average(x_max, "X_average_max")  # Використ. тільки для визначення варіанту

m = 3  # За замовчуванням
q = 0.05  # рівень значимості
y_max = round(200 + x_average_max)  # Максимальні і мінімальні значення для генерації функції відгуку
printf("Y_max", y_max)
y_min = round(200 + x_average_min)
printf("Y_min", y_min)

while True:
    # Стовпці матриці планування (нормована)
    x_norm = [[1, 1, 1, 1],
              [-1, -1, 1, 1],
              [-1, 1, -1, 1],
              [-1, 1, 1, -1]]  # масив нормованої матриці

    x_factor_experiment = MatrixExper(x_norm, x_min, x_max)  # Формуємо експер. матрицю

    y = generate_y(y_min, y_max, len(x_norm), m)  # генеруємо значення функції відгуку

    y_average_list = []  # cереднє значення рядка Y
    for i in range(len(y[0])):
        y_average_list.append(average([y[j][i] for j in range(m)], "y_average_{}row".format(i + 1)))

    y_average_average = average(y_average_list, "Y_average_average")  # середнє середніх значень Y

    x_average = []  # cереднє стовпчика Х експеремент
    for i in range(len(x_factor_experiment)):
        x_average.append(average(x_factor_experiment[i], "X{}_average".format(i + 1)))

    a_n = a_n_funct(x_factor_experiment, y_average_list)  # шукаю a1,a2,a3

    a_nn = a_nn_funct(x_factor_experiment)  # шукаю a11,a22,a33

    a_mn = a_mn_funct(x_factor_experiment)  # ierf. a12, a13, a23

    # y = b0 + b1 x1 + b2 x2+ b3 x3

    # Пошук коефицієнтів регресії
    numerator = np.array([[y_average_average, x_average[0], x_average[1], x_average[2]],
                          [a_n[0], a_nn[0], a_mn[0], a_mn[2]],
                          [a_n[1], a_mn[0], a_nn[1], a_mn[1]],
                          [a_n[2], a_mn[2], a_mn[1], a_nn[2]]])

    denominator = np.array([[1, x_average[0], x_average[1], x_average[2]],
                            [x_average[0], a_nn[0], a_mn[0], a_mn[2]],
                            [x_average[1], a_mn[0], a_nn[1], a_mn[1]],
                            [x_average[2], a_mn[2], a_mn[1], a_nn[2]]])

    b0 = np.linalg.det(numerator) / np.linalg.det(denominator)
    printf("b0", b0)

    numerator = np.array([[1, y_average_average, x_average[1], x_average[2]],
                          [x_average[0], a_n[0], a_mn[0], a_mn[2]],
                          [x_average[1], a_n[1], a_nn[1], a_mn[1]],
                          [x_average[2], a_n[2], a_mn[1], a_nn[2]]])

    denominator = np.array([[1, x_average[0], x_average[1], x_average[2]],
                            [x_average[0], a_nn[0], a_mn[0], a_mn[2]],
                            [x_average[1], a_mn[0], a_nn[1], a_mn[1]],
                            [x_average[2], a_mn[2], a_mn[1], a_nn[2]]])

    b1 = np.linalg.det(numerator) / np.linalg.det(denominator)
    printf("b1", b1)

    numerator = np.array([[1, x_average[0], y_average_average, x_average[2]],
                          [x_average[0], a_nn[0], a_n[0], a_mn[2]],
                          [x_average[1], a_mn[0], a_n[1], a_mn[1]],
                          [x_average[2], a_mn[2], a_n[2], a_nn[2]]])

    denominator = np.array([[1, x_average[0], x_average[1], x_average[2]],
                            [x_average[0], a_nn[0], a_mn[0], a_mn[2]],
                            [x_average[1], a_mn[0], a_nn[1], a_mn[1]],
                            [x_average[2], a_mn[2], a_mn[1], a_nn[2]]])

    b2 = np.linalg.det(numerator) / np.linalg.det(denominator)
    printf("b2", b2)

    numerator = np.array([[1, x_average[0], x_average[1], y_average_average],
                          [x_average[0], a_nn[0], a_mn[0], a_n[0]],
                          [x_average[1], a_mn[0], a_nn[1], a_n[1]],
                          [x_average[2], a_mn[2], a_mn[1], a_n[2]]])

    denominator = np.array([[1, x_average[0], x_average[1], x_average[2]],
                            [x_average[0], a_nn[0], a_mn[0], a_mn[2]],
                            [x_average[1], a_mn[0], a_nn[1], a_mn[1]],
                            [x_average[2], a_mn[2], a_mn[1], a_nn[2]]])

    b3 = np.linalg.det(numerator) / np.linalg.det(denominator)
    printf("b3", b3)
    b_koef = [b0, b1, b2, b3]

    print("Отримане рівняння регресії: y = {} + {}*x1 + {}*x2 + {}*x3".format(r(b0), par(b1), par(b2), par(b3)))

    # Перевірка вірності складеного рівняння
    y_average_row_controls = []
    for i in range(4):
        y_average_row_controls.append(0)
        y_average_row_controls[i] = b0 + b1 * x_factor_experiment[0][i] + b2 * x_factor_experiment[1][i] + b3 * \
                                    x_factor_experiment[2][i]
        if abs(y_average_row_controls[i] - y_average_list[i]) >= 0.001:
            print(
                "\033[0m Yrow{} = {} + {}*{} + {}*{} + {}{} = \033[31m {}\t\t\t\033[0mY_average_{}row = \033[31m {}\033[0m".format(
                    i + 1, r(b0), par(b1), par(x_factor_experiment[0][i]), par(b2),
                    par(x_factor_experiment[1][i]), par(b3),
                    par(x_factor_experiment[2][i]),
                    r(y_average_row_controls[i]), i + 1, r(y_average_list[i])))
        else:
            print("Yrow{} = {} + {}*{} + {}*{} + {}{} = {}\t\t\tY_average_{}row =  {}".format(i + 1, r(b0), par(b1),
                                                                                              par(x_factor_experiment[
                                                                                                      0][
                                                                                                      i]),
                                                                                              par(b2),
                                                                                              par(x_factor_experiment[
                                                                                                      1][
                                                                                                      i]),
                                                                                              par(b3),
                                                                                              par(x_factor_experiment[
                                                                                                      2][
                                                                                                      i]),
                                                                                              r(y_average_row_controls[
                                                                                                    i]),
                                                                                              i + 1,
                                                                                              r(y_average_list[i])))
            print("Результат збігається! (точність 0.001)")

    print("Критерія Кохрена")

    s2_list = dispers(y, y_average_list)  # дисперсії по рядках

    Gp = max(s2_list) / sum(s2_list)
    print("Gp = (max(s2) / sum(s2)) = {}".format(par(Gp)))
    print("f1=m-1={} ; f2=N=4 Рівень значимості приймемо 0.05.".format(m))
    f1 = m - 1
    f2 = N = 4
    N = 4
    Gt_tableN4 = {1: 0.9065, 2: 0.7679, 3: 0.6841, 4: 0.6287, 5: 0.5892, 6: 0.5598, 7: 0.5365, 8: 0.5175, 9: 0.5017,
                  10: 0.4884}
    Gt = Gt_tableN4[f1]  # табличне значення критерію Кохрена при N=4, f1=2, рівень значимості 0.05
    printf("Gt", Gt)
    if Gp <= Gt:
        Krit_Kohr = "Однор" + " m=" + str(m)
        print("Дисперсія однорідна")
        break
    else:
        Krit_Kohr = "Не однор."
        print("Дисперсія неоднорідна\n\n\n\n")
        print("m+1")
        m += 1
        if m > 10:
            print("Недостатньо інформації для обчислення.")
            quit()

print("Далі оцінимо значимість коефіцієнтів регресії згідно критерію Стьюдента")

s2_B = sum(s2_list) / len(s2_list)
printf("s2_B", s2_B)

s2_BetaS = s2_B / (N * m)
printf("s2_BetaS", s2_BetaS)

s_BetaS = sqrt(s2_BetaS)
printf("s_betaS", s_BetaS)

beta_list = beta(x_norm, y_average_list)  # значенння B0, B1, B2, B3

t_list = t(beta_list, s_BetaS)  # t0, t1, t2, t3

f3 = (m - 1) * N  # N завжди 4
# print("T_tab:", t_tab)
t_tabl = scipy.stats.t.ppf((1 + (1 - q)) / 2, f3)  # табличне значення за критерієм Стюдента
printf("t_tabl", t_tabl)

b_list = []
print("Утворене рівняння регресії: Y = ", end="")
for i in range(len(t_list)):
    b_list.append(0)
    if t_list[i] > t_tabl:
        b_list[i] = b_koef[i]
        if i == 0:
            print("{}".format(r(b_koef[i])), end="")
        else:
            print(" + {}*X{}".format(par(b_koef[i]), i), end="")
print()

# Порівняння результатів
y_average_row_Student = []
dodanki = []
for i in range(4):
    for j in range(len(b_list)):
        if j == 0:
            dodanki.append("{}".format(r(b_list[j])))
        else:
            if b_list[j] == 0:
                dodanki.append("")
            else:
                dodanki.append(" + {}*{}".format(par(b_list[j]), x_factor_experiment[j-1][i]))
    y_average_row_Student.append(0)
    y_average_row_Student[i] = b_list[0] + b_list[1] * x_factor_experiment[0][i] + b_list[2] * x_factor_experiment[1][i] \
                               + b_list[3] * x_factor_experiment[2][i]

    if abs(y_average_row_Student[i] - y_average_list[i]) >= 20:
        print("Yrow{} = {}{}{}{} = \033[31m {}\t\t\t\033[0mY_average_{}row = \033[31m {}\033[0m".format(
            i + 1, dodanki[0], dodanki[1], dodanki[2], dodanki[3],
            r(y_average_row_Student[i]), i + 1, r(y_average_list[i])))
    elif abs(y_average_row_Student[i] - y_average_list[i]) >= 10:
        print("Yrow{} = {}{}{}{} = {}\t\t\tY_average_{}row =  {}".format(
            i + 1, dodanki[0], dodanki[1], dodanki[2], dodanki[3],
            r(y_average_row_Student[i]), i + 1, r(y_average_list[i])))
        print("Результат приблизно (+-10) збігається! (Рівень значимості 0.05)")
    else:
        print("Yrow{} = {}{}{}{} = {}\t\t\tY_average_{}row =  {}".format(
            i + 1, dodanki[0], dodanki[1], dodanki[2], dodanki[3],
            r(y_average_row_Student[i]), i + 1, r(y_average_list[i])))
        print("Результат приблизно (+-10) збігається! (Рівень значимості 0.05)")
    dodanki.clear()
print("Критерій Фішера")
d = b_list.count(0)
f4 = N - d
s2_od = s2_od_func(y_average_list, y_average_row_Student, m, N, d)

Fp = s2_od / s2_B
print("Fp = {} / {} = {}".format(r(s2_od), par(s2_B), r(Fp)))

# Ft = 4.5  # для f3=8; f4=2
F_table = scipy.stats.f.ppf(1 - q, f4, f3)
printf("F_table", F_table)

if Fp > F_table:
    print("За критерієм Фішера рівняння регресії неадекватно оригіналу при рівні значимості 0.05")
    Krit_Fish = "Не адекв."
else:
    print("За критерієм Фішера рівняння регресії адекватно оригіналу при рівні значимості 0.05")
    Krit_Fish = "Адекв."

"""Таблиця з головными результатами розрахунків"""
print("\nТаблиця результату:")

for j in range(4):
    print("|{: ^11}|".format("x" + str(j) + "factor"), end="")
for j in range(3):
    print("|{: ^11}|".format("x" + str(j + 1)), end="")
for j in range(m):
    print("|{: ^11}|".format("y" + str(j + 1)), end="")
print("|{: ^11}||{: ^11}||{: ^11}||{: ^11}||{: ^11}|"
      .format("Y_mid", "Y_mid_exp", "Стьюдент", "Krit_Kohr", "Krit_Fish"))
print("{:-^195}".format("-"))
for i in range(4):
    for j in range(4):
        print("|{: ^11}|".format(x_norm[j][i]), end="")
    for j in range(3):
        print("|{: ^11}|".format(x_factor_experiment[j][i]), end="")
    for j in range(m):
        print("|{: ^11}|".format(y[j][i]), end="")
    print("|{: ^11}||{: ^11}||{: ^11}|".format(r(y_average_list[i]), r(y_average_row_controls[i]),
                                               r(y_average_row_Student[i])), end="")
    if i == 0:
        print("|{: ^11}||{: ^11}|".format(Krit_Kohr, Krit_Fish), end="")
    print()
