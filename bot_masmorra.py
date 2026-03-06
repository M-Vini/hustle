import pyautogui
import time
import random

pyautogui.FAILSAFE = True

# ==========================================
# FUNÇÕES DE AMORTECIMENTO
# ==========================================
def localizar_seguro(imagem, confianca=0.75):
    try:
        return pyautogui.locateOnScreen(f'imagens_masmorra/{imagem}', confidence=confianca)
    except Exception:
        return None

def localizar_todos_seguro(imagem, confianca=0.75):
    try:
        return list(pyautogui.locateAllOnScreen(f'imagens_masmorra/{imagem}', confidence=confianca))
    except Exception:
        return []

def clicar(imagem, confianca=0.75, nome="", espera=1, mover_duration=0.3):
    posicao = localizar_seguro(imagem, confianca)
    if posicao:
        x, y = pyautogui.center(posicao)
        pyautogui.moveTo(x + random.randint(-5, 5), y + random.randint(-5, 5), duration=mover_duration)
        pyautogui.click()
        print(f"✅ {nome}")
        time.sleep(espera)
        return True
    return False

# ==========================================
# AÇÃO: ARRASTAR TROPAS (DRAG & DROP)
# ==========================================
def arrastar_tropas():
    """Procura espaços vazios e arrasta os bonecos vivos para eles."""
    slots_vazios = localizar_todos_seguro('slot_vazio.png', 0.8)
    
    if not slots_vazios:
        return False # Não estamos na tela de posicionar tropas

    tropas = localizar_todos_seguro('base_tropa.png', 0.8)
    
    if not tropas:
        print("⚠️ Sem tropas vivas disponíveis para arrastar!")
        return False

    print(f"🧩 Posicionando {min(len(slots_vazios), len(tropas))} tropa(s)...")

    # Faz o Drag & Drop (Arrasta do boneco para o buraco)
    for i in range(min(len(slots_vazios), len(tropas))):
        tropa_x, tropa_y = pyautogui.center(tropas[i])
        slot_x, slot_y = pyautogui.center(slots_vazios[i])

        pyautogui.moveTo(tropa_x, tropa_y, duration=0.2)
        # Clica, segura e puxa até o slot
        pyautogui.dragTo(slot_x, slot_y, duration=0.5, button='left')
        time.sleep(0.3)

    # Após arrastar, usa a sua estratégia genial de Ataque Rápido
    if clicar('ataque_rapido_btn.png', 0.8, "Ataque Rápido acionado!"):
        return True
    # Se for um Altar/Sacrifício ou chefe que não tem ataque rápido, clica no finalizar
    elif clicar('finalizar_selecao_btn.png', 0.8, "Seleção finalizada!"):
        return True

    return True

# ==========================================
# LÓGICA DE EXPLORAÇÃO DO MAPA
# ==========================================
def explorar_masmorra():
    """Varredura inteligente do mapa e ações de combate."""
    
    # 1. Tenta arrastar tropas se a tela de esquadrão estiver aberta
    if arrastar_tropas():
        return True

    # 2. Fecha pop-ups chatos ou recusa ressurreições com diamantes
    clicar('fechar_x.png', 0.8, "Fechando janela/pop-up", 0.5)

    # 3. Confirmação de movimentação (O jogo pede para confirmar o passo)
    if clicar('mover_para_ca.png', 0.8, "Andando pelo mapa..."):
        return True

    # 4. Escaneia o mapa procurando ícones de Combate ou Sacrifício
    if clicar('no_combate.png', 0.8, "Entrando em Combate (Machados)"):
        return True
    if clicar('no_sacrificio.png', 0.8, "Entrando no Altar de Sacrifício"):
        return True

    # 5. Recolhe recompensas do chão ou baús
    clicar('recolher_premio.png', 0.8, "Pegando baú no caminho", 0.5)

    return False

# ==========================================
# LOOP PRINCIPAL DO BOT
# ==========================================
def bot_masmorra():
    print("🏰=== BOT DA MASMORRA 2.0 INICIADO ===🏰")
    print("Mude para a janela do jogo! O bot assume em 5 segundos...")
    time.sleep(5)

    estado_atual = "SAGUAO" 

    while True:
        
        if estado_atual == "SAGUAO":
            if clicar('icone_masmorra_mapa.png', 0.8, "Abrindo Saguão"): pass
            elif clicar('participar_btn.png', 0.8, "Participando da Masmorra!"):
                clicar('posicionar_inicio_btn.png',0.8,"Posicionando tropas...")
                clicar('confirmar_inicio_btn.png',0.8,"Confirmando tropas...")
                estado_atual = "BUSCANDO_PARCEIRO"
        
        elif estado_atual == "BUSCANDO_PARCEIRO":
            if clicar('aleatorio_inicio_btn.png', 0.8, "Parceiro Encontrado!"):
                print("⚔️ Entrando no mapa... Preparando radar!")
                time.sleep(6) # Carregamento
                estado_atual = "EXPLORANDO_MAPA"
            # elif localizar_seguro('parceiro_aleatorio_btn.png', 0.8):
            #     estado_atual = "SAGUAO" # Fila caiu

        elif estado_atual == "EXPLORANDO_MAPA":
            # Chama a função que faz tudo lá dentro
            explorar_masmorra()
            
            # Condição de Saída (Fim da Masmorra ou Morte)
            if clicar('terminar_jornada_btn.png', 0.8, "Masmorra concluída/Derrota. Saindo..."):
                time.sleep(1)
                clicar('sim_btn.png', 0.8, "Confirmando saída.")
                print("🔄 Retornando ao Saguão para nova rodada...")
                time.sleep(4)
                estado_atual = "SAGUAO"

        time.sleep(1.5)

bot_masmorra()