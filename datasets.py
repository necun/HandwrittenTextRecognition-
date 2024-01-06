import stow
import tarfile
from tqdm import tqdm
from urllib.request import urlopen
from io import BytesIO
from zipfile import ZipFile

def download_and_unzip(url, extract_to='Datasets', chunk_size=1024*1024):
    http_response = urlopen(url)

    data = b''
    iterations = http_response.length // chunk_size + 1
    for _ in tqdm(range(iterations)):
        data += http_response.read(chunk_size)

    zipfile = ZipFile(BytesIO(data))
    zipfile.extractall(path=extract_to)

dataset_path = stow.join('Datasets', 'IAM_Words')
if not stow.exists(dataset_path):
    download_and_unzip('https://git.io/J0fjL', extract_to='Datasets')

    file = tarfile.open(stow.join(dataset_path, "words.tgz"))
    file.extractall(stow.join(dataset_path, "words"))
    dataset, vocab, max_len = [], set(), 0

    # Preprocess the dataset by the specific IAM_Words dataset file structure
    words = open(stow.join(dataset_path, "words.txt"), "r").readlines()
    for line in tqdm(words):
        if line.startswith("#"):
            continue

        line_split = line.split(" ")
        if line_split[1] == "err":
            continue

        folder1 = line_split[0][:3]
        folder2 = line_split[0][:8]
        file_name = line_split[0] + ".png"
        label = line_split[-1].rstrip('\n')

        rel_path = stow.join(dataset_path, "words", folder1, folder2, file_name)
        if not stow.exists(rel_path):
            continue

        dataset.append([rel_path, label])
        vocab.update(list(label))
        max_len = max(max_len, len(label))
