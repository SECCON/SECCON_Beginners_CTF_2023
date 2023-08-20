
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

function generateRandomString() {
    return crypto.randomBytes(16).toString("hex");
}

let adminPass = generateRandomString();

function readKeyFromFile(filename) {
    return fs.readFileSync(path.join(__dirname, filename));
}

function getAdminPassword() {
    return adminPass;
}

module.exports = {
    readKeyFromFile,
    generateRandomString,
    getAdminPassword
}