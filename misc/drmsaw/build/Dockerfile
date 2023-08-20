# build wasm
FROM golang:1.18 AS wasm-builder

WORKDIR /app
COPY wasm .

RUN GOOS=js GOARCH=wasm go build -o main.wasm main.go

# build app
From node:18 AS ts-builder

COPY app/package.json app/tsconfig* app/yarn.lock app/video.mp4 /app/
COPY app/src/ /app/src/
COPY app/tools/ /app/tools/
COPY app/public/videos/_enc.key /app/public/videos/enc.key

WORKDIR /app

RUN apt-get update && apt-get install -y ffmpeg

RUN mkdir dist
RUN yarn
RUN yarn build

RUN echo "video://hello_where_is_my_key?\nenc.key" > ./public/videos/enc.keyinfo
RUN cd ./public/videos && ffmpeg -i ../../video.mp4 -c copy -hls_key_info_file enc.keyinfo -f hls -hls_time 3 -hls_list_size 0 -muxdelay 0 -hls_flags split_by_time video.m3u8

RUN cd ./public/videos && rm enc.key enc.keyinfo && echo "This key is a dummy. How can it be played without the key file?" > enc.key

# Run Express
FROM node:18

COPY app/public/index.html app/public/wasm_exec.js /app/public/

COPY --from=wasm-builder /app/main.wasm /app/public/
COPY --from=ts-builder /app/dist/ /app/dist/
COPY --from=ts-builder /app/node_modules/ /app/node_modules/
COPY --from=ts-builder /app/public/videos/ /app/public/videos/

RUN apt-get update && apt-get install -y ffmpeg

WORKDIR /app

CMD ["node", "dist/index.js"]
