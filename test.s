.data
;; .global hello
hello:
.ascii "Hi World\n"

.text
.global main
main:
    pushq   %rbp
    movq    %rsp,       %rbp
    movq    $hello,     %rdi
    call    puts@PLT
    movq    $0,         %rax
    leave
    ret
