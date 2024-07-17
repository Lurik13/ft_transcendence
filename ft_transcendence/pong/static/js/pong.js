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

const board = document.getElementById("board");
const ctx = board.getContext("2d");

const board_x_min = 15;
const board_x_max = 775;
const board_y_min = 15;
const board_y_max = 405;

const bar_height = 100;
const bar_width = 20;
const left_bar_x = 30;
const right_bar_x = 760;
const bar_movement = 7;

let left_bar_current_y = 210;
let right_bar_current_y = 210;

const ball_radius = 13;

let ball_x = 405;
let ball_y = 260;
let ball_direction = [-0.5, 0];

function draw_bar(x, bar_coords)
{
	ctx.beginPath();
	ctx.rect(x, bar_coords, bar_width, bar_height);
	ctx.fillStyle = "#009000";
	ctx.fill();
	ctx.closePath();
}

function draw_ball(x, y)
{
	ctx.beginPath();
	ctx.arc(x, y, ball_radius, 0, 2 * Math.PI);
	ctx.fillStyle = "black";
	ctx.fill();
	ctx.closePath();
}

function draw_board(left_bar_coords, right_bar_coords)
{
	ctx.fillStyle = "#9b0000";
	ctx.fillRect(10, 10, 800, 500);
	ctx.clearRect(board_x_min, board_y_min, 780, 490);

	draw_bar(left_bar_x, left_bar_coords);
	draw_bar(right_bar_x, right_bar_coords);
	draw_ball(ball_x, ball_y);
}

draw_board(left_bar_current_y, right_bar_current_y);

window.onkeydown=function(key)
{
	if (key.keyCode === 87)
	{
		left_bar_current_y -= bar_movement;
		if (left_bar_current_y < board_y_min)
			left_bar_current_y = board_y_min;
		draw_board(left_bar_current_y, right_bar_current_y);
	}
	if (key.keyCode === 83)
	{
		left_bar_current_y += bar_movement;
		if (left_bar_current_y > board_y_max)
			left_bar_current_y = board_y_max;
		draw_board(left_bar_current_y, right_bar_current_y);
	}

	if (key.keyCode === 73)
	{
		right_bar_current_y -= bar_movement;
		if (right_bar_current_y < board_y_min)
			right_bar_current_y = board_y_min;
		draw_board(left_bar_current_y, right_bar_current_y);
	}
	if (key.keyCode === 75)
	{
		right_bar_current_y += bar_movement;
		if (right_bar_current_y > board_y_max)
			right_bar_current_y = board_y_max;
		draw_board(left_bar_current_y, right_bar_current_y);
	}
}

while (true)
{
	
}