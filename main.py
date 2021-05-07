import os
import json 
import requests
import time
import urllib

KEY = "1836991292:AAG-MWxvt3RfATyTEQN4KyJktdK1oU7fY20"
URL = "https://api.telegram.org/bot{}/".format(KEY)

dictionary = {}
stopwords = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]

def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content

def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js

def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    return js

def send_message(text, chat_id):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)

def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)

def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)

def echo_all(updates):
    for update in updates["result"]:
        try:
            text = update["message"]["text"]
            chat = update["message"]["chat"]["id"]
            for word in text.split():
                if (word.lower() == "pay" or word.lower() == "transfer" or word.lower() == "money"):
                    send_message("Possible scam detcted from " + update["message"]["from"]["first_name"] + ". Think better be careful of this siaoeh", chat)
                    break
                elif (word.lower() == "army" or word.lower() == "ns" or word.lower() == "air force"):
                    send_message("LOL wgt ord lo", chat)
            # for word in text.split():
            if (text.lower() == "wakanda"):
                send_message("FOREVER", chat)
            # if (text == "/stat"):
            #     print(dictionary)
            #     for word in dictionary.keys:
            #         send_message(word + " | " + dictionary[word], chat)
            # else:
            #     print (text.split())
            #     for word in text.split():
            #         print(word)
            #         if (word not in stopwords):
            #             if (word not in dictionary.keys()):
            #                 dictionary[word] = 1
            #             else:
            #                 dictionary[word] = dictionary[word] + 1
        except Exception as e:
            print(e)

def main():
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            echo_all(updates)
        time.sleep(0.5)

if __name__ == '__main__':
    main()