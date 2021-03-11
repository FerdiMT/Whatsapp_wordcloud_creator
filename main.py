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
chat = chat[chat.text.str.contains(' \u200eimatge omesa') == False].reset_index(drop=True)

# Load stopwords (change language as needed)
stop_words = get_stop_words('catalan')

# Custom list of stop_words
removable_words = ['si', 'que', 'per', 'un', 'de', 'la', 'jajajaja', 'jaja', 'jajaja', 'jajajajaja',
                   'àudio', 'omès', 'video', 'amb', 'quan', 'quin', 'en', 'xd', 'tant', 'pues',
                   'el', 'dos', 'ya', 'ok', 'molt', 'quin', 'som', 'qui', 'fa', 'li', 'allà', 'crec', 'és', 'es', 'se', 'em',
                   'et', 'estic', 'doncs', 'era', 'https', 'més', 'jaj', 'ha', 'jo', 'pot', 'nosaltres', 'gif', 'ja', 's', 'l', 'enganxina', 'però', 'us', 'del', 'els', 'ho', 'jajajajajajaja', 'està', 'estem', 'hi',
                   'tot', 'perquè', 'ser', 'te', 'tu', 'ho', 'q', 'al', 'fer', 'o', 'ara', 'han', 'va', 'lo', 'y', 'aquest', 'm', 'dir', 'por', 'son', 're', 'omesa', 'm', 'fet', 'oh', 'una', 'un', 'vam', 'hola',
                   'd', 'vale', 'teniu', 'tenim', 'nos', 'diu', 'tots', 'vídeo', 'algo', 'així', 'dels', 'tots', 'diu', 'bé', 'sou', 'ni', 'oi', 'mi', 'vale', 'x', 'quina', 'jajajajajajajaja', 'vol',
                   'le', 'jajajajajaja', 'estan', 'vosaltres', 'això', 'està', 'esteu', 'hem', 'pel', 'anar', 'mes', 'ens', 'demà', 'perq', 'les', 'també', 'anem', 'heu', 'esta', 'abans', 'aquí',
                   'xddd', 'pq', 'tinc', 'xo', 'res', 'pero', 'eh', 'xdxd', 'avui', 'sino', 'fem', 'dia', 'xk', 'pero', 'foto', 'algu', 'aixi', 'n', 'ca', 'alla', 'teu', 've', 'pa', 'aqui', 'alla', 'uns', 'xdd', 'van', 'veig',
                   'tb', 'cap', 'aixo', 'xdddd', 'val', 'pots', 'soc', 'havia', 'veure', 'algú', 'vaig', 'què', 'hahahaha', 'ah', 'pk']

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

