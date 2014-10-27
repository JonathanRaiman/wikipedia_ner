from .parsed_page import ParsedPage

class ParsedPageParent(ParsedPage):
	"""
	Stores the content of a parsed page. Specialized for
	parent pages (that can have children pages, e.g. leaves
	/ articles)
	
	"""

	def __init__(self, *args):
		super().__init__(*args)
		self.children = set()

	def add_child(self, child):
		"""
		Register a new child for a category
		"""
		self.children.add(child)
		ParsedPage.categories_counter.update([self.name])