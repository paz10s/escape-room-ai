import pygame, sys, random, os
from time import sleep
pygame.font.init()

clock = pygame.time.Clock()

# Screens
WINDOW_WIDTH, WINDOW_HEIGHT = 450, 600
SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
CELL = pygame.Surface([150,150])
DOOR = pygame.Surface([150,20])
pygame.display.set_caption('Escape Room AI')

# Values
DARK = (33, 33, 33)
GRAY = (100, 100, 100)
FPS = 60

class State:

    def __init__(self, name, a1, k1, k2):
        self.name = name
        self.a1 = a1
        self.k1 = k1
        self.k2 = k2

        self.children = []
        self.parents = []
        self.traversed = False

        self.move_up = None
        self.move_down = None
        self.move_left = None
        self.move_right = None

    def set(self):
        agent1.state = self
        agent1.cell = self.a1
        key1.taken = self.k1
        key2.taken = self.k2

    def set_children(self, children):
        for child in children:
            self.children.append(child)

            child.parents.append(self)

    def set_parents(self, parents):
        self.parents = parents

    def set_traversed(self, state):
        self.traversed = state

    def get_name(self):
        return self.name

    def get_children(self):
        return self.children

    def get_parents(self):
        return self.parents

    def get_traversed_parents(self):
        traversed_parents = [parent for parent in self.parents if parent.traversed == True]

        return traversed_parents

    def get_traversed(self):
        return self.traversed

    def up(self, state):
        self.move_up = state

    def down(self, state):
        self.move_down = state

    def left(self, state):
        self.move_left = state

    def right(self, state):
        self.move_right = state

class Cell:

    def __init__(self, name, y, x, coords, traversable):
        self.name = name
        self.x = x
        self.y = y
        self.coords = coords
        self.traversable = traversable
        self.traversed = False
        self.key = None

    def set_key(self, key):
        self.key = key

    def get_agent(self):
        return self.agent

    def get_key(self):
        return self.key

class Key:

    def __init__(self, cell):
        self.cell = cell
        self.taken = False

    def get_cell(self):
        return self.cell

class Agent:

    def __init__(self):
        self.key_count = 0
        self.cell = None
        self.search_dist = 1
        self.ref_cell = self.cell
        self.state = None
        self.move = None

    def cw(self):
        if self.cell in [a1, b1]:
            self.move_right()
            self.move = 'R'
        elif self.cell in [c1, c2]:
            self.move_down()
            self.move = 'D'
        elif self.cell in [c3, b3]:
            self.move_left()
            self.move = 'L'
        elif self.cell in [a3, a2]:
            self.move_up()
            self.move = 'U'

    def ccw(self):
        if self.cell in [c1, b1]:
            self.move_left()
            self.move = 'L'
        elif self.cell in [c3, c2]:
            self.move_up()
            self.move = 'U'
        elif self.cell in [a3, b3]:
            self.move_right()
            self.move = 'R'
        elif self.cell in [a1, a2]:
            self.move_down()
            self.move = 'D'

    def move_up(self):
        next_cell = GRID[self.cell.y-1][self.cell.x]
        self.cell = next_cell

    def move_down(self):
        next_cell = GRID[self.cell.y+1][self.cell.x]
        self.cell = next_cell

    def move_left(self):
        next_cell = GRID[self.cell.y][self.cell.x-1]
        self.cell = next_cell

    def move_right(self):
        next_cell = GRID[self.cell.y][self.cell.x+1]
        self.cell = next_cell

    def key_pickup(self):
        self.key_count += 1
        self.cell.key.taken = True
        self.cell.set_key(None)

    def ex(self):
        self.cell = ex

    def get_cell(self):
        return self.cell

class Door:

    def __init__(self):
        self.opened = False

#region Grid object init
o1 = Cell('o1', 0, 0, (0,0), False)
o2 = Cell('o2', 0, 1, (150,0), False)
ex = Cell('ex', 0, 2, (300,0), False)
a1 = Cell('a1', 1, 0, (0,150), True)
b1 = Cell('b1', 1, 1, (150,150), True)
c1 = Cell('c1', 1, 2, (300,150), True)
a2 = Cell('a2', 2, 0, (0,300), True)
b2 = Cell('b2', 2, 1, (150,300), False)
c2 = Cell('c2', 2, 2, (300,300), True)
a3 = Cell('a3', 3, 0, (0,450), True)
b3 = Cell('b3', 3, 1, (150,450), True)
c3 = Cell('c3', 3, 2, (300,450), True)
GRID =  [[o1, o2, ex],
         [a1, b1, c1],
         [a2, b2, c2],
         [a3, b3, c3]]
