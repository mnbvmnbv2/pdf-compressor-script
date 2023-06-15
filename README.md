# PDF Compressor
This is a Python script that compresses all PDF files in a specified directory and its subdirectories using Ghostscript. The script replaces each original PDF with its compressed version if the compressed file is smaller. The script will skip and not compress PDF files that would increase in size after compression. It does not compress the files a lot (like some other programs and 3rd party apps), but you could get significant savings if you have a lot of pdfs.

## Requirements
- Python 3
- Ghostscript

## Installation
Ensure that you have Python 3 installed on your system. You can download Python from the official website.

Install Ghostscript on your system. The installation process varies by system:

- On Ubuntu, you can use: `sudo apt-get install ghostscript` (not tested)
- On Windows, you can download the installer from the Ghostscript website. You then need to add the bin folder to PATH and make sure to have the file `gswin64c` in the bin folder.
- On Mac, you can use Homebrew: `brew install ghostscript` (not tested)

- Clone this repository or download the Python script.

## Usage
To compress all PDFs in a directory, navigate to the directory containing the Python script in your terminal or command prompt, then run:

`python pdf_compress.py *path* *logpath*`

Replace `*path*` with the path to the directory that contains the PDFs you want to compress. Replace `*logpath*` with a path to a txt file for keeping track of which files is compressed so you can continue later. The script will recursively search the specified directory and all its subdirectories for PDF files to compress.

For each PDF, the script will print a message indicating whether the file was compressed or skipped, and if compressed, the percentage by which the file size was reduced.

## Troubleshooting
If you encounter an error message like "gs not found", it means Ghostscript is not installed or not found in your system's PATH. Ensure that Ghostscript is installed and added to your PATH. In the script at line `9` the script calls `gswin64c` which could for example be called something else for you.

## Credits/Disclaimer
This code was made almost exclusively with ChatGPT.

## Results
I used this on a folder with about **14GB** of random pdfs (about 15000, everything from just text to just pictures, mostly academic lectures or other academic pdfs) and it got compressed to **6.5GB**.