
Compilation/exécution :
>> sudo apt-get install python3-tk
>> pip install z3-solver
>> python main_gp.python

--------------------------
Les tests de jeu est dans le dossier "tests/...", 
(n1, n2 ... correspond aux différents niveaux de difficulté)
  test_4x4_n1.tkz
  test_4x4_non_reg2.tkz
  test_6x6_n1.tkz
  test_6x6_n2.tkz
  test_6x6_n3.tkz
  test_8x8_n1.tkz
  test_8x8_n2.tkz
  test_8x8_n2_2.tkz
  test_8x8_n3.tkz

Ou tu peux trouver plus de puzzles sur le site: https://www.20minutes.fr/services/jeux/takuzu

--------------------------
#------ Update 07/05
1. Ajouter le fichier "config", avec la paramètre "small_mode:1/0" pour les screen low-display
2. Générer .exe avec la nouvelle version Pyinstaller, non plus de warning of virus

#------ Update 02/05
1. Réaliser une interface graphique avec Tkinter

#------ Update 25/04
1. Transformer le règle 3 en code

#------ Update 15/04
1. Transformer le règle 1 et 2 en code
2. Réaliser une interface de la ligne des commandes
