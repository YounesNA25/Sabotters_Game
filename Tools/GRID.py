
from Tools.CARDs import *

import random


"""
  x : column 
  y : row
"""


class Grid():
    def __init__(self):
        self.__col = 9
        self.__row = 5
        self.__listGoal = GoalCards().cards
        self.__startX = 0
        self.__startY = 2

        grid = []
        empty_card = Card("", "")
        for i in range(self.__row):
            ligne = []
            for j in range(self.__col):
                ligne.append(empty_card)
            grid.append(ligne)
        self.__grid = grid



    @property
    def startX(self):
        return self.__startX 
    
    @property
    def startY(self):
        return self.__startY
    
    @property
    def col(self):
        return self.__col 
    
    @property
    def row(self):
        return self.__row
    
    @property
    def grid(self):
        return self.__grid



    def create_grid(self):
        self.__grid[2][0] = Card("path", "1111S")

        index = random.randint(0, 2)
        self.__grid[0][8] = self.__listGoal[index]

        if index == 0:
            index = random.randint(1, 2)
            if index == 1:
                self.__grid[2][8] = self.__listGoal[1]
                self.__grid[4][8] = self.__listGoal[2]
            else:
                self.__grid[2][8] = self.__listGoal[2]
                self.__grid[4][8] = self.__listGoal[1]

        elif index == 2:
            if index == 1:
                self.__grid[2][8] = self.__listGoal[1]
                self.__grid[4][8] = self.__listGoal[0]
            else:
                self.__grid[2][8] = self.__listGoal[0]
                self.__grid[4][8] = self.__listGoal[1]

        else:
            # 0 pour la case 0 / 1 pour la case 2
            index = random.randint(0, 1)
            if index == 1:
                self.__grid[2][8] = self.__listGoal[2]
                self.__grid[4][8] = self.__listGoal[0]
            else:
                self.__grid[2][8] = self.__listGoal[0]
                self.__grid[4][8] = self.__listGoal[2]



    def print_grid(self):
        #pattern_col = " |  0    1    2    3    4    5    6    7    8  "
        #pattern_border = "-+---------------------------------------------"
        pattern_col = " |"
        pattern_border = "-+"

        for i in range(self.__col):
            pattern_col += "  " + str(i) + "  "
            pattern_border += "-----"

        print(pattern_col)
        print(pattern_border)
        l1 = " |"
        l2 = str(0) + "|"
        l3 = " |"
        for i in range(self.__row):
            for j in range(self.__col):
                c = self.__grid[i][j].__str__()
                l1 = l1 + c[:5]
                l2 = l2 + c[6:11]
                l3 = l3 + c[12:]
            print(l1)
            print(l2)
            print(l3)

            l1 = " |"
            l2 = str(i+1) + "|"
            l3 = " |"
        print(pattern_border)



    def __eq__(self, other, x, y):
        myCard = self.__grid[y][x]
        if myCard.symbol != other.symbol:
            return False
        else:
            if myCard.name != other.name:
                return False
            else:
                return True
    
    
    
    def AI_place_card(self,c , x, y):
        self.__grid[y][x] = c
        
    
    def print_Goal(self, GoalX, GoalY, condition):
        
        res, flag = False, "OFF"
        
        if condition == "path" :
            if self.__grid[GoalY][GoalX].symbol == "END":
                self.__grid[GoalY][GoalX].symbol = self.__grid[GoalY][GoalX].name
                res = True
                
                if self.__grid[GoalY][GoalX].name == "Gold" :
                    flag = "ON"
                
        if condition == "MAP" :

            # coordinates of the Goal Cards :
            listeCoordinates = [ [ self.__startX + 8 , self.__startY - 2 ] , [ self.__startX + 8 , self.__startY ] , [ self.__startX + 8 , self.__startY + 2 ] ]
             
            print('What is the emplacement of the card that you want to see (x,y)? ')
            GoalX = int(input('x = '))
            GoalY = int(input('y = '))
                
            val = False
            
            # To check if the coordinates chosen are one of the three Goal coordinates
            for coord in listeCoordinates :
                if GoalX == coord[0] and GoalY == coord[1]:
                    val = True or val
                    
            if val :
                
                res = True
 
                self.__grid[GoalY][GoalX].symbol = self.__grid[GoalY][GoalX].name
                self.print_grid()
                input('Press Enter to continue ...')
                self.__grid[GoalY][GoalX].symbol = "END"   
                
        return res, flag
    
    
    """
        The original grid has 5 rows and 9 columns
        it's possibal to make the grid bigger, but we have to respect somme conditions:
            - we have c : the actual col number 
                      r : the actual row number
            - if we want to put a card on line   -1 or l+1 => modify the number of the rows
            - if we want to put a card on column -1 or c+1 => modify the number of the columns
            - in other cases ( exp :to put a card on line  -2  or l+2 ) => no modifications
    """

    def __add_col_row(self, x, y, new_card: Card):
        # we recover actual r and actual c :
        r, c = self.__row, self.__col

        if (y >= -1 and y <= r) and (x >= -1 and x <= c):

            # add a row :
            if x >= 0 and x <= c-1:
                self.__row += 1
                empty_card = Card("", "")
                new_row = [empty_card] * c      # a line of empty card
                self.__grid.append(new_row)       # add the line to the grid

                # add a row at the top
                if y == -1:
                    self.__startY += 1
                    for i in range(r, 0, -1):
                        for j in range(c):
                            self.__grid[i][j] = self.__grid[i-1][j]
                    for i in range(c):
                        self.__grid[0][i] = empty_card
                    self.__grid[0][x] = new_card

                # add a row at the bottom
                else:
                    self.__grid[r][x] = new_card

            # add a column :
            if y >= 0 and y <= r-1:
                self.__col += 1
                empty_card = Card("", "")
                for i in range(r):
                    self.__grid[i].append(empty_card)

                # add a column to the left
                if x == -1:
                    self.__startX += 1
                    for j in range(c, 0, -1):
                        for i in range(r):
                            self.__grid[i][j] = self.__grid[i][j-1]

                    for i in range(r):
                        self.__grid[i][0] = empty_card

                    self.__grid[y][0] = new_card

                # add a column to the right
                else:
                    self.__grid[y][c] = new_card

            return True
        else:
            return False


    def __check_card(self, c, x, y, status_player):

        empty_card = Card("", "")

        # to Check if the emplacement choosen is an empty card, otherwase it's not possible to place a card in the emplacemnt if there is already a card
        if x == -1 or y == -1 or x == len(self.__grid[0]) or y == len(self.__grid) or (self.__eq__(empty_card, x, y) and x >= 0 and x < len(self.__grid[0]) and y >= 0 and y < len(self.__grid)) :
            U, R, D, L, P_N = c.symbol[0], c.symbol[1], c.symbol[2], c.symbol[3], c.symbol[4]
            nb_connection = 0
