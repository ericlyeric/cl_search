import csv
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class GoodReadsBookSearch():
	def __init__(self):
		self.MAX_PAGE_NUM = 15
		self.driver = webdriver.Chrome()
		self.filename = 'Motivational_and_Self_Improvement_Books'

	def CreateCSV(self):
		with open(self.filename + '.csv', 'w') as f:
			f.write('Book Title, Book Rating\n')

	def WriteCSV(self, books, rating):
		with open(self.filename + '.csv', 'a') as f:
			for rank in range(len(books)):
				f.write(books[rank].text + ',' + rating[rank].text 
					+ '\n')
	
	def PopUpCheck(self):
		try:
			time.sleep(2)
			self.driver.find_element_by_xpath('/html/body/div[5]\
				/div/div/div[1]/button/img').click()
		except:
			pass

	def PageSearch(self, url):
		for page in range(1, self.MAX_PAGE_NUM + 1):
			url_base = url
			url_new = url_base + str(page)

			self.driver.get(url_new)

			# check and close pop up
			self.PopUpCheck()

			# extract books
			books = self.driver.find_elements_by_class_name('bookTitle')
			rating = self.driver.find_elements_by_class_name('minirating')

			# save results to csv
			self.WriteCSV(books, rating)
			
		# close browser when finished
		self.driver.close()

if __name__ == "__main__":
	search1 = GoodReadsBookSearch()
	search1.CreateCSV()
	url = 'https://www.goodreads.com/list/show/7616.Motivational\
		_and_Self_Improvement_Books?page='
	search1.PageSearch(url)