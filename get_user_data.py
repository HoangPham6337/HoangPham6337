from typing import Dict
import requests
import os

USER_TOKEN = os.environ['ACCESS_TOKEN']
print("user token: " + USER_TOKEN)
USERNAME = os.environ['USER_NAME']
GITHUB_API_USER = "https://api.github.com/users/"
GITHUB_API_GRAPHQL = "https://api.github.com/graphql"


def fetch_user_data(username: str) -> Dict[str, int]:
    response = requests.get(f"{GITHUB_API_USER}{username}").json()

    return {
        "account_name": response["login"],
        "name": response["name"],
        "avatar_url": response["avatar_url"],
        "followers": response["followers"],
        "following": response["following"],
        "public_repos": response["public_repos"],
    }


def fetch_repo_and_star() ->tuple[int, int] | tuple[None, None]:
    headers = {
        "Authorization": f"Bearer {USER_TOKEN}",
        "Content-Type": "application/json"
    }

    query = """
    query($login: String!, $cursor: String) {
      user(login: $login) {
        repositories(first: 100, after: $cursor) {
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
    total_repos = 0
    total_stars = 0

    while True:
        response = requests.post(GITHUB_API_GRAPHQL, json={"query": query, "variables": variables}, headers=headers)
        if response.status_code != 200:
            print(f"❌ Error: {response.status_code} - {response.json()}")
            return None, None

        data = response.json()
        user_data = data.get("data", {}).get("user", {})

        if total_repos == 0:
            total_repos = user_data.get("repositories", {}).get("totalCount", 0)

        repos = user_data.get("repositories", {}).get("edges", [])
        for repo in repos:
            total_stars += repo["node"]["stargazers"]["totalCount"]
    
        page_info = user_data.get("repositories", {}).get("pageInfo", {})
        if page_info.get("hasNextPage"):
            variables["cursor"] = page_info["endCursor"]
        else:
            break

    return total_repos, total_stars


def fetch_last_year_commits() -> int | None:
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
    response = requests.post(GITHUB_API_GRAPHQL, json={"query": query, "variables": variables}, headers=headers)

    if response.status_code != 200:
        print(f"❌ Error: {response.status_code} - {response.json()}")
        return None

    data = response.json()
    return data["data"]["user"]["contributionsCollection"]["contributionCalendar"]["totalContributions"]


def fetch_all_commits() -> tuple[int] | None:
    headers = {
        "Authorization": f"Bearer {USER_TOKEN}",
        "Content-Type": "application/json"
    }
    query = """
    query($login: String!, $cursor: String) {
      user(login: $login) {
        repositories(first: 100, after: $cursor) {
          totalCount
          edges {
            node {
              nameWithOwner
              defaultBranchRef {
                target {
                  ... on Commit {
                    history(first: 100) {
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
        response = requests.post(GITHUB_API_GRAPHQL, json={"query": query, "variables": variables}, headers=headers)

        if response.status_code != 200:
            print(f"❌ Error: {response.status_code} - {response.json()}")
            return None

        data = response.json()
        user_data = data.get("data", {}).get("user", {})

        repos = user_data.get("repositories", {}).get("edges", [])

        for repo in repos:
            if repo["node"]["defaultBranchRef"]:
                total_commits += repo["node"]["defaultBranchRef"]["target"]["history"]["totalCount"]

        page_info = user_data.get("repositories", {}).get("pageInfo", {})
        if page_info.get("hasNextPage"):
            variables["cursor"] = page_info["endCursor"]
        else:
            break
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
    total_additions = 0
    total_deletions = 0

    while True:
        response = requests.post(GITHUB_API_GRAPHQL, json={"query": query, "variables": variables}, headers=headers)

        if response.status_code != 200:
            print(f"❌ Error: {response.status_code} - {response.json()}")
            return None, None

        data = response.json()
        user_data = data.get("data", {}).get("user", {})

        repos = user_data.get("repositories", {}).get("edges", [])
        for repo in repos:
            if repo["node"]["defaultBranchRef"]:
                commit_history = repo["node"]["defaultBranchRef"]["target"]["history"]["edges"]
                for commit in commit_history:
                    total_additions += commit["node"]["additions"]
                    total_deletions += commit["node"]["deletions"]

        page_info = user_data.get("repositories", {}).get("pageInfo", {})
        if page_info.get("hasNextPage"):
            variables["cursor"] = page_info["endCursor"]
        else:
            break

    return total_additions, total_deletions



if __name__ == "__main__":
    # print(fetch_user_data(USERNAME))
    # total_repos, total_stars = fetch_repo_and_star()
    # print(f"📦 Total Repositories: {total_repos}")
    # print(f"🌟 Total Stars Received: {total_stars}")
    # last_year_commits = fetch_last_year_commits()
    # all_time_commits = fetch_all_commits()
    #
    # print(f"📌 Commits in Last Year: {last_year_commits}")
    # print(f"📌 All-Time Commits: {all_time_commits}")

    total_additions, total_deletions = fetch_total_lines()

    print(f"🔥 Total Lines of Code Added: {total_additions}")
    print(f"🔥 Total Lines of Code Deleted: {total_deletions}")
    print(f"🔥 Net Lines of Code: {total_additions - total_deletions}")