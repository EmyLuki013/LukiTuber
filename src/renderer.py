from logger import log

class Renderer:
    ZOOM_STEP = 1.1
    ZOOM_MIN  = 0.2
    ZOOM_MAX  = 4.0

    def __init__(self):
        self.avatar = None

    def set_avatar(self, avatar):
        self.avatar = avatar
        avatar.apply_bbox_scale()
        log.info(f"Avatar '{avatar.name}' definido no Renderer")

    def render(self, surface):
        if self.avatar is None:
            log.warning("Renderer sem avatar definido.")
            return
        self.avatar.draw(surface)

    def zoom_in(self, factor=None):
        self._apply_zoom(factor if factor is not None else self.ZOOM_STEP)

    def zoom_out(self, factor=None):
        f = factor if factor is not None else self.ZOOM_STEP
        self._apply_zoom(1 / f)

    def reset_zoom(self):
        if self.avatar is None:
            return
        if self.avatar.scale == 1.0:
            return
        self.avatar.scale = 1.0
        self.avatar.apply_bbox_scale()
        log.info("Zoom resetado para 1.0")

    def _apply_zoom(self, factor: float):
        if self.avatar is None:
            return

        new_scale = self.avatar.scale * factor
        new_scale = max(self.ZOOM_MIN, min(self.ZOOM_MAX, new_scale))

        if new_scale == self.avatar.scale:
            return

        self.avatar.scale = new_scale
        self.avatar.apply_bbox_scale()
        log.debug(f"Zoom: {new_scale:.3f}")