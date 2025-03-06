
# code de génération de couleurs selon le 
# nombre de parts (nb de couleurs nécessaire)

def generate_colors(n:int)->list[str]:
    """Génère N couleurs différentes en format hexadécimal, réparties uniformément.
    Les couleurs changent à chaque exécution grâce à un mélange aléatoire.
    """
    # Diviser l'espace des couleurs de manière uniforme
    step = 256 // n
    # Générer une palette de couleurs de base
    tmp = range(n)
    base_colors = [(i * step, j * step, k * step) for i in tmp for j in tmp for k in tmp]
    rd.shuffle(base_colors) # mélange
    selected_colors = base_colors[:n] # les N premières couleurs
    # return conveted colors to hex
    return [f"#{r:02x}{g:02x}{b:02x}" for r, g, b in selected_colors]

def int_to_rgb(color_int_:int)->str:
    '''convertit une valeur int tres grande (255**3) en rgb'''
    if type(color_int_) != int:
        raise ValueError(f"(function) int_to_rgb(n=\"{color_int_}\"), n is not int")
    color_int = color_int_ % (256**3+1)
    r = (color_int >> 16) & 0xFF
    g = (color_int >> 8) & 0xFF
    b = color_int & 0xFF
    return f"#{r:02x}{g:02x}{b:02x}"

def generate_colors2(n:int)->list[str]:
    """Génère N couleurs réparties uniformément 
    avec un décalage cyclique global aléatoire format rgb hex (#000000)"""
    max_colors = 256 ** 3  
    step = max_colors // n
    rd_decal = rd.randint(0, max_colors - 1) 
    # Générer les N couleurs en considérant l'espace continu
    colors = [(i * step + rd_decal) % max_colors for i in range(n)]
    # Convertir les couleurs décalées en format RGB puis en hexadécimal
    return [int_to_rgb(color) for color in colors]