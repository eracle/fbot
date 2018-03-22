# Facebook Bot
Facebook bot with Selenium Webdriver.

### Features:
- Login
- Post messages on groups
- Delete messages on a group
- List all the posts on a group

It can be used also for crawling/scraping all the posts on a group.

## Installation
Ubuntu 14.04:
- Install Virtual Environment - Python 3.4+
- Install Requirements:
    `    pip install -r requirements.txt    `

### Install Dependencies:
[Firefox 45](https://www.mozilla.org) English Version.




## Usage:
#### Post a msg on a group:
    ...
    import fbot
    (driver, username) = fbot.login(email, password)
    fbot.post_to_group(driver=driver, post_msg=msg, group_id=group_id)
    ...


#### Delete the first owned post on a group:
    ...
    import fbot
    (driver, username) = fbot.login(email, password)
    fbot.delete_first_post_in_group(driver=driver, group_id=group_id)
    ...

#### Iterate over the posts on a group:
    ...
    import fbot
    (driver, username) = fbot.login(email, password)
    fbot.iterate_group_posts(driver=driver, group_id=group_id)
    ...

## Testing
pytest.
In order to run the tests put Facebook username and password in the tests/conf.py.
Rename and modify the tests/conf_template.py file. Then type:

    pytest


# Todo:
Keep the software always up-to-date with the changes on the facebook platform.




