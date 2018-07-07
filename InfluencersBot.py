# Dependencies
import tweepy
import time
from datetime import datetime, timezone
import pandas as pd
from ConfigTweetBot import consumer_key, consumer_secret, access_token, access_token_secret
# Twitter credentials
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

# List of handles that we are monitoring
List_of_handles_to_monitor = ["@Riicha_r","@MonikerAsh","@ruchichandra26","@one171717","@IBaloyan","@KarnaniDeepa","@JAVillalbaUs","@JillStratton78",
"@JonathanGroth1","@Mike3dup","@TheRealAndrew19","@fervis_lauan","@TuerosVeronika","@pvenk14","@JingXu35625367",
"@MegNew2","@Pragati43524667","@WaqasIs69506672","@ThaDevelYouKnow"]

# list of Hashtags being monitered
Target_Hash_Tags = [    "#HarvardHealth","#WeightLoss","#Drug",'#Medicine','#inflammation','#hcsm','#digitalhealth',
                        '#hcsmeu','#doctorsday','#NNM','#skincare','#pharmacy','#PlasticSurgery','#pharma','#ONC','#massagetherapy',
                        '#SelfCare','#KeepTalkingMH','#publichealth','#medicine','#SupportRadiopaedia','#AllTeachAllLearn',
                        '#patientcentric']

# List of Health Quotes to be tweeted at 6:00 AM 
quote_list = [  'From the bitterness of disease man learns the sweetness of health.',
                'Keep your best wishes, close to your heart and watch what happens.',
                'Very little is needed to make a happy life; it is all within yourself, in your way of thinking.',  
                'Cakes are healthy too, you just eat a small slice.',
                'A fit, healthy body—that is the best fashion statement.',
                'Let food be thy medicine and medicine be thy food.',
                'The individual who says it is not possible should move out of the way of those doing it.',
                'We are healthy only to the extent that our ideas are humane.',
                'Healthy citizens are the greatest asset any country can have.',
                'Happiness is part of who we are. Joy is the feeling.',
                'Wine is the most healthful and most hygienic of beverages.',
                'Healthy is merely the slowest rate at which one can die.',
                'The best doctor gives the least medicine.',
                'Dieting is the only game where you win when you lose!',
                'As for butter versus margarine, I trust cows more than chemists.',
                'A fit, healthy body-- that is the best fashion statement.',
                'A diet is the penalty we pay for exceeding the feed limit.',
                'Success is getting what you want, happiness is wanting what you get.',
                'Early to bed and early to rise, makes a man healthy wealthy and wise.',
                'The greatest wealth is Health.',
                'Let food be thy medicine and medicine be thy food',
                # 'If you don\'t take care of your body, where are you going to live?.',
                'Life expectancy would grow by leaps and bounds if green vegetables smelled as good as bacon.'
                # 'Health is a state of complete harmony of the body, mind and spirit. When one is free from physical disabilities and mental distractions, the gates of the soul open.',
                'In order to change we must be sick and tired of being sick and tired.',
                'Health is like money, we never have a true idea of its value until we lose it.',
                # 'Time And health are two precious assets that we don’t recognize and appreciate until they have been depleted.',
                'Health and cheerfulness naturally beget each other.',
                'Your body is a temple, but only if you treat it as one.',
                # 'Mainstream medicine would be way different if they focused on prevention even half as much as they focused on intervention…',
                # 'Our bodies are our gardens – our wills are our gardeners.',
                'The best and most efficient pharmacy is within your own system.',
                'Health is not simply the absence of sickness.',
                'My own prescription for health is less paperwork and more running barefoot through the grass',
                'The more you eat, the less flavor; the less you eat, the more flavor.',
                'The doctor of the future will no longer treat the human frame with drugs, but rather will cure and prevent disease with nutrition.',
                'An apple a day keeps the doctor away',
                'A merry heart doeth good like a medicine, but a broken spirit dries the bones..',
                'True healthcare reform starts in your kitchen, not in Washington',
                'A man too busy to take care of his health is like a mechanic too busy to take care of his tools.',
                # 'To keep the body in good health is a duty, for otherwise we shall not be able to trim the lamp of wisdom, and keep our mind strong and clear. Water surrounds the lotus flower, but does not wet its petals.',
                'Health is a relationship between you and your body',
                'He who takes medicine and neglects to diet wastes the skill of his doctors.',
                'Sickness comes on horseback but departs on foot.',
                'Diseases of the soul are more dangerous and more numerous than those of the body.',
                # 'A good laugh and a long sleep are the best cures in the doctor’s book.',
                'Water, air and cleanliness are the chief articles in my pharmacopoeia.',
                'Health of body and mind is a great blessing, if we can bear it.',
                # 'Today, more than 95 percent of all chronic disease is caused by food choice, toxic food ingredients, nutritional deficiencies and lack of physical exercise.',
                # 'It’s bizarre that the produce manager is more important to my children’s health than the pediatrician.',
                'Healing in a matter of time, but it is sometimes also a matter of opportunity.',
                'The part can never be well unless the whole is well.',
                'Health is merely the slowest way someone can die.'
                # 'By cleansing your body on a regular basis and eliminating as many toxins as possible from your environment, your body can begin to heal itself, prevent disease, and become stronger and more resilient than you ever dreamed possible!'
             ]



