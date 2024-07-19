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
// const paddle_width = 20;
const paddle_width = 7;
// const left_paddle_x = 30;
const left_paddle_x = 100;
// const right_paddle_x = 760;
const right_paddle_x = 600;
const paddle_speed = 10;

let left_paddle_current_y = 210;
let right_paddle_current_y = 210;

const ball_radius = 13;
let ball_speed = 7;

let ball_x = 405;
let ball_y = 260;
let ball_direction = [-0.5, -0.2];



///////////////////////////////////////////////////////////
///////////////////////// Drawing /////////////////////////
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



///////////////////////////////////////////////////////////
/////////////////////// Collisions ////////////////////////
///////////////////////////////////////////////////////////

function wall_collisions(future_x, future_y)
{
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
	if (future_x > board_x_max + ball_radius - 7)
	{
		future_x = board_x_max + ball_radius - 7;
		ball_direction[0] *= -1;
	}
	if (future_y > board_y_max - ball_radius)
	{
		future_y = board_y_max - ball_radius;
		ball_direction[1] *= -1;
	}
	ball_x = future_x;
	ball_y = future_y;

}

function paddle_collisions(future_x, future_y)
{
	// horizontal
	if ((future_x - ball_radius <= left_paddle_x + paddle_width && future_x - ball_radius >= left_paddle_x + paddle_width - ball_radius)
		&& future_y >= left_paddle_current_y && future_y <= left_paddle_current_y + paddle_height)
		{
			ball_direction[0] *= -1;
			console.log(future_x);
			ball_speed += 0.1;
		}
	// horizontal
	if (future_x <= left_paddle_x + paddle_width + 9 * ball_radius / 10 && future_x >= left_paddle_x + paddle_width - ball_radius
		&& future_y >= left_paddle_current_y && future_y <= left_paddle_current_y + paddle_height)
		{
			ball_direction[0] = Math.abs(ball_direction[0]);
			// ball_x = left_paddle_x + paddle_width + ball_radius;
			ball_x += ball_radius / 10;
			console.log(future_x);
			ball_speed += 0.1;
		}

	else if (((future_x + ball_radius >= right_paddle_x && future_x <= right_paddle_x + ball_radius)
		|| (future_x - ball_radius <= right_paddle_x + paddle_width && future_x + ball_radius >= right_paddle_x + paddle_width))
		&& future_y >= right_paddle_current_y && future_y <= right_paddle_current_y + paddle_height)
		{
			ball_direction[0] *= -1;
			console.log(future_x);
			ball_speed += 0.1;
		}
		console.log(ball_speed);
	// sur le cote exterieur du terrain
	// else if future_x

	// sur le cote vers les murs
	// if (future_x >= left_paddle_x && future_x <= left_paddle_x + paddle_width)
	// {
	// 	if (future_y + ball_radius >= left_paddle_current_y
	// 		&& future_y + ball_radius <= left_paddle_current_y + paddle_height / 2)
	// 		ball_direction[1] *= -1;
	// 	else if (future_y - ball_radius <= left_paddle_current_y + paddle_height
	// 		&& future_y - ball_radius >= left_paddle_current_y + paddle_height / 2)
	// 		ball_direction[1] *= -1;
	// }
	// else if (future_x >= right_paddle_x && future_x <= right_paddle_x + paddle_width)
	// {
	// 	if (future_y + ball_radius >= right_paddle_current_y
	// 		&& future_y + ball_radius <= right_paddle_current_y + paddle_height / 2)
	// 		ball_direction[1] *= -1;
	// 	else if (future_y - ball_radius <= right_paddle_current_y + paddle_height
	// 		&& future_y - ball_radius >= right_paddle_current_y + paddle_height / 2)
	// 		ball_direction[1] *= -1;
	// }

	//diagonales
	// else if (future_x >= left_paddle_x && future_y >= left_paddle_current_y
	// 	&& future_x <= (left_paddle_x + paddle_width) && future_y <= (left_paddle_current_y + paddle_height))
	// {
	// 	console.log(ball_direction[0]);
	// 	// ball_direction[0] *= -1;
	// 	// ball_direction[1] *= -1;
	// 	ball_direction[0] = Math.abs(ball_direction[0]) * -1;
	// }

	// future_x 109.5, left_paddle_x 100, future_y 38.800000000006236, left_paddle_current_y 15
	// left_paddle_x + paddle_width 160, left_paddle_current_y + paddle_height 115
}

function move_ball()
{
	let future_x = ball_x + ball_direction[0] * ball_speed;
	let future_y = ball_y + ball_direction[1] * ball_speed;
	wall_collisions(future_x, future_y);
	paddle_collisions(future_x, future_y);
	draw_board(left_paddle_current_y, right_paddle_current_y);
	setTimeout(move_ball, 10);
}

