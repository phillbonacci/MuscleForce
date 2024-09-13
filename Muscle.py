from dataclasses import dataclass
import numpy as np
import matplotlib.pyplot as plt

@dataclass
class Muscle:
    # Defaults defined based on anatomical measurements of the human gastric soleus
    n_motor_units: int = 120
    muscle_length: float = 39.3 #cm
    muscle_volume: float = 414.0 #cm3
    force_range: float = 120 #unitless, stronges motor unit (MU) peaks 120x weakest
    fatigue_range: float = 180 #unitless, strongest MU fatigue factor 180x weakest
    ct_range: float = 3 #contraction time range (unitless), strongest motor unit 3x faster than weakest
    ct_slowest: float = 90 #slowest MU contration time (ms, stimulation to peak force), estimates vary (90-145ms)
    fatigueFactor: float = 1.25e-4

    def __post_init__(self):
        self.muscleRadius = np.sqrt(self.muscle_volume / self.muscle_length / np.pi)
        self.initMotorPool()

    def initMotorPool(self):
        relative_unit = np.array([i/(self.n_motor_units-1) for i in range(self.n_motor_units)])
        self.force_scaling = np.exp(np.log(self.force_range) * relativeUnit)

        ctScaleFactor = np.log(self.force_range) / np.log(self.contraction_time_range)
        self.contraction_times = self.cTSlowest * np.power((1/self.force_scaling),(1/cTScaleFactor)) # contraction times of MUs (ms)
        
        self.fatigue_factors = self.fatigue_factor * np.exp(np.log(self.fatigue_range) * relative_unit)# tau fatigue in literatre

        '''
        TODO: Add diameter, estimated from cross sectional area, to nerve model. 
        
        The electrical properties of axons under stimulation vary with diameter.
        There is also a direct relationship between nerve diameter, and the size of the motor unit.
        These differences in electrical properties may be useful in 
        '''
        self.csas = np.power(self.force_scaling,0.4544) / np.sum(np.power(self.force_scaling,0.4544)) * 3.05e-2 # 
        
        self.arbor_lengths = np.power(self.force_scaling, 0.4938) / np.max(np.power(self.force_scaling, 0.4938))

    def plotForces(self, ax):
        ax.scatter(np.arange(self.nMotorUnits), self.force_scaling, s=8)
        ax.set_xlabel('Motor Unit')
        ax.set_ylimits(1,self.force_range)
        ax.set_ylabel('Relative Twitch Force')
        ax.set_title('Twitch Force vs Motor Unit')
            
    def histForces(self, ax):
        ax.hist(self.force_scaling, bins = np.arange(0,self.forceRange,10), density=True)
        ax.set_xlabel('Twitch Force')
        ax.set_ylabel('Proportion of MUs')
        ax.set_title('Motor Unit Force Distribution')

    def plotFatigues(self, ax):
        ax.scatter(self.force_scaling/self.nMotorUnits, self.fatigue_factors, s=8)
        ax.set_xlabel('Relative Twitch Force')
        ax.set_ylabel('Normalized Fatigue Factor')
        ax.set_title('Fatigue Factor vs Twitch Force')

    def plotCTs(self, ax):
        ax.scatter(self.force_scaling/self.nMotorUnits, self.contraction_times, s=8)
        ax.set_xlabel('Relative Twitch Force')
        ax.set_ylabel('Contraction Time (ms)')
        ax.set_title('Contraction Time vs Twitch Force')

    def plotMUProperties(self):
        fig, axs = plt.subplots(nrows=2,ncols=2,figsize=(9,7), layout='tight', dpi=1200)
        self.plotForces(axs.flat[0])
        axs.flat[0].text(0.05, 0.83, 'A', fontsize=18, fontweight='bold', transform=axs.flat[0].transAxes)
        self.histForces(axs.flat[1])
        axs.flat[1].text(0.9, 0.83, 'B', fontsize=18, fontweight='bold', transform=axs.flat[1].transAxes)
        self.plotFatigues(axs.flat[2])
        axs.flat[2].text(0.05, 0.83, 'C', fontsize=18, fontweight='bold', transform=axs.flat[2].transAxes)
        self.plotCTs(axs.flat[3])
        axs.flat[3].text(0.9, 0.83, 'D', fontsize=18, fontweight='bold', transform=axs.flat[3].transAxes)
        return fig, axs

@dataclass
class ForceModel:
    muscle: Muscle = Muscle()
    force_factor_rest: float = 5.1 #N
    duration: float = 100e3 #(ms) total simulation duration
    dt: float  = 0.1 #(ms) model time step
    track_values: bool = True
    t1: float = 43.8 #(ms) time constant of force decline in abence of actin linkage
    t2: float = 124.4 #(ms) time constant of force decline with strong actin linkages, (paralyzed 58-87ms, nonparalysed 124-1564ms)
    t_fat_center: float = 53.4e3 #(ms)Fatigue Rate 47.8s, 46.9s, 53.4s, 126s from lit
    tc_rest: float = 20
    km_rest: float = 0.3

    a_force = -8.8e-7
    a_t1 = 5.7e-6
    a_km = 1.9e-8

    def __post_init__(self):
        steps = np.floor(self.duration / self.dt)
        self.forces_applied = np.zeros([self.muscle.n_motor_units, steps])

        # initialize arrays to capture the tracked membrane coefficients
        if track_values:
            self.cn_tracked = np.zeros([self.muscle.n_motor_units, steps])
            self.a_tracked = np.zeros([self.muscle.n_motor_units, steps])
            self.a_tracked[:,0] += self.
            self.km_tracked = np.zeros([self.muscle.n_motor_units, steps])
            self.t1_tracked = np.zeros([self.muscle.n_motor_units, steps])
            self.r0_tracked = np.zeros([self.muscle.n_motor_units, steps])

    def step_model(self, units_stimulated):