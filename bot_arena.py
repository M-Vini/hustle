import pyautogui
import time
import random

# CONFIGURAÇÕES DE SEGURANÇA
pyautogui.FAILSAFE = True

# ==========================================
# FUNÇÕES DE AMORTECIMENTO (Evitam Erros Críticos)
# ==========================================
def localizar_seguro(imagem, confianca=0.8):
    """Busca uma imagem. Se não achar, não dá erro, apenas retorna Vazio (None)."""
    try:
        return pyautogui.locateOnScreen(f'imagens_arena/{imagem}', confidence=confianca)
    except Exception:
        return None

def localizar_todos_seguro(imagem, confianca=0.8):
    """Busca todas as imagens. Se não achar, retorna uma lista vazia sem dar erro."""
    try:
        return list(pyautogui.locateAllOnScreen(f'imagens_arena/{imagem}', confidence=confianca))
    except Exception:
        return []

# ==========================================
# AÇÃO DO MOUSE
# ==========================================
def clicar(imagem, confianca=0.8, nome="", espera=1, mover_duration=0.3):
    """Procura uma imagem na tela e clica nela com movimento suave."""
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
# INTELIGÊNCIA DO RADAR
# ==========================================
def executar_ataque_priorizado():
    """
    Radar de alvos priorizado.
    Prioridade 1: Mesma linha e à esquerda.
    Prioridade 2: Qualquer um acima.
    Prioridade 3: Qualquer um abaixo.
    """
    try:
        # 1. Acha o radar do usuário
        eu = localizar_seguro('meu_perfil_arena.png', 0.35)
        if not eu:
            print("⚠️ Radar: Não achei o seu perfil na tabela para referência.")
            time.sleep(3)
            return False

        meu_y = eu.top
        meu_x = eu.left

        # 2. Scanner de Oponentes SEGURO
        ouro = localizar_todos_seguro('arena_ouro.png', 0.75)
        prata = localizar_todos_seguro('arena_prata.png', 0.75)
        bronze = localizar_todos_seguro('arena_bronze.png', 0.75)
        normal = localizar_todos_seguro('arena_normal.png', 0.75)

        botoes_ataque = ouro + prata + bronze + normal

        if not botoes_ataque:
            print("⚠️ Radar: Nenhum oponente válido encontrado na tabela.")
            return False

        # 3. A Nova Matemática de Prioridades
        margem_y = 60 # Aumentamos para 60! O castelo fica mais baixo que as taças

        # Filtro 1: Mesma linha (diferença de Y <= 60) E à esquerda
        alvos_esquerda_linha = [alvo for alvo in botoes_ataque if abs(alvo.top - meu_y) <= margem_y and alvo.left < meu_x]
        
        # Filtro 2: Acima de mim (Y é menor)
        alvos_acima = [alvo for alvo in botoes_ataque if alvo.top < (meu_y - margem_y)]

        # Filtro 3: Abaixo de mim
        alvos_abaixo = [alvo for alvo in botoes_ataque if alvo.top > (meu_y + margem_y)]

        # 4. Decisão de Combate seguindo a sua regra exata
        if alvos_esquerda_linha:
            print(f"🎯 PRIORIDADE 1: Achei {len(alvos_esquerda_linha)} alvo(s) na MESMA LINHA e à ESQUERDA!")
            # Pega o que está mais à esquerda possível
            alvos_esquerda_linha.sort(key=lambda x: x.left, reverse=True)
            alvo_escolhido = alvos_esquerda_linha[0]
            
        elif alvos_acima:
            print(f"🎯 PRIORIDADE 2: Achei {len(alvos_acima)} alvo(s) ACIMA de você!")
            # O "top // 50" cria prateleiras. O "reverse=True" pega a prateleira mais próxima da sua cabeça e o maior X (mais à direita)
            alvos_acima.sort(key=lambda x: (x.top // 50, x.left), reverse=True)
            alvo_escolhido = alvos_acima[0]
            
        elif alvos_abaixo:
            print(f"🎯 PRIORIDADE 3: Atacando o último alvo possível ABAIXO de você!")
            # Pega a fileira mais baixa (maior Y) e dentro dela, o mais à direita (maior X)
            alvos_abaixo.sort(key=lambda x: (x.top // 50, x.left), reverse=True)
            alvo_escolhido = alvos_abaixo[0]
            
        else:
            print("⚠️ Fallback: Atacando aleatório de todos disponíveis!")
            alvo_escolhido = random.choice(botoes_ataque)

        # 5. ETAPA 1: Seleção (Clique na placa)
        x, y = pyautogui.center(alvo_escolhido)
        pyautogui.moveTo(x + random.randint(-5, 5), y + random.randint(-5, 5), duration=0.4)
        pyautogui.click()
        print("⚔️ Etapa 1: Oponente selecionado. Aguardando tela de perfil...")
        time.sleep(2)

        # 6. ETAPA 2: Confirmação
        for _ in range(4):
            if clicar('ataque_rapido_btn.png', 0.75, "Etapa 2: Confirmado combate final!", 5):
                return True
            time.sleep(1)

        print("❌ Falha: Selecionou o oponente, mas não achou o botão 'À batalha!'.")
        return False

    except Exception as e:
        print(f"❌ Erro INESPERADO no radar: {e}")
        return False

# ==========================================
# LOOP PRINCIPAL
# ==========================================
def bot_arena():
    print("🤖=== BOT DA ARENA 2.1 (ANTI-CRASH) INICIADO ===🤖")
    print("Mude para a janela do jogo! O bot assume em 5 segundos...")
    time.sleep(5)

    while True:
        # PRIORIDADE 1: ENTRADA NA ARENA
        if clicar('participar_btn.png', 0.8, "Entrando na Arena (Maçãs)", 1.5): 
            clicar('posicionar_inicio_btn.png', 0.8, "Posicionando tropas...")
            clicar('confirmar_inicio_btn.png', 0.8, "Confirmando arena...")
            continue

        # PRIORIDADE 1.5: SALA DE ESPERA DE FORMA SEGURA
        if localizar_seguro('esperando_fila.png', 0.8):
            print("⏳ Na fila do torneio. Aguardando adversários...")
            time.sleep(3)
            continue

        # PRIORIDADE 2: LÓGICA DE COMBATE
        if executar_ataque_priorizado():
            print("⚔️ Batalha iniciada. Aguardando fim do combate...")
            continue

        # PRIORIDADE 3: PÓS-COMBATE E ACELERAÇÃO
        elif clicar('inicio_btn.png', 0.8, "Saindo da tela de vitória/derrota"): continue
        elif clicar('resgatar_recompensa_btn.png', 0.8, "Arena terminada, recolhendo baú!"): continue
        elif clicar('fim_btn.png', 0.8, "Arena terminada, recolhendo baú!"): continue

        time.sleep(2)

bot_arena()