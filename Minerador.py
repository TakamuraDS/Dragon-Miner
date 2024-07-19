
# ---------------------------------------------------------------
# Minerador de Bitcoin Dragon Miner - version 1.0
# ---------------------------------------------------------------



from signal import signal, SIGINT
import context as ctx
import threading, requests, binascii, hashlib, logging, random, socket, time, json, sys , traceback , os
from colorama import init, Fore, Back, Style
import click, re 

# Define o minerador de Bitcoin com uma mensagem de abertura e cores personalizadas
miner = '''
    ██████╗ ██████╗  █████╗  ██████╗  ██████╗ ███╗   ██╗
    ██╔══██╗██╔══██╗██╔══██╗██╔════╝ ██╔═══██╗████╗  ██║
    ██║  ██║██████╔╝███████║██║  ███╗██║   ██║██╔██╗ ██║
    ██║  ██║██╔══██╗██╔══██║██║   ██║██║   ██║██║╚██╗██║
    ██████╔╝██║  ██║██║  ██║╚██████╔╝╚██████╔╝██║ ╚████║
    ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝
                                                        
    ███╗   ███╗██╗███╗   ██╗███████╗██████╗             
    ████╗ ████║██║████╗  ██║██╔════╝██╔══██╗            
    ██╔████╔██║██║██╔██╗ ██║█████╗  ██████╔╝            
    ██║╚██╔╝██║██║██║╚██╗██║██╔══╝  ██╔══██╗            
    ██║ ╚═╝ ██║██║██║ ╚████║███████╗██║  ██║            
    ╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝  
A mineração de bitcoin requer paciência, persistência e um bom conhecimento técnico, mas pode ser uma atividade lucrativa e emocionante.                        
'''
# Versão do minerador
miner2 = '''
    ඞ 𝚂𝚎𝚓𝚊 𝙱𝚎𝚖 𝚟𝚒𝚗𝚍𝚘 - 1.3v ඞ
'''
miner3 = '''
    ╔═══════════════════════════════════════════════════════╗
    ║✦-𝙵𝚒𝚚𝚞𝚎 𝚍𝚎 𝙾𝚕𝚑𝚘 𝚗𝚘 𝙶𝚒𝚝𝚑𝚞𝚋 𝚗𝚊𝚘 𝚙𝚎𝚛𝚍𝚎𝚛 𝚊𝚜 𝙽𝚘𝚟𝚒𝚍𝚊𝚍𝚎𝚜    
    ║✦-𝚂𝚎𝚖𝚙𝚛𝚎 𝚊𝚝𝚞𝚊𝚕𝚒𝚣𝚊𝚗𝚍𝚘 𝚘 𝚌𝚘𝚍𝚒𝚐𝚘 𝚙𝚊𝚛𝚊 𝚖𝚊𝚒𝚜 𝚎𝚏𝚒𝚎𝚗𝚌𝚒𝚊 !.
    ║✦-𝚄𝚕𝚝𝚒𝚕𝚒𝚣𝚎 𝚌𝚘𝚖 𝚛𝚎𝚜𝚙𝚘𝚗𝚜𝚊𝚋𝚒𝚕𝚒𝚍𝚊𝚍𝚎 𝚎 𝚋𝚘𝚊 𝚖𝚒𝚗𝚎𝚛𝚊𝚍𝚊
    ╚═══════════════════════════════════════════════════════╝
'''
miner4 = '''
======================================
'''

# Define o minerador de Bitcoin com uma mensagem de abertura e cores personalizadas
print(Fore.RED, miner, Style.RESET_ALL)
print(Fore.BLUE, miner2, Style.RESET_ALL)
print(Fore.WHITE, miner3, Style.RESET_ALL)





# ---------------------------------------------------------------
# Variáveis globais
# ---------------------------------------------------------------

# informação da carteira Bitcoin do usuário

