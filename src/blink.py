import random

from logger import log

class BlinkController:
    def __init__(self, states, config=None):
        """
        config (opcional) com chaves:
            min_interval: float   - segundos mínimos entre blinks
            max_interval: float   - segundos máximos entre blinks
            duration: float       - duração do blink (olhos fechados)
        """
        self.states = states

        config = config or {}
        self.min_interval = config.get("min_interval", 2.0)
        self.max_interval = config.get("max_interval", 6.0)
        self.duration     = config.get("duration", 0.12)

        self._timer = self._next_interval()
        self._is_closed = False
        self._closed_for = 0.0

        self.states.set_eyes("open")

    def _next_interval(self) -> float:
        return random.uniform(self.min_interval, self.max_interval)

    def update(self, dt: float):
        if self._is_closed:
            self._closed_for += dt
            if self._closed_for >= self.duration:
                self._is_closed = False
                self._closed_for = 0.0
                self._timer = self._next_interval()
                self.states.set_eyes("open")
        else:
            self._timer -= dt
            if self._timer <= 0:
                self._is_closed = True
                self._closed_for = 0.0
                self.states.set_eyes("closed")
                log.debug("Blink")