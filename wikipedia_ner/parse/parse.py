from epub_conversion import convert_wiki_to_lines
from epub_conversion.wiki_decoder import almost_smart_open
from .utils import line_converter
from .dump_result import DumpResult, DumpResultSqlite

def parse_dump(path, sqlite= False, commit_frequency = 300, sqlite_path="out.db", max_articles = 1000, report_every = 100, clear_output = False):
	"""
	Convert a dump to a set of articles with their
	text tokenized and the intrawiki links separated and
	matched with the corresponding sentences.
	Also creates a unique id over the articles for better
	memory footprint (though overall this script is probably
	notoriously bad at its memory management)
	

	Inputs
	------
	        path str : the location of the wiki
	                   dump (bz2 or xml file).
	max_articles int : the number of [valid] articles
	                   to be read before stopping

	
	Output
	------
	result DumpResult : the result of the parse.

	"""
	if sqlite:
		result = DumpResultSqlite(sqlite_path)
	else:
		result = DumpResult()
	wiki = almost_smart_open(path)

	for line, article_name, links in convert_wiki_to_lines(
		wiki,
		max_articles = max_articles,
		clear_output = clear_output,
		report_every = report_every,
		line_converter = line_converter):
			result.observe_line(line, article_name, links)

	if sqlite:
		# flush out any remaining pieces to put in the db.
		result.update_db()

	return result