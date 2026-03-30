class Cases:

    def __init__(self, ligne, colonne):
        # Position de la case dans la grille (indices logiques, pas graphiques)
        self.ligne = ligne
        self.colonne = colonne

        # Indique si la case contient une mine (False par défaut)
        self.est_une_bombe = False

        # Nombre de mines autour de cette case (calculé plus tard par la grille)
        self.nombre_de_bombes_autour = 0

        # État initial de la case : toujours "cachee" au début de la partie
        self.etat = "cachee"
    
    def changer_etat_clic_droit(self):

        # Si la case est révélée, on ne peut pas mettre de drapeau ou de question
        if self.etat == "revelee":
            return

        # Si la case est cachée → elle devient un drapeau
        if self.etat == "cachee":
            self.etat = "drapeau"
            return

        # Si la case a un drapeau → elle devient un point d'interrogation
        if self.etat == "drapeau":
            self.etat = "question"
            return

        # Si la case est en question → elle redevient cachée
        if self.etat == "question":
            self.etat = "cachee"
            return

    #Clique gauche
    def reveler_case(self):
        # Si la case a un drapeau, on ne révèle pas
        if self.etat == "drapeau":
            return
        
        # Si la case est déjà révélée, on ne fait rien
        if self.etat == "revelee":
            return
        
        # Sinon, on révèle la case
        self.etat = "revelee"