black = [o1, o2, b2] # non-traversable cells
white = [ex, a1, b1, c1, a2, c2, a3, b3, c3] # traversable cells
coords = black + white # all cells
spawns = [a3, a2, a1, c1, c2, b3]
#endregion

#region States object init
s1 = State('s1', a3, False, False)
s2 = State('s2', a2, False, False)
s3 = State('s3', a1, False, False)
s4 = State('s4', c1, False, False)
s5 = State('s5', c2, False, False)
s6 = State('s6', b3, False, False)
s7 = State('s7', a3, True, False)
s8 = State('s8', a2, True, False)
s9 = State('s9', a1, True, False)
s10 = State('s10', b1, True, False)
s11 = State('s11', c1, True, False)
s12 = State('s12', c2, True, False)
s13 = State('s13', b3, True, False)
s14 = State('s14', a3, False, True)
s15 = State('s15', a2, False, True)
s16 = State('s16', a1, False, True)
s17 = State('s17', c1, False, True)
s18 = State('s18', c2, False, True)
s19 = State('s19', c3, False, True)
s20 = State('s20', b3, False, True)
s21 = State('s21', a3, True, True)
s22 = State('s22', a2, True, True)
s23 = State('s23', a1, True, True)
s24 = State('s24', b1, True, True)
s25 = State('s25', c1, True, True)
s26 = State('s26', c2, True, True)
s27 = State('s27', c3, True, True)
s28 = State('s28', b3, True, True)
s29 = State('s29', ex, True, True)

GOAL = s29

STATES = [s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15, s16, s17, s18, s19, s20, s21, s22, s23, s24, s25, s26, s27, s28, s29]

s1.set_children([s2, s6])
s2.set_children([s1, s3])
s3.set_children([s2, s10])
s4.set_children([s5, s10])
s5.set_children([s4, s19])
s6.set_children([s1, s19])
s7.set_children([s8, s13])
s8.set_children([s7, s9])
s9.set_children([s8, s10])
s10.set_children([s9, s11])
s11.set_children([s10, s12])
s12.set_children([s11, s27])
s13.set_children([s7, s27])
s14.set_children([s15, s20])
s15.set_children([s14, s16])
s16.set_children([s15, s24])
s17.set_children([s18, s24])
s18.set_children([s17, s19])
s19.set_children([s18, s20])
s20.set_children([s14, s19])
s21.set_children([s22, s28])
s22.set_children([s21, s23])
s23.set_children([s22, s24])
s24.set_children([s23, s25])
s25.set_children([s29])
s26.set_children([s25, s27])
s27.set_children([s26, s28])
s28.set_children([s21, s27])

s1.up(s2)
s1.right(s6)
s2.up(s3)
s2.down(s1)
s3.right(s10)
s3.down(s2)
s4.down(s5)
s4.left(s10)
s5.down(s19)
s5.up(s4)
s6.left(s1)
s6.right(s19)
s7.right(s13)
s7.up(s8)
s8.down(s7)
s8.up(s9)
s9.down(s8)
s9.right(s10)
s10.left(s9)
s10.right(s11)
s11.left(s10)
s11.down(s12)
s12.up(s11)
s12.down(s27)
s13.right(s27)
s13.left(s7)
s14.up(s15)
s14.right(s20)
s15.up(s16)
s15.down(s14)
s16.right(s24)
s16.down(s15)
s17.down(s18)
s17.left(s24)
s18.down(s19)
s18.up(s17)
s19.left(s20)
s19.up(s18)
s20.left(s14)
s20.right(s19)
s21.right(s28)
s21.up(s22)
s22.down(s21)
s22.up(s23)
s23.down(s22)
s23.right(s24)
s24.left(s23)
s24.right(s25)
s25.up(s29)
s26.up(s25)
s26.down(s27)
s27.up(s26)
s27.left(s28)
s28.right(s27)
s28.left(s21)
#endregion

