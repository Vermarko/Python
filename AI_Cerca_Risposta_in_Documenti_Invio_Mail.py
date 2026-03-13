import smtplib
from email.message import EmailMessage
import json
import os
from groq import Groq
from PyPDF2 import PdfReader
from langchain_text_splitters import CharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# Inizializzazioni
client = Groq(api_key="API-KEY")
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
#
def prepara_conoscenza(cartella_pdf):
    print("--- Fase 1: Lettura PDF ---")
    raw_text = ""
    for filename in os.listdir(cartella_pdf):
        if filename.endswith(".pdf"):
            reader = PdfReader(os.path.join(cartella_pdf, filename))
            for page in reader.pages:
                raw_text += page.extract_text()
    
    print("--- Fase 2: Creazione Pezzi (Chunking) ---")
    text_splitter = CharacterTextSplitter(separator="\n", chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_text(raw_text)
    
    print("--- Fase 3: Creazione Database Vettoriale locale ---")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vector_store = FAISS.from_texts(texts=chunks, embedding=embeddings)
    return vector_store
#
# 1. CARICAMENTO DATABASE PDF (Assumiamo che tu lo abbia già creato e salvato)
# Se non lo hai salvato, usa la funzione 'prepara_conoscenza' della lezione precedente
#db_pdf = FAISS.load_local("mio_indice_faiss", embeddings, allow_dangerous_deserialization=True)
db_pdf = prepara_conoscenza("C:/Users/Marco/Desktop/Cure Domiciliari/OK_Approvazione delle convenzioni con le ASL per l'erogazione delle Cure Domiciliari Integrate")
# --- GLI STRUMENTI (TOOLS) ---

def cerca_nei_pdf(domanda):
    """Cerca informazioni specifiche nei documenti PDF caricati."""
    docs = db_pdf.similarity_search(domanda, k=2)
    return "\n".join([d.page_content for d in docs])

def invia_email(corpo, oggetto="Report Agente IA"):
    """Invia una mail con il testo specificato."""
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

# --- DEFINIZIONE TOOLS PER L'IA ---

tools = [
    {
        "type": "function",
        "function": {
            "name": "cerca_nei_pdf",
            "description": "Usa questo tool per rispondere a domande basate sui documenti privati dell'utente.",
            "parameters": {
                "type": "object",
                "properties": {"domanda": {"type": "string"}},
                "required": ["domanda"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "invia_email",
            "description": "Invia un riassunto o una nota via email all'utente.",
            "parameters": {
                "type": "object",
                "properties": {
                    "corpo": {"type": "string", "description": "Il testo della mail."},
                    "oggetto": {"type": "string"}
                },
                "required": ["corpo"]
            }
        }
    }
]

# --- CICLO DI RAGIONAMENTO (AGENT LOOP) ---

def esegui_agente(richiesta_utente):
    messages = [
        {
            "role": "system", 
            "content": "Sei un assistente operativo. Se l'utente chiede informazioni presenti nei documenti, USA SEMPRE il tool 'cerca_nei_pdf'. Se l'utente chiede di inviare una mail, USA il tool 'invia_email'."
        },
        {
        "role": "user", "content": richiesta_utente
        }]
    
    # Primo passaggio: l'IA decide cosa fare
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,
        tools=tools,
        tool_choice="auto", # Forza l'IA a considerare i tool
        temperature=0.1     # Abbassiamo la temperatura per rendere l'IA più precisa e meno creativa
    )
    
    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls
    
    if tool_calls:
        # L'IA potrebbe voler chiamare più tool in sequenza!
        for tool_call in tool_calls:
            nome_funzione = tool_call.function.name
            argomenti = json.loads(tool_call.function.arguments)
            
            if nome_funzione == "cerca_nei_pdf":
                risultato = cerca_nei_pdf(argomenti['domanda'])
                print(f"-> L'IA ha letto i PDF per rispondere a: {argomenti['domanda']}")
            elif nome_funzione == "invia_email":
                risultato = invia_email(argomenti['corpo'], argomenti.get('oggetto'))
                print(f"-> L'IA ha inviato una mail.")
            
            # (Opzionale) Possiamo rimandare il risultato all'IA per una risposta finale
            return f"Azione '{nome_funzione}' completata: {risultato[:50]}..."
    
    return response_message.content

# ESEMPIO DI UTILIZZO
#print(esegui_agente("Controlla nei documenti cosa cosiste approvazione e convenzioni con le ASL per le cure domiciliari"))
esegui_agente("Cosa trattano questi documenti, cosa centrano le Asl?")