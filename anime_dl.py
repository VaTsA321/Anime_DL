import requests
from bs4 import BeautifulSoup
import re
from super_download import super_download
from fuzzywuzzy import process
import sys
import os

def search_anime(name):
	url = 'http://www.chia-anime.tv/search/' + name.replace(' ', '+')
	r = requests.get(url)
	soup = BeautifulSoup(r.text)
	for item in soup.find_all('h2'):
		if item.text == 'Anime Results':
			head = item.nextSibling.nextSibling
			break
	title_list = []
	link_list = []
	for item in head.find_all('a'):
		if item.text:
			title_list.append(item.text)
			link_list.append(item['href'])

	(title, score) = process.extractOne(name, title_list)
	link = link_list[title_list.index(title)]
	return title, link

def get_req_episode_links(link, ep_range):
	#print link
	r = requests.get(link)
	soup = BeautifulSoup(r.text)
	link_list = []
	title_list = []
	ep_min,ep_max = ep_range
	#print ep_min 
	#print ep_max 
	for item in soup.find_all('a'):
		#print item.text
		if 'Episode' in item.text and int(re.search(r'Episode (\w+)', item.text).group(1)) in range(ep_range[0], ep_range[1] + 1):
			link_list.append(item['href'])		
			title_list.append(re.search(r'Episode (\w+)', item.text).group(1))	
	#print title_list	
	return title_list, link_list	
		

def get_anime_prem_url(link):
	#print link
	r = requests.get(link)
	soup = BeautifulSoup(r.text)
	for item in soup.find_all('a'):
		try:
			#print item.id
			if item['id'] == 'download':
				url = item['href']
				break
		except KeyError:
			continue
	return url

def batch_download(title_list, link_list, name):
	i = 0
	#print 'entered'
	if not os.path.exists('./Anime/' + name):
		os.makedirs('./Anime/' + name)
	for link in link_list:
		#print link
		anime_prem_url = get_anime_prem_url(link)
		path_without_ext = './Anime/' + name + '/' + title_list[i].strip('\n') 
		print 'Downloading ', title_list[i].strip('\n') 
		download_episode(path_without_ext, anime_prem_url)	
		print 'Done'				
		i += 1

def download_episode(path, url):
	'''	if '720' in item.text and 'mp4' in item.text:
			super_download(item['href'], path + '.mp4')
			break
		elif '480' in item.text and 'mp4' in item.text:
			super_download(item['href'], path + '.mp4')
			break
		elif '360' in item.text and 'mp4' in item.text:
			super_download(item['href'], path + '.mp4')
			break
		elif '720' in item.text and 'flv' in item.text:
			super_download(item['href'], path + '.flv')
			break
		elif '480' in item.text and 'flv' in item.text:
			super_download(item['href'], path + '.flv')
			break
		elif '360' in item.text and 'flv' in item.text:
			super_download(item['href'], path + '.flv')
			break'''
	r = requests.get(url)
	soup = BeautifulSoup(r.text)
	for item in soup.find_all('a'):
		
		if 'Server 2' in item.text: 
			super_download(item['href'], path + '.mp4')
			break
		elif 'Server 3' in item.text: 
			super_download(item['href'], path + '.mp4')
			break
		elif 'Server 1' in item.text:
			super_download(item['href'], path + '.mp4')
			break
		elif 'Server Zero' in item.text:
			super_download(item['href'], path + '.mp4')
			break
	else:
		print 'could not find link for ', path

def anime_dl(name, ep_range):
	actual_ep_range = map(int, ep_range.split('-'))
	actual_name, eps_page_url = search_anime(name) #check
	(title_list, link_list) = get_req_episode_links(eps_page_url, actual_ep_range)#check
	batch_download(title_list, link_list, actual_name)#check	 

def main():
	if len(sys.argv) != 3:
		print 'usage: ', sys.argv[0], ' <anime name> <episode range>'	
		sys.exit(1)
	anime_dl(sys.argv[1], sys.argv[2])	

if __name__ == '__main__':
	main()
