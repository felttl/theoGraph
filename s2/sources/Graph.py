class Graph:
    """créée un graphe avec une liste de "Node" en paramètre et un titre
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
        self.color_edges=[] # arretes a colorer (GUI)
        self.is_colored=True # autorise la coloration (GUI)
        self._render()
        self.__grg = [] # variable interne pour la repr graphique (cytoscape callback)
        
    def _render(self):
        '''initialize graphic things'''
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
        """effectue le rendu du graphe visuellement
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

    def _color_grg(self, nb_colors:int):
        '''permet de colorer le graphe affiché avec cytoscape'''
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
        self._color_grg(couleur_max) # rendu graphique

        