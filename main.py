import data
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
import  time

# No modificar
def retrieve_phone_code(driver) -> str:
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
        if code:
            return code
        time.sleep(1)
    raise Exception("No se encontró el código de confirmación del teléfono.\n"
                    "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")

def create_driver_with_capabilities():
    from selenium.webdriver import DesiredCapabilities
    from selenium.webdriver.chrome.options import Options

    # Configurar las capacidades y opciones
    capabilities = DesiredCapabilities.CHROME.copy()
    capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}

    # Crear las opciones de Chrome
    chrome_options = Options()
    chrome_options.set_capability("goog:loggingPrefs", {'performance': 'ALL'})

    # Ajustar el servicio
    service = Service()  # Puedes especificar la ruta si es necesario

    # Crear y devolver el WebDriver con las opciones y capacidades ajustadas
    return webdriver.Chrome(service=service, options=chrome_options)


class UrbanRoutesPage:
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    personal_mode_button = (By.XPATH, "//div[@class='mode' and contains(text(),'Personal')]")
    taxi_icon_button = (By.XPATH, "//img[contains(@src, 'taxi-active')]")
    request_taxi_button = (By.XPATH, "//button[contains(text(),'Pedir un taxi')]")
    comfort_tariff_button = (By.XPATH, "//div[contains(text(), 'Comfort')]")
    phone_number_button = (By.CLASS_NAME, 'np-button')
    phone_input = (By.ID, 'phone')
    phone_submit_button = (By.XPATH, "//button[contains(text(),'Siguiente')]")
    payment_method_button = (By.CLASS_NAME, 'pp-button')
    add_card_button = (By.XPATH, "//div[contains(text(), 'Agregar tarjeta')]")
    card_number_input = (By.ID, 'number')
    card_code_input = (By.XPATH, "//input[@id='code' and @placeholder='12']")
    confirm_card_button = (By.XPATH, "//button[contains(text(),'Agregar')]")
    message_div = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[3]/div')
    message_input_field = (By.XPATH, '//*[@id="comment"]')
    blanket_switch = (By.XPATH, "//*[@id='root']/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[1]/div/div[2]/div")
    ice_cream_counter_plus = (By.XPATH, "//*[@id='root']/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[3]/div/div[2]/div[1]/div/div[2]/div/div[3]")
    find_taxi_button = (By.XPATH, "//span[contains(text(),'Pedir un taxi')]")
    driver_info_modal = (By.CLASS_NAME, 'order-header-title')
    close_button = (By.XPATH, "//*[@id='root']/div/div[2]/div[2]/div[1]/button")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)  # Esperar hasta 10 segundos para que los elementos sean visibles

    def set_route(self, from_address, to_address):
        self.set_from(from_address)
        self.set_to(to_address)

    def set_from(self, from_address):
        from_element = self.wait.until(EC.visibility_of_element_located(self.from_field))
        from_element.clear()
        from_element.send_keys(from_address)

    def set_to(self, to_address):
        to_element = self.wait.until(EC.visibility_of_element_located(self.to_field))
        to_element.clear()
        to_element.send_keys(to_address)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def select_personal_mode(self):
        element = self.wait.until(EC.element_to_be_clickable(self.personal_mode_button))
        element.click()

    def click_taxi_icon(self):
        element = self.wait.until(EC.element_to_be_clickable(self.taxi_icon_button))
        element.click()

    def request_taxi(self):
        element = self.wait.until(EC.element_to_be_clickable(self.request_taxi_button))
        element.click()

    def select_comfort_tariff(self):
        element = self.wait.until(EC.element_to_be_clickable(self.comfort_tariff_button))
        element.click()

    def click_phone_number_button(self):
        element = self.wait.until(EC.element_to_be_clickable(self.phone_number_button))
        element.click()

    def enter_phone_number(self, phone_number):
        phone_field = self.wait.until(EC.element_to_be_clickable(self.phone_input))
        phone_field.clear()
        phone_field.send_keys(phone_number)
        self.driver.find_element(*self.phone_submit_button).click()

        # Esperar a que aparezca la ventana emergente "Introduce el código"
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//div[contains(text(),'Introduce el código')]"))
        )

        # Obtener el código del SMS desde los logs de rendimiento
        code = retrieve_phone_code(self.driver)

        # Ingresar el código de confirmación
        code_input = self.driver.find_element(By.ID, 'code')
        code_input.clear()
        code_input.send_keys(code)

        # Hacer clic en el botón de confirmar
        confirm_button = self.driver.find_element(By.XPATH, "//button[contains(text(),'Confirmar')]")
        confirm_button.click()

    def choose_payment_method(self):
        element = self.wait.until(EC.element_to_be_clickable(self.payment_method_button))
        element.click()

    def add_credit_card(self, card_number, card_code):
        # Esperar y hacer clic en el botón "Agregar tarjeta"
        add_card_element = self.wait.until(EC.element_to_be_clickable(self.add_card_button))
        add_card_element.click()

        # Ingresar número de tarjeta
        card_number_field = self.wait.until(EC.visibility_of_element_located(self.card_number_input))
        card_number_field.clear()
        card_number_field.send_keys(card_number)

        # Hacer clic en el campo de código de tarjeta
        card_code_field = self.wait.until(EC.visibility_of_element_located(self.card_code_input))
        card_code_field.click()

        # Ingresar código de tarjeta
        card_code_field.send_keys(card_code)

        # Hacer clic en cualquier parte de la página para que el botón "Agregar" se habilite
        self.driver.find_element(By.TAG_NAME, 'body').click()

        # Esperar a que el botón "Agregar" esté habilitado
        confirm_button = self.wait.until(EC.element_to_be_clickable(self.confirm_card_button))
        confirm_button.click()

        # Cerrar la ventana emergente de "Método de pago"
        close_button = self.wait.until(EC.element_to_be_clickable(self.close_button))
        close_button.click()

    def write_message_to_driver(self, message):
        # Hacer clic en el div para enfocar el campo de entrada de mensajes
        message_div_element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.message_div)
        )
        message_div_element.click()

        # Esperar a que el campo de entrada de mensaje esté visible y clickeable
        message_input_element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.message_input_field)
        )

        # Limpiar cualquier texto existente en el campo de entrada
        message_input_element.clear()

        # Escribir el mensaje en el campo de entrada
        message_input_element.send_keys(message)

    def open_requirements_section(self):
        reqs_section = self.driver.find_element(By.CLASS_NAME, 'reqs')
        class_attr = reqs_section.get_attribute('class')
        if 'open' not in class_attr:
            header = reqs_section.find_element(By.CLASS_NAME, 'reqs-header')
            header.click()
            WebDriverWait(self.driver, 10).until(
                lambda driver: 'open' in reqs_section.get_attribute('class')
            )

    def request_blanket_and_tissues(self):
        # Asegúrate de que la sección de requisitos esté abierta
        self.open_requirements_section()

        # Localizar el switch de "Manta y pañuelos"
        blanket_switch_element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.blanket_switch)
        )

        # Utilizamos JavaScript para hacer clic en el switch (útil si hay capas sobre el switch)
        self.driver.execute_script("arguments[0].click();", blanket_switch_element)

    def request_two_ice_creams(self):
        self.open_requirements_section()
        self.wait_for_overlay_to_disappear()
        ice_cream_plus = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.ice_cream_counter_plus)
        )
        for _ in range(2):
            ice_cream_plus.click()
            time.sleep(0.5)

    def wait_for_overlay_to_disappear(self):
        WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.CLASS_NAME, 'overlay')))

    def find_taxi(self):
        find_taxi_button_element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.find_taxi_button)
        )
        find_taxi_button_element.click()

    def wait_for_driver_info(self):
        WebDriverWait(self.driver, 60).until(EC.visibility_of_element_located(self.driver_info_modal))
        time.sleep(5)

