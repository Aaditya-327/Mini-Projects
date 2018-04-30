# r/Gonewild
#!/usr/bin/env python3

import os
import praw # reddit API Wrapper
from urllib.error import URLError, HTTPError
import urllib.request as web
import shutil # shell utilities
import colorama
from colorama import Fore, Style


def main(subreddit_name = 'all', current_dir = os.getcwd()):
    number = 0
    reddit = praw.Reddit(
        client_id = '', 
        client_secret = '', 
        username = '', 
        password = '', 
        user_agent = 'User-Agent: android:com.example.myredditapp:v1.2.3 (by /u/kemitche)')

    dir_path = os.path.join(current_dir,subreddit_name)
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)

    colorama.init(autoreset = True)
    subreddit = reddit.subreddit(subreddit_name).top(limit=1000)

    print("Download files...")

    for submissions in subreddit:
        if not submissions.stickied and submissions.score > 50:
            fullfilename = os.path.join(dir_path, "{}.jpg".format(submissions))
            request = web.Request(submissions.url, headers = {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'})
            try:
                with web.urlopen(request) as response, open(fullfilename, 'wb') as out_file:                
                    try:
                        shutil.copyfileobj(response, out_file)
                    except HTTPError as e:
                        print("{}{}{}".format(Fore.RED, e.code, Style.RESET_ALL))
                    except URLError as e:
                        print("{}{}{}".format(Fore.RED, e.reason, Style.RESET_ALL))                 
            except:
                continue
            # delete corrupted files smaller than 55 KB
            filesize = os.path.getsize(fullfilename)
            if filesize < 55000:
                os.remove(fullfilename)
            else:
                number += 1
                # this is for debugging purposes only
                temp = "{}[{:07d}KB]{}".format(Fore.GREEN, filesize, Style.RESET_ALL)
                print("{} [{}] ID: {} URL: {}".format(temp, number, submissions, submissions.url))

    dir_count = len(os.listdir(dir_path))
    print("Download succeeded. {} files saved in '{}'.".format(dir_count, dir_path))

if __name__ == '__main__':
    main('me_irl')
