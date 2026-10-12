import json
import os

from logger import log
from layer import Layer

LAYERS_FILE = "layers.json"

class LayersManager:
    def __init__(self, basePath):
        self.layers = []
        self.basePath = basePath
        self.layer_file_path = os.path.join(self.basePath, LAYERS_FILE)

    def get_layers_sorted(self):
        return sorted(self.layers, key=lambda l: l.z_index)

    def apply_scale_from_reference(self, bbox_size, reference_layer="body", user_scale=1.0):
        ref = self.get_layer(reference_layer)
        if ref is None or ref.texture is None:
            log.error(f"Layer de referência '{reference_layer}' ausente ou sem textura.")
            return

        ref_w, ref_h = ref.get_original_size()
        if ref_w == 0 or ref_h == 0:
            log.error(f"Layer '{reference_layer}' tem dimensão inválida.")
            return

        bbox_w, bbox_h = bbox_size
        bbox_scale = min(bbox_w / ref_w, bbox_h / ref_h)
        final_scale = bbox_scale * user_scale

        log.info(
            f"Escala base={bbox_scale:.3f} × user={user_scale:.3f} = {final_scale:.3f} "
            f"(referência: '{reference_layer}' {ref_w}x{ref_h})"
        )

        for layer in self.layers:
            layer.apply_scale(final_scale)

    def load_textures(self):
        for layer in self.layers:
            layer.load_texture()
        log.info(f"{len(self.layers)} texturas carregadas")

    def get_layers_by_names(self, names):
        return [l for l in self.layers if l.name in names]

    def get_layer(self, name: str):
        for a in self.layers:
            if a.name == name:
                return a
        return None

    def create_layer(self, name, path, z_index=0):
        if self.get_layer(name):
            log.warning(f"Layer '{name}' já existe. Ignorando criação.")
            return self.get_layer(name)

        new_layer = Layer(name, path, z_index=z_index)
        self.layers.append(new_layer)

    def save_layers(self):
        layers_obj = [a.get_obj() for a in self.layers]

        with open(self.layer_file_path, "w", encoding="utf-8") as f:
            json.dump(layers_obj, f, indent=2, ensure_ascii=False)

        log.info(f"Arquivo '{LAYERS_FILE}' salvo ({len(layers_obj)} layers)")

    def _create_default_layers(self, layer_path):
        self.layers = []
        body_path  = f"{layer_path}/body/default.png"
        eyes_path  = f"{layer_path}/eyes"
        mouth_path = f"{layer_path}/mouth"

        self.create_layer("body", body_path, z_index=0)

        for i, eye in enumerate(("open", "closed"), start=10):
            self.create_layer(f"eye_{eye}", f"{eyes_path}/{eye}.png", z_index=i)

        for i, mouth in enumerate(("closed", "open", "open_big"), start=20):
            self.create_layer(f"mouth_{mouth}", f"{mouth_path}/{mouth}.png", z_index=i)

    def load_layers(self):
        if not os.path.exists(self.layer_file_path):
            log.warning(f"Arquivo '{LAYERS_FILE}' não encontrado. Criando novo...")

            self.layers = []
            self._create_default_layers(self.basePath.replace("\\", "/"))
            self.save_layers()
            self.load_textures()
            return

        with open(self.layer_file_path, "r", encoding="utf-8") as file:
            content = file.read().strip()

        if not content:
            log.warning(f"Arquivo '{LAYERS_FILE}' vazio. Recriando...")

            self._create_default_layers(self.basePath.replace("\\", "/"))
            self.save_layers()
            self.load_textures()
            return

        try:
            layers_json = json.loads(content)
        except json.JSONDecodeError as e:
            log.error(f"JSON inválido em '{LAYERS_FILE}': {e}")
            raise

        self.layers = []

        log.info("Carregando Layers...")
        for obj in layers_json:
            new_layer = Layer(obj["name"], obj["path"])
            new_layer.set_offset(obj["x_offset"], obj["y_offset"])
            new_layer.active = obj.get("active", True)
            new_layer.z_index = obj.get("z_index", 0)
            new_layer.scale_modifier = obj.get("scale_modifier", 1.0)
            self.layers.append(new_layer)

        self.load_textures()