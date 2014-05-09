// ---------------------------------------------------------------------------------------
// Script Name: XML Quiz Converter
// Description: A Javascript/jQuery converter which reads the old PD XML quiz format and
//              outputs HTML code that can be copied and pasted into Blox (or anywhere). 
//              Requires the path to the quiz's directory in MDS.
//      Author: Josh Renaud
//     Version: 0.1
//        Date: 2011-03-27
// ---------------------------------------------------------------------------------------


var judgmentImg = '';
var quesType = [];
var quesNum = 0;
var score = 0;
var totalQuestions = 0;
var scoringResponse = '';
var scoringRangeSize = 0;
var scoringRange = [];
var scoringEvaluation = [];
var basePath = '';
var credits ='';


function outputCode(snippet) {
	$('#codeOutput').val($('#codeOutput').val()+snippet);
	}


// grab the quiz.xml file and generate the HTML

function parseXml(xml) {

	$(xml).find('quiz').each(function() {
		totalQuestions = $(this).attr('totalQuestions');
		judgmentImg = $(this).attr('judgment');
		credits = $(this).attr('credits');
		});

	outputCode('<link rel="stylesheet" type="text/css" href="http://images.stltoday.com/mds/00003409/content/style.css" />\r');
	outputCode('<div id="quiz">\r');
	outputCode('\t<div class="spinningWheel"><span>The quiz is loading</span></div>\r');


	for (x=0; x<totalQuestions; x++) {
		$(xml).find('question'+x).each(function() {


			// Figure out what sort of question this is
			quesType[x] = $(this).find('type').text();

			// ==== MULTIPLE PHOTOS =====

			if (quesType[x] === 'multiple 2x2') {
				var question = $(this).find('question').text();
				var answer0 = $(this).find('answer0').text();
				var answer1 = $(this).find('answer1').text();
				var answer2 = $(this).find('answer2').text();
				var answer3 = $(this).find('answer3').text();
				var answerPhoto0 = $(this).find('answerPhoto0').text();
				var answerPhoto1 = $(this).find('answerPhoto1').text();
				var answerPhoto2 = $(this).find('answerPhoto2').text();
				var answerPhoto3 = $(this).find('answerPhoto3').text();
				var response = $(this).find('response').text();
				outputCode('\t<div class="questions multiphoto" id="question'+x+'">\r');
				outputCode('\t\t<div class="photos">\r');
				outputCode('\t\t\t<img id="ques'+x+'pho0" class="correct" src="'+basePath+answerPhoto0+'" />\r');
				outputCode('\t\t\t<img id="ques'+x+'pho1" class="wrong" src="'+basePath+answerPhoto1+'" />\r');
				outputCode('\t\t\t<img id="ques'+x+'pho2" class="wrong" src="'+basePath+answerPhoto2+'" />\r');
				outputCode('\t\t\t<img id="ques'+x+'pho3" class="wrong" src="'+basePath+answerPhoto3+'" />\r');
				outputCode('\t\t</div>\r');
				outputCode('\t\t<div class="question">' +question+ '</div>\r');
				outputCode('\t\t<div class="answers">\r');
				outputCode('\t\t\t<div class="answerLine"><input type="radio" class="correct" value="correct" id="ques'+x+'ans0" name="ques'+x+'" /><label for="ques'+x+'ans0">'+answer0+'</label></div>\r');
				outputCode('\t\t\t<div class="answerLine"><input type="radio" class="wrong" value="wrong" id="ques'+x+'ans1" name="ques'+x+'" /><label for="ques'+x+'ans1">'+answer1+'</label></div>\r');
				outputCode('\t\t\t<div class="answerLine"><input type="radio" class="wrong" value="wrong" id="ques'+x+'ans2" name="ques'+x+'" /><label for="ques'+x+'ans2">'+answer2+'</label></div>\r');
				outputCode('\t\t\t<div class="answerLine"><input type="radio" class="wrong" value="wrong" id="ques'+x+'ans3" name="ques'+x+'" /><label for="ques'+x+'ans3">'+answer3+'</label></div>\r');
				outputCode('\t\t</div>\r');
				outputCode('\t\t<div class="response"><span class="answeredWrong">Wrong.</span><span class="answeredCorrect">Right.</span> '+response+'</div>\r');
				outputCode('\t</div>\r');
			}

			// ==== MULTIPLE CHOICE =====

			else if (quesType[x] === 'multiple choice') {
				var question = $(this).find('question').text();
				var answer0 = $(this).find('answer0').text();
				var answer1 = $(this).find('answer1').text();
				var answer2 = $(this).find('answer2').text();
				var answer3 = $(this).find('answer3').text();
				var answerPhoto0 = $(this).find('answerPhoto0').text();
				var response = $(this).find('response').text();
				outputCode('\t<div class="questions multichoice" id="question'+x+'">\r');
				outputCode('\t\t<div class="photos">\r');
				outputCode('\t\t\t<img id="ques'+x+'pho0" class="layer correct" src="'+basePath+answerPhoto0+'" />\r');
				outputCode('\t\t</div>\r');
				outputCode('\t\t<div class="question">' +question+ '</div>\r');
				outputCode('\t\t<div class="answers">\r');
				outputCode('\t\t\t<div class="answerLine"><input type="radio" class="correct" value="correct" id="ques'+x+'ans0" name="ques'+x+'" /><label for="ques'+x+'ans0">'+answer0+'</label></div>\r');
				outputCode('\t\t\t<div class="answerLine"><input type="radio" class="wrong" value="wrong" id="ques'+x+'ans1" name="ques'+x+'" /><label for="ques'+x+'ans1">'+answer1+'</label></div>\r');
				outputCode('\t\t\t<div class="answerLine"><input type="radio" class="wrong" value="wrong" id="ques'+x+'ans2" name="ques'+x+'" /><label for="ques'+x+'ans2">'+answer2+'</label></div>\r');
				outputCode('\t\t\t<div class="answerLine"><input type="radio" class="wrong" value="wrong" id="ques'+x+'ans3" name="ques'+x+'" /><label for="ques'+x+'ans3">'+answer3+'</label></div>\r');
				outputCode('\t\t</div>\r');
				outputCode('\t\t<div class="response"><span class="answeredWrong">Wrong.</span><span class="answeredCorrect">Right.</span> '+response+'</div>\r');
				outputCode('\t</div>\r');
			}

			// ==== TRUE / FALSE =====

			else if (quesType[x] === 'true/false') {
				var question = $(this).find('question').text();
				var answerPhoto0 = $(this).find('answerPhoto0').text();
				var answer0 = $(this).find('answer0').text();
				var response = $(this).find('response').text();
				var trueLabel  = $(this).find('trueLabel').text();
				var falseLabel = $(this).find('falseLabel').text();

				if (answer0 === 'true') { 
					var answerValue0 = 'correct';
					var answerValue1 = 'wrong';
				}
				else { 
					var answerValue0 = 'wrong';
					var answerValue1 = 'correct';
				}
				outputCode('\t<div class="questions truefalse" id="question'+x+'">\r');
				outputCode('\t\t<div class="photos">\r');
				outputCode('\t\t\t<img id="ques'+x+'pho0" class="layer correct" src="'+basePath+answerPhoto0+'" />\r');
				outputCode('\t\t</div>\r');
				outputCode('\t\t<div class="question">' +question+ '</div>\r');
				outputCode('\t\t<div class="answers">\r');
				outputCode('\t\t\t<div class="answerLine"><input type="radio" class="'+answerValue0+'" value="'+answerValue0+'" id="ques'+x+'ans0" name="ques'+x+'" /><label for="ques'+x+'ans0">'+trueLabel+'</label></div>\r');
				outputCode('\t\t\t<div class="answerLine"><input type="radio" class="'+answerValue1+'" value="'+answerValue1+'" id="ques'+x+'ans1" name="ques'+x+'" /><label for="ques'+x+'ans1">'+falseLabel+'</label></div>\r');
				outputCode('\t\t</div>\r');
				outputCode('\t\t<div class="response"><span class="answeredWrong">Wrong.</span><span class="answeredCorrect">Right.</span> '+response+'</div>\r');
				outputCode('\t</div>\r');
			}

		});
	}

	// ==== SCORING SCREEN ====

	$(xml).find('scoring').each(function() {
		scoringResponse = $(this).attr('scoringResponse');
		// strip out a few things hardcoded into most of these responses
		scoringResponse = scoringResponse.replace('<br><br><br>','');
		scoringResponse = scoringResponse.replace('target="_blank"','');
		scoringResponse = scoringResponse.replace('class = "linkStyle"','');
	});
	outputCode('\t<div id="scoring">\r');
	outputCode('\t\t<div class="photos"><img id="judgment" src="'+basePath+judgmentImg+'" /></div>\r')
	outputCode('\t\t<div id="response">'+scoringResponse+'</div>\r');
	outputCode('\t</div>\r'); // close #scoring
	outputCode('</div>\r'); // close #quiz
	outputCode('<div id="credits"><strong>CREDITS:</strong> '+credits+'</div>\r');


	// ==== "FOOTER" JAVASCRIPT/CSS LINKS ====

	// no longer need to include jquery. Reader will use the jquery included on stltoday template
//	outputCode('<script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.5.1/jquery.min.js"></script>\r');
	outputCode('<script type="text/javascript">\r');
	outputCode('\tvar totalQuestions = ' +totalQuestions+ ';\r');
	outputCode('\tvar scoringRange = [];\r');
	outputCode('\tvar scoringEvaluation = [];\r');

	$(xml).find('scoring').each(function() {
		scoringRangeSize = $(this).children().size();
		for (x=scoringRangeSize-1; x>=0; x--) {
			scoringRange[x] = $(this).children().eq(x).text();
			scoringEvaluation[x] = $(this).children().eq(x).attr('evaluation');
			// gotta watch out for double quote marks, so use regex
			// The /g flag tells it to match all instances of "
			scoringEvaluation[x] = scoringEvaluation[x].replace(/"/g,'\'');
			outputCode('\tscoringRange['+x+'] = '+scoringRange[x]+';\r');
			outputCode('\tscoringEvaluation['+x+'] = "'+scoringEvaluation[x]+'";\r');
		}
//		outputCode('\tvar quesType = [];\r');
//		for (x=0; x<totalQuestions; x++) {
//			outputCode('\tquesType['+x+'] = "'+quesType[x]+'";\r');
//		}
//		outputCode('\tvar hasFlash = false;\r');
		outputCode('</script>\r');
	});

	outputCode('<script type="text/javascript" src="http://images.stltoday.com/mds/00003409/content/quizReader.js"></script>\r');

}






$(document).ready(function() {

	basePath = prompt("Enter quiz's MDS directory (include a trailing slash)");

	$('#codeOutput').val('');

	$.ajax({
		type: "GET",
		url: basePath+"quiz.xml",
		dataType: "xml",
		success: parseXml
	});


});
