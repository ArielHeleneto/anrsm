import os
from anrsm.config.config import settings
from rich.progress import track
def find_source_id(name: str, ver: str=None, arch: str=None):
    if arch==None:
        import platform
        arch=platform.machine()
    with open(os.path.join(settings["cargocache"],"source.json"),'r') as file:
        import json
        info=json.load(file)
        id=-1
        for data in range(0,len(info)):
            if info[data]["name"]==name and info[data]["arch"]==arch:
                if ver==None:
                    if id==-1:
                        id=data
                    elif info[data]["versioncode"]>info[id]["versioncode"]:
                        id=data
                elif info[data]["version"]==ver:
                    id=data
                    break
    return id

def sourcache_check(id: int):
    with open(os.path.join(settings["cargocache"],"source.json"),'r') as file:
        import json
        info=json.load(file)
        if os.path.exists(os.path.join(settings["cargocache"],"cache",info[id]["files"]["source"]["sha256"])):
            import hashlib
            with open(os.path.join(settings["cargocache"],"cache",info[id]["files"]["source"]["sha256"]), "rb") as f:
                sha256obj = hashlib.sha256()
                sha256obj.update(f.read())
                return sha256obj.hexdigest()==info[id]["files"]["source"]["sha256"].lower()
        return False

def metacache_check(id: int):
    with open(os.path.join(settings["cargocache"],"source.json"),'r') as file:
        import json
        info=json.load(file)
        if os.path.exists(os.path.join(settings["cargocache"],"cache",info[id]["files"]["manifest"]["sha256"])):
            import hashlib
            with open(os.path.join(settings["cargocache"],"cache",info[id]["files"]["manifest"]["sha256"]), "rb") as f:
                sha256obj = hashlib.sha256()
                sha256obj.update(f.read())
                return sha256obj.hexdigest()==info[id]["files"]["manifest"]["sha256"].lower()
        return False