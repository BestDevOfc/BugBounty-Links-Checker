import time
import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from concurrent.futures import ThreadPoolExecutor, as_completed



class DomainFlyOver(object):
    def __init__(self):
        self.urls = []
        self.settings = {
            "timeout": 30,
            "sleep": 5
        }
        self.results_dir = f"Screenshots-{time.time()}"

    def get_chrome_options(self):
        # Configure options for headless Chrome
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')  # Useful for running in Docker
        chrome_options.add_argument('--window-size=1920x1080')
        return chrome_options

    def process_url(self, index, url):
        try:
            driver = webdriver.Chrome(options=self.get_chrome_options())
            driver.set_page_load_timeout( self.settings["timeout"] )
            print(f"Opening URL {index + 1}/{len(self.urls)}: {url}")
            driver.get(url)
            
            
            # Wait for the page to load completely
            time.sleep( self.settings["sleep"] )
            
            # Save a screenshot of the page
            domain = url.replace("https://", '').replace("http://", '')
            screenshot_path = f'{self.results_dir}/screenshot_{domain}.png'
            driver.save_screenshot(screenshot_path)
            print(f"Screenshot saved as {screenshot_path}")
        except Exception as e:
            print(f"An error occurred while processing {url}: {e}")
        finally:
            driver.quit()

    def main(self):
        # create needed directories:
        os.makedirs(self.results_dir, exist_ok=True)
        
        # load in the URLs:
        domains = open("domains.txt", 'r').readlines()
        self.urls = []
        for domain in domains:
            try:
                domain = domain.strip().rstrip()
                # add the https:// prefix if not already present:
                self.urls.append(domain if ("http:" in domain) or ("https:" in domain) else f"https://{domain}")
            except Exception as err:
                print(f"Domain: {domain}, Err --> {err}")
        
        domains = []

        
        # Use ThreadPoolExecutor to handle multiple URLs concurrently
        max_threads = 5  # Adjust thread count as needed

        with ThreadPoolExecutor(max_threads) as executor:
            futures = [executor.submit(self.process_url, index, url) for index, url in enumerate(self.urls)]
            
            for future in as_completed(futures):
                try:
                    future.result()  # Wait for each thread to complete
                except Exception as e:
                    print(f"An error occurred in one of the threads: {e}")

if __name__ == "__main__":
    Obj = DomainFlyOver()
    Obj.main()
