import typer

import configcli
import sourcecli

app=typer.Typer()
app.add_typer(configcli.app,name="config")
app.add_typer(sourcecli.app,name="source")

@app.command("hullo")
def hullo():
    '''
    Print a hullo message and some position of config files.
    '''
    print("Hullo! This is Another RISC-V SDK Manager!")

if __name__ == "__main__":
    app()