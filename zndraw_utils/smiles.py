import numpy as np
import rdkit2ase
from pydantic import Field
from zndraw import Extension, ZnDraw

from zndraw_utils.utils import freeze_copy_atoms


class AddFromSMILES(Extension):
    """Place a molecule from a SMILES at all points."""

    SMILES: str = Field(..., description="SMILES string of the molecule to add")

    def run(self, vis: ZnDraw, **kwargs) -> None:
        molecule = rdkit2ase.smiles2atoms(self.SMILES)

        scene = vis.atoms

        points = vis.points
        if len(points) == 0:
            points = [np.array([0, 0, 0])]

        for point in points:
            molecule_copy = molecule.copy()
            molecule_copy.translate(point)
            scene.extend(molecule_copy)

        if hasattr(scene, "connectivity"):
            del scene.connectivity

        vis.append(freeze_copy_atoms(scene))
        vis.bookmarks = vis.bookmarks | {vis.step: "AddFromSMILES"}
