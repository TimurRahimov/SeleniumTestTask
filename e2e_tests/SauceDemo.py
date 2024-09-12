import random
import unittest

from dataclasses import dataclass
from faker import Faker
from selenium import webdriver
from selenium.webdriver.common.by import By


class SauceDemo(unittest.TestCase):
    @dataclass
    class CartItem:
        name: str = ""
        desc: str = ""
        price: str = ""

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.faker = Faker()
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

    def test_adding_one_good_to_cart(self, cart_item: CartItem = None):
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

        self.__goto_shopping_cart()

        cart_items = self.driver.find_elements(By.CLASS_NAME, "cart_item")
        self.assertEqual(len(cart_items), 1)

        cart_item_name = cart_items[0].find_element(By.CLASS_NAME, "inventory_item_name").text
        cart_item_desc = cart_items[0].find_element(By.CLASS_NAME, "inventory_item_desc").text
        cart_item_price = cart_items[0].find_element(By.CLASS_NAME, "inventory_item_price").text

        self.assertEqual(inventory_item_name, cart_item_name)
        self.assertEqual(inventory_item_desc, cart_item_desc)
        self.assertEqual(inventory_item_price, cart_item_price)

        if cart_item is not None:
            cart_item.name = cart_item_name
            cart_item.desc = cart_item_desc
            cart_item.price = cart_item_price.split("$")[1]

    def test_adding_and_removing_good_to_cart(self):
        self.test_adding_one_good_to_cart()

        for cart_item in self.driver.find_elements(By.CLASS_NAME, "cart_item"):
            cart_item.find_element(By.CLASS_NAME, "cart_button").click()

        self.assertEqual(len(self.driver.find_elements(By.CLASS_NAME, "cart_item")), 0)
        self.driver.refresh()
        self.assertEqual(len(self.driver.find_elements(By.CLASS_NAME, "cart_item")), 0)

    def test_purchase(self):
        cart_item = self.CartItem()
        self.test_adding_one_good_to_cart(cart_item)

        checkout_btn = self.driver.find_element(By.ID, "checkout")
        checkout_btn.click()

        first_name = self.driver.find_element(By.ID, "first-name")
        first_name.send_keys(self.faker.first_name())
        last_name = self.driver.find_element(By.ID, "last-name")
        last_name.send_keys(self.faker.last_name())
        postal_code = self.driver.find_element(By.ID, "postal-code")
        postal_code.send_keys(self.faker.postcode())

        continue_btn = self.driver.find_element(By.ID, "continue")
        continue_btn.click()

        checkout_items = self.driver.find_elements(By.CLASS_NAME, "cart_item")
        self.assertEqual(len(checkout_items), 1)

        cart_item_name = checkout_items[0].find_element(By.CLASS_NAME, "inventory_item_name").text
        cart_item_desc = checkout_items[0].find_element(By.CLASS_NAME, "inventory_item_desc").text
        cart_item_price = checkout_items[0].find_element(By.CLASS_NAME, "inventory_item_price").text.split("$")[1]

        self.assertEqual(cart_item.name, cart_item_name)
        self.assertEqual(cart_item.desc, cart_item_desc)
        self.assertEqual(cart_item.price, cart_item_price)

        summary_subtotal = self.driver.find_element(By.CLASS_NAME, "summary_subtotal_label").text.split("$")[1]
        self.assertEqual(summary_subtotal, cart_item.price)

        summary_tax = self.driver.find_element(By.CLASS_NAME, "summary_tax_label").text.split("$")[1]
        summary_total = self.driver.find_element(By.CLASS_NAME, "summary_total_label").text.split("$")[1]

        self.assertEqual(round(float(summary_subtotal) + float(summary_tax), 2), round(float(summary_total), 2))

        finish_btn = self.driver.find_element(By.ID, "finish")
        finish_btn.click()

        complete_headers = self.driver.find_elements(By.CLASS_NAME, "complete-header")
        self.assertEqual(len(complete_headers), 1)

        self.__goto_shopping_cart()
        self.assertEqual(len(self.driver.find_elements(By.CLASS_NAME, "cart_item")), 0)

    def __goto_shopping_cart(self):
        shopping_cart_div = self.driver.find_element(By.ID, "shopping_cart_container")
        shopping_cart_div.click()

    def tearDown(self):
        self.driver.close()
