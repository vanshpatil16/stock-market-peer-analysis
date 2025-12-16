import streamlit as st
import yfinance as yf
import pandas as pd
import altair as alt
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import requests
import time

st.set_page_config(
    page_title="Indian Stock Peer Analysis Dashboard",
    page_icon=":chart_with_upwards_trend:",
    layout="wide",
)

"""
# :material/query_stats: Indian Stock Peer Analysis

Easily compare Indian stocks (NSE/BSE) against others in their peer group.
"""

# Display marquee with all stocks news at the top (after functions are defined below)
# This will be rendered after helper functions are loaded

""  # Add some space.

cols = st.columns([1, 3])
# Will declare right cell later to avoid showing it when no data.

STOCKS = [
    # Large Cap Stocks
    "RELIANCE.NS",
    "TCS.NS",
    "HDFCBANK.NS",
    "INFY.NS",
    "ICICIBANK.NS",
    "HINDUNILVR.NS",
    "ITC.NS",
    "SBIN.NS",
    "BHARTIARTL.NS",
    "KOTAKBANK.NS",
    "LT.NS",
    "HCLTECH.NS",
    "AXISBANK.NS",
    "ASIANPAINT.NS",
    "MARUTI.NS",
    "WIPRO.NS",
    "NESTLEIND.NS",
    "SUNPHARMA.NS",
    "BAJFINANCE.NS",
    "TITAN.NS",
    "ULTRACEMCO.NS",
    "ONGC.NS",
    "NTPC.NS",
    "POWERGRID.NS",
    "COALINDIA.NS",
    "ADANIPORTS.NS",
    "ADANIENT.NS",
    "JSWSTEEL.NS",
    "TATAMOTORS.NS",
    "TATASTEEL.NS",
    "M&M.NS",
    "TECHM.NS",
    "DIVISLAB.NS",
    "BAJAJFINSV.NS",
    "GRASIM.NS",
    "HDFCLIFE.NS",
    "BRITANNIA.NS",
    "INDUSINDBK.NS",
    "DRREDDY.NS",
    "CIPLA.NS",
    "EICHERMOT.NS",
    "HEROMOTOCO.NS",
    "DABUR.NS",
    "GODREJCP.NS",
    "MARICO.NS",
    "PIDILITIND.NS",
    "HAVELLS.NS",
    "VOLTAS.NS",
    "WHIRLPOOL.NS",
    "AMBUJACEM.NS",
    "SHREECEM.NS",
    "ACC.NS",
    "RAMCOCEM.NS",
    "JINDALSAW.NS",
    "VEDL.NS",
    "HINDALCO.NS",
    "NMDC.NS",
    "IOC.NS",
    "BPCL.NS",
    "HPCL.NS",
    "GAIL.NS",
    "PETRONET.NS",
    "GSPL.NS",
    "IGL.NS",
    "MGL.NS",
    # Additional Large Cap Stocks
    "APOLLOHOSP.NS",
    "BAJAJ-AUTO.NS",
    "BAJAJHOLDING.NS",
    "BANKBARODA.NS",
    "BHARATFORG.NS",
    "CANBK.NS",
    "CHOLAFIN.NS",
    "COLPAL.NS",
    "DALBHARAT.NS",
    "DLF.NS",
    "GODREJPROP.NS",
    "HDFCAMC.NS",
    "ICICIPRULI.NS",
    "ICICIGI.NS",
    "INDIGO.NS",
    "IRCTC.NS",
    "JINDALSTEL.NS",
    "LICI.NS",
    "LUPIN.NS",
    "MCDOWELL-N.NS",
    "NAUKRI.NS",
    "PAGEIND.NS",
    "PFC.NS",
    "PIIND.NS",
    "POLICYBZR.NS",
    "RECLTD.NS",
    "SAIL.NS",
    "SBILIFE.NS",
    "SIEMENS.NS",
    "TATACONSUM.NS",
    "TATAPOWER.NS",
    "TORNTPHARM.NS",
    "TVSMOTOR.NS",
    "UNIONBANK.NS",
    "ZOMATO.NS",
    # Mid Cap Stocks
    "ABB.NS",
    "ADANIGREEN.NS",
    "ADANITRANS.NS",
    "ALKEM.NS",
    "APLLTD.NS",
    "AUBANK.NS",
    "BALKRISIND.NS",
    "BANDHANBNK.NS",
    "BERGEPAINT.NS",
    "BIOCON.NS",
    "BOSCHLTD.NS",
    "CADILAHC.NS",
    "CAMS.NS",
    "CONCOR.NS",
    "CUMMINSIND.NS",
    "DIXON.NS",
    "ESCORTS.NS",
    "FEDERALBNK.NS",
    "GLENMARK.NS",
    "GODREJIND.NS",
    "GUJGASLTD.NS",
    "HAL.NS",
    "HINDCOPPER.NS",
    "IDFCFIRSTB.NS",
    "IEX.NS",
    "IGL.NS",
    "INDIAMART.NS",
    "INDIANB.NS",
    "JKCEMENT.NS",
    "JUBLFOOD.NS",
    "JUSTDIAL.NS",
    "KEI.NS",
    "LAURUSLABS.NS",
    "MANKIND.NS",
    "MAXHEALTH.NS",
    "MOTHERSON.NS",
    "MPHASIS.NS",
    "NYKAA.NS",
    "OBEROIRLTY.NS",
    "OFSS.NS",
    "PERSISTENT.NS",
    "POLICYBZR.NS",
    "POWERINDIA.NS",
    "RAJESHEXPO.NS",
    "RAMKY.NS",
    "RATNAMANI.NS",
    "RVNL.NS",
    "SCHAEFFLER.NS",
    "SHYAMMETL.NS",
    "SOLARIND.NS",
    "STARHEALTH.NS",
    "SUNDARMFIN.NS",
    "SUPREMEIND.NS",
    "TATACHEM.NS",
    "TATAELXSI.NS",
    "TATACOMM.NS",
    "TRENT.NS",
    "UNOMINDA.NS",
    "VBL.NS",
    "VEDANTU.NS",
    "WIPRO.NS",
    "YESBANK.NS",
    "ZYDUSLIFE.NS",
    # Small Cap & Emerging Stocks
    "AARTIIND.NS",
    "AAVAS.NS",
    "ADANIPOWER.NS",
    "AFFLE.NS",
    "ALEMBICLTD.NS",
    "ALOKTEXT.NS",
    "ANGELONE.NS",
    "APARINDS.NS",
    "APTUS.NS",
    "ASAHIINDIA.NS",
    "ASHOKLEY.NS",
    "ASTERDM.NS",
    "ASTRAL.NS",
    "ATUL.NS",
    "AURIONPRO.NS",
    "BAJAJELEC.NS",
    "BALRAMCHIN.NS",
    "BATAINDIA.NS",
    "BEL.NS",
    "BHARATRAS.NS",
    "BLUEDART.NS",
    "BOROSIL.NS",
    "BRIGADE.NS",
    "CERA.NS",
    "CHALET.NS",
    "CHEMCON.NS",
    "CLEAN.NS",
    "COFORGE.NS",
    "COROMANDEL.NS",
    "CREDITACC.NS",
    "CRISIL.NS",
    "CYIENT.NS",
    "DCMSHRIRAM.NS",
    "DEEPAKNTR.NS",
    "DELHIVERY.NS",
    "DEVYANI.NS",
    "DIXON.NS",
    "EASEMYTRIP.NS",
    "EIHOTEL.NS",
    "ENDURANCE.NS",
    "EQUITAS.NS",
    "ERIS.NS",
    "FACT.NS",
    "FINOLEXIND.NS",
    "FORTIS.NS",
    "FRETAIL.NS",
    "FSL.NS",
    "GARFIBRES.NS",
    "GHCL.NS",
    "GILLETTE.NS",
    "GNFC.NS",
    "GODFRYPHLP.NS",
    "GRANULES.NS",
    "GRAPHITE.NS",
    "GRINDWELL.NS",
    "GSFC.NS",
    "HAPPSTMNDS.NS",
    "HATSUN.NS",
    "HEG.NS",
    "HEIDELBERG.NS",
    "HEMIPROP.NS",
    "HINDZINC.NS",
    "HONAUT.NS",
    "HSCL.NS",
    "IBREALEST.NS",
    "IBULHSGFIN.NS",
    "ICRA.NS",
    "IDEA.NS",
    "IDFC.NS",
    "IFBIND.NS",
    "IIFL.NS",
    "IMAGICAA.NS",
    "INDIACEM.NS",
    "INDIAGLYCO.NS",
    "INDIANHUME.NS",
    "INDIGOPNTS.NS",
    "INDIGRID.NS",
    "INDUSINDBK.NS",
    "INDUSTOWER.NS",
    "INFIBEAM.NS",
    "INFOBEAN.NS",
    "INOXLEISUR.NS",
    "INTELLECT.NS",
    "IOB.NS",
    "IPCALAB.NS",
    "IRB.NS",
    "ISEC.NS",
    "ITDCEM.NS",
    "ITI.NS",
    "JAGRAN.NS",
    "JAIPRAKASH.NS",
    "JAMNAAUTO.NS",
    "JBCHEPHARM.NS",
    "JBMA.NS",
    "JCHAC.NS",
    "JINDALSAW.NS",
    "JINDALSTEL.NS",
    "JISLJALEQS.NS",
    "JKLAKSHMI.NS",
    "JKPAPER.NS",
    "JKTYRE.NS",
    "JMFINANCIL.NS",
    "JOCIL.NS",
    "JPPOWER.NS",
    "JSL.NS",
    "JSWENERGY.NS",
    "JTEKTINDIA.NS",
    "JUBLINGREA.NS",
    "JUBLPHARMA.NS",
    "JUSTDIAL.NS",
    "JYOTHYLAB.NS",
    "KAJARIACER.NS",
    "KALPATPOWR.NS",
    "KANSAINER.NS",
    "KARURVYSYA.NS",
    "KAYCEE.NS",
    "KEC.NS",
    "KEI.NS",
    "KENNAMET.NS",
    "KESORAMIND.NS",
    "KEYFINSERV.NS",
    "KFINTECH.NS",
    "KIMS.NS",
    "KIRLOSBROS.NS",
    "KIRLOSENG.NS",
    "KOTAKBANK.NS",
    "KPITTECH.NS",
    "KPRMILL.NS",
    "KRBL.NS",
    "KSB.NS",
    "L&TFH.NS",
    "LAOPALA.NS",
    "LATENTVIEW.NS",
    "LAXMIMACH.NS",
    "LEMONTREE.NS",
    "LICHSGFIN.NS",
    "LINDEINDIA.NS",
    "LODHA.NS",
    "LTIM.NS",
    "LTTS.NS",
    "LUMAXIND.NS",
    "LUPIN.NS",
    "LUXIND.NS",
    "LYKALABS.NS",
    "M&M.NS",
    "M&MFIN.NS",
    "MAHABANK.NS",
    "MAHINDCIE.NS",
    "MAHLOG.NS",
    "MAHSCOOTER.NS",
    "MAHSEAMLES.NS",
    "MANAPPURAM.NS",
    "MANGLMCEM.NS",
    "MANINDS.NS",
    "MARICO.NS",
    "MARKSANS.NS",
    "MASFIN.NS",
    "MASTEK.NS",
    "MAYURUNIQ.NS",
    "MAZDA.NS",
    "MCX.NS",
    "MEDANTA.NS",
    "MEDPLUS.NS",
    "MEGH.NS",
    "METROBRAND.NS",
    "METROPOLIS.NS",
    "MFSL.NS",
    "MGL.NS",
    "MHRIL.NS",
    "MIDHANI.NS",
    "MINDACORP.NS",
    "MINDAIND.NS",
    "MINDTREE.NS",
    "MIRCELECTR.NS",
    "MIRZAINT.NS",
    "MMTC.NS",
    "MOIL.NS",
    "MORARJEE.NS",
    "MOTHERSON.NS",
    "MPHASIS.NS",
    "MRF.NS",
    "MRPL.NS",
    "MSUMI.NS",
    "MTARTECH.NS",
    "MTNL.NS",
    "MUKANDLTD.NS",
    "MUNJALSHOW.NS",
    "MUTHOOTFIN.NS",
    "NACLIND.NS",
    "NAGARFERT.NS",
    "NAHARSPING.NS",
    "NAM-INDIA.NS",
    "NATCOPHARM.NS",
    "NAUKRI.NS",
    "NAVINFLUOR.NS",
    "NAZARA.NS",
    "NBCC.NS",
    "NCC.NS",
    "NEOGEN.NS",
    "NESTLEIND.NS",
    "NETWORK18.NS",
    "NEULANDLAB.NS",
    "NEWGEN.NS",
    "NFL.NS",
    "NHPC.NS",
    "NIACL.NS",
    "NILKAMAL.NS",
    "NIPPOBATRY.NS",
    "NLCINDIA.NS",
    "NMDC.NS",
    "NOCIL.NS",
    "NOIDATOLL.NS",
    "NRBBEARING.NS",
    "NTPC.NS",
    "NUVOCO.NS",
    "OBEROIRLTY.NS",
    "OFSS.NS",
    "OIL.NS",
    "OLECTRA.NS",
    "OMAXE.NS",
    "ONGC.NS",
    "ONMOBILE.NS",
    "ORIENTBANK.NS",
    "ORIENTCEM.NS",
    "ORIENTELEC.NS",
    "ORIENTREF.NS",
    "PAGEIND.NS",
    "PAISALO.NS",
    "PALREDTECH.NS",
    "PANACEABIO.NS",
    "PANAMAPET.NS",
    "PARAGMILK.NS",
    "PARAS.NS",
    "PATANJALI.NS",
    "PATELENG.NS",
    "PCBL.NS",
    "PCJEWELLER.NS",
    "PDSL.NS",
    "PEL.NS",
    "PENIND.NS",
    "PERSISTENT.NS",
    "PETRONET.NS",
    "PFC.NS",
    "PFIZER.NS",
    "PGHL.NS",
    "PGHH.NS",
    "PHILIPCARB.NS",
    "PHOENIXLTD.NS",
    "PIDILITIND.NS",
    "PIIND.NS",
    "PILANIINVS.NS",
    "PIONEEREMB.NS",
    "PITTIENG.NS",
    "PLASTIBLEN.NS",
    "PNB.NS",
    "PNBHOUSING.NS",
    "PNCINFRA.NS",
    "POLICYBZR.NS",
    "POLYCAB.NS",
    "POLYMED.NS",
    "POLYPLEX.NS",
    "POWERGRID.NS",
    "POWERINDIA.NS",
    "PPAP.NS",
    "PPLPHARMA.NS",
    "PRESTIGE.NS",
    "PRICOLLTD.NS",
    "PRINCEPIPE.NS",
    "PRISMCHEM.NS",
    "PROZONINTU.NS",
    "PSB.NS",
    "PSPPROJECT.NS",
    "PTC.NS",
    "PTL.NS",
    "PUNJLLOYD.NS",
    "PURAVANKARA.NS",
    "PVRINOX.NS",
    "QUESS.NS",
    "RADICO.NS",
    "RAILTEL.NS",
    "RAIN.NS",
    "RAJESHEXPO.NS",
    "RAJMET.NS",
    "RALLIS.NS",
    "RAMCOCEM.NS",
    "RAMKY.NS",
    "RATNAMANI.NS",
    "RBLBANK.NS",
    "RCF.NS",
    "RECLTD.NS",
    "REDINGTON.NS",
    "RELAXO.NS",
    "RELCAPITAL.NS",
    "RELCHEM.NS",
    "RELIANCE.NS",
    "RELINFRA.NS",
    "REPCOHOME.NS",
    "RESPONIND.NS",
    "RIIL.NS",
    "RITES.NS",
    "RKFORGE.NS",
    "ROHLTD.NS",
    "ROLEXRINGS.NS",
    "ROSSARI.NS",
    "ROUTE.NS",
    "RPGLIFE.NS",
    "RPOWER.NS",
    "RPPINFRA.NS",
    "RPSGVENT.NS",
    "RSWM.NS",
    "RTNPOWER.NS",
    "RUBYMILLS.NS",
    "RUPA.NS",
    "RUSHIL.NS",
    "RVNL.NS",
    "SADBHAV.NS",
    "SAIL.NS",
    "SAKSOFT.NS",
    "SALASAR.NS",
    "SALONA.NS",
    "SAMHI.NS",
    "SANOFI.NS",
    "SAPPHIRE.NS",
    "SARDAEN.NS",
    "SAREGAMA.NS",
    "SASKEN.NS",
    "SASTASUNDR.NS",
    "SATIA.NS",
    "SATIN.NS",
    "SBICARD.NS",
    "SBILIFE.NS",
    "SCHAEFFLER.NS",
    "SCHNEIDER.NS",
    "SCI.NS",
    "SDBL.NS",
    "SEAMEC.NS",
    "SECURKLOUD.NS",
    "SEQUENT.NS",
    "SFL.NS",
    "SGIL.NS",
    "SHANTIGEAR.NS",
    "SHARDACROP.NS",
    "SHARDAMOTR.NS",
    "SHIL.NS",
    "SHIVALIK.NS",
    "SHK.NS",
    "SHOPERSTOP.NS",
    "SHRIRAMFIN.NS",
    "SHYAMMETL.NS",
    "SIEMENS.NS",
    "SIGIND.NS",
    "SIS.NS",
    "SJVN.NS",
    "SKFINDIA.NS",
    "SMSPHARMA.NS",
    "SOBHA.NS",
    "SOLARIND.NS",
    "SOLARA.NS",
    "SONACOMS.NS",
    "SONATSOFTW.NS",
    "SOUTHBANK.NS",
    "SPANDANA.NS",
    "SPANDANE.NS",
    "SPARC.NS",
    "SPICEJET.NS",
    "SPTL.NS",
    "SRF.NS",
    "SRHHYPOLTD.NS",
    "STAR.NS",
    "STARCEMENT.NS",
    "STARHEALTH.NS",
    "STCINDIA.NS",
    "STEELCAS.NS",
    "STEELXIND.NS",
    "STEL.NS",
    "STERTOOLS.NS",
    "STLTECH.NS",
    "SUBEXLTD.NS",
    "SUDARSCHEM.NS",
    "SUMEETINDS.NS",
    "SUMMITSEC.NS",
    "SUNCLAYLTD.NS",
    "SUNDARMFIN.NS",
    "SUNDRMFAST.NS",
    "SUNFLAG.NS",
    "SUNPHARMA.NS",
    "SUNTECK.NS",
    "SUPERHOUSE.NS",
    "SUPERSPIN.NS",
    "SUPRAJIT.NS",
    "SUPREMEIND.NS",
    "SUPREMEINF.NS",
    "SURANAT&P.NS",
    "SURYAROSNI.NS",
    "SURYODAY.NS",
    "SUTLEJTEX.NS",
    "SUULD.NS",
    "SUVEN.NS",
    "SUVENPHAR.NS",
    "SUZLON.NS",
    "SWANENERGY.NS",
    "SWARAJENG.NS",
    "SWARAJMAZ.NS",
    "SYMPHONY.NS",
    "SYNGENE.NS",
    "TAALENTECH.NS",
    "TALBROAUTO.NS",
    "TANLA.NS",
    "TARACHAND.NS",
    "TARAPUR.NS",
    "TARSONS.NS",
    "TASTYBITE.NS",
    "TATACHEM.NS",
    "TATACOMM.NS",
    "TATACONSUM.NS",
    "TATACOFFEE.NS",
    "TATAELXSI.NS",
    "TATAINVEST.NS",
    "TATAMETALI.NS",
    "TATAMOTORS.NS",
    "TATAPOWER.NS",
    "TATASPONGE.NS",
    "TATASTEEL.NS",
    "TATVA.NS",
    "TCI.NS",
    "TCIEXP.NS",
    "TCNSBRANDS.NS",
    "TCPLPACK.NS",
    "TCS.NS",
    "TEAMLEASE.NS",
    "TECHM.NS",
    "TECHNOE.NS",
    "TEJASNET.NS",
    "TEXINFRA.NS",
    "TEXMOPIPES.NS",
    "TEXRAIL.NS",
    "THANGAMAYL.NS",
    "THEMISMED.NS",
    "THERMAX.NS",
    "THOMASCOOK.NS",
    "THYROCARE.NS",
    "TIINDIA.NS",
    "TIMETECHNO.NS",
    "TIMKEN.NS",
    "TIPS.NS",
    "TITAGARH.NS",
    "TITAN.NS",
    "TMB.NS",
    "TNPL.NS",
    "TOKYOPLAST.NS",
    "TORNTPHARM.NS",
    "TORNTPOWER.NS",
    "TOTAL.NS",
    "TOUCHWOOD.NS",
    "TPLPLASTEH.NS",
    "TRACXN.NS",
    "TRANSPEK.NS",
    "TRENT.NS",
    "TRF.NS",
    "TRIDENT.NS",
    "TRIL.NS",
    "TRITURBINE.NS",
    "TRIVENI.NS",
    "TTKHLTCARE.NS",
    "TTKPRESTIG.NS",
    "TTML.NS",
    "TV18BRDCST.NS",
    "TVSELECT.NS",
    "TVSMOTOR.NS",
    "TVTODAY.NS",
    "TWL.NS",
    "UBL.NS",
    "UCALFUEL.NS",
    "UCOBANK.NS",
    "UFLEX.NS",
    "UFO.NS",
    "UGARSUGAR.NS",
    "UJJIVAN.NS",
    "UJJIVANSFB.NS",
    "ULTRACEMCO.NS",
    "UMANGDAIRY.NS",
    "UNICHEMLAB.NS",
    "UNIDT.NS",
    "UNIENTER.NS",
    "UNIONBANK.NS",
    "UNITECH.NS",
    "UNIVCABLES.NS",
    "UPL.NS",
    "URJA.NS",
    "USHAMART.NS",
    "UTIAMC.NS",
    "UTIBANK.NS",
    "UTKARSHBNK.NS",
    "VADILALIND.NS",
    "VAIBHAVGBL.NS",
    "VAKRANGEE.NS",
    "VARDHMAN.NS",
    "VARDHMANPOL.NS",
    "VARROC.NS",
    "VASWANI.NS",
    "VBL.NS",
    "VEDANTU.NS",
    "VEDL.NS",
    "VENKEYS.NS",
    "VENUSPIPES.NS",
    "VENUSREM.NS",
    "VERANDA.NS",
    "VESUVIUS.NS",
    "VGUARD.NS",
    "VHL.NS",
    "VIDHIING.NS",
    "VIJAYA.NS",
    "VIJAYABANK.NS",
    "VIKASECO.NS",
    "VIMTALABS.NS",
    "VINATIORGA.NS",
    "VINDHYATEL.NS",
    "VINEETLABS.NS",
    "VINYLINDIA.NS",
    "VIPCLOTHNG.NS",
    "VIPIND.NS",
    "VIRINCHI.NS",
    "VISAKAIND.NS",
    "VISESHINFO.NS",
    "VISHAL.NS",
    "VISHNU.NS",
    "VIVIDHA.NS",
    "VLSFINANCE.NS",
    "VMART.NS",
    "VOLTAS.NS",
    "VOLTAMP.NS",
    "VPRPL.NS",
    "VRLLOG.NS",
    "VSSL.NS",
    "VSTIND.NS",
    "VSTTILLERS.NS",
    "VTL.NS",
    "WABAG.NS",
    "WABCOINDIA.NS",
    "WALCHANNAG.NS",
    "WANBURY.NS",
    "WATERBASE.NS",
    "WEBELSOLAR.NS",
    "WEIZMANN.NS",
    "WELCORP.NS",
    "WELENT.NS",
    "WELSPUNIND.NS",
    "WENDT.NS",
    "WESTLIFE.NS",
    "WHEELS.NS",
    "WHIRLPOOL.NS",
    "WILLAMAGOR.NS",
    "WINDMACHIN.NS",
    "WINSOME.NS",
    "WIPRO.NS",
    "WOCKPHARMA.NS",
    "WONDERLA.NS",
    "WORTH.NS",
    "WSI.NS",
    "WSTCSTPAPR.NS",
    "XCHANGING.NS",
    "XELPMOC.NS",
    "XPROINDIA.NS",
    "YESBANK.NS",
    "YUKEN.NS",
    "ZANDUREALT.NS",
    "ZEEL.NS",
    "ZEELEARN.NS",
    "ZENSAR.NS",
    "ZENTEC.NS",
    "ZFCVINDIA.NS",
    "ZODIACLOTH.NS",
    "ZOMATO.NS",
    "ZUARI.NS",
    "ZUARIGLOB.NS",
    "ZYDUSLIFE.NS",
    "ZYLOG.NS",
    # BSE Stocks
    "RELIANCE.BO",
    "TCS.BO",
    "HDFCBANK.BO",
    "INFY.BO",
    "ICICIBANK.BO",
]

