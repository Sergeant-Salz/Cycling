import argparse
import math
from pathlib import Path

from src.model.bicycle_state import BicycleState
from src.model.simulation import Simulation
from src.model.simulation_parameters import SimulationParameters
from src.model.simulation_result import SimulationResult
from src.visualization.visualize import visualize_animation


def setup_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description='Cycling for computer science. Numeric simulation of bicycle (self-)stability.')
    parser.add_argument('--verbose', '-v', action='store_true', help='Print debug information')

    # add a subparser for the visualize command
    subparsers = parser.add_subparsers(dest='command')
    visualize_parser = subparsers.add_parser('visualize', help='Visualize the bicycle model')
    visualize_parser.add_argument('--input', '-i',
                                  type=Path,
                                  help='Input file with bicycle parameters',
                                  required=True)

    # add a subparser for the simulate command
    simulate_parser = subparsers.add_parser('simulate', help='Simulate the bicycle model')
    simulate_parser.add_argument('--show',
                                 action='store_true',
                                 help='Show the visualization instead of writing to a file')
    simulate_parser.add_argument('--output', '-o',
                                 type=Path,
                                 help='Output file for simulation results',
                                 required=True)

    return parser


def visualize(sim_res: SimulationResult, verbose = False):
    visualize_animation(sim_res)

def visualize_from_file(input_file: Path, verbose = False):
    if verbose:
        print(f'Loading {input_file} for visualization')
    # load the input file
    animation = SimulationResult.load_from(input_file)
    visualize(animation, verbose)


def simulate(verbose = False) -> SimulationResult:
    if verbose:
        print('Simulating bicycle model')
    # create initial state
    initial_state = BicycleState(math.radians(5), math.radians(-2), 0, 0, 0, 0)
    # create default parameters
    parameters = SimulationParameters(initial_state=initial_state)
    # create a simulation
    simulation = Simulation(parameters)
    # run the simulation
    simulation.run()
    # get the results
    return simulation.get_result()

def simulate_to_file(output_file: Path, verbose = False):
    if verbose:
        print(f'Simulating bicycle model and saving results to {output_file}')
    # check, that the output directory exists
    if not output_file.parent.exists():
        if verbose:
            print(f"Creating directory {output_file.parent.absolute()}")
        output_file.parent.mkdir(parents=True, exist_ok=True)

    simulate(verbose).save_to(output_file)

def cli_main():
    parser = setup_parser()

    # handle the arguments
    args = parser.parse_args()

    if args.command == 'visualize':
        visualize_from_file(args.input, args.verbose)

    if args.command == 'simulate':
        if args.show:
            visualize(simulate(args.verbose), args.verbose)
        else:
            simulate_to_file(args.output, args.verbose)


if __name__ == '__main__':
    cli_main()