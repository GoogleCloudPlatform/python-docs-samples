"""The script has functions that adds arguments to the CLI parser"""

def add_simulation_arguments(parser):
    """Adds in 'parser' the arguments '--simulation' and '--no-simulation'"""
    parser.add_argument(
        '-S',
        '--simulation',
        help='Simulate the execution. Do not execute any command.',
        dest='dry_run',
        action='store_true')

    parser.add_argument(
        '-NS',
        '--no-simulation',
        help='Really execute. Execute everything.',
        dest='dry_run',
        action='store_false')
