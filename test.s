.code32
.section .data:
ga:
  .fill 1,4,0
gb:
  .fill 1,4,0

.section .code:
.globl func
  pushl %ebp
  movl %esp, %ebp
  movl ga, -4(%ebp)
  addl $1, -4(%ebp)
  movl -4(%ebp), -8(%ebp)
  movl %ebp, %esp
  popl %ebp
  ret

.globl main
  pushl %ebp
  movl %esp, %ebp
  movl $10, -4(%ebp)
  movl $10, -8(%ebp)
  movl $20, -12(%ebp)
  movl $3001, -16(%ebp)
  movl $0, %edx
  movl $1, %eax
  mull $20
  movl %eax, -824(%ebp)
  addl $2, -824(%ebp)
  movl %ebp, %eax
  addl 824, %eax
  movl $10, -24(%ebp, %eax, 4)
  movl $0, -4(%ebp)
L2:
  cmpl -4(%ebp), $20
  ja L0
  movl $0, -828(%ebp)
  jmp L1
L0:
  movl $1, -828(%ebp)
L1:
  cmpl $0, -828(%ebp)
  jz L3
  addl $2, -12(%ebp)
  addl $1, -4(%ebp)
  jmp L2
L3:
  movl %ebp, %esp
  popl %ebp
  movl $0, %eax
  ret
  movl %ebp, %esp
  popl %ebp
  ret

