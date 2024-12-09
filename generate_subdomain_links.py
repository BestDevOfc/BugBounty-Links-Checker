# sick of using FFUF for this bcs they like to filter stuff out that might lead to subdomain takeover or cert errors aren't handled 
# well by HTTPX/FFUF either.


subdomains_file = input(f"[ Enter subdomains wordlist file path ]: ")
subdomains = open(f"{subdomains_file}", 'r').readlines()
target = input(f"[ Enter target (DOMAIN.com) ]: ")

results_file = open("subdomains_links.txt", 'w')

for subdomain in subdomains:
    subdomain = subdomain.strip().rstrip()
    url = f"http://{subdomain}.{target}:80/"
    results_file.write(f"{url}\n")
    results_file.flush()
    print(url)
results_file.close()
