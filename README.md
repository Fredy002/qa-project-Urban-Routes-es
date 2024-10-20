# Urban Routes Automation

Automate the process of ordering a taxi on the **Urban Routes** platform using **Selenium WebDriver**. This project simulates user interactions with the website, from setting up the route to confirming the taxi request, including optional features like adding special requests.

## Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Tests](#running-the-tests)
- [Features](#features)
- [Implementation Details](#implementation-details)
- [Additional Notes](#additional-notes)
- [Contact](#contact)

## Overview

This project provides an automated testing suite for the **Urban Routes** web application. It uses **Selenium WebDriver** to perform end-to-end testing of the taxi ordering process, ensuring that all functionalities work as expected.

## Project Structure

- **`data.py`**: Contains input data and configuration variables used throughout the tests.
- **`main.py`**: The main test script containing the `TestUrbanRoutes` class with all test cases.
- **`urban_routes_page.py`**: Implements the `UrbanRoutesPage` class, encapsulating all page interactions.
- **`utilities.py`**: Includes utility functions such as `retrieve_phone_code` for additional functionalities.

## Requirements

- **Python 3.7+**
- **Selenium WebDriver** (`selenium`)
- **ChromeDriver** (compatible with your installed version of Google Chrome)
- **pytest** (for running the tests)

### Python Libraries

Install the required Python libraries using pip:

```bash
pip install selenium pytest
```

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/Fredy002/urban-routes-automation.git
   cd urban-routes-automation
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

   *If a `requirements.txt` file is not provided, you can install the necessary packages as shown in the [Python Libraries](#python-libraries) section.*

3. **Download ChromeDriver**:

   - Download **ChromeDriver** from the [official website](https://chromedriver.chromium.org/downloads) matching your installed version of Google Chrome.
   - Place the `chromedriver` executable in a directory included in your system's `PATH`, or specify its location when initializing the WebDriver in the code.

## Configuration

Update the `data.py` file with any necessary configurations or input data. The default values are:

```python
# data.py

urban_routes_url = 'https://cnt-63745af8-6330-47b4-89f7-1161024645a6.containerhub.tripleten-services.com?lng=es'
address_from = 'East 2nd Street, 601'
address_to = '1300 1st St'
phone_number = '+1 123 123 12 12'
card_number = '1234 5678 9100'
card_code = '111'
message_for_driver = 'Camino al museo'  # (Heading to the museum)
```

## Running the Tests

You can run the tests using **pytest** or directly from the script.

### Using pytest

```bash
pytest main.py
```

### Directly from the Script

If you prefer, you can run the script directly:

```bash
python main.py
```

### Notes

- Ensure that the **ChromeDriver** is properly installed and accessible.
- Make sure all dependencies are installed and up-to-date.
- Adjust the waiting times or selectors if the web application has changed.

## Features

The automated tests cover the following features:

- **Setting Up the Route**: Inputs the starting and destination addresses.
- **Selecting Transportation Mode**: Chooses the "Personal" mode.
- **Requesting a Taxi**: Initiates a taxi request.
- **Selecting Tariff**: Chooses the "Comfort" tariff.
- **Entering Phone Number**: Inputs the phone number and retrieves the confirmation code automatically.
- **Adding Payment Method**: Inputs credit card details for payment.
- **Sending Message to Driver**: Writes a custom message to the driver.
- **Adding Special Requests**: Requests a blanket, tissues, and two ice creams.
- **Confirming Taxi Search**: Initiates the search for a taxi and waits for driver information.

## Implementation Details

### Classes and Methods

#### `UrbanRoutesPage` (in `urban_routes_page.py`)

Encapsulates all interactions with the Urban Routes web page.

Key methods include:

- **`set_route(from_address, to_address)`**: Sets the starting and destination addresses.
- **`select_personal_mode()`**: Selects the "Personal" transportation mode.
- **`click_taxi_icon()`**: Clicks the taxi icon to select the taxi service.
- **`request_taxi()`**: Clicks the button to request a taxi.
- **`select_comfort_tariff()`**: Chooses the "Comfort" tariff option.
- **`enter_phone_number(phone_number)`**: Inputs the phone number and handles the confirmation code retrieval.
- **`add_credit_card(card_number, card_code)`**: Inputs credit card information.
- **`write_message_to_driver(message)`**: Sends a custom message to the driver.
- **`request_blanket_and_tissues()`**: Requests additional items like blanket and tissues.
- **`request_two_ice_creams()`**: Adds two ice creams to the order.
- **`find_taxi()`**: Initiates the search for a taxi.
- **`wait_for_driver_info()`**: Waits until the driver information is displayed.

#### `TestUrbanRoutes` (in `main.py`)

Contains the test cases for the Urban Routes automation.

Key test methods include:

- **`test_set_route()`**: Verifies that the starting and destination addresses are set correctly.
- **`test_select_personal_mode()`**: Checks if the "Personal" transportation mode is selected.
- **`test_click_taxi_icon()`**: Verifies the selection of the taxi service.
- **`test_request_taxi()`**: Confirms that the taxi request process is initiated.
- **`test_select_comfort_tariff()`**: Checks if the "Comfort" tariff is selected.
- **`test_enter_phone_number()`**: Validates phone number entry and confirmation code handling.
- **`test_add_credit_card()`**: Verifies that credit card details are added successfully.
- **`test_write_message_to_driver()`**: Checks if the message to the driver is set.
- **`test_request_blanket_and_tissues()`**: Ensures that special requests are added.
- **`test_request_two_ice_creams()`**: Verifies the addition of two ice creams.
- **`test_find_taxi()`**: Confirms that the taxi search is initiated.
- **`test_wait_for_driver_info()`**: Checks if the driver information is displayed after searching.

### Utilities

- **`retrieve_phone_code(driver)`** (in `utilities.py`): Intercepts and retrieves the phone confirmation code from browser logs.

## Additional Notes

- **Browser Compatibility**: The script is designed for Google Chrome. Ensure that the ChromeDriver version matches your browser version.
- **Dynamic Elements**: The script uses explicit waits to handle dynamic elements and loading times.
- **JavaScript Execution**: In some cases, JavaScript is used to interact with elements that are not easily clickable using standard Selenium methods.
- **Error Handling**: The script includes exception handling to manage potential issues during execution.
- **Modular Design**: The project follows a modular design, separating concerns into different files and classes for better maintainability.

## Contact

- **GitHub**: [Fredy002](https://github.com/Fredy002)
- **LinkedIn**: [Fredy Antonio Almeyda Alania](https://www.linkedin.com/in/fredy-antonio-almeyda-alania/)

Feel free to explore the code, raise issues, or contribute to the project. If you have any questions or need assistance, don't hesitate to reach out.
