import random
import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By


class SauceDemo(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.root_url = "https://www.saucedemo.com/"

    def test_standard_authorization(self):
        self.driver.get(self.root_url)
        self.driver.delete_all_cookies()

        username = self.driver.find_element(By.ID, "user-name")
        username.send_keys("standard_user")
        password = self.driver.find_element(By.ID, "password")
        password.send_keys("secret_sauce")
        login_button = self.driver.find_element(By.ID, "login-button")
        login_button.click()

        cookies = self.driver.get_cookies()
        self.assertEqual(len(cookies), 1)
        self.assertEqual(cookies[0]['name'], 'session-username')
        self.assertNotEqual(len(cookies[0]['value']), 0)

    def test_adding_one_good_to_cart(self):
        self.test_standard_authorization()

        inventory_items_count = len(self.driver.find_elements(By.CLASS_NAME, "btn_inventory"))
        inventory_item_index = random.randint(0, inventory_items_count - 1)

        inventory_item = self.driver.find_elements(By.CLASS_NAME, "inventory_item")[inventory_item_index]
        inventory_item_name = inventory_item.find_element(By.CLASS_NAME, "inventory_item_name").text
        inventory_item_desc = inventory_item.find_element(By.CLASS_NAME, "inventory_item_desc").text
        inventory_item_price = inventory_item.find_element(By.CLASS_NAME, "inventory_item_price").text

        inventory_btn = inventory_item.find_element(By.CLASS_NAME, "btn_inventory")
        self.assertEqual(inventory_btn.text, "Add to cart")
        inventory_btn.click()

        self.assertEqual(self.driver.find_element(By.CLASS_NAME, "shopping_cart_badge").text, "1")

        inventory_btn = inventory_item.find_element(By.CLASS_NAME, "btn_inventory")
        self.assertEqual(inventory_btn.text, "Remove")

        shopping_cart_div = self.driver.find_element(By.ID, "shopping_cart_container")
        shopping_cart_div.click()

        cart_items = self.driver.find_elements(By.CLASS_NAME, "cart_item")
        self.assertEqual(len(cart_items), 1)

        cart_item_name = cart_items[0].find_element(By.CLASS_NAME, "inventory_item_name").text
        cart_item_desc = cart_items[0].find_element(By.CLASS_NAME, "inventory_item_desc").text
        cart_item_price = cart_items[0].find_element(By.CLASS_NAME, "inventory_item_price").text

        self.assertEqual(inventory_item_name, cart_item_name)
        self.assertEqual(inventory_item_desc, cart_item_desc)
        self.assertEqual(inventory_item_price, cart_item_price)

    def test_purchase(self):
        pass

    def tearDown(self):
        self.driver.close()
