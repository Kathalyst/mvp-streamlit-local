
#Python program to print topological sorting of a DAG
from collections import defaultdict
 
#Class to represent a graph
class Graph:
    def __init__(self,vertices):
        self.graph = defaultdict(list) #dictionary containing adjacency List
        self.V = vertices #No. of vertices
 
    # function to add an edge to graph
    def addEdge(self,u,v):
        self.graph[u].append(v)
 
    # A recursive function used by topologicalSort
    def topologicalSortUtil(self,v,visited,stack):
 
        # Mark the current node as visited.
        visited[v] = True
 
        # Recur for all the vertices adjacent to this vertex
        for i in self.graph[v]:
            if visited[i] == False:
                self.topologicalSortUtil(i,visited,stack)
 
        # Push current vertex to stack which stores result
        stack.insert(0,v)
 
    # The function to do Topological Sort. It uses recursive
    # topologicalSortUtil()
    def topologicalSort(self):
        # Mark all the vertices as not visited
        visited = [False]*self.V
        stack =[]
 
        # Call the recursive helper function to store Topological
        # Sort starting from all vertices one by one
        for i in range(self.V):
            if visited[i] == False:
                self.topologicalSortUtil(i,visited,stack)
 
        # Print contents of stack
        print (stack)
        return (stack)


def new_order_for_processing(matches):
    # extract all source_of_external_functions in order from matches
    source_of_external_functions = []
    filenames = []
    for match in matches:
        for file in match:
            source_of_external_functions.append(file['source_of_external_functions'])
            filenames.append(file['filename'])
    g= Graph(len(filenames))
    for i in range(len(filenames)):
        source = source_of_external_functions[i]
        for i in range(len(source)):
            s = source[i]
            if s in filenames:
                pos = filenames.index(s)
                g.addEdge(pos,i)

    print ("Following is a Topological Sort of the given graph")
    position_score = g.topologicalSort()

    new_matches = []
    for i in range(len(position_score)):
        new_matches.append(matches[position_score[i]])
 
    return new_matches

if __name__== "__main__":
    matches =  [[{'filename': 'hello.py', 'internal_functions': ['control', 'tabs', 'spinner', 'markdown'], 'external_functions': ['gpt4_process.control', 'llama2_process.control', 'pd.DataFrame'], 'source_of_external_functions': ['gpt4_process.py', 'llama2_process.py', 'pandas/__init__.py']}], [{'filename': 'llama2_process.py', 'internal_functions': ['remove_non_ascii', 'create_base_prompt', 'custom_prompt', 'control'], 'external_functions': ['LlamaForCausalLM', 'CodeLlamaTokenizer', 'pipeline', 'torch', 'vault', 'os', 'replicate'], 'source_of_external_functions': ['transformers', 'transformers', 'transformers', 'torch', 'vault.py', 'os', 'replicate']}], [{'filename': 'vault.py', 'internal_functions': ['get_Access_Token', 'get_Secret'], 'external_functions': ['requests.post', 'requests.get'], 'source_of_external_functions': ['requests', 'requests']}], [{'filename': 'github_process.py', 'internal_functions': ['clone_repo', 'read_files_in_directory', 'remove_empty_files', 'control'], 'external_functions': [], 'source_of_external_functions': []}], [{'filename': 'gpt4_process.py', 'internal_functions': ['create_base_prompt', 'check_prompt_tokens', 'get_response_README', 'parse_response', 'control'], 'external_functions': ['openai.api_key', 'tiktoken.encoding_for_model', 'openai.ChatCompletion.create'], 'source_of_external_functions': ['openai', 'tiktoken']}]]
    print(new_order_for_processing(matches))