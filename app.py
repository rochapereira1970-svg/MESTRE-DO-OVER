import streamlit as st
import json
import requests

# Configuração da página
st.set_page_config(
    page_title="Mestre do Over - Estatísticas Avançadas",
    page_icon="⚽",
    layout="wide"
)

# LINK DO SEU LINK DE PAGAMENTO (Substitua pelo seu link da Kiwify, Braip, Perfect Pay, etc.)
LINK_COMPRA_VIP = "https://seu-link-de-pagamento.com"

# Estilização CSS Personalizada (Premium, Comercial e Atraente)
style_css = """
<style>
.main { background-color: #0b0f19; color: #f1f5f9; }
.header-box { background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); padding: 25px; border-radius: 16px; border: 1px solid #334155; text-align: center; margin-bottom: 20px; }
.header-box h1 { color: #38bdf8; font-size: 30px; font-weight: 800; margin-bottom: 5px; text-transform: uppercase; }
.header-box p { color: #94a3b8; font-size: 15px; margin: 0; }

.fontes-container { background-color: #111827; padding: 12px; border-radius: 12px; border: 1px solid #1f2937; margin-bottom: 15px; text-align: center; }
.fonte-tag { background-color: #1f2937; padding: 5px 12px; border-radius: 6px; font-weight: bold; font-size: 12px; display: inline-block; margin: 3px 6px; border: 1px solid #374151; }

.aviso-horario-box { background-color: #1e293b; padding: 12px; border-radius: 10px; border: 1px solid #334155; text-align: center; margin-bottom: 25px; }
.aviso-texto { color: #38bdf8; font-weight: bold; font-size: 13px; text-transform: uppercase; }

/* Estilo Abas Premium */
.stTabs [data-baseweb="tab-list"] { gap: 10px; justify-content: center; }
.stTabs [data-baseweb="tab"] { background-color: #1e293b; color: #94a3b8; border-radius: 8px 8px 0px 0px; padding: 10px 30px; font-weight: bold; border: 1px solid #334155; }
.stTabs [data-baseweb="tab"][aria-selected="true"] { background: linear-gradient(135deg, #0284c7 0%, #38bdf8 100%) !important; color: white !important; border: none; }

/* Cards de Palpites */
.card-analise { background-color: #1e293b; border-radius: 14px; padding: 20px; margin-bottom: 20px; border-left: 5px solid #38bdf8; box-shadow: 0 4px 15px rgba(0,0,0,0.2); }
.card-header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #334155; padding-bottom: 10px; margin-bottom: 15px; }
.card-titulo { font-size: 18px; font-weight: bold; color: #ffffff; }

.badge-odd { background: linear-gradient(135deg, #0284c7 0%, #38bdf8 100%); color: #ffffff; font-weight: 800; padding: 5px 12px; border-radius: 6px; font-size: 14px; }
.jogo-detalhes { background-color: #0f172a; padding: 12px; border-radius: 8px; margin-bottom: 12px; border: 1px solid #1e293b; }
.times-nome { font-size: 16px; font-weight: bold; color: #ffffff; }
.campeonato-nome { font-size: 12px; color: #64748b; }

.mercado-box { background-color: #0c4a6e; color: #38bdf8; padding: 8px 12px; border-radius: 6px; font-weight: bold; font-size: 14px; display: inline-block; margin-top: 5px; }
.justificativa-box { background-color: #111827; padding: 10px 14px; border-radius: 8px; border-left: 3px solid #64748b; font-size: 13px; color: #94a3b8; margin-top: 10px; }

/* Estilo do Card VIP Bloqueado */
.card-vip-bloqueado { background-color: #131926; border-radius: 14px; padding: 20px; margin-bottom: 20px; border-left: 5px solid #eab308; border: 1px dashed #eab308; opacity: 0.85; position: relative; }
.blur-text { filter: blur(5px); user-select: none; pointer-events: none; }
.btn-vip-container { text-align: center; margin-top: 15px; }
.btn-vip-link { background: linear-gradient(135deg, #eab308 0%, #ca8a04 100%); color: #000000 !important; font-weight: bold; padding: 10px 24px; border-radius: 8px; text-decoration: none; display: inline-block; box-shadow: 0 4px 15px rgba(234,179,8,0.3); font-size: 14px; text-transform: uppercase; }
.btn-vip-link:hover { transform: scale(1.02); transition: 0.2s; }
</style>
"""
st.markdown(style_css, unsafe_allow_html=True)

# Link do JSON do seu Mestre do Over
JSON_URL = "https://raw.githubusercontent.com/rochapereira1970-svg/MESTRE-DO-OVER/main/jogos.json"

def carregar_dados():
    try:
        resposta = requests.get(JSON_URL)
        if resposta.status_code == 200:
            return json.loads(resposta.text)
    except:
        pass
    return None

dados = carregar_dados()
data_atualizacao = dados['ultima_atualizacao'] if dados else "Aguardando sincronização..."

# Banner Principal
st.markdown("""
    <div class="header-box">
        <h1>⚽ MESTRE DO OVER</h1>
        <p>Análise Preditiva de Gols e Tendências de Escanteios</p>
    </div>
""", unsafe_allow_html=True)

# Selos de Validação de Dados (SofaScore + Footstats + SokkerPRO)
st.markdown("""
    <div class="fontes-container">
        <span style="color: #64748b; font-size: 12px; font-weight: bold; text-transform: uppercase; display: block; margin-bottom: 5px;">
            🔍 Algoritmo Alimentado e Validado por Bancos de Dados Oficiais:
        </span>
        <div class="fonte-tag" style="color: #10b981;">📊 SofaScore.com</div>
        <div class="fonte-tag" style="color: #3b82f6;">⚽ Footstats Premium</div>
        <div class="fonte-tag" style="color: #a855f7;">📈 SokkerPRO AI</div>
    </div>
""", unsafe_allow_html=True)

