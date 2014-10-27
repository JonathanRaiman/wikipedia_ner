from collections import Counter

class ParsedPage:
	"""
	Stores the content of a parsed page
	"""

	categories = {}
	categories_counter = Counter()

	def __init__(self, name, id):
		"""
		Add a name and an id to a parsed page
		for referencing.
		"""
		self.id      = id
		self.name    = name