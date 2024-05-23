# PsycheGPT

## Project Overview
PsycheGPT is a simulation framework that integrates Large Language Models (LLMs) to simulate psychological and brain functions. PsycheGPT aims to explore cognitive processes through modular simulations that mimic different psychological functions.

## Installation

### Prerequisites
- Python 3.10 or higher
- pip (Python package installer)

### Libraries
To install the required libraries, run the following command:

```bash
pip install -r requirements.txt
```

## Configuration

### Setting up API Keys
1. Create a `.env` file in your project root directory.
2. Add your OpenAI API key to this file:

```
OPENAI_API_KEY=your_openai_api_key_here
```

Ensure that this key is kept secure and is not exposed publicly.

### Using Pydantic for Configuration
The project uses `pydantic-settings` for environment management. Ensure your settings are configured correctly as shown in the provided `config.py` script.

## Usage

To use PsycheGPT, instantiate modules representing different cognitive functions and link them based on desired simulation dynamics.

```python
from system import PsychologicalModule, System

# Initialize the system
system = System()

# Create modules
memory = PsychologicalModule("Memory", "stores and retrieves information")
attention = PsychologicalModule("Attention", "allocates cognitive resources")

# Connect modules
memory.add_output(attention)
attention.add_input(memory)

# Run simulation
memory.process_information()
attention.process_information()
```

## Contributing
Contributions to PsycheGPT are welcome! Please refer to CONTRIBUTING.md (TODO) for guidelines on how to contribute to this project.

## Support
If you encounter any issues or have questions, please file an issue on the GitHub repository.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) (TODO) file for details.
