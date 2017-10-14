from konlpy.tag import Twitter
import os, re, json, random
from pprint import pprint
from bs4 import BeautifulSoup
import urllib.request

# Create Markov Chain Dictionary
def make_dic(words):
    tmp = ["@"]
    dic = {}

    for word in words:
        tmp.append(word)
        if word == "" or word == "\r\n" or word == "\n": continue
        if len(tmp) < 3: continue
        if len(tmp) > 3: tmp = tmp[1:]

        set_word3(dic, tmp)

        if word == ".":
            tmp = ["@"]
            continue

    return dic


# Put data in Dictionary
def set_word3(dic, s3):
    w1, w2, w3 = s3

    if not w1 in dic: dic[w1] = {}
    if not w2 in dic[w1]: dic[w1][w2] = {}
    if not w3 in dic[w1][w2]: dic[w1][w2][w3] = 0

    dic[w1][w2][w3] += 1


# Create Sentence
def make_sentence(dic):
    ret = []
    if not '@' in dic:
        return "no dic"
    top = dic['@']

    w1 = word_choice(top)
    w2 = word_choice(top[w1])

    ret.append(w1)
    ret.append(w2)

    while True:
        try:
            w3 = word_choice(dic[w1][w2])
            ret.append(w3)
            if w3 == ".":
                break
            w1, w2 = w2, w3
        except KeyError:
            continue

    ret = "".join(ret)

    # Spacing words using spellchecker
    params = urllib.parse.urlencode({
        "_callback": "",
        "q": ret
    })

    # Spellchecker (KOREAN)
    data = urllib.request.urlopen("https://m.search.naver.com/p/csearch/dcontent/spellchecker.nhn?" + params)

    data = data.read().decode("utf-8")[1:-2]
    data = json.loads(data)
    data = data["message"]["result"]["html"]
    data = soup = BeautifulSoup(data, "html.parser").getText()

    return data


def word_choice(sel):
    keys = sel.keys()
    return random.choice(list(keys))


if __name__ == '__main__':
    dict_file = "markov-bamboo.json"    # make json file

    file = open('data 2017-01-01 2017-10-02.txt', 'r', encoding='utf-8')
    data = file.read()

    twitter = Twitter()
    malist = twitter.pos(data, norm=True)

    words = []
    for word in malist:
        if not word[1] in ["Punctuation"]:
            words.append(word[0])
        if word[0] == '.':
            words.append(word[0])

    dic = make_dic(words)
    print(words)
    pprint(dic)

    json.dump(dic, open(dict_file, "w", encoding="utf-8"))

    for i in range(101):   # the number of sentence
        new_sentence = make_sentence(dic)
        print(str(i) + ": " + new_sentence)



