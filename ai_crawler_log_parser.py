#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ai-crawler-log-parser — lê um log de servidor (formato common/combined,
Apache ou Nginx) e mostra quantas vezes cada bot de IA conhecido bateu no
site: quantidade de hits, primeiro e último acesso, e uma amostra dos
caminhos visitados.

O QUE FAZ
    Faz o parsing de linhas no formato combined log
    (`IP - - [data] "MÉTODO caminho PROTOCOLO" status tamanho "referer" "user-agent"`),
    extrai o user agent de cada linha e cruza com a lista de bots de IA
    conhecidos (`ai_bots.json`, mesma fonte do repositório ai-bots-list).
    O resultado é prova de LEITURA (o bot passou pelo site), nunca prova de
    citação — se a IA usou o conteúdo em uma resposta, isso não aparece em
    log nenhum.

USO
    python ai_crawler_log_parser.py access.log
    python ai_crawler_log_parser.py access.log --categoria busca
    python ai_crawler_log_parser.py access.log --caminho-contem /blog/
    python ai_crawler_log_parser.py access.log --bots-json outro-ai_bots.json
    zcat access.log.gz | python ai_crawler_log_parser.py -

LIMITAÇÕES
    Cobre o formato combined log padrão (Apache/Nginx). Log em formato
    diferente (JSON estruturado, CloudFront, Cloudflare Logpush) precisa ser
    convertido antes. Detecção de bot é por substring do user agent
    declarado — um cliente mal-intencionado pode forjar esse cabeçalho;
    isso não é verificação de IP/ASN.

Autor: Lucas Ferraz (lucasferraz.com) — dependência zero, só biblioteca padrão.
Licença do código: MIT. Licença dos dados (ai_bots.json): CC BY 4.0.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import defaultdict

LINHA_LOG = re.compile(
    r'(?P<ip>\S+) \S+ \S+ \[(?P<data>[^\]]+)\] '
    r'"(?P<metodo>\S+) (?P<caminho>\S+) \S+" '
    r'(?P<status>\d{3}) (?P<tamanho>\S+) '
    r'"(?P<referer>[^"]*)" "(?P<ua>[^"]*)"'
)


def carrega_bots(caminho: str) -> list[dict]:
    with open(caminho, encoding="utf-8") as fh:
        return json.load(fh)["bots"]


def identifica_bot(user_agent: str, bots: list[dict]) -> dict | None:
    for bot in bots:
        if bot["user_agent"] in user_agent:
            return bot
    return None


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Classifica hits de log de servidor por bot de IA conhecido."
    )
    ap.add_argument("log", help="arquivo de log (formato combined), ou '-' para entrada padrão")
    ap.add_argument("--categoria", choices=["busca", "treinamento"], default="",
                     help="filtra por categoria (padrão: mostra as duas)")
    ap.add_argument("--caminho-contem", default="",
                     help="só conta hits cujo caminho contém esta substring (ex.: /blog/)")
    ap.add_argument("--amostra", type=int, default=3, help="quantos caminhos de amostra mostrar por bot (padrão 3)")
    ap.add_argument("--bots-json", default=os.path.join(os.path.dirname(__file__), "ai_bots.json"),
                     help="caminho do ai_bots.json (padrão: a cópia deste repositório)")
    args = ap.parse_args()

    bots = carrega_bots(args.bots_json)
    if args.categoria:
        bots = [b for b in bots if b["categoria"] == args.categoria]

    contagem: dict[str, int] = defaultdict(int)
    primeiro: dict[str, str] = {}
    ultimo: dict[str, str] = {}
    caminhos: dict[str, list[str]] = defaultdict(list)
    linhas_lidas = 0
    linhas_sem_match = 0

    origem = sys.stdin if args.log == "-" else open(args.log, encoding="utf-8", errors="replace")
    with origem:
        for linha in origem:
            linhas_lidas += 1
            m = LINHA_LOG.search(linha)
            if not m:
                linhas_sem_match += 1
                continue
            if args.caminho_contem and args.caminho_contem not in m.group("caminho"):
                continue
            bot = identifica_bot(m.group("ua"), bots)
            if not bot:
                continue
            ua = bot["user_agent"]
            contagem[ua] += 1
            primeiro.setdefault(ua, m.group("data"))
            ultimo[ua] = m.group("data")
            if len(caminhos[ua]) < args.amostra:
                caminhos[ua].append(m.group("caminho"))

    print(f"\n=== ai-crawler-log-parser: {args.log} ===")
    print(f"{linhas_lidas} linha(s) lida(s), {linhas_sem_match} fora do formato combined log\n")

    if not contagem:
        print("Nenhum bot de IA conhecido encontrado no log.")
        return

    for categoria, rotulo in (("busca", "BUSCA COM IA"), ("treinamento", "TREINAMENTO E COLETA")):
        do_grupo = [b for b in bots if b["categoria"] == categoria and b["user_agent"] in contagem]
        if not do_grupo:
            continue
        print(f"-- {rotulo} --")
        for bot in sorted(do_grupo, key=lambda b: -contagem[b["user_agent"]]):
            ua = bot["user_agent"]
            print(f"  {ua:<24} {bot['produto']:<32} {contagem[ua]:>6} hit(s)  "
                  f"{primeiro[ua]} -> {ultimo[ua]}")
            for c in caminhos[ua]:
                print(f"      {c}")
        print()

    print("(Prova de leitura pelo bot, não prova de citação em uma resposta de IA.)")


if __name__ == "__main__":
    main()
