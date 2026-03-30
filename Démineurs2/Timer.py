"""
Timer : chronomettre de partie.
Une classe = un fichier (principe de responsabilite unique).
"""
import time


class Timer:
    """
    Chronomettre de partie.
    Demarre au premier clic, s'arrete a la victoire ou defaite.
    """

    def __init__(self):
        self._debut    = 0.0
        self._fin      = 0.0
        self._en_cours = False

    def demarrer(self):
        """Demarre le chronometre."""
        self._debut    = time.time()
        self._fin      = 0.0
        self._en_cours = True

    def arreter(self):
        """Arrete le chronometre."""
        if self._en_cours:
            self._fin      = time.time()
            self._en_cours = False

    def reinitialiser(self):
        """Remet le chronometre a zero."""
        self._debut    = 0.0
        self._fin      = 0.0
        self._en_cours = False

    def secondes(self) -> int:
        """Retourne le nombre de secondes ecoulees."""
        if not self._debut:
            return 0
        fin = self._fin if not self._en_cours else time.time()
        return int(fin - self._debut)

    def formater(self) -> str:
        """Retourne le temps formate MM:SS."""
        s = self.secondes()
        return f"{s // 60:02d}:{s % 60:02d}"

    def est_en_cours(self) -> bool:
        return self._en_cours
