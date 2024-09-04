from rag_prep_tool.graph_db.llm import get_chatgpt_response

def coref_text(text:str):
    """ Perform coreference resolution on text"""
    prompt = f"""
            ## Objective:
            You are a top-tier algorithm designed for resolving coreferences in the input text to build a knowledge graph.

            ## Instructions:
            -Resolve all the coreferences in the following text.
            -Replace the pronouns with the actual entities.
            -Other than the resolved text, don't include any other information.
            -The text content is book by Dalai Lama.So the pronoun 'I' refers to Dalai Lama.
            
            ## Output format:
            Resolved text

            [INPUT TEXT START]
            {text}
            [INPUT TEXT END]

    """
    
    try:
        response_text = "".join(get_chatgpt_response(prompt))
        return response_text
    except Exception as e:
        print(f"Error occurred: {e}")
        return ""