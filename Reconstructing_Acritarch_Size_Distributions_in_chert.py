import math

T = float(input("Enter thickness of the rock section (μm): "))
m = float(input("Enter minimum value of all bins (μm): "))
n = int(input("Enter number of bins: "))
i = float(input("Enter width of bins (μm): "))
D = list(map(float, input("Enter data for all bins separated by spaces: ").split()))

if len(D) != n:
    print("The number of input values does not match the number of bins.")
else:
    P = [D[j] / sum(D) for j in range(n)]
    mid_values = [m + (j + 0.5) * i for j in range(n)]
    G = [math.sqrt((mid_values[j] ** 2 - m ** 2) / 4) for j in range(n)]

    E = []
    for j in range(n):
        bin_E = []
        for k in range(j + 1):
            min_k = m + k * i
            E_jk = (2 * G[j] - math.sqrt(mid_values[j] ** 2 - min_k ** 2)) / (T + 2 * G[j])
            bin_E.append(E_jk)
        E.append(bin_E)

    U = []
    for j in range(n):
        bin_U = []
        for k in range(j):
            bin_U.append(E[j][k + 1] - E[j][k])
        bin_U.append(1 - E[j][-1])
        U.append(bin_U)

    X = [0] * n
    X[-1] = P[-1] / U[-1][-1]
    for j in range(n - 2, -1, -1):
        numerator = P[j]
        for k in range(j + 1, n):
            numerator -= X[k] * U[k][j]
        X[j] = numerator / U[j][j]
        if X[j] < 0:
            X[j] = 0

    F_sum = sum(X)
    F = [x / F_sum for x in X] if F_sum > 0 else [0] * n

    print("Transformed histogram data:")
    print("\n".join(map(str, F)))