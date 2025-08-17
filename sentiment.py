import pandas as pd
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_csv("quora_all_answers.csv")


nltk.download('vader_lexicon')


sia = SentimentIntensityAnalyzer()

def analyze_sentiment(text):
    score = sia.polarity_scores(str(text))  # convert to string to avoid errors
    if score['compound'] >= 0.05:
        return "Positive"
    elif score['compound'] <= -0.05:
        return "Negative"
    else:
        return "Neutral"

df['Sentiment'] = df['Text'].apply(analyze_sentiment)


df.to_csv("quora_answers_sentiment.csv", index=False, encoding="utf-8-sig")
print("Sentiment analysis completed. Saved to quora_answers_sentiment.csv")


print(df['Sentiment'].value_counts())


sns.set(style="whitegrid")

# Overall Sentiment Distribution
plt.figure(figsize=(8,5))
sns.countplot(data=df, x='Sentiment', order=['Positive','Neutral','Negative'], palette="viridis")
plt.title("Overall Sentiment Distribution")
plt.show()
