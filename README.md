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

## Usage
Provide a picture of a _mostly_ completed ER diagram along with a description of the system as a text file. The AI agent will fill in the missing entities, relationships, cardinality indicators, and uniqueness constraints and create PlantUML code for you!