# per mandare mail da python
import smtplib
from email.message import EmailMessage
import json
#from openai import OpenAI
from groq import Groq

#client = OpenAI(api_key="TUA_CHIAVE_OPENAI")
client = Groq(api_key="Api-KeY")


def send_email(body, subject="Nota dell'agente AI"):
    try:
        msg = EmailMessage()
        msg.set_content(body)
        msg['Subject'] = subject
        msg['From'] = "example@libero.it"
        msg['To'] = "example@gmail.com"

    # Connessione al server Gmail
        with smtplib.SMTP_SSL('smtp.libero.it', 465) as smtp:
            smtp.login("example@libero.it", "Password")
            smtp.send_message(msg)
            return "Mail inviata con successo"
    except Exception as e:
        return f"Errore nell'invio: {e}"
# 2. Descriviamo la funzione all'IA (il "Contratto")
tools = [
    {
        "type": "function",
        "function": {
            "name": "send_email",
            "description": "Invia una mail per ricordare qualcosa o notificare l'utente",
            "parameters": {
                "type": "object",
                "properties": {
                    "subject": {"type": "string", "description": "oggetto della mail."},
                    "body": {"type": "string", "description": "Il messaggio completo da inviare."}
                },
                "required": ["body"]
            }
        }
    }
]

# 3. Chiediamo all'IA di decidere
user_input = "Invia una mail a te stesso con scritto che devo comprare il latte"

response = client.chat.completions.create(
    #model="gpt-4o",
    model="llama-3.1-8b-instant", # Modello veloce e gratuito
    #model="llama-3.3-70b-versatile",
    messages=[{"role": "user", "content": user_input}],
    tools=tools,
    tool_choice="auto"
)

# 4. Gestione della chiamata
message = response.choices[0].message
tool_calls = message.tool_calls

if tool_calls:
    for call in tool_calls:
        # L'IA ha deciso di usare la funzione!
        args = json.loads(call.function.arguments)
        
        risultato = send_email(
            body=args.get('body'), 
            subject=args.get('subject', 'Promemoria IA')
        )
        print(f"Azione eseguita: {risultato}")
else:
    print("L'IA non ha ritenuto necessario inviare una mail.")