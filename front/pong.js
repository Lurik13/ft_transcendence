var     keyDown = {};
const   fps = 120;
const   deltaTime = 1000 / fps;
const   canvas = document.getElementById("gameArea");
const   ctx = canvas.getContext("2d");
const   aspectRatio = 16 / 9;

class   Player
{
    constructor([x, w, h])
    {
        this.element = document.createElement("div");
        this.speed = this.yToPx(1);
        this.w = this.xToPx(w);
        this.h = this.yToPx(h);
        this.x = this.xToPx(x);
        this.y = (canvas.height - this.h) / 2;
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
        this.speed = this.yToPx(1);
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
        this.r = this.xToPx(1);
        this.speed = this.xToPx(1);
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
        this.r = this.xToPx(1);
        this.speed = this.xToPx(1);
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

    setTimeout(() => {
        requestAnimationFrame(animate);
    }, deltaTime);
}

document.addEventListener("keydown", (e) => keyDown[e.key] = true);
document.addEventListener("keyup", (e) => keyDown[e.key] = false);
window.addEventListener('resize', resizeCanvas);

resizeCanvas();
animate();
