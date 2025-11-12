"""
Debug script to find the expand all button on the inspection checklist page.
Run this after manually navigating to the inspection checklist page (Page 2/2).
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def debug_expand_button():
    print("\n" + "="*60)
    print("EXPAND BUTTON DEBUG SCRIPT")
    print("="*60)
    
    # Start browser
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    
    try:
        # Login
        print("\n[1] Logging in...")
        driver.get("http://localhost:8080/login")
        driver.find_element(By.XPATH, "//input[@type='email']").send_keys("contractor1@gmail.com")
        driver.find_element(By.XPATH, "//input[@type='password']").send_keys("Test@123")
        driver.find_element(By.XPATH, "//button[normalize-space(text())='Login']").click()
        time.sleep(2)
        
        # Navigate to create RFI
        print("[2] Navigating to Create RFI...")
        driver.get("http://localhost:8080/welcome")
        time.sleep(1)
        
        # Click Create RFI button
        print("[3] Opening Create RFI form...")
        driver.find_element(By.XPATH, "//button[normalize-space()='Create RFI']").click()
        time.sleep(2)
        
        # Quick fill (you'll need to adapt this to your form)
        print("[4] Please manually fill the form and click Proceed to get to Page 2/2")
        print("    (Or modify this script to automate form filling)")
        input("    Press Enter when you're on Page 2/2 (Inspection Checklist)...")
        
        # Now debug the page structure
        print("\n" + "="*60)
        print("PAGE STRUCTURE ANALYSIS")
        print("="*60)
        
        # Check current page
        try:
            page_indicator = driver.find_element(By.XPATH, "//p[contains(text(), 'Page')]")
            print(f"\n✓ Current page: {page_indicator.text}")
        except:
            print("\n✗ Could not find page indicator")
        
        # Check collapsible sections
        collapsibles = driver.find_elements(By.CSS_SELECTOR, "div[data-scope='collapsible']")
        print(f"✓ Total collapsible sections: {len(collapsibles)}")
        
        closed = driver.find_elements(By.XPATH, "//div[@data-scope='collapsible'][@data-state='closed']")
        print(f"  - Closed sections: {len(closed)}")
        
        open_sections = driver.find_elements(By.XPATH, "//div[@data-scope='collapsible'][@data-state='open']")
        print(f"  - Open sections: {len(open_sections)}")
        
        # Check for the expand button with different locators
        print("\n" + "="*60)
        print("TESTING LOCATORS FOR EXPAND BUTTON")
        print("="*60)
        
        locators = [
            ("1. By 'Answer all' text", By.XPATH, "//p[contains(text(), 'Answer all the questions')]"),
            ("2. By square-plus SVG", By.XPATH, "//svg[contains(@class, 'lucide-square-plus')]"),
            ("3. Text + sibling button", By.XPATH, "//p[contains(text(), 'Answer all the questions')]/following-sibling::button"),
            ("4. Parent div + button", By.XPATH, "//div[.//p[contains(text(), 'Answer all the questions')]]//button"),
            ("5. SVG parent button", By.XPATH, "//svg[contains(@class, 'lucide-square-plus')]/parent::button"),
            ("6. Ghost variant button", By.XPATH, "//button[contains(@class, 'button--variant_ghost')]"),
            ("7. Ghost + square-plus", By.XPATH, "//button[contains(@class, 'button--variant_ghost')]//svg[contains(@class, 'lucide-square-plus')]/parent::button"),
        ]
        
        successful_locator = None
        successful_element = None
        
        for name, by_type, locator in locators:
            try:
                elements = driver.find_elements(by_type, locator)
                print(f"\n{name}:")
                print(f"  Found: {len(elements)} element(s)")
                
                if elements:
                    for idx, elem in enumerate(elements):
                        visible = elem.is_displayed()
                        enabled = elem.is_enabled()
                        print(f"  Element {idx+1}: Visible={visible}, Enabled={enabled}")
                        
                        if visible and enabled and not successful_locator:
                            successful_locator = name
                            successful_element = elem
                            print(f"  ✓✓✓ THIS ONE LOOKS GOOD! ✓✓✓")
            except Exception as e:
                print(f"\n{name}:")
                print(f"  Error: {str(e)}")
        
        # Try to click the successful locator
        if successful_locator and successful_element:
            print("\n" + "="*60)
            print(f"ATTEMPTING TO CLICK: {successful_locator}")
            print("="*60)
            
            try:
                # Scroll to element
                driver.execute_script("arguments[0].scrollIntoView({block:'center'});", successful_element)
                time.sleep(0.5)
                
                # Highlight element
                driver.execute_script("arguments[0].style.border='3px solid red'", successful_element)
                time.sleep(0.5)
                
                # Try click
                successful_element.click()
                print("✓ Clicked using regular click()")
                time.sleep(1)
                
                # Check results
                open_after = driver.find_elements(By.XPATH, "//div[@data-scope='collapsible'][@data-state='open']")
                print(f"✓ Open sections after click: {len(open_after)}")
                
                if len(open_after) > len(open_sections):
                    print("\n🎉 SUCCESS! Button worked!")
                else:
                    print("\n⚠️ Button clicked but sections didn't expand")
                    
            except Exception as e:
                print(f"✗ Failed to click: {str(e)}")
        else:
            print("\n" + "="*60)
            print("❌ NO SUITABLE BUTTON FOUND")
            print("="*60)
            print("\nTaking screenshot for manual inspection...")
            driver.save_screenshot("expand_button_debug.png")
            print("Screenshot saved as: expand_button_debug.png")
        
        # Keep browser open for inspection
        input("\n\nPress Enter to close browser...")
        
    finally:
        driver.quit()

if __name__ == "__main__":
    debug_expand_button()
