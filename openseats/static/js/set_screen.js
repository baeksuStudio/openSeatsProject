// 화면 구성

var WIDTH = 3000;
var HEIGHT = 2000;


var stage = new Konva.Stage({
  container: 'konva-canvas',   // id of container <div>
  width: WIDTH,
  height: HEIGHT,
});

// then create layer
var layer = new Konva.Layer();


export {stage, layer};