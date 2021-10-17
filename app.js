const express = require('express');
const bp = require('body-parser');
const app = express();
const port = 5000;

var cors = require('cors');
app.use(cors());

app.use(express.urlencoded({ extended: true }));
app.use(express.json());

const spawn = require("child_process").spawn;
var jsondata = 0;


app.get("/", (req, res, next) => {
    console.log(`hello ${req.headers["arg1"]} ${req.headers["arg2"]}`);
    const pythonProcess = spawn('python',["get_amzn_json.py", req.headers["arg1"], req.headers["arg2"]]);
    pythonProcess.stdout.on('data', (data) => {
        jsondata = data;
        //res.send(jsondata);
        res.send(jsondata);
        console.log(jsondata.toString());
    });
});

app.listen(process.env.PORT || port, () => {
    console.log(`listening to port ${port}`);
});