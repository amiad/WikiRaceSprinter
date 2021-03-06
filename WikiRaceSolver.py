#!/usr/bin/python2
import urllib2, argparse
from urlparse import urlparse
from BeautifulSoup import BeautifulSoup

class WikiSolver:
	excludeWikiPrefix = ('Wikipedia:', 'Special:', 'Talk:', 'Category:', 'Help:', 'Portal:', 'File:', 'List_', 'Template:', 'Template_talk:', 'User:',
						)
	urlPrefix = '/wiki/'
	def __init__(self):
		args = self.parser()
		self.source = args.source
		self.target = args.target
		self.max = int(args.max)
		self.file = args.file if args.file is not None else False
		self.verbose = args.verbose

		if not self.file:
			self.scannedLinks = set()
		else:
			self.scannedLinks = set(item.strip() for item in self.file)

		solve = self.solve(self.source, self.max)
		if self.verbose: print("*****")
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
		parser.add_argument('-f', '--file', help = 'file for resume', type = argparse.FileType('a+'))
		parser.add_argument('-v', '--verbose', help = 'print progress', action = "store_true")
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
			if not link is None and link.startswith(self.urlPrefix) and not self.getName(link).startswith(self.excludeWikiPrefix) and not self.getName(link) in self.scannedLinks and not link in linksList:
				linksList.append(link)
		return linksList

	def getName(self, url):
		# get name from url
		name = url.rpartition('/')[2]
		name = name.partition('#')[0] # remove anchor
		return name

	def fixName(self, name): # not work
		name = urllib2.unquote(name)
		return name

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
		if self.verbose:
			print(str(len(self.scannedLinks)) + ": " + self.getName(url))

		if self.getName(url) == self.getName(self.target):
			stepsList.append(self.getName(url))
			return stepsList
		elif self.getName(url) in stepsList:
			return False
		elif stepsLeft == 0:
			return False
		else:
			linksList = self.getLinksFromUrl(url)
			for link in linksList:
				mySteps = list(stepsList)
				mySteps.append(self.getName(url))
				self.addScannedLinks(link)
				steps = self.solve(link, stepsLeft - 1, mySteps)
				if steps: return steps
			return False

	def addScannedLinks(self, link):
		name = self.getName(link)
		self.scannedLinks.add(name)
		if self.file:
			self.file.write(name + "\n")
			self.file.flush()

wiki = WikiSolver()
