import typer
from zndraw import ZnDraw

app = typer.Typer()

@app.command()
def zndraw_register(
    name: str = typer.Argument(..., help="The name of the extension."),
    url: str = typer.Argument(..., help="The URL of the ZnDraw Instance."),
    auth_token: str = typer.Argument(..., help="The authentication token."),
    token: str = typer.Argument(..., help="The token."),
):
    if name == "md":
        from zndraw_utils.md import MolecularDynamics

        vis = ZnDraw(url=url, auth_token=auth_token, token=token)

        vis.register(MolecularDynamics)
        typer.echo("Registered MolecularDynamics extension")
        vis.socket.wait()
    else:
        typer.echo("Unknown extension")
        typer.Exit(code=1) 


