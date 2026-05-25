import discord
import asyncio
import random
import os
import re

# ─────────────────────────────────────────
#  CONFIGURAÇÃO — coloque seu token aqui
# ─────────────────────────────────────────
TOKEN = "SEU_TOKEN_AQUI"

PASTA_AUDIOS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "audios")
LIMITE_COMANDOS = 5


intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
intents.guilds = True

bot = discord.Client(intents=intents)

estado = {}


def get_estado(gid):
    if gid not in estado:
        estado[gid] = {"tasks": [], "proximo_audio": None}
    return estado[gid]


def listar_audios():
    try:
        if not os.path.exists(PASTA_AUDIOS):
            os.makedirs(PASTA_AUDIOS)
        return [f for f in os.listdir(PASTA_AUDIOS) if f.lower().endswith(".mp3")]
    except Exception as ex:
        print(f"Erro ao listar áudios: {ex}")
        return []


def pegar_audio(gid):
    e = get_estado(gid)
    forcado = e.get("proximo_audio")
    if forcado:
        e["proximo_audio"] = None
        caminho = os.path.join(PASTA_AUDIOS, forcado)
        if os.path.exists(caminho):
            return caminho
    arquivos = listar_audios()
    if not arquivos:
        return None
    return os.path.join(PASTA_AUDIOS, random.choice(arquivos))


async def entrar_e_tocar(gid, canal_voz, canal_texto):
    audio = pegar_audio(gid)
    if audio is None:
        await canal_texto.send("⚠️ Nenhum áudio encontrado na pasta `audios/`.")
        return

    vc = None
    try:
        guild = canal_voz.guild
        if guild.voice_client:
            await guild.voice_client.disconnect(force=True)
            await asyncio.sleep(2)

        print(f"🎵 Conectando em: {canal_voz.name}")
        vc = await canal_voz.connect()
        await asyncio.sleep(1)

        print(f"▶️ Tocando: {audio}")
        source = discord.FFmpegPCMAudio(audio)
        vc.play(source)

        while vc.is_playing():
            await asyncio.sleep(1)

        await asyncio.sleep(1)
        print("✅ Áudio tocado com sucesso!")

    except Exception as ex:
        print(f"❌ Erro: {ex}")
        await canal_texto.send(f"⚠️ Erro: {ex}")
    finally:
        try:
            if vc and vc.is_connected():
                await vc.disconnect()
        except:
            pass


@bot.event
async def on_ready():
    print(f"✅ KioBot online como {bot.user}")
    print(f"📂 Pasta de áudios: {PASTA_AUDIOS}")
    print(f"🎵 Áudios encontrados: {listar_audios()}")
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.listening,
        name="@KioBot ajuda"
    ))


