import requests
import threading
from concurrent.futures import ThreadPoolExecutor
import random
import time
import sys
import os
import platform
# Color codes for formatting output
purple = "\033[1;35m"
blue = "\033[34m"
green = "\033[1;32m"
red = "\033[1;31m"
yellow = "\033[1;33m"
white = "\033[1;37m"
import random
import string
def clear_screen():
    if 'termux' in platform.system().lower():
        os.system('clear')
    elif platform.system().lower() == 'windows':
        os.system('cls')
    else:
        os.system('clear')
def generate_user_agent():
    fbav = f"{random.randint(111, 999)}.0.0.{random.randint(11, 99)}.{random.randint(111, 999)}"
    fbbv = str(random.randint(111111111, 999999999))
    fbrv = '0'
    random_seed = random.Random()
    adid = ''.join(random_seed.choices(string.hexdigits, k=16))

    # Randomly vary the Android OS version, device, and app version for realism
    device = random.choice(["HUAWEI MAR-LX1M", "Samsung SM-G960F", "OnePlus GM1913"])
    fbav_version = str(random.randint(49, 150))  # Updated range for FBAV versions
    fbbv_version = str(random.randint(11111111, 77777777))
    carrier = random.choice(["Ooredoo TN", "Orange", "Vodafone", "T-Mobile"])

    ua_bgraph = f'[FBAN/FB4A;FBAV/{fbav_version}.0.0.{random.randrange(20, 49)}.{random.randint(11, 99)};FBBV/{fbbv_version};' \
                f'[FBAN/FB4A;FBAV/{fbav};FBBV/{fbbv};FBDM/{{density=3.0,width=1080,height=2107}};FBLC/fr_FR;' \
                f'FBRV/{fbrv};FBCR/{carrier};FBMF/{device.split(" ")[0]};FBBD/{device.split(" ")[0]};' \
                f'FBPN/com.facebook.katana;FBDV/{device};FBSV/9;FBOP/1;FBCA/arm64-v8a:]'
    
    return ua_bgraph

ua_bgraph = generate_user_agent()


import requests
import random
import concurrent.futures as thread
import os
import string

# Random FB version generation
fbav = f'{random.randint(111, 999)}.0.0.{random.randint(11, 99)}.{random.randint(111, 999)}'
fbbv = str(random.randint(111111111, 999999999))
fbrv = '0'
random_seed = random.Random()
adid = ''.join(random_seed.choices(string.hexdigits, k=16))

# User agent string
ua_bgraph = '[FBAN/FB4A;FBAV/' + str(random.randint(49, 66)) + '.0.0.' + str(random.randrange(20, 49)) + str(random.randint(11, 99)) + ';FBBV/' + str(random.randint(11111111, 77777777)) + ';' + '[FBAN/FB4A;FBAV/' + fbav + ';FBBV/' + fbbv + ';FBDM/{density=3.0,width=1080,height=2107};FBLC/fr_FR;FBRV/' + fbrv + ';FBCR/Ooredoo TN;FBMF/HUAWEI;FBBD/HUAWEI;FBPN/com.facebook.katana;FBDV/MAR-LX1M;FBSV/9;FBOP/1;FBCA/arm64-v8a:]'

def bgraph(uid, pw, path_file, extract_type, success_count, existing_uids):
    accessToken = '350685531728|62f8ce9f74b12f84c123cc23437a4a32'  # Example token

    data = {
        'method': 'auth.login',
        'fb_api_req_friendly_name': 'authenticate',
        'fb_api_caller_class': 'com.facebook.account.login.protocol.Fb4aAuthHandler',
        'api_key': '62f8ce9f74b12f84c123cc23437a4a32',
        'email': uid,
        'password': pw,
        'access_token': accessToken
    }

    url = 'https://b-graph.facebook.com/auth/login?include_headers=false&decode_body_json=false&streamable_json_response=true'

    try:
        
        if uid in existing_uids:
            print(f"     {yellow}[INFO] {red}ACCOUNT --> {white}{uid} {red}already exists.")
            print("\033[1;37m───────────────────────────────────────────────────────────────\033[0m")
            return

        response = requests.post(url, data=data).json()
        
        print(response)
        if 'access_token' in response:
            token = response['access_token']

            with open(path_file, 'a') as f:
                f.write(f"{uid}|{token}\n")

            print("\033[1;37m───────────────────────────────────────────────────────────────\033[0m")
            print(f"     \033[32m[SUCCESS]\033[0m: Extracted Account ─────> {uid}.")
            print("\033[1;37m───────────────────────────────────────────────────────────────\033[0m")
            success_count.append(uid)
        else:
            print("\033[1;37m───────────────────────────────────────────────────────────────\033[0m")
            print(f"     \033[31m[FAILED]\033[0m: TO EXTRACT Account ─────> {uid}.")
            print("\033[1;37m───────────────────────────────────────────────────────────────\033[0m")

    except Exception as e:
        print(f"     \033[1;31m[ERROR]\033[0m Error extracting account: {uid}. Reason: {str(e)}\033[0m\n")


