import os
# ============================================================
# FILTRO DE ALTA QUALIDADE (ANISOTRÓPICO / LINEAR PARA 1080p)
# ============================================================
os.environ['SDL_RENDER_SCALE_QUALITY'] = '2' # Força suavização de altíssima qualidade

import ctypes
import random
import pygame

# --- CORREÇÃO DE DPI NO WINDOWS ---
try:
    ctypes.windll.user32.SetProcessDPIAware()
except AttributeError:
    pass

# ============================================================
# FORÇAR MODO FULL HD DESDE A INICIALIZAÇÃO
# ============================================================
original_set_mode = pygame.display.set_mode
def tela_escala_corrigida(size, flags=0, depth=0, display=0, vsync=0):
    flags |= pygame.SCALED
    return original_set_mode(size, flags, depth, display, vsync)
pygame.display.set_mode = tela_escala_corrigida

import pgzero
import pgzrun
from pgzero.actor import Actor

# ============================================================
# CONFIGURAÇÕES DO PGZERO (FULL HD NATIVO)
# ============================================================

WIDTH = 1920
HEIGHT = 1080
TITLE = "Quiz dos Campeões"

# ============================================================
# PALETA DE CORES MODERNA (ALTO CONTRASTE PARA TVS)
# ============================================================
COR_BG = (15, 23, 42)          # Slate Navy Escuro
COR_PAINEL = (30, 41, 59)      # Slate Navy Médio
COR_CABECALHO = (10, 15, 30)

COR_DOURADO = (245, 158, 11)   # Amber/Ouro
COR_TEXTO = (241, 245, 249)    # Off-White
COR_TEXTO_MUTED = (148, 163, 184)

COR_VERDE = (16, 185, 129)     # Esmeralda
COR_VERMELHO = (239, 68, 68)   # Coral
COR_CIANO = (6, 182, 212)

# ============================================================
# ESTADOS E VARIÁVEIS DO JOGO
# ============================================================

estado_jogo = "menu"
pergunta_atual = 0
acertos = 0
tempo_restante = 10.0
opcao_selecionada = None
bloquear_respostas = False
tela_cheia = False 

premios = [
    "Prêmio Surpresa 1", "Vale-Brinde Especial", "Kit de Estudos",
    "Camiseta Exclusiva", "Troféu Simbólico", "Caderno Personalizado",
    "Caneta Especial SESI/SENAI", "Mochila Exclusiva", "Squeeze Térmica",
    "Fone de Ouvido", "Power Bank", "Kit Robótica",
    "Ingresso de Evento", "Super Prêmio Especial"
]

roleta_estado = "aguardando"
roleta_premio_atual = 0
roleta_velocidade = 0.05
roleta_tempo_acumulado = 0.0
roleta_velocidade_parada = 0.4

# ============================================================
# BANCO DE PERGUNTAS (COMPLETO: SENAI + SESI + CONHECIMENTOS)
# ============================================================

