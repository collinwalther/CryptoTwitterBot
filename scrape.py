import urllib.request
import json

if __name__ == "__main__":
    t = "all"
    limit = 10
    subreddit = "cryptocurrency"
    after = ""

    # Delete the old copy of the text we've gotten
    with open('SourceText.txt', 'w') as dst:
        pass

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
        
        # Get the data and write it to a file, so we don't have to 
        # hit the API endpoint too much
        after = jsonData['data']['after']
        print(after)
        with open('SourceText.txt', 'a') as dst:
            for i in range(limit):
                if i >= len(post):
                    return
                post = jsonData['data']['children'][i]
                selfText = post['data']['selftext']
                title = post['data']['title']
                dst.write("{}\n".format(title))
                dst.write("{}\n".format(selfText))

