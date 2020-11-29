from datetime import datetime, date
import re

def cmos_citation(citation_raw, htmlify=True):
    if htmlify == True:
        #if citation_raw["container"] and citation_raw["title"]:
        container_cmos = "In <i>" + get_container_cmos(citation_raw["container"]) + "</i>"
    else:
        container_cmos = get_container_cmos(citation_raw["container"])
    if citation_raw["publisher"] and citation_raw["pubdate"]:
        publish_cmos = get_publisher_cmos(citation_raw["publisher"]) + ", " + get_pubdate_cmos(citation_raw["pubdate"])
    else:
        publish_cmos = get_pubdate_cmos(citation_raw["pubdate"])

    citation_list = [
        get_author_cmos(citation_raw["authors"]),
        get_title_cmos(citation_raw["title"]),
        container_cmos,
        get_contributor_cmos(citation_raw["contributors"]),
        publish_cmos,
        get_location_cmos(citation_raw["location"])
        ]
    citation = [element for element in citation_list if element]
    return ". ".join(citation) + '.'

def research_citation(citation_raw, htmlify=True):
    if not get_pages_cmos(citation_raw["pages"]):
        section_cmos = get_volume_cmos(citation_raw["volume"])
    else:
        section_cmos = get_pages_cmos(citation_raw["pages"])
    if htmlify == True:
        block_list = ["In <i>" + get_container_cmos(citation_raw["container"]) + "</i>", section_cmos,]
    else:
        block_list = [get_container_cmos(citation_raw["container"]), section_cmos]
    block_cmos = ", ".join([element for element in block_list if element])

    citation_list = [
        get_author_cmos(citation_raw["authors"]),
        get_title_cmos(citation_raw["title"]),
        block_cmos,
        get_publisher_cmos(citation_raw["publisher"]),
        get_pubdate_cmos(citation_raw["pubdate"]),
        get_location_cmos(citation_raw["location"])
        ]
    citation = [element for element in citation_list if element]
    return ". ".join(citation) + '.'

#takes a list of authors
def get_author_cmos(authors):
    if authors:
        if len(authors) > 3:
            authors = authors[:3]
        name = authors[0].split(' ')
        formatted_name = name[-1]
        if len(name) > 1:
            formatted_name += ', '
            for i in range(len(name) - 1):
                formatted_name += ' ' + name[i]
        author_cmos = formatted_name
        if len(authors) > 1:
            for i in range(len(authors) - 1):
                author_cmos += ', '
                if authors[i + 1] == authors[-1]:
                    author_cmos += 'and '
                author_cmos += authors[i + 1]
    else:
        author_cmos = None
    return author_cmos

def get_title_cmos(title, is_stand_alone=False):
    if title and is_stand_alone == False:
        title_cmos = "\"" + title + "\""
    elif title and is_stand_alone == True:
        title_cmos = title #italics
    else:
        title_cmos = None
    return title_cmos

def get_container_cmos(container):
    return container #italics

def get_contributor_cmos(contributors):
    contributor_cmos = None
    if contributors:
        contributor_cmos = "Contribution from " + contributors[0]
        if len(contributors) > 1:
            for i in range(len(contributors) - 1):
                contributor_cmos += ', ' + contributors[i + 1]
    return contributor_cmos

#if no page number available
def get_volume_cmos(volume):
    return "vol. " + volume

#not needed
def get_issue_cmos(issue):
    return "no. " + issue

def get_pages_cmos(pages):
    return pages

def get_publisher_cmos(publisher):
    return publisher

def get_pubdate_cmos(pubdate):
    if pubdate:
        return pubdate.strftime("%Y")
    else:
        return "n.d."

def get_location_cmos(location):
    return location

#Not needed
def get_accessdate_cmos(accessdate):
    return "Accessed " + accessdate.strftime("%d %b. %Y")
