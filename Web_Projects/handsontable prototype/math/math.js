var container = document.getElementById('mathTable');

var cars = [
	["Honda", 10000, 2013],
	["Toyota", 70000, 2015],
	["Ford", 50000, 2009],
	["Nissan", 20000, 2016],
	["Summary", "=SUM(B1:B4)", "N/A"]
];

var mathTable = new Handsontable(container, {
	data: cars,
	rowHeaders: true,
	colHeaders: ["Make", "Mileage", "Year"],
	colWidths: [100, 120, 120],
	minSpareRows: 1,
	formulas: true
});

console.log("table should have been created");