
def summarize_documents(docs):
    """
    Summarizes a list of documents into key bullet points.
    In a real application, this would use a summarization model (e.g., a smaller LLM).
    """
    # For this example, we are using the pre-computed summaries from the PRD.
    # In a real scenario, you would parse the docs and generate these summaries.
    return [
        "Key Q3 Sales Data: Sales exceeded target by 15%.",
        "Key Project Phoenix Data: Launched successfully, user adoption 10% below forecast."
    ] 