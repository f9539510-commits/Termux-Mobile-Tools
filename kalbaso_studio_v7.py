#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
====================================================================
 KALBASO TERMUX STUDIO v7.0
 Developer: Calypsu (كالبسو مطروح)
 Description: أداة متكاملة لمطوري تيرمكس (بحث ذكي + إعداد GitHub + رفع).
====================================================================
"""

import os
import sys
import time
import subprocess
import urllib.request
import json
import getpass
import configparser

# =========================================================
# 1. الألوان
# =========================================================
class C:
    RESET = "\033[0m"
    BOLD  = "\033[1m"
    CYAN  = "\033[96m"
    PINK  = "\033[95m"
    GREEN = "\033[92m"
    YELLOW= "\033[93m"
    RED   = "\033[91m"
    WHITE = "\033[97m"

# =========================================================
# 2. مسارات الملفات (للحفظ الآمن)
# =========================================================
CONFIG_DIR = os.path.expanduser("~/.kalbaso")
CONFIG_FILE = os.path.join(CONFIG_DIR, "git_config.ini")

# =========================================================
# 3. دوال مساعدة (الطباعة والتنسيق)
# =========================================================
def clear():
    os.system('clear')

def print_header():
    clear()
    print(f"""
{C.CYAN}╔══════════════════════════════════════════════════════════════════════╗{C.RESET}
{C.CYAN}║{C.RESET} {C.WHITE}KALBASO TERMUX STUDIO v7.0{C.RESET} | {C.CYAN}DEV: Calypsu{C.RESET} | {C.GREEN}STATUS: READY{C.RESET} {C.CYAN}║{C.RESET}
{C.CYAN}╚══════════════════════════════════════════════════════════════════════╝{C.RESET}
""")

def wait_enter():
    input(f"\n{C.BOLD}Press Enter to return...{C.RESET}")

def print_success(msg):
    print(f"\n{C.GREEN}╔══════════════════════════════════════════════════════════════════════╗{C.RESET}")
    print(f"{C.GREEN}║{C.RESET} {C.WHITE}{msg}{C.RESET}")
    print(f"{C.GREEN}╚══════════════════════════════════════════════════════════════════════╝{C.RESET}")

def print_error(msg, solution=""):
    print(f"\n{C.RED}╔══════════════════════════════════════════════════════════════════════╗{C.RESET}")
    print(f"{C.RED}║{C.RESET} {C.WHITE}ERROR: {msg}{C.RESET}")
    if solution:
        print(f"{C.RED}║{C.RESET} {C.YELLOW}Solution: {solution}{C.RESET}")
    print(f"{C.RED}╚══════════════════════════════════════════════════════════════════════╝{C.RESET}")

# =========================================================
# 4. إدارة إعدادات GitHub (حفظ آمن)
# =========================================================
def load_git_config():
    if not os.path.exists(CONFIG_FILE):
        return None
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    return config

def save_git_config(username, token):
    os.makedirs(CONFIG_DIR, exist_ok=True)
    config = configparser.ConfigParser()
    config['GitHub'] = {'Username': username, 'Token': token}
    with open(CONFIG_FILE, 'w') as f:
        config.write(f)
    os.chmod(CONFIG_FILE, 0o600)  # حماية الملف

# =========================================================
# 5. الميزات (المهام)
# =========================================================

# --- 1. إعداد GitHub (Setup) ---
def setup_github():
    clear()
    print_header()
    print(f"{C.YELLOW}[*] GitHub Account Setup{C.RESET}")
    print(f"{C.CYAN}This will save your GitHub credentials securely.{C.RESET}\n")
    
    username = input(f"{C.PINK}GitHub Username: {C.RESET}").strip()
    if not username:
        print_error("Username cannot be empty.")
        wait_enter()
        return
    
    print(f"{C.YELLOW}[!] You need a Personal Access Token (not password).{C.RESET}")
    print(f"{C.YELLOW}[!] Create one at: https://github.com/settings/tokens{C.RESET}")
    
    token = getpass.getpass(f"{C.PINK}GitHub Token (hidden): {C.RESET}").strip()
    if not token:
        print_error("Token cannot be empty.")
        wait_enter()
        return
    
    save_git_config(username, token)
    
    # إعداد git config (اختياري لتحسين تجربة git)
    subprocess.run(f'git config --global user.name "{username}"', shell=True)
    subprocess.run(f'git config --global user.email "{username}@users.noreply.github.com"', shell=True)
    
    print_success(f"GitHub Account saved for: {username}")
    wait_enter()

# --- 2. البحث الذكي (Smart Install) ---
def smart_install():
    clear()
    print_header()
    print(f"{C.YELLOW}[*] Smart Package Search & Install{C.RESET}")
    print(f"{C.CYAN}Enter package/tool name (e.g., requests, nmap, flask){C.RESET}")
    
    pkg = input(f"\n{C.PINK}package> {C.RESET}").strip()
    if not pkg:
        return

    print(f"\n{C.YELLOW}[*] Searching for '{pkg}'...{C.RESET}")
    
    # 1. محاولة البحث في PyPI (بايثون)
    pypi_found = False
    try:
        url = f"https://pypi.org/pypi/{pkg}/json"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())
            print(f"  {C.GREEN}[+] Found on PyPI: {data['info']['name']}{C.RESET}")
            pypi_found = True
    except:
        pass

    # 2. محاولة البحث في حزم النظام (pkg)
    if not pypi_found:
        print(f"  {C.YELLOW}[*] Not on PyPI. Searching System Packages (pkg)...{C.RESET}")
        cmd = f"pkg install {pkg} -y"
        print(f"  {C.GREEN}[>] Executing: {cmd}{C.RESET}")
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if "Unable to locate package" in result.stderr or "E: " in result.stderr:
            print_error(f"Package '{pkg}' not found in PyPI or System.", "Make sure the name is correct.")
        else:
            print_success(f"System Package '{pkg}' installed!")
        wait_enter()
        return

    # 3. تنزيل من PyPI
    if pypi_found:
        cmd = f"pip install {pkg}"
        print(f"  {C.GREEN}[>] Executing: {cmd}{C.RESET}")
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print_success(f"Python Package '{pkg}' installed!")
        else:
            print_error(f"Failed to install '{pkg}'.", "Check your internet connection.")
    
    wait_enter()

# --- 3. توليد سكريبت التثبيت (Setup Script) ---
def generate_setup():
    clear()
    print_header()
    print(f"{C.YELLOW}[*] Generate Setup Script{C.RESET}")
    print(f"{C.CYAN}This script will install all needed packages.{C.RESET}")
    
    pkgs = input(f"\n{C.PINK}Enter packages (e.g., requests colorama): {C.RESET}").strip()
    if not pkgs:
        return
    
    script = f"""#!/bin/bash
