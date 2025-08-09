import os
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import JSONLoader
from openai import OpenAI

class RAGSystem:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings()
        self.vectorstore = None
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
    def initialize(self):
        if self.vectorstore:
            return
            
        loaders = [
            JSONLoader("data/ai_curriculum.json"),
            JSONLoader("data/ai_product.json")
        ]
        documents = []
        for loader in loaders:
            documents.extend(loader.load())
        
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        docs = text_splitter.split_documents(documents)
        
        self.vectorstore = Chroma.from_documents(docs, self.embeddings, persist_directory="./chroma_db")
    
    def answer_question(self, question: str):
        if not self.vectorstore:
            self.initialize()
        
        docs = self.vectorstore.similarity_search(question, k=3)
        context = "\n".join([d.page_content for d in docs])
        
        prompt = f"""
        Ты - консультант для абитуриентов ИТМО. Отвечай ТОЛЬКО на вопросы, связанные с магистерскими программами по ИИ.
        Используй только предоставленный контекст:
        
        {context}
        
        Вопрос: {question}
        Ответ:"""
        
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            max_tokens=500
        )
        return response.choices[0].message.content

rag_system = RAGSystem()
rag_system.initialize()

def answer_question(question: str):
    return rag_system.answer_question(question)