from nltk.tag.stanford import StanfordPOSTagger
import nltk
import re
import requests
import json

url = "http://pcsync-01/shoppersstop.com/pcf_catalog.json"
file_request = requests.get(url, stream = True)

username = "abishkarchhetri"
_path_to_model = "/home/" + username+ "/Product-Queries/stanford_tagger_files/stanford-postagger-2017-06-09/models/english-bidirectional-distsim.tagger" 
_path_to_jar = "/home/" + username+ "/Product-Queries/stanford_tagger_files/stanford-postagger-2017-06-09/stanford-postagger.jar"


def lazy_json_read_line(line):
    try:
        line_json = json.loads(line[line.index("{"):len(line)-1])
        line_description = line_json["description"]
        return line_description
    except:
        return "error"

f = open('tpdb.txt', 'w').close()
f = open("tpdb.txt", "a")

for line in file_request.iter_lines():
    f.write(lazy_json_read_line(line))
    f.write("\n")

f.close()

def create_data_structure(long_string):
    st = StanfordPOSTagger(model_filename=_path_to_model, path_to_jar=_path_to_jar)
    main_data_structure = {}    
    sentences_with_tag = []
    sentences = re.split("\. |\n", long_string)
    print("sentences",sentences)    
    for sentence_index in range(len(sentences)): 
        tokenized = nltk.word_tokenize(sentences[sentence_index])
    	tagged = st.tag(tokenized)
	sentences_with_tag.append(tagged)
	
	for word_index in range(len(tagged)):
	    word = tagged[word_index][0]

	    if word not in main_data_structure:
		main_data_structure[word] = [(sentence_index, word_index)]
	    else:
		main_data_structure[word].append((sentence_index, word_index))

    return (main_data_structure, sentences_with_tag)

#sample_string = "Some things never change. Do they?"

#data, sentences = create_data_structure(sample_string)

#print(data)
#print(sentences)
