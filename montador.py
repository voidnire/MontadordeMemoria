import sys


def binInst(pal):
  if pal == "add" or pal == "ADD":
    return [1, 0, 0, 0]
  if pal == "shr" or pal == "SHR":
    return [1, 0, 0, 1]
  if pal == "shl" or pal == "SHL":
    return [1, 0, 1, 0]
  if pal == "NOT" or pal == "not":
    return [1, 0, 1, 1]
  if pal == "AND" or pal == "and":
    return [1, 1, 0, 0]
  if pal == "or" or pal == "OR":
    return [1, 1, 0, 1]
  if pal == "xor" or pal == "XOR":
    return [1, 1, 1, 0]
  if pal == "CMP" or pal == "cmp":
    return [1, 1, 1, 1]
  if pal == "LD" or pal == "ld":
    return [0, 0, 0, 0]
  if pal == "ST" or pal == "st":
    return [0, 0, 0, 1]

  if pal == "data" or pal == "DATA":
    return [0, 0, 1, 0, 0, 0]
  if pal == "jmpr" or pal == "JMPR":
    return [0, 0, 1, 1, 0, 0]
  if pal == "jmp" or pal == "JMP":
    return [0, 1, 0, 0, 0, 0, 0, 0]
  if pal == "jcaez" or pal == "JCAEZ":
    return [0, 1, 0, 1, 1, 1, 1, 1]
  if pal == "CLF" or pal == "clf":
    return [0, 1, 1, 0, 0, 0, 0, 0]
  return [0, 0, 0, 0, 0, 0, 0, 0]

def binR(pal):
  if pal == "r1" or pal == "R1":
    return [0, 1]
  if pal == "r0" or pal == "R0":
    return [0, 0]
  if pal == "r2" or pal == "R2":
    return [1, 0]
  if pal == "r3" or pal == "R3":
    return [1, 1]

def dataInst(vet, pal):
  vet.append(pal)  
  return vet#o endereço ta guardado como string no fim do vetor

def proBinario(instruc):  #traduz uma linha por vez pra binario
  instruc = instruc.replace(',', ' ')
  palavras = instruc.split()
  
  vetbin = []
  vetaux = []
  count = 0
  instrucao = ""
  for palavra in palavras:
    if count == 0:
      if palavra == "CLF" or palavra == "clf":
        return binInst(palavra)
        
      instrucao = palavra
      vetaux = binInst(palavra)
      #if vetbin is not None:
      vetbin.append(vetaux)

    if count == 1:
      if instrucao == "JCAEZ" or instrucao == "jcaez" or instrucao == "JMP" or instrucao == "jmp":
        dataInst(vetbin, palavra)
        return vetbin

      vetaux = binR(palavra)

      if vetbin is not None:
        vetbin.append(vetaux)
      if (instrucao == "JMPR" or instrucao == "jmpr"):
        return vetbin

    if count == 2:
      if instrucao == "DATA" or instrucao == "data":
        return dataInst(vetbin, palavra)

      vetbin.append(binR(palavra))

    count += 1
  return vetbin

def bintoHex(vetor_binario):
  binario = ''.join(str(digito) for digito in vetor_binario)

  decimal = int(binario, 2)

  hexadecimal = hex(decimal)[2:].upper()
  return hexadecimal



def linhaporlinha(assembly_file, vet):  # Abre o arquivo assembly e retorna o binario
  with open(assembly_file, 'r') as arquivo:
      linhas = arquivo.readlines()
  linhas = linhas[1:]  # Ignora a primeira linha do arquivo

  for linha in linhas:
      linha = linha.strip()  
    
      if not linha or linha.startswith(';') or linha.startswith(".data") or linha.startswith(".DATA"):
          continue  # remove comentários ao final da linha
      if ';' in linha:
          linha = linha.split(';')[0].strip()  # divide em duas partes e pega só a 1°
    
      if linha.startswith("word") or linha.startswith("WORD"):#guarda apenas o numero para a memoria
        ultimo = linha.split()[-1]
        
        if ultimo.startswith("0x"):
          ul = str(ultimo)
          ultimo = ul[2:]

        vet.append(ultimo)
        continue
      
      lista = proBinario(linha)  # lê cada linha e transforma em binário
      endereco = ""
      end = ""
      ultimo = str(lista[-1])
      if ultimo.startswith("0x"):#ve se tem endereço no ultimo elemento da lista
        endereco = lista[-1]
        endstr = str(endereco)
        end = endstr[2:]
        lista.pop()
        
      binarios = []
      if any(isinstance(elemento, list) for elemento in lista):#verifica se tem sublistas na lista
        binarios = [item for sublist in lista for item in sublist]
      else:
        binarios=lista
      
    
      hexa = bintoHex(binarios)
      
      vet.append(hexa)
      if endereco != "":
        vet.append(end)

def write_outputfile(memory_file,vet):
  with open(memory_file, "w") as f:
    x = 0
    f.write('v3.0 hev words plain')
    for i in range(0, 16):
      f.write('\n')
      for j in range(0, 16):
        if x < len(vet):
          f.write(vet[x]+" ")
          x+=1
        else:
          f.write("00 ")


def main(mem_file,assembly_file):
  vet = []
  linhaporlinha(assembly_file, vet)
  write_outputfile(mem_file,vet)


if __name__ == '__main__':
  n = len(sys.argv)

  assert n == 3, 'number argument error'
  main(sys.argv[1],sys.argv[2])
  
#terminal:  python3 montador.py saida.m teste.asm 
