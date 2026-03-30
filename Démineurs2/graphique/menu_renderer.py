"""
MenuRenderer : barre de selection du niveau de difficulte.
Importe BoutonNiveau depuis bouton_niveau.py (une classe par fichier).
"""
import pygame
from graphique import theme as T
from graphique.dessin import rect_arrondi
from graphique.bouton_niveau import BoutonNiveau


class MenuRenderer:
    """
    Dessine la barre de niveaux et detecte les clics sur les boutons.
    Utilise des instances de BoutonNiveau (importe depuis bouton_niveau.py).
    """

    LARGEUR_BTN = 110
    HAUTEUR_BTN = 30
    ESPACEMENT  = 10

    def __init__(self, font: pygame.font.Font, largeur_fenetre: int, niveau_actuel: str):
        self._font          = font
        self._largeur       = largeur_fenetre
        self._niveau_actuel = niveau_actuel
        self._boutons       = []
        self._construire()

    def _construire(self):
        from Jeu import Jeu
        noms    = Jeu.noms_niveaux()
        total   = len(noms) * self.LARGEUR_BTN + (len(noms) - 1) * self.ESPACEMENT
        start_x = (self._largeur - total) // 2
        y       = (T.HAUTEUR_MENU - self.HAUTEUR_BTN) // 2
        for i, nom in enumerate(noms):
            x    = start_x + i * (self.LARGEUR_BTN + self.ESPACEMENT)
            rect = pygame.Rect(x, y, self.LARGEUR_BTN, self.HAUTEUR_BTN)
            self._boutons.append(BoutonNiveau(nom, rect, self._font))

    def dessiner(self, surface: pygame.Surface, survol_pos):
        rect_fond = pygame.Rect(0, 0, self._largeur, T.HAUTEUR_MENU)
        rect_arrondi(surface, T.FOND_FENETRE, rect_fond, rayon=0)
        label = self._font.render("NIVEAU :", True, T.COULEUR_ACCENT)
        surface.blit(label, (10, (T.HAUTEUR_MENU - label.get_height()) // 2))
        for btn in self._boutons:
            survol = btn.collide(survol_pos) if survol_pos else False
            btn.dessiner(surface, btn.nom == self._niveau_actuel, survol)

    def niveau_sous_curseur(self, pos):
        for btn in self._boutons:
            if btn.collide(pos):
                return btn.nom
        return None

    def definir_niveau(self, nom: str):
        self._niveau_actuel = nom

    def mettre_a_jour_largeur(self, largeur: int):
        self._largeur = largeur
        self._boutons.clear()
        self._construire()
