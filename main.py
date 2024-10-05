import zipfile
import tarfile
import string
import zlib
import time
import os
import itertools
import string
import sys
import requests  # Importando requests para fazer requisições
from colorama import init, Fore, Style
from tqdm import tqdm

# Inicializa o colorama para garantir que funcione em qualquer terminal
init(autoreset=True)

# Exibir a mensagem inicial em branco
os.system('clear' if os.name == 'posix' else 'cls') 
print(Fore.BLUE + """
__  __ _____ _   _ _   _   ____  _____
|  \/  | ____| \ | | | | | |  _ \| ____|  
| |\/| |  _| |  \| | | | | | | | |  _|  
| |  | | |___| |\  | |_| | | |_| | |___  
|_|  |_|_____|_| \_|\___/  |____/|_____|  

  ____ ___  _   _ ____  _   _ _   _____  _  
 / ___/ _ \| \ | / ___|| | | | | |_   _|/ \  
| |  | | | |  \| \___ \| | | | |   | | / _ \  
| |__| |_| | |\  |___) | |_| | |___| |/ ___ \  
\____\___/|_| \_|____/ \___/|_____|_/_/   \_\\
""")

# Esperar 3 segundos
time.sleep(3)

# Exibir o menu com cores
print(Fore.BLUE + Style.BRIGHT + "Menu do ghzinmaker:\n")
print(Fore.MAGENTA + "[1] Consulta CPF") #funfando
print(Fore.MAGENTA + "[2] Consulta CNPJ") #funfando
print(Fore.MAGENTA + "[3] Consulta Telefone")
print(Fore.MAGENTA + "[4] Bruteforce")
print(Fore.MAGENTA + "[5] Buscar sites") #funfando
print(Fore.MAGENTA + "[6] Buscar CEP")
print(Fore.MAGENTA + "[7] Buscar Placa") #funfando
print(Fore.MAGENTA + "[8] Consulta IP") #funfando
print(Fore.MAGENTA + "[0] Exit") #funfando

def testar_zip(arquivo, senha):
    """Testa a senha em um arquivo ZIP."""
    try:
        with zipfile.ZipFile(arquivo, 'r') as z:
            z.extractall(pwd=senha.encode())
        return True
    except (RuntimeError, zipfile.BadZipFile):
        return False

def testar_7z(arquivo, senha):
    """Testa a senha em um arquivo 7z."""
    try:
        with py7zr.SevenZipFile(arquivo, mode='r', password=senha) as z:
            z.extractall()
        return True
    except Exception:
        return False

def testar_pdf(arquivo, senha):
    """Testa a senha em um arquivo PDF."""
    try:
        with pikepdf.open(arquivo, password=senha) as pdf:
            return True
    except (pikepdf.PasswordError, FileNotFoundError):
        return False

def testar_tar(arquivo, senha):
    """Testa a senha em um arquivo TAR (assumindo que o conteúdo é ZIP, por exemplo)."""
    # Aqui você pode adicionar a lógica de descompressão usando uma senha, se houver.
    return False  # Substitua por sua lógica se necessário

def testar_txt_db(arquivo, senha):
    """Testa senhas em arquivos TXT ou DB."""
    # Normalmente, TXT e DB não têm proteção por senha, apenas um placeholder.
    return senha == "senha_esperada"  # Substitua pela lógica necessária.

def testar_senha(arquivo, senha):
    """Testa a senha no tipo de arquivo."""
    extensao = os.path.splitext(arquivo)[1].lower()
    if extensao == '.zip':
        return testar_zip(arquivo, senha)
    elif extensao == '.7z':
        return testar_7z(arquivo, senha)
    elif extensao == '.pdf':
        return testar_pdf(arquivo, senha)
    elif extensao == '.tar':
        return testar_tar(arquivo, senha)
    elif extensao in ['.txt', '.db']:
        return testar_txt_db(arquivo, senha)
    return False

