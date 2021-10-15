/* ***********************************************************************
						maze_layout table (text array)
	This table keeps track of individual maze layouts and solutions.
**************************************************************************/	

DROP TABLE IF EXISTS maze_layout;

CREATE TABLE IF NOT EXISTS maze_layout
	(
		maze_id 	SERIAL PRIMARY KEY,
		maze_name	text,
		body 		json,
		solution	text
		
	);


/* ***********************************************************************
						run_stats table
	This table keeps track of individual runs of various algorithms on
	a given maze.
**************************************************************************/

DROP TABLE IF EXISTS run_stats;

CREATE TABLE IF NOT EXISTS run_stats
	(
		run_id 					SERIAL PRIMARY KEY ,
		maze_id 				integer references maze_layout(maze_id),
		algo_id					integer references algo_info(algo_id),
		user_id 				integer references users(user_id), 
		computations_to_solve 	integer
	);	
	
	
/* ***********************************************************************
						users table
	This table keeps track of user info.
**************************************************************************/

DROP TABLE IF EXISTS users;

CREATE TABLE IF NOT EXISTS users
	(
		user_id 		SERIAL PRIMARY KEY,
		user_name 		text,
		user_email		text,
		user_password	text
	);


/* ***********************************************************************
						algo_info table
	This table keeps track of individual algorithms.
**************************************************************************/

DROP TABLE IF EXISTS algo_info;

CREATE TABLE IF NOT EXISTS algo_info
	(
		algo_id 		SERIAL PRIMARY KEY,
		algo_name 		text
	);







