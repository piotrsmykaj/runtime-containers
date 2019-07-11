import argparse
import yaml

parser = argparse.ArgumentParser(description='Runtime containers generator')
parser.add_argument('cmd', nargs='?', type=str, help='Command')
parser.add_argument('runtime',
                    nargs='?', type=str, help='Runtime')
parser.add_argument('--version', nargs='*', default='all',
                    type=str, help='Versions to compile')
parser.add_argument('--clean', dest='clean',
                    action='store_const', const=True, default=False)
args = parser.parse_args()
