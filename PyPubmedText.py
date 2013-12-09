import MySQLdb
from Bio import Entrez
from Bio import Medline
import xml.parsers.expat
from cStringIO import StringIO
from ConfigParser import SafeConfigParser
import optparse
import ReadConfig
import sys

class NcbiArticle:
    'Class for PubMed or PMC articles from the local database'
    def __init__(self):
		self.id_ext = '' # PMID or PMCID
		self.source = '' # PubMed or PMC
		self.xml = ''   # the xml format of the article
		self.id_map = '' # only used for the PMC articles
		self.text_title = ''
		self.text_abstract = ''
		self.text_body = ''
		self.journal = ''
		self.id_issn = ''
		self.volume = ''
		self.issue = ''
		self.pages = ''
		self.date = ''
		self.affiliation = ''
		self.authors = '' # define an empty list of authors
		self.pubType = '' # publication type
		self.mesh_terms = ''
		self.supplMesh = ''

    def displayArticle(self):
    	print self.id_ext, self.text_title

    def getText(self):
    	text = self.text_title + self.text_abstract
    	return text

def getArticlesById(idList, articleType, db): 
	cur = db.cursor()

	if cur is None:
		print 'Database connection not valid. Please check'

	tableName = 'shared.articles_medline_2013' # for PubMed articles
	meshTable = 'shared.mesh_medline_2013'
	if articleType == 'pmc': # for PMC articles
		tableName = 'shared.articles_pmc_feb_2013' 
		meshTable = 'shared.mesh_pmc_2013'

	artMap = {}

	cnt = 0
	unicode_cnt = 0

	for id in idList:
		sql = "select * from " + tableName + " where id_ext = '%s';" % id
		
		cur.execute(sql) #execute many queries in a batch
		row = cur.fetchone()

		if row is None:
			continue

		article = NcbiArticle()
		article.xml = row[1]
		article.id_ext = row[2]
		article.source = row[3]
		article.text_title = row[5]
		article.text_abstract = row[6]
		article.text_body = row[7]
		article.pubType = row[9]
		article.authors = row[11]
		article.date = row[12]
		article.journal = row[13]
		article.id_issn = row[14]
		article.volume = row[15]
		article.issue = row[16]
		article.pages = row[17]

		if article.text_abstract is None or len(article.text_abstract) == 0:
			continue

		medline_citation = parseXml(article.xml)

		if medline_citation is not None:
			mesh_terms = getMesh(medline_citation)
			article.mesh_terms = '|'.join(mesh_terms)
			article.supplMesh = '|'.join(getSupplMesh(medline_citation))
			article.affiliation = getAffilication(medline_citation)
		else:
			unicode_cnt = unicode_cnt + 1
			continue

		for k,v in article.__dict__.items():
			if not k.startswith("__"):
				if isinstance(v, unicode):
					setattr(article, k, v.encode('utf-8'))

		artMap[article.id_ext] = article

		cnt = cnt + 1

		if cnt % 100 == 0:
			print cnt, ' records processed.'

	cur.close()

	print unicode_cnt, ' records contains unicode'

	return artMap

def parseXml(xml):
	xml = xml.replace("MedlineCitationSet", "PubmedArticle")
	xml = xml.replace('<?xml version="1.0" encoding="UTF-8"?>', '<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE PubmedArticleSet PUBLIC "-//NLM//DTD PubMedArticle, 1st May 2013//EN" "http://www.ncbi.nlm.nih.gov/corehtml/query/DTD/pubmed_130501.dtd">')

	try:
		handle = StringIO(xml)
		medline_citation = Entrez.read(handle) #There is only one citation record

		return medline_citation
	except:
		return None

def getMesh(medline_citation):
	mesh_terms = []

	if 'MeshHeadingList' not in medline_citation['MedlineCitation']:
		return mesh_terms

	mesh_list = medline_citation['MedlineCitation']['MeshHeadingList']
	
	for mesh in mesh_list:
		descriptor = mesh['DescriptorName']
		major1 = descriptor.attributes['MajorTopicYN']
		descriptorName = descriptor

		qualiferNames = []
		major2 = {}

		for qualifer in mesh['QualifierName']:
			if len(qualifer) > 0:
				major2[qualifer] = qualifer.attributes['MajorTopicYN']
				qualiferNames.append(qualifer)

		if len(qualiferNames) > 0 :
			for qualiferName in qualiferNames:
				mesh_term = descriptorName + '/' + qualiferName
				if major2[qualiferName] == 'Y':
					mesh_term = mesh_term + '*'
				mesh_terms.append(mesh_term)

		else:
			mesh_term = descriptorName
			if major1 == 'Y':
				mesh_term = mesh_term + '*'
			mesh_terms.append(mesh_term)

	return mesh_terms

