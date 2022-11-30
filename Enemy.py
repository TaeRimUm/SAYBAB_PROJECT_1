import random
import game_framework
import server
from pico2d import *
import game_world

from BehaviorTree import BehaviorTree, Selector, Sequence, Leaf


# Skul Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 40.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Skul Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

class Skul:
    frame = 0
    image = None



    def do(self):
        self.x = clamp(0, self.x, 1600)

    def __init__(self):
        print('Skul에 있는 메소드 실행(해골 소환)')
        self.font = load_font('ENCR10B.TTF', 16) # x, y가 이동한 위치 나타내는 글씨 크기
        if Skul.image == None:
            Skul.image = load_image('Enemy_Skul_1.png')

        self.x, self.y, self.fall_speed = random.randint(50, 1600), random.randint(50, 150), 0


    def draw(self):
        sx, sy = self.x - server.background.window_left, self.y - server.background.window_bottom
        self.font.draw(sx - 40, sy + 40, '(%d, %d)' % (self.x, self.y), (25, 25, 0))

        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        self.image.clip_draw(int(self.frame) * 100, 200, 100, 100, sx, sy)

        if math.cos(self.dir) < 0:
            if self.speed == 0:
                self.image.clip_draw(int(self.frame) * 100, 200, 100, 100, sx, sy)

        #draw_rectangle(*self.get_bb())  # pico2d 가 제공하는 사각형 그리는거
        #이건 야매 방법인데, sx랑 sy를 어케든 만지면 (충돌박스 + 해골이미지) 같이 움직이게 할 수 있는데,
        #시간은 없고, 유혹을 견디지 못하고... 야매로 해결해 버렸다.....
        # 방법은 그냥 충돌박스를 지워버리기. # 원래는 그냥 충돌박스도 같이 따라다니는데, 지워버림 ㅇㅇ #



    def update(self):
        self.x += self.fall_speed

    def get_bb(self): #박스의 왼쪽 좌표, 오른쪽 좌표 알려주기(4개의 값을 넘겨주기)
        return self.x - 20, self.y - 30, self.x + 20, self.y + 20

    def handle_collision(self, other, group):
        if group == 'Saybar:Skul': #볼 입장에서 소년이 부딪히면
            game_world.remove_object(self) #근데 이렇게 삭제해도 game_world에는 안없어짐. 여전히 충돌됨. 그 리스트에서도 삭제를 해 줘야 함.
            #나랑 부딪혔을 때 정보가 필요하니까 other도 넘겨줌.



    def find_random_location(self):
        # fill here
        self.target_ball = None
        shortest_distance = 1280 ** 2
        # find in-sight(5meters) and nearest ball
        for o in game_world.all_objects():
            if type(o) is Ball:
                ball = o
        distance = (ball.x - self.x) ** 2 + (ball.y - self.y) ** 2
        if distance < (PIXEL_PER_METER * 7) ** 2 and distance < shortest_distance:
            self.target_ball = ball
        shortest_distance = distance
        if self.target_ball is not None:
            self.tx, self.ty = self.target_ball.x, self.target_ball.y
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL
        pass



    def move_to(self, radius=0.5):
        distance = (self.tx - self.x) ** 2 + (self.ty - self.y) ** 2
        self.dir = math.atan2(self.ty - self.y, self.tx - self.x)
        if distance < (PIXEL_PER_METER * radius) ** 2:
            self.speed = 0
            return BehaviorTree.SUCCESS
        else:
            self.speed = RUN_SPEED_PPS
            return BehaviorTree.RUNNING

    def play_beep(self):
        winsound.Beep(440, 100)
        return BehaviorTree.SUCCESS

    def find_ball_location(self):
        # fill here
        self.target_ball = None
        shortest_distance = 1280 ** 2 #max를 찾기위한 방법(가장 긴 거리)
        # find in-sight(5meters) and nearest ball
        for o in game_world.all_objects(): #게임 월드에 있는 모든 오브젝트를 가져와서
            if type(o) is Ball:            #그게 볼인지 아닌지 파악. 볼만 찾아야 함.
                ball = o                   #그 볼에 대해서
                distance = (ball.x - self.x) ** 2 + (ball.y - self.y) ** 2 #볼과 좀비와 거리를 계산
                if distance < (PIXEL_PER_METER * 7) ** 2 and distance < shortest_distance:
                    #그 계산한 거리가 7M 이하이고, 동시에 distance < 최대 거리(가장 긴 거리): 이면
                    self.target_ball = ball #타겟에 발견됐으면 현재 볼로 해주기.
                    shortest_distance = distance
        if self.target_ball is not None: #이렇게 해서 가장 가까운걸 찾기! 그 볼이 찾아졌으면,
            self.tx, self.ty = self.target_ball.x, self.target_ball.y #타겟을 설정해서
            return BehaviorTree.SUCCESS #성공.
        else:
            return BehaviorTree.FAIL #만약 7m이네에 볼이 없으면 실패.

    def move_to_boy(self):
        # fill here
        distance = self.calculate_squared_distance(self, server.boy)
        if distance > (PIXEL_PER_METER * 10) ** 2:
            self.speed = 0
            return BehaviorTree.FAIL

        if self.hp > server.boy.hp:
            self.dir = math.atan2(server.boy.y - self.y, server.boy.x - self.x)
            if distance < (PIXEL_PER_METER * 0.5) ** 2:
                self.speed = 0
                return BehaviorTree.SUCCESS
            else:
                self.speed = RUN_SPEED_PPS
                return BehaviorTree.RUNNING
        else:
            self.speed = 0
            return BehaviorTree.FAIL

    def flee_from_boy(self):
        # fill here
        # move_to_node = Leaf('Move To', self.move_to)
        # self.bt = BehaviorTree(move_to_node)

        distance = self.calculate_squared_distance(self, server.boy)
        if distance > (PIXEL_PER_METER * 10) ** 2:
            self.speed = 0
            return BehaviorTree.FAIL

        if self.hp <= server.boy.hp:
            self.dir = math.atan2(self.y - server.boy.y, self.x - server.boy.x)
            self.speed = RUN_SPEED_PPS
            return BehaviorTree.RUNNING
        else:
            self.speed = 0
            return BehaviorTree.FAIL

    def build_behavior_tree(self):  # move_to_node를 생성, self.move_to 함수를 연결
        find_random_location_node = Leaf('Find Random Location', self.find_random_location)
        move_to_node = Leaf('Move To', self.move_to)
        play_beep_node = Leaf('Play Beep', self.play_beep)
        wander_sequence = Sequence('Wander', find_random_location_node, move_to_node, play_beep_node)
        find_ball_location_node = Leaf('Find Ball Location', self.find_ball_location)
        eat_ball_sequence = Sequence('Eat Ball', find_ball_location_node, move_to_node, play_beep_node)
        wander_or_eat_ball_selector = Selector('Wander & Eat Ball', eat_ball_sequence, wander_sequence)
        move_to_boy_node = Leaf('Move to Boy', self.move_to_boy)
        flee_from_boy_node = Leaf('Flee from Boy', self.flee_from_boy)
        chase_or_flee_selector = Selector('Chase or Flee Boy', move_to_boy_node, flee_from_boy_node)
        final_selector = Selector('Final', chase_or_flee_selector, wander_or_eat_ball_selector)
        self.bt = BehaviorTree(final_selector)
        # 좀비가 볼을 계속 먹으면서, 점수가 더 높으면 나를 따