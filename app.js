var express = require('express')
var port = process.env.PORT || 3000
var multer = require('multer');
var bodyParser = require('body-parser');
var iconv = require('iconv-lite');
var fs = require('fs');
var done = false;
var newName = '';
var from_code = '';
var textContent = '';

var storage = multer.diskStorage({
	destination: function (req, file, cb) {
		cb(null, 'uploads/')
	},
	filename: function (req, file, cb) {
		newName = Date.now() + '.txt';
		cb(null, newName)

	}
})
var upload = multer({ storage: storage })
var app = express();
var path = require('path');
var exec = require('child_process').exec, child;

app.set('views', './src')
app.set('view engine', 'jade')
app.use(express.static(path.join(__dirname, '/')));
app.use(bodyParser.urlencoded({ extended: true }));
app.listen(port)
console.log('started!')


app.get('/', function (req, res) {
	res.render('index', {
		title: '文本分类首页'
	})
});
//接收上传的文件
app.post('/upload', upload.any(), function (req, res, next) {
	res.json(newName);
	res.end();
	child = exec('.\\\encodeDetecter\\\probeEncode.exe ' + 'uploads\\' + newName, function (error, stdout, stderr) {
		from_code = stdout;
		if (error !== null) {
			console.log('exec error: ' + error);
		}
		convertEncode('uploads/' + newName);
	})
})
//ajax请求调用程序进行分类
app.get('/classify1', function (req, res) {
	convertEncode('uploads/' + newName);
	child = exec('python execfile/main.py ' + 'uploads/' + newName, { encoding: 'binary' }, function (error, stdout, stderr) {
		var buffer = new Buffer(stdout, 'binary')
		//console.log('stderr: ' + stderr);
		if (error !== null) {
			console.log('exec error: ' + error);
		}
		res.send(convertToString(iconv.decode(buffer, 'gbk')));
		deleteUploadFile('uploads/');
	})
})
//ajax对post过来的数据进行分类
app.post('/classify2', function (req, res) {
	textContent = req.body.data;
	newName = Date.now() + '.txt';
	fs.writeFile('uploads/' + newName, textContent, {
        encoding: 'utf8'
	}, function (err) {
        if (err) {
			throw err;
        }
		child = exec('python execfile/main.py ' + 'uploads/' + newName, { encoding: 'binary' }, function (error, stdout, stderr) {
			var buffer = new Buffer(stdout, 'binary')
			//console.log('stderr: ' + stderr);
			if (error !== null) {
				console.log('exec error: ' + error);
			}
			res.send(convertToString(iconv.decode(buffer, 'gbk')));
			deleteUploadFile('uploads/');
		})
	});

})


//对结果进行解析
function convertToString(stdout) {
	var temp = (stdout + '').split(',');
	var result = "";
	result += temp[0].split(':')[1];
	result += ','
	result += temp[1].split(':')[1];
	return result;
}
//对文件字符编码格式进行转换
function convertEncode(filename) {
	if (from_code == 'utf8')
		return;
	else if (from_code == '')
		from_code = 'gbk'
	fs.writeFile(filename, iconv.decode(fs.readFileSync(filename), from_code), {
        encoding: 'utf8'
	}, function (err) {
        if (err) {
			throw err;
        }
	});
}
//删除上传的文件
function deleteUploadFile(path) {
	if (fs.existsSync(path)) {
		var files = fs.readdirSync(path);
		files.forEach(function (file, index) {         
			if(file!='.gitkeep'){
				var curPath = path + "/" + file;
				fs.unlinkSync(curPath);
			}			
        });
	}
}