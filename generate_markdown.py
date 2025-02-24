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


if not USER_TOKEN:
    raise ValueError("❌ Error: Missing required environment variables `GITHUB_TOKEN`.")

if not USERNAME:
    raise ValueError("❌ Error: Missing required environment variables `USER_NAME`.")

if not BIRTHDAY:
    raise ValueError("❌ Error: Missing required environment variables `BIRTHDAY`.")

GITHUB_API_USER = "https://api.github.com/users/"
GITHUB_API_GRAPHQL = "https://api.github.com/graphql"

try:
    user_data = fetch_user_data(USERNAME)
    total_repos, total_stars = fetch_repo_and_star()
    last_year_commits = fetch_last_year_commits()
    all_time_commits = fetch_all_commits()
    total_additions, total_deletions = fetch_total_lines()
    if None in (user_data, total_repos, total_stars, last_year_commits, all_time_commits):
        print("❌ Error: Failed to retrieve necessary data. Exiting.")
        exit(1)
    net_lines = total_additions - total_deletions if total_additions is not None and total_deletions is not None else "N/A"
except Exception as e:
    print(f"❌ Failed to fetch GitHub data: {e}")
    exit(1)


ascii_avatar = convert_picture_to_ascii(120)

readme_content = f"""### 🚀 Optimizing the Digital World, One Line of Code at a Time

I'm a software developer fascinated by performance, efficiency, and low-level computing. My journey began at 12 when I tried to fix a sluggish laptop—what started as simple tweaks led to a passion for operating systems, automation, and writing optimized code.

I believe software should be clean, resource-efficient, and powerful without unnecessary overhead. From AI-driven image processing to low-level system automation, I build tools that push performance limits while keeping things lightweight.

Every project I work on is a challenge to solve real-world problems with better, faster, and smarter software—because innovation isn’t just about adding more, but making the most of what we have.

### 🧰 Languages and Tools

<p align="left">
  <img alt="Linux" width="30px" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/linux/linux-original.svg" />
  <img alt="Windows" width="30px" src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/windows11/windows11-original.svg" />
  <img alt="Git" width="30px" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/git/git-original.svg" />
  <img alt="C" width="30px" src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/c/c-original.svg" />
  <img alt="Python" width="30px" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-plain.svg" />
  <img alt="Java" width="30px" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/java/java-original.svg" />
  <br>
  <img alt="TypeScript" width="30px" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/typescript/typescript-plain.svg" />
  <img alt="JavaScript" width="30px" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/javascript/javascript-plain.svg" />
  <img alt="HTML" width="30px" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/html5/html5-plain.svg" />
  <img alt="CSS" width="30px" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/css3/css3-plain.svg" />
  <img alt="React" width="30px" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/react/react-original.svg" />
  <img alt="NodeJS" width="30px" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/nodejs/nodejs-original.svg" />
  <br>
  <img alt="Jenkins" width="30px" src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/jenkins/jenkins-original.svg" />
  <img alt="Docker" width="30px" src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/docker/docker-original-wordmark.svg" />
  <img alt="Redis" width="30px" src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/redis/redis-original-wordmark.svg" />
  <img alt="MongoDB" width="30px" src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/mongodb/mongodb-original-wordmark.svg" />
</p>

### 👤 {user_data["account_name"]}'s GitHub Stats

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
<p>This README is updated automatically by Jenkins.</p>
"""

try:
    with open("README.md", "w", encoding="utf-8") as file:
        file.write(readme_content)
        print("✅ README.md successfully updated!")
except IOError as e:
    print("❌ Failed to write README.md: {e}")
    exit(1)