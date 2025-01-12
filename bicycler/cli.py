import argparse
import math
import warnings
from argparse import ArgumentTypeError
from pathlib import Path

from model.bicycle_controller import NoControlController, RollRateFeedbackController, RollFeedbackController
from model.bicycle_model import BicycleModel
from model.bicycle_state import BicycleState
from model.simulation import Simulation
from model.simulation_parameters import SimulationParameters
from model.simulation_result import SimulationResult
from visualization.visualize import visualize_animation


def setup_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description='Cycling for computer science. Numeric simulation of bicycle (self-)stability.')
    parser.add_argument('--verbose', '-v', action='store_true', help='Print debug information')

    # add a subparser for the visualize command
    subparsers = parser.add_subparsers(dest='command', required=True)
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
    simulate_parser.add_argument('--timestep', '-t', type=float,
                                 help='Timestep for the simulation in s', default=0.01)
    simulate_parser.add_argument('--stepcount', '-s', type=int,
                                    help='Number of steps for the simulation', default=500)
    simulate_parser.add_argument('--velocity', '-v', type=float,
                                    help='Velocity of the bicycle in m/s', default=5)
    simulate_parser.add_argument('--roll', '-r', type=float,
                                    help='Initial roll angle in degree', default=5)
    simulate_parser.add_argument('--steer', '-d', type=float,
                                    help='Initial steering angle in degree', default=-2)
    simulate_parser.add_argument('--controller', '-c', type=str,
                                    help='Controller to use for the simulation',
                                 choices=['none', 'roll', 'rollrate'], default='none')
    simulate_parser.add_argument('--model-parameters', metavar='PARAMETER=VALUE', type=str, nargs='+',
                                    help='Vary parameter values of the bicycle model. '
                                         'Give name and value pairs as NAME=VALE separated by spaces.'
                                         'Do not put spaces around the = sign.')

    return parser

def parse_model_parameters(specified_items: list[str]) -> BicycleModel:
    specified_parameters = {}
    if specified_items:
        for kv_pair in specified_items:
            if kv_pair.count('=') != 1:
                raise ArgumentTypeError(f'Invalid parameter specification: "{kv_pair}"". Use NAME=VALUE!')
            key, value = kv_pair.split('=')
            # now, check if the specified parameters are valid
            if key in BicycleModel.default_parameters:
                specified_parameters[key.strip()] = float(value)
            else:
                warnings.warn(f'Unknown parameter "{key}" with value {value} specified. Ignoring it.')

    # create the model with the default parameters
    return BicycleModel(**specified_parameters)


def visualize_from_file(input_file: Path, verbose = False):
    if verbose:
        print(f'Loading {input_file} for visualization')
    # load the input file
    animation = SimulationResult.load_from(input_file)
    visualize_animation(animation)


def simulate(simulation_parameters: SimulationParameters,verbose = False) -> SimulationResult:
    if verbose:
        print('Simulating bicycle model')
    # create a simulation
    simulation = Simulation(simulation_parameters)
    # run the simulation
    simulation.run()
    # get the results
    return simulation.get_result()

def simulate_to_file(simulation_parameters: SimulationParameters,
                     output_file: Path, verbose = False):
    if verbose:
        print(f'Simulating bicycle model and saving results to {output_file}')
    # check, that the output directory exists
    if not output_file.parent.exists():
        if verbose:
            print(f"Creating directory {output_file.parent.absolute()}")
        output_file.parent.mkdir(parents=True, exist_ok=True)

    simulate(simulation_parameters, verbose).save_to(output_file)

def cli_main():
    parser = setup_parser()

    # handle the arguments
    args = parser.parse_args()

    if args.command == 'visualize':
        visualize_from_file(args.input, args.verbose)

    if args.command == 'simulate':
        # first, parse the model parameters
        model = parse_model_parameters(args.model_parameters)
        # parse the initial state
        init_state = BicycleState(math.radians(args.roll), math.radians(args.steer), 0, 0, 0, 0)
        # instantiate the controller
        if args.controller == 'none':
            controller = NoControlController()
        elif args.controller == 'rollrate':
            controller = RollRateFeedbackController(50.0)
        elif args.controller == "roll":
            controller = RollFeedbackController(50.0)
        else:
            raise ValueError(f'Unknown controller {args.controller} specified')
        # create the simulation parameters
        simulation_parameters = SimulationParameters(init_state, model, args.velocity, controller, args.timestep, args.stepcount)

        if args.show:
            visualize_animation(simulate(simulation_parameters, args.verbose))
        else:
            simulate_to_file(simulation_parameters, args.output, args.verbose)


if __name__ == '__main__':
    cli_main()