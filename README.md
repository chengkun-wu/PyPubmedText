PyPubmedText
============

A python wrapper for fetching Pubmed articles


If you are doing biomedical text-mining using MEDLINE abstracts or PMC articles, you might often want to build a corpus of your own. You can maintain a local copy of the MEDLINE baseline. The baseline is updated on yearly bases. You might also want to retrieve the latest. PyPubmedText is a wrapper for such purposes. It's based on the Entrez package of Biopython. 

== 2013-12-09

1. Fix the bug brought about by unicode. The solution is to check whether a string is in unicode or not, if so, then .encode('utf-8').
2. DB cursors are opened and close within each function.
3. Take commandline arguments for corpus file name and database connection details.
4. Added ReadConfig module for the configuration in 3. 
5. PyPubmedText can be imported and used as a module


== 2013-12-05

For the moment, PyPubmedText takes a corpus file (of PMIDs) and it fetches articles first from the local database and then try to communicate with Pubmed if some are missing from the local database. All retrieved information will be stored into a dictionary (PMID as the key, a NcbiArticle object for article information)
