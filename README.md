## Keyword Search Tool

This Python script allows you to search for specific keywords within `.txt` files, extract URLs with associated usernames and passwords (in the format `https://url:username:password`), and save the results in a specified format (JSON, CSV, or TXT).

## Features

- **Search for specific keywords** within `.txt` files.
- **Extract URL:username:password patterns** from each line.
- **Support for multiple file types**: process individual files or an entire directory of `.txt` files.
- **Progress bar** for file processing to monitor the search's progress.
- **Error handling** to manage invalid file encoding or other read errors.
- **Save results** in multiple formats: JSON, CSV, or TXT.

## Requirements

- Python 3.x
- The following Python libraries:
  - `tqdm` for progress bar functionality.

To install the required dependencies, use the following command:
```markdown
pip install -r requirements.txt
```

## Installation

1. Clone this repository or download the script to your local machine.
2. Install dependencies using the provided `requirements.txt` file.
3. Run the script with the desired options (explained below).

## Usage

To use the tool, run the script from the command line as follows:

```bash
python extractorCredentials.py --path <directory_or_file_path> --keywords <keyword1> <keyword2> ... --output <output_file_name>
```

### Arguments:
- `--path`: The path to the directory or file to be processed. If a directory is provided, all `.txt` files within it will be searched.
- `--keywords`: A list of keywords to search for in the `.txt` files. You can provide multiple keywords separated by spaces.
- `--output`: The name of the output file where the search results will be saved. The output file can be in JSON, CSV, or TXT format.

### Example:

```bash
python extractorCredentials.py --path ./logs --keywords "admin" "password" --output results.json
```

This command will search for the keywords "admin" and "password" in all `.txt` files within the `./logs` directory and save the results in `results.json`.

## Output Format

The results can be saved in one of the following formats:
- **JSON**: A JSON file containing an array of results with `url`, `username`, `password`, and `source` fields.
- **CSV**: A CSV file containing `url`, `username`, `password`, and `source` as columns.
- **TXT**: A plain text file containing the results in the format:
  ```
  URL: <url>, Username: <username>, Password: <password>, Source: <source>
  ```

## Example Output (CSV):
```
url,username,password,source
https://example.com,admin,secretpassword,/path/to/file.txt
https://test.com,user,password123,/path/to/file2.txt
```

## Error Handling

- The script handles errors related to file reading and invalid UTF-8 encoding.
- Errors during processing are logged and can be viewed in the output file.

## Contributing

Feel free to fork this repository, contribute improvements, or open issues for any bugs or suggestions!

## Acknowledgements
tqdm for providing the progress bar functionality.
argparse for parsing command-line arguments.

