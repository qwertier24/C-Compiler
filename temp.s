.code32
.data:
_s0:
  .ascii "%d\n\0"

.code:
.globl _main
_main:
  pushl %ebp
  movl %esp, %ebp
  subl $8, %esp
  movl $1, %eax
  pushl %eax
  movl $_s0, %eax
  movl %eax, -4(%ebp)
  movl -4(%ebp), %eax
  pushl %eax
  call _printf
  addl $8, %esp
  movl %ebp, %esp
  popl %ebp
  ret

