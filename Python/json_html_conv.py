import json
import argparse
import sys, os

def json_to_html_table(json_data):
    # Define the columns to exclude and rename headers for clarity
    excluded_columns = {"throughput", "receivedKBytesPerSec", "sentKBytesPerSec"}
    headers_map = {
        "transaction": "Transaction Name",
        "sampleCount": "Sample Count",
        "errorCount": "Error Count",
        "errorPct": "Error Percentage (%)",
        "meanResTime": "Mean Response Time (ms)",
        "medianResTime": "Median Response Time (ms)",
        "minResTime": "Min Response Time (ms)",
        "maxResTime": "Max Response Time (ms)",
        "pct1ResTime": "90th Percentile Response Time (ms)",
        "pct2ResTime": "95th Percentile Response Time (ms)",
        "pct3ResTime": "99th Percentile Response Time (ms)"
    }

    # Start the HTML table
    html = "<table>"
    html += "<tr>"
    
    # Add table headers (with renamed headings)
    headers = [key for key in json_data[next(iter(json_data))].keys() if key not in excluded_columns]
    for header in headers:
        html += f"<th>{headers_map.get(header, header)}</th>"
    html += "</tr>"

    # Add table rows
    for key, row in json_data.items():
        if key != "Total":  # Exclude "Total" row
            html += "<tr>"
            for header in headers:
                html += f"<td>{row.get(header, '')}</td>"
            html += "</tr>"

    # End the HTML table
    html += "</table>"
    return html

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Convert JSON data to an HTML table and insert it into success.html.")
    parser.add_argument("json_file_path", help="Path to the JSON data file")
    args = parser.parse_args()

    # Append 'statistics.json' to the folder path
    json_file_path = os.path.join(args.json_file_path, "statistics.json")
    print("File Path",json_file_path)
    success_html_path = './Templates/success.html'

    # Check if the file exists
    if not os.path.isfile(json_file_path):
        print(f"Error: '{json_file_path}' does not exist. Terminating process.", file=sys.stderr)
        sys.exit(1)  # Terminate the process with a non-zero exit code
    
    try:
        # Read JSON data from the specified file
        with open(json_file_path, "r") as file:
            json_data = json.load(file)

        # Convert JSON data to HTML table
        html_table = json_to_html_table(json_data)

        # Read success.html, replace placeholder, and write output to the same file
        with open(success_html_path, "r") as file:
            success_html = file.read()

        # Replace placeholder with generated HTML table
        updated_html = success_html.replace("${JMETER_TXN_TABLE}", html_table)

        # Save the modified HTML content back to success.html
        with open(success_html_path, "w") as file:
            file.write(updated_html)

        print("HTML table inserted into 'success.html'")
    
    except FileNotFoundError as e:
        print(f"Error: {e}. Make sure the file path is correct.", file=sys.stderr)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON file: {e}. Ensure it contains valid JSON.", file=sys.stderr)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
