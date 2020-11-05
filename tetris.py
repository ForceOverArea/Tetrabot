import copy, random

"""
This library is a 'toolbox' for building a tetris game elsewhere

- This library intended for use with Discord.py/Discord API
"""

def default():
    # This function can be copied and modified to 
    # provide different skins for the game
    """
    Returns a dict of the default discord emojis used by the game.
    """
    return {
    "r":":red_square:",
    "o":":orange_square:",
    "y":":yellow_square:",
    "g":":green_square:",
    "b":":blue_square:",
    "p":":purple_square:",
    "w":":blue_circle:",
    "empty":":black_circle:"}


def new_board(entities=default()):
    """
    Returns a blank 8x12 tetris board with only empty spaces.
        - This is in list(list(str)) format
    """
    #tile = entities["empty"]
    
    top_margin = 2*[11*[""]]
    body = 16*[[""] + 8*[entities["empty"]] + [""] + [""]]
    #real_body = copy.deepcopy(body) #BUG: spotted a potential bug where all rows point to the same address
    real_body = [
        [""] + 8*[copy.deepcopy(entities["empty"])] + [""] + [""],
        [""] + 8*[copy.deepcopy(entities["empty"])] + [""] + [""],
        [""] + 8*[copy.deepcopy(entities["empty"])] + [""] + [""],
        [""] + 8*[copy.deepcopy(entities["empty"])] + [""] + [""],
        [""] + 8*[copy.deepcopy(entities["empty"])] + [""] + [""],
        [""] + 8*[copy.deepcopy(entities["empty"])] + [""] + [""],
        [""] + 8*[copy.deepcopy(entities["empty"])] + [""] + [""],
        [""] + 8*[copy.deepcopy(entities["empty"])] + [""] + [""],
        [""] + 8*[copy.deepcopy(entities["empty"])] + [""] + [""],
        [""] + 8*[copy.deepcopy(entities["empty"])] + [""] + [""],
        [""] + 8*[copy.deepcopy(entities["empty"])] + [""] + [""],
        [""] + 8*[copy.deepcopy(entities["empty"])] + [""] + [""],
        [""] + 8*[copy.deepcopy(entities["empty"])] + [""] + [""],
        [""] + 8*[copy.deepcopy(entities["empty"])] + [""] + [""],
        [""] + 8*[copy.deepcopy(entities["empty"])] + [""] + [""],
        [""] + 8*[copy.deepcopy(entities["empty"])] + [""] + [""]
    ]
    bottom_margin = [11*[""]]
    
    raw = top_margin + real_body + bottom_margin
    return raw


