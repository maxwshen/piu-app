// easeljs

var stage;

// https://stackoverflow.com/questions/21605989/how-to-draw-a-polygon-using-easeljs
(createjs.Graphics.Polygon = function(x, y, points) {
  this.x = x;
  this.y = y;
  this.points = points;
}).prototype.exec = function(ctx) {
  var start = this.points[0];
  ctx.moveTo(start.x, start.y);
  this.points.slice(1).forEach(function(point) {
      ctx.lineTo(point.x, point.y);
  });
  ctx.lineTo(start.x, start.y);
}
createjs.Graphics.prototype.drawPolygon = function(x, y, args) {
  var points = [];
  if (Array.isArray(args)) {
      args.forEach(function(point) {
          point = Array.isArray(point) ? {x:point[0], y:point[1]} : point;
          points.push(point);
      });
  } else {
      args = Array.prototype.slice.call(arguments).slice(2);
      var x = null;
      args.forEach(function(val) {
          if (x == null) {
              x = val;
          } else {
              points.push({x: x, y: val});
              x = null;
          }
      });
  }
  return this.append(new createjs.Graphics.Polygon(x, y, points));
}


function draw_lines() {
  const colors = ['DeepSkyBlue', 'red', 'gold', 'red', 'DeepSkyBlue'];
  const line_space = 30;
  const line_width = 1;
  const line_height = 1000;
  const left_x = 50;
  const top_y = 50;
  for (let i = 0; i < colors.length + 1; i++) {
    var rect = new createjs.Shape();
    rect.graphics.beginFill(colors[i]).drawRect(0, 0, line_width, line_height);
    rect.x = left_x + line_space * i;
    rect.y = top_y;
    stage.addChild(rect);
  }
}


function draw_arrow() {
  var poly = new createjs.Shape();
  const x = 200;
  const y = 200;
  poly.graphics.beginFill("#000").drawPolygon(0, 0, [[0, 0], [0, 100], [100, 0]])
  poly.x = x;
  poly.y = y;
  stage.addChild(poly)
}


function draw_text() {
}

function stress_test() {
  for (let i = 0; i < 1000; i++) {
    var text = new createjs.Text("Hello World");
    text.x = 100;
    text.y = i * 10;
    stage.addChild(text)

    for (let j = 0; j < 10; j++) {
      var poly = new createjs.Shape();
      poly.graphics.beginFill("#000").drawPolygon(0, 0, [[0, 0], [0, 20], [20, 0]])
      poly.x = 150 + j*20;
      poly.y = i * 10;
      stage.addChild(poly)
    }

    var rect = new createjs.Shape();
    rect.graphics.beginFill("red").drawRect(0, 0, 50, 1);
    rect.x = 200
    rect.y = i * 10;
    stage.addChild(rect);
  }
}


function init(canvas, name) {
  // name: list
  stage = new createjs.Stage(canvas);

  console.log(name);

  var text = new createjs.Text(name[0]);
  text.x = 20;
  text.y = 200;
  stage.addChild(text)  

  // draw_lines()
  // draw_arrow()

  // stress_test()

  // var circle = new createjs.Shape();
  // circle.graphics.beginFill("DeepSkyBlue").drawCircle(0, 0, 50);
  // circle.x = 100;
  // circle.y = 100;
  // stage.addChild(circle);

  stage.update();
}