import requests
from bs4 import BeautifulSoup
from datetime import datetime, date
import re

import format.mla as mla
import format.cmos as cmos

#TODO: create a citation from manual inputs
class ManualCitation:
    def __init__(self, form):
        self.author_first = form.author_first.data
        self.author_sur = form.author_sur.data
        self.title = form.title.data
        self.container = form.container.data
        self.contributor_first = form.contributor_first.data
        self.contributor_sur = form.contributor_sur.data
        self.version = form.version.data
        self.number = form.number.data
        self.publisher = form.publisher.data
        self.date_published = form.pubdate.data
        self.location = form.location.data
        self.date_accessed = form.accessdate.data

    def __repr__(self):
        return '<ManualCitation {}>'.format(self.title)

    def get_author(self):
        if self.author_first and self.author_sur:
            author = [self.author_first + " " + self.author_sur]
        elif self.author_first:
            author = [self.author_first]
        elif self.author_sur:
            author = [self.author_sur]
        else:
            author = None
        return author

    def get_title(self):
        if self.title:
            return self.title
        else:
            return None

    def get_container(self):
        return self.container

    def get_contributor(self):
        if self.contributor_first and self.contributor_sur:
            contributor = [self.contributor_first + " " + self.contributor_sur]
        elif self.contributor_first:
            contributor = [self.contributor_first]
        elif self.contributor_sur:
            contributor = [self.contributor_sur]
        else:
            contributor = None
        return contributor

    def get_version(self):
        return self.version

    def get_number(self):
        return self.number

    def get_publisher(self):
        return self.publisher

    def get_pubdate(self):
        return self.date_published

    def get_location(self):
        return self.location

    def get_accessdate(self):
        return self.date_accessed

def create_citation_manual(form, style="mla"):
    manual_citation = ManualCitation(form)

    citation_raw = {
        "authors" : manual_citation.get_author(),
        "title" : manual_citation.get_title(),
        "container" : manual_citation.get_container(),
        "contributors" : manual_citation.get_contributor(),
        "version" : manual_citation.get_version(),
        "number" : manual_citation.get_number(),
        "publisher" : manual_citation.get_publisher(),
        "pubdate" : manual_citation.get_pubdate(),
        "location" : manual_citation.get_location(),
        "accessdate" : manual_citation.get_accessdate()
        }
    if style == "mla":
        return mla.mla_citation(citation_raw, htmlify=True)
    elif style == "cmos":
        return cmos.cmos_citation(citation_raw, htmlify=True)
    else:
        return None
