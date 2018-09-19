import csv
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# keep track of number of pages
MAX_PAGE_NUM = 15
PAGE_NUM = 1

# open csv file
with open('Motivational_and_Self_Improvement_Books.csv', 'w') as f:
	f.write('Book Title, Book Rating\n')

# open up chrome browser
driver = webdriver.Chrome()

for page in range(1, MAX_PAGE_NUM+1):
	url = 'https://www.goodreads.com/list/show/7616.Motivational\
	_and_Self_Improvement_Books?page='+str(page)

	driver.get(url)

	# wait to see if there is a pop up if there is then close the window
	try:
		time.sleep(2)
		driver.find_element_by_xpath('/html/body/div[5]/div/div/div[1]/\
			button/img').click()
	except:
		pass

	try:
		alert = driver.switch_to_alert()
		alert.dismiss()
	except:
		pass

	# extract books
	books = driver.find_elements_by_class_name('bookTitle')
	rating = driver.find_elements_by_class_name('minirating')

	with open('Motivational_and_Self_Improvement_Books.csv', 'a') as f:
		for rank in range(len(books)):
			f.write(books[rank].text + ',' + rating[rank].text + '\n')

# close browser when finished
driver.close()