banco_perguntas = [
    # --- QUESTÕES SENAI ---
    {
        "pergunta": "O que significa a sigla SENAI?",
        "opcoes": [
            "Serviço Nacional de Aprendizagem Industrial",
            "Serviço Nacional de Apoio Industrial",
            "Sistema Nacional da Indústria",
            "Serviço Nacional de Aprendizagem Integrada"
        ],
        "correta": 0
    },
    {
        "pergunta": "Qual é o principal objetivo do SENAI?",
        "opcoes": [
            "Formar atletas",
            "Promover educação profissional e tecnológica",
            "Fiscalizar empresas",
            "Realizar concursos públicos"
        ],
        "correta": 1
    },
    {
        "pergunta": "Em que ano o SENAI foi criado?",
        "opcoes": ["1930", "1950", "1942", "1964"],
        "correta": 2
    },
    {
        "pergunta": "Qual instituição administra o SENAI Goiás?",
        "opcoes": ["Sebrae", "SENAC", "Prefeitura Municipal", "FIEG"],
        "correta": 3
    },
    {
        "pergunta": "O SENAI oferece apenas cursos presenciais?",
        "opcoes": ["Sim", "Não", "Apenas aos sábados", "Apenas cursos online"],
        "correta": 1
    },
    {
        "pergunta": "O que significa EAD?",
        "opcoes": [
            "Ensino Aberto Digital",
            "Educação Avançada Digital",
            "Educação a Distância",
            "Ensino de Alta Direção"
        ],
        "correta": 2
    },
    {
        "pergunta": "Qual é a cor predominante da marca SENAI?",
        "opcoes": ["Vermelho", "Verde", "Azul", "Amarelo"],
        "correta": 2
    },
    {
        "pergunta": "Qual é o foco principal dos cursos do SENAI?",
        "opcoes": [
            "Preparar profissionais para o mercado de trabalho",
            "Formar atletas",
            "Ensinar idiomas exclusivamente",
            "Realizar pesquisas eleitorais"
        ],
        "correta": 0
    },
    {
        "pergunta": "O que significa a sigla EPI?",
        "opcoes": [
            "Equipamento de Produção Industrial",
            "Equipamento de Proteção Individual",
            "Escola Profissional Industrial",
            "Equipamento Profissional Integrado"
        ],
        "correta": 1
    },
    {
        "pergunta": "O SENAI é reconhecido principalmente por:",
        "opcoes": [
            "Formação profissional de qualidade",
            "Administração de rodovias",
            "Transporte de cargas",
            "Construção civil"
        ],
        "correta": 0
    },
    {
        "pergunta": "Em qual cidade está localizada a Unidade SENAI Otávio Lage de Siqueira Filho?",
        "opcoes": ["Goiânia", "Jaraguá", "Goianésia", "Anápolis"],
        "correta": 2
    },
    {
        "pergunta": "O SENAI Goianésia oferece:",
        "opcoes": [
            "Apenas cursos de informática",
            "Apenas graduação",
            "Qualificação, técnico e aprendizagem",
            "Apenas pós-graduação"
        ],
        "correta": 2
    },
    {
        "pergunta": "Uma das principais vantagens de estudar no SENAI Goianésia é:",
        "opcoes": [
            "Ensino alinhado às necessidades das empresas",
            "Aulas apenas aos domingos",
            "Ausência de avaliações",
            "Ensino exclusivamente teórico"
        ],
        "correta": 0
    },
    {
        "pergunta": "O SENAI Goianésia realiza parcerias com empresas da região?",
        "opcoes": ["Não", "Apenas em anos pares", "Sim", "Apenas empresas internacionais"],
        "correta": 2
    },
    {
        "pergunta": "Qual é a importância do SENAI para o desenvolvimento regional?",
        "opcoes": [
            "Formar mão de obra qualificada",
            "Administrar municípios",
            "Fiscalizar escolas",
            "Construir rodovias"
        ],
        "correta": 0
    },
    {
        "pergunta": "Por que o SENAI é considerado uma das maiores instituições do Brasil?",
        "opcoes": [
            "Pela quantidade de estádios que possui",
            "Pela qualidade do ensino e abrangência nacional",
            "Pela atuação política",
            "Pela fabricação de máquinas"
        ],
        "correta": 1
    },
    {
        "pergunta": "Por que o SENAI Goianésia é referência na formação profissional?",
        "opcoes": [
            "Porque oferece apenas cursos gratuitos",
            "Porque atende somente empresas industriais",
            "Porque alia qualidade, estrutura e proximidade com a indústria",
            "Porque atua apenas em Goianésia"
        ],
        "correta": 2
    },

    # --- QUESTÕES SESI ---
    {
        "pergunta": "O que significa a sigla SESI?",
        "opcoes": [
            "Sistema de Estudos da Indústria",
            "Serviço Social da Indústria",
            "Serviço Escolar do Setor Industrial",
            "Sistema Educacional Social Integrado"
        ],
        "correta": 1
    },
    {
        "pergunta": "O SESI integra qual grande sistema brasileiro?",
        "opcoes": [
            "Sistema Financeiro Nacional",
            "Sistema Único de Educação",
            "Sistema Indústria",
            "Sistema Federal de Universidades"
        ],
        "correta": 2
    },
    {
        "pergunta": "Na proposta educacional do SESI, qual é o papel do estudante?",
        "opcoes": [
            "Estudar somente para avaliações",
            "Receber conhecimento sem investigação",
            "Participar ativamente e desenvolver protagonismo",
            "Apenas ouvir e reproduzir conteúdos"
        ],
        "correta": 2
    },
    {
        "pergunta": "O que melhor representa a aprendizagem “mão na massa”?",
        "opcoes": [
            "Realizar apenas atividades individuais",
            "Experimentar, criar, testar e construir soluções",
            "Usar tecnologia em todas as aulas",
            "Copiar conteúdos para memorizar"
        ],
        "correta": 1
    },
    {
        "pergunta": "Qual experiência representa um diferencial da educação SESI?",
        "opcoes": [
            "Memorização como estratégia principal",
            "Robótica e tecnologia integradas à aprendizagem",
            "Aulas baseadas somente em apostilas",
            "Atividades sem projetos ou investigação"
        ],
        "correta": 1
    },
    {
        "pergunta": "A robótica educacional contribui especialmente para desenvolver:",
        "opcoes": [
            "Somente treino para provas",
            "Apenas memorização de respostas",
            "Raciocínio, criatividade e resolução de problemas",
            "Somente velocidade de leitura"
        ],
        "correta": 2
    },
    {
        "pergunta": "Por que trabalhar Educação Financeira na escola?",
        "opcoes": [
            "Para ensinar somente operações bancárias",
            "Para transformar todas as atividades em cálculos",
            "Para substituir o ensino de Matemática",
            "Para desenvolver planejamento e escolhas conscientes"
        ],
        "correta": 3
    },
    {
        "pergunta": "Para o SESI, uma educação de qualidade deve promover:",
        "opcoes": [
            "Quantidade elevada de tarefas",
            "Aprendizagem, desenvolvimento integral e autonomia",
            "Uso de tecnologia como objetivo final",
            "Somente notas altas em avaliações"
        ],
        "correta": 1
    },
    {
        "pergunta": "Para que servem indicadores e evidências de aprendizagem?",
        "opcoes": [
            "Medir apenas a quantidade de atividades",
            "Substituir o planejamento dos professores",
            "Acompanhar resultados e orientar ações pedagógicas",
            "Classificar estudantes como finalidade principal"
        ],
        "correta": 2
    },
    {
        "pergunta": "Qual é a principal finalidade do AVALIA SESI?",
        "opcoes": [
            "Avaliar apenas comportamento e frequência",
            "Substituir todas as avaliações realizadas pela escola",
            "Gerar evidências para acompanhar a aprendizagem e orientar ações",
            "Aplicar uma nota sem uso pedagógico posterior"
        ],
        "correta": 2
    },
    {
        "pergunta": "Qual conjunto representa competências valorizadas na formação do estudante?",
        "opcoes": [
            "Silêncio, reprodução e respostas padronizadas",
            "Velocidade, quantidade de tarefas e cópia",
            "Autonomia, criatividade, colaboração e pensamento crítico",
            "Memorização, repetição e competição permanente"
        ],
        "correta": 2
    },
    {
        "pergunta": "Qual é o papel da tecnologia na educação SESI?",
        "opcoes": [
            "Ser usada apenas para entretenimento",
            "Eliminar atividades presenciais e práticas",
            "Ampliar experiências de aprendizagem, criação e investigação",
            "Substituir completamente o professor"
        ],
        "correta": 2
    },
    {
        "pergunta": "Em quais etapas e frentes educacionais o SESI atua nacionalmente?",
        "opcoes": [
            "Somente Ensino Fundamental e Ensino Médio",
            "Apenas Educação Profissional Técnica",
            "Educação Infantil, Ensino Fundamental, Ensino Médio e EJA",
            "Ensino Superior, Mestrado, Doutorado e EJA"
        ],
        "correta": 2
    },
    {
        "pergunta": "Por que o SESI é uma escolha para a educação dos filhos?",
        "opcoes": [
            "Porque utiliza tecnologia como único recurso",
            "Porque o estudante aprende apenas dentro da sala de aula",
            "Porque prioriza somente conteúdos e avaliações",
            "Porque une aprendizagem, inovação, experiências práticas e desenvolvimento integral"
        ],
        "correta": 3
    },
    {
        "pergunta": "Complete a frase da nossa campanha: “O futuro começa com boas...”",
        "opcoes": ["Provas", "Escolhas", "Tarefas", "Notas"],
        "correta": 1
    },

    # --- QUESTÕES GERAIS E REGIONAIS ---
    {
        "pergunta": "Qual é a capital do Brasil?",
        "opcoes": ["São Paulo", "Brasília", "Rio de Janeiro", "Belo Horizonte"],
        "correta": 1
    },
    {
        "pergunta": "Quanto é 7 x 8?",
        "opcoes": ["54", "56", "62", "48"],
        "correta": 1
    },
    {
        "pergunta": "Qual instituição é referência em formação profissional industrial?",
        "opcoes": ["CEPI", "SENAI", "FIEG", "MEC"],
        "correta": 1
    },
    {
        "pergunta": "Qual é o maior oceano do planeta Terra?",
        "opcoes": ["Oceano Atlântico", "Oceano Índico", "Oceano Pacífico", "Oceano Ártico"],
        "correta": 2
    },
    {
        "pergunta": "Qual é o elemento químico representado pelo símbolo 'O'?",
        "opcoes": ["Ouro", "Oxigênio", "Ozônio", "Ósmio"],
        "correta": 1
    },
    {
        "pergunta": "Quantos estados compõem a República Federativa do Brasil?",
        "opcoes": ["25", "26", "27", "28"],
        "correta": 1
    },
    {
        "pergunta": "Qual planeta é conhecido como o 'Planeta Vermelho'?",
        "opcoes": ["Vênus", "Marte", "Júpiter", "Saturno"],
        "correta": 1
    },
    {
        "pergunta": "Em que ano o Brasil declarou sua Independência?",
        "opcoes": ["1500", "1822", "1889", "1988"],
        "correta": 1
    },
    {
        "pergunta": "Qual é o maior país do mundo em área territorial?",
        "opcoes": ["Canadá", "China", "Estados Unidos", "Rússia"],
        "correta": 3
    },
    {
        "pergunta": "Qual o resultado de 12 + 15 - 7?",
        "opcoes": ["18", "20", "22", "25"],
        "correta": 1
    },
    {
        "pergunta": "O que significa a sigla FIEG?",
        "opcoes": [
            "Federação das Indústrias do Estado de Goiás",
            "Frente Industrial de Goiás",
            "Fundação de Incentivo ao Estudo de Goiás",
            "Federação Internacional de Educação Geral"
        ],
        "correta": 0
    },
    {
        "pergunta": "Qual é o idioma oficial do Brasil?",
        "opcoes": ["Espanhol", "Inglês", "Português", "Tupi-Guarani"],
        "correta": 2
    }
]

