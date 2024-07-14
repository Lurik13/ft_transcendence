class Player
{
    constructor()
    {
        this.element = document.createElement("div");
        this.posY = 50;
        this.speed = 1;

        document.body.appendChild(this.element);
    }
}

var     pl = new Player();
var     keyDown = {};
const   fps = 120;
const   deltaTime = 1000 / fps;

document.addEventListener("load", () =>
{
    pl.element.style.setProperty("--top", `${pl.posY}px`);
});

window.addEventListener("keydown", (e) =>
{
    keyDown[e.key] = true;
});
window.addEventListener("keyup", (e) =>
{
    keyDown[e.key] = false;
});

function animate()
{
    pl.element.style.setProperty("--top", `${pl.posY}px`);
    if (keyDown["ArrowUp"] == true)
        pl.posY -= pl.speed * deltaTime;
    if (keyDown["ArrowDown"] == true)
        pl.posY += pl.speed * deltaTime;

    setTimeout(() => {
        requestAnimationFrame(animate);
    }, deltaTime);
}

animate();