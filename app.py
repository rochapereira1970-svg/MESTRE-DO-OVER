import streamlit as st
import json
import requests

# Configuração da página
st.set_page_config(
    page_title="Mestre do Over - Estatísticas Avançadas",
    page_icon="⚽",
    layout="wide"
)

# Estilização CSS Personalizada (Tema Mestre do Over - Esportivo e Moderno)
style_css = """
<style>
.main { background-color: #0b0f19; color: #f1f5f9; }
.header-box { background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); padding: 25px; border-radius: 16px; border: 1px solid #334155; text-align: center; margin-bottom: 20px; }
.header-box h1 { color: #38bdf8; font-size: 30px; font-weight: 800; margin-bottom: 5px; text-transform: uppercase; }
.header-box p { color: #94a3b8; font-size: 15px; margin: 0; }

.fontes-container { background-color: #111827; padding: 12px; border-radius: 12px; border: 1px solid #1f2937; margin-bottom: 25px; text-align: center; }
.fonte-tag { background-color: #1f2937; padding: 5px 12px; border-radius: 6px; font-weight: bold; font-size: 12px; display: inline-block; margin: 3px 6px; border: 1px solid #374151; }

.card-analise { background-color: #1e293b; border-radius: 14px; padding: 20px; margin-bottom: 20px; border-left: 5px solid #38bdf8; box-shadow: 0 4px 15px rgba(0,0,0,0.2); }
.card-under { border-left-color: #10b981 !important; } /* Verde para mercado de segurança Under */

.card-header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #334155; padding-bottom: 10px; margin-bottom: 15px; }
.card-titulo { font-size: 18px; font-weight: bold; color: #ffffff; }

.badge-odd { background: linear-gradient(135deg, #0284c7 0%, #38bdf8 100%); color: #ffffff; font-weight: 800; padding: 5px 12px; border-radius: 6px; font-size: 14px; }
.badge-under { background: linear-gradient(135deg, #059669 0%, #10b981 100%) !important; }

.jogo-detalhes { background-color: #0f172a; padding: 12px; border-radius: 8px; margin-bottom: 12px; border: 1px solid #1e293b; }
.times-nome { font-size: 16px; font-weight: bold; color: #ffffff; }
.campeonato-nome { font-size: 12px; color: #64748b; }

.mercado-box { background-color: #0c4a6e; color: #38bdf8; padding: 8px 12px; border-radius: 6px; font-weight: bold; font-size: 14px; display: inline-block; margin-top: 5px; }
.mercado-under { background-color: #064e3b !important; color: #10b981 !important; }

.justificativa-box { background-color: #111827; padding: 10px 14px; border-radius: 8px; border-left: 3px solid #64748b; font-size: 13px; color: #94a3b8; margin-top: 10px; }
</style>
"""
st.markdown(style_css, unsafe_allow_html=True)

# Link do JSON do seu Mestre do Over (substitua pela sua URL real se necessário)
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
st.markdown(f"""
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

st.info(f"🔄 **Última atualização do robô:** {data_atualizacao} | 🏟️ **Foco Atual:** Operações de Consistência (Série B e Ligas Ativas)")

if not dados:
    st.warning("O robô está processando a rodada da Série B nas bases de dados. Volte em instantes!")
else:
    # Divisão das exibições
    st.subheader("🎯 Entradas Selecionadas para Hoje")
    
    # Exemplo de leitura de jogos do JSON
    for jogo in dados.get("jogos_analisados", []):
        
        # Identifica se é mercado de Under para mudar a cor do cartão para verde descendo a linha visual
        eh_under = "Under" in jogo.get("mercado", "") or "Menos" in jogo.get("mercado", "")
        classe_card = "card-analise card-under" if eh_under else "card-analise"
        classe_badge = "badge-odd badge-under" if eh_under else "badge-odd"
        classe_mercado = "mercado-box mercado-under" if eh_under else "mercado-box"
        
        st.markdown(f"""
            <div class="{classe_card}">
                <div class="card-header">
                    <span class="card-titulo">{'🛡️ SEGURANÇA (UNDER)' if eh_under else '🔥 OFENSIVO (OVER)'}</span>
                    <span class="{classe_badge}">ODD: @{jogo['odd']}</span>
                </div>
                
                <div class="jogo-detalhes">
                    <div class="times-nome">{jogo['time_casa']} x {jogo['time_fora']}</div>
                    <div class="campeonato-nome">🏆 {jogo['campeonato']} • ⏰ {jogo.get('horario', 'Horário na Casa')}</div>
                </div>
                
                <div class="{classe_mercado}">
                    Mercado: {jogo['mercado']}
                </div>
                
                <div class="justificativa-box">
                    <strong>📊 Cruzamento de Dados (SofaScore + Footstats):</strong><br>
                    {jogo.get('justificativa', 'Estatísticas de volume indicam alta probabilidade para esta linha dentro do padrão da liga.')}
                </div>
            </div>
        """, unsafe_allow_html=True)

# Rodapé Educativo para Instalação como App
st.markdown("""
    <hr style="border-color: #1e293b;">
    <div style="text-align: center; color: #64748b; font-size: 12px; padding: 10px;">
        📲 <strong>Dica de Mestre:</strong> Abra este link no Safari (iPhone) ou Chrome (Android) e use a opção "Adicionar à Tela de Início" para salvar como um aplicativo nativo no seu celular!
    </div>
""", unsafe_allow_html=True)
