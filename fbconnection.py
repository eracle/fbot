from itertools import ifilter

from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.firefox import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)

def init_firefox_driver():
    logger.info('Init Firefox Browser')
    profile = webdriver.FirefoxProfile()
    profile.set_preference('dom.disable_beforeunload', True)
    return webdriver.Firefox(profile)







class FbConnection(object):

    def __init__(self, email, password, driver=None, web_wait_timeout=10, max_n_retry=10):
        if driver is None:
            self.driver = init_firefox_driver()
        else:
            self.driver = driver
        self.driver.get('https://www.facebook.com')

        self.max_n_retry = max_n_retry
        self.web_wait_timeout = web_wait_timeout

        logger.info('Log in - Searching for the email input')
        wait = WebDriverWait(self.driver, self.web_wait_timeout)
        el_email = wait.until(
            ec.presence_of_element_located(
                (By.XPATH, '//input[@id="email"]')
            ))

        el_email.send_keys(email)

        logger.info('Log in - Searching for the password input')
        wait = WebDriverWait(self.driver, self.web_wait_timeout)
        el_pass = wait.until(
            ec.presence_of_element_located(
                (By.XPATH, '//input[@id="pass"]')
            ))

        el_pass.send_keys(password)

        logger.info('Log in - Searching for the submit button')
        wait = WebDriverWait(self.driver, self.web_wait_timeout)
        el_login = wait.until(
            ec.presence_of_element_located(
                (By.XPATH, '//input[@type="submit"]')
            ))

        el_login.click()

        # get the user name
        self.user_name = WebDriverWait(self.driver, self.web_wait_timeout).until(
            ec.presence_of_element_located(
                (By.XPATH, "/html/body/div[1]/div[2]/div[1]/div/div[2]/div[1]/div[1]/ul/li[1]/div/div"))).text
        logger.info('Log in - Saving the username, which is: %s' % self.user_name)

    def post_to_sale_group(self, group_id,  sell_msg, item_description, price=0, location=None):

        logger.info('Posting to Sale Group - group id: %s' % group_id)

        first_what_placeholder = 'What are you selling?'
        second_what_placeholder = 'What are you selling?'
        price_placeholder = 'Add price'
        location_placeholder = 'Add Location (optional)'

        url = 'https://www.facebook.com/groups/%s/' % group_id

        for n_retry in range(self.max_n_retry):
            # Opening the group page
            logger.info('Posting to Sale Group  - Opening the group page (number of retry: %s)' % n_retry)

            self.driver.get(url)

            try:
                # Opening the what to sell form
                logger.info('Posting to Sale Group  - Opening the what to sell form')
                wait = WebDriverWait(self.driver, self.web_wait_timeout)
                first_what_xpath = wait.until(
                    ec.presence_of_element_located((By.XPATH, '//*[@placeholder=\'%s\']' % first_what_placeholder)))

                first_what_xpath.click()

                logger.info('Posting to Sale Group  - Selecting the what to sell form')
                # Selecting the what to sell form
                wait = WebDriverWait(self.driver, self.web_wait_timeout)
                what_xpath = wait.until(
                    ec.presence_of_element_located((By.XPATH, '//*[@placeholder=\'%s\']' % second_what_placeholder)))
                # what_xpath = driver.find_element(By.XPATH, '//*[@placeholder=\'%s\']' % second_what_placeholder)

                what_xpath.send_keys(sell_msg)

                logger.info('Posting to Sale Group  - Selecting the price form')
                # Selecting the price form
                wait = WebDriverWait(self.driver, self.web_wait_timeout)
                price_xpath = wait.until(
                    ec.presence_of_element_located((By.XPATH, '//*[@placeholder=\'%s\']' % price_placeholder)))
                # price_xpath = driver.find_element(By.XPATH, '//*[@placeholder=\'%s\']' % price_placeholder)

                price_xpath.send_keys(price)

                logger.info('Posting to Sale Group  - Selecting the location form')
                # Selecting the location form
                wait = WebDriverWait(self.driver, self.web_wait_timeout)
                location_xpath = wait.until(
                    ec.presence_of_element_located(
                        (By.XPATH, '//input[@placeholder=\'%s\']' % location_placeholder)))

                logger.info('Posting to Sale Group  - Deleting (if present) the location by pressing the remove button')
                # Deleting (if present) the location by pressing the remove button
                location_xpath.clear()

                if location is not None:
                    location_xpath.send_keys(location)
                    location_xpath.send_keys(Keys.ENTER)

                logger.info('Posting to Sale Group  - Selecting the description form')
                # Selecting the description form
                wait = WebDriverWait(self.driver, self.web_wait_timeout)
                description_span_xpath = wait.until(
                    ec.presence_of_element_located(
                        (By.XPATH,
                         "//div[2]/div[3]/div/div[1]/div[1]/div/div[2]/div/div[1]/div[4]/div[1]/div/div/div[2]/div")))

                description_span_xpath.send_keys(item_description)

                #    self.driver.save_screenshot('screenshot1.png')

                logger.info('Posting to Sale Group  - Pressing the Post Button!')
                # Pressing the Post Button!
                wait = WebDriverWait(self.driver, self.web_wait_timeout)
                post_button = wait.until(
                    ec.presence_of_element_located(
                        (By.XPATH, '//span/button[@type=\'submit\' and text()=\'Post\']')))

                post_button.send_keys(Keys.ENTER)

                logger.info('Posting to Sale Group  - Waiting for the publishing of the post')
                # waiting for the publishing of the post
                wait = WebDriverWait(self.driver, self.web_wait_timeout)
                wait.until(
                    ec.invisibility_of_element_located(
                        (By.XPATH, '//span/button[@type=\'submit\' and text()=\'Post\']')))

                # seems everything gone well
                return
            except (TimeoutException, StaleElementReferenceException):
                print "Timeout encountered"
                # self.driver.save_screenshot('post_to_group-.png')
                # self.driver.save_screenshot('screenshot2.png')

    def post_to_group(self, group_id, post_msg):

        driver = self.driver
        web_wait_timeout = self.web_wait_timeout
        max_n_retry = self.max_n_retry

        logger.info('Posting to Normal Group - group id: %s' % group_id)

        write_post_placeholder = 'Write something...'
        url = 'https://www.facebook.com/groups/%s/' % group_id
        for n_retry in range(max_n_retry):

            logger.info('Posting to Normal Group - Opening the page (number retry: %s)'% n_retry)
            # Opening the group page
            driver.get(url)

            try:
                logger.info('Posting to Normal Group - Selecting the write form')
                # Selecting the write form
                wait = WebDriverWait(driver, web_wait_timeout)
                write_xpath = wait.until(
                    ec.presence_of_element_located((By.XPATH, '//*[@placeholder=\'%s\']' % write_post_placeholder)))

                if write_xpath.text != "":
                    write_xpath.clear()

                # write_xpath.click()
                write_xpath.send_keys(post_msg)



                logger.info('Posting to Normal Group - Pressing the Post Button!')
                # Pressing the Post Button!
                post_button_xpath = "//div/div[2]/button[@type='submit' and @value='1']"
                post_button = WebDriverWait(driver, web_wait_timeout).until(
                    ec.presence_of_element_located((By.XPATH, post_button_xpath)))

                post_button.send_keys(Keys.ENTER)

                logger.info('Posting to Normal Group - Waiting for the publishing of the post')
                # waiting for the publishing of the post
                wait = WebDriverWait(driver, web_wait_timeout)
                wait.until(
                    ec.invisibility_of_element_located(
                        (By.XPATH, post_button_xpath)))
                # every things seems gone well, I can exit from the loop
                return
            except (TimeoutException, StaleElementReferenceException) as e:
                print e
                print "n_retry:%s" % n_retry
                print "Refreshing"
                # self.driver.save_screenshot('post_to_group-.png')

    def delete_first_post_in_group(self, group_id, msg_to_remove=None):
        """
            Identifies the first occurrence of a post in a group and remove it
            :param group_id: The id of the group where must be deleted the post.
            :param msg_to_remove: The msg to remove, if not give the first post of the user_name will be deleted
            :return:
        """

        driver = self.driver
        web_wait_timeout = self.web_wait_timeout
        user_name = self.user_name

        logger.info('Delete first post in a group - group id: %s' % group_id)

        for n_retry in range(self.max_n_retry):
            try:
                logger.info('Delete first post in a group - Opening the page (number retry: %s)' % n_retry)

                for item_dict in self.iterate_group_posts(group_id):

                    logger.info('Delete first post in a group - Extracting name and message for every post')
                    # extracting name and message for every post
                    # name
                    name = item_dict["name"]

                    # msg
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
                        # clicking the curtain button
                        curtain_xpath = item_xpath.find_element(By.XPATH, ".//a[@aria-label='Story options']")
                        # code.interact(local=locals())

                        curtain_xpath.send_keys(Keys.NULL)
                        curtain_xpath.click()

                        logger.info('Delete first post in a group - selecting and clicking the delete button')
                        # selecting and clicking the delete button
                        WebDriverWait(driver, web_wait_timeout).until(ec.presence_of_element_located(
                            (By.XPATH, "//a/span/span/div[text()='Delete Post']"))).click()

                        logger.info('Delete first post in a group - selecting and clicking the confirm delete button')
                        # selecting and clicking the confirm delete button
                        WebDriverWait(driver, web_wait_timeout).until(ec.presence_of_element_located(
                            (By.XPATH, "//button[text()='Delete']"))).click()

                        logger.info('Delete first post in a group - waiting for the del of the post')
                        # waiting for the del of the post
                        WebDriverWait(driver, web_wait_timeout).until(
                            ec.invisibility_of_element_located(
                                (By.XPATH, "//button[text()='Delete']")))

                        # seems everything gone well
                        logger.info('Deleted')
                        return
            except (TimeoutException, StaleElementReferenceException) as e:
                print e
                print "n_retry:%s" % n_retry
                print "Refreshing"

    def iterate_group_posts(self, group_id):
        """
        Iterate through all the posts of a group.
        The returned object iterates over dictionaries.
        :param fbconnection: the facebook connection object
        :param group_id:
        :return:
        """
        driver = self.driver
        web_wait_timeout = self.web_wait_timeout

        logger.info("Iterate Group\'s Posts - group id: %s" % group_id)
        url = 'https://www.facebook.com/groups/%s/' % group_id
        driver.refresh()
        driver.get(url)

        something_changed = True
        iterated_yet = set()

        logger.info("Iterate Group\'s Posts - load first post")
        # load first post
        WebDriverWait(driver, web_wait_timeout).until(
            ec.presence_of_element_located(
                (By.XPATH, "//div/div[@role='article']/div[1]")
            ))

        logger.info("Iterate Group\'s Posts - retrieve all the post's divs")
        # retrieve all the posts_divs:
        posts_divs = WebDriverWait(driver, web_wait_timeout).until(ec.presence_of_all_elements_located(
            (By.XPATH, "//div/div[@role='article']/div[1]")
        ))

        while something_changed:
            logger.info("Iterate Group\'s Posts - Executing a page scroll")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            for single_post_div in ifilter(lambda x: x not in iterated_yet, posts_divs):

                name_and_date_div = try_or_none(single_post_div, "./div[3]")

                name_div = try_or_none(name_and_date_div, "./div/div/div[2]/div/div/div[2]/h5/span/span/a")

                date_div = try_or_none(name_and_date_div, "./div/div/div[2]/div/div/div[2]/div/span/span/a/abbr/span")
