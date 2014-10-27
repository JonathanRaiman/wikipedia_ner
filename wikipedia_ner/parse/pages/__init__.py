"""
Module for Container classes useful for storing metadata
and graph relations within the wiki stored in a wiki dump.

"""

from .parsed_page import ParsedPage
from .parsed_page_child import ParsedPageChild
from .parsed_page_parent import ParsedPageParent

__all__ = ["ParsedPage", "ParsedPageChild", "ParsedPageParent"]