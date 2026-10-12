import numpy as np
import sounddevice as sd

from logger import log

class AudioCapture:
    def __init__(self, device_name=None, samplerate=44100, blocksize=1024):
        self.device_name = device_name
        self.samplerate = samplerate
        self.blocksize = blocksize
        self.stream = None
        self.current_rms = 0.0

    def _resolve_device_index(self):
        if not self.device_name:
            return None
        try:
            devices = sd.query_devices()
        except Exception as e:
            log.exception(f"Falha ao consultar dispositivos: {e}")
            return None

        for i, dev in enumerate(devices):
            if dev.get("max_input_channels", 0) > 0 and dev["name"] == self.device_name:
                return i

        log.warning(f"Microfone '{self.device_name}' não encontrado. Usando default.")
        return None

    def _callback(self, indata, frames, time_info, status):
        if status:
            log.debug(f"Stream status: {status}")
        self.current_rms = float(np.sqrt(np.mean(indata ** 2)))

    def start(self):
        device_index = self._resolve_device_index()
        try:
            self.stream = sd.InputStream(
                device=device_index,
                channels=1,
                samplerate=self.samplerate,
                blocksize=self.blocksize,
                callback=self._callback,
            )
            self.stream.start()
            log.info(
                f"AudioCapture iniciado "
                f"(device={self.device_name or 'default'}, "
                f"sr={self.samplerate}, blocksize={self.blocksize})"
            )
        except Exception as e:
            log.exception(f"Falha ao abrir microfone: {e}")
            self.stream = None

    def stop(self):
        if self.stream is not None:
            try:
                self.stream.stop()
                self.stream.close()
                log.info("AudioCapture parado")
            except Exception as e:
                log.exception(f"Erro ao parar AudioCapture: {e}")
            finally:
                self.stream = None

    @property
    def is_running(self):
        return self.stream is not None