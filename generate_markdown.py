import os
from datetime import datetime
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

USER_TOKEN = os.environ['GITHUB_TOKEN']
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
<h3>Personal details</h3>
<ul>
    <li><strong>Username:</strong> PHAM Xuan Hoang</li>
    <li><strong>Age:</strong> {calculate_my_age(BIRTHDAY)["years"]} years, {calculate_my_age(BIRTHDAY)["days"]} days</li>
</ul>

<h3>Hobbies</h3>
<ul>
    <li>Tweaking Operating Systems</li>
    <li>Coding</li>
    <li>Listening to music</li>
    <li>Reading books</li>
</ul>

<h3>Contacts</h3>
<ul>
    <li><strong>Email:</strong> hoangphamat0407@gmail.com</li>
    <li><strong>LinkedIn:</strong> <a href="https://www.linkedin.com/in/xuan-hoang-pham">Hoang Pham Xuan</a></li>
</ul>

<h3>GitHub stats</h3>
<ul>
    <li><strong>Account Age:</strong> {calculate_account_age(USERNAME)["years"]} years, {calculate_account_age(USERNAME)["days"]} days</li>
    <li><strong>Repositories:</strong> {total_repos}</li>
    <li><strong>Stars:</strong> {total_stars}</li>
    <li><strong>Commits (Last Year):</strong> {last_year_commits}</li>
    <li><strong>Commits (All-time):</strong> {all_time_commits}</li>
    <li><strong>Lines of Code Added:</strong> {total_additions}</li>
    <li><strong>Lines of Code Deleted:</strong> {total_deletions}</li>
    <li><strong>Net Lines of Code:</strong> {net_lines}</li>
</ul>

<p><em>Last updated on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</em></p>


</td>
</tr>
</table>
"""


with open("README.md", "w", encoding="utf-8") as file:
    file.write(readme_content)

print("Operation complete")