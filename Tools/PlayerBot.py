
from Tools.Player import * 
import random


class PlayerBot(Player):
    
        
    def __init__(self,Pseudo): 
        super().__init__(Pseudo)
        self.status = 1
    
    
    
    def __eq__(self, other):
        if isinstance(other, PlayerBot):
            
            if self.status != other.status or self.Player_Role.symbol != other.Player_Role.symbol or len( self.Player_Cards ) != len( other.Player_Cards ) :
                return False
            
            elif True :
                
                for i in range( len( self.Player_Cards ) ):
                    if self.Player_Cards[i].symbol != other.Player_Cards[i].symbol or self.Player_Cards[i].name != other.Player_Cards[i].name :
                        return False
                
            elif True :
                
                if self.tools['Pick'] != other.tools['Pick'] : return False
                if self.tools['Light'] != other.tools['Light'] : return False
                if self.tools['Wheels'] != other.tools['Wheels'] : return False
            
            else :
                return True
        else :
            return False
        
    
    
    def Action(self, otherPlayers , blockCards , unblockCards , cartes_de_jeu ):
        
        if len ( unblockCards[0] ) != 0 : # AI sabotter : prefer to unblock a sabotters if there is one 
                                       # AI digger : prefer to unblock a digger
            for i in range (len(unblockCards[0])) :
                count = 1           # The number of the player
                for otherPlayer in otherPlayers :
                    if self.Player_Role.symbol == otherPlayer.Player_Role.symbol :
                        res = super().Unblock_Player( otherPlayer, unblockCards[0][i] )
                        if res : 
                            self.Player_Cards.pop(unblockCards[1][i])
                            if(len(cartes_de_jeu)>0):
                                self.Player_Cards.append(cartes_de_jeu[0])
                                cartes_de_jeu.pop(0)
                            return res , count 
                    count += 1
            
            
        if len ( blockCards[0] ) != 0  : # AI sabotter : will block a digger
                                         # AI digger : will block a sabotter
            for i in range (len(blockCards[0])) : 
                count = 1                # The number of the player
                for otherPlayer in otherPlayers :
                    if ( not self.__eq__(otherPlayer) ) and ( (self.Player_Role.symbol == "saboteur" and otherPlayer.Player_Role.symbol == "digger") or (self.Player_Role.symbol == "digger" and otherPlayer.Player_Role.symbol == "saboteur") ):
                        res = super().Block_Player( otherPlayer , blockCards[0][i] ) 
                        if res : 
                            self.Player_Cards.pop(blockCards[1][i])
                            if(len(cartes_de_jeu)>0):
                                self.Player_Cards.append(cartes_de_jeu[0])
                                cartes_de_jeu.pop(0)
                            return res , count  
                    count += 1
                    
        return False , 0
    


    def ROF( self , grid , cartes_de_jeu):
        
        """
        Depth search starting with start card 
        if saboteur delete a positive path card 
        if digger delete a negative path card 
        """
        for idROF in range( len( self.Player_Cards ) ):
            if self.Player_Cards[idROF].name == "ROF" :
                
                x  , y = grid.startX , grid.startY
                exploredCoord = [[x, y]]
                
                id = 1
                
                while len(exploredCoord) != ( grid.col * grid.row ):

                    for i in range ( -id , id+1 ) : 
                        for j in range ( -id , id+1 ):
                            if ( grid.startY + i > -1 ) and ( grid.startY + i < grid.row ) and ( grid.startX + j > -1 ) and ( grid.startX + j < grid.col ) :
                                
                                if [grid.startX + j,grid.startY + i] in exploredCoord: 
                                    # coordinates already explored 
                                    pass
                                else : 
                                    # explore new coordinates
                                    exploredCoord.append( [grid.startX + j,grid.startY + i] )
                                    
                                    if grid.grid[grid.startY + i][grid.startX + j].name == "path" and ( (self.Player_Role.symbol == "saboteur" and grid.grid[grid.startY + i][grid.startX + j].symbol[4] == '1') or (self.Player_Role.symbol  == "digger" and grid.grid[grid.startY + i][grid.startX + j].symbol[4] == '0') ): 
                                        # card to throw found 
                                        grid.delete_card(1, grid.startX + j , grid.startY + i)
                                        self.Player_Cards.pop(idROF)
                                        if(len(cartes_de_jeu)>0):
                                            self.Player_Cards.append(cartes_de_jeu[0])
                                            cartes_de_jeu.pop(0)
                                        
                                        return True
                                    else :  pass 
                                
                            else :  continue
                    
                    id += 1
                
                return False 
            
        return False 
    
    
    
    def throwCard(self, cards_to_throw , cartes_de_jeu):
        """
        To delete a cared randomly from the list of cards to throw :
            if it's a sabotters the list contain only the positive path cards 
            if it's a digger the list contain only the negative pathg c ards
            if the list is empty, then a random card will be choosen from the AI cards
        """
        if len(cards_to_throw[0]) != 0 : 
            id = random.randint(0, len(cards_to_throw[0]) - 1)
            index = cards_to_throw[1][id]
            self.Player_Cards.pop(id)
            if(len(cartes_de_jeu)>0):
                self.Player_Cards.append(cartes_de_jeu[0])
                cartes_de_jeu.pop(0)
            return True , index+1
        else : 
            id = random.randint(0, len(self.Player_Cards) - 1)
            self.Player_Cards.pop(id)
            if(len(cartes_de_jeu)>0):
                self.Player_Cards.append(cartes_de_jeu[0])
                cartes_de_jeu.pop(0)
            return True , id+1
    
    
    
    def calculate_distance_to_goal(self, XY , grid ):
        """
        Returns the X and Y : closest coordinates to the gold card
        """
        
        listeCoordinates = [ [ grid.startX + 8 , grid.startY - 2 ] , [ grid.startX + 8 , grid.startY ] , [ grid.startX + 8 , grid.startY + 2 ] ]
    
        for Coordinates in listeCoordinates :
            GoalX, GoalY = Coordinates
            
            if grid.grid[GoalY][GoalX].name == "Gold" :
                break
            
        distance = []
        for coord in XY :
            # if coord[0] == -1 : 
            #     coord[0] = 0
            #     coord[1] += 1
            # if coord[1] == -1 : 
            #     coord[1] = 0
            #     coord[0] += 1  
            
            distance.append( abs( GoalX - coord[0] ) + abs( GoalY - coord[1] ) - 1 )
        
        dmin = float("inf")
        index = 0
        
        for i in range(  len(distance) ) :
            if distance[i] < dmin :
                dmin = distance[i]
                index = i
            
        return index
        
    
    
    def find_paths( self, grid ):
        """
        Retourne les coordonnées ou l'IA peut potentiellement poser une carte
        """

        list_of_path = []

                
        x , y = grid.startX , grid.startY
        exploredCoord = [[x, y]]
        
        id = 1
        
        # Exploration inside of mine
        while len(exploredCoord) != ( grid.col * grid.row ):

            for i in range ( -id , id+1 ) : 
                for j in range ( -id , id+1 ):
                    if ( grid.startY + i > -1 ) and ( grid.startY + i < grid.row ) and ( grid.startX + j > -1 ) and ( grid.startX + j < grid.col ) :
                        
                        if [grid.startX + j,grid.startY + i] in exploredCoord: 
                            # coordinates already explored 
                            pass
                        else : 
                            # explore new coordinates
                            exploredCoord.append( [grid.startX + j,grid.startY + i] )
                            
                            if grid.grid[grid.startY + i][grid.startX + j].name == "" and grid.grid[grid.startY + i][grid.startX + j].symbol == "" : 
                                """
                                1 - Verify if the emplacement ( grid.startX + j , grid.startY + i) = empty 
                                2 - verify if there is a card nearby
                                3 - Save the emplacement if so 
                                """
                                if   ( grid.startY + i + 1 > -1 and grid.startY + i + 1 < grid.row ) and grid.grid[grid.startY + i + 1][grid.startX + j].name != "" : list_of_path.append([grid.startX + j ,grid.startY + i])
                                elif ( grid.startY + i - 1 > -1 and grid.startY + i - 1 < grid.row ) and grid.grid[grid.startY + i - 1][grid.startX + j].name != "" : list_of_path.append([grid.startX + j ,grid.startY + i])
                                elif ( grid.startX + j + 1 > -1 and grid.startX + j + 1 < grid.col ) and grid.grid[grid.startY + i][grid.startX + j + 1].name != "" : list_of_path.append([grid.startX + j ,grid.startY + i])
                                elif ( grid.startX + j - 1 > -1 and grid.startX + j - 1 < grid.col ) and grid.grid[grid.startY + i][grid.startX + j - 1].name != "" : list_of_path.append([grid.startX + j ,grid.startY + i])
                                else :  pass
                            else :  pass 
                        
                    else :  continue
            
            id += 1
            
        # Exploration around the mine : add col/row
        # for idCol in range ( grid.col ) :
        #     if grid.grid[0][idCol].name == "END" or grid.grid[0][idCol].name == "Gold" or grid.grid[0][idCol].name == "Stone" or ( grid.grid[0][idCol].symbol != "" and grid.grid[0][idCol].symbol[0] == '1') : 
        #         if [idCol , -1] in exploredCoord: pass
        #         else : list_of_path.append([idCol , -1])
        #     if grid.grid[grid.row-1][idCol].name == "END" or grid.grid[grid.row-1][idCol].name == "Gold" or grid.grid[grid.row-1][idCol].name == "Stone" or ( grid.grid[grid.row-1][idCol].symbol != "" and grid.grid[grid.row-1][idCol].symbol[2] == '1') : 
        #         if [idCol , grid.row] in exploredCoord: pass
        #         else : list_of_path.append([idCol , grid.row])
        
        # for idRow in range ( grid.row ) :
        #     if grid.grid[idRow][0].name == "END" or grid.grid[idRow][0].name == "Gold" or grid.grid[idRow][0].name == "Stone" or (grid.grid[idRow][0].symbol != "" and grid.grid[idRow][0].symbol[3] == '1') : 
        #         if [-1 , idRow] in exploredCoord: pass
        #         else : list_of_path.append([-1 , idRow])
        #     if grid.grid[idRow][grid.col-1].name == "END" or grid.grid[idRow][grid.col-1].name == "Gold" or grid.grid[idRow][grid.col-1].name == "Stone" or (grid.grid[idRow][grid.col-1].symbol != "" and grid.grid[idRow][0].symbol[1] == '1') : 
        #         if [grid.col , idRow] in exploredCoord: pass
        #         else : list_of_path.append([grid.col , idRow])
        
        return list_of_path
    
    
    
    def Path( self, cards_to_play, grid, cartes_de_jeu ):
        """
        Retourne l'emplacement ou l'IA peut potentiellement poser une carte si possible
        1 - Verifier s'il y'a des emplacement possible grace à la methode : find_paths
        3 - Verifier s'il y'a une carte qu'on pourra poser dans l'emplacement grace à la methode de la grille : place_card 
        4 - S'il y'a plusieurs possibilité d'emplacement on choisi la meilleurs : 
                Jouer une carte prés de la carte gold : négative pour bloquer ou positive pour avancer
                Donc on fais un calcul de distance avec la fonction : calculate_distance_to_goal
        """
        res, flag = False, "OFF"
        
        PATHS = self.find_paths(grid)
        
        possible_X_Y = [[] for i in range(2)]
        flag_X_Y = []
        
        if len ( PATHS ) == 0 : return False , "OFF"
        
        else :
            
            for indexC in range( len( cards_to_play[0] ) ):
                c = cards_to_play[0][indexC]
                
                for path in PATHS :
                    res , flag = grid.place_card( c , 1 , path[0] , path[1] )
                    
                    if res :
                        if flag == "ON" and self.Player_Role.symbol == "digger" : 
                            grid.AI_place_card( c, path[0], path[1])
                            self.Player_Cards.pop(cards_to_play[1][indexC])
                            if(len(cartes_de_jeu)>0):
                                self.Player_Cards.append(cartes_de_jeu[0])
                                cartes_de_jeu.pop(0)
                            return True , "ON"
                        
                        possible_X_Y[0].append( path )
                        possible_X_Y[1].append( indexC )
                        flag_X_Y.append( flag )
            
            if len( possible_X_Y[0] ) != 0 :
                bestindex = self.calculate_distance_to_goal( possible_X_Y[0] , grid )
                bestXY = possible_X_Y[0][ bestindex ]
                bestflag = flag_X_Y[ bestindex ]

                grid.AI_place_card( cards_to_play[0][possible_X_Y[1][bestindex]], bestXY[0], bestXY[1])
                TorF, CoordGoal = grid.check_Goal(cards_to_play[0][possible_X_Y[1][bestindex]], bestXY[0], bestXY[1])
                check = grid.check_path( cards_to_play[0][possible_X_Y[1][bestindex]] , bestXY[0], bestXY[1], "GoalCard")                 
                if TorF and check :
                    print("Felicitation, you reached the Goal Card ! ")
                    for Coord in CoordGoal :
                        GoalX, GoalY = Coord
                        res , flag = grid.print_Goal(GoalX, GoalY, "path")

                    bestflag = "ON"
                    
                self.Player_Cards.pop(cards_to_play[1][possible_X_Y[1][bestindex]])
                if(len(cartes_de_jeu)>0):
                    self.Player_Cards.append(cartes_de_jeu[0])
                    cartes_de_jeu.pop(0)
                
                return True , bestflag
            
            else : return False , "OFF"

    
    
    def Choose_Card(self, otherPlayers, grid , cartes_de_jeu ):  # otherPlayers : list of all players
        resAction, resROF, resPath, resThrow , flag = False , False , False , False , "OFF"
        
        # Print IA cards : 
        super().print_cards()
        
        Role = self.Player_Role.symbol
        
        
        # 1 - Block / Unblock other players
        cards_block = [[] for i in range(2)]
        cards_unblock = [[]for i in range(2)]
        for i in range (len(self.Player_Cards)) :
            if self.Player_Cards[i].symbol in ["broke_Li", "broke_P", "broke_W"] :
                cards_block[0].append( self.Player_Cards[i] ) 
                cards_block[1].append( i )
                    
            if self.Player_Cards[i].symbol in ["Li", "P", "W", "LIP", "LIW", "PW"] :
                cards_unblock[0].append( self.Player_Cards[i] )
                cards_unblock[1].append( i )
            
        if len ( cards_block[0] ) != 0 or len ( cards_unblock[0] ) != 0 :
            resAction , count =  self.Action(otherPlayers , cards_block , cards_unblock , cartes_de_jeu)
            
        if not(resAction) : 
            
            # 2 - Play a ROF card :
            resROF = self.ROF(grid , cartes_de_jeu)
            
            if not( resROF ) :
                # AI saboteur plays with a negative path card 
                # AI digger plays  with a positive path card 
                cards_to_play = [[] for i in range(2)]
                cards_to_throw = [[] for i in range(2)]
                
                for i in range (len(self.Player_Cards)) :

                    if ( self.Player_Cards[i].name == 'path' ) and ( ( self.Player_Role.symbol == "saboteur" and self.Player_Cards[i].symbol[4] == '0' ) or ( self.Player_Role.symbol == "digger" and self.Player_Cards[i].symbol[4] == '1' ) ):
                        cards_to_play[0].append( self.Player_Cards[i] )
                        cards_to_play[1].append( i )
                    else :
                        # AI sabotter throws positive cards
                        # AI digger throws negative cards
                        cards_to_throw[0].append( self.Player_Cards[i] )  
                        cards_to_throw[1].append( i )
                 
                            
                # 3 - Play a path card  
                if not(super().Is_Blocked()) and len( cards_to_play[0] ) != 0 :  
                    resPath , flag = self.Path( cards_to_play , grid , cartes_de_jeu ) 
                        
                # 4 - Throw a card
                if not(resPath) : 
                    resThrow , id = self.throwCard(cards_to_throw, cartes_de_jeu)
        
        if resAction : print(" AI choose to play an action card on the player N°", count )
        if resThrow : print(" AI choose to throw the card N°", id )
        if resPath : print(" AI choose to play a path card" )
        if resROF : 
            print(" AI choose to play a ROF card" )
            grid.print_grid()
            
        
        #print ( resAction , resROF , resPath , resThrow )  
        return ( resAction or resROF or resPath or resThrow ) , flag 
    
    
                     

            
