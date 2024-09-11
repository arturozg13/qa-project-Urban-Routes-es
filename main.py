from operator import truediv
from selenium.webdriver.ie.webdriver import WebDriver
import data
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from data import card_number
from UrbanRoutesPage import UrbanRoutesPage

class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        from selenium.webdriver import DesiredCapabilities
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        cls.driver = webdriver.Chrome()

    def test_set_route(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        WebDriverWait(self.driver, 5).until(expected_conditions.presence_of_element_located((By.ID, 'to')))
        routes_page.set_route(address_from, address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to

#2
    def test_comfort_rate_request(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        self.test_set_route()
        routes_page.comfort_rate_request()
        assert routes_page.check_comfort_rate_selected() == True #implementando la validacion del text 'Manta y panuelos'

#3
    def test_send_phone_number(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        self.test_comfort_rate_request()
        routes_page.send_phone_number()
        assert routes_page.get_phone_input_field() == data.phone_number #implementando la validacion del campo en el formulario


#4
    def test_add_credit_card(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        self.test_send_phone_number()
        routes_page.send_credit_card()
        assert routes_page.get_card_field() == data.card_number
        assert routes_page.check_card_added_text() == True


#5
    def test_send_message_for_driver(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        self.test_add_credit_card()
        routes_page.click_close_add_payment_window()
        routes_page.fill_message_for_driver_field()
        assert  routes_page.get_message_for_driver() == data.message_for_driver

#6
    def test_request_blanket_and_cloth(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        self.test_send_message_for_driver()
        routes_page.select_cloth_and_blanket()
        assert routes_page.check_cloth_and_blanket_is_selected() == True

#7
    def test_request_2_ice_cream(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        self.test_request_blanket_and_cloth()
        routes_page.select_add_ice_cream_button()
        assert routes_page.check_ice_cream_counter_value_2() == True

#8
    def test_request_taxi_pop_up_window(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        self.test_request_2_ice_cream()
        WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, '.smart-button-main')))
        routes_page.click_request_taxi_button()
        assert routes_page.check_taxi_requested_window_visible() == True




    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
