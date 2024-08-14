from rag_prep_tool.graph_db.get_chatgpt_response import get_chatgpt_response


def get_entities_terms(text:str):
    """ Get entities and terms from text"""
    prompt = f"""
            ## Objective:
            You are a top-tier algorithm designed for extracting all entities from the input text to build a knowledge graph.

            ## Instructions:
            -Extract key entities from the following text that are capable of having properties, and identify their types (e.g., Person, Organization, Location, Event, etc.). 
            -Exclude non-entity elements like dates or simple attributes. 
            -Other than the entities, don't include any other information.
            -The text content is book by Dalai Lama.So the pronoun 'I' refers to Dalai Lama.
            
            ## Output format:
            Entity Name: Entity Type
            Entity Name: Entity Type
            .
            .


            [INPUT TEXT START]
            {text}
            [INPUT TEXT END]

    """
    response_text = ""

    for response in get_chatgpt_response(prompt):
        response_text += response 
    
    entities = response_text.split("\n")
    entities = [entity.strip() for entity in entities if entity.strip() != ""]
    entities = list(set(entities))
    return entities


if __name__ == "__main__":
    from pathlib import Path 

    text = Path("mlmp_first_page.txt").read_text(encoding="utf-8") 
    entities = get_entities_terms(text)
    print(f"Number of entities: {len(entities)}")
    print(entities)