import requests
import json
import time
import os
import subprocess

# GitHub repository releases URL (change this if you don't want the ergo releases)
repo_url = "https://api.github.com/repos/ergoplatform/ergo/releases"

# File to store information about the latest release
last_release_file = "last_release.json"

# Function to forward a message to Nostr using noscl
def forward_to_nostr(message_content):
    try:
        subprocess.run(['./noscl', 'publish', message_content], check=True)
    except subprocess.CalledProcessError as e:
        print(f'Failed to forward the message to Nostr. Error: {e}')
    except Exception as e:
        print(f'Error while forwarding message to Nostr: {e}')

def fetch_latest_release():
    response = requests.get(repo_url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch releases:", response.status_code)
        return None

def check_for_new_release():
    latest_release = fetch_latest_release()
    if latest_release:
        if os.path.exists(last_release_file):
            with open(last_release_file, "r") as file:
                last_release = json.load(file)
        else:
            last_release = {}

        if latest_release[0]['tag_name'] != last_release.get('tag_name'):
            message = f"🚀 New release: {latest_release[0]['name']} ({latest_release[0]['tag_name']})\n\n{latest_release[0]['body']}\n\nCheck it out here: {latest_release[0]['html_url']}"
            forward_to_nostr(message)  # Forward the message to Nostr

            last_release = {
                "tag_name": latest_release[0]['tag_name']
            }
            with open(last_release_file, "w") as file:
                json.dump(last_release, file)

def main():
    while True:
        check_for_new_release()
        time.sleep(3600)  # Check every hour

if __name__ == "__main__":
    if not os.path.exists(last_release_file):
        with open(last_release_file, "w") as file:
            file.write("{}")
    main()
