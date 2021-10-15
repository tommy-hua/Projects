/***********************
  Load Components!

  Express      - A Node.js Framework
  Body-Parser  - A tool to help use parse the data in a post request
  Pg-Promise   - A database tool to help use connect to our PostgreSQL database
***********************/
var express = require('express'); //Ensure our express framework has been added
var app = express();
var bodyParser = require('body-parser'); //Ensure our body-parser tool has been added
app.use(bodyParser.json());              // support json encoded bodies
app.use(bodyParser.urlencoded({ extended: true })); // support encoded bodies

//Create Database Connection
var pgp = require('pg-promise')();

/**********************
  Database Connection information
  host: This defines the ip address of the server hosting our database.
		We'll be using `db` as this is the name of the postgres container in our
		docker-compose.yml file. Docker will translate this into the actual ip of the
		container for us (i.e. can't be access via the Internet).
  port: This defines what port we can expect to communicate to our database.  We'll use 5432 to talk with PostgreSQL
  database: This is the name of our specific database.  From our previous lab,
		we created the football_db database, which holds our football data tables
  user: This should be left as postgres, the default user account created when PostgreSQL was installed
  password: This the password for accessing the database. We set this in the
		docker-compose.yml for now, usually that'd be in a seperate file so you're not pushing your credentials to GitHub :).
**********************/
const dev_dbConfig = {
	host: 'db',
	port: 5432,
	database: process.env.POSTGRES_DB,
	user:  process.env.POSTGRES_USER,
	password: process.env.POSTGRES_PASSWORD
};

/** If we're running in production mode (on heroku), the we use DATABASE_URL
 * to connect to Heroku Postgres.
 */
const isProduction = process.env.NODE_ENV === 'production';
const dbConfig = isProduction ? process.env.DATABASE_URL : dev_dbConfig;

// Heroku Postgres patch for v10
// fixes: https://github.com/vitaly-t/pg-promise/issues/711
if (isProduction) {
  pgp.pg.defaults.ssl = {rejectUnauthorized: false};
}

const db = pgp(dbConfig);

// set the view engine to ejs
app.set('view engine', 'ejs');
app.set('views', __dirname + '/');
app.use(express.static(__dirname + '/'));//This line is necessary for us to use relative paths and access our resources directory

// login page
app.get('/', function(req, res) {
	res.render('./login',{
		local_css:"signin.css",
		my_title:"Login Page"
	});
});

// registration page
app.get('/register', function(req, res) {
	res.render('./register',{
		local_css:"signin.css",
		my_title:"Registration Page"
	});
});

app.get('/main', function(req, res) {
	res.render('./MainPage',{
		my_title:"Main Page"
	});
});

app.get('/stats', function(req, res) {
	res.render('./stats',{
		my_title:"Stats Page"
	});
});

app.get('/management', function(req, res) {
	res.render('./MazeManagement',{
		my_title:"Management Page"
	});
});
/*Add your other get/post request handlers below here: */

app.get('/home', function(req, res) {
	var query = 'select * from favorite_colors;';
	db.any(query)
		.then(function (rows) {
			res.render('pages/home',{
				my_title: "Home Page",
				data: rows,
				color: '',
				color_msg: ''
			})

		})
		.catch(function (err) {
			// display error message in case an error
			request.flash('error', err);
			response.render('pages/home', {
				title: 'Home Page',
				data: '',
				color: '',
				color_msg: ''
			})
		})
});


app.post('/home/pick_color', function(req, res) {
	var color_hex = req.body.color_hex;
	var color_name = req.body.color_name;
	var color_message = req.body.color_message;
	var insert_statement = "INSERT INTO favorite_colors(hex_value, name, color_msg) VALUES('" + color_hex + "','" +
		color_name + "','" + color_message +"') ON CONFLICT DO NOTHING;";

	var color_select = 'select * from favorite_colors;';
	db.task('get-everything', task => {
				return task.batch([
					task.any(insert_statement),
					task.any(color_select)
				]);
			})
		.then(info => {
			res.render('pages/home',{
				my_title: "Home Page",
				data: info[1],
				color: color_hex,
				color_msg: color_message
			})
		})
		.catch(error => {
			// display error message in case an error
			request.flash('error', err);
			response.render('pages/home', {
				title: 'Home Page',
				data: '',
				color: '',
				color_msg: ''
			})
		});
});

//app.listen(3000);
const server = app.listen(process.env.PORT || 3000, () => {
  console.log(`Express running → PORT ${server.address().port}`);
});