
from Tools.CARDs import *
from Game_manager.Game_Manager import *

import random

#_______________________ GAME CARDS _______________________________
if __name__ == "__main__" :
    cartes_jeu = []

    list = PathCards()

    for i in range(len(list.cards)):
        c = list.cards[i]
        cartes_jeu.append(c)



    list = BlockActionCards()

    for i in range(len(list.cards)) :
        c = list.cards[i]
        cartes_jeu.append(c)
        

    list = UnblockActionCards()

    for i in range(len(list.cards)):
        c = list.cards[i]
        cartes_jeu.append(c)
        
    
    list = MAPActionCards()

    for i in range(len(list.cards)):
        c = list.cards[i]
        cartes_jeu.append(c)


    list = ROFActionCards()

    for i in range(len(list.cards)):
        c = list.cards[i]
        cartes_jeu.append(c)
        

    random.shuffle(cartes_jeu)

    #___________________________________________________________________

    print("+--------------------------------------------------------------------+")
    print("| Welcome to SabOOtters, where dwarf otters look for gold in a mine! |")
    print("+--------------------------------------------------------------------+\n")

    #_______________________ GAME LAUNCH _______________________________

    Game = GameManager(cartes_jeu)

    Game.state_Game()
    c