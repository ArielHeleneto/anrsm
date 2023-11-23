import typer
from config.config import settings

app = typer.Typer()

@app.command("set")
def config_set(item: str,value: str):
    from dynaconf.loaders.toml_loader import write
    write('settings.toml', {item: value}, merge=True)

@app.command("unset")
def config_unset(item: str):
    from dynaconf.loaders.toml_loader import write
    write('settings.toml', {item: None}, merge=True)

@app.command("get")
def config_get(item: str):
    print(f"{item} = {settings[item]}")

if __name__ == "__main__":
    app()