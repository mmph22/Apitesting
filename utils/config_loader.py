import yaml
import os

def load_config(env="dev"):
    config_path = os.path.join("config", f"{env.lower()}.yml")
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found: {config_path}")
    with open(config_path, "r") as f:
        return yaml.safe_load(f)