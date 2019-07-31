
// Load Navigation
$( "#navigation" ).load( "navigation.html " );

$( document ).ready(function() {

    var standardGraphWidth = 580;
    var standardGraphHeight = 400;
     
    resizeGraph()
    
	// Zusatzfilter ausblenden
	$("#passwordOptionsMask").fadeToggle(0);
	$(".addMetaFields").fadeToggle(0);
    $("h1#finalScoreH1").html("-");
    $("h3#subScoreHS").html("-");
    $("h3#subScoreAM").html("-");
    $("h3#subScoreBF").html("-");
    $("h3#subScorePB").html("-");
    
    calcHeuristicLmin();
    calcAMMaxExample();
    
    $('.scoreNormalizationArea').toggle();
    $('.scoreLevelFusionArea').toggle();
    $('.scoreTrainingArea').toggle();
    $('.scoreStrengthArea').toggle();
	
	
	$( ".showIncludeIngredient" ).click(function() {
		$("#passwordOptionsMask").fadeToggle();
		$(".addMetaFields").fadeToggle();
        
	});

    

	//
	// "Search" button pressed
	//
	$('#searchButton').click(function(){
    
        var ugh = parseFloat($('.number-spinner-ugh-value').val().trim())|| 180;
        var ogh = parseFloat($('.number-spinner-ogh-value').val().trim())|| 1.5;
        var scoreLevelDic = parseFloat($('.fustionScoreDic').val().trim())|| 0.3;
        var scoreLevelBF = parseFloat($('.fustionScoreBF').val().trim()) || 0.3;
        var scoreLevelAM = parseFloat($('.fustionScoreAM').val().trim())|| 0.2;
        var scoreLevelHS = parseFloat($('.fustionScoreHS').val().trim())|| 0.2;
        var scoreStrengthBFN = parseFloat($('.strengthBFN').val().trim())|| 94;
        var scoreStrengthBFNOGMAX = parseFloat($('.strengthBFNOGMAX').val().trim()) || 100000000;
        var scoreStrengthBFTMAX = parseFloat($('.strengthBFTMAX').val().trim()) || 32140800;
        var scoreStrengthAMMAX = parseFloat($('.strengthAMMAX').val().trim()) || 4;
        
        var areaDicValue = $('.areaDicValue').val();
        var areaAMValue = $('.areaAMValue').val();
        var areaHSValue = $('.areaHSValue').val();

        
        
        test ={ ugh: ugh , ogh:ogh, scoreLevelDic:scoreLevelDic,scoreLevelBF:scoreLevelBF, scoreLevelAM:scoreLevelAM,scoreLevelHS:scoreLevelHS,scoreStrengthBFN:scoreStrengthBFN,scoreStrengthBFNOGMAX:scoreStrengthBFNOGMAX,scoreStrengthBFTMAX:scoreStrengthBFTMAX,scoreStrengthAMMAX:scoreStrengthAMMAX,areaDicValue:areaDicValue,areaAMValue:areaAMValue,areaHSValue:areaHSValue };
         $.ajax({
            type: 'POST',
            url: 'write_ini.php',
            
            data: test,
            success: function (data) {

            }
        }).done(function() {
            $("#finalScoreH1").html('<i class="fa fa-spinner fa-spin score-spin" style="font-size:54px"></i>');
            $("#subScoreHS").html('<i class="fa fa-spinner fa-spin score-spin" style="font-size:32px"></i>');
            $("#subScoreAM").html('<i class="fa fa-spinner fa-spin score-spin" style="font-size:32px"></i>');
            $("#subScoreBF").html('<i class="fa fa-spinner fa-spin score-spin" style="font-size:32px"></i>');
            $("#subScorePB").html('<i class="fa fa-spinner fa-spin score-spin" style="font-size:32px"></i>');
        
            $('#searchButton').prop( "disabled", true );
            password = $('#passwordSearch').val();
            $.ajax({
                    type: 'POST',
                    url: 'score.php',
                    data: { pwd_param: password },
                    success: function (data) {
                        $('#searchButton').prop( "disabled", false );
                        obj = $.parseJSON(data);
                    //$('h1#finalScoreH1').animateNumber({number: obj['final_score'].toFixed(2),color: 'green',easing: 'easeInQuad',},1500);
                        $("#finalScoreH1").html(obj['final_score'].toFixed(1));
                        $("#subScoreHS").html(obj['hs_score'].toFixed(2));
                        $("#subScoreAM").html(obj['am_score'].toFixed(2));
                        $("#subScoreBF").html(obj['bf_score'].toFixed(2));
                        $("#subScorePB").html(obj['pwb_score'].toFixed(2));
                    }
            });
        });
    
    

	});
		
	//
	// Return pressed
	//
    $('#titelsearch').keypress(function(e) {
        if (e.keyCode == '13') {
            alert('enter');
        }
    });
    
    

	
    //
	// UGH Spinner
	//
    $(document).on('click', '.number-spinner-ugh button', function () {
        var btn = $(this),
        oldValue = btn.closest('.number-spinner-ugh').find('input').val().trim(),
        newVal = 0;
        if (btn.attr('data-dir') == 'up') {
            newVal = parseInt(oldValue) + 10;
        } else {
            if (oldValue > 1) {
                newVal = parseInt(oldValue) - 10;
            } else {
                newVal = 1;
            }
        }
        btn.closest('.number-spinner-ugh').find('input').val(newVal.toFixed(2));
        
        var ugh = parseInt($('.number-spinner-ugh-value').val().trim());
        var ogh = parseFloat($('.number-spinner-ogh-value').val().trim());

        updateGraph(ugh,ogh, standardGraphWidth,standardGraphHeight);
    });

    //
	// OGH Spinner
	//
    $(document).on('click', '.number-spinner-ogh button', function () {
        var btn = $(this),
        oldValue = btn.closest('.number-spinner-ogh').find('input').val().trim(),
        newVal = 0;
        if (btn.attr('data-dir') == 'up') {
            newVal = parseFloat(oldValue) + 0.1;
        } else {
            if (oldValue > 0) {
                newVal = parseFloat(oldValue) - 0.1;
            } else {
                newVal = 0;
            }
        }

        btn.closest('.number-spinner-ogh').find('input').val(newVal.toFixed(2));
        var ugh = parseInt($('.number-spinner-ugh-value').val().trim());
        var ogh = parseFloat($('.number-spinner-ogh-value').val().trim());

        updateGraph(ugh,ogh, standardGraphWidth,standardGraphHeight);
        
    });



    $(document).on('change', '.btn-group input#scoreDetails[type="checkbox"]', function () {
        $('.scoreDetailsArea').toggle();
    });

    $(document).on('change', '.btn-group input#scoreNormalization[type="checkbox"]', function () {
        $('.scoreNormalizationArea').toggle();
    });
    
    $(document).on('change', '.btn-group input#scoreLevelFusion[type="checkbox"]', function () {
        $('.scoreLevelFusionArea').toggle();
    });
    
    $(document).on('change', '.btn-group input#scoreTraining[type="checkbox"]', function () {
        $('.scoreTrainingArea').toggle();
    });
    
    $(document).on('change', '.btn-group input#scoreStrength[type="checkbox"]', function () {
        $('.scoreStrengthArea').toggle();
    });
    
    
    //
    // Resize Window - Paint Graph new
    //
    $( window ).resize(function() {
        resizeGraph();
    });
    
    $( ".strengthBFN" ).keyup(function() {
        calcHeuristicLmin();
    });
    
    $( ".strengthBFNOGMAX" ).keyup(function() {
        calcHeuristicLmin();
    });
    
    $( ".strengthBFTMAX" ).keyup(function() {
        calcHeuristicLmin();
    });
        
    $( ".strengthAMMAX" ).keyup(function() {
        calcAMMaxExample();
    });
        
});



