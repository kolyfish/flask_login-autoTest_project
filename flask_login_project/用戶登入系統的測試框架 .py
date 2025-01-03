from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# 設定 WebDriver
driver = webdriver.Chrome()

try:
    # 開啟登入頁面
    driver.get("http://localhost:8000/login")

    # 輸入用戶名和密碼
    username_input = driver.find_element(By.ID, "username")
    password_input = driver.find_element(By.ID, "password")
    login_button = driver.find_element(By.ID, "login-btn")

    username_input.send_keys("testuser")
    password_input.send_keys("password123")
    login_button.click()

    # 驗證登入結果
    time.sleep(2)
    success_message = driver.find_element(By.ID, "success-message")
    assert "歡迎 testuser" in success_message.text
finally:
    # 關閉瀏覽器
    driver.quit()
