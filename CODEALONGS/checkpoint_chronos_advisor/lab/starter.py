"""Checkpoint lab: compose the local chat, RAG, and bounded agent seams."""

def build_messages(portfolio, history, question):
    raise NotImplementedError("Add trusted facts and history[-4:] to the messages.")

def build_policy_engine(documents):
    raise NotImplementedError("Return a VectorStoreIndex query engine.")

def allowed_client(client_id):
    raise NotImplementedError("Allow Alice only before a portfolio tool call.")