def proz(accounts_file, token_output_path, extract_type):
    """Process the accounts and extract tokens concurrently."""
    success_count = []

    # Load existing uids from the output file to avoid duplicates
    existing_uids = set()
    if os.path.exists(token_output_path):
        with open(token_output_path, 'r') as f:
            existing_uids = {line.split('|')[0] for line in f.readlines()}

    try:
        with open(accounts_file, 'r') as file:
            accounts = file.readlines()

        accounts = [line.strip() for line in accounts if '|' in line.strip()]

        if not accounts:
            print(f"No valid accounts found in {accounts_file}.")
            return

        with thread.ThreadPoolExecutor(max_workers=30) as executor:
            futures = [executor.submit(bgraph, uid, pw, token_output_path, extract_type, success_count, existing_uids)
                       for uid, pw in [account.split('|') for account in accounts]]

            for future in futures:
                future.result()

        print("\033[1;37m───────────────────────────────────────────────────────────────\033[0m")
        print(f"     \033[1;34m[SUCCESS]\033[0m: {len(success_count)} {extract_type}(s) successfully extracted.")
        print("\033[1;37m───────────────────────────────────────────────────────────────\033[0m")

    except FileNotFoundError:
        print(f"File not found: {accounts_file}")
        return

import requests
import random
import concurrent.futures as thread
import os
import string

fbav = f'''{random.randint(111, 999)}.0.0.{random.randint(11, 99)}.{random.randint(111, 999)}'''
fbbv = str(random.randint(111111111, 999999999))
fbrv = '0'
random_seed = random.Random()
adid = ''.join(random_seed.choices(string.hexdigits, k=16))
ua_bgraph = '[FBAN/FB4A;FBAV/' + str(random.randint(49, 66)) + '.0.0.' + str(random.randrange(20, 49)) + str(random.randint(11, 99)) + ';FBBV/' + str(random.randint(11111111, 77777777)) + ';' + '[FBAN/FB4A;FBAV/' + fbav + ';FBBV/' + fbbv + ';FBDM/{density=3.0,width=1080,height=2107};FBLC/fr_FR;FBRV/' + fbrv + ';FBCR/Ooredoo TN;FBMF/HUAWEI;FBBD/HUAWEI;FBPN/com.facebook.katana;FBDV/MAR-LX1M;FBSV/9;FBOP/1;FBCA/arm64-v8a:]'

def load_existing_tokens(path_file):
    """Load existing accounts or pages from the output file."""
    if os.path.exists(path_file):
        with open(path_file, 'r') as f:
            return {line.split('|')[0] for line in f.readlines()}  # Set of existing uids or page ids
    return set()

