from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from bs4 import BeautifulSoup as soup
import urllib.request
import csv

class CLScraper():
	def __init__(self, location, query, radius, postal):
		self.location = location
		self.query = query
		self.radius = radius
		self.postal = postal
		self.page_num = 0
		# self.url = ('https://{}.craigslist.ca/search/sss?query={}'
		# 	'&sort=rel&search_distance={}&postal={}').format(
		# 	location, query, radius, postal)
		self.url = ('https://{}.craigslist.ca/search/sss?s={}&postal='
			'{}&query={}&search_distance={}&sort=rel').format(
			location, self.page_num, postal, query, radius)
		self.driver = webdriver.Chrome()
		self.delay = 3
		self.html_page = urllib.request.urlopen(self.url)
		# create csv file
		with open(self.query + 'search' + '.csv', 'w') as f:
			f.write('Post Title, Price, Post Date, URL\n')

	# load url and browser
	def load_url(self):
		self.driver.get(self.url)
		try:
			wait = WebDriverWait(self.driver, self.delay)
			wait.until(EC.presence_of_element_located((By.ID,
				'searchform')))
			print('Page is ready')
		except TimeoutException:
			print('Loading took too much time')

	# extract number of items found on current page
	def num_searches(self):
		num = self.driver.find_elements_by_class_name(
			'rangeTo')
		search_num = num[0].text
		return search_num

	# extract posting titles
	def extract_titles(self):
		all_titles = self.driver.find_elements_by_class_name(
			'result-row')
		titles_list = []
		for post in all_titles:
			titles_list.append(post.text)
		print(titles_list)
		return titles_list

	# extract urls
	def extract_urls(self):
		url_list = []
		data = soup(self.html_page, 'lxml')
		for links in data.findAll('a', {'class':
			'result-title hdrlnk'}):
			url_list.append(links['href'])
		return url_list

	# extract the dates of the postings
	def extract_dates(self):
		dates_list = []
		data = soup(self.html_page, 'lxml')
		for links in data.findAll('time', {'class':
			'result-date'}):
			dates_list.append(links['datetime'].split(' ')[0])
		return(dates_list)

	# extract the price of the items
	def extract_prices(self):
		price_list = []
		count = 0
		data = soup(self.html_page, 'lxml')
		for links in data.findAll('span', {'class':
			'result-price'}):
			# will have duplicates, two classes named result-price
			# use a loop checker, skips every odd numbered iteration
			if count%2 == 1:
				pass
			else:
				price = str(links).split('">')[1].split('</')[0]
				price_list.append(price)
			count += 1
		return(price_list)

	# write results into a spreadsheet
	def write_to_csv(self):
		num = self.num_searches()
		post_list = self.extract_titles()
		price_list = self.extract_prices()
		date_list = self.extract_dates()
		url_list =  self.extract_urls()
		# rows = zip(post_list, price_list, date_list, url_list)
		# print(post_list)
		# print(price_list)
		# print(date_list)
		# print(url_list)
		# with open(self.query + 'search' + '.csv', 'w') as f:
		# 	write = csv.writer(f)
		# 	# for entries in range(len(num)):
		# 		# print(posts)
		# 	for row in rows:
		# 		writer.writerow(row)

	# checking other pages
	def num_pages(self):
		pass

	def quit(self):
		self.driver.close()

if __name__ == "__main__":
	location = 'vancouver'
	query = 'foosball'
	radius = '40'
	postal = 'V3W7H5'
	
	scraper = CLScraper(location, query, radius, postal)
	scraper.load_url()
	# scraper.extract_titles()
	# scraper.extract_urls()
	# scraper.extract_dates()
	# scraper.extract_prices()
	# scraper.num_searches()
	scraper.write_to_csv()
	scraper.quit()