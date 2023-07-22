from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

service = ChromeService(executable_path=ChromeDriverManager().install())

browser = webdriver.Chrome(service=service)

browser.get('http://localhost:8000')
assert 'Congratulations!' in browser.title



