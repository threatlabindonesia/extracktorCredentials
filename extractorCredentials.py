import os
import re
import json
import csv
import argparse
from tqdm import tqdm
import time

# Function to print the centered banner
def show_signature():
    signature = "\n".join([
        "===========================================================================",
        "        Welcome to Parsing Tools Extractor Credentials",
        "===========================================================================",
        "          Author: Afif Hidayatullah",
        "          Organization: ITSEC Asia",
        "===========================================================================",
    ])
    try:
        terminal_width = os.get_terminal_size().columns
        lines = signature.split('\n')
        centered_signature = "\n".join(line.center(terminal_width) for line in lines)
        print(centered_signature)
    except OSError:
        # Fallback in case terminal width cannot be determined
        print(signature)

# Function to search for keywords within a file
def search_keywords_in_file(file_name, keywords):
    try:
        search_results = []
        encodings_to_try = ['utf-8', 'ISO-8859-1', 'utf-16']
        file_content = None

        for encoding in encodings_to_try:
            try:
                with open(file_name, 'r', encoding=encoding) as file:
                    # Read file in chunks
                    for chunk in iter(lambda: file.read(1024 * 1024), ''):  # Read 1MB chunks
                        for pattern in [
                            r'(https?://[^\s:]+):([^:]+):([^:\s]+)',
                            r'([^:\s]+):([^:\s]+):(https?://[^\s]+)'
                        ]:
                            for match in re.finditer(pattern, chunk, re.IGNORECASE):
                                if pattern == r'(https?://[^\s:]+):([^:]+):([^:\s]+)':
                                    url, username, password = match.groups()
                                else:
                                    username, password, url = match.groups()

                                if any(re.search(keyword, url, re.IGNORECASE) for keyword in keywords):
                                    search_results.append({
                                        "url": url,
                                        "username": username,
                                        "password": password,
                                        "source": file_name
                                    })
                break
            except UnicodeDecodeError:
                continue

        if file_content is None:
            return [{"error": f"Could not read {file_name} with available encodings", "source": file_name}]

        return search_results
    except Exception as e:
        return [{"error": f"An error occurred while reading {file_name}: {str(e)}", "source": file_name}]

# Function to save results to the specified output format
def save_results(search_results, output_file, output_format):
    sorted_results = sorted(search_results, key=lambda x: x.get("source", ""))

    if output_format == 'json':
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(sorted_results, f, ensure_ascii=False, indent=4)
    elif output_format == 'csv':
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=["url", "username", "password", "source"])
            writer.writeheader()
            for result in sorted_results:
                if "error" not in result:
                    writer.writerow(result)
    elif output_format == 'txt':
        with open(output_file, 'w', encoding='utf-8') as f:
            for result in sorted_results:
                if "error" not in result:
                    f.write(f"URL: {result['url']}, Username: {result['username']}, Password: {result['password']}, Source: {result['source']}\n")
    else:
        print("Unsupported output format. Choose 'json', 'csv', or 'txt'.")

# Argument parsing
def parse_arguments():
    parser = argparse.ArgumentParser(description="Search for keywords within text files")
    parser.add_argument('--path', type=str, default='.', help="Path to directory or specific file")
    parser.add_argument('--keywords', type=str, nargs='+', required=True, help="List of keywords to search for")
    parser.add_argument('--output', type=str, required=True, help="Output file name (with extension .json, .csv, or .txt)")
    return parser.parse_args()

# Main logic
if __name__ == '__main__':
    show_signature()
    args = parse_arguments()
    all_search_results = []
    txt_files = []

    if os.path.isfile(args.path):
        if args.path.endswith('.txt'):
            txt_files.append(args.path)
    else:
        for root, dirs, files in os.walk(args.path):
            for file in files:
                if file.endswith('.txt'):
                    txt_files.append(os.path.join(root, file))

    total_files = len(txt_files)

    with tqdm(total=total_files, 
              desc="Processing files", 
              bar_format="{l_bar}{bar} | {n_fmt}/{total_fmt} files | Elapsed: {elapsed} | ETA: {remaining}") as progress_bar:
        for file_name in txt_files:
            search_results = search_keywords_in_file(file_name, args.keywords)
            all_search_results.extend(search_results)
            progress_bar.update(1)

    save_results(all_search_results, args.output, os.path.splitext(args.output)[-1][1:])
    print(f"Search results have been saved to {args.output}")
