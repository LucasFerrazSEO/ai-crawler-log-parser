[English](README.md) · **Português (Brasil)**

# ai-crawler-log-parser

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE) ![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg) [![Data: CC BY 4.0](https://img.shields.io/badge/Data-CC%20BY%204.0-lightgrey.svg)](#licença)

`ai-crawler-log-parser` é uma ferramenta gratuita e de código aberto que
lê um log de servidor (formato combined, Apache ou Nginx) e mostra quantas
vezes cada bot de IA conhecido bateu no site: quantidade de hits, primeiro
e último acesso, e uma amostra dos caminhos visitados. Separa por
categoria, bots de busca com IA (retrieval) e bots de treinamento e
coleta. Roda localmente e nenhum dado sai da sua máquina.

## Sumário

- [Contexto](#contexto)
- [Instalação](#instalação)
- [Uso](#uso)
- [Perguntas frequentes](#perguntas-frequentes)
- [Limitações](#limitações)
- [Método e origem](#método-e-origem)
- [Como contribuir](#como-contribuir)
- [Autor](#autor)
- [Licença](#licença)

## Contexto

"O ChatGPT, o Claude, a Perplexity e os outros estão de fato passando pelo
meu site?" É uma checagem que uma auditoria de SEO tradicional não cobre,
porque olha para SERP e Search Console, não para o log bruto do servidor.

**Guard-rail importante: isto é prova de leitura, não prova de citação.**
O log mostra que o bot passou pela página. Não mostra, e não pode mostrar,
se aquele conteúdo virou parte de uma resposta gerada por IA. Essa
informação não existe em log nenhum.

## Instalação

Python 3.9 ou mais recente, só biblioteca padrão. Sem dependência externa.

```bash
git clone https://github.com/LucasFerrazSEO/ai-crawler-log-parser.git
cd ai-crawler-log-parser
```

## Uso

**1. Rode contra o seu arquivo de log.**

```bash
python ai_crawler_log_parser.py access.log
```

**2. Ou processe um log compactado direto**, sem descompactar antes:

```bash
zcat access.log.gz | python ai_crawler_log_parser.py -
```

**3. Leia o resultado.** Exemplo real, de um log de três linhas com dois
hits de bot:

```
=== ai-crawler-log-parser: access.log ===
3 linha(s) lida(s), 0 fora do formato combined log

-- TREINAMENTO E COLETA --
  GPTBot                   Coleta para treinamento               1 hit(s)  24/Sep/2026:10:05:00 +0000 -> 24/Sep/2026:10:05:00 +0000
      /
  ClaudeBot                Coleta para treinamento               1 hit(s)  24/Sep/2026:10:00:00 +0000 -> 24/Sep/2026:10:00:00 +0000
      /blog/post-x/

(Prova de leitura pelo bot, não prova de citação em uma resposta de IA.)
```

**4. Filtre por categoria**, se quiser ver só bots de busca (retrieval em
tempo real) ou só os de treinamento:

```bash
python ai_crawler_log_parser.py access.log --categoria busca
```

**5. Filtre por caminho**, para saber se um bot específico está lendo uma
seção do site (por exemplo, o blog):

```bash
python ai_crawler_log_parser.py access.log --caminho-contem /blog/
```

**6. Aumente a amostra de caminhos mostrados por bot** (padrão: 3):

```bash
python ai_crawler_log_parser.py access.log --amostra 10
```

## Perguntas frequentes

**ai-crawler-log-parser é realmente grátis?**
Sim, código aberto sob licença MIT. Os dados de bots (`ai_bots.json`) são
CC BY 4.0.

**Onde encontro o log do meu servidor?**
Depende da hospedagem. Em VPS com Apache/Nginx, geralmente em
`/var/log/apache2/access.log` ou `/var/log/nginx/access.log`. Em
hospedagem compartilhada ou gerenciada, procure por "logs de acesso" ou
"raw logs" no painel.

**Preciso de internet para usar?**
Não. A ferramenta só lê o arquivo de log local; nenhum dado sai da sua
máquina.

**O bot pode estar mentindo no user agent?**
Pode. A detecção é por substring do user agent declarado, e um cliente
mal-intencionado consegue forjar esse cabeçalho. Isto não é verificação de
IP/ASN, é leitura do que o servidor recebeu.

## Limitações

Cobre o formato combined log padrão de Apache/Nginx. Log em outro formato
(JSON estruturado, CloudFront, Cloudflare Logpush) precisa ser convertido
antes de usar aqui.

## Método e origem

A lista de bots (`ai_bots.json`) é uma cópia sincronizada manualmente do
repositório [`ai-bots-list`](https://github.com/LucasFerrazSEO/ai-bots-list).
Se você já usa aquele repositório, pode apontar `--bots-json` para a
versão dele em vez desta cópia.

## Como contribuir

Relatos de erro e sugestões são bem-vindos pelas [Issues do GitHub](https://github.com/LucasFerrazSEO/ai-crawler-log-parser/issues).

## Autor

[Lucas Ferraz](https://lucasferraz.com) é especialista em SEO, criação de sites e Generative Engine Optimization e fundador da [Lucas Ferraz SEO](https://lucasferrazseo.com).

## Licença

MIT. Veja o arquivo [LICENSE](LICENSE). Os dados de bots em
`ai_bots.json` estão sob CC BY 4.0, veja
[ai-bots-list](https://github.com/LucasFerrazSEO/ai-bots-list).
