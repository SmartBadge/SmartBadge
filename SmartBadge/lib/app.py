import lvgl as lv
import lib.screen.widgets as w
import lib.screen.icons as i
import lib.game.game as g
import time as t
import gc

NIGHT_THEME = lv.theme_night_init(210, lv.font_roboto_16)
DEFAULT_THEME = lv.theme_default_init(210, lv.font_roboto_16)
MATERIAL_THEME = lv.theme_material_init(210, lv.font_roboto_16)

DISP_SCALE = 4
SCR_Y = 32
SCR_X = 40


class App():

    def __init__(self, name, display, buttons, timer, **kwargs):
        gc.collect()
        self.disp = display
        self.buttons = buttons
        self.tim = timer
        # self.theme = th
        self.group = lv.group_create()
        # lv.theme_set_current(self.theme)
        self.scr = lv.obj()
        self.name = name
        self.items = {}
        self.item_ids = {}
        self.cont = w.Container(self.scr)
        self.set_buttons(kwargs.get("btn_left", lambda x: print("undefined left")),
                         kwargs.get("btn_right", lambda x: print(
                             "undefined right")),
                         kwargs.get("btn_up", lambda x: print("undefined up")),
                         kwargs.get("btn_down", lambda x: print(
                             "undefined down")),
                         kwargs.get("btn_a", lambda x: print("undefined a")),
                         kwargs.get("btn_b", lambda x: print("undefined b")),
                         kwargs.get("btn_x", lambda x: print("undefined x")),
                         kwargs.get("btn_y", lambda x: print("undefined y")),
                         )
        gc.collect()

    def set_title(self, title, font_size=None):
        self.items['title'] = w.Label(
            self.cont.lv_obj, title, font_size=font_size)

    def load_screen(self):
        lv.scr_load(self.scr)

    def add_item(self, name, item, selectable=False):
        self.items[name] = item
        self.item_ids[id(item.lv_obj)] = item
        if selectable:
            lv.group_add_obj(self.group, item.lv_obj)

    def get_cont(self):
        return self.cont

    def set_buttons(self, btn_left, btn_right, btn_up, btn_down, btn_a, btn_b, btn_x, btn_y):
        self.buttons.left.set_callback_edge(btn_left)
        self.buttons.right.set_callback_edge(btn_right)
        self.buttons.up.set_callback_edge(btn_up)
        self.buttons.down.set_callback_edge(btn_down)
        # self.buttons.a.set_callback_edge(btn_a)
        self.buttons.b.set_callback_edge(btn_b)
        # self.buttons.x.set_callback_edge(btn_x)
        self.buttons.y.set_callback_edge(btn_y)


