from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.firefox import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver

from itertools import count
import collections

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)


"""
number of seconds used to wait the web page's loading.
"""
WAIT_TIMEOUT = 10

"""
Maximum number of times a TimeoutException or StaleElementReferenceException can happen before quitting the program.
"""
MAX_N_RETRY = 5


def get_by_xpath(driver, xpath):
    """
    Get a web element through the xpath passed by performing a Wait on it.
    :param driver: Selenium web driver to use.
    :param xpath: xpath to use.
    :return: The web element
    """
    return WebDriverWait(driver, WAIT_TIMEOUT).until(
        ec.presence_of_element_located(
            (By.XPATH, xpath)
        ))


def retry_if_timeout(function):
    """
    Execute a function code, if a TimeoutException or StaleElementReferenceException
    happens the function is re-executed a MAX_N_RETRY of times.
    :param function: function to execute.
    :return: what the function returns None otherwise.
    """
    for n_retry in range(MAX_N_RETRY):
        try:
            logger.info('retry_if_timeout (number of retry: %s)' % n_retry)
            return function()
        except (TimeoutException, StaleElementReferenceException) as err:
            logger.info(err)
            # driver.save_screenshot('post_to_group-.png')
            # driver.save_screenshot('screenshot2.png')


def login(email, password):
    """
    Performs a Login to the Facebook platform.
    :param email: The used email account.
    :param password: Its password
    :return: Returns the logged Selenium web driver and the user name string.
    """
    logger.info('Init Firefox Browser')
    profile = webdriver.FirefoxProfile()
    profile.set_preference('dom.disable_beforeunload', True)
    driver =  webdriver.Firefox(profile)

    driver.get('https://www.facebook.com')

    logger.info('Log in - Searching for the email input')
    get_by_xpath(driver, '//input[@id="email"]').send_keys(email)

    logger.info('Log in - Searching for the password input')
    get_by_xpath(driver, '//input[@id="pass"]').send_keys(password)

    logger.info('Log in - Searching for the submit button')
    get_by_xpath(driver, '//input[@type="submit"]').click()

    logger.info('Log in - get the user name')
    user_name = get_by_xpath(driver, "/html/body/div[1]/div[2]/div[1]/div/div[2]/div[1]/div[1]/ul/li[1]/div/div").text

    logger.info('Log in - Saving the username, which is: %s' % user_name)
    return driver, user_name


def post_to_sale_group(driver, group_id, sell_msg, item_description, price=0, location=None):
    """
    Writes a post to a sell group.
    :param driver:
    :param group_id:
    :param sell_msg:
    :param item_description:
    :param price:
    :param location:
    :return:
    """

    first_what_placeholder = 'What are you selling?'
    second_what_placeholder = 'What are you selling?'
    price_placeholder = 'Add price'
    location_placeholder = 'Add Location (optional)'

    url = 'https://www.facebook.com/groups/%s/' % group_id

    logger.info('Posting to Sale Group - group id: %s' % group_id)

    def _post_to_sale_group():
        driver.get(url)

        logger.info('Posting to Sale Group  - Opening the what to sell form')
        get_by_xpath(driver, '//*[@placeholder=\'%s\']' % first_what_placeholder).click()


        logger.info('Posting to Sale Group  - Selecting the what to sell form')
        get_by_xpath(driver, '//*[@placeholder=\'%s\']' % second_what_placeholder).send_keys(sell_msg)

        logger.info('Posting to Sale Group  - Selecting the price form')
        get_by_xpath(driver, '//*[@placeholder=\'%s\']' % price_placeholder).send_keys(price)


        logger.info('Posting to Sale Group  - Selecting the location form')
        location_xpath = get_by_xpath(driver, '//input[@placeholder=\'%s\']' % location_placeholder)

        logger.info('Posting to Sale Group  - Deleting (if present) the location by pressing the remove button')
        location_xpath.clear()

        if location is not None:
            location_xpath.send_keys(location)
            location_xpath.send_keys(Keys.ENTER)

        logger.info('Posting to Sale Group  - Selecting the description form')
        get_by_xpath(driver,"//div[2]/div[3]/div/div[1]/div[1]/div/div[2]/div/div[1]/div[4]/div[1]/div/div/div[2]/div").send_keys(item_description)

        logger.info('Posting to Sale Group  - Pressing the Post Button!')
        get_by_xpath(driver, '//span/button[@type=\'submit\' and text()=\'Post\']').send_keys(Keys.ENTER)

        logger.info('Posting to Sale Group  - Waiting for the publishing of the post')
        WebDriverWait(driver, WAIT_TIMEOUT).until(ec.invisibility_of_element_located((By.XPATH, '//span/button[@type=\'submit\' and text()=\'Post\']')))

        # seems everything gone well
        return

    retry_if_timeout(_post_to_sale_group)


