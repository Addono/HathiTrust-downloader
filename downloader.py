from tqdm import tqdm
import requests
import time
import argparse

parser = argparse.ArgumentParser(description='Book downloader from Hathitrust')

parser.add_argument('id', type=str, help="The ID of the book, e.g 'mdp.39015027794331'.")
parser.add_argument('pages', type=int, help="The amount of pages to be downloaded")
parser.add_argument('--name', dest='name', type=str, help="The start of the filename. Defaults to using the id")

args = parser.parse_args()

urls = ["https://babel.hathitrust.org/cgi/imgsrv/download/pdf?id=%s;orient=0;size=100;seq=%s;attachment=0" % (args.id, i) for i in range(1, args.pages)]

for index, url in tqdm(enumerate(urls), unit="pages", total=len(urls)):
    filename = "%s_p%s.pdf" % (args.name or args.id, str(index).zfill(6))

    while True:
        try:
            response = requests.get(url, stream=True)

            if response.ok:
                with open(filename, "wb") as handle:
                    for data in response.iter_content():
                        handle.write(data)

                break
        except Exception as e:
            print(e)

        time.sleep(1)
