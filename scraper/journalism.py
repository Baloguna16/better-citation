from datetime import datetime, date
import re

import format.mla as mla
import format.cmos as cmos
import scraper.main as scraper

def get_authors(soup):
    author_tag = soup.find("meta", {"name": "author"})
    if not author_tag:
        author_tag = soup.find("meta", {"property": "author"})
        if not author_tag:
            return None
    if " and " in author_tag['content']:
        author_list = author_tag['content'].split(" and ")
        authors = [author for author in author_list]
    else:
        authors = [author_tag['content']]
    return authors

def get_title(soup):
    header = soup.find("meta", {'property': "og:title"})
    if header:
        title = header["content"]
    else:
        title = None
    return title

#could also work for get_container()
def get_container(soup):
    header = soup.find("title")
    return header.string.split(" - ")[-1]

def get_contributors(soup):
    #TODO: people who illustrate, photgraph, translate...
    contributors = []
    contributors_raw = soup.find_all("span", {"itemprop": "copyrightHolder"})
    for contributor_raw in contributors_raw:
        children = contributor_raw.find_all("span")
        if children is not None:
            for child in children:
                if "Credit" not in child.string:
                    contributors.append(' '.join(re.split("\W", child.string)[:2]))
    return list(set(contributors))

def get_publisher(soup):
    #TODO: eventually find a replicable way of scraping the website.
    container_tag = soup.find("meta", {'property': "og:site_name"})
    if container_tag:
        container = container_tag["content"]
    else:
        container = None
    return container

def get_pubdate(soup):
    if soup.find("meta", {'property': "og:updated_time"}):
        date_tag = soup.find("meta", {'property': "og:updated_time"})
        if 'T' in date_tag["content"]:
            publication_date = date_tag["content"]
            time_str = publication_date.split('T')[0]
        else:
            time_str = date_tag["content"]
        formatted_date = datetime.strptime(time_str, "%Y-%m-%d")
    else:
        date_tag = soup.find("time")
        if date_tag:
            if date_tag["datetime"]:
                publication_date = date_tag["datetime"]
                time_str = publication_date.split('T')[0]
                formatted_date = datetime.strptime(time_str, "%Y-%m-%d")
            else:
                formatted_date = date.today()
        else:
            formatted_date = date.today()
    return formatted_date

def get_location(link):
    if "?" in link:
        formatted_link_step_1 = link.split("?")[0]
    else:
        formatted_link_step_1 = link

    if "http://" in formatted_link_step_1:
        formatted_link_step_2 = formatted_link_step_1.split("http://")[1]
    elif "https://" in formatted_link_step_1:
        formatted_link_step_2 = formatted_link_step_1.split("https://")[1]
    else:
        formatted_link_step_2 = formatted_link_step_1
    return formatted_link_step_2

def get_accessdate():
    return date.today()

def create_citation_journalism(link, style="mla"):
    soup = scraper.create_soup(link)
    if soup:
        citation_raw = {
        "authors" : get_authors(soup),
        "title" : get_title(soup),
        "container" : get_container(soup),
        "contributors" : get_contributors(soup),
        "publisher" : get_publisher(soup),
        "pubdate" : get_pubdate(soup),
        "location" : get_location(link),
        "accessdate" : get_accessdate()
        }
        if style == "mla":
            return mla.mla_citation(citation_raw, htmlify=True)
        elif style == "cmos":
            return cmos.cmos_citation(citation_raw, htmlify=True)
        else:
            return None
    else:
        return None
