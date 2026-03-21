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

# def resolver_influencia_invisivel():
#     """Identifica a balança, usa o 'Pronto' como bússola e confirma."""
    
#     # TRAVA DE SEGURANÇA: Se tiver o buraco azul do sacrifício, NÃO é balança! Aborta.
#     if localizar_seguro('slot_sacrificio.png', 0.8):
#         return False

#     # A ÂNCORA: O botão de finalizar seleção (que só aparece lá dentro)
#     if localizar_seguro('finalizar_selecao_btn.png', 0.8):
#         print("⚖️ Tela de Influência detectada!")
        
#         # A BÚSSOLA: Acha o botão Pronto para saber de qual lado nós estamos
#         pos_pronto = localizar_seguro('pronto_btn.png', 0.8)
        
#         if pos_pronto:
#             pronto_x, pronto_y = pyautogui.center(pos_pronto)
            
#             # MATEMÁTICA: Move o mouse 100 pixels para CIMA do Pronto (Exatamente no meio do ícone)
#             print("🎯 Selecionando o efeito acima do botão Pronto...")
#             pyautogui.moveTo(pronto_x, pronto_y - 100, duration=0.3)
#             pyautogui.click()
#             time.sleep(1)
            
#             # Agora sim ele aperta o Pronto para travar a escolha
#             clicar('selecionar_bencao_btn.png', 0.8, "Efeito selecionado!", 1.5)
#             clicar('pronto_btn.png', 0.8, "Efeito travado no Pronto!", 1.5)
        
#         # Tenta finalizar a seleção (O líder aperta isso quando os dois terminarem)
#         clicar('finalizar_selecao_btn.png', 0.8, "Apertando em Finalizar Seleção...", 2)
#         return True
        
#     return False

def resolver_influencia_invisivel():
    """Identifica a balança, usa o 'Pronto' específico como bússola e confirma."""
    
    # TRAVA DE SEGURANÇA 1: Se tiver buraco de sacrifício, NÃO é balança!
    if localizar_seguro('slot_sacrificio.png', 0.8):
        return False
        
    # TRAVA DE SEGURANÇA 2 (A CORREÇÃO): Se tiver buraco de tropa normal, é Combate Mortal! Aborta.
    if localizar_seguro('slot_vazio.png', 0.8):
        return False

    # A ÂNCORA: O botão de finalizar seleção (que só aparece lá dentro)
    if localizar_seguro('finalizar_selecao_btn.png', 0.8):
        print("⚖️ Tela de Influência detectada!")
        
        # A BÚSSOLA CORRIGIDA: Usa o botão 'Pronto' PEQUENO, exclusivo desta tela!
        pos_pronto = localizar_seguro('pronto_bencao_btn.png', 0.8)
        
        if pos_pronto:
            pronto_x, pronto_y = pyautogui.center(pos_pronto)
            
            # MATEMÁTICA: Move o mouse 100 pixels para CIMA do Pronto
            print("🎯 Achei o Pronto! Selecionando o efeito acima dele...")
            pyautogui.moveTo(pronto_x, pronto_y - 100, duration=0.3)
            pyautogui.click()
            time.sleep(1)
            
            clicar('pronto_bencao_btn.png', 0.8, "Efeito travado no Pronto!", 1.5)
            return True 
        
        clicar('finalizar_selecao_btn.png', 0.8, "Apertando em Finalizar Seleção...", 2)
        clicar('fechar_btn.png', 0.8, "Apertando em Fechar Benção...", 2)

        return True
        
    return False

