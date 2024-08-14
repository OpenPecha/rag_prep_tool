from rag_prep_tool.graph_db.get_chatgpt_response import get_chatgpt_response


def get_entities_terms(text:str):
    """ Get entities and terms from text"""
    prompt = f"""
            
            Extract key entities from the following text that are capable of having properties, and identify their types (e.g., Person, Organization, Location, Event, etc.). Include any relevant relationships between them. Exclude non-entity elements like dates or simple attributes. Present the information in the following output format:
            Entity Name: Entity Type
            Entity Name: Entity Type
            .
            .


            [TEXT START]
            {text}
            [TEXT END]

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