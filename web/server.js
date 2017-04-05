var express = require('express'),
    app = express(),
    server = require('http').Server(app),
    io = require('socket.io')(server)
    exec = require('child_process').exec
    compression = require('compression')
    path = require('path'),
    router = express.Router();


server.listen(8088);
router.use(express.static(__dirname + '/static'))
router.use(compression())
router.use('/assets/', express.static(__dirname + '/../assets/'))


var record = path.resolve(__dirname, '../record.py');
router.get('/play', function(request, response) {
  var child = exec('python3 ' + record, { maxBuffer: 1024 * 5000 }, function(err, out, stderr) {
    if (err || stderr) {
      console.log(err || stderr)
      response.send(err || stderr);
      return;
    }
  });

  child.stdout.pipe(response);
});


app.use('/flappy-bird', router);