DEFAULT_STOCKS = ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "ICICIBANK.NS", "HINDUNILVR.NS", "ITC.NS"]


# Helper functions for news processing
def is_valid_article(article: Dict) -> bool:
    """Check if an article has valid data."""
    title = article.get('title', '').strip()
    # Filter out articles with no title or placeholder titles
    if not title or title.lower() in ['no title', 'untitled', '']:
        return False
    
    # Check for valid timestamp (not 0 or epoch start)
    timestamp = article.get('providerPublishTime', 0)
    if timestamp == 0 or timestamp < 946684800:  # Before year 2000
        return False
    
    return True


def is_growth_related(title: str, summary: str = "") -> bool:
    """Check if news is related to growth or positive performance."""
    growth_keywords = [
        "growth", "surge", "rise", "gain", "profit", "revenue", "earnings beat",
        "outperform", "upgrade", "bullish", "rally", "soar", "jump", "climb",
        "increase", "expansion", "acquisition", "partnership", "deal", "positive",
        "strong", "record", "high", "beat", "exceed", "outperform"
    ]
    text = (title + " " + summary).lower()
    return any(keyword in text for keyword in growth_keywords)


def is_depreciation_related(title: str, summary: str = "") -> bool:
    """Check if news is related to depreciation or negative performance."""
    depreciation_keywords = [
        "fall", "drop", "decline", "loss", "downgrade", "bearish", "plunge",
        "crash", "slump", "decrease", "miss", "disappoint", "negative", "weak",
        "concern", "worry", "risk", "uncertainty", "challenge", "struggle",
        "underperform", "sell-off", "correction", "volatility"
    ]
    text = (title + " " + summary).lower()
    return any(keyword in text for keyword in depreciation_keywords)


