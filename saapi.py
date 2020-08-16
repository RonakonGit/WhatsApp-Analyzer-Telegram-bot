import os
import re
import emoji
import nltk
import telegram
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import Counter
from textblob import TextBlob

for k in list(os.environ.keys()): # remove this for loop block if u are behind any proxy
    if k.lower().endswith('_proxy'):
        del os.environ[k]

def when_user_is_inactive(df) :
    N = 1
    df1 =  (df.set_index('Name')['weekday']
              .str.lower()
              .str.split(expand=True)
              .stack()
              .groupby(level=0)
              .value_counts()
              .groupby(level=0)
              .tail(N)
              .rename_axis(('Name','inactive_day'))
              .reset_index(name='count'))
    (df1[['Name','inactive_day']]).to_csv('when_user_is_inactive.csv')
    return
def when_user_is_active(df) :
    N = 1
    df1 =  (df.set_index('Name')['weekday']
              .str.lower()
              .str.split(expand=True)
              .stack()
              .groupby(level=0)
              .value_counts()
              .groupby(level=0)
              .head(N)
              .rename_axis(('Name','active_weekday'))
              .reset_index(name='count'))
    (df1[['Name','active_weekday']]).to_csv('when_user_is_active.csv')
    return
def active_day_week(df_of_days) :
    ax = df_of_days.value_counts().plot(kind='bar',figsize=(25,8), title="On which day user are active")
    ax.set_xlabel("Day")
    ax.set_ylabel("COUNT OF MESSAGE")
    plt.setp(ax.get_xticklabels(), rotation=30, horizontalalignment='right')
    plt.savefig('active_weekday_of_chat.png')
    return
def user_top_use_emoji(df) :
    N = 5
    df1 =  (df.set_index('Name')['emoji']
              .str.lower()
              .str.split(expand=True)
              .stack()
              .groupby(level=0)
              .value_counts()
              .groupby(level=0)
              .head(N)
              .rename_axis(('Name','emoji'))
              .reset_index(name='count'))
    (df1).to_csv('user_top_used_emoji.csv')
    return
def user_top_use_keyword(df) :
    N = 5
    df1 =  (df.set_index('Name')['Keyword']
              .str.lower()
              .str.split(expand=True)
              .stack()
              .groupby(level=0)
              .value_counts()
              .groupby(level=0)
              .head(N)
              .rename_axis(('Name','Keyword'))
              .reset_index(name='count'))
    (df1).to_csv('user_top_used_keyword.csv')
    return
def extract_keyword(text) :
    try :
        l1 = []
        l1.append(text)
        vectorizer = TfidfVectorizer()
        X = vectorizer.fit_transform(l1)
        ret = (" ".join(vectorizer.get_feature_names()))
    except :
        ret = " "
    return(ret)
def chek_tone_of_chat(df) :
    df.to_csv('tone_of_chat_msg.csv')
    ax = df.plot(x='Date',y= 'polarity',kind='line',figsize=(25,8), title="TONE OF Chat over time")
    ax.set_xlabel("TIME")
    ax.set_ylabel("<---negative- POLARITY- positive-->")
    plt.setp(ax.get_xticklabels(), rotation=30, horizontalalignment='right')
    plt.savefig('graph_tone_of_chat.png') 
    return

def count_msg_by_sender(df_of_sender_name) :
    ax = df_of_sender_name.value_counts().head(40).plot(kind='bar',figsize=(25,8), title="COUNT OF MESSAGE BY top 40 AUTHOR")
    ax.set_xlabel("AUTHOR")
    ax.set_ylabel("COUNT OF MESSAGE")
    plt.setp(ax.get_xticklabels(), rotation=30, horizontalalignment='right')
    plt.savefig('COUNT_OF_MESSAGE_BY_top_40_AUTHOR.png')
    (df_of_sender_name.value_counts()).to_csv('Author_Message_count.csv')
    return
def count_emoji(text) :
    emoji_list = [i['emoji'] for i in emoji.emoji_lis((text))]
    count = (Counter((emoji_list)))
    df_from_counter = pd.DataFrame.from_dict(count, orient='index').reset_index()
    df_from_counter = df_from_counter.rename(columns={'index':'Emoji', 0:'count'})
    df_from_counter = df_from_counter.sort_values('count',ascending=False)
    df_from_counter.to_csv('most_used_emoji.csv')
def extract_emoji(text) :
    emoji_list = [i['emoji'] for i in emoji.emoji_lis((text))] #list of emoji
    return(" ".join(emoji_list))
def read_file(file): 
    x = open(file,'r', encoding = 'utf-8') #Opens the text file into variable x but the variable cannot be explored yet
    y = x.read() #By now it becomes a huge chunk of string that we need to separate line by line
    content = y.splitlines() #The splitline method converts the chunk of string into a list of strings
    return content 

