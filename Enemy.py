import random

import game_framework
import server
from pico2d import *
import game_world


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

        self.x, self.y, self.fall_speed = random.randint(50, 1600), 50, 0


    def draw(self):
        sx, sy = self.x - server.background.window_left, self.y - server.background.window_bottom
        self.font.draw(sx - 40, sy + 40, '(%d, %d)' % (self.x, self.y), (25, 25, 0))

        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
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