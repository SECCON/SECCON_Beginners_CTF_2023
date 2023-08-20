const express = require("express");
const session = require("express-session");
const jwt = require("jsonwebtoken");
const _ = require("lodash");

const { readKeyFromFile, generateRandomString, getAdminPassword } = require("./utils");

const HOST = process.env.CTF4B_HOST;
const PORT = process.env.CTF4B_PORT;
const FLAG = process.env.CTF4B_FLAG;

const app = express();
app.use(express.json());

app.use(session({
  secret: generateRandomString(),
  resave: false,
  saveUninitialized: true,
  cookie: { secure: false }
}));

app.post("/register", (req, res) => {
  const { username, password } = req.body;
  if(!username || !password) {
    res.status(400).json({ error: "Please send username and password" });
    return;
  }

  const user = {
    username: username,
    password: password
  };
  if (username === "admin" && password === getAdminPassword()) {
    user.admin = true;
  }
  req.session.user = user;

  let signed;
  try {
    signed = jwt.sign(
      _.omit(user, ["password"]),
      readKeyFromFile("keys/private.key"), 
      { algorithm: "RS256", expiresIn: "1h" } 
    );
  } catch (err) {
    res.status(500).json({ error: "Internal server error" });
    return;
  }
  res.header("Authorization", signed);

  res.json({ message: "ok" });
});

app.post("/flag", (req, res) => {
  if (!req.header("Authorization")) {
    res.status(400).json({ error: "No JWT Token" });
    return;
  }

  if (!req.session.user) {
    res.status(401).json({ error: "No User Found" });
    return;
  }

  let verified;
  try {
    verified = jwt.verify(
      req.header("Authorization"),
      readKeyFromFile("keys/public.key"), 
      { algorithms: ["RS256", "HS256"] }
    );
  } catch (err) {
    console.error(err);
    res.status(401).json({ error: "Invalid Token" });
    return;
  }

  if (req.session.user.username !== "admin" || req.session.user.password !== getAdminPassword()) {
    verified = _.omit(verified, ["admin"]);
  }

  const token = Object.assign({}, verified);
  const user = Object.assign(req.session.user, verified);

  if (token.admin && user.admin) {
    res.send(`Congratulations! Here"s your flag: ${FLAG}`);
    return;
  }

  res.send("No flag for you");
});

app.listen(PORT, HOST, () => {
  console.log(`Server is running on port ${PORT}`);
});