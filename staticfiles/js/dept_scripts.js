/* ****************************
*	   CHART UTILITIES        *
**************************** */
var getTotal = function(myPieChart) {
	var sum = myPieChart.config.data.datasets[0].data.reduce((a, b) => a + b, 0);
	return sum;
}

var getDatasetLists = function(names, data, color1, color2) {
	var count = data.length;
	var datasetArr = []
	for (var i = 0; i < count; i++) {
		datasetArr[i] = {
			label: names[i],
			data: data[i],
			backgroundColor: color1[i],
			borderColor: color2,
			borderWidth: 2
		}
	}
	return datasetArr;
}

var formatHorizontalBarChartData = function(data, labels) {	
	var len1 = Object.keys(data).length;
	var len2 = labels.length;
	var dataSetInfo = [];
	for (var j = 0; j < len2; j++) {
		var datalist = [];
		for (var k = 0; k < len1; k++) {
			var info = data[k][labels[j]];
			datalist.push(info);
		}
		dataSetInfo.push(datalist);
	}
	return dataSetInfo;
}

var formatHorizontalBarChartData2 = function(data, labels) {	
	var len1 = data.length;
	var len2 = labels.length;
	var dataSetInfo = [];
	for (var j = 0; j < len2; j++) {
		var datalist = [];
		for (var k = 0; k < len1; k++) {
			var info = data[k][j];
			datalist.push(info);
		}
		dataSetInfo.push(datalist);
	}
	return dataSetInfo;
}

function getRandomColorHex() {
	var hex = "0123456789ABCDEF",
		color = "#";
	for (var i = 1; i <= 6; i++) {
		color += hex[Math.floor(Math.random() * 16)];
	}
	return color;
}

function getColorsList(arr) {
	var list = [];
	var count = arr.length;
	for (var i = 0; i < count; i++) {
		var color = getRandomColorHex();
		if (list.includes(color) == false) {
			list.push(color);
		} else {
			count += 1;
		}
	}
	return list;
}

function startCSSurveyGraphsTimeOut() {
	$('#mySpinner1, #mySpinner2, #mySpinner3, #mySpinner4, #mySpinner5, #mySpinner6').addClass('spinner');	
	setTimeout(function(){ 	 	
		$('#mySpinner1, #mySpinner2, #mySpinner3, #mySpinner4, #mySpinner5, #mySpinner6').removeClass('spinner');
		allSurveyCharts();
	}, 1000);
}

function startAttritionChartsTimeOut() {
	$('#mySpinnerA1, #mySpinnerB1, #mySpinnerC1').addClass('spinner');
	setTimeout(function(){ 	 
		$('#mySpinnerA1, #mySpinnerB1, #mySpinnerC1').removeClass('spinner');		
		attritionDeptOnlyCharts();
	}, 1000);
}

function startCompensationChartsTimeOut() {
	$('#mySpinnerA2, #mySpinnerB2, #mySpinnerC2').addClass('spinner');
	setTimeout(function(){ 
		$('#mySpinnerA2, #mySpinnerB2, #mySpinnerC2').removeClass('spinner');
		compensationDeptOnlyCharts();
	}, 1000);
}

function startRelationsChartsTimeOut() {
	$('#mySpinnerA3, #mySpinnerB3').addClass('spinner');
	setTimeout(function(){ 
		$('#mySpinnerA3, #mySpinnerB3').removeClass('spinner');
		relationsDeptOnlyCharts();
	}, 1000);
}

function startRecruitmentChartsTimeOut() {
	$('#mySpinnerA4, #mySpinnerB4').addClass('spinner');
	setTimeout(function(){ 
		$('#mySpinnerA4, #mySpinnerB4').removeClass('spinner');
		recruitmentDeptOnlyCharts();
	}, 1000);
}

function startTalentChartsTimeOut() {
	$('#mySpinnerA5, #mySpinnerB5').addClass('spinner');
	setTimeout(function(){ 
		$('#mySpinnerA5, #mySpinnerB5').removeClass('spinner');
		talentDeptOnlyCharts();
	}, 1000);
}






/* ***********************************
*	   CHART-MAKING FUNCTIONS        *
************************************ */
function pie_graph(graphID, labelList, graphData, labelName, colors, options){
	var ctx = document.getElementById(graphID);
	var myPieChart = new Chart(ctx, {
		type: 'doughnut',
		data: {
			datasets: [{
				data: graphData,
				label: labelName,				
				backgroundColor: colors,
				borderColor: ['#fff'],
				borderWidth: 2
			}],
			labels: labelList
		},
		options: options
	});
}

function line_graph1(graphID, labelList, graphData, labelName, colors){
	var ctx = document.getElementById(graphID);
	var myLineChart = new Chart(ctx, {
		type: 'line',
		data: {
			labels: labelList,
			datasets: [{ 
				data: graphData,
				label: labelName,
				borderColor: colors,
				fill: true
				}, 
			]
		},
		options: lineGraph_options
	});
}

