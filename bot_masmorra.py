import pyautogui
import time
import random

# ==========================================
# CONFIGURAÇÕES DE SEGURANÇA
# ==========================================
pyautogui.FAILSAFE = True 

def localizar_seguro(imagem, confianca=0.8):
    try:
        return pyautogui.locateOnScreen(f'imagens_masmorra/{imagem}', confidence=confianca)
    except Exception:
        return None

def localizar_todos_seguro(imagem, confianca=0.8):
    try:
        return list(pyautogui.locateAllOnScreen(f'imagens_masmorra/{imagem}', confidence=confianca))
    except Exception:
        return []

def clicar(imagem, confianca=0.8, nome="", espera=1):
    try:
        posicao = localizar_seguro(imagem, confianca)
        if posicao:
            x, y = pyautogui.center(posicao)
            pyautogui.moveTo(x + random.randint(-5, 5), y + random.randint(-5, 5), duration=0.3)
            pyautogui.click()
            print(f"✅ {nome}")
            time.sleep(espera)
            return True
        return False
    except Exception:
        return False

def clicar_lista(imagem, confianca=0.8, nome="", espera=2):
    """Procura TODAS as opções no mapa e clica na primeira que achar (Lógica da Catedral)."""
    try:
        itens = localizar_todos_seguro(imagem, confianca)
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

def arrastar_mapa():
    largura, altura = pyautogui.size()
    centro_x = largura // 1.2
    centro_y = altura // 2
    pyautogui.moveTo(centro_x, centro_y)
    pyautogui.dragTo(centro_x - 400, centro_y, duration=0.5, button='left')
    time.sleep(1.5)

def resolver_influencia_invisivel():
    if localizar_seguro('finalizar_selecao_btn.png', 0.8):
        print("⚖️ Tela de Influência detectada! Escolhendo bênção/maldição...")
        if clicar('efeito_positivo.png', 0.8, "Selecionado Efeito Verde!", 1): pass
        elif clicar('efeito_negativo.png', 0.8, "Selecionado Efeito Vermelho!", 1): pass
        clicar('finalizar_selecao_btn.png', 0.8, "Efeito confirmado!", 3)
        return True
    return False

def preparar_esquadrao_masmorra():
    # 1. Escaneia todos os sinais vitais da tela de tropas
    slots_normais = localizar_todos_seguro('slot_vazio.png', 0.8)
    slots_sacrificio = localizar_todos_seguro('slot_sacrificio.png', 0.8)
    tem_posicionar = localizar_seguro('posicionar_melhores_btn.png', 0.8)
    tem_ataque = localizar_seguro('ataque_rapido_btn.png', 0.8)
    tem_pronto = localizar_seguro('pronto_btn.png', 0.8)
    tem_finalizar = localizar_seguro('finalizar_selecao_btn.png', 0.8)

    # 2. A Trava de Segurança: Se não tem NENHUM DESSES, aborta!
    if not (slots_normais or slots_sacrificio or tem_posicionar or tem_ataque or tem_pronto or tem_finalizar):
        return False 

    # 3. Lógica de Preenchimento (Só age se tiver buraco faltando)
    if slots_normais or slots_sacrificio:
        print("✨ Tela de Esquadrão! Preenchendo buracos vazios...")
        
        if tem_posicionar:
            clicar('posicionar_melhores_btn.png', 0.8, "Auto-preenchimento ativado!", 1.5)
        else:
            alvos_vazios = slots_normais if slots_normais else slots_sacrificio
            tropas = localizar_todos_seguro('base_tropa.png', 0.8)
            if alvos_vazios and tropas:
                for i in range(min(len(alvos_vazios), len(tropas))):
                    tropa_x, tropa_y = pyautogui.center(tropas[i])
                    slot_x, slot_y = pyautogui.center(alvos_vazios[i])
                    pyautogui.moveTo(tropa_x, tropa_y, duration=0.2)
                    pyautogui.dragTo(slot_x, slot_y, duration=0.5, button='left')
                    time.sleep(0.3)

    # 4. O Arremate (Finalmente ele chega aqui!)
    if clicar('ataque_rapido_btn.png', 0.8, "Ataque Rápido acionado!", 3): return True
    elif clicar('pronto_btn.png', 0.8, "Tropa confirmada! Aguardando o parceiro...", 3): return True
    elif clicar('finalizar_selecao_btn.png', 0.8, "Seleção finalizada (Sacrifício/Chefe)!", 3): return True

    return True

