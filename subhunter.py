 import requests
import time
import sys
import os



http_subdomains = []
https_subdomains = []

file = open("files/subdomains.txt","r")
content = file.read()
subdomains = content.split()

banner = '''
iii iii      iii iiiiiiiiii    ooo
iii iiiii    iii iii          ooooo
iii iii ii   iii iiiiiiiiii  oo   oo
iii iii iii  iii iii        oo     oo
iii iii  iii iii iii        oo     oo
iii iii   iiiiii iii         oo   oo
iii iii    iiiii iii          ooooo
iii iii     iiii iii           ooo

developed by: CyberSec
Telegram group: CyberSec
'''

print(banner)

def find_https_domain(subdomain):

    url = f"https://{subdomain}"

    #spliting subdomain from domain
    split_it = url.split(".")

    domain = split_it[1] + "." + split_it[-1] # combining domain and extension

   

    with open(f"{domain}.subdomains.txt","a+") as file:
    
        try:

            status = requests.get(url,allow_redirects = False)
            if status.status_code == 200:
                https_subdomains.append(url)
                file.write(url + ":" + str(status.status_code))
                MESSAGE = f"[+] Domain found: {url} {status.status_code}"
                return MESSAGE
            elif status.status_code == 301:
                print("[+] Detected a redirect...")
            else:
                print("[+] Something went wrong...")
        except requests.ConnectionError:

            MESSAGE = f"[+] Could noy find http or https for: {url}"
            return MESSAGE




def find_http_domain(domain):



    try:
        os.system(f"mkdir {domain}")
    except:
        pass

    with open(f"{domain}/{domain}.subdomains.txt","a+") as file:

        for subdomain in subdomains:

            url = f"http://{subdomain}.{domain}"

            try:

                status = requests.get(url,allow_redirects = False)

                if status.status_code == 200:
                    http_subdomains.append(url)
                    print("[+] Discovered subdomain:", url, status.status_code)
                elif status.status_code == 301:
                    print("[+] Detected a redirect...")
                else:
                    print("[+] Something went wrong...")

                file.write(url + ":" + str(status.status_code) + "\n")

            except KeyboardInterrupt:
                print("[+] Exiting....")
                time.sleep(2)
                exit()
            except requests.ConnectionError:

                print("[+] Trying https connection...")
                
                results = find_https_domain(url.split("//")[1]) #here we omit http:// from the url
                print(results)

            




find_http_domain(sys.argv[1])
