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
        this.speed = this.speed / oldCanvasHeight * canvas.height;
    }
}

class   Ball
{
    constructor()
    {
        this.r = this.xToPx(1);
        this.x = canvas.width / 2;
        this.y = canvas.height / 2;
        // this.speed = this.xToPx(1);
        this.velocity = {
            x: 0,
            y: 0
        };
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
        this.r = this.r / oldCanvasHeight * canvas.height;
        // this.speed = this.speed / oldCanvasHeight * canvas.height;
        this.velocity.x = this.velocity.x / oldCanvasHeight * canvas.height;
        this.velocity.y = this.velocity.y / oldCanvasHeight * canvas.height;
    }

    // Change direction and speed of ball
    bounce([x1, x2], [y1, y2])
    {
        const   vx = Math.random() * (x2 - x1) + x1;
        const   vy = Math.random() * (y2 - y1) + y1;

        if (x1 != 0 && x2 != 0)
            this.velocity.x = this.xToPx(vx);
        if (y1 == 0 && y2 == 0)
            this.velocity.y *= -1;
        else
            this.velocity.y = this.yToPx(vy);
    }

    checkCollides()
    {
        // if ball is between left paddle on axe x
        // if ball is between left paddle on axe y
        if (this.x - this.r <= pl.x + pl.w && this.x - this.r >= pl.x
            && this.y >= pl.y && this.y <= pl.y + pl.h)
            this.bounce([0.6, 0.8], [-0.8, 0.8]);
        if (this.y - this.r <= 0)
            this.bounce([0, 0], [0, 0]);
        // if ball is between left paddle on axe x
        // if ball is between left paddle on axe y
        if (this.x + this.r >= pr.x && this.x + this.r <= pr.x + pr.w
            && this.y >= pr.y && this.y <= pr.y + pr.h)
            this.bounce([-0.6, -0.8], [-0.8, 0.8]);
        if (this.y + this.r >= canvas.height)
            this.bounce([0, 0], [0, 0]);
    }

    // Check collide and play move the ball
    move()
    {
        this.checkCollides();
        this.x += this.velocity.x;
        this.y += this.velocity.y;
    }

    // Launch the ball on start (set velocity)
    launch()
    {
        const   s = Math.round(Math.random());
        var     vx = 0;
        var     vy = 0;
        if (s)
            vx = Math.random() * (-0.8 - -0.6) + -0.6;
        else
            vx = Math.random() * (0.8 - 0.6) + 0.6;
        vy = Math.random() * (0.8 - -0.8) + -0.8;
        this.velocity.x = this.xToPx(vx);
        this.velocity.y = this.yToPx(vy);
    }
}

function    refresh_canvas_size()
{
    const   windowWidth = window.innerWidth;
    const   windowHeight = window.innerHeight;

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
