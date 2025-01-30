import ase
import numpy as np
import rdkit2ase
from pydantic import Field
from zndraw import Extension, ZnDraw

from zndraw_utils.utils import freeze_copy_atoms


class AddFromSMILES(Extension):
    """Place a molecule from a SMILES at all points."""

    SMILES: str = Field(..., description="SMILES string of the molecule to add")
    add: bool = Field(
        True,
        description="Add the molecule to the current scene.",
    )

    @classmethod
    def model_json_schema(cls):
        schema = super().model_json_schema()
        schema["properties"]["add"]["format"] = "checkbox"
        
        return schema

    def run(self, vis: ZnDraw, **kwargs) -> None:
        vis.log(f"Running {self.__class__.__name__}")
        molecule = rdkit2ase.smiles2atoms(self.SMILES)

        if self.add:
            scene = vis.atoms
        else:
            scene = ase.Atoms()

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
        vis.bookmarks.update({vis.step: "AddFromSMILES"})