function hbar_graph1(graphID, labelList, graphData, labelNames, bgColors, bColor, options) {
	var ctx = document.getElementById(graphID);
	var myBarChart = new Chart(ctx, {
		type: 'horizontalBar',
		data: {
			labels: labelList,
			datasets: getDatasetLists(labelNames, graphData, bgColors, bColor)
		},
		options: options
	});
}

function hbar_graph2(graphID, labelList, graphData, labelNames, color, options) {
	var ctx = document.getElementById(graphID);
	var myBarChart = new Chart(ctx, {
		type: 'horizontalBar',
		data: {
			labels: labelList,
			datasets: [{
				label: labelNames,
				data: graphData,
				backgroundColor: color,
				borderColor: blue_menu_color,
				borderWidth: 2		
			}]
		},
		options: options
	});
}

function boxplot_graph1(graphID, labelList, graphData, colors, options) {
	var ctx = document.getElementById(graphID);
	var myBoxPlot = new Chart(ctx, {
		type: 'horizontalBoxplot',
		data: {  
			labels: labelList,
			datasets: [{
				label: '',
				data: graphData,
				backgroundColor: colors,
				borderColor: blue_menu_color,
				borderWidth: 2,
				outlierColor: '#999999',
				padding: 10,
				itemRadius: 0,					
			}]
		},
		options: options 
	});

}





/* ****************************
*	COLORS & COLOR SCHEMES    *
**************************** */
var scheme1_colors = ['rgba(153, 51, 51, 0.75)',
					 'rgba(102, 0, 204, 0.75)',
					 'rgba(115, 153, 0, 0.75)',
					 'rgba(255, 159, 64, 0.75)']
					
var scheme2_colors = ['rgba(54, 162, 235, 0.75)',
					 'rgba(226, 211, 87, 0.75)',
					 'rgba(255, 51, 153, 0.75)',
					 'rgba(0, 179, 134, 0.75)']

var scheme3_colors = ['rgba(204, 102, 255, 0.75)',
					 'rgba(210, 210, 45, 0.75)',
					 'rgba(255, 179, 204, 0.75)',
					 'rgba(0, 153, 204, 0.75)']
					 
var scheme4_colors = ['rgba(75, 119, 169, 0.75)',
						'rgba(95, 37, 95, 0.75)',
						'rgba(210, 18, 67, 0.75)',
						'rgba(255, 140, 26, 0.75)',
						'rgba(255, 51, 204, 0.75)',
						'rgba(0, 102, 0, 0.75)',
						'rgba(179, 179, 0, 0.75)']
						
var scheme5_colors = ['rgba(75, 119, 169, 0.75)',
						'rgba(95, 37, 95, 0.75)',
						'rgba(210, 18, 67, 0.75)',
						'rgba(255, 140, 26, 0.75)',
						'rgba(255, 51, 204, 0.75)',
						'rgba(204, 204, 0, 0.75)']						

var satScore_colors = ['rgba(140, 140, 140, 0.75)',
				   'rgba(255, 0, 0, 0.75)',
				   'rgba(115, 153, 0, 0.75)',
				   'rgba(153, 204, 0, 0.75)']

var dissatisfied_color = 'rgba(255, 0, 0, 0.75)'
var unknown_color = 'rgba(140, 140, 140, 0.75)'
var blue_menu_color = 'rgba(33, 170, 234, 0.75)'
var line1_color = '#8e5ea2'





/* *********************************
*	     CHART LABEL NAMES         *
********************************** */
var scoreLabels = ['Unknown', 'Dissatisfied', 'Satisfied', 'Highly Satisfied']
var requestorLabels = ['Interns', 'Regular Staff', 'Non-staff', 'Management']
var raceLabels = ['American Indian or Alaska Native', 'Asian', 'Black or African American', 'Hispanic', 'Two or more races', 'White']
var maritalStatLabels = ['Divorced', 'Married', 'Separated', 'Single', 'Widowed']
var deptLabels = ['Admin Offices', 'Information Systems', 'Production', 'Sales', 'Software Engineering', 'Executive Office']
var genderLabels = ['Male', 'Female']
var perfScoreLabels = ['Not applicable - too early to review', 'Exceptional', '90-day meets', 'Fully Meets', 'Exceeds', 'PIP', 'Needs Improvement']
var hourlyPayLabels = ['Minimum Hourly Pay', 'Middle Hourly Pay', 'Maximum Hourly Pay']
var monthlyLabels2019 = ['January 2019','February 2019','March 2019','April 2019','May 2019','June 2019','July 2019','August 2019','September 2019','October 2019','November 2019','December 2019']





