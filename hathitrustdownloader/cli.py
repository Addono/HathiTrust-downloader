from tqdm import tqdm
import os
import requests
import time
import argparse
from urllib.parse import urlparse, parse_qs

def extract_id_from_url(url):
    """
    Extracts the ID parameter from a HathiTrust URL.

    Args:
        url (str): The complete URL containing the ID parameter.

    Returns:
        str: The extracted ID value or None if not found.
    """
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    return query_params.get('id', [None])[0]

def main():
    parser = argparse.ArgumentParser(description='Book downloader for HathiTrust')

    parser.add_argument('id', type=str, help="The ID of the book, e.g 'mdp.39015027794331' or a complete URL.")
    parser.add_argument('start_page', type=int, help="The page number of the first page to be downloaded.")
    parser.add_argument('end_page', type=int, help="The last number of the last page to be downloaded (inclusive).")
    parser.add_argument('--name', dest='name', type=str, help="The start of the filename. Defaults to using the id. This can also be used to change the path.")

    args = parser.parse_args()

    # Extract ID from URL if necessary
    book_id = extract_id_from_url(args.id) if args.id.startswith("http") else args.id

    # If --name is used to specify a path, extract the directory part
    if args.name:
        directory = os.path.dirname(args.name)
        if directory and not os.path.exists(directory):
            try:
                os.makedirs(directory)
                print(f"Directory '{directory}' created.")
            except Exception as e:
                print(f"Failed to create directory '{directory}': {e}")
                return

    page_numbers = [i for i in range(args.start_page - 1, args.end_page)]
    urls = ["https://babel.hathitrust.org/cgi/imgsrv/download/pdf?id=%s;orient=0;size=100;seq=%s;attachment=0" % (book_id, i + 1) for i in page_numbers]

    for page_number, url in tqdm(zip(page_numbers, urls), unit="pages", total=len(urls)):
        filename = "%s_p%s.pdf" % (args.name or book_id, str(page_number).zfill(6))

        while True:
            try:
                response = requests.get(url, stream=True)

                if response.status_code == 404:
                    print(f"Error: Page {page_number} for book with ID '{book_id}' not found.")
                    exit(1)
                elif response.status_code == 500:
                    print(f"Error: The server failed to serve page {page_number} for book '{book_id}', this could indicate that the book identifier is invalid.")
                    return
                elif response.ok:
                    with open(filename, "wb") as handle:
                        for data in response.iter_content():
                            handle.write(data)

                    break
            except KeyboardInterrupt:
                return
            except Exception as e:
                print(f"An error occurred: {e}. Retrying in 1 second. Press Ctrl+C to abort.")
                time.sleep(1)

if __name__ == "__main__":
    main()
