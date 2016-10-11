# Facebook Bot
Facebook bot with Selenium Webdriver.

### Features:
- Login
- Post messages in groups
- Delete messages in a group
- List all the posts in a group

It can be used also for crawling/scraping of all the posts in a group.

## Installation
Ubuntu 14.04 works for me.
- Install Virtual Environment - Python 3.4.3
- Install Requirements:
    `    pip install -r requirements.txt    `

### Install Dependencies:
[Firefox 45](https://www.mozilla.org) English Version.




## Usage:
#### Post a msg in a group:
    ...
    import fbot
    (driver, username) = fbot.login(email, password)
    fbot.post_to_group(driver=driver, post_msg=msg, group_id=group_id)
    ...


#### Delete the first owned post in a group:
    ...
    import fbot
    (driver, username) = fbot.login(email, password)
    fbot.delete_first_post_in_group(driver=driver, group_id=group_id)
    ...

#### Iterate over the posts of a group:
    ...
    import fbot
    (driver, username) = fbot.login(email, password)
    fbot.iterate_group_posts(driver=driver, group_id=group_id)
    ...

## Testing
pytest is used.
In order to run the test you must provide Facebook username and password in the tests/conf.py.
You can rename and modify the tests/conf_template.py file. Then:

    pytest


# Todo:
Keep the software always up-to-date with the changes on the facebook platform.