@bot.event
async def on_message(message):
    if message.author.bot:
        return
    if bot.user not in message.mentions:
        return

    conteudo = message.content.replace(f"<@{bot.user.id}>", "").replace(f"<@!{bot.user.id}>", "").strip().lower()
    gid = message.guild.id
    canal_texto = message.channel
    e = get_estado(gid)

    # ── OI ─────────────────────────────────────────────
    if conteudo in ("oi", "olá", "ola", "hey", "e aí", "e ai", "salve"):
        await canal_texto.send("Pode falar, seu bunda mole 😤")
        return

    # ── AJUDA ──────────────────────────────────────────
    if conteudo in ("ajuda", "help", ""):
        embed = discord.Embed(title="🎵 KioBot — Comandos", color=0x5865F2)
        embed.add_field(name="@KioBot 20m / 1h", value="Toca um áudio após o tempo definido.", inline=False)
        embed.add_field(name="@KioBot aleatório", value="Pergunta o intervalo e quantas vezes tocar.", inline=False)
        embed.add_field(name="@KioBot tocar", value="Toca um áudio imediatamente.", inline=False)
        embed.add_field(name="@KioBot me mostre os áudios", value="Mostra todos os MP3s disponíveis.", inline=False)
        embed.add_field(name="@KioBot quero que toque (nome)", value="Define qual áudio vai tocar na próxima vez.", inline=False)
        embed.add_field(name="@KioBot reiniciar", value="Cancela tudo e reinicia.", inline=False)
        embed.set_footer(text="Limite: 5 comandos simultâneos por servidor.")
        await canal_texto.send(embed=embed)
        return

    # ── TOCAR IMEDIATO ─────────────────────────────────
    if conteudo == "tocar":
        canal_voz = message.author.voice.channel if message.author.voice else None
        if canal_voz is None:
            await canal_texto.send("❌ Você precisa estar em um canal de voz!")
            return
        await canal_texto.send("🎵 Tocando agora!")
        await entrar_e_tocar(gid, canal_voz, canal_texto)
        return

    # ── MOSTRAR ÁUDIOS ─────────────────────────────────
    if "mostre os áudio" in conteudo or "mostre os audio" in conteudo or "listar" in conteudo or "quais áudio" in conteudo or "quais audio" in conteudo:
        arquivos = listar_audios()
        if not arquivos:
            await canal_texto.send("⚠️ Nenhum áudio disponível ainda.")
            return
        lista = "\n".join(f"🎵 `{f}`" for f in arquivos)
        await canal_texto.send(f"**Áudios disponíveis:**\n{lista}")
        return

    # ── QUERO QUE TOQUE ────────────────────────────────
    match_toque = re.search(r"quero que toque\s*[\(\[]?(.+?)[\)\]]?\s*$", conteudo)
    if match_toque:
        nome_pedido = match_toque.group(1).strip()
        arquivos = listar_audios()
        encontrado = next((f for f in arquivos if nome_pedido.lower() in f.lower()), None)
        if encontrado:
            e["proximo_audio"] = encontrado
            await canal_texto.send(f"✅ O próximo áudio será: `{encontrado}` 🎵")
        else:
            lista = "\n".join(f"`{f}`" for f in arquivos)
            await canal_texto.send(f"❌ Não encontrado. Disponíveis:\n{lista}")
        return

    # ── REINICIAR ──────────────────────────────────────
    if conteudo in ("parar", "stop", "reiniciar", "reset", "sair daqui", "sair"):
        for t in e["tasks"]:
            t.cancel()
        e["tasks"] = []
        e["proximo_audio"] = None
        if message.guild.voice_client:
            await message.guild.voice_client.disconnect(force=True)
        await canal_texto.send("🔄 Reiniciado! Tudo cancelado.")
        return

    # ── MODO ALEATÓRIO ─────────────────────────────────
    if conteudo in ("aleatório", "aleatorio", "random"):
        canal_voz = message.author.voice.channel if message.author.voice else None
        if canal_voz is None:
            await canal_texto.send("❌ Você precisa estar em um canal de voz!")
            return

        # Pergunta os minutos
        await canal_texto.send("🎲 Modo aleatório! A cada quantos minutos quer que eu toque um áudio?")

        def check_numero(m):
            return m.author == message.author and m.channel == canal_texto and m.content.strip().isdigit()

        # Loop para validar minutos
        while True:
            try:
                resp_min = await bot.wait_for("message", check=check_numero, timeout=30)
            except asyncio.TimeoutError:
                await canal_texto.send("⏰ Tempo esgotado!")
                return

            minutos = int(resp_min.content.strip())
            if 1 <= minutos <= 60:
                break
            await canal_texto.send("❌ O intervalo precisa ser entre 1 e 60 minutos. Tente de novo:")

        # Pergunta as vezes
        await canal_texto.send(f"✅ A cada **{minutos} minutos**! Quantas vezes quer que eu toque?")

        # Loop para validar vezes
        while True:
            try:
                resp_vez = await bot.wait_for("message", check=check_numero, timeout=30)
            except asyncio.TimeoutError:
                await canal_texto.send("⏰ Tempo esgotado!")
                return

            vezes = int(resp_vez.content.strip())
            if 1 <= vezes <= 10:
                break
            await canal_texto.send("❌ O número de vezes precisa ser entre 1 e 10. Tente de novo:")

        segundos = minutos * 60
        await canal_texto.send(f"✅ Vou tocar **{vezes} vez(es)** a cada **{minutos} minuto(s)**. agora é só questão de tempo... 👀")

        async def tarefa_aleatoria():
            for i in range(vezes):
                await asyncio.sleep(segundos)
                await entrar_e_tocar(gid, canal_voz, canal_texto)
                if i < vezes - 1:
                    print(f"🔁 Tocou {i+1}/{vezes}. Próximo em {minutos} minutos.")

        e["tasks"] = [t for t in e["tasks"] if not t.done()]
        if len(e["tasks"]) >= LIMITE_COMANDOS:
            await canal_texto.send(f"🚫 Já estou com {LIMITE_COMANDOS} cronômetros na fila!")
            return

        task = asyncio.create_task(tarefa_aleatoria())
        e["tasks"].append(task)
        return

    # ── TEMPO FIXO ─────────────────────────────────────
    match = re.fullmatch(r"(\d+)\s*(m|min|minutos?|h|horas?)", conteudo)
    if match:
        valor = int(match.group(1))
        unidade = match.group(2)

        if unidade.startswith("h"):
            segundos = valor * 3600
            label = f"{valor}h"
        else:
            segundos = valor * 60
            label = f"{valor} minuto(s)"

        canal_voz = message.author.voice.channel if message.author.voice else None
        if canal_voz is None:
            await canal_texto.send("❌ Você precisa estar em um canal de voz!")
            return

        e["tasks"] = [t for t in e["tasks"] if not t.done()]
        if len(e["tasks"]) >= LIMITE_COMANDOS:
            await canal_texto.send(f"🚫 Já estou com {LIMITE_COMANDOS} cronômetros na fila!")
            return

        await canal_texto.send(f"⏱️ Cronômetro de **{label}** iniciado! agora é só questão de tempo... 👀")

        async def tarefa_tempo():
            await asyncio.sleep(segundos)
            await entrar_e_tocar(gid, canal_voz, canal_texto)

        task = asyncio.create_task(tarefa_tempo())
        e["tasks"].append(task)
        return

    # ── COMANDO NÃO RECONHECIDO ────────────────────────
    await canal_texto.send("❓ Não entendi esse comando. Manda `@KioBot ajuda` para ver o que eu sei fazer!")


bot.run(TOKEN)