class GameApp():
    
    def __init__(self, name, display, buttons, th=MATERIAL_THEME, debug=False, roll_over=False, border=False, kill=False, **kwargs):
        gc.collect()
        self.disp = display
        self.buttons = buttons
        self.theme = th
        # lv.theme_set_current(self.theme)
        self.scr = lv.obj()
        self.name = name
        self.game = g.Game(SCR_X, SCR_Y, debugger=debug)
        self.sprites = {}
        self.roll_over = roll_over
        self.border = border
        self.kill = kill
        self.set_buttons(kwargs.get("btn_left", lambda x: print("undefined left")),
                         kwargs.get("btn_right", lambda x: print(
                             "undefined right")),
                         kwargs.get("btn_up", lambda x: print("undefined up")),
                         kwargs.get("btn_down", lambda x: print(
                             "undefined down")),
                         kwargs.get("btn_a", lambda x: print("undefined a")),
                         kwargs.get("btn_b", lambda x: print("undefined b")),
                         kwargs.get("btn_x", lambda x: print("undefined x")),
                         kwargs.get("btn_y", lambda x: print("undefined y")),
                         )
        gc.collect()

    def load_screen(self):
        lv.scr_load(self.scr)

    def draw_screen(self):
        # 160 x 128 screen
        for x in range(self.game.x):
            for y in range(self.game.y):
                if self.game.present_at(x, y) != "ball":
                    w.Rectangle(self.scr, x*DISP_SCALE, y *
                                DISP_SCALE, (x*DISP_SCALE)+DISP_SCALE, (y*DISP_SCALE)+DISP_SCALE)

    def draw_initial_sprite(self, sprite):
        x = sprite.x
        y = sprite.y
        width = sprite.width
        height = sprite.height
        if sprite.type == "BALL":
            sprite.set_icon(
                i.Ball(self.scr, width*DISP_SCALE, height*DISP_SCALE, x*DISP_SCALE, y*DISP_SCALE))
        elif sprite.type == "PADDLE":
            sprite.set_icon(i.PongBoard(self.scr, width*DISP_SCALE,
                                        height*DISP_SCALE, x*DISP_SCALE, y*DISP_SCALE))
        elif sprite.type == "WALL":
            sprite.set_icon(i.Wall(self.scr, width, height, x, y))
        else:
            print("Undefined sprite type requested, defaulting to grid of squares")
            sprite.set_icon(i.Wall(self.scr, width, height, x, y))

    def _add_spr(self, spr, x, y):
        self.sprites[spr.name] = spr
        self.game.add_sprite(spr, x, y)
        self.draw_initial_sprite(spr)

    def add_sprite(self, name, x, y, width=1, height=1, typ=None):
        sprite = g.Sprite(name, width, height, typ)
        self._add_spr(sprite, x, y)
        return sprite

    def add_custom_sprite(self, sprite, x, y):
        self._add_spr(sprite, x, y)

    def move_sprite(self, sprite_id, dx, dy):
        spr = self.sprites[sprite_id]
        killed = self.game.move_sprite(
            spr, dx, dy, roll_over=self.roll_over, border=self.border, kill=self.kill)
        x = spr.x
        y = spr.y

        if killed:
            del self.sprites[sprite_id]
            return (spr.name, sprite_id)

        if spr.type != None:
            spr.icon.move(x*DISP_SCALE, y*DISP_SCALE)

    def sprite_wait(self, length_of_time):
        inital = t.time()
        x = False
        while not x:
            current = t.time()
            x = (current - inital) > length_of_time

    def _debug(self, string):
        self.game._debug(string)

    def set_buttons(self, btn_left, btn_right, btn_up, btn_down, btn_a, btn_b, btn_x, btn_y):
        self.buttons.left.set_callback_edge(btn_left)
        self.buttons.right.set_callback_edge(btn_right)
        self.buttons.up.set_callback_edge(btn_up)
        self.buttons.down.set_callback_edge(btn_down)
        # self.buttons.a.set_callback_edge(btn_a)
        self.buttons.b.set_callback_edge(btn_b)
        # self.buttons.x.set_callback_edge(btn_x)
        self.buttons.y.set_callback_edge(btn_y)

class ListApp():

    def __init__(self, display, buttons, th=MATERIAL_THEME, debug=False, **kwargs):
        self.disp = display
        self.buttons = buttons
        self.theme = th
        self.scr = lv.obj()
        self.cont = w.Container(self.scr)
        self.items = {}
        self.item_ids = {}



        self.set_buttons(kwargs.get("btn_left", lambda x: print("undefined left")),
                         kwargs.get("btn_right", lambda x: print(
                             "undefined right")),
                         kwargs.get("btn_up", lambda x: print("undefined up")),
                         kwargs.get("btn_down", lambda x: print(
                             "undefined down")),
                         kwargs.get("btn_a", lambda x: print("undefined a")),
                         kwargs.get("btn_b", lambda x: print("undefined b")),
                         kwargs.get("btn_x", lambda x: print("undefined x")),
                         kwargs.get("btn_y", lambda x: print("undefined y")),
                         )


    def create_list(self, x, y):
        list1 = lv.list(lv.scr_act())
        list1.set_size(x, y)
        list1.align(None, lv.ALIGN.CENTER, 0, 0)
        return list1

    def add_btn(self, list):
        return list.add_btn(lv.SYMBOL.FILE, "New")


    def get_cont(self):
        return self.cont

    def load_screen(self):
        lv.scr_load(self.scr)

    def set_buttons(self, btn_left, btn_right, btn_up, btn_down, btn_a, btn_b, btn_x, btn_y):
        self.buttons.left.set_callback_edge(btn_left)
        self.buttons.right.set_callback_edge(btn_right)
        self.buttons.up.set_callback_edge(btn_up)
        self.buttons.down.set_callback_edge(btn_down)
        # self.buttons.a.set_callback_edge(btn_a)
        self.buttons.b.set_callback_edge(btn_b)
        # self.buttons.x.set_callback_edge(btn_x)
        self.buttons.y.set_callback_edge(btn_y)

    def event_handler(obj, event):
        if event == lv.EVENT.CLICKED:
            print("Clicked: %s" % lv.list.get_btn_text(obj))

    def set_title(self, title, font_size=None):
        self.items['title'] = w.Label(
            self.cont.lv_obj, title, font_size=font_size)

    def add_item(self, name, item, selectable=False):
        self.items[name] = item
        self.item_ids[id(item.lv_obj)] = item
        if selectable:
            lv.group_add_obj(self.group, item.lv_obj)