def format_news_date(timestamp: int) -> str:
    """Convert timestamp to readable relative time format (like '2h ago', '1d ago')."""
    try:
        if timestamp == 0 or timestamp < 946684800:  # Invalid timestamp
            return "Unknown date"
        
        dt = datetime.fromtimestamp(timestamp)
        now = datetime.now()
        
        # Check if date is reasonable
        if dt.year < 2000 or dt.year > datetime.now().year + 1:
            return "Unknown date"
        
        # Calculate relative time
        time_diff = now - dt.replace(tzinfo=None) if dt.tzinfo else now - dt
        
        if time_diff.total_seconds() < 60:
            return "Just now"
        elif time_diff.total_seconds() < 3600:
            minutes = int(time_diff.total_seconds() / 60)
            return f"{minutes}m ago"
        elif time_diff.total_seconds() < 86400:
            hours = int(time_diff.total_seconds() / 3600)
            return f"{hours}h ago"
        elif time_diff.days < 7:
            days = time_diff.days
            return f"{days}d ago"
        else:
            return dt.strftime("%Y-%m-%d")
    except:
        return "Unknown date"


# Load news for all stocks in marquee (runs in background)
@st.cache_resource(show_spinner=False, ttl="30m")
def load_all_stocks_news() -> List[Dict]:
    """Load news for all stocks in STOCKS list using multi-source approach."""
    all_news = []
    
    # Get API keys from streamlit secrets
    try:
        finnhub_key = st.secrets.get("FINNHUB_API_KEY", None)
        newsapi_key = st.secrets.get("NEWSAPI_KEY", None)
    except Exception:
        finnhub_key = None
        newsapi_key = None
    
    # Process stocks in batches to avoid rate limits
    batch_size = 10
    for i in range(0, len(STOCKS), batch_size):
        batch = STOCKS[i:i+batch_size]
        for ticker in batch:
            try:
                # Try Finnhub first
                finnhub_news = fetch_news_finnhub(ticker, finnhub_key)
                all_news.extend(finnhub_news)
                
                # Try NewsAPI if key available
                if newsapi_key:
                    newsapi_news = fetch_news_newsapi(ticker, newsapi_key)
                    all_news.extend(newsapi_news)
                
                # Fallback to yfinance
                ticker_obj = yf.Ticker(ticker)
                yf_news = ticker_obj.news
                if yf_news:
                    for article in yf_news:
                        if is_valid_article(article):
                            article['ticker'] = ticker
                            all_news.append(article)
            except Exception:
                continue
        
        # Small delay between batches to respect rate limits
        if i + batch_size < len(STOCKS):
            time.sleep(0.5)
    
    # Remove duplicates
    seen_titles = set()
    unique_news = []
    for article in all_news:
        title_lower = article.get('title', '').lower().strip()
        if title_lower and title_lower not in seen_titles:
            unique_news.append(article)
            seen_titles.add(title_lower)
    
    # Sort by date (newest first)
    unique_news.sort(key=lambda x: x.get('providerPublishTime', 0), reverse=True)
    return unique_news[:100]  # Limit to 100 most recent articles


