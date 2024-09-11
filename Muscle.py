from dataclasses import dataclass
import numpy as np

@dataclass
class Muscle:
    nMotorUnits: int = 120
    muscleLength: float = 39.3 #cm
    muscleVolume: float = 414 #cm3
    initMotorUnits: bool = True
    forceRange: float = 120 #unitless, stronges MU is 120*weakest
    fatigueRange: float = 180 #unitless, strongest MU fatigues 180*weakest
    contractionDurationRange: float = 3 #unitless, stronges motor unit takes 3*faster than weakest

    def __post_init__(self):
        self.muscleRadius = np.sqrt(self.muscleVolume / self.muscleLength / np.pi)

@dataclass
class MotorUnit:
    fatigueConstant: float = 1.0
    peakForce: float = 1.0
    crossSectionalArea: float = 1.0

@dataclass
class PulseTrain: