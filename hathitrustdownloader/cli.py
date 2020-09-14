from tqdm import tqdm

import requests
import time
import argparse

def main():
    parser = argparse.ArgumentParser(description='Book downloader from Hathitrust')

    parser.add_argument('id', type=str, help="The ID of the book, e.g 'mdp.39015027794331'.")
    parser.add_argument('start_page', type=int, help="The page number of the first page to be downloaded.")
    parser.add_argument('end_page', type=int, help="The last number of the last page to be downloaded (inclusive).")
    parser.add_argument('--name', dest='name', type=str, help="The start of the filename. Defaults to using the id. This can also be used to change the path.")

    args = parser.parse_args()

    page_numbers = [i for i in range(args.start_page - 1, args.end_page)]
    urls = ["https://babel.hathitrust.org/cgi/imgsrv/download/pdf?id=%s;orient=0;size=100;seq=%s;attachment=0" % (args.id, i + 1) for i in page_numbers]

    for page_number, url in tqdm(zip(page_numbers, urls), unit="pages", total=len(urls)):
        filename = "%s_p%s.pdf" % (args.name or args.id, str(page_number).zfill(6))

        while True:
            try:
                response = requests.get(url, stream=True)

                if response.ok:
                    with open(filename, "wb") as handle:
                        for data in response.iter_content():
                            handle.write(data)

                    break
            except KeyboardInterrupt:
                return
            except:
                time.sleep(1)

if __name__ == "__main__":
    main()
