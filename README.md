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

Check that you have Python 3 installed and available on your shell. The following command should return something like `Python 3.12.5`. 

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

There are also Windows executables available. Download the `downloader_<version>_win.zip` from [releases](https://github.com/Addono/HathiTrust-downloader/releases/) and extract it. Then open a shell, e.g. `cmd` or `powershell`, to the directory where the ZIP is extracted. The easiest way to do this is by opening the folder in Explorer and right click while holding shift, now select the option "Open PowerShell Window Here".

The executable is bundled with Python and all other dependencies, hence you do not need to have anything installed. Now the tool can be used like:

```powershell
.\downloader.exe --help 
```

## Usage

The help should give some instructions on how to use the tool:

```bash
usage: hathitrust-downloader [-h] [--name NAME] id start_page end_page

Book downloader for HathiTrust

positional arguments:
  id           The ID of the book, e.g 'mdp.39015027794331' or a complete URL.
  start_page   The page number of the first page to be downloaded.
  end_page     The last number of the last page to be downloaded (inclusive).

options:
  -h, --help   show this help message and exit
  --name NAME  The start of the filename. Defaults to using the id. This can also be used to change the path.
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
> Alternatively, you can provide the complete URL as the ID argument, and the tool will attempt to parse the ID from the URL. Note that this feature is best-effort, and for optimal stability, it is still recommended to provide the specific ID directly.

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
