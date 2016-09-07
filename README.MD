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
- Install Virtual Environment - Python 2.7
- Install Requirements:
    `    pip install -r requirements.txt    `

### Install Dependencies:
[Firefox 45](https://www.mozilla.org) English Version.




## Usage:
#### Post a msg in a group:
    ...
    from fbconnection import FbConnection
    sut = FbConnection(email, password)
    sut.post_to_group(post_msg=msg, group_id=group_id)
    ...


#### Delete the first owned post in a group:
    ...
    from fbconnection import FbConnection
    sut = FbConnection(email, password)
    sut.delete_first_post_in_group(group_id=group_id)
    ...

#### Iterate over the posts of a group:
    ...
    from fbconnection import FbConnection
    sut = FbConnection(email, password)
    sut.iterate_group_posts(group_id=group_id)
    ...

## Testing
there are some unittest, they are called test*.py.

In order to use them rename the file test_conf_template.py in test_conf.py and fill the variables in there.
Then call the selected test file, for instance:
    `
    python test_regression.py
    `


# Todo:
Keep the software always up-to-date with the changes on the facebook platform.