function calcAMMaxExample(){
        var text = "<br>";
        
        for (i = 0; i < ("ananas".length-parseInt($( ".strengthAMMAX" ).val())+1); i++) {
            text += "→ "+ "ananas".substr(i, $( ".strengthAMMAX" ).val())+ "<br>";
        }
        if ("ananas".length <= parseInt($( ".strengthAMMAX" ).val())){
            text += "ananas";
        }
        $('.adaptiveWordSplit').html(text);
}

function resizeGraph(){
    var ugh = parseInt($('.number-spinner-ugh-value').val().trim());
    var ogh = parseFloat($('.number-spinner-ogh-value').val().trim());
    if ($(window).width() < 580) {
        standardGraphWidth = 350
        standardGraphHeight = 233
        updateGraph(ugh,ogh, standardGraphWidth,standardGraphHeight);
    }
    else{
        standardGraphWidth = 580
        standardGraphHeight = 400
        updateGraph(ugh,ogh, standardGraphWidth,standardGraphHeight);
    }
}

function calcHeuristicLmin(){
    var N = parseInt($('.strengthBFN').val().trim());
    var Nogmax = parseInt($('.strengthBFNOGMAX').val().trim());
    var Tmax = parseInt($('.strengthBFTMAX').val().trim());
    var lmin = (Math.log(Nogmax*Tmax)/Math.log(N));
    $('h4#strengthBFResult').html(lmin.toFixed(2) + " → " + Math.ceil(lmin));

};

function updateGraph(ugh,ogh,width,height){
    var options = {
//    title: 'Hampel tanh Normalization',
    target: '#quadratic',
    width: width,
    height: height,
    tip: {
    xLine: true,    // dashed line parallel to y = 0
    yLine: true,    // dashed line parallel to x = 0
    renderer: function (x, y, index) {
        // the returning value will be shown in the tip
    }
    },

    disableZoom: true,
    xAxis: {
    label: 'x - axis',
    domain: [-1, 400]
    },
    yAxis: {
    label: 'y - axis',
    domain: [-1, 11]
    },
    data: [{
           fn: '5*(tanh(0.01*(x-'+ugh+')/'+ogh+')+1)',
           }]
    };
    
    functionPlot(options)

}
