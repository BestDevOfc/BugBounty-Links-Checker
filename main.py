import colorama
import threading
import time
import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import Fore, Style


colorama.init(autoreset=True)

class Colors:
    RED     = f"{Style.BRIGHT}{Fore.RED}"
    GREEN   = f"{Style.BRIGHT}{Fore.GREEN}"
    YELLOW  = f"{Style.BRIGHT}{Fore.YELLOW}"
    MAGENTA = f"{Style.BRIGHT}{Fore.MAGENTA}"
    CYAN    = f"{Style.BRIGHT}{Fore.CYAN}"
C = Colors()


class DomainFlyOver(object):
    def __init__(self):
        self.urls = []
        self.settings = {
            "timeout": 30,
            "sleep": 5,
            "threads": 5
        }
        self.results_dir = f"Screenshots-{time.time()}"
        self.errs_file = open("Errors.log", 'w')
        self.lock = threading.Lock()

    def log_err(self, err):
        self.lock.acquire()
        self.errs_file(f"{err}\n")
        self.lock.release()
    def get_chrome_options(self):
        # Configure options for headless Chrome
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')  # Useful for running in Docker
        chrome_options.add_argument('--window-size=1920x1080')
        chrome_options.add_argument('--ignore-certificate-errors')  # Ignore SSL certificate errors
        chrome_options.add_argument('--allow-insecure-localhost')  # Allow access to localhost with invalid certs
    
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
        except Exception as err:
            print(f"{C.GREEN} [!] - {C.RED}An error occurred while processing {url}: {err}")
            self.log_err(f"An error occurred while processing {url}: {err}")
            

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
                print(f"{C.RED}Domain: {domain}, Err --> {err}")
        
        domains = []

        
        # Use ThreadPoolExecutor to handle multiple URLs concurrently
        max_threads = self.settings[ "threads" ]  # Adjust thread count as needed

        with ThreadPoolExecutor(max_threads) as executor:
            futures = [executor.submit(self.process_url, index, url) for index, url in enumerate(self.urls)]
            
            for future in as_completed(futures):
                try:
                    future.result()  # Wait for each thread to complete
                except Exception as err:
                    err = f"An error occurred in one of the threads: {err}"
                    self.log_err(f"{err}")
                    print(f"{C.RED}{err}")


if __name__ == "__main__":
    Obj = DomainFlyOver()
    Obj.main()
