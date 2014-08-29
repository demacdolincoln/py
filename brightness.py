#!/usr/bin/python3
# -*- encoding: utf-8 -*-
'''
aplicativo criado devido a dificuldades enfrentadas para
alterar o brilho do monitor com os recursos nativos do sistema

antes de usa-lo, edite como super usuário o arquivo /etc/rc.local adicionando esta linha antes do "exit"
chmod go+w /sys/class/backlight/acpi_video0/brightness
também execute o comando acima como super usuário para testar este aplicativo sem precisar reiniciar
ou pode simplesmente usar o parâmetro '-c' neste script
'''

import argparse
import textwrap
import os
import subprocess

arq = "/sys/class/backlight/acpi_video0/brightness" #arquivo responsável pelo ajuste de brilho
conf = "/etc/rc.local" #arquivo original de configurações


def config():
	'''
	adiciona o comando
	'chmod go+w /sys/class/backlight/acpi_video0/brightness'
	na penútima linha do arquivo /etc/rc.local
	a fim de que seja executado na inicialização

	também altera as premissões do arquivo já citado
	para que qualquer seja possível edita-lo sem reiniciar o sistema
	'''
	bkp = conf+'.bkp' #arquivo de backup
	try:
		#	fazendo backup do arquivo de configuração
		
		fOrigin = open(conf, 'r')
		fCopy = open(bkp, 'w')

		fCopy.write(fOrigin.read())

		fOrigin.close()
		fCopy.close()
		print("arquivo original copiado para \n" + conf + '.bkp')

		# 	adicionando um comando na penúltima linha
		fBkp = open(bkp, 'r')
		fMod = open(conf, 'w')

		listArq = fBkp.readlines()
		
		nLine = len(listArq) - 1

		newCont = ''

		for i in range(nLine):
			newCont = newCont + listArq.readlines[i]

		newCont = newCont + '\n' + 'chmod go+w ' + arq + '\n' + 'exit 0' + '\n'

		fMod.write(newCont)
		fMod.close()
		fBkp.close()

		print(textwrap.dedent('''
			alterações no arquivo {cf} concluídas, agora ao iniciar
			você poderá alterar livremente o arquivo
			{aq}
			responsável pelas alterações de brilho do monitor
			''' .format(cf=conf, aq=arq)))

		os.chmod(arq, 438) #altera a permissao do arquivo para leitura e escrita para todos os usuários

		print(textwrap.dedent('''também foi alterada a permissão do arquivo
			{aq}
			para que possa utilizar este script desde já'''.format(aq=arq)))
	except Exception:
		print('-' * 20)
		print('excute como super usuário')
		print('-' * 20)

def verifica_config():
	'''antes de iniciar a função para alterar as configurações
	esta função verifica se as alteraçoes já foram feitasS'''

	fVeri = open(conf, 'r')
	veri = str(fVeri.read())
	fVeri.close()

	if arq in veri:
		config()
	else:
		opt = input(textwrap.dedent('''
				o arquivo já está configurado corretamente,
				mesmo assim deseja continuar?
				[s = sim | n = não]
			'''))
		if opt == 's':
			config()
		else:
			pass

def upBright(percent):
	'''aumenta o brilho da tela'''

	f = open(arq, 'r')
	brilho = int(f.read())
	f.close()

	brilho = brilho + percent

	f = open(arq, 'w')

	if brilho > 100:
		f.write('100')
		f.close()
	else:
		f.write(str(brilho))
		f.close()

	subprocess.call(['notify-send', '-u', 'normal', 'Brightness', str(brilho)])


def downBright(percent):
	'''diminui o brilho da tela'''

	f = open(arq, 'r')
	brilho = int(f.read())
	f.close()

	brilho = brilho - percent

	f = open(arq, 'w')

	if brilho < 5:
		f.write('5')
		f.close()
	else:
		f.write(str(brilho))
		f.close()

	subprocess.call(['notify-send', '-u', 'normal', 'Brightness', str(brilho)])

def setBright(percent):
	'''aumenta o brilho da tela'''

	newPerc = str(percent)

	f = open(arq, 'w')

	if percent > 100:
		f.write('100')
		f.close()
	elif percent < 5:
		f.write('5')
		f.close()
	else:
		f.write(newPerc)
		f.close()

	subprocess.call(['notify-send', '-u', 'normal', 'Brightness', newPerc])

if __name__ == '__main__':

	parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
									description=textwrap.dedent('''\
										este script foi criado para permitir que fosse possível atribuir a teclas de função
										e atalhos de teclado as opções de ajuste de brilho do monitor e ao final do ajuste
										ele ainda exibe uma notificação na área de trabalho.
										'''),
									epilog=textwrap.dedent('''
										exemplo de uso:
										
										$ python brightness.py -u 20 -> aumenta em 20% o brilho do monitor

										este script aceita a quantidade máxima de brilho em 100% e a mínima em 5%,
										caso colocoque algum número que exceda estes valores, ele define o brilho
										no seu limite máximo, ou mínimo.
										'''))

	# parâmetros:
	parser.add_argument('-u', '--up', action='store', dest='up',
						type=int,  required=False, help='aumenta o brilho do monitor')
	parser.add_argument('-d', '--down', action='store', dest='down',
						type=int, required=False, help='diminui o brilho do monitor')
	parser.add_argument('-s', '--set', action='store', dest='set',
						type=int, required=False, help='define a porcentagem de brilho do monitor')
	parser.add_argument('-c', '--conf', action='store_true',
						required=False, help='ajusta as configurações')

	args = parser.parse_args()

	# verificando as permissões
	
	mod = str(subprocess.check_output(['ls', '-l', arq]))
	
	if '-rw-rw-rw-' in mod:
		if args.conf:
			verifica_config()
		if args.up:
			upBright(args.up)
		if args.down:
			downBright(args.down)
		if args.set:
			setBright(args.set)

	else:
		print(textwrap.dedent(''' 
			você não tem permissão de alterar o arquivo {aq} 

			para alterar o brilho por favor,
			execute este script como super usuário passando o parâmetro '-c'
			''' .format(aq=arq)))