# Display marquee with all stocks news at the top
try:
    all_news = load_all_stocks_news()
    if all_news:
        # Create marquee HTML
        news_items = []
        for article in all_news:
            title = article.get('title', '').strip()
            ticker = article.get('ticker', '')
            link = article.get('link', '#')
            publish_time = article.get('providerPublishTime', 0)
            date_str = format_news_date(publish_time)
            
            # Determine sentiment color
            summary = article.get('summary', '')
            is_growth = is_growth_related(title, summary)
            is_depreciation = is_depreciation_related(title, summary)
            
            if is_growth:
                color = "#00cc00"
                icon = "📈"
            elif is_depreciation:
                color = "#ff4444"
                icon = "📉"
            else:
                color = "#888888"
                icon = "📰"
            
            news_items.append(
                f'<span style="color: {color}; margin-right: 30px;">{icon} <strong>{ticker}</strong>: '
                f'<a href="{link}" target="_blank" style="color: {color}; text-decoration: none;">{title}</a> '
                f'({date_str})</span>'
            )
        
        marquee_html = f"""
        <div style="background: linear-gradient(90deg, #1e3a5f 0%, #2d4a6e 100%); 
                    padding: 12px 0; 
                    border-radius: 5px; 
                    margin-bottom: 20px;
                    overflow: hidden;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            <div style="display: flex; align-items: center;">
                <span style="color: #ffd700; font-weight: bold; margin-right: 15px; white-space: nowrap; padding-left: 10px;">
                    📊 Market News:
                </span>
                <marquee behavior="scroll" direction="left" scrollamount="3" style="color: white; font-size: 14px;">
                    {' • '.join(news_items)}
                </marquee>
            </div>
        </div>
        """
        st.markdown(marquee_html, unsafe_allow_html=True)
