from collections import Counter
from .pages import ParsedPageChild

class DumpResult:
	"""
	Stores the result of a dump parse.
	Contains the lines observed with their intra wiki links,
	the counters for each article seen,
	and the targets along with a mapping to a unique integer id.
	"""

	def __init__(self):
		"""
		Stores the result of a dump parse.
		Contains the lines observed with their intra wiki links,
		the counters for each article seen,
		and the targets along with a mapping to a unique integer id.
		"""
		self.stored_lines = {}
		self.target_counters = Counter()
		self.targets = {}
		self.index2target = []

	def observe_line(self, line, article_name, links):
		"""
		Adds a set of line to the result by integrating the
		article name, the links, and converting the links to their
		unique ids as stored previously.

		Inputs
		------

		             line list<str> : a list of strings with double bracket
		                              wiki syntax inter wiki links
		           article_name str : the name of the article these links come
		                              from.
		links list<tuple<str, str>> : a pairing of target and anchor text

		"""

		if self.stored_lines.get(article_name, None) == None:

			# get the id of this article:
			if self.targets.get(article_name):
				article_id = self.targets[article_name]
			else:
				article_id = len(self.targets)
				self.targets[article_name] = article_id
				self.index2target.append(article_name)

			page = ParsedPageChild(article_name, article_id)
			self.stored_lines[article_name] = page
		else:
			page = self.stored_lines[article_name]

		page.lines.append(
			(line, list(self.replace_links_with_index(links)))
		)

		page.add_parents([(link[0], self.targets[link[0]]) for link in links if link[0].startswith("Category")])
		self.target_counters.update((link[0] for link in links))

	def replace_links_with_index(self, links):
		"""
		Takes a set of tuples of targets and anchor text and replaces the
		targets by their integer id from the dump result.

		Inputs
		------
		
		links list<tuple<str, str>> : a pairing of target and anchor text

		"""
		for target, anchor in links:
			if self.targets.get(target):
				yield((self.targets[target], anchor))
			else:
				self.targets[target] = len(self.targets)
				self.index2target.append(target)
				yield((self.targets[target], anchor))