def bruteforce_numbers(arquivo, tamanho=8):
    """Realiza ataque de força bruta para tentar senhas numéricas em arquivos."""
    for tentativa in tqdm(itertools.product(string.digits, repeat=tamanho), total=10**tamanho):
        senha = ''.join(tentativa)
        if testar_senha(arquivo, senha):
            print(f"\033[32m\nSenha encontrada: {senha}\033[0m")
            return senha
    print("\033[91m\nNão foi possível encontrar a senha.\033[0m")
    return None

def bruteforce_custom(arquivo, info):
    """Realiza ataque de força bruta para tentar senhas com base nas informações fornecidas pelo usuário."""
    combinacoes = []
    for key, value in info.items():
        if value.lower() != "n/a":
            combinacoes.append(value)

    for tentativa in tqdm(itertools.product(combinacoes, repeat=len(combinacoes))):
        senha = ''.join(tentativa)
        if testar_senha(arquivo, senha):
            print("\033[32m\nSenha encontrada: {senha}\033[0m")
            return senha
    print("\033[91m\nNão foi possível encontrar a senha.\033[0m")
    return None

def menu():
    print("\033[34mMenu Bruteforce\033[0m")
    print("\033[35m[11] Pasta\033[0m")
    print("\033[35m[22] Arquivo\033[0m")
    print("\033[35m[00] Sair\033[0m")

def iniciar_bruteforce_pasta():
    print("Coloque o arquivo .ZIP ou .7z dentro da pasta 'senhas/Pasta'")
    arquivo = input("Nome do arquivo (com extensão): ")
    arquivo = os.path.join('senhas', 'Pasta', arquivo)

    tipo_senha = input("A senha é composta de números ou letras? [números/letras]: ").strip().lower()

    if tipo_senha == 'números':
        tamanho_senha = int(input("Tamanho da senha (quantos dígitos): "))
        bruteforce_numbers(arquivo, tamanho=tamanho_senha)

    elif tipo_senha == 'letras':
        info = {
            'Nome': input("Nome: "),
            'Número': input("Número: "),
            'Animal': input("Animal: "),
            'Cidade': input("Cidade: "),
            'Mãe': input("Mãe: "),
            'Pai (N/A se não quiser informar)': input("Pai: "),
            'Música favorita': input("Música favorita: "),
            'Canal favorito': input("Canal favorito: ")
        }
        bruteforce_custom(arquivo, info)

    else:
        print("Tipo de senha inválido. Por favor, escolha 'números' ou 'letras'.")

def menu_bruteforce():
    while True:
        menu()  # Chama a função que exibe o menu
        escolha = input("\n[ghzin] $ Escolha uma opção: ")
        
        if escolha == '11':
            iniciar_bruteforce_pasta()
        elif escolha == '22':
            print("Função de bruteforce para arquivos ainda não implementada.")
        elif escolha == '00':
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")


# Função para fazer a requisição de consulta de cnpj
def req_consulta_cnpj(cnpj):
    try:
        url = f"https://brasilapi.com.br/api/cnpj/v1/{cnpj}"
        response = requests.get(url)

        if response.status_code == 200:
            dados = response.json()
            resposta = (
                Fore.GREEN + "Dados consultados:\n"
                f"CNPJ: {dados.get('cnpj', 'Não informado')}\n"
                f"Nome: {dados.get('nome', 'Não informado')}\n"
                f"Nome Fantasia: {dados.get('fantasia', 'Não informado')}\n"
                f"Tipo: {dados.get('tipo', 'Não informado')}\n"
                f"Atividade: {dados.get('atividade_principal', 'Não informado')}\n"
                f"Endereço: {dados.get('endereco', 'Não informado')}\n"
                f"Complemento: {dados.get('complemento', 'Não informado')}\n"
                f"Município: {dados.get('municipio', 'Não informado')}\n"
                f"UF: {dados.get('uf', 'Não informado')}\n"
                f"CEP: {dados.get('cep', 'Não informado')}\n"
            )
            return resposta
        else:
            return Fore.RED + f"Falha na consulta: Código de status {response.status_code}"
    except Exception as e:
        return Fore.RED + f"Ocorreu uma exceção: {e}"

