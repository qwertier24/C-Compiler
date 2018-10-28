from django.shortcuts import render
from django.http import JsonResponse
import ccompiler
import subprocess

# Create your views here.

def index(request):
    return render(request, "index.html")

def gen_asm(codes):
    # temp.txt to temp.s
    return ccompiler.compile(codes)

def run(request):
    input = request.POST['input']
    codes = request.POST['codes']
    asm = gen_asm(codes)
    open("input.txt", "w").write(input)
    # str(self.file.read(1), encoding='utf-8')
    result = subprocess.run(["g++", "-m32", "temp.s", "-o", "temp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        return JsonResponse({"message": str(result.stderr, encoding='utf-8')})
    with open("input.txt", "w") as f:
        f.write(input)
    with open("input.txt", "rb") as f:
        result = subprocess.run(["temp"], stdin=f, stdout=subprocess.PIPE, encoding='utf-8')
    return JsonResponse({"output":result.stdout, "verdict":"success"})

def compile(request):
    codes = request.POST['codes']
    output = gen_asm(codes)
    return JsonResponse({"output":output, "verdict":"success"})
