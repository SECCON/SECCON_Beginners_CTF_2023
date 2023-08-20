package main

import (
	"strings"
	"syscall/js"
)

var keyUrl = "/enc.key"
var cnt = 0
var intervalId js.Value

func Load(this js.Value, args []js.Value) interface{} {
	window := js.Global()
	key := [16]byte{99, 9, 61, 110, 94, 114, 119, 194, 42, 163, 63, 8, 97, 114, 131, 41}
	bytes := window.Get("Uint8Array").New(len(key))
	js.CopyBytesToJS(bytes, key[:])
	window.Get("gContext").Get("keyInfo").Get("decryptdata").Set("key", bytes)

	intervalId = window.Call("setInterval", js.FuncOf(func(this js.Value, args []js.Value) interface{} {
		if strings.HasSuffix(window.Get("gContext").Get("url").String(), keyUrl) {
			window.Get("gContext").Get("keyInfo").Get("decryptdata").Set("key", bytes)
		}
		cnt += 1
		if cnt > 1000 {
			window.Call("clearInterval", intervalId)
			window.Set("gContext", nil)
		}
		return nil
	}), 10)
	return nil
}

func main() {
	c := make(chan struct{})
	js.Global().Set("hlscotext", js.ValueOf(
		map[string]any{
			"load": js.FuncOf(Load),
		},
	))
	<-c
}
