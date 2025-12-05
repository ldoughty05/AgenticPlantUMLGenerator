You are an expert database designer analyzing an ER diagram image and verifying it against a system description.

## System Description
{system_description}

## Your Task

### Step 1: Analyze the Image
First, carefully examine the provided ER diagram image and extract:
- All entities/tables visible in the diagram
- All attributes listed for each entity
- All relationships shown (lines connecting entities)
- Any cardinality notations visible (crow's foot, numbers, etc.)

### Step 2: Compare Image vs Description
Identify discrepancies between what you see in the image and what the system description requires:
- **Entities in image but NOT in description**: List any extra tables that appear in the diagram but aren't mentioned in the requirements
- **Entities in description but NOT in image**: List any required tables that are missing from the diagram
- **Missing attributes**: For each entity, note attributes mentioned in the description but absent from the diagram
- **Extra attributes**: Note any attributes in the diagram that weren't specified in the description
- **Relationship issues**: Note any missing, extra, or incorrectly drawn relationships

### Step 3: Generate Corrected PlantUML
Create complete PlantUML code that:
- Includes everything from BOTH the image AND the description
- Corrects any cardinality errors you identified
- Adds any missing entities, attributes, or relationships
- Preserves valid elements from the original diagram

## Output Format

### Analysis
Provide your analysis with these sections:
1. **Entities found in image**: [list what you see]
2. **Entities required by description**: [list what's needed]
3. **Discrepancies identified**: [list mismatches, missing items, extras]
4. **Corrections made**: [summarize what you fixed]

### PlantUML Code
Then output the corrected PlantUML code in a code block.

Use this PlantUML ER diagram syntax:
```plantuml
@startuml
' Use IE notation for ER diagrams
skinparam linetype ortho

entity "EntityName" as entity_alias {{
  * primary_key : type <<PK>>
  --
  * required_field : type
  optional_field : type
}}

entity_alias ||--o{{ other_entity : "relationship_label"
@enduml
```

Cardinality notation:
- ||--|| : one to one
- ||--o{{ : one to many (one required, many optional)
- ||--|{{ : one to many (both required)
- }}o--o{{ : many to many (both optional)
- }}|--|{{ : many to many (both required)

If the image appears completely unrelated to the system description, state this clearly and explain what you observe in the image versus what the description requires.

Now analyze the image and generate the corrected PlantUML code: