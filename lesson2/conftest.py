import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from locators import username_field, password_field, login_button
from data import login, password


@pytest.fixture()
def browser():
    browser = webdriver.Chrome()
    yield browser
    print('\nquit browser...')
    browser.quit()

@pytest.fixture()
def auth(browser):
    browser.get('https://www.saucedemo.com/v1/')

    browser.find_element('xpath', username_field).send_keys(login)
    browser.find_element(By.XPATH, password_field).send_keys(password)
    browser.find_element(By.XPATH, login_button).click()
    assert browser.current_url == 'https://www.saucedemo.com/v1/inventory.html', 'The URL is not as expected'
