import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
import data
import locators

# no modificar

def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""

    import json
    import time
    from selenium.common import WebDriverException
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
        return code

class UrbanRoutesPage:

# Controlador

    def __init__(self, driver):
        self.driver = driver
# Espera a que aparezca el campo DESDE:
    def wait_for_from_field(self):
        WebDriverWait(self.driver, 10).until(expected_conditions.visibility_of_element_located(locators.from_field))
# Busco y relleno el campo DESDE:
    def set_from(self, from_address):
        self.driver.find_element(*locators.from_field).send_keys(from_address)
# Espera a que aparezca el campo HASTA:
    def wait_for_to_field(self):
        WebDriverWait(self.driver, 10).until(expected_conditions.visibility_of_element_located(locators.to_field))
# Busco y relleno el campo HASTA:
    def set_to(self, to_address):
        self.driver.find_element(*locators.to_field).send_keys(to_address)
# Este código me devuelve el valor del campo DESDE:
    def get_from(self):
        return self.driver.find_element(*locators.from_field).get_property('value')
# Este código me devuelve el valor del campo HASTA:
    def get_to(self):
        return self.driver.find_element(*locators.to_field).get_property('value')
# Busco y hago clic en el botón PEDIR TAXI:
    def wait_for_taxi_button(self):
        WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(locators.taxi_button))

    def click_taxi_button(self):
        self.driver.find_element(*locators.taxi_button).click()
#Todas estas acciones juntas:
    def set_route(self, from_address, to_address):
        self.wait_for_from_field()
        self.set_from(from_address)
        self.wait_for_to_field()
        self.set_to(to_address)
        self.wait_for_taxi_button()
        self.click_taxi_button()

#Espero hasta que aparezca el botón COMFORT:
    def wait_for_comfort_button(self):
        WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(locators.comfort_button))
# Busco y selecciona el botón COMFORT:
    def click_in_comfort(self):
        return self.driver.find_element(*locators.comfort_button).click()
    def comfort_button_is_selected(self):
        return self.driver.find_element(*locators.comfort_button).is_enabled()

# Busco, hago clic en el campo "agregar un número teléfono", se abre ventana emergente,
    def wait_for_telephone_button(self):
        WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(locators.phone_number_button))
    def click_telephone_number(self):
        self.driver.find_element(*locators.phone_number_button).click()

# agrego un número de teléfono, hago clic en siguiente
    def wait_for_telephone_field(self):
        WebDriverWait(self.driver, 10).until(expected_conditions.visibility_of_element_located(locators.phone_number_field))
    def add_telephone_number(self,phone_number):
        self.driver.find_element(*locators.phone_number_field).send_keys(phone_number)
    def click_siguiente_button(self):
        self.driver.find_element(*locators.siguiente_button).click()
    def get_telephone_description(self):
        return self.driver.find_element(*locators.phone_number_field).get_property('value')

# Se abre ventana emergente, obtengo código y busco y agrego código, hago clic en confirmar:
    def wait_for_code_field(self):
        WebDriverWait(self.driver, 10).until(expected_conditions.visibility_of_element_located(locators.code_field))
    def get_code(self,code):
        return self.driver.find_element(*locators.code_field).send_keys(code)

    # Espero hasta que aparezca el botón CONFIRMAR:
    def wait_for_confirmar_button(self):
        WebDriverWait(self.driver, 5).until(expected_conditions.element_to_be_clickable(locators.confirmar_button))
    def click_in_confirmar_button(self):
        self.driver.find_element(*locators.confirmar_button).click()

# Busco y hago clic en "Método de pago", se abre ventana emergente, clic nuevamente en "agregar una tarjeta",
    def click_metodo_de_pago(self):
        return self.driver.find_element(*locators.metodo_de_pago_button).click()
    def wait_for_add_card(self):
        WebDriverWait(self.driver, 3).until(expected_conditions.element_to_be_clickable(locators.add_card_button))
    def click_add_card(self):
        return self.driver.find_element(*locators.add_card_button).click()

