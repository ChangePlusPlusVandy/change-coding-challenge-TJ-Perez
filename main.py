import tweepy
import PySimpleGUI as sg
import random
from PIL import Image
import requests
import io
import urllib.request
from io import BytesIO
import base64
# using the tweepy library because it allows easy access of the Twitter API within python


#tried to add in GUI quickly at the end, couldn't quite figure the text spacing in time,it was my first time working
#with this GUI library so I wasn't able to use it very effectively but I was glad to be able to get image processing and
#updating working


score = 0
tweetCount = 0

tweetSG = None
tweetImage = None

randNums1 = []
randNums2 = []
def getRandTweet1(tweetList):
    x = random.randint(0, len(tweetList) - 1)
    while x in randNums1:
        x = random.randint(0, len(tweetList) - 1)
    randNums1.append(x)

    return tweetList[x]

def getRandTweet2(tweetList):
    x = random.randint(0, len(tweetList) - 1)
    while x in randNums2:
        x = random.randint(0, len(tweetList) - 1)
    randNums2.append(x)

    return tweetList[x]

def refreshTweet(message,textBox, imageOut):
    tweetSG.update(message)
    elonButton.update(visible=False)
    kanyeButton.update(visible=False)
    okButton.update(visible=True)

    tweetFrom = random.randint(1, 2)
    print(tweetFrom)

    if tweetFrom == 1:
        displayTweet = getRandTweet1(muskTweets)
    else:
        displayTweet = getRandTweet2(kanyeTweets)

    print(displayTweet)

    if "http://" in displayTweet:
        imageOut.update(data=getTweetFromImage(displayTweet),
                              size=(100, 100))
        textBox = sg.Text("Image:", font=("Courier", 10), pad=((10,10),0))
    else:
        textBox = sg.Text(displayTweet, font=("Courier", 10), pad=((10,10),0))
        imageOut.update(data=getTweetFromImage(twitterLogo),
                              size=(100, 100))

    print("dis",displayTweet, type(displayTweet))
    return displayTweet, tweetFrom

def getTweetFromImage(url):
    image = urllib.request.urlopen(url).read()
    image2 = Image.open(io.BytesIO(urllib.request.urlopen(url).read()))
    image2 = image2.resize((100,100))


    bytesImage = io.BytesIO(image)
    imgByteArr = io.BytesIO()
    image2.save(imgByteArr, format='PNG')
    imgByteArr = imgByteArr.getvalue()

    encoded_string = base64.b64encode(io.BytesIO(imgByteArr).read())


    return encoded_string





if __name__ == '__main__':

    # Enter API keys and Access Tokens here:
    apiKey = "9Cc1uKihbDF74j9UdDLsxSsGZ"
    apiKeySecret = "ipJ1EALwrjKF70ZWUiXiTWqLortrbZ5iz5Tsrpm8pyaqqlY2sf"
    accessToken = "1169746931020484608-RqKJ3v968NeSo9gCYn5NypGl27kCjF"
    accessTokenSecret = "ECejswLVTui9dTFP0u0YjBOOc7fCWpY39B0E3Z3v7E4ys"

    # Setup OAuth and create API using tweepy
    auth = tweepy.OAuthHandler(apiKey, apiKeySecret)
    auth.set_access_token(accessToken, accessTokenSecret)
    api = tweepy.API(auth)

    numTweetsToLoad= 3200

    screenName = "@elonmusk"
    muskTweets = []

    #load in 3200 Elon Musk tweets, then filter out ones mentioning others and add into a list
    for tweet in tweepy.Cursor(api.user_timeline, screen_name=screenName, tweet_mode="extended",
                               include_entities=True).items(numTweetsToLoad):
        if 'media' in tweet.entities:
            for image in tweet.extended_entities['media']:
                print(image)
                muskTweets.append(image['media_url'])
        if "@" not in tweet.full_text:
            if "http" not in tweet.full_text:
                muskTweets.append(tweet.full_text)



    screenName = "@kanyewest"
    kanyeTweets = []

    #load in 3200 Kanye tweets, then filter out ones mentioning others and add into a list
    for tweet in tweepy.Cursor(api.user_timeline, screen_name=screenName, tweet_mode="extended",
                               include_entities=True).items(numTweetsToLoad):
        if 'media' in tweet.entities:
            for image in tweet.extended_entities['media']:
                kanyeTweets.append(image['media_url'])
        if "@" and "http" not in tweet.full_text:
            if "http" not in tweet.full_text:
                kanyeTweets.append(tweet.full_text)

    displayTweet = ''
    tweetFrom = random.randint(1, 2)
    print(tweetFrom)

    if tweetFrom == 1:
        displayTweet = getRandTweet1(muskTweets)
    else:
        displayTweet = getRandTweet2(kanyeTweets)


    twitterLogo = "https://static01.nyt.com/images/2014/08/10/magazine/10wmt/10wmt-articleLarge-v4.jpg"

    #creating the GUI and logic

    if "http://" in displayTweet:
        tweetImage = sg.Image(data=getTweetFromImage(displayTweet),
                              size=(100, 100), key='update')
        tweetSG = sg.Text("Image:", font=("Courier", 10), pad=((10,10),0))
    else:
        tweetSG = sg.Text(displayTweet, font=("Courier", 10), pad=((10,10),0))
        tweetImage = sg.Image(data=getTweetFromImage(twitterLogo),
                              size=(100, 100), key= 'update')



    elonButton = sg.Button("Elon")
    kanyeButton = sg.Button("Kanye")
    okButton = sg.Button("OK", visible=False)

    layout = [[tweetSG, tweetImage],
              [elonButton],
              [kanyeButton],
              [okButton]]

    window = sg.Window("Who Said it?", layout, margins=(200, 100))

    while True:
        event, values = window.read()
        print(event)
        # End program if user closes window or
        # presses the OK button
        if event == "Elon":
            if tweetFrom == 1:
                score += 1
                tweetCount += 1
                displayTweet, tweetFrom = refreshTweet("Correct!", tweetSG, tweetImage)
            else:
                tweetCount += 1
                displayTweet, tweetFrom = refreshTweet("Incorrect :(", tweetSG, tweetImage)

        if event == "Kanye":
            if tweetFrom == 2:
                score += 1
                tweetCount += 1
                displayTweet, tweetFrom = refreshTweet("Correct!", tweetSG, tweetImage)
            else:
                tweetCount += 1
                displayTweet, tweetFrom = refreshTweet("Incorrect :(", tweetSG, tweetImage)
        if event == "OK" and tweetCount < 2:
            print(displayTweet)
            tweetSG.update(displayTweet)
            #tweetImage.update()
            elonButton.update(visible=True)
            kanyeButton.update(visible=True)
            okButton.update(visible=False)
        if event == "OK" and tweetCount >= 2:
            break
        if tweetCount >= 2:
            tweetSG.update("Your Score is: " + str((score/tweetCount)* 100) + "%")
            print("Your Score is: " + str((score/tweetCount)* 100) + "%")
            elonButton.update(visible=False)
            kanyeButton.update(visible=False)
            okButton.update(visible=True)

        if event == sg.WIN_CLOSED:
            break

    window.close()

