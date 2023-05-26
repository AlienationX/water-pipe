from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common import exceptions

import time
import csv

# 创建保存文件
f = open('boss_数据仓库_selenium.csv', mode='w', encoding='utf-8-sig', newline='')
csv_writer = csv.DictWriter(f, fieldnames=["职位名称",
                                           "地区",
                                           "薪水",
                                           "标签",
                                           "能力要求",
                                           "公司名字",
                                           "公司介绍",
                                           "福利待遇",
                                           "职位描述",
                                           "企业类型",
                                           "工作地址",
                                           "详情链接"])
csv_writer.writeheader()  # 写入表头

options = ChromeOptions()
# 反检测
options.add_experimental_option("excludeSwitches", ["enable-automation"])
driver = Chrome(options=options)

# 设置隐性等待时间为10s
# driver.implicitly_wait(20)

driver.get('https://www.zhipin.com/web/geek/job?query=%E6%95%B0%E6%8D%AE%E4%BB%93%E5%BA%93&city=101010100')

for i in range(1, 10):
    k = 0  # 用来设置每页爬取的数量，每页有30条数据，因全部爬取用selenium较慢，为测试效果每页只爬取5条
    
    # 滚动条滚到底部
    driver.execute_script('document.documentElement.scrollTop = document.documentElement.scrollHeight')
    
    # li_lists = driver.find_elements(By.CSS_SELECTOR, '.job-card-wrapper')
    li_lists = WebDriverWait(driver, timeout=60).until(lambda d: d.find_elements(By.CSS_SELECTOR, '.job-card-wrapper'))
    print(type(li_lists))
    print(i, "当前页面job_list:", len(li_lists))

    for li in li_lists:
        # job_name = li.find_element(By.CLASS_NAME, 'job-name').text
        job_name = WebDriverWait(li, timeout=60).until(lambda d: d.find_element(By.CLASS_NAME, 'job-name')).text

        job_area = li.find_element(By.CLASS_NAME, 'job-area').text
        salary = li.find_element(By.CLASS_NAME, 'salary').text
        job_tag = li.find_element(By.CSS_SELECTOR, '.job-card-wrapper .job-card-left .tag-list').text.replace('\n', ',')
        job_ability = li.find_element(By.XPATH, './div[2]/ul').text
        company_name = li.find_element(By.CLASS_NAME, 'company-name').text
        welfare = li.find_element(By.CLASS_NAME, 'info-desc').text
        link = li.find_element(By.CLASS_NAME, 'job-card-left').get_attribute('href')
        
        # 点击详情页
        detail_page = li.find_element(By.CSS_SELECTOR, '.job-card-left')
        driver.execute_script('arguments[0].click()', detail_page)
        
        # 窗口切换到最新打开的页面
        driver.switch_to.window(driver.window_handles[-1])

        # job_des = driver.find_element(By.XPATH, '//*[@id="main"]/div[3]/div/div[2]/div[1]/div[2]').text
        job_des = WebDriverWait(driver, timeout=60).until(lambda d: d.find_element(By.XPATH, '//*[@id="main"]/div[3]/div/div[2]/div[1]/div[2]')).text
        
        try:  # 有的公司没有公司介绍
            company_info = driver.find_element(By.CSS_SELECTOR, '.job-body-wrapper .company-info-box .fold-text').text.replace('\n', ' ')
        except exceptions.NoSuchElementException:
            company_info = ''
            
        try:
            company_type = driver.find_element(By.CLASS_NAME, 'company-type').text.replace('企业类型\n', '')
        except exceptions.NoSuchElementException:
            company_type = ''
            
        address = driver.find_element(By.CLASS_NAME, 'location-address').text
        
        data = {
            "职位名称": job_name,
            "地区": job_area,
            "薪水": salary,
            "标签": job_tag,
            "能力要求": job_ability,
            "公司名字": company_name,
            "公司介绍": company_info,
            "福利待遇": welfare,
            "职位描述": job_des,
            "企业类型": company_type,
            "工作地址": address,
            "详情链接": link
        }
        # 写入数据
        csv_writer.writerow(data)
        k = k + 1
        print(i, k, data)
        driver.close()
        # 窗口切换到第一个页面
        driver.switch_to.window(driver.window_handles[0])

    time.sleep(2)
    # 点击下一页按钮
    next_button = WebDriverWait(driver, timeout=60).until(lambda d: d.find_element(By.XPATH, '//*[@class="options-pages"]/a[10]'))
    driver.execute_script('arguments[0].click()', next_button)
    
driver.close()
driver.quit()
