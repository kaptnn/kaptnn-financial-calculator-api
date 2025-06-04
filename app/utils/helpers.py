import re

def make_safe_onedrive_folder_name(name: str) -> str:
    name = name.lower()
    name = re.sub(r'[^a-z0-9]+', '_', name)
    name = name.strip('_')

    return name
