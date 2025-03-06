#!bin/python3
# modules importants pour le(s) tp(s) :

# visualisation des couleurs et autres... (partie graphique)
from dash import Dash, html # type: ignore
import dash_cytoscape as cyto # type: ignore

# partie système
from time import time, sleep
import os, sys, random as rd
from random import randint

# partie mathématique + structure
import numpy as np # type: ignore
from math import inf, sqrt, cos, sin, tan

# ON IMPORTE LES CLASSES DU TP PRECEDENT (TP1 et 2 du Semestre 1)
# on import les classes d'anciens projet de théorie des graphes pour pas 
# passer notre temps a coder mais a comprendre le problème
class V:
    '''représente les informations des sommets (vertex)'''
    def __init__(self, name:str | int, weight=0):
        self.name = name
        self.weight = weight

# classe impotée d'ancien projet
class Vertex:
    """
    représente les sommets et leurs adjacences dans un graphe
    
    on crée la classe qui s'occupe de toutes les adjacences entre 
    les sommets (vertex/vertices) et leurs autres sommets reliés
    les arrêtes (edges) ne sont pas représentés car c'est la matrice d'adjacence qui s'occupe de ça
    qui est situé dans la classe Graph
    """
    id = 0 # identifiant du sommet 

    def __init__(self, name:str, neighbor:list[V]=[]):
        self.name = name
        self.total_weight = sum([v.weight for v in neighbor]) # poids total du sommet
        self.neighbor = neighbor
        self.vertices_names = [v.name for v in self.neighbor]
        self.degree = len(neighbor)
        self.id = Vertex.id
        Vertex.id += 1

    def __str__(self):
        '''si on affiche Node (print(Node)) renverra ce qui suit'''
        res = f"{self.name} ["
        v_size = len(self.neighbor)
        for i, v in enumerate(self.neighbor):
            res += f"{v.name} w={v.weight}"
            if(i!=v_size-1):
                if v_size>1:
                    res+="," 
                res+=" "
        res+="]"
        return res

# classe joutée
class Edge:
    '''représente une arrête entre deux sommets/vertex
    manière différente de représenter un graphe'''

    id = 0

    def __init__(self, vfrom:str | int, vto:str | int, weight: int | float):
        self.a = vfrom
        self.b = vto
        self.weight = weight
        self.id = Edge.id
        Edge.id += 1
    
    def __eq__(self, other:"Edge"): # equivalent to self == other
        '''permet d'utiliser l'objet dans un set (le rendre hashable)
        pour faire des comparaisons entre des ensembles (set) d'objet Edge'''
        # On considère que deux arêtes sont égales si leurs sommets et poids sont égaux
        return (self.a == other.a and self.b == other.b and self.weight == other.weight)
    
    def __ne__(self, edge:object): # equivalent de !=
        return not self.__eq__(edge)    

    def __hash__(self): # equivalent to set(self) == set(other)
        """permet d'utiliser l'objet dans un set (le rendre hashable)
        pour faire des comparaisons entre des ensembles (set) d'objet Edge"""
        # Calculer le hash en fonction des attributs de l'objet
        return hash((self.start, self.end, self.weight))

