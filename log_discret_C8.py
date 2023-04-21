import math

p = 22091
gen = 2
y = 12345

def naive_logarithm(g, y, p):
    x = 1
    for i in range(1, p):
        x = (x * g) % p
        if x == y:
            return i
    
    return None

def discrete_logarithm(g, y, p):
    t = math.ceil(math.sqrt(p))
    table = {}
    for i in range(t):
        table[(g**i) % p] = i
    
    g_inv = (g**(p - 2)) % p
    g_t = (g_inv**t) % p
    for i in range(t):
        if y in table:
            return i * t + table[y]
        y = (y * g_t) % p
    return None

res = naive_logarithm(gen, y, p)
dis_log = discrete_logarithm(gen, y, p)
print(res, dis_log)
print((gen**res) % p, (gen**dis_log) % p)