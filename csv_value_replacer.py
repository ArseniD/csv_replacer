import csv
import shutil

from tempfile import NamedTemporaryFile
from argparse import ArgumentParser

TEMP_FILE = NamedTemporaryFile(mode='w', delete=False)
FIELDS = ['id', 'stock_total', 'hub_total', 'store_pool_total']


def load_data(filename):
    with open(filename, 'r') as csvfile, TEMP_FILE:
        # check headers
        has_header = csv.Sniffer().has_header(csvfile.read(1024))
        reader = csv.DictReader(csvfile, fieldnames=FIELDS)
        writer = csv.DictWriter(TEMP_FILE, fieldnames=FIELDS)
        writer.writeheader()  # write headers from FILEDS to the new file

        # skip the first line if a read file has headers
        if has_header:
            next(reader)

        # iterate through each row in read file and write data to the new file
        # after headers
        for row in reader:
            row = {'id': row['id'],
                   'stock_total': row['hub_total'],
                   'hub_total': row['hub_total'],
                   'store_pool_total': row['store_pool_total']}
            writer.writerow(row)
    shutil.move(TEMP_FILE.name, 'output_data.csv')


def create_parser():
    parser = ArgumentParser(description="""
    Change row 'stock_total' value equal to 'hub_total' based on CSV file.""")
    parser.add_argument('--path', '-p', required=True,
                        help="the path to the csv file")
    return parser


if __name__ == '__main__':
    args = create_parser().parse_args()

    try:
        if args.path:
            load_data(args.path)
    except IOError as error:
        print(error)
