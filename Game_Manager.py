
from GRID import *
from CARDs import *
from Player import *
from PlayerBot import *

import sys
import time
import random


class GameManager() :
    
    def __init__(self, Cards) :
        self.begin_state = ''   # Au départ on a rien avant de lancer le jeu
        self.state = 'start_game' # Pour commencer le jeu 
        self.players_list = []
        self.winners = []
        self.round_scores = {}
        self.saboteur_win = False
        self.digger_win = False
        self.winners = []
        self.score = {}
        self.round = 0
        self.tour_actuel = 0
        self.__Cards = Cards
        self.reward_cards = []
        
        @property
        def Cards(self):
            return self.__Cards

    

    def add_player(self):
        
        test = 1
        val1 = True
        nb_players = 0
        
        """
        Boucle while pour creer les players : - Verifier que le nombre de players est entre 3 et 10 
                                              - Entrer les noms des players 
                                              - Entrer les statuts des players
                                              - Distribuer les roles des players
                
        """
        
        while val1:
            
            nb_players = str(input('How many players ? '))
            
            if nb_players != '3' and nb_players != '4' and nb_players != '5' and nb_players != '6' and nb_players != '7' and nb_players != '8' and nb_players != '9' and nb_players != '10' and test <= 3 :
                print("You can only play if you are at least 3 players ! \nPlease try again :\n ")
                test += 1
            
            if  nb_players == '3' or nb_players == '4' or nb_players == '5' or nb_players == '6' or nb_players == '7' or nb_players == '8' or nb_players == '9' or nb_players == '10' and test <= 3 :
                val1 = False
                val2 = True
                
            if test > 3 :
                val1 = False
                val2 = False 
            
        if val2 :
    
            roles = RoleCards(int(nb_players))
            random.shuffle(roles.Cards)
            cpt_stat = 0
            
            
            for i in range( int(nb_players) ) :
                    
                pseudo_player = str(input(f"Please enter the name of player {i+1}: "))
                while pseudo_player == '' :
                    print("Please try again :")
                    pseudo_player = str(input(f"Please enter the name of player {i+1}: "))
                
                status_player = str(input(f"Please enter the status of player {i+1}: \n \t - For Human enter 0 - for IA enter 1 : "))
                while status_player != '0' and  status_player != '1'  :
                    print("Please try again :")
                    status_player = str(input(f"\t - For Human enter 0 - For IA enter 1 : "))
                
                if int(status_player) == 0 :
                    player = Player( pseudo_player )
                    cpt_stat += 1
                elif int(status_player) == 1 :
                    player = PlayerBot( pseudo_player )
                    
                player.Player_Role = roles.Cards[i]
                
                self.players_list.append(player)
                
            if cpt_stat > 0:
                return self.players_list
            
            else:
                self.players_list = []
                print("There must be at least one player with status 0!")
                print("+----------------------------------------------------------------+")
                print("|                    END GAME, SEE YOU SOON !                    |")
                print("+-----------------------------------------------------------------+\n")
                
                sys.exit()
        else : # END GAME 
            
            print("You have exhausted the maximum number of tries :( ")
            print("+----------------------------------------------------------------+")
            print("|                    END GAME, SEE YOU SOON !                    |")
            print("+-----------------------------------------------------------------+\n")
            
            sys.exit()
            
        
    
    
    def print_players(self) :
        print("liste des joueurs : \n")
        for i in range(len(self.players_list)):
            
            status = 'Human' if ( self.players_list[i].status == 0 ) else  'AI'
            
            print(i+1,"/- ",self.players_list[i].Pseudo," is ", status )
    
    
    
    def state_Game(self):

        if self.begin_state != self.state:
            self.begin_state = self.state

            if self.state == 'start_game':
                self.start_game()
            elif self.state == 'start_round':
                self.play_round()              
            elif self.state == 'round_over':
                self.round_over()
            elif self.state == 'game_over':
                self.game_over()       
    
    
                        
    def start_game(self):
        
        self.round = 0
        self.round_scores = {}

        print("+--------------------------------------------------------------------+")
        print("|                            Game started !                          |")
        print("+--------------------------------------------------------------------+\n")
        
        
        self.state = 'start_round'
        self.state_Game()
    

        
    def play_card(self,grille,cartes_jeu):
        
        flag = "OFF" 
        #Choisir une carte a jouer
        if(len(self.players_list[self.tour_actuel].Player_Cards) == 0):
            res = "KO"
            return res,flag
            
        else:
            
            
            if self.players_list[self.tour_actuel].status == 0 :
            
                card = self.players_list[self.tour_actuel].Choose_Card()
              
                # si on a choisi de ne pas jeter une carte et qu'on est pas apte a jouer la carte demande
                while((card != len(self.players_list[self.tour_actuel].Player_Cards)+1) and self.players_list[self.tour_actuel].Player_Apt_To_play(self.players_list[self.tour_actuel].Player_Cards[card-1]) == False) :
                    card = self.players_list[self.tour_actuel].Choose_Card()
                
                #si on decide de jeter une carte ou qu'on est apte a jouer
                if (card == (len(self.players_list[self.tour_actuel].Player_Cards) +1)) or self.players_list[self.tour_actuel].Player_Apt_To_play(self.players_list[self.tour_actuel].Player_Cards[card-1]) == True :
                    
                    #Si on choisit de jeter la carte
                    if card == (len(self.players_list[self.tour_actuel].Player_Cards) +1):
                        print("what card would you throw? ")
                        c = str(input())
                        while len(c) != 1 or ( ord(c) < ord(str(1)) or ord(c) > ord(str(len(self.players_list[self.tour_actuel].Player_Cards)))):
                            c = str(input("Error : Please enter a valid number : "))
                        self.players_list[self.tour_actuel].Player_Cards.pop(int(c)-1)
                        
                        #Si il reste des cartes a tirer
                        if(len(cartes_jeu)>0):
                            self.players_list[self.tour_actuel].Player_Cards.append(cartes_jeu[0])
                            cartes_jeu.pop(0)
                        result = True
                        
                    #si on decide de jouer une carte  
                    else :
                        
                        #Si on decide de jouer une carte chemin
                        if self.players_list[self.tour_actuel].Player_Cards[card-1].name == 'path' :
                            result, flag = grille.place_card(self.players_list[self.tour_actuel].Player_Cards[card-1] , self.players_list[self.tour_actuel].status, 0, 0) 
                            if(result == False):
                                print("Error: the chosen position is wrong ! \n")
                            
                        
                        # Si on decide de jouer une carte action
                        elif self.players_list[self.tour_actuel].Player_Cards[card-1].name == 'action' :
                            
                            Test = True
                            count = 0
                            while Test :
                                
                                if count == 0 : i = input("Please enter the number of the player you want to apply the action : ")
                                else : i = input("Please try again : ")
                                
                                for nb in range( 1, len(self.players_list) + 1 , 1) :
                                    if i != str(nb) : continue
                                    else : 
                                        Test = False
                                        break 
                            
                                count = 1
                                
                            i = int(i) - 1
                            
                            #Blockage
                            if self.players_list[self.tour_actuel].Player_Cards[card-1].symbol == "broke_Li" or self.players_list[self.tour_actuel].Player_Cards[card-1].symbol == "broke_P" or self.players_list[self.tour_actuel].Player_Cards[card-1].symbol == "broke_W" :
                                if (i == self.tour_actuel):
                                    print("Error : You can not block yourself !")
                                    result = False 
                                 
                                else : 
                                    result = self.players_list[self.tour_actuel].Block_Player(self.players_list[i],self.players_list[self.tour_actuel].Player_Cards[card-1])
                                    if(result == False):
                                        print("Error: the tool is already broken ! \n")
        
                              
                            #Debloquage
                            elif self.players_list[self.tour_actuel].Player_Cards[card-1].symbol == "Li" or self.players_list[self.tour_actuel].Player_Cards[card-1].symbol == "P" or self.players_list[self.tour_actuel].Player_Cards[card-1].symbol == "W" or self.players_list[self.tour_actuel].Player_Cards[card-1].symbol == "LIP" or self.players_list[self.tour_actuel].Player_Cards[card-1].symbol == "PW" or self.players_list[self.tour_actuel].Player_Cards[card-1].symbol == "LIW":
                                print(i,self.tour_actuel)
                                result = self.players_list[self.tour_actuel].Unblock_Player(self.players_list[i],self.players_list[self.tour_actuel].Player_Cards[card-1])
                                print(result)
                                if(result == False):
                                    print("Error: the tool was not broken ! \n")
        
                        
                        #Si on decide de jouer une carte MAP
                        elif self.players_list[self.tour_actuel].Player_Cards[card-1].name == "MAP" :
                            result, flagOFF = grille.print_Goal(0, 0, "MAP")
                            if (result == False):
                                print("Error: you did not choose one of the goal cards ! \n" )
                                
                        
                        #Si on decide de jouer une carte ROF
                        elif self.players_list[self.tour_actuel].Player_Cards[card-1].name == "ROF" :
                            result = grille.delete_card(0, 0, 0 )
                            if (result == False):
                                print("Error : can not perform this action ! " )
                            
                        if(result == True):
                            self.players_list[self.tour_actuel].Player_Cards.pop(card-1)
                            if (len(cartes_jeu)>0) :
                                self.players_list[self.tour_actuel].Player_Cards.append(cartes_jeu[0])
                                cartes_jeu.pop(0)       
                            
                        
                        
                                
            elif self.players_list[self.tour_actuel].status == 1 :
                print('IA is playing ... ')
                result , flag = self.players_list[self.tour_actuel].Choose_Card( self.players_list, grille , cartes_jeu )
                time.sleep(3)
        return result , flag
    
    
    
    def getCurrentPlayer(self):
        player = self.players_list[self.tour_actuel].Pseudo
        return player
    
    
    
    def etat_player(self,current):
        res = ''
        for tool in self.players_list[current].tools :
            if self.players_list[current].tools[tool] == False:
                res += '[{} is off]'.format(tool) + '  '
        return res
    
    
    
    def isSaboteur(self):
        for i in range(len(self.players_list)):
            if self.players_list[i].Player_Role.symbol == 'saboteur':
                return True
        return False
    
    
    
    def valueGold(self,carte):
        if carte.symbol == "3G":
            value_card = 3
        
        if carte.symbol == "2G":
            value_card = 2
        
        if carte.symbol == "1G":
            value_card = 1
        
        return value_card
    
    
        
    def play_round(self):
        print("+--------------------------------------------------------------------+")
        print("|                            Round started !                         |")
        print("+--------------------------------------------------------------------+\n")
        round_ended = False
        
        if self.round == 0:
            self.add_player()
        self.print_players()
        
        Cartes = []
        for i in self.__Cards :
            Cartes.append(i)
            
        random.shuffle(Cartes)
        grille = Grid()
        grille.create_grid()
        
        for i in range(len(self.players_list)):
            self.players_list[i].Player_Cards.clear()
        
        
        for i in range(len(self.players_list)):
            self.players_list[i].player_hand(Cartes)
            
        while not round_ended: #  s'arreter a la fin du jeu
            print("\n")
            print('Player ',self.tour_actuel +1, ' : ',self.getCurrentPlayer(),'(',self.players_list[self.tour_actuel].Player_Role,')', self.etat_player(self.tour_actuel))
            print("\n")
            
            print("Current mine state : \n")
            grille.print_grid()
            
            res , flag= self.play_card(grille,Cartes)
            
            end = 0
            for i in range(len(self.players_list)):
                if(len(self.players_list[i].Player_Cards) == 0):
                    end = end + 1
            
            if res == True :
                self.tour_actuel = (self.tour_actuel + 1) % len(self.players_list)
            elif res == False :
                print("Error : cannot perform this action ! \n")
                self.tour_actuel = self.tour_actuel
            elif res == "KO"  :
                
                if(end == len(self.players_list)):
                    
                    if(self.isSaboteur() == True):
                        print("+--------------------------------------------------------------------+")
                        print("|                     End Round : Saboteur Wins !                    |")
                        print("+--------------------------------------------------------------------+\n")
                        self.saboteur_win = True
                    else :
                        print("+--------------------------------------------------------------------+")
                        print("\                     End Round : No one wins !                      |")
                        print("+--------------------------------------------------------------------+\n")
                    round_ended = True
                        
            if flag == "ON" :
                grille.print_grid()
                print("+--------------------------------------------------------------------+")
                print("|                    End Round : Digger Wins !                       |")
                print("+--------------------------------------------------------------------+\n")
                self.tour_actuel = self.tour_actuel
                self.digger_win = True
                round_ended = True
                
            
        self.state = 'round_over'
        self.state_Game()
      
        
      
    def round_over(self) :
        
        #Distribution Recompenses Saboteurs
        nombre_saboteurs = 0
        
        if(self.saboteur_win == True):
            for i in range(len(self.players_list)):
                if self.players_list[i].Player_Role.symbol == "saboteur" :
                    nombre_saboteurs += 1
            if (nombre_saboteurs == 1):
                for i in range(len(self.players_list)):
                    if self.players_list[i].Player_Role.symbol == "saboteur" :
                        self.players_list[i].reward_gold.append(Card("Reward","3G"))
                        self.players_list[i].reward_gold.append(Card("Reward","1G"))
            if(nombre_saboteurs == 2 or nombre_saboteurs == 3 ):
                for i in range(len(self.players_list)):
                    if self.players_list[i].Player_Role.symbol == "saboteur" :
                        self.players_list[i].reward_gold.append(Card("Reward","3G"))
            
            if (nombre_saboteurs == 4):
                for i in range(len(self.players_list)):
                    if self.players_list[i].Player_Role.symbol == "saboteur" :
                        self.players_list[i].reward_gold.append(Card("Reward","2G"))
        
        
        #Distribution Recompenses Digger
        if self.round == 0 :
            self.reward_cards = RewardCards()
            random.shuffle(self.reward_cards.Cards)
        
        reward_picked = []
        nombre_joueurs = len(self.players_list)
        
        if(nombre_joueurs == 10):
            for i in range(nombre_joueurs - 1):
                reward_picked.append(self.reward_cards.Cards[0])
                self.reward_cards.Cards.pop(0)
        else :
            for i in range(nombre_joueurs):
                reward_picked.append(self.reward_cards.Cards[0])
                self.reward_cards.Cards.pop(0)
        
        reward_picked = sorted(reward_picked, key=lambda RewardCards: RewardCards.symbol,reverse=True)
        nombre_rewards = len(reward_picked)
        
        if (self.digger_win == True):
            # for i in range(len(reward_picked)):
            #     print(reward_picked[i])
            while(nombre_rewards>0):
                if (self.players_list[self.tour_actuel-1].Player_Role.symbol == 'digger'):
                    self.players_list[self.tour_actuel-1].reward_gold.append(reward_picked[0])
                    reward_picked.pop(0)
                    nombre_rewards -= 1
                self.tour_actuel = (self.tour_actuel + 1) % len(self.players_list)
                  
        self.round = self.round + 1
        self.saboteur_win = False
        self.digger_win = False
        self.tour_actuel = 0
        
        if(self.round >2) :
            self.state = 'game_over'
            input("Press Enter to show results ...")
            
        else :
            self.state = 'start_round'
            input("Press Enter to start new round ...")
        
        roles = RoleCards(len(self.players_list))
        random.shuffle(roles.Cards) 
        for i in range(len(self.players_list)):
            self.players_list[i].PlayerRole = ''  
        
        for i in range(len(self.players_list)):
            self.players_list[i].Player_Role = roles.Cards[i]
        
        for i in range(len(self.players_list)):
            for tool in self.players_list[i].tools :
                self.players_list[i].tools[tool] = True
                
            
        
        
        self.state_Game()
        
        
        
    def game_over(self):
        
        
        print("+---------------------------------------------------------------+")
        print("|                          END GAME !                           |")
        print("+---------------------------------------------------------------+\n")

            
        for i in range(len(self.players_list)):
            for j in range(len(self.players_list[i].reward_gold)):
                self.players_list[i].Gold += self.valueGold(self.players_list[i].reward_gold[j])
        
        print("Scores of the Game : ")
        for i in range(len(self.players_list)):
            print("Player ",self.players_list[i].Pseudo," :  ", self.players_list[i].Gold,"G")
            
        objects = [(i, player.Gold) for i, player in enumerate(self.players_list)]
        maximum = max(objects, key=lambda x: x[1]) 
        index = maximum[0]
        
        print("Le grand vainquer de cette partie est : ....\n",self.players_list[index].Pseudo)
    
        
        print("+---------------------------------------------------------------+")
        print("|                        SEE YOU SOON :)                        |")
        print("+---------------------------------------------------------------+\n")
                
            
        


        
        