def obter_saldo(carteira):
    url = f'https://blockchain.info/balance?active={carteira}'
    response = requests.get(url)
    if response.status_code == 200:
        dados = response.json()
        if 'n_received' in dados:
            return dados['n_received'] / 100000000
    else:
        print("Não foi possível obter o saldo da carteira, tente novamente.")
        return None

Carteira_registrada = '1EdjZbdZPFR4ot1ZhydLGyC4S54kTqugpD'

def validar_carteira(carteira):
    pattern = re.compile(r'^[13][a-zA-HJ-NP-Z1-9]{25,34}$')
    return bool(pattern.match(carteira))

def solicitar_carteira():
    while True:
        resposta = input(click.style("Deseja usar a carteira registrada Digite [1] ou inserir outra carteira [2]? ", bold=True))
        if resposta == '1':
            return Carteira_registrada
        elif resposta == '2':
            carteira_usuario = input("Por favor, insira sua carteira bitcoin !: ")
            if validar_carteira(carteira_usuario):
                logging.info(f'Carteira inserida: {carteira_usuario}')
                return carteira_usuario
            else:
                print("Carteira inválida, tente novamente.")
        else:
            print("Opção inválida, tente novamente.")

Carteira = solicitar_carteira()

# ---------------------------------------------------------------
# Funções auxiliares
# ---------------------------------------------------------------

def handler(signal_received, frame):
    # Handle any cleanup here
    ctx.fShutdown = True
    print('Desligando Minerador ...')


# O objetivo final dessa função é ajudar a gerenciar logs em um arquivo (.log)
def logg(msg):
    # basic logging 
    logging.basicConfig(level=logging.INFO, filename="miner.log", format='%(asctime)s %(message)s') # include timestamp
    logging.info(msg)

def get_current_block_height():
    # retorna a altura atual da rede
    r = requests.get('https://blockchain.info/latestblock')
    return int(r.json()['height'])


# ---------------------------------------------------------------
# Calcular Taxa de Hash
# ---------------------------------------------------------------


def calculate_hashrate(nNonce, last_updated):
    global velocidadeHash
    if nNonce % 1000000 == 999999:
        now  = time.time()
        hashrate  = round(1000000 / (now - last_updated))
        velocidadeHash = str(hashrate) + " hash/s"
        print(Fore.RED + "       Velocidade do Hash: " + velocidadeHash)
        sys.stdout.flush()
        return now   
    else:
        return last_updated
    
    
# ---------------------------------------------------------------
# Calcular Taxa de Hash
# ---------------------------------------------------------------

# Função para verificar se a thread deve ser encerrada
def check_for_shutdown(t):
    # handle shutdown 
    n = t.n
    if ctx.fShutdown:
        if n != -1:
            ctx.listfThreadRunning[n] = False
            t.exit = True
            
# Classe de thread personalizada
class ExitedThread(threading.Thread):
    def __init__(self, arg, n):
        super(ExitedThread, self).__init__()
        self.exit = False
        self.arg = arg
        self.n = n

    def run(self):
        self.thread_handler(self.arg, self.n)
        pass

    def thread_handler(self, arg, n):
        while True:
            check_for_shutdown(self) # Verificar se a thread deve ser encerrada
            if self.exit:
                break
            ctx.listfThreadRunning[n] = True
            try:
                self.thread_handler2(arg)
            except Exception as e:
                logg("ThreadHandler()")
                logg(e)
            ctx.listfThreadRunning[n] = False

            time.sleep(5)
            pass

    def thread_handler2(self, arg):
        raise NotImplementedError("NO")

    def check_self_shutdown(self):
        check_for_shutdown(self)

    def try_exit(self):
        self.exit = True
        ctx.listfThreadRunning[self.n] = False
        pass
    
# ---------------------------------------------------------------
# Função para minerar Bitcoin
# ---------------------------------------------------------------
def bitcoin_miner(t, restarted=False):

    if restarted:
        logg('[*] Minerador Resetou')
        time.sleep(10)

