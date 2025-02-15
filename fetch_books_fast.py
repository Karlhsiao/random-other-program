from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoAlertPresentException, UnexpectedAlertPresentException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import pandas as pd
import numpy as np
import time
import os
from multiprocessing import Pool, cpu_count
import re

start_time = time.time()  # 記錄開始時

# 設定資料夾路徑
input_folder = "book_list"
output_folder = "output_book_list"
os.makedirs(output_folder, exist_ok=True)

def init_driver(unique_id):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument(f"--user-data-dir=/tmp/chrome_user_{unique_id}")
    options.page_load_strategy = "eager"
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def fetch_book_info(isbn, unique_id):
    # 忽略套書
    isbn_cleaned = re.sub(r"\(套書\)", "", isbn).strip()

    driver = init_driver(unique_id)
    url = "https://isbn.ncl.edu.tw/NEW_ISBNNet/"
    driver.get(url)

    try:
        dropdown = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.NAME, "FO_SearchField0"))
        )
        Select(dropdown).select_by_value("ISBN")

        search_box = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.NAME, "FO_SearchValue0"))
        )
        search_box.send_keys(isbn_cleaned)
        search_box.send_keys(Keys.RETURN)
        
        '''
        try:
            WebDriverWait(driver, 2).until(EC.alert_is_present())
            alert = driver.switch_to.alert
            print(f"ISBN {isbn_cleaned} 找不到資料，已忽略。")
            alert.accept()
            driver.quit()
            return "未知書名", "未知作者", "未知圖書類號"
        except (NoAlertPresentException, UnexpectedAlertPresentException):
            pass
        '''
        
        book_link = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'main_DisplayRecord.php?&Pact=init&Pstart=1')]"))
        )
        book_link.click()

        title_element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//td[contains(@aria-label, '書名')]/following-sibling::td"))
        )
        title = title_element.text.strip() if title_element else "未知書名"

        author_element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//td[contains(@aria-label, '作者')]/following-sibling::td"))
        )
        author = author_element.text.strip() if author_element else "未知作者"

        category_element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//td[contains(@aria-label, '圖書類號')]/following-sibling::td"))
        )
        category = category_element.text.strip() if category_element else "未知圖書類號"

        print("data get!", title, author, category)

        # 檢查並處理「套書」
        if "套書" in title or "套" in title:
            title = f"{title} (套書)"

        driver.quit()
        return title, author, category

    except Exception as e:
        print(f"查詢 ISBN {isbn_cleaned} 時發生錯誤：{e}")
        driver.quit()
        return "未知書名", "未知作者", "未知圖書類號"

def process_file(args):
    filename, unique_id = args
    input_path = os.path.join(input_folder, filename)
    output_path = os.path.join(output_folder, f"{filename}")

    df = pd.read_csv(input_path, dtype={"isbn": str, "作者": str, "書名": str, "分類": str})

    save_interval = 5  # 每 5 筆儲存一次
    counter = 0

    for index, row in df.iterrows():
        if pd.isna(row["書名"]) or row["書名"] == "未知書名":
            title, author, category = fetch_book_info(str(row["isbn"]).strip(), unique_id)
            df.at[index, "書名"] = str(title)
            df.at[index, "作者"] = str(author)

            try:
                df.at[index, "分類"] = float(category) if category.strip() else np.nan
            except ValueError:
                df.at[index, "分類"] = category.strip() if category.strip() else "未知分類"

            counter += 1

            # 定期儲存
            if counter % save_interval == 0:
                df.to_csv(output_path, index=False, encoding="utf-8-sig")
                print(f"已儲存中間結果至 {output_path}")

    df.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(f"處理完成！輸出結果已儲存為 {output_path}")

if __name__ == "__main__":
    files = [f for f in os.listdir(input_folder) if f.endswith(".csv")]
    with Pool(cpu_count()) as pool:
        pool.map(process_file, [(file, i) for i, file in enumerate(files)])

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"所有檔案處理完成！總執行時間: {elapsed_time:.2f} 秒")