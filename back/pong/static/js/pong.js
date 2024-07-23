///////////////////////////////////////////////////////////
//////////////////////// Variables ////////////////////////
///////////////////////////////////////////////////////////

const board = document.getElementById("board");
const ctx = board.getContext("2d");
let keys = {};

const board_x_min = 15;
const board_x_max = 775;
const board_y_min = 15;
const board_y_max = 505;

const paddle_height = 100;
const paddle_width = 5;
const left_paddle_x = 50;
const right_paddle_x = 755;
const paddle_speed = 10;

let left_paddle_current_y;
let right_paddle_current_y;

const ball_radius = 13;
let ball_speed;

let ball_x;
let ball_y;
let ball_angle = Math.random() > 0.5 ? 180 : 0;

let score = [0,0];



///////////////////////////////////////////////////////////
////////////////////// Key functions //////////////////////
///////////////////////////////////////////////////////////

function move_ball()
{
	let future_x = ball_x + Math.cos(ball_angle * Math.PI / 180) * ball_speed;
	let future_y = ball_y + Math.sin(ball_angle * Math.PI / 180) * ball_speed;
	if (wall_collisions(future_x, future_y) == 0)
	{
		paddle_collisions(future_x, future_y);
		draw_board(left_paddle_current_y, right_paddle_current_y);
		setTimeout(move_ball, 10);
	}
}

function victory(future_x)
{
	if (future_x < board_x_max / 2)
	{
		score[1]++;
		ball_angle = 180;
		begin_point(3 * (board_x_max) / 4, (board_y_max + board_y_min) / 2);
	}
	else
	{
		score[0]++;
		ball_angle = 0;
		begin_point(1 * (board_x_max) / 4, (board_y_max + board_y_min) / 2);
	}
}

function begin_point(x_coords, y_coords)
{
	left_paddle_current_y = 210;
	right_paddle_current_y = 210;
	ball_speed = 5;
	ball_x = x_coords;
	ball_y = y_coords;
	draw_board(left_paddle_current_y, right_paddle_current_y);
	setTimeout(move_ball, 1500);
}



///////////////////////////////////////////////////////////
////////////////////// Initial move ///////////////////////
///////////////////////////////////////////////////////////

begin_point((board_x_max) / 2, (board_y_max + board_y_min) / 2);
