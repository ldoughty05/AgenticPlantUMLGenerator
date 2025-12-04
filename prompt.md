You are an expert database designer analyzing an ER diagram.

## System Description
{system_description}

## Your Task
Analyze the provided ER diagram image and:

1. **Identify all entities** visible in the diagram
2. **List attributes** for each entity (infer primary keys, mark them)
3. **Determine relationships** between entities:
   - Identify cardinality (1:1, 1:N, M:N)
   - Note any participation constraints (total/partial)
4. **Identify anything missing** based on the system description
5. **Generate complete PlantUML code** that represents the full, corrected ER diagram

## Output Format
First, provide a brief analysis section, then output the PlantUML code in a code block.

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

Now analyze the image and generate the PlantUML code: