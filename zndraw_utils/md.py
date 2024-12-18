import tqdm
from ase import units
from ase.calculators.lj import LennardJones
from ase.md.langevin import Langevin
from pydantic import Field
from zndraw import Extension, ZnDraw

from zndraw_utils.base import Models
from zndraw_utils.utils import freeze_copy_atoms


class MolecularDynamics(Extension):
    """Run molecular dynamics in the NVT ensemble using Langevin dynamics."""

    model: Models = Models.MACE_MP_0
    # remote_model: str = Field(
    #     "",
    #     description="Access a model provided via ZnTrack, like `repo@rev:<node-name>`. The model must provide a `get_calculator()` method.",
    # )
    temperature: float = 300
    time_step: float = 0.5
    n_steps: int = 100
    friction: float = 0.002

    upload_interval: int = 10

    def run(self, vis: ZnDraw, calc, **kwargs):
        if self.model.value == "LJ":
            calc = LennardJones()
        if self.n_steps > 1000:
            raise ValueError("n_steps should be less than 1000")
        if len(vis) > vis.step + 1:
            del vis[vis.step + 1 :]
        atoms = vis.atoms
        if len(atoms) > 1000:
            raise ValueError("Number of atoms should be less than 1000")
        atoms.calc = calc
        dyn = Langevin(
            atoms,
            timestep=self.time_step * units.fs,
            temperature_K=self.temperature,
            friction=self.friction,
        )
        vis.bookmarks.update({vis.step: "Molecular dynamics"})
        atoms_cache = []

        for _ in tqdm.trange(self.n_steps):
            dyn.run(1)
            atoms_cache.append(freeze_copy_atoms(atoms))
            if len(atoms_cache) == self.upload_interval:
                vis.extend(atoms_cache)
                atoms_cache = []
        vis.extend(atoms_cache)
