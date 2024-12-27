import argparse
from pathlib import Path


def cli_main():
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
    visualize_parser.add_argument('--save', type=Path, help='Save the visualization to a file')