import json 
import networkx as nx
import matplotlib.pyplot as plt

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

def visualize_knowledge_graph(data, file_name="knowledge_graph.png"):
    # Create a directed graph
    G = nx.DiGraph()

    # Add nodes
    for node in data['nodes']:
        G.add_node(node['label'], label=node['type'], **node.get('properties', {}))

    # Add edges
    for rel in data['relationships']:
        G.add_edge(rel['source'], rel['target'], label=rel['type'])

    # Draw the graph
    pos = nx.spring_layout(G, k=0.5, seed=42)  # Adjust 'k' to increase/decrease spacing
    plt.figure(figsize=(14, 10))  # Increase figure size for better spacing
    nx.draw(G, pos, with_labels=True, node_color='lightblue', font_weight='bold', node_size=6000, font_size=12)
    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10)
    
    # Save the graph as an image
    plt.savefig(file_name, format="PNG", bbox_inches='tight')
    plt.close()

if __name__ == "__main__":


    with open("triplets.json", "r") as f:
        data = json.load(f)
    visualize_knowledge_graph(data)
    