function is_ball_in_paddle(paddle_x, paddle_y)
{
	// if (ball_x - ball_radius <= left_paddle_x + paddle_width && ball_x + ball_radius >= left_paddle_x
	// 	&& ball_y >= left_paddle_current_y && ball_y <= left_paddle_current_y + paddle_height)
	// {
	// 	ball_direction[1] *= -1;
	// 	ball_y += ball_speed;
	// }
	// else if (ball_x + ball_radius >= right_paddle_x && ball_x - ball_radius <= right_paddle_x + paddle_width
	// 	&& ball_y >= right_paddle_current_y && ball_y <= right_paddle_current_y + paddle_height)
	// {
	// 	ball_direction[1] *= -1;
	// 	ball_y += ball_speed;
	// }

	// if (ball_x >= left_paddle_x && ball_x <= left_paddle_x + paddle_width)
	// {
	// 	if (ball_y + ball_radius >= left_paddle_current_y
	// 		&& ball_y + ball_radius <= left_paddle_current_y + paddle_height / 2)
	// 	{
	// 		ball_direction[0] = Math.abs(ball_direction[0]) * -1;
	// 		ball_direction[1] = Math.abs(ball_direction[1]) * -1;
	// 		ball_x += ball_radius;
	// 		ball_y -= paddle_speed;
	// 	}

	// 	else if (ball_y - ball_radius <= left_paddle_current_y + paddle_height
	// 		&& ball_y - ball_radius >= left_paddle_current_y + paddle_height / 2)
	// 	{
	// 		ball_direction[0] = Math.abs(ball_direction[0]) * -1;
	// 		ball_direction[1] = Math.abs(ball_direction[1]) * -1;
	// 		ball_y -= paddle_speed;
	// 	}
	// }
	// else if (ball_x >= right_paddle_x && ball_x <= right_paddle_x + paddle_width)
	// {
	// 	if (ball_y + ball_radius >= right_paddle_current_y
	// 		&& ball_y + ball_radius <= right_paddle_current_y + paddle_height / 2)
	// 	{
	// 		ball_direction[0] = Math.abs(ball_direction[0]) * -1;
	// 		ball_direction[1] = Math.abs(ball_direction[1]) * -1;
	// 		ball_y -= paddle_speed;
	// 	}
	// 	else if (ball_y - ball_radius <= right_paddle_current_y + paddle_height
	// 		&& ball_y - ball_radius >= right_paddle_current_y + paddle_height / 2)
	// 	{
	// 		ball_direction[0] = Math.abs(ball_direction[0]) * -1;
	// 		ball_direction[1] = Math.abs(ball_direction[1]) * -1;
	// 		ball_y -= paddle_speed;
	// 	}
	// }

	// if (paddle_x == left_paddle_x)
	// {
	// 	if ((ball_x + ball_radius >= paddle_x && ball_x + ball_radius <= paddle_x + paddle_width)
	// 		|| (ball_x - ball_radius >= paddle_x && ball_x - ball_radius <= paddle_x + paddle_width))
	// 	{
	// 		ball_y = paddle_y + ball_radius + 1;
	// 		ball_direction[0] *= -1;
	// 		draw_board(left_paddle_current_y, right_paddle_current_y);
	// 		// console.log("I'm inside the paddle");
	// 		// if (ball_y + ball_radius >= paddle_y && ball_y + ball_radius <= paddle_y + paddle_height / 2)
	// 		// 	console.log("haut");
	// 	}
	// }
}



///////////////////////////////////////////////////////////
////////////////////// Initial moves //////////////////////
///////////////////////////////////////////////////////////

draw_board(left_paddle_current_y, right_paddle_current_y);
move_ball();



///////////////////////////////////////////////////////////
///////////////////////// Events //////////////////////////
///////////////////////////////////////////////////////////

window.addEventListener('keydown', (e) =>
{
	if (e.key == 'w' || e.key == 's' || e.key == 'i' || e.key == 'k'
		|| e.key == 'W' || e.key == 'S' || e.key == 'I' || e.key == 'K')
	{
		keys[e.key] = true;
		handleKeyPress();
	}
});

window.addEventListener('keyup', (e) => {keys[e.key] = false});

let last_time = 0;

function handleKeyPress()
{
	if (Date.now() > last_time + 1)
	{
		last_time = Date.now();
		if (keys['w'] == true || keys['W'] == true)
		{
			left_paddle_current_y -= paddle_speed;
			if (left_paddle_current_y < board_y_min)
				left_paddle_current_y = board_y_min;
			// else if (left_paddle_current_y)
			is_ball_in_paddle(left_paddle_x, left_paddle_current_y);
			draw_board(left_paddle_current_y, right_paddle_current_y);
		}
		if (keys['s'] == true  || keys['S'] == true )
		{
			left_paddle_current_y += paddle_speed;
			if (left_paddle_current_y > board_y_max - paddle_height)
				left_paddle_current_y = board_y_max - paddle_height;
			draw_board(left_paddle_current_y, right_paddle_current_y);
		}
		
		if (keys['i'] == true  || keys['I'] == true )
		{
			right_paddle_current_y -= paddle_speed;
			if (right_paddle_current_y < board_y_min)
				right_paddle_current_y = board_y_min;
			draw_board(left_paddle_current_y, right_paddle_current_y);
		}
		if (keys['k'] == true  || keys['K'] == true )
		{
			right_paddle_current_y += paddle_speed;
			if (right_paddle_current_y > board_y_max - paddle_height)
				right_paddle_current_y = board_y_max - paddle_height;
			draw_board(left_paddle_current_y, right_paddle_current_y);
		}
	}
	requestAnimationFrame(handleKeyPress);
}
