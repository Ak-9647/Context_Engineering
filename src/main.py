from write.user_profile import get_user_profile
from select.document_retriever import get_q3_sales_performance_pdf, get_project_phoenix_q3_retro
from compress.summarizer import summarize_documents
from isolate.tool_isolator import get_isolated_tool_schema
from assembler.prompt_assembler import assemble_prompt


def main():
    # Step 1: WRITE (Memory)
    user_profile = get_user_profile()

    # Step 2: SELECT (RAG)
    doc1 = get_q3_sales_performance_pdf()
    doc2 = get_project_phoenix_q3_retro()
    documents = [doc1, doc2]

    # Step 3: COMPRESS
    summarized_data = summarize_documents(documents)

    # Step 4: ISOLATE
    isolated_tool = get_isolated_tool_schema()

    # Step 5: Assemble final prompt
    original_query = "Help me write my Q3 performance report."
    final_prompt = assemble_prompt(user_profile, summarized_data, isolated_tool, original_query)

    print("\n===== CLAUDE-STYLE CONTEXT-ENGINEERED PROMPT =====\n")
    print(final_prompt)
    print("\n===============================================\n")

if __name__ == "__main__":
    main()
