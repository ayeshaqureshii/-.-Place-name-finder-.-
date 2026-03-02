PLACE NAME IDENTIFIER FOR PULSE CODE HACKATHON (CIS DEPT. NED UNIVERCITY)
OBJECTIVE: to make a NLP-Based Location Extraction System

WHAT IT DOES: Accepts text input and produces output such that it extracts and lists all Places (Cities, Countries, Streets, Buildings etc).
              Produces a read able output.
FEATURES: [1] Uses Dependency Parsing to filter out location names acting as subjects of human actions
          [2] Provides Wikipedia articles link of found places.
          [3] Utilizes spaCy's en_core_web_md model for 300-dimensional word vector accuracy.
          [4] Provides clean interface for input and output display.

OPEN ENDED ENHANCEMENTS:
        Entity Linking	:Link detected locations to their Wikipedia or Wikidata entries.

CITATIONS:
[1] Core Natural Language Processing:
         Library: spaCy (v3.7.1)
         Developer: Explosion AI
         License: MIT License

Citation: Honnibal, M., & Montani, I. (2017). spaCy 2: Natural language understanding with Bloom embeddings, convolutional neural networks and incremental parsing.

[2] Pre-trained Statistical Model:
        Model: en_core_web_md
        Dataset Source: OntoNotes 5.0
        Description: A multi-genre corpus of Chinese, English, and Arabic text with structural, semantic, and coreference annotations.

DOCUMENTATION:

Spacy (NLP): Integrated via a cached resource function (@st.cache_resource) to ensure high-performance loading.
             I utilized the statistical Entity Recognizer and the Dependency Parser to create a custom filtering layer.

SET UP INSTRUCTIONS:

Execute these commands in your terminal to run the project
[1] Clone the Repository
git clone <https://github.com/ayeshaqureshii/-.-Place-name-finder-.->
cd <https://github.com/ayeshaqureshii/-.-Place-name-finder-.->

[2] Install Dependencies
pip install -r requirements.txt

[3] Run the Application
streamlit run project.py

USAGE:

In the Input Box, paste any text you would like and press Ctrl+Enter.
You will see all locations in the text identified in output.