/* ****************************
*	   CHART OPTIONS          *
**************************** */
var donutGraph_options1 = {
	responsive: true,
	maintainAspectRatio: false,
	legend: { display: false },
	tooltips: { enabled: true },		
	plugins: {
		datalabels: {
			formatter: (value, ctx) => {
				let sum = 0;
				let dataArr = ctx.chart.data.datasets[0].data;
				dataArr.map(data => {
					sum += data;
				});
				let percentage = (value * 100/sum).toFixed(0) + "%";
				return percentage;
			},
			color: '#fff',
		},
		doughnutlabel: {
			labels: [
			  {
				text: getTotal,
				font: { size: '35'},
				color: '#ccc'
			  },
			  {
				text: 'TOTAL',
				font: { size: '15'},
				color: '#ccc'
			  },
			]
		}
	}
}

var donutGraph_options2 = {
	responsive: true,
	maintainAspectRatio: false,
	legend: { 
		display: true,
		position: 'top',
		labels: { fontSize: 8 }
	},
	tooltips: { enabled: true },		
	plugins: {
		datalabels: {
			formatter: (value, ctx) => {
				let sum = 0;
				let dataArr = ctx.chart.data.datasets[0].data;
				dataArr.map(data => {
					sum += data;
				});
				let percentage = (value * 100/sum).toFixed(0) + "%";
				return percentage;
			},
			color: '#fff',
		},
		doughnutlabel: {
			labels: [
			  {
				text: getTotal,
				font: { size: '50'},
				color: '#ccc'
			  },
			  {
				text: 'TOTAL',
				font: { size: '20'},
				color: '#ccc'
			  },
			]
		}
	}
}

var donutGraph_options3 = {
	responsive: true,
	maintainAspectRatio: false,
	legend: { 
		display: true,
		position: 'top',
		labels: { fontSize: 8 }
	},
	tooltips: { enabled: true },		
	plugins: {
		datalabels: {
			formatter: (value, ctx) => {
				let sum = 0;
				let dataArr = ctx.chart.data.datasets[0].data;
				dataArr.map(data => {
					sum += data;
				});
				let percentage = (value * 100/sum).toFixed(0) + "%";
				return percentage;
			},
			color: '#fff',
		},
		doughnutlabel: {
			labels: [
			  {
				text: getTotal,
				font: { size: '32'},
				color: '#ccc'
			  },
			  {
				text: 'TOTAL',
				font: { size: '15'},
				color: '#ccc'
			  },
			]
		}
	}
}

var lineGraph_options = {
	responsive: true,
	maintainAspectRatio: false,
	legend: { display: false },
	tooltips: { enabled: true },
    title: { display: false },
	plugins: {
		datalabels: { display: false }
	}
}

var horizStackedBarGraph_options1 = {
	responsive: true,
	maintainAspectRatio: false,
	legend: { 
		display: true,
		position : 'right',
		labels: { fontSize: 9 }				
	},
	plugins: {
		datalabels: { display: false }
	},			
	scales: {
		xAxes: [{ stacked: true }],
		yAxes: [{ stacked: true }]		
	}
}

var horizStackedBarGraph_options2 = {
	responsive: true,
	maintainAspectRatio: false,
	legend: { display: false },
	plugins: {
		datalabels: { display: false }
	},			
	scales: {
		xAxes: [{ stacked: true }],
		yAxes: [{ stacked: true }]		
	}
}

var horizStackedBarGraph_options3 = {
	responsive: true,
	maintainAspectRatio: false,
	legend: { 
		display: true,
		position : 'top',
		labels: { fontSize: 7 }				
	},
	plugins: {
		datalabels: { display: false }
	},			
	scales: {
		xAxes: [{ 
			stacked: true,
			ticks: {  
				beginAtZero: true,
				precision: 1
			} 
		}],
		yAxes: [{ stacked: true }]		
	}
}

var horizStackedBarGraph_options4 = {
	responsive: true,
	maintainAspectRatio: false,
	legend: { 
		display: true,
		position : 'top',
		labels: { fontSize: 7 }				
	},
	plugins: {
		datalabels: { display: false }
	},
	tooltips: { enabled: false },
	scales: {
		xAxes: [{ stacked: true }],
		yAxes: [{ stacked: true }]		
	}
}

var horizBarGraph_options1 = {
	responsive: true,
	maintainAspectRatio: false,
	legend: { display: false },
	plugins: { 
		datalabels: { display: false }
	},			
}

var boxPlot_options1 = {
	responsive: true,
	maintainAspectRatio: false,
	legend: { display: false },
	plugins: { 
		datalabels: { display: false }
	},
	tooltipDecimals: 4,
	title: { display: false }	
}

var boxPlot_options2 = {
	responsive: true,
	maintainAspectRatio: false,
	legend: { display: false },
	plugins: { 
		datalabels: { display: false }
	},
	tooltipDecimals: 2,
	scales: {
		yAxes: [{
			ticks: { fontSize: 10 }
		}]
	},
	title: { display: false }	
}
