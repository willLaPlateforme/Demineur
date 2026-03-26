"""
Fenetre : fenetre pygame principale et boucle de jeu.
Orchestre tous les renderers et delegue la logique a Jeu.py.
Logique metier : Jeu -> Grille -> Cases (fichiers de l'etudiant).
"""
import sys
import pygame

from Jeu import Jeu
from graphique import theme as T
from graphique.dessin import rect_arrondi
from graphique.case_renderer import CaseRenderer
from graphique.grille_renderer import GrilleRenderer
from graphique.entete_renderer import EnteteRenderer
from graphique.menu_renderer import MenuRenderer


class Fenetre:
    """
    Fenetre pygame principale.
    Gere : initialisation, boucle d'evenements, rendu a 60 FPS.
    Toute la logique metier est deleguee a Jeu -> Grille -> Cases.
    """

    TITRE = "Minesweeper - La Plateforme"
    FPS   = 60

    def __init__(self):
        pygame.init()
        pygame.display.set_caption(self.TITRE)

        self._jeu   = Jeu("Facile")
        self._clock = pygame.time.Clock()

        # Polices
        self._font_chiffre = pygame.font.SysFont("couriernew", T.TAILLE_POLICE_CHIFFRE, bold=True)
        self._font_entete  = pygame.font.SysFont("couriernew", T.TAILLE_POLICE_ENTETE,  bold=True)
        self._font_label   = pygame.font.SysFont("couriernew", T.TAILLE_POLICE_LABEL)
        self._font_btn     = pygame.font.SysFont("couriernew", T.TAILLE_POLICE_BTN,     bold=True)

        # Renderers (initialises dans _construire)
        self._case_renderer   = None
        self._grille_renderer = None
        self._entete_renderer = None
        self._menu_renderer   = None
        self._screen          = None

        self._survol_case  = None
        self._survol_reset = False

        # Overlay fin de partie
        self._overlay_alpha = 0
        self._message_fin   = ""

        self._construire()

    # ── Construction ──────────────────────────────────────────────────────────

    def _construire(self):
        """(Re)calcule les dimensions et instancie les renderers."""
        g = self._jeu.grille

        larg_grille = g.nombre_de_colonnes * (T.TAILLE_CASE + T.GAP) - T.GAP + 2 * T.MARGE_GRILLE
        haut_grille = g.nombre_de_lignes   * (T.TAILLE_CASE + T.GAP) - T.GAP + 2 * T.MARGE_GRILLE

        larg_fen = max(larg_grille, 420)
        haut_fen = T.HAUTEUR_MENU + T.HAUTEUR_ENTETE + haut_grille + 6

        self._screen = pygame.display.set_mode((larg_fen, haut_fen))

        offset_x = (larg_fen - larg_grille) // 2
        offset_y = T.HAUTEUR_MENU + T.HAUTEUR_ENTETE + 4

        self._case_renderer = CaseRenderer(self._font_chiffre, self._font_chiffre)

        self._grille_renderer = GrilleRenderer(
            self._jeu.grille, self._case_renderer, offset_x, offset_y
        )

        self._entete_renderer = EnteteRenderer(
            self._font_entete, self._font_label, self._font_btn,
            larg_fen, T.HAUTEUR_MENU
        )

        if self._menu_renderer is None:
            self._menu_renderer = MenuRenderer(self._font_btn, larg_fen, self._jeu.nom_niveau)
        else:
            self._menu_renderer.mettre_a_jour_largeur(larg_fen)

        self._overlay_alpha = 0
        self._message_fin   = ""

    def _reconstruire(self):
        self._grille_renderer.reinitialiser(self._jeu.grille)
        self._construire()

    # ── Boucle principale ─────────────────────────────────────────────────────

    def lancer(self):
        """Demarre la boucle de jeu pygame a 60 FPS."""
        while True:
            self._traiter_evenements()
            self._dessiner()
            self._clock.tick(self.FPS)

    # ── Evenements ────────────────────────────────────────────────────────────

    def _traiter_evenements(self):
        mx, my = pygame.mouse.get_pos()
        self._survol_reset = self._entete_renderer.bouton.collide((mx, my))
        self._survol_case  = self._grille_renderer.case_sous_curseur(mx, my)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._traiter_clic(event.button, event.pos)

    def _traiter_clic(self, bouton: int, pos: tuple):
        mx, my = pos

        # Bouton RESET
        if self._entete_renderer.bouton.collide(pos):
            self._reset()
            return

        # Bouton de niveau
        nom = self._menu_renderer.niveau_sous_curseur(pos)
        if nom:
            self._changer_niveau(nom)
            return

        # Case de la grille
        case_pos = self._grille_renderer.case_sous_curseur(mx, my)
        if case_pos:
            l, c = case_pos
            if bouton == 1:      # clic gauche -> reveler
                self._on_clic_gauche(l, c)
            elif bouton == 3:    # clic droit  -> drapeau/question
                self._jeu.clic_droit(l, c)

    def _on_clic_gauche(self, ligne: int, colonne: int):
        if self._jeu.est_termine():
            return
        self._jeu.clic_gauche(ligne, colonne)
        if self._jeu.etat == Jeu.ETAT_PERDU:
            mt = self._jeu.mine_touchee()
            if mt:
                self._grille_renderer.definir_mine_touchee(*mt)
            self._declencher_overlay("BOOM ! Vous avez saute sur une mine !")
        elif self._jeu.etat == Jeu.ETAT_GAGNE:
            self._declencher_overlay("Bravo ! Terrain demine avec succes !")

    def _reset(self):
        self._jeu.reinitialiser()
        self._reconstruire()

    def _changer_niveau(self, nom: str):
        self._jeu.reinitialiser(nom)
        self._menu_renderer.definir_niveau(nom)
        self._reconstruire()

    def _declencher_overlay(self, message: str):
        self._message_fin   = message
        self._overlay_alpha = 0

    # ── Rendu ─────────────────────────────────────────────────────────────────

    def _dessiner(self):
        self._screen.fill(T.FOND_FENETRE)

        # Separateur menu / entete
        pygame.draw.rect(self._screen, T.COULEUR_SEPARATEUR,
                         (0, T.HAUTEUR_MENU, self._screen.get_width(), 3))

        # Barre de niveaux
        menu_surf = self._screen.subsurface(
            pygame.Rect(0, 0, self._screen.get_width(), T.HAUTEUR_MENU)
        )
        self._menu_renderer.dessiner(menu_surf, pygame.mouse.get_pos())

        # En-tete
        entete_surf = self._screen.subsurface(
            pygame.Rect(0, T.HAUTEUR_MENU, self._screen.get_width(), T.HAUTEUR_ENTETE)
        )
        self._entete_renderer.dessiner(
            entete_surf,
            mines_restantes   = self._jeu.nb_bombes_restantes(),
            temps             = self._jeu.temps_formate(),
            nb_drapeaux       = self._jeu.compter_drapeaux(),
            nb_interrogations = self._jeu.compter_questions(),
            etat              = self._jeu.etat,
            survol_reset      = self._survol_reset,
        )

        # Separateur entete / grille
        sep_y = T.HAUTEUR_MENU + T.HAUTEUR_ENTETE
        pygame.draw.rect(self._screen, T.COULEUR_SEPARATEUR,
                         (0, sep_y, self._screen.get_width(), 3))

        # Grille
        self._grille_renderer.dessiner(self._screen, self._survol_case)

        # Overlay fin de partie (anime)
        if self._message_fin:
            self._dessiner_overlay()

        pygame.display.flip()

    def _dessiner_overlay(self):
        """Overlay semi-transparent anime en fin de partie."""
        if self._overlay_alpha < 210:
            self._overlay_alpha = min(self._overlay_alpha + 8, 210)

        w, h = self._screen.get_size()
        overlay = pygame.Surface((w, h), pygame.SRCALPHA)
        overlay.fill((10, 15, 35, self._overlay_alpha))
        self._screen.blit(overlay, (0, 0))

        if self._overlay_alpha < 120:
            return

        bw, bh = 500, 130
        bx = (w - bw) // 2
        by = (h - bh) // 2

        box = pygame.Surface((bw, bh), pygame.SRCALPHA)
        box.fill((25, 35, 75, 230))
        self._screen.blit(box, (bx, by))
        pygame.draw.rect(self._screen, T.COULEUR_ACCENT,
                         (bx, by, bw, bh), 2, border_radius=10)

        font_msg = pygame.font.SysFont("couriernew", 16, bold=True)
        font_sm  = pygame.font.SysFont("couriernew", 13)

        surf = font_msg.render(self._message_fin, True, (240, 240, 240))
        self._screen.blit(surf, (bx + (bw - surf.get_width()) // 2, by + 18))

        surf2 = font_msg.render(f"Temps : {self._jeu.temps_formate()}", True, T.COULEUR_ACCENT)
        self._screen.blit(surf2, (bx + (bw - surf2.get_width()) // 2, by + 50))

        surf3 = font_sm.render("Cliquez RESET pour rejouer", True, (150, 160, 190))
        self._screen.blit(surf3, (bx + (bw - surf3.get_width()) // 2, by + 90))
