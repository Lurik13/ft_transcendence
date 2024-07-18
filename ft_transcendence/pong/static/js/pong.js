const board = document.getElementById("board");
const ctx = board.getContext("2d");

const board_x_min = 15;
const board_x_max = 775;
const board_y_min = 15;
const board_y_max = 505;

const paddle_height = 100;
const paddle_width = 20;
const left_paddle_x = 30;
const right_paddle_x = 760;
const paddle_speed = 7;

let left_paddle_current_y = 210;
let right_paddle_current_y = 210;

const ball_radius = 13;
const ball_speed = 13;

let ball_x = 405;
let ball_y = 260;
let ball_direction = [-0.5, -0.2];


///////////////////////////////////////////////////////////


function draw_paddle(x, paddle_coords)
{
	ctx.beginPath();
	ctx.rect(x, paddle_coords, paddle_width, paddle_height);
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

function draw_board(left_paddle_coords, right_paddle_coords)
{
	ctx.fillStyle = "#9b0000";
	ctx.fillRect(10, 10, 800, 500);
	ctx.clearRect(board_x_min, board_y_min, 780, 490);
	
	draw_paddle(left_paddle_x, left_paddle_coords);
	draw_paddle(right_paddle_x, right_paddle_coords);
	draw_ball(ball_x, ball_y);
}

function move_ball()
{
	let future_x = ball_x + ball_direction[0] * ball_speed;
	let future_y = ball_y + ball_direction[1] * ball_speed;

	if (future_x < board_x_min + ball_radius)
	{
		future_x = board_x_min + ball_radius;
		ball_direction[0] *= -1;
	}
	if (future_y < board_y_min + ball_radius)
	{
		future_y = board_y_min + ball_radius;
		ball_direction[1] *= -1;
	}

	if (future_x > board_x_max + ball_radius)
	{
		future_x = board_x_max + ball_radius;
		ball_direction[0] *= -1;
	}
	if (future_y > board_y_max - ball_radius)
	{
		future_y = board_y_max - ball_radius;
		ball_direction[1] *= -1;
	}


	ball_x = future_x;
	ball_y = future_y;
	draw_board(left_paddle_current_y, right_paddle_current_y);
}

function main()
{
	move_ball();
	setTimeout(main, 10);
}


///////////////////////////////////////////////////////////


draw_board(left_paddle_current_y, right_paddle_current_y);
main();


///////////////////////////////////////////////////////////


window.onkeydown=function(key)
{
	if (key.keyCode === 87)
	{
		left_paddle_current_y -= paddle_speed;
		if (left_paddle_current_y < board_y_min)
			left_paddle_current_y = board_y_min;
		draw_board(left_paddle_current_y, right_paddle_current_y);
	}
	if (key.keyCode === 83)
	{
		left_paddle_current_y += paddle_speed;
		if (left_paddle_current_y > board_y_max - paddle_height)
			left_paddle_current_y = board_y_max - paddle_height;
		draw_board(left_paddle_current_y, right_paddle_current_y);
	}

	if (key.keyCode === 73)
	{
		right_paddle_current_y -= paddle_speed;
		if (right_paddle_current_y < board_y_min)
			right_paddle_current_y = board_y_min;
		draw_board(left_paddle_current_y, right_paddle_current_y);
	}
	if (key.keyCode === 75)
	{
		right_paddle_current_y += paddle_speed;
		if (right_paddle_current_y > board_y_max - paddle_height)
			right_paddle_current_y = board_y_max - paddle_height;
		draw_board(left_paddle_current_y, right_paddle_current_y);
	}
}

// function main()
// {
// 	setTimeout(main, 1000);
// 	console.log("Delayed for 1 second.");
// }