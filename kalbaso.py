import os
import time
import sys
import subprocess

class Colors:
    CYAN = '\033[96m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    WHITE = '\033[97m'
    MAGENTA = '\033[95m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

CHANNELS = {
    "1": {"name": "BRAZIL (Pardinho)", "desc": "HF/VHF Live Radio", "url": "http://appr.org.br:8901/"},
    "2": {"name": "NETHERLANDS (Twente)", "desc": "Wideband SDR", "url": "http://websdr.ewi.utwente.nl:8901/"},
    "3": {"name": "NETHERLANDS (Maasbree)", "desc": "VHF SDR", "url": "http://sdr.maasbree.nl:8901/"},
    "4": {"name": "GLOBAL MAP", "desc": "WebSDR Directory", "url": "http://websdr.org/"},
}

def play_stream(url):
    print(f"\n{Colors.YELLOW}[>] Connecting to {url}...{Colors.RESET}")
    try:
        subprocess.Popen(['termux-open', url])
        print(f"{Colors.GREEN}[✔] Opened in your browser.{Colors.RESET}")
    except:
        print(f"{Colors.RED}[-] Failed to open. Please use your browser manually.{Colors.RESET}")

def show_panel():
    os.system('clear')
    print(f"""
{Colors.CYAN}╔══════════════════════════════════════════════════════════════╗{Colors.RESET}
{Colors.CYAN}║  {Colors.WHITE}KALBASO {Colors.CYAN}WebSDR Receiver{Colors.RESET}                             {Colors.CYAN}║{Colors.RESET}
{Colors.CYAN}╚══════════════════════════════════════════════════════════════╝{Colors.RESET}

{Colors.BLUE}  CH   NAME                          DESCRIPTION                 {Colors.RESET}
{Colors.GREEN}────────────────────────────────────────────────────────────────{Colors.RESET}
""")
    for key, ch in CHANNELS.items():
        print(f"  {Colors.YELLOW}[{key}]{Colors.RESET}  {Colors.WHITE}{ch['name']:<30}{Colors.RESET} {Colors.CYAN}{ch['desc']:<25}{Colors.RESET}")
    print(f"""{Colors.GREEN}────────────────────────────────────────────────────────────────{Colors.RESET}
  {Colors.RED}[0]{Colors.RESET}  {Colors.WHITE}POWER OFF / EXIT{Colors.RESET}
{Colors.GREEN}────────────────────────────────────────────────────────────────{Colors.RESET}
{Colors.CYAN}[+] MODE: STANDBY | WAITING FOR YOUR COMMAND{Colors.RESET}
{Colors.CYAN}❯ {Colors.RESET}""", end='')

def main():
    while True:
        show_panel()
        choice = input().strip()
        if choice in CHANNELS:
            play_stream(CHANNELS[choice]["url"])
            input(f"\n{Colors.BLUE}[!] Press Enter to return...{Colors.RESET}")
        elif choice == "0":
            print(f"\n{Colors.RED}[!] Goodbye!{Colors.RESET}")
            break
        else:
            print(f"\n{Colors.RED}[-] Invalid selection.{Colors.RESET}")
            time.sleep(1)

if __name__ == "__main__":
    main()

