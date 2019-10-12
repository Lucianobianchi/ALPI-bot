let BOT, ANCHOR, objects;

const initX = 300; const initY = 200;
function setup() {
  createCanvas(1200, 780);
  BOT = new Bot(initX, initY);
  ANCHOR = new DraggableAnchor(initX, initY, initX + 100, initY);
  objects = [BOT, ANCHOR];
}

function draw() {
  background(200);
  [bx, by, ba] = BOT.update();
  ANCHOR.updateBotPosition(bx, by, ba);
  for (let i = 0; i < objects.length; i++) {
    objects[i].show();
  }
}

function mousePressed() {
  ANCHOR.mousePress(mouseX, mouseY);
}

function mouseReleased() {
  ANCHOR.mouseRelease(mouseX, mouseY);
}

function mouseDragged() {
  ANCHOR.mouseDrag(mouseX, mouseY);
}

function keyPressed() {
  console.log('Pressed', keyCode);
  switch(keyCode) {
    case(75): // k
      BOT.accelerate(0, 1);
      break;
    case (76):
      BOT.accelerate(1, 1);
      break;
    case(188): // ,
      BOT.accelerate(0, -1);
      break;
    case (190): // .
      BOT.accelerate(1, -1);
      break;
  }
}