def send_files(chat_id):
    token = '' #enter your bot token from bot father
    bot = telegram.Bot(token=token) 
    bot.send_message(chat_id=chat_id, text = "data : on what week day user is inactive->")
    bot.send_document(chat_id=chat_id, document = open('when_user_is_inactive.csv','rb'))

    bot.send_message(chat_id=chat_id, text = "data : on what week day user is inactive")
    bot.send_document(chat_id=chat_id, document = open('when_user_is_active.csv','rb'))

    bot.send_message(chat_id=chat_id, text = "Most used emojis in chat")
    bot.send_document(chat_id=chat_id, document = open('most_used_emoji.csv','rb'))

    bot.send_message(chat_id=chat_id, text = "Top keywords used by users")
    bot.send_document(chat_id=chat_id, document = open('user_top_used_keyword.csv','rb'))

    bot.send_message(chat_id=chat_id, text = "Most used emojis by each user")
    bot.send_document(chat_id=chat_id, document = open('user_top_used_emoji.csv','rb'))

    bot.send_message(chat_id=chat_id, text = "Graph - Tone of chats over time :")
    bot.send_photo(chat_id=chat_id, photo = open('graph_tone_of_chat.png','rb'))
    
    bot.send_message(chat_id=chat_id, text = "tone of chat over time : Negative , Neutral , Positive->")
    bot.send_document(chat_id=chat_id, document = open('tone_of_chat_msg.csv','rb'))

    bot.send_message(chat_id=chat_id, text = "Graph - on which day group is active :")
    bot.send_photo(chat_id=chat_id, photo = open('active_weekday_of_chat.png','rb'))

    bot.send_message(chat_id=chat_id, text = "Number of messages sent by each user :")
    bot.send_document(chat_id=chat_id, document = open('Author_Message_count.csv','rb'))

    bot.send_message(chat_id=chat_id, text = "COUNT_OF_MESSAGE_BY_top_40_AUTHOR :")
    bot.send_photo(chat_id=chat_id, photo = open('COUNT_OF_MESSAGE_BY_top_40_AUTHOR.png','rb'))

    bot.send_message(chat_id=chat_id, text = "Complete parsed data in csv format")
    bot.send_document(chat_id=chat_id, document = open('complete_data.csv','rb'))

def analysis(filename , chat_id ) :
    chat = read_file(filename)
    join = [line for line in chat if  "joined using this" in line] #seprate list to store joined group
    media = [line for line in chat if  "<Media omitted>" in line] #media
    left = [line for line in chat if line.endswith("left")] #seprate list members who left
    chat = [line.strip() for line in chat] # removing extrax space from each line
    clean_chat = [line for line in chat if not "joined using this" in line] # removing joined chat line
    clean_chat = [line for line in chat if not "<Media omitted>" in line]
    clean_chat= [line for line in clean_chat if not line.endswith("left")] # remove left people list


    #we need to merg message  which dosenot start with date as single message
    msgs = [] #message
    pos = 0 #counter for position of msgs in chek_tone_of_chatthe container
    #Flow:
    #For every line, see if it matches the expression which is starting with the format "number(s)+slash" eg "12/"
    #If it does, it is a new line of conversion as they begin with dates, add it to msgs container
    #Else, it is a continuation of the previous line, add it to the previous line and append to msgs, then pop previous line.

    for line in clean_chat:
        if re.findall("\A\d+[/]", line):
            msgs.append(line)
            pos += 1
        else:
            take = msgs[pos-1] + ". " + line
            msgs.append(take)
            msgs.pop(pos-1)

    #seprating date ,time , author, message
    time = [msgs[i].split(',')[1].split('-')[0] for i in range(len(msgs))]
    time = [s.strip(' ') for s in time] # Remove spacing
    date = [msgs[i].split(',')[0] for i in range(len(msgs))]
    name = [msgs[i].split('-')[1].split(':')[0] for i in range(len(msgs))]
    content = []

    for i in range(len(msgs)):
        try:
            content.append(msgs[i].split(':')[2])
        except IndexError:
            content.append('Missing Text')

    df = pd.DataFrame(list(zip(date, time, name, content)), columns = ['Date', 'Time', 'Name', 'Content'])
    df = df[df["Content"]!='Missing Text']
    df.reset_index(inplace=True, drop=True)
    df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])
    df['weekday'] = df['DateTime'].apply(lambda x: x.day_name()) 
    df['Letter_Count'] = df['Content'].apply(lambda s : len(s))
    df['Keyword'] = df['Content'].apply(lambda s : extract_keyword(s))
    df['Word_Count'] = df['Content'].apply(lambda s : len(s.split(' ')))
    df['emoji'] = df['Content'].apply(lambda msg : extract_emoji(msg))
    df['Hour'] = df['Time'].apply(lambda x : x.split(':')[0]) # The first token of a value in the Time Column contains the hour (Eg., "12" in "12:15")
    df['polarity'] = df['Content'].apply(lambda msg : 100*TextBlob(msg).polarity) # -1 negative ,1 pos , 0 neutral 
    df['subjectivity'] = df['Content'].apply(lambda msg : TextBlob(msg).subjectivity) # Subjectivity is a float value within the range [0.0 to 1.0] where 0.0 is very objective and 1.0 is very subjective

    count_msg_by_sender(df['Name']) #count who sends most message in group
    print(count_emoji("".join(df['emoji'].tolist()))) #print emoji most used
    chek_tone_of_chat((df[['Date','polarity']].copy())) #polarity of chat
    user_top_use_keyword((df[['Name','Keyword']].copy())) 
    user_top_use_emoji((df[['Name','emoji']].copy())) 
    when_user_is_active((df[['Name','weekday']].copy())) #on what day user is active
    when_user_is_inactive((df[['Name','weekday']].copy())) #on what day user is inactive
    active_day_week(df['weekday'])#on which day group is active
    (df).to_csv('complete_data.csv')

    send_files(chat_id)
    return
