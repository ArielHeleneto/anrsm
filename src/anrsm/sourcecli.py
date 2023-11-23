import typer
from config.config import settings
from typing_extensions import Annotated
from typing import Optional
from rich.progress import track
import os
from source.source import find_source_id
from rich import print

app = typer.Typer()

@app.command("update")
def source_update(sourceurl: Annotated[Optional[str], typer.Argument(help="Set this item if you wish to use this source temporarily.")] = None):
    """
    Update the source file.
    """
    if sourceurl != None:
        settings.set("sourceurl",sourceurl)
    import requests
    resp=requests.get(settings["sourceurl"],stream=True)
    with open(os.path.join(settings["cargocache"],"source.json"),'wb') as file:
        for data in track(resp.iter_content(chunk_size=1024), description="Updating..."):
            file.write(data)
    print("Susscessfully update.")

@app.command("list")
def source_list():
    """
    List all package.
    """
    from rich.console import Console
    from rich.table import Table
    with open(os.path.join(settings["cargocache"],"source.json"),'r') as file:
        table = Table(title="Available Package")
        table.add_column("Uunique Code", justify="left", style="cyan")
        table.add_column("Source Type")
        table.add_column("Architecture", justify="left", style="green")
        import json
        info=json.load(file)        
        for data in track(info, description="Parsing..."):
            table.add_row(data["name"]+"@"+data["version"], ', '.join(data["tag"]), data["arch"])
        console = Console()
        console.print(table)

@app.command("info")
def source_info(code: Annotated[str, typer.Argument(help="the package name you want to look inside. Put @+version to see a specify version",metavar="Package Name")]):
    """
    Print the detailed information for package.
    """
    from rich import print
    id=find_source_id(code)
    if id==-1:
        print("[bold red]Error[/bold red]: No matches found. :boom:")
        raise typer.Exit()
    with open(os.path.join(settings["cargocache"],"source.json"),'r') as file:
        import json
        info=json.load(file)
        print(f"[green]Name[/green]: {info[id]["name"]}")
        print(f"[green]Version[/green]: {info[id]["version"]}")
        print(f"[green]Version Code[/green]: {info[id]["versioncode"]}")
        print(f"[green]Source Type[/green]: {', '.join(info[id]["tag"])}")
        print(f"[green]Description[/green]: {info[id]["desc"]}")
        print(f"[green]Origin[/green]: {info[id]["origin"]}")
        print(f"[green]Arch[/green]: {info[id]["arch"]}")

@app.command("cache")
def source_install(code: Annotated[str, typer.Argument(help="the package name you want to download. Put @+version to get a specify version",metavar="Package Name")]):
    """
    Download a package.
    """
    id=find_source_id(code)
    if id==-1:
        print("[bold red]Error[/bold red]: No matches found. :boom:")
        raise typer.Exit()
    # check if cached
    cached=False
    with open(os.path.join(settings["cargocache"],"source.json"),'r') as file:
        import json
        info=json.load(file)
        cached=False
        if os.path.exists(os.path.join(settings["cargocache"],"cache",info[id]["files"]["source"]["sha256"]+".zip")):
            import hashlib
            with open(os.path.join(settings["cargocache"],"cache",info[id]["files"]["source"]["sha256"]+".zip"), "rb") as f:
                sha256obj = hashlib.sha256()
                sha256obj.update(f.read())
                cached=(sha256obj.hexdigest().upper()==info[id]["files"]["source"]["sha256"])
        if not cached:
            import requests
            resp=requests.get(info[id]["files"]["source"]["url"],stream=True)
            with open(os.path.join(settings["cargocache"],"cache",info[id]["files"]["source"]["sha256"]+".zip"),'wb') as file:
                for data in track(resp.iter_content(chunk_size=1024), description="Downloading Source Zip..."):
                    file.write(data)
        cached=False
        if os.path.exists(os.path.join(settings["cargocache"],"cache",info[id]["files"]["manifest"]["sha256"]+".json")):
            import hashlib
            with open(os.path.join(settings["cargocache"],"cache",info[id]["files"]["manifest"]["sha256"]+".json"), "rb") as f:
                sha256obj = hashlib.sha256()
                sha256obj.update(f.read())
                cached=(sha256obj.hexdigest().upper()==info[id]["files"]["manifest"]["sha256"])
        if not cached:
            import requests
            resp=requests.get(info[id]["files"]["manifest"]["url"],stream=True)
            with open(os.path.join(settings["cargocache"],"cache",info[id]["files"]["manifest"]["sha256"]+".json"),'wb') as file:
                for data in track(resp.iter_content(chunk_size=1024), description="Downloading Manifest..."):
                    file.write(data)

@app.command("expand")
def source_expand(code: Annotated[str, typer.Argument(help="the package name you want to look inside. Put @+version to see a specify version",metavar="Package Name")],dest: Annotated[str, typer.Argument(help="the destination you want to put this package to.",metavar="Destination")],softlink: Annotated[bool,typer.Option(help="Build softlink")] = False):
    """
    Expand package.
    """
    id=find_source_id(code)
    if id==-1:
        print("[bold red]Error[/bold red]: No matches found. :boom:")
        raise typer.Exit()
    # check if cached
    with open(os.path.join(settings["cargocache"],"source.json"),'r') as file:
        import json
        info=json.load(file)
        cached=False
        if os.path.exists(os.path.join(settings["cargocache"],"cache",info[id]["files"]["source"]["sha256"]+".zip")):
            import hashlib
            with open(os.path.join(settings["cargocache"],"cache",info[id]["files"]["source"]["sha256"]+".zip"), "rb") as f:
                sha256obj = hashlib.sha256()
                sha256obj.update(f.read())
                cached=(sha256obj.hexdigest().upper()==info[id]["files"]["source"]["sha256"])
        if not cached:
            print("[bold red]Error[/bold red]: No Source Zip cache found. Please cache it first. :boom:")
        cached=False
        if os.path.exists(os.path.join(settings["cargocache"],"cache",info[id]["files"]["manifest"]["sha256"]+".json")):
            import hashlib
            with open(os.path.join(settings["cargocache"],"cache",info[id]["files"]["manifest"]["sha256"]+".json"), "rb") as f:
                sha256obj = hashlib.sha256()
                sha256obj.update(f.read())
                cached=(sha256obj.hexdigest().upper()==info[id]["files"]["manifest"]["sha256"])
        if not cached:
            print("[bold red]Error[/bold red]: No Manifest cache found. Please cache it first. :boom:")
        
        import zipfile
        with zipfile.ZipFile(os.path.join(settings["cargocache"],"cache",info[id]["files"]["source"]["sha256"]+".zip"), 'r') as file:
            file.extractall(dest)
        
        if softlink:
            with open(os.path.join(settings["cargocache"],"cache",info[id]["files"]["manifest"]["sha256"]+".json")) as mani:
                import json
                mmm=json.load(mani)
                for link in track(mmm["softlink"], description="Building softlink..."):
                    print(f"[green]Info:[/green]  {os.path.join(settings["softlink"],link["from"])} [grey]->[/grey] {os.path.join(dest,link["to"])}")
                    os.symlink(os.path.join(dest,link["to"]),os.path.join(settings["softlink"],link["from"]))

if __name__ == "__main__":
    app()