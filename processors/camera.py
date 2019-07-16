import esper

from components.position import PositionComponent
from queue import Queue

class CameraProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
        self.queue = Queue()
    
    def process(self):
        while not self.queue.empty():
            event = self.queue.get()

            _center_camera_on = event.get('center_camera_on')
            _update_camera = event.get('update_camera')

            if _center_camera_on:
                cx, cy = _center_camera_on
                self.snap_camera(cx, cy)
            elif _update_camera:
                dx, dy = _update_camera
                self.move_camera(dx, dy)
    
    def snap_camera(self, center_x, center_y):
        self.world.camera.x = center_x - self.world.camera.width // 2
        self.world.camera.y = center_y - self.world.camera.height // 2
        
    def move_camera(self, dx, dy):
        leash = self.world.camera.leash
        player_pos = self.world.component_for_entity(1, PositionComponent)
        player_x, player_y = player_pos.x, player_pos.y
        w, h = self.world.camera.width, self.world.camera.height
        x, y = self.world.camera.x, self.world.camera.y
        
        center_x, center_y = x + w // 2, y + h // 2

        if abs(center_x - player_x) >= leash:
            self.world.camera.x += dx
        if abs(center_y - player_y) >= leash:
            self.world.camera.y += dy
