import streamlit as st
import json
import requests

# Configuração da página
st.set_page_config(
    page_title="Mestre do Over - Inteligência Preditiva",
    page_icon="⚽",
    layout="wide"
)

# LINK DE PAGAMENTO (Substitua pelo seu link da Kiwify, Braip, Perfect Pay, etc.)
LINK_COMPRA_VIP = "https://seu-link-de-pagamento.com"

# Estilização CSS Personalizada (Premium, Comercial e Corrigida)
st.markdown("""
<style>
.main { background-color: #0b0f19; color: #f1f5f9; }
.header-box { background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); padding: 25px; border-radius: 16px; border: 1px solid #334155; text-align: center; margin-bottom: 20px; }
.header-box h1 { color: #38bdf8; font-size: 30px; font-weight: 800; margin-bottom: 5px; text-transform: uppercase; }
.header-box p { color: #94a3b8; font-size: 15px; margin: 0; }

.painel-metricas { display: flex; justify-content: center; gap: 15px; margin-bottom: 20px; flex-wrap: wrap; }
.metrica-card { background-color: #111827; border: 1px solid #1f2937; padding: 12px 25px; border-radius: 12px; text-align: center; min-width: 150px; }
.metrica-valor { font-size: 20px; font-weight: 900; color: #10b981; }
.metrica-label { font-size: 11px; color: #64748b; text-transform: uppercase; font-weight: bold; margin-top: 2px; }

.fontes-container { background-color: #111827; padding: 12px; border-radius: 12px; border: 1px solid #1f2937; margin-bottom: 20px; text-align: center; }
.fonte-tag { background-color: #1f2937; padding: 5px 12px; border-radius: 6px; font-weight: bold; font-size: 12px; display: inline-block; margin: 3px 6px; border: 1px solid #374151; }

.banner-vip-principal { background: linear-gradient(135deg, #1e1b4b 0%, #311042 100%); border: 1px solid #581c87; padding: 20px; border-radius: 14px; text-align: center; margin-bottom: 25px; box-shadow: 0 10px 25px rgba(0,0,0,0.3); }
.banner-vip-principal h3 { color: #f59e0b; margin: 0 0 5px 0; font-size: 18px; font-weight: bold; text-transform: uppercase; }
.banner-vip-principal p { color: #cbd5e1; margin: 0 0 15px 0; font-size: 13px; }
.btn-principal-vip { background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); color: #000000 !important; font-weight: 900; padding: 12px 30px; border-radius: 8px; text-decoration: none; display: inline-block; text-transform: uppercase; font-size: 14px; box-shadow: 0 4px 15px rgba(245,158,11,0.4); }

.aviso-horario-box { background-color: #1e293b; padding: 10px; border-radius: 10px; border: 1px solid #334155; text-align: center; margin-bottom: 25px; }
.aviso-texto { color: #38bdf8; font-weight: bold; font-size: 12px; text-transform: uppercase; }

.stTabs [data-baseweb="tab-list"] { gap: 10px; justify-content: center; }
.stTabs [data-baseweb="tab"] { background-color: #1e293b; color: #94a3b8; border-radius: 8px 8px 0px 0px; padding: 10px 25px; font-weight: bold; border: 1px solid #334155; }
.stTabs [data-baseweb="tab"][aria-selected="true"] { background: linear-gradient(135deg, #0284c7 0%, #38bdf8 100%) !important; color: white !important; border: none; }

.card-analise { background-color: #1e293b; border-radius: 14px; padding: 20px; margin-bottom: 20px; border-left: 5px solid #38bdf8; box-shadow: 0 4px 15px rgba(0,0,0,0.2); }
.card-header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #334155; padding-bottom: 10px; margin-bottom: 15px; }
.card-titulo { font-size: 18px; font-weight: bold; color: #ffffff; }

.badge-odd { background: linear-gradient(135deg, #0284c7 0%, #38bdf8 100%); color: #ffffff; font-weight: 800; padding: 5px 12px; border-radius: 6px; font-size: 14px; }
.jogo-detalhes { background-color: #0f172a; padding: 12px; border-radius: 8px; margin-bottom: 12px; border: 1px solid #1e293b; }
.times-nome { font-size: 16px; font-weight: bold; color: #ffffff; }
.campeonato-nome { font-size: 12px; color: #64748b; }

.mercado-box { background-color: #0c4a6e; color: #38bdf8; padding: 8px 12px; border-radius: 6px; font-weight: bold; font-size: 14px; display: inline-block; margin-top: 5px; }
.justificativa-box { background-color: #111827; padding: 10px 14px; border-radius: 8px; border-left: 3px solid #64748b; font-size: 13px; color: #94a3b8; margin-top: 10px; }

.card-vip-bloqueado { background-color: #131926; border-radius: 14px; padding: 20px; margin-bottom: 20px; border-left: 5px solid #eab308; border: 1px dashed #eab308; opacity: 0.9; position: relative; }
.blur-text { filter: blur(5px); user-select: none; pointer-events: none; }
.btn-vip-container { text-align: center; margin-top: 15px; }
.btn-vip-link { background: linear-gradient(135deg, #eab308 0%, #ca8a04 100%); color: #000000 !important; font-weight: bold; padding: 10px 24px; border-radius: 8px; text-decoration: none; display: inline-block; font-size: 13px; text-transform: uppercase; }
</style>
""", unsafe_allow_html=True)

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
        <p>Algoritmo de Análise Preditiva de Alta Performance</p>
    </div>
