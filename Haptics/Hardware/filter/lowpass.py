import math


def calc_L(f0, C):
    return 1 / (4 * (math.pi**2) * (f0**2) * C)


def calc_R(L, C):
    return (2 * L / C) ** 0.5


if __name__ == "__main__":
    f0 = float(input("Enter f0 (Hz): "))
    C = float(input("Enter C (F): "))
    L = calc_L(f0, C)
    R = calc_R(L, C)
    print("L = {:.3f} mH".format(L * 1000))
    print("R = {:.3f} Ohm".format(R))
    print("C = {:.3f} uF".format(C * 1000000))
