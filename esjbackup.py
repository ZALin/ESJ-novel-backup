import requests
import lxml.html


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

	dst_filename = html_element.xpath('//h2[@class="p-t-10 text-normal"]')[0].text_content()
	chapter_list = html_element.get_element_by_id("chapterList").getchildren()

	for element in chapter_list:
		
		with open(dst_filename, 'a') as f:
			#print element.text_content()
			f.write(element.text_content().encode('utf-8')+'\n')
		
		if element.tag == 'a' :
			write_page(element.attrib['href'],dst_filename)

