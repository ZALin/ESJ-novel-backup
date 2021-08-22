#!/usr/bin/env python
#coding=utf-8

import requests
import lxml.html
import re
import json
import os

symbol_list = {
    "\\": "-",
    "/": "-",
    ":": "：",
    "*": "☆",
    "?": "？",
    "\"": " ",
    "<": "《",
    ">": "》",
    "|": "-",
    ".": "。",
    "\t": " ",
    "\n": " ",
}


def write_page(url, dst_file):
    r = requests.get(url)
    html_element = lxml.html.document_fromstring(r.text)
    if html_element.xpath('//h2'):
        title = html_element.xpath('//h2')[0]
        author = html_element.xpath('//div[@class="single-post-meta m-t-20"]/div')[0]
        content = html_element.xpath('//div[@class="forum-content mt-3"]')[0]
        with open(dst_file, 'a') as f:
            f.write('[' + title.text_content().encode('utf-8') + '] ' + author.text_content().strip().encode('utf-8') + '\n')
            f.write(content.text_content().encode('utf-8')+'\n\n')

def contain(string, array):
    if isinstance(array, dict):
        return any(symbol in string for symbol in array.keys())
    elif isinstance(array, list) or isinstance(array, tuple):
        return any(symbol in string for symbol in array)
    return False


def escape_symbol(string):
    while contain(string, symbol_list):
        for char, replace_char in symbol_list.items():
            string = string.replace(char, replace_char)
    return string


if __name__ == "__main__":

    current_path = os.path.split(os.path.realpath(__file__))[0]

    url = ''
    
    r = requests.get(url)
    html_element = lxml.html.document_fromstring(r.text)
    novel_name = html_element.xpath('//h2[@class="p-t-10 text-normal"]')[0].text_content()
    novel_name = escape_symbol(novel_name.encode('utf-8'))
    print r.text
    m = re.search(r"var mem_id='(u?\d+)',mem_nickname='.*',token='(.+)';", r.text) 
    mem_id, token = m.groups()
    m = re.search(r"forum_list_data\.php\?token=.+&totalRows=(\d+)&bid=(\d+)", r.text) 
    totalRows, bid = m.groups()

    r = requests.get(url + 'forum_list_data.php?token=' + token + '&totalRows=' + str(totalRows) + '&bid=' + str(bid) + \
                     '&sort=cdate&order=asc&offset=0&limit=' + str(totalRows) )

    chapter_josn = json.loads(r.text)

    if chapter_josn["rows"]:

        if not os.path.isdir( os.path.normpath( current_path + '/' + novel_name ) ):
            os.system("mkdir " + str(os.path.normpath( current_path + '/' + novel_name )))

        for chapter in chapter_josn["rows"]:
            chapter_name = chapter["subject"].split('target="_blank">')[1].split('</a>')[0]
            chapter_name = escape_symbol(chapter_name.encode('utf-8'))
            dst_filename = os.path.normpath( current_path + '/' + novel_name + '/' + chapter_name + '.txt')
            chapter_url = re.sub(r'/forum/\d+/\d+/', chapter["subject"].split('"')[1], url)
            write_page(chapter_url, dst_filename)


    

    '''
    novel_id = ''  # the novel id which you want to download
    r = requests.get('https://www.esjzone.cc/detail/' + novel_id + '.html')
    html_element = lxml.html.document_fromstring(r.text)

    novel_name = html_element.xpath('//h2[@class="p-t-10 text-normal"]')[0].text_content()
    dst_filename = escape_symbol(novel_name.encode('utf-8')) + ".txt"

    novel_details_element = html_element.xpath('//ul[@class="list-unstyled mb-2 book-detail"]')[0]
    if novel_details_element.xpath('//ul[@class="list-unstyled mb-2 book-detail"]/li/div'):
        bad_divs = novel_details_element.xpath('//ul[@class="list-unstyled mb-2 book-detail"]/li/div')
        for bad_div in bad_divs:
            bad_div.getparent().remove(bad_div)
    novel_details = novel_details_element.text_content()
    with open(dst_filename, 'w') as f:
        f.write(novel_details.encode('utf-8'))

    if re.search('id="details"', r.text):
        novel_description = html_element.get_element_by_id("details").text_content()
        with open(dst_filename, 'a') as f:
            f.write(novel_description.encode('utf-8'))
    else:
        with open(dst_filename, 'a') as f:
            f.write('\n\n')

    if re.search('id="chapterList"', r.text):
        chapter_list = html_element.get_element_by_id("chapterList").getchildren()
        
        for element in chapter_list:
    
            with open(dst_filename, 'a') as f:
                f.write(element.text_content().encode('utf-8')+'\n')
            
            if element.tag == 'a':

                if re.search(r'esjzone\.cc/forum/\d+/\d+\.html', element.attrib['href']):
                    write_page(element.attrib['href'],dst_filename)
                else:
                    with open(dst_filename, 'a') as f:
                        f.write(element.attrib['href'] + u' {非站內連結，略過}\n\n'.encode('utf-8'))

    '''