# Função para filtrar CPF
def filtrar_cpf(cpf):
    return cpf.replace('.', '').replace('-', '')

# Função para fazer a requisição de consulta de CPF
def req_consulta_cpf(cpf):
    try:
        url = f"https://api.consultanacional.org:3000/consulta/{cpf}"
        response = requests.get(url)

        if response.status_code == 200:
            resp_json = response.json()
            if 'cpf' in resp_json:
                # Organizando a resposta
                dados = resp_json
                resposta = (
                    Fore.GREEN + "Dados consultados:\n"
                    f"CPF: {dados['cpf']}\n"
                    f"Nome: {dados['nome']}\n"
                    f"Sexo: {dados['sexo']}\n"
                    f"Nascimento: {dados['nascimento']}\n"
                    f"Mãe: {dados['mae']}\n"
                    f"Pai: {dados['pai']}\n"
                    f"Idade: {dados['idade']}\n"
                    f"Raça/Cor: {dados.get('raça/cor', 'Não informado')}\n"
                )
                return resposta
            else:
                return "Ocorreu um erro ao consultar os dados."
        else:
            return "Falha na consulta: Código de status " + str(response.status_code)
    except Exception as e:
        return f"Ocorreu uma exceção: {e}"

def carregar_progresso(progresso):
    # Função para mostrar o progresso no terminal
    print(Fore.YELLOW + f"Progresso: {progresso}%", end='\r')

def buscar_nos_arquivos(pasta_database, termo_busca):
    resultados = []
    arquivos = [f for f in os.listdir(pasta_database) if f.endswith('.txt')]
    total_arquivos = len(arquivos)

    if total_arquivos == 0:
        print(Fore.RED + "Nenhum arquivo .txt encontrado na pasta database.")
        return resultados

    for idx, arquivo in enumerate(arquivos):
        caminho_arquivo = os.path.join(pasta_database, arquivo)
        try:
            with open(caminho_arquivo, 'r', encoding='utf-8', errors='ignore') as f:
                linhas = f.readlines()
                for linha in linhas:
                    if termo_busca in linha:
                        resultados.append(linha.strip())
        except Exception as e:
            print(Fore.RED + f"Erro ao ler o arquivo {arquivo}: {e}")
        
        # Calcula e mostra o progresso da busca
        progresso = int(((idx + 1) / total_arquivos) * 100)
        carregar_progresso(progresso)
        time.sleep(0.1)  # Simula um pequeno atraso para a barra de progresso ser visível
    
    return resultados

def salvar_resultados(arquivo_resultado, resultados):
    # Função para salvar os resultados no arquivo results.txt
    with open(arquivo_resultado, 'w') as f:
        for resultado in resultados:
            f.write(resultado + '\n')

def executar_busca():
    # Função que será executada ao escolher o botão [5]
    pasta_database = "database"
    arquivo_resultado = "results.txt"
    
    comando = input(Fore.CYAN + "Digite o comando (/buscar + url): ")
    
    if comando.startswith("/buscar "):
        termo_busca = comando[len("/buscar "):].strip()

        print(Fore.GREEN + f"Iniciando busca por '{termo_busca}' nos arquivos da pasta '{pasta_database}'...")
        resultados = buscar_nos_arquivos(pasta_database, termo_busca)

        if resultados:
            salvar_resultados(arquivo_resultado, resultados)
            print(Fore.GREEN + f"\nBusca concluída! Resultados salvos em '{arquivo_resultado}'")
        else:
            print(Fore.RED + "\nNenhum resultado encontrado.")
    else:
        print(Fore.RED + "Comando inválido")