# Keys creation
key1 = Key(b1)
key2 = Key(c3)

# Agent creation
agent1 = Agent()

# Door creation
door1 = Door()

# Images
KEY_IMG = pygame.image.load(os.path.join('images', 'key.png'))
KEY = pygame.transform.scale(KEY_IMG, (60, 60))
AGENT_IMG = pygame.image.load(os.path.join('images', 'agent.png'))
AGENT = pygame.transform.scale(AGENT_IMG, (80, 80))

# Text
LABEL_FONT = pygame.font.SysFont('Arial', 20)
SPAWN_FONT = pygame.font.SysFont('Arial', 35)

def draw_spawns():
    for n in range(6):
        SCREEN.blit(SPAWN_FONT.render('['+str(n+1)+']', 1, (255,255,255)), (tuple(i+60 for i in spawns[n].coords)))

def draw_labels():
    for coord in coords:
        SCREEN.blit(LABEL_FONT.render(coord.name, 1, (DARK)), (tuple(i+5 for i in coord.coords)))

    SCREEN.blit(LABEL_FONT.render(b2.name, 1, (200,200,200)), (tuple(i+5 for i in b2.coords)))

def render():
    draw_grid()
    draw_agent1()
    draw_labels()
    if key1.taken == False:
        draw_key1()
    if key2.taken == False:
        draw_key2()
    if door1.opened == False:
        draw_door()

def draw_grid():
    CELL.fill(DARK)
    for cell in black:
        SCREEN.blit(CELL, cell.coords)
        rect = pygame.Rect(cell.coords[0], cell.coords[1], 150, 150)
        pygame.draw.rect(SCREEN, DARK, rect, 1)

    CELL.fill(GRAY)
    for cell in white:
        SCREEN.blit(CELL, cell.coords)
        rect = pygame.Rect(cell.coords[0], cell.coords[1], 150, 150)
        pygame.draw.rect(SCREEN, DARK, rect, 1)

def draw_key1():
    SCREEN.blit(KEY, [i+85 for i in b1.coords])
    b1.set_key(key1)

def draw_key2():
    SCREEN.blit(KEY, [i+85 for i in c3.coords])
    c3.set_key(key2)

def draw_agent1():
    SCREEN.blit(AGENT, [i+35 for i in agent1.cell.coords])

def draw_door():
    DOOR.fill((162, 97, 59))
    SCREEN.blit(DOOR, (300,130))

def rand_dir():
    return random.choice(['cw','ccw'])

def move(dir):
    if dir == 'cw':
        agent1.cw()
    elif dir == 'ccw':
        agent1.ccw()