perguntas = []

# ============================================================
# LOGOS E ELEMENTOS (POSIÇÕES AJUSTADAS PARA 1080p)
# ============================================================

try:
    logo_cepi = Actor("cepi", (210, 90))
    logo_jalles = Actor("jalles", (375, 90))       
    logo_fieg = Actor("fieg", (960, 90))           
    logo_sesisenai = Actor("sesisenai", (1530, 90)) 
except:
    pass 

# Botões reajustados para áreas de toque maiores (Touch Screen friendly)
botao_comecar = Rect((660, 720), (600, 105))
botao_acao = Rect((660, 840), (600, 98)) 
botao_tela = Rect((30, 990), (330, 60))  

botoes_opcoes = [
    Rect((360, 410), (1200, 95)),
    Rect((360, 530), (1200, 95)),
    Rect((360, 650), (1200, 95)),
    Rect((360, 770), (1200, 95))
]

# ============================================================
# FUNÇÃO AUXILIAR DE DESENHO (CARDS COM BORDAS ARREDONDADAS)
# ============================================================

def desenhar_card(rect, cor_fundo, cor_borda=None, raio=24, espessura=3, sombra=True):
    """Desenha cards com bordas arredondadas e sombra projetada."""
    if sombra:
        sombra_rect = Rect((rect.x + 6, rect.y + 6), (rect.width, rect.height))
        pygame.draw.rect(screen.surface, (5, 10, 20), sombra_rect, border_radius=raio)
    
    pygame.draw.rect(screen.surface, cor_fundo, rect, border_radius=raio)
    
    if cor_borda:
        pygame.draw.rect(screen.surface, cor_borda, rect, width=espessura, border_radius=raio)

