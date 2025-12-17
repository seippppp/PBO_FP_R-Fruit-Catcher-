class ScreenManager:
    def __init__(self, screen):
        self.screen = screen
        self.screens = {}
        self.current_screen = None
    
    def add_screen(self, name, screen_instance):
        self.screens[name] = screen_instance

    # UPDATE BAGIAN INI: Tambah **kwargs
    def set_screen(self, name, **kwargs):
        self.current_screen = self.screens[name]
        # Kirim data tambahan (seperti nomor level) ke fungsi on_enter
        if hasattr(self.current_screen, 'on_enter'):
            self.current_screen.on_enter(**kwargs)
            
    def handle_event_list(self, events):
        if self.current_screen:
            self.current_screen.handle_event_list(events)
            
    def update(self):
        if self.current_screen:
            self.current_screen.update()
            
    def draw(self):
        if self.current_screen:
            self.current_screen.draw()