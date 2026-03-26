"""
Jeu : controleur principal qui orchestre la Grille, le Timer et les niveaux.
Fait le pont entre la logique metier (Grille/Cases) et l'interface graphique.
"""
import random
import time


# ── Configuration des niveaux ──────────────────────────────────────────────────

NIVEAUX = {
    "Facile":    {"lignes": 9,  "colonnes": 9,  "bombes_min": 8,  "bombes_max": 12},
    "Moyen":     {"lignes": 16, "colonnes": 16, "bombes_min": 30, "bombes_max": 45},
    "Difficile": {"lignes": 16, "colonnes": 30, "bombes_min": 70, "bombes_max": 99},
}


class Timer:
    """Chronomettre de partie."""

    def __init__(self):
        self._debut = 0.0
        self._fin = 0.0
        self._en_cours = False

    def demarrer(self):
        self._debut = time.time()
        self._fin = 0.0
        self._en_cours = True

    def arreter(self):
        if self._en_cours:
            self._fin = time.time()
            self._en_cours = False

    def reinitialiser(self):
        self._debut = 0.0
        self._fin = 0.0
        self._en_cours = False

    def secondes(self) -> int:
        if not self._debut:
            return 0
        fin = self._fin if not self._en_cours else time.time()
        return int(fin - self._debut)

    def formater(self) -> str:
        s = self.secondes()
        return f"{s // 60:02d}:{s % 60:02d}"

    def est_en_cours(self) -> bool:
        return self._en_cours


class Jeu:
    """
    Orchestre une partie de Demineur.
    Utilise Grille (logique) + Timer (chrono) + config niveau (taille/bombes).
    """

    ETAT_ATTENTE  = "attente"
    ETAT_EN_COURS = "en_cours"
    ETAT_GAGNE    = "gagne"
    ETAT_PERDU    = "perdu"

    def __init__(self, nom_niveau: str = "Facile"):
        self.nom_niveau = nom_niveau
        self.timer = Timer()
        self.etat = self.ETAT_ATTENTE
        self.grille = None
        self.nb_bombes = 0
        self._mine_touchee = None
        self._initialiser_grille()

    def _initialiser_grille(self):
        """Cree une nouvelle Grille selon le niveau choisi."""
        from Grille import Grille
        cfg = NIVEAUX[self.nom_niveau]
        self.nb_bombes = random.randint(cfg["bombes_min"], cfg["bombes_max"])
        self.grille = Grille(cfg["lignes"], cfg["colonnes"], self.nb_bombes)
        self.etat = self.ETAT_ATTENTE
        self.timer.reinitialiser()
        self._mine_touchee = None

    # ── Proprietes utiles pour les renderers ──────────────────────────────────

    @property
    def lignes(self) -> int:
        return self.grille.nombre_de_lignes

    @property
    def colonnes(self) -> int:
        return self.grille.nombre_de_colonnes

    # ── Actions joueur ────────────────────────────────────────────────────────

    def clic_gauche(self, ligne: int, colonne: int):
        """Traite un clic gauche : place bombes au 1er clic, puis revele."""
        if self.etat in (self.ETAT_GAGNE, self.ETAT_PERDU):
            return

        case = self.grille.cases[ligne][colonne]
        if case.etat == "drapeau":
            return

        # Premier clic : placer les bombes et demarrer le timer
        if self.etat == self.ETAT_ATTENTE:
            # Grille.placer_les_bombes marque aussi les cases est_une_bombe=True
            self.grille.placer_les_bombes(ligne, colonne)
            self.grille.calcule_nombre_de_bombe_autour_de_chaque_cases()
            self.timer.demarrer()
            self.etat = self.ETAT_EN_COURS

        # Deleguer le clic a la Grille
        self.grille.clique_gauche(ligne, colonne)

        # Verifier les conditions de fin
        if case.est_une_bombe and case.etat == "revelee":
            self._mine_touchee = (ligne, colonne)
            self.etat = self.ETAT_PERDU
            self.timer.arreter()
        elif self.grille.a_gagne():
            self.etat = self.ETAT_GAGNE
            self.timer.arreter()

    def clic_droit(self, ligne: int, colonne: int):
        """Traite un clic droit : cycle drapeau/question/cache."""
        if self.etat in (self.ETAT_GAGNE, self.ETAT_PERDU):
            return
        self.grille.clique_droit(ligne, colonne)

    def reinitialiser(self, nom_niveau: str = None):
        """Remet a zero la partie, avec optionnellement un nouveau niveau."""
        if nom_niveau:
            self.nom_niveau = nom_niveau
        self._initialiser_grille()

    # ── Infos pour l'interface ─────────────────────────────────────────────────

    def nb_bombes_restantes(self) -> int:
        """Bombes totales moins drapeaux poses."""
        return self.nb_bombes - self.compter_drapeaux()

    def compter_drapeaux(self) -> int:
        return sum(1 for l in self.grille.cases for c in l if c.etat == "drapeau")

    def compter_questions(self) -> int:
        return sum(1 for l in self.grille.cases for c in l if c.etat == "question")

    def temps_formate(self) -> str:
        return self.timer.formater()

    def mine_touchee(self):
        return self._mine_touchee

    def est_termine(self) -> bool:
        return self.etat in (self.ETAT_GAGNE, self.ETAT_PERDU)

    @staticmethod
    def noms_niveaux() -> list:
        return list(NIVEAUX.keys())
