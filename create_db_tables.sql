CREATE TABLE `articles_medline_2013` (
  `id_art` int(10) unsigned NOT NULL auto_increment,
  `xml` longtext collate utf8_bin,
  `id_ext` varchar(255) collate utf8_bin NOT NULL,
  `source` enum('medline','pmc','elsevier','text','other') collate utf8_bin NOT NULL,
  `date_inserted` datetime NOT NULL,
  `text_title` varchar(4096) collate utf8_bin default NULL,
  `text_abstract` mediumtext collate utf8_bin,
  `text_body` longtext collate utf8_bin,
  `text_raw` mediumtext collate utf8_bin,
  `text_raw_type` enum('xml','ocr','pdf2text','text') collate utf8_bin default NULL,
  `article_type` enum('research','review','other') collate utf8_bin default NULL,
  `authors` mediumtext collate utf8_bin,
  `year` varchar(255) collate utf8_bin default NULL,
  `journal` varchar(255) collate utf8_bin default NULL,
  `id_issn` varchar(255) collate utf8_bin default NULL,
  `volume` varchar(255) collate utf8_bin default NULL,
  `issue` varchar(255) collate utf8_bin default NULL,
  `pages` varchar(255) collate utf8_bin default NULL,
  PRIMARY KEY  (`id_art`),
  KEY `index_issn` (`id_issn`),
  KEY `index_type` (`article_type`),
  KEY `index_id_ext` USING BTREE (`id_ext`),
  KEY `index_src` (`source`),
  KEY `yearIdx` (`year`),
  KEY `type` (`article_type`)
) ENGINE=MyISAM AUTO_INCREMENT=21478362 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

CREATE TABLE `articles_pmc_feb_2013` (
  `id_art` int(10) unsigned NOT NULL auto_increment,
  `xml` longtext collate utf8_bin,
  `id_ext` varchar(255) collate utf8_bin NOT NULL,
  `source` enum('medline','pmc','elsevier','text','other') collate utf8_bin NOT NULL,
  `date_inserted` datetime NOT NULL,
  `text_title` varchar(4096) collate utf8_bin default NULL,
  `text_abstract` mediumtext collate utf8_bin,
  `text_body` longtext collate utf8_bin,
  `text_raw` mediumtext collate utf8_bin,
  `text_raw_type` enum('xml','ocr','pdf2text','text') collate utf8_bin default NULL,
  `article_type` enum('research','review','other') collate utf8_bin default NULL,
  `authors` mediumtext collate utf8_bin,
  `year` varchar(255) collate utf8_bin default NULL,
  `journal` varchar(255) collate utf8_bin default NULL,
  `id_issn` varchar(255) collate utf8_bin default NULL,
  `volume` varchar(255) collate utf8_bin default NULL,
  `issue` varchar(255) collate utf8_bin default NULL,
  `pages` varchar(255) collate utf8_bin default NULL,
  PRIMARY KEY  (`id_art`),
  KEY `index_issn` (`id_issn`),
  KEY `index_type` (`article_type`),
  KEY `index_id_ext` USING BTREE (`id_ext`),
  KEY `index_src` (`source`),
  KEY `yearIdx` (`year`),
  KEY `type` (`article_type`),
  KEY `index_journal` (`journal`)
) ENGINE=MyISAM AUTO_INCREMENT=584709 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

CREATE TABLE `mesh_medline_2013` (
  `document` varchar(127) NOT NULL,
  `descriptor` varchar(127) NOT NULL,
  `qualifier` varchar(127) default NULL,
  `major` tinyint(1) NOT NULL,
  KEY `document` (`document`),
  KEY `descriptor` (`descriptor`),
  KEY `qualifier` (`qualifier`),
  KEY `major` (`major`),
  KEY `mesh_index` (`document`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

CREATE TABLE `mesh_pmc_2013` (
  `pmcid` varchar(255) NOT NULL,
  `pmid` varchar(127) NOT NULL,
  `descriptor` varchar(127) NOT NULL,
  `qualifier` varchar(127) default NULL,
  `major` tinyint(1) NOT NULL,
  KEY `pmcid_index` (`pmcid`),
  KEY `pmid_index` (`pmid`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

CREATE TABLE `table_text` (
  `id_ext` varchar(256) NOT NULL,
  `text_title` text,
  `text_body` text,
  `xml` text,
  `text_abstract` text,
  `authors` text,
  `date` mediumtext,
  `article_type` mediumtext,
  `mesh_terms` mediumtext,
  `journal` mediumtext,
  `affiliation` text,
  PRIMARY KEY  (`id_ext`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

CREATE TABLE `table_corpus` (
  `id_ext` varchar(30) NOT NULL,
  `title_type` varchar(200) default NULL,
  `article_type` varchar(200) default NULL,
  PRIMARY KEY  (`id_ext`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

CREATE TABLE `table_supplmesh` (
  `id_ext` varchar(50) NOT NULL,
  `SupplMesh` text,
  PRIMARY KEY  (`id_ext`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
