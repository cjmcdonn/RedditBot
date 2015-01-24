# -*- coding: utf-8 -*-
"""
Created on Fri Jan 23 13:16:53 2015

@author: casey
"""


import praw
import csv
import time
import os


phrase_dict = {
    'Extract revenge' : 'exact revenge',
    'Nip it in the butt' : 'nip it in the bud',
    'I could care less' : 'I couldn\'t care less',
    'One in the same' : 'one and the same',
    'Each one worse than the next' : 'each one worse than the last',
    'On accident' : 'by accident',
    'Statue of limitations' : 'statute of limitations',
    'For all intensive purposes' : 'for all intents and purposes',
    'He did good' : 'he did well',
    'Old timer\'s disease' : 'Alzheimer\'s Disease',
    'I\'m giving you leadway' : 'I\'m giving you leeway',
    'Expresso' : 'espresso',
    'Momento' : 'memento',
    'Irregardless' : 'regardless',
    'Conversating' : 'conversing',
    'Scotch free' : 'scot free',
    'Curl up in the feeble position' : 'curl up in the fetal position',
    'Hone in' : 'home in',
    'Brother in laws' : 'brothers in law',
}


def touch(file_name, times=None):
    """Re-create the functionality of the unix touch command."""
    with open(file_name, 'a'):
        os.utime(file_name, times)
        
        
def read_list(file_name):
    """
    Read string of comment IDs that have already been replied to, convert to a
    list and return the list.
    """
    with open(file_name, "r") as my_file:
        commented_str = my_file.read()
    commented_list = commented_str.split('\n')
    return commented_list
  
  
def append_id(file_name, comment_id):
    """Append new comment ID to file."""
    with open(file_name, "a") as myfile:
        myfile.write(comment_id + '\n')


def main():
    
    # Login and bot information
    r = praw.Reddit(user_agent='sarahbot/0.1 by /u/monstermudder78')
    r.login('', '')
    
    # Touch file to make sure it exists, then read commented_list from
    # commented_list.csv to restore commenting history after a crash.
    touch('commented_list.csv')
    commented_list = read_list('commented_list.csv')
    
    # Keep bot running and running and running...
    while True:
        
        # Keep bot alive at all costs
        try:
        
            # Get comments from one subreddit
            #subreddit = r.get_subreddit('test')
            #comments = subreddit.get_comments()
               
            # Or get all of the latest comments
            comments = r.get_comments('all')
            
            # Loop through all the comments one by one, looking for each key
            # in each comment. If there is a match and this bot did not
            # previously comment, post comment then append comment ID to
            # commented_list and commented_list.csv.
            for comment in comments:
                for key in phrase_dict:
                    if (key.lower() in comment.body.lower() and
                            comment.id not in commented_list):
                        reply_str = key+'?' + ' I think you meant:' \
                                '\''+phrase_dict[key]+'.\''
                        comment.reply(reply_str)
                        print reply_str
                        commented_list.append(comment.id)
                        append_id('commented_list.csv', comment.id)
        
        except:
            pass
        
        time.sleep(5)
        

if __name__ == "__main__":
    # execute only if run as a script
    main()