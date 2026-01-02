import random

# -------------------------
# Fonctions de base
# -------------------------

def createEmptyGrid(size=10):
    return [[0 for _ in range(size)] for _ in range(size)]

def printGrid(grid):
    print("   " + " ".join([chr(ord('A') + i) for i in range(10)]))
    for i, row in enumerate(grid):
        print(f"{i + 1:2} " + " ".join(str(cell) for cell in row))

def printHiddenGrid(grid):
    print("   " + " ".join([chr(ord('A') + i) for i in range(10)]))
    for i, row in enumerate(grid):
        display_row = []
        for cell in row:
            if cell == 6:
                display_row.append("6")
            else:
                display_row.append("0")
        print(f"{i + 1:2} " + " ".join(display_row))

def validPosition(g, li, co, di, t):
    taille = len(g)
    if di == 1:  # horizontal
        if co + t > taille:
            return False
        return all(g[li][co + i] == 0 for i in range(t))
    elif di == 2:  # vertical
        if li + t > taille:
            return False
        return all(g[li + i][co] == 0 for i in range(t))
    return False

# -------------------------
# Initialisation des grilles
# -------------------------

def initGridComp():
    grille = createEmptyGrid()
    boat_sizes = [5, 4, 3, 3, 2]
    for taille in boat_sizes:
        placed = False
        while not placed:
            li= random.randint(0, 9)
            co = random.randint(0, 9)
            di = random.choice([1, 2])
            if validPosition(grille, li, co, di, taille):
                for i in range(taille):
                    if di == 1:
                        grille[li][co + i] = taille
                    else:
                        grille[li + i][co] = taille
                placed = True
    return grille 

def initGridPlay():
    grid = createEmptyGrid()
    boat_list = [
        ("porte-avions", 5),
        ("croiseur", 4),
        ("contre-torpilleur", 3),
        ("sous-marin", 3),
        ("torpilleur", 2)
    ]
    for name, size in boat_list:
        placed = False
        while not placed:
            try:
                col_letter = input(f"Donnez la lettre pour le {name} : ").strip().upper()
                if col_letter == "STOP":
                    print("Arrêt du placement.")
                    return grid
                if col_letter not in "ABCDEFGHIJ":
                    print("Erreur : lettre invalide.")
                    continue
                col = ord(col_letter) - ord('A')

                row_input = input(f"Donnez le numéro de ligne pour le {name} : ").strip()
                if row_input.upper() == "STOP":
                    print("Arrêt du placement.")
                    return grid
                if not row_input.isdigit():
                    print("Erreur : ligne invalide.")
                    continue
                row = int(row_input) - 1
                if not (0 <= row <= 9):
                    print("Erreur : ligne hors limites.")
                    continue

                dir_input = input("Horizontal (1) ou vertical (2) ? ").strip()
                if dir_input.upper() == "STOP":
                    print("Arrêt du placement.")
                    return grid
                if dir_input not in ("1", "2"):
                    print("Erreur : direction invalide.")
                    continue
                direction = int(dir_input)

                if not validPosition(grid, row, col, direction, size):
                    print("Erreur : le bateau ne peut pas être placé ici.")
                    continue

                for i in range(size):
                    if direction == 1:
                        grid[row][col + i] = size
                    else:
                        grid[row + i][col] = size
                placed = True

            except Exception as e:
                print("Erreur inattendue :", e)
    return grid

# -------------------------
# Logique de jeu
# -------------------------

def hasDrowned(grid, bateau_num):
    for row in grid:
        for cell in row:
            if cell == bateau_num:
                return False
    return True

def oneMove(grid, row, col):
    if grid[row][col] == 0:
        print("À l’eau.")
    elif grid[row][col] == 6:
        print("Déjà touché ici.")
    else:
        bateau_num = grid[row][col]
        grid[row][col] = 6
        if hasDrowned(grid, bateau_num):
            print(f"Coulé : bateau de taille {bateau_num}")
        else:
            print("Touché !")
    return grid

def isOver(grid):
    for row in grid:
        for cell in row:
            if cell in [2, 3, 4, 5]:
                return False
    return True

# -------------------------
# Jouer un coup
# -------------------------

def playComp():
    return [random.randint(0, 9), random.randint(0, 9)]

def playPlayer(grille_joueur, grille_adverse):
    while True:
        lettre = input("Lettre de tir (A-J ou AFFICHER/STOP) : ").strip().upper()
        if lettre == "STOP":
            print("Partie interrompue.")
            exit()
        if lettre == "AFFICHER":
            print("Grille adverse (brouillard de guerre) :")
            printHiddenGrid(grille_adverse)
            continue
        if lettre not in "ABCDEFGHIJ":
            print(" Lettre invalide.")
            continue
        col = ord(lettre) - ord('A')

        ligne = input("Numéro de ligne (1-10 ou STOP) : ").strip()
        if ligne.upper() == "STOP":
            print(" Partie interrompue.")
            exit()
        if not ligne.isdigit() or not (1 <= int(ligne) <= 10):
            print("Numéro de ligne invalide.")
            continue
        row = int(ligne) - 1

        return [row, col]

# -------------------------
# Partie complète
# -------------------------

def play():
    print("=== Bienvenue dans la Bataille Navale ! ===")
    
    # Initialisation
    print("\n--- Placement des bateaux du joueur ---")
    gridPlayer = initGridPlay()
    print("\n--- Placement des bateaux de l'ordinateur... ---")
    gridComp = initGridComp()
    
    print("\n--- Début de la bataille ! ---")
    
    while True:
        # Tour du joueur
        print("\n>>> À vous de jouer !")
        pos = playPlayer(gridPlayer, gridComp)
        row, col = pos[0], pos[1]
        gridComp = oneMove(gridComp, row, col)

        if isOver(gridComp):
            print("\n Félicitations ! Vous avez gagné.")
            break

        # Tour de l'ordinateur
        print("\n>>> L'ordinateur tire...")
        valid_shot = False
        while not valid_shot:
            row_c, col_c = playComp()
            if gridPlayer[row_c][col_c] != 6:
                valid_shot = True
        print(f"L'ordinateur tire en {chr(col_c + ord('A'))}{row_c + 1}")
        gridPlayer = oneMove(gridPlayer, row_c, col_c)

        if isOver(gridPlayer):
            print("\n L'ordinateur a gagné. Tous vos bateaux sont coulés.")
            break

        # Affichage
        print("\n--- Votre grille ---")
        printGrid(gridPlayer)

# -------------------------
# Lancer le jeu
# -------------------------

if __name__ == "__main__":
    play()
