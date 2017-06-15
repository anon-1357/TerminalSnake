import curses
from curses import KEY_RIGHT, KEY_LEFT, KEY_DOWN, KEY_UP
from random import randint

# Variables
WIDTH = 35 # game cell width
HEIGHT = 20 # game cell height
MAX_X = WIDTH - 2 # sets max inside the game, so the snake wont hit the border
MAX_Y = HEIGHT - 2
SNAKE_LENGTH = 5 # Snake length at game start
SNAKE_X = SNAKE_LENGTH + 1
SNAKE_Y = 3
TIMEOUT = 100 #this controls the speed of the game

class Snake(object):
    # REV_DIR_MAP
    REV_DIR_MAP = {
        KEY_UP: KEY_DOWN, KEY_DOWN: KEY_UP,
        KEY_LEFT: KEY_RIGHT, KEY_RIGHT: KEY_LEFT,
        }
    
    # Init, score, timeout, body list
    def __init__(self, x, y, window):
        self.body_list = []
        self.hit_score = 0
        self.timeout = TIMEOUT
        # Append The Snake's range to the Body object for Snakes Body
        for i in range(SNAKE_LENGTH, 0, -1):
            self.body_list.append(Body(x - i, y))
            
        self.body_list.append(Body(x, y, '0')) # Defines the snakes head
        self.window = window # Defines the window
        self.direction = KEY_RIGHT # Move snake to right when game starts
        self.last_head_coor = (x, y) # set snakes lst head coordinate
        # Defines direction map
        self.direction_map = {
            KEY_UP: self.move_up,
            KEY_DOWN: self.move_down,
            KEY_LEFT: self.move_left,
            KEY_RIGHT: self.move_right
            }
    
    # Properties on the objects
    @property
    def score(self):
        return 'Score: {}'.format(self.hit_score)

    # This adds the snake body
    def add_body(self, body_list):
        self.body_list.extend(body_list)

    # Eat food function
    def eat_food(self, food):
        food.reset() # reset food
        # Choosing x y coordinates for the new body part on the snake
        body = Body(self.last_head_coor[0], self.last_head_coor[1])
        # Adding above variable to the body array on the snake
        self.body_list.insert(-1, body)
        self.hit_score += 1 # update game score
        # Timer function. Play with this to see what it acutally does
        if self.hit_score % 3 == 0:
            self.timeout -= 5
            self.window.timeout(self.timeout)

    # Property decorator
    @property
    def collided(self): # Body collided function, if snake head hits body part end game
        return any([body.coor == self.head.coor
            for body in self.body_list[:-1]])

    # Animation updating function
    def update(self):
        last_body = self.body_list.pop(0)
        last_body.x = self.body_list[-1].x # setting x and y for the snake head
        last_body.y = self.body_list[-1].y
        self.body_list.insert(-1, last_body)
        self.last_head_coor = (self.head.x, self.head.y) # sets last head coordinate
        # grabs direction map from above, sets its direction on update
        self.direction_map[self.direction]()

    # Change direction function
    def change_direction(self, direction):
        if direction != Snake.REV_DIR_MAP[self.direction]:
            self.direction = direction
    # Render Function
    def render(self):
        for body in self.body_list:
            # Adds snake body to window
            self.window.addstr(body.y, body.x, body.char)

    # Property decorator
    @property
    # Defines the snake's head
    def head(self):
        # snake head should always be the first in the body list, thats why its negative here
        return self.body_list[-1]
    
    @property
    # Sets snake's head initial coordinate
    def coor(self):
        return self.head.x, self.head.y

    # Move up function
    def move_up(self):
        self.head.y -= 1
        if self.head.y < 1:
            self.head.y = MAX_Y
            
    # Move down function
    def move_down(self):
        self.head.y += 1
        if self.head.y > MAX_Y:
            self.head.y = 1
            
    # Move left function
    def move_left(self):
        self.head.x -= 1
        if self.head.x < 1:
            self.head.x = MAX_X
    # Move right function
    def move_right(self):
        self.head.x += 1
        if self.head.x > MAX_X:
            self.head.x = 1

# Body object
class Body(object):
    def __init__(self, x, y, char='='): # Initializes self
        self.x = x
        self.y = y
        self.char = char
    @property
    # Sets coordinate 
    def coor(self):
        return self.x, self.y

# Food object
class Food(object):
    # Defines init Food
    def __init__(self, window, char='&'):
        self.x = randint(1, MAX_X) # Gives random postion for food
        self.y = randint(1, MAX_Y)
        self.char = char # Setting the food character
        self.window = window

    # Defines Render Function with Curses
    def render(self):
        self.window.addstr(self.y, self.x, self.char)
    
    # Defines reset method
    def reset(self):
        self.x = randint(1, MAX_X)
        self.y = randint(1, MAX_Y)

if __name__ == '__main__':
    curses.initscr() # Curses Function for initializing Curses
    curses.beep() # Make Beeping Noise twice
    curses.beep()
    
    window = curses.newwin(HEIGHT, WIDTH, 0, 0) # Makes Curses Window
    window.timeout(TIMEOUT) # Sets window timeout
    window.keypad(1) # Set keypad
    curses.noecho() # Leave echo mode. Echoing of input characters is turned off.
    curses.curs_set(0) # Sets curses visibility state
    window.border(0) # Sets window border
    
    snake = Snake(SNAKE_X, SNAKE_Y, window) # Grab snake and food object
    food = Food(window, '*')
    
    while True:
        window.clear() # clear window
        window.border(0) # set border
        snake.render() # render snake
        food.render() # render food
        window.addstr(0, 5, snake.score) # addstr to the window
        event = window.getch() # gets a character from user input
        
        if event == 27: # Breaks if event equals to windo.getch if == 27
            break
        
        # Allows to move the snakes direction
        if event in [KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT]:
            snake.change_direction(event)

        # Allows the snake to eat the food, and then reset see line 50
        if snake.head.x == food.x and snake.head.y == food.y:
            snake.eat_food(food)

        if event == 32:
            key = -1
            while key != 32:
                key = window.getch()

        snake.update() # Calls snake
        if snake.collided: # Ends game if snake collides
            break
                
    curses.endwin() # end curses