import os
import requests
import pandas as pd
import csv
import dns.resolver
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image
import pyautogui
import time


def take_screenshot_with_url_bar(url, output_file):
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")  # Maximize window
    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get(url)
        time.sleep(5)  # Adjust the sleep duration as needed (e.g., 5 seconds)

        # Take screenshot of the entire screen
        screenshot = pyautogui.screenshot()
        screenshot.save(output_file)
        print(f"Screenshot saved: {output_file}")
    except Exception as e:
        print(f"Failed to take screenshot: {e}")
    finally:
        driver.quit()


def check_dns(domain):
    resolver = dns.resolver.Resolver(configure=False)
    resolver.nameservers = ['8.8.8.8']  # Using Google's public DNS resolver
    try:
        resolver.query(domain)
        return True, "NoError"
    except dns.resolver.NXDOMAIN:
        return False, "NXDOMAIN"
    except dns.resolver.NoAnswer:
        return False, "NoAnswer"
    except dns.exception.Timeout:
        return False, "Timeout"
    except dns.resolver.NoNameservers:
        return False, "NoNameservers"
    except dns.resolver.NoRootSOA:
        return False, "NoRootSOA"
    except dns.exception.SyntaxError:
        return False, "SyntaxError"
    except dns.exception.FormError:
        return False, "FormError"
    except dns.exception.BadQuery:
        return False, "BadQuery"
    except dns.exception.BadResponse:
        return False, "BadResponse"
    except dns.exception.WantRead:
        return False, "WantRead"
    except dns.exception.WantWrite:
        return False, "WantWrite"
    except dns.exception.ConnectTimeout:
        return False, "ConnectTimeout"
    except dns.exception.SessionError:
        return False, "SessionError"


# Create folder for screenshots
screenshot_folder = "WebScreenshots"
if not os.path.exists(screenshot_folder):
    os.makedirs(screenshot_folder)

# Read domains from the file
with open('domains.txt', 'r') as file:
    domains = file.read().splitlines()

# Prepare a list to hold the combined data
combined_data = []

# Iterate over each domain to get WHOIS information and DNS status
for domain in domains:
    url = f"https://who-dat.as93.net/{domain}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        domain_info = data.get('domain', {})
        registrar_info = data.get('registrar', {})

        whois_entry = {
            'Domain': domain_info.get('domain'),
            'Registrar Name': registrar_info.get('name'),
            'Registrar Email': registrar_info.get('email'),
            'WHOIS Status': domain_info.get('status', ''),  # Original WHOIS status
            'Creation Date': domain_info.get('created_date'),
            'Expiry Date': domain_info.get('expiration_date'),
            'Update Date': domain_info.get('updated_date')
        }
    else:
        whois_entry = {
            'Domain': domain,
            'Registrar Name': None,
            'Registrar Email': None,
            'WHOIS Status': '',  # Keeping Status blank
            'Creation Date': None,
            'Expiry Date': None,
            'Update Date': None
        }

    # Check DNS status
    dns_status, dns_code = check_dns(domain)

    # Take screenshot if the domain is available
    if dns_status:
        url = f"http://{domain}"
        # Replace special characters in domain name to make it a valid filename
        sanitized_domain = domain.replace(".", "_").replace("/", "_")
        output_screenshot_file = os.path.join(screenshot_folder, f"{sanitized_domain}.png")
        take_screenshot_with_url_bar(url, output_screenshot_file)

    combined_entry = {
        **whois_entry,
        'DNS Status': 'Available' if dns_status else 'Unavailable',
        'DNS Code': dns_code,
        'Screenshot Path': output_screenshot_file if dns_status else None
    }

    combined_data.append(combined_entry)

# Convert the combined data to a DataFrame
df = pd.DataFrame(combined_data)

# Write the DataFrame to an Excel file
output_excel_file = 'output.xlsx'
df.to_excel(output_excel_file, index=False)

print(f"Combined data has been written to {output_excel_file}")
