var express = require("express");
var bodyParser = require("body-parser");
var mongoose = require("mongoose");

const app = express();

app.use(bodyParser.json());
app.use(express.static('public'));
app.use(bodyParser.urlencoded({
    extended: true
}));

mongoose.connect('mongodb://localhost:27017/wood', { useNewUrlParser: true, useUnifiedTopology: true });
var db = mongoose.connection;
db.on('error', () => console.log("Error connecting to DB"));
db.once('open', () => console.log("DB connected"));

app.post("/sign_up", (req, res) => {
    var name = req.body.name;
    var email = req.body.email;
    var phone = req.body.phno; // Corrected variable name here
    var password = req.body.password;
    var data = {
        "name": name,
        "email": email,
        "phone": phone,
        "password": password
    };
    db.collection('users').insertOne(data, (err, collection) => {
        if (err) {
            throw err;
        }
        console.log("Record Inserted Successfully");
    });
    return res.redirect('signup_sucess.html'); // Corrected redirect URL
});

app.get("/", (req, res) => {
    res.set({
        "Allow-access-Allow-Origin": '*'
    });
    return res.redirect('index.html');
}).listen(3000);

console.log("listening");