# ---------------------------------------------------------------
# Calcula o alvo para o hash do bloco
# ---------------------------------------------------------------

    target = (ctx.nbits[2:]+'00'*(int(ctx.nbits[:2],16) - 3)).zfill(64)
    
    ctx.extranonce2 = hex(random.randint(0,2**32-1))[2:].zfill(2*ctx.extranonce2_size)      # <--- Gera um novo extranonce2 randomico

    coinbase = ctx.coinb1 + ctx.extranonce1 + ctx.extranonce2 + ctx.coinb2   # <----- Calcula o hash da transação coinbase
    coinbase_hash_bin = hashlib.sha256(hashlib.sha256(binascii.unhexlify(coinbase)).digest()).digest()

    merkle_root = coinbase_hash_bin
    for h in ctx.merkle_branch:
        merkle_root = hashlib.sha256(hashlib.sha256(merkle_root + binascii.unhexlify(h)).digest()).digest()

    # Calcula a raiz da árvore de Merkle para o bloco
    merkle_root = binascii.hexlify(merkle_root).decode()

    #little endian
    merkle_root = ''.join([merkle_root[i]+merkle_root[i+1] for i in range(0,len(merkle_root),2)][::-1])

    work_on = get_current_block_height() # Atualiza a altura do bloco que o minerador está tentando resolver

    ctx.nHeightDiff[work_on+1] = 0 

# ---------------------------------------------------------------
# Explicação desta Parte
# ---------------------------------------------------------------


    _diff = int("00000000FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF", 16)
 
# ---------------------------------------------------------------
# Esta linha define a variável _diff com o valor hexadecimal 00000000FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF, que representa o máximo possível para um hash de Bitcoin SHA-256 (2^256 − 1). 
# O valor é convertido de hexadecimal para decimal usando a função int(). A notação 16 como argumento indica que o valor é em base 16 (hexadecimal).
# Este valor é usado como referência para calcular a dificuldade de mineração de um bloco de Bitcoin. 
# Quando um hash é gerado, o algoritmo compara-o com este valor de referência e ajusta a dificuldade da mineração com base no número de zeros iniciais no hash.
# O objetivo é manter um tempo médio de geração de blocos de aproximadamente 10 minutos.
# Em resumo, _diff = int("00000000FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF", 16) define o valor máximo possível para um hash SHA-256 de Bitcoin e é usado como referência para calcular a dificuldade de mineração.
# --------------------------------------------------------------- 
    
    
# ---------------------------------------------------------------
# Explicação desta Parte
# ---------------------------------------------------------------    
    

    logg('[*] Trabalhando para resolver bloco com altura {}'.format(work_on+1)) # Exibe uma mensagem indicando que o minerador está trabalhando em um novo bloco

    if len(sys.argv) > 1:
        random_nonce = False 
    else:
        random_nonce = True

    nNonce = 0 

    last_updated = int(time.time())
# Loop principal de mineração
    while True:
        t.check_self_shutdown()
        if t.exit:
            break
# Verifica se um novo bloco foi detectado na rede
        if ctx.prevhash != ctx.updatedPrevHash:
            logg('[*] Novo bloco {} detectado na rede '.format(ctx.prevhash))
            logg('[*] A melhor dificuldade para tentar resolver o bloco {} foi {}'.format(work_on+1, ctx.nHeightDiff[work_on+1]))
            ctx.updatedPrevHash = ctx.prevhash
            bitcoin_miner(t, restarted=True)
            break 
        # Gera um nonce randomico
        if random_nonce:
            nonce = hex(random.randint(0,2**32-1))[2:].zfill(8) # nNonce   #hex(int(nonce,16)+1)[2:]
        else:
            nonce = hex(nNonce)[2:].zfill(8) # <----- Gera um nonce sequencial
        # Monta o cabeçalho do bloco
        blockheader = ctx.version + ctx.prevhash + merkle_root + ctx.ntime + ctx.nbits + nonce +\
        '000000800000000000000000000000000000000000000000000000000000000000000000000000000000000080020000'
        hash = hashlib.sha256(hashlib.sha256(binascii.unhexlify(blockheader)).digest()).digest()
        hash = binascii.hexlify(hash).decode()
        
