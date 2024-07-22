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

let last_time_pressed = 0;

function handleKeyPress()
{
	if (Date.now() > last_time_pressed + 1)
	{
		last_time_pressed = Date.now();
		if (keys['w'] == true || keys['W'] == true)
		{
			left_paddle_current_y -= paddle_speed;
			if (left_paddle_current_y < board_y_min)
				left_paddle_current_y = board_y_min;
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
