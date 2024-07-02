from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time

# Replace 'path_to_chromedriver' with the path to your ChromeDriver executable
chrome_driver_path = './chromedriver-win64/chromedriver.exe'

# Canvas login page
canvas_login_url = ''


def ask_login_url():
    return input('Please enter the login URL of Canvas: ')


def set_login_url():
    global canvas_login_url
    canvas_login_url = ask_login_url()


def get_login_url():
    global canvas_login_url
    if not canvas_login_url:
        set_login_url()
    return canvas_login_url


canvas_login_url = ask_login_url()
# Base module URL

base_module_url = ''


def ask_base_url():
    return input('Please enter the base URL of the module or week: ')


def set_base_url():
    global base_module_url
    base_module_url = ask_base_url()


def get_base_url():
    global base_module_url
    if not base_module_url:
        set_base_url()
    return base_module_url


base_module_url = get_base_url()

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument('--start-maximized')
chrome_options.binary_location = 'C:\Program Files\Google\Chrome\Application\chrome.exe'

# Create a WebDriver instance
service = ChromeService(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# Log in to Canvas (manual login step or use automation if credentials are provided)
driver.get('https://www.york.ac.uk/eldt/canvas/canvas_landing_page.html')
time.sleep(20)  # Adjust sleep time for manual login

# Navigate to the base module URL
driver.get(base_module_url)
time.sleep(5)


# Function to add a bookmark
def add_bookmark(url, title):
    script = f"""
    (function() {{
        var bookmarkBar = document.getElementById('bookmarks-bar');
        if (!bookmarkBar) {{
            bookmarkBar = document.createElement('div');
            bookmarkBar.id = 'bookmarks-bar';
            bookmarkBar.style.position = 'fixed';
            bookmarkBar.style.top = '0';
            bookmarkBar.style.left = '0';
            bookmarkBar.style.width = '100%';
            bookmarkBar.style.backgroundColor = '#ffffff';
            bookmarkBar.style.zIndex = '10000';
            document.body.appendChild(bookmarkBar);
        }}
        var bookmark = document.createElement('a');
        bookmark.href = '{url}';
        bookmark.innerText = '{title}';
        bookmark.style.display = 'block';
        bookmark.style.margin = '5px';
        bookmarkBar.appendChild(bookmark);
    }})();
    """
    driver.execute_script(script)


# Expand all module items
expand_buttons = driver.find_elements(By.CSS_SELECTOR, '.ig-header-expand')
for button in expand_buttons:
    button.click()
    time.sleep(1)

# Get all module items
module_items = driver.find_elements(
    By.CSS_SELECTOR, '.item-group-condensed .ig-row .ig-title a')

# Create bookmarks for each module item
for item in module_items:
    item_title = item.text
    item_url = item.get_attribute('href')
    add_bookmark(item_url, item_title)
    time.sleep(1)

# Close the WebDriver
driver.quit()