# ---------------------------------------------------------------        
        # Exibe um log indicando que um novo hash foi encontrado
        if hash.startswith('0000000'): logg('[*] Novo hash: {} para bloco {}'.format(hash, work_on+1))
# ---------------------------------------------------------------
# Calcula a dificuldade do hash atual  
        this_hash = int(hash, 16)

        difficulty = _diff / this_hash
# Atualiza a dificuldade do bloco se necessário
        if ctx.nHeightDiff[work_on+1] < difficulty:
            # new best difficulty for block at x height
            ctx.nHeightDiff[work_on+1] = difficulty
# Atualiza a velocidade de hash do minerador
        if not random_nonce:
            last_updated = calculate_hashrate(nNonce, last_updated)
# Verifica se o hash atende aos requisitos de dificuldade
        if hash < target :
            # Exibe logs indicando que o bloco foi resolvido
            logg('[*] Bloco {} resolvido.'.format(work_on+1))
            logg('[*] Bloco hash: {}'.format(hash))
            logg('[*] Cabeça Do Bloco: {}'.format(blockheader))
            # Prepara e envia o bloco resolvido para a piscina            
            payload = bytes('{"params": ["'+Carteira+'", "'+ctx.job_id+'", "'+ctx.extranonce2 \
                +'", "'+ctx.ntime+'", "'+nonce+'"], "id": 1, "method": "mining.submit"}\n', 'utf-8')
            logg('[*] Pagamento: {}'.format(payload))
            ctx.sock.sendall(payload)
            ret = ctx.sock.recv(1024)
            logg('[*] Resposta do conjunto: {}'.format(ret))
            return True
        # Incrementa o nonce e itera no loop principal de mineração
        nNonce +=1

def block_listener(t):
    # Esta seção é responsável pela conexão com um pool e quase todas as comunicações
    # com a rede Bitcoin
    
    # Inicializa a conexão com o pool de mineração
    sock  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('equihash144.mine.zergpool.com', 3333))
    # Recebe a resposta do pool e extrai as informações relevantes para o minerador
    sock.sendall(b'{"id": 1, "method": "mining.subscribe", "params": []}\n')
    # Recebe a resposta do pool e extrai as informações relevantes para o minerador
    lines = sock.recv(1024).decode().split('\n')
    response = json.loads(lines[0])
    ctx.sub_details,ctx.extranonce1,ctx.extranonce2_size = response['result']
    # Autentica o minerador com o pool usando o endereço Bitcoin e uma senha (não mostrada aqui)
    sock.sendall(b'{"params": ["'+Carteira.encode()+b'", "password"], "id": 2, "method": "mining.authorize"}\n')
    # Monitora as mensagens do pool e processa as informações de bloco
    response = b''
    while response.count(b'\n') < 4 and not(b'mining.notify' in response):response += sock.recv(1024)

    responses = [json.loads(res) for res in response.decode().split('\n') if len(res.strip())>0 and 'mining.notify' in res]
    #Atualiza as informações do bloco atual no contexto do minerador
    ctx.job_id, ctx.prevhash, ctx.coinb1, ctx.coinb2, ctx.merkle_branch, ctx.version, ctx.nbits, ctx.ntime, ctx.clean_jobs = responses[0]['params']
    # faça isso uma vez, será sobrescrito pelo loop de mineração quando um novo bloco for detectado
    ctx.updatedPrevHash = ctx.prevhash
    # setar sock 
    ctx.sock = sock 

    while True:
        t.check_self_shutdown()
        if t.exit:
            break

        # verifica se há novo bloco
        response = b''
        while response.count(b'\n') < 4 and not(b'mining.notify' in response):response += sock.recv(1024)
        responses = [json.loads(res) for res in response.decode().split('\n') if len(res.strip())>0 and 'mining.notify' in res]     
        

        if responses[0]['params'][1] != ctx.prevhash:
            # novo bloco detectado na rede 
            # atualiza dados de trabalho de contexto 
            ctx.job_id, ctx.prevhash, ctx.coinb1, ctx.coinb2, ctx.merkle_branch, ctx.version, ctx.nbits, ctx.ntime, ctx.clean_jobs = responses[0]['params']
            