except Exception:
    # Silently fail if marquee news can't be loaded
    pass


def stocks_to_str(stocks):
    return ",".join(stocks)


if "tickers_input" not in st.session_state:
    st.session_state.tickers_input = st.query_params.get(
        "stocks", stocks_to_str(DEFAULT_STOCKS)
    ).split(",")


# Callback to update query param when input changes
def update_query_param():
    if st.session_state.tickers_input:
        st.query_params["stocks"] = stocks_to_str(st.session_state.tickers_input)
    else:
        st.query_params.pop("stocks", None)


top_left_cell = cols[0].container(
    border=True, height="stretch", vertical_alignment="center"
)

with top_left_cell:
    # Selectbox for stock tickers
    tickers = st.multiselect(
        "Stock tickers",
        options=sorted(set(STOCKS) | set(st.session_state.tickers_input)),
        default=st.session_state.tickers_input,
        placeholder="Choose stocks to compare. Example: RELIANCE.NS or TCS.NS",
        accept_new_options=True,
    )

# Time horizon selector
horizon_map = {
    "1 Months": "1mo",
    "3 Months": "3mo",
    "6 Months": "6mo",
    "1 Year": "1y",
    "5 Years": "5y",
    "10 Years": "10y",
    "20 Years": "20y",
}

with top_left_cell:
    # Buttons for picking time horizon
    horizon = st.pills(
        "Time horizon",
        options=list(horizon_map.keys()),
        default="6 Months",
    )

