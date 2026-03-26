import pygame
from Grille import Grille
from Bonus import Bonus

pygame.init()

# ------------------------------
# CONFIG DIFFICULTÉS
# ------------------------------
DIFFICULTES = {
    "facile":  (9, 9, 10),
    "moyen":   (16, 16, 40),
    "difficile": (16, 30, 99)
}

TAILLE_CASE = 40
HAUTEUR_BARRE = 60

font = pygame.font.SysFont("arial", 24, bold=True)
font_small = pygame.font.SysFont("arial", 18, bold=True)

GRIS_FONCE = (120, 120, 120)
GRIS_CLAIR = (200, 200, 200)
GRIS_TRES_CLAIR = (240, 240, 240)
NOIR = (0, 0, 0)
ROUGE = (255, 0, 0)
BLANC = (255, 255, 255)

COULEURS_CHIFFRES = {
    1: (0, 0, 255),
    2: (0, 128, 0),
    3: (255, 0, 0),
    4: (0, 0, 128),
    5: (128, 0, 0),
    6: (0, 128, 128),
    7: (0, 0, 0),
    8: (128, 128, 128)
}

# ------------------------------
# ÉTAT GLOBAL DU JEU
# ------------------------------
difficulte_actuelle = "moyen"
NB_LIGNES, NB_COLONNES, NB_BOMBES = DIFFICULTES[difficulte_actuelle]

LARGEUR = NB_COLONNES * TAILLE_CASE
HAUTEUR = NB_LIGNES * TAILLE_CASE + HAUTEUR_BARRE

screen = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Démineur - Style Windows XP")

grille = None
bonus = None
premier_clic = True
etat_jeu = "en_cours"
start_time = None
temps_final = 0
smiley_rect = None


# ------------------------------
# FONCTIONS UTILITAIRES
# ------------------------------
def nouvelle_partie(nom_difficulte=None):
    global grille, bonus, premier_clic, etat_jeu, start_time, temps_final
    global NB_LIGNES, NB_COLONNES, NB_BOMBES, LARGEUR, HAUTEUR, difficulte_actuelle, screen

    if nom_difficulte is not None:
        difficulte_actuelle = nom_difficulte

    NB_LIGNES, NB_COLONNES, NB_BOMBES = DIFFICULTES[difficulte_actuelle]
    LARGEUR = NB_COLONNES * TAILLE_CASE
    HAUTEUR = NB_LIGNES * TAILLE_CASE + HAUTEUR_BARRE
    screen = pygame.display.set_mode((LARGEUR, HAUTEUR))

    grille = Grille(NB_LIGNES, NB_COLONNES, NB_BOMBES)
    bonus = Bonus()

    premier_clic = True
    etat_jeu = "en_cours"
    start_time = None
    temps_final = 0


def compter_drapeaux():
    nb = 0
    for l in range(NB_LIGNES):
        for c in range(NB_COLONNES):
            if grille.cases[l][c].etat == "drapeau":
                nb += 1
    return nb


# ------------------------------
# DESSIN DES CASES
# ------------------------------
def dessiner_case_cachee(x, y):
    pygame.draw.line(screen, GRIS_TRES_CLAIR, (x, y), (x + TAILLE_CASE, y))
    pygame.draw.line(screen, GRIS_TRES_CLAIR, (x, y), (x, y + TAILLE_CASE))
    pygame.draw.line(screen, GRIS_FONCE, (x, y + TAILLE_CASE), (x + TAILLE_CASE, y + TAILLE_CASE))
    pygame.draw.line(screen, GRIS_FONCE, (x + TAILLE_CASE, y), (x + TAILLE_CASE, y + TAILLE_CASE))
    pygame.draw.rect(screen, GRIS_CLAIR, (x + 2, y + 2, TAILLE_CASE - 4, TAILLE_CASE - 4))


def dessiner_case_revelee(x, y):
    pygame.draw.rect(screen, GRIS_TRES_CLAIR, (x, y, TAILLE_CASE, TAILLE_CASE))
    pygame.draw.rect(screen, GRIS_FONCE, (x, y, TAILLE_CASE, TAILLE_CASE), 1)


