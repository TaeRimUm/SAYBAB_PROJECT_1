# import random
# import json
# import pickle
# import os

from pico2d import *
import game_framework
# import game_world
# import server

import play_state

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
            game_framework.change_state(play_state)
        # elif event.type == SDL_KEYDOWN and event.key == SDLK_l:
        #     load_saved_world()
        #     game_framework.change_state(play_state)

def update():
    pass

def draw():
    menu = load_image('menu.png')
    clear_canvas()
    menu.draw(get_canvas_width()//2, get_canvas_height()//2)
    update_canvas()
