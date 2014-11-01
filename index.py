from flask import Flask, render_template, request
from birdy.twitter import UserClient
import time
import os


if 'ON_HEROKU' not in os.environ:
    # replace keys with your twitter application keys from dev.twitter.com
    os.environ['CONSUMER_KEY'] = 'key'
    os.environ['CONSUMER_SECRET'] = 'key'
    os.environ['ACCESS_TOKEN'] = 'key'
    os.environ['ACCESS_TOKEN_SECRET'] = 'key'


client = UserClient(os.environ['CONSUMER_KEY'],
                    os.environ['CONSUMER_SECRET'],
                    os.environ['ACCESS_TOKEN'],
                    os.environ['ACCESS_TOKEN_SECRET'])
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/citation', methods=['POST'])
def show_cite():
    url = request.form['url']   # get the url from the form
    id  = url.rsplit('/', 1)[1] # get only the id from the url

    # make sure the id is an int
    if id.isdigit():
        # get twitter json for tweet
        tweet = client.api.statuses.show.get(id=id)

        # get certain meta from the tweet
        text        = tweet.data['text']
        name        = tweet.data['user']['name']
        screen_name = tweet.data['user']['screen_name']
        date        = time.strftime('%d %b. %Y, %H:%M UTC',\
                      time.strptime(tweet.data['created_at'],\
                      '%a %b %d %H:%M:%S +0000 %Y'))

        # check if the tweet isn't from a company
        if 'company' not in request.form:
            # set the name as it is a real person
            name = name.rsplit(None, 1)[-1] + ', '  + name.rsplit(' ', 1)[0]

        # render the generated template
        return render_template(
            'generated.html',
            id=id,
            text=text,
            name=name,
            screen_name=screen_name,
            date=date
        )
    else:
        # id is invalid
        return 'invalid url'


if __name__ == '__main__':
    if 'ON_HEROKU' in os.environ:
        app.debug = False
    else:
        app.debug = True
    app.run(host = 'localhost', port = 5000)
