
from sentistrength import PySentiStr
from textblob import TextBlob
import re
import string
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from textblob import Word
import pandas as pd

def cleanData(text):
    # remove URL
    result = re.sub(r"http\S+", "", text)

    # Numbers removing
    result = re.sub(r'\d+', '', result)

    # To lowercase
    result = result.lower()

    # remove punctuation
    result = result.translate(str.maketrans('', '', string.punctuation))

    # remove white space
    result = result.strip()

    # remove stopwords
    stop_words = set(stopwords.words('english'))
    from nltk.tokenize import word_tokenize
    tokens = word_tokenize(result)
    result = [i for i in tokens if not i in stop_words]

    # stemming
    #     stemmer= PorterStemmer()
    #     newResult = []
    #     for word in result:
    #         newResult.append(stemmer.stem(word))
    #     print(newResult)
    return result


senti = PySentiStr()
senti.setSentiStrengthPath('C:\ProgramData\Anaconda3\Lib\site-packages\sentistrength\SentiStrength.jar')
senti.setSentiStrengthLanguageFolderPath('C:\ProgramData\Anaconda3\Lib\site-packages\sentistrength\\')

data = pd.read_csv("D:\senior\sentiment\Moodle_comments2.csv")
tagcomment= pd.read_csv("D:\\senior\\sentiment\\data\\tags.csv", encoding='iso-8859-1')
tagcommentId = tagcomment['commentid']

commendId = []
cleanComment = []
sentiment = []
# tagger = []
# tagee = []
countnon = 0
count = 0
for index ,row in data.iterrows():
    countnon = countnon +1
    if row['commentid'] in tagcommentId:
        if count%10 == 0:
            print(count, countnon)
        commendId.append(row['commentid'])
        result = cleanData(row['message'])
        result = ' '.join(word for word in result)
        cleanComment.append(result)
        try:
            score = senti.getSentiment(result)
            sentiment.append(score[0])
        except:
            print(result,"cannot analyze")
#         print('commendId: ', row['commentid'], 'sentiment:', score[0])
        count = count + 1
#         tagger.append()
#         tagee.append()
        if count == 10000:
            datadict = {'commendId': commendId, 'score': sentiment}
            commentSentiment = pd.DataFrame(datadict)
            commentSentiment = commentSentiment[['commendId', 'score']]
            commentSentiment.to_csv('D:\senior\sentiment\commentSentiment.csv', index=False)
            commendId = []
            cleanComment = []
            sentiment = []
            break

# result = cleanData(sample[1])
# result = ' '.join(word for word in result)
# print(result)
# #sentiment
# sentiment = senti.getSentiment(result)
# textblob = TextBlob(result)
# print(sentiment)
# print(format(textblob.sentiment))