def bgraph_page(uid, pw, path_file, extract_type, success_count, existing_tokens):
    accessToken = '350685531728|62f8ce9f74b12f84c123cc23437a4a32'  # Example token
    
    if uid in existing_tokens:
        print("\033[1;37m───────────────────────────────────────────────────────────────\033[0m")
        print(f"     {white}ACCOUNT ─────> {red}{uid} {green}ALREADY EXISTS")
        return

    data = {
        'method': 'auth.login',
        'fb_api_req_friendly_name': 'authenticate',
        'fb_api_caller_class': 'com.facebook.account.login.protocol.Fb4aAuthHandler',
        'api_key': '62f8ce9f74b12f84c123cc23437a4a32',
        'email': uid,
        'password': pw,
        'access_token': accessToken
    }

    url = 'https://b-graph.facebook.com/auth/login?include_headers=false&decode_body_json=false&streamable_json_response=true'

    try:
        response = requests.post(url, data=data).json()
        
        if 'access_token' in response:
            token = response['access_token']

            # Extract Facebook Pages associated with the account token
            pages = extract_fb_pages(token)
            if pages:
                for page in pages:
                    page_id = page['id']
                    if page_id not in existing_tokens:
                        with open(path_file, 'a') as f:
                            f.write(f"{page_id}|{page['accessToken']}\n")
                        print(f"{white}{uid}  ─────> {green}Page ID: {red}{page_id} {yellow}EXTRACTED SUCCESSFULLY")
                        existing_tokens.add(page_id)
                    else:
                        print(f"{white}ID:  {page_id} ─────> {green}ALREADY EXISTS ! ")

            else:
                print(f"{white}{uid} ─────> {red}DOESN'T HAVE PAGES !")
            
            success_count.append(uid)
        else:
            print(f"{white}{uid}  ─────> {red}FAILED TO EXTRACT ! ")

    except Exception as e:
        print(f"[ERROR] Error extracting account: {uid}. Reason: {str(e)}")

def extract_fb_pages(token):
    url = 'https://graph.facebook.com/v18.0/me/accounts'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    
    pages_data = []
    
    while url:
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            print(f'Error: {response.text}')
            return None
        
        data = response.json()
        for page in data.get('data', []):
            pages_data.append({
                'id': page.get('id'),
                'accessToken': page.get('access_token')
            })
        
        url = data.get('paging', {}).get('next')  # Update the URL for the next request

    return pages_data

def prozc(accounts_file, token_output_path, extract_type):
    success_count = []
    existing_tokens = load_existing_tokens(token_output_path)

    try:
        with open(accounts_file, 'r') as file:
            accounts = file.readlines()

        accounts = [line.strip() for line in accounts if '|' in line.strip()]

        if not accounts:
            print(f"No valid accounts found in {accounts_file}.")
            return

        with thread.ThreadPoolExecutor(max_workers=30) as executor:
            futures = [executor.submit(bgraph_page, uid, pw, token_output_path, extract_type, success_count, existing_tokens)
                       for uid, pw in [account.split('|') for account in accounts]]

            for future in futures:
                future.result()

        print("\033[1;37m───────────────────────────────────────────────────────────────\033[0m")
        print(f"     \033[1;34m[SUCCESS]\033[0m: {len(success_count)} {extract_type}(s) successfully extracted.")
        print("\033[1;37m───────────────────────────────────────────────────────────────\033[0m")

    except FileNotFoundError:
        print(f"File not found: {accounts_file}")
def extraction():

    clear_screen()
    jovan()
    print(f"     {white}[1] {yellow}EXTRACT {red}ACCOUNT")
    print(f"     {white}[2] {yellow}EXTRACT {red}PAGES")
    print("     \033[1;34m───────────────────────────────────────────────────────────────\033[0m")
    choice = input(f"     {green}CHOICE: ").strip() 
    if choice == '1':
        axl1()
    elif choice == '2':
        axl2()
    else:
        print(f"     {red}INVALID CHOICE")
def axl2():
    clear_screen()
    jovan()
    folder_path = "/sdcard/boostphere"  
    print(f"    \033[34m───────────────────────────────────────────────────────────────\033[0m")
    print(f"     \033[31m[01] \033[32mFRA EXTRACT ACCOUNT")
    print(f"     \033[31m[02] \033[32mFRA EXTRACT PAGES")
    print(f"     \033[31m[03] \033[32mRPW EXTRACT ACCOUNT")
    print(f"     \033[31m[04] \033[32mRPW EXTRACT PAGES")
    print(f"    \033[34m───────────────────────────────────────────────────────────────\033[0m")
    save_choice = input(f"     \033[32mCHOICE: ").strip()

    if save_choice == '1':
        account_file = os.path.join(folder_path, "FRAACCOUNT.txt")
        extract_type = 'account'
    elif save_choice == '2':
        account_file = os.path.join(folder_path, "FRAPAGES.txt")
        extract_type = 'page'
    elif save_choice == '3':
        account_file = os.path.join(folder_path, "RPWACCOUNT.txt")
        extract_type = 'account'
    elif save_choice == '4':
        account_file = os.path.join(folder_path, "RPWPAGES.txt")
        extract_type = 'page'
    else:
        print("Invalid choice. Exiting.")
        return

    print(f"    \033[34m───────────────────────────────────────────────────────────────\033[0m")
    print(f"     \033[33mTHE FORMAT SHOULD BE \033[31muid|pass")
    print(f"    \033[34m───────────────────────────────────────────────────────────────\033[0m")
    file_path = input(f"     \033[33mPATH: ").strip()

    prozc(file_path, account_file, extract_type)
