"""
Invio Messaggio Telegram (Il più comodo)
Telegram è fantastico per le automazioni perché è gratuito e immediato.

Cerca @BotFather su Telegram e crea un nuovo bot per ottenere un Token.

Avvia una chat con il tuo bot e scrivi qualcosa.

Usa questo codice per inviare il riassunto:

"""
import requests

def send_telegram_msg(text):
    token = "IL_TUO_TOKEN_BOT"
    chat_id = "IL_TUO_CHAT_ID" # Puoi trovarlo con il bot @userinfobot
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, data=payload)