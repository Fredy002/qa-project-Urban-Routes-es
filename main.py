import data
from urban_routes_page import UrbanRoutesPage
from utilities import create_driver_with_capabilities

class TestUrbanRoutes:

    driver = None
    routes_page = None

    @classmethod
    def setup_class(cls):
        cls.driver = create_driver_with_capabilities()
        cls.driver.get(data.urban_routes_url)
        cls.routes_page = UrbanRoutesPage(cls.driver)

    def test_set_route(self):
        address_from = data.address_from
        address_to = data.address_to
        self.routes_page.set_route(address_from, address_to)
        assert self.routes_page.get_from() == address_from
        assert self.routes_page.get_to() == address_to

    def test_select_personal_mode(self):
        self.routes_page.select_personal_mode()

    def test_click_taxi_icon(self):
        self.routes_page.click_taxi_icon()

    def test_request_taxi(self):
        self.routes_page.request_taxi()

    def test_select_comfort_tariff(self):
        self.routes_page.select_comfort_tariff()
        selected_tariff = self.routes_page.get_selected_tariff()
        assert selected_tariff == 'Comfort'

    def test_enter_phone_number(self):
        self.routes_page.click_phone_number_button()
        self.routes_page.enter_phone_number(data.phone_number)
        # Formatear el número como se muestra en la interfaz
        formatted_phone_number = '+1 123 123 12 12'
        displayed_phone_number = self.routes_page.get_displayed_phone_number()
        assert displayed_phone_number == formatted_phone_number

    def test_add_credit_card(self):
        self.routes_page.choose_payment_method()
        self.routes_page.add_credit_card(data.card_number, data.card_code)
        card_added = self.routes_page.is_card_added()
        assert card_added

    def test_write_message_to_driver(self):
        self.routes_page.write_message_to_driver(data.message_for_driver)
        message_set = self.routes_page.get_message_to_driver()
        assert message_set == data.message_for_driver

    def test_request_blanket_and_tissues(self):
        self.routes_page.request_blanket_and_tissues()
        blanket_selected = self.routes_page.is_blanket_selected()
        assert blanket_selected

    def test_request_two_ice_creams(self):
        self.routes_page.request_two_ice_creams()
        ice_cream_count = self.routes_page.get_ice_cream_count()
        assert ice_cream_count == 2

    def test_find_taxi(self):
        self.routes_page.find_taxi()
        # Verificar que la búsqueda de taxi ha comenzado
        search_started = self.routes_page.is_search_started()
        assert search_started

    def test_wait_for_driver_info(self):
        self.routes_page.wait_for_driver_info()
        driver_info_displayed = self.routes_page.is_driver_info_displayed()
        assert driver_info_displayed

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
