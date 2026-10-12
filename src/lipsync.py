from logger import log

class LipsyncController:
    def __init__(self, audio_capture, states, config):
        """
        config: dict com chaves:
            threshold_open: float   - RMS pra abrir a boca
            threshold_big: float    - RMS pra abrir a boca grande
            threshold_close: float  - RMS pra fechar (histerese)
            smoothing: float        - 0.0 (sem) a 1.0 (muito suave)
        """
        self.audio = audio_capture
        self.states = states

        self.threshold_open = config.get("threshold_open", 0.02)
        self.threshold_big  = config.get("threshold_big",  0.08)
        self.threshold_close = config.get("threshold_close", self.threshold_open * 0.5)
        self.smoothing = config.get("smoothing", 0.4)

        self._smoothed_rms = 0.0
        self._current_state = "closed"

    def update(self):
        if not self.audio.is_running:
            return

        rms = self.audio.current_rms

        s = self.smoothing
        self._smoothed_rms = self._smoothed_rms * s + rms * (1 - s)
        r = self._smoothed_rms

        if self._current_state == "closed":
            if r >= self.threshold_big:
                new_state = "open_big"
            elif r >= self.threshold_open:
                new_state = "open"
            else:
                new_state = "closed"
        elif self._current_state == "open":
            if r >= self.threshold_big:
                new_state = "open_big"
            elif r < self.threshold_close:
                new_state = "closed"
            else:
                new_state = "open"
        else:  # open_big
            if r < self.threshold_close:
                new_state = "closed"
            elif r < self.threshold_open:
                new_state = "open"
            else:
                new_state = "open_big"

        if new_state != self._current_state:
            self._current_state = new_state
            self.states.set_mouth(new_state)