# Busco e ingreso numero de tarjeta de crédito, busco e ingreso código de tarjeta:
    def add_card_number(self,card_number):
        return self.driver.find_element(*locators.add_card_field).send_keys(card_number)

    def add_code_number(self,card_code):
        return self.driver.find_element(*locators.add_code_card_field).send_keys(card_code)

# hago clic en cualquier otro elemento, hago clic en agregar, aparece ventana emergente, busco y clic en "cerrar"
    def click_in_any_other_element(self):
        return self.driver.find_element(*locators.any_other_element).click()
    def click_in_agregar(self):
        return self.driver.find_element(*locators.agregar_button).click()
    def get_number_credit_card(self):
        return self.driver.find_element(*locators.add_card_field).get_property('value')
    def get_code_credit_card(self):
        return self.driver.find_element(*locators.add_code_card_field).get_property('value')
    def click_in_cerrar(self):
        return self.driver.find_element(*locators.cerrar_button).click()

#Todo el proceso junto para agregar una tarjeta de credito
    def all_the_process_to_add_credit_card(self,card_number,card_code):
        self.click_metodo_de_pago()
        self.wait_for_add_card()
        self.click_add_card()
        self.add_card_number(card_number)
        time.sleep(3)
        self.add_code_number(card_code)
        time.sleep(3)
        self.click_in_any_other_element()
        self.click_in_agregar()
        self.click_in_cerrar()

# Scroll hasta que aparezca en pantalla el campo "Mensaje para el conductor", Busco el campo y Agrego mensaje:

    def wait_for_message_for_driver(self):
        WebDriverWait(self.driver, 3).until(expected_conditions.visibility_of_element_located(locators.message_for_driver))

    def send_message_for_driver(self):
        self.driver.find_element(*locators.message_for_driver).send_keys(data.message_for_driver)

    def get_message_for_driver(self):
        return self.driver.find_element(*locators.message_for_driver).get_property('value')

# Busco "requisitos del pedido" y hago clic en él

    def wait_for_requisitos_del_pedido(self):
        WebDriverWait(self.driver, 15).until(expected_conditions.element_to_be_clickable(locators.requisitos_del_pedido))
    def click_requisitos_del_pedido(self):
        self.driver.find_element(*locators.requisitos_del_pedido).click()

# Busco y clic la opción de pedir manta y pañuelos.
    def wait_for_pedido(self):
        WebDriverWait(self.driver, 15).until(expected_conditions.visibility_of_element_located(locators.manta_y_panuelos))

    def click_in_manta_y_panuelos(self):
        self.driver.find_element(*locators.manta_y_panuelos).click()

# Chequear que manta y pañuelos está seleccionado:
    def manta_y_panuelos_is_selected(self):
        return self.driver.find_element(*locators.manta_y_panuelos).is_enabled()

# Busco y hago dos veces clic a "Helado":

    def wait_for_icecream_button(self):
        WebDriverWait(self.driver, 15).until(expected_conditions.visibility_of_element_located(locators.helado_button))

    def click_in_icecream(self):
        self.driver.find_element(*locators.helado_button).click()

    def icecream_is_selected(self):
        return self.driver.find_element(*locators.helado_button).is_enabled()

# Busco el botón de el recorrido será de 1 kilometro y se hará en 1 minuto

    def wait_for_recorrido_button(self):
        WebDriverWait(self.driver, 15).until(expected_conditions.visibility_of_element_located(locators.recorrido_button))

# Hago click en él
    def click_in_recorrido(self):
        self.driver.find_element(*locators.recorrido_button).click()
# Busco la ventana emergente del modal de busqueda

    def wait_for_modal_de_busqueda(self):
        WebDriverWait(self.driver,15).until(expected_conditions.visibility_of_element_located(locators.modal_de_busqueda))