#                                                               ( | )
# ______________________________________Connection with the top (   ) _____________________________________________
#                                                               (   )
            if U == '1' and x >= 0 and x < len( self.__grid[0] ):
                if y > 0 and y < len(self.__grid) :
                    if not (self.__eq__(empty_card, x, y-1)) and self.__grid[y-1][x].name == "path" and self.__grid[y-1][x].symbol[2] == '1':
                        nb_connection += 1
                    elif not (self.__eq__(empty_card, x, y-1)) and self.__grid[y-1][x].name == "path" and self.__grid[y-1][x].symbol[2] == '0':
                        return False
                    else:  # if the card in y-1 is an empty card
                        nb_connection = nb_connection
                elif y <= 0:   # No verification needed here
                    nb_connection = nb_connection
                else:  # y == len( self.__grid ) :  # Grid extension
                    if not (self.__eq__(empty_card, x, y-1)) and self.__grid[y-1][x].name == "path" and self.__grid[y-1][x].symbol[2] == '1':
                        self.__add_col_row(x, y, c)
                        return True
                    else:
                        return False

            if U == '0' and x >= 0 and x < len( self.__grid[0] ):
                if y > 0 and y < len(self.__grid) :
                    if not (self.__eq__(empty_card, x, y-1)) and self.__grid[y-1][x].name == "path" and self.__grid[y-1][x].symbol[2] == '1':
                        return False
                    else:  # if the card in y-1 is an empty card or a card with D = '0'
                        nb_connection = nb_connection
                elif y <= 0:   # No verification needed here
                    nb_connection = nb_connection
                else:  # y == len( self.__grid ) :  # No Grid extension : it's possible to add a row at the bottom only if U == '1' and the card at y-1 has D == '1
                    return False
