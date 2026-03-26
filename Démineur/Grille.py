from Case import Cases
from Bonus import Bonus
import random 

class Grille:

    def __init__(self, nombre_de_lignes, nombre_de_colonnes, nombre_de_bombes):
        self.nombre_de_lignes = nombre_de_lignes
        self.nombre_de_colonnes = nombre_de_colonnes
        self.nombre_de_bombes = nombre_de_bombes
        self.positions_des_bombes = []  # liste des positions des bombes (tuples)

        self.cases = []  # liste qui contiendra chaque ligne de cases
        
        self.bonus = Bonus()

        for l in range(self.nombre_de_lignes):
            ligne = []

            for c in range(self.nombre_de_colonnes):
                ligne.append(Cases(l, c))  # création d'une case dans la grille

            self.cases.append(ligne)

    def placer_les_bombes(self, ligne_interdite, colonne_interdite):
        positions_interdites = []

        for dl in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                l = ligne_interdite + dl
                c = colonne_interdite + dc

                if 0 <= l < self.nombre_de_lignes and 0 <= c < self.nombre_de_colonnes:
                    positions_interdites.append((l, c))

        positions_possibles = []

        for l in range(self.nombre_de_lignes):
            for c in range(self.nombre_de_colonnes):
                positions_possibles.append((l, c))

        for pos in positions_interdites:
            if pos in positions_possibles:
                positions_possibles.remove(pos)

        # Tirage aléatoire des bombes
        self.positions_des_bombes = random.sample(positions_possibles, self.nombre_de_bombes)

        # --------------------------------------------------------------------
        # AJOUT : on marque les cases tirées comme étant des bombes
        # (sinon est_une_bombe reste toujours False → aucune bombe dans la grille)
        # --------------------------------------------------------------------
        for (l, c) in self.positions_des_bombes:
            self.cases[l][c].est_une_bombe = True  # AJOUT : activation de la bombe dans l'objet Case

    def calcule_nombre_de_bombe_autour_de_chaque_cases(self):

        for l in range(self.nombre_de_lignes):
            for c in range(self.nombre_de_colonnes):
                case = self.cases[l][c]

                case.nombre_de_bombes_autour = 0

                for dl in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:

                        if dl == 0 and dc == 0:
                            continue

                        voisin_l = l + dl
                        voisin_c = c + dc

                        # Vérifier si le voisin est dans la grille
                        if self.est_dans_la_grille(voisin_l, voisin_c):

                            # Vérifier si le voisin est une bombe
                            if (voisin_l, voisin_c) in self.positions_des_bombes:
                                case.nombre_de_bombes_autour += 1

    # Renvoie True si la position (l, c) se trouve à l'intérieur de la grille
    def est_dans_la_grille(self, l, c):
        return 0 <= l < self.nombre_de_lignes and 0 <= c < self.nombre_de_colonnes

    # Cette méthode révélera automatiquement toutes les cases vides (0)
    def reveler_zone_vide(self, ligne, colonne):
        
        # Liste des cases à traiter
        a_traiter = [(ligne, colonne)]

        # Ensemble des cases déjà traitées pour éviter les doublons
        deja_vu = set()

        while a_traiter:
            l, c = a_traiter.pop()   # on prend une case à traiter

            # Eviter de traiter deux fois la même case
            if (l, c) in deja_vu:
                continue
            deja_vu.add((l, c))

            case = self.cases[l][c]

            # révéler la case
            case.reveler_case()

            # Si la case vaut 0, on ajoute ses voisins
            if case.nombre_de_bombes_autour == 0:
                for dl in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:

                        if dl == 0 and dc == 0:
                            continue

                        voisin_l = l + dl
                        voisin_c = c + dc

                        if self.est_dans_la_grille(voisin_l, voisin_c):

                            voisin = self.cases[voisin_l][voisin_c]

                            # Ajouter seulement les voisins non-bombes et non révélés
                            if not voisin.est_une_bombe and voisin.etat != "revelee":
                                a_traiter.append((voisin_l, voisin_c))

    def reveler_toutes_les_bombes(self):
        # on révèle toutes les bombes quand le joueur clique sur une bombe
        for (l, c) in self.positions_des_bombes:
            case = self.cases[l][c]      # on récupère la case qui contient une bombe
            case.reveler_case()               # on révèle la bombe

    def clique_gauche(self, ligne, colonne):
        case_cliquee = self.cases[ligne][colonne]   # case sur laquelle le joueur a cliqué

        #Verification de la case si elle a un drapeau (éviter bug drapeau 1er tour)
        if case_cliquee.etat =="drapeau":
            return

        if case_cliquee.est_une_bombe:
            case_cliquee.reveler_case()                  # on révèle la bombe cliquée
            self.reveler_toutes_les_bombes()        # on révèle toutes les bombes (game over)

        elif case_cliquee.est_un_bonus:
            case_cliquee.est_un_bonus = False
            case_cliquee.etat = "revelee"
            self.bonus.activer_les_bonus(self)
            return
        
        else:
            case_cliquee.reveler_case()                  # on révèle la case car ce n'est pas une bombe

            if case_cliquee.nombre_de_bombes_autour == 0:
                # si la case vaut 0, on révèle automatiquement toute la zone vide
                self.reveler_zone_vide(ligne, colonne)

    def clique_droit(self, ligne, colonne):
        case = self.cases[ligne][colonne]  #Récuperation de la case cliquée
        case.changer_etat_clic_droit() #on change son état (drapeau / question / cachée)

    def a_gagne(self):

        #On parcourt toutes les cases de la grille
        for l in range(self.nombre_de_lignes):
            for c in range(self.nombre_de_colonnes):
                case = self.cases[l][c]

                #Si la case n'est pas une bombe
                if not case.est_une_bombe:

                    #et qu'elle n'est pas révélée → le joueur n'a pas gagné
                    if case.etat !="revelee":
                        return False

        #Si toutes les cases non-bombes sont révélées → victoire            
        return True