tickers = [t.upper() for t in tickers]

# Update query param when text input changes
if tickers:
    st.query_params["stocks"] = stocks_to_str(tickers)
else:
    # Clear the param if input is empty
    st.query_params.pop("stocks", None)

if not tickers:
    top_left_cell.info("Pick some stocks to compare", icon=":material/info:")
    st.stop()


right_cell = cols[1].container(
    border=True, height="stretch", vertical_alignment="center"
)


@st.cache_resource(show_spinner=False, ttl="6h")
def load_data(tickers, period):
    tickers_obj = yf.Tickers(tickers)
    data = tickers_obj.history(period=period)
    if data is None:
        raise RuntimeError("YFinance returned no data.")
    return data["Close"]


def fetch_news_finnhub(ticker: str, api_key: Optional[str] = None) -> List[Dict]:
    """Fetch news from Finnhub API (free tier available)."""
    articles = []
    try:
        # Remove .NS or .BO suffix for Finnhub
        symbol = ticker.split('.')[0]
        url = f"https://finnhub.io/api/v1/company-news"
        params = {
            'symbol': symbol,
            'from': (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d'),
            'to': datetime.now().strftime('%Y-%m-%d')
        }
        # Always use API key if provided (required for better rate limits)
        if api_key:
            params['token'] = api_key
        else:
            # Without API key, Finnhub has very limited access
            return articles
        
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list):
                for item in data[:20]:  # Limit to 20 articles
                    article = {
                        'title': item.get('headline', ''),
                        'summary': item.get('summary', ''),
                        'link': item.get('url', ''),
                        'publisher': item.get('source', 'Finnhub'),
                        'providerPublishTime': item.get('datetime', 0),
                        'ticker': ticker
                    }
                    if is_valid_article(article):
                        articles.append(article)
    except Exception:
        pass
    return articles


