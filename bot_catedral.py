import pyautogui
import time
import random

# ==========================================
# CONFIGURAÇÕES DE SEGURANÇA
# ==========================================
# Se o bot enlouquecer, puxe o seu mouse físico rapidamente para 
# qualquer um dos 4 cantos extremos do monitor. Isso aborta o script na hora!
pyautogui.FAILSAFE = True 

def clicar(imagem, confianca=0.8, nome="", espera=1):
    """Procura uma única imagem na tela e clica nela."""
    try:
        posicao = pyautogui.locateOnScreen(f'imagens/{imagem}', confidence=confianca)
        if posicao:
            x, y = pyautogui.center(posicao)
            # Toque humano: clica com uma leve variação nos pixels
            pyautogui.moveTo(x + random.randint(-5, 5), y + random.randint(-5, 5), duration=0.3)
            pyautogui.click()
            print(f"✅ {nome}")
            time.sleep(espera)
            return True
        return False
    except Exception:
        return False

def clicar_lista(imagem, confianca=0.8, nome="", espera=2):
    """Procura TODAS as opções no mapa e clica na primeira que achar."""
    try:
        itens = list(pyautogui.locateAllOnScreen(f'imagens/{imagem}', confidence=confianca))
        if itens:
            alvo = itens[0]
            x, y = pyautogui.center(alvo)
            pyautogui.moveTo(x + random.randint(-5, 5), y + random.randint(-5, 5), duration=0.4)
            pyautogui.click()
            print(f"🗺️ {nome}")
            time.sleep(espera)
            return True
        return False
    except Exception:
        return False

def escolher_bencao_inteligente():
    """Identifica as cartas pela chama azul e clica em uma delas dinamicamente."""
    try:
        # 1. Verifica se a tela é de fato a de bênção (pelo botão finalizar)
        if pyautogui.locateOnScreen('imagens/confirmar_btn.png', confidence=0.8):
            print("✨ Tela de Bênção detectada! Lendo as cartas disponíveis...")
            time.sleep(1) # Espera a animação das cartas terminar
            
            # 2. Tenta achar as chamas azuis blindando contra o erro do PyAutoGUI
            try:
                chamas = pyautogui.locateAllOnScreen('imagens/bencao_topo_chama.png', confidence=0.75)
                cartas = list(chamas)
            except pyautogui.ImageNotFoundException:
                cartas = [] # Se não achar a chama, a lista fica vazia para não dar erro
            
            if cartas:
                # 3. Escolhe uma carta aleatória entre as que encontrou
                alvo = random.choice(cartas)
                carta_x, carta_y = pyautogui.center(alvo)
                
                # Move o mouse para a carta e clica (desce 20 pixels para clicar no meio)
                pyautogui.moveTo(carta_x, carta_y + 20, duration=0.4)
                pyautogui.click()
                print("🎯 Carta selecionada!")
                time.sleep(1)
                
                # 4. Procura o botão de confirmar e clica nele
                if clicar('confirmar_btn.png', 0.8, "Bênção confirmada com sucesso!", 2):
                    return True
            else:
                print("⚠️ A tela abriu, mas o bot não achou o recorte 'bencao_topo_chama.png'.")
                
        return False
        
    except pyautogui.ImageNotFoundException:
        # É normal ele não achar o botão finalizar enquanto o jogo rola, apenas ignora
        return False
    except Exception as e:
        print(f"❌ Erro inesperado na bênção: {e}")
        return False

