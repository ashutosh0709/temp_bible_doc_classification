
def get_query_from_db():
    
    word_map_dictionary = {}

    #from pyArango.connection import *
    from pyArango.connection import Connection

    conn = Connection(username="root", password="")
    #conn = Connection(arangoURL='http://172.31.5.100:8529',username=arangodb_username, password=arangodb_password)

    db = conn["articles_db"]   

    articles_Collection = db["keyword_to_url_collection"]

    aql = "FOR x IN keyword_to_url_collection RETURN x"
    queryResult = db.AQLQuery(aql, rawResults=True, batchSize=100)
    for entry in queryResult:
        word_map_dictionary.update({entry.get('KEYWORD') : entry.get('URL_ARRAY')})

    dict_of_keywords_with_no_of_urls_associated = {}
    #print(word_map_dictionary) 
    #list1 = []
    #list2 = []
    for word in word_map_dictionary:
        dict_of_keywords_with_no_of_urls_associated.update({word : len(word_map_dictionary.get(word))})
        #list1.append(word)
        #list2.append(len(word_map_dictionary.get(word)))
    #print(dict_of_keywords_with_no_of_urls_associated)    


    # import pandas as pd
    # df = pd.DataFrame(list2 , list1)
    # #print(df)
    # df.to_csv("list_of_keywords_frequency.csv")
    # #print("done")    

    
    #flag = 1
    #while(True):

    return word_map_dictionary



def get_list_of_filenames_of_urls():
   
    i = 1
    list_of_filenames_generated = {}


    import pandas as pd
    df = pd.read_csv('article_url_list.csv')
    urls = df['url'].tolist() 

    for url in urls:
        import re
        filteredurl = re.sub(r'[^a-zA-Z]',' ',url) #no-2
        filteredurl = re.sub(r' ' , '_',filteredurl)
        
        filename = '_' + str(i) + "_" + filteredurl
        list_of_filenames_generated.update({url : filename})
    
        i += 1


    return list_of_filenames_generated