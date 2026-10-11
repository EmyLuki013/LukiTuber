from logger import log

from logger import log


class Renderer:
    def __init__(self):
        self.avatar = None

    def set_avatar(self, avatar):
        self.avatar = avatar
        avatar.apply_bbox_scale()

    def render(self, surface):
        if self.avatar is None:
            log.warning("Renderer sem avatar definido.")
            return
        self.avatar.draw(surface)