#
#                text_div = try_or_none(single_post_div, "./div[4]")
#
#                img_div = try_or_none(single_post_div, "./div[5]/div/div/div/a/div/img")

                # comments_div = try_or_none(item, "./div/div[2]/div[2]")

                ignore_items = [u'RECENT ACTIVITY', u'OLDER']
                ignore = False
                if single_post_div.text.split('\n')[0] in ignore_items:
                    ignore = True

                if single_post_div.text.split('\n')[0].endswith(u'created the group.'):
                    ignore = True

                import q
                q.d()

                if not ignore:
                    ret = {
                        "name": name_div.text,
                        "date": date_div.text,
#                        "text": text_div.text,
                        "web_element": single_post_div
                    }
                    logger.info("Iterate Group\'s Posts - Retrieved: %s,%s" % (ret["name"], ret["date"]))
                    iterated_yet.add(single_post_div)
                    yield ret

            logger.info("Iterate Group\'s Posts - waiting for the first posts div (again)")
            # waiting for the first posts div (again)
            WebDriverWait(driver, web_wait_timeout).until(
                ec.presence_of_element_located(
                    (By.XPATH, "//div/div[@role='article']/div[1]")
                ))

            old_posts = posts_divs

            logger.info("Iterate Group\'s Posts - retrieve all the posts_divs (again)")
            # retrieve all the posts_divs:
            posts_divs = WebDriverWait(driver, web_wait_timeout).until(ec.presence_of_all_elements_located(
                (By.XPATH, "//div/div[@role='article']/div[1]")
            ))

            if len(old_posts) == len(posts_divs):
                something_changed = False







def try_or_none(item, xpath):
    logging.debug("Try Or None, (item,xpath): %s,%s" % (item,xpath))
    try:
        r = item.find_element(By.XPATH, xpath)
        return r
    except (TimeoutException, NoSuchElementException):
        logging.warning("Returned None!")
        return None

