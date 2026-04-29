try:  # import as appropriate for 2.x vs. 3.x
    import tkinter as tk
    import tkinter.messagebox as tkMessageBox
except:
    import Tkinter as tk
    import tkMessageBox

from sokobanXSBLevels import *
from enum import Enum

"""
Direction :
    Utile pour gérer le calcul des positions pour les mouvements
"""
class Direction(Enum):
    Up = 1
    Down = 2
    Left = 3
    Right = 4
    
class Position(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return 'Position(' + str(self.x) + ',' + str(self.y) + str(')') 

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    #calcule de la nouvelle position
    def positionTowards(self, direction, offset):
        if direction == Direction.Up:
            return Position(self.x, self.y - offset)
        elif direction == Direction.Down:
            return Position(self.x, self.y + offset)
        elif direction == Direction.Left:
            return Position(self.x - offset, self.y)
        elif direction == Direction.Right:
            return Position(self.x + offset, self.y)

    #vérification si la place est valide
    def isValidInWharehouse(self, wharehouse):
        return wharehouse.isPositionValid(self)

    #convertir en position graphique
    def asCanvasPositionIn(self, elem):
        lx = self.getX() * elem.getWidth() 
        ly = self.getY() * elem.getHeight()
        return Position(lx, ly)
    
class WharehousePlan(object):
    def __init__(self):
        self.rawMatrix = []

    #Initialise une matrice avec le nombre de lignes et colonnes spécifiées, remplie avec des valeurs None
    def initializeMatrix(self, rows, columns):
        self.rawMatrix = [[None for _ in range(columns)] for _ in range(rows)]

    def appendRow(self, row):
        self.rawMatrix.append(row)

    #récuperer la position demandé
    def at(self, position):
        return self.rawMatrix[position.getY()][position.getX()]

    #positionner les élements selon notre demande aprés
    def atPut(self, position, elem):
        self.rawMatrix[position.getY()][position.getX()] = elem

    #verification si la postion ne dépasse pas la limite la fenetre
    def isPositionValid(self, position):
        return 0 <= position.getX() < len(self.rawMatrix[0]) and 0 <= position.getY() < len(self.rawMatrix)


    def hasFreePlaceAt(self, position):
        return self.at(position).isFreePlace()

    def asXsbMatrix(self):
        return xsbMatrix(self.rawMatrix)
    
    
class Floor(object):
    def __init__(self):
        None
    def isMovable(self):
        return False
    def canBeCovered(self):
        return True
    def xsbChar(self):
        return ' '
    def isFreePlace(self):
        return True
    def isGoal(self):
        return False
    

class Goal(object):
    def __init__(self, canvas, position):
        self.canvas = canvas
        self.position = position
        self.image = tk.PhotoImage(file="goal.png")
        self.width = self.image.width()
        self.height = self.image.height()
        self.canvas.create_image(position.asCanvasPositionIn(self).getX(),position.asCanvasPositionIn(self).getY(),
                                 image=self.image,anchor="nw",tags="static")


    def isMovable(self):
        return False

    def getHeight(self):
        return self.height
    
    def getWidth(self):
        return self.width

    def canBeCovered(self):
        return True
        
    def xsbChar(self):
        return '.'

    def isFreePlace(self):
        return True

    #Vérifie si goal est couvert par un objet déplaçable
    def isCovered(self):
        for obj in self.canvas.find_withtag("movable"): # Trouve tous les objets déplaçable sur canvas
            coords = self.canvas.coords(obj)
            goal_coords = self.position.asCanvasPositionIn(self)
            if coords[0] == goal_coords.getX() and coords[1] == goal_coords.getY():
                return True
        return False
        
    def isGoal(self):
        return True

class Wall(object):
    def __init__(self, canvas, position):
        self.canvas = canvas
        self.position = position
        self.image = tk.PhotoImage(file="wall.png")
        self.width = self.image.width()
        self.height = self.image.height()
        self.canvas.create_image(position.asCanvasPositionIn(self).getX(),position.asCanvasPositionIn(self).getY(),image=self.image,anchor="nw",tags="static")


    def getHeight(self):
        return self.height
    
    def getWidth(self):
        return self.width

    def isMovable(self):
        return False

    def canBeCovered(self):
        return False

    def xsbChar(self):
        return '#'

    def isFreePlace(self):
        return False
        
    def isGoal(self):
        return False
    
    
class Box(object):
    def __init__(self, canvas, wharehouse, position, onGoal):
        self.canvas = canvas
        self.wharehouse = wharehouse
        self.position = position
        self.onGoal = onGoal
        self.imageNormal = tk.PhotoImage(file="box.png")
        self.imageOnGoal = tk.PhotoImage(file="boxOnTarget.png")
        self.image = self.imageOnGoal if onGoal else self.imageNormal
        self.width = self.image.width()
        self.height = self.image.height()
        self.canvas_obj = self.canvas.create_image(position.asCanvasPositionIn(self).getX(),position.asCanvasPositionIn(self).getY(),image=self.image,anchor="nw",tags="movable")

    def getHeight(self):
        return self.height
    
    def getWidth(self):
        return self.width

    def isMovable(self):
        return True

    def canBeCovered(self):
        return False
        
    #Déplace un objet dans une direction donnée, si la position cible est libre.
    def moveTowards(self, direction):
        new_pos = self.position.positionTowards(direction, 1)  
        if self.wharehouse.hasFreePlaceAt(new_pos):  # Vérifie si la nouvelle position est libre
            self.position = new_pos  
            canvas_pos = new_pos.asCanvasPositionIn(self)  # Convertit la nouvelle position en coordonnées graphiques
            self.canvas.coords(self.canvas_obj, canvas_pos.getX(), canvas_pos.getY())  # Déplace l'objet sur le canevas
            self.onGoal = self.wharehouse.at(new_pos).isGoal()  # Vérifie si l'objet est sur un objectif
            self.image = self.imageOnGoal if self.onGoal else self.imageNormal  # Met à jour l'image selon la situation
            self.canvas.itemconfig(self.canvas_obj, image=self.image)  # Applique la nouvelle image à l'objet


 
    def xsbChar(self):
        return '*' if self.onGoal else '$'


    def isFreePlace(self):
        return False

    def startGoalCoveredAnimation(self):
        self.animation_steps = 10
        self.current_radius = 0
        self.animation_id = self.canvas.after(100, self.goalCoveredAnimation)
    
    def goalCoveredAnimation(self):
        if self.animation_steps > 0:
            x, y = self.position.asCanvasPositionIn(self).getX(), self.position.asCanvasPositionIn(self).getY()
            self.current_radius += 5
            self.canvas.create_oval(
                x - self.current_radius, y - self.current_radius,
                x + self.current_radius, y + self.current_radius,
                outline="green", width=2
            )
            self.animation_steps -= 1
            self.canvas.after(100, self.goalCoveredAnimation)
        else:
            self.cleanUpAnimation()
    
    def cleanUpAnimation(self):
        self.canvas.delete("animation")


class Mover(object):
    def __init__(self, canvas, wharehouse, position, onGoal):
        self.canvas = canvas
        self.wharehouse = wharehouse
        self.position = position
        self.onGoal = onGoal
        self.images = {
            Direction.Up: tk.PhotoImage(file="playerUp.png"),
            Direction.Down: tk.PhotoImage(file="playerDown.png"),
            Direction.Left: tk.PhotoImage(file="playerLeft.png"),
            Direction.Right: tk.PhotoImage(file="playerRight.png")
        } #Un dictionnaire qui stocke les images associées aux différentes directions
        self.current_image = self.images[Direction.Down]
        self.width = self.current_image.width()
        self.height = self.current_image.height()
        self.canvas_obj = self.canvas.create_image(
            position.asCanvasPositionIn(self).getX(),
            position.asCanvasPositionIn(self).getY(),
            image=self.current_image,
            anchor="nw",
            tags="movable"
        )

    def getHeight(self):
        return self.height
    
    def getWidth(self):
        return self.width

    def isMoveable(self):
        return True

    def moveInCanvas(self, direction):
        new_pos = self.position.positionTowards(direction, 1)
        canvas_pos = new_pos.asCanvasPositionIn(self)
        self.canvas.coords(self.canvas_obj, canvas_pos.getX(), canvas_pos.getY())
        self.position = new_pos
        
    #Vérifie si le Mover peut se déplacer dans une direction donnée en respectant les règles du jeu.
    def canMove(self, direction):
        next_pos = self.position.positionTowards(direction, 1)
        beyond_pos = self.position.positionTowards(direction, 2)

        if not next_pos.isValidInWharehouse(self.wharehouse):
            return False

        next_elem = self.wharehouse.at(next_pos)
        if next_elem.isFreePlace():
            return True
        elif next_elem.isMovable():
            beyond_elem = self.wharehouse.at(beyond_pos)
            return beyond_elem.isFreePlace()
        return False

    #Déplace le Mover dans une direction donnée en suivant les règles du Sokoban.
    def moveTowards(self, direction):
        next_pos = self.position.positionTowards(direction, 1)
        next_elem = self.wharehouse.at(next_pos)
        if next_elem.isMovable():
            beyond_pos = next_pos.positionTowards(direction, 1)
            next_elem.moveTowards(direction)
            self.wharehouse.atPut(beyond_pos, next_elem)

        self.wharehouse.atPut(self.position, Floor() if not self.onGoal else Goal(self.canvas, self.position))
        self.moveInCanvas(direction)
        self.onGoal = next_elem.xsbChar() == '.'
        self.wharehouse.atPut(self.position, self)

    #Met à jour l'image du Mover en fonction de la direction de mouvement.
    def setupImageForDirection(self, direction):
        self.current_image = self.images[direction]
        self.canvas.itemconfig(self.canvas_obj, image=self.current_image)

    #Tente de pousser un élément (comme une boîte) dans une direction donnée.
    def push(self, direction):
        self.setupImageForDirection(direction)
        if not self.canMove(direction): 
            self.startImpossiblePushAnimation() #vérifie si il peut pousser sinon il apelle l'animation
            return
        self.moveTowards(direction)

    def xsbChar(self):
        return '@' if self.onGoal else '+'

    def isFreePlace(self):
        return False

    def startImpossiblePushAnimation(self):
        self.animation_steps = 10
        self.current_radius = 0
        self.animation_id = self.canvas.after(100, self.impossiblePushAnimation)

    def cleanUpAnimation(self):
        self.canvas.delete("animation")

    def impossiblePushAnimation(self):
        if self.animation_steps > 0:
            x, y = self.position.asCanvasPositionIn(self).getX(), self.position.asCanvasPositionIn(self).getY()
            self.current_radius += 5
            self.canvas.create_oval(
                x - self.current_radius, y - self.current_radius,
                x + self.current_radius, y + self.current_radius,
                outline="red", width=2, tags="animation"
            )
            self.animation_steps -= 1
            self.canvas.after(100, self.impossiblePushAnimation)
        else:
            self.cleanUpAnimation()


class Level(object):
    def __init__(self, root, xsbMatrix, game):
        self.root = root
        self.game = game 
        self.wharehouse = WharehousePlan()

        nbrows = len(xsbMatrix)
        nbcolumns = max(len(row) for row in xsbMatrix)

        self.height = nbrows * 64 
        self.width = nbcolumns * 64 

        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, bg="gray")
        self.canvas.pack()
        self.wharehouse.initializeMatrix(nbrows, nbcolumns)
        self.initWharehouseFromXsb(xsbMatrix)
        self.root.bind("<Key>", self.keypressed)

    #Initialise le plan  à partir  xsbMatrix
    def initWharehouseFromXsb(self, xsbMatrix):
        for y, line in enumerate(xsbMatrix):
            for x, char in enumerate(line):
                position = Position(x, y)
                if char == '#':  
                    wall = Wall(self.canvas, position)
                    self.wharehouse.atPut(position, wall)
                elif char == '$':  
                    box = Box(self.canvas, self.wharehouse, position, onGoal=False)
                    self.wharehouse.atPut(position, box)
                elif char == '.':  
                    goal = Goal(self.canvas, position)
                    self.wharehouse.atPut(position, goal)
                elif char == '*':  
                    goal = Goal(self.canvas, position)
                    box = Box(self.canvas, self.wharehouse, position, onGoal=True)
                    self.wharehouse.atPut(position, goal)
                    self.wharehouse.atPut(position, box)
                elif char == '@':  
                    floor = Floor()
                    mover = Mover(self.canvas, self.wharehouse, position, onGoal=False)
                    self.wharehouse.atPut(position, floor)
                    self.wharehouse.atPut(position, mover)
                    self.mover = mover
                elif char == '+':  
                    goal = Goal(self.canvas, position)
                    mover = Mover(self.canvas, self.wharehouse, position, onGoal=True)
                    self.wharehouse.atPut(position, goal)
                    self.wharehouse.atPut(position, mover)
                    self.mover = mover
                elif char in ('-', ' '):  
                    floor = Floor()
                    self.wharehouse.atPut(position, floor)
        self.canvas.tag_raise("movable", "static")

    #Gère les entrées clavier pour déplacer le joueur.
    def keypressed(self, event):
        direction_map = {
            "Up": Direction.Up,
            "Down": Direction.Down,
            "Left": Direction.Left,
            "Right": Direction.Right
        }
    
        key = event.keysym

        # Si la touche pressée est une direction valide, effectue le déplacement
        if key in direction_map:
            direction = direction_map[key]
            self.mover.push(direction)
            if self.checkLevelCompletion():
                tkMessageBox.showinfo("Sokoban", "Niveau terminé !")

    ## Si tous les objectifs sont couverts, le niveau est terminé
    def checkLevelCompletion(self):
        for row in self.wharehouse.rawMatrix:
            for elem in row:
                #La fonction isinstance() est une fonction intégrée (built-in) qui vérifie si un objet appartient à une classe ou à un type.
                if isinstance(elem, Goal) and not elem.isCovered():
                    return False
        self.root.after(1000, self.game.next_level)
        return True
    
    
