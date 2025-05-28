from tqdm import tqdm
import os
import requests
import time
import argparse
from urllib.parse import urlparse, parse_qs

DEFAULT_USER_AGENT='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'

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

    parser.add_argument('id', type=str, help="The ID of the book, e.g 'mdp.39015002388380' or a complete URL.")
    parser.add_argument('start_page', type=int, help="The page number of the first page to be downloaded.")
    parser.add_argument('end_page', type=int, help="The last number of the last page to be downloaded (inclusive).")
    parser.add_argument('--name', dest='name', type=str, help="The start of the filename. Defaults to using the id. This can also be used to change the path.")
    parser.add_argument('--user-agent', dest='user_agent', type=str, help="The User-Agent string to use for requests.")
    parser.add_argument('--max-retries', dest='max_retries', type=int, default=8, help="The maximum number of retries for retriable errors (e.g., 403 Forbidden) before skipping a page. Default is 8.")

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
        
        retries = 0
        # Use the max_retries from command line arguments
        backoff_factor = 1  # Initial backoff in seconds

        while True:
            try:
                user_agent = args.user_agent if args.user_agent else DEFAULT_USER_AGENT
                headers = {
                    'User-Agent': user_agent,
                }
                response = requests.get(url, stream=True, headers=headers)

                if response.status_code == 403:
                    if retries < args.max_retries:
                        wait_time = backoff_factor * (2 ** retries)
                        print(f"Warning: Access forbidden (403) for page {page_number}, book ID '{book_id}'. Retrying in {wait_time} seconds... (Attempt {retries + 1}/{args.max_retries})")
                        time.sleep(wait_time)
                        retries += 1
                        continue  # Retry the request
                    else:
                        print(f"Error: Access forbidden (403) for page {page_number}, book ID '{book_id}' after {args.max_retries} retries. Skipping this page.")
                        break # Break from the while True loop for this page
                elif response.status_code == 404:
                    print(f"Error: Page {page_number} for book with ID '{book_id}' not found.")
                    # We might want to decide if we exit or just skip this page. For now, let's keep exit.
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
