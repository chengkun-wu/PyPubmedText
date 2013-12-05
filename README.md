PyPubmedText
============

A python wrapper for fetching Pubmed articles


If you are doing biomedical text-mining using MEDLINE abstracts or PMC articles, you might often want to build a corpus of your own. You can maintain a local copy of the MEDLINE baseline. The baseline is updated on yearly bases. You might also want to retrieve the latest. PyPubmedText is a wrapper for such purposes. It's based on the Entrez package of Biopython. 


== 2013-12-05
For the moment, PyPubmedText takes a corpus file (of PMIDs) and it fetches articles first from the local database and then try to communicate with Pubmed if some are missing from the local database. All retrieved information will be stored into a dictionary (PMID as the key, a NcbiArticle object for article information)
