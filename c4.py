import random

key = ["0", "4", "8", "12"] # Il y a pas 16 hex au lieu de 16 bits ? Voir version original et chat gtp
a = random.randint(0,400000)
print(a)
mes = hex(a)

def cut_mes(m): # m en hex -> on retourne un tab de la forme [[hex][hex][hex][hex]][...]
    # print(m)
    m = [i for i in m[2:]] # On ne prends pas en compte "0x"
    m = [m[i:i+4] for i in range(0, len(m), 4)] # On fait tableau de tableau, ds chaque cas 16 bits sous forme de 4 case contenant un hex
    # print(m)
    last_elem_len = len(m[-1])
    if last_elem_len < 4:
        last = hex((4 - last_elem_len))   # Le nombre de hex ajouté
        m[-1] += [last[2:]] * (4 - last_elem_len) # On ajoute last hex dans le dernier tab de 16 bits
        m += [[last[2:]] * 4] # Puis on ajoute 16 bits, de 4 hex de valeur last
    else:
        m += [[hex(0)[2:]] * 4]
    print(m) # On aura ajouté au moins 16 bits qu'il faudra supprimé et qui indiquent le nbr de hex à enlevé en plus
    return m

# On reconstitue le message à partir d'un tableaux des morceaux du messages
def uncut_mes(m): # On supprime les 16 derniers bits donc la derniere case, et dans l'avant derniere case on supprime a cases car a indique le nombre de hex qui ont été ajoutés
    a = 4 - m[-1][-1]
    m = m.pop()
    m[-1] = m[-1][:-a]
    new_m = ""
    for elem in m:
        for i in elem:
            new_m.append(i)
    return new_m

