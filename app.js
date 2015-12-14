var express = require('express')
var port = process.env.PORT || 3000
var multer = require('multer');
var iconv = require('iconv-lite');
var fs = require('fs');
var done = false;
var newName = '';

var storage = multer.diskStorage({
	destination: function (req, file, cb) {
		cb(null, 'uploads/')
	},
	filename: function (req, file, cb) {
		cb(null, file.originalname)
		newName = file.originalname;
	}
})
var upload = multer({ storage: storage })
var app = express();
var path = require('path');
var exec = require('child_process').exec, child;


app.set('views', './src')
app.set('view engine', 'jade')
app.use(express.static(path.join(__dirname, '/')));
app.listen(port)
console.log('started!')


app.get('/', function (req, res) {
	res.render('index', {
		title: '文本分类首页'
	})
});
app.post('/upload', upload.any(), function (req, res, next) {
	console.log(req.files);
	res.json(newName);
	res.end();
})
//ajax请求调用程序进行分类
app.get('/classify', function (req, res) {
	convertEncode('uploads/'+newName);
	child = exec('python execfile/main.py ' + 'uploads/' + newName, { encoding: 'binary' }, function (error, stdout, stderr) {
		//console.log('stdout: ' + iconv.decode(Buffer.concat(chunks), 'gbk'));
		var buffer = new Buffer(stdout, 'binary')
		console.log('stderr: ' + stderr);
		if (error !== null) {
			console.log('exec error: ' + error);
		}
		//res.json(convertToString(iconv.decode(buffer, 'gbk')));
		res.send(convertToString(iconv.decode(buffer, 'gbk')));
		//res.end();
	})
})
app.get('/test', function (req, res) {

})
app.get('/apply', function (req, res) {

})
//对文件格式进行转换
function convertEncode(filename) {
	fs.readFile(filename, function (err, data) {
		if (err) throw err;
		console.log(iconv.decode(data, 'utf8'));
		console.log(data);
	});
}
//对结果进行解析
function convertToString(stdout) {
	var temp = (stdout + '').split(',');
	var result = "";
	result += temp[0].split(':')[1];
	result += ','
	result += temp[1].split(':')[1];
	return result;
}