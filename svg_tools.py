import os
import re
from datetime import datetime
from lxml import etree
from get_user_data import (
    fetch_user_data,
    fetch_repo_and_star,
    fetch_last_year_commits,
    fetch_all_commits,
    fetch_total_lines,
)
from image_to_ascii import convert_picture_to_ascii
SVG_TEMPLATE = "template.svg"
SVG_OUTPUT = "github-stats.svg"

def update_svg():
    """
    Fetch GitHub stats and update the SVG profile card dynamically.
    """
    # Fetch user information
    user_data = fetch_user_data(os.environ["USER_NAME"])
    total_repos, total_stars = fetch_repo_and_star()
    last_year_commits = fetch_last_year_commits()
    all_time_commits = fetch_all_commits()
    total_additions, total_deletions = fetch_total_lines()
    net_lines = total_additions - total_deletions if total_additions and total_deletions else "N/A"

    # Download and embed profile picture
    ascii_avatar = convert_picture_to_ascii(20).split("\n")
    ascii_avatar = [
        re.sub(r'[^\x20-\x7E]', '', line) for line in ascii_avatar  # Keep only printable ASCII
    ]

    # Load the SVG template
    tree = etree.parse(SVG_TEMPLATE)
    root = tree.getroot()

    y_position = 30
    for line in ascii_avatar:
        text_element = etree.Element("text", x="20", y=str(y_position), font_size="8", fill="#FFFFFF", font_family="monospace")
        text_element.text = line
        root.append(text_element)
        y_position += 10  # Move each line down

    # Update text values in the SVG
    find_and_replace(root, "username", user_data['account_name'])
    find_and_replace(root, "age", "20 years, 339 days")  # Replace with dynamic age if needed
    find_and_replace(root, "repos", str(total_repos))
    find_and_replace(root, "stars", str(total_stars))
    find_and_replace(root, "loc_added", str(total_additions))
    find_and_replace(root, "loc_deleted", str(total_deletions))
    find_and_replace(root, "net_loc", str(net_lines))
    find_and_replace(root, "updated", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))



    # Save the modified SVG
    tree.write(SVG_OUTPUT, encoding="utf-8", xml_declaration=True)
    print(f"✅ SVG updated: {SVG_OUTPUT}")

def find_and_replace(root, element_id, new_text):
    """
    Finds an element in the SVG and updates its text value.
    """
    element = root.find(f".//*[@id='{element_id}']")
    if element is not None:
        element.text = new_text

if __name__ == "__main__":
    update_svg()