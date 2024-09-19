
import random

# _________________________________CARDs________________________________________

class Card():

    def __init__(self, name, symbol ) :
        self.__name = name
        self.__symbol = symbol
        
    @property
    def name(self):
        return self.__name
        
    @property
    def symbol(self):
        return self.__symbol
    
    @symbol.setter 
    def symbol(self, symbol) :
        if self.symbol == "END" or self.symbol == "Stone" or self.symbol == "Gold" and ( symbol == "END" or symbol == "Stone" or symbol == "Gold"):
            self.__symbol = symbol
        
        
    
    def __str__(self):     
        
        #Print Path Cards "URDL+/-"
        if self.__symbol == "11110" : # "URDLNx" :
            c = "( | )\n(-x-)\n( | )" 
        if self.__symbol == "11100" : #"URDNx" :
            c = "( | )\n( x-)\n( | )" 
        if self.__symbol == "11010" : #"URLNx" :
            c = "( | )\n(-x-)\n(   )" 
        if self.__symbol == "11000" : #"URNx" :
            c = "( | )\n( x-)\n(   )" 
        if self.__symbol == "10010" : #"ULNx" :
            c = "( | )\n(-x )\n(   )" 
        if self.__symbol == "10100" : #"UDNx" :
            c = "( | )\n( x )\n( | )" 
        if self.__symbol == "01010" : #"RLNx" :
            c = "(   )\n(-x-)\n(   )" 
        if self.__symbol == "10000" : #"UNx" :
            c = "( | )\n( x )\n(   )" 
        if self.__symbol == "01000" : #"RNx" :
            c = "(   )\n( x-)\n(   )" 
        if self.__symbol == "11111" : #"URDLN+" :
            c = "( | )\n(-+-)\n( | )" 
        if self.__symbol == "11101" : #"URDN+" :
            c = "( | )\n( +-)\n( | )" 
        if self.__symbol == "11011" : #"URLN+" :
            c = "( | )\n(-+-)\n(   )" 
        if self.__symbol == "11001" : #"URN+" :
            c = "( | )\n( +-)\n(   )" 
        if self.__symbol == "10011" : #"ULN+" :
            c = "( | )\n(-+ )\n(   )" 
        if self.__symbol == "10101" : #"UDN+" :  
            c = "( | )\n( + )\n( | )" 
        if self.__symbol == "01011" : #"RLN+" : 
            c = "(   )\n(-+-)\n(   )" 
        # Print MAP Cards
        if self.__symbol == "MAP" :
            c = "( M )\n(MAP)\n( P )"
        # Print ROF Cards
        if self.__symbol == "ROF" :
            c = "( R )\n(ROF)\n( F )"
        # Print Block Cards
        if self.__symbol == "broke_Li" :
            c = "(ATT)\n( L )\n(   )" 
        if self.__symbol == "broke_P" :
            c = "(ATT)\n( P )\n(   )" 
        if self.__symbol == "broke_W" :
            c = "(ATT)\n( W )\n(   )"  
        # Print UNblock Cards
        if self.__symbol == "Li" :
            c = "(DEF)\n( L )\n(   )" 
        if self.__symbol == "P" :
            c = "(DEF)\n( P )\n(   )" 
        if self.__symbol == "W" :
            c = "(DEF)\n( W )\n(   )" 
        if self.__symbol == "LIP" :
            c = "(DEF)\n(L&P)\n(   )" 
        if self.__symbol == "LIW" :
            c = "(DEF)\n(W&L)\n(   )" 
        if self.__symbol == "PW" :
            c = "(DEF)\n(P&W)\n(   )"
        # Print No card
        if self.__symbol == "" :
            c = "     \n     \n     "
        # Print Role  
        if self.__symbol == "saboteur" :
            c = "Saboteur"
        if self.__symbol == "digger" :
            c = "Digger"

        #Print Goal Cards
        if self.__symbol == "Gold" :
            c = "( | )\n(-G-)\n( | )" 
        if self.__symbol == "Stone" :
            c = "( | )\n(-N-)\n( | )"
        if self.__symbol == "END" :
            c = "( E )\n(END)\n( D )"
            
        #Print Start Card
        if self.__symbol == "1111S" :
            c = "( | )\n(-S-)\n( | )" 
        
        #Print Gold Cards
        if self.__symbol == "3G" :
            c = "(   )\n( 3G)\n(   )"
        if self.__symbol == "2G" :
            c = "(   )\n( 2G)\n(   )"
        if self.__symbol == "1G" :
            c = "(   )\n( 1G)\n(   )"
        return c

            

#_______________________________________________________________________________           

