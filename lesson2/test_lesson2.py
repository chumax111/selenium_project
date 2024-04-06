import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from data import main_page, first_product_page
from locators import (username_field, password_field, login_button, first_add_to_cart_button, cart_button,
                      error_login_cross, first_product_id, burger_button, logout_button, about_button,
                      reset_app_button, bm_cross_button, dropdown_menu)
def test_auth_negative(browser):
    browser.get(main_page)

    browser.find_element('xpath', username_field).send_keys('user')
    browser.find_element(By.XPATH, password_field).send_keys('user')
    browser.find_element(By.XPATH, login_button).click()
    assert browser.current_url == main_page, 'The URL is not as expected'
    assert browser.find_element(By.XPATH, error_login_cross).is_displayed(), 'Error message is missing'

def test_cart_add_product_from_catalog(auth, browser):
    browser.find_element(By.XPATH, first_add_to_cart_button).click()
    browser.find_element(By.XPATH, cart_button).click()
    assert browser.find_element(By.XPATH, first_product_id).is_displayed(), 'Product is missing in the cart'

def test_cart_remove_product_through_cart(auth, browser):
    browser.find_element(By.XPATH, first_add_to_cart_button).click()
    browser.find_element(By.XPATH, cart_button).click()
    browser.find_element(By.XPATH, '//*[@class="btn_secondary cart_button"]').click()
    assert not browser.find_elements(By.XPATH, first_product_id), 'Product wasn\'t removed from the cart'

def test_cart_add_product_from_product_card(auth, browser):
    browser.find_element(By.XPATH, first_product_id).click()
    browser.find_element(By.XPATH, '//*[@class="btn_primary btn_inventory"]').click()
    browser.find_element(By.XPATH, cart_button).click()
    assert browser.find_element(By.XPATH, first_product_id).is_displayed(), 'Product is missing in the cart'

def test_cart_remove_product_through_product_card(auth, browser):
    browser.find_element(By.XPATH, first_product_id).click()
    browser.find_element(By.XPATH, '//*[@class="btn_primary btn_inventory"]').click()
    browser.find_element(By.XPATH, '//*[@class="btn_secondary btn_inventory"]').click()
    browser.find_element(By.XPATH, cart_button).click()
    assert not browser.find_elements(By.XPATH, first_product_id), 'Product wasn\'t removed from the cart'

def test_product_card_navigate_from_image(auth, browser):
    browser.find_element(By.XPATH, '//*[@id="item_4_img_link"]/img').click()
    assert browser.current_url == first_product_page, 'The URL is not as expected'

def test_product_card_navigate_from_name(auth, browser):
    browser.find_element(By.XPATH, first_product_id).click()
    assert browser.current_url == first_product_page, 'The URL is not as expected'

def test_placing_an_order(auth, browser):
    browser.find_element(By.XPATH, first_add_to_cart_button).click()
    browser.find_element(By.XPATH, cart_button).click()
    browser.find_element(By.XPATH, '//*[@class="btn_action checkout_button"]').click()
    browser.find_element(By.XPATH, '//*[@id="first-name"]').send_keys('Max')
    browser.find_element(By.XPATH, '//*[@id="last-name"]').send_keys('Johns')
    browser.find_element(By.XPATH, '//*[@id="postal-code"]').send_keys('99019')
    browser.find_element(By.XPATH, '//*[@value="CONTINUE"]').click()
    browser.find_element(By.XPATH, '//*[@class="btn_action cart_button"]').click()
    assert browser.current_url == 'https://www.saucedemo.com/v1/checkout-complete.html', 'The URL is not as expected'

def test_filter_a_to_z(auth, browser):
    dropdown = browser.find_element(By.XPATH, dropdown_menu)
    select = Select(dropdown)
    select.select_by_value('az')
    products = browser.find_elements(By.XPATH, '//*[@class="inventory_item_name"]')
    products_names = [product.text for product in products]
    assert products_names == sorted(products_names), 'No filter was applied'

def test_filter_z_to_a(auth, browser):
    dropdown = browser.find_element(By.XPATH, dropdown_menu)
    select = Select(dropdown)
    select.select_by_value('za')
    products = browser.find_elements(By.XPATH, '//*[@class="inventory_item_name"]')
    products_names = [product.text for product in products]
    assert products_names == sorted(products_names, reverse=True), 'No filter was applied'

def test_filter_low_to_high(auth, browser):
    dropdown = browser.find_element(By.XPATH, dropdown_menu)
    select = Select(dropdown)
    select.select_by_value('lohi')
    products = browser.find_elements(By.XPATH, '//*[@class="inventory_item_price"]')
    products_prices = [float(product.text[1:]) for product in products]
    print(products_prices)
    print(sorted(products_prices))
    assert products_prices == sorted(products_prices), 'No filter was applied'

def test_filter_high_to_low(auth, browser):
    dropdown = browser.find_element(By.XPATH, dropdown_menu)
    select = Select(dropdown)
    select.select_by_value('hilo')
    products = browser.find_elements(By.XPATH, '//*[@class="inventory_item_price"]')
    products_prices = [float(product.text[1:]) for product in products]
    assert products_prices == sorted(products_prices, reverse=True), 'No filter was applied'

def test_burger_logout(auth, browser):
    browser.find_element(By.XPATH, burger_button).click()
    browser.implicitly_wait(0.5)
    browser.find_element(By.XPATH, logout_button).click()
    assert browser.current_url == 'https://www.saucedemo.com/v1/index.html', 'The URL is not as expected'

def test_burger_about(auth, browser):
    browser.find_element(By.XPATH, burger_button).click()
    browser.implicitly_wait(0.5)
    browser.find_element(By.XPATH, about_button).click()
    assert browser.current_url == 'https://saucelabs.com/', 'The URL is not as expected'

def test_burger_reset_app(auth, browser):
    browser.find_element(By.XPATH, first_add_to_cart_button).click()
    browser.find_element(By.XPATH, burger_button).click()
    browser.implicitly_wait(0.5)
    browser.find_element(By.XPATH, reset_app_button).click()
    browser.implicitly_wait(1.0)
    browser.find_element(By.XPATH, bm_cross_button).click()
    browser.implicitly_wait(1.0)
    browser.find_element(By.XPATH, cart_button).click()
    assert not browser.find_elements(By.XPATH, first_product_id), 'App wasn\'t reset correctly.'