def iniciar_automacao():
    print("🤖=== BOT DO HUSTLE CASTLE INICIADO ===🤖")
    print("Mude para a janela do jogo agora! O bot assume o controle em 5 segundos...")
    time.sleep(5)
    print("Iniciando varredura da tela...\n")
    
    while True:
        # ==========================================
        # PRIORIDADE 1: EMERGÊNCIAS, EVENTOS E POP-UPS
        # ==========================================
        if clicar('participar_btn.png', 0.8, "Iniciando Jornada..."): 
            clicar('posicionar_inicio_btn.png', 0.8, "Posicionando os melhores guerreiros!", 1.5)
            clicar('confirmar_inicio_btn.png', 0.8, "Confirmando Jornada", 2)
            clicar('atacar_inicio_btn.png', 0.8, "Começando Ataque...", 5)
            continue            
        elif clicar('fechar_btn.png', 0.8, "Fechando Janela"): continue
        elif clicar('sim_btn.png', 0.8, "Confirmando (Sim)"): continue
        
        # COMBO 1: Tenta o Arriscar primeiro!
        elif clicar('arriscar_btn.png', 0.8, "Selecionou Arriscar evento!", 1.5): 
            # Mini-loop teimoso: Tenta confirmar até 4 vezes antes de desistir
            for _ in range(4):
                if clicar('finalizar_btn.png', 0.8, "Confirmando o Risco! Boa sorte...", 2):
                    break # Se conseguiu clicar, sai do mini-loop
                time.sleep(1) # Espera 1 segundo e tenta achar o botão de novo
            continue
            
        # COMBO 2: Se não tiver o arriscar, tenta a Recompensa
        elif clicar('recompensa_btn.png', 0.8, "Selecionou a Recompensa!", 1.5): 
            for _ in range(4):
                if clicar('finalizar_btn.png', 0.8, "Confirmando a Recompensa...", 2):
                    clicar('finalizar_aviso_btn.png', 0.8, "Recompensa Confirmada!", 2)
                    break
                time.sleep(1)
            continue
            
        # COMBO 3: Se não tiver nenhum dos dois, apenas Prossegue
        elif clicar('prosseguir_btn.png', 0.8, "Selecionou Prosseguir na história...", 1.5): 
            for _ in range(4):
                if clicar('finalizar_btn.png', 0.8, "Confirmando o Prosseguir...", 2):
                    break
                time.sleep(1)
            continue
        
        # ==========================================
        # PRIORIDADE 2: TRANSIÇÕES E COMBATE
        # ==========================================
        
        # COMBO: Tenta posicionar as tropas PRIMEIRO
        elif clicar('posicionar_btn.png', 0.8, "Posicionando os melhores guerreiros!", 1.5):
            clicar('fast_atack_btn.png', 0.8, "Iniciando Ataque Rápido (Combo)!", 5)
            print("⚔️ Batalha rápida em andamento. Aguardando...")
            continue
            
        # SEGURANÇA: Se o botão 'posicionar' não existir, tenta atacar normal.
        elif clicar('fast_atack_btn.png', 0.8, "Botão Ataque Rápido pressionado!", 5): 
            print("⚔️ Batalha rápida em andamento. Aguardando...")
            continue
            
        # Lógica inteligente das cartas de bênção
        elif escolher_bencao_inteligente(): 
            continue 
            
        elif clicar('colocar_pelotao_btn.png', 0.8, "Saindo/Voltando ao Início"): continue
        elif clicar('inicio_btn.png', 0.8, "Saindo/Voltando ao Início"): continue

        
        # ==========================================
        # PRIORIDADE 3: NAVEGAÇÃO NO MAPA
        # ==========================================
        # O bot sempre vai tentar ir nos mais difíceis primeiro se tiver caminho livre
        elif clicar_lista('guardiao_node.png', 0.8, "Caminhando: CHEFE (Guardião)"): continue
        elif clicar_lista('lacaio_node.png', 0.7, "Caminhando: Elite (Lacaio)"): continue
        elif clicar_lista('tormento_node.png', 0.8, "Caminhando: Elite (Tormento)"): continue
        
        # Caminhos normais
        elif clicar_lista('catedral_node_batalha.png', 0.8, "Caminhando: Batalha Normal"): continue
        
        # Utilitários
        elif clicar_lista('campo_node.png', 0.8, "Caminhando: Acampamento", 1.5): continue
        elif clicar_lista('altar_node.png', 0.8, "Caminhando: Altar da Ressurreição"): continue
        elif clicar_lista('aleatoria_node.png', 0.8, "Caminhando: Sala Aleatória"): continue

        # Se não achou absolutamente nada na tela, apenas dorme 1 seg e recomeça a checar
        elif clicar('proximo_andar_btn.png', 0.8, "Avançando para o Próximo Andar", 4): continue
        elif clicar('terminar_jornada_btn.png', 0.8, "Terminando Jornada...", 4): continue
        elif clicar('inicio_jornada_btn.png', 0.8, "Terminando Jornada...", 4): continue
        time.sleep(1)

# ==========================================
# RODA O PROGRAMA
# ==========================================
iniciar_automacao()