class CoinMinerThread(ExitedThread):
    def __init__(self, arg=None):
        # Inicializa a classe pai ExitedThread com os parâmetros necessários
        super(CoinMinerThread, self).__init__(arg, n=0)

    def thread_handler2(self, arg):
        # Executa a mineração de bitcoin
        self.thread_bitcoin_miner(arg)

    def thread_bitcoin_miner(self, arg):
        # Define o status da thread como "rodando"
        ctx.listfThreadRunning[self.n] = True
        # Verifica se a thread deve ser encerrada
        check_for_shutdown(self)
        try:
            # Inicia a mineração de bitcoin
            ret = bitcoin_miner(self)
            # Registra o retorno da função bitcoin_miner() no log
            logg("[*] Minerador voltou %s\n\n" % "true" if ret else"false")
        except Exception as e:
            # Registra a ocorrência de uma exceção na função bitcoin_miner() no log
            logg("[*] Minerador()")
            logg(e)
            traceback.print_exc()
            # Define o status da thread como "parada"
        ctx.listfThreadRunning[self.n] = False

    pass  




class NewSubscribeThread(ExitedThread):
    def __init__(self, arg=None):
        # Inicializa a classe pai ExitedThread com os parâmetros necessários
        super(NewSubscribeThread, self).__init__(arg, n=1)

    def thread_handler2(self, arg):
        # Executa a função thread_new_block()
        self.thread_new_block(arg)

    def thread_new_block(self, arg):
        ctx.listfThreadRunning[self.n] = True
        check_for_shutdown(self)
        try:
            block_listener(self)
        except Exception as e:
            logg("[*] Inscrever-se no tópico()")
            logg(e)
            traceback.print_exc()
        ctx.listfThreadRunning[self.n] = False

    pass  


# ---------------------------------------------------------------
# Parte do Codigo para fica Bonito.
# ---------------------------------------------------------------

def get_crypto_prices():
    url = "https://api.coinpaprika.com/v1/tickers"
    response = requests.get(url)
    data = response.json()

    btc_price = next((x['quotes']['USD']['price'] for x in data if x['symbol'] == 'BTC'), None)
    eth_price = next((x['quotes']['USD']['price'] for x in data if x['symbol'] == 'ETH'), None)
    doge_price = next((x['quotes']['USD']['price'] for x in data if x['symbol'] == 'DOGE'), None)

    return btc_price, eth_price, doge_price


print(Fore.BLUE, miner4, Style.RESET_ALL)

btc_price, eth_price, doge_price = get_crypto_prices()

print(Fore.WHITE, f"Preços atualizados em tempo real:\n", Style.RESET_ALL)
print(Fore.RED, f"Bitcoin: ${btc_price:.2f}\n", Style.RESET_ALL)
print(Fore.GREEN, f"Ethereum: ${eth_price:.2f}\n", Style.RESET_ALL)
print(Fore.YELLOW, f"Dogecoin: ${doge_price:.2f}\n\n", Style.RESET_ALL)

print(Fore.WHITE, miner4, Style.RESET_ALL)



MOEDAS_ALTERNATIVAS = [
    {
        'symbol': '€',
        'name': 'Euro',
        'rate_id': 'latest/EUR'
    },
    {
        'symbol': '£',
        'name': 'Libra Esterlina',
        'rate_id': 'latest/GBP'
    }
]

