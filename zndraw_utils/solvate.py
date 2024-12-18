from zndraw import Extension, ZnDraw
import rdkit2ase
from pydantic import Field




class Solvate(Extension):
    """Solvate the current scene."""

    solvent: str = Field(..., description="Solvent to use (SMILES)")
    count: int = Field(
        10, ge=1, le=500, description="Number of solvent molecules to add"
    )
    density: float = Field(789, description="Density of the solvent")
    pbc: bool = Field(True, description="Whether to use periodic boundary conditions")
    tolerance: float = Field(2.0, description="Tolerance for the solvent")

    def run(self, vis: ZnDraw, **kwargs) -> None:
        scene = vis.atoms
        solvent = rdkit2ase.smiles2atoms(self.solvent)

        scene = rdkit2ase.pack(
            [[scene], [solvent]],
            [int(len(scene) > 0), self.count],
            density=self.density,
            pbc=self.pbc,
            tolerance=self.tolerance,
        )

        vis.append(scene)
        vis.bookmarks.update({vis.step: "Solvate"})
