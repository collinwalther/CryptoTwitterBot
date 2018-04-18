from textblob import TextBlob
import tweepy
import time
import markovify

class FakeCryptoNews:
    def __init__(self):
        # Set up tweet API
        # This is horrible practice, but I don't particularly care if anyone 
        # else has access to this bot
        consumer_key = "5ijvz2yaCyh9uRYfgp8F3vVHk"
        consumer_secret = "uWfPYnIwttzRLmIntb29IF81NrAI9YVXlMKtErElkFwQjfEZGh"
        access_token = "983463112857665536-AZ7CSMeoRfWOYUnF2ed4ydJH8wz2RfD"
        access_token_secret = "eLugkQRmIYli9rwYE8K2H8Z5N6xy9QUK2vx5k9Ay1BF1n"
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth)

        # Set up markov model of source text
        with open("SourceText.txt", 'r') as f:
            text = f.read()
        self.model = markovify.Text(text, state_size=3)

        # Maintain a list of sentences that we've already generated, so we
        # never accidentally repeat ourself.
        self.sentences = set()
        
    def GetHappyTweet(self):
        threshold = .3
        sentence = ""
        while True:
            sentence = self.model.make_short_sentence(138)
            if sentence.strip() in self.sentences:
                continue
            t = TextBlob(sentence)
            if t.sentiment.polarity >= threshold:
                self.sentences.add(sentence.strip())
                break
        return "😄 " + sentence

    def GetSadTweet(self):
        threshold = -.3
        sentence = ""
        while True:
            sentence = self.model.make_short_sentence(138)
            if sentence.strip() in self.sentences:
                continue
            t = TextBlob(sentence)
            if t.sentiment.polarity <= threshold:
                self.sentences.add(sentence.strip())
                break
        return "😢 " + sentence
    
    def Tweet(self, message):
        self.api.update_status(message)
    
    def Run(self):
        happy = True
        while (1):
            if happy:
                self.Tweet(self.GetHappyTweet())
            else:
                self.Tweet(self.GetSadTweet())
            time.sleep(900)
    
if __name__ == "__main__":
    fcn = FakeCryptoNews()
    fcn.Run()

