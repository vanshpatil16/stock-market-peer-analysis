"""One-click PDF portfolio review. Pure-Python via reportlab."""
from __future__ import annotations
import io
from datetime import date
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, Image)
from reportlab.lib.styles import getSampleStyleSheet


def _metrics_rows(m):
    return [
        ["Total return", f"{m.total_return*100:.2f}%"],
        ["Annualized return", f"{m.annualized_return*100:.2f}%"],
        ["Annualized volatility", f"{m.annualized_volatility*100:.2f}%"],
        ["Sharpe ratio", f"{m.sharpe:.2f}"],
        ["Sortino ratio", f"{m.sortino:.2f}"],
        ["Max drawdown", f"{m.max_drawdown*100:.2f}%"],
        ["95% VaR (historical)", f"{m.hist_var*100:.2f}%"],
        ["95% CVaR", f"{m.cvar*100:.2f}%"],
        ["Beta vs benchmark", f"{m.beta:.2f}"],
    ]


def build_pdf(portfolio, metrics, narrative, chart_pngs=None) -> bytes:
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, title="WealthLens Portfolio Review")
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("WealthLens — Portfolio Review", styles["Title"]))
    story.append(Paragraph(date.today().isoformat(), styles["Normal"]))
    story.append(Spacer(1, 0.6 * cm))

    story.append(Paragraph("Holdings", styles["Heading2"]))
    holdings = [["Ticker", "Weight"]] + [
        [t, f"{w*100:.1f}%"] for t, w in zip(portfolio.tickers, portfolio.weights)]
    h_table = Table(holdings, hAlign="LEFT")
    h_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0E1626")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    story.append(h_table)
    story.append(Spacer(1, 0.5 * cm))

    story.append(Paragraph("Risk & performance metrics", styles["Heading2"]))
    m_table = Table([["Metric", "Value"]] + _metrics_rows(metrics), hAlign="LEFT")
    m_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0E1626")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    story.append(m_table)
    story.append(Spacer(1, 0.5 * cm))

    story.append(Paragraph("AI commentary", styles["Heading2"]))
    story.append(Paragraph(narrative, styles["Normal"]))

    for _, png in (chart_pngs or {}).items():
        story.append(Spacer(1, 0.4 * cm))
        story.append(Image(io.BytesIO(png), width=15 * cm, height=8 * cm))

    doc.build(story)
    return buf.getvalue()
