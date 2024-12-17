import ase.optimize
from ase.calculators.lj import LennardJones
from zndraw import Extension, ZnDraw

from zndraw_utils.base import Models, Optimizer
from zndraw_utils.utils import freeze_copy_atoms


class StructureOptimization(Extension):
    """Run geometry optimization"""

    model: Models = Models.MACE_MP_0

    optimizer: Optimizer = Optimizer.LBFGS
    fmax: float = 0.05

    upload_interval: int = 10

    def run(self, vis: ZnDraw, calc, **kwargs) -> None:
        if self.model.value == "LJ":
            calc = LennardJones()
        optimizer = getattr(ase.optimize, self.optimizer.value)
        atoms = vis.atoms
        if len(atoms) > 1000:
            raise ValueError("Number of atoms should be less than 1000")
        atoms.calc = calc
        dyn = optimizer(atoms)
        vis.bookmarks.update({vis.step: "Geometric optimization"})

        atoms_cache = []

        for idx, _ in enumerate(dyn.irun(fmax=self.fmax)):
            atoms_cache.append(freeze_copy_atoms(atoms))
            if len(atoms_cache) == self.upload_interval:
                vis.extend(atoms_cache)
                atoms_cache = []
            if idx > 100:  # max 100 steps
                break
        vis.extend(atoms_cache)
