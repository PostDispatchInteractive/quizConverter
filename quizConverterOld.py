import re
from xml.dom import minidom
import xml.etree.ElementTree as ET
import os
import inspect
import tkFileDialog
from io import StringIO
import urllib2

# ---------------------------------------------------------------------------------------
# Script Name: XML Quiz Converter
# Description: A Javascript/jQuery converter which reads the old PD XML quiz format and
#              outputs HTML code that can be copied and pasted into Blox (or anywhere). 
#              Requires the path to the quiz's directory in MDS.
#      Author: Josh Renaud
#     Version: 0.1
#        Date: 2011-03-27
# ---------------------------------------------------------------------------------------




def cleanText(text) :
	if text is not None:
		# If it's not unicode already, make it unicode.
		if not isinstance(text, unicode):
			# ElementTree turns everything into UTF-8, so that's why I have utf-8 here.
			text = unicode(text, 'utf-8')
		text = text.strip()
		# Change single letter Yes/No into the full word
		# Converts curly quotes to straight. Also converts ellipses and dashes.
		# adapted from: http:#www.therothefamily.com/blog/entry/textexpander-smarten-straighten-quotes
		text = re.sub(ur'\u2018', u"'", text)
		text = re.sub(ur'\u2019', u"'", text)
		text = re.sub(ur'\u201c', u'"', text)
		text = re.sub(ur'\u201d', u'"', text)
		text = re.sub(ur'\u2010|\u2011|\u2012|\u2013', u"-", text)
		text = re.sub(ur'\u2014', u"--", text)
		text = re.sub(ur'\u2026', u"...", text)
		text = text.strip()
	return text



# define line endings
# Windows: \r\n  |   Mac/Unix: \n
eol = '\n'


# CHARACTER ENCODING NOTES
# Here are the ways you can save this file and have InDesign properly recognize it:
#
# <UNICODE-MAC>
# Use utf-16 encoding, \n line endings, and \u2018 style characters.
# This is probably the best way. Any stray special characters will be properly parsed.
#
# <UNICODE-WIN>
# Use utf-16 encoding, \r\n line endings, and \u2018 style characters.
#
# <ASCII-WIN>
# Use utf-8 encoding, \r\n line endings, and <0x2018> style characters.
# This is the way I have done it in the past. Problem is if users enter special characters
# you haven't anticipated and replaced with <0xXXXX>, then they show up garbled on the page.



def outputText(tt, text):
	if text is not None:
		try:
			text = text.encode('utf-8')
		except Warning, e:
			print e + ' | ' + text
		tt.write(text)

def outputList(tt, quizName, credits, mdsId, url):
	tt.write(quizName + '\t' + credits + '\t' + mdsId + '\t' + url + eol)

def outputBad(tt, mdsId, url):
	tt.write(mdsId + '\t' + url + eol)


