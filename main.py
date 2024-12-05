import urllib3
import requests
import colorama

from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
from colorama import Fore, Style

colorama.init(autoreset=True)
urllib3.disable_warnings()



class linksChecker(object):
    def __init__(self, fname):
        self.urls = list(set(open(f"{fname}", 'r').readlines()))
        self.results_file = open(f"Live_{fname}", 'w')
        self.pbar = tqdm(total=len(self.urls))
    def check_url(self, url):
        try:
            url = f"{url}".strip().rstrip()
            if 'https://' not in url.lower() and 'http://' not in url.lower():
                url = f"https://{url}"
            headers = {
                'User-Agent': "Firefox Mozilla Google"
            }
            req = requests.get(url=f"{url}", headers=headers, verify=False, timeout=60)
            self.results_file.write(f"{url} | ({len(req.text)}) | {req.status_code}\n")
            self.results_file.flush()
        except Exception as err:
            if f"Failed to resolve" in f"{err}":
                pass # non-reachable
            else:
                # this may be due to certificate errors, these may be missed by many scanning tools and 
                # bounty hunters! (read a writeup about how a guy found a simple LFI bcs of it)
                print(f"{Fore.RED}[+] - {Fore.GREEN}[*** Non-Standard Error: {Fore.YELLOW}{url} {Fore.GREEN}***]\n")
                self.results_file.write(f"[ *** Non-Standard Errors {url}  ]")
                self.results_file.flush()
        self.pbar.update(1)
    def main(self):
        with ThreadPoolExecutor(max_workers=150) as executor:
            executor.map(self.check_url, self.urls)

if __name__ == "__main__":
    fname = input(f"[ File Name ]: ")
    checkerObj = linksChecker(fname)
    checkerObj.main()
