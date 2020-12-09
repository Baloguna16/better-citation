from datetime import datetime, date
import re

import format.mla as mla
import format.cmos as cmos
import scraper.main as scraper

def get_authors_nyt(soup):
    #ALT METHOD-----
    #links = soup.find_all("a", {'class': "css-brehiz e1jsehar0"})
    #authors = [link.find("span").string for link in links]
    #---------------
    spans = soup.find_all("span", {"itemprop": "name"})
    if spans:
        authors = [span.string for span in spans]
    elif soup.find("meta", {"name": "byl"}):
        spans = soup.find("meta", {"name": "byl"})
        span_content = spans['content']
        if "By " in spans['content']:
            span_content = spans['content'].replace("By ", "")
        if ' and ' in span_content and ', ' not in span_content:
            authors = span_content.split(' and ')
        elif ' and ' in span_content and ', ' in span_content:
            authors_part1 = span_content.split(',')[:-1]
            authors_part2 = span_content.split(' and ')[1]
            authors = []
            authors.append(authors_part1)
            authors.append(authors_part2)
        else:
            authors = [span_content]
    else:
        authors = None
    return authors

def get_title_nyt(soup):
    header = soup.find("meta", {'property': "og:title"})
    if header:
        title = header["content"]
    else:
        title = None
    return title

def get_container_nyt(soup):
    try:
        container = soup.find("title")
        return container.string.split(" - ")[-1]
    except:
        return "The New York Times"

def get_contributors_nyt(soup):
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

def get_publisher_nyt(soup):
    return "The New York Times Company"

def get_pubdate_nyt(soup):
    date = soup.find("time")
    if date:
        publication_date = date["datetime"]
        parts = publication_date.split('T')
        try:
            formatted_date = datetime.strptime(parts[0], "%Y-%m-%d")
        except:
            formatted_date = date.today()
    else:
        formatted_date = date.today()
    return formatted_date

def get_location_nyt(link):
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

def create_citation_nyt(link, style="mla"):
    soup = scraper.create_soup(link)
    if soup:
        citation_raw = {
        "authors" : get_authors_nyt(soup),
        "title" : get_title_nyt(soup),
        "container" : get_container_nyt(soup),
        "contributors" : get_contributors_nyt(soup),
        "publisher" : get_publisher_nyt(soup),
        "pubdate" : get_pubdate_nyt(soup),
        "location" : get_location_nyt(link),
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