def alternar_tela():
    global tela_cheia
    tela_cheia = not tela_cheia
    pygame.display.toggle_fullscreen()

# ============================================================
# LÓGICA DO QUIZ
# ============================================================

def reiniciar_jogo():
    global pergunta_atual, acertos, tempo_restante, opcao_selecionada, bloquear_respostas, perguntas
    perguntas = random.sample(banco_perguntas, k=3)
    pergunta_atual = 0
    acertos = 0
    tempo_restante = 10.0
    opcao_selecionada = None
    bloquear_respostas = False

def preparar_roleta():
    global roleta_estado, roleta_velocidade, roleta_tempo_acumulado, roleta_velocidade_parada, roleta_premio_atual
    roleta_estado = "aguardando"
    roleta_velocidade = 0.05
    roleta_tempo_acumulado = 0.0
    roleta_velocidade_parada = random.uniform(0.35, 0.5)
    roleta_premio_atual = random.randint(0, len(premios) - 1)

def proxima_pergunta():
    global pergunta_atual, tempo_restante, opcao_selecionada, bloquear_respostas, estado_jogo
    pergunta_atual += 1
    opcao_selecionada = None
    bloquear_respostas = False
    tempo_restante = 10.0

    if pergunta_atual >= len(perguntas):
        estado_jogo = "fim"

