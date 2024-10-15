import data
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException

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
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    personal_mode_button = (By.XPATH, "//div[@class='mode' and text()='Personal']")
    taxi_icon_button = (By.XPATH, "//div[@class='type active']//img[contains(@src, 'taxi-active')]")
    request_taxi_button = (By.XPATH, "//button[contains(text(),'Pedir un taxi')]")
    comfort_tariff_button = (By.XPATH, "//div[contains(text(), 'Comfort')]")
    phone_number_button = (By.CLASS_NAME, 'np-button')
    phone_input = (By.ID, 'phone')
    phone_submit_button = (By.XPATH, "//button[contains(text(),'Siguiente')]")
    payment_method_button = (By.CLASS_NAME, 'pp-button')
    add_card_button = (By.XPATH, "//div[contains(text(), 'Agregar tarjeta')]")
    card_number_input = (By.ID, 'number')
    card_code_input = (By.ID, 'code')
    confirm_card_button = (By.XPATH, "//button[contains(text(),'Agregar')]")
    message_input = (By.ID, 'comment')
    blanket_switch = (By.XPATH, "//div[@class='r-sw-label' and text()='Manta y pañuelos']//..//input")
    ice_cream_counter_plus = (
    By.XPATH, "//div[@class='r-counter-label' and text()='Helado']//..//div[@class='counter-plus']")
    find_taxi_button = (By.XPATH, "//span[contains(text(),'Pedir un taxi')]")
    driver_info_modal = (By.CLASS_NAME, 'order-header-title')

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)  # Esperar hasta 10 segundos para que los elementos sean visibles

    def set_route(self, from_address, to_address):
        self.set_from(from_address)
        self.set_to(to_address)

    def set_from(self, from_address):
        # Esperar hasta que el campo 'from' sea visible y luego interactuar con él
        from_element = self.wait.until(EC.visibility_of_element_located(self.from_field))
        from_element.clear()
        from_element.send_keys(from_address)

    def set_to(self, to_address):
        # Esperar hasta que el campo 'to' sea visible y luego interactuar con él
        to_element = self.wait.until(EC.visibility_of_element_located(self.to_field))
        to_element.clear()
        to_element.send_keys(to_address)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def select_personal_mode(self):
        self.driver.find_element(*self.personal_mode_button).click()

    def click_taxi_icon(self):
        self.driver.find_element(*self.taxi_icon_button)

    def request_taxi(self):
        self.driver.find_element(*self.request_taxi_button).click()

    def select_comfort_tariff(self):
        self.driver.find_element(*self.comfort_tariff_button).click()

    def click_phone_number_button(self):
        self.driver.find_element(*self.phone_number_button).click()

    def enter_phone_number(self, phone_number):
        # Ingresar el número de teléfono
        phone_field = self.driver.find_element(*self.phone_input)
        phone_field.clear()
        phone_field.send_keys(phone_number)
        self.driver.find_element(*self.phone_submit_button).click()

        # Esperar a que aparezca la ventana emergente "Introduce el código"
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//div[contains(text(),'Introduce el código')]")))

        # Obtener el código del SMS desde los logs de rendimiento
        code = retrieve_phone_code(self.driver)

        # Ingresar el código de confirmación
        code_input = self.driver.find_element(By.ID, 'code')
        code_input.clear()
        code_input.send_keys(code)

        # Hacer clic en el botón de confirmar
        confirm_button = self.driver.find_element(By.XPATH, "//button[contains(text(),'Confirmar')]")
        confirm_button.click()

        # Verificar que el número de teléfono ahora está mostrado en el formato +1 123 123 12 12
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(
            (By.XPATH, "//div[@class='np-text' and contains(text(), '+1 123 123 12 12')]")))

    def choose_payment_method(self):
        # Hacer clic en el botón de "Método de pago"
        self.driver.find_element(*self.payment_method_button).click()

        # Esperar a que el botón "Agregar tarjeta" esté visible
        add_card_button_locator = (By.XPATH, "//div[contains(text(), 'Agregar tarjeta')]")
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(add_card_button_locator)).click()

    def add_credit_card(self, card_number, card_code):
        try:
            # Asegúrate de que el campo de número de tarjeta sea clicable y visible
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.card_number_input)).send_keys(
                card_number)

            # Asegúrate de que el campo de código de la tarjeta sea clicable y visible
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.card_code_input)).send_keys(card_code)

            # Esperar a que el botón de "Agregar" esté clicable antes de hacer clic
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.confirm_card_button)).click()

        except TimeoutException:
            print("Uno de los elementos no estaba disponible o no era clicable")

            # revisar que campos no estaban disponibles
            if not self.driver.find_element(*self.card_number_input).is_displayed():
                print("Campo de número de tarjeta no disponible")
            if not self.driver.find_element(*self.card_code_input).is_displayed():
                print("Campo de código de tarjeta no disponible")
            if not self.driver.find_element(*self.confirm_card_button).is_displayed():
                print("Botón de confirmar no disponible")

    def write_message_to_driver(self, message):
        self.driver.find_element(*self.message_input).send_keys(message)

    def request_blanket_and_tissues(self):
        self.driver.find_element(*self.blanket_switch).click()

    def request_two_ice_creams(self):
        for _ in range(2):
            self.driver.find_element(*self.ice_cream_counter_plus).click()

    def find_taxi(self):
        self.driver.find_element(*self.find_taxi_button).click()

    def wait_for_driver_info(self):
        WebDriverWait(self.driver, 60).until(EC.visibility_of_element_located(self.driver_info_modal))


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
