import requests
import sys

def download_url_last_result(TOKEN: str, owner: str, repo: str, to_fetch: str) -> str:
    "This function will be used to fetch id of the last specific artifact to generate allure report"
    curl = f"https://api.github.com/repos/{owner}/{repo}/actions/artifacts"
    headers = {
        "Accept" : "application/vnd.github+json",
        "Authorization" : TOKEN,
        "X-GitHub-Api-Version" : "2022-11-28"
    }
    r = requests.get(curl + f"?name={to_fetch}", headers=headers)
    data = r.json()
    if r.status_code == 200:
        if data["total_count"] != 0:
            return data['artifacts'][0]['archive_download_url']
        else:
            return "EMPTY"
    else:
        raise ConnectionError(f'Status connection is off for your spec: owner = {owner}, repo = {repo}, fetch = {to_fetch}\n'
                              f'Your data = {data}\n'
                              f'Status = {r.status_code}')


if __name__ == "__main__":
    download_url_last_result(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
