const ANCHOR_DIST = 100;
const ANCHOR_RAD = 10;

function DraggableAnchor(botX, botY, anchorX, anchorY) {
    this.anchorX = anchorX;
    this.anchorY = anchorY;
    this.draggingAnchor = false;
    this.botX = botX; this.botY = botY; this.botAngle = 0;

    this.show = function() {
        // Point
        fill(0, 255, 0);
        ellipse(this.anchorX, this.anchorY, ANCHOR_RAD*2, ANCHOR_RAD*2);
        
        let vDist = createVector(0, ANCHOR_SPACE/2).rotate(this.botAngle);
        let vLeft = createVector(this.botX, this.botY).sub(vDist);
        let vRight = createVector(this.botX, this.botY).add(vDist);

        // Strings
        stroke(0, 255, 0);
        strokeWeight(2);
        line(vLeft.x, vLeft.y, this.anchorX, this.anchorY);
        line(vRight.x, vRight.y, this.anchorX, this.anchorY);
    }

    this.mousePress = function(x, y) {
        const d = dist(x, y, this.anchorX, this.anchorY);
        if (d <= ANCHOR_RAD) {
            this.draggingAnchor = true;
            this.dragOffX = x - this.anchorX;
            this.dragOffY = y - this.anchorY;
        }
    }

    this.mouseDrag = function(x ,y) {
        if (this.draggingAnchor) {
            this.anchorX = x - this.dragOffX;
            this.anchorY = y - this.dragOffY;
        }
    }

    this.mouseRelease = function(x, y) {
        this.draggingAnchor = false;
    }

    this.updateBotPosition = function(x, y, angle) {
        this.botX = x;
        this.botY = y;
        this.botAngle = angle;
    }
}