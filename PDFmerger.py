print('Loading')
from PyPDF2 import PdfFileMerger
from pathlib import Path
import csv

print('Loaded Library')
print()


def get_file_names(input_path):
    input_path = (Path(input_path)).resolve()
    cwd_files = [e.name for e in input_path.resolve().iterdir()]
    for e in sorted(cwd_files, reverse=True):
        if Path(e).suffix == '.pdf':
            print(e)
    print()


def get_specific_page(input_path, pathIP, page):
    folder_chk = 'CHK'
    fileOP = (input_path / folder_chk).resolve()
    fileOP.mkdir(exist_ok=True)
    merger = PdfFileMerger()
    merger.append(str(Path(input_path / pathIP).resolve()), pages=(page - 1, page))

    page_name = str(page) + '.pdf'
    with open(fileOP / page_name, 'wb') as file:
        merger.write(file)


# @getos
def main(input_path):
    folder_out = 'OUT'
    param_file = '*definition.csv'

    input_path = (Path(input_path)).resolve()
    param_path = [*input_path.glob(param_file)][0].resolve()

    with open(param_path) as csvfile:
        csv_data = csv.DictReader(csvfile, delimiter=',')
        csv_data = [*csv_data]

    file_names = [e["file"] for e in csv_data]
    cwd_files = [e.name for e in input_path.resolve().iterdir()]

    # Find the file that is not in the definition file, ie the input file
    pathIP = [e for e in cwd_files if e not in file_names and Path(e).suffix == '.pdf'][0]
    fileIP = input_path / pathIP

    fileOP = (input_path / folder_out).resolve()
    fileOP.mkdir(exist_ok=True)

    merger = PdfFileMerger()
    merger.append(str(Path(fileIP).resolve()))

    for e in csv_data:
        print(e)
        try:
            specific_pages = (int(e['start']), int(e['end']))
            print(specific_pages)
        except ValueError:
            specific_pages = None

        get_specific_page(input_path, pathIP, int(e['pos']))
        file_path = (input_path / e['file']).resolve().absolute()
        merger.merge(int(e['pos']), str(file_path), pages=specific_pages)
        print()

    with open(fileOP / fileIP.name, 'wb') as file:
        merger.write(file)


print('Loaded Function')

if __name__ == '__main__':
    input_path = input('Provide path to input directory:')
    input_bool = input('Yes for running merger? No for getting file names (Y/N):')
    if input_bool.lower() in ['y', 'yes', 'true']:
        main(input_path)
    else:
        get_file_names(input_path)
    print('Finished')
