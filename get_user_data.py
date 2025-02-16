import time
from sys import exec_prefix
from typing import Dict, Optional, Type
import requests
import os

from requests import Response

USER_TOKEN = os.environ['GITHUB_TOKEN'].strip()
USERNAME = os.environ['USER_NAME'].strip()

if not USER_TOKEN:
    raise ValueError("❌ Error: Missing required environment variables `GITHUB_TOKEN`.")

if not USERNAME:
    raise ValueError("❌ Error: Missing required environment variables `USER_NAME`.")

GITHUB_API_USER = "https://api.github.com/users/"
GITHUB_API_GRAPHQL = "https://api.github.com/graphql"


def fetch_user_data(username: str) -> Optional[Dict[str, int]]:
    url: str = f"{GITHUB_API_USER}{username}"
    for attempt in range(3):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            user_data = response.json()

            return {
                "account_name": user_data.get("login", "Unknown"),
                "name": user_data.get("name", "Unknown"),
                "avatar_url": user_data.get("avatar_url", ""),
                "followers": user_data.get("followers", 0),
                "following": user_data.get("following", 0),
                "public_repos": user_data.get("public_repos", 0),
            }
        except requests.exceptions.RequestException as e:
            print(f"⚠️ Warning: API request failed (attempt {attempt + 1}/3): {e}")
            time.sleep(2)
    print("❌ Error: Failed to fetch user data after 3 attempts.")
    return None