def parseXml(xml,basePath,mdsId) :
	tree = ET.ElementTree(ET.fromstring(xml))
	root = tree.getroot()
	questions = {}

	# Top of the quiz stuff
	quizName = root.get('name')
	totalQuestions = root.get('totalQuestions')
	judgmentImg = root.get('judgment')

	# Some quizzes misspelled the judgment element
	if not judgmentImg:
		judgmentImg = root.get('judgement')
	credits = root.get('credits')
	coverPhoto = root.get('titleScreen')

	# Some quizzes didn't have a name
	if quizName is not None:
		quizName = re.sub(r'[^\s\w-]','',quizName)
		quizName = re.sub(r'[\s]','-',quizName).lower()
		quizName = re.sub(r'^the-','',quizName).lower()
		outputFile = r'M:\My Documents\GitHub\quizConverter\converted\\' + quizName + '.html'
	else:
		print 'No name'
		return False
		#quizName = str(mdsId)
		#outputFile = r'M:\My Documents\GitHub\quizConverter\converted' + quizName + '.html'

	tt = open(outputFile,'wb')
	print quizName

	outputText(tt, '<link rel="stylesheet" type="text/css" href="http://images.stltoday.com/mds/00003409/content/style-old-version.css" charset="utf-8" />' + eol)
	outputText(tt, '<div id="quiz">' + eol)
	outputText(tt, '\t<div class="spinningWheel"><span>The quiz is loading</span></div>' + eol)

	# Output quiz cover, if there is one
	if coverPhoto is not None:
		outputText(tt, '\t<div class="cover">' + eol)
		outputText(tt, '\t\t<img id="quizCover" src="' + basePath + coverPhoto + '" alt="' + quizName + '" />' + eol)
		outputText(tt, '\t</div>' + eol)
		outputText(tt, '\t<div id="playButton" class="joshButtons"><span>Play!</span></div>' + eol)

	# Check if this quiz uses SWFs or FLA or other weird formats
	firstQuestion = root.find('question0')
	answerImgType = firstQuestion.find('answerPhoto0').text
	answerImgType = answerImgType[-3:].lower()
	# If this is a SWF or something, we need to stop.
	if answerImgType not in { 'jpg', 'gif', 'png' }:
		print answerImgType
		return False

	# Iterate over all questions and scoring
	for question in root:
		tag = question.tag
		# Is this a question element?
		if tag[0:7] == 'questio':
			x = tag[8:10].strip()
			quesType = question.find('type').text

			# ==== MULTIPLE PHOTOS =====
			if (quesType == 'multiple 2x2'):
				questionText = cleanText( question.find('question').text )
				answer0 = cleanText( question.find('answer0').text )
				answer1 = cleanText( question.find('answer1').text )
				answer2 = cleanText( question.find('answer2').text )
				answer3 = cleanText( question.find('answer3').text )
				answerPhoto0 = question.find('answerPhoto0').text
				answerPhoto1 = question.find('answerPhoto1').text
				answerPhoto2 = question.find('answerPhoto2').text
				answerPhoto3 = question.find('answerPhoto3').text
				response = cleanText( question.find('response').text )
				if response is None:
					response = ''
				outputText(tt, '\t<div class="questions multiphoto" id="question'+x+'">' + eol)
				outputText(tt, '\t\t<div class="photos">' + eol)
				outputText(tt, '\t\t\t<img id="ques'+x+'pho0" class="correct" src="'+basePath+answerPhoto0+'" />' + eol)
				outputText(tt, '\t\t\t<img id="ques'+x+'pho1" class="wrong" src="'+basePath+answerPhoto1+'" />' + eol)
				outputText(tt, '\t\t\t<img id="ques'+x+'pho2" class="wrong" src="'+basePath+answerPhoto2+'" />' + eol)
				outputText(tt, '\t\t\t<img id="ques'+x+'pho3" class="wrong" src="'+basePath+answerPhoto3+'" />' + eol)
				outputText(tt, '\t\t</div>' + eol)
				outputText(tt, '\t\t<div class="question">' +questionText+ '</div>' + eol)
				outputText(tt, '\t\t<div class="answers">' + eol)
				outputText(tt, '\t\t\t<div class="answerLine"><input type="radio" class="correct" value="correct" id="ques'+x+'ans0" name="ques'+x+'" /><label for="ques'+x+'ans0">'+answer0+'</label></div>' + eol)
				outputText(tt, '\t\t\t<div class="answerLine"><input type="radio" class="wrong" value="wrong" id="ques'+x+'ans1" name="ques'+x+'" /><label for="ques'+x+'ans1">'+answer1+'</label></div>' + eol)
				outputText(tt, '\t\t\t<div class="answerLine"><input type="radio" class="wrong" value="wrong" id="ques'+x+'ans2" name="ques'+x+'" /><label for="ques'+x+'ans2">'+answer2+'</label></div>' + eol)
				outputText(tt, '\t\t\t<div class="answerLine"><input type="radio" class="wrong" value="wrong" id="ques'+x+'ans3" name="ques'+x+'" /><label for="ques'+x+'ans3">'+answer3+'</label></div>' + eol)
				outputText(tt, '\t\t</div>' + eol)
				outputText(tt, '\t\t<div class="response"><span class="answeredWrong">Wrong.</span><span class="answeredCorrect">Right.</span> '+response+'</div>' + eol)
				outputText(tt, '\t</div>' + eol)

			# ==== MULTIPLE CHOICE =====
			elif (quesType == 'multiple choice'):
				questionText = cleanText( question.find('question').text )
				answer0 = cleanText( question.find('answer0').text )
				answer1 = cleanText( question.find('answer1').text )
				answer2 = cleanText( question.find('answer2').text )
				answer3 = cleanText( question.find('answer3').text )
				answerPhoto0 = question.find('answerPhoto0').text
				response = cleanText( question.find('response').text )
				if response is None:
					response = ''
				outputText(tt, '\t<div class="questions multichoice" id="question'+x+'">' + eol)
				outputText(tt, '\t\t<div class="photos">' + eol)
				outputText(tt, '\t\t\t<img id="ques'+x+'pho0" class="layer correct" src="'+basePath+answerPhoto0+'" />' + eol)
				outputText(tt, '\t\t</div>' + eol)
				outputText(tt, '\t\t<div class="question">' +questionText+ '</div>' + eol)
				outputText(tt, '\t\t<div class="answers">' + eol)
				outputText(tt, '\t\t\t<div class="answerLine"><input type="radio" class="correct" value="correct" id="ques'+x+'ans0" name="ques'+x+'" /><label for="ques'+x+'ans0">'+answer0+'</label></div>' + eol)
				outputText(tt, '\t\t\t<div class="answerLine"><input type="radio" class="wrong" value="wrong" id="ques'+x+'ans1" name="ques'+x+'" /><label for="ques'+x+'ans1">'+answer1+'</label></div>' + eol)
				outputText(tt, '\t\t\t<div class="answerLine"><input type="radio" class="wrong" value="wrong" id="ques'+x+'ans2" name="ques'+x+'" /><label for="ques'+x+'ans2">'+answer2+'</label></div>' + eol)
				outputText(tt, '\t\t\t<div class="answerLine"><input type="radio" class="wrong" value="wrong" id="ques'+x+'ans3" name="ques'+x+'" /><label for="ques'+x+'ans3">'+answer3+'</label></div>' + eol)
				outputText(tt, '\t\t</div>' + eol)
				outputText(tt, '\t\t<div class="response"><span class="answeredWrong">Wrong.</span><span class="answeredCorrect">Right.</span> '+response+'</div>' + eol)
				outputText(tt, '\t</div>' + eol)

			# ==== TRUE / FALSE =====
			elif (quesType == 'true/false'):
				questionText = cleanText( question.find('question').text )
				answerPhoto0 = cleanText( question.find('answerPhoto0').text )
				answer0 = question.find('answer0').text
				response = cleanText( question.find('response').text )
				if response is None:
					response = ''
				#trueLabel  = cleanText( question.find('trueLabel').text )
				trueLabel  = 'true'
				#falseLabel = cleanText( question.find('falseLabel').text )
				falseLabel = 'false'

				if (answer0 == 'true'):
					answerValue0 = 'correct'
					answerValue1 = 'wrong'
				else:
					answerValue0 = 'wrong'
					answerValue1 = 'correct'

				outputText(tt, '\t<div class="questions truefalse" id="question'+x+'">' + eol)
				outputText(tt, '\t\t<div class="photos">' + eol)
				outputText(tt, '\t\t\t<img id="ques'+x+'pho0" class="layer correct" src="'+basePath+answerPhoto0+'" />' + eol)
				outputText(tt, '\t\t</div>' + eol)
				outputText(tt, '\t\t<div class="question">' +questionText+ '</div>' + eol)
				outputText(tt, '\t\t<div class="answers">' + eol)
				outputText(tt, '\t\t\t<div class="answerLine"><input type="radio" class="'+answerValue0+'" value="'+answerValue0+'" id="ques'+x+'ans0" name="ques'+x+'" /><label for="ques'+x+'ans0">'+trueLabel+'</label></div>' + eol)
				outputText(tt, '\t\t\t<div class="answerLine"><input type="radio" class="'+answerValue1+'" value="'+answerValue1+'" id="ques'+x+'ans1" name="ques'+x+'" /><label for="ques'+x+'ans1">'+falseLabel+'</label></div>' + eol)
				outputText(tt, '\t\t</div>' + eol)
				outputText(tt, '\t\t<div class="response"><span class="answeredWrong">Wrong.</span><span class="answeredCorrect">Right.</span> '+response+'</div>' + eol)
				outputText(tt, '\t</div>' + eol)


		# No, this is not a question element. Is it the scoring element?

		# ==== SCORING SCREEN =====
		elif tag[0:7] == 'scoring':

			scoringResponse = cleanText( question.get('scoringResponse') )
			if scoringResponse:
				# strip out a few things hardcoded into most of these responses
				scoringResponse = scoringResponse.replace('<br><br><br>','');
				scoringResponse = scoringResponse.replace('target="_blank"','');
				scoringResponse = scoringResponse.replace('class = "linkStyle"','');
				scoringResponse = scoringResponse.replace('   >','>');
			else:
				scoringResponse = ''
	
			outputText(tt, '\t<div id="scoring">' + eol)
			outputText(tt, '\t\t<div class="photos"><img id="judgment" src="'+basePath+judgmentImg+'" /></div>' + eol)
			outputText(tt, '\t\t<div id="response">'+scoringResponse+'</div>' + eol)
			outputText(tt, '\t</div>' + eol) # close div#scoring
			outputText(tt, '</div>' + eol) # close div#quiz
			outputText(tt, '<div id="credits"><strong>CREDITS:</strong> '+credits+'</div>' + eol)

			# ==== "FOOTER" JAVASCRIPT/CSS LINKS ====
			outputText(tt, '<script type="text/javascript">' + eol)
			outputText(tt, '\tvar totalQuestions = ' +totalQuestions+ ';' + eol)
			outputText(tt, '\tvar scoringRange = [];' + eol)
			outputText(tt, '\tvar scoringEvaluation = [];' + eol)

			x = 0
			for scoringRangeElem in question:
				scoringRange = scoringRangeElem.text
				scoringEvaluation = cleanText( scoringRangeElem.get('evaluation') )
				# gotta watch out for double quote marks, so use regex
				scoringEvaluation = scoringEvaluation.replace(r'"','\'')
				outputText(tt, '\tscoringRange[' + str(x) + '] = ' + scoringRange + ';' + eol)
				outputText(tt, '\tscoringEvaluation[' + str(x) + '] = "' + scoringEvaluation + '";' + eol)
				x += 1
			outputText(tt, '</script>' + eol)

	# Generally don't want to include jQuery, since the site template has it already.
	#outputText(tt, '<script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js" charset="utf-8"></script>' + eol)

	outputText(tt, '<script type="text/javascript" src="http://images.stltoday.com/mds/00003409/content/quizReader.js" charset="utf-8"></script>' + eol)

	# Clean up the title and credits for outputting our TSV
	quizTitle = quizName.replace('-',' ').title()
	replacements = [
		#('',''),
		('Quiz design by ',''),
		(' | STLtoday.com',''),
		('Quiz by ',''),
		('Programming by ',''),
		('programming by ',''),
		('Quiz written and designed by ',''),
		('design by ',''),
		('Compiled by: ',''),
		('&#xD;','')
	]
	for key, replacement in replacements:
		credits = credits.replace(key, replacement)
	outputList(quizList, quizTitle, credits, mdsId, basePath)

	tt.close()

	return True




