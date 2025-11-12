"""Quick test to verify the expand all button locator works"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Start browser
driver = webdriver.Chrome()
driver.get("http://localhost:8080/login")

# Login
driver.find_element(By.XPATH, "//input[@type='email']").send_keys("contractor1@gmail.com")
driver.find_element(By.XPATH, "//input[@type='password']").send_keys("Test@123")
driver.find_element(By.XPATH, "//button[normalize-space(text())='Login']").click()

time.sleep(2)

# Navigate to create RFI
driver.get("http://localhost:8080/welcome")
time.sleep(1)

# Click Create RFI button
driver.find_element(By.XPATH, "//button[normalize-space()='Create RFI']").click()
time.sleep(2)

# Fill minimal form to get to inspection checklist
# ... (you would need to fill the form here)

# Try to find the expand all button with different locators
print("\n=== Testing Locators ===")

locators = [
    ("By SVG class", "//button[.//svg[contains(@class, 'lucide-square-plus')]]"),
    ("By button class + SVG", "//button[@class='button button--variant_ghost button--size_xs as_end p_0']//svg[contains(@class, 'lucide-square-plus')]"),
    ("By text + sibling", "//p[contains(text(), 'Answer all the questions')]/following-sibling::button[.//svg[contains(@class, 'lucide-square-plus')]]"),
    ("By parent div text", "//div[.//p[contains(text(), 'Answer all the questions')]]//button[.//svg[contains(@class, 'lucide-square-plus')]]"),
]

for name, xpath in locators:
    try:
        elements = driver.find_elements(By.XPATH, xpath)
        print(f"✓ {name}: Found {len(elements)} element(s)")
        if elements:
            print(f"  - Visible: {elements[0].is_displayed()}")
            print(f"  - Enabled: {elements[0].is_enabled()}")
    except Exception as e:
        print(f"✗ {name}: {str(e)}")

print("\n=== Checking page structure ===")
# Check if we're on the inspection checklist page
try:
    page_2 = driver.find_elements(By.XPATH, "//p[contains(text(), 'Page 2/2')]")
    print(f"Page 2/2 indicator: {'Found' if page_2 else 'Not found'}")
    
    collapsibles = driver.find_elements(By.CSS_SELECTOR, "div[data-scope='collapsible']")
    print(f"Collapsible sections: {len(collapsibles)}")
    
    closed = driver.find_elements(By.XPATH, "//div[@data-scope='collapsible'][@data-state='closed']")
    print(f"Closed sections: {len(closed)}")
    
    open_sections = driver.find_elements(By.XPATH, "//div[@data-scope='collapsible'][@data-state='open']")
    print(f"Open sections: {len(open_sections)}")
except Exception as e:
    print(f"Error checking structure: {e}")

input("\n\nPress Enter to close browser...")
driver.quit()
