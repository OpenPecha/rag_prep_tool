import json 
from rag_prep_tool.graph_db.llm import get_chatgpt_response


def extract_entities(text:str):
    """ Get entities and terms from text"""
    prompt = f"""
            ## Objective:
            You are a top-tier algorithm designed for extracting all entities from the input text to build a knowledge graph.

            ## Instructions:
            -Extract key entities from the following text that are capable of having properties, and identify their types (e.g., Person, Organization, Location, Event, etc.). 
            -Exclude non-entity elements like dates or simple attributes. 
            -Entities should always be singular and proper nouns.
            -The text content is book by Dalai Lama.So the pronoun 'I' refers to Dalai Lama.
            -Entities should be in CamelCase.
            -Other than the entities, don't include any other information.
            
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

def extract_relations(text:str):
    """ Get relations from text"""
    prompt = f"""
            ## Objective:
            You are a top-tier algorithm designed for extracting all relations that would be use to connect between entities from the input text to build a knowledge graph.

            ## Instructions:
            -relations should be verbs or verb phrases that connect entities such as 'is', 'was', 'has', 'belongs to', etc.
            -Extract key relations from the following text that are connecting entities(e.g., Person, Organization, Location, Event, etc.) . 
            -Relations should be always be verbs or verb phrases.
            -Relations should be in CamelCase.
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
    

def build_triplets(text:str):
    """ Get entities, relations and triplets from text"""
    entities = extract_entities(text)
    relations = extract_relations(text)
    entities_str = "\n".join(entities)
    relations_str = "\n".join(relations)
    prompt = f"""
            ## 1. Overview
            You are a top-tier algorithm designed for extracting information in structured formats to build a knowledge graph.
            - **Nodes** represent entities and concepts. 
            
            ## 2. Labeling Nodes
            - **Consistency**: Ensure you use only given in entities for labeling Nodes.                        
            - **Node labels**: Never utilize integers as node labels. Node labels should be names or human-readable identifiers found in the text.
            
                        
            ## 3. Handling Numerical Data and Dates
            - Numerical data, like age or other related information, should be incorporated as attributes or properties of the respective nodes.
            - **Property Format**: Properties must be in a key-value format.
            - **Quotation Marks**: Never use escaped single or double quotes within property values.
            - **Naming Convention**: Use camelCase for property keys, e.g., `birthDate`.
                
            ## 5. Strict Compliance
            -Adhere to the rules strictly. Non-compliance will result in termination.

            [ENTITIES START]
            {entities_str}
            [ENTITIES END]

            [RELATIONS START]
            {relations_str}
            [RELATIONS END]

            [INPUT TEXT START]
            {text}
            [INPUT TEXT END]
    """

    response_text = get_chatgpt_response(prompt)
    return response_text

def parse_build_triplets_output(response):
    cleaned_text = response.strip('```json\n')

    # Step 2: Convert the cleaned JSON string to a Python dictionary
    json_data = json.loads(cleaned_text)

    return json_data


if __name__ == "__main__":
    text = """
    The Art of Happiness is a book by the Dalai Lama and Howard Cutler, a psychiatrist who posed questions to the Dalai Lama. Cutler quotes the Dalai Lama as saying that the purpose of life is to seek happiness. He writes that the Dalai Lama suggests that the more we care for the happiness of others, the greater our own sense of well-being becomes. Cutler also reports that the Dalai Lama believes that a person can only obtain true happiness by living in harmony with others. The book explores training the human mind to seek happiness.
    """
    
    response_text = "".join(build_triplets(text))
    response_json = parse_build_triplets_output(response_text)

    # Now `json_data` is a dictionary you can work with
    with open("triplets.json", "w") as f:
        json.dump(response_json, f, indent=4)
    