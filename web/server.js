var express = require('express'),
    app = express(),
    server = require('http').Server(app),
    io = require('socket.io')(server)
    exec = require('child_process').exec
    compression = require('compression')
    path = require('path');


server.listen(8088);
app.use(express.static(__dirname + '/static'))
app.use(compression())
app.use('/assets/', express.static(__dirname + '/../assets/'))


var record = path.resolve(__dirname, '../record.py');
app.get('/play', function(request, response) {
  var child = exec('python3 ' + record, { maxBuffer: 1024 * 5000 }, function(err, out, stderr) {
    if (err || stderr) {
      console.log(err || stderr)
      response.send(err || stderr);
      return;
    }
  });

  child.stdout.pipe(response);
});

