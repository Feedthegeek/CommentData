*CommentData*
================

This Python script uses the PRAW (Python Reddit API Wrapper) library to read Reddit comments from a specified subreddit, sort them by newest posts, and store the information in a text file.

*Usage*
--------

1. Run the script and enter the name of the subreddit you want to scrape.
2. The script will check if the subreddit exists and prompt you to try again if it doesn't.
3. Once a valid subreddit is entered, the script will retrieve the latest 10 posts and their corresponding comments.
4. The comments are sorted by post title, timestamp, and then comment timestamp.
5. The script writes the comment data to a text file with the same name as the subreddit.

*Requirements*
--------------

* PRAW (Python Reddit API Wrapper) library
* pytz library for timezone conversion

*Timezone Conversion*
--------------------

The script uses the US/Eastern timezone for converting UTC timestamps to local time. You can modify this setting to suit your needs.

*Note*
-----

Please be aware that scraping Reddit comments may be against Reddit's terms of service. Use at your own risk!

*Author*
---------

Nicholas D Herrick

*License*
---------

Personal license. Feel free to use and modify the script as needed.

*Acknowledgments*
----------------

Thanks to the PRAW developers for creating an awesome library!