def verificar_resposta(indice_resposta):
    global acertos, opcao_selecionada, bloquear_respostas
    if bloquear_respostas:
        return

    bloquear_respostas = True
    opcao_selecionada = indice_resposta
    resposta_correta = perguntas[pergunta_atual]["correta"]

    if indice_resposta == resposta_correta:
        acertos += 1

    clock.schedule_unique(proxima_pergunta, 1.2)

def update(dt):
    global tempo_restante, estado_jogo, bloquear_respostas
    global roleta_estado, roleta_tempo_acumulado, roleta_velocidade, roleta_premio_atual

    if estado_jogo == "quiz" and not bloquear_respostas:
        tempo_restante -= dt
        if tempo_restante <= 0:
            tempo_restante = 0
            bloquear_respostas = True
            clock.schedule_unique(proxima_pergunta, 1.0)
            
    elif estado_jogo == "roleta" and roleta_estado == "girando":
        roleta_tempo_acumulado += dt
        
        if roleta_tempo_acumulado >= roleta_velocidade:
            roleta_tempo_acumulado = 0
            roleta_premio_atual = (roleta_premio_atual + 1) % len(premios)
            roleta_velocidade += 0.015 
            
            if roleta_velocidade >= roleta_velocidade_parada:
                roleta_estado = "parou"

# ============================================================
# TELAS DO JOGO (ADAPTADAS PARA 1080p)
# ============================================================

def desenhar_cabecalho():
    pygame.draw.rect(screen.surface, COR_CABECALHO, Rect((0, 0), (1920, 165)))
    pygame.draw.rect(screen.surface, COR_DOURADO, Rect((0, 160), (1920, 6)))
    try:
        logo_cepi.draw()
        logo_jalles.draw()
        logo_fieg.draw()
        logo_sesisenai.draw()
    except:
        pass

