import random

# Un tableau d'entier entre 0 et 15 convertit en un chiffre de 16 bits
def tab_int_to_bin(mes_int):
    mes_bin = ''.join(format(entier, '04b') for entier in mes_int)
    return mes_bin

# Un chiffre de 16 bits convertit en tableau d'entier entre 0 et 15
def bin_to_tab_int(mes_bin):
    mes_int = [int(mes_bin[i:i+4], 2) for i in range(0, len(mes_bin), 4)]
    return mes_int

# Un texte convertit en binaire (chaque caractère est encodé sur 16 bits)
def text_to_bin(txt):
    mes_bin = ''.join( [format(ord(c), '016b') for c in txt] )
    # ord() pour convertir caractére en code ascii et convertion sur 16 bits avec format()
    return mes_bin


# Cette fonction permet de convertir un tableau d'entier entre 0 et 15 en un texte
# Attention cette fonction n'est utilisé que pour afficher le résultat du décryptage, 
# elle ne peut pas convertir n'importe quel tableau en texte
def tab_int_to_text(mes_int):
    mes_bin = tab_int_to_bin(mes_int)
    mes = ''.join([chr( int(mes_bin[i:i+16], 2) ) for i in range(0, len(mes_bin), 16)])
    return mes

# Convertit le texte en un tableau d'entiers entre 0 et 15
def text_to_tab_int(txt):
    # On convertit le message en binaire :
    mes_bin = text_to_bin(txt)
    # On convertit en tab de int entre 0 et 15 :
    mes_int = bin_to_tab_int(mes_bin)
    return mes_int
    
# from [1, 2, 3, 4, 5, 6, 7, 8] to [[1, 2, 3, 4], [5 6 7 8]]
def cut_mes(m):
    m = [m[i:i+4] for i in range(0, len(m), 4)]
    return m

# inverse de cut
def uncut_mes(m):
    new_m = []
    for elem in m:
        for i in elem:
            new_m.append(i)
    return new_m

# La permutation
def P(l):
    bin = tab_int_to_bin(l) # convertit tab de 4 int entre 0 et 15 en 16 bits
    permutation = [0, 4, 8, 12, 1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15]
    perm = ''.join([bin[permutation[i]] for i in range(16)]) # On applique la permutation
    p = bin_to_tab_int(perm) # On reconvertit en tab de 4 int entre 0 et 15
    return p

# Substitution
def S(entree):
    substitution = [
        0xE, 0x4, 0xD, 0x1, 0x2, 0xF, 0xB, 0x8, 0x3, 0xA, 0x6, 0xC, 0x5, 0x9, 0x0, 0x7
    ]  # Table de substitution

    # Extraire les 4 bits de poids faible
    index = entree & 0b1111

    # Substituer les 4 bits avec la table de substitution
    decimal = substitution[index]

    # Convertir la sortie décimale en hexadécimal
    # sortie_hex = hex(decimal)[2:].upper()

    return decimal

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

def chiffre(m, k):
    for i in range(0,4):
        m[i] = m[i] ^ k[i] # XOR
    return m

def dechiffre(m, k):
    for i in range(0,4):
        m[i] = m[i] ^ k[i]
    return m

def chiffrement(m, k):
    l = cut_mes(m)
    for j in range(0,len(l)):
        elem = l[j]
        for i in range(0,4):
            elem = chiffre(elem, F(k, i))
            for i in range(0,4):
                elem[i] = S(elem[i])
            elem = P(elem)
        l[j] = elem
    l = uncut_mes(l)
    return l

def dechiffrement(m, k):
    l = cut_mes(m)
    for j in range(0,len(l)):
        elem = l[j]
        index = 3
        while index >= 0:
            elem = P(elem)
            for i in range(0,4):
                elem[i] = inv_S(elem[i])
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


####### Initialisation #############
message = input("Quel texte souhaitez vous crypter ?\nEntrez votre texte:\n")
    ## On convertit le message en un tableau d'entier entre 0 et 15 :
mes_int = text_to_tab_int(message)

key = [0, 4, 8, 12] # clef 

########## Cryptage et décryptage ############

crypt = chiffrement(mes_int, key)
decrypt = dechiffrement(crypt, key)
print("Message crypté: ", tab_int_to_text(crypt))
print("Message décrypté: ", tab_int_to_text(decrypt))
# print(res == decrypt)
# print(crypt == decrypt)
# print(res == crypt)