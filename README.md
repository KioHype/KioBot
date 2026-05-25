# KioBot 

> Um bot de Discord que funciona como cronômetro com áudios aleatórios em calls de voz.

---

## O que é isso?

KioBot é um bot de Discord simples com um propósito muito específico: você pede um tempo, ele entra na call e toca um áudio aleatório quando o tempo acaba.

---

## Como surgiu

A ideia começou com uma necessidade real: ter um cronômetro que avisasse com áudio em chamadas de voz no Discord, sem depender de ninguém lembrar de verificar o tempo.

O desenvolvimento foi feito do zero, sem experiência prévia em programação. Todo o processo — desde a concepção até o código — foi construído iterativamente, resolvendo um problema de cada vez.

**O que funcionou:**
- Estrutura de comandos via menção (`@KioBot`)
- Sistema de fila com até 5 cronômetros simultâneos
- Seleção aleatória de áudios MP3
- Modo aleatório com intensidades (baixa, média, alta)
- Hospedagem e deploy do código

**O que não funcionou:**
- Hospedagem gratuita em nuvem para bots de voz — a maioria dos serviços gratuitos (HeavenCloud, Discloud) tem IPs bloqueados pelo Discord para conexões de voz. Não é bug do código, é uma limitação real do ecossistema de hospedagem gratuita.

**Conclusão:** bots que tocam áudio em calls precisam de um servidor com IP limpo. As opções gratuitas não entregam isso de forma confiável.

---

## Comandos

| Comando | O que faz |
|---|---|
| `@KioBot xm` | Toca um áudio após x minutos |
| `@KioBot xh` | Toca um áudio após x hora |
| `@KioBot aleatório` | Pergunta a intensidade e toca após intervalo aleatório |
| `@KioBot tocar` | Toca um áudio imediatamente |
| `@KioBot me mostre os áudios` | Lista os MP3s disponíveis |
| `@KioBot quero que toque (nome)` | Define qual áudio toca na próxima vez |
| `@KioBot parar` | Para o modo aleatório |
| `@KioBot reiniciar` | Cancela todos os cronômetros |
| `@KioBot sair daqui` | Sai da call imediatamente |
| `@KioBot ajuda` | Mostra todos os comandos |

---

## Como rodar no seu PC

### Requisitos
- Python 3.10 ou superior
- FFmpeg instalado no sistema

### Instalação

**1. Clone o repositório**
```
git clone https://github.com/KioHype/KioBot
cd KioBot
```

**2. Instale as dependências**
```
pip install -r requirements.txt
```

**3. Configure o token**

Abra o arquivo `bot.py` e substitua o token na linha:
```python
TOKEN = "SEU_TOKEN_AQUI"
```

**4. Adicione seus áudios**

Coloque seus arquivos MP3 dentro da pasta `audios/`.

**5. Inicie o bot**

No Windows, clique duas vezes no arquivo `Iniciar KioBot.bat`.

Ou pelo terminal:
```
python bot.py
```

---

## Como hospedar na nuvem (opção paga)

Se você não quer depender do seu PC estar ligado, a opção mais simples e barata é o **Railway**.

- Acesse [railway.app](https://railway.app)
- Conecte seu repositório do GitHub
- Adicione a variável de ambiente `DISCORD_TOKEN` com o token do seu bot
- Deploy automático

Custo aproximado: **$5/mês**.

Outras opções testadas e suas limitações:
- **Discloud** — gratuito, mas IP bloqueado pelo Discord para voz
- **HeavenCloud** — gratuito, mesmo problema de IP
- **Render** — removeu plano gratuito para workers
- **Oracle Cloud** — gratuito para sempre, mas cadastro complexo

---

## Estrutura do projeto

```
KioBot/
├── bot.py                    # Código principal
├── requirements.txt          # Dependências Python
├── audios/                   # Pasta dos arquivos MP3
│   └── (coloque seus MP3s aqui)
├── Iniciar KioBot.bat        # Atalho para iniciar no Windows
└── README.md
```

---

## Tecnologias

- [Python 3](https://python.org)
- [discord.py](https://discordpy.readthedocs.io)
- [FFmpeg](https://ffmpeg.org)

---

## Autor

Feito por **Daniel Perin**  
Canal: [https://www.youtube.com/@KioHype]


---

*Código aberto para consulta e aprendizado. Sem executável para download.*
