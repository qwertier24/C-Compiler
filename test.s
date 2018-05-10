.code32
.section .data:
ga:
  .fill 1,4,0
gb:
  .fill 1,4,0

.section .code:
.globl func
func:
  pushl %ebp
  movl %esp, %ebp
  subl $0, %esp
  movl %ebp, %esp
  popl %ebp
  ret

.globl main
main:
  pushl %ebp
  movl %esp, %ebp
  subl $824, %esp
  movl $10, %eax
  movl %eax, -4(%ebp)
  movl $10, %eax
  movl %eax, -8(%ebp)
  movl $20, %eax
  movl %eax, -12(%ebp)
  movl $3001, %eax
  movl %eax, -16(%ebp)
  movl %ebp, %esp
  popl %ebp
  ret