# KALBASO Setup Script
echo "Installing dependencies..."
pip install {pkgs}
echo "Done!"
"""
    filename = "setup.sh"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(script)
    os.chmod(filename, 0o755)
    print_success(f"Saved: {filename}")
    print(f"{C.YELLOW}[!] Run it using: bash {filename}{C.RESET}")
    wait_enter()

# --- 4. الرفع لـ GitHub (Push) ---
def push_to_github():
    clear()
    print_header()
    print(f"{C.YELLOW}[*] Push File to GitHub{C.RESET}")
    
    # التحقق من وجود إعدادات
    config = load_git_config()
    if not config:
        print_error("GitHub not configured.", "Please run 'Setup GitHub' first.")
        wait_enter()
        return

    # عرض الملفات الجاهزة
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    print(f"{C.CYAN}Files available for push:{C.RESET}")
    for i, f in enumerate(files, 1):
        print(f"  {C.GREEN}[{i}]{C.RESET} {f}")
    
    choice = input(f"\n{C.PINK}Select file number to push: {C.RESET}")
    try:
        idx = int(choice) - 1
        filename = files[idx]
    except:
        print_error("Invalid choice.", "Please enter a number from the list.")
        wait_enter()
        return

    print(f"\n{C.YELLOW}[*] Pushing '{filename}' to GitHub...{C.RESET}")
    
    # إعداد التوكن في الرابط (للتأكد من الرفع)
    username = config['GitHub']['Username']
    token = config['GitHub']['Token']
    
    # التحقق من وجود .git
    if not os.path.exists(".git"):
        print_error("Not a Git repository.", "Run 'git init' and 'git remote add origin <URL>' first.")
        wait_enter()
        return

    # إضافة ورفع
    cmd = f"git add {filename} && git commit -m 'Add {filename}' && git push https://{username}:{token}@github.com/{username}/{os.path.basename(os.getcwd())}.git"
    print(f"  {C.GREEN}[>] Executing Git Push...{C.RESET}")
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print_success(f"'{filename}' pushed to GitHub successfully!")
        else:
            print_error(f"Push failed.", "Check your internet, or token permissions.")
    except Exception as e:
        print_error(f"Error: {e}")
    
    wait_enter()

# =========================================================
# 6. الحلقة الرئيسية
# =========================================================
def main():
    while True:
        print_header()
        print(f"{C.CYAN}┌──[ STUDIO MENU ]{C.RESET}")
        print(f"{C.CYAN}│{C.RESET}  {C.GREEN}[1]{C.RESET} Smart Install (PyPI / System)")
        print(f"{C.CYAN}│{C.RESET}  {C.GREEN}[2]{C.RESET} Generate Setup Script")
        print(f"{C.CYAN}│{C.RESET}  {C.GREEN}[3]{C.RESET} Setup GitHub Account")
        print(f"{C.CYAN}│{C.RESET}  {C.GREEN}[4]{C.RESET} Push File to GitHub")
        print(f"{C.CYAN}│{C.RESET}  {C.RED}[0]{C.RESET} Exit")
        print(f"{C.CYAN}└──>{C.RESET}")
        
        choice = input(f"\n{C.PINK}studio> {C.RESET}").strip()
        
        if choice == "1":
            smart_install()
        elif choice == "2":
            generate_setup()
        elif choice == "3":
            setup_github()
        elif choice == "4":
            push_to_github()
        elif choice in ["0", "exit", "q"]:
            print(f"\n{C.YELLOW}[!] Goodbye!{C.RESET}")
            break
        else:
            print(f"{C.RED}[!] Invalid.{C.RESET}")
            time.sleep(1)

if __name__ == "__main__":
    main()

