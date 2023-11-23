import typer
from config.config import settings
from typing_extensions import Annotated

app = typer.Typer()

@app.command("set")
def config_set(item: Annotated[str, typer.Argument(help="the variable you want to set")],value: Annotated[str, typer.Argument(help="the value you want to set")]):
    """
    Set a variable in the setting file.
    """
    from dynaconf.loaders.toml_loader import write
    write('settings.toml', {item: value}, merge=True)

@app.command("unset")
def config_unset(item: Annotated[str, typer.Argument(help="the variable you want to reset")]):
    """
    Reset a variable in the settings file.
    """
    from dynaconf.loaders.toml_loader import write
    write('settings.toml', {item: None}, merge=True)

@app.command("get")
def config_get(item: Annotated[str, typer.Argument(help="the variable you want to get")]):
    """
    get a variable in the current setting file.
    """
    print(f"{item} = {settings[item]}")

if __name__ == "__main__":
    app()