import requests
from bs4 import BeautifulSoup

def test_manuale():
    url = "https://www.wired.it/article/openai-modelli-rag-agenti/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Usiamo solo i selettori CSS che sono i più stabili
        article_body = (
            soup.find('article') or 
            soup.select_one('div[class*="content"]') or 
            soup.select_one('main')
        )
        
        if article_body:
            p_tags = article_body.find_all('p')
            testo = "\n".join([p.get_text() for p in p_tags])
            print("SUCCESSO! Caratteri estratti:", len(testo))
            print(testo[:200] + "...")
        else:
            print("Corpo non trovato, ma niente errore di Python.")
            
    except Exception as e:
        print(f"ERRORE TROVATO: {e}")

test_manuale()