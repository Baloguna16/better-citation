from datetime import datetime, date
import re

def mla_citation(citation_raw, htmlify=True):
    if htmlify == True:
        container_mla = "<i>" + get_container_mla(citation_raw["container"]) + "</i>"
    else:
        container_mla = get_container_mla(citation_raw["container"])

    citation_list = [
        get_author_mla(citation_raw["authors"]),
        get_title_mla(citation_raw["title"]),
        container_mla,
        get_contributor_mla(citation_raw["contributors"]),
        get_publisher_mla(citation_raw["publisher"]),
        get_pubdate_mla(citation_raw["pubdate"]),
        get_location_mla(citation_raw["location"]),
        get_accessdate_mla(citation_raw["accessdate"])
        ]
    citation = [element for element in citation_list if element]
    return ". ".join(citation) + '.'

def research_citation(citation_raw, htmlify=True):
    if htmlify == True:
        block_list = [
            "<i>" + get_container_mla(citation_raw["container"]) + "</i>",
            get_volume_mla(citation_raw["volume"]),
            get_issue_mla(citation_raw["issue"]),
            get_pubdate_mla(citation_raw["pubdate"]),
            get_pages_mla(citation_raw["pages"])
            ]
    else:
        block_list = [
            get_container_mla(citation_raw["container"]),
            get_volume_mla(citation_raw["volume"]),
            get_issue_mla(citation_raw["issue"]),
            get_pubdate_mla(citation_raw["pubdate"]),
            get_pages_mla(citation_raw["pages"])
            ]

    block_mla = ", ".join([element for element in block_list if element])


    citation_list = [
        get_author_mla(citation_raw["authors"]),
        get_title_mla(citation_raw["title"]),
        block_mla,
        get_publisher_mla(citation_raw["publisher"]),
        get_pubdate_mla(citation_raw["pubdate"]),
        get_location_mla(citation_raw["location"]),
        get_accessdate_mla(citation_raw["accessdate"])
        ]
    citation = [element for element in citation_list if element]
    return ". ".join(citation) + '.'

#takes a list of authors
def get_author_mla(authors):
    if authors:
        name = authors[0].split(' ')
        formatted_name = name[-1]
        if len(name) > 1:
            formatted_name += ', '
            for i in range(len(name) - 1):
                formatted_name += ' ' + name[i]

        author_mla = formatted_name
        if len(authors) > 1:
            for i in range(len(authors) - 1):
                author_mla += ', '
                if authors[i + 1] == authors[-1]:
                    author_mla += 'and '
                author_mla += authors[i + 1]
    else:
        author_mla = None
    return author_mla

def get_title_mla(title, is_stand_alone=False):
    if title and is_stand_alone == False:
        title_mla = "\"" + title + "\""
    elif title and is_stand_alone == True:
        title_mla = title #italics
    else:
        title_mla = None
    return title_mla

def get_container_mla(container):
    return container #italics

def get_contributor_mla(contributors):
    contributor_mla = None
    if contributors:
        contributor_mla = "Contribution from " + contributors[0]
        if len(contributors) > 1:
            for i in range(len(contributors) - 1):
                contributor_mla += ', ' + contributors[i + 1]
    return contributor_mla

def get_volume_mla(volume):
    return "vol. " + volume

def get_issue_mla(issue):
    return "no. " + issue

def get_pages_mla(pages):
    return "pp. " + pages

def get_publisher_mla(publisher):
    return publisher

def get_pubdate_mla(pubdate):
    return pubdate.strftime("%d %b. %Y")

def get_location_mla(location):
    return location

def get_accessdate_mla(accessdate):
    return "Accessed " + accessdate.strftime("%d %b. %Y")
