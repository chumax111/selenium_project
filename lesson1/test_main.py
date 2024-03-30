from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import pytest

browser = webdriver.Chrome()

def test_auth_positive():
    browser.get('https://www.saucedemo.com/v1/')

    browser.find_element('xpath', '//*[@id="user-name"]').send_keys('standard_user')
    browser.find_element(By.XPATH, '//*[@id="password"]').send_keys('secret_sauce')
    browser.find_element(By.XPATH, '//*[@id="login-button"]').click()
    assert browser.current_url == 'https://www.saucedemo.com/v1/inventory.html', 'The URL is not as expected'
    # browser.quit()

def test_auth_negative():
    browser.get('https://www.saucedemo.com/v1/')

    browser.find_element('xpath', '//*[@id="user-name"]').send_keys('user')
    browser.find_element(By.XPATH, '//*[@id="password"]').send_keys('user')
    browser.find_element(By.XPATH, '//*[@id="login-button"]').click()
    assert browser.current_url == 'https://www.saucedemo.com/v1/', 'The URL is not as expected'
    assert browser.find_element(By.XPATH, '//*[@class="error-button"]').is_displayed(), 'Error message is missing'

def test_cart_add_product_from_catalog():
    test_auth_positive()
    browser.find_element(By.XPATH, '//*[@id="item_4_img_link"]/parent::*/following-sibling::div[@class="pricebar"]//button[@class="btn_primary btn_inventory"]').click()
    browser.find_element(By.XPATH, '//*[@id = "shopping_cart_container"]').click()
    assert browser.find_element(By.XPATH, '//*[@id="item_4_title_link"]').is_displayed(), 'Product is missing in the cart'

def test_cart_remove_product_through_cart():
    test_auth_positive()
    browser.find_element(By.XPATH, '//*[@id="item_4_img_link"]/parent::*/following-sibling::div[@class="pricebar"]//button[@class="btn_primary btn_inventory"]').click()
    browser.find_element(By.XPATH, '//*[@id = "shopping_cart_container"]').click()
    browser.find_element(By.XPATH, '//*[@class="btn_secondary cart_button"]').click()
    assert not browser.find_elements(By.XPATH, '//*[@id="item_4_title_link"]'), 'Product wasn\'t removed from the cart'

def test_cart_add_product_from_product_card():
    test_auth_positive()
    browser.find_element(By.XPATH, '//*[@id="item_4_title_link"]').click()
    browser.find_element(By.XPATH, '//*[@class="btn_primary btn_inventory"]').click()
    browser.find_element(By.XPATH, '//*[@id= "shopping_cart_container"]').click()
    assert browser.find_element(By.XPATH, '//*[@id="item_4_title_link"]').is_displayed(), 'Product is missing in the cart'

def test_cart_remove_product_through_product_card():
    test_auth_positive()
    browser.find_element(By.XPATH, '//*[@id="item_4_title_link"]').click()
    browser.find_element(By.XPATH, '//*[@class="btn_primary btn_inventory"]').click()
    browser.find_element(By.XPATH, '//*[@class="btn_secondary btn_inventory"]').click()
    browser.find_element(By.XPATH, '//*[@id= "shopping_cart_container"]').click()
    assert not browser.find_elements(By.XPATH, '//*[@id="item_4_title_link"]'), 'Product wasn\'t removed from the cart'

def test_product_card_navigate_from_image():
    test_auth_positive()
    browser.find_element(By.XPATH, '//*[@id="item_4_img_link"]/img').click()
    assert browser.current_url == 'https://www.saucedemo.com/v1/inventory-item.html?id=4', 'The URL is not as expected'

def test_product_card_navigate_from_name():
    test_auth_positive()
    browser.find_element(By.XPATH, '//*[@id="item_4_title_link"]').click()
    assert browser.current_url == 'https://www.saucedemo.com/v1/inventory-item.html?id=4', 'The URL is not as expected'