class Graph:
    """créée un graphe avec une liste de "Vertex" en paramètre et un titre
    @version 3.0.1"""

    def __init__(self, data:list[Vertex], title:str="default"): # OK
        '''@version 3.0.0'''
        self.title = title # titre du graphique si utilisé
        self.adj = data # liste d'adjacences
        self.edges = []
        self.verticesn = [] # liste des sommets (seulement les noms)
        self.weight = 0 # poids total du graphe    
        self.degree = 0 # pas encore calculé le degré du graphe
        self.is_complete = True
        for vx in self.adj:
            self.verticesn.append(vx.name)
            self.weight += vx.total_weight
            for v in vx.neighbor:
                self.edges.append(Edge(vx.name, v.name, v.weight))
                self.degree += 1
        self.create_matrix() # matrice des liens entre les noeuds (Edges) (matrice d'adjacences)
        self.port = 8054+randint(10,round(1e4))
        self.show_weights=True
        self.color_edges=[] # arretes a colorer (UGI)
        self.is_colored=True # autorise la coloration (UGI)

    def create_matrix(self): # OK
        """créer la matrice d'ajdacence des points\n
        (fonctionne avec les graphes orienté également)
        @version {3.0.1}
        prochaine version supprimer l'initialisation de la matrice a False
        et ajouter un par un les True et False (reduction de complexité)
        """
        # si on trouve que m[i][j] != m[j][i] 
        # ou que les poids ne sont pas les mêmes c'est oriente
        # attention dans les Vertex les V peuvent ne pas être dans l'ordre
        self.matrix = [[False for _ in self.adj] for _ in self.adj]
        self.is_oriented=False
        for lin, vis in enumerate(self.adj):
            for v in vis.neighbor:
                v_jx_idx = self.verticesn.index(v.name)
                self.matrix[lin][v_jx_idx]=True
                if not self.is_oriented:
                    if vis.name not in self.adj[v_jx_idx].vertices_names:
                        self.is_oriented=True
                    else:
                        vi_xj_idx = self.adj[v_jx_idx].vertices_names.index(vis.name)
                        vi_ji = self.adj[v_jx_idx].neighbor[vi_xj_idx]
                        if v.weight != vi_ji.weight :
                            self.is_oriented=True
        iter = range(len(self.matrix))
        # matrice d'un graphe complet avec la liste des sommets actuel
        complete = [[self.matrix[i][j] if i == j else True for i in iter] for j in iter]
        if(self.matrix == complete):
            self.is_complete = True

    def __str__(self): # OK
        """si jamais on print un graph (print(Graph)) c'est executé ici
        affichage au plus simple du graphe avec des caractères
        @version 3.0.0"""
        res = ""
        for i, vis in enumerate(self.adj):
            res += f"{i}\t | {vis.name} ["
            v_size = len(vis.neighbor)
            for j in range(v_size):
                res += f"{vis.neighbor[j].name} w={vis.neighbor[j].weight}"
                if(j!=v_size-1):
                    if v_size>1:
                        res += "," 
                    res+=" "
            res += "]\n"
        return res
    
    def _sort_edges(self, edges:list[Edge])->list[Edge]: # OK complexite≈O(n+log(5n))
        """fonction privée a ne pas utiliser (en dehors de la classe)
        algorithme reccursif pour les problèmes de pronfondeur et de performances
        @version 3.0.0"""
        if len(edges)<2 :
            return edges
        else:
            pivot = edges[len(edges)//2].weight
            l, m, r = [],[],[] # mineurs, égal, majeurs 
            for e in edges:
                if(e.weight < pivot): l.append(e)
                    # si reccursion sur len(m) ce n'est jamais < 2
                    # et donc (boucle infini) dans certains cas                
                elif(e.weight == pivot): m.append(e) 
                else: r.append(e)
            return self._sort_edges(l)+m+self._sort_edges(r)

    def sort_by_weight(self): # OK
        """trie le graphe par poids croissants(asc)
        on trie chaque arrêtes du graphe
        @version 3.0.0
        """
        self.edges = self._sort_edges(self.edges)

    def show_edges(self):
        '''affiche les edges sous forme de liste de string
        @version 3.0.0'''
        print([e.a+e.b+" w="+str(e.weight) for e in self.edges])

    def resume(self):
        '''crée un résumé du graphe
        @version 3.0.0'''
        print("quelques informations sur le graphe : \n")
        print(f"\tdegré: {self.degree}")
        print(f"\tpoids: {self.weight}")
        print(f"\tcomplet : {self.is_complete} (def: si tous les sommets sont reliés)")
        print(f"\tplanaire: voir si les arrêtes se croisent ou non")
        print(f"\t\tnecessite surement de déplacer\n\t\tles noeuds (sur la partie graphique)")

# code de génération de couleurs selon le 
# nombre de parts (nb de couleurs nécessaire)
# importé de mes librairies personelles (pas codé dans le cours)

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

class Graph(Graph): 
    # on ajoute des méthodes a l'existant (extension)

    def __init__(self, data, title = "default"):
        super().__init__(data, title)
        self._render()

    def _render(self):
        '''initialise les parties graphiques (cytoscape)
        trés utile pour quand on utilise self.render() sur un graphe (qui permet 
        d'afficher le graphique)'''
        self.custom_style = {
            'width': '100%', 
            'height': '500px',
            "border": "3px white solid",
            "border-radius":"5px",
            "background-color":"#666666",
            "title" : {"background-color":"white"}
        }
        self.unique = f' {time()%1e4:.5}'
        allow_arrows = "linear" # ce style n'autorise pas les flèches
        if self.is_oriented:
            allow_arrows = "bezier" # ce style oui
        self.my_styles_sheet = [{
                'selector': 'node',
                'style': {
                    'background-color': '#222222', 
                    'color': 'white',
                    'label': 'data(label)',
                    'font-size': '16px',
                    'text-valign': 'center', 
                    'text-halign': 'center' 
                }
            },
            {
                'selector': 'edge',
                'style': {
                    'width': 2,
                    'target-arrow-shape': "vee",
                    "target-arrow-color": "#4a7cf2",
                    'arrow-scale': 2,
                    'curve-style': allow_arrows
                }
            }
        ]

    def render(self, layout_name="breadthfirst"): # rendu UGI
        """effectue le rendu du graphe visuellement avec Cytoscape
        @version 3.1.4"""
        if self.show_weights:
            self.my_styles_sheet.append({
                'selector': 'edge',
                'style': {
                    'label': 'data(weight)',
                    "color": 'white'
                }
            })   
        elems = [] # éléments à afficher (formattés)
        for node in self.adj:
            elems.append({'data': {"id":node.name, "label":node.name}})
        # add edges
        for edge in self.edges:
            elems.append({
                'data': {
                    'source': edge.a, 
                    'target': edge.b, 
                    'weight': edge.weight
                }
            })
        app = Dash(self.title+self.unique)            
        app.layout = html.Div([
            cyto.Cytoscape(
                id='cytoscape'+self.unique,
                elements=elems,
                layout={'name': layout_name},
                style=self.custom_style,
                stylesheet=self.my_styles_sheet
            )
        ])
        print('\nrendu graphique : ')
        print(f"\tégalement ouvert sur la page web : \"localhost:{self.port}\"")
        print(f"\topened too at the web page : \"localhost:{self.port}\"")
        app.run_server(debug=True,port=self.port)

    # partie graphique optionelle (visualisation) de la fonction de cours
    def _coloration_grg(self, nb_colors:int):
        '''permet de colorer le graphe affiché avec cytoscape
        méthode privée a ne pas utiliser'''
        color = generate_colors(nb_colors)
        for k in self.res["data"]:
            v = self.res["data"][k]
            self.my_styles_sheet.append(
                { # la règle la plus importante a la fin (override des précédentes)
                    'selector': f'node[id="{k}"]',
                    'style': {
                        'background-color': f'{color[v-1]}',
                    }
                }                    
            )

    # fonction de cours
    def coloration(self)->dict[str:int, str:dict[str:int]]:
        """Réalise une coloration des sommets d'un graphe donné.
        renvoie un dict: Un dictionnaire associant chaque sommet à une couleur numérotée.
        @version 3.5.9
        """
        sommets_tries = sorted(self.adj, key=lambda v: len(v.neighbor), reverse=True)
        # Initialiser les couleurs
        coloration = {vertex.name: None for vertex in self.adj}
        couleur_max = 0
        # Attribuer les couleurs
        for vertex in sommets_tries:
            # Collecter les couleurs déjà utilisées par les voisins
            couleurs_voisines = [
                coloration[neighbor.name]
                for neighbor in vertex.neighbor
                if coloration[neighbor.name] is not None
            ]
            # Trouver la première couleur non utilisée
            couleur = 1
            while couleur in couleurs_voisines:
                couleur += 1
            coloration[vertex.name] = couleur
            couleur_max = max(couleur_max, couleur)
            coloration[vertex.name] = couleur
            couleur_max = max(couleur_max, couleur)
        # pour voir le résultat de l'extérieur            
        self.res=dict()
        self.res["Nombre de couleurs utilisées"]=couleur_max
        self.res["data"] = coloration
        self._coloration_grg(couleur_max) # rendu graphique

#################################################################

    # méthode importée d'ancien projets
    @staticmethod
    def dfs(graph:Graph)->list[str]: # a faire plus tard
        '''Fonction DFS pour trouver le chemin le plus court entre 2 sommets
        Depth First Search (algorithme de parcours en profondeur)'''
        visited = set(graph.adj[0].name)
        path = list(graph.adj[0].name)
        if(graph.is_oriented):
            # code here
            ...
        else:
            # code here
            ...
        return path

    # a implémenter hors du cours (importé)
    @staticmethod
    def get_cycles(edges: list[Edge]) -> list[list[Edge]]: # not OK
        '''Détecte les cycles dans un graphe orienté ou non orienté\n
        attention cependant sur les graphe orienté ça peut prendre beaucoup de temps\n
        renverra que les cycles différent (les cycles dans un ordre d'arrêtes\n
        différent n'y seront pas)'''
        visited = set()  # Pour marquer les sommets visités
        cycles = []  # stocker les cycles trouvés
        data : dict[V] = dict()
        for edge in edges:
            if edge.a not in data :
                data[edge.a] = []
            if edge.b not in data :
                data[edge.b] = []
            data[edge.a].append(
                V(edge.b, edge.weight)
            )
        graph = Graph([Vertex(name, data[name]) for name in data])
        visited.add(graph.edges[0].a)
        visited.add(graph.edges[0].b)
        current_path : list[Edge] = set(graph.edges[0])
        cpt : int
        carry : bool
        while(...):
            carry = True
            cpt = 1
            while(carry):
                current_e = graph.edges[cpt]
                if(current_e.a in visited and current_e.b not in visited):
                    visited.add(current_e.b)
                    current_path.add(current_e)
                elif(current_e.a not in visited and current_e.b not in visited):
                    ...
                elif(current_e.a in visited and current_e.b not in visited):
                    carry = False
                    ...
                cpt += 1
            cycles.append(list(current_path))
        return ...

    # fonction de cours
    def kruskal(self,red_tarjan_rule=False)->list[Edge]: # OK
        """renvoie l'arbre couvrant de poids minimal
        applique la règle rouge de tarjan si booléen est True (False par défaut)
        @version 3.1.4"""
        # comme vue en cours
        # trie les arrêtes de tout le graphe par poids croissants
        self.sort_by_weight()
        res : list[Edge] = []
        ok : bool = True
        if(self.is_oriented):
            ok=False
            raise NotImplemented("kruskal's algorithm not implemented yet for oriented graphs")
        if(red_tarjan_rule):
            ok=False
            raise NotImplemented("red tarjan rule not implemented yet")        
        if(len(self.adj)<3):
            ok=False
            raise Exception(f"under minimum required data ({len(self.adj)} vertices < 3)")
        if ok:
            self.poids_total : int | float = self.edges[0].weight
            visited = set(self.edges[0].a)
            visited.add(self.edges[0].b)
            res.append(self.edges[0])
            cpt = 0
            while(cpt < len(self.edges)):
                current = self.edges[cpt]
                if(current.a not in visited and current.b in visited):
                    visited.add(current.a)
                    res.append(current)
                    self.poids_total+=current.weight
                elif (current.a in visited and current.b not in visited):
                    visited.add(current.b)
                    res.append(current)
                    self.poids_total+=current.weight
                cpt += 1
        return res
    
    # fonction de cours
    def sollin(self) -> list[Edge]:
        """Renvoie l'arbre couvrant de poids minimal sous forme de liste d'arêtes."""
        if not self.adj:
            return []
        # Chaque sommet est une composante distincte
        components = {v.name: v.name for v in self.adj}  
        edges = []  # Liste des arêtes de l'arbre couvrant
        self.poids_total = 0
        while len(set(components.values())) > 1:  # Tant qu'il y a plusieurs composantes
            # Trouver l'arête de poids minimal pour chaque composante
            min_edges = {}
            for vertex in self.adj:
                for neighbor in vertex.neighbor:
                    # Vérifier que l'arête connecte deux composantes différentes
                    if components[vertex.name] != components[neighbor.name]:
                        # Vérifier si c'est la plus petite arête pour la composante
                        current_min = min_edges.get(components[vertex.name])
                        if not current_min or neighbor.weight < current_min.weight:
                            min_edges[components[vertex.name]] = Edge(vertex.name, neighbor.name, neighbor.weight)
            for edge in min_edges.values():
                if components[edge.b] != components[edge.a]:
                    edges.append(edge)
                    self.poids_total += edge.weight
                    # Fusionner les composantes
                    old_component = components[edge.a]
                    new_component = components[edge.b]
                    for v in components:
                        if components[v] == old_component:
                            components[v] = new_component

        return edges
    
    # rendu graphique optionnel
    def _prim(self, path:list[str]):
        '''fonction reccursive de l'algorithme de primm
        @version 2.0.0'''
        if(path == []):
            return self._prim(list(self.adj[randint(0,len(self.adj))]))
        else:
            pass

    # algorithme de Prim du cours
    def prim(self)->list[Edge]:
        """Renvoie l'arbre couvrant de poids minimal sous forme de liste d'arêtes."""
        if not self.adj:
            return []  # Si le graphe est vide
        # Initialisation
        rd = randint(0, len(self.adj) - 1)  # Choisir un sommet de départ au hasard
        visited = set([self.adj[rd].name])  # Sommets visités
        edges = []  # Liste des arêtes de l'arbre couvrant
        self.poids_total = 0
        self.sm = ""
        while len(visited) < len(self.adj):
            min_edge = None  # Arête avec le poids minimal
            # Chercher l'arête de poids minimal connectée à un sommet visité
            for vertex in [v for v in self.adj if v.name in visited]:
                for neighbor in vertex.neighbor:
                    if neighbor.name not in visited and (min_edge is None or neighbor.weight < min_edge.weight):
                        min_edge = Edge(vertex.name, neighbor.name, neighbor.weight)
            if min_edge:
                visited.add(min_edge.b)
                edges.append(min_edge)  # Ajouter l'arête à la liste des résultats
                self.poids_total += min_edge.weight
                self.sm += f"{min_edge.weight}+"
        # Nettoyage de la chaîne self.sm pour enlever le dernier "+"
        if self.sm.endswith("+"):
            self.sm = self.sm[:-1]
        return edges


    # autres alrogithme non vus a implémenter plus tard (hors cours)

    # importé de projets perso
    def welsh_powell(self):
        '''algorithme de coloration'''
        pass
    def steiner_tree(self)->Graph:
        """renoie un abre de steiner"""
        pass
    def bellman_ford()->Graph:
        '''renvoie un graphe orienté sans circuits'''
        pass








# ------------------ partie Exercice : ------------------

# exemple de fonctionnement

# rappel format du Vertex : 
# Vertex(nomActuel, [V("nomLié1", poid1),V("nomLié2", poid2),etc...])
data = [
    Vertex("1",[V("2",2),V("3",1)]),
    Vertex("2",[V("1",2),V("4",2),V("5",3),V("3",3)]),
    Vertex("3",[V("1",1),V("2",3),V("4",5)]),
    Vertex("4",[V("2",2),V("3",5),V("5",2),V("6",4)]),
    Vertex("5",[V("2",3),V("4",2),V("6",2)]),
    Vertex("6",[V("4",4),V("5",2)])
]
graphe = Graph(data,"exemple de graphe")
print(np.matrix(graphe.matrix))

# on crée la comparaison "a la main"
ok = [[False, True, True, False, False, False],
      [True, False, True, True, True, False],
      [True, True, False, True, False, False],
      [False, True, True, False, True, True],
      [False, True, False, True, False, True],
      [False, False, False, True, True, False]]
# on vérifie et renvoie un message si erreur
assert ok == graphe.matrix, "une des valeurs de la matrice attendue n'est pas bonne"

##  TP1 implémentation de la solution pour Kruskal, Prim et Sollin -------------------------

data = [
    Vertex("1",[V("2",2),V("3",1)]),
    Vertex("2",[V("1",2),V("4",2),V("5",3),V("3",3)]),
    Vertex("3",[V("1",1),V("2",3),V("4",5)]),
    Vertex("4",[V("2",2),V("3",5),V("5",2),V("6",4)]),
    Vertex("5",[V("2",3),V("4",2),V("6",2)]),
    Vertex("6",[V("4",4),V("5",2)])
]
# 3, 4, 6, 5, 4, 4
graphe = Graph(data) # conversion
print("graphe : ")
print(graphe)
# graph.prim() est une liste on peut la formater :
print("méthode Kruskal :")
print("\t"," -> ".join([f"{edge.a}-{edge.b}" for edge in graphe.kruskal()]))
print(f"\tpoids de l'arbre couvrant minimal : {graphe.poids_total}")
print(graphe.sm)
print("méthode Prim :")
print("\t"," -> ".join([f"{edge.a}-{edge.b}" for edge in graphe.prim()]))
print(f"\tpoids de l'arbre couvrant minimal : {graphe.poids_total}")
print("méthode Sollin :")
print("\t"," -> ".join([f"{edge.a}-{edge.b}" for edge in graphe.sollin()]))
print(f"\tpoids de l'arbre couvrant minimal : {graphe.poids_total}")
graphe.render()
# données saisies a la main : (comparer le résultat)
# 654321 : poids = 14
# solution 312456: poids = 9

## TP2 implémentation de la solution pour la coloration et couplage -------------------------
# (a executer séparément normalement) 

# rappel format du Vertex : 
# Vertex(nomActuel, [V("nomLié1", poid1),V("nomLié2", poid2),etc...])
data = [
    Vertex("1",[V("2"),V("3")]),
    Vertex("2",[V("1"),V("4")]),
    Vertex("3",[V("1"),V("4"),V("6")]),
    Vertex("4",[V("2"),V("3"),V("5"),V("7")]),
    Vertex("5",[V("4"),V("7"),V("9")]),
    Vertex("6",[V("3"),V("7"),V("10")]),
    Vertex("7",[V("4"),V("5"),V("6"),V("8"),V("10")]),
    Vertex("8",[V("7"),V("9"),V("10")]),
    Vertex("9",[V("5"),V("8"),V("10")]),
    Vertex("10",[V("6"),V("7"),V("8"),V("9")])
]
graphe = Graph(data,"graphe a colorer")
graphe.show_weights=False
graphe.render()
print("""afficher les sommets (clefs):(valeur) avec les clef qui sont les nom des sommets
et valeurs les numéros des couleurs qui leurs sont attribués""")
print(graphe.coloration())
print(graphe.res)
