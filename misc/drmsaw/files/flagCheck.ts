import { v4 as uuidv4 } from "uuid";
import { execSync } from "child_process";
import fs from "fs";
import crypto from "crypto";

const FLAG = process.env.FLAG || "ctf4b{dummy_flag}";

class FFmpeg {
  constructor(public dirPath: string) {}
  async mp4ToPng() {
    execSync(
      `ffmpeg -i ${this.dirPath}/video.mp4  -vcodec png -r 30 ${this.dirPath}/images/%03d.png`
    );
  }
}

function flagCheck(file: Express.Multer.File) {
  // save video file
  const uuid = uuidv4();
  const dirPath = `/tmp/${uuid}`;
  fs.mkdirSync(`${dirPath}/images`, { recursive: true });
  fs.writeFileSync(`${dirPath}/video.mp4`, file.buffer);

  // check mimetype
  if (file.mimetype !== "video/mp4") {
    return "mimetype is not video/mp4";
  }

  // convert video to image and audio
  const ffmpeg = new FFmpeg(dirPath);
  try {
    ffmpeg.mp4ToPng();
  } catch (e) {
    console.log(e);
    return "ffmpeg error";
  }

  // get hashes
  const imageHashes: string[] = [];
  fs.readdirSync(`${dirPath}/images`).forEach((file) => {
    const image = fs.readFileSync(`${dirPath}/images/${file}`);
    const imageHash = crypto.createHash("sha256").update(image).digest("hex");
    imageHashes.push(imageHash);
  });

  fs.rm(dirPath, { recursive: true }, (err) => {
    if (err) throw err;
  });

  const hashes = JSON.parse(fs.readFileSync("dist/hashes.json", "utf8"));
  for (let i = 0; i < 30; i++) {
    const idx = Math.floor(Math.random() * hashes.image.length);
    if (!imageHashes.includes(hashes.image[idx])) {
      return "Sorry, the video you submitted is a fake.";
    }
  }
  return `(｡˃ ᵕ ˂ ) Congratulation! ${FLAG}`;
}

export default flagCheck;
