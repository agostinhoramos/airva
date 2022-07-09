// Import express.js
let express = require('express');

// Import body parser
let bodyParser = require('body-parser');

// .Env
const dotenv = require('dotenv');
dotenv.config();

// Import mongoose
let app = express();
const cors = require("cors");

// Configure bodyparser to process orders
app.use(bodyParser.urlencoded({
    extended: true
}));
app.use(bodyParser.json());

app.post("/*", function(req, res) {
    console.log("POST -> OK");
    res.send("OK");
});

app.get("/*", function(req, res) {
    console.log("GET -> OK");
    res.send("OK");
});

const PORT = process.env.PORT || 1350; 
app.listen(PORT, function() {
    console.log(`Server running: http://127.0.0.1:${PORT}`);
});