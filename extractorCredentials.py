import os
import re
import json
import csv
import argparse
from tqdm import tqdm
import time


# Function to print the centered banner
import os

def show_signature():
    signature = "\n".join([
        "===========================================================================\n"
        "        Welcome to Parsing Tools Extractor Credentials\n"
        "===========================================================================\n"
        "          Author: Afif Hidayatullah\n"
        "          Organization: ITSEC Asia\n"
        "===========================================================================\n"
    ])
    
    # Get terminal width
    terminal_width = os.get_terminal_size().columns

    # Split the signature into lines
    lines = signature.split('\n')
    
    # Center each line based on terminal width
    centered_signature = "\n".join(line.center(terminal_width) for line in lines)

    # Print the centered signature
    print(centered_signature)

# Call show_signature to see the result
show_signature()

# Function to search for keywords within a file
def search_keywords_in_file(file_name, keywords):
    try:
        search_results = []
        # List of encodings to try in case of errors
        encodings_to_try = ['utf-8', 'ISO-8859-1', 'utf-16']
        file_content = None

        # Try opening the file with different encodings
        for encoding in encodings_to_try:
            try:
                with open(file_name, 'r', encoding=encoding) as file:
                    file_content = file.readlines()
                break  # If successful, break out of the loop
            except UnicodeDecodeError:
                continue  # Try the next encoding if the current one fails

        if file_content is None:
            return [{"error": f"Could not read {file_name} with available encodings", "source": file_name}]

        # Patterns to search for (updated to exclude specific patterns)
        patterns = [
            r'(https?://[^\s:]+):([^:]+):([^:\s]+)',            # url:username:password
            r'([^:\s]+):([^:\s]+):(https?://[^\s]+)',          # username:password:url
        ]

        # Search for keywords in the file content
        for line in file_content:
            for pattern in patterns:
                match = re.search(pattern, line, re.IGNORECASE)
                if match:
                    if pattern == patterns[0]:
                        url, username, password = match.groups()
                    elif pattern == patterns[1]:
                        username, password, url = match.groups()

                    # Check if any keyword matches in the detected URL
                    if any(re.search(keyword, url, re.IGNORECASE) for keyword in keywords):
                        search_results.append({
                            "url": url,
                            "username": username,
                            "password": password,
                            "source": file_name
                        })

        return search_results
    except Exception as e:
        return [{"error": f"An error occurred while reading {file_name}: {str(e)}", "source": file_name}]

# Function to save results to the specified output format
def save_results(search_results, output_file, output_format):
    # Sort results by the source (file name) to ensure consistent output
    sorted_results = sorted(search_results, key=lambda x: x.get("source", ""))

    if output_format == 'json':
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(sorted_results, f, ensure_ascii=False, indent=4)
    elif output_format == 'csv':
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=["url", "username", "password", "source"])
            writer.writeheader()
            for result in sorted_results:
                # Skip results with errors
                if "error" not in result:
                    writer.writerow(result)
                else:
                    print(f"Error: {result['error']} in {result['source']}")
    elif output_format == 'txt':
        with open(output_file, 'w', encoding='utf-8') as f:
            for result in sorted_results:
                # Write URL, username, password, and source, or error message
                if "error" not in result:
                    f.write(f"URL: {result['url']}, Username: {result['username']}, Password: {result['password']}, Source: {result['source']}\n")
                else:
                    f.write(f"Error: {result['error']} in Source: {result['source']}\n")
    else:
        print("Unsupported output format. Choose 'json', 'csv', or 'txt'.")

# Argument parsing
def parse_arguments():
    # Create the parser
    parser = argparse.ArgumentParser(description="Search for keywords within text files")
    parser.add_argument('--path', type=str, default='.', help="Path to directory or specific file")
    parser.add_argument('--keywords', type=str, nargs='+', required=True, help="List of keywords to search for")
    parser.add_argument('--output', type=str, required=True, help="Output file name (with extension .json, .csv, or .txt)")

    # Check if --help was called
    args, unknown = parser.parse_known_args()
    # Print the banner before any output
     
    return parser.parse_args()

# Main logic
if __name__ == '__main__':
    # Parse the arguments
    args = parse_arguments()

    # Initialize list to store all search results
    all_search_results = []

    # List to store all text files in the directory
    txt_files = []

    # Loop through the directory to collect all .txt files
    if os.path.isfile(args.path):
        if args.path.endswith('.txt'):
            txt_files.append(args.path)
    else:
        # If the path is a directory
        for root, dirs, files in os.walk(args.path):
            for file in files:
                if file.endswith('.txt'):
                    txt_files.append(os.path.join(root, file))

    # Total number of .txt files to process
    total_files = len(txt_files)

    # Using tqdm to show progress bar with additional information
with tqdm(total=total_files, 
          desc="Processing files", 
          bar_format="{l_bar}{bar} | {n_fmt}/{total_fmt} files | Elapsed: {elapsed} | ETA: {remaining}") as progress_bar:
    # Loop to search keywords in each .txt file
    for file_name in txt_files:
        start_time = time.time()  # Track processing start time for each file
        search_results = search_keywords_in_file(file_name, args.keywords)
        all_search_results.extend(search_results)
        progress_bar.update(1)  # Update progress bar for each file processed

    # Save results to the specified file format
    save_results(all_search_results, args.output, os.path.splitext(args.output)[-1][1:])

    print(f"Search results have been saved to {args.output}")
