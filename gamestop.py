from pico2d import *
import game_framework
import play_state
import time

running = True
frame = 0
x = 0

def enter():
    global gamestop
    gamestop = load_image('gamestop.png')
    pass

def exit():
    global gamestop
    del gamestop
    # fill here
    pass

def update():

    pass

def do(self):
    pass

def draw():
    gamestop = load_image('gamestop.png')
    clear_canvas()
    play_state.draw_world() #잘 실행하다가, Q키를 누르면 일시정지 창이 뜸. 하지만 배경은 없어짐으로 이를 해결하기 위한 코드

    #이거 왜 무한반복하지#
    print('일시정지')
    gamestop.draw(500, 300)
    update_canvas()


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN: #and event.key == SDLK_ESCAPE:
            # game_framework.change_state(logo_state)
            match event.key:
                case pico2d.SDLK_ESCAPE:
                    print('일시정지 끝남')
                    game_framework.pop_state()