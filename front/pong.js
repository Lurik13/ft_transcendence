// Object to track keys presses.
var     keyDown = {};
// Frame rate and time interval between frames.
const   fps = 120;
const   deltaTime = 1000 / fps;
// Reference to HTML canvas and 2D rendering context.
const   canvas = document.getElementById("gameArea");
const   ctx = canvas.getContext("2d");
// Game aspect ratio (16:9).
const   aspectRatio = 16 / 9;

class   Player
{
    constructor([x, w, h])
    {
        // Position, size and speed
        this.w = this.xToPx(w);
        this.h = this.yToPx(h);
        this.x = this.xToPx(x);
        this.y = (canvas.height - this.h) / 2;
        this.rspeed = 1;
        this.speed = this.yToPx(this.rspeed);
    }

    // Converts a percentage of the canvas width into pixels
    xToPx(px)
    {
        return (canvas.width * px / 100);
    }

    // Converts a percentage of the canvas's height (adjusted by the aspect ratio) into pixels.
    yToPx(px)
    {
        return (canvas.height * aspectRatio * px / 100);
    }

    draw()
    {
        ctx.beginPath();
        ctx.rect(this.x, this.y, this.w, this.h);
        ctx.fillStyle = "#FFF";
        ctx.fill();
        ctx.closePath();
    }

    movePaddleLeft()
    {
        if (keyDown["w"] && this.y > 0)
            this.y -= this.speed;
        if (keyDown["s"] && this.y < canvas.height - this.h)
            this.y += this.speed;
    }

    movePaddleRight()
    {
        if (keyDown["ArrowUp"] && this.y > 0)
            this.y -= this.speed;
        if (keyDown["ArrowDown"] && this.y < canvas.height - this.h)
            this.y += this.speed;
    }

    resize()
    {
        this.x = this.x / oldCanvasWidth * canvas.width;
        this.y = this.y / oldCanvasHeight * canvas.height;
        this.w = this.w / oldCanvasWidth * canvas.width;
        this.h = this.h / oldCanvasHeight * canvas.height;
        this.speed = this.yToPx(this.rspeed);
    }
}

class   Ball
{
    constructor()
    {
        this.w = this.xToPx(2);
        this.h = this.yToPx(2);
        this.x = (canvas.width - this.w) / 2;
        this.y = (canvas.height - this.h) / 2;
        this.rr = 1;
        this.r = this.xToPx(this.rr);
        // this.rspeed = 1;
        // this.speed = this.xToPx(this.rspeed);
        this.velocity = {
            x: 0,
            y: 0
        };
        this.rvelocity = {
            x: 0,
            y: 0
        }
    }

    xToPx(px)
    {
        return (canvas.width * px / 100);
    }

    yToPx(px)
    {
        return (canvas.height * aspectRatio * px / 100);
    }

    draw()
    {
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.r, 0, 2 * Math.PI);
        ctx.strokeStyle = "#FFF";
        ctx.stroke();
        ctx.closePath();
    }

    resize()
    {
        this.x = this.x / oldCanvasWidth * canvas.width;
        this.y = this.y / oldCanvasHeight * canvas.height;
        this.w = this.w / oldCanvasWidth * canvas.width;
        this.h = this.h / oldCanvasHeight * canvas.height;
        this.r = this.xToPx(this.rr);
        // this.speed = this.xToPx(this.rspeed);
        this.velocity.x = this.xToPx(this.rvelocity.x);
        this.velocity.y = this.yToPx(this.rvelocity.y);
    }

    bounce([x1, x2], [y1, y2])
    {
        const   vx = Math.random() * (x2 - x1) + x1;
        const   vy = Math.random() * (y2 - y1) + y1;

        if (x1 != 0 && x2 != 0)
        {
            this.velocity.x = this.xToPx(vx);
            this.rvelocity.x = vx;
        }
        if (y1 == 0 && y2 == 0)
        {
            this.velocity.y *= -1;
            this.rvelocity.y *= -1;
        }
        else
        {
            this.velocity.y = this.yToPx(vy);
            this.rvelocity.y = vy;
        }
    }

    move()
    {
        this.x += this.velocity.x;
        this.y += this.velocity.y;
        if (this.x <= 0)
            this.bounce([0.6, 0.8], [-0.8, 0.8]);
        if (this.y <= 0)
            this.bounce([0, 0], [0, 0]);
        if (this.x >= canvas.width)
            this.bounce([-0.6, -0.8], [-0.8, 0.8]);
        if (this.y >= canvas.height)
            this.bounce([0, 0], [0, 0]);
    }

    launch()
    {
        const   vx = Math.random() * (0.8 - -0.6) + -0.6;
        const   vy = Math.random() * (0.8 - -0.6) + -0.6;
        this.velocity.x = this.xToPx(vx);
        this.velocity.y = this.yToPx(vy);
        this.rvelocity.x = vx;
        this.rvelocity.y = vy;
    }
}

function    refresh_canvas_size()
{
    const   windowWidth = window.innerWidth - 100;
    const   windowHeight = window.innerHeight - 100;

    if (windowWidth / windowHeight > aspectRatio)
    {
        canvas.width = windowHeight * aspectRatio;
        canvas.height = windowHeight;
    }
    else
    {
        canvas.width = windowWidth;
        canvas.height = windowWidth / aspectRatio;
    }
}

refresh_canvas_size()

var pl = new Player([1, 1, 10]);
var pr = new Player([98, 1, 10]);
var ball = new Ball();

function resizeCanvas()
{
    refresh_canvas_size()
    pl.resize();
    pr.resize();
    ball.resize();
    oldCanvasWidth = canvas.width;
    oldCanvasHeight = canvas.height;
}

let oldCanvasWidth = canvas.width;
let oldCanvasHeight = canvas.height;

function    draw()
{
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    pl.draw();
    pr.draw();
    ball.draw();
}

function    animate()
{
    draw();
    pl.movePaddleLeft();
    pr.movePaddleRight();
    ball.move();

    setTimeout(() => {
        requestAnimationFrame(animate);
    }, deltaTime);
}

document.addEventListener("keydown", (e) => keyDown[e.key] = true);
document.addEventListener("keyup", (e) => keyDown[e.key] = false);
window.addEventListener('resize', resizeCanvas);

resizeCanvas();
animate();
ball.launch();
