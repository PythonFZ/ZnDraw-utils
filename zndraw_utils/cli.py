from enum import Enum

import typer
from zndraw import ZnDraw

app = typer.Typer()


class Methods(str, Enum):
    all = "all"
    md = "md"
    relax = "relax"
    smiles = "smiles"
    solvate = "solvate"



@app.command()
def zndraw_register(
    names: list[Methods] = typer.Argument(..., help="The name of the extension."),
    url: str = typer.Option(
        ..., help="The URL of the ZnDraw Instance.", envvar="ZNDRAW_UTILS_URL"
    ),
    token: str | None = typer.Option(
        None, help="The token.", envvar="ZNDRAW_UTILS_TOKEN"
    ),
    auth_token: str | None = typer.Option(
        None, help="The authentication token.", envvar="ZNDRAW_UTILS_AUTH_TOKEN"
    ),
    public: bool = typer.Option(True),
):
    from mace.calculators import mace_mp
    if names == ["all"]:
        names = [Methods.md, Methods.relax, Methods.smiles, Methods.solvate]

    calc = mace_mp()
    vis = ZnDraw(url=url, auth_token=auth_token, token=token)
    for name in set(names):
        if name == Methods.md:
            from zndraw_utils.md import MolecularDynamics

            vis.register(MolecularDynamics, run_kwargs={"calc": calc}, public=public)
            typer.echo("Registered MolecularDynamics extension")
        elif name == Methods.relax:
            from zndraw_utils.relax import StructureOptimization

            vis.register(
                StructureOptimization, run_kwargs={"calc": calc}, public=public
            )
            typer.echo("Registered StructureOptimization extension")
        elif name == Methods.smiles:
            from zndraw_utils.smiles import AddFromSMILES

            vis.register(AddFromSMILES, public=public)
            typer.echo("Registered AddFromSMILES extension")
        elif name == Methods.solvate:
            from zndraw_utils.solvate import Solvate

            vis.register(Solvate, public=public)
            typer.echo("Registered Solvate extension")

    vis.socket.wait()
