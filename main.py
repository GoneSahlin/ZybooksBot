from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from seletools.actions import drag_and_drop
import os
import time


def open_webdriver(url):
    options = Options()

    # options.headless = True
    driver_path = os.path.join('drivers', 'geckodriver')
    firefox_path = R"C:\Program Files\Mozilla Firefox\firefox.exe"

    driver = webdriver.Firefox(options=options, executable_path=driver_path, firefox_binary=firefox_path)
    driver.get(url)

    return driver


def login(driver):
    email = 'zsahlin@zagmail.gonzaga.edu'
    password = open('pass.txt', 'r').read()

    time.sleep(1)
    driver.find_element_by_id('ember9').send_keys(email)
    pass_box = driver.find_element_by_id('ember11')
    pass_box.send_keys(password)
    pass_box.send_keys(Keys.ENTER)


def play_videos(driver):
    # video start buttons
    start_buttons = driver.find_elements_by_xpath("//*[text()='Start']")
    for start_button in start_buttons:
        start_button.click()

    # 2x speed buttons
    # speed_buttons = driver.find_elements_by_class_name('speed-control anti-bounce')
    speed_buttons = driver.find_elements_by_xpath("//*[text()='2x speed']")
    for speed_button in speed_buttons:
        speed_button.click()

    # play all videos
    while(True):
        time.sleep(1)

        play_buttons = driver.find_elements_by_css_selector('.play-button.bounce')

        if len(play_buttons) > 0:
            for play_button in play_buttons:
                play_button.click()
            continue

        pause_buttons = driver.find_elements_by_css_selector('.pause-button')
        if len(pause_buttons) == 0:
            break


def multiple_choices(driver):
    choice_divs = driver.find_elements_by_class_name('question-choices')
    for choice_div in choice_divs:
        for div in choice_div.find_elements_by_tag_name('div'):
            div.click()


def drag_activities(driver):
    activities = driver.find_elements_by_css_selector('.content-resource.definition-match-payload.ember-view')

    print(activities)

    for activity in activities:
        terms = activity.find_elements_by_class_name('unselected-term')
        buckets = activity.find_elements_by_class_name('term-bucket')
        # print('terms:', terms)
        # print('buckets:', buckets)
        driver.execute_script("arguments[0].scrollIntoView();", terms[0])
        actions = ActionChains(driver)
        actions.move_to_element(terms[0]).perform()
        driver.execute_script("window.scrollBy(0, -50)")
        # actions.drag_and_drop(terms[0], buckets[0]).pause(2).perform()
        # actions.click_and_hold(terms[0]).pause(1).move_to_element(buckets[0]).pause(1).release().perform()
        drag_and_drop(driver, terms[0], buckets[0])

        break

        # terms[0].click()


def questions(driver):
    # questions = driver.find_elements_by_class_name('question-container')
    questions = driver.find_elements_by_css_selector('.question-set-question.short-answer-question.ember-view')
    print(questions)
    for question in questions:
        # show answer
        show_button = question.find_element_by_css_selector('.zb-button.secondary.show-answer-button')
        actions = ActionChains(driver)
        driver.execute_script("arguments[0].scrollIntoView();", show_button)
        driver.execute_script("window.scrollBy(0, -50)")
        actions.double_click(show_button).perform()

        # find answer
        answer = question.find_element_by_class_name('forfeit-answer')

        # type answer
        text_area = question.find_element_by_tag_name('textarea')
        text_area.send_keys(answer.text)

        # check answer
        check_button = question.find_element_by_css_selector('.zb-button.primary.raised.check-button')
        check_button.click()


def next(driver):
    next_button = driver.find_element_by_css_selector('.nav-text.next')
    next_button.click()


if __name__ == '__main__':
    url = 'https://learn.zybooks.com/zybook/GONZAGACPSC333OlivaresFall2022/chapter/1/section/4'

    driver = open_webdriver(url)

    login(driver)

    # load
    time.sleep(2)

    # drag_activities(driver)

    while(True):
        questions(driver)
        multiple_choices(driver)
        play_videos(driver)

        time.sleep(1)
        next(driver)
        time.sleep(3)




    time.sleep(1000)
