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
        
        # FILTRO ANTI-ALUCINAÇÃO: Ignora se a imagem for detectada grudada no canto superior (0,0)
        if posicao and posicao.top > 30 and posicao.left > 30:
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
    """Identifica a balança, usa o 'Pronto' como bússola e confirma."""
    
    # TRAVA DE SEGURANÇA: Se tiver o buraco azul do sacrifício, NÃO é balança! Aborta.
    if localizar_seguro('slot_sacrificio.png', 0.8):
        return False

    # A ÂNCORA: O botão de finalizar seleção (que só aparece lá dentro)
    if localizar_seguro('finalizar_selecao_btn.png', 0.8):
        print("⚖️ Tela de Influência detectada!")
        
        # A BÚSSOLA: Acha o botão Pronto para saber de qual lado nós estamos
        pos_pronto = localizar_seguro('pronto_btn.png', 0.8)
        
        if pos_pronto:
            pronto_x, pronto_y = pyautogui.center(pos_pronto)
            
            # MATEMÁTICA: Move o mouse 100 pixels para CIMA do Pronto (Exatamente no meio do ícone)
            print("🎯 Selecionando o efeito acima do botão Pronto...")
            pyautogui.moveTo(pronto_x, pronto_y - 100, duration=0.3)
            pyautogui.click()
            time.sleep(1)
            
            # Agora sim ele aperta o Pronto para travar a escolha
            clicar('selecionar_bencao_btn.png', 0.8, "Efeito selecionado!", 1.5)
            clicar('pronto_btn.png', 0.8, "Efeito travado no Pronto!", 1.5)
        
        # Tenta finalizar a seleção (O líder aperta isso quando os dois terminarem)
        clicar('finalizar_selecao_btn.png', 0.8, "Apertando em Finalizar Seleção...", 2)
        return True
        
    return False

def preparar_esquadrao_masmorra():
    # 1. Escaneia todos os sinais vitais da tela de tropas
    slots_normais = localizar_todos_seguro('slot_vazio.png', 0.8)
    slots_sacrificio = localizar_todos_seguro('slot_sacrificio.png', 0.8)
    tem_posicionar = localizar_seguro('posicionar_melhores_btn.png', 0.8)
    tem_ataque_rapido = localizar_seguro('ataque_rapido_btn.png', 0.8) 
    
    tem_batalha_laranja = localizar_seguro('a_batalha_laranja_btn.png', 0.8)
    tem_batalha_verde = localizar_seguro('a_batalha_verde_btn.png', 0.8)
    
    tem_pronto = localizar_seguro('pronto_btn.png', 0.8)
    tem_finalizar = localizar_seguro('finalizar_selecao_btn.png', 0.8)

    # 2. A Trava de Segurança
    if not (slots_normais or slots_sacrificio or tem_posicionar or tem_ataque_rapido or 
            tem_batalha_laranja or tem_batalha_verde or tem_pronto or tem_finalizar):
        return False 

    # 3. Lógica de Preenchimento (Arruma a casa primeiro)
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

    # ==================================================
    # 4. A NOVA ORDEM: Confirmar que está Pronto PRIMEIRO!
    # ==================================================
    if clicar('pronto_btn.png', 0.8, "Tropa posicionada! Confirmando 'Pronto'...", 2): 
        # Ele retorna True aqui para voltar pro loop e dar tempo do jogo liberar o ataque
        return True 

    # ==================================================
    # 5. O Arremate (Só chega aqui se o Pronto já sumiu)
    # ==================================================
    ataque_desativado = localizar_seguro('ataque_rapido_cinza.png', 0.8)
    
    # Tenta o rápido se não estiver cinza
    if not ataque_desativado:
        if clicar('ataque_rapido_btn.png', 0.9, "Ataque Rápido acionado!", 3): 
            return True
            
    # Planos B, C e D
    if clicar('a_batalha_laranja_btn.png', 0.8, "À Batalha LARANJA acionado!", 3): return True
    elif clicar('a_batalha_verde_btn.png', 0.8, "À Batalha VERDE acionado!", 3): return True
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
        elif clicar('va_para_o_mapa_btn.png', 0.8, "Fechando aviso e entrando no mapa interno!", 3):
            tentativas_sem_achar_nada = 0; continue
        
        # ==========================================
        # PRIORIDADE 2: EMERGÊNCIAS, PREPARAÇÃO E TRANSIÇÕES IMPORTANTES
        # ==========================================
        # 1º O Botão Verde de entrar nas salas
        elif clicar('ir_aqui_btn.png', 0.8, "Entrando no ponto de interesse...", 2): tentativas_sem_achar_nada = 0; continue

        # 2º A Balança DEVE vir antes do esquadrão!
        elif resolver_influencia_invisivel(): tentativas_sem_achar_nada = 0; continue
        
        # 3º O Esquadrão/Tropas
        elif preparar_esquadrao_masmorra(): tentativas_sem_achar_nada = 0; continue

        elif clicar('fechar_x.png', 0.8, "Fechando Janela/Pop-up"): tentativas_sem_achar_nada = 0; continue
        elif clicar('sim_btn.png', 0.8, "Confirmando (Sim)"): tentativas_sem_achar_nada = 0; continue

        # ==========================================
        # PRIORIDADE 3: SAÍDA E MAPA
        # ==========================================
        elif clicar('inicio_btn.png', 0.8, "Saindo da tela de Vitória!", 2): tentativas_sem_achar_nada = 0; continue
        elif clicar('mover_para_ca.png', 0.8, "Confirmando passo no mapa...", 2): tentativas_sem_achar_nada = 0; continue
        
        elif clicar('terminar_jornada_btn.png', 0.8, "Masmorra concluída com sucesso! Saindo...", 2): tentativas_sem_achar_nada = 0; continue
        elif clicar('recolher_premio.png', 0.8, "Recolhendo baú no chão", 1.5): tentativas_sem_achar_nada = 0; continue

        # ==========================================
        # PRIORIDADE 4: LÓGICA DE NÓS (SÓ PARA O LÍDER)
        # ==========================================
        # Reduzimos a confiança para 0.75 para o robô não se confundir com as animações de brilho
        elif clicar_lista('lacaio_node.png', 0.75, "Caminhando: Chefe/Lacaio"): tentativas_sem_achar_nada = 0; continue
        elif clicar_lista('node_btn.png', 0.75, "Caminhando: Câmara dos Espíritos (Caveira)"): tentativas_sem_achar_nada = 0; continue
        elif clicar_lista('machados_btn.png', 0.75, "Caminhando: Combate Difícil (Machados)"): tentativas_sem_achar_nada = 0; continue
        
        # <-- O NOVO CAMINHO ADICIONADO AQUI -->
        elif clicar_lista('no_espada.png', 0.75, "Caminhando: Combate Normal (Espada)"): tentativas_sem_achar_nada = 0; continue
        
        elif clicar_lista('no_espelho.png', 0.75, "Caminhando: Combate das Sombras (Espelho)"): tentativas_sem_achar_nada = 0; continue
        elif clicar_lista('no_influencia.png', 0.75, "Caminhando: Balança (Influência)"): tentativas_sem_achar_nada = 0; continue
        elif clicar_lista('no_sacrificio.png', 0.75, "Caminhando: Altar (Cálice)"): tentativas_sem_achar_nada = 0; continue

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