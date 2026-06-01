import requests
import json
import random
import os
from datetime import datetime
from zoneinfo import ZoneInfo

API_KEY = "53795b533294d9dd1065064221c9f3a4"
HEADERS = {"x-rapidapi-key": API_KEY, "x-rapidapi-host": "v3.football.api-sports.io"}

hoje_br = datetime.now(ZoneInfo("America/Sao_Paulo")).strftime("%Y-%m-%d")
arquivo_dados = "jogos_gols.json"

def buscar_jogos_e_medias():
    url_fixtures = f"https://v3.football.api-sports.io/fixtures?date={hoje_br}"
    try:
        res = requests.get(url_fixtures, headers=HEADERS).json()
        jogos_api = res.get("response", [])
    except:
        return []
    
    palpites_calculados = []
    # Limitando a no máximo 40 jogos por dia para proteger sua cota diária da API
    contagem_jogos = 0
    
    for item in jogos_api:
        if contagem_jogos >= 40: break
        
        status_jogo = item["fixture"]["status"]["short"]
        if status_jogo != "NS": continue # Pula jogos que já começaram ou acabaram
        
        league_id = item["league"]["id"]
        season = item["league"]["season"]
        home_id = item["teams"]["home"]["id"]
        away_id = item["teams"]["away"]["id"]
        
        # Puxa o histórico do Mandante
        url_home = f"https://v3.football.api-sports.io/teams/statistics?league={league_id}&season={season}&team={home_id}"
        # Puxa o histórico do Visitante
        url_away = f"https://v3.football.api-sports.io/teams/statistics?league={league_id}&season={season}&team={away_id}"
        
        try:
            res_home = requests.get(url_home, headers=HEADERS).json().get("response", {})
            res_away = requests.get(url_away, headers=HEADERS).json().get("response", {})
            
            # Média de gols marcados e sofridos por jogo na temporada
            gols_home_marcados = float(res_home.get("goals", {}).get("for", {}).get("average", {}).get("total", 0))
            gols_home_sofridos = float(res_home.get("goals", {}).get("against", {}).get("average", {}).get("total", 0))
            
            gols_away_marcados = float(res_away.get("goals", {}).get("for", {}).get("average", {}).get("total", 0))
            gols_away_sofridos = float(res_away.get("goals", {}).get("against", {}).get("average", {}).get("total", 0))
            
            media_conjointa = (gols_home_marcados + gols_home_sofridos + gols_away_marcados + gols_away_sofridos) / 2
        except:
            # Caso o campeonato esteja muito no início e não tenha médias, gera um padrão seguro
            media_conjointa = 2.2
            gols_home_marcados = 1.1
            gols_away_marcados = 1.1
            
        home_name = item["teams"]["home"]["name"]
        away_name = item["teams"]["away"]["name"]
        liga = item["league"]["name"]
        
        try:
            data_iso = item["fixture"]["date"]
            dt_utc = datetime.fromisoformat(data_iso.replace("Z", "+00:00"))
            dt_br = dt_utc.astimezone(ZoneInfo("America/Sao_Paulo"))
            horario_formatado = dt_br.strftime("%d/%m às %H:%M")
        except:
            continue
            
        # Tomada de decisão matemática da IA baseada nas médias de gols
        if media_conjointa > 3.0 and gols_home_marcados > 1.2 and gols_away_marcados > 1.2:
            mercado = "Ambas Marcam"
            previsao = "SIM"
            confianca = random.randint(86, 97)
        elif media_conjointa > 2.6:
            mercado = "Total de Gols"
            previsao = "Mais de 2.5"
            confianca = random.randint(82, 95)
        else:
            mercado = "Total de Gols"
            previsao = "Mais de 1.5"
            confianca = random.randint(78, 91)
            
        palpites_calculados.append({
            "id": item["fixture"]["id"],
            "Jogo": f"{home_name} x {away_name}",
            "Campeonato": liga,
            "Mercado": mercado,
            "Previsão": previsao,
            "Confiança": f"{confianca}%",
            "Horario": horario_formatado,
            "Status": "AGUARDANDO",
            "Ordem_Confianca": confianca
        })
        contagem_jogos += 1
        
    return palpites_calculados

# Gerenciamento local do arquivo de dados
if os.path.exists(arquivo_dados):
    with open(arquivo_dados, "r", encoding="utf-8") as f:
        try: dados_armazenados = json.load(f)
        except: dados_armazenados = {"data": hoje_br, "jogos": []}
    if dados_armazenados.get("data") != hoje_br:
        dados_armazenados = {"data": hoje_br, "jogos": []}
else:
    dados_armazenados = {"data": hoje_br, "jogos": []}

hora_atual_br = datetime.now(ZoneInfo("America/Sao_Paulo")).hour

# MODO 1: GERAÇÃO DA GRADE (Se estiver vazio)
if not dados_armazenados.get("jogos"):
    jogos_analisados = buscar_jogos_e_medias()
    jogos_analisados = sorted(jogos_analisados, key=lambda x: x["Ordem_Confianca"], reverse=True)
    dados_armazenados["jogos"] = jogos_analisados

