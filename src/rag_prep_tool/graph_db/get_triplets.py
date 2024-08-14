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
    
    try:
        response_text = "".join(get_chatgpt_response(prompt))
        entities = list({entity.strip() for entity in response_text.splitlines() if entity.strip()})
        return sorted(entities)
    except Exception as e:
        print(f"Error occurred: {e}")
        return []

def generate_relations(text:str):
    """ Get relations from text"""
    prompt = f"""
            ## Objective:
            You are a top-tier algorithm designed for extracting all relations that would be use to connect between entities from the input text to build a knowledge graph.

            ## Instructions:
            -relations should be verbs or verb phrases that connect entities such as 'is', 'was', 'has', 'belongs to', etc.
            -Extract key relations from the following text that are connecting entities(e.g., Person, Organization, Location, Event, etc.) . 
            -Other than the relations, don't include any other information.
            
            
            ## Output format:
            Each relation name should be on a new line.


            [INPUT TEXT START]
            {text}
            [INPUT TEXT END]

    """
    
    try:
        response_text = "".join(get_chatgpt_response(prompt))
        relations = list({relation.strip() for relation in response_text.splitlines() if relation.strip()})
        return sorted(relations)
    except Exception as e:
        print(f"Error occurred: {e}")
        return []
    
if __name__ == "__main__":
    from pathlib import Path 

    text = Path("mlmp_first_page.txt").read_text(encoding="utf-8") 
    relations = generate_relations(text)
    print(f"Number of relations: {len(relations)}")
    print(relations)

    entities = get_entities_terms(text)
    print(f"Number of entities: {len(entities)}")
    print(entities)