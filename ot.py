import os
import sys
import uuid

from bs4 import BeautifulSoup as bs4
import regex as re
import requests as rs


def hyphonate(words):
    return u"-".join(words.split(" "))


def pprint(posts):
    for uuid, post in posts.items():
        location = post['location']
        salary = post['salary']
        title = post['title']
        url = post['url']

        print("Link:\t\t%s" % url)
        print("Title:\t\t%s" % title)
        print("Location:\t%s" % location)
        print("Salary:\t\t%s" % salary)
        print("-----------------------\n")
    print("End")


def parse_ot_posting(data):
    post = {}

    _klass = 'rh-job-result-table'
    _k_title = '%s__job-title' % _klass
    _k_url = _k_title
    _k_loc = '%s__location' % _klass
    _k_cash = '%s__salary' % _klass
    _k_emtype = '%s_emptype' % _klass

    post['location'] = data.find('span', attrs={'class': _k_loc}).text.strip()
    post['salary'] = data.find('span', attrs={'class': _k_cash}).text.strip()
    post['title'] = data.find('a', attrs={'class': _k_title}).text.strip()
    post['url'] = data.find('a', attrs={'class': _k_title})['href']

    return post

def parse_officeteam(data):
    page = bs4(str(data, encoding='utf-8'), 'html5lib')

    _klass = 'rh-job-result-table'
    rows = page.find_all(attrs={"class": "%s__job-summary" % _klass})
    print("Office Team: %d jobs found." % len(rows))
    postings = dict()
    for row in rows:
        post_id = str(uuid.uuid4())
        postings[post_id] = parse_ot_posting(row)

    pprint(postings)


def search_officeteam_cached(keywords, location):
    try:
        os.makedirs(
            os.path.join(
                # Create $PWD/cachedir/officeteam if needed
                # XXX Needs to be configurable
                os.getcwd(), "cachedir", "officeteam"
            ), exist_ok=True)
    except Exception as error:
        print(error)


def search_officeteam(keywords="", location=1):
    ACTION = "https://www.roberthalf.com/jobs/%s/%s"
    URL = ACTION % (hyphonate(keywords), location)
    print("Searching: %s" % URL)

    request = rs.get(URL)
    return parse_officeteam(request.content)
