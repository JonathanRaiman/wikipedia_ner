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

		if article_name in self.stored_lines:
			page = self.stored_lines[article_name]
		else:
			# get the id of this article:
			if article_name in self.targets:
				article_id = self.targets[article_name]
			else:
				article_id = len(self.targets)
				self.targets[article_name] = article_id
				self.index2target.append(article_name)

			page = ParsedPageChild(article_name, article_id)
			self.stored_lines[article_name] = page

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
			if target in self.targets:
				yield((self.targets[target], anchor))
			else:
				self.targets[target] = len(self.targets)
				self.index2target.append(target)
				yield((self.targets[target], anchor))

import sqlite3
from .sqlite_utils import create_schema
import pickle

sqlite3.register_converter("pickle", pickle.loads)
sqlite3.register_adapter(list, pickle.dumps)
sqlite3.register_adapter(set, pickle.dumps)

class DumpResultSqlite(DumpResult):
	def __init__(self, sqlite_path, commit_frequency = 50):
		self.sqlite_path = sqlite_path
		self.sqlite_conn = sqlite3.connect(
			sqlite_path,
			detect_types=sqlite3.PARSE_DECLTYPES)

		insert_into_db, update_in_db, get_obj_from_db = create_schema(
			self.sqlite_conn,
			[
				("lines", "pickle"),
				("parents", "pickle")
			],
			"articles")

		self.insert_into_db = insert_into_db
		self.update_in_db = update_in_db
		self.get_obj_from_db = get_obj_from_db

		self.commit_frequency = commit_frequency
		self.to_insert = {}
		self.to_insert_parents = {}
		self.to_update = {}
		self.to_update_parents = {}
		DumpResult.__init__(self)

	def should_save_to_db(self):
		return (
			(len(self.to_insert)         > self.commit_frequency) or \
			(len(self.to_insert_parents) > self.commit_frequency) or \
			(len(self.to_update)         > self.commit_frequency) or \
			(len(self.to_update_parents) > self.commit_frequency))

	def update_db(self):
		insert_keys = list(self.to_insert.keys())

		for key in insert_keys:
			# create a new saved copy in the db:
			self.insert_into_db(
				(
					self.targets[key],
					self.to_insert[key],
					self.to_insert_parents[key]
				)
			)
			self.stored_lines[key] = True
			del self.to_insert[key]
			del self.to_insert_parents[key]

		update_keys = list(self.to_update.keys())

		for key in update_keys:
			object_id = self.targets[key]
			# get previous saved copy:
			old_key, lines, parents = self.get_obj_from_db(object_id)

			# update that copy
			self.update_in_db(
				(
					object_id,
					lines + self.to_update[key],
					parents.update( self.to_update_parents[key] )
				)
			)
			del self.to_update[key]
			del self.to_update_parents[key]

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

		if article_name in self.stored_lines:
			# remember whether the page exists in the db:

			if article_name not in self.to_update:
				self.to_update[article_name] = []
				self.to_update_parents[article_name] = set()
			
			self.to_update[article_name].append(
				(line, list(self.replace_links_with_index(links)))
			)
			cat_links = [self.targets[link[0]] for link in links if link[0].startswith("Category")]

			if len(cat_links) > 0:
				self.to_update_parents[article_name].update(
					cat_links
				)

		else:
			# get the id of this article:
			if article_name in self.targets:
				article_id = self.targets[article_name]
			else:
				article_id = len(self.targets)
				self.targets[article_name] = article_id
				self.index2target.append(article_name)

			if article_name not in self.to_insert:
				self.to_insert[article_name] = []
				self.to_insert_parents[article_name] = set()

			self.to_insert[article_name].append(
				(line, list(self.replace_links_with_index(links)))
			)
			cat_links = [self.targets[link[0]] for link in links if link[0].startswith("Category")]
			if len(cat_links) > 0:
				self.to_insert_parents[article_name].update(
					cat_links
				)

			self.target_counters.update((link[0] for link in links))

		if self.should_save_to_db():
			self.update_db()