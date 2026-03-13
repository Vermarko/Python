# 
# pip install feedparser groq -> GROQ
# pip install feedparser openai python-dotenv -> OPENAI
# feed

"""
# Articoli: https://www.iprogrammatori.it/rss/articoli.xml
# Notizie: https://www.iprogrammatori.it/rss/news.xml
     https://www.wired.it/feed/rss/
     https://www.punto-informatico.it/feed/
     https://www.hdblog.it/feed/
"""
import feedparser
from groq import Groq
# scaping
from bs4 import BeautifulSoup
import requests
# Regex
import re

client = Groq(api_key="API-KEY")

RSS_FEEDS = [
    "https://www.iprogrammatori.it/rss/articoli.xml",
    "https://www.iprogrammatori.it/rss/news.xml",
    "https://www.wired.it/feed/rss/",
    "https://www.punto-informatico.it/feed/",
    "https://www.hdblog.it/feed/"
    ]

def get_latest_news():
    all_news= ""
    
    for url in RSS_FEEDS:
        feed = feedparser.parse(url)
        """
        if not feed.entries:
            return "Nessuna notizia trovata o feed non valido."
        """
        all_news += f"\nFonte: {feed.feed.title}\n"
      
        # Prendi i primi 3 articoli
        for entry in feed.entries[:3]:
            #url = entry.link
            all_news += f"- {scrabing(entry.link)}\n"
            #all_news += f"- {entry.title}\n"
            
    return all_news

def scrabing(url):
         
    #headers = {"'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'"}  # Alcuni siti richiedono uno user-agent
       
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers, timeout=10)

    if response.status_code == 200:
         
        try:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Strategia 2026: Cerchiamo i tag comuni degli articoli (<article> o div con classe 'content')
            #article_body = soup.find('article') or soup.find('div', class_='content')
            # con Regex
            #article_body = soup.find(class_=re.compile(r"article|post|content"))
            #article_body = soup.find('article') or \
            #       soup.find(class_=re.compile(r"content|body|post", re.I))
            article_body = (soup.find('article') or soup.select_one('div[class*="content"]') or soup.select_one('div[class*="article"]') or 
                soup.select_one('body')
                )

            if article_body:
                # Puliamo il testo: prendiamo solo i paragrafi <p>
                paragraphs = article_body.find_all('p')
                full_text = "\n".join([p.get_text() for p in paragraphs])
                return full_text[:3000] # Limite di caratteri per non sprecare token
    
        except Exception as e:
             
            return f"errore nello scraping {e}"
        
    return "Contenuto non disponibile."
    
def summarize_news(news_text):
    
    response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "Sei un analista tech esperto. Riassumi le seguenti notizie in un bollettino rapido, raggruppandole per temi (es. AI, Hardware, Software)."
                },
                {
                    "role": "user",
                    "content": news_text,
                }
            ],
            #model="llama-3.1-8b-instant", # Modello veloce e gratuito
            model="llama-3.3-70b-versatile",
            temperature=0.5
    )
    return response.choices[0].message.content

# Esecuzione
raw_news = get_latest_news()
summary = summarize_news(raw_news)
print("--- BOLLETTINO TECH DEL GIORNO ---\n")
print(summary)
    
    