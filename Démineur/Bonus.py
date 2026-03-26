import random

class Bonus:

    def __init__(self):
        # Liste des positions des bonus (3 cases)
        self.positions_des_bonus = []
        
    def placer_les_bonus(self, grille):
        # 1. On prépare une liste vide pour stocker les cases possibles
        cases_valides = []

        # 2. On parcourt toute la grille
        for l in range(grille.nombre_de_lignes):
            for c in range(grille.nombre_de_colonnes):

                case = grille.cases[l][c]

                # 3. On élimine les cases impossibles
                if case.est_une_bombe:
                    continue
                if case.etat != "cachee":
                    continue

                # 4. Si la case est valide, on l'ajoute
                cases_valides.append((l, c))

        # 5. On choisit 3 cases au hasard parmi les valides
        self.positions_des_bonus = random.sample(cases_valides, 3)

        # 6. On marque ces cases comme bonus dans la grille
        for (l, c) in self.positions_des_bonus:
            grille.cases[l][c].est_un_bonus = True


    def activer_les_bonus(self, grille):
        # 1. On récupère toutes les bombes encore cachées
        bombes_cachees = []

        for (l, c) in grille.positions_des_bombes:
            case = grille.cases[l][c]
            if case.etat == "cachee":
                bombes_cachees.append((l, c))

        # 2. S'il n'y a plus de bombes cachées, on ne fait rien
        if not bombes_cachees:
            return

        # 3. On choisit une bombe au hasard
        (l, c) = random.choice(bombes_cachees)

        # 4. On révèle cette bombe SANS déclencher la défaite
        #    → on utilise reveler_case() pour garder la logique cohérente
        case_bombe = grille.cases[l][c]
        case_bombe.reveler_case()

        # 5. On désactive le bonus utilisé
        #    On cherche la case bonus encore cachée (celle cliquée)
        for (bl, bc) in self.positions_des_bonus:
            case_bonus = grille.cases[bl][bc]

            # On désactive UNIQUEMENT le bonus encore caché
            if case_bonus.est_un_bonus and case_bonus.etat == "cachee":
                case_bonus.est_un_bonus = False
                case_bonus.etat = "revelee"
                break  # On arrête ici car un seul bonus doit être consommé
