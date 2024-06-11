# WHOIS, DNS, and Screenshot Checker

This script is designed to fetch WHOIS information, DNS status, and take screenshots for a list of domains. It provides detailed information about each domain, including WHOIS data such as registrar name, registrar email, creation date, expiry date, and update date, along with DNS status and associated error codes. Additionally, it takes screenshots of accessible domains and saves them to a specified folder.

## Features

- Retrieves WHOIS information, DNS status, and takes screenshots for multiple domains.
- Provides detailed WHOIS data including registrar information and status.
- Checks DNS status and provides associated error codes.
- Takes screenshots of accessible domains and saves them to a specified folder.
- Outputs all collected data into an Excel file for further analysis.

## Requirements

- Python 3.x
- Libraries: requests, pandas, dnspython, selenium, Pillow

## Installation

1. Clone the repository or download the script file.
2. Install the required Python libraries using pip:
   ```
   pip install requests pandas dnspython selenium Pillow
   ```
3. Ensure you have Google Chrome installed as the script uses the Chrome WebDriver for taking screenshots.

## Usage

1. Create a text file named `domains.txt` containing the list of domains to check, with each domain on a new line.
2. Run the script `whois_dns_screenshot_checker.py`.
3. The script will fetch WHOIS information, check DNS status, take screenshots of accessible domains, and save the data.
4. The collected data will be saved to an Excel file named `output.xlsx` in the same directory.

## Configuration

- The script uses the `https://who-dat.as93.net/` API to fetch WHOIS information. No API key is required.
- Ensure the `domains.txt` file is in the same directory as the script and contains the list of domains to check.
