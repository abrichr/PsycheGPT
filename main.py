import io
import json

from loguru import logger
from openai import OpenAI
from PIL import Image
import networkx as nx
import pygraphviz as pgv

from config import settings


client = OpenAI(
    api_key=settings.openai_api_key,
)


class PsychologicalModule:
    def __init__(self, name: str, function: str):
        self.name = name
        self.function = function
        self.inputs = []
        self.outputs = []
        self.system_prompt = "You are simulating a human mind."
        self.base_prompt = (
            f"This is a simulation of a psychological module called '{name}'. "
            f"Its main function is to {function}."
        )

    def add_input(self, module: 'PsychologicalModule'):
        self.inputs.append(module)

    def add_output(self, module: 'PsychologicalModule'):
        self.outputs.append(module)

    def process_information(self):
        logger.info(f"Processing in {self.name}")
        prompt = f"{self.base_prompt} How would this module process information given its function?"
        response = self.prompt_llm(prompt)
        logger.info(f"{self.name} processes: {response}")
        for output in self.outputs:
            output.receive_information(self, response)

    def receive_information(self, input_module: 'PsychologicalModule', information):
        prompt = f"{self.base_prompt} It has received information from {input_module.name}, which says '{information}'. How should it integrate this information?"
        response = self.prompt_llm(prompt)
        logger.info(f"{self.name} integrates: {response}")
        return response

    def prompt_llm(self, prompt: str) -> str:
        """Send a prompt to OpenAI's LLM and receive a response."""
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": self.system_prompt,
                },
                {
                    "role": "user",
                    "content": "prompt",
                }
            ],
            model="gpt-4",
        )
        result = response.choices[0].message.content.strip()
        logger.info(f"{result=}")
        import ipdb; ipdb.set_trace()
        return result


class System:
    def __init__(self):
        self.modules = {}
        self.graph = nx.DiGraph()

    def add_module(self, module_info: dict, layer: int):
        name = module_info['name']
        function = module_info['function']
        module = PsychologicalModule(name, function)
        self.modules[name] = module
        # Add node with layer information for layout purposes
        self.graph.add_node(name, label=name + "\n" + function, layer=layer)

    def connect_modules(self, module_name: str, input_names: list):
        module = self.modules.get(module_name)
        if not module:
            return
        for input_name in input_names:
            input_module = self.modules.get(input_name)
            if input_module:
                module.add_input(input_module)
                input_module.add_output(module)
                self.graph.add_edge(input_name, module_name)

    def setup_structure(self, structure: dict):
        """Set up the modules and connections from a structure dictionary."""
        layer = 0
        for module_name, module_info in structure.items():
            layer += 1  
            self.add_module({
                "name": module_name,
                "function": module_info["function"]
            }, layer)
        for module_name, module_info in structure.items():
            if "inputs" in module_info:
                self.connect_modules(module_name, module_info["inputs"])

    def load_structure(self, structure: dict):
        """Directly load the structure from a provided dictionary."""
        self.setup_structure(structure)

    def load_structure_from_file(self, filename: str):
        """Load the structure from a JSON file."""
        with open(filename, 'r') as file:
            structure = json.load(file)
        self.setup_structure(structure)

    def process_all(self):
        for module in self.modules.values():
            module.process_information()

    def display_graph(self):
        A = pgv.AGraph(strict=True, directed=True)  # Create a directed graph

        # Add nodes and edges from the system's graph
        for node, data in self.graph.nodes(data=True):
            A.add_node(node, label=data['label'], shape='box', style='filled', fillcolor='lightblue')

        for u, v in self.graph.edges():
            A.add_edge(u, v)

        # Use Graphviz layout which tends to handle large graphs well
        A.layout(prog='dot')  # 'dot' layout for hierarchical structures

        # Render and display the graph in-memory
        buffer = io.BytesIO()
        A.draw(buffer, format='png')  # Draw in-memory
        buffer.seek(0)
        image = Image.open(buffer)
        image.show()  # Show the image using the default viewer
        buffer.close()


def main():
    # Create the system and load the structure
    system = System()
    system.load_structure_from_file("./structure.json")
    system.process_all()
    system.display_graph()


if __name__ == "__main__":
    main()
