var canvas = document.getElementById('canvas'),
    c = canvas.getContext('2d'),
    birdie = document.getElementById('birdie'),
    socket = io();

var JUMP_SPEED = 7
var bird = {
  x: 0,
  y: 0,
}

WALL_WIDTH = 30
GATE_HEIGHT = 60
var wall = {
  x: 0,
  gate: {
    y: 0,
    height: GATE_HEIGHT
  },
  width: WALL_WIDTH,
}

var game = {
  width: 250,
  height: 200,
  lost: false,
  score: 0,
}

socket.on('game', function() {

});

(function loop() {
  requestAnimationFrame(function() {
    
    loop();
  });
})


function draw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  ctx.draw
}
