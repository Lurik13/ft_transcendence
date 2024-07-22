///////////////////////////////////////////////////////////
/////////////////////// Collisions ////////////////////////
///////////////////////////////////////////////////////////

function wall_collisions(future_x, future_y)
{
	if (future_x < board_x_min + ball_radius || future_x > board_x_max + ball_radius / 2)
	{
		victory(future_x);
		return (1);
	}
	if (future_y < board_y_min + ball_radius)
	{
		future_y = board_y_min + ball_radius;
		ball_angle = -ball_angle;
	}
	if (future_y > board_y_max - ball_radius)
	{
		future_y = board_y_max - ball_radius;
		ball_angle = -ball_angle;
	}
	ball_x = future_x;
	ball_y = future_y;
	return (0);
}

function speed_up_ball()
{
	let new_speed = 0;

	if (ball_speed < 7)
		new_speed = 0.3;
	else if (ball_speed < 9)
		new_speed = 0.1;
	else if (ball_speed < 11)
		new_speed = 0.07;
	else if (ball_speed < 13)
		new_speed = 0.05;
	return (new_speed);
}

function paddle_collisions(future_x, future_y)
{
	if (future_x <= left_paddle_x + paddle_width + ball_radius && future_x >= left_paddle_x + paddle_width
		&& future_y >= left_paddle_current_y - ball_radius && future_y <= left_paddle_current_y + paddle_height + ball_radius)
	{
		let position_in_paddle = (2 * (ball_y + ball_radius - left_paddle_current_y) / (paddle_height + ball_radius * 2)) - 1;
		ball_angle = 80 * position_in_paddle;
		ball_x += ball_radius / 10;
		ball_speed += speed_up_ball();
	}

	if (future_x >= right_paddle_x - ball_radius && future_x <= right_paddle_x
		&& future_y >= right_paddle_current_y - ball_radius && future_y <= right_paddle_current_y + paddle_height + ball_radius)
	{
		let position_in_paddle = (2 * (ball_y + ball_radius - right_paddle_current_y) / (paddle_height + ball_radius * 2)) - 1;
		ball_angle = 180 - 80 * position_in_paddle;
		ball_x -= ball_radius / 10;
		ball_speed += speed_up_ball();
	}
}
