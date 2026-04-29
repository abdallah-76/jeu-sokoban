# 🎮 Jeu Sokoban — Python / Tkinter

Un jeu de réflexion classique **Sokoban** développé en Python avec une interface graphique Tkinter, des sprites pixel-art, des animations et un système de scores persistant.

---

## 📸 Aperçu

### Écran de sélection du joueur
![Sélection joueur](screenshots/screen4.png)

### Niveau 1 — Départ
![Niveau 1](screenshots/screen1.png)

### Niveau 2 — En cours de résolution
![Niveau 2](screenshots/screen2.png)

### Niveau résolu ✔
![Niveau résolu](screenshots/screen3.png)

---

## 🚀 Fonctionnalités

- 🎯 **Plusieurs niveaux** chargés depuis un fichier XSB standard
- 🧱 **Sprites pixel-art** : murs, caisses, joueur (4 directions), objectifs
- 🎨 **Animations** : feedback visuel sur les coups impossibles (cercle rouge) et sur les caisses placées correctement (cercle vert)
- 👤 **Sélection de joueur** au démarrage avec saisie du nom
- 🏆 **Système de scores persistant** : sauvegarde en fichier texte, classement affiché
- 🔁 **Recommencer** le niveau en cours (pénalité de -1 point)
- ✅ **Passage automatique** au niveau suivant (+10 points) avec détection de complétion
- 🔄 **Architecture orientée objet** : classes `Floor`, `Wall`, `Box`, `Goal`, `Mover`, `Level`, `Sokoban`

---

## 🕹️ Contrôles

| Touche | Action |
|--------|--------|
| ↑ ↓ ← → | Déplacer le joueur |
| R | Recommencer le niveau |
| Q | Quitter |

---

## 🛠️ Technologies utilisées

| Technologie | Usage |
|-------------|-------|
| Python 3 | Langage principal |
| Tkinter | Interface graphique (canvas, fenêtres, événements clavier) |
| PIL/Pillow | Gestion des sprites PNG |
| Enum | Direction (Up/Down/Left/Right) |
| Fichiers texte | Persistance des scores et des niveaux |

---

## 🏗️ Architecture du projet

```
Jeu-Sokoban/
├── Sokoban-skeleton.py      # Code source principal
├── sokobanXSBLevels.py      # Niveaux au format XSB
├── levels.txt               # Niveaux alternatifs
├── scores.txt               # Scores persistants des joueurs
├── requirements.txt         # Dépendances Python
├── screenshots/             # Captures d'écran
│   ├── screen1.png          # Niveau 1 — Départ
│   ├── screen2.png          # Niveau 2 — En cours
│   ├── screen3.png          # Niveau résolu
│   └── screen4.png          # Écran de sélection
├── wall.png                 # Sprite mur
├── box.png                  # Sprite caisse
├── boxOnTarget.png          # Sprite caisse sur objectif
├── goal.png                 # Sprite objectif
├── playerUp.png             # Sprite joueur (haut)
├── playerDown.png           # Sprite joueur (bas)
├── playerLeft.png           # Sprite joueur (gauche)
└── playerRight.png          # Sprite joueur (droite)
```

---

## 🎯 Règles du jeu

- Le joueur se déplace dans **4 directions**
- Il peut **pousser une caisse** (jamais la tirer)
- Impossible de traverser les **murs** ou d'empiler les **caisses**
- Le niveau est **réussi** quand toutes les caisses sont sur les objectifs (⬇)
- Feedback visuel immédiat : **rouge** = coup impossible, **vert** = caisse placée

---

## 🧠 Concepts POO utilisés

- **Encapsulation** : chaque élément (Wall, Box, Goal...) gère sa propre logique et son rendu
- **Polymorphisme** : méthodes `isMovable()`, `canBeCovered()`, `isFreePlace()`, `xsbChar()` communes à tous les éléments
- **Séparation des responsabilités** : `WharehousePlan` gère la grille, `Level` gère le rendu, `Sokoban` gère le jeu, `ScoreManager` gère les scores
- **Gestion d'événements** : binding clavier Tkinter avec `<Key>`

