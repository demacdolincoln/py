#!/usr/bin/python
# -*- coding: utf-8 -*-
#Filename: downoff.py

#a função deste script é criar um arquivo HTML com os links para download dos pacotes das atualizações diponíveis em sistemas Debian-like

import os #permite acessar alguns recursos do sistema, assim como gerenciar arquivos e diretórios
import commands #permite usa os comandos do shell usado pelo sistema
import operator #permite fazer operações matemáticas, aqui o utilizei para fazer repetições

print ("iniciando o apt-get --print-uris")
endre = commands.getoutput("sudo apt-get -qq --print-uris upgrade && echo \" \"")
f = open('link.txt', 'w')
f.write(endre)
f.close()

print("""estágio concluido
      iniciando o redirecionamento dos endereços""")
linkss = (commands.getoutput("cut -d \\' -f 2 link.txt"))
f = open('link2.txt', 'w')
f.write(linkss)
f.close()

print('verificando o número de linhas')
linhas = int(commands.getoutput("cat link2.txt | wc -l"))


print ('criando as colunas')
rep1 = operator.repeat('<address><a href="\n', linhas)
f = open('col1', 'w')
f.write(rep1)
f.close()

print ('coluna 1 concluida')
rep2 = operator.repeat('"><span style="font-family: serif;">\n', linhas)
f = open('col2', 'w')
f.write(rep2)
f.close()

print('coluna 2 concluida')
rep3 = operator.repeat ('</span></a></address>\n', linhas)
f = open('col3', 'w')
f.write(rep3)
f.close()

print ('coluna 3 concluida')
linksfinal = str(commands.getoutput("paste col1 link2.txt col2 link2.txt col3"))

print ('criando e organizando o arquivo HTML')

f = open('downoff.html', 'w')
f.write('<body><h3 style=\"text-align: center;\">DownOff<br></h3><br>\"')
f.write(linksfinal)
f.write ("\n")
f.write('<div style=\"text-align: center;\">DownOff<br></div></body>\"')

print ('removendo arquivos temporários')
commands.getoutput("rm col1 col2 col3 link.txt link2.txt")
print """script finalizado com sucesso
abra o arquivo downoff.html no Firefox e use a extenção DownThemAll para baixar todos os links"""