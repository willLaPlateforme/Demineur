"""
Fenetre : fenetre pygame principale et boucle de jeu.
Orchestre tous les renderers et delegue la logique a Jeu.py.
Importe BoutonBonus depuis bouton_bonus.py (une classe par fichier).
"""
import sys
import os
import pygame

from Jeu import Jeu
from graphique import theme as T
from graphique.dessin import rect_arrondi, texte_centre, texte_gauche
from graphique.case_renderer import CaseRenderer
from graphique.grille_renderer import GrilleRenderer
from graphique.entete_renderer import EnteteRenderer
from graphique.menu_renderer import MenuRenderer
from graphique.bouton_bonus import BoutonBonus


class Fenetre:
    """
    Fenetre pygame principale.
    Gere : initialisation, boucle d'evenements, rendu a 60 FPS.
    Contient : barre niveaux, en-tete, barre bonus, grille, overlay de fin.
    """

    TITRE         = "Minesweeper - La Plateforme"
    FPS           = 60
    HAUTEUR_BONUS = 58   # hauteur de la barre bonus entre l'en-tete et la grille

    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption(self.TITRE)

        self._jeu   = Jeu("Facile")
        self._clock = pygame.time.Clock()

        # Chargement du son bonus (wtf.mp3 au meme niveau que main.py)
        self._son_bonus = None
        chemin_son = os.path.join(os.path.dirname(os.path.dirname(__file__)), "wtf.mp3")
        if os.path.exists(chemin_son):
            try:
                self._son_bonus = pygame.mixer.Sound(chemin_son)
                self._son_bonus.set_volume(0.8)
            except Exception:
                self._son_bonus = None

        # Polices
        self._font_chiffre = pygame.font.SysFont("couriernew", T.TAILLE_POLICE_CHIFFRE, bold=True)
        self._font_entete  = pygame.font.SysFont("couriernew", T.TAILLE_POLICE_ENTETE,  bold=True)
        self._font_label   = pygame.font.SysFont("couriernew", T.TAILLE_POLICE_LABEL)
        self._font_btn     = pygame.font.SysFont("couriernew", T.TAILLE_POLICE_BTN,     bold=True)
        self._font_bonus   = pygame.font.SysFont("couriernew", 12,                      bold=True)

        # Renderers
        self._case_renderer   = None
        self._grille_renderer = None
        self._entete_renderer = None
        self._menu_renderer   = None
        self._screen          = None

        # Bouton bonus (classe importee depuis bouton_bonus.py)
        self._bouton_bonus   = BoutonBonus(self._font_bonus)
        self._survol_bonus   = False

        self._survol_case  = None
        self._survol_reset = False

        # Overlay fin de partie
        self._overlay_alpha      = 0
        self._message_fin        = ""
        self._overlay_actif      = False
        self._overlay_btn_rect   = pygame.Rect(0, 0, 190, 44)
        self._overlay_btn_survol = False

        self._construire()

    # ── Construction ──────────────────────────────────────────────────────────

    def _construire(self):
        """Calcule les dimensions et instancie tous les renderers."""
        g = self._jeu.grille

        larg_grille = g.nombre_de_colonnes * (T.TAILLE_CASE + T.GAP) - T.GAP + 2 * T.MARGE_GRILLE
        haut_grille = g.nombre_de_lignes   * (T.TAILLE_CASE + T.GAP) - T.GAP + 2 * T.MARGE_GRILLE

        larg_fen = max(larg_grille, 460)
        haut_fen = T.HAUTEUR_MENU + T.HAUTEUR_ENTETE + self.HAUTEUR_BONUS + haut_grille + 8

        self._screen = pygame.display.set_mode((larg_fen, haut_fen))

        offset_x = (larg_fen - larg_grille) // 2
        offset_y = T.HAUTEUR_MENU + T.HAUTEUR_ENTETE + self.HAUTEUR_BONUS + 4

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

        # Positionner le bouton bonus au centre de la barre bonus
        bonus_cy = T.HAUTEUR_MENU + T.HAUTEUR_ENTETE + self.HAUTEUR_BONUS // 2 - 4
        self._bouton_bonus.centrer(larg_fen // 2, bonus_cy)

        # Reset overlay
        self._overlay_alpha = 0
        self._message_fin   = ""
        self._overlay_actif = False

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

        bonus_actif = (
            self._jeu.bonus_drapeaux_restants > 0
            and self._jeu.etat == Jeu.ETAT_EN_COURS
        )
        self._survol_bonus = (
            not self._overlay_actif
            and bonus_actif
            and self._bouton_bonus.collide((mx, my))
        )

        self._overlay_btn_survol = (
            self._overlay_actif
            and self._overlay_btn_rect.collidepoint(mx, my)
        )

        if not self._overlay_actif:
            self._survol_case = self._grille_renderer.case_sous_curseur(mx, my)
        else:
            self._survol_case = None

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self._traiter_clic_gauche(event.pos)

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                if not self._overlay_actif:
                    case_pos = self._grille_renderer.case_sous_curseur(*event.pos)
                    if case_pos:
                        self._jeu.clic_droit(*case_pos)

    def _traiter_clic_gauche(self, pos):
        # Priorite 1 : overlay bloquant
        if self._overlay_actif:
            if self._overlay_btn_rect.collidepoint(pos):
                self._reset()
            return

        # Priorite 2 : bouton RESET de l'en-tete
        if self._entete_renderer.bouton.collide(pos):
            self._reset()
            return

        # Priorite 3 : bouton BONUS (instance de BoutonBonus)
        if self._bouton_bonus.collide(pos):
            if (self._jeu.bonus_drapeaux_restants > 0
                    and self._jeu.etat == Jeu.ETAT_EN_COURS):
                resultat = self._jeu.utiliser_bonus_drapeau()
                if resultat:
                    self._jouer_son_bonus()
            return

        # Priorite 4 : bouton de niveau
        nom = self._menu_renderer.niveau_sous_curseur(pos)
        if nom:
            self._changer_niveau(nom)
            return

        # Priorite 5 : case de la grille
        case_pos = self._grille_renderer.case_sous_curseur(*pos)
        if case_pos:
            l, c = case_pos
            self._on_clic_gauche(l, c)

    def _jouer_son_bonus(self):
        """Joue le son WTF une seule fois si disponible."""
        if self._son_bonus:
            self._son_bonus.stop()
            self._son_bonus.play()

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
        self._overlay_actif = True

    # ── Rendu ─────────────────────────────────────────────────────────────────

    def _dessiner(self):
        self._screen.fill(T.FOND_FENETRE)
        w = self._screen.get_width()

        # Barre de niveaux
        menu_surf = self._screen.subsurface(pygame.Rect(0, 0, w, T.HAUTEUR_MENU))
        self._menu_renderer.dessiner(menu_surf, pygame.mouse.get_pos())

        pygame.draw.rect(self._screen, T.COULEUR_SEPARATEUR,
                         (0, T.HAUTEUR_MENU, w, 2))

        # En-tete
        entete_surf = self._screen.subsurface(
            pygame.Rect(0, T.HAUTEUR_MENU, w, T.HAUTEUR_ENTETE)
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

        pygame.draw.rect(self._screen, T.COULEUR_SEPARATEUR,
                         (0, T.HAUTEUR_MENU + T.HAUTEUR_ENTETE, w, 2))

        # Barre BONUS
        bonus_top = T.HAUTEUR_MENU + T.HAUTEUR_ENTETE
        rect_arrondi(self._screen, (255, 252, 230),
                     pygame.Rect(0, bonus_top, w, self.HAUTEUR_BONUS), rayon=0)

        bonus_actif = (
            self._jeu.bonus_drapeaux_restants > 0
            and self._jeu.etat == Jeu.ETAT_EN_COURS
            and not self._overlay_actif
        )
        self._bouton_bonus.dessiner(
            self._screen,
            restants = self._jeu.bonus_drapeaux_restants,
            actif    = bonus_actif,
            survol   = self._survol_bonus,
        )

        font_lbl = pygame.font.SysFont("couriernew", 11)
        texte_gauche(self._screen, font_lbl, "BONUS :",      (120, 100, 40), (12, bonus_top + 8))
        texte_gauche(self._screen, font_lbl, "drapeau",      (150, 130, 60), (12, bonus_top + 26))
        texte_gauche(self._screen, font_lbl, "sur une bombe",(150, 130, 60), (12, bonus_top + 40))

        pygame.draw.rect(self._screen, (210, 190, 100),
                         (0, bonus_top + self.HAUTEUR_BONUS - 1, w, 1))
        pygame.draw.rect(self._screen, T.COULEUR_SEPARATEUR,
                         (0, bonus_top + self.HAUTEUR_BONUS, w, 2))

        # Grille
        self._grille_renderer.dessiner(self._screen, self._survol_case)

        # Overlay fin de partie
        if self._overlay_actif:
            self._dessiner_overlay()

        pygame.display.flip()

    def _dessiner_overlay(self):
        """Overlay de fin : fond sombre, message, bouton NOUVELLE PARTIE."""
        if self._overlay_alpha < 210:
            self._overlay_alpha = min(self._overlay_alpha + 8, 210)

        w, h = self._screen.get_size()
        overlay = pygame.Surface((w, h), pygame.SRCALPHA)
        overlay.fill((10, 15, 35, self._overlay_alpha))
        self._screen.blit(overlay, (0, 0))

        if self._overlay_alpha < 120:
            return

        bw, bh = 500, 175
        bx = (w - bw) // 2
        by = (h - bh) // 2

        victoire   = "Bravo" in self._message_fin
        fond_boite = (230, 250, 235, 245) if victoire else (250, 230, 230, 245)
        bord_coul  = (30, 155, 75)        if victoire else (190, 45, 60)
        coul_titre = (25, 130, 60)        if victoire else (180, 35, 50)

        box = pygame.Surface((bw, bh), pygame.SRCALPHA)
        box.fill(fond_boite)
        self._screen.blit(box, (bx, by))
        pygame.draw.rect(self._screen, bord_coul, (bx, by, bw, bh), 3, border_radius=12)

        font_msg = pygame.font.SysFont("couriernew", 17, bold=True)
        font_sm  = pygame.font.SysFont("couriernew", 13)
        font_btn = pygame.font.SysFont("couriernew", 14, bold=True)

        surf_msg = font_msg.render(self._message_fin, True, coul_titre)
        self._screen.blit(surf_msg, (bx + (bw - surf_msg.get_width()) // 2, by + 16))

        surf_temps = font_sm.render(
            f"Temps : {self._jeu.temps_formate()}  |  Bombes : {self._jeu.nb_bombes}",
            True, (60, 70, 90)
        )
        self._screen.blit(surf_temps, (bx + (bw - surf_temps.get_width()) // 2, by + 50))

        # Bouton NOUVELLE PARTIE
        btn_w, btn_h = 190, 44
        btn_x = bx + (bw - btn_w) // 2
        btn_y = by + bh - btn_h - 16
        self._overlay_btn_rect = pygame.Rect(btn_x, btn_y, btn_w, btn_h)

        fond_btn = (
            (55, 185, 100) if victoire else (220, 65, 80)
        ) if self._overlay_btn_survol else (
            (35, 155, 75)  if victoire else (190, 45, 60)
        )

        rect_arrondi(self._screen, fond_btn, self._overlay_btn_rect, rayon=9)
        pygame.draw.rect(self._screen, (255, 255, 255),
                         self._overlay_btn_rect, 1, border_radius=9)

        surf_btn = font_btn.render("NOUVELLE PARTIE", True, (255, 255, 255))
        self._screen.blit(surf_btn, (
            btn_x + (btn_w - surf_btn.get_width()) // 2,
            btn_y + (btn_h - surf_btn.get_height()) // 2
        ))

        surf_aide = font_sm.render(
            "ou cliquez RESET dans la barre du haut",
            True, (130, 140, 160)
        )
        self._screen.blit(surf_aide,
                          (bx + (bw - surf_aide.get_width()) // 2, by + bh - 14))