def post_to_group(driver, group_id, post_msg):
    """
    Writes a post to a group.
    :param driver:
    :param group_id:
    :param post_msg:
    :return:
    """

    write_post_placeholder = 'Write something...'

    url = 'https://www.facebook.com/groups/%s/' % group_id

    logger.info('Posting to Normal Group - group id: %s' % group_id)

    driver.get(url)

    def _post_to_group():

        logger.info('Posting to Normal Group - Selecting the write form')
        write_xpath = get_by_xpath(driver, '//*[@placeholder=\'%s\']' % write_post_placeholder)

        if write_xpath.text != "":
            write_xpath.clear()

        # write_xpath.click()
        write_xpath.send_keys(post_msg)


        logger.info('Posting to Normal Group - Pressing the Post Button!')

        post_button_xpath = "//div/div[2]/button[@type='submit' and @value='1']"
        get_by_xpath(driver, post_button_xpath).send_keys(Keys.ENTER)


        logger.info('Posting to Normal Group - Waiting for the publishing of the post')
        WebDriverWait(driver, WAIT_TIMEOUT).until(ec.invisibility_of_element_located(
                (By.XPATH, post_button_xpath)))

        return

    retry_if_timeout(_post_to_group)


def delete_first_post_in_group(driver, user_name, group_id, msg_to_remove=None):
    """
    Identifies the first occurrence of a post in a group and remove it
    :param driver:  The Selenium web driver to use.
    :param user_name:   The user name of the account.
    :param group_id: The id of the group where must be deleted the post.
    :param msg_to_remove: The msg to remove, if not give the first post of the user_name will be deleted
    :return:
    """

    logger.info('Delete first post in a group - group id: %s' % group_id)

    def _delete_first_post_in_group():
        for item_dict in iterate_group_posts(driver=driver, group_id=group_id):

            logger.info('Delete first post in a group - Extracting name and message for every post')
            name = item_dict["name"]
            msg = item_dict["text"]
            item_xpath = item_dict["web_element"]

            logger.info('Delete first post in a group - Name and Msg: %s,%s' % (name, msg[:min(20, len(msg))]))

            # delete only if name and msg matches
            to_delete = False
            if msg_to_remove is None and user_name == name:
                to_delete = True
            if msg_to_remove == msg and user_name == name:
                to_delete = True

            if to_delete:
                logger.info('Delete first post in a group - name and msg matches')
                # new item_xpath
                # /html/body/div[1]/div[2]/div[1]/div/div[2]/div[2]/div[3]/div/div[5]/div[3]/div/div[1]/div[2]/div/div[2]/div[1]

                # selecting the "curtain" button
                # WebDriverWait(item_xpath, web_wait_timeout).until(
                # lambda inner_driver: len(
                # [but for but in inner_driver.find_elements(By.XPATH, ".//div/div[2]/div[1]/div[1]/div")
                # if but.rect['height'] == 30 and but.rect['width'] == 27]) > 0)

                logger.info('Delete first post in a group - clicking the curtain button')
                curtain_xpath = item_xpath.find_element(By.XPATH, ".//a[@aria-label='Story options']")
                # code.interact(local=locals())

                curtain_xpath.send_keys(Keys.NULL)
                curtain_xpath.click()

                logger.info('Delete first post in a group - selecting and clicking the delete button')
                get_by_xpath(driver, "//a/span/span/div[text()='Delete Post']").click()

                logger.info('Delete first post in a group - selecting and clicking the confirm delete button')
                delete_xpath = "//button[text()='Delete']"
                get_by_xpath(driver, delete_xpath).click()

                logger.info('Delete first post in a group - waiting for the del of the post')
                WebDriverWait(driver, WAIT_TIMEOUT).until(ec.invisibility_of_element_located((By.XPATH, delete_xpath)))

                # seems everything gone well
                logger.info('Deleted')
                return
    retry_if_timeout(_delete_first_post_in_group)


def iterate_group_posts(driver, group_id):
    """
    Iterate through all the posts of a group.
    :param driver:
    :param group_id:
    :return:
    """

    see_more_placeholder = 'See more'

    post = collections.namedtuple('post', 'name date title price location text xpath_element')

    logger.info("Iterate Group\'s Posts - group id: %s" % group_id)
    url = 'https://www.facebook.com/groups/%s/' % group_id
    driver.get(url)

    def get_single_post(i):
        post_element = get_by_xpath(driver, '//div[%d][contains(@id,"mall_post_")]' % i)

        if see_more_placeholder in post_element.text:
            get_by_xpath(driver, '//div[%d][contains(@id,"mall_post_")]//*[text()="%s"]' %
                         (i, see_more_placeholder)).click()
            post_element = get_by_xpath(driver, '//div[%d][contains(@id,"mall_post_")]' % i)

        lines = post_element.text.splitlines()

        p = post(name=lines[0], date=lines[1], title=lines[2], price=lines[3], location=lines[4],
                 text=lines[5], xpath_element=post_element)

        logger.info("Iterate Group's Posts - Retrieved: %s, %s" % (p.name, p.date))

        return p

    def scroll_if_timeout(function, param):
        n_retry = 0
        try:
            return function(param)
        except (TimeoutException, NoSuchElementException):
            logger.info("Iterate Group's Posts - Executing a page scroll")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            n_retry += 1
            if n_retry > MAX_N_RETRY:
                raise

    for i in count(start=2):
        yield scroll_if_timeout(get_single_post, i)
