#!/bin/bash
# Path to the PlantUML jar file
PLANTUML_JAR_PATH="../../Tools/PlantUml/plantuml-1.2024.5.jar"

# Generate the diagram
java -jar $PLANTUML_JAR_PATH PlanningPart1.puml
java -jar $PLANTUML_JAR_PATH PlanningPart2.puml

echo "Diagram rendered successfully!"
