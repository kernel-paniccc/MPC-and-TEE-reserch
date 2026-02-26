import json
import secrets

K = 16
SAFETY_FACTOR = 2 # Запас по тройкам в 2 раза

def gen_triple(): # Создаём саму тройку чисел
    a = secrets.randbits(1)
    b = secrets.randbits(1)
    c = a & b
    return a, b, c

def share_bit(bit): # Делим значения
    s0 = secrets.randbits(1)
    s1 = s0 ^ bit
    return s0, s1

def main(): # Шерим биты и записываем в файл
    need = 3 * K
    total_needed = int(need * SAFETY_FACTOR)
    p0, p1 = [], []
    for _ in range(total_needed):
        a,b,c = gen_triple()
        a0,a1 = share_bit(a)
        b0,b1 = share_bit(b)
        c0,c1 = share_bit(c)
        p0.append([a0,b0,c0])
        p1.append([a1,b1,c1])

    with open("triples_party0.json", "w") as f0:
        json.dump({"triples": p0}, f0)

    with open("triples_party1.json", "w") as f1:
        json.dump({"triples": p1}, f1)

    print(f" Генерация {total_needed} троек")


if __name__ == "__main__":
    main()