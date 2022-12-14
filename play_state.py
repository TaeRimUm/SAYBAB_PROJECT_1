from pico2d import *

import game_framework
import game_world

import server
import gamestop
from saybar import Saybar

from Enemy import Skul
from Enemy2 import Skul2
from Enemy3 import Skul3
from Enemy4 import Skul4

from Hamburger import hamburger
from background import FixedBackground as Background


def enter():

    global Hamburger
    server.Hamburger = hamburger()
    Hamburger = [hamburger() for i in range(100)]
    game_world.add_objects(Hamburger, 2)

    global saybar
    server.saybar = Saybar()
    game_world.add_object(server.saybar, 3)

    server.background = Background()
    game_world.add_object(server.background, 0)

    global Enemy
    server.Enemy = Skul()
    Enemy = [Skul() for i in range(50)]
    game_world.add_objects(Enemy, 1)

    global Enemy2
    server.Enemy2 = Skul2()
    Enemy2 = [Skul2() for i in range(50)]
    game_world.add_objects(Enemy2, 1)

    global Enemy3
    server.Enemy3 = Skul3()
    Enemy3 = [Skul3() for i in range(50)]
    game_world.add_objects(Enemy3, 1)

    global Enemy4
    server.Enemy4 = Skul4()
    Enemy4 = [Skul4() for i in range(50)]
    game_world.add_objects(Enemy4, 1)

    # 충돌 대상 정보 등록
    game_world.add_collision_pairs(server.saybar, Enemy, 'Saybar:Skul')
    game_world.add_collision_pairs(server.saybar, Enemy2, 'Saybar:Skul2')
    game_world.add_collision_pairs(server.saybar, Enemy3, 'Saybar:Skul3')
    game_world.add_collision_pairs(server.saybar, Enemy4, 'Saybar:Skul4')
    # 'Saybar:Skul' 이란 그룹의 이름으로 Saybar와 Skul의 충돌하겠다라는걸 저장함.
    game_world.add_collision_pairs(Hamburger, Enemy, 'hamburger:Skul')
    game_world.add_collision_pairs(Hamburger, Enemy2, 'hamburger:Skul2')
    game_world.add_collision_pairs(Hamburger, Enemy3, 'hamburger:Skul3')
    game_world.add_collision_pairs(Hamburger, Enemy4, 'hamburger:Skul4')



def exit():
    game_world.clear()

def pause():
    pass


def resume():
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
                game_framework.quit()
        else:
            server.saybar.handle_event(event)

        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_q):
            game_framework.push_state(gamestop)




def collide(a, b):
    # fill here
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True


def update():
    for game_object in game_world.all_objects():
        game_object.update()

    for a, b, group in game_world.all_collision_pairs():
        if collide(a, b):
            print('충돌', group)
            a.handle_collision(b, group)
            b.handle_collision(a, group)

def draw_world():
    for game_object in game_world.all_objects():
        game_object.draw()


def draw():
    clear_canvas()
    draw_world()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()






