import requests
import threading
from concurrent.futures import ThreadPoolExecutor
import random
import time

# Color codes for formatting output
purple = "\033[1;35m"
blue = "\033[34m"
green = "\033[1;32m"
red = "\033[1;31m"
yellow = "\033[1;33m"
white = "\033[1;37m"

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

def main():
    jovan()
    print(f"""     \033[1;37mCHOOSE TYPE OF ACCOUNTS TO JOIN GROUP: 
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

if __name__ == "__main__":
    main()
