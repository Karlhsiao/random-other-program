from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import pandas as pd
import numpy as np
import time
import os

start_time = time.time()  # 記錄開始時 

# 設定 WebDriver（自動下載 ChromeDriver）
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # 不開啟瀏覽器視窗
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")  # 禁用 GPU 減少資源消耗
options.add_argument("--no-sandbox")  # 避免沙盒模式導致效能降低

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# 設定資料夾路徑
input_folder = "book_list"   # 替換成你的資料夾名稱
output_folder = "output_book_list" # 輸出結果的資料夾
os.makedirs(output_folder, exist_ok=True)  # 若無則創建資料夾

# 定義函數來使用 Selenium 查詢書籍資訊
def fetch_book_info(isbn):
    url = "https://isbn.ncl.edu.tw/NEW_ISBNNet/"
    driver.get(url)  # 開啟網站

    try:
       
        # 找到下拉選單元素
        dropdown = Select(driver.find_element(By.NAME, "FO_SearchField0"))  # 修改為網站的對應名稱

        # 方法 2：根據值 (`value` 屬性) 選擇
        dropdown.select_by_value("ISBN")
        
        search_box = driver.find_element(By.NAME, "FO_SearchValue0")
        
        search_box.send_keys(isbn)
        
        search_box.send_keys(Keys.RETURN)

        time.sleep(1)  # 等待網頁加載

        # 查找第一個搜尋結果的超連結
        book_link = driver.find_element(By.XPATH, "//a[contains(@href, 'main_DisplayRecord.php?&Pact=init&Pstart=1')]")
        book_url = book_link.get_attribute("href")
        book_link.click()  # 進入詳細頁面

        time.sleep(1)  # 等待詳細頁面加載

        # 擷取書名
        title_element = driver.find_element(By.XPATH, "//td[contains(@aria-label, '書名')]/following-sibling::td")
        title = title_element.text.strip() if title_element else "未知書名"
        #book_title = driver.find_element(By.XPATH, "//td[@aria-label='書名']/following-sibling::td").text print(book_title)  # 預期輸出：視覺溝通的法則

        # 擷取作者
        author_element = driver.find_element(By.XPATH, "//td[contains(@aria-label, '作者')]/following-sibling::td")
        author = author_element.text.strip() if author_element else "未知作者"

        # 擷取圖書類號
        category_element = driver.find_element(By.XPATH, "//td[contains(@aria-label, '圖書類號')]/following-sibling::td")
        category = category_element.text.strip() if category_element else "未知圖書類號"

        print("data get!", title, author, category)
        
        return title, author, category

    except Exception as e:
        print(f"查詢 ISBN {isbn} 時發生錯誤：{e}")
        return "未知書名", "未知作者", "未知圖書類號"

for file_index, filename in enumerate(os.listdir(input_folder), start=1):
    if filename.endswith(".csv"):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, f"{filename}.csv")

        # 讀取 CSV
        df = pd.read_csv(input_path, dtype={"isbn": str, "作者": str, "書名": str, "分類": str})
        
        # 逐行處理 CSV
        for index, row in df.iterrows():
            if pd.isna(row["書名"]) or row["書名"] == "未知書名":
                title, author, category = fetch_book_info(str(row["isbn"]).strip())
                df.at[index, "書名"] = str(title)  
                df.at[index, "作者"] = str(author)
                
                try:
                    df.at[index, "分類"] = float(category) if category.strip() else np.nan
                except ValueError:
                    df.at[index, "分類"] = category.strip() if category.strip() else "未知分類"
                                    
                time.sleep(1)  # 避免過快請求

        # 存回 CSV 檔案
        df.to_csv(output_path, index=False, encoding="utf-8-sig")

        print(f"處理完成！輸出結果已儲存為 {output_path}")

# 關閉瀏覽器
driver.quit()
print("所有檔案處理完成！")

end_time = time.time()  # 記錄結束時間
elapsed_time = end_time - start_time  # 計算總耗時
print(f"總執行時間: {elapsed_time:.2f} 秒")