listFile = r'M:\My Documents\GitHub\quizConverter\converted\\quiz-list.txt'
quizList = open(listFile,'wb')
quizList.write('Quiz\tCredits\tMDS ID\tURL' + eol)

badFile = r'M:\My Documents\GitHub\quizConverter\converted\\quiz-bad.txt'
badList = open(badFile,'wb')

# quiz.xml missing (probably alternative formats)
# 2718, 2216, 2014, 1998, 1894, 1893, 1865, 1855, 1850, 1828, 1795, 1787, 1786, 1777, 1760, 1748, 1702, 1670, 1660, 1631, 1624, 1553, 1552

# well formated
# 1891, 1898, 1903, 1931, 1946, 1994, 2028, 2029, 2030, 2040, 2048, 2089, 2094, 2101, 2105, 2108, 2114, 2115, 2130, 2133, 2141, 2145, 2163, 2182, 2185, 2187, 2197, 2202, 2209, 2222, 2229, 2232, 2235, 2240, 2250, 2253, 2290, 2292, 2296, 2299, 2305, 2312, 2330, 2331, 2335, 2343, 2344, 2346, 2363, 2364, 2366, 2375, 2381, 2393, 2406, 2424, 2449, 2451, 2470, 2487, 2501, 2508, 2517, 2518, 2519, 2523, 2525, 2526, 2527, 2531, 2535, 2538, 2539, 2589, 2597, 2601, 2602, 2604, 2606, 2623, 2628, 2645, 2658, 2666, 2672, 2675, 2676, 2692, 2696, 2704, 2705, 2709, 2719, 2722, 2728, 2729, 2737, 2742, 2752, 2755, 2776, 2779, 2803, 2809, 2810, 2813, 2817, 2818, 2820, 2825, 2826, 2827, 2830, 2837, 2844, 2854, 2869, 2870, 2875, 2876, 2880, 2881, 2884, 2885, 2894, 2910, 2921, 2924, 2930, 2940, 2942, 2944, 2946, 2948, 2949, 2950, 2951, 2952, 2957, 2961, 2982, 2983, 3009, 3010, 3025, 3027, 3030, 3032, 3033, 3036, 3038, 3050, 3054, 3059, 3060, 3074, 3077, 3130, 3132, 3136, 3137, 3138, 3143, 3145, 3167, 3171, 3184, 3185, 3194, 3205, 3206, 3207, 3208, 3216, 3219, 3220, 3221, 3224, 3225, 3226, 3231, 3233, 3235, 3236, 3239, 3242, 3243, 3246, 3249

