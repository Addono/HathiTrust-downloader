# HathiTrust Downloader

## Installing

### Python 3 (OS Agnostic)

Download or clone the source code, then open a shell and point it to this folder. To check which version of Python you have installed, run:

```bash
python -V
```

Then install the dependencies using `pip`:

```bash
pip install -r requirements.txt
```

Then you can use the application from the command line, e.g. to show the help instructions run:

```bash
python downloader.py --help
```

### Windows Executable

There are also Windows executables available. Download the `downloader.zip` from [releases](https://github.com/Addono/HathiTrust-downloader/releases/) and extract it. Then open a shell, e.g. `cmd` or `powershell`, to the directory where the ZIP is extracted. The easiest way to do this is by opening the folder in Explorer and right click while holding shift, now select the option "Open PowerShell Window Here".

The executable is bundled with Python and all other dependencies, hence you do not need to have anything installed. Now the tool can be used like:

```powershell
.\downloader.exe --help 
```

## Usage

The help should give some instructions on how to use the tool:

```bash
usage: downloader.py [-h] [--name NAME] id start_page end_page

Book downloader from Hathitrust

positional arguments:
  id           The ID of the book, e.g 'mdp.39015027794331'.
  start_page   The page number of the first page to be downloaded.
  end_page     The last number of the last page to be downloaded (inclusive).

optional arguments:
  -h, --help   show this help message and exit
  --name NAME  The start of the filename. Defaults to using the id. This can
```

One example which downloads page 1 until (and including) 10 of the book with id `mdp.39015027794331` and naming the files `my-book_page_<page_number>.pdf`:

```bash
python downloader.py mdp.39015027794331 1 10 --name my-book
```

The ID of the file can be found as part of the URL when opening a book through your browser.