def iniciar_automacao_masmorra():
    print("🏰=== BOT DA MASMORRA (COM LÓGICA DE NÓS) INICIADO ===🏰")
    print("Mude para a janela do jogo agora! O bot assume em 5 segundos...")
    time.sleep(5)
    
    tentativas_sem_achar_nada = 0
    sou_lider = False

    while True:
        # ==========================================
        # PRIORIDADE 1: NAVEGAÇÃO DO CASTELO ATÉ O SAGUÃO
        # ==========================================
        if clicar('mapa_btn.png', 0.8, "Indo para o Mapa"): tentativas_sem_achar_nada = 0; continue
        elif clicar('masmorra_btn.png', 0.8, "Abrindo Saguão da Masmorra"): tentativas_sem_achar_nada = 0; continue
            
        # ==========================================
        # PRIORIDADE 1.5: SEQUÊNCIA DE ENTRADA (MINI-COMBO)
        # ==========================================
        elif clicar('participar_btn.png', 0.8, "Entrada: Participar"): tentativas_sem_achar_nada = 0; continue
        
        elif localizar_seguro('confirmar_inicio_btn.png', 0.8):
            clicar('posicionar_melhores_inicio_btn.png', 0.8, "Entrada: Posicionando tropas...", 1.5)
            clicar('confirmar_inicio_btn.png', 0.8, "Entrada: Confirmar Tropas", 2)
            tentativas_sem_achar_nada = 0; continue
            
        elif clicar('aleatorio_inicio_btn.png', 0.8, "Entrada: Parceiro Aleatório"):
            print("⏳ Entrando na fila da Masmorra...")
            tentativas_sem_achar_nada = 0; sou_lider = False; continue

        elif localizar_seguro('aguardando_jogador.png', 0.8):
            print("⏳ Aguardando jogador aleatório aceitar a partida...")
            tentativas_sem_achar_nada = 0; continue
            
        elif clicar('aceitar_partida_btn.png', 0.8, "Aceitando Parceiro!", 4): tentativas_sem_achar_nada = 0; continue

        # --- A DECISÃO DE LIDERANÇA SIMPLIFICADA ---
        elif clicar('va_para_mapa_btn.png', 0.8, "Fechando aviso e entrando no mapa interno!", 3):
            tentativas_sem_achar_nada = 0; continue
        
        # ==========================================
        # PRIORIDADE 2: EMERGÊNCIAS E PREPARAÇÃO
        # ==========================================
        elif preparar_esquadrao_masmorra(): tentativas_sem_achar_nada = 0; continue
        elif resolver_influencia_invisivel(): tentativas_sem_achar_nada = 0; continue
        
        elif clicar('fechar_x.png', 0.8, "Fechando Janela/Pop-up"): tentativas_sem_achar_nada = 0; continue
        elif clicar('sim_btn.png', 0.8, "Confirmando (Sim)"): tentativas_sem_achar_nada = 0; continue

        # ==========================================
        # PRIORIDADE 3: TRANSIÇÕES LÁ DENTRO E SAÍDA
        # ==========================================
        elif clicar('inicio_btn.png', 0.8, "Saindo da tela de Vitória!", 2): tentativas_sem_achar_nada = 0; continue
        elif clicar('ir_aqui_btn.png', 0.8, "Entrando no ponto de interesse...", 2): tentativas_sem_achar_nada = 0; continue
        elif clicar('mover_para_ca.png', 0.8, "Confirmando passo no mapa...", 2): tentativas_sem_achar_nada = 0; continue
        
        # O botão agora é o verde!
        elif clicar('terminar_jornada_btn.png', 0.8, "Masmorra concluída com sucesso! Saindo...", 2): tentativas_sem_achar_nada = 0; continue
        elif clicar('recolher_premio.png', 0.8, "Recolhendo baú no chão", 1.5): tentativas_sem_achar_nada = 0; continue

        # ==========================================
        # PRIORIDADE 4: LÓGICA DE NÓS (SÓ PARA O LÍDER)
        # ==========================================
        # O bot vai escanear e tentar clicar do mais difícil/importante para o mais simples
        elif clicar_lista('lacaio_node.png', 0.8, "Caminhando: Chefe/Lacaio"): tentativas_sem_achar_nada = 0; continue
        elif clicar_lista('node_btn.png', 0.8, "Caminhando: Câmara dos Espíritos (Caveira)"): tentativas_sem_achar_nada = 0; continue
        elif clicar_lista('machados_btn.png', 0.8, "Caminhando: Combate Normal (Machados)"): tentativas_sem_achar_nada = 0; continue
        elif clicar_lista('no_espelho.png', 0.8, "Caminhando: Combate das Sombras (Espelho)"): tentativas_sem_achar_nada = 0; continue
        elif clicar_lista('no_influencia.png', 0.8, "Caminhando: Balança (Influência)"): tentativas_sem_achar_nada = 0; continue
        elif clicar_lista('no_sacrificio.png', 0.8, "Caminhando: Altar (Cálice)"): tentativas_sem_achar_nada = 0; continue

        # ==========================================
        # PRIORIDADE 5: ARRASTAR MAPA (FALLBACK)
        # ==========================================
        tentativas_sem_achar_nada += 1
        
        if tentativas_sem_achar_nada >= 3:
            if sou_lider or not localizar_seguro('icone_masmorra_mapa.png', 0.8):
                print("🗺️ Visão limpa. Puxando o mapa para o lado...")
                arrastar_mapa()
            tentativas_sem_achar_nada = 0 
            
        time.sleep(1)

# ==========================================
# RODA O PROGRAMA
# ==========================================
iniciar_automacao_masmorra()