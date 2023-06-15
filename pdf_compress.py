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

    try:
        result = subprocess.run(gs_command, stderr=subprocess.PIPE, timeout=300)
    except subprocess.TimeoutExpired:
        print(f"Compression timed out for: {input_file}")
        return False
    except UnicodeEncodeError:
        print(f"UnicodeEncodeError occurred while processing: {input_file}")
        return False

    if result.returncode != 0:
        try:
            error_message = result.stderr.decode("utf-8")
            print(f"An error occurred: {error_message}")
        except UnicodeEncodeError:
            print(
                f"UnicodeEncodeError occurred while decoding error message for: {input_file}"
            )
        return False

    return True


def compress_pdfs_in_folder(folder, log_file):
    with open(log_file, "a+", encoding="utf-8") as f:
        f.seek(0)
        processed_files = f.read().splitlines()

    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(".pdf"):
                original_file = os.path.join(root, file)

                if original_file in processed_files:
                    print(f"Skipping {original_file} as it has already been processed.")
                    continue

                temp_file = os.path.join(root, "temp_compressed.pdf")

                if compress_pdf(original_file, temp_file):
                    original_size = os.path.getsize(original_file)
                    compressed_size = os.path.getsize(temp_file)

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

                with open(log_file, "a", encoding="utf-8") as f:
                    f.write(original_file + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Compress all PDFs in a specified folder and its subfolders."
    )
    parser.add_argument(
        "folder", help="The path to the folder containing the PDFs to compress."
    )
    parser.add_argument(
        "log_file", help="The path to the log file to keep track of processed PDFs."
    )

    args = parser.parse_args()

    compress_pdfs_in_folder(args.folder, args.log_file)
