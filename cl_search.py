from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from bs4 import BeautifulSoup as soup
import urllib.request

class CLScraper():
	def __init__(self, location, postal, radius):
		self.location = location
		self.postal = postal
		self.radius = radius
		self.url = ('https://{}.craigslist.ca/search/sss?search_'
			'distance={}&postal={}').format(location, radius, postal)
		self.driver = webdriver.Chrome()
		self.delay = 3

	def load_url(self):
		self.driver.get(self.url)
		try:
			wait = WebDriverWait(self.driver, self.delay)
			wait.until(EC.presence_of_element_located((By.ID,
				'searchform')))
			print('Page is ready')
		except TimeoutException:
			print('Loading took too much time')

	def extract_titles(self):
		all_titles = self.driver.find_elements_by_class_name(
			'result-row')
		titles_list = []
		for post in all_titles:
			titles_list.append(post.text)
		return titles_list

	def extract_urls(self):
		url_list = []
		html_page = urllib.request.urlopen(self.url)
		data = soup(html_page, 'lxml')
		for links in data.findAll('a', {'class':
			'result-title hdrlnk'}):
			url_list.append(links['href'])
		print(url_list)
		return url_list

	def extract_date(self):
		pass

	def extract_price(self):
		pass

	def write_to_csv(self):
		pass

	# want to extract titles, urls, date of posting, price

	def quit(self):
		self.driver.close()

if __name__ == "__main__":
	location = 'vancouver'
	postal = 'V3W7H5'
	radius = '40'
	
	scraper = CLScraper(location, postal, radius)
	scraper.load_url()
	# scraper.extract_titles()
	scraper.extract_urls()
	scraper.quit()