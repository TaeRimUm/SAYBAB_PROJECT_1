import random
import time
import schedule
    #pip install schedule
import Hamburger
import game_framework
import server
from pico2d import *
import game_world
import winsound

from BehaviorTree import BehaviorTree, Selector, Sequence, Leaf
from Hamburger import hamburger


# Skul Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 10.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Skul Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 10

animation_names = ['Idle', 'Walk']

class Skul:
    frame = 0
    images = None
    font = None

    def load_images(self):
        if Skul.images == None:
            Skul.images = {}
            for name in animation_names:
                Skul.images[name] = [load_image("./Skul_1/" + name + " (%d)" % i + ".png") for i in range(1, 11)]

    # def do(self):
    #     self.x = clamp(0, self.x, 1600)

    def __init__(self, name='NONAME', x=0, y=0, size=1):
        print('Skul에 있는 메소드 실행(해골 소환)')
        self.name = name
        self.x, self.y = x * PIXEL_PER_METER, y * PIXEL_PER_METER
        self.size = size
        if Skul.font is None:
            Skul.font = load_font('ENCR10B.TTF', 16)
        self.load_images()
        self.dir = random.random() * 2 * math.pi  # random moving direction
        self.speed = 0
        self.timer = 1.0  # change direction every 1 sec when wandering
        self.frame = 0
        self.build_behavior_tree()

        self.hp = 0
        self.target_Hamburger = None

        self.font = load_font('ENCR10B.TTF', 16) # x, y가 이동한 위치 나타내는 글씨 크기
        self.x, self.y, self.fall_speed = random.randint(50, 100), random.randint(50, 600), 0

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
        self.x = clamp(50, self.x, get_canvas_width() + 600)
        self.y = clamp(50, self.y, get_canvas_height() - 50)

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

    def build_behavior_tree(self): #move_to_node를 생성, self.move_to 함수를 연결

        find_random_location_node = Leaf('Find Random Location', self.find_random_location)
        move_to_node = Leaf('Move To', self.move_to)
        wander_sequence = Sequence('Wander', find_random_location_node, move_to_node)
        find_Hamburger_location_node = Leaf('Find hamburger Location', self.find_Hamburger_location)
        eat_Hamburger_sequence = Sequence('Eat hamburger', find_Hamburger_location_node, move_to_node)
        self.bt = BehaviorTree(eat_Hamburger_sequence)


    def update(self):
        # print넣으면 계~속 반복됨.
        self.bt.run()
        self.calculate_current_position()


    def draw(self):
        #print넣으면 계~속 반복됨.
        sx, sy = self.x - server.background.window_left, self.y - server.background.window_bottom
        self.font.draw(sx - 40, sy + 40, '(%d, %d)' % (self.x, self.y), (25, 25, 0))


        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        # self.image.clip_draw(int(self.frame) * 100, 200, 100, 100, sx, sy)

        if math.cos(self.dir) < 0:
            if self.speed == 0:
                Skul.images['Idle'][int(self.frame)].composite_draw(0, 'h', sx, sy, 100, 100)
            else:
                Skul.images['Walk'][int(self.frame)].composite_draw(0, 'h', sx, sy, 100, 100)
        else:
            if self.speed == 0:
                Skul.images['Idle'][int(self.frame)].draw(sx, sy, 100, 100)
            else:
                Skul.images['Walk'][int(self.frame)].draw(sx, sy, 100, 100)


        #draw_rectangle(*self.get_bb())  # pico2d 가 제공하는 사각형 그리는거
        #이건 야매 방법인데, sx랑 sy를 어케든 만지면 (충돌박스 + 해골이미지) 같이 움직이게 할 수 있는데,
        #시간은 없고, 유혹을 견디지 못하고... 야매로 해결해 버렸다.....
        # 방법은 그냥 충돌박스를 지워버리기. # 원래는 그냥 충돌박스도 같이 따라다니는데, 지워버림 ㅇㅇ #


    def get_bb(self): #박스의 왼쪽 좌표, 오른쪽 좌표 알려주기(4개의 값을 넘겨주기)
        return self.x - 10, self.y - 10, self.x + 10, self.y + 10

    def handle_collision(self, other, group):
        if group == 'Saybar:Skul': #해골 입장에서 세이버가 부딪히면
            game_world.remove_object(self) #근데 이렇게 삭제해도 game_world에는 안없어짐. 여전히 충돌됨. 그 리스트에서도 삭제를 해 줘야 함.
            #나랑 부딪혔을 때 정보가 필요하니까 other도 넘겨줌.



    def find_Hamburger_location(self):
        # fill here
        self.target_Hamburger = None
        shortest_distance = 1280 ** 2 #max를 찾기위한 방법(가장 긴 거리)
        # find in-sight(5meters) and nearest Hamburger
        for o in game_world.all_objects(): #게임 월드에 있는 모든 오브젝트를 가져와서
            if type(o) is hamburger:            #그게 햄버거인지 아닌지 파악. 햄버거만 찾아야 함.
                Hamburger = o                   #그 햄버거에 대해서
                distance = (Hamburger.x - self.x) ** 2 + (Hamburger.y - self.y) ** 2 #햄버거와 해골의 거리를 계산
                if distance < (PIXEL_PER_METER * 100) ** 2 and distance <= shortest_distance:
                    #그 계산한 거리가 100M 이하이고, 동시에 distance < 최대 거리(가장 긴 거리): 이면
                    self.target_Hamburger = Hamburger #타겟에 발견됐으면 현재 햄버거로 해주기.
                    shortest_distance = distance
        if self.target_Hamburger is not None: #이렇게 해서 가장 가까운걸 찾기! 그 햄버거가 찾아졌으면,
            self.tx, self.ty = self.target_Hamburger.x, self.target_Hamburger.y #타겟을 설정해서
            return BehaviorTree.SUCCESS #성공.
        else:
            return BehaviorTree.FAIL #만약 100m이네에 볼이 없으면 실패.



    def calculate_squared_distance(self, a, b):
        return (a.x-b.x)**2 + (a.y-b.y)**2


    def move_to_Hamburger(self):
        # fill here
        distance = self.calculate_squared_distance(self, Hamburger)
        if distance > (PIXEL_PER_METER * 10) ** 2:
            self.speed = 0
            return BehaviorTree.FAIL

        if self.hp > Hamburger.hp:
            self.dir = math.atan2(Hamburger.y - self.y, Hamburger.x - self.x)
            if distance < (PIXEL_PER_METER * 0.5) ** 2:
                self.speed = 0
                return BehaviorTree.SUCCESS
            else:
                self.speed = RUN_SPEED_PPS
                return BehaviorTree.RUNNING
        else:
            self.speed = 0
            return BehaviorTree.FAIL

    # def flee_from_Hamburger(self):
    #     # fill here
    #     # move_to_node = Leaf('Move To', self.move_to)
    #     # self.bt = BehaviorTree(move_to_node)
    #
    #     distance = self.calculate_squared_distance(self, server.Hamburger)
    #     if distance > (PIXEL_PER_METER * 10) ** 2:
    #         self.speed = 0
    #         return BehaviorTree.FAIL
    #
    #     if self.hp <= server.Hamburger.hp:
    #         self.dir = math.atan2(self.y - hamburger.y, self.x - hamburger.x)
    #         self.speed = RUN_SPEED_PPS
    #         return BehaviorTree.RUNNING
    #     else:
    #         self.speed = 0
    #         return BehaviorTree.FAIL