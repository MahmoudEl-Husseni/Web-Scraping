import os 
import pandas as pd
from config import *

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC


# utils functions

# Wait for element to be loaded
def wait_for_element_xpath(driver, xpath, wait_time=10):
    return WebDriverWait(driver, wait_time).until(EC.presence_of_element_located((By.XPATH, xpath)))

def wait_for_element_id(driver, id, wait_time=5):
    return WebDriverWait(driver, wait_time).until(EC.presence_of_element_located((By.ID, id)))

def wait_for_element_class(driver, class_name, wait_time=5):
    return WebDriverWait(driver, wait_time).until(EC.presence_of_element_located((By.CLASS_NAME, class_name)))

def wait_for_click_xpath(driver, xpath, wait_time=10):
    return WebDriverWait(driver, wait_time).until(EC.element_to_be_clickable((By.XPATH, xpath)))
    
def write_in_file(titles):
    with open("titles.txt", "w") as f:
        for title in titles:
            f.write(title.text + "\n")

# ================================== # ================================== #
# TODO : Get all (titles, coresponding categories, source, time, link) & Store them in array

def search_news(driver, search_term):
    search_bar = driver.find_element(By.XPATH, XPATHS["search_bar"])
    search_bar.send_keys(search_term)
    search_bar.send_keys(Keys.ENTER)
    
    return driver

def advanced_search(driver, exact_phrase="", has_words="", exclude_words="", website="", date_op="Anytime"):
    adv_btn = wait_for_element_xpath(driver, XPATHS["Adv_search_btn"])
    adv_btn.click()
    
    # Exact phrase
    if exact_phrase != "":
        exact_phrase_input = wait_for_click_xpath(driver, XPATHS["Exact_phrase"])
        exact_phrase_input.send_keys(exact_phrase)

    # Has words
    if has_words != "":
        has_words_input = wait_for_click_xpath(driver, XPATHS['Has_words'])
        has_words_input.send_keys(has_words)
    
    # Exclude words
    if exclude_words != "":
        exclude_words_input = wait_for_click_xpath(driver, XPATHS["Exclude_words"])
        exclude_words_input.send_keys(exclude_words)
    
    # Website
    if website != "":
        website_input = wait_for_click_xpath(driver, XPATHS["Website"])
        website_input.send_keys(website)

    # date
    date = wait_for_click_xpath(driver, XPATHS["Date"])
    date.click()
    
    choice = wait_for_click_xpath(driver, XPATHS["Date_choice"].format(DATE_OPTIONS[date_op]))
    choice.click()


    btn = wait_for_click_xpath(driver, XPATHS["Search_btn"])
    btn.click()

    return driver


def get_news(driver, DF=True, DEBUG=False):

    # Prepare containers
    if DF:
        df = pd.DataFrame(columns=['Category', 'Title', 'Source', 'Time', 'Link'])
    else:
        CATEGORIES = []
        TITLES = []
        LINKS = []
        SOURCES = []
        TIME = []

    # Get divs with categories
    driver.implicitly_wait(5)

    main_sub_divs = driver.find_elements(By.CLASS_NAME, CLASS_NAMES["Main_sub_divs1"])
    for sdiv in main_sub_divs:
        try: 
            category = sdiv.find_element(By.CLASS_NAME, CLASS_NAMES["Category"])
            category_txt = category.text
            if DEBUG:
                print(category.text)
                write_in_file([category])
        except: 
            category_txt = "Not Specified"
        titles = sdiv.find_elements(By.CLASS_NAME, CLASS_NAMES["Titles"])
        l_titles = len(titles)
        cats = [category_txt] * l_titles
        sources = sdiv.find_elements(By.CLASS_NAME, CLASS_NAMES["Sources"])
        links_div = sdiv.find_elements(By.CLASS_NAME, CLASS_NAMES["links_div"])
        links = [link.get_attribute("href") for link in links_div]


        # Store elements
        if DF:
            row = {'Category': cats,
                    'Title': [title.text for title in titles],
                    'Source': [source.text for source in sources],
                    'Time': [time.get_attribute('datetime') for time in sdiv.find_elements(By.CLASS_NAME, CLASS_NAMES["time"])],
                    'Link': links}
            df = pd.concat([df, pd.DataFrame(row)], ignore_index=True)

        else : 
            CATEGORIES.extend(cats)
            TITLES.extend([title.text for title in titles])
            LINKS.extend(links)
            TIME.extend([time.get_attribute('datetime') for time in sdiv.find_elements(By.CLASS_NAME, CLASS_NAMES["time"])])
            SOURCES.extend([source.text for source in sources])

        if DEBUG: 
            for title in titles:
                print(title.text)
                write_in_file(titles)
        if DEBUG: 
            print(f"Number of titles: {l_titles}, Number of sources: {len(sources)}")
            for source in sources:
                print(source.text)
                write_in_file(sources)


    if DEBUG: print(5*'\n')


    # Get divs without categories
    main_sub_divs = driver.find_elements(By.CLASS_NAME, CLASS_NAMES["Main_sub_divs2"])

    if DEBUG: print("No Category elements: Length: {}".format(len(main_sub_divs)))

    for sdiv in main_sub_divs:
        # title of subdiv
        title = sdiv.find_element(By.CLASS_NAME, CLASS_NAMES["Titles"])
        # Source of subdiv
        source = sdiv.find_element(By.CLASS_NAME, CLASS_NAMES["Sources"])
        # time of subdiv
        time = sdiv.find_element(By.CLASS_NAME, CLASS_NAMES["time"])
        # links 
        links = sdiv.find_elements(By.CLASS_NAME, CLASS_NAMES["links_div"])

        
        # Store elements
        if DF:
            row = {'Category': "Not Specified",
                    'Title': title.text, 
                    'Source': source.text, 
                    'Time': time.get_attribute('datetime'), 
                    'Link': [link.get_attribute("href") for link in links]}
            df = pd.concat([df, pd.DataFrame(row)], ignore_index=True)
            
        else:  
            CATEGORIES += ["Not Specified"]
            TITLES += [title.text]
            SOURCES += [source.text]
            TIME += [time.get_attribute('datetime')]
            LINKS += [link.get_attribute("href") for link in links]

        if DEBUG: 
            print(title.text)
            print(source.text)
            print(time.get_attribute("datetime"))
    if DEBUG: print(5*'\n')

    if DF : 
        return df
    else:
        return CATEGORIES, TITLES, SOURCES, TIME, LINKS


# ================================== TEST ==================================
if __name__ == "__main__":
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized");
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")

    driver = webdriver.Chrome(DRIVER_PATH, options=options)
    driver.get(URL)
    
    # basic search
    driver = search_news(driver, "sudan")
    df = get_news(driver, "sudan", DF=True, DEBUG=True)
    print(df)
    print(df.shape)


    # Advanced search
    driver = advanced_search(driver, exact_phrase="sudan", has_words="protest", exclude_words="corona", date_op="Past year")

    df = get_news(driver, DF=True, DEBUG=True)
    print(df)
    print(df.shape)


    if SAVE: 
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)
        df.to_csv(os.path.join(DATA_DIR, "news.csv"), index=False)

    driver.close()