def axl1():
    clear_screen()
    jovan()
    folder_path = "/sdcard/boostphere"
    print(f"    \033[34m───────────────────────────────────────────────────────────────\033[0m")
    print(f"     \033[31m[01] \033[32mFRA EXTRACT ACCOUNT")
    print(f"     \033[31m[02] \033[32mFRA EXTRACT PAGES")
    print(f"     \033[31m[03] \033[32mRPW EXTRACT ACCOUNT")
    print(f"     \033[31m[04] \033[32mRPW EXTRACT PAGES")
    print(f"    \033[34m───────────────────────────────────────────────────────────────\033[0m")
    save_choice = input(f"     \033[32mCHOICE: ").strip()

    if save_choice == '1':
        account_file = os.path.join(folder_path, "FRAACCOUNT.txt")
        extract_type = 'account'
    elif save_choice == '2':
        account_file = os.path.join(folder_path, "FRAPAGES.txt")
        extract_type = 'page'
    elif save_choice == '3':
        account_file = os.path.join(folder_path, "RPWACCOUNT.txt")
        extract_type = 'account'
    elif save_choice == '4':
        account_file = os.path.join(folder_path, "RPWPAGES.txt")
        extract_type = 'page'
    else:
        print("Invalid choice. Exiting.")
        return

    print(f"    \033[34m───────────────────────────────────────────────────────────────\033[0m")
    print(f"     \033[33mTHE FORMAT SHOULD BE \033[31muid|pass")
    print(f"    \033[34m───────────────────────────────────────────────────────────────\033[0m")
    file_path = input(f"     \033[33mPATH: ").strip()

    token_output_path = account_file

    proz(file_path, token_output_path, extract_type)
def jovan():
    adrkz = "\033[34m "
    print(f"""
    {adrkz} 
            ██╗███╗   ██╗██████╗ ██╗ ██████╗  ██████╗ 
            ██║████╗  ██║██╔══██╗██║██╔════╝ ██╔═══██╗
            ██║██╔██╗ ██║██║  ██║██║██║  ███╗██║   ██║
            ██║██║╚██╗██║██║  ██║██║██║   ██║██║   ██║
            ██║██║ ╚████║██████╔╝██║╚██████╔╝╚██████╔╝
            ╚═╝╚═╝  ╚═══╝╚═════╝ ╚═╝ ╚═════╝  ╚═════╝
     {blue}───────────────────────────────────────────────────────────────\033[0m""")

def get_token_from_file(file_path):
    """Read tokens from the file and return a random token."""
    with open(file_path, 'r') as file:
        lines = file.readlines()
        tokens = [line.strip().split('|')[1] for line in lines if '|' in line]
    return random.choice(tokens)

class FacebookPoster:
    def __init__(self, link):
        self.link = link

    def share_post(self, token):
        """Shares a post on the user's feed with 'Only Me' privacy."""
        url = "https://graph.facebook.com/v13.0/me/feed"
        payload = {
            'link': self.link,
            'published': '0',
            'privacy': '{"value":"SELF"}',
            'access_token': token
        }
        try:
            response = requests.post(url, data=payload)
            if response.status_code == 200:
                print(f"    {blue}───────────────────────────────────────────────────────────────\033[0m")
                print("      Successfully Shared")
                return True
            else:
                return False
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return False

def share_in_threads(link, file_path, num_shares):
    start_all = time.time()  # Record the start time for the entire operation
    
    def worker():
        success = False
        while not success:
            token = get_token_from_file(file_path)
            fb_poster = FacebookPoster(link)
            success = fb_poster.share_post(token)

    max_workers = 40
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for _ in range(num_shares):
            executor.submit(worker)

    end_all = time.time()  # Record the end time for the entire operation
    duration = end_all - start_all
    print(f"    {blue}───────────────────────────────────────────────────────────────\033[0m")
    print(f"\n  {yellow}Sharing started: {start_all}")
    print(f"    {blue}───────────────────────────────────────────────────────────────\033[0m")
    print(f"     {yellow}Sharing ended: {end_all}")
    print(f"    {blue}───────────────────────────────────────────────────────────────\033[0m")
    print(f"    {yellow}Total duration: {duration:.2f} seconds\033[0m")
