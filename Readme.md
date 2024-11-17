
Voici une version améliorée et plus structurée du README que vous avez fourni :

Projet de Sethika Samaranayake, William Pecoraro et Ilian Ghouti-Terki

                                      Description:
Ce jeu est un jeu de bataille navale où les joueurs peuvent choisir de jouer en mode PvP (joueur contre joueur) ou PvAI (joueur contre IA). Le jeu est structuré autour de différentes classes qui gèrent les aspects du jeu, de l'interface utilisateur à la gestion du terrain et des bateaux.

Dépendances
Le jeu utilise la bibliothèque Pygame pour la gestion de l'affichage, des événements, et des interactions. Vous pouvez installer Pygame en utilisant la commande suivante :


    pip install pygame

Structure du projet:
Le jeu est organisé autour de plusieurs classes qui encapsulent différentes fonctionnalités :

1. Game Class
La classe principale du jeu qui gère le déroulement de la partie. Elle contient la logique de jeu, notamment les fonctions de placement des bateaux et la gestion des tours. C'est la classe centrale qui gere le gameplay, avec des méthodes comme run() et run_ai() pour jouer contre un autre joueur ou contre l'IA.

2. UserInterface Class
La classe qui gère l'interface utilisateur, y compris l'affichage des boutons et des éléments de texte comme le score. Elle met à jour l'interface en fonction des actions du joueur.

3. Text Class
Cette classe est utilisée pour afficher et gérer le texte dans l'interface utilisateur, notamment pour les scores et les messages d'état.

4. Button Class
La classe de base pour tous les boutons du jeu. Elle comprend deux types de boutons spécifiques :

    __ShipButton__ : Utilisé pour sélectionner et placer des bateaux.

    __MenuButton__ : Utilisé pour naviguer dans les menus du jeu (par exemple, démarrer une nouvelle partie, revenir au menu principal, etc.).
5. Player Class
Cette classe représente un joueur et contient des informations essentielles comme le nom du joueur et son score. Elle aide la classe Game à savoir quand un joueur a placé tous ses bateaux ou a détruit tous ceux de l'adversaire.

6. StartMenu et ReplayMenu Classes
Ces classes gèrent l'interface de démarrage du jeu et l'interface de redémarrage après la fin d'une partie. Elles offrent des boutons qui permettent au joueur de démarrer une nouvelle partie en mode PvP ou PvAI, et utilisent les fonctions appropriées de la classe Game.

7. Terrain Class
La classe Terrain contient toutes les cellules du terrain de jeu et gère l'affichage et le placement des bateaux. Elle s'assure que le placement des bateaux respecte les règles du jeu. Elle utilise les fonctions place_ship() et place_ship_ai() pour placer des bateaux, et vérifie si le placement est valide.

8. Cell Class
La classe Cell représente une cellule du terrain de jeu. Elle stocke l'état de la cellule (si elle est cachée ou révélée, si elle contient un bateau ou non) ainsi que sa position dans la grille.

9. Button and Text Classes
Ces classes sont utilisées pour gérer les éléments de l'interface utilisateur comme les boutons interactifs et l'affichage du texte dans le jeu. Elles sont utilisées dans des éléments comme UserInterface, StartMenu, et ReplayMenu pour créer une interface fluide et interactive.

10. Renderable and UIElement Classes
Il s'agit d'interfaces qui définissent des méthodes comme render(), hide(), et reset(). Elles permettent à certaines classes (par exemple, Button, Text, Menu) d'implémenter ces méthodes pour gérer leur affichage et leur comportement dans l'interface utilisateur.

__Fonctionnalités principales__

                                Choix du mode de jeu : 

Le joueur peut choisir entre un mode PvP ou PvAI dès le début du jeu.


                                Placement des bateaux : 

Le placement des bateaux obéit à des règles spécifiques, et les joueurs doivent positionner correctement leurs navires sur la grille.
                                    
                                    Interactivité :
L'utilisateur peut interagir avec le jeu via des boutons et voir les scores mis à jour en temps réel.

                                        Mode IA : 
En mode PvAI, un joueur affronte une IA qui effectue des mouvements automatiquement selon un algorithme de base.

                                    
                                    Menus interactifs : 
Le jeu offre des menus pour démarrer une nouvelle partie ou redémarrer après une victoire ou une défaite.