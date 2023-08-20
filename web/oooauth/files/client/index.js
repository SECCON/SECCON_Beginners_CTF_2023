const path = require("path");
const express = require("express");
const session = require("express-session");
const crypto = require("crypto");
const logger = require("morgan");
const axios = require("axios");

const HOST = process.env.HOST;
const PORT = process.env.PORT;
const CLIENT_URL = process.env.CLIENT_URL || "http://localhost:3000";
const SERVER_URL = process.env.SERVER_URL || "http://localhost:3001";
const CLIENT_ID = process.env.CLIENT_ID;
const CLIENT_SECRET = process.env.CLIENT_SECRET;

const app = express();
app.use(logger("common"));

app.set("views", path.join(__dirname, "views"));
app.set("view engine", "ejs");

// Session
app.use(session({
  secret: crypto.randomBytes(16).toString("hex"),
  resave: false,
  saveUninitialized: true,
  cookie: { secure: false }
}));

app.use(function(req, res, next) {
  // CSP Setting
  const nonce = crypto.randomBytes(8).toString("hex");
  req.nonce = nonce; 
  res.setHeader("Content-Security-Policy", `script-src 'nonce-${nonce}'; connect-src 'self'; base-uri 'self'; object-src 'none';`);
  return next();
});

app.get("/", (req, res) => {
  res.render("index", { 
    username: req.session.username, 
    scopes: req.session.scopes, 
    nonce: req.nonce 
  });
});

app.get("/auth", (req, res) => {
  // Send Authorization Request
  console.log("SERVER_URL:", SERVER_URL);
  const authUrl = new URL(`${SERVER_URL}/auth`);

  authUrl.searchParams.append("response_type", "code"); // Use Authrozation Code Grant
  authUrl.searchParams.append("client_id", CLIENT_ID);
  authUrl.searchParams.append("redirect_uri", `${CLIENT_URL}/callback`);
  authUrl.searchParams.append("scopes", "email profile");

  res.redirect(authUrl.href);
});

app.get("/callback", async(req, res) => {
  if (req.query.error) {
    res.render("error", { error: req.query.error, error_description: req.query.error_description });
    return;
  }

  // Send Access Token Request
  const params = req.query;
  params.grant_type = "authorization_code";
  params.redirect_uri = `${CLIENT_URL}/callback`;
  const tokenUrl = "http://server:3001/token";

  try {
    const response = await axios.post(tokenUrl, params, {
      headers: { 
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": "Basic " + Buffer.from(CLIENT_ID + ":" + CLIENT_SECRET).toString("base64")
      }
    });
    if (response.data.access_token) {
      req.session.username = response.data.username;
      req.session.access_token = response.data.access_token;
      req.session.scopes = response.data.scopes;
    }
  } catch(err) {
    res.render("error", { 
      error: err.response.data.error, 
      error_description: err.response.data.error_description 
    });
    return;
  }

  res.render("index", { 
    username: req.session.username, 
    scopes: req.session.scopes, 
    nonce: req.nonce 
  });
});

app.get("/flag", async(req, res) => {
  if (!req.session.access_token) {
    res.render(
      "error", { 
        error: "you are not logged in", 
        error_description: ""
    });
    return;
  }
  const flagUrl = "http://server:3001/flag";
  const params = new URLSearchParams();
  params.append("access_token", req.session.access_token);
  try {
    const response = await axios.post(flagUrl, params, {
      headers: { "Content-Type": "application/x-www-form-urlencoded" }
    });
    res.send(response.data);
  } catch(err) {
    res.render("error", { 
      error: err.response.data.error, 
      error_description: "" 
    });
  }
});

app.post("/logout", async(req, res) => {
  req.session.destroy();
  res.redirect("/");
});


app.listen(PORT, HOST, () => {
  console.log(`OAuth client listening at http://${HOST}:${PORT}`);
});