def P(l):   
    # # Créer la liste de la permutation
    # perm = [1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15, 4, 8, 12, 16]
    # # Initialiser la liste de bits de sortie
    # nouvelle_liste = [0] * 16  # Créer une liste de même taille avec des zéros, 4 c'est len(l) car on veut chiffrer des morceaux de 16 bits

    # l = uncut_mes(l)
    # # Appliquer la permutation aux bits d'entrée
    # for i in range(16):
    #     nouvelle_liste[i] = l[perm[i]-1]
    # nouvelle_liste = [nouvelle_liste[i:i+4] for i in range(0, len(nouvelle_liste), 4)]
    # return nouvelle_liste

    
    l = uncut_mes(l)
    nouvelle_liste = [0] * len(l)  # Créer une liste de même taille avec des zéros

    for i, valeur in enumerate(l):
        # Trouver la nouvelle position de la valeur
        nouvelle_position = (i // 4) + (i % 4) * 4
        
        # Affecter la valeur à la nouvelle position
        nouvelle_liste[nouvelle_position] = valeur
    
    nouvelle_liste = [nouvelle_liste[i:i+4] for i in range(0, len(nouvelle_liste), 4)]

    return nouvelle_liste

substitution = {
    '0': 'e',
    '1': '4',
    '2': 'd',
    '3': '1',
    '4': '2',
    '5': 'f',
    '6': 'b',
    '7': '8',
    '8': '3',
    '9': 'a',
    'a': '6',
    'b': 'c',
    'C': '5',
    'd': '9',
    'e': '0',
    'f': '7'
}

def inv_S(entree):
    substitution = [
        0xE, 0x3, 0x4, 0x8, 0x1, 0xC, 0xA, 0xF, 0x7, 0xD, 0x9, 0x6, 0xB, 0x2, 0x0, 0x5
    ]  # Table de substitution

    # Extraire les 4 bits de poids faible
    index = entree & 0b1111

    # Substituer les 4 bits avec la table de substitution
    decimal = substitution[index]

    # Convertir la sortie décimale en hexadécimal
    # sortie_hex = hex(decimal)[2:].upper()

    return decimal

def F(k, decalage):
    k = k[-decalage:] + k[:-decalage]
    return k

def xor_4_bits(a, b): # a du message et b de la clef sous forme de 4 bits 
    # print("xor")
    # print(type(a))
    bin_a = bin(int(a, 16))[2:].zfill(4) # On convertit a en int de 0 à 15 puis en binaire avec bin 
    # Puis on enleve "0b" avec [2:] puis avec zfill(4) on s'assure que on ai bien 4 bits en ajoutant des 0 au debut si nécéssaire.
    # print(type(b))
    bin_b = bin(int(b, 16))[2:].zfill(4)

    res = ""

    for i in range(4):
        if bin_a[i] != bin_b[i]: 
            res += "1"
        else: res += "0"
    
    return hex(int(res,2))[2:]

def chiffre(m, k): #Fait le xor bit par bit sur chaque elem qui fait 4 bits
    for i in range(0,4): # decomposé en 4, x1..x4
        m[i] = xor_4_bits(m[i], k[i])
        # m[i][j] = (m[i][j] + k[i][j])%16   # Ici k est Ki car on a appelé F avant
    return m

def dechiffre(m, k):
    for i in range(0,4):
        for j in range(0,4):
            m[i][j] = (m[i][j] - k[i][j])%16
    return m

def chiffrement(m, k):
    l = cut_mes(m)    
    print("Chiffrement...")
    print(l)
    for j in range(0,len(l)):
        elem = l[j]
        print(elem)
        # elem = [elem[i:i+4] for i in range(0, len(elem), 4)]
        print(elem)
        for i in range(0,4): # On met en bits pour faire XOR
            elem = chiffre(elem, F(k, i))
            # elem = uncut_mes(elem) # On remets sous forme hexa en gros, avec 4 xi de 4 bits
            for i in range(0,4):
                elem[i] = substitution[elem[i]] # On applique la substitution sur chaque xi
            elem = [elem[i:i+4] for i in range(0, len(elem), 4)] # On les remets sous formes de bits 
            elem = P(elem) # et on applique permutation
        elem = uncut_mes(elem)
        l[j] = elem
    l = uncut_mes(l)
    return l

def dechiffrement(m, k):
    l = cut_mes(m)
    for j in range(0,len(l)):
        elem = l[j]
        elem = [elem[i:i+4] for i in range(0, len(elem), 4)]
        index = 3
        while index >= 0:
            elem = P(elem)
            elem = uncut_mes(elem)
            for i in range(0,16):
                elem[i] = inv_S(elem[i])
            elem = [elem[i:i+4] for i in range(0, len(elem), 4)]
            elem = dechiffre(elem, F(k, index))
            index -= 1
        l[j] = elem
    
    l = uncut_mes(l)
    return l

def to_hex(l):
    hex_l = [0x0 for i in range(0,len(l))]
    for i in range(0,len(hex_l)):
        hex_l[i] = hex(l[i])[2:].upper()
    return hex_l

res = mes 
# print(cut_mes(res))
# print(key)
crypt = chiffrement(res, key)
print("on passe le chiffrement")
print(to_hex(crypt))
decrypt = uncut_mes(dechiffrement(crypt, key))
print(to_hex(decrypt))
# print(res == decrypt)
# print(crypt == decrypt)
# print(res == crypt)








# mes = [random.randrange(0,2) for i in range(0,a)] # le mess devrait être en bits non ?
# Découpe le message en un tableau avec des morceaux de 16 bits 
# Si le message ne fait pas 16k bits cela pose problème
# On pourrait crypter de la même maniére avec seulements les premiers bits de la clef pour la fin du message mais ce n'est pas ce qui est demandé je pense
# Donc on va ajouter des bits pour qu'il fasse 16k bits.
# On va ensuite pour tous les messages ajouté 2 octets (16 bits) qui représenteront le nombre de bits ajoutés.
# Donc pour le dechiffrement il faudra toujours enlever les 2 derniers octets + le nbr de bits designé par ces 2 octets
# Par ex message de 14 bits, on ajoute 2bits 0, puis (0000000000000010)=2. Et dans dechiffrement on enlévera les 16+2 derniers bits 