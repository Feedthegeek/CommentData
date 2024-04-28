"""
CommentData

Author: Nicholas D Herrick
Date: 2024-04-24
License: Personal

This python module reads Reddit comments from Reddit API, sorting by 10 newest posts from a declared subreddit.
Then, store, sort and write the information and content to a text file.
To use this script, you'll need to replace the client_id, client_secret, and user_agent with your own
Reddit API credentials.
"""

import praw
from praw import exceptions
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
Check is subreddit exists and return subreddit name
"""


def get_valid_subreddit():
    while True:
        subreddit_name = input("Please enter the name of the subreddit you want to scrape: ")
        try:
            subreddit = reddit.subreddit(subreddit_name)
            # Fetch subreddit data to ensure it exists
            if len(list(subreddit.new(limit=1))) > 0:
                print(f"You've chosen the subreddit: {subreddit_name}")
                return subreddit.display_name
            else:
                print(f"Sorry, the subreddit {subreddit_name} doesn't exist")

        except praw.exceptions.RedditAPIException as e:
            if e.error_type == "NOT_FOUND":
                print(f"Sorry, the subreddit '{subreddit_name}' was not found. Please try again.")
            else:
                print(f"Sorry, an error occurred: {e}")
        except Exception:
            print(f"'{subreddit_name}' was not found. Please try again.")



"""
Obtain comments if subreddit is valid, sorted by 10 newest posts from declared subreddit.
Return comment data in sorted list.
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
Write to file function, parses comment data and writes to a text file, formatted.
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
                timestamp = comment_info['timestamp'].strftime('%Y-%m-%d %I:%M %p')  # Format timestamp to 12HR, XX:XX
                outfile.write(f"Timestamp: {timestamp}\n")
                outfile.write(f"URL: {comment_info['link']}\n\n")
    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print(F"An error occurred: {e}")


"""
Obtain filepath from input, pass to write_to_file() function.
"""


def file_check(comments_data: List[dict]):
    # Obtain and check input for filepath
    while True:
        output_file_path = input(
            "Please enter the file path where you want to save the comments (default is 'D:\\AI\\{}\\.txt'): ".format(
                subreddit_name))
        if output_file_path != "":
            break
        else:
            output_file_path = fr"D:\AI\{subreddit_name}.txt"
            break
    write_to_file(comments_data, output_file_path)
    print(f"Writing to {output_file_path}...")
    print("Write to file successful.")


"""
Run program, if subreddit is valid.
"""
if __name__ == '__main__':
    est_tz = pytz.timezone('US/Eastern')  # Set to desired time zone

    try:
        subreddit_name = get_valid_subreddit()

        print(f"Reading Reddit comments from {subreddit_name}...")

        comments_data = get_comments(subreddit_name)

        file_check(comments_data)

    except Exception as e:
        print(f"Sorry, an error occurred: {e}.")
