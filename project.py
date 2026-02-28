import spacy

nlp = spacy.load("en_core_web_md")
text = input("Enter Your Text: ")

doc = nlp(text)
for ent in doc.ents:
    main_word = ent[0]
    if ent.label_ == "GPE" and main_word.dep_=="nsubj":
        continue
    #this skips if a country is found as a person (ambiguity, Rule 3.1)
    elif ent.label_=="GPE":
        print(f"Found: {ent.text} ; Label: {ent.label_}")


