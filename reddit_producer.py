import json
import socket
import praw
from praw.models.reddit.subreddit import SubredditStream


class RedditProducer(SubredditStream):
    def __init__(self, subreddit, socket):
        super().__init__(subreddit)
        self.socket = socket
        
    def run(self):
        for comment in self.comments(skip_existing=False):
            ###### your logic goes here #######
            print(dir(comment))
            
            #### check the PRAW docunmentation to see
            #### what attributes from comment are available
            res = ''
            ###################################
            self.socket.send(
                (repr({'content':comment.body, 'time':comment.collected_utc })+'\n').encode('utf-8')
            )        



if __name__ == '__main__':

    ## You must first modify your config.json file
    ## to insert the credentials you obtained from 
    ## Reddit
    with open("config.json", "r") as jsonfile:
        data = json.load(jsonfile)  # Reading the config file
        # print("Config data read successful", data)

    reddit = praw.Reddit(
            client_id=data["client_id"],
            client_secret=data["client_secret"],
            user_agent="COM3021 Reddit Producer"
    )

    host = '127.0.0.1'
    port = 5590
    address = (host, port)

    #Initializing the socket

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(address)
    server_socket.listen(5)

    print("Listening for client...")

    conn, address = server_socket.accept()

    print("Connected to Client at " + str(address))



    subreddits = reddit.subreddit("AskUk+AskAnAmerican")
    stream = RedditProducer(subreddits, conn)
    stream.run()

    