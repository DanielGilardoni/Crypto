import random

def test_Miller_Rabin(n, k):
    if n == 2 or n == 3:
        return True
    
    if n % 2 == 0:
        return False
    
    d = n - 1
    r = 0
    while d % 2 == 0:
        r += 1
        d //= 2
    
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def gen_premier_sophie_germain():
    n = random.randint(2, 2**10)
    while not test_Miller_Rabin(n, 10):
        n = random.randint(2, 2**10)
    
    q = 2 * n + 1
    while not test_Miller_Rabin(q, 10):
        n = random.randint(2, 2**10)
        while not test_Miller_Rabin(n, 10):
            n = random.randint(2, 2**10)
        q = 2 * n + 1
    
    return q, n

def trouver_generateur(p):
    g = random.randint(3, p - 2)
    while g**2 % p != 1 or g**((p - 1) // 2) % p != 1:
        g = random.randint(3, p - 2)
    return g

# B utilise pour générer le triplet (p, g, h)
def genB():
    p, q = gen_premier_sophie_germain()
    g = trouver_generateur(p)
    h = random.randint(2, p - 2)
    if h**q % p != 1:
        h = random.randint(2, p - 2)
    return p, g, h