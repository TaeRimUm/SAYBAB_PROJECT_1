import game_framework
import pico2d

import load_state

#pico2d.open_canvas(400, 300)
pico2d.open_canvas(1000, 600)
game_framework.run(load_state)
pico2d.close_canvas()