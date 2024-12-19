import requests
import sys
import os

def download_url_last_result(TOKEN: str, owner: str, repo: str, to_fetch: str) -> None:
    "This function will be used to fetch id of the last specific artifact to generate allure report"
    curl = f"https://api.github.com/repos/{owner}/{repo}/actions/artifacts"
    headers = {
        "Accept" : "application/vnd.github+json",
        "Authorization" : TOKEN,
        "X-GitHub-Api-Version" : "2022-11-28"
    }
    r = requests.get(curl + f"?name={to_fetch}", headers=headers)
    data = r.json()
    env_file = os.getenv('GITHUB_ENV')
    if r.status_code == '200':
        with open(env_file, "a") as myenv:
            if data["total_count"] != 0:
                myenv.write(f"DOWNLOAD_LINK={data['artifacts'][0]['archive_download_url']}")
            else:
                myenv.write(f"DOWNLOAD_LINK=EMPTY")
    else:
        raise ConnectionError(f'Status connection is off for your spec: owner = {owner}, repo = {repo}, fetch = {to_fetch}')


if __name__ == "__main__":
    download_url_last_result(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])