#                                                                 (   )
# ________________________________________Connection to the right (  -) _____________________________________________
#                                                                 (   )
            if R == '1':
                if x >= 0 and x < len(self.__grid[0]) - 1:
                    if not (self.__eq__(empty_card, x+1, y)) and self.__grid[y][x+1].name == "path" and self.__grid[y][x+1].symbol[3] == '1':
                        nb_connection += 1
                    elif not (self.__eq__(empty_card, x+1, y)) and self.__grid[y][x+1].name == "path" and self.__grid[y][x+1].symbol[3] == '0':
                        return False
                    else:  # if the card in x+1 is an empty card
                        nb_connection = nb_connection
                elif x >= len(self.__grid) - 1:   # No verification needed
                    nb_connection = nb_connection
                else:  # x == -1 :  # Grid extension
                    if not (self.__eq__(empty_card, x+1, y)) and self.__grid[y][x+1].name == "path" and self.__grid[y][0].symbol[3] == '1':
                        self.__add_col_row(x, y, c)
                        return True
                    else:
                        return False

            else:  # R == '0' :
                if x >= 0 and x < len(self.__grid[0]) - 1:
                    if not (self.__eq__(empty_card, x+1, y)) and self.__grid[y][x+1].name == "path" and self.__grid[y][x+1].symbol[3] == '1':
                        return False
                    else:  # if the card in y+1 is an empty card or a card with U = '0'
                        nb_connection = nb_connection
                elif x >= len(self.__grid[0]) - 1:   # No verification needed
                    nb_connection = nb_connection
                else:  # x == -1 :  # No Grid extension : it's possible to add a column to the left only if R == '1' and the card at x = 0 has L == '1'
                    return False
#                                                                  (   )
# ______________________________________Connection with the bottom (   ) _____________________________________________
#                                                                  ( | )
            if D == '1' and x >= 0 and x < len( self.__grid[0] ):
                if y >= 0 and y < len(self.__grid) - 1 :
                    if not (self.__eq__(empty_card, x, y+1)) and self.__grid[y+1][x].name == "path" and self.__grid[y+1][x].symbol[0] == '1':
                        nb_connection += 1
                    elif not (self.__eq__(empty_card, x, y+1)) and self.__grid[y+1][x].name == "path" and self.__grid[y+1][x].symbol[0] == '0':
                        return False
                    else:  # if the card in y+1 is an empty card
                        nb_connection = nb_connection
                elif y >= len(self.__grid) - 1:   # No verification needed
                    nb_connection = nb_connection
                else:  # y == -1 :  # Grid extension
                    if not (self.__eq__(empty_card, x, y+1)) and self.__grid[0][x].name == "path" and self.__grid[0][x].symbol[0] == '1':
                        self.__add_col_row(x, y, c)
                        return True
                    else:
                        return False

            if D == '0' and x >= 0 and x < len( self.__grid[0] ):
                if y >= 0 and y < len(self.__grid) - 1 :
                    if not (self.__eq__(empty_card, x, y+1)) and self.__grid[y+1][x].name == "path" and self.__grid[y+1][x].symbol[0] == '1':
                        return False
                    else:  # if the card in y+1 is an empty card or a card with U = '0'
                        nb_connection = nb_connection
                elif y >= len(self.__grid) - 1:   # No verification needed
                    nb_connection = nb_connection
                else:  # y == -1 :  # No Grid extension : it's possible to add a row at the top only if D == '1' and the card at y = 0 has U == '1
                    return False
