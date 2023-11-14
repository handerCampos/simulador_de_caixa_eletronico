import sqlite3
from time import sleep

print('='*30)
print('{:^30}'.format('SIMULADOR DE CAIXA ELETRONICO'))
print('='*30)

#CRIANDO O BANCO DE DADOS E A TABELA PARA A SIMULAÇÃO DO SALDO.
try:
    banco = sqlite3.connect('simulacao_de_banco.db')
    cursor = banco.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS controle_de_saldo (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    saldo VARCHAR(50) NOT NULL
    );
    ''')
    banco.close()
    print('TABELA PARA SIMULAÇÃO DO BANCO CRIADA COM SUCESSO')
except sqlite3.Error as erro:
    print('ERRO AO CRIAR A TABELA PARA A SIMULAÇÃO DO BANCO: ', erro)

try:
    banco = sqlite3.connect('simulacao_de_banco.db')
    cursor = banco.cursor()
    cursor.execute('SELECT * FROM controle_de_saldo')
    dados_do_banco = cursor.fetchall()
    print(dados_do_banco)
    if dados_do_banco == []:
        # INSERINDO O SALDO PARA A SIMULAÇÃO
        try:
            banco = sqlite3.connect('simulacao_de_banco.db')
            cursor = banco.cursor()
            cursor.execute('INSERT INTO controle_de_saldo (saldo) VALUES ("3000")')
            banco.commit()
            banco.close()
            print('O SALDO FOI INSERIDO COM SUCESSO!')
        except sqlite3.Error as erro:
            print('NÃO FOI POSSIVEL INSERIR O SALDO. ')
    else:
        try:
            banco = sqlite3.connect('simulacao_de_banco.db')
            cursor = banco.cursor()
            cursor.execute('SELECT * FROM controle_de_saldo')
            leitura_da_tabela = cursor.fetchall()[0][1]
            print(f'Dados da tabela : {leitura_da_tabela}')
        except sqlite3.Error as erro:
            print('NÃO FOI POSSIVEL LER OS DADOS DA TABELA!')
        saldo = int(leitura_da_tabela)
        print('{:^30}'.format('SEU SALDO É DE R$' + leitura_da_tabela))
        valor = int(input('Qual valor deseja sacar? R$:'))
        # tratando o saldo insuficiente
        try:
            if valor > saldo:
                resposta = str(input('SALDO INSUFICIENTE. '
                                     'Deseja sacar um valor disponivel em conta? [S/N] '))

                while resposta != 'S' and 'N' or resposta != 's' and 'n':
                    resposta = str(
                        input('RESPOSTA INVÁLIDA, PRESSIONE S para prosseguir ou N para cancelar a operação: '))
                    if resposta == 'S' or 'N':
                        break
                if resposta == 'S':
                    valor = int(input('Qual valor deseja sacar? R$:'))
                    while valor > saldo:
                        print(f'SEU SALDO ATUAL É DE R$ {saldo}')
                        resposta = str(input('Deseja continuar com a operação? [S/N]: '))
                        if resposta == 'S' or resposta == 's':
                            valor = int(input(f'Digite um valor menor ou igual a R${saldo}. R$: '))
                            if valor <= saldo:
                                break
                            else:
                                print('OPERAÇÃO CANCELADA DEVIDO A UM ERRO INESPERADO.')
                        elif resposta == 'N' or resposta == 'n':
                            print('operação canselada pelo usuário com sucesso.')
                            break
                        else:
                            print('resposta inválida, tente novamente.')

                    valortotal = valor
                    cedula = 50
                    totalcedula = 0
                    while True:
                        if valortotal >= cedula:
                            valortotal -= cedula
                            totalcedula += 1
                        else:
                            if totalcedula > 0:
                                print(f'Total de {totalcedula} cédula de R${cedula} ')
                            if cedula == 50:
                                cedula = 20
                            elif cedula == 20:
                                cedula = 10
                            if cedula == 10:
                                cedula = 1
                            totalcedula = 0
                            if valortotal == 0:
                                break
                elif resposta == 'N':
                    print('operação cancelada pelo usuário.')
            elif valor <= saldo:
                valortotal = valor
                cedula = 50
                totalcedula = 0
                while True:
                    if valortotal >= cedula:
                        valortotal -= cedula
                        totalcedula += 1
                    else:
                        if totalcedula > 0:
                            print(f'Total de {totalcedula} cédula de R${cedula} ')
                        if cedula == 50:
                            cedula = 20
                        elif cedula == 20:
                            cedula = 10
                        if cedula == 10:
                            cedula = 1
                        totalcedula = 0
                        if valortotal == 0:
                            saldoAtual = saldo - valor
                            print(saldoAtual)
                            # atualizando o saldo no banco de dados.
                            try:
                                banco = sqlite3.connect('simulacao_de_banco.db')
                                banco = banco.cursor()
                                cursor.execute('SELECT id FROM controle_de_saldo')
                                id = cursor.fetchall()[0][0]
                                print(f'o id lido é : {id}')
                                banco.close()
                            except sqlite3.Error as erro:
                                print('erro ao retornar id')
                            try:
                                banco = sqlite3.connect('simulacao_de_banco.db')
                                cursor = banco.cursor()
                                cursor.execute(" UPDATE controle_de_saldo SET saldo = ? WHERE id = ? ",
                                               (str(saldoAtual), str(id)))
                                banco.commit()
                                banco.close()
                                sleep(1)
                                print(saldoAtual)
                                print('Saldo atualizado com sucesso!')
                            except sqlite3.Error as erro:
                                print(f'Erro ao atualizar o saldo no banco de dados erro ({erro})')
                            try:
                                # lendo o saldo atualizado no banco de dados
                                banco = sqlite3.connect('simulacao_de_banco.db')
                                cursor = banco.cursor()
                                cursor.execute('SELECT saldo FROM controle_de_saldo WHERE id = 1')
                                leituradosaldo = cursor.fetchall()[0][0]
                                print(f'O novo saldo da tabela é R$ {leituradosaldo}')
                                break
                            except sqlite3.Error as erro:
                                print('Erro ao ler o saldo atualizado')

        except sqlite3.Error as erro:
            print(f'operação não executada {erro}')
except sqlite3.Error as erro:
    print(f'teste de leitura não executado erro{erro}')
print('=' * 30)
print('simulação encerrada')


