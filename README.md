# KioBot

Bot de Discord que funciona como cronômetro com áudios aleatórios em calls de voz. Você pede um tempo, ele entra na call e toca um áudio quando o tempo acaba.

Feito do zero, sem experiência prévia em programação. Esse README documenta o processo completo — o que funcionou, o que não funcionou, e por quê.

---

## O que ele faz

Você manda uma mensagem mencionando o bot com um comando. Ele responde, aguarda o tempo pedido, entra no canal de voz onde você está, toca um MP3 aleatório da pasta de áudios e sai. Simples assim.

O modo aleatório permite configurar um intervalo fixo e um número de repetições. O bot vai repetir o ciclo entra-toca-sai quantas vezes você pedir.

---

## Comandos

| Comando | O que faz |
|---|---|
| `@KioBot 20m` | Toca um áudio após 20 minutos |
| `@KioBot 1h` | Toca um áudio após 1 hora |
| `@KioBot aleatório` | Pergunta o intervalo em minutos e quantas vezes tocar |
| `@KioBot tocar` | Toca um áudio imediatamente |
| `@KioBot me mostre os áudios` | Lista todos os MP3s disponíveis |
| `@KioBot quero que toque (nome)` | Define qual áudio vai tocar na próxima vez |
| `@KioBot reiniciar` | Cancela tudo que está na fila |
| `@KioBot ajuda` | Mostra todos os comandos |

**Modo aleatório em detalhe:**

Quando você manda `@KioBot aleatório`, o bot faz duas perguntas em sequência. Primeira: a cada quantos minutos quer que ele toque? Aceita de 1 a 60. Segunda: quantas vezes quer que ele repita? Aceita de 1 a 10. Se você extrapolar os limites, ele avisa e pergunta de novo. Depois de confirmar os dois valores, ele agenda tudo e executa na ordem.

Limite de 5 cronômetros simultâneos por servidor. `@KioBot reiniciar` cancela todos de uma vez.

---

## Como rodar no seu PC

Essa é a forma mais simples e a que funcionou. O bot roda na sua máquina enquanto a janela estiver aberta. Fechar a janela desliga o bot. Nenhum processo fica em segundo plano.

### Requisitos

- Python 3.11 — versão obrigatória. Versões mais novas (3.12, 3.13, 3.14) têm incompatibilidade com a biblioteca de voz do discord.py. Mais detalhes na seção de problemas.
- FFmpeg — necessário para reproduzir os arquivos MP3.

### Passo a passo

**1. Instale o Python 3.11**

Baixe em https://www.python.org/downloads/release/python-3119/ e escolha "Windows installer (64-bit)". Durante a instalação, marque a opção "Add Python to PATH".

**2. Instale o FFmpeg**

Baixe o arquivo `ffmpeg-release-essentials.zip` em https://www.gyan.dev/ffmpeg/builds/. Descompacte e copie a pasta `bin` para `C:\ffmpeg`. Depois abra o Prompt de Comando como Administrador e rode:

```
setx /M PATH "C:\ffmpeg\bin;%PATH%"
```

Feche e abra o CMD de novo. Teste com `ffmpeg -version`.

**3. Instale as dependências do bot**

```
py -3.11 -m pip install "discord.py[voice]" PyNaCl
```

**4. Clone o repositório**

```
git clone https://github.com/KioHype/KioBot
cd KioBot
```

**5. Configure o token**

Abra o arquivo `bot.py` e substitua `SEU_TOKEN_AQUI` pelo token do seu bot. Para obter o token:

- Acesse https://discord.com/developers/applications
- Crie uma aplicação, vá em "Bot"
- Ative os três Privileged Gateway Intents (Presence, Server Members, Message Content)
- Clique em "Reset Token" e copie

**6. Adicione seus áudios**

Coloque seus arquivos MP3 dentro da pasta `audios/`.

**7. Convide o bot para o seu servidor**

No portal do desenvolvedor, vá em OAuth2, marque o escopo "bot" e as permissões: Send Messages, View Channels, Connect, Speak, View Message History. Copie o link gerado e abra no navegador.

**8. Configure a região do canal de voz**

Clique com botão direito no canal de voz, vá em "Editar canal" e mude a região para "US East" ou "US South". Isso evita problemas de conexão que acontecem com o servidor de voz de São Paulo.

**9. Inicie o bot**

Clique duas vezes no arquivo `Iniciar KioBot.bat`. Para desligar, feche a janela preta.

---

## Como hospedar na nuvem

Se você quer o bot rodando sem precisar manter o computador ligado, as opções são limitadas para quem não quer pagar.

**Railway — recomendado se for pagar**

Custa aproximadamente $5 por mês. É a opção mais simples: conecte o repositório GitHub, adicione a variável de ambiente `DISCORD_TOKEN` com o token do bot, e o deploy é automático. IP limpo, sem problemas de conexão de voz.

**Oracle Cloud — gratuito**

Gratuito para sempre com uma VM de capacidade razoável. O processo de cadastro é burocrático e exige cartão de crédito para verificação (sem cobrança). Uma vez configurado, funciona bem. Não é para quem não tem paciência com setup.

---

## O que não funcionou e por quê

Essa seção existe porque a maior parte da documentação de bots de Discord não fala sobre os problemas reais de hospedagem gratuita. Aqui está o que aconteceu na prática.

**Discloud e HeavenCloud**

Ambos têm plano gratuito e são específicos para bots de Discord. O bot subia, ficava online, respondia mensagens de texto normalmente. O problema aparecia na hora de entrar em calls de voz: o erro `WebSocket closed with 4006` aparecia consistentemente após alguns segundos de tentativa de conexão.

O código não tinha bug. O problema é que o Discord bloqueia conexões de voz vindas de IPs conhecidos de servidores gratuitos de hospedagem. Não há solução para isso sem mudar de servidor ou pagar por um IP diferente.

**Render**

Tinha plano gratuito anteriormente. Removeu a opção gratuita para workers. O plano mais barato hoje é $7 por mês.

**bot-hosting.net**

Usa sistema de moedas diárias para criar servidores. O limite gratuito diário é insuficiente para criar qualquer plano funcional sem pagar.

**Fly.io**

Exige cartão de crédito para verificação mesmo no plano gratuito. Não testado além do cadastro.

**Python 3.14**

O discord.py não tem suporte completo para voz no Python 3.14. O bot conectava no canal de voz, mas perdia a conexão antes de conseguir tocar qualquer áudio. O erro era o mesmo 4006, mas a causa era diferente: incompatibilidade interna da biblioteca com a versão do Python, não bloqueio de IP.

A solução foi instalar o Python 3.11 em paralelo com o 3.14 e rodar o bot especificamente com `py -3.11`.

**Servidor de voz de São Paulo**

Mesmo com Python 3.11 e IP limpo, o servidor de voz `c-gru13` de São Paulo causava erros 4006. Mudar a região do canal de voz para US East resolveu o problema.

---

## Estrutura do projeto

```
KioBot/
├── bot.py                    # Código principal
├── requirements.txt          # Dependências Python
├── Iniciar KioBot.bat        # Atalho para iniciar no Windows
├── audios/                   # Pasta dos arquivos MP3
└── README.md
```

---

## Tecnologias

- Python 3.11
- discord.py com suporte a voz
- FFmpeg

---

## Canal do criador

[SEU CANAL AQUI]
