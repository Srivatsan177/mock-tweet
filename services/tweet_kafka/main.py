from consumers.tweet_like_consumer import TweetLikeConsumer
import time

if __name__ == "__main__":
    while True:
        time.sleep(10)
        print("consuming")
        TweetLikeConsumer().run()
