import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from utilities import retrieve_phone_code

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
    ice_cream_count = (By.XPATH, "//*[@id='root']/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[3]/div/div[2]/div[1]/div/div[2]/div/div[2]")
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

    def get_selected_tariff(self):
        element = self.driver.find_element(*self.comfort_tariff_button)
        return element.text

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

    def get_displayed_phone_number(self):
        element = self.driver.find_element(*self.phone_input)
        return element.get_attribute('value')

    def choose_payment_method(self):
        element = self.wait.until(EC.element_to_be_clickable(self.payment_method_button))
        element.click()

    def add_credit_card(self, card_number, card_code):
        add_card_element = self.wait.until(EC.element_to_be_clickable(self.add_card_button))
        add_card_element.click()

        card_number_field = self.wait.until(EC.visibility_of_element_located(self.card_number_input))
        card_number_field.clear()
        card_number_field.send_keys(card_number)

        card_code_field = self.wait.until(EC.visibility_of_element_located(self.card_code_input))
        card_code_field.click()
        card_code_field.send_keys(card_code)

        # Hacer clic en cualquier parte de la página para que el botón "Agregar" se habilite
        self.driver.find_element(By.TAG_NAME, 'body').click()

        confirm_button = self.wait.until(EC.element_to_be_clickable(self.confirm_card_button))
        confirm_button.click()

        close_button = self.wait.until(EC.element_to_be_clickable(self.close_button))
        close_button.click()

    def is_card_added(self):
        self.driver.find_element(*self.close_button)
        return True

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

    def get_message_to_driver(self):
        element = self.driver.find_element(*self.message_input_field)
        return element.get_attribute('value')

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
        self.open_requirements_section()
        blanket_switch_element = self.wait.until(
            EC.element_to_be_clickable(self.blanket_switch)
        )
        blanket_switch_element.click()

    def is_blanket_selected(self):
        self.open_requirements_section()
        blanket_switch_element = self.driver.find_element(*self.blanket_switch)
        class_attr = blanket_switch_element.get_attribute('class')
        return class_attr

    def request_two_ice_creams(self):
        self.open_requirements_section()
        self.wait_for_overlay_to_disappear()
        ice_cream_plus = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.ice_cream_counter_plus)
        )
        for _ in range(2):
            ice_cream_plus.click()
            time.sleep(0.5)

    def get_ice_cream_count(self):
        element = self.wait.until(
            EC.visibility_of_element_located(self.ice_cream_count)
        )
        count_text = element.text
        return int(count_text)

    def wait_for_overlay_to_disappear(self):
        WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.CLASS_NAME, 'overlay')))

    def find_taxi(self):
        find_taxi_button_element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.find_taxi_button)
        )
        find_taxi_button_element.click()

    def is_search_started(self):
        self.wait.until(EC.text_to_be_present_in_element(
            (By.CLASS_NAME, 'order-header-title'), 'Buscar automóvil'
        ))
        return True

    def wait_for_driver_info(self):
        WebDriverWait(self.driver, 60).until(EC.visibility_of_element_located(self.driver_info_modal))
        time.sleep(5)

    def is_driver_info_displayed(self):
        self.wait.until(EC.visibility_of_element_located(self.driver_info_modal))
        return True