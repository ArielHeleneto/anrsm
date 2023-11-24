import os
from anrsm.config.config import settings
from rich.progress import track
def find_source_id(code: str):
    # find the target
    x = code.split("@", 1)
    with open(os.path.join(settings["cargocache"],"source.json"),'r') as file:
        import json
        info=json.load(file)
        id=-1
        for data in range(0,len(info)):
            if info[data]["name"]==x[0] and len(x)==1 and info[data]["arch"]=="x86":
                if id==-1:
                    id=data
                elif info[data]["versioncode"]>info[id]["versioncode"]:
                    id=data
            elif info[data]["name"]==x[0] and len(x)==2 and info[data]["version"]==x[1] and info[data]["arch"]=="x86":
                id=data
                break
    return id