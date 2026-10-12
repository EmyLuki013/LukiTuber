from logger import log

class Renderer:
    ZOOM_STEP = 1.1
    ZOOM_MIN  = 0.2
    ZOOM_MAX  = 4.0

    def __init__(self):
        self.avatar = None
        self.is_dragging = False
        self.drag_offset = (0, 0)

    def set_avatar(self, avatar):
        self.avatar = avatar
        self.is_dragging = False
        avatar.apply_bbox_scale()
        log.info(f"Avatar '{avatar.name}' definido no Renderer")

    def render(self, surface):
        if self.avatar is None:
            log.warning("Renderer sem avatar definido.")
            return
        self.avatar.draw(surface)

    # ---------- Zoom ----------

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

    # ---------- Drag ----------

    def start_drag(self, mouse_pos):
        """Inicia o drag. Só faz efeito se o clique foi em cima do avatar."""
        if self.avatar is None:
            return

        bbox = self.avatar.get_bounding_rect()
        if bbox is None or not bbox.collidepoint(mouse_pos):
            return

        ax, ay = self.avatar.position
        mx, my = mouse_pos
        self.drag_offset = (mx - ax, my - ay)
        self.is_dragging = True
        log.debug(f"Drag iniciado (offset={self.drag_offset})")

    def update_drag(self, mouse_pos):
        if not self.is_dragging or self.avatar is None:
            return

        mx, my = mouse_pos
        ox, oy = self.drag_offset
        self.avatar.position = (mx - ox, my - oy)

    def end_drag(self):
        if not self.is_dragging:
            return
        self.is_dragging = False
        log.debug(f"Drag terminado (posição final={self.avatar.position})")