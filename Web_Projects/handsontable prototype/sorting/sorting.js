

var container = document.getElementById('sortable');

var cars = [
	["Honda", 10000, 2013],
	["Toyota", 70000, 2015],
	["Ford", 50000, 2009],
	["Nissan", 20000, 2016]
];

var sortableTable = new Handsontable(container, {
	data: cars,
	rowHeaders: true,
	colHeaders: ["Make", "Mileage", "Year"],
	colWidths: [100, 120, 120],
	columnSorting: true,
	minSpareRows: 1,
	sortIndicator: true
});

console.log("table should have been created");