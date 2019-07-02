import tcod
import tcod.event

class State(tcod.event.EventDispatch):
    def ev_quit(self, event):
        raise SystemExit()

    def ev_keydown(self, event):
        if event.sym == "k":
            self.ev_textinput(event)

    def ev_mousebuttondown(self, event):
        print(event)

    def ev_mousemotion(self, event):
        print(event)
    
    def ev_textinput(self, event):
        print(event)

tcod.console_set_custom_font('16x16-sb-ascii.png', tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_CP437)
console = tcod.console_init_root(40, 30, title='ECS Game', order='F', renderer=tcod.RENDERER_SDL2)

state = State()

while True:
    for event in tcod.event.wait():
        state.dispatch(event)