def preparar_esquadrao_masmorra(estou_lider):
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

    # 3. Lógica de Preenchimento (Trabalho braçal ou automático)
    if slots_normais or slots_sacrificio:
        
        if tem_posicionar:
            print("✨ Tela de Esquadrão Normal! Preenchendo automático...")
            clicar('posicionar_melhores_btn.png', 0.8, "Auto-preenchimento ativado!", 1.5)
        else:
            # Descobrindo se é um combate ou um altar de sangue
            eh_sacrificio = len(slots_sacrificio) > 0
            alvos_vazios = slots_normais if slots_normais else slots_sacrificio
            todas_tropas = localizar_todos_seguro('base_tropa.png', 0.8) 
            
            if alvos_vazios and todas_tropas:
                # O FILTRO DE ALTURA: Ignora a barra de vida do Tank posicionado e pega SÓ o andar de baixo.
                altura_dos_buracos = alvos_vazios[0].top
                tropas_reserva = [t for t in todas_tropas if t.top > altura_dos_buracos + 150]
                
                # Garante que a lista está perfeitamente ordenada da Esquerda (Fortes) para a Direita (Fracos)
                tropas_reserva.sort(key=lambda t: t.left)
                
                # A ESTRATÉGIA GENIAL DE ORDENAÇÃO:
                if eh_sacrificio:
                    # Em altares de sacrifício, nós queremos entregar os mais fracos.
                    print(f"🩸 Altar de Sacrifício detectado! Selecionando as {len(alvos_vazios)} tropas MAIS FRACAS (Fim da fila)...")
                    # Inverte a lista! Agora os fracos (direita) viram os primeiros a serem puxados.
                    tropas_reserva.reverse() 
                else:
                    # Em combates restritos, nós queremos os mais fortes.
                    print(f"⚔️ Combate Restrito detectado! Selecionando as {len(alvos_vazios)} tropas MAIS FORTES (Início da fila)...")
                    # Não inverte. Puxa do início da fila (esquerda).
                
                # Relatório para você acompanhar se ele achou as imagens corretamente
                print(f"🤖 Visão do Bot: Achei {len(alvos_vazios)} buracos vazios e {len(tropas_reserva)} tropas disponíveis.")
                
                if alvos_vazios and tropas_reserva:
                    for i in range(min(len(alvos_vazios), len(tropas_reserva))):
                        tropa_x, tropa_y = pyautogui.center(tropas_reserva[i])
                        slot_x, slot_y = pyautogui.center(alvos_vazios[i])
                        
                        pyautogui.moveTo(tropa_x, tropa_y, duration=0.2)
                        pyautogui.dragTo(slot_x, slot_y, duration=0.6, button='left')
                        time.sleep(0.5)

    # ==================================================
    # 4. A NOVA ORDEM: Confirmar que está Pronto PRIMEIRO!
    # ==================================================
    if clicar('pronto_btn.png', 0.8, "Tropa posicionada! Confirmando 'Pronto'...", 2): 
        # Ele retorna True aqui para voltar pro loop e dar tempo do jogo liberar o ataque
        return True 

    # ==================================================
    # 5. O Arremate (Inteligência de Liderança INFALÍVEL)
    # ==================================================
    # O bot aceita a informação que detetamos no mapa!
    if estou_lider:
        # Se formos líder, liberamos o arsenal de ataques Amarelos/Laranjas
        print("👑 Modo Líder: Tropa Pronta. Preparando o ataque...")
        ataque_desativado = localizar_seguro('ataque_rapido_cinza.png', 0.8)
        
        if not ataque_desativado:
            if clicar('ataque_rapido_btn.png', 0.9, "Ataque Rápido acionado!", 3): return True
                
        if clicar('a_batalha_laranja_btn.png', 0.8, "À Batalha LARANJA acionado!", 3): return True
        elif clicar('a_batalha_verde_btn.png', 0.8, "À Batalha VERDE acionado!", 3): return True
        elif clicar('finalizar_selecao_btn.png', 0.8, "Seleção finalizada (Sacrifício/Chefe)!", 3): return True

    # SE O MAPA DISSE QUE SOU PASSAGEIRO:
    if not estou_lider:
        print("⏳ Modo Passageiro: Tropas prontas! Fechando a tela para aguardar o líder...")
        # Como o botão "Pronto" já foi apertado na Etapa 4, ele cai aqui, aperta o X e espera.
        # Nós usamos o "X" padrão, pois o exclusivo de vitória só aparece na tela de vitória.
        if clicar('fechar_x.png', 0.8, "Fechando tela de tropas (Aguardando ataque do líder)", 2): 
            return True

    return True

