"""
MenuRenderer : barre de sélection du niveau de difficulté.
"""
import pygame
from niveau import Niveau
from graphique import theme as T
from graphique.dessin import rect_arrondi, texte_centre


class BoutonNiveau:
    """Un bouton de niveau de difficulté."""

    def __init__(self, nom: str, rect: pygame.Rect, font: pygame.font.Font):
        self.nom = nom
        self.rect = rect
        self._font = font

    def dessiner(self, surface: pygame.Surface, actif: bool, survol: bool):
        if actif:
            couleur = T.COULEUR_MENU_ACTIF
        elif survol:
            couleur = (55, 85, 140)
        else:
            couleur = T.COULEUR_MENU_INACTIF
        rect_arrondi(surface, couleur, self.rect, rayon=6)
        texte_centre(surface, self._font, self.nom.upper(), T.COULEUR_MENU_TEXTE, self.rect)

    def collide(self, pos) -> bool:
        return self.rect.collidepoint(pos)


class MenuRenderer:
    """
    Dessine la barre de niveaux et détecte les clics sur les boutons.
    """

    LARGEUR_BTN = 110
    HAUTEUR_BTN = 30
    ESPACEMENT  = 10

    def __init__(self, font: pygame.font.Font, largeur_fenetre: int, niveau_actuel: str):
        self._font = font
        self._largeur = largeur_fenetre
        self._niveau_actuel = niveau_actuel
        self._boutons: list[BoutonNiveau] = []
        self._construire()

    def _construire(self):
        noms = Niveau.noms_disponibles()
        total = len(noms) * self.LARGEUR_BTN + (len(noms) - 1) * self.ESPACEMENT
        start_x = (self._largeur - total) // 2
        y = (T.HAUTEUR_MENU - self.HAUTEUR_BTN) // 2

        for i, nom in enumerate(noms):
            x = start_x + i * (self.LARGEUR_BTN + self.ESPACEMENT)
            rect = pygame.Rect(x, y, self.LARGEUR_BTN, self.HAUTEUR_BTN)
            self._boutons.append(BoutonNiveau(nom, rect, self._font))

    def dessiner(self, surface: pygame.Surface, survol_pos):
        rect_fond = pygame.Rect(0, 0, self._largeur, T.HAUTEUR_MENU)
        rect_arrondi(surface, T.FOND_FENETRE, rect_fond, rayon=0)

        # Label
        label = self._font.render("NIVEAU :", True, T.COULEUR_ACCENT)
        surface.blit(label, (10, (T.HAUTEUR_MENU - label.get_height()) // 2))

        for btn in self._boutons:
            survol = btn.collide(survol_pos) if survol_pos else False
            btn.dessiner(surface, btn.nom == self._niveau_actuel, survol)

    def niveau_sous_curseur(self, pos) -> str | None:
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
