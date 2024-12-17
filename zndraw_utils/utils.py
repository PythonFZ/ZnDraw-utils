# import enum

import ase
import ase.optimize
# import numpy as np
# import rdkit2ase
# import tqdm
# from ase import units
# from ase.calculators.lj import LennardJones
from ase.calculators.singlepoint import SinglePointCalculator
# from ase.md.langevin import Langevin
# from mace.calculators import mace_mp
# from pydantic import Field
# from zndraw import Extension, ZnDraw
# from zndraw_utils.base import Models



def freeze_copy_atoms(ref: ase.Atoms) -> ase.Atoms:
    """Create a copy of the atoms object."""

    atoms = ase.Atoms(
        ref.get_atomic_numbers(),
        ref.get_positions(),
        pbc=ref.get_pbc(),
        cell=ref.get_cell(),
    )
    if ref.calc is not None:
        results = {}
        if "energy" in ref.calc.results:
            results["energy"] = ref.calc.results["energy"]
        if "forces" in ref.calc.results:
            results["forces"] = ref.calc.results["forces"]
        atoms.calc = SinglePointCalculator(atoms, **results)
    return atoms