#                                                                  (   )
# ___________________________________________Connection to the left(-  ) _____________________________________________
#                                                                  (   )
            if L == '1':

                if x > 0 and x < len(self.__grid[0]):
                    if not (self.__eq__(empty_card, x-1, y)) and self.__grid[y][x-1].name == "path" and self.__grid[y][x-1].symbol[1] == '1':
                        nb_connection += 1
                    elif not (self.__eq__(empty_card, x-1, y)) and self.__grid[y][x-1].name == "path" and self.__grid[y][x-1].symbol[1] == '0':
                        return False
                    else:  # if the card in x-1 is an empty card
                        nb_connection = nb_connection
                elif x <= 0:   # No verification needed here
                    nb_connection = nb_connection
                else:  # x == len( self.__grid[0] ) :  # Grid extension
                    if not (self.__eq__(empty_card, x-1, y)) and self.__grid[y][x-1].name == "path" and self.__grid[y][x-1].symbol[1] == '1':
                        self.__add_col_row(x, y, c)
                        return True
                    else:
                        return False

            else:  # L == '0'
                if x > 0 and x < len(self.__grid[0]):
                    if not (self.__eq__(empty_card, x-1, y)) and self.__grid[y][x-1].name == "path" and self.__grid[y][x-1].symbol[1] == '1':
                        return False
                    else:  # if the card in x-1 is an empty card or a card with R = '0'
                        nb_connection = nb_connection
                elif x <= 0:   # No verification needed here
                    nb_connection = nb_connection
                else:  # x == len( self.__grid[0] ) :  # No Grid extension : it's possible to add a row to the right only if L == '1' and the card at x-1 has R == '1
                    return False

            if nb_connection > 0:
                if status_player == 0 : self.__grid[y][x] = c
                return True
            else:
                return False

        else:
            return False


    def __getNextMoves(self, currentC, currentX, currentY, condition ):

        U, R, D, L , PN= currentC.symbol[0], currentC.symbol[1], currentC.symbol[2], currentC.symbol[3], currentC.symbol[4]
        empty_card = Card("", "")
        listCoord = []
        
        if condition == "PathCard" :
            if U == '1' and currentY > 0 and currentX < len(self.__grid[0]) and not (self.__eq__(empty_card, currentX, currentY-1)) and (self.__grid[currentY-1][currentX].name == "path") and self.__grid[currentY-1][currentX].symbol[2] == '1':
                listCoord.append([currentX, currentY-1])
            if D == '1' and currentY < len(self.__grid)-1 and currentX < len(self.__grid[0]) and not (self.__eq__(empty_card, currentX, currentY+1)) and (self.__grid[currentY+1][currentX].name == "path") and self.__grid[currentY+1][currentX].symbol[0] == '1':
                listCoord.append([currentX, currentY+1])
            if L == '1' and currentX > 0 and currentY < len(self.__grid) and not (self.__eq__(empty_card, currentX-1, currentY)) and (self.__grid[currentY][currentX-1].name == "path") and self.__grid[currentY][currentX-1].symbol[1] == '1':
                listCoord.append([currentX-1, currentY])
            if R == '1' and currentX < len(self.__grid[0])-1 and currentY < len(self.__grid) and not (self.__eq__(empty_card, currentX+1, currentY)) and (self.__grid[currentY][currentX+1].name == "path") and self.__grid[currentY][currentX+1].symbol[3] == '1':
                listCoord.append([currentX+1, currentY])
                
        if condition == "GoalCard" :
            if U == '1' and PN == '1' and currentY > 0 and currentX < len(self.__grid[0]) and not (self.__eq__(empty_card, currentX, currentY-1)) and (self.__grid[currentY-1][currentX].name == "path") and self.__grid[currentY-1][currentX].symbol[2] == '1':
                listCoord.append([currentX, currentY-1])
            if D == '1' and PN == '1' and currentY < len(self.__grid)-1 and currentX < len(self.__grid[0]) and not (self.__eq__(empty_card, currentX, currentY+1)) and (self.__grid[currentY+1][currentX].name == "path") and self.__grid[currentY+1][currentX].symbol[0] == '1':
                listCoord.append([currentX, currentY+1])
            if L == '1' and PN == '1' and currentX > 0 and currentY < len(self.__grid) and not (self.__eq__(empty_card, currentX-1, currentY)) and (self.__grid[currentY][currentX-1].name == "path") and self.__grid[currentY][currentX-1].symbol[1] == '1':
                listCoord.append([currentX-1, currentY])
            if R == '1' and PN == '1' and currentX < len(self.__grid[0])-1 and currentY < len(self.__grid) and not (self.__eq__(empty_card, currentX+1, currentY)) and (self.__grid[currentY][currentX+1].name == "path") and self.__grid[currentY][currentX+1].symbol[3] == '1':
                listCoord.append([currentX+1, currentY])

        return listCoord


    def check_path(self, c, x, y, condition):
        """
            Conditions d'arret: 1- si  j'arrive à la carte start
                                2- si aucun des chemins me conduisent à la carte start 
        """
        searchPaths = [[[x, y]]]
        visitedCoord = [[x, y]]

        Val = True

        while (Val):

            if len(searchPaths) == 0:
                return False

            currentPath = searchPaths.pop(0)
            currentCoord = currentPath[-1]
            currentX, currentY = currentCoord

            if currentX == x and currentY == y:
                currentC = c
            else:
                currentC = self.__grid[currentY][currentX]

            if currentX == self.__startX and currentY == self.__startY:
                return True
            else:
                
                listCoord = self.__getNextMoves(currentC, currentX, currentY, condition)
                if len(listCoord) == 0:
                    if len(searchPaths) == 0:
                        return False
                else:
                    for nextCoord in listCoord:
                        if nextCoord in visitedCoord:
                            continue

                        searchPaths.append(currentPath + [nextCoord])
                        visitedCoord += [nextCoord]


    def check_Goal(self, c, x, y):
        # coordinates of the Goal Cards :
        listeCoordinates = [ [ self.__startX + 8 , self.__startY - 2 ] , [ self.__startX + 8 , self.__startY ] , [ self.__startX + 8 , self.__startY + 2 ] ]
        
        # in the case of a grid extension the new x and y of the new card that is already added to the grid 
        if x == -1 : x = 0  
        if y == -1 : y = 0
        
        # the list that we will return full of the Gaol Card Coordinates reached
        list = []
        
        for Coordinates in listeCoordinates :
            GoalX, GoalY = Coordinates
            
            if  self.__grid[GoalY][GoalX].symbol == "END" and (  ( x == GoalX and ( ( y == GoalY-1 and c.symbol[1] == '1') or ( y == GoalY+1 and c.symbol[3] == '1' ) ) ) or ( y == GoalY and ( ( x == GoalX-1 and c.symbol[1] == '1' ) or ( x == GoalX+1 and c.symbol[3] == '1' ) ) ) ):
                list.append([GoalX, GoalY])
            else : 
                continue

        if len(list) != 0 : return True , list 
        else : return False , list 


    def place_card(self, c, status_player, x, y):
        
        Test , TestX, TestY, count = True, True, True, 0
        
        if status_player == 0 :  # if the player is a Human he will choose the emplacement of his card
            while Test :
            
                if count == 0 : print('Where do you want to place your card (x,y)? :  ')
                if count == 1 : print('Please try again, wich (x,y)? :  ')
                x = input('x = ')
                y = input('y = ')
    
                for nb in range( -1, self.__col, 1) :
                    if x != str(nb) : continue
                    else : 
                        TestX = False
                        break 
                    
                for nb in range( -1, self.__row, 1) :
                    if y != str(nb) : continue
                    else : 
                        TestY = False
                        break 
                
                Test = TestX or TestY
                count = 1
            
            x = int(x) ; y = int(y) ;

        
        if self.check_path(c, x, y, "PathCard") :
            res = self.__check_card(c, x, y, status_player)
            if res : 
                TorF, CoordGoal = self.check_Goal(c, x, y)
                flag = "OFF"
                
                if TorF and self.check_path(c, x, y, "GoalCard") :
                    print("Felicitation, you reached the Goal Card ! ")
                    for Coord in CoordGoal :
                        GoalX, GoalY = Coord
                        res , flag = self.print_Goal(GoalX, GoalY, "path")
                return True, flag      #"The chosen position is validated"       
            else : return False, "OFF" #"Error: the chosen position is wrong ! "
        else : return False, "OFF"     #"Error: the chosen position is wrong ! "

    
    def delete_card( self, status_player, x , y ):
        empty_card = Card("", "")
        
        Test , TestX, TestY, count = True, True, True, 0
        if status_player == 0 :
            while Test :
                
                    if count == 0 : print('What is the emplacement of the card that you want to remove from the grid (x,y)? ')
                    if count == 1 : print('Please try again, wich (x,y)? :  ')
                    x = input('x = ')
                    y = input('y = ')
            
                    for nb in range( -1, self.__col, 1) :
                        if x != str(nb) : continue
                        else : 
                            TestX = False
                            break 
                        
                    for nb in range( -1, self.__row, 1) :
                        if y != str(nb) : continue
                        else : 
                            TestY = False
                            break 
                    
                    Test = TestX or TestY
                    count = 1
                
                    x = int(x) ; y = int(y) ;
                
        
        if x >= 0 and y >= 0 and x < self.__col and y < self.__row and not (self.__eq__(empty_card, x, y)) and self.grid[y][x].symbol[4] != 'S' and self.grid[y][x].name != "END" and self.grid[y][x].name != "Stone" and self.grid[y][x].name != "Gold" :
            self.__grid[y][x] = Card("", "")
            return True 
        
        else : return False