quizzes = [1891, 1898, 1903, 1931, 1946, 1994, 2028, 2029, 2030, 2040, 2048, 2089, 2094, 2101, 2105, 2108, 2114, 2115, 2130, 2133, 2141, 2145, 2163, 2182, 2185, 2187, 2197, 2202, 2209, 2222, 2229, 2232, 2235, 2240, 2250, 2253, 2290, 2292, 2296, 2299, 2305, 2312, 2330, 2331, 2335, 2343, 2344, 2346, 2363, 2364, 2366, 2375, 2381, 2393, 2406, 2424, 2449, 2451, 2470, 2487, 2501, 2508, 2517, 2518, 2519, 2523, 2525, 2526, 2527, 2531, 2535, 2538, 2539, 2589, 2597, 2601, 2602, 2604, 2606, 2623, 2628, 2645, 2658, 2666, 2672, 2675, 2676, 2692, 2696, 2704, 2705, 2709, 2719, 2722, 2728, 2729, 2737, 2742, 2752, 2755, 2776, 2779, 2803, 2809, 2810, 2813, 2817, 2818, 2820, 2825, 2826, 2827, 2830, 2837, 2844, 2854, 2869, 2870, 2875, 2876, 2880, 2881, 2884, 2885, 2894, 2910, 2921, 2924, 2930, 2940, 2942, 2944, 2946, 2948, 2949, 2950, 2951, 2952, 2957, 2961, 2982, 2983, 3009, 3010, 3025, 3027, 3030, 3032, 3033, 3036, 3038, 3050, 3054, 3059, 3060, 3074, 3077, 3130, 3132, 3136, 3137, 3138, 3143, 3145, 3167, 3171, 3184, 3185, 3194, 3205, 3206, 3207, 3208, 3216, 3219, 3220, 3221, 3224, 3225, 3226, 3231, 3233, 3235, 3236, 3239, 3242, 3243, 3246, 3249]

