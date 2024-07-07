import os
import json
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def setup_driver():
    service = Service(executable_path="chromedriver.exe")  # Adjust the path if necessary
    options = webdriver.ChromeOptions()
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--incognito")
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def find_li_with_links(url):
    driver = setup_driver()
    driver.get(url)
    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'fund-popup-close'))
        ).click()
    except Exception as e:
        print("No popup appeared or could not close the popup.")
    
    li_with_links = driver.find_elements(By.CSS_SELECTOR, 'li.nav-item a')
    links_data = []

    for element in li_with_links:
        link_text = element.text.strip()
        link_url = element.get_attribute('href')
        if link_url:  # Only add links that are not None
            links_data.append({"text": link_text, "url": link_url})
    
    driver.quit()
    return links_data

def extract_information(links_data):
    extracted_data = []

    driver = setup_driver()

    for link_info in links_data:
        link_text = link_info['text']
        link_url = link_info['url']

        driver.get(link_url)
        # Initialize data storage for this link
        link_content = {}

        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, 'body'))
            )

            # Extract text from <p> tags
            paragraphs = driver.find_elements(By.TAG_NAME, 'p')
            paragraph_texts = [p.text.strip() for p in paragraphs if p.text.strip()]
            link_content['paragraphs'] = paragraph_texts

            # Extract text from <li> tags
            list_items = driver.find_elements(By.TAG_NAME, 'li')
            list_texts = [li.text.strip() for li in list_items if li.text.strip()]
            link_content['list_items'] = list_texts

            # Extract text from <p tabindex="0"> tags
            tabindex_paragraphs = driver.find_elements(By.CSS_SELECTOR, 'p[tabindex="0"]')
            tabindex_paragraph_texts = [p.text.strip() for p in tabindex_paragraphs if p.text.strip()]
            link_content['tabindex_paragraphs'] = tabindex_paragraph_texts

            # Check for PDF links and store the URLs
            pdf_links = driver.find_elements(By.XPATH, '//a[contains(@href, ".pdf")]')
            pdf_urls = []
            for pdf_link in pdf_links:
                pdf_url = pdf_link.get_attribute('href')
                if pdf_url:
                    pdf_urls.append(pdf_url)

            link_content['pdf_urls'] = pdf_urls

            extracted_data.append({link_text: link_content})

        except Exception as e:
            print(f"Failed to extract information from {link_url}: {str(e)}")
            extracted_data.append({link_text: "Failed to extract"})

    driver.quit()

    return extracted_data

def save_to_json(data, filename):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)

if __name__ == "__main__":
    url = "https://ddtg.hp.gov.in/"
    li_links = find_li_with_links(url)
    extracted_data = extract_information(li_links)
    print(extracted_data)
    save_to_json(extracted_data, 'extracted_information.json')

    print("Extraction and saving to JSON completed.")
