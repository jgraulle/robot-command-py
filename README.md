


# Etape 0. Mise en place du simulateur 

- ouvrir un terminal (ctrl-alt-t)
- lancer le simu (robotSimulator)

## Description 

- carré vert: robot
- ligne rouge: télémètre infrarouge
- cone bleu: télémètre ultrason
- pixel blanc: mur
- pixel jaune: couleur du sol

## Touche de contrôle du simulateur

- espace: réinitialiser la position du robot
- flèches: déplacer le robot


# Etape 1. Lancement de l'environnement de développement 

- lancer MS Code (depuis le bandeau de gauche)
- clicker sur l'icône MS Code (serpentin bleu)
- Menu: File, Option: Open Folder, sélectionner "Home", puis "Workspace", puis "robot-command-py", valider
- Ouvir le fichier "main.py"
- Lancer le programme : Clicker sur le triangle blanc en haut à droite


# Etape 2. 1er programme : tourner

- dans le fichier "main.py"
- remplacer "TODO step2" par le pseudo-code suivant (en vous inspirant de la fonction "step1_move3s") 
    - faire touner le robot sur lui-même
    - attendre 3 secondes 
    - arrêter le robot 
- à la fin du fichier (dans le "main") : 
    - commenter la ligne "step1_move3s(robot)" (rajouter # devant la ligne)
    - décommenter la ligne "step2_turn3s(robot)" (enlever # devant la ligne)
- Lancer le programme : Clicker sur le triangle blanc en haut à droite

Remarque : essayer de faire varier le centre de rotation du robot.

# Etape 3. 1er évênement : se déplacer jusqu'au mur

- remplacer "TODO step3" par le pseudo-code suivant
    - faire avancer le robot tout droit
    - attendre d'être en collision avec le mur en utilisant "robot.waitChanged(robot.EventType.SWITCH)"

Remarque : vérifier que lorsqu'on lance le programme, la console affiche bien  
    - "Lancement du programme"
    - "Fin du programme" 
Si ce n'est pas le cas, le programme est bloqué, faire un ctrl-c dans la console pour le débloquer


# Etape 4. 1ère boucle : figure géométrique

- remplacer "TODO step4" par le code suivant
```
    while True:
        robot.setMotorsSpeed(0.2, 0.2)
        time.sleep(2.0)
        robot.setMotorsSpeed(-0.1, 0.1)
        time.sleep(0.5)
```

# Etape 5. 1er algorithme : explorer la pièce

- remplacer "TODO step5" par le pseudo-code suivant
    - boucle infinie
        - avancer le robot tout droit
        - attendre d'être en collision avec le mur
        - reculer un peu
        - tourner un peu

# Etape 6. algorithme avancé : suivi de ligne

- remplacer "TODO step6" par un algorithme qui permet de faire un suivi du bord de la forme jaune
- vous aurez besoins de :
    - attendre l'évênement de changement de couleur du sol : "robot.waitChanged(robot.EventType.LINE_TRACK_IS_DETECTED)"
    - lire la couleur du sol : "robot.getLineTracksIsDetected(0)" qui renvoit "True" ou "False" selon si la couleur est jaune ou noire
    - exécuter une action en fonction d'un condition 
    ```
        if condition:
            action_true()
        else:
            action_false()
    ```