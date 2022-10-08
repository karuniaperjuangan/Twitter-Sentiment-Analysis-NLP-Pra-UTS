import snscrape.modules.twitter as sntwitter
import pandas as pd
from tqdm import tqdm
import os
import datetime as dt
import re


def scrape_tweets(query, max_tweets=-1,output_path="./scraper/output/" ): 
    output_path = os.path.join(output_path,dt.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")+"-"+str(query)+".csv")
    
    tweets_list = []
    try:
        for i,tweet in tqdm(enumerate(sntwitter.TwitterSearchScraper(query).get_items())):
            if max_tweets != -1 and i >= int(max_tweets):
                break
            tweets_list.append([tweet.date, tweet.id, tweet.content, tweet.user.username, tweet.likeCount, tweet.retweetCount, tweet.replyCount, tweet.quoteCount, tweet.url])
    except KeyboardInterrupt:
        print("Scraping berhenti atas permintaan pengguna")
    df = pd.DataFrame(tweets_list, columns=['Datetime', 'Tweet Id', 'Text', 'Username', 'Likes', 'Retweets', 'Replies', 'Quotes', 'URL'])
    df.to_csv(output_path, index=False)
    return df



def remove_unnecessary_char(text):
  text = re.sub("\[USERNAME\]", " ", text)
  text = re.sub("\[URL\]", " ", text)
  text = re.sub("\[SENSITIVE-NO\]", " ", text)
  text = re.sub('  +', ' ', text)
  return text

def preprocess_tweet(text):
  text = re.sub('\n',' ',text) # Remove every '\n'
  # text = re.sub('rt',' ',text) # Remove every retweet symbol
  text = re.sub('^(\@\w+ ?)+',' ',text)
  text = re.sub(r'\@\w+',' ',text) # Remove every username
  text = re.sub('((www\.[^\s]+)|(https?://[^\s]+)|(http?://[^\s]+))',' ',text) # Remove every URL
  text = re.sub('/', ' ', text)
  # text = re.sub(r'[^\w\s]', '', text)
  text = re.sub('  +', ' ', text) # Remove extra spaces
  return text
    
def remove_nonaplhanumeric(text):
  text = re.sub('[^0-9a-zA-Z]+', ' ', text) 
  return text

def preprocess_text(text):
  text = preprocess_tweet(text)
  text = remove_unnecessary_char(text)
  text = text.lower()
  return text