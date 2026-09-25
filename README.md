**English** · [Português (Brasil)](README.pt-BR.md)

# ai-crawler-log-parser

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE) ![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg) [![Data: CC BY 4.0](https://img.shields.io/badge/Data-CC%20BY%204.0-lightgrey.svg)](#license)

`ai-crawler-log-parser` is a free, open source tool that reads a server
log (Apache or Nginx combined log format) and shows how many times each
known AI bot hit the site: number of hits, first and last access, and a
sample of the paths visited. It splits the results by category, AI search
bots (retrieval) and training and collection bots. It runs locally and no
data leaves your machine.

## Contents

- [Background](#background)
- [Installation](#installation)
- [Usage](#usage)
- [FAQ](#faq)
- [Limitations](#limitations)
- [Methodology](#methodology)
- [Contributing](#contributing)
- [Author](#author)
- [License](#license)

## Background

"Are ChatGPT, Claude, Perplexity and the others actually crawling my
site?" A traditional SEO audit does not cover this, because it looks at
the SERP and Search Console, not at the raw server log.

**Important guard rail: this is proof of reading, not proof of
citation.** The log shows that the bot fetched the page. It does not and
cannot show whether that content became part of an AI-generated answer.
That information does not exist in any log.

## Installation

Python 3.9 or newer, standard library only. No external dependencies.

```bash
git clone https://github.com/LucasFerrazSEO/ai-crawler-log-parser.git
cd ai-crawler-log-parser
```

## Usage

**1. Run it against your log file.**

```bash
python ai_crawler_log_parser.py access.log
```

**2. Or process a compressed log directly**, without unpacking it first:

```bash
zcat access.log.gz | python ai_crawler_log_parser.py -
```

**3. Read the result.** Real output from a three-line log with two bot
hits. The tool prints its report in Brazilian Portuguese.

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

**4. Filter by category** if you only want the search bots (real-time
retrieval) or only the training bots:

```bash
python ai_crawler_log_parser.py access.log --categoria busca
```

**5. Filter by path** to find out whether a bot is reading a specific
section of the site (the blog, for example):

```bash
python ai_crawler_log_parser.py access.log --caminho-contem /blog/
```

**6. Show more sample paths per bot** (default: 3):

```bash
python ai_crawler_log_parser.py access.log --amostra 10
```

## FAQ

**Is ai-crawler-log-parser really free?**
Yes. It is open source under the MIT license. The bot data
(`ai_bots.json`) is CC BY 4.0.

**Where do I find my server log?**
It depends on your hosting. On a VPS with Apache or Nginx it is usually at
`/var/log/apache2/access.log` or `/var/log/nginx/access.log`. On shared or
managed hosting, look for "access logs" or "raw logs" in the control
panel.

**Do I need an internet connection to use it?**
No. The tool only reads the local log file; no data leaves your machine.

**Can a bot lie in its user agent?**
Yes. Detection is a substring match on the declared user agent, and a
malicious client can forge that header. This is not IP or ASN
verification, it is a reading of what the server received.

## Limitations

It covers the standard Apache/Nginx combined log format. Logs in other
formats (structured JSON, CloudFront, Cloudflare Logpush) need to be
converted before you use them here.

## Methodology

The bot list (`ai_bots.json`) is a manually synced copy of the
[`ai-bots-list`](https://github.com/LucasFerrazSEO/ai-bots-list)
repository. If you already use that repository, you can point
`--bots-json` at its version instead of this copy.

## Contributing

Bug reports and suggestions are welcome through [GitHub Issues](https://github.com/LucasFerrazSEO/ai-crawler-log-parser/issues).

## Author

[Lucas Ferraz](https://lucasferraz.com) is an SEO, website development and Generative Engine Optimization specialist and the founder of [Lucas Ferraz SEO](https://lucasferrazseo.com).

## License

MIT. See [LICENSE](LICENSE). The bot data in `ai_bots.json` is licensed
under CC BY 4.0, see
[ai-bots-list](https://github.com/LucasFerrazSEO/ai-bots-list).
