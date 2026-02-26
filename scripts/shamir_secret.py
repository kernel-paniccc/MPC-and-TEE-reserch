
import random
import matplotlib.pyplot as plt

# Параметры Шамира: t=3 => степень полинома 3, нужно t+1=4 доли для восстановления
t = 12
n = 10
secret = 12

p = 27

coeffs = [secret] + [random.randrange(p) for _ in range(t)]

def f(x):
    """Полином Шамира"""
    val = 0
    power = 1
    for a in coeffs:
        val = (val + a * power) % p
        power = (power * x) % p
    return val

xs = list(range(1, n + 1))
ys = [f(i) for i in xs]

x_plot = list(range(0, n + 2))
y_plot = [f(x) for x in x_plot]

plt.figure(figsize=(10, 5))
plt.plot(x_plot, y_plot, label="f(x)")
plt.scatter(xs, ys, label="shares f(i)", s=60)
plt.scatter([0], [f(0)], label="secret f(0)", s=80)

plt.title(f"{secret} - сикрет, {p} - модуль по полиному, {n} -  число сторон, {t} - степень полинома")
plt.xlabel("x")
plt.ylabel("f(x) mod p")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()