import random


# fonction de génération d'une grille sudoku de taille n*n
def generate_sudoku(n):
    taille = int(n ** 0.5) # On prends la partie entiere de la racine carrée (un sudoku 11*11 est impossible, on fera 9*9 avec sous-grille 3*3)
    n = taille ** 2
    print(f"taille: {taille}")
    num_range = range(1, n+1) # liste de 1 à n
    grille = [[0 for i in range(n)] for j in range(n)] # grille n*n de 0

    #On remplis chaque ligne avec une permutation aléatoire des nombres de 1 à n
    for i in range(n):
        numbers = random.sample(num_range, n) # liste des nombres de 1 à n dans ordre aleatoire
        for j in range(n):
            grille[i][j] = numbers[j]
    return grille

def permute_sudoku(sudo):
    n = len(sudo)
    for i in range(n):
        sudo[i] = random.sample(sudo[i], n)
    return sudo


def challenge(sudo):
    n = len(sudo)
    root_n = int(n**0.5)
    challenge = random.randint(0,3*n+1)
    print(f"challenge: {challenge}")
    if challenge < n:
        num = challenge - n # le numero de la ligne vérifier
        return [sudo[num][i] for i in range(n)]
    elif challenge < 2*n:
        num = challenge - 2*n # le numero de la colonne vérifier
        return [sudo[i][num] for i in range(n)]
    elif challenge < 3*n:
        c = challenge - 2*n
        num1 = min(c,root_n) * root_n # le numéro de ligne de la première case de la sous-grille (entre 0 et n) 
        num2 = max(num1-root_n, 0) # le num de la colonne de la premiére case de la sous-grille
        return [sudo[num1 + i][num2 + j] for i in range(root_n) for j in range(root_n)]
    else:
        cells = generate_known_cells(n, 6) # On génére les 6 cases connues par Alice et Bob
        return [sudo[cells[i][0]][cells[i][1]] for i in range(n)]

# Génére une liste de tuple (i,j) représentant les cases connues par Alice et Bob. La liste est de taille nb. n est la longueur d'une ligne du sudoku
def generate_known_cells(n, nb):
    return [(random.randint(0, n-1), random.randint(0, n-1)) for i in range(nb)]

s1 = generate_sudoku(6)
s2 = permute_sudoku(s1)
c = challenge(s2)
print(f"s1: {s1}")
print(f"s2: {s2}")
print(f"c: {c}")















# k environ 250

print(random.sample(range(1,10), 9)) # permutation aléatoire

#On envoie vecteur de 81 valeur en sachant que c1 ect corresp à case 1...
#Peut demander à reveler 9 valeurs ci (pas n'importe quel ordre)


# 1 du C10
# -on choisit n
# -on genere q premier n bits (cryptodome)
#     -on test si p = 2q+1 jusqu'a succes
# -on trv un gain g pour Zp* (au hasard, on test que g != 1 mod p, g²!=1.. g^q=1 mod p jusqu'au succes)
# -h.t.q tq h^q = 1 h=g^2x   h^q = g^2qx = g^(p-1)x = 1^x = 1 
