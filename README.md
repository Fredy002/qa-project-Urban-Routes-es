# Urban Routes Automation

This project automates the process of ordering a taxi on the **Urban Routes** platform. It uses **Selenium** to automate interactions with the website, from setting routes to confirming the taxi request.

## Requirements

- **Python 3.7+**
- **Selenium WebDriver** (for browser automation)
- **ChromeDriver** (to interact with Google Chrome)

### Python Libraries

- **selenium**
  ```bash
  pip install selenium
  ```

## Environment Setup

1. **Install dependencies**:
   Make sure you have installed the necessary dependencies, such as Selenium.
   ```bash
   pip install selenium
   ```

2. **Download ChromeDriver**:
   You need **ChromeDriver** to match your installed version of Google Chrome. You can download it from [here](https://sites.google.com/a/chromium.org/chromedriver/).

   Ensure the `chromedriver` is accessible from your `PATH` or specify its location in the code if necessary.

## Project Structure

### Test URL

The project interacts with the following **Urban Routes** URL:

```python
urban_routes_url = 'https://cnt-63745af8-6330-47b4-89f7-1161024645a6.containerhub.tripleten-services.com?lng=es'
```

### Input Data

These are the input values used for the automated tests:

- **Starting address**: `East 2nd Street, 601`
- **Destination address**: `1300 1st St`
- **Phone number**: `+1 123 123 12 12`
- **Card number**: `1234 5678 9100`
- **Card code**: `111`
- **Message for driver**: `Camino al museo` (Heading to the museum)

### Main Classes and Methods

- **`UrbanRoutesPage`**:
  This class contains methods to interact with the web page, such as:
  
  - **`set_route`**: Set the trip’s starting and destination addresses.
  - **`select_personal_mode`**: Select the "Personal" mode of transportation.
  - **`request_taxi`**: Place a taxi request on the platform.
  - **`add_credit_card`**: Add credit card details for payment.
  - **`write_message_to_driver`**: Send a message to the driver.
  - **`request_blanket_and_tissues`**: Request blankets and tissues.
  - **`request_two_ice_creams`**: Add two ice creams to the order.

- **`TestUrbanRoutes`**:
  This class contains the automated tests. The main methods include:
  
  - **`test_set_route`**: Verifies that the route (from and to addresses) is set correctly.
  - **`test_complete_taxi_order`**: A full test that performs the entire process of ordering a taxi, from start to driver confirmation.

## Running the Tests

1. **Configure the WebDriver**:
   The project is set up to use Google Chrome as the default browser. Make sure you have **ChromeDriver** installed and matching your browser version.

2. **Execution**:

   You can run the tests using `pytest` or directly from the script:

   ```bash
   pytest main.py
   ```

   Alternatively, you can execute the script directly if you are using **PyCharm** or another IDE.

3. **Expected behavior**:
   - The script will open the **Urban Routes** page, enter the starting and destination addresses, select the "Personal" transportation mode, enter the phone number and credit card details, send a message to the driver, and finally request a taxi.
   - At the end of the process, the test will display the driver details if successful.

## Additional Notes

- The script retrieves the phone confirmation code from browser logs using the **`retrieve_phone_code`** method.
- **JavaScript** is used to click on certain elements that might be hidden or covered by other layers.
- The functionality automates the full taxi request process, including adding optional details like blankets and ice creams.
  
## Contact

- **GitHub:** [Fredy002](https://github.com/Fredy002)
- **LinkedIn:** [Fredy Antonio Almeyda Alania](https://www.linkedin.com/in/fredy-antonio-almeyda-alania/)

Feel free to explore the code to understand how the API functionalities are implemented and maybe tweak some values to see how the application behaves. Happy coding!