from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
import time
import re


dim = 'https://app.destinyitemmanager.com/'

user_name = "Helvemix"

# 输入次数
# times = int(input('请输入任务次数:'))
times = 100
max_wait_time = 5



# 实例化并配置参数
chrome_options = ChromeOptions()
# 启动开发者模式(关闭chrome控制) & 关闭日志输出
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation'])
chrome_options.add_experimental_option("useAutomationExtension", 'False')
# 调用用户配置文件
chrome_options.add_argument("--user-data-dir=C:/Users/" + user_name +"/AppData/Local/Google/Chrome/User Data")
# 最大化窗口
chrome_options.add_argument('--start-maximized')

# 设置加载策略为eager
chrome_options.page_load_strategy = 'normal'

# 启动浏览器
# service=ChromeService(ChromeDriverManager().install())
# 创建一个Service对象
driver = webdriver.Chrome(executable_path='F:/All_Project/cod/chromedriver.exe', options=chrome_options)

# 设置隐性等待时间
max_wait_time = 10




# 打开网页
def open_collect():
    time.sleep(max_wait_time)
    driver.get(dim)
    print("打开dim")
    time.sleep(max_wait_time)
    driver.find_element(By.XPATH,'/html/body/div[1]/div[1]/div/div[1]/div[1]/div[1]/div[1]/div[1]/button').click()
    print("点击当前人物")
    time.sleep(max_wait_time)
    driver.find_element(By.CLASS_NAME,'iiYyReH2').click()
    print("开启收集模式")
    time.sleep(max_wait_time)

def get_item():
    driver.find_element(By.XPATH,'/html/body/div[1]/div[1]/div/header/div/div[2]/div/button').click()
    print("刷新")
    time.sleep(max_wait_time)
    driver.find_element(By.XPATH,'/html/body/div[1]/div[1]/div/div[1]/div[1]/div[1]/div[5]/div[2]/div[1]/button').click()
    print("获取")
    time.sleep(max_wait_time)

def item_num():
    itemnum=driver.find_element(By.CLASS_NAME,'zNYTPZxC').text
    print(itemnum)
    return itemnum

def tell():
    if allnumber == 21:
        print('已完成')
        driver.quit()

if __name__ == '__main__':
    open_collect()
    for i in range(times):
        get_item()
        item_num()
        match = re.search(r'\d+', item_num())
        allnumber = int(match.group(0))  # 将匹配到的字符串转换为整数
        print(allnumber)
        print('done')
        print(i)
        time.sleep(600)