def fetch_data_api(api_link: str, query: str, headers: dict[str, str], variables: dict[str, str]) \
        -> Optional[Response]:
    headers.update({
        "Authorization": f"Bearer {USER_TOKEN}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    })
    try:
        response = requests.post(api_link, json={"query": query, "variables": variables}, headers=headers)
        response.raise_for_status()
        json_response = response.json()
        if "errors" in json_response:
            print(f"⚠️ GraphQL API returned errors: {json_response['errors']}")
            return None
        return response

    except requests.exceptions.RequestException as e:
        print(f"❌ Error: API request failed: {e}")
        return None


def fetch_repo_and_star() -> tuple[int, int] | tuple[None, None]:
    headers = {
        "Authorization": f"Bearer {USER_TOKEN}",
        "Content-Type": "application/json"
    }

    query = """
    query($login: String!, $cursor: String) {
      user(login: $login) {
        repositories(first: 50, after: $cursor) {
          totalCount
          edges {
            node {
              stargazers {
                totalCount
              }
            }
          }
          pageInfo {
            endCursor
            hasNextPage
          }
        }
      }
    }
    """

    variables = {"login": USERNAME, "cursor": None}
    total_repos, total_stars = 0, 0

    while True:
        response = fetch_data_api(GITHUB_API_GRAPHQL, query, headers, variables)
        if response is None:
            print("❌ Error: Failed to fetch repository data.")
            return None, None

        try:
            user_data = response.json()
        except ValueError:
            print("❌ Error: Failed to decode JSON. API might be down.")
            return None, None
        if "data" not in user_data or "user" not in user_data["data"]:
            print(f"⚠️ Warning: 'data' or 'user' missing in API response: {user_data}")
            return None, None

        user_info = user_data["data"]["user"]

        total_repos = user_info.get("repositories", {}).get("totalCount", 0)
        repos = user_info.get("repositories", {}).get("edges", [])

        for repo in repos:
            total_stars += repo["node"]["stargazers"]["totalCount"]

        page_info = user_info.get("repositories", {}).get("pageInfo", {})
        if page_info.get("hasNextPage"):
            variables["cursor"] = page_info["endCursor"]
        else:
            break

    return total_repos, total_stars


def fetch_last_year_commits() -> Optional[int]:
    """
    Fetch total commit count from GitHub's contribution calendar (last 12 months only).
    """
    headers = {
        "Authorization": f"Bearer {USER_TOKEN}",
        "Content-Type": "application/json"
    }

    query = """
    query($login: String!) {
      user(login: $login) {
        contributionsCollection {
          contributionCalendar {
            totalContributions
          }
        }
      }
    }
    """

    variables = {"login": USERNAME}
    response = fetch_data_api(GITHUB_API_GRAPHQL, query, headers, variables)
    if response is None:
        print("❌ API request failed: No response received.")
        return None
    try:
        data = response.json()
        total_commits = (data.get("data", {})
                         .get("user", {})
                         .get("contributionsCollection", {})
                         .get("contributionCalendar", {})
                         .get("totalContributions", 0)
                         )
        return total_commits
    except (KeyError, TypeError):
        print("⚠️ Warning: Unexpected response format in fetch_last_year_commits.")
        return None


def fetch_all_commits() -> tuple[int] | None:
    headers = {
        "Authorization": f"Bearer {USER_TOKEN}",
        "Content-Type": "application/json"
    }
    query = """
    query($login: String!, $cursor: String) {
      user(login: $login) {
        repositories(first: 50, after: $cursor) {
          totalCount
          edges {
            node {
              nameWithOwner
              defaultBranchRef {
                target {
                  ... on Commit {
                    history(first: 50) {
                      totalCount
                    }
                  }
                }
              }
            }
          }
          pageInfo {
            endCursor
            hasNextPage
          }
        }
      }
    }
    """
    variables = {"login": USERNAME, "cursor": None}
    total_commits = 0

    while True:
        response = fetch_data_api(GITHUB_API_GRAPHQL, query, headers, variables)
        if response is None: return None
        try:
            data = response.json()
            user_data = data.get("data", {}).get("user", {})

            repos = user_data.get("repositories", {}).get("edges", [])

            for repo in repos:
                if repo["node"].get("defaultBranchRef"):
                    total_commits += repo["node"]["defaultBranchRef"]["target"].get("history", {}).get("totalCount", {})

            page_info = user_data.get("repositories", {}).get("pageInfo", {})
            if page_info.get("hasNextPage"):
                variables["cursor"] = page_info["endCursor"]
            else:
                break
        except (KeyError, TypeError):
            print("⚠️ Warning: Unexpected response format in fetch_all_commits.")
            return None
    return total_commits


def fetch_total_lines() -> tuple[int, int] | tuple[None, None]:
    headers = {
        "Authorization": f"Bearer {USER_TOKEN}",
        "Content-Type": "application/json"
    }
    query = """
    query($login: String!, $cursor: String, $commitCursor: String) {
      user(login: $login) {
        repositories(first: 50, after: $cursor) {
          edges {
            node {
              defaultBranchRef {
                target {
                  ... on Commit {
                    history(first: 50, after: $commitCursor) {
                      edges {
                        node {
                          additions
                          deletions
                        }
                      }
                      pageInfo {
                        endCursor
                        hasNextPage
                      }
                    }
                  }
                }
              }
            }
          }
          pageInfo {
            endCursor
            hasNextPage
          }
        }
      }
    }
    """
    variables = {"login": USERNAME, "cursor": None}
    additions, deletions = 0, 0

    while True:
        response = fetch_data_api(GITHUB_API_GRAPHQL, query, headers, variables)
        if response is None:
            return None, None

        try:
            data = response.json()
            user_data = data.get("data", {}).get("user", {})

            repos = user_data.get("repositories", {}).get("edges", [])
            for repo in repos:
                if repo["node"].get("defaultBranchRef"):
                    commit_history = repo["node"]["defaultBranchRef"]["target"].get("history", {}).get("edges", [])
                    for commit in commit_history:
                        additions += commit["node"].get("additions", 0)
                        deletions += commit["node"].get("deletions", 0)

            page_info = user_data.get("repositories", {}).get("pageInfo", {})
            if page_info.get("hasNextPage"):
                variables["cursor"] = page_info["endCursor"]
            else:
                break
        except (KeyError, TypeError):
            print("⚠️ Warning: Unexpected response format in fetch_total_lines.")
            return None, None

    return additions, deletions


if __name__ == "__main__":
    print(fetch_user_data(USERNAME))
    all_repos, stars = fetch_repo_and_star()
    print(f"📦 Total Repositories: {all_repos}")
    print(f"🌟 Total Stars Received: {stars}")
    last_year_commits = fetch_last_year_commits()
    all_time_commits = fetch_all_commits()

    print(f"📌 Commits in Last Year: {last_year_commits}")
    print(f"📌 All-Time Commits: {all_time_commits}")

    total_additions, total_deletions = fetch_total_lines()

    print(f"🔥 Total Lines of Code Added: {total_additions}")
    print(f"🔥 Total Lines of Code Deleted: {total_deletions}")
    print(f"🔥 Net Lines of Code: {total_additions - total_deletions}")
