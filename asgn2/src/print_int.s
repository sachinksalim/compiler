
__printInt:
    movl 4(%esp), %ecx
    cmpl $0, %ecx
    jge __positive
    notl %ecx
    inc %ecx
    movl %ecx, %edi
    movl $45, %eax
    pushl %eax
    movl $4, %eax
    movl $1, %ebx
    movl %esp, %ecx
    movl $1, %edx
    int $0x80
    popl %eax
    movl %edi, %ecx

__positive:
    movl %ecx, %eax
    movl %esp, %esi

__iterate:
    cdq
    movl $10, %ebx
    idivl %ebx
    pushl %edx
    cmpl $0, %eax
    jne __iterate
    jmp __printNum
    
__printNum:
    popl %edx
    addl $48, %edx
    pushl %edx
    movl $4, %eax
    movl $1, %ebx
    movl %esp, %ecx
    movl $1, %edx
    int $0x80
    popl %edx
    cmp %esp, %esi
    jne __printNum
    movl $4, %eax
    movl $1, %ebx
    movl $new, %ecx
    movl $1, %edx
    int $0x80
    ret
