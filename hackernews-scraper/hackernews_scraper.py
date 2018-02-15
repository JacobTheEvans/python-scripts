import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def scrape(driver):
    result = []
    outer_table = driver.find_element_by_id("hnmain")
    outer_body = outer_table.find_element_by_tag_name("tbody")
    inner_table = outer_body.find_element_by_class_name("itemlist")
    rows = inner_table.find_elements_by_class_name("title")

    for item in rows:
        link_object = item.find_elements_by_tag_name("a")
        if len(link_object) > 0:
            link = link_object[0].get_attribute("href")
            title = link_object[0].text
            result.append({"title": title, "link": link})
    return result

def load_content(driver):
    url = "https://news.ycombinator.com/"
    driver.get(url)
    time.sleep(4)

def main():
    print "[+] Hacker News Scraper Starting"
    print "[+] Loading Connection"
    driver = webdriver.Firefox()
    load_content(driver)
    print "[+] Success, Starting Scraping Of Page"
    data = scrape(driver)
    driver.quit()
    print "[+] Success, See Articles Below"
    time.sleep(2)
    for i in data:
        print i["title"]
        print "Link: " + i["link"] + "\n"


if __name__ == "__main__":
    main()
