import requests
from datetime import datetime, timedelta
import csv

# GitHub API base URL
GITHUB_API_URL = "https://api.github.com/users/"
ACCESS_TOKEN = 'TOKEN12345'

# Function to fetch all repositories of a GitHub user (up to 1000 repositories)
def fetch_repositories(username):
    repos = []
    page = 1
    while True:
        repo_url = f"{GITHUB_API_URL}{username}/repos"
        params = {'per_page': 100, 'page': page}
        headers = {'Authorization': f'token {ACCESS_TOKEN}'}
        try:
            response = requests.get(repo_url, params=params, headers=headers)
            response.raise_for_status()
            batch = response.json()
            if not batch:
                break
            repos.extend([repo['name'] for repo in batch])
            if len(repos) >= 1000:
                repos = repos[:1000]
                break
            page += 1
        except requests.exceptions.RequestException as e:
            print(f"Error fetching repositories: {e}")
            break
    return repos

# Function to fetch commits from the last 365 days for a repository
def fetch_recent_commits(username, repo_name):
    commit_url = f"https://api.github.com/repos/{username}/{repo_name}/commits"
    commits = []
    params = {
        'since': (datetime.utcnow() - timedelta(days=365)).isoformat() + 'Z',
        'per_page': 100
    }
    headers = {'Authorization': f'token {ACCESS_TOKEN}'}

    try:
        while commit_url:
            response = requests.get(commit_url, params=params, headers=headers)
            response.raise_for_status()
            batch = response.json()
            if not batch:
                break
            commits.extend(batch)
            commit_url = response.links.get('next', {}).get('url')
        
        return len(commits)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching commits for {repo_name}: {e}")
        return 0

# Save statistics to a CSV file
def save_statistics_to_csv(stats, filename='statistics.csv'):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Repository', 'Commits in Last 365 Days'])
        for repo, commit_count in stats.items():
            writer.writerow([repo, commit_count])

# Main function
def main():
    username = "sourceduty"  # Replace with the GitHub username
    repositories = fetch_repositories(username)
    
    commit_stats = {}
    for repo in repositories:
        commit_count = fetch_recent_commits(username, repo)
        commit_stats[repo] = commit_count
    
    save_statistics_to_csv(commit_stats)

if __name__ == "__main__":
    main()