def check_state():
    if agent1.cell == a3 and key1.taken == False and key2.taken == False:
        agent1.state = s1
        return ('s1')
    elif agent1.cell == a2 and key1.taken == False and key2.taken == False:
        agent1.state = s2
        return ('s2')
    elif agent1.cell == a1 and key1.taken == False and key2.taken == False:
        agent1.state = s3
        return ('s3')
    elif agent1.cell == c1 and key1.taken == False and key2.taken == False:
        agent1.state = s4
        return ('s4')
    elif agent1.cell == c2 and key1.taken == False and key2.taken == False:
        agent1.state = s5
        return ('s5')
    elif agent1.cell == b3 and key1.taken == False and key2.taken == False:
        agent1.state = s6
        return ('s6')
    elif agent1.cell == a3 and key1.taken == True and key2.taken == False:
        agent1.state = s7
        return ('s7')
    elif agent1.cell == a2 and key1.taken == True and key2.taken == False:
        agent1.state = s8
        return ('s8')
    elif agent1.cell == a1 and key1.taken == True and key2.taken == False:
        agent1.state = s9
        return ('s9')
    elif agent1.cell == b1 and key1.taken == True and key2.taken == False:
        agent1.state = s10
        return ('s10')
    elif agent1.cell == c1 and key1.taken == True and key2.taken == False:
        agent1.state = s11
        return ('s11')
    elif agent1.cell == c2 and key1.taken == True and key2.taken == False:
        agent1.state = s12
        return ('s12')
    elif agent1.cell == b3 and key1.taken == True and key2.taken == False:
        agent1.state = s13
        return ('s13')
    elif agent1.cell == a3 and key1.taken == False and key2.taken == True:
        agent1.state = s14
        return ('s14')
    elif agent1.cell == a2 and key1.taken == False and key2.taken == True:
        agent1.state = s15
        return ('s15')
    elif agent1.cell == a1 and key1.taken == False and key2.taken == True:
        agent1.state = s16
        return ('s16')
    elif agent1.cell == c1 and key1.taken == False and key2.taken == True:
        agent1.state = s17
        return ('s17')
    elif agent1.cell == c2 and key1.taken == False and key2.taken == True:
        agent1.state = s18
        return ('s18')
    elif agent1.cell == c3 and key1.taken == False and key2.taken == True:
        agent1.state = s19
        return ('s19')
    elif agent1.cell == b3 and key1.taken == False and key2.taken == True:
        agent1.state = s20
        return ('s20')
    elif agent1.cell == a3 and key1.taken == True and key2.taken == True:
        agent1.state = s21
        return ('s21')
    elif agent1.cell == a2 and key1.taken == True and key2.taken == True:
        agent1.state = s22
        return ('s22')
    elif agent1.cell == a1 and key1.taken == True and key2.taken == True:
        agent1.state = s23
        return ('s23')
    elif agent1.cell == b1 and key1.taken == True and key2.taken == True:
        agent1.state = s24
        return ('s24')
    elif agent1.cell == c1 and key1.taken == True and key2.taken == True:
        agent1.state = s25
        return ('s25')
    elif agent1.cell == c2 and key1.taken == True and key2.taken == True:
        agent1.state = s26
        return ('s26')
    elif agent1.cell == c3 and key1.taken == True and key2.taken == True:
        agent1.state = s27
        return ('s27')
    elif agent1.cell == b3 and key1.taken == True and key2.taken == True:
        agent1.state = s28
        return ('s28')
    elif agent1.cell == ex:
        agent1.state = s29
        return ('s29')

def get_path(start_node):
    checked = []
    while solution[-1] != start_node:

        if solution[-1].get_traversed_parents() == []:
            while len(solution[-1].get_traversed_parents()) <= 1:   # while node <= 1 parent
                checked.append(solution[-1])
                solution.pop(-1)

        for parent in solution[-1].get_traversed_parents():
             if (parent not in checked) and (parent not in solution):
                solution.append(parent)
                break

    solution.reverse()
    done = True

def get_actions():

    actions = []

    for i in range(0, len(solution)-1):
        if solution[i].move_up == solution[i+1]:
            actions.append('U')
        elif solution[i].move_down == solution[i+1]:
            actions.append('D')
        elif solution[i].move_left == solution[i+1]:
            actions.append('L')
        elif solution[i].move_right == solution[i+1]:
            actions.append('R')

    return(actions)



solution = []

# ====================================================================



