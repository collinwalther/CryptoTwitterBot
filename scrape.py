from textblob import TextBlob
import urllib.request
import os.path
import datetime
import json

posts = [] 
prices = []

def GetAllSubredditPosts(destFile):
    # Get the data and write it to a file, so we don't have to 
    # hit the API endpoint too much
    global posts
    with open(destFile, 'w') as dst:
        for post in posts:
            selfText = post['selftext']
            title = post['title']
            dst.write("{}\n".format(title))
            dst.write("{}\n".format(selfText))


def MakeSubredditAPIRequest(subreddit):
    # Don't do anything if we already have the files, so we can avoid
    # getting rate limited by reddit (perish the thought)
    global posts
    cachedFileName = "r-" + subreddit + ".txt"
    if os.path.isfile(cachedFileName):
        with open(cachedFileName, 'r') as src:
            jsonData = json.loads(src.read())
            posts = jsonData
            return

    t = "all"
    limit = 100
    after = ""

    # Start getting the content via the reddit API
    while after is not None:
        # Generate the API endpoint
        url = "https://www.reddit.com/r/{}/top.json?t={}&limit={}"
        url = url.format(subreddit, t, limit)
        if after != "":
            url = url + "&after={}".format(after)

        # GET request the API endpoint
        pageRequest = urllib.request.Request(url, headers={'User-Agent': 'Mozilla'})
        source = urllib.request.urlopen(pageRequest).read().decode('utf-8')

        # Parse the JSON from the response
        jsonData = json.loads(source)
        posts += [child['data'] for child in jsonData['data']['children']]

        # Set the "after" variable so we can iterate over the next 
        # few posts
        after = jsonData['data']['after']
        print(after)

    # Save the data we just got to a file, so we don't always have to retrieve it 
    # from reddit.
    with open(cachedFileName, 'w') as dst:
        json.dump(posts, dst)

if __name__ == "__main__":
    MakeSubredditAPIRequest("cryptocurrency")
    GetAllSubredditPosts("SourceText.txt")
