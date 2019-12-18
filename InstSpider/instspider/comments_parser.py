from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import numpy as np
from igramscraper.instagram import Instagram # pylint: disable=no-name-in-module
import json
import instspider
import pickle

def parseinst(linkinst):
    open('f1.json', 'w').close()

    settings = get_project_settings()
    settings.overrides['FEED_FORMAT'] = 'json'
    settings.overrides['FEED_URI'] = 'f1.json'
    process = CrawlerProcess(settings)

    process.crawl('comment', link = linkinst)
    process.start()

    with open('f1.json') as json_file:
        id_text = json.load(json_file)
        idstr = id_text[0]['idstr']
    json_file.close()
    ind = idstr.index('=') + 1
    idstr = idstr[ind:]

    instagram = Instagram()
    instagram.with_credentials('grouchysalmon', 'ulofob37', '')
    instagram.login()

    comments = instagram.get_media_comments_by_id(idstr, 10000)
    k = 0
    comments_list = []
    for comment in comments['comments']:
        k +=1
        comments_list.append(comment.text)
        #print(comment.owner)
    print(k)

    with open('comments.txt', 'wb') as f:
        pickle.dump(comments_list,f)

parseinst('https://www.instagram.com/p/BxVh_ZYBerN/')