def desenhar_menu():
    screen.fill(COR_BG)
    desenhar_cabecalho()

    # Título Principal
    screen.draw.text("QUIZ", center=(960, 360), fontsize=130, color=COR_DOURADO)
    screen.draw.text("DOS CAMPEÕES", center=(960, 470), fontsize=85, color=COR_TEXTO)
    
    # Linha Decorativa
    pygame.draw.line(screen.surface, COR_DOURADO, (660, 530), (1260, 530), 4)

    screen.draw.text("Mostre seus conhecimentos!", center=(960, 580), fontsize=38, color=COR_TEXTO)
    screen.draw.text("Responda corretamente e conquiste o título de campeão!", center=(960, 630), fontsize=26, color=COR_TEXTO_MUTED)

    # Botão Começar
    desenhar_card(botao_comecar, COR_DOURADO, cor_borda=COR_TEXTO, raio=28)
    screen.draw.text("COMEÇAR QUIZ", center=botao_comecar.center, fontsize=40, color=(15, 23, 42))

    # Botão Tela Cheia
    desenhar_card(botao_tela, COR_PAINEL, cor_borda=COR_TEXTO_MUTED, raio=16, sombra=False)
    texto_tela = "TELA CHEIA" if not tela_cheia else "MODO JANELA"
    screen.draw.text(texto_tela, center=botao_tela.center, fontsize=24, color=COR_TEXTO)

    screen.draw.text("PREPARE-SE PARA O DESAFIO!", center=(960, 900), fontsize=28, color=COR_DOURADO)
    screen.draw.text("Desenvolvido por: 2º Tec A do Curso Tecnico em Desenvolvimento de Sistemas do CEPI Costa e Silva\nInstrutor Orientador Isaac Mendes | Instrutor de Informatica Isaque Pontes", center=(960, 980), fontsize=20, color=COR_TEXTO_MUTED)

def desenhar_quiz():
    screen.fill(COR_BG)
    desenhar_cabecalho()

    dados_pergunta = perguntas[pergunta_atual]

    # Indicadores da Partida
    screen.draw.text(f"Acertos: {acertos}", (90, 200), fontsize=38, color=COR_DOURADO)
    screen.draw.text(f"Pergunta {pergunta_atual + 1}/{len(perguntas)}", (870, 200), fontsize=38, color=COR_TEXTO)

    # Barra de Tempo Arredondada
    largura_max = 300
    largura_atual = int((tempo_restante / 10.0) * largura_max)
    cor_tempo = COR_VERMELHO if tempo_restante <= 3 else COR_CIANO
    rect_tempo_bg = Rect((1530, 200), (largura_max, 32))
    rect_tempo_fill = Rect((1530, 200), (max(0, largura_atual), 32))
    
    pygame.draw.rect(screen.surface, COR_PAINEL, rect_tempo_bg, border_radius=16)
    if largura_atual > 0:
        pygame.draw.rect(screen.surface, cor_tempo, rect_tempo_fill, border_radius=16)

    # Caixa da Pergunta
    caixa_pergunta = Rect((210, 260), (1500, 120))
    desenhar_card(caixa_pergunta, COR_PAINEL, cor_borda=COR_DOURADO, raio=24)
    screen.draw.text(dados_pergunta["pergunta"], center=caixa_pergunta.center, fontsize=36, color=COR_TEXTO)

    correta = dados_pergunta["correta"]

    # Opções de Resposta
    for i, caixa in enumerate(botoes_opcoes):
        cor_fundo = COR_PAINEL
        cor_borda = COR_TEXTO_MUTED

        if bloquear_respostas:
            if i == correta:
                cor_fundo = COR_VERDE
                cor_borda = COR_TEXTO
            elif i == opcao_selecionada:
                cor_fundo = COR_VERMELHO
                cor_borda = COR_TEXTO

        desenhar_card(caixa, cor_fundo, cor_borda=cor_borda, raio=20)
        texto_opcao = f"{chr(65 + i)}) {dados_pergunta['opcoes'][i]}"
        screen.draw.text(texto_opcao, midleft=(caixa.x + 40, caixa.centery), fontsize=30, color=COR_TEXTO)

def desenhar_fim():
    screen.fill(COR_BG)
    desenhar_cabecalho()

    if acertos == 3:
        screen.draw.text("PARABÉNS! VOCÊ É UM CAMPEÃO!", center=(960, 340), fontsize=75, color=COR_VERDE)
        screen.draw.text("Você teve 100% de aproveitamento!", center=(960, 440), fontsize=45, color=COR_DOURADO)
        
        desenhar_card(botao_acao, COR_VERDE, cor_borda=COR_TEXTO, raio=28)
        screen.draw.text("SORTEAR MEU PRÊMIO", center=botao_acao.center, fontsize=38, color=(15, 23, 42))
    else:
        screen.draw.text("FIM DO QUIZ!", center=(960, 340), fontsize=85, color=COR_DOURADO)
        screen.draw.text(f"Você acertou {acertos} de {len(perguntas)} perguntas.", center=(960, 440), fontsize=45, color=COR_TEXTO)
        screen.draw.text("Tente novamente para acertar todas e ganhar prêmios!", center=(960, 510), fontsize=32, color=COR_TEXTO_MUTED)

        desenhar_card(botao_acao, COR_DOURADO, cor_borda=COR_TEXTO, raio=28)
        screen.draw.text("VOLTAR AO MENU", center=botao_acao.center, fontsize=38, color=(15, 23, 42))

