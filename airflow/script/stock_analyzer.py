import pandas as pd
import os
import argparse
from datetime import date


today = date.today()
file_path = f'/usr/local/airflow/tmp/data/{today}'
print(file_path)


def parse_args():
    parser = argparse.ArgumentParser(
        prog="stock price download")
    parser.add_argument('-s', '--symbol', type=str,
                        help='the symbol to download')
    return parser.parse_args()


def read_data(ticker):
    file_name = f'{ticker}.csv'
    file = os.path.join(file_path, file_name)
    df = pd.read_csv(file)
    print(df.head())


def main():
    args = parse_args()
    symbol = args.symbol
    read_data(symbol)


if __name__ == '__main__':
    main()
