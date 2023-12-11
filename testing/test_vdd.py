# from graphviz import Digraph

# # # Create a directed graph
# # graph = Digraph('FunctionRelationships', format='png')

# # # Add nodes (functions) with filenames and color backgrounds
# # graph.node('file1.py', 'file1.py (Streamlit App)', shape='box', color='lightblue', style='filled')
# # graph.node('st.set_page_config', 'st.set_page_config', shape='box', color='lightyellow', style='filled')
# # graph.node('st.header', 'st.header', shape='box', color='lightyellow', style='filled')
# # graph.node('st.sidebar.text_input', 'st.sidebar.text_input', shape='box', color='lightyellow', style='filled')
# # graph.node('gpt4_process.control', 'gpt4_process.control', shape='box', color='lightyellow', style='filled')
# # graph.node('st.spinner', 'st.spinner', shape='box', color='lightyellow', style='filled')
# # graph.node('st.markdown', 'st.markdown', shape='box', color='lightyellow', style='filled')
# # graph.node('gpt4_process.py', 'gpt4_process.py', shape='box', color='lightgreen', style='filled')
# # graph.node('create_base_prompt', 'create_base_prompt', shape='box', color='lightyellow', style='filled')
# # graph.node('check_prompt_tokens', 'check_prompt_tokens', shape='box', color='lightyellow', style='filled')
# # graph.node('get_response_README', 'get_response_README', shape='box', color='lightyellow', style='filled')
# # graph.node('parse_response', 'parse_response', shape='box', color='lightyellow', style='filled')
# # graph.node('control', 'control', shape='box', color='lightyellow', style='filled')
# # graph.node('openai.ChatCompletion.create', 'openai.ChatCompletion.create', shape='box', color='lightyellow', style='filled')

# # # Add edges (function calls)
# # graph.edge('file1.py', 'st.set_page_config')
# # graph.edge('file1.py', 'st.header')
# # graph.edge('file1.py', 'st.sidebar.text_input')
# # graph.edge('file1.py', 'st.sidebar.radio')
# # graph.edge('file1.py', 'st.sidebar.button')
# # graph.edge('file1.py', 'gpt4_process.control')
# # graph.edge('file1.py', 'llama2_process.control')
# # graph.edge('file1.py', 'st.spinner')
# # graph.edge('file1.py', 'st.markdown')
# # graph.edge('file1.py', 'st.table')
# # graph.edge('gpt4_process.control', 'create_base_prompt')
# # graph.edge('gpt4_process.control', 'check_prompt_tokens')
# # graph.edge('gpt4_process.control', 'get_response_README')
# # graph.edge('gpt4_process.control', 'parse_response')
# # graph.edge('gpt4_process.control', 'control')
# # graph.edge('gpt4_process.control', 'openai.ChatCompletion.create')

# # # Render and save the graph as a PNG file
# # graph.render(filename='function_relationships1', directory='.', cleanup=True, format='png')

# # print("Diagram exported to function_relationships.png")

# # from graphviz import Digraph

# class Entity:
#     def __init__(self, name, attributes=None):
#         self.name = name
#         self.attributes = attributes or []

#     def add_attribute(self, attribute):
#         self.attributes.append(attribute)

#     def __str__(self):
#         return f"{self.name} ({', '.join(self.attributes)})"


# class Relationship:
#     def __init__(self, name, entities):
#         self.name = name
#         self.entities = entities

#     def __str__(self):
#         return f"{self.name} ({', '.join(entity.name for entity in self.entities)})"


# class ERD:
#     def __init__(self):
#         self.entities = []
#         self.relationships = []

#     def add_entity(self, entity):
#         self.entities.append(entity)

#     def add_relationship(self, relationship):
#         self.relationships.append(relationship)

#     def display(self):
#         print("Entities:")
#         for entity in self.entities:
#             print(f"  {entity}")

#         print("\nRelationships:")
#         for relationship in self.relationships:
#             print(f"  {relationship}")

#     def to_dot(self):
#         dot = Digraph(comment='ERD')

#         for entity in self.entities:
#             dot.node(entity.name, f"{entity.name}\n({', '.join(entity.attributes)})")

#         for relationship in self.relationships:
#             entity_names = [entity.name for entity in relationship.entities]
#             dot.node(relationship.name, f"{relationship.name}\n({', '.join(entity_names)})")
#             for entity in relationship.entities:
#                 dot.edge(entity.name, relationship.name)

#         return dot

def write_erd(database):
    data = {} # key - table_name ,  value: list of fields of the database and their type
    """ Note: to access element of a dictionnary, you use: table_name= data["table_1"] which returns a list of columns. So to get the column from that list we used column = table[0] to set it as a string""" 
    tables = {} # key - Table Name, value - their primary keys.
    
    for n in range(len(database)):  
        line_read = database.splitlines() # use .readlines() and we get the list of lines and .splitlines to make the list a new element so we don't get a list inside an other one. 
        
        if '=' in line_read[n]: # line read: table name (table) = <function>. 
            
            # Finds the column name and sets it as a string, do the same for its type and set them in their respective dictionaries with key=table_name.
            test1 = str(line_read[n])
            words = test1.split() # [<statement>, = , <function>] 
            
            table_name = words[-2] # use -2 to get the second last element which is the table name.
            table = database[(database.index(table_name))+3].split(',') # split by column, find the column in the line that we have just extracted from database[n], column=words[-1].
            
            data[str(table_name)] = table 
            tables[table_name] = [] # define an empty list in this dictionnary. 
        
        elif ',' in line_read[n]: # <column name>,<type>
            table = database[(database.index(line_read[n]))+1].split(',') # we use the last element of each table to find its column names and types so we start by +1 on top of lines where the primary keys are defined and then we use split by ","
            
            for n in range (len(table)): # we go through every line that have comma inside. 
                words = str(table[n]).split

# Example usage:
if __name__ == "__main__":
    # erd = ERD()

    # erd = ERD()

    # # Creating entities
    # person_entity = Entity("Person", ["ID", "Name", "Age"])
    # address_entity = Entity("Address", ["ID", "Street", "City", "Zip"])

    # # Creating relationships
    # lives_relationship = Relationship("Lives", [person_entity, address_entity])

    # # Adding entities and relationships to the ERD
    # erd.add_entity(person_entity)
    # erd.add_entity(address_entity)
    # erd.add_relationship(lives_relationship)

    # # Displaying the ERD
    # erd.display()

    # Generate the DOT format representation
    dot_representation = erd.to_dot()

    # Save the DOT representation to a file (optional)
    dot_file_path = "erd.dot"
    dot_representation.save(dot_file_path)

    # Convert DOT to PNG using Graphviz (requires Graphviz software installed)
    png_file_path = "erd.png"
    dot_representation.render(png_file_path, format='png', cleanup=True)

    print(f"ERD image saved to {png_file_path}")


    
