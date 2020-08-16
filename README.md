# WhatsApp-Analyzer-Telegram-bot

The script reads an exported whatsapp chat and then extracts the data. You may need to install some packages before run it. also you can access it by a telegram bot of your after geeting a bot if from @botfather telegram.


# Supported analysis
    count_msg_by_sender(df['Name']) #count who sends most message in group
    print(count_emoji("".join(df['emoji'].tolist()))) #print emoji most used
    chek_tone_of_chat((df[['Date','polarity']].copy())) #polarity of chat negative , neutral , postive
    user_top_use_keyword((df[['Name','Keyword']].copy())) 
    user_top_use_emoji((df[['Name','emoji']].copy()))  # top used emojis by each user
    when_user_is_active((df[['Name','weekday']].copy())) #on what day user is active
    when_user_is_inactive((df[['Name','weekday']].copy())) #on what day user is inactive
    active_day_week(df['weekday'])#on which day group is active
    (df).to_csv('complete_data.csv') # comple dataframe to csv
    
#use 
 - export chat  without media from  whatsapp 
 -  send it to your bot 
 -  it return you set of some csv and graph.png files of your anaysis
 
# code is self explanatory

- note change the Tokedn with your telegram bot token
- this is ready to go bot on heroku server for expansion .

#what you sholud know -
pandas dataframe and method
matplotlib for ploting graphs
good knowledge of telegram api - message handler, command handler , telegam-python-bot liabrary.