def req_consulta_ip(ip):
    try:
        url = "http://ip-api.com/batch?fields=61439"
        response = requests.post(url, json=[ip])

        if response.status_code == 200:
            resp_json = response.json()
            if resp_json and isinstance(resp_json, list):
                # Organiza a resposta
                dados = resp_json[0]
                resposta = (
                    Fore.GREEN + "Dados consultados:\n"
                    f"IP: {dados.get('query', 'Não informado')}\n"
                    f"Status: {dados.get('status', 'Não informado')}\n"
                    f"Região: {dados.get('regionName', 'Não informado')}\n"
                    f"Cidade: {dados.get('city', 'Não informado')}\n"
                    f"Zip: {dados.get('zip', 'Não informado')}\n"
                    f"Latitude: {dados.get('lat', 'Não informado')}\n"
                    f"Longitude: {dados.get('lon', 'Não informado')}\n"
                    f"ISP: {dados.get('isp', 'Não informado')}\n"
                    f"Organização: {dados.get('org', 'Não informado')}\n"
                    f"País: {dados.get('country', 'Não informado')}\n"
                )
                return resposta
            else:
                return "Ocorreu um erro na consulta."
        else:
            return f"Falha na consulta: Código de status {response.status_code}"
    except Exception as e:
        return f"Ocorreu uma exceção: {e}"

# Função para lidar com a escolha do usuário
while True:
    escolha = input("\n[ghzin] $ Escolha uma opção: ")

    if escolha == '1':
        cpf_input = input(Fore.CYAN + "Digite o CPF para consulta (/cpf + número do CPF): ")
        if cpf_input.startswith("/cpf "):
            cpf = filtrar_cpf(cpf_input[len("/cpf "):].strip())
            resultado = req_consulta_cpf(cpf)
            print(Fore.GREEN + resultado)
        else:
            print(Fore.RED + "Comando inválido.")
    
    elif escolha == '4':  # Nova opção para o menu de força bruta
        menu_bruteforce()  # Chama a função que exibe o menu de força bruta
    
    elif escolha == '22':
        print("Função de bruteforce para arquivos ainda não implementada.")
    
    elif escolha == '00':
        print("Saindo...")
        break

    elif escolha == '2':  # Corrigido para 'elif'
        cnpj_input = input(Fore.CYAN + "Digite o CNPJ para consulta (/cnpj + número do CNPJ): ")
        if cnpj_input.startswith("/cnpj "):
            cnpj = cnpj_input[len("/cnpj "):].strip()
            resultado = req_consulta_cnpj(cnpj)  # Certifique-se de que essa função está definida
            print(Fore.GREEN + resultado)
        else:
            print(Fore.RED + "Comando inválido.")

    elif escolha == '6':  # Esta parte deve estar alinhada corretamente
        cep_input = input(Fore.CYAN + "Digite o CEP para consulta (/cep + número do CEP): ")
        if cep_input.startswith("/cep "):
            cep = cep_input[len("/cep "):].strip()
            resultado = req_consulta_cep(cep)  # Certifique-se de que essa função está definida
            print(Fore.GREEN + resultado)
        else:
            print(Fore.RED + "Comando inválido.")

    elif escolha == '8':
        ip_input = input(Fore.CYAN + "Digite o IP para consulta (/ip + endereço IP): ")
        if ip_input.startswith("/ip "):
            ip = ip_input[len("/ip "):].strip()
            resultado = req_consulta_ip(ip)  # Certifique-se de que essa função está definida
            print(Fore.GREEN + resultado)
        else:
            print(Fore.RED + "Comando inválido.")

    elif escolha == '5':
        executar_busca()  # Chama a função de busca

    elif escolha == '0':
        print(Fore.RED + "\nEncerrando o menu...")
        time.sleep(1)
        os.system('clear' if os.name == 'posix' else 'cls')  # 'clear' para Linux/Mac, 'cls' para Windows
        sys.exit()  # Finaliza o script

    else:
        print(Fore.RED + "Opção inválida. Tente novamente.")