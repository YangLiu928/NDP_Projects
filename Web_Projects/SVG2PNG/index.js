var express = require('express');
var app = express();
var fs = require('pn/fs');
var svg2png = require('svg2png');
var shortid = require('shortid');
var bodyParser = require('body-parser');
app.use(bodyParser.json({limit: '50mb'}));
app.use(bodyParser.urlencoded({limit: '50mb', extended: true}));
app.set('port', (process.env.PORT || 5000));
app.set ('views', __dirname + '/views');
app.set ('view engine', 'ejs');

ids=[];

// declare the folders (relative to index.js location) that serves static files
app.use(express.static('frontend'));
app.use(express.static('images'));
app.use(express.static('views'))	
app.use(express.static(__dirname+''));

// cross origin
app.use(function(req, res, next) {
  res.header("Access-Control-Allow-Origin", "*");
  res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
  next();
});

// the client side sends an initial request to the nodejs requesting a unique identifier for the image
app.get('/id', function (req, res) {
  res.send(shortid.generate());
});


// the client side then sends a post with the svg file to the server, and the server converts the svg
// into PNG format in order for Twitter to access the image
app.post('/generatePNG',function(req, res){
	fs.writeFile(req.body.id + '.svg', req.body.svg, function(){
		console.log('file ' + req.body.id + '.svg written to the file system');
		fs.readFile(req.body.id + '.svg')
	  	.then(svg2png)
	  	.then(buffer => fs.writeFile(req.body.id + '.png', buffer))
	  	.then(fs.unlink(req.body.id + '.svg'))
	  	.then(console.log('successfully generated a png file from the svg file'))
	  	.catch(e => console.error(e));
	  	ids.push(req.body.id);
	});
	res.send('request processed');
});

// the Twitter card then requests the server to serve the png image generated. The GET call uses the id to identify
// which image to capture
app.get('/share',function(req, res){

	var id = req.param('id');
	if (ids.indexOf(id)!=-1){
		ids.splice(ids.indexOf(id),1);
		res.render('index.ejs',{"id":id});
		// fs.unlink(id+'.png');
	} else {
		res.render('index.ejs',{"id":id});
		// res.sendFile(__dirname + '/frontend/index.html');
	}
	
});

app.listen(app.get('port'), function() {
  console.log('Node app is running on port', app.get('port'));
});