def count_tokens(accounts_file, pages_file):
    """Count the number of accounts and pages stored in the respective files."""
    total_accounts = 0
    total_pages = 0

    try:
        with open(accounts_file, 'r') as af:
            total_accounts = sum(1 for line in af if line.strip())  # Count non-empty lines
    except FileNotFoundError:
        print(f"Account file not found: {accounts_file}")

    try:
        with open(pages_file, 'r') as pf:
            total_pages = sum(1 for line in pf if line.strip())  # Count non-empty lines
    except FileNotFoundError:
        print(f"Page file not found: {pages_file}")

    return total_accounts, total_pages
def share():
    clear_screen()
    jovan()
    print(f"""     \033[1;37mCHOOSE TYPE OF ACCOUNTS TO AUTO SHARE: 
     \033[1;34m[1] \033[1;32mFRA ACCOUNT 
     \033[1;34m[2] \033[1;32mFRA PAGES
     \033[1;34m[3] \033[1;32mRPW ACCOUNT
     \033[1;34m[4] \033[1;32mRPW PAGES
     \033[1;31m[0] \033[1;31mEXIT 
    \033[1;34m───────────────────────────────────────────────────────────────\033[0m""")
    choice = input(f"     {blue}Choice ")
    
    file_map = {
        '1': '/sdcard/boostphere/FRAACCOUNT.txt',
        '2': '/sdcard/boostphere/FRAPAGES.txt',
        '3': '/sdcard/boostphere/RPWACCOUNT.txt',
        '4': '/sdcard/boostphere/RPWACCOUNT.txt'
    }

    file_path = file_map.get(choice)
    if not file_path:
        print("Invalid choice. Exiting.")
        return

    print(f"    {blue}───────────────────────────────────────────────────────────────\033[0m")
    post_id = input(f"   {yellow}Enter the post ID to share: ")
    print(f"    {blue}───────────────────────────────────────────────────────────────\033[0m")
    num_shares = int(input(f"   {blue}Limit: "))

    # Construct the link using the post ID
    link = f"https://www.facebook.com/{post_id}"

    share_in_threads(link, file_path, num_shares)
def main2(): 
    open('/sdcard/boostphere/FRAACCOUNT.txt', 'a').write('')
    open('/sdcard/boostphere/FRAPAGES.txt', 'a').write('')
    open('/sdcard/boostphere/RPWACCOUNT.txt', 'a').write('')
    open('/sdcard/boostphere/RPWACCOUNT.txt', 'a').write('')
    fraaccounts_file = '/sdcard/boostphere/FRAACCOUNT.txt'
    frapages_file = '/sdcard/boostphere/FRAPAGES.txt'
    rpwaccounts = '/sdcard/boostphere/RPWACCOUNT.txt'
    rpwpages = '/sdcard/boostphere/RPWPAGES.txt'
    total_accounts, total_pages = count_tokens(fraaccounts_file, frapages_file)
    total_account_rpw, total_pages_rpw = count_tokens(rpwaccounts,rpwpages)
    clear_screen()
    jovan()
    print(f"""                 {yellow}OVERVIEW OF STORED ACCOUNT & PAGES💫
          
                            {blue}FRA ACCOUNT{yellow} : {green}{total_accounts}
                            {blue}FRA PAGES  {yellow} : {green}{total_pages}
                            {blue}RPW ACCOUNT{yellow} : {green}{ total_account_rpw}
                            {blue}RPW PAGES  {yellow} : {green}{total_pages_rpw}
      {blue}───────────────────────────────────────────────────────────────\033[0m""")
    print(f"     {blue}[1] {yellow}EXTRACT ACCOUNT")
    print(f"     {blue}[2] {yellow}AUTO SHARE ")
    print(f"    {blue}───────────────────────────────────────────────────────────────\033[0m")
    choice = input(f'    {yellow}Enter Choice: ')
    if choice == '1': 
        extraction()
    if choice == '2': 
        share()

if __name__ == "__main__":
    main2()