def get_latest_currency_rate(base_currency='USD'):
    """Retorna o dólar ($) atual convertido nas moedas necessárias"""

    url = f'https://api.exchangerate-api.com/v4/latest/{base_currency}'
    response = requests.get(url)
    return response.json()

def display_alternative_crypto_prices(btc_price, eth_price, doge_price):
    currency_rates = get_latest_currency_rate()

    euro_rate = currency_rates["rates"].get('€', 0)
    gbp_rate = currency_rates["rates"].get('£', 0)

    print(Fore.WHITE, '\nPreços atualizados em tempo real:\n', Style.RESET_ALL)
    print(Fore.CYAN, 'Bitcoin:')
    print(Fore.RED, f'${btc_price:.2f} ${euro_rate:.2f}€ ${gbp_rate:.2f}£')
    print(Fore.CYAN, 'Ethereum:')
    print(Fore.GREEN, f"${eth_price:.2f} ${euro_rate:.2f}€ ${gbp_rate:.2f}£")
    print(Fore.CYAN, 'Dogecoin:')
    print(Fore.YELLOW, f'${doge_price:.2f} ${euro_rate:.2f}€ ${gbp_rate:.2f}£')
    
def get_crypto_prices2():
    url = 'https://api.coinpaprika.com/v1/tickers'
    response = requests.get(url)
    data = response.json()

    crypto_prices = {
        'btc': data[0]['quotes']['USD']['price'],
        'eth': data[1]['quotes']['USD']['price'],
        'doge': data[2]['quotes']['USD']['price'],
    }

    return crypto_prices

# ---------------------------------------------------------------
# Parte do Codigo para fica Bonito.
# ---------------------------------------------------------------

def StartMining():
    # Inicializa a thread de inscrição no tópico
    subscribe_t = NewSubscribeThread(None)
    subscribe_t.start()
    logg("[*] O tópico de inscrição foi iniciado.")
    
# Aguarda 4 segundos para garantir que a inscrição seja concluída
    time.sleep(4)
# Inicializa a thread de mineração de bitcoin
    miner_t = CoinMinerThread(None)
    miner_t.start()
    logg("[*] Tópico de minerador de Bitcoin iniciado")
      
    print('O minerador de Bitcoin começou')





def mine(block_header, difficulty):
    nonce = 0
    start_time = time.time()

    while True:
        # Calcular o hash do bloco
        hash_result = calculate_hash(block_header, nonce, difficulty)

        # Verificar se o hash é menor ou igual ao alvo
        if int(hash_result, 16) <= difficulty:
            # Parar o cronômetro
            end_time = time.time()
            elapsed_time = end_time - start_time
            # Calcular a velocidade de hash
            hashes_per_second = (nonce / elapsed_time)
            # Exibir os resultados
            print(f'Encontrado hash válido com nonce {nonce} em {elapsed_time} segundos. Velocidade: {hashes_per_second:.2f} H/s')
            # Retornar o hash válido
            return hash_result

        # Incrementar o nonce
        nonce += 1

def calculate_hash(block_header, nonce, difficulty):
    # Criar uma string que representa o bloco
    block_string = block_header + str(nonce).zfill(8)

    # Calcular o hash SHA-256 do bloco
    raw_hash = hashlib.sha256(block_string.encode()).hexdigest()

    # Ajustar o hash para atender à dificuldade
    adjusted_hash = '0' * difficulty

    while len(raw_hash) < difficulty:
        adjusted_hash += '0'
        raw_hash = hashlib.sha256(adjusted_hash.encode() + block_string.encode()).hexdigest()

    return raw_hash

# ---------------------------------------------------------------
# Chamada principal do script
# ---------------------------------------------------------------

if __name__ == '__main__':
    # Registra a função 'handler' como manipuladora do sinal 'SIGINT'
    signal(SIGINT, handler)
 
# Definição da variável fShutdown como False
ctx.fShutdown = False

# Inicia o processo de mineração
StartMining()