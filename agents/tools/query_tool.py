import os
from typing import Optional
from langchain_core.tools import tool
from db import chroma_db

@tool
def get_results(query):
    '''
    Find possible answers to questions 

    Returns:
        list: best answers
    '''

    try:
        results = chroma_db.get_results(f'{query}')['documents'][0]
    except Exception as e:
        results = str(e)
    return results