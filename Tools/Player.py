
from Tools.CARDs import *

import random


class Player():

    def __init__(self, Pseudo):
        """
        Constructeur de Player
        @attribut Pseudo : nom du joueur
        @attribut Status : le statut du joueur (IA/Joueur)
        @attribut Player_Card : les cartes du joueur
        @attribut Blocked_Nb : nombre de fois que le joueur est bloqué
        @attribut Player_Role : savoir si le joueur (Saboteur ou Mineur)
        @attribut id_card : L'index d'une carte
        @attribut Current_Player : Le joueur en cours de jeu
        """

        self.__Pseudo = Pseudo
        self.Player_Cards = []
        self.Player_Role = ''
        self.Gold = 0
        self.reward_gold = []
        self.tools = {'Pick' : True, 'Light' : True , 'Wheels' : True} 
        self.status = 0

#______________________________________________________________________________
    @property
    def Pseudo(self):
        return self.__Pseudo
    
    
    
    def player_hand(self,Cartes):
        self.Player_Cards = Cartes[:5]
        i = 0
        while i<5 :
            Cartes.pop(0)
            i += 1
    
    
    
    def get_player_role(self) :
        return self.Player_Role



    def Delete_Card(self, id_card):
        del self.Player_Cards[id_card]
        return self.Player_Cards




    def print_cards(self):
        c = self.Player_Cards[0].__str__()
        l1 = "   " + c[:5] + " "
        l2 = str(1) + ": " + c[6:11] + ", "      
        l3 = "   " + c[12:] + " "
        
        for i in range(1,len(self.Player_Cards),1):
            c = self.Player_Cards[i].__str__()
            l1 = l1 + "    " + c[:5] + " "
            l2 = l2 + str(i+1) + ": " + c[6:11] + ", "      
            l3 = l3 + "    " + c[12:] + " "
        l2 = l2 + str(len(self.Player_Cards)+1) + ") Throw away a card"
           
        print(l1)
        print(l2)
        print(l3)



    def Choose_Card(self):
        
        self.print_cards()
        
        id_card = str(input(f"What card you like to play (1 to {len(self.Player_Cards)}) ? ")) # Demande apres pour le control de saisie
        while len(id_card) != 1 or ord(id_card) > ord(str( len(self.Player_Cards) + 1 )) or ord(id_card) < ord(str(1)) :
            print("Error : Choose a valid card !")
            id_card = str(input(f"What card you like to play (1 to {len(self.Player_Cards)}) ? "))
        
        return int(id_card)
    
    
    
    def Block_Player(self, otherPlayer , actionCard):    # bloquer un autre joueur
        
        if( actionCard.symbol == "broke_P"   ) :  # broke pick
            if otherPlayer.tools['Pick'] == True :
                otherPlayer.tools['Pick'] = False
                return True
            else:
                return False
            
        if( actionCard.symbol == "broke_Li"   ) :  # broke light
            if otherPlayer.tools['Light'] ==True :
                otherPlayer.tools['Light'] = False
                return True
            else:
                return False
          
        if( actionCard.symbol == "broke_W"   ) :  # broke wheels
              if otherPlayer.tools['Wheels'] == True :
                  otherPlayer.tools['Wheels'] = False
                  return True
              else:
                  return False



    def Is_Blocked(self):
        
        for tool in self.tools :
            if self.tools[tool] == False: # if one of the tools is brocken return True
                return True
        return False
        
        
        
    def Unblock_Player(self, otherPlayer, defenseCard : Card): 

        if otherPlayer.Is_Blocked() :
            if defenseCard.symbol == "Li" or defenseCard.symbol == "LIP" or defenseCard.symbol == "LIW":
                    if otherPlayer.tools['Light'] == False:
                        otherPlayer.tools['Light'] = True
                        return True
                    
            if defenseCard.symbol == "P" or defenseCard.symbol == "PW" or defenseCard.symbol == "LIP":
                    if otherPlayer.tools['Pick'] == False:
                        otherPlayer.tools['Pick'] = True
                        return True   
                    
            if defenseCard.symbol == "W" or defenseCard.symbol == "PW" or defenseCard.symbol == "LIW":
                    if otherPlayer.tools['Wheels'] == False:
                        otherPlayer.tools['Wheels'] = True
                        return True 
            return False    
        else :
            return False

    def Player_Apt_To_play(self,card):
        for tool in self.tools :
            if self.tools[tool] == False :  # if one of the tools is brocken
                if card.name == 'path':
                    print('you can not currently play a path card')
                    return False
                elif card.name == 'MAP' or card.name == 'action':
                    return True
        return True
    
    

