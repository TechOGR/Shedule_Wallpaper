import json
from os.path import join, exists

DEFAULT_CONFIG = {
    "blur": True,
    "trash": True,
    "music": False,
    "activeWeek": "A"
}


class AppConfig:

    def __init__(self, full_path):
        self.config_path = join(full_path, "data", "documents", "app_config.json")
        self._config = self._load()

    def _load(self):
        if exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    return {**DEFAULT_CONFIG, **json.load(f)}
            except Exception:
                pass
        return dict(DEFAULT_CONFIG)

    def _save(self):
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(self._config, f, indent=2)

    def get_all(self):
        return dict(self._config)

    def update(self, data: dict):
        for key in DEFAULT_CONFIG:
            if key in data:
                self._config[key] = data[key]
        self._save()
        return self._config
