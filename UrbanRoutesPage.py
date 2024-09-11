from operator import truediv
from selenium.webdriver.ie.webdriver import WebDriver
import data
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
import helpers

class UrbanRoutesPage:
    #Direccion
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    #Tarrifa
    book_a_taxi_button = (By.CSS_SELECTOR, '.button.round')
    select_comfort_rate = (By.XPATH, '//div[@class="tcard-title"][text()="Comfort"]')
    validate_comfort_rate = (By.XPATH, '//*[text()="Manta y pañuelos"]') #implementando la validacion de el texto 'manta y panuelos'
    #Telefono
    phone_input_button = (By.CLASS_NAME, 'np-button')
    phone_input_field = (By.XPATH, '//*[@id="phone"]')
    phone_input_send = (By.XPATH, '//div[@class="buttons"]/button[text()="Siguiente"]')
    input_sms_code = (By.XPATH, '//input[@placeholder="xxxx"]')
    send_sms_code = (By.XPATH, '//*[@class="button full"][text()="Confirmar"]')
    validate_phone_number = (By.XPATH, '//*[@class="np-text"]') #implementando la validacion del campo en el formularion
    #Metodo de pago
    payment_method_button = (By.CSS_SELECTOR, '.pp-text')
    add_card_button = (By.CSS_SELECTOR, '.pp-plus')
    add_card_field = (By.ID, 'number')
    card_code_field = (By.NAME, 'code')
    change_focus_click_card_field = (By.ID, 'number')
    send_card_info = (By.XPATH, '//*[@class="button full"][text()="Agregar"]')
    card_added_text = (By.XPATH, '//*[@class="pp-title"][text()="Tarjeta"]')
    close_add_payment_window = (By.XPATH, '//div[@class="payment-picker open"]/div[@class="modal"]/div[@class="section active"]/button')
    #Mensaje para conductor
    message_for_driver_field = (By.CSS_SELECTOR, '#comment')
    #Pedir manta/panuelo y helado
    slider_for_blanket_and_cloth  = (By.XPATH, '(//*[@class="slider round"])[1]')
    blanket_cloth_selected = (By.XPATH, '(//*[@type="checkbox"][@class="switch-input"])[1]')
    counter_add_for_icecream = (By.XPATH , '(//*[@class="counter-plus"])[1]')
    ice_cream_counter_value_2 = (By.XPATH, '//*[@class="counter-value"][text()="2"]')
    #Modal para buscar taxi
    request_taxi_button = (By.CSS_SELECTOR, '.smart-button-main')
    taxi_requested_window = (By.CLASS_NAME, 'order-header-title')


    def __init__(self, driver):
        self.driver = driver
#1 Configurar direccion
    def set_from(self, from_address):
        self.driver.find_element(*self.from_field).send_keys(from_address)

    def set_to(self, to_address):
        self.driver.find_element(*self.to_field).send_keys(to_address)

                 # Paso set_route
    def set_route(self, from_address, to_address):
        self.set_from(from_address)
        self.set_to(to_address)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')
#2 Seleccionar tarifa comfort
    def click_book_a_taxi_button(self):
        self.driver.find_element(*self.book_a_taxi_button).click()

    def click_comfort_rate(self):
        self.driver.find_element(*self.select_comfort_rate).click()

    def check_comfort_rate_selected(self):
        return self.driver.find_element(*self.validate_comfort_rate).is_displayed() #implementando la validacion del texto 'manta y panuelos'


                # Paso comfort_rate_request
    def comfort_rate_request(self):
        WebDriverWait(self.driver, 3).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, '.button.round')))
        self.click_book_a_taxi_button()
        self.click_comfort_rate()

#3 Rellenar el numero de telefono
    def click_phone_input_button(self):
        self.driver.find_element(*self.phone_input_button).click()

    def fill_phone_input_field(self, phone_number):
        self.driver.find_element(*self.phone_input_field).send_keys(phone_number)

    def submit_phone_number(self):
        self.driver.find_element(*self.phone_input_send).click()

    def get_phone_input_field(self):
        return self.driver.find_element(*self.validate_phone_number).get_property('innerText') #implementando la validacion del campo en el formulario

    def fill_sms_field(self):
        self.driver.find_element(*self.input_sms_code).send_keys(helpers.retrieve_phone_code(self.driver))

    def confirm_sms_code(self):
        self.driver.find_element(*self.send_sms_code).click()


                # Paso send_phone_number
    def send_phone_number(self):
        self.click_phone_input_button()
        self.fill_phone_input_field(data.phone_number)
        self.submit_phone_number()
        self.fill_sms_field()
        self.confirm_sms_code()

#4 Agregar tarjeta de credito
    def click_payment_method_button(self):
        self.driver.find_element(*self.payment_method_button).click()

    def click_add_card_button(self):
        self.driver.find_element(*self.add_card_button).click()

    def fill_add_card_field(self):
        self.driver.find_element(*self.add_card_field).send_keys(data.card_number)

    def fill_card_code_field(self):
        self.driver.find_element(*self.card_code_field).send_keys(data.card_code)

    def change_card_code_focus(self):
        self.driver.find_element(*self.change_focus_click_card_field).click()

    def submit_card_info(self):
        self.driver.find_element(*self.send_card_info).click()

    def get_card_field(self):
        return self.driver.find_element(*self.add_card_field).get_property('value')

    def check_card_added_text(self):
        return self.driver.find_element(*self.card_added_text).is_displayed()

    def click_close_add_payment_window(self):
        self.driver.find_element(*self.close_add_payment_window).click()


                # Paso send_credit_card
    def send_credit_card(self):
        self.click_payment_method_button()
        self.click_add_card_button()
        self.fill_add_card_field()
        self.fill_card_code_field()
        self.change_card_code_focus()
        self.submit_card_info()


#5 Mensaje para conductor
    def fill_message_for_driver_field(self):
        self.driver.find_element(*self.message_for_driver_field).send_keys(data.message_for_driver)

    def get_message_for_driver(self):
        return self.driver.find_element(*self.message_for_driver_field).get_property('value')

#6 Pedir manta y panuelo
    def select_cloth_and_blanket(self):
        self.driver.find_element(*self.slider_for_blanket_and_cloth).click()

    def check_cloth_and_blanket_is_selected(self):
         return self.driver.find_element(*self.blanket_cloth_selected).is_selected()


#7 Pedir 2 helados
    def select_add_ice_cream_button(self):
       self.driver.find_element(*self.counter_add_for_icecream).click()
       self.driver.find_element(*self.counter_add_for_icecream).click()

    def check_ice_cream_counter_value_2(self):
       return self.driver.find_element(*self.ice_cream_counter_value_2).is_displayed()


#8 Aparece modal para buscar taxi
    def click_request_taxi_button(self):
        self.driver.find_element(*self.book_a_taxi_button).click()

    def check_taxi_requested_window_visible(self):
        return self.driver.find_element(*self.taxi_requested_window).is_displayed()