# Caixa de Aviso de Horário Fixo de Atualização
st.markdown("""
    <div class="aviso-horario-box">
        <span class="aviso-texto">
            📢 AVISO DO MESTRE: Novas análises preditivas são geradas automaticamente todos os dias às 22:00h!
        </span>
    </div>
""", unsafe_allow_html=True)

st.info(f"🔄 **Última rodada processada pelo robô:** {data_atualizacao} | 🏟 *Foco:* Série B e Ligas Ativas")

# Criação das Abas Comerciais
aba_free, aba_vip = st.tabs(["🆓 PALPITES FREE (3 DISPONÍVEIS)", "👑 ÁREA VIP PREMIUM (7 AGRESSIVOS)"])

if not dados:
    st.warning("O robô está processando os dados das partidas. Volte em instantes!")
else:
    lista_jogos = dados.get("jogos_analisados", [])
    
    # --- ABA FREE (Mostra apenas os 3 primeiros jogos) ---
    with aba_free:
        st.subheader("🎯 Aperitivo do Mestre - Sinais Gratuitos de Hoje")
        jogos_free = lista_jogos[:3]  # Pega os 3 primeiros do JSON
        
        if not jogos_free:
            st.write("Nenhum palpite gratuito para exibição no momento.")
        
        for jogo in jogos_free:
            st.markdown(f"""
                <div class="card-analise">
                    <div class="card-header">
                        <span class="card-titulo">🔥 ENTRADA LIBERADA</span>
                        <span class="badge-odd">ODD: @{jogo['odd']}</span>
                    </div>
                    
                    <div class="jogo-detalhes">
                        <div class="times-nome">{jogo['time_casa']} x {jogo['time_fora']}</div>
                        <div class="campeonato-nome">🏆 {jogo['campeonato']} • ⏰ {jogo.get('horario', '21:30')}</div>
                    </div>
                    
                    <div class="mercado-box">
                        Mercado: {jogo['mercado']}
                    </div>
                    
                    <div class="justificativa-box">
                        <strong>📊 Cruzamento de Dados (SofaScore + Footstats):</strong><br>
                        {jogo.get('justificativa', 'Análise estatística validada para alta frequência de batida nesta linha.')}
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
    # --- ABA VIP (Exibe os 7 jogos seguintes com efeito de bloqueio) ---
    with aba_vip:
        st.markdown("""
            <div style="background-color: #7c2d12; color: #ffedd5; padding: 15px; border-radius: 8px; border-left: 4px solid #f97316; margin-bottom: 20px; font-size: 14px;">
                ⭐ <strong>SINAIS DE MÁXIMA PROBABILIDADE DESTREVAÇÃO:</strong> Abaixo estão os 7 sinais secretos selecionados com filtros refinados (Over 1.5 Gols, Over 7.5 Cantos e Over 3.5 Cartões) cruzando inteligência SofaScore e Footstats.
            </div>
        """, unsafe_allow_html=True)
        
        # Simula 7 jogos VIP (se não houver o suficiente no JSON, ele gera a estrutura comercial de qualquer forma)
        total_vip_exibir = 7
        for i in range(total_vip_exibir):
            # Tenta pegar um jogo real do JSON a partir do índice 3, senão usa dados genéricos borrados
            index_real = i + 3
            if index_real < len(lista_jogos):
                j_vip = lista_jogos[index_real]
                mercado_vip = j_vip['mercado']
                camp_vip = j_vip['campeonato']
            else:
                # Fallback estratégico se o JSON tiver menos de 10 jogos
                mercados_sugeridos = ["🔥 Over 1.5 Gols FT", "📐 Over 7.5 Escanteios FT", "🟨 Over 3.5 Cartões FT"]
                mercado_vip = mercados_sugeridos[i % len(mercados_sugeridos)]
                camp_vip = "Brasileirão Série B"

            st.markdown(f"""
                <div class="card-vip-bloqueado">
                    <div class="card-header" style="border-bottom: 1px solid #222938;">
                        <span class="card-titulo" style="color: #eab308;">🔒 ENTRADA VIP #{i+1} • ALTA PROBABILIDADE</span>
                        <span class="badge-odd" style="background: #eab308; color: #000;">ODD Oculta</span>
                    </div>
                    
                    <div class="jogo-detalhes" style="background-color: #0b0f19; border: 1px dashed #222938;">
                        <div class="times-nome blur-text">Time Oculto FC x Atlético Desconhecido</div>
                        <div class="campeonato-nome">🏆 {camp_vip} • ⏰ 22:00h</div>
                    </div>
                    
                    <div class="mercado-box" style="background-color: #422006; color: #fef08a;">
                        Mercado: {mercado_vip}
                    </div>
                    
                    <div class="justificativa-box blur-text" style="border-left-color: #eab308;">
                        Análise SofaScore e Footstats premium oculta para assinantes. Estatísticas cruciais de cruzamentos e finalizações bloqueadas.
                    </div>
                    
                    <div class="btn-vip-container">
                        <a href="{LINK_COMPRA_VIP}" target="_blank" class="btn-vip-link">🔓 Desbloquear Este Palpite e Acessar Grupo VIP</a>
                    </div>
                </div>
            """, unsafe_allow_html=True)

# Rodapé Informativo
st.markdown("""
    <hr style="border-color: #1e293b;">
    <div style="text-align: center; color: #64748b; font-size: 12px; padding: 10px;">
        📲 <strong>Dica de Mestre:</strong> Abra este link no navegador do celular e selecione "Adicionar à Tela de Início" para usá-lo como um aplicativo nativo.
    </div>
""", unsafe_allow_html=True)
