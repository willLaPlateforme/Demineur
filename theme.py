"""
Constantes visuelles : couleurs, polices, dimensions pour pygame.
"""

# ── Palette ───────────────────────────────────────────────────────────────────

FOND_FENETRE        = (15,  20,  40)
FOND_ENTETE         = (20,  28,  58)
FOND_GRILLE         = (12,  48,  90)
FOND_CASE_CACHEE    = (35,  68, 120)
FOND_CASE_REVELEE   = (220, 220, 215)
FOND_CASE_MINE      = (200,  50,  50)
FOND_CASE_MINE_HIT  = (255,  30,  30)   # mine cliquée
FOND_CASE_SURVOL    = (55,  95, 155)
FOND_CASE_DRAPEAU   = (35,  68, 120)

BORD_CASE_CLAIR     = (70, 110, 180)
BORD_CASE_SOMBRE    = (18,  38,  75)
BORD_REVELEE        = (180, 180, 175)

COULEUR_TEXTE       = (224, 224, 224)
COULEUR_ACCENT      = (233,  69,  96)
COULEUR_SUCCES      = (39,  174,  96)
COULEUR_TIMER       = (233,  69,  96)
COULEUR_SEPARATEUR  = (12,  48,  90)

COULEUR_MENU_ACTIF  = (233,  69,  96)
COULEUR_MENU_INACTIF= (45,  74, 122)
COULEUR_MENU_TEXTE  = (224, 224, 224)

# Couleurs des chiffres (1–8)
COULEURS_CHIFFRES = {
    1: ( 21, 101, 192),
    2: ( 46, 125,  50),
    3: (198,  40,  40),
    4: ( 74,  20, 140),
    5: (191,  54,  12),
    6: (  0, 131, 143),
    7: ( 33,  33,  33),
    8: (117, 117, 117),
}

# ── Dimensions ────────────────────────────────────────────────────────────────

TAILLE_CASE     = 36        # pixels par case
MARGE_GRILLE    = 10        # padding autour de la grille
HAUTEUR_ENTETE  = 72        # px
HAUTEUR_MENU    = 44        # px barre de niveaux
RAYON           = 4         # arrondi des cases
GAP             = 2         # espace entre cases

# ── Polices ───────────────────────────────────────────────────────────────────
# Chargées dynamiquement dans Fenetre via pygame.font

TAILLE_POLICE_CHIFFRE  = 18
TAILLE_POLICE_ENTETE   = 22
TAILLE_POLICE_LABEL    = 14
TAILLE_POLICE_BTN      = 13
