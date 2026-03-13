"""
Progetto 2: Il tuo "Analista di Documenti" Personale
1. Gli strumenti del mestiere
Per questo progetto ci servono librerie che gestiscono i PDF e i "vettori" (il linguaggio matematico dell'IA).

Bash
pip install PyPDF2 langchain langchain-community sentence-transformers faiss-cpu
"""
import os
from PyPDF2 import PdfReader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings 

# 1. Caricamento e Lettura PDF
def load_pdfs(folder_path):
    raw_text = ""
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            reader = PdfReader(os.path.join(folder_path, filename))
            for page in reader.pages:
                raw_text += page.extract_text()
    return raw_text

# 2. Suddivisione in pezzi (Chunking)
# L'IA lavora meglio con piccoli pezzi di testo
def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200, # Sovrapponiamo i pezzi per non perdere il contesto
        length_function=len
    )
    return text_splitter.split_text(text)

# 3. Creazione del "Cervello" (Vector Store)
def create_vector_store(chunks):
    # Usiamo un modello di embedding gratuito che gira sul tuo PC
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vector_store = FAISS.from_texts(texts=chunks, embedding=embeddings)
    return vector_store

# ESECUZIONE
testo_totale = load_pdfs("C:/Users/Marco/Desktop/Cure Domiciliari/OK_Approvazione delle convenzioni con le ASL per l'erogazione delle Cure Domiciliari Integrate")
pezzi_di_testo = get_text_chunks(testo_totale)
conoscenza_ia = create_vector_store(pezzi_di_testo)

# 4. Ricerca (Esempio)
#domanda = "Qual è la scadenza del progetto X citata nei documenti?"
domanda = "Che tipo di approvazine necessita la convenzione con le ASL?"
documenti_rilevanti = conoscenza_ia.similarity_search(domanda)

print("L'IA ha trovato queste parti rilevanti:")
for doc in documenti_rilevanti:
    print(f"---\n{doc.page_content[:200]}...")