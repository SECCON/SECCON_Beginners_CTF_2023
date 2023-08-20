.intel_syntax noprefix
.data
.Lstack_32bit:
.long .Lcalc_xor_32
.long 0x23

.Lstack_64bit:
.long .Lcalc_xor_64
.long 0x33

.text
.global calc_xor
calc_xor:
  push rbp
  mov rbp, rsp
  lea esp, .Lstack_32bit
  retf
  .Lcalc_xor_32:
  mov eax, edi

  xor rax, rsi

  lea esp, .Lstack_64bit
  retf
  .Lcalc_xor_64:
  mov rsp, rbp
  pop rbp
  ret