def getSupplMesh(medline_citation):
	supplMesh = []

	if 'SupplMeshList' not in medline_citation['MedlineCitation']:
		return supplMesh

	supplMeshList = medline_citation['MedlineCitation']['SupplMeshList']

	for supplMeshEle in supplMeshList:
		supplMeshType = supplMeshEle.attributes['Type']
		supplMesh.append(supplMeshEle + '[%s]' % supplMeshType)

	return supplMesh

def getAffilication(medline_citation):
	affiliation = ''

	if 'Affiliation' not in medline_citation['MedlineCitation']['Article']:
		return ''
	else:
		return medline_citation['MedlineCitation']['Article']['Affiliation']

def getArticlesFromPubmed(idList):
	artMap = {}
	batch_size = 200

	cnt = 0

	#[seq[start:start + 20] for start in range(0, len(seq), 20)]

	for sublist in [idList[start:start + batch_size] for start in range(0, len(idList), batch_size)]:
		#Now retrieving the articles from PubMed (using PMIDs in the sublist)

		Entrez.email = "chengkun.wu@manchester.ac.uk"
		handle=Entrez.efetch(db='pubmed',id=sublist, retmode='xml')

		records = Entrez.read(handle)

		for record in records:
			'''
			for absEle in record["MedlineCitation"]["Article"]["Abstract"]["AbstractText"]:
				print absEle.encode('utf-8').strip()
			'''

			if 'MedlineCitation' not in record:
				continue

			articleEle = record["MedlineCitation"]["Article"]
			article = NcbiArticle()
			pmid = record["MedlineCitation"]["PMID"]
			article.id_ext = pmid
			article.mesh_terms = '|'.join(getMesh(record))
			article.supplMesh = '|'.join(getSupplMesh(record))

			article.text_title = articleEle["ArticleTitle"].encode('utf-8')
			article.text_abstract = ''

			if 'Abstract' in articleEle:
				for absEle in articleEle["Abstract"]["AbstractText"]:
					article.text_abstract = article.text_abstract + absEle.encode('utf-8').strip()


			article.pubType = '|'.join(articleEle["PublicationTypeList"])
			
			if 'Affiliation' in articleEle:
				article.affiliation = articleEle['Affiliation'].encode('utf-8')

			#print article.pubType

			if 'AuthorList' in articleEle:
				authors = []
				#print articleEle['AuthorList']
				for author in articleEle['AuthorList']:

					if 'CollectiveName' in author:
						authorName = author['CollectiveName']
					else:
						lastName = ''
						foreName = ''
						initials = ''
						if 'LastName' in author:
							lastName = author['LastName']

						if 'ForeName' in author:
							foreName = author['ForeName']

						if 'Initials' in author:
							initials = author['Initials']

						authorName = ' '.join([lastName, foreName])

					authors.append(authorName)

				article.authors = '|'.join(authors).encode('utf-8')

			journalEle = articleEle['Journal']

			if 'ISSN' in journalEle:
				journalISSN = journalEle['ISSN']

			journalIssueEle = journalEle['JournalIssue']
			journalTitle = journalEle['Title'].encode('utf-8')

			article.journal = journalTitle
			article.id_issn = journalISSN

			if 'Volume' in journalIssueEle:			
				article.volume = journalIssueEle['Volume']

			if 'Issue' in journalIssueEle:
				article.issue = journalIssueEle['Issue']

			if 'ArticleDate' in articleEle:
				articleDate = articleEle['ArticleDate']
				dateStr = ''
				if len(articleDate) > 0:
					# articleDate is a single element list
					year = articleDate[0]['Year']
					month = articleDate[0]['Month']
					day = articleDate[0]['Day']
					dateStr = '-'.join([year, month, day])
				else:
					dateStr = '-'.join(journalIssueEle['PubDate'].values())
			else:
				
				#month = journalIssueEle['PubDate']['Month']
				#Some articles don't have 'Month', they have 'Season'
				dateStr = '-'.join(journalIssueEle['PubDate'].values())

			article.date = dateStr

			article.pages = articleEle['Pagination']['MedlinePgn']

			artMap[pmid] = article
			
			cnt = cnt + 1

			if cnt % 100 == 0:
				print cnt, 'records fetched from PubMed'
		
	print len(artMap), 'records fetched from PubMed in total.'
	return artMap

