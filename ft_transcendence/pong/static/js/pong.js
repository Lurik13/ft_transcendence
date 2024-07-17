// window.onload = function() {
// 	var demo = document.getElementById('demo');
// 	var value = 0;
// 	var space_bar = 32;
// 	var right_arrow = 39
// 	window.onkeydown=function(gfg) {
// 		if (gfg.keyCode === space_bar) {
// 			value++;
// 			demo.innerHTML = "Number of spaces: " + value;
// 		};
// 		if (gfg.keyCode === right_arrow)
// 			alert("Welcome, young jedi!");
// 	};
// };


// function draw() {
var canvas = document.getElementById("canvas");
var ctx = canvas.getContext("2d");
ctx.fillStyle = "green";
ctx.fillRect(10, 10, 100, 100);
// }