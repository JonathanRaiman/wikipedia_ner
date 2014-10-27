class ParsedPage:
	"""
	Stores the content of a parsed page
	"""

	categories = {}

	def __init__(self, name, id):
		"""
		Add a name and an id to a parsed page
		for referencing.
		"""
		self.id      = id
		self.name    = name
		self.lines   = []
		self.parents = set()

	def add_parents(self, parents):
		"""
		Add parents to a parsed page

		Inputs
		------

		parents list : a list of parent ids that correspond to this page

		"""
		for parent, parent_id in parents:
			if ParsedPageParent.categories.get(parent, None):
				parent_page = ParsedPageParent.categories[parent]
			else:
				parent_page = ParsedPageParent(parent, parent_id)
				ParsedPageParent.categories[parent] = parent_page
			
			parent_page.add_child(self.id)


		self.parents.update(parents)