class PathCards(Card):
    # URDL 5*N+ 1* Nx
    # URD  5*N+ 1* Nx
    # URL  5*N+ 1* Nx
    # UR   5*N+ 1* Nx
    # UL   4*N+ 1* Nx
    # UD   4*N+ 1* Nx
    # RL   3*N+ 1* Nx
    # U         1* Nx
    # R         1* Nx
     
    # 40 cards
    def __init__(self) :
        super().__init__( "path" , None )
        self.__cards = []
        
        Values = ["11110","11100","11010","11000","10010","10100","01010","10000","01000"]
        for val in Values :
            self.cards.append(Card("path" , val))
                              
                                 
        Values = ["11111","11101","11011","11001"]
        for i in range(5):
            for val in Values :
                self.cards.append(Card("path" , val))
                                  
        Values = ["10011","10101"]
        for i in range(4):
            for val in Values :
                self.cards.append(Card("path" , val))  
                                  
        for i in range(3):
            self.__cards.append(Card("path" , "01011")) 
        
    @property
    def cards(self):
        return self.__cards
    
    def __str__(self):
        pass         
    


#_______________________________________________________________________________ 
class BlockActionCards(Card) :
    # 27 Action cards 
    # 9 cards to block
    # Li, P, W: Light, Pike, Wagon (tools required to dig galleries)
        # Li  *3 Block
        # P   *3 Block
        # W   *3 Block 
    def __init__(self) :
        super().__init__( "Block" , None)
        self.__cards = []
        for i in range(3):
            self.__cards.append(Card("action" ,"broke_Li"))
            self.__cards.append(Card("action" ,"broke_P"))
            self.__cards.append(Card("action" ,"broke_W"))
       
    @property
    def cards(self):
        return self.__cards



#_______________________________________________________________________________             
class UnblockActionCards(Card) :
    # 9 cards to unblock
    # Li, P, W: Light, Pike, Wagon (tools required to dig galleries)
        # Li  *2 Unblock 
        # P   *2 Unblock 
        # W   *2 Unblock 
        # LIP *1 Unblock
        # LIW *1 Unblock
        # PW  *1 Unblock 
    def __init__(self) :
        super().__init__( "Unblock" , None)
        self.__cards = []
        self.__cards.append(Card("action" ,"LIP"))
        self.__cards.append(Card("action" ,"LIW"))
        self.__cards.append(Card("action" ,"PW"))
        for i in range(2):
            self.__cards.append(Card("action" ,"Li"))
            self.__cards.append(Card("action" ,"P"))
            self.__cards.append(Card("action" ,"W"))
       
    @property
    def cards(self):
        return self.__cards



#_______________________________________________________________________________ 
class MAPActionCards(Card) :
    # 6 cards
    # MAP *6: card allowing a player to look at one of the end
    def __init__(self) :
        super().__init__( "MAP" , None )
        self.__cards = []
        for i in range(6):
            self.__cards.append(Card("MAP", "MAP"))
    
    @property
    def cards(self):
        return self.__cards
        
    

#_______________________________________________________________________________ 
class ROFActionCards(Card) :
    # 3 cards
    # RoF *3: Rock Fall (card allowing a player to remove 1 gallery)
    
    def __init__(self) :
        super().__init__( "ROF" , None )
        self.__cards = []
        for i in range(3):
            self.__cards.append(Card("ROF","ROF"))
        
    @property
    def cards(self):
        return self.__cards


    
#_______________________________________________________________________________ 
class GoalCards (Card) :
    # 2 * stone Cards
    # 1 * gold Card
    def __init__( self ) :
        super().__init__( "Goal" , None )
        self.__cards = []
        self.__cards.append(Card("Gold"  ,"END"))
        self.__cards.append(Card("Stone" ,"END"))
        self.__cards.append(Card("Stone" ,"END"))

    @property
    def cards(self):
        return self.__cards
    
        
    def isGold( c: Card) :
         if c.name == "Gold" :
             return True
         else :
             return False



#_______________________________________________________________________________ 
class RoleCards (Card) :

    def __init__(self,nb_Player) :
        super().__init__( "Role" , None )
        self.__Cards = []
        
        if nb_Player == 3 or nb_Player == 4 :
            self.__Cards.append(Card("Role","saboteur"))
            for i in range ( 1 , nb_Player ):
                self.__Cards.append(Card("Role","digger"))
        if nb_Player == 5 or nb_Player == 6 :
            for i in range ( 2 ):
                self.__Cards.append(Card("Role","saboteur"))
            for i in range ( 2 , nb_Player ):
                self.__Cards.append(Card("Role","digger"))
        if nb_Player == 7 or nb_Player == 8 or nb_Player == 9 :
            for i in range ( 3 ):
                self.__Cards.append(Card("Role","saboteur"))
            for i in range ( 3 , nb_Player ):
                self.__Cards.append(Card("Role","digger"))
        if nb_Player == 10 :
            for i in range ( 4 ):
                self.__Cards.append(Card("Role","saboteur"))
            for i in range ( 4 , nb_Player ):
                self.__Cards.append(Card("Role","digger"))
    @property           
    def Cards(self):
        return self.__Cards
    


#_______________________________________________________________________________ 
class RewardCards (Card) :
    # 1G, 2G, 3G: reward cards (1, 2 or 3 gold)
    def __init__(self) :
        super().__init__( "Reward", None)
        self.__Cards = []
        for i in range(4):
            self.__Cards.append(Card("Reward","3G"))
        for i in range(8):
            self.__Cards.append(Card("Reward","2G"))
        for i in range(16):
            self.__Cards.append(Card("Reward","1G"))
        
        
    
    @property
    def Cards(self):
        return self.__Cards