def Send_Tweet(message,sender):
    try:
        if (len(sender) > 0):
            tweet_to_send = 'Hey '+ sender + ' thanks for your message:' + message + '. Appreciate your business. '
            tweet_to_send = tweet_to_send[:280] + (tweet_to_send[280:] and '..')
            # if (len(message) < 281):
            api.retweet(message) # post the tweet 
            api.direct_messages(sender,tweet_to_send)
        else:
            tweet_to_send = message[:280] + (message[280:] and '..')
            api.update_status(tweet_to_send)
        # Monitor every 30 seconds    
        time.sleep(5)
    except Exception as ex:
        pass       

# Create function for tweeting
def QuoteItUp(index):
    if(index < len(quote_list)): # prevent index out of range
        text = quote_list[index]
        current_time = datetime.today().strftime('%Y-%m-%d')
        message = 'Today is : '+ current_time + ' Quote for today - ' + text
        Send_Tweet(message,'') # send the tweet on that index number within the quote_list
    
# Match the tweet with the Hashtag
def matcher_tweet(tweet):
    for tag in Target_Hash_Tags:
        if tag.lower() in tweet.lower(): #  make case insensitive
            return True  


# Create tweet function
def Send_user_Tweet(target_user):
    # get the tweets of the target_user (which is listed in the list List_of_handles_to_monitor)
    public_tweets = api.user_timeline(target_user, count=1, result_type="recent", include_rts=1)

    for tweet in public_tweets:     
        # Appended the tweeted tweets in the dictionery within the list all_tweet_listing
        all_tweet_listing.append({  "Influencer":target_user,
                                    "Tweet":tweet["text"]                                   
                                })

    # convert the dictionery into a dataframe
    tweet_listing_pd = pd.DataFrame.from_dict(all_tweet_listing)
        
    # The matcher function is being passed to the apply() to search for tweets in the dictionery
    # to find the matching hashtag in the tweets of the target user.(The function any() returns true/false.)
    # If there is no collection found then the any() returns False 
    Matching_Tweets = tweet_listing_pd['Tweet'].apply(matcher_tweet)
    if (Matching_Tweets.any()):
        for row in tweet_listing_pd.iterrows():
            # tweet_to_send = 'Hey '+ row[1]['Influencer'] + ' thanks for your message:' + row[1]['Tweet'] + '. Appreciate your '
            if(matcher_tweet(row[1]['Tweet'])):
                Send_Tweet(row[1]['Tweet'],row[1]['Influencer'])
                 
                
def process_tweets():
    for target_user in List_of_handles_to_monitor:
        Send_user_Tweet(target_user)






all_tweet_listing = []

Quote_Index = 0

# Set timer to run every 30 sec
while(True):
    try:
        current_time = datetime.now()
        if (current_time.hour == 11 and current_time.minute == 30):        
            QuoteItUp(Quote_Index)
            Quote_Index += 1
        else:
            process_tweets()

    except Exception as ex:
        # print("unsuccessful post")
        continue
