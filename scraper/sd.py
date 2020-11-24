from datetime import datetime, date
import re

import format.mla as mla
import scraper.main as scraper

def get_authors_sd(soup):
    authors =[]
    author_group = soup.find_all("a", {"class": re.compile("author")})
    if author_group:
        for author_raw in author_group:
            names = author_raw.find_all("span", {"class": re.compile("text")})
            if names:
                authors.append(names[0].string + " " + names[1].string)
    else:
        authors = None
    return authors

def get_title_sd(soup):
    header = soup.find("meta", {'name': "citation_title"})
    if header:
        title = header["content"]
    else:
        title = None
    return title

def get_container_sd(soup):
    scrape = soup.find("meta", {'name': "citation_journal_title"})
    if scrape:
        container = scrape["content"]
    else:
        container = None
    return container

def get_publisher_sd(soup):
    scrape = soup.find("meta", {'name': "citation_publisher"})
    if scrape:
        publisher = scrape["content"]
    else:
        publisher = None
    return publisher

def get_issue_sd(soup):
    scrape = soup.find("meta", {'name': "citation_issn"})
    if scrape:
        issue = scrape["content"]
    else:
        issue = None
    return issue

def get_volume_sd(soup):
    scrape = soup.find("meta", {'name': "citation_volume"})
    if scrape:
        volume = scrape["content"]
    else:
        volume = None
    return volume

def get_pubdate_sd(soup):
    scrape = soup.find("meta", {'name': "citation_publication_date"})
    if scrape:
        try:
            pubdate = datetime.strptime(scrape["content"], "%Y/%m/%d")
        except:
            pubdate = None
    else:
        pubdate = None
    return pubdate

def get_pages_sd(soup):
    scrape = soup.find("meta", {'name': "citation_firstpage"})
    if scrape:
        firstpage = scrape["content"]
        scrape = soup.find("meta", {'name': "citation_lastpage"})
        if scrape:
            lastpage = scrape["content"]
            pages = firstpage + "-" + lastpage
        else:
            pages = firstpage
    else:
        pages = None
    return pages

def get_onlinedate_sd(soup):
    scrape = soup.find("meta", {'name': "citation_online_date"})
    if scrape:
        onlinedate = datetime.strptime(scrape["content"], "%Y/%m/%d")
    else:
        onlinedate = None
    return onlinedate

def get_doi_sd(soup):
    scrape = soup.find("meta", {'name': "citation_doi"})
    if scrape:
        doi = scrape["content"]
    else:
        doi = None
    return doi

def get_accessdate():
    return date.today()

def create_citation_sd(link, style="mla"):
    soup = scraper.create_soup(link)
    if soup:
        citation_raw = {
        "authors" : get_authors_sd(soup),
        "title" : get_title_sd(soup),
        "container" : get_container_sd(soup),
        "publisher" : get_publisher_sd(soup),
        "volume" : get_volume_sd(soup),
        "issue" : get_issue_sd(soup),
        "pages" : get_pages_sd(soup),
        "pubdate" : get_pubdate_sd(soup),
        "location" : get_doi_sd(soup),
        "accessdate" : get_accessdate()
        }
        return mla.research_citation(citation_raw, htmlify=True)
    else:
        return None
