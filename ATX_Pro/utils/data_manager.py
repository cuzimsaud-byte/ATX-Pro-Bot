import json
import os
from typing import Any, Dict

DATA_FILE = "data/data.json"

class DataManager:
    @staticmethod
    def load_data() -> Dict[str, Any]:
        if not os.path.exists(DATA_FILE):
            os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
            default_data = {
                "guilds": {},
                "streamers": {"twitch": [], "kick": []},
                "stream_status": {}
            }
            DataManager.save_data(default_data)
            return default_data
        
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {"guilds": {}, "streamers": {"twitch": [], "kick": []}, "stream_status": {}}

    @staticmethod
    def save_data(data: Dict[str, Any]):
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    @staticmethod
    def get_guild_config(guild_id: str) -> Dict[str, Any]:
        data = DataManager.load_data()
        return data["guilds"].get(guild_id, {"alert_channel": None, "admin_role": None})

    @staticmethod
    def update_guild_config(guild_id: str, key: str, value: Any):
        data = DataManager.load_data()
        if guild_id not in data["guilds"]:
            data["guilds"][guild_id] = {"alert_channel": None, "admin_role": None}
        data["guilds"][guild_id][key] = value
        DataManager.save_data(data)
