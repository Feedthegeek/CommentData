"""
CommentData

Author: Nicholas D Herrick
Date: 2024-04-24
License: Personal

This python module reads Reddit comments from Reddit API, sorting by 10 newest posts from a declared subreddit.
Then, store, sort and write the information and content to a text file.
"""

import praw
from datetime import datetime
import pytz
from typing import List

""" 
Set up Reddit API
"""
reddit = praw.Reddit(
    client_id="WX8uWSBjqpQfJ8Ki6nQWww",
    client_secret="qCZzsYtxpJaeyk2iy9HzGslhUUShkg",
    user_agent="CommentData",

)

"""
Check is subreddit exists and return boolean
"""


def check_subreddit():
    while True:
        # get subreddit name from input from user
        subreddit_name = input("Please enter then name of the subreddit you want to scrape: ")
        # Check if subreddit exists
        try:
            reddit.subreddit(subreddit_name)
            print_confirm(subreddit_name)
            break  #exit if subreddit exists
        except Exception:
            print(f"Sorry, {subreddit_name} was not found. Please try again.")


"""
Obtain comments from subreddit if subreddit is valid
"""


def get_comments(subreddit_name: str) -> List[dict]:
    subreddit = reddit.subreddit(subreddit_name)  # Assign subreddit name
    comments_data = []  # Create empty list to store comment data
    for post in subreddit.new(limit=10):  # Iterate through new posts
        # Checks if comment is stickied, then iterates over comments in post
        comments = [comment for comment in post.comments if not comment.stickied]
        # Append comment details as listed to comments_data []
        comments_data.extend([{
            'title': post.title,
            'link': post.url,
            'title_time': post.created_utc,
            'id': comment.id,
            'author': comment.author,
            'text': comment.body,
            'timestamp': est_tz.localize(datetime.fromtimestamp(comment.created_utc)),
        } for comment in comments])
    # Sort comments by title, title timestamp, and then comment timestamp
    return sorted(comments_data, key=lambda x: (x['title'], x['title_time'], x['timestamp']))


"""
Write to file function, converts utc-8 to declared timezone in main
"""


def write_to_file(comments_data, output_file_path: str):
    try:
        # Write the data to the file
        with open(output_file_path, 'w', encoding='utf-8') as outfile:
            for comment_info in comments_data:
                outfile.write(f"Post Title : {comment_info['title']}\n")
                outfile.write(f"I.D.: {comment_info['id']}\n")
                outfile.write(f"Author: {comment_info['author']}\n")
                outfile.write(f"Text: {comment_info['text']}\n")
                timestamp = comment_info['timestamp'].strftime('%Y-%m-%d %I:%M %p')
                outfile.write(f"Timestamp: {timestamp}\n")
                outfile.write(f"URL: {comment_info['link']}\n\n")
    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print(F"An error occurred: {e}")


"""
Print confirmation of success and filepath
"""


def print_confirm(subreddit_name: str):
    print(f"You've chosen the subreddit: {subreddit_name}")
    print(f"Reading Reddit comments from {subreddit_name}...")
    output_file_path = fr'D:\AI\{subreddit_name}.txt'
    comments_data = get_comments(subreddit_name)
    write_to_file(comments_data, output_file_path)
    print(f"Writing to {output_file_path}...")
    print("Write to file successful.")


"""
Run program, if subreddit is valid.
"""
if __name__ == '__main__':
    est_tz = pytz.timezone('US/Eastern')  # Set to your desired time zone
    # assign subreddit name
    try:
        check_subreddit()

    except Exception as e:
        print(f"Sorry, an error occurred: {e}.")
