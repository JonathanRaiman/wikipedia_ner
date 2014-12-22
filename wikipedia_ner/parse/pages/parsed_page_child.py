from .parsed_page import ParsedPage
from .parsed_page_parent import ParsedPageParent

class ParsedPageChild(ParsedPage):
	"""
	Stores the content of a parsed page. Specialized for
	child pages (that can have parent pages, e.g. categories)
	
	"""
	def __init__(self, *args):
		super().__init__(*args)
		self.lines = []
		self.parents = set()

	def add_parents(self, parents):
		"""
		Add parents to a parsed page

		Inputs
		------

		parents list : a list of parent ids that correspond to this page

		"""
		for parent, parent_id in parents:
			if parent in ParsedPage.categories:
				parent_page = ParsedPage.categories[parent]
			else:
				parent_page = ParsedPageParent(parent, parent_id)
				ParsedPage.categories[parent] = parent_page
			
			parent_page.add_child(self.id)

		self.parents.update([link[1] for link in parents])