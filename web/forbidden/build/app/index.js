var express = require("express");
var app = express();

const HOST = process.env.CTF4B_HOST;
const PORT = process.env.CTF4B_PORT;
const FLAG = process.env.CTF4B_FLAG;

app.get("/", (req, res, next) => {
    return res.send('FLAG はこちら: <a href="/flag">/flag</a>');
});

const block = (req, res, next) => {
    if (req.path.includes('/flag')) {
        return res.send(403, 'Forbidden :(');
    }

    next();
}

app.get("/flag", block, (req, res, next) => {
    return res.send(FLAG);
})

var server = app.listen(PORT, HOST, () => {
    console.log("Listening:" + server.address().port);
});
