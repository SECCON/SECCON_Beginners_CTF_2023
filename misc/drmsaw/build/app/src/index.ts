import express from "express";
import path from "path";
import flagCheck from "./flagCheck";
import multer from "multer";
const upload = multer();

const app = express();
const port = process.env.PORT || 3000;

app.get("/", function (_req, res) {
  res.sendFile(path.join(__dirname, "../public/index.html"));
});
app.get("/main.wasm", function (_req, res) {
  res.sendFile(path.join(__dirname, "../public/main.wasm"));
});
app.get("/wasm_exec.js", function (_req, res) {
  res.sendFile(path.join(__dirname, "../public/wasm_exec.js"));
});
app.get("/enc.key", function (req, res) {
  res.sendFile(path.join(__dirname, "../public/videos/enc.key"));
});

app.get("/public/videos/:id", function (req, res) {
  res.sendFile(path.join(__dirname, `../public/videos/${req.params.id}`));
});

app.post("/flag", upload.single("video"), async function (req, res) {
  const file = req.file;
  if (!file) {
    res.send("no video file");
    return;
  }
  const resMes = flagCheck(file);
  res.send(resMes);
});

app.listen(port, () => {
  console.log(`Server started at http://localhost:${port}`);
});
