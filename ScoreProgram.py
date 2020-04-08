import sys
import subprocess
import os


def compile(cmd):
  fd = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  fd.communicate()
  return fd.stdout, fd.stderr


def execute(cmd, lines):
  fd = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  out, err = fd.communicate(input=lines, timeout=1)
  return out.decode('utf-8')


path = './hw'

for root, dirs, files in os.walk(path):
  for file in files:
    cmd = ''
    # 제출파일 명이 바뀔 경우 split 코드 수정
    fname, ext = file.split('.')
    stuno, name = fname.split('_')
    
    if(ext == 'c'):
      cmd = 'gcc -o '+fname+' '+path+'/'+file
    elif(ext == 'cpp'):
      cmd = 'g++ -o '+fname+' '+path+'/'+file

    test = compile(cmd)
    cmd2 = fname+'.exe'

    inputFile = open('./static/input.txt')
    inputs = bytes('', 'utf-8')

    for line in inputFile.readlines():
      input_line = line.rstrip('\n')
      inputs = inputs+bytes(input_line+'\n', 'utf-8')
    result = execute(cmd2, inputs)
    rresult = ''
    for i in result.split():
      rresult = rresult+i+'\n'
    fp = open('./output/'+fname+'output.txt', 'w')
    fp.write(rresult)
    fp.close()

    fp = open('./output/'+fname+'output.txt')
    fp2 = open('./static/output.txt')
    cmp1 = fp.readlines()
    cmp2 = fp2.readlines()
    flag=1;
    # print(cmp1, cmp2)
    if(len(cmp1) == len(cmp2)):
      for i in range(len(cmp1)):
        if(cmp1[i].rstrip('\n') != cmp2[i].rstrip('\n')):
          print('fail')
          flag=0;
          break;
      # 여기에서 CSV나 엑셀로 정리하는 걸 할까?
      if flag==1:
        print(stuno, name, 'success')
      else:
        print(stuno, name, 'fail')
    else:
      print(stuno, name, 'fail')
    os.remove('./'+cmd2)
