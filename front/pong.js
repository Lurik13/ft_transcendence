var     keyDown = {};
const   fps = 120;
const   deltaTime = 1000 / fps;
const   canvas = document.getElementById("gameArea");
const   ctx = canvas.getContext("2d");
const   aspectRatio = 16 / 9; // Ratio 16:9

class   Player
{
    constructor([x, y], [w, h])
    {
        this.element = document.createElement("div");
        this.speed = this.yToPx(10);
        this.w = this.xToPx(w);
        this.h = this.yToPx(h);
        this.x = this.xToPx(x);
        this.y = this.yToPx(y);
    }

    xToPx(px)
    {
        const res = canvas.width * px / canvas.width;
        const pos = res / 1000 * canvas.width;
        return (pos);
    }

    yToPx(px)
    {
        const res = canvas.height * px / canvas.height;
        const pos = res / 1000 * canvas.height * aspectRatio;
        return (pos);
    }

    drawPaddle()
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
        else if (keyDown["s"] && this.y < canvas.height - this.h)
            this.y += this.speed;
    }

    movePaddleRight()
    {
        if (keyDown["ArrowUp"] && this.y > 0)
            this.y -= this.speed;
        else if (keyDown["ArrowDown"] && this.y < canvas.height - this.h)
            this.y += this.speed;
    }

    resize()
    {
        this.x = this.x / oldCanvasWidth * canvas.width;
        this.y = this.y / oldCanvasHeight * canvas.height;
        this.w = this.w / oldCanvasWidth * canvas.width;
        this.h = this.h / oldCanvasHeight * canvas.height;
        this.speed = this.yToPx(10);
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

var pl = new Player([10, 0], [10, 100]);
var pr = new Player([1000 - 20, 0], [10, 100]);

function resizeCanvas()
{
    refresh_canvas_size()

    // Convert current positions and sizes to proportional values
    pl.resize();
    pr.resize();

    // Save the new canvas dimensions for the next resize
    oldCanvasWidth = canvas.width;
    oldCanvasHeight = canvas.height;
}

let oldCanvasWidth = canvas.width;
let oldCanvasHeight = canvas.height;

function    draw()
{
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    pl.drawPaddle();
    pr.drawPaddle();
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
