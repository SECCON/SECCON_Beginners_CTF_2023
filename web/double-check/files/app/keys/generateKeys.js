const { generateKeyPairSync } = require("crypto");
const fs = require("fs");
const path = require("node:path");

function generateRSAKeyPair() {
  const { publicKey, privateKey } = generateKeyPairSync("rsa", {
    modulusLength: 4096,
    publicKeyEncoding: { type: "spki", format: "pem" },
    privateKeyEncoding: { type: "pkcs8", format: "pem" },
  });
  return { publicKey, privateKey };
}

const { publicKey, privateKey } = generateRSAKeyPair();
fs.writeFileSync(path.join(__dirname, "private.key"), privateKey);
fs.writeFileSync(path.join(__dirname, "public.key"), publicKey);