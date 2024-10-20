from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import DesiredCapabilities

def create_driver_with_capabilities():
    from selenium.webdriver.chrome.options import Options

    capabilities = DesiredCapabilities.CHROME.copy()
    capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
    chrome_options = Options()
    chrome_options.set_capability("goog:loggingPrefs", {'performance': 'ALL'})
    service = Service()
    return webdriver.Chrome(service=service, options=chrome_options)

# Función retrieve_phone_code
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
