from flask import Flask , render_template
from flask import request, jsonify
from flask.templating import render_template
from main_search_api import searchFunc
from get_arango_query_for_search_string import get_query_from_db
from get_arango_query_for_search_string import get_list_of_filenames_of_urls
import time
import re
from flask_cors import CORS
import threading
from tts import tts_speak
from stt import stt_listen
app = Flask(__name__)
app.config["DEBUG"] = True
CORS(app)

##################################################################
from one_time_load_files import one_load_files
lemmatizer , stop_words = one_load_files()
##################################################################
speech_text = ''
##################################################################
# add arango connection here and do computations only but once.
# word_map_dictionary = get_query_from_db()
# list1 = []
# list2 = []
# for key in word_map_dictionary:
#     list1.append(key)
#     list2.append(word_map_dictionary.get(key))
# import pandas as pd
# df = pd.DataFrame(word_map_dictionary.items() , index= None , columns=["word" , "list_of_urls"])
# df.to_csv("cache_of_db_for_search_string.csv" , index= None)

word_map_dictionary = {}
import pandas as pd
df = pd.read_csv("cache_of_db_for_search_string.csv")
list1 = df.values.tolist()

import ast
for idx in range(len(list1)):
    word_map_dictionary.update({list1[idx][0] : ast.literal_eval(list1[idx][1])})

#print(word_map_dictionary)



list_of_fienames_generated = get_list_of_filenames_of_urls()
##################################################################

@app.route('/', methods=["GET", "POST"])
def index():
    return render_template('index.html')
@app.route('/search', methods=['GET' , 'POST'])
def api_id():
    start = int(time.time()*1000)
    if 'input' in request.args:
        inputstr = str(request.args['input'])
    #else:
    #    return "Error: No input field provided. Please specify an input string."

    retdict = []

    global speech_text
    if speech_text != '':
        inputstr = str(speech_text)
        print(inputstr)
        speech_text = '' 
    
    retval , retval1 = searchFunc(word_map_dictionary , inputstr , lemmatizer , stop_words , list_of_fienames_generated)
    
    retdict = []
    for idx in range(len(retval)):
        retdict.append([retval[idx] , retval1[idx]])

    # retdict.append([retval1 , str(1)])
    # retdict.append([retval2 , str(2)])
    
    #retdict =  jsonify(retdict)
    #retdict =  jsonify(retval)
    
    audio_string = str(retval1[0].replace('"', ''))
    audio_string = str(retval1[0].replace('\'', ''))
    print(type(audio_string))
    t1 = threading.Thread(target=tts_speak, args= [audio_string])
    t1.start()
    
    import re
    inputstr = inputstr.replace(' ', '_')
    end = int(time.time()*1000)
    print("time for search string to result generation = " , end - start)
    return render_template('resultUI.html', data=retdict , search_string = inputstr)

@app.route('/converter_stt', methods=['GET' , 'POST'])
def converter():
    text = stt_listen()
    global speech_text
    speech_text = text
    return api_id()


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000)
    #app.run(debug=True) #can alter host and port number here. Right now the default host is localhost and port is 5000


#app.run()

# requirements new -: py -m pipwin install pyaudio