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

# Estilização CSS Personalizada (Ultra Premium e Focada em Conversão)
style_css = """
<style>
.main { background-color: #0b0f19; color: #f1f5f9; }
.header-box { background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); padding: 25px; border-radius: 16px; border: 1px solid #334155; text-align: center; margin-bottom: 20px; }
.header-box h1 { color: #38bdf8; font-size: 30px; font-weight: 800; margin-bottom: 5px; text-transform: uppercase; }
.header-box p { color: #94a3b8; font-size: 15px; margin: 0; }

/* Vitrine de Resultados e EV+ */
.painel-metricas { display: flex; justify-content: center; gap: 15px; margin-bottom: 20px; flex-wrap: wrap; }
.metrica-card { background-color: #111827; border: 1px solid #1f2937; padding: 12px 25px; border-radius: 12px; text-align: center; min-width: 150px; }
.metrica-valor { font-size: 20px; font-weight: 900; color: #10b981; }
.metrica-label { font-size: 11px; color: #64748b; text-transform: uppercase; font-weight: bold; margin-top: 2px; }

/* Selos dos Mercados Operados */
.fontes-container { background-color: #111827; padding: 12px; border-radius: 12px; border: 1px solid #1f2937; margin-bottom: 20px; text-align: center; }
.fonte-tag { background-color: #1f2937; padding: 5px 12px; border-radius: 6px; font-weight: bold; font-size: 12px; display: inline-block; margin: 3px 6px; border: 1px solid #374151; }

/* Banner de Convite VIP Principal */
.banner-vip-principal { background: linear-gradient(135deg, #1e1b4b 0%, #311042 100%); border: 1px solid #581c87; padding: 20px; border-radius: 14px; text-align: center; margin-bottom: 25px; box-shadow: 0 10px 25px rgba(0,0,0,0.3); }
.banner-vip-principal h3 { color: #f59e0b; margin: 0 0 5px 0; font-size: 18px; font-weight: bold; text-transform: uppercase; }
.banner-vip-principal p { color: #cbd5e1; margin: 0 0 15px 0; font-size: 13px; }
.btn-principal-vip { background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); color: #000000 !important; font-weight: 900; padding: 12px 30px; border-radius: 8px; text-decoration: none; display: inline-block; text-transform: uppercase; font-size: 14px; box-shadow: 0 4px 15px rgba(245,158,11,0.4); transition: 0.2s; }
.btn-principal-vip:hover { transform: scale(1.03); }

.aviso-horario-box { background-color: #1e293b; padding: 10px; border-radius: 10px; border: 1px solid #334155; text-align: center; margin-bottom: 25px; }
.aviso-texto { color: #38bdf8; font-weight: bold; font-size: 12px; text-transform: uppercase; }

/* Abas */
.stTabs [data-baseweb="tab-list"] { gap: 10px; justify-content: center; }
.stTabs [data-baseweb="tab"] { background-color: #1e293b; color: #94a3b8; border-radius: 8px 8px 0px 0px; padding: 10px 25px; font-weight: bold; border: 1px solid #334155; }
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

/* Card VIP Bloqueado */
.card-vip-bloqueado { background-color: #131926; border-radius: 14px; padding: 20px; margin-bottom: 20px; border-left: 5px solid #eab308; border: 1px dashed #eab308; opacity: 0.9; position: relative; }
.blur-text { filter: blur(5px); user-select: none; pointer-events: none; }
.btn-vip-container { text-align: center; margin-top: 15px; }
.btn-vip-link { background: linear-gradient(135deg, #eab308 0%, #ca8a04 100%); color: #000000 !important; font-weight: bold; padding: 10px 24px; border-radius: 8px; text-decoration: none; display: inline-block; font-size: 13px; text-transform: uppercase; }
</style>
