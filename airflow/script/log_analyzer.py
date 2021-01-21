
from pathlib import Path
import re
import argparse


def analyze_log(files):
    error_list = []
    c = 0
    for file in files:
        with open(file, 'r') as f:
            content = f.readlines()
        for line in content:
            if '} ERROR -' in line:
                error_list.append(line.rstrip('\n'))
                c += 1
    return error_list, c


def parse_args():
    parser = argparse.ArgumentParser(
        prog="logs to parse")
    parser.add_argument('-p', '--log_path', type=str,
                        help='path to the logs')
    parser.add_argument('-v', '--verbosity', type=int,
                        help='1 to stdout errors, 0 otherwise')
    return parser.parse_args()


def output(counter, errors, verbose):
    print(f'Total number of errors: {counter}')
    if verbose == 1:
        print('\nHere are all the errors:')
        for error in errors:
            print(error)
    else:
        print('Quiet mode turned on')


def main():
    args = parse_args()
    log_dir = args.log_path
    verbose = args.verbosity
    file_list = list(Path(log_dir).rglob('*.log'))
    errors, counter = analyze_log(file_list)
    output(counter, errors, verbose)


if __name__ == "__main__":
    main()