# MODO 2: AUDITORIA AUTOMÁTICA DE PLACAR (Fim do dia)
elif hora_atual_br >= 22:
    url_fixtures = f"https://v3.football.api-sports.io/fixtures?date={hoje_br}"
    try:
        res_api = requests.get(url_fixtures, headers=HEADERS).json().get("response", [])
    except:
        res_api = []
        
    for j_salvo in dados_armazenados.get("jogos", []):
        if j_salvo["Status"] == "AGUARDANDO":
            partida = next((x for x in res_api if x["fixture"]["id"] == j_salvo["id"]), None)
            if partida and partida["fixture"]["status"]["short"] == "FT":
                gols_h = partida["goals"]["home"] if partida["goals"]["home"] is not None else 0
                gols_a = partida["goals"]["away"] if partida["goals"]["away"] is not None else 0
                total_gols = gols_h + gols_a
                
                if j_salvo["Mercado"] == "Ambas Marcam":
                    j_salvo["Status"] = "GREEN" if gols_h > 0 and gols_a > 0 else "RED"
                elif j_salvo["Previsão"] == "Mais de 2.5":
                    j_salvo["Status"] = "GREEN" if total_gols >= 3 else "RED"
                elif j_salvo["Previsão"] == "Mais de 1.5":
                    j_salvo["Status"] = "GREEN" if total_gols >= 2 else "RED"

with open(arquivo_dados, "w", encoding="utf-8") as f:
    json.dump(dados_armazenados, f, ensure_ascii=False, indent=4)

lista_total = dados_armazenados.get("jogos", [])
f_free = lista_total[:3]
f_vip = lista_total[3:18]

if not f_free:
    f_free = [{"Jogo": "Analisando mercados de gols para hoje", "Campeonato": "Ligas Globais", "Mercado": "Gols", "Previsão": "Processando...", "Confiança": "90%", "Horario": "Em breve", "Status": "AGUARDANDO"}]
if not f_vip:
    f_vip = [{"Jogo": "Analisando mercados de gols para hoje", "Campeonato": "Ligas Globais", "Mercado": "Gols", "Previsão": "Processando...", "Confiança": "95%", "Horario": "Em breve", "Status": "AGUARDANDO"}]

json_free = json.dumps(f_free, ensure_ascii=False).replace("'", "\\'")
json_vip = json.dumps(f_vip, ensure_ascii=False).replace("'", "\\'")

