from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from langchain_ollama import ChatOllama
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain.text_splitter import CharacterTextSplitter
from langchain_ollama.embeddings import OllamaEmbeddings
from src.llm.base_model_function import IModelFunction, recommendation_app

from src.utils.python_util import get_nested


# Question :
# Which card will be best for me considering that my monthly spends are as follows : ~0.1 Million on online shopping,
# ~0.1 Million on travelling and ~0.05 Million INR on groceries and other stuff.

class OllamaMistralNomicEmbedTextRecommendationModel(IModelFunction):

    __model_name__ = 'ollama-mistral-nomic-embed-text'

    recommendation_model = None

    def __init__(self):
        super().__init__()

    def prepare_model(self):
        model_local = ChatOllama(model="mistral")
        docs = [TextLoader(file_path=fp, encoding='utf-8').load() for fp in self.files]
        docs_list = [item for sublist in docs for item in sublist]
        text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=int(self.get_config()['chunk_size']),
            chunk_overlap=int(self.get_config()['chunk_overlap']))
        doc_splits = text_splitter.split_documents(docs_list)
        vectorstore = Chroma.from_documents(
            documents=doc_splits,
            collection_name="ollama-mistral-nomic-embed-text-chromadb",
            embedding=OllamaEmbeddings(model='nomic-embed-text'),
        )
        retriever = vectorstore.as_retriever()

        after_rag_template = """Answer the question based only on the following context:
        {context}
        Question: {question}
        """
        after_rag_prompt = ChatPromptTemplate.from_template(after_rag_template)
        self.recommendation_model = (
                {"context": retriever, "question": RunnablePassthrough()}
                | after_rag_prompt
                | model_local
                | StrOutputParser()
        )

    def recommend(self, query):
        return self.recommendation_model.invoke(query)