class tetramino():
    def __init__(self, shape, rotation=0, entities=default()): # defaults to plain square emoji set
        self.entities = entities
        self.shape = shape.upper()  # shape must be a string representing the "letter name" of each tetramino
        self.rot = rotation # rotation can have value 0-3 with each int corresponding to 90deg rotation


    def render(self):
        """
        Renders the tetramino in a list(list(str)) format.
             - NOTE doing this "unpacks" the information about the tetramino to a 
                    more visual-fiendly format, but is much harder to manipulate 
                    than the tetramino obj itself.
        """
        if self.shape == "T":
            # define the entities used here, then put them in a grid below
            # this applies to all shapes
            t = self.entities["p"]
            o = self.entities["empty"]

            if self.rot == 0:
                return [
                    [o,o,o,o],
                    [t,t,t,o],
                    [o,t,o,o],
                    [o,o,o,o]
                ]

            if self.rot == 1:
                return [
                    [o,o,o,o],
                    [o,t,o,o],
                    [o,t,t,o],
                    [o,t,o,o]
                ]

            if self.rot == 2:
                return [
                    [o,o,o,o],
                    [o,t,o,o],
                    [t,t,t,o],
                    [o,o,o,o]
                ]

            if self.rot == 3:
                return [
                    [o,o,o,o],
                    [o,t,o,o],
                    [t,t,o,o],
                    [o,t,o,o]
                ]

        if self.shape == "I":
            t = self.entities["w"]
            o = self.entities["empty"]
            
            if self.rot in [0,2]:
                return [
                    [o,o,o,o],
                    [o,o,o,o],
                    [t,t,t,t],
                    [o,o,o,o]
                ]

            if self.rot in [1,3]:
                return [
                    [o,t,o,o],
                    [o,t,o,o],
                    [o,t,o,o],
                    [o,t,o,o]
                ]
                
        if self.shape == "L":
            t = self.entities["o"]
            o = self.entities["empty"]
            
            if self.rot == 0:
                return [
                    [o,o,o,o],
                    [o,t,o,o],
                    [o,t,o,o],
                    [o,t,t,o]
                ]

            if self.rot == 1:
                return [
                    [o,o,o,o],
                    [o,o,t,o],
                    [t,t,t,o],
                    [o,o,o,o]
                ]

            if self.rot == 2:
                return [
                    [o,o,o,o],
                    [t,t,o,o],
                    [o,t,o,o],
                    [o,t,o,o]
                ]

            if self.rot == 3:
                return [
                    [o,o,o,o],
                    [o,o,o,o],
                    [t,t,t,o],
                    [t,o,o,o]
                ]

        if self.shape == "J":
            t = self.entities["b"]
            o = self.entities["empty"]
            
            if self.rot == 0:
                return [
                    [o,o,o,o],
                    [o,t,o,o],
                    [o,t,o,o],
                    [t,t,o,o]
                ]

            if self.rot == 1:
                return [
                    [o,o,o,o],
                    [o,o,o,o],
                    [t,t,t,o],
                    [o,o,t,o]
                ]

            if self.rot == 2:
                return [
                    [o,o,o,o],
                    [o,t,t,o],
                    [o,t,o,o],
                    [o,t,o,o]
                ]

            if self.rot == 3:
                return [
                    [o,o,o,o],
                    [t,o,o,o],
                    [t,t,t,o],
                    [o,o,o,o]
                ]

        if self.shape == "S":
            t = self.entities["g"]
            o = self.entities["empty"]
            
            if self.rot in [0,2]:
                return [
                    [o,o,o,o],
                    [o,t,t,o],
                    [t,t,o,o],
                    [o,o,o,o]
                ]

            if self.rot in [1,3]:
                return [
                    [o,o,o,o],
                    [t,o,o,o],
                    [t,t,o,o],
                    [o,t,o,o]
                ]

        if self.shape == "Z":
            t = self.entities["r"]
            o = self.entities["empty"]
            
            if self.rot in [0,2]:
                return [
                    [o,o,o,o],
                    [t,t,o,o],
                    [o,t,t,o],
                    [o,o,o,o]
                ]

            if self.rot in [1,3]:
                return [
                    [o,o,o,o],
                    [o,t,o,o],
                    [t,t,o,o],
                    [t,o,o,o]
                ]

        if self.shape == "O":
            t = self.entities["y"]
            o = self.entities["empty"]
            return [ # shape has only one unique orientation, so no decision tree
                [o,o,o,o],
                [o,t,t,o],
                [o,t,t,o],
                [o,o,o,o]
            ]


    def rotate(self, direction:bool):
        if not direction:
            self.rot += 1
            if self.rot > 3:
                self.rot = 0
        elif direction:
            self.rot += -1
            if self.rot < 0:
                self.rot = 3
        else:
            raise Exception("error in '.rotate' method")


