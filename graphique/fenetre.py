"""
Fenetre : fenêtre pygame principale et boucle de jeu.
Orchestre tous les renderers et délègue la logique au Jeu.
"""
import sys
import pygame

from jeu import Jeu
from niveau import Niveau
from graphique import theme as T
from graphique.dessin import rect_arrondi
from graphique.case_renderer import CaseRenderer
from graphique.grille_renderer import GrilleRenderer
from graphique.entete_renderer import EnteteRenderer
from graphique.menu_renderer import MenuRenderer


class Fenetre:
    """
    Fenêtre pygame principale.
    Gère : initialisation, boucle d'événements, rendu frame-by-frame.
    """

    TITRE = "💣 MinesWeeper — La Plateforme"
    FPS   = 60

    def __init__(self):
        pygame.init()
        pygame.display.set_caption(self.TITRE)

        self._jeu = Jeu(Niveau.FACILE)
        self._clock = pygame.time.Clock()

        # ── Polices ───────────────────────────────────────────────────────────
        self._font_chiffre = pygame.font.SysFont("couriernew",  T.TAILLE_POLICE_CHIFFRE, bold=True)
        self._font_entete  = pygame.font.SysFont("couriernew",  T.TAILLE_POLICE_ENTETE,  bold=True)
        self._font_label   = pygame.font.SysFont("couriernew",  T.TAILLE_POLICE_LABEL)
        self._font_btn     = pygame.font.SysFont("couriernew",  T.TAILLE_POLICE_BTN,     bold=True)
        self._font_emoji   = pygame.font.SysFont("segoeuiemoji", 22)

        # ── Renderers ─────────────────────────────────────────────────────────
        self._case_renderer: CaseRenderer = None
        self._grille_renderer: GrilleRenderer = None
        self._entete_renderer: EnteteRenderer = None
        self._menu_renderer: MenuRenderer = None

        self._screen: pygame.Surface = None
        self._survol_case: tuple[int, int] | None = None
        self._survol_reset: bool = False

        # Overlay fin de partie
        self._overlay_alpha = 0
        self._message_fin: str = ""

        self._construire()

    # ── Construction / reconstruction ─────────────────────────────────────────

    def _construire(self):
        """(Re)calcule les dimensions et instancie/met à jour les renderers."""
        p = self._jeu.plateau

        # Taille de la grille
        larg_grille = p.colonnes * (T.TAILLE_CASE + T.GAP) - T.GAP + 2 * T.MARGE_GRILLE
        haut_grille = p.lignes   * (T.TAILLE_CASE + T.GAP) - T.GAP + 2 * T.MARGE_GRILLE

        larg_fen = max(larg_grille, 360)
        haut_fen = T.HAUTEUR_MENU + T.HAUTEUR_ENTETE + haut_grille + 6

        self._screen = pygame.display.set_mode((larg_fen, haut_fen))

        offset_grille_y = T.HAUTEUR_MENU + T.HAUTEUR_ENTETE + 4
        offset_grille_x = (larg_fen - larg_grille) // 2

        # Case renderer (partagé)
        self._case_renderer = CaseRenderer(self._font_chiffre, self._font_emoji)

        # Grille renderer
        self._grille_renderer = GrilleRenderer(
            self._jeu.plateau, self._case_renderer,
            offset_grille_x, offset_grille_y
        )

        # Entête renderer
        self._entete_renderer = EnteteRenderer(
            self._font_entete, self._font_label, self._font_emoji,
            larg_fen, T.HAUTEUR_MENU
        )

        # Menu renderer
        if self._menu_renderer is None:
            self._menu_renderer = MenuRenderer(
                self._font_btn, larg_fen, self._jeu.niveau.nom
            )
        else:
            self._menu_renderer.mettre_a_jour_largeur(larg_fen)

        # Reset overlay
        self._overlay_alpha = 0
        self._message_fin = ""

    def _reconstruire_apres_reset(self):
        self._grille_renderer.reinitialiser(self._jeu.plateau)
        self._construire()

    # ── Boucle principale ─────────────────────────────────────────────────────

    def lancer(self):
        """Démarre la boucle de jeu pygame."""
        while True:
            self._traiter_evenements()
            self._dessiner()
            self._clock.tick(self.FPS)

    # ── Événements ────────────────────────────────────────────────────────────

    def _traiter_evenements(self):
        mx, my = pygame.mouse.get_pos()

        # Mise à jour survol menu (décalé en y=0)
        survol_menu = (mx, my) if my < T.HAUTEUR_MENU else None
        self._survol_reset = self._entete_renderer.bouton.collide((mx, my))
        self._survol_case = self._grille_renderer.case_sous_curseur(mx, my)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._traiter_clic(event.button, event.pos)

    def _traiter_clic(self, bouton: int, pos: tuple):
        mx, my = pos

        # Clic sur bouton reset
        if self._entete_renderer.bouton.collide(pos):
            self._reset()
            return

        # Clic sur un niveau
        nom = self._menu_renderer.niveau_sous_curseur(pos)
        if nom:
            self._changer_niveau(nom)
            return

        # Clic sur la grille
        case_pos = self._grille_renderer.case_sous_curseur(mx, my)
        if case_pos:
            l, c = case_pos
            if bouton == 1:      # gauche → révéler
                self._on_clic_gauche(l, c)
            elif bouton == 3:    # droit → drapeau
                self._jeu.clic_droit(l, c)

    def _on_clic_gauche(self, ligne: int, colonne: int):
        if self._jeu.est_termine():
            return
        self._jeu.clic_gauche(ligne, colonne)
        if self._jeu.etat == "perdu":
            self._grille_renderer.definir_mine_touchee(ligne, colonne)
            self._declencher_overlay("💥  BOOM !  Vous avez sauté sur une mine !")
        elif self._jeu.etat == "gagne":
            self._declencher_overlay("🎉  Bravo ! Terrain déminé !")

    def _reset(self):
        self._jeu.reinitialiser()
        self._reconstruire_apres_reset()

    def _changer_niveau(self, nom: str):
        self._jeu.reinitialiser(nom)
        self._menu_renderer.definir_niveau(nom)
        self._reconstruire_apres_reset()

    def _declencher_overlay(self, message: str):
        self._message_fin = message
        self._overlay_alpha = 0   # animation d'apparition

    # ── Rendu ─────────────────────────────────────────────────────────────────

    def _dessiner(self):
        self._screen.fill(T.FOND_FENETRE)

        # Séparateur horizontal menu / entête
        pygame.draw.rect(self._screen, T.COULEUR_SEPARATEUR,
                         (0, T.HAUTEUR_MENU, self._screen.get_width(), 3))

        # Menu niveaux (sur surface décalée en y=0)
        menu_surf = self._screen.subsurface(
            pygame.Rect(0, 0, self._screen.get_width(), T.HAUTEUR_MENU)
        )
        self._menu_renderer.dessiner(menu_surf, pygame.mouse.get_pos())

        # Entête
        entete_surf = self._screen.subsurface(
            pygame.Rect(0, T.HAUTEUR_MENU, self._screen.get_width(), T.HAUTEUR_ENTETE)
        )
        self._entete_renderer.dessiner(
            entete_surf,
            mines_restantes=self._jeu.nb_mines_restantes(),
            temps=self._jeu.temps_formate(),
            nb_drapeaux=self._jeu.plateau.compter_drapeaux(),
            nb_interrogations=self._jeu.plateau.compter_interrogations(),
            etat=self._jeu.etat,
            survol_reset=self._survol_reset,
        )

        # Séparateur entête / grille
        sep_y = T.HAUTEUR_MENU + T.HAUTEUR_ENTETE
        pygame.draw.rect(self._screen, T.COULEUR_SEPARATEUR,
                         (0, sep_y, self._screen.get_width(), 3))

        # Grille
        self._grille_renderer.dessiner(self._screen, self._survol_case)

        # Overlay fin de partie
        if self._message_fin:
            self._dessiner_overlay()

        pygame.display.flip()

    def _dessiner_overlay(self):
        """Affiche un message de fin semi-transparent avec animation."""
        if self._overlay_alpha < 210:
            self._overlay_alpha = min(self._overlay_alpha + 8, 210)

        w, h = self._screen.get_size()
        overlay = pygame.Surface((w, h), pygame.SRCALPHA)
        overlay.fill((10, 15, 35, self._overlay_alpha))
        self._screen.blit(overlay, (0, 0))

        if self._overlay_alpha < 120:
            return

        # Boîte de message
        bw, bh = 460, 120
        bx = (w - bw) // 2
        by = (h - bh) // 2
        box = pygame.Surface((bw, bh), pygame.SRCALPHA)
        box.fill((25, 35, 75, 230))
        self._screen.blit(box, (bx, by))
        pygame.draw.rect(self._screen, T.COULEUR_ACCENT,
                         (bx, by, bw, bh), 2, border_radius=10)

        # Message
        font = pygame.font.SysFont("couriernew", 17, bold=True)
        surf = font.render(self._message_fin, True, (240, 240, 240))
        self._screen.blit(surf, (bx + (bw - surf.get_width()) // 2, by + 22))

        # Temps
        temps_txt = f"Temps : {self._jeu.temps_formate()}"
        surf2 = font.render(temps_txt, True, T.COULEUR_ACCENT)
        self._screen.blit(surf2, (bx + (bw - surf2.get_width()) // 2, by + 52))

        # Instruction
        font_sm = pygame.font.SysFont("couriernew", 13)
        surf3 = font_sm.render("Cliquez sur 🙂 pour rejouer", True, (150, 160, 190))
        self._screen.blit(surf3, (bx + (bw - surf3.get_width()) // 2, by + 85))
