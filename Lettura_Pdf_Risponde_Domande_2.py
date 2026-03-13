import os
from groq import Groq
from PyPDF2 import PdfReader
from langchain_text_splitters import CharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# 1. Inizializzazione Client (Assicurati di avere la KEY nelle variabili d'ambiente o incollala qui)
client = Groq(api_key="API-KEY")

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

def chiedi_all_ia(query, vector_store):
    # Cerca i 3 pezzi più rilevanti
    docs = vector_store.similarity_search(query, k=3)
    context = "\n---\n".join([d.page_content for d in docs])

    prompt = f"""Usa solo questi estratti per rispondere. Se non sai, di' 'Non trovato'.
    CONTESTO:
    {context}
    DOMANDA: {query}"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "system", "content": "Sei un assistente che analizza documenti tecnici."},
                  {"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# --- ESECUZIONE PRINCIPALE ---
if __name__ == "__main__":
    # Assicurati che la cartella esista
    cartella = "C:/Users/Marco/Desktop/Cure Domiciliari/OK_Approvazione delle convenzioni con le ASL per l'erogazione delle Cure Domiciliari Integrate"
    if not os.path.exists(cartella):
        os.makedirs(cartella)
        print(f"Ho creato la cartella '{cartella}'. Metti dentro i PDF e riavvia!")
    else:
        cervello_ia = prepara_conoscenza(cartella)
        
        while True:
            domanda = input("\nCosa vuoi sapere dai documenti? (o scrivi 'esci'): ")
            if domanda.lower() == 'esci': break
            
            risposta = chiedi_all_ia(domanda, cervello_ia)
            print(f"\nRISPOSTA IA:\n{risposta}")