class board(): 
    """THIS CLASS IS PRIMARILY MEANT FOR USE WITHIN THE 'GAME' CLASS. IT MAY MISBEHAVE WHEN ALTERED INDEPENDENTLY"""
    def __init__(self, entities=default(), state=new_board()):
        self.entities = entities
        self.state = state


    def merge(self, sprite, x, y):
        """
        Merges a tetramino to the board's 'state' attribute if the result 
        adheres to game rules
        """
        sprite = sprite.render()
        ymargin = 1
        xmargin = 0
        entities = self.entities

        for j in range(y+ymargin, y+4+ymargin):
            for i in range(x+xmargin, x+4+xmargin):
                sj = j-y-ymargin #find x,y coords for pixels in the 'sprite list'
                si = i-x-xmargin

                sprite_pixel_empty = sprite[sj][si] == entities["empty"]
                board_pixel_empty = self.state[j][i] == entities["empty"]

                if sprite_pixel_empty: 
                    continue

                if not sprite_pixel_empty:
                    
                    if board_pixel_empty: 
                        self.state[j][i] = sprite[sj][si]
                    
                    else: # if the above conditions are not meant, crash
                        raise Exception(f"Tetramino is colliding with a solid object at board pixel x:{i} y:{j}")


    def clear_lines(self):
        """Clears all lines that have no empty entities in them."""
        count = 0
        for j in range(2,18): #not sure what index the bottom of the board is at |:[
            if self.entities["empty"] not in self.state[j]:
                self.state.pop(j)
                count+=1
                self.state.insert(2, [""] + 8*[copy.deepcopy(self.entities["empty"])] + [""] + [""],)

        return count


    def display(self, sprite, x, y):
        """Method that overlays a sprite on the board temporarily"""
        sprite = sprite.render()
        tempstate = copy.deepcopy(self.state)
        ymargin = 1
        xmargin = 0
        entities = self.entities

        for j in range(y+ymargin, y+4+ymargin):
            for i in range(x+xmargin, x+4+xmargin):
                sj = j-y-ymargin #find x,y coords for pixels in the 'sprite list'
                si = i-x-xmargin

                sprite_pixel_empty = sprite[sj][si] == entities["empty"]
                board_pixel_empty = tempstate[j][i] == entities["empty"]

                if sprite_pixel_empty: 
                    continue

                if not sprite_pixel_empty:
                    
                    if board_pixel_empty: 
                        tempstate[j][i] = sprite[sj][si]
                    
                    else: # if the above conditions are not meant, crash
                        raise Exception(f"Tetramino is colliding with a solid object at board pixel x:{i} y:{j}")
        
        return "\n".join(["".join(row) for row in tempstate])
        
    
    def dispraw(self):
        return "\n".join(["".join(row) for row in self.state])


class game():
    """Represents a tetris game with a distinct board and active piece.""" 
    def __init__(self, player, instance, board:board, x:int, y:int):
        self.instance = instance
        self.player = player
        
        self.board = board
        self.grab_bag = ["T","I","O","L","J","S","Z"]
        random.shuffle(self.grab_bag)
        self.score = 0;
        self.piece = tetramino(self.grab_bag.pop())
        self.x = x
        self.y = y


    def left(self):
        """Moves the cursor 1 unit left."""
        self.board.display(self.piece, self.x-1, self.y)
        # if the operation is illegal, the board.display() 
        # method will crash and prevent the data update
        self.x += -1


    def right(self):
        """Moves the cursor 1 unit right."""
        self.board.display(self.piece, self.x+1, self.y)
        
        self.x += 1


    def drop(self):
        """Drops the piece by 1 unit if possible."""
        self.board.display(self.piece, self.x, self.y+1)
        
        self.y += 1


    def cw(self):
        """Changes the piece's angle by -90deg."""
        rotation_test = copy.copy(self.piece)
        rotation_test.rotate(True)
        self.board.display(rotation_test, self.x, self.y)
        self.piece.rotate(True)
            

    def ccw(self):
        """Changes the piece's angle by +90deg."""
        rotation_test = copy.copy(self.piece)
        rotation_test.rotate(False)
        self.board.display(rotation_test, self.x, self.y)
        self.piece.rotate(False)

    def harddrop(self):
        """Instantly drops a piece as far down as possible."""
        for hdy in range((self.y),18):
            try:
                self.board.display(self.piece, self.x, hdy)
            except:
                self.board.display(self.piece, self.x, hdy-1) #crashes if the resulting harddrop is impossible/illegal
                self.y = hdy-1 #sets the cursor position


    def clear(self):
        """Clears all complete lines on the board."""
        score_factor = self.board.clear_lines()
        if score_factor != 0:
            self.score += 10**score_factor


    def grab(self):
        """Picks a new piece from the grab bag and automatically refills it when empty."""
        try:
            self.piece = tetramino(self.grab_bag.pop())
        except:
            self.grab_bag = ["T","I","O","L","J","S","Z"]
            random.shuffle(self.grab_bag)
            self.piece = tetramino(self.grab_bag.pop())


    def merge(self):
        """Merges the current piece to the board at the current cursor position."""
        self.board.merge(self.piece, self.x, self.y)


    def display(self):
        """Returns a string of the current game's screen."""
        return self.board.display(self.piece, self.x, self.y) 