def main():

    print('\n\n==========================================================')

    print('Choose an algorithm (press the number):')
    print('[1] Depth First Search')
    print('[2] Breadth First Search')

    algo = None
    while algo == None:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_1:
                    algo = "DFS"
                    print('Depth First Search chosen.')
                if event.key == pygame.K_2:
                    algo = "BFS"
                    print('Breadth First Search chosen.')

        draw_grid()
        draw_labels()
        if key1.taken == False:
            draw_key1()
        if key2.taken == False:
            draw_key2()
        if door1.opened == False:
            draw_door()

        pygame.display.flip()
        clock.tick(4)

    print('\nChoose spawn point (press any number seen in the GUI): ')

    start_node = None
    start_cell = None
    while start_node == None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_1:
                    start_cell = a3
                    start_node = s1
                    s1.set()
                if event.key == pygame.K_2:
                    start_cell = a2
                    start_node = s2
                    s2.set()
                if event.key == pygame.K_3:
                    start_cell = a1
                    start_node = s3
                    s3.set()
                if event.key == pygame.K_4:
                    start_cell = c1
                    start_node = s4
                    s4.set()
                if event.key == pygame.K_5:
                    start_cell = c2
                    start_node = s5
                    s5.set()
                if event.key == pygame.K_6:
                    start_cell = b3
                    start_node = s6
                    s6.set()

        draw_spawns()

        pygame.display.flip()
        clock.tick(4)

    print('State ' + check_state() + ' chosen.')
    print('Starting.')


    print('==========================================================\n')

    direction = rand_dir()
    steps = 1

    if algo == "DFS":

        queue = [check_state()]

        print('START. (Screen displays the last state in PATH).')
        print('*Goal check occurs every time after a node is added.')
        print('Added ' + queue[-1], end='\t')
        print('>1 child detected.', end='\t')
        print('PATH:', end=' ')
        for i in queue:
            print(i, end=' ')
        print()

        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_RETURN:
                        if agent1.cell == ex:
                            print('======SOLUTION======')
                            print('State transition:', end='\t')

                            for i in queue:
                                print(i, end='  ' if len(i) == 2 else ' ')
                            print()

                            print('Actions (from ' + start_node.get_name() + '):', end='\t')
                            for i in solution:
                                print(i, end='   ')
                            print('\nGoal is achieved (state {} to {}) in {} steps.'.format(start_node.get_name(), GOAL.get_name(), steps))
                            print('Press [ESC] to exit.\n')

                        elif agent1.cell.key == None:

                            steps += 1

                            if agent1.state == s25:
                                agent1.ex()
                                solution.append('U')
                            else:
                                move(direction)
                                solution.append(agent1.move)

                            if agent1.cell.key == None:
                                queue.append(check_state())
                                print('Added ' + queue[-1], end='\t\t\t\t')
                                print('PATH:', end=' ')
                                for i in queue:
                                    print(i, end=' ')
                                print()

                                if agent1.key_count == 2 and agent1.cell == ex:
                                    print('\nGOAL (s29) FOUND.\n')

                            else:
                                agent1.key_pickup()
                                queue.append(check_state())
                                prev_direction = direction
                                direction = rand_dir()
                                print('Added ' + queue[-1], end='\t')
                                print('>1 child detected.', end='\t')
                                print('PATH:', end=' ')
                                for i in queue:
                                    print(i, end=' ')
                                print()

            SCREEN.fill(GRAY)

            # Rendering
            render()

            # Door rules
            if agent1.cell == c1 and agent1.key_count == 2:
                door1.opened = True

            pygame.display.flip()
            clock.tick(30)

    elif algo == "BFS":
        solution.append(s29)
        queue = [start_node]
        done = False

        print('START. (Screen displays the first state in QUEUE).')
        print('*Goal check occurs every time before a node is enqueued.')
        print('Queued ' + start_node.get_name(), end='\t\t\t\t\t')
        print('QUEUE:', end=' ')
        for i in queue:
            print(i.get_name(), end=' ')
        print()

        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_RETURN:
                        if done == False:
                            if queue != []:
                                steps += 1
                                node = queue[0]

                                if not all(child.get_traversed() for child in node.get_children()):
                                    node.set_traversed(True)

                                for child in node.get_children():

                                    if child == GOAL:
                                        print('\nGOAL (s29) FOUND.\n')
                                        door1.opened = True
                                        get_path(start_node)
                                        done = True
                                        break
                                    elif child.get_traversed() == False:
                                        queue.append(child)

                                if done != True:
                                    i = 0
                                    print('Queued', end=' ')
                                    for child in node.get_children():
                                        if child.get_traversed() == False:
                                            print(child.get_name(), end=' ')
                                            i += 1
                                    if i == 0:
                                        print('None', end='')

                                    print('\t\tDequeued ' + queue[0].get_name(), end='\t\t')
                                    queue.pop(0)
                                    queue[0].set()

                                    print('QUEUE:', end=' ')
                                    for i in queue:
                                        print(i.get_name(), end=' ')
                                    print()

                            else:
                                print('Nothing in queue')


                        else:
                            agent1.ex()

                            print('======SOLUTION======')
                            print('State transition:', end='\t')
                            for i in solution:
                                print(i.get_name(), end='  ' if len(i.get_name()) == 2 else ' ')
                            print()


                            print('Actions (from ' + start_node.get_name() + '):', end='\t')
                            for i in get_actions():
                                print(i, end='   ')
                            print('\nGoal is achieved (state {} to {}) in {} steps.'.format(start_node.get_name(), GOAL.get_name(), steps))
                            print('Press [ESC] to exit.\n')

            SCREEN.fill(GRAY)

            # Rendering
            render()

            # Door rules
            if agent1.state == 25:
                door1.opened = True

            pygame.display.flip()
            clock.tick(30)

if __name__ == "__main__":
    main()