from fastapi import FastAPI
import spacy
import pandas as pd
from newsapi import NewsApiClient

    # Init
newsapi = NewsApiClient(api_key='f57245fcdf7e4b1983a11798d9595b92')

app=FastAPI(title="News API from keywords")

@app.get("/")
async def demo():
    return "Hello World"

@app.get("/demo")
async def d1():
    return "DEMO"

@app.get("/get_news_keywords/{text}")
async def get_keywords(text :str):
    nlp=spacy.load("en_core_web_md")
    
    stop_words = spacy.lang.en.stop_words.STOP_WORDS 
    
    doc = nlp(text) 
     
    filtered_tokens = [token for token in doc if not token.is_stop] 
    final_txt= ' '.join([token.text for token in filtered_tokens])


    mykeys=['ORG','PERSON','EVENT','PRODUCT','WORK_OF_ART','GPE']
    myorgs=set()
    mypersons=set()
    myevents=set()
    myprods=set()
    myplaces=set()


    doc=nlp(final_txt)

    for token in doc.ents:
        if(token.label_ in mykeys):
            if(token.label_=='ORG'):
                myorgs.add(token.text)
            if(token.label_=='PERSON'):
                mypersons.add(token.text)
            if(token.label_=='EVENT'):
                myevents.add(token.text)
            if(token.label_=='PRODUCT'):
                myprods.add(token.text)
            if(token.label_=='GPE'):
                myplaces.add(token.text)    

    myorgs=list(myorgs)
    myevents=list(myevents)
    mypersons=list(mypersons)
    myprods=list(myprods)
    myplaces=list(myplaces)

    results={"Organizations":myorgs,"Events":myevents,"Individuals":mypersons,"Products": myprods,"Places": myplaces}
    
    # results=prediction.json()

    mycategories=['Organizations','Events','Products','Places','Individuals']
    # results=prediction.json()
    # results=prediction.json()
    # print(type(results['Events']))
    # print(results)

    mylist_categories=list()
    for cat in mycategories:
        temp_list=results[cat]
        mylist_keywords=list()
        for keyword in temp_list:
            top_headlines = newsapi.get_top_headlines(q=keyword,
                                            language='en',
                                            )
            
            temp=top_headlines['articles'][:2]

            mydict_keywords=dict()
            mydict_keywords[keyword]=temp

            mylist_keywords.append(mydict_keywords)

        mydict_categories=dict()
        mydict_categories[cat]=mylist_keywords


        mylist_categories.append(mydict_categories)

    

    return mylist_categories



