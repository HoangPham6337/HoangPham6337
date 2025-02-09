import os
import urllib.request
from datetime import datetime
from ascii_magic import AsciiArt
from get_user_data import (
    fetch_user_data,
    fetch_repo_and_star,
    fetch_last_year_commits,
    fetch_all_commits,
    fetch_total_lines,
)
from image_to_ascii import convert_picture_to_ascii
from calculate_age import (
    calculate_account_age,
    calculate_my_age
)

USER_TOKEN = os.environ['ACCESS_TOKEN']
USERNAME = os.environ['USER_NAME']
BIRTHDAY = os.environ['BIRTHDAY']
GITHUB_API_USER = "https://api.github.com/users/"
GITHUB_API_GRAPHQL = "https://api.github.com/graphql"

user_data = fetch_user_data(USERNAME)
total_repos, total_stars = fetch_repo_and_star()
last_year_commits = fetch_last_year_commits()
all_time_commits = fetch_all_commits()

total_additions, total_deletions = fetch_total_lines()

net_lines = total_additions - total_deletions if total_additions is not None and total_deletions is not None else "N/A"

ascii_avatar = convert_picture_to_ascii(120)

readme_content = f"""{user_data["account_name"]}'s GitHub Stats

<table>
<tr>
<td>
{ascii_avatar}
</td>
<td>

👤 **Username:** Pham Xuan Hoang  
📅 **Age:** {calculate_my_age(BIRTHDAY)["years"]} years, {calculate_my_age(BIRTHDAY)["days"]} days  
📅 **Account Age:** {calculate_account_age(USERNAME)["years"]}, {calculate_account_age(USERNAME)["days"]} days  
📦 **Repositories:** {total_repos}  
🌟 **Stars:** {total_stars}  
📌 **Commits (Last Year):** {last_year_commits}  
📌 **Commits (All-Time):** {all_time_commits}  
🔥 **Lines of Code Added:** {total_additions}  
🔥 **Lines of Code Deleted:** {total_deletions}  
🔥 **Net Lines of Code:** {net_lines}  
_Last updated on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}_  
</td>
</tr>
</table>
"""


with open("README.md", "w", encoding="utf-8") as file:
    file.write(readme_content)

print("Operation complete")