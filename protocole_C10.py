import random
import math
from Crypto.Util.number import *

def gen_premier_sophie_germain():
    n = getPrime(2**4)
    
    q = 2 * n + 1
    while not isPrime(q):
        n = getPrime(2**4)
        q = 2 * n + 1
    
    return q, n

def trouver_generateur(p):
    q = p - 1
    factors = []
    for i in range(2, int(math.sqrt(q))+1):
        if q % i == 0:
            factors.append(i)
            while q % i == 0:
                q //= i
        if q > 1:
            factors.append(q)

    for g in range(2, p):
        if all(pow(g, (p-1)//f, p) != 1 for f in factors):
            return g
    return None

def prime_factors(n):
    factors = []
    while n % 2 == 0:
        factors.append(2)
        n //= 2
    for i in range(3, int(n**0.5)+1, 2):
        while n % i == 0:
            factors.append(i)
            n //= i
    if n > 2:
        factors.append(n)
    return factors

# B utilise pour générer le triplet (p, g, h)
def genB():
    p, q = gen_premier_sophie_germain()
    g = trouver_generateur(p)
    h = random.randint(2, p - 2)
    while h**q % p != 1:
        h = random.randint(2, p - 2)
    return p, g, h

# A vérifie le triplet (p, g, h)
def verifA(triplet):
    p, g, h = triplet

    if not isPrime(p) or not isPrime((p-1)//2):
        return False

    if pow(g, p-1, p) != 1:
        return False
    for f in prime_factors(p-1):
        if pow(g, (p-1)//f, p) == 1:
            return False
    
    q = (p - 1) // 2
    if pow(h, q, p) != 1:
        return False
        
    return True

def commitA(triplet, xy):
    p, g, h = triplet
    x, y = xy
    c = (pow(g, 2*y, p) * pow(h, x, p)) % p
    return c

def revealA(xy):
    return xy

def verifB(triplet, c, xy):
    p, g, h = triplet
    x, y = xy
    if c == pow(g, 2*y, p) * pow(h, x, p) % p:
        return True
    return False

gen_b = genB()
print(gen_b)
print(verifA(gen_b))

xy = (random.randint(2, gen_b[0]-1), random.randint(2, gen_b[0]-1))
print(revealA(xy))

c = commitA(gen_b, xy)
print(c)

print(verifB(gen_b, c, xy))