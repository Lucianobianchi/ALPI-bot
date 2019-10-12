const WHEEL_DIAM = 120;
const WHEEL_WIDTH = 40;

const FRONT_AXIS_WIDTH = 16;
const FRONT_AXIS_LENGTH = 160;

const ANCHOR_SPACE = 100;

const BACK_WHEEL_DIST = 200;
const BACK_WHEEL_RAD = 35;

const L = FRONT_AXIS_LENGTH + WHEEL_WIDTH

function Bot(x, y) {
    this.x = x; this.y = y;
    this.vr = 0; this.vl = 0;
    this.angle = 0;

    this.show = function() {
        push();
        translate(this.x, this.y);
        rotate(this.angle);
        
        // Wheels and middle axis
        noStroke();
        rectMode(CENTER);
        fill(50);
        rect(0,-FRONT_AXIS_LENGTH/2-WHEEL_WIDTH/2, WHEEL_DIAM, WHEEL_WIDTH);
        
        fill(100);
        rect(0,0, FRONT_AXIS_WIDTH, FRONT_AXIS_LENGTH);
        
        fill(50);
        rect(0,FRONT_AXIS_LENGTH/2+WHEEL_WIDTH/2, WHEEL_DIAM, WHEEL_WIDTH);
        
        // Back wheel and triangle
        stroke(100);
        strokeWeight(3);
        fill(100);
        triangle(0, -FRONT_AXIS_LENGTH/2+10, -BACK_WHEEL_DIST, 0, 0, FRONT_AXIS_LENGTH/2-10);

        fill(50);
        ellipse(-BACK_WHEEL_DIST, 0, BACK_WHEEL_RAD, BACK_WHEEL_RAD);

        // Anchors
        noStroke();
        fill(255, 0, 0);
        rect(0, -ANCHOR_SPACE/2, 20, 20);
        rect(0, ANCHOR_SPACE/2, 20, 20);

        stroke(0);
        line(0, 0, 100, 0);

        pop();
    }

    this.accelerate = function(wheel, acc) {
        if (wheel === 0) {
            this.vr += acc;
        } else {
            this.vl += acc;
        }
    }

    this.update = function() {
        const v = (this.vl + this.vr) / 2;
        const dx = v * Math.cos(this.angle);
        const dy = v * Math.sin(this.angle);
        const dang = (this.vr - this.vl) / L;
        
        this.x += dx; 
        this.y += dy;
        this.angle += dang;

        return [this.x, this.y, this.angle];
    }
}