# Extraigo el texto de ese elemento para comprobarlo luego

    def modal_de_busqueda_text(self):
        return self.driver.find_element(*locators.modal_de_busqueda).text
class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        from selenium.webdriver import DesiredCapabilities
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        cls.driver = webdriver.Chrome()
        cls.driver.get(data.urban_routes_url)
        cls.driver.maximize_window()

    # Prueba 1: que los campos DESDE y HASTA se llenaron y guardaron correctamente:
    def test_set_route(self):
        routes_page = UrbanRoutesPage(self.driver)
        from_address = data.from_address
        to_address = data.to_address
        routes_page.set_route(from_address, to_address)
        assert routes_page.get_from() == from_address
        assert routes_page.get_to() == to_address

    #Prueba 2: comprueba que se ha seleccionado la opción comfort:
    def test_comfort_button_is_selected(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.wait_for_comfort_button()
        routes_page.click_in_comfort()
        comfort_is_selected = routes_page.comfort_button_is_selected()
        assert comfort_is_selected == True


    #Prueba 3: comprueba que se ha llenado correctamente el campo de numero de telefono:
    def test_telephone_number_field_is_filled(self):
        routes_page = UrbanRoutesPage(self.driver)
        phone_number = data.phone_number
        routes_page.wait_for_telephone_button()
        routes_page.click_telephone_number()
        routes_page.wait_for_telephone_field()
        routes_page.add_telephone_number(phone_number)
        time.sleep(3)
        routes_page.click_siguiente_button()
        routes_page.wait_for_code_field()
        phone_code = retrieve_phone_code(self.driver)
        routes_page.get_code(phone_code)
        routes_page.wait_for_confirmar_button()
        routes_page.click_in_confirmar_button()
        telephone_description = routes_page.get_telephone_description()
        assert telephone_description == phone_number

    #Prueba 4: Comprueba la funcionalidad de Agregar una tarjeta de crédito. Para que se active el el botón 'link' (enlace) no se activa hasta que el campo CVV
    # de la tarjeta en el modal 'Agregar una tarjeta' pierde el enfoque.
    # Se necesita el código de confirmación requerido para agregar una tarjeta.

    def test_credit_card_is_filled(self):
        routes_page = UrbanRoutesPage(self.driver)
        card_number = data.card_number
        card_code = data.card_code
        routes_page.all_the_process_to_add_credit_card(card_number,card_code)
        assert routes_page.get_number_credit_card() == card_number
        assert routes_page.get_code_credit_card() == card_code

    #Prueba 5:  Comprueba que se haya guardado el mensaje para el  controlador.

    def test_message_driver(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.wait_for_message_for_driver()
        routes_page.send_message_for_driver()
        text_message_for_driver = routes_page.get_message_for_driver()
        assert text_message_for_driver == data.message_for_driver


    # Prueba 6: Comprueba si se agrego al pedido una manta y pañuelos.
    def test_manta_y_panuelos_is_selected(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.wait_for_pedido()
        routes_page.click_in_manta_y_panuelos()
        manta_is_selected = routes_page.manta_y_panuelos_is_selected()
        assert manta_is_selected == True

    # Prueba 7: Comprueba si se agregaron al pedido 2 helados.

    def test_add_two_icecream(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.wait_for_icecream_button()
        routes_page.click_in_icecream()
        routes_page.click_in_icecream()
        is_icecream_selected = routes_page.icecream_is_selected()
        assert is_icecream_selected == True

    # Prueba 8: Comprueba si aparece el modal para buscar un taxi

    def test_modal_de_espera(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.wait_for_recorrido_button()
        routes_page.click_in_recorrido()
        routes_page.wait_for_modal_de_busqueda()
        modal_de_busqueda_text = routes_page.modal_de_busqueda_text()
        assert modal_de_busqueda_text == "Buscar automóvil"

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()