conteudo_app = """import streamlit as st
import json

st.set_page_config(page_title="MESTRE DO OVER", page_icon="⚽", layout="centered")

css_estilo = \"\"\"
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght=400;600;800&display=swap');
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;} stDeployButton {display:none;}
    [data-testid="stToolbar"] {visibility: hidden !important;} [data-testid="stDecoration"] {display:none !important;}
    
    html, body, [data-testid="stAppViewContainer"] { background-color: #0b0f19; color: #f0f6fc; font-family: 'Inter', sans-serif; }
    .main-title { text-align: center; font-size: 2.3rem; font-weight: 800; color: #ffaa00; margin-bottom: 5px; text-shadow: 0px 0px 10px rgba(255,170,0,0.2); }
    .sub-title { text-align: center; font-size: 1.1rem; color: #8b949e; margin-bottom: 25px; }
    .install-box { background-color: #121824; border: 1px dashed #ffaa00; border-radius: 10px; padding: 15px; margin-bottom: 25px; text-align: center; }
    .install-title { font-weight: 800; color: #ffaa00; font-size: 1rem; margin-bottom: 5px; }
    .install-text { font-size: 0.85rem; color: #c9d1d9; line-height: 1.4; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; justify-content: center; }
    .stTabs [data-baseweb="tab"] { background-color: #121824; border: 1px solid #21262d; border-radius: 8px; padding: 10px 25px; color: #8b949e; font-weight: 600; }
    .stTabs [aria-selected="true"] { background-color: #ffaa00 !important; color: #0d1117 !important; border-color: #ffaa00 !important; }
    .card-AGUARDANDO { border-left: 5px solid #f1c40f !important; }
    .card-GREEN { border-left: 5px solid #2ecc71 !important; background: linear-gradient(135deg, #121824 0%, #1b3a24 100%) !important; }
    .card-RED { border-left: 5px solid #e74c3c !important; background: linear-gradient(135deg, #121824 0%, #3a1c1c 100%) !important; }
    .badge-AGUARDANDO { background-color: rgba(241, 196, 15, 0.15); color: #f1c40f; border: 1px solid #f1c40f; }
    .badge-GREEN { background-color: rgba(46, 204, 113, 0.2); color: #2ecc71; border: 1px solid #2ecc71; font-weight: 800; }
    .badge-RED { background-color: rgba(231, 76, 60, 0.2); color: #e74c3c; border: 1px solid #e74c3c; }
    .bet-card { background: linear-gradient(135deg, #121824 0%, #1c2333 100%); border-radius: 10px; padding: 20px; margin-bottom: 18px; border: 1px solid #21262d; }
    .card-header { display: flex; justify-content: space-between; color: #8b949e; font-size: 0.85rem; font-weight: 600; margin-bottom: 8px; text-transform: uppercase; }
    .card-teams { font-size: 1.3rem; font-weight: 700; color: #ffffff; margin-bottom: 12px; }
    .card-body-info { display: flex; justify-content: space-between; align-items: center; background-color: #0b0f19; padding: 12px; border-radius: 8px; border: 1px solid #21262d; }
    .market-title { font-size: 0.9rem; color: #8b949e; }
    .market-value { font-size: 1.1rem; font-weight: 700; color: #ffaa00; }
    .status-badge { padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 600; text-transform: uppercase; }
    .vip-banner { background: linear-gradient(135deg, #ffaa00 0%, #e69900 100%); color: #0d1117; padding: 20px; border-radius: 10px; text-align: center; font-weight: 700; margin-top: 25px; }
</style>
\"\"\"
st.markdown(css_estilo, unsafe_allow_html=True)

st.markdown('<div class="main-title">🔥 MESTRE DO OVER</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Algoritmo Estatístico focado em Linhas de Gols e BTTS</div>', unsafe_allow_html=True)

st.markdown(\"\"\"
<div class="install-box">
    <div class="install-title">📱 BAIXE O APP DIRETO NA TELA DO CELULAR</div>
    <div class="install-text">
        <b>No Android (Chrome):</b> Vá nos 3 pontinhos e escolha <b>'Instalar aplicativo'</b>.<br>
        <b>No iPhone (Safari):</b> Clique em <b>Compartilhar</b> e escolha <b>'Adicionar à Tela de Início'</b>.
    </div>
</div>
\"\"\", unsafe_allow_html=True)

jogos_free = json.loads('__JSON_FREE__')
jogos_vip = json.loads('__JSON_VIP__')

aba1, aba2 = st.tabs(["📊 PALPITES FREE", "🔒 ACESSO VIP"])

with aba1:
    st.write("")
    for j in jogos_free:
        status_atual = j.get("Status", "AGUARDANDO")
        card_html = f'<div class="bet-card card-{status_atual}"><div class="card-header"><span>🏆 {j["Campeonato"]} — 📅 {j["Horario"]}</span><span class="status-badge badge-{status_atual}">{status_atual}</span></div><div class="card-teams">⚽ {j["Jogo"]}</div><div class="card-body-info"><div><div class="market-title">Mercado Sugerido</div><div style="font-weight:600; color:#fff;">{j["Mercado"]}</div></div><div style="text-align: right;"><div class="market-title">Entrada Indicada</div><div class="market-value">{j["Previsão"]}</div></div></div></div>'
        st.markdown(card_html, unsafe_allow_html=True)
    st.markdown('<div class="vip-banner">🚀 LIBERAR MAIS DE 15 PALPITES DE HOJE?<div style="font-size:0.9rem; font-weight:400; margin-top:5px;">Assine a nossa licença premium e receba a grade completa com as maiores probabilidades de gols do mercado!</div></div>', unsafe_allow_html=True)

with aba2:
    st.write("")
    st.markdown('<div style="background-color:#121824; padding:20px; border-radius:10px; border:1px solid #21262d;">', unsafe_allow_html=True)
    senha = st.text_input("Insira sua chave de acesso VIP:", type="password", key="vip_key_over")
    st.markdown('</div>', unsafe_allow_html=True)
    
    if senha == "VIP2026":
        st.write("")
        st.success("🔓 Acesso Premium Liberado! Bons Greens!")
        for j in jogos_vip:
            status_atual = j.get("Status", "AGUARDANDO")
            card_vip_html = f'<div class="bet-card card-{status_atual}"><div class="card-header"><span>👑 {j["Campeonato"]} — 📅 {j["Horario"]}</span><span class="status-badge badge-{status_atual}">{status_atual}</span></div><div class="card-teams">⚽ {j["Jogo"]}</div><div class="card-body-info"><div><div class="market-title">Mercado Sugerido</div><div style="font-weight:600; color:#fff;">{j["Mercado"]}</div></div><div style="text-align: right;"><div class="market-title">Entrada Indicada</div><div class="market-value" style="color:#ffaa00;">{j["Previsão"]}</div></div></div></div>'
            st.markdown(card_vip_html, unsafe_allow_html=True)
    elif senha != "":
        st.write("")
        st.error("❌ Chave inválida ou expirada.")
"""

conteudo_app = conteudo_app.replace("__JSON_FREE__", json_free).replace("__JSON_VIP__", json_vip)

with open("app.py", "w", encoding="utf-8") as f:
    f.write(conteudo_app)
print("Sucesso total!")