def desenhar_roleta():
    screen.fill(COR_BG)
    desenhar_cabecalho()

    screen.draw.text("ROLETA DE PRÊMIOS", center=(960, 210), fontsize=58, color=COR_DOURADO)

    # Prêmios organizados em 2 colunas amplas
    for i, premio in enumerate(premios):
        coluna = i // 7
        linha = i % 7

        caixa_x = 270 if coluna == 0 else 990
        caixa_y = 270 + (linha * 68)
        caixa_premio = Rect((caixa_x, caixa_y), (660, 58))

        if i == roleta_premio_atual:
            cor_fundo = COR_DOURADO
            cor_texto = (15, 23, 42)
            cor_borda = COR_TEXTO
        else:
            cor_fundo = COR_PAINEL
            cor_texto = COR_TEXTO
            cor_borda = None

        desenhar_card(caixa_premio, cor_fundo, cor_borda=cor_borda, raio=14, sombra=False)
        screen.draw.text(premio, center=caixa_premio.center, fontsize=28, color=cor_texto)

    # Ações da Roleta
    if roleta_estado == "aguardando":
        desenhar_card(botao_acao, COR_VERDE, cor_borda=COR_TEXTO, raio=28)
        screen.draw.text("GIRAR AGORA", center=botao_acao.center, fontsize=38, color=(15, 23, 42))
        
    elif roleta_estado == "girando":
        screen.draw.text("Girando...", center=(960, 870), fontsize=45, color=COR_CIANO)
        
    elif roleta_estado == "parou":
        nome_premio = premios[roleta_premio_atual]
        screen.draw.text(f"VOCÊ GANHOU: {nome_premio.upper()}!", center=(960, 800), fontsize=40, color=COR_VERDE)
        
        botao_voltar = Rect((660, 870), (600, 75))
        desenhar_card(botao_voltar, COR_DOURADO, cor_borda=COR_TEXTO, raio=24)
        screen.draw.text("VOLTAR AO MENU", center=botao_voltar.center, fontsize=32, color=(15, 23, 42))
        
        global botao_voltar_roleta 
        botao_voltar_roleta = botao_voltar

# ============================================================
# RENDERING
# ============================================================

def draw():
    if estado_jogo == "menu":
        desenhar_menu()
    elif estado_jogo == "quiz":
        desenhar_quiz()
    elif estado_jogo == "fim":
        desenhar_fim()
    elif estado_jogo == "roleta":
        desenhar_roleta()

# ============================================================
# EVENTOS DE TECLADO E CLIQUE (TOUCH SCREEN)
# ============================================================

def on_key_down(key):
    if key == keys.F11:
        alternar_tela()

def on_mouse_down(pos):
    global estado_jogo, roleta_estado

    if estado_jogo == "menu":
        if botao_comecar.collidepoint(pos):
            reiniciar_jogo()
            estado_jogo = "quiz"
        elif botao_tela.collidepoint(pos):
            alternar_tela()

    elif estado_jogo == "quiz":
        if not bloquear_respostas:
            for i, caixa in enumerate(botoes_opcoes):
                if caixa.collidepoint(pos):
                    verificar_resposta(i)

    elif estado_jogo == "fim":
        if botao_acao.collidepoint(pos):
            if acertos == 3:
                preparar_roleta()
                estado_jogo = "roleta"
            else:
                estado_jogo = "menu"
                
    elif estado_jogo == "roleta":
        if roleta_estado == "aguardando":
            if botao_acao.collidepoint(pos):
                roleta_estado = "girando"
        elif roleta_estado == "parou":
            if 'botao_voltar_roleta' in globals() and botao_voltar_roleta.collidepoint(pos):
                estado_jogo = "menu"

# ============================================================
# INICIAR O JOGO
# ============================================================

pgzrun.go()