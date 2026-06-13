# HathiTrust Downloader
[![PyPI](https://img.shields.io/pypi/v/hathitrust-downloader?style=flat-square&logo=pypi)][pypi]
[![PyPI - Downloads](https://img.shields.io/pypi/dm/hathitrust-downloader?logo=pypi&style=flat-square)][pypi]
[![GitHub version](https://img.shields.io/github/release/Addono/HathiTrust-downloader.svg?style=flat-square&logo=github)][github-releases]
[![GitHub download](https://img.shields.io/github/downloads/Addono/HathiTrust-downloader/total.svg?style=flat-square&logo=github)][github-releases]
[![GitHub stars](https://img.shields.io/github/stars/Addono/HathiTrust-downloader?style=flat-square)](https://github.com/Addono/HathiTrust-downloader/stargazers)
[![License](https://img.shields.io/github/license/Addono/HathiTrust-downloader.svg?style=flat-square)](LICENSE)
[![CI](https://img.shields.io/github/actions/workflow/status/Addono/HathiTrust-downloader/ci.yaml?event=push&style=flat-square)][ci-badge]

## Installing

### Python 3 (OS Agnostic)

Check that you have Python 3 installed and available on your shell. The following command should return something like `Python 3.12.5`, any version from Python 3.11 and above is supported. 

```bash
python -V
```

> Windows users: Make sure to enable the "Add to PATH" option when installing Python.

Now you can install using `pip` with the following command.

```bash
pip install hathitrust-downloader
```

Which allows you to interact with the downloader from the command line:

```bash
hathitrust-downloader --help
```

### Windows Executable

There are also Windows executables available, which come with all required software. This means you do not need to install anything separately.

Download the `downloader_<version>_win.zip` from [releases](https://github.com/Addono/HathiTrust-downloader/releases/) and extract it. Then open a shell, e.g. `cmd` or `powershell`, to the directory where the ZIP is extracted.

> [!TIP]
>
> The easiest way to open a shell in a specific folder is by first opening the folder in Explorer, then right click while holding shift, now select the option "Open PowerShell Window Here".
>

Now you can use the tool by typing commands into the shell like this, and then pressing enter:

```powershell
.\downloader.exe --help 
```

## Usage

The help should give some instructions on how to use the tool:

usage: hathitrust-downloader [-h] [--name NAME] [--user-agent USER_AGENT]
                             [--max-retries MAX_RETRIES] [--cookies COOKIE_JAR]
                             [--cert CERT_FILE] [--key KEY_FILE]
                             id start_page end_page

Book downloader for HathiTrust

positional arguments:
  id                    The ID of the book, e.g 'mdp.39015002388380' or a complete URL.
  start_page            The page number of the first page to be downloaded.
  end_page              The last number of the last page to be downloaded (inclusive).

options:
  -h, --help            show this help message and exit
  --name NAME           The start of the filename. Defaults to using the id. This can also be used to change the path.
  --user-agent USER_AGENT
                        The User-Agent string to use for requests.
  --max-retries MAX_RETRIES
                        The maximum number of retries for retriable errors (e.g., 403 Forbidden) before skipping a page. Default is 8.
  --cookies COOKIE_JAR  Path to a Netscape-format cookie jar file for authenticated requests.
  --cert CERT_FILE      Path to a client SSL certificate file (PEM format) for authentication.
  --key KEY_FILE        Path to a private key file (PEM format) corresponding to the client certificate.
```

For example, the following command will download page 1 until (and including) 10 of the book with id `mdp.39015073487137` and naming the files output files `my-book_page_<page_number>.pdf`:

```bash
hathitrust-downloader mdp.39015073487137 1 10 --name my-book
```

> [!IMPORTANT]
> The ID of the file can be found as part of the URL when opening a book through your browser. Below is an example URL and where to find the ID:
> ```
> https://babel.hathitrust.org/cgi/pt?id=mdp.39015073487137&seq=13
>                                        ^^^^^^^^^^^^^^^^^^ This demarks the ID of this book
> ```


> [!TIP]
> Alternatively to providing the ID, you can provide the complete URL containing the ID. Then the the tool will attempt to parse the ID from the URL automatically for you.
>
> For example, you can use it like so:
>
> ```bash
> hathitrust-downloader 'https://babel.hathitrust.org/cgi/pt?id=mdp.39015073487137&seq=13' 1 10 --name my-book
> ```

### Authentication

Some books on HathiTrust are only available if you are logged in through a partner institution, or if you are connecting from a specific region (e.g. the United States). If you are getting **403 Forbidden** errors or the download keeps retrying without making progress, you may need to pass your browser cookies to the downloader so it can access the book on your behalf.

#### When do I need this?

- You can open and read the book in your browser, but the downloader gives **403** errors.
- You are accessing HathiTrust through a university or library login.
- You are outside the US and some books are blocked in your region, but you have legitimate access through an institution.

#### Step 1: Log in to HathiTrust in your browser

Open [HathiTrust](https://www.hathitrust.org/) in your browser and log in through your institution. Verify that you can view the book you want to download.

#### Step 2: Export your cookies

You need to export your browser cookies for `hathitrust.org` into a text file. The easiest way to do this is with a browser extension:

- **Firefox**: Install the [cookies.txt](https://addons.mozilla.org/en-US/firefox/addon/cookies-txt/) extension. After installing, navigate to the HathiTrust page, click the extension icon, and select **"Export"** to save the cookies to a file (e.g. `cookies.txt`).
- **Chrome**: Install the [Get cookies.txt LOCALLY](https://chromewebstore.google.com/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc) extension. Navigate to the HathiTrust page, click the extension icon, and export the cookies.

> [!NOTE]
> The exported file must be in **Netscape/Mozilla cookie jar format** (this is the default format for the extensions listed above). The file typically looks like a text file with tab-separated values — you do not need to edit it.

#### Step 3: Use the `--cookies` flag

Pass the path to your exported cookie file using the `--cookies` flag:

```bash
hathitrust-downloader mdp.39015073487137 1 10 --name my-book --cookies cookies.txt
```

That's it! The downloader will now use your browser session to authenticate with HathiTrust.

> [!WARNING]
> Cookie files contain sensitive session data. Do not share your `cookies.txt` file with others. Cookies typically expire after some time, so you may need to re-export them if your downloads start failing again.

### Client Certificate Authentication (Advanced)

If your institution uses client SSL certificates to authenticate access to restricted HathiTrust volumes, you can specify them using the `--cert` and `--key` switches:

```bash
hathitrust-downloader mdp.39015073487137 1 10 --cert my-cert.pem --key my-key.pem
```

You can also combine cookies with client certificates if needed:

```bash
hathitrust-downloader mdp.39015073487137 1 10 --cookies cookies.txt --cert my-cert.pem --key my-key.pem
```

> [!NOTE]
> The certificate and key files should be in **PEM format**. Most users will only need `--cookies`. Client certificates are uncommon and typically only required by specific institutional setups. If you are unsure, start with just `--cookies`.



## Troubleshooting

### No Progess / Progress Bar is Stuck

Make sure that you can access books on HathiTrust. Try to open a book in your browser to see if everything is working fine. HathiTrust can require you to connect from an American IP. In addition, they limit the amount of pages you can download to 15 every 5 minutes. When you hit that limit you will need to wait, the tool will automatically wait and resume when the timeout is finished.

[pypi]: https://pypi.org/project/hathitrust-downloader/
[github-releases]: https://github.com/Addono/HathiTrust-downloader/releases/latest
[ci-badge]: https://img.shields.io/github/actions/workflow/status/Addono/HathiTrust-downloader/ci.yaml?event=push&style=flat-square

## Developing

Clone the repository:

```bash
git clone https://github.com/Addono/HathiTrust-downloader.git
cd ./HathiTrust-downloader
```

(Optional) Create a virtual Python environment, recommended but not required.

Install the package with dependencies:
```
pip install .
```

Now you can run the tool with:

```bash
python -m hathitrustdownloader.cli --help
```
