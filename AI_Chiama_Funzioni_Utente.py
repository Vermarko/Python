import json
#from openai import OpenAI
from groq import Groq

#client = OpenAI(api_key="TUA_CHIAVE_OPENAI")
client = Groq(api_key="API-KEY")

# 1. Definiamo la funzione reale in Python
def scrivi_nota_su_file(contenuto, nome_file="note.txt"):
    with open(nome_file, "a") as f:
        f.write(contenuto + "\n")
    return f"Nota salvata con successo in {nome_file}!"

# 2. Descriviamo la funzione all'IA (il "Contratto")
tools = [
    {
        "type": "function",
        "function": {
            "name": "scrivi_nota_su_file",
            "description": "Salva un testo o un promemoria in un file fisico.",
            "parameters": {
                "type": "object",
                "properties": {
                    "contenuto": {"type": "string", "description": "Il testo da salvare."},
                    "nome_file": {"type": "string", "description": "Il nome del file (opzionale)."}
                },
                "required": ["contenuto"]
            }
        }
    }
]

# 3. Chiediamo all'IA di decidere
user_input = "Ricordami di comprare il latte nel file della spesa"

response = client.chat.completions.create(
    #model="gpt-4o",
    model="llama-3.1-8b-instant", # Modello veloce e gratuito
    #model="llama-3.3-70b-versatile",
    messages=[{"role": "user", "content": user_input}],
    tools=tools,
    tool_choice="auto"
)

# 4. Gestiamo la chiamata dello strumento
tool_calls = response.choices[0].message.tool_calls
if tool_calls:
    for call in tool_calls:
        # L'IA ha deciso di usare la funzione!
        args = json.loads(call.function.arguments)
        risultato = scrivi_nota_su_file(args['contenuto'], args.get('nome_file', 'note.txt'))
        print(f"L'Agente ha eseguito l'azione: {risultato}")