import argparse
from pathlib import Path

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
    simulate_parser.add_argument('--output', '-o',
                                 type=Path,
                                 help='Output file for simulation results',
                                 required=True)

    return parser


def visualize(input_file: Path, verbose = False):
    if verbose:
        print(f'Loading {input_file} for visualization')
    # load the input file
    animation = SimulationResult.load_from(input_file)
    # visualize the animation
    visualize_animation(animation)


def cli_main():
    parser = setup_parser()

    # handle the arguments
    args = parser.parse_args()

    if args.command == 'visualize':
        visualize(args.input, args.verbose)

    if args.command == 'simulate':
        raise NotImplementedError('Simulation not implemented yet')