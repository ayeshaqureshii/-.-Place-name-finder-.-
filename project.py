import spacy
import streamlit as st
import json
import base64

st.set_page_config(page_title = "Place name identifier", page_icon="location.png")

def get_base_64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()
img_base64 = get_base_64("Untitled design.gif")

st.markdown(f""" 
            
            <style>
            h1{{
                color:#fbc3ed !important;
                text-shadow:2px 2px 4px #000000;
            
            
            }}
            h3,p,span{{
                color: #f299e6!important;
            }}
            .stWidget label {{
                color:#FFB6C1 !important;
                font-size: 20px !important;
            }}

            .stApp {{background-image: url("data:image/gif;base64,{img_base64}");
                    background-attachment: fixed;
                    background-size: cover;
                    background-position: center;
            
            }}
            .stMain, .stHeader, .stAppHeader, .stMainView {{
            background-color: transparent !important;
            background: transparent !important;
            
           }} 

        

            .stTextArea textarea{{
            
            background-color: #fef6ec !important; /* 0.8 Transparent Blue */
            /*backdrop-filter: blur(8px);*/
            padding: 20px;
            border-radius: 12px;
            color: #0D47A1;
            margin-bottom: 15px;

            
            }}
            .result_box{{
            background-color: rgba(220,192,236,0.8) !important; /* 0.8 Transparent Blue */
            backdrop-filter: blur(8px);
            padding: 20px;
            border-radius: 12px;
            color: #0D47A1;
            margin-bottom: 15px;
            
            }}

            .stWidget label {{color: #D02090 !important; font-weight: bold;}}



            </style>""", unsafe_allow_html=True)

# loading spacy 
@st.cache_resource
def load_nlp():
    return spacy.load("en_core_web_md")
nlp_model = load_nlp()


#interface
st.title("PLACE NAME IDENTIFIER")
st.subheader("NLP based location extraction using Spacy")
st.write("Enter text in the Input Box to identify location")


#input field
user_input = st.text_area("Input Text:",placeholder="Enter Text Here", height=150)

#working and ambiguity handle

if user_input:
    doc = nlp_model(user_input)
    action_verbs = ["go", "walk", "run", "eat", "talk", "say", "buy", "sell"]
    extracted_data = []
    for ent in doc.ents:
      
        if ent.label_ in ["GPE", "LOC","FAC"]:

            # Open Ended Enhancements: Entity Linking
            wiki_URL = f"https://en.wikipedia.org/wiki/{ent.text.replace(' ', '_')}"
            
            is_valid = True
            #testing for ambiguity
            if ent.label_ =="GPE":  
               verb_head = ent.root.head
               is_subject= ent.root.dep_ =="nsubj"
               is_action =verb_head.lemma_.lower() in action_verbs

               # if a person named after a Geographical entity is doing something, skio
               if is_subject and is_action:
                   is_valid = False
            if not is_valid:
                continue   
            if ent.label_ == "GPE":
                display_label ="CITY / COUNTRY"
            elif ent.label_ == "LOC"   :
                display_label ="REGION / LANDMARK"
            elif ent.label_ == "FAC"   :
                display_label ="STREET / BUILDING"  
            else:
                display_label="LOCATION"  

            extracted_data.append({
                "Place": ent.text ,
                "Type":display_label,
                "Link":wiki_URL

            })
    st.subheader("Detected Places")       
    if extracted_data:
        for item in extracted_data:
            st.markdown(f"""
                        <div class = "result_box">
                            <div style = "display: flex ; align-items: center; justify-content: space-between;">
                                <div>
                                    <img src = "https://i.pinimg.com/webp/736x/b7/db/41/b7db412ce4fa61ddf2aeb150b796d493.webp" width = "25" style = "vertical-align :middle; margin-right: 10px;">
                                    <span style="font-size: 18px; font-weight: bold;">{item["Place"]}</span>
                                    <br><small style="margin-left: 35px; color: #555;">{item["Type"]}</small>
                                <div>
                                <a href="{item['Link']}" target="_blank" style="text-decoration: none;">
                                    <div style="background-color: #f299e6; color: white; padding: 5px 15px; border-radius: 20px; font-size: 12px; font-weight: bold; border: 1px solid #fff; transition: 0.3s;">
                                🗒 WIKIPEDIA ˎˊ˗ 
                                    </div>
                                </a>
                            </div>
                                  
                        
                        
                        {item["Place"]} 𓂃✃ {item["Type"]}
                        </div>
                        
                        """,unsafe_allow_html=True)


    # JSON 
    st.divider()
    st.subheader("Json Output")
    st.json(extracted_data)
#Testing data to show Accuracy Metrices
test_data =[
    ("I am visiting London.", ["London"]),
    ("Paris went to Germany.",["Germany"]),
    ("The Eiffel Tower is in Paris.",["Eiffel Tower","Paris"]),
    ("Jordan walks towards candy shop.",[]),
    ("I went to Lahore, Karachi and Islamabad in August.",["Lahore","Karachi","Islamabad"])
    ]
def accuracy_test():
    true_positive =0 #Found place correctly
    false_positive = 0 # Found Person as a Place
    false_negative = 0 # missed actual places
    action_verbs = ["go", "walk", "run", "eat", "talk", "say", "buy", "sell","sleep","drink"]


    for text , expected in test_data:
        doc = nlp_model(text)
        found = []
        for ent in doc.ents:

      
            if ent.label_ in ["GPE", "LOC","FAC"]:
               is_subject = False
               is_action = False
               
               if ent.label_=="GPE":
                    verb_head = ent.root.head
                    is_subject= ent.root.dep_ =="nsubj"
                    is_action =verb_head.lemma_.lower() in action_verbs
        
               if is_subject and is_action:
                    continue
               found.append(ent.text)

        for item in found:
            if item in expected: 
                true_positive+=1
            else:
                false_positive+=1
        for item in expected:
            if item not in found:
                false_negative+=1        
    #calculating Precision and Recall and habdling zero devision error

    precision = (true_positive/(true_positive+false_positive)) if (true_positive+false_positive)>0 else 0
    recall = (true_positive/(true_positive+false_negative)) if (true_positive+false_negative)>0 else 0
    f1 = 2*(precision*recall)/(precision+recall) if (precision+recall)>0 else 0
     
    return precision*100, recall*100, f1*100

#running the test
p_score, r_score, f1_score = accuracy_test()

#Accuracy Metrices Display(Precision, Recall and F1 Score)
with st.sidebar:
    st.header("Accuracy Metrices")
    st.markdown("★ Tested against 5 differnt sentences.")

    col1, col2 ,col3 = st.columns(3)
    with col1:
        st.metric(label ="Precision", value=f"{p_score:.1f}%")

    with col2:
        st.metric(label="Recall", value=f"{r_score:.1f}%")
    with col3:
        st.metric(label="F1 Score ",value=f"{f1_score:.1f}%")  

    st.divider()  


      

