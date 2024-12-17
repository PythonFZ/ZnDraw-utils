from enum import Enum

import typer
from zndraw import ZnDraw

app = typer.Typer()


class Methods(str, Enum):
    md = "md"
    relax = "relax"


@app.command()
def zndraw_register(
    name: Methods = typer.Argument(..., help="The name of the extension."),
    url: str = typer.Argument(..., help="The URL of the ZnDraw Instance."),
    token: str | None = typer.Argument(None, help="The token."),
    auth_token: str | None = typer.Argument(None, help="The authentication token."),
    public: bool = typer.Argument(True),
):
    from mace.calculators import mace_mp

    calc = mace_mp()
    vis = ZnDraw(url=url, auth_token=auth_token, token=token)

    if name == Methods.md:
        from zndraw_utils.md import MolecularDynamics

        vis.register(MolecularDynamics, run_kwargs={"calc": calc}, public=public)
        typer.echo("Registered MolecularDynamics extension")
    elif name == Methods.relax:
        from zndraw_utils.relax import StructureOptimization

        vis.register(StructureOptimization, run_kwargs={"calc": calc}, public=public)
    else:
        typer.echo("Unknown extension")
        typer.Exit(code=1)

    vis.socket.wait()