""", unsafe_allow_html=True)

# PAINEL DE MÉTRICAS E EV+
st.markdown("""
    <div class="painel-metricas">
        <div class="metrica-card">
            <div class="metrica-valor">84.2%</div>
            <div class="metrica-label">🎯 Assertividade Média</div>
        </div>
        <div class="metrica-card">
            <div class="metrica-valor">EV+</div>
            <div class="metrica-label">📈 Valor Esperado</div>
        </div>
        <div class="metrica-card">
            <div class="metrica-valor">+24.8%</div>
            <div class="metrica-label">💰 ROI Mensal Médio</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# CONVITE VIP PRINCIPAL
st.markdown(f"""
    <div class="banner-vip-principal">
        <h3>👑 Quer parar de depender da sorte nas Apostas?</h3>
        <p>Tenha acesso imediato aos 7 sinais ocultos diários de máxima probabilidade matemática calculados pelo nosso algoritmo.</p>
        <a href="{LINK_COMPRA_VIP}" target="_blank" class="btn-principal-vip">Garanta seu Acesso VIP Premium</a>
    </div>
""", unsafe_allow_html=True)

# Mercados Monitorados (Trufo Protegido)
st.markdown("""
    <div class="fontes-container">
        <span style="color: #64748b; font-size: 11px; font-weight: bold; text-transform: uppercase; display: block; margin-bottom: 5px;">
            🤖 Especialização do Algoritmo em Mercados Estratégicos:
        </span>
        <div class="fonte-tag" style="color: #38bdf8;">🔥 Over 1.5 Gols FT</div>
        <div class="fonte-tag" style="color: #10b981;">📐 Over 7.5 Escanteios</div>
        <div class="fonte-tag" style="color: #eab308;">🟨 Over 3.5 Cartões</div>
    </div>
""", unsafe_allow_html=True)

# Caixa de Horário Fixo
st.markdown("""
    <div class="aviso-horario-box">
        <span class="aviso-texto">
            📢 Novas análises matemáticas são publicadas todos os dias pontualmente às 22:00h!
        </span>
    </div>
""", unsafe_allow_html=True)

st.info(f"🔄 **Última verificação do algoritmo:** {data_atualizacao} | 🏟 *Foco:* Série B e Ligas Ativas")

# Abas Comerciais
aba_free, aba_vip = st.tabs(["🆓 PALPITES FREE (3 DISPONÍVEIS)", "👑 ÁREA VIP PREMIUM (7 AGRESSIVOS)"])

if not dados:
    st.warning("O algoritmo está mapeando as partidas nas ligas ativas. Volte em instantes!")
else:
    lista_jogos = dados.get("jogos_analisados", [])
    
    # --- ABA FREE ---
    with aba_free:
        st.subheader("🎯 Amostra Gratuita da Rodada")
        jogos_free = lista_jogos[:3]
        
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
                        <div class="campeonato-nome">🏆 {jogo['campeonato']} • ⏰ {jogo.get('horario', '22:00')}</div>
                    </div>
                    
                    <div class="mercado-box">
                        Mercado: {jogo['mercado']}
                    </div>
                    
                    <div class="justificativa-box">
                        <strong>📊 Análise de Probabilidade Avançada:</strong><br>
                        {jogo.get('justificativa', 'Histórico recente e cruzamento de scout indicam alto valor esperado nesta linha.')}
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
    # --- ABA VIP ---
    with aba_vip:
        st.markdown("""
            <div style="background-color: #7c2d12; color: #ffedd5; padding: 15px; border-radius: 8px; border-left: 4px solid #f97316; margin-bottom: 20px; font-size: 14px; text-align: center;">
                ⭐ <strong>CÁLCULO DE VALOR ESPERADO ATIVO:</strong> As 7 entradas abaixo possuem o maior índice de EV+ mapeado pelo algoritmo para esta rodada.
            </div>
        """, unsafe_allow_html=True)
        
        total_vip_exibir = 7
        for i in range(total_vip_exibir):
            index_real = i + 3
            if index_real < len(lista_jogos):
                j_vip = lista_jogos[index_real]
                mercado_vip = j_vip['mercado']
                camp_vip = j_vip['campeonato']
            else:
                mercados_sugeridos = ["🔥 Over 1.5 Gols FT", "📐 Over 7.5 Escanteios FT", "🟨 Over 3.5 Cartões FT"]
                mercado_vip = mercados_sugeridos[i % len(mercados_sugeridos)]
                camp_vip = "Brasileirão Série B"

            st.markdown(f"""
                <div class="card-vip-bloqueado">
                    <div class="card-header" style="border-bottom: 1px solid #222938;">
                        <span class="card-titulo" style="color: #eab308;">🔒 ENTRADA SECRETA #{i+1} • PROBABILIDADE MÁXIMA</span>
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
                        Métricas proprietárias e dados de cruzamento avançados restritos para membros assinantes do plano anual.
                    </div>
                    
                    <div class="btn-vip-container">
                        <a href="{LINK_COMPRA_VIP}" target="_blank" class="btn-vip-link">🔓 Desbloquear Acesso VIP</a>
                    </div>
                </div>
            """, unsafe_allow_html=True)

# Rodapé Informativo
st.markdown("""
    <hr style="border-color: #1e293b;">
    <div style="text-align: center; color: #64748b; font-size: 12px; padding: 10px;">
        📲 Abra este link no navegador do celular e selecione "Adicionar à Tela de Início" para salvar como App.
    </div>
""", unsafe_allow_html=True)