# ------------------------------
# BARRE DU HAUT
# ------------------------------
def afficher_barre_haut():
    global smiley_rect

    pygame.draw.rect(screen, GRIS_CLAIR, (0, 0, LARGEUR, HAUTEUR_BARRE))
    pygame.draw.rect(screen, GRIS_FONCE, (0, 0, LARGEUR, HAUTEUR_BARRE), 2)

    if start_time is not None and etat_jeu == "en_cours":
        temps = (pygame.time.get_ticks() - start_time) // 1000
    else:
        temps = temps_final

    texte_temps = font.render(f"{temps:03}", True, ROUGE)
    screen.blit(texte_temps, (LARGEUR - 80, 15))

    nb_drapeaux = compter_drapeaux()
    bombes_restantes = max(0, NB_BOMBES - nb_drapeaux)
    texte_bombes = font.render(f"{bombes_restantes:03}", True, ROUGE)
    screen.blit(texte_bombes, (20, 15))

    smiley_x = LARGEUR // 2 - 20
    smiley_y = 10
    smiley_rect = pygame.Rect(smiley_x, smiley_y, 40, 40)

    if etat_jeu == "en_cours":
        smiley = "😃"
    elif etat_jeu == "perdu":
        smiley = "😵"
    elif etat_jeu == "gagne":
        smiley = "😎"
    else:
        smiley = "😐"

    pygame.draw.rect(screen, GRIS_TRES_CLAIR, smiley_rect)
    pygame.draw.rect(screen, GRIS_FONCE, smiley_rect, 2)
    texte_smiley = font.render(smiley, True, NOIR)
    screen.blit(texte_smiley, (smiley_x + 2, smiley_y + 2))


# ------------------------------
# AFFICHAGE GRILLE + BONUS
# ------------------------------
def afficher_grille():
    for l in range(NB_LIGNES):
        for c in range(NB_COLONNES):
            case = grille.cases[l][c]
            x = c * TAILLE_CASE
            y = HAUTEUR_BARRE + l * TAILLE_CASE

            if case.etat == "cachee":
                dessiner_case_cachee(x, y)

                # BONUS visible en debug
                if case.est_un_bonus:
                    texte = font.render("+", True, (255, 165, 0))
                    screen.blit(texte, (x + 12, y + 5))

            elif case.etat == "drapeau":
                dessiner_case_cachee(x, y)
                texte = font.render("⚑", True, ROUGE)
                screen.blit(texte, (x + 10, y + 5))

            elif case.etat == "question":
                dessiner_case_cachee(x, y)
                texte = font.render("?", True, (255, 165, 0))
                screen.blit(texte, (x + 14, y + 5))

            elif case.etat == "revelee":
                dessiner_case_revelee(x, y)

                if case.est_une_bombe:
                    pygame.draw.circle(screen, NOIR, (x + 20, y + 20), 10)
                else:
                    n = case.nombre_de_bombes_autour
                    if n > 0:
                        couleur = COULEURS_CHIFFRES[n]
                        texte = font.render(str(n), True, couleur)
                        screen.blit(texte, (x + 12, y + 5))


# ------------------------------
# BOUCLE PRINCIPALE
# ------------------------------
nouvelle_partie()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F1:
                nouvelle_partie("facile")
            elif event.key == pygame.K_F2:
                nouvelle_partie("moyen")
            elif event.key == pygame.K_F3:
                nouvelle_partie("difficile")

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos

            if smiley_rect is not None and smiley_rect.collidepoint(mx, my):
                nouvelle_partie()
                continue

            if my < HAUTEUR_BARRE:
                continue

            if etat_jeu != "en_cours":
                continue

            ligne = (my - HAUTEUR_BARRE) // TAILLE_CASE
            colonne = mx // TAILLE_CASE

            if 0 <= ligne < NB_LIGNES and 0 <= colonne < NB_COLONNES:

                if event.button == 1:  # clic gauche
                    case = grille.cases[ligne][colonne]

                    if premier_clic:
                        grille.placer_les_bombes(ligne, colonne)
                        grille.calcule_nombre_de_bombe_autour_de_chaque_cases()

                        # → PLACEMENT DES BONUS
                        bonus.placer_les_bonus(grille)

                        premier_clic = False
                        start_time = pygame.time.get_ticks()

                    # → ACTIVATION BONUS
                    if case.est_un_bonus:
                        bonus.activer_les_bonus(grille)

                    grille.clique_gauche(ligne, colonne)

                    if case.est_une_bombe and case.etat == "revelee":
                        etat_jeu = "perdu"
                        if start_time is not None:
                            temps_final = (pygame.time.get_ticks() - start_time) // 1000

                    elif grille.a_gagne():
                        etat_jeu = "gagne"
                        if start_time is not None:
                            temps_final = (pygame.time.get_ticks() - start_time) // 1000

                elif event.button == 3:  # clic droit
                    grille.clique_droit(ligne, colonne)

    screen.fill(GRIS_FONCE)
    afficher_barre_haut()
    afficher_grille()
    pygame.display.flip()

pygame.quit()
