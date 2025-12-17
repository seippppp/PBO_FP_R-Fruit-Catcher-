class BaseScreen:
    def __init__(self, screen, manager):
        self.screen = screen
        self.manager = manager

    def on_enter(self):
        pass

    def handle_event_list(self, events):
        pass

    def update(self):
        pass

    def draw(self):
        pass