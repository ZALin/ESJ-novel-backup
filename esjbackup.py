#!/usr/bin/env python
#coding=utf-8

import requests
import lxml.html
import re

def write_page(url, dst_file):
    r = requests.get(url)
    html_element = lxml.html.document_fromstring(r.text)
    title = html_element.xpath('//h2')[0]
    content = html_element.xpath('//div[@class="forum-content mt-3"]')[0]
    with open(dst_file, 'a') as f:
        f.write(title.text_content().encode('utf-8')+'\n')
        f.write(content.text_content().encode('utf-8')+'\n\n')

if __name__ == "__main__":

    novel_id = ''
    r = requests.get('https://www.esjzone.cc/detail/' + novel_id + '.html')
    html_element = lxml.html.document_fromstring(r.text)

    dst_filename = html_element.xpath('//h2[@class="p-t-10 text-normal"]')[0].text_content() + ".txt"
    chapter_list = html_element.get_element_by_id("chapterList").getchildren()

    for element in chapter_list:
        
        with open(dst_filename, 'a') as f:
            #print element.text_content()
            f.write(element.text_content().encode('utf-8')+'\n')
        
        if element.tag == 'a':

            if re.search(r'esjzone\.cc/forum/\d+/\d+\.html', element.attrib['href']):
                write_page(element.attrib['href'],dst_filename)
            else:
                with open(dst_filename, 'a') as f:
                    #print element.text_content()
                    f.write(u'{非站內連結，略過}\n'.encode('utf-8'))

