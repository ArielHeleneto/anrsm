import typer

import configcli
import sourcecli

app=typer.Typer()
app.add_typer(configcli.app,name="config",help="Permanently sets program-related variables.")
app.add_typer(sourcecli.app,name="source",help="Commands on updating and downloading packages.")

@app.command("hullo")
def hullo():
    '''
    Print a hullo message.
    '''
    print("Hullo! This is Another RISC-V SDK Manager!")

if __name__ == "__main__":
    app()