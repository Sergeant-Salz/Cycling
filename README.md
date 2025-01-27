# Cycling for Computer Scientists
Simulation of bicycle (self-)stability

## Introduction
In this project we examine the self-stability of a bicycle by numerically simulating the dynamics of a bicycle.
The math is based on the paper _"Linearized dynamics equations for the balance and steer of a bicycle: a benchmark and review"_ by J. P. Meijaard et al (2007). The paper is available [here](https://royalsocietypublishing.org/doi/full/10.1098/rspa.2007.1857).

Additionally, to simulating the bicycle on its own, we also model a rider controlling the bicycle via the steering angle to keep it upright.


## Usage
To use the project, create a virtual environment and install the required packages:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```


#### Run the simulation and store the results
```bash
python bicycler simulate --output FILENAME
```
For additional parameters like model parameters, simulation settings and rider control, see the help message:
```bash
python bicycler simulate --help
```

#### Play a simulation result
```bash
python bicycler visualize -i FILENAME
```

#### ... or simulate and immediately play the result
```bash
python bicycler simulate --show -o show
```
Add any parameters just like in the `simulate` command.

## Evaluation
The behavior of the simulation is evaluated by comparing the results to the analytical results presented in the paper. Below are the parameters used in the evaluation:
```bash
// inverted-prendulum-like fall
python bicycler simulate --show -o show -t 0.01 -s 1600 -v 4.

// low speed weave mode
python bicycler simulate --show -o show -t 0.01 -s 1600 -v 4.2

// riderless stable mode
python bicycler simulate --show -o show -t 0.005 -s 1500 -v 4.35

// capsize mode
python bicycler simulate --show -o show -t 0.01 -s 2000 -v 10
```

Furthermore we show that the rider control can stabilize the bicycle at otherwise installable speeds:
```bash
// stability at high speed with rider control
python bicycler simulate --show -o show -t 0.01 -s 500 -v 10 -c pid

// stability with high initial lean
python bicycler simulate --show -o show -t 0.005 -s 1000 -v 20 -c pid --roll 20
```
