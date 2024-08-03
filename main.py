import requests
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm


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
            req = requests.get(url=f"{url}", headers=headers, timeout=60)
            self.results_file.write(f"{url}\n")
            self.results_file.flush()
        except Exception as err:
            # print(err)
            pass # non-reachable
        self.pbar.update(1)
    def main(self):
        with ThreadPoolExecutor(max_workers=150) as executor:
            executor.map(self.check_url, self.urls)

if __name__ == "__main__":
    fname = input(f"[ File Name ]: ")
    checkerObj = linksChecker(fname)
    checkerObj.main()
    
