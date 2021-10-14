const express = require('express');
const bp = require('body-parser');
const app = express();
const port = 5000;

app.use(bp.json());
app.use(bp.urlencoded({ extended: true }));

const spawn = require("child_process").spawn;
var jsondata = 0;


app.get("/", (req, res, next) => {
    console.log(`hello ${req.body["token"]}`);
    const pythonProcess = spawn('python',["get_amzn_json.py", req.body["arg1"], req.body["arg2"]]);
    pythonProcess.stdout.on('data', (data) => {
        jsondata = data;
    res.send(jsondata);
    });
});

app.listen(port, () => {
    console.log(`listening to port ${port}`);
});