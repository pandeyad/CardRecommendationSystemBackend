from pyexpat.errors import messages
from warnings import deprecated

import openai
from langchain_community.document_loaders import TextLoader

from src import load_config
from src.llm.base_model_function import IModelFunction
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
import shutil
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate


# Question :
# Which card will be best for me considering that my monthly spends are as follows : ~0.1 Million on online shopping,
# ~0.1 Million on travelling and ~0.05 Million INR on groceries and other stuff.

@deprecated("Require high token count for this to process. Will revisit with a better approach.")
class OpenAISimilaritySearchRecommendationModel(IModelFunction):
    __model_name__ = 'openai-similarity-search-model'

    PROMPT_TEMPLATE = """
    Answer the question based only on the following context:
    
    {context}
    
    ---
    
    Answer the question based on the above context: {question}
    """

    def __init__(self):
        super().__init__()
        self.db = None
        self.key = self.get_config().get('openai', {}).get('key', '')
        if not self.key:
            raise Exception("No OpenAI Key is present. Please ensure the key is present in configuration.")
        self.chroma_path = 'openai-chroma-collection'


    def prepare_model(self):
        try:
            docs = [TextLoader(file_path=fp, encoding='utf-8').load() for fp in self.files]
            docs_list = [item for sublist in docs for item in sublist]
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=10000,
                chunk_overlap=500,
                length_function=len,
                add_start_index=True,
            )
            chunks = text_splitter.split_documents(docs_list)
            print(f"Split {len(docs_list)} documents into {len(chunks)} chunks.")

            document = chunks[10]
            print(document.page_content)
            print(document.metadata)
            # Clear out the database first.
            if os.path.exists(self.chroma_path):
                shutil.rmtree(self.chroma_path)

            # Create a new DB from the documents.
            embedding_function = OpenAIEmbeddings(model="text-embedding-ada-002", openai_api_key=self.key)
            self.db = Chroma.from_documents(
                chunks, embedding_function, persist_directory=self.chroma_path
            )
            print(f"Saved {len(chunks)} chunks to {self.chroma_path}.")
        except:
            return

    def recommend(self, query):
        self.db.persist()
        results = self.db.similarity_search_with_relevance_scores(query, k=self.get_config().get('ranking-groups'))
        if len(results) == 0 or results[0][1] < 0.5:
            print(f"Unable to find matching results.")
            return
        context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
        prompt_template = ChatPromptTemplate.from_template(self.PROMPT_TEMPLATE)
        prompt = prompt_template.format(context=context_text, question=query)
        print(prompt)

        model = ChatOpenAI()
        response_text = model.predict(prompt)
        # sources = [doc.metadata.get("source", None) for doc, _score in results]
        return response_text
