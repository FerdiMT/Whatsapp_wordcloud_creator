import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from stop_words import get_stop_words
import re

# Load whatsapp chat
df = pd.read_csv(r"chat.txt", header=None, error_bad_lines=False, encoding='utf8', sep=']')
df=df.drop(0)
df.columns=['Date', 'text']

# Get the chat text divided between user and words
chat = df['text'].str.split(":", n=1, expand=True)
chat.columns = ['user', 'text']

# For groups, drop. Else, pass (or error would be found)
try:
    chat = chat.drop(0)
except:
    pass

chat['text'] = chat['text'].str.lower()
# Remove the lines that have images. Depending on the language, will need to change the "imatge omesa" text.
chat = chat[chat.text.str.contains(' \u200eimatge omesa') == False].reset_index(drop=True)

# Load stopwords (change language as needed)
stop_words = get_stop_words('catalan')

# Custom list of stop_words
removable_words = ['jajajaja', 'jaja', 'jajaja', 'jajajajaja']

# Remove stopwords
chat['text'] = chat['text'].str.replace(r"\s*(?<!\w)(?:{})(?!\w)".format("|".join([re.escape(x) for x in removable_words])), " ")
chat['text'] = chat['text'].str.replace(r"\s*(?<!\w)(?:{})(?!\w)".format("|".join([re.escape(x) for x in stop_words])), " ")
# Replace non-text characters
chat['text'] = chat['text'].str.replace('[#,@,&,?,!]', '')

# Number of participations per user
chat['user'].value_counts()
chat['user'].unique()

# Wordcloud per user
for user in list(chat['user'].value_counts().index):
    user_name = user
    subchat = chat.loc[chat['user'] == user]

    wordcloud = WordCloud().generate(' '.join(subchat['text']))
    plt.imshow(wordcloud)
    plt.title('Wordcloud' + str(user))
    plt.show()

