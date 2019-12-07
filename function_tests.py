from selenium import webdriver

# https://codedragon.tistory.com/6114
# C:\Users\sdrlu\Anaconda\Library\bin
browser = webdriver.Firefox()
browser.get('http://localhost:8000')

assert 'Django' in browser.title