class ScoreManager:
    def __init__(self, filename="scores.txt"):
        self.filename = filename
        self.scores = self.load_scores()

    def load_scores(self):
        with open(self.filename, "r") as file:
            # Lecture de chaque ligne, suppression des espaces inutiles et séparation par la virgule.
            return [line.strip().split(",") for line in file.readlines()]


    def save_scores(self):
        with open(self.filename, "w") as file:
            for player, score in self.scores:
                # Écriture de chaque score sous la forme "nom,score" dans le fichier.
                file.write(player + "," + str(score) + "\n")

    def update_score(self, player, score):
        for i, (name, old_score) in enumerate(self.scores):
            # Si le joueur existe on remplace son ancien score par le maximum entre l'ancien et le nouveau score.
            if name == player:
                if int(old_score) < score:
                    self.scores[i] = (player, score)
        else:
            # Si le joueur n'existe pas dans la liste, on l'ajoute avec son score.
            self.scores.append((player, score))

        self.save_scores()


class Sokoban:
    def __init__(self):
        # Initialisation de la fenêtre principale du jeu.
        self.root = tk.Tk()
        self.root.title("Sokoban")  
        
        self.current_level = 0 
        self.player_name = ""  
        self.score_manager = ScoreManager()  # Instance de la gestion des scores.
        
        # Affichage du panneau de sélection du joueur au démarrage.
        self.show_score_panel()
        self.score_label = tk.Label(self.root, text="Score : " + str(0))  # Label pour afficher le score.
        self.score_label.pack(pady=5) 
        self.current_score = 0 
        

        self.restart_button.pack(pady=10)  
        self.quit_button.pack(pady=10)  

    def show_score_panel(self):
        # Crée une fenêtre secondaire pour entrer le nom du joueur et afficher les scores.
        self.score_window = tk.Toplevel(self.root)
        self.score_window.title("Sélection du joueur") 

        tk.Label(self.score_window, text="Entrez votre nom :").pack(pady=5)  
        self.player_name_entry = tk.Entry(self.score_window)  
        self.player_name_entry.pack(pady=5) 

        tk.Button(self.score_window, text="Commencer", command=self.start_game).pack(pady=10) 
        
        self.restart_button = tk.Button(self.root, text="Recommencer", command=self.restart_level)
        self.quit_button = tk.Button(self.root, text="Quitter", command=self.quit)
        
        # Affichage des scores sauvegardés.
        tk.Label(self.score_window, text="Scores sauvegardés :").pack(pady=5)
        for player, score in self.score_manager.scores:
            tk.Label(self.score_window, text=player + ": " + str(score)).pack() 

    def start_game(self):
        self.player_name = self.player_name_entry.get().strip()  # Récupère le nom du joueur et enlève les espaces superflus.
        if not self.player_name:
            tkMessageBox.showerror("Erreur", "Vous devez entrer un nom !")  
            return

        self.score_window.destroy()  
        self.load_level(self.current_level)  # Charge le niveau actuel du jeu.

    def load_level(self, level_index):
        #hasattr renvoie vrai ou faux (True ou False) après avoir vérifié si l’objet possède un attribut nommé ou pas
        if hasattr(self, 'level'):
            # Si 'self' possède l'attribut 'level', on détruit le canvas du niveau précédent
            self.level.canvas.destroy() 

        xsbMatrix = SokobanXSBLevels[level_index]  # Récupère la matrice XSB pour ce niveau.
        self.level = Level(self.root, xsbMatrix, self)  # Crée un nouvel objet Level avec la matrice XSB.

    def restart_level(self):
        # Redémarre le niveau actuel en réinitialisant le score et en rechargeant le niveau.
        self.current_score -= 1 
        self.score_label.config(text="Score : " + str(self.current_score))  # Met à jour le label du score.
        self.load_level(self.current_level)  # Recharge le niveau actuel.

    def next_level(self):
        # Passe au niveau suivant en augmentant le score et en rechargeant le niveau.
        self.current_score += 10 
        self.score_label.config(text="Score : " + str(self.current_score)) 
        self.current_level += 1  

        if self.current_level < len(SokobanXSBLevels):
            self.load_level(self.current_level)  # Charge le niveau suivant.
        else:
            # Si tous les niveaux sont terminés, affiche un message de félicitations.
            messagebox.showinfo("Sokoban", "Félicitations, vous avez terminé tous les niveaux ! Score final : " + str(self.current_score))
            self.save_score_and_exit() 

    def quit(self):
        self.save_score_and_exit()

    def save_score_and_exit(self):
        # Sauvegarde le score du joueur dans le fichier et ferme la fenêtre principale.
        self.score_manager.update_score(self.player_name, self.current_score)  
        self.root.destroy()  

    def play(self):
        self.root.mainloop()


Sokoban().play()