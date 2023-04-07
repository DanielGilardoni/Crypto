import random

def is_prime(n):
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n**0.5)+1, 2):
        if n % i == 0:
            return False
    return True

def polynome(a, x):
    y = 0
    for i in range(len(a)):
        y += a[i] * (x**i)
    return y

# retourne un nombre premier p adapté et les coefficients du polynome
def generate(m, k):
    p = random.randint(m, 2**(m+1)) # nombre premier
    while not is_prime(p):
        p = random.randint(m, 2**(m+1))

    a = [] # coefficients du polynome
    for i in range(k-1):
        a.append(random.randint(1, p-1))

    return p, a

# génère les parts de secret si pour les agents
def distribute(m, k, g, s):
    res = []
    p, a = g
    new_a = [s] + a
    print(new_a)
    for i in range(1,m+1):
        res.append((i, polynome(new_a, i) % p))
    return res

def coalition(p, k, agents):
    k = len(agents) - 1
    x_values = [agents[i][0] for i in range(k+1)]
    y_values = [agents[i][1] for i in range(k+1)]
    secret = 0
    for j in range(k+1):
        term = y_values[j]
        for i in range(k+1):
            if i != j:
                term *= (0 - x_values[i]) * pow(x_values[j] - x_values[i], -1, p)
        secret += term % p
    return secret % p

m = 10
k = 10
gen = generate(m, k)
secret = 157 % gen[0]
print(secret)
dis = distribute(m, k, gen, secret)
coal = coalition(gen[0], 3, dis)
print(coal)
print(secret == coal)