for quiz in quizzes:
	mdsPath = 'http://images.stltoday.com/mds/0000'
	mdsId = str(quiz)
	basePath = mdsPath + mdsId + '/content/'
	url = basePath + 'quiz.xml'

	f = urllib2.urlopen(url)
	if f:
		# Read 
		xml = f.read()
		f.close()

		# Remove opening whitespace which otherwise invalidates the xml.
		xml = xml.strip()			

		# If the top of the quiz is not a <quiz> element, it's likely a BOM.
		# That means we need to convert to UTF-8
		if xml[0:3] != '<qu':
			print xml[0:3]
			xml = xml.decode('utf-16')
			xml = xml.encode('utf-8')

		# Change curly quotes to straight quotes
		xml = re.sub(r'&amp;#8217',"'",xml)

		# Change any stray ampersands that are NOT part of html entities into &amp;
		xml = re.sub(r'&(?!(?:[a-z]+|#[0-9]+|#x[0-9a-f]+);)','&amp;',xml)

		print url

		# Run the quiz parser
		parsed = parseXml(xml,basePath,mdsId)

		# If the parser failed for any reason, add the quiz number to the bad quiz list.
		# Reasons it might fail: No title; use of SWFs.
		if parsed is False:
			outputBad(badList, mdsId, basePath)

quizList.close()