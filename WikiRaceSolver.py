#!/usr/bin/python2
import urllib2, argparse
from urlparse import urlparse
from BeautifulSoup import BeautifulSoup

class WikiSolver:
	excludeWikiPrefix = ('Wikipedia:', 'Special:', 'Talk:', 'Category:', 'Help:', 'Portal:', 'File:', 'List_')
	urlPrefix = '/wiki/'
	def __init__(self):
		args = self.parser()
		self.source = args.source
		self.target = args.target
		self.max = int(args.max)
		
		solve = self.solve(self.source, self.max)
		if not solve: print 'Not Found Solve'
		else:
			for step in solve:
				print step
			
	def parser(self):
		# get arguments
		parser = argparse.ArgumentParser(description='Slove Wikipedia Race')
		parser.add_argument('source', help = 'source page in the race')
		parser.add_argument('target', help = 'target page in the race')
		parser.add_argument('-m', '--max', required = True, help = 'maximum steps', const = int, nargs ='?')
		return parser.parse_args()
		
	def getPage(self, url):
		# get page from url
		url = self.fullUrl(url)
		req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"}) 
		page = urllib2.urlopen(req).read()
		return page
	
	def getLinks(self, page):
		# get links from html page
		soup = BeautifulSoup(page)
		linksList = []
		for a in soup.findAll('a'):
			link = a.get('href')
			if not link is None and link.startswith(self.urlPrefix) and not link[len(self.urlPrefix):].startswith(self.excludeWikiPrefix) and not link in linksList: 
				linksList.append(link)
		return linksList
		
	def getName(self, url):
		# get name from url
		return url.rpartition('/')[2]
	
	def fullUrl(self, url):
		if url.startswith('http'): return url
		if not hasattr(self, 'wikipediaUrl'):
			urlparser = urlparse(self.source)
			self.wikipediaUrl = 'http://' + urlparser.hostname
		return self.wikipediaUrl + url
		
	def getLinksFromUrl(self, url):
		page = self.getPage(url)
		return self.getLinks(page)
			
	def solve(self, url, stepsLeft, stepsList = []):
		if self.getName(url) == self.getName(self.target):
			stepsList.append(self.getName(url))
			return stepsList
		elif stepsLeft == 0: 
			return False
		else:
			linksList = self.getLinksFromUrl(url)
			for link in linksList:
				mySteps = list(stepsList)
				mySteps.append(self.getName(url))
				steps = self.solve(link, stepsLeft - 1, mySteps)
				if steps: return steps
			return False

wiki = WikiSolver()