def iniciar_automacao_masmorra():
    print("🏰=== BOT DA MASMORRA (RECONSTRUTOR) INICIADO ===🏰")
    print("Mude para a janela do jogo agora! O bot assume em 5 segundos...")
    time.sleep(5)
    
    tentativas_sem_achar_nada = 0
    sou_lider = False # Inicializamos como passageiro por padrão

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
            tentativas_sem_achar_nada = 0; continue

        elif localizar_seguro('aguardando_jogador.png', 0.8):
            print("⏳ Aguardando jogador aleatório aceitar a partida...")
            tentativas_sem_achar_nada = 0; continue
            
        elif clicar('aceitar_partida_btn.png', 0.8, "Aceitando Parceiro!", 4): tentativas_sem_achar_nada = 0; continue

        # --- A CORREÇÃO DE LIDERANÇA DEFINTIVA: Olhar Antes de Pular ---
        pos_va_mapa = localizar_seguro('va_para_o_mapa_btn.png', 0.8)
        
        if pos_va_mapa:
            print("👀 Aviso de entrada detectado! Analisando a liderança ANTES de prosseguir...")
            
            # 1. Procura a moeda da liderança COM A TELA AINDA PARADA
            moeda = localizar_seguro('moeda_nao_lider_mapa.png', 0.9)
            
            if moeda:
                sou_lider = False
                print("👑 Moeda de Liderança NÃO detectada! Seguindo como passageiro.")
            else:
                sou_lider = True
                print("⏳ Moeda de Liderança detectada. Assumindo o comando da jornada.")
                
            # 2. Agora sim ele clica no botão "Vá para o mapa" para fechar o aviso!
            x, y = pyautogui.center(pos_va_mapa)
            pyautogui.moveTo(x + random.randint(-5, 5), y + random.randint(-5, 5), duration=0.3)
            pyautogui.click()
            print("✅ Fechando aviso e entrando no mapa interno!")
            time.sleep(3) # Espera a animação de entrada terminar
            
            tentativas_sem_achar_nada = 0; continue
        
        # ==========================================
        # PRIORIDADE 2: EMERGÊNCIAS, PREPARAÇÃO E TRANSIÇÕES IMPORTANTES
        # ==========================================
        # 1º O Botão Verde de entrar nas salas
        elif clicar('ir_aqui_bencao_btn.png', 0.5, "Entrando no ponto de interesse...", 2): tentativas_sem_achar_nada = 0; continue

        # 2º A Balança DEVE vir antes do esquadrão!
        elif resolver_influencia_invisivel(): tentativas_sem_achar_nada = 0; continue
        
        # 3º O Esquadrão/Tropas (PASSAMOS A INFORMAÇÃO DA LIDERANÇA COMO ARGUMENTO)
        elif preparar_esquadrao_masmorra(sou_lider): tentativas_sem_achar_nada = 0; continue

        # O botão de fechar pop-up normal
        elif clicar('fechar_x.png', 0.8, "Fechando Janela/Pop-up"): tentativas_sem_achar_nada = 0; continue
        elif clicar('sim_btn.png', 0.8, "Confirmando (Sim)"): tentativas_sem_achar_nada = 0; continue

        # ==========================================
        # PRIORIDADE 3: SAÍDA E MAPA
        # ==========================================
        # O X exclusivo de vitória, com 90% de confiança
        elif clicar('fechar_vitoria_x.png', 0.9, "Fechando tela de Vitória (X)!", 3): tentativas_sem_achar_nada = 0; continue
        
        elif clicar('inicio_btn.png', 0.8, "Saindo da tela de Vitória!", 2): tentativas_sem_achar_nada = 0; continue
        elif clicar('mover_para_ca.png', 0.8, "Confirmando passo no mapa...", 2): tentativas_sem_achar_nada = 0; continue
        
        elif clicar('terminar_jornada_btn.png', 0.8, "Masmorra concluída com sucesso! Saindo...", 2): tentativas_sem_achar_nada = 0; continue
        elif clicar('recolher_premio.png', 0.8, "Recolhendo baú no chão", 1.5): tentativas_sem_achar_nada = 0; continue

        # ==========================================
        # PRIORIDADE 4: LÓGICA DE NÓS (SÓ PARA O LÍDER)
        # ==========================================
        # Usamos a mesma variável para decidir se devemos andar
        if sou_lider:
            if clicar_lista('lacaio_node.png', 0.75, "Caminhando: Chefe/Lacaio"): tentativas_sem_achar_nada = 0; continue
            elif clicar_lista('node_btn.png', 0.75, "Caminhando: Câmara dos Espíritos (Caveira)"): tentativas_sem_achar_nada = 0; continue
            elif clicar_lista('machados_btn.png', 0.75, "Caminhando: Combate Difícil (Machados)"): tentativas_sem_achar_nada = 0; continue
            
            elif clicar_lista('no_espada.png', 0.75, "Caminhando: Combate Normal (Espada)"): tentativas_sem_achar_nada = 0; continue
            elif clicar_lista('no_espelho.png', 0.75, "Caminhando: Combate das Sombras (Espelho)"): tentativas_sem_achar_nada = 0; continue
            elif clicar_lista('no_influencia.png', 0.75, "Caminhando: Balança (Influência)"): tentativas_sem_achar_nada = 0; continue
            # Nó do altar, com a nova imagem salva.
            elif clicar_lista('no_sacrificio.png', 0.75, "Caminhando: Altar (Cálice)"): tentativas_sem_achar_nada = 0; continue

        # ==========================================
        # PRIORIDADE 5: ARRASTAR MAPA (FALLBACK)
        # ==========================================
        tentativas_sem_achar_nada += 1
        
        # Tenta fechar X residuais
        clicar('fechar_x.png', 0.8, "Fechando Janela/Pop-up")
        
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