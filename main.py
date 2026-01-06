import argparse
import csv
import sys
import time
import webbrowser
import requests

from config import CLIENT_ID, AUTH_URL, TOKEN_URL, API_URL


def authenticate_device_flow(client_id):
    """
    Executes the OAuth Device Flow to obtain an access token.
    """
    # 1. Request device code
    payload = {
        "client_id": client_id,
        "scope": "repo",  # Scope needed to read private repos
    }
    headers = {"Accept": "application/json"}

    response = requests.post(AUTH_URL, data=payload, headers=headers)

    if response.status_code != 200:
        print(f"❌ OAuth initialization error: {response.text}")
        sys.exit(1)

    data = response.json()
    device_code = data["device_code"]
    user_code = data["user_code"]
    verification_uri = data["verification_uri"]
    interval = data.get("interval", 5)

    # 2. Show instructions to the user
    print("\n🔐 LOGIN REQUIRED")
    print(f"The browser will open shortly. If not, go to: {verification_uri}")
    print(f"Enter this code: \033[1m{user_code}\033[0m")
    print("\n⏳ Waiting for authorization...", end="", flush=True)

    # Automatically open the browser
    try:
        webbrowser.open(verification_uri)
    except Exception:
        pass  # If auto-open fails, the user has the link printed above

    # 3. Polling for user approval
    while True:
        time.sleep(interval)

        token_payload = {
            "client_id": client_id,
            "device_code": device_code,
            "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
        }

        res = requests.post(TOKEN_URL, data=token_payload, headers=headers)
        token_data = res.json()

        if "access_token" in token_data:
            print("\n✅ Authentication successful!")
            return token_data["access_token"]

        error = token_data.get("error")

        if error == "authorization_pending":
            print(".", end="", flush=True)
            continue
        elif error == "slow_down":
            interval += 5
            print("(slow)", end="", flush=True)
        elif error == "expired_token":
            print("\n❌ Timed out. Please try again.")
            sys.exit(1)
        else:
            print(f"\n❌ Unexpected error: {error}")
            sys.exit(1)


def get_all_repos(token):
    """
    Fetches all repositories for the authenticated user, handling pagination.
    """
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }
    repos = []
    page = 1

    print("\n📥 Downloading repository list...", end="", flush=True)
    while True:
        url = f"{API_URL}?per_page=100&page={page}&type=all"
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print(f"\n❌ API Error: {response.status_code}")
            sys.exit(1)

        data = response.json()
        if not data:
            break

        repos.extend(data)
        print(".", end="", flush=True)
        page += 1

    print(f"\n📦 Total repositories found: {len(repos)}")
    return repos


def save_to_csv(repos, filename):
    """
    Saves the list of repository dictionaries to a CSV file.
    """
    if not repos:
        return

    # Data extraction and formatting
    rows = []
    for repo in repos:
        lic = repo.get("license")
        rows.append(
            {
                "owner": repo["owner"]["login"],
                "name": repo["name"],
                "primary_language": repo["language"] or "N/A",
                "stars": repo["stargazers_count"],
                "license": lic.get("spdx_id", "N/A") if lic else "None",
                "type": "Private" if repo["private"] else "Public",
                "archived": repo["archived"],
                "is_template": repo["is_template"],
                "is_mirror": bool(repo.get("mirror_url")),
                "is_fork": repo["fork"],
            }
        )

    # Get headers from the first dictionary keys
    keys = rows[0].keys()

    try:
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(rows)
        print(f"💾 File saved: {filename}")
    except IOError as e:
        print(f"❌ Save error: {e}")


def main():
    parser = argparse.ArgumentParser(description="GitHub Repo Exporter (OAuth)")
    parser.add_argument(
        "-o",
        "--output",
        default="repos.csv",
        help="Output filename (default: repos.csv)",
    )

    args = parser.parse_args()

    # 1. Interactive Login
    token = authenticate_device_flow(CLIENT_ID)

    # 2. Fetch Data
    repos = get_all_repos(token)

    # 3. Save to CSV
    save_to_csv(repos, args.output)


if __name__ == "__main__":
    main()