def fetch_news_newsapi(ticker: str, api_key: Optional[str] = None) -> List[Dict]:
    """Fetch news from NewsAPI (free tier available)."""
    articles = []
    if not api_key:
        return articles
    
    try:
        # Remove .NS or .BO suffix
        symbol = ticker.split('.')[0]
        url = "https://newsapi.org/v2/everything"
        params = {
            'q': f"{symbol} stock",
            'language': 'en',
            'sortBy': 'publishedAt',
            'pageSize': 20,
            'apiKey': api_key
        }
        
        response = requests.get(url, params=params, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'ok':
                for item in data.get('articles', [])[:20]:
                    # Convert publishedAt to timestamp
                    try:
                        pub_date = datetime.fromisoformat(item['publishedAt'].replace('Z', '+00:00'))
                        timestamp = int(pub_date.timestamp())
                    except:
                        timestamp = int(time.time())
                    
                    article = {
                        'title': item.get('title', ''),
                        'summary': item.get('description', ''),
                        'link': item.get('url', ''),
                        'publisher': item.get('source', {}).get('name', 'NewsAPI'),
                        'providerPublishTime': timestamp,
                        'ticker': ticker
                    }
                    if is_valid_article(article):
                        articles.append(article)
    except Exception:
        pass
    return articles


@st.cache_resource(show_spinner=False, ttl="30m")
def load_news_multi_source(tickers: List[str]) -> Dict[str, List[Dict]]:
    """Load news from multiple sources for better coverage."""
    news_data = {}
    
    # Get API keys from streamlit secrets
    try:
        finnhub_key = st.secrets.get("FINNHUB_API_KEY", None)
        newsapi_key = st.secrets.get("NEWSAPI_KEY", None)
    except Exception:
        finnhub_key = None
        newsapi_key = None
    
    for ticker in tickers:
        all_articles = []
        
        # Try Finnhub first (free tier, no key required for limited requests)
        try:
            finnhub_news = fetch_news_finnhub(ticker, finnhub_key)
            all_articles.extend(finnhub_news)
        except Exception:
            pass
        
        # Try NewsAPI if key is available
        if newsapi_key:
            try:
                newsapi_news = fetch_news_newsapi(ticker, newsapi_key)
                all_articles.extend(newsapi_news)
            except Exception:
                pass
        
        # Fallback to yfinance
        try:
            ticker_obj = yf.Ticker(ticker)
            yf_news = ticker_obj.news
            if yf_news and len(yf_news) > 0:
                for article in yf_news:
                    article['ticker'] = ticker
                    if is_valid_article(article):
                        all_articles.append(article)
        except Exception:
            pass
        
        # Remove duplicates based on title similarity
        unique_articles = []
        seen_titles = set()
        for article in all_articles:
            title_lower = article.get('title', '').lower().strip()
            # Simple deduplication - check if similar title exists
            is_duplicate = False
            for seen in seen_titles:
                # Check if titles are very similar (simple approach)
                if title_lower and seen and (title_lower == seen or title_lower in seen or seen in title_lower):
                    is_duplicate = True
                    break
            if not is_duplicate and title_lower:
                unique_articles.append(article)
                seen_titles.add(title_lower)
        
        # Sort by date (newest first)
        unique_articles.sort(key=lambda x: x.get('providerPublishTime', 0), reverse=True)
        
        if unique_articles:
            news_data[ticker] = unique_articles[:30]  # Limit to 30 per ticker
    
    return news_data


@st.cache_resource(show_spinner=False, ttl="1h")
def load_news(tickers: List[str]) -> Dict[str, List[Dict]]:
    """Load news articles for given tickers (uses multi-source approach)."""
    return load_news_multi_source(tickers)


# Load the data
try:
    data = load_data(tickers, horizon_map[horizon])
except yf.exceptions.YFRateLimitError as e:
    st.warning("YFinance is rate-limiting us :(\nTry again later.")
    load_data.clear()  # Remove the bad cache entry.
    st.stop()

empty_columns = data.columns[data.isna().all()].tolist()

if empty_columns:
    st.error(f"Error loading data for the tickers: {', '.join(empty_columns)}.")
    st.stop()

# Normalize prices (start at 1)
# Handle cases where first value might be 0 or NaN
normalized = data.div(data.iloc[0].replace(0, pd.NA))
# Replace inf values (from division by zero) with NaN
normalized = normalized.replace([float('inf'), float('-inf')], pd.NA)

# Filter out NaN values and get latest normalized values
latest_norm_values = {}
for ticker in tickers:
    latest_value = normalized[ticker].iat[-1]
    if pd.notna(latest_value) and pd.notna(normalized[ticker].iloc[0]):
        latest_norm_values[latest_value] = ticker

# Only show metrics if we have valid data
if latest_norm_values:
    max_norm_value = max(latest_norm_values.items())
    min_norm_value = min(latest_norm_values.items())
    
    bottom_left_cell = cols[0].container(
        border=True, height="stretch", vertical_alignment="center"
    )
    
    with bottom_left_cell:
        cols = st.columns(2)
        # Safely calculate delta, handling NaN cases
        max_delta = max_norm_value[0] * 100 if pd.notna(max_norm_value[0]) else 0
        min_delta = min_norm_value[0] * 100 if pd.notna(min_norm_value[0]) else 0
        
        cols[0].metric(
            "Best stock",
            max_norm_value[1],
            delta=f"{round(max_delta)}%",
            width="content",
        )
        cols[1].metric(
            "Worst stock",
            min_norm_value[1],
            delta=f"{round(min_delta)}%",
            width="content",
        )
else:
    bottom_left_cell = cols[0].container(
        border=True, height="stretch", vertical_alignment="center"
    )
    with bottom_left_cell:
        st.warning("Unable to calculate performance metrics. Some stocks may have missing data.")


# Plot normalized prices
with right_cell:
    st.altair_chart(
        alt.Chart(
            normalized.reset_index().melt(
                id_vars=["Date"], var_name="Stock", value_name="Normalized price"
            )
        )
        .mark_line()
        .encode(
            alt.X("Date:T"),
            alt.Y("Normalized price:Q").scale(zero=False),
            alt.Color("Stock:N"),
        )
        .properties(height=400)
    )

""
""

# Plot individual stock vs peer average
"""
## Individual stocks vs peer average

For the analysis below, the "peer average" when analyzing stock X always
excludes X itself.
"""

if len(tickers) <= 1:
    st.warning("Pick 2 or more tickers to compare them")
    st.stop()

NUM_COLS = 4
cols = st.columns(NUM_COLS)

for i, ticker in enumerate(tickers):
    # Skip if ticker doesn't exist in normalized data or has no valid data
    if ticker not in normalized.columns or normalized[ticker].isna().all():
        continue
    
    # Calculate peer average (excluding current stock)
    peers = normalized.drop(columns=[ticker])
    # Only calculate peer average if there are other valid peers
    if peers.empty or peers.isna().all().all():
        continue
    peer_avg = peers.mean(axis=1)

    # Create DataFrame with peer average.
    plot_data = pd.DataFrame(
        {
            "Date": normalized.index,
            ticker: normalized[ticker],
            "Peer average": peer_avg,
        }
    ).melt(id_vars=["Date"], var_name="Series", value_name="Price")

    chart = (
        alt.Chart(plot_data)
        .mark_line()
        .encode(
            alt.X("Date:T"),
            alt.Y("Price:Q").scale(zero=False),
            alt.Color(
                "Series:N",
                scale=alt.Scale(domain=[ticker, "Peer average"], range=["red", "gray"]),
                legend=alt.Legend(orient="bottom"),
            ),
            alt.Tooltip(["Date", "Series", "Price"]),
        )
        .properties(title=f"{ticker} vs peer average", height=300)
    )

    cell = cols[(i * 2) % NUM_COLS].container(border=True)
    cell.write("")
    cell.altair_chart(chart, use_container_width=True)

    # Create Delta chart
    plot_data = pd.DataFrame(
        {
            "Date": normalized.index,
            "Delta": normalized[ticker] - peer_avg,
        }
    )

    chart = (
        alt.Chart(plot_data)
        .mark_area()
        .encode(
            alt.X("Date:T"),
            alt.Y("Delta:Q").scale(zero=False),
        )
        .properties(title=f"{ticker} minus peer average", height=300)
    )

    cell = cols[(i * 2 + 1) % NUM_COLS].container(border=True)
    cell.write("")
    cell.altair_chart(chart, use_container_width=True)

""
""

"""
## Raw data
"""

data

"""
---
## 📰 Latest News & Market Updates
"""

# Display color legend for news sentiment
legend_col1, legend_col2, legend_col3 = st.columns(3)
with legend_col1:
    st.markdown(
        """
        <div style="background: #1a3a1a; border-left: 4px solid #00cc00; padding: 10px; border-radius: 5px; margin-bottom: 15px;">
            <div style="display: flex; align-items: center; gap: 8px;">
                <span style="color: #00cc00; font-size: 20px; font-weight: bold;">●</span>
                <div>
                    <strong style="color: #00cc00;">Green - Growth/Positive</strong>
                    <p style="color: #aaa; font-size: 12px; margin: 4px 0 0 0;">Positive news, growth, profits, gains, upgrades</p>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
with legend_col2:
    st.markdown(
        """
        <div style="background: #3a1a1a; border-left: 4px solid #ff4444; padding: 10px; border-radius: 5px; margin-bottom: 15px;">
            <div style="display: flex; align-items: center; gap: 8px;">
                <span style="color: #ff4444; font-size: 20px; font-weight: bold;">●</span>
                <div>
                    <strong style="color: #ff4444;">Red - Depreciation/Negative</strong>
                    <p style="color: #aaa; font-size: 12px; margin: 4px 0 0 0;">Negative news, losses, declines, downgrades</p>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
with legend_col3:
    st.markdown(
        """
        <div style="background: #1a1a3a; border-left: 4px solid #4A90E2; padding: 10px; border-radius: 5px; margin-bottom: 15px;">
            <div style="display: flex; align-items: center; gap: 8px;">
                <span style="color: #4A90E2; font-size: 20px; font-weight: bold;">●</span>
                <div>
                    <strong style="color: #4A90E2;">Blue - General/Neutral</strong>
                    <p style="color: #aaa; font-size: 12px; margin: 4px 0 0 0;">General news, updates, neutral information</p>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# Load and display news if at least one stock is selected
if tickers:
    try:
        with st.spinner("Loading news articles..."):
            news_data = load_news(tickers)
        
        # Collect all articles from all selected stocks
        all_articles = []
        for ticker, articles in news_data.items():
            for article in articles:
                if is_valid_article(article):
                    article['source_ticker'] = ticker
                    all_articles.append(article)
        
        if all_articles:
            # Sort by sentiment (green first, then red, then blue), then by date (newest first)
            def get_sentiment_priority(article):
                title = article.get('title', '').strip()
                summary = article.get('summary', '').strip()
                is_growth = is_growth_related(title, summary)
                is_depreciation = is_depreciation_related(title, summary)
                
                # Priority: 0 = green (growth), 1 = red (depreciation), 2 = blue (general)
                if is_growth:
                    return 0
                elif is_depreciation:
                    return 1
                else:
                    return 2
            
            # Sort by sentiment priority first, then by date (newest first)
            all_articles.sort(key=lambda x: (
                get_sentiment_priority(x),
                -x.get('providerPublishTime', 0)  # Negative for descending order (newest first)
            ))
            
            # Display in flashcard grid (3 columns)
            st.caption(f"Showing {len(all_articles)} news articles • Last updated: {datetime.now().strftime('%H:%M:%S')}")
            
            # Display articles in rows of 3 cards
            num_cols = 3
            for i in range(0, len(all_articles), num_cols):
                cols = st.columns(num_cols)
                batch = all_articles[i:i+num_cols]
                
                for col_idx, article in enumerate(batch):
                    if col_idx >= len(cols):
                        break
                    
                    with cols[col_idx]:
                        title = article.get('title', '').strip()
                        link = article.get('link', '#')
                        publisher = article.get('publisher', 'Unknown')
                        publish_time = article.get('providerPublishTime', 0)
                        summary = article.get('summary', '').strip()
                        ticker = article.get('source_ticker', article.get('ticker', ''))
                        
                        if not title:
                            continue
                        
                        # Determine sentiment and color
                        is_growth = is_growth_related(title, summary)
                        is_depreciation = is_depreciation_related(title, summary)
                        time_str = format_news_date(publish_time)
                        
                        # Color coding: green for growth, red for depreciation, blue for general
                        if is_growth:
                            ticker_color = "#00cc00"  # Green
                        elif is_depreciation:
                            ticker_color = "#ff4444"  # Red
                        else:
                            ticker_color = "#4A90E2"  # Blue
                        
                        # Create flashcard with dark theme styling (matching the image)
                        # Truncate summary for display
                        summary_display = summary[:150] + ('...' if len(summary) > 150 else '') if summary else ''
                        
                        card_html = f"""
                        <div style="
                            background: #2a2a2a;
                            border: 1px solid #3a3a3a;
                            border-radius: 10px;
                            padding: 20px;
                            margin-bottom: 20px;
                            height: 100%;
                            display: flex;
                            flex-direction: column;
                            box-shadow: 0 4px 6px rgba(0,0,0,0.4);
                            transition: transform 0.2s;
                        ">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
                                <span style="color: {ticker_color}; font-weight: 700; font-size: 20px; letter-spacing: 0.5px;">{ticker}</span>
                                <span style="color: #999; font-size: 13px; font-weight: 400;">{time_str}</span>
                            </div>
                            <a href="{link}" target="_blank" style="text-decoration: none; color: #fff; display: block; margin-bottom: 12px;">
                                <h3 style="color: #fff; font-size: 17px; font-weight: 700; margin: 0; line-height: 1.4; letter-spacing: -0.2px;">
                                    {title}
                                </h3>
                            </a>
                            <p style="color: #bbb; font-size: 14px; line-height: 1.6; margin: 0 0 16px 0; flex-grow: 1; overflow: hidden;">
                                {summary_display}
                            </p>
                            <div style="color: #888; font-size: 12px; margin-top: auto; border-top: 1px solid #3a3a3a; padding-top: 12px;">
                                {publisher}
                            </div>
                        </div>
                        """
                        st.markdown(card_html, unsafe_allow_html=True)
        else:
            st.info("No news articles available for the selected stocks at this time.")
            st.caption(f"Attempted to load news for: {', '.join(tickers)}")
            
    except Exception as e:
        st.warning(f"Unable to load news articles. Error: {str(e)}")
        st.caption("News feature may not be available for all tickers or may be temporarily unavailable.")
else:
    st.info("Select at least one stock to view news articles.")