class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        cls.driver = create_driver_with_capabilities()

    def test_set_route(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to

    def test_complete_taxi_order(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)

        # Ingresar direcciones en "Desde" y "Hasta"
        routes_page.set_route(data.address_from, data.address_to)
        assert routes_page.get_from() == data.address_from
        assert routes_page.get_to() == data.address_to

        # Seleccionar "Personal" como modo de transporte
        routes_page.select_personal_mode()

        # Hacer clic en el ícono de taxi
        routes_page.click_taxi_icon()

        # Solicitar un taxi
        routes_page.request_taxi()

        # Seleccionar tarifa Comfort
        routes_page.select_comfort_tariff()

        # Ingresar número de teléfono
        routes_page.click_phone_number_button()
        routes_page.enter_phone_number(data.phone_number)

        # Seleccionar método de pago y agregar tarjeta de crédito
        routes_page.choose_payment_method()
        routes_page.add_credit_card(data.card_number, data.card_code)

        # Enviar mensaje al conductor
        routes_page.write_message_to_driver(data.message_for_driver)

        # Pedir manta y pañuelos
        routes_page.request_blanket_and_tissues()

        # Pedir 2 helados
        routes_page.request_two_ice_creams()

        # Buscar un taxi
        routes_page.find_taxi()

        # Esperar información del conductor
        routes_page.wait_for_driver_info()

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
