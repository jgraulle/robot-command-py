


# Etape 0. Mise en place du simulateur 

- Ouvrir un terminal (ctrl-alt-t)
- Lancer le simu (taper "robotSimulator" puis la touche entrée)

## Description

- Carré vert: robot
- Ligne rouge: télémètre infrarouge
- Cone bleu: télémètre ultrason
- Pixel blanc: mur
- Pixel jaune: couleur du sol

## Touche de contrôle du simulateur

- Espace: réinitialiser la position du robot
- Flèches: déplacer le robot


# Etape 1. Lancement de l'environnement de développement 

## Description

Dans le code que nous allons utiliser il y a une variable "robot" sur lequel on va utiliser la
fonction "robot.setMotorsSpeed(rightValue, leftValue)" qui permet de modifier la vitesse des
moteurs des roues du robot. Il y a 2 paramètres car le robot à 2 roues. Pour chacune des roues on
peut avoir une valeur entre -1 et 1 dont :

- 1.0 en avant à vitesse maximale
- 0.0 arrêter le moteur
- -1.0 en arrière à vitesse maximale

## Lancement

- Lancer MS Code (cliquer sur l'icone serpentin bleu dans le bandeau de gauche)
- Cliquer sur le menu "File" puis l'option "Open Folder", sélectionner "Home", puis "Workspace", puis "robot-command-py", puis cliquer sur "Open"
- Ouvrir le fichier "main.py" (double clic sur le fichier "main.py" à gauche)
- Chercher la ligne contenant "def step1_move3s(robot: Robot):"
    - "robot.setMotorsSpeed(0.2, 0.2)" : veut donc dire avancer tout droit
    - "time.sleep(3.0)" : attendre 3 secondes
    - "robot.setMotorsSpeed(0.0, 0.0)" : veut donc dire stopper les 2 roues du robot
- Lancer le programme : Cliquer sur le triangle blanc en haut à droite (en regardant le robot sur le simu)


# Etape 2. 1er programme : tourner

- Dans le fichier "main.py"
- Remplacer "TODO step2" par le pseudo-code suivant (en vous inspirant de la fonction "step1_move3s")
    - faire touner le robot sur lui-même
    - attendre 3 secondes 
    - arrêter le robot 
- A la fin du fichier (dans le "main") :
    - commenter la ligne "step1_move3s(robot)" (rajouter # devant la ligne)
    - décommenter la ligne "step2_turn3s(robot)" (enlever # devant la ligne)
- Lancer le programme : Cliquer sur le triangle blanc en haut à droite

Remarque 1 : vérifier que lorsqu'on lance le programme, la console affiche bien

- Lancement du programme
- Fin du programme
- ~/workspace/robot-command-py$

Si ce n'est pas le cas, le programme est bloqué, faire un ctrl-c dans la console pour le débloquer

Remarque 2 : essayer de faire varier le centre de rotation du robot.


# Etape 3. 1er évênement : se déplacer jusqu'au mur

- Remplacer "TODO step3" par le pseudo-code suivant
    - faire avancer le robot tout droit
    - attendre d'être en collision avec le mur en utilisant "robot.waitChanged(robot.EventType.SWITCH)"
    - arrêter les roues du robot

Remarque : penser à commenter et décommenter les fonctions à la fin du programme comme dans l'étape 2


# Etape 4. 1ère boucle : figure géométrique

- Remplacer "TODO step4" par le code suivant
```
    while True:
        robot.setMotorsSpeed(0.2, 0.2)
        time.sleep(2.0)
        robot.setMotorsSpeed(-0.1, 0.1)
        time.sleep(0.5)
```


# Etape 5. 1er algorithme : explorer la pièce

- Remplacer "TODO step5" par le pseudo-code suivant
    - boucle infinie
        - avancer le robot tout droit
        - attendre d'être en collision avec le mur
        - reculer un peu
        - tourner un peu


# Etape 6. algorithme avancé : suivi de ligne

- Remplacer "TODO step6" par un algorithme qui permet de faire un suivi du bord de la forme jaune
- Vous aurez besoin de :
    - attendre l'évênement de changement de couleur du sol : "robot.waitChanged(robot.EventType.LINE_TRACK_IS_DETECTED)"
    - lire la couleur du sol : "robot.getLineTracksIsDetected(0)" qui renvoit "True" ou "False" selon si la couleur est jaune ou noire
    - exécuter une action en fonction d'une condition
    ```
        if <condition>:
            <action vrai>
        else:
            <action faux>
    ```