def insert2DB(artMap, db):
	insert_cnt = 0
	supplMesh_cnt = 0
	dbCur = db.cursor()

	if dbCur is None:
		print 'Database connection not valid. Please check'

	for pmid in artMap.keys():
		article = artMap[pmid]


		insert_sql = """REPLACE into prj_mjkijcw2.tc_text(id_ext, text_title, text_body, xml, text_abstract, authors, date, article_type, mesh_terms, journal, affiliation) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)"""

		try:
			dbCur.execute(insert_sql, (article.id_ext, article.text_title, article.text_body, article.xml, article.text_abstract, article.authors, article.date, article.pubType, article.mesh_terms, article.journal, article.affiliation))
		except e:
			print e.strerr
			print 'Error-causing document ID:', pmid
			exit(-1)

		insert_cnt = insert_cnt + 1

		if insert_cnt % 100 == 0:
			print insert_cnt, 'records inserted'

		supplMesh = article.supplMesh

		if len(supplMesh) > 0:
			#Need to insert to a different table
			supplMesh_sql = 'REPLACE INTO prj_mjkijcw2.tc_supplmesh(id_ext, supplMesh) values(%s,%s)'
			dbCur.execute(supplMesh_sql, (pmid, supplMesh))
			supplMesh_cnt = supplMesh_cnt + 1
	dbCur.close()

	print supplMesh_cnt, 'supplementary concepts found'

	print 'Insert2DB finished!'

def rebuildCorpus(corpus, db):
	pmidList = []

	if type(corpus).__name__ == 'list':
		pmidList = corpus
	if type(corpus).__name__ == 'str':
		pmidList = [line.strip() for line in open(corpus)]

	#Clear the corpus first
	if db is None:
		print 'You need to have a valid DB connection first!'
		return
	else:
		print 'Now rebuilding the thyroid cancer corpus'
	
	dbCur = db.cursor()

	clear_sql = "delete from prj_mjkijcw2.tc_corpus"
	dbCur.execute(clear_sql)
	print 'Corpus table cleared. '

	clear_sql = "delete from prj_mjkijcw2.tc_text"
	dbCur.execute(clear_sql)
	print 'Thyroid cancer text table cleared'

	for pmid in pmidList:
		insert_sql = "insert into prj_mjkijcw2.tc_corpus (id_ext) values(\'%s\')" % pmid
		dbCur.execute(insert_sql)

	print len(pmidList), 'records inserted to the thyroid cancer corpus'

	dbCur.close()

	print 'Now fetching PubMed articles, from local DB first'

	dbArtMap = getArticlesById(pmidList, 'pubmed', db)
	noAbstractList = []
	print len(dbArtMap), 'articles fetched from local database'

#Insert
	insert2DB(dbArtMap, db)

	print 'Now fetching directly from PubMed'
	waitList = []

	for pmid in set(pmidList) ^ set(dbArtMap.keys()):
		waitList.append(pmid)

	print len(waitList), 'articles to be fetched from PubMed'
	artMap = getArticlesFromPubmed(waitList)
	insert2DB(artMap, db)

if __name__ == "__main__":
	(corpus, dbConfig) = ReadConfig.config(sys.argv)

	db = MySQLdb.connect(host=dbConfig['dbHost'], # your host, usually localhost
		 user=dbConfig['dbUser'], # your username
		  passwd=dbConfig['dbPass'] , # your password
		  db=dbConfig['dbSchema'], 
		  charset=dbConfig['dbCharset'], 
		  use_unicode=dbConfig['dbUnicode']) # name of the data base

	print 'Database connected.'

	rebuildCorpus(corpus, db)

	db.close()
