# Agentic ER Diagram Verifier and PlantUML Code Generator
Authors: Luke Doughty _(add your name if you contribute anything)_

## Installation
```{bash}
git clone git@github.com:ldoughty05/AgenticPlantUMLGenerator.git
cd AgenticPlantUMLGenerator
python3 -m venv venv
pip install requirements.txt
```

Generate a Google Cloud API key, make a .env file based on the provided .env.TEMPLATE, and paste in your api in the appropriate space.

## Purpose
Provide a picture of a _mostly_ completed ER diagram along with a description of the system as a text file. The AI agent will fill in the missing entities, relationships, cardinality indicators, and uniqueness constraints and create PlantUML code for you!

## Usage
```{bash}
er_verifier.py [-h] [--list] [--list-models] [--all] [--output OUTPUT]
                    [--output-dir OUTPUT_DIR] [--full-response]
                    [name]
```

Convert ER diagram image to PlantUML

### positional arguments:
  name                  Diagram name (without extension)

### options:
  ``-h, --help``                  Show this help message and exit  
  ``--list, -l``                  List available diagrams  
  ``--list-models``               List available Gemini models  
  ``--all, -a``                   Process all available diagrams  
  ``--output OUTPUT, -o OUTPUT``  Output file for PlantUML code  
  ``--output-dir OUTPUT_DIR``     Output directory for batch processing  
  ``--full-response, -f``         Show full analysis, not just PlantUML code  

### Examples:  
  ``python er_verifier.py mydiagram``  
  ``python er_verifier.py --list``  
  ``python er_verifier.py --all``  
  ``python er_verifier.py --list-models``  
  ``python er_verifier.py mydiagram --output result.puml``  