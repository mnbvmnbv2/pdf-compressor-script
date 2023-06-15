import os
import subprocess
import shutil
import argparse


def compress_pdf(input_file, output_file):
    gs_command = [
        "gswin64c",
        "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.4",
        "-dPDFSETTINGS=/ebook",
        "-dNOPAUSE",
        "-dBATCH",
        "-dQUIET",
        "-sstdout=%stderr",
        "-q",
        "-sOutputFile=" + output_file,
        input_file,
    ]

    result = subprocess.run(gs_command, stderr=subprocess.PIPE)

    if result.returncode != 0:
        error_message = result.stderr.decode("utf-8")
        print(f"An error occurred: {error_message}")
        return False

    return True


def compress_pdfs_in_folder(folder):
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(".pdf"):
                original_file = os.path.join(root, file)
                temp_file = os.path.join(root, "temp_compressed.pdf")

                if compress_pdf(original_file, temp_file):
                    original_size = os.path.getsize(original_file)
                    compressed_size = os.path.getsize(temp_file)

                    # Only replace the original file if the compressed file is smaller
                    if compressed_size < original_size:
                        shutil.move(temp_file, original_file)
                        compression_ratio = (
                            100 * (original_size - compressed_size) / original_size
                        )
                        print(f"Compressed {original_file} by {compression_ratio:.2f}%")
                    else:
                        os.remove(temp_file)
                        print(
                            f"Compression of {original_file} would increase file size. Skipping."
                        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Compress all PDFs in a specified folder and its subfolders."
    )
    parser.add_argument(
        "folder", help="The path to the folder containing the PDFs to compress."
    )

    args = parser.parse_args()

    compress_pdfs_in_folder(args.folder)
