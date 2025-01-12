import numpy as np

class BicycleModel:
    """
    Physical constants and matrices of the bicycle model.
    Code for computing the matrices is based on the matlab implementation:
        https://moorepants.github.io/eme134/scripts/compute_benchmark_bicycle_matrices.m
    """
    M: np.ndarray
    C1: np.ndarray
    K0: np.ndarray
    K2: np.ndarray
    non_default_values: dict[str, float]

    default_parameters = {
        'IBxx': 9.2,  # Rear frame and human body x moment of inertia (kg*m^2)
        'IBxz': 2.4,  # Rear frame and human body xz product of inertia (kg*m^2)
        'IByy': 11.0,  # Rear frame and human body y moment of inertia (kg*m^2)
        'IBzz': 2.8,  # Rear frame and human body z moment of inertia (kg*m^2)
        'IFxx': 0.1405,  # Front wheel radial moment of inertia (kg*m^2)
        'IFyy': 0.28,  # Front wheel spin moment of inertia (kg*m^2)
        'IHxx': 0.05892,  # Handlebar and fork x moment of inertia (kg*m^2)
        'IHxz': -0.00756,  # Handlebar and fork xz product of inertia (kg*m^2)
        'IHyy': 0.06,  # Handlebar and fork y moment of inertia (kg*m^2)
        'IHzz': 0.00708,  # Handlebar and fork z moment of inertia (kg*m^2)
        'IRxx': 0.0603,  # Rear wheel radial moment of inertia (kg*m^2)
        'IRyy': 0.12,  # Rear wheel spin moment of inertia (kg*m^2)
        'c': 0.08,  # Trail (m)
        'g': 9.81,  # Acceleration due to gravity (m/s^2)
        'lambda': np.pi / 10,  # Steer axis tilt (rad)
        'mB': 85.0,  # Mass of rear frame and human body (kg)
        'mF': 3.0,  # Mass of front wheel (kg)
        'mH': 4.0,  # Mass of handlebar and fork (kg)
        'mR': 2.0,  # Mass of rear wheel (kg)
        'rF': 0.35,  # Radius of front wheel (m)
        'rR': 0.3,  # Radius of rear wheel (m)
        'w': 1.02,  # Wheelbase (m)
        'xB': 0.3,  # Rear frame and human body mass center x coordinate (m)
        'xH': 0.9,  # Handlebar and fork mass center x coordinate (m)
        'zB': -0.9,  # Rear frame and human body mass center z coordinate (m)
        'zH': -0.7,  # Handlebar and fork mass center z coordinate (m)
    }

    def __init__(self, **parameters):
        # Update default values with provided parameters
        params = {**self.default_parameters, **parameters}

        # Compute non-default values
        self.non_default_values = {k: v for k, v in params.items() if v != self.default_parameters[k]}

        # Compute total mass and center of mass coordinates
        mT = params['mR'] + params['mB'] + params['mH'] + params['mF']
        xT = (params['xB'] * params['mB'] + params['xH'] * params['mH'] + params['w'] * params['mF']) / mT
        zT = (-params['rR'] * params['mR'] + params['zB'] * params['mB'] + params['zH'] * params['mH'] - params['rF'] * params['mF']) / mT

        # Compute moments of inertia
        ITxx = (params['IRxx'] + params['IBxx'] + params['IHxx'] + params['IFxx'] + params['mR'] * params['rR']**2 +
                params['mB'] * params['zB']**2 + params['mH'] * params['zH']**2 + params['mF'] * params['rF']**2)
        ITxz = (params['IBxz'] + params['IHxz'] - params['mB'] * params['xB'] * params['zB'] - params['mH'] * params['xH'] * params['zH'] +
                params['mF'] * params['w'] * params['rF'])
        params['IRzz'] = params['IRxx']
        params['IFzz'] = params['IFxx']
        ITzz = (params['IRzz'] + params['IBzz'] + params['IHzz'] + params['IFzz'] + params['mB'] * params['xB']**2 +
                params['mH'] * params['xH']**2 + params['mF'] * params['w']**2)

        # Compute auxiliary variables
        mA = params['mH'] + params['mF']
        xA = (params['xH'] * params['mH'] + params['w'] * params['mF']) / mA
        zA = (params['zH'] * params['mH'] - params['rF'] * params['mF']) / mA

        IAxx = (params['IHxx'] + params['IFxx'] + params['mH'] * (params['zH'] - zA)**2 + params['mF'] * (params['rF'] + zA)**2)
        IAxz = (params['IHxz'] - params['mH'] * (params['xH'] - xA) * (params['zH'] - zA) + params['mF'] * (params['w'] - xA) * (params['rF'] + zA))
        IAzz = (params['IHzz'] + params['IFzz'] + params['mH'] * (params['xH'] - xA)**2 + params['mF'] * (params['w'] - xA)**2)
        uA = (xA - params['w'] - params['c']) * np.cos(params['lambda']) - zA * np.sin(params['lambda'])
        IAll = (mA * uA**2 + IAxx * np.sin(params['lambda'])**2 + 2 * IAxz * np.sin(params['lambda']) * np.cos(params['lambda']) +
                IAzz * np.cos(params['lambda'])**2)
        IAlx = (-mA * uA * zA + IAxx * np.sin(params['lambda']) + IAxz * np.cos(params['lambda']))
        IAlz = (mA * uA * xA + IAxz * np.sin(params['lambda']) + IAzz * np.cos(params['lambda']))

        mu = params['c'] / params['w'] * np.cos(params['lambda'])

        SR = params['IRyy'] / params['rR']
        SF = params['IFyy'] / params['rF']
        ST = SR + SF
        SA = mA * uA + mu * mT * xT

        # Compute matrices
        Mpp = ITxx
        Mpd = IAlx + mu * ITxz
        Mdp = Mpd
        Mdd = IAll + 2 * mu * IAlz + mu**2 * ITzz
        self.M = np.array([[Mpp, Mpd], [Mdp, Mdd]])

        K0pp = mT * zT
        K0pd = -SA
        K0dp = K0pd
        K0dd = -SA * np.sin(params['lambda'])
        self.K0 = np.array([[K0pp, K0pd], [K0dp, K0dd]])

        K2pp = 0.0
        K2pd = (ST - mT * zT) / params['w'] * np.cos(params['lambda'])
        K2dp = 0.0
        K2dd = (SA + SF * np.sin(params['lambda'])) / params['w'] * np.cos(params['lambda'])
        self.K2 = np.array([[K2pp, K2pd], [K2dp, K2dd]])

        C1pp = 0.0
        C1pd = (mu * ST + SF * np.cos(params['lambda']) + ITxz / params['w'] * np.cos(params['lambda']) - mu * mT * zT)
        C1dp = -(mu * ST + SF * np.cos(params['lambda']))
        C1dd = (IAlz / params['w'] * np.cos(params['lambda']) + mu * (SA + ITzz / params['w'] * np.cos(params['lambda'])))
        self.C1 = np.array([[C1pp, C1pd], [C1dp, C1dd]])

    def is_default(self) -> bool:
        return len(self.non_default_values) == 0

    def get_non_default_values(self) -> dict[str, float]:
        return self.non_default_values

    def get_parameter(self, name: str) -> float:
        return self.non_default_values[name] if name in self.non_default_values else self.default_parameters[name]