import sounddevice as sd
from logger import log

def list_input_devices():
    try:
        devices = sd.query_devices()
    except Exception as e:
        log.exception(f"Falha ao consultar dispositivos de áudio: {e}")
        return []

    inputs = []
    for i, dev in enumerate(devices):
        if dev.get("max_input_channels", 0) > 0:
            inputs.append({"index": i, "name": dev["name"]})
    return inputs

def find_device_by_name(name):
    if not name:
        return None
    for dev in list_input_devices():
        if dev["name"] == name:
            return dev["index"]
    return None