def test_placing_an_order():
    test_auth_positive()
    browser.find_element(By.XPATH,'//*[@id="item_4_img_link"]/parent::*/following-sibling::div[@class="pricebar"]//button[@class="btn_primary btn_inventory"]').click()
    browser.find_element(By.XPATH, '//*[@id = "shopping_cart_container"]').click()
    browser.find_element(By.XPATH, '//*[@class="btn_action checkout_button"]').click()
    browser.find_element(By.XPATH, '//*[@id="first-name"]').send_keys('Max')
    browser.find_element(By.XPATH, '//*[@id="last-name"]').send_keys('Johns')
    browser.find_element(By.XPATH, '//*[@id="postal-code"]').send_keys('99019')
    browser.find_element(By.XPATH, '//*[@value="CONTINUE"]').click()
    browser.find_element(By.XPATH, '//*[@class="btn_action cart_button"]').click()
    assert browser.current_url == 'https://www.saucedemo.com/v1/checkout-complete.html', 'The URL is not as expected'

def test_filter_a_to_z():
    test_auth_positive()
    dropdown = browser.find_element(By.CLASS_NAME, 'product_sort_container')
    select = Select(dropdown)
    select.select_by_value('az')
    products = browser.find_elements(By.XPATH, '//*[@class="inventory_item_name"]')
    products_names = [product.text for product in products]
    assert products_names == sorted(products_names), 'No filter was applied'

def test_filter_z_to_a():
    test_auth_positive()
    dropdown = browser.find_element(By.CLASS_NAME, 'product_sort_container')
    select = Select(dropdown)
    select.select_by_value('za')
    products = browser.find_elements(By.XPATH, '//*[@class="inventory_item_name"]')
    products_names = [product.text for product in products]
    assert products_names == sorted(products_names, reverse=True), 'No filter was applied'

def test_filter_low_to_high():
    test_auth_positive()
    dropdown = browser.find_element(By.CLASS_NAME, 'product_sort_container')
    select = Select(dropdown)
    select.select_by_value('lohi')
    products = browser.find_elements(By.XPATH, '//*[@class="inventory_item_price"]')
    products_prices = [float(product.text[1:]) for product in products]
    print(products_prices)
    print(sorted(products_prices))
    assert products_prices == sorted(products_prices), 'No filter was applied'

def test_filter_high_to_low():
    test_auth_positive()
    dropdown = browser.find_element(By.CLASS_NAME, 'product_sort_container')
    select = Select(dropdown)
    select.select_by_value('hilo')
    products = browser.find_elements(By.XPATH, '//*[@class="inventory_item_price"]')
    products_prices = [float(product.text[1:]) for product in products]
    assert products_prices == sorted(products_prices, reverse=True), 'No filter was applied'

def test_burger_logout():
    test_auth_positive()
    browser.find_element(By.XPATH, '//*[@class="bm-burger-button"]').click()
    browser.implicitly_wait(0.5)
    browser.find_element(By.XPATH, '//*[@id="logout_sidebar_link"]').click()
    assert browser.current_url == 'https://www.saucedemo.com/v1/index.html', 'The URL is not as expected'

def test_burger_about():
    test_auth_positive()
    browser.find_element(By.XPATH, '//*[@class="bm-burger-button"]').click()
    browser.implicitly_wait(0.5)
    browser.find_element(By.XPATH, '//*[@id="about_sidebar_link"]').click()
    assert browser.current_url == 'https://saucelabs.com/', 'The URL is not as expected'

def test_burger_reset_app():
    test_auth_positive()
    browser.find_element(By.XPATH, '//*[@id="item_4_img_link"]/parent::*/following-sibling::div[@class="pricebar"]//button[@class="btn_primary btn_inventory"]').click()
    browser.find_element(By.XPATH, '//*[@class="bm-burger-button"]').click()
    browser.implicitly_wait(0.5)
    browser.find_element(By.XPATH, '//*[@id="reset_sidebar_link"]').click()
    browser.implicitly_wait(1.0)
    browser.find_element(By.XPATH, '//*[@class="bm-cross-button"]').click()
    browser.implicitly_wait(1.0)
    browser.find_element(By.XPATH, '//*[@id="shopping_cart_container"]').click()
    assert not browser.find_elements(By.XPATH, '//*[@id="item_4_title_link"]'), 'App wasn\'t reset correctly.'





