import { execSync } from "child_process";
import fs from "fs";
import crypto from "crypto";

class FFmpeg {
  constructor(public dirPath: string) {}
  async mp4ToPng() {
    execSync(
      `ffmpeg -i video.mp4 -vcodec png -r 30 ${this.dirPath}/images/%03d.png`
    );
  }
}

function main() {
  const dirPath = "./dist-tools";
  fs.mkdirSync(`${dirPath}/images`);
  const ffmpeg = new FFmpeg(dirPath);
  try {
    ffmpeg.mp4ToPng();
  } catch (e) {
    console.log(e);
    return "ffmpeg error";
  }

  const imageHashes: string[] = [];
  fs.readdirSync(`${dirPath}/images`).forEach((file: string) => {
    const image = fs.readFileSync(`${dirPath}/images/${file}`);
    const imageHash = crypto.createHash("sha256").update(image).digest("hex");
    imageHashes.push(imageHash);
  });

  const hashes = {
    image: imageHashes,
  };
  fs.writeFileSync("dist/hashes.json", JSON.stringify(hashes, null, "  "));
}
main();
