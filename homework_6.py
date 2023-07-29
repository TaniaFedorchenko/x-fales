import argparse
import re
import sys
from pathlib import Path
from shutil import copyfile

parser = argparse.ArgumentParser(description='Sorting folder')
parser.add_argument('--source', '-s', required=True, help = 'Source folder')
parser.add_argument('--output', '-o', default='dist', help = 'Source folder')
args = vars(parser.parse_args())
source = args.get('source')
output = args.get('output')

def read_folder(path: Path) -> None:
    for el in path.iterdir():
        if el.is_dir():
            read_folder(el)
        else:
            copy_file(el)


def copy_file(file: Path) -> None:
    ext = file.suffix
    new_path = output_folder / ext
    new_path.mkdir(exist_ok=True, parents=True)
    copyfile(file, new_path / file.name)


output_folder = Path(output)
read_folder(Path(source))

cyrillic_sumbols = 'абвгдеєжзиіїйклмнопрстуфцчшщьюя'
latinic_sumbols = ('a', 'b', 'v', 'g', 'd', 'e', 'e', 'j', 'z', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'r', 's', 't', 'u', 'f', 'h', 'ts', 'ch', 'sh', 'sch', '', 'yo', 'ya')

TRANS = {}
for a, b in zip(cyrillic_sumbols, latinic_sumbols):
    TRANS[ord(a)] = b
    TRANS[ord(a.upper)] = b.upper

def normalize(name: str) -> str:
    n_name = name.translate(TRANS)
    n_name = re.sub(r'\w', '_', n_name)
    return n_name




IMAGES = []
MUSIC = []
VIDEO = []
DOCUMENTS = []
ARCHIVES = []
MY_OTHERS = []

REGISTER_EXTENTIONS = {
    "JPEG":IMAGES,
    'PNG': IMAGES,
    'JPG': IMAGES,
    'SVG': IMAGES,
    'AVI': VIDEO,
    'MP4': VIDEO,
    'MOV': VIDEO,
    'MKV': VIDEO,
    'DOC': DOCUMENTS,
    'TXT': DOCUMENTS,
    'PDF': DOCUMENTS,
    'MP3': MUSIC,
    'WAV': MUSIC,
    'ARM': MUSIC,
    'ZIP': ARCHIVES,
    'GZ':  ARCHIVES,
    'TAR': ARCHIVES

}
FOLDERS = []
EXTENSION = set()
UNKNOWS = set()

def get_extention(filename: str) -> str:
    return Path(filename). suffix[1:]. upper()

def scan(folder: Path) -> None:
    for item in folder.iterdir():
        if item.is_dir():
            if item.name not in ('archives', 'images', 'audio', 'video', 'documents', 'MY_OTHERS'):
                FOLDERS.append(item)
                scan(item)
            continue

        ext = get_extention(item.name)
        fullname = folder / item.name 
        if not ext:
            MY_OTHERS.append(fullname)
        else:
            container = REGISTER_EXTENTIONS[ext]     # я не робила виклюючень , перевірити під час запуску 
            EXTENSION.add(ext)
            container.append(fullname)
    
if __name__ == "__main__":
    folder_to_scan = sys.argv[1]
    print(f'start in folder {folder_to_scan}')   
    scan(Path(folder_to_scan))
    print(f'Images:{IMAGES}')
    print(f'Audio: {MUSIC}')
    print(f'Video: {VIDEO}')
    print(f'Documents:{DOCUMENTS}')
    print(f'Archives: {ARCHIVES}')
    print(f'My_others: {MY_OTHERS}')

    print(FOLDERS[::-1])