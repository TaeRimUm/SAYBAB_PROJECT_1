import random
import time
import threading
    #pip install threading

#pip install schedule
import Hamburger
import game_framework
import server
from pico2d import *
import game_world
import winsound

from BehaviorTree import BehaviorTree, Selector, Sequence, Leaf
from Hamburger import hamburger

# Skul4 Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 10.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Skul4 Action Speed
TIME_PER_ACTION = 1.0
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 10

animation_names = ['Idle', 'Walk']

class Skul4: #맨 위에
    frame = 0
    images = None
    font = None

    def load_images(self):
        if Skul4.images == None:
            Skul4.images = {}
            for name in animation_names:
                Skul4.images[name] = [load_image("./Skul_1/" + name + " (%d)" % i + ".png") for i in range(1, 11)]


    def __init__(self, name='NONAME', x=0, y=0, size=1):
        self.name = name
        self.x, self.y = x * PIXEL_PER_METER, y * PIXEL_PER_METER
        self.size = size
        if Skul4.font is None:
            Skul4.font = load_font('ENCR10B.TTF', 16)
        self.load_images()
        self.dir = random.random() * 2 * math.pi
        self.speed = 0
        self.timer = 1.0
        self.frame = 0
        self.build_behavior_tree()
        self.hp = 0
        self.target_Hamburger = None

        self.x, self.y, self.fall_speed = random.randint(0, 1600), random.randint(740, 750), 0


    def __getstate__(self):
        state = {'x': self.x, 'y': self.y, 'dir': self.dir, 'name': self.name, 'size': self.size}
        return state

    def __setstate__(self, state):
        self.__init__()
        self.__dict__.update(state)

    def calculate_current_position(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        self.x += self.speed * math.cos(self.dir) * game_framework.frame_time
        self.y += self.speed * math.sin(self.dir) * game_framework.frame_time
        self.x = clamp(0, self.x, get_canvas_width() + 750)
        self.y = clamp(0, self.y, get_canvas_height() + 1600)

    def find_random_location(self):
        self.tx, self.ty = random.randint(50, get_canvas_width()-50), random.randint(50, get_canvas_height() - 50)
        return BehaviorTree.SUCCESS

    def move_to(self, radius=0.5):
        distance = (self.tx - self.x) ** 2 + (self.ty - self.y) ** 2
        self.dir = math.atan2(self.ty - self.y, self.tx - self.x)
        if distance < (PIXEL_PER_METER * radius) ** 2:
            self.speed = 0
            return BehaviorTree.SUCCESS
        else:
            self.speed = RUN_SPEED_PPS
            return BehaviorTree.RUNNING

    def flee_from_saybar(self):

        distance = self.calculate_squared_distance(self, server.saybar)
        if distance > (PIXEL_PER_METER * 10) ** 2:
            self.speed = 0
            return BehaviorTree.FAIL

        if self.hp <= server.saybar.hp:
            self.dir = math.atan2(self.y - server.saybar.y, self.x - server.saybar.x)
            self.speed = RUN_SPEED_PPS
            return BehaviorTree.RUNNING
        else:
            self.speed = 0
            return BehaviorTree.FAIL

    def build_behavior_tree(self):
        find_random_location_node = Leaf('Find Random Location', self.find_random_location)
        move_to_node = Leaf('Move To', self.move_to)
        wander_sequence = Sequence('Wander', find_random_location_node, move_to_node)
        find_Hamburger_location_node = Leaf('Find hamburger Location', self.find_Hamburger_location)
        eat_Hamburger_sequence = Sequence('Eat hamburger', find_Hamburger_location_node, move_to_node)
        wander_or_eat_ball_selector = Selector('Wander & Eat hamburger', eat_Hamburger_sequence, wander_sequence)
        flee_from_saybar_node = Leaf('Flee from Saybar', self.flee_from_saybar)
        final_selector = Selector('Final', flee_from_saybar_node, wander_or_eat_ball_selector)
        self.bt = BehaviorTree(final_selector)


    def update(self):
        self.bt.run()
        self.calculate_current_position()


    def draw(self):
        sx, sy = self.x - server.background.window_left, self.y - server.background.window_bottom
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION

        if math.cos(self.dir) < 0:
            if self.speed == 0:
                Skul4.images['Idle'][int(self.frame)].composite_draw(0, 'h', sx, sy, 100, 100)
            else:
                Skul4.images['Walk'][int(self.frame)].composite_draw(0, 'h', sx, sy, 100, 100)
        else:
            if self.speed == 0:
                Skul4.images['Idle'][int(self.frame)].draw(sx, sy, 100, 100)
            else:
                Skul4.images['Walk'][int(self.frame)].draw(sx, sy, 100, 100)

    def get_bb(self):
        return self.x - 10, self.y - 10, self.x + 10, self.y + 10

    def handle_collision(self, other, group):
        if group == 'Saybar:Skul4':
            game_world.remove_object(self)

    def find_Hamburger_location(self):
        # fill here
        self.target_Hamburger = None
        shortest_distance = 1280 ** 2
        for o in game_world.all_objects():
            if type(o) is hamburger:
                Hamburger = o
                distance = (Hamburger.x - self.x) ** 2 + (Hamburger.y - self.y) ** 2
                if distance < (PIXEL_PER_METER * 1000) ** 2 and distance <= shortest_distance:
                    self.target_Hamburger = Hamburger
                    shortest_distance = distance
        if self.target_Hamburger is not None:
            self.tx, self.ty = self.target_Hamburger.x, self.target_Hamburger.y
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def calculate_squared_distance(self, a, b):
        return (a.x-b.x)**2 + (a.y-b.y)**2

    def move_to_Hamburger(self):
        # fill here
        distance = self.calculate_squared_distance(self, Hamburger)
        if distance > (PIXEL_PER_METER * 10) ** 2:
            self.speed = 0
            return BehaviorTree.FAIL

