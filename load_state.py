# import random
# import json
# import pickle
# import os

from pico2d import *
import game_framework
# import game_world
#
# import server

import play_state
#
# from saybar import Saybar
# from Enemy import Skul
# from Enemy2 import Skul2
# from Enemy3 import Skul3
# from Enemy4 import Skul4
#
# from background import FixedBackground
# from Hamburger import hamburger

menu = None

def enter():
    global menu
    menu = load_image('menu.png')
    hide_cursor()
    hide_lattice()


def exit():
    global menu
    del menu


def pause():
    pass


def resume():
    pass


def create_new_world():
    pass


def load_saved_world():
    # game_world.load()
    # for o in game_world.all_objects():
    #     if isinstance(o, Saybar):
    #         server.saybar = o
    #         break
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_n:
            create_new_world()
        #     game_framework.change_state(play_state)
        # elif event.type == SDL_KEYDOWN and event.key == SDLK_l:
        #     load_saved_world()
        #     game_framework.change_state(play_state)


def update():
    pass


def draw():
    clear_canvas()
    menu.draw(get_canvas_width() // 2, get_canvas_height() // 2)
    update_canvas()



    # server.saybar = Saybar()
    # game_world.add_object(server.saybar, 1)
    # game_world.add_collision_pairs(server.saybar, None, 'saybar:Enemy')
    # game_world.add_collision_pairs(server.saybar, None, 'saybar:Enemy2')
    # game_world.add_collision_pairs(server.saybar, None, 'saybar:Enemy3')
    # game_world.add_collision_pairs(server.saybar, None, 'saybar:Enemy4')
    # game_world.add_collision_pairs(server.saybar, None, 'saybar:Hamburger')
    #
    # background = FixedBackground()
    # game_world.add_object(background, 0)
    #
    # hamburgers = [hamburger() for i in range(50)]
    # game_world.add_objects(hamburgers, 1)
    # game_world.add_collision_pairs(None, hamburgers, 'Enemy:Hamburger')
    # game_world.add_collision_pairs(None, hamburgers, 'Enemy2:Hamburger')
    # game_world.add_collision_pairs(None, hamburgers, 'Enemy3:Hamburger')
    # game_world.add_collision_pairs(None, hamburgers, 'Enemy4:Hamburger')



    # # load json object data
    # with open('Enemy_data.json', 'r') as f:
    #     Enemy_data_list = json.load(f)
    #     Enemys = [Skul(o['name'], o['x'], o['y'], o['size']) for o in Enemy_data_list]
    #     Enemys2 = [Skul2(o['name'], o['x'], o['y'], o['size']) for o in Enemy_data_list]
    #     Enemys3 = [Skul3(o['name'], o['x'], o['y'], o['size']) for o in Enemy_data_list]
    #     Enemys4 = [Skul4(o['name'], o['x'], o['y'], o['size']) for o in Enemy_data_list]
    #     game_world.add_objects(Enemys, 1)
    #     game_world.add_collision_pairs(None, Enemys, 'saybar:Enemy')
    #     game_world.add_collision_pairs(None, Enemys2, 'saybar:Enemy2')
    #     game_world.add_collision_pairs(None, Enemys3, 'saybar:Enemy3')
    #     game_world.add_collision_pairs(None, Enemys4, 'saybar:Enemy4')
    #
    #     game_world.add_collision_pairs(Enemys, None, 'Enemy:Hamburger')
    #     game_world.add_collision_pairs(Enemys2, None, 'Enemy2:Hamburger')
    #     game_world.add_collision_pairs(Enemys3, None, 'Enemy3:Hamburger')
    #     game_world.add_collision_pairs(Enemys4, None, 'Enemy4:Hamburger')

