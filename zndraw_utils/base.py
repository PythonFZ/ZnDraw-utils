import enum


class Optimizer(str, enum.Enum):
    """Available optimizers for geometry optimization."""

    LBFGS = "LBFGS"
    FIRE = "FIRE"
    BFGS = "BFGS"


class Models(str, enum.Enum):
    """Available models for energy and force prediction."""

    MACE_MP_0 = "MACE-MP-0"
    LJ = "LJ"
    null = "null"
