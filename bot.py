import discord
from discord.ext import commands
import chess
from bot_logic import *

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

games = {}

@bot.event
async def on_ready():
    print(f'Hemos iniciado sesión como {bot.user}')

@bot.command()
async def hello(ctx):
    await ctx.send("Hi!")

@bot.command()
async def bye(ctx):
    await ctx.send(":(")

@bot.command()
async def password(ctx):
    await ctx.send(gen_pass(10))

@bot.command()
async def smile(ctx):
    await ctx.send(gen_emodji())

@bot.command()
async def coin(ctx):
    await ctx.send(flip_coin())

@bot.command()
async def start_chess(ctx):
    global games
    if ctx.author.id in games:
        await ctx.send("Ya tienes una partida en curso.")
    else:
        games[ctx.author.id] = chess.Board()
        await ctx.send("Se ha iniciado una nueva partida de ajedrez. Haz tu primer movimiento usando $move <jugada>. El formato de jugada es en notación estándar, como e2e4.")

@bot.command()
async def move(ctx, move: str):
    global games
    if ctx.author.id not in games:
        await ctx.send("No tienes una partida en curso. Inicia una con $start_chess.")
        return
    
    board = games[ctx.author.id]
    try:
        chess_move = chess.Move.from_uci(move)
        if chess_move in board.legal_moves:
            board.push(chess_move)
            await ctx.send(f"Movimiento realizado: {move}\n{board}")
        else:
            await ctx.send("Movimiento ilegal. Intenta de nuevo.")
    except ValueError:
        await ctx.send("Formato de movimiento inválido. Usa el formato estándar, como e2e4.")

@bot.command()
async def show_board(ctx):
    global games
    if ctx.author.id not in games:
        await ctx.send("No tienes una partida en curso. Inicia una con $start_chess.")
    else:
        board = games[ctx.author.id]
        await ctx.send(f"Tablero actual:\n```\n{board}\n```")

@bot.command()
async def resign(ctx):
    global games
    if ctx.author.id in games:
        del games[ctx.author.id]
        await ctx.send("Te has rendido. La partida ha terminado.")
    else:
        await ctx.send("No tienes una partida en curso.")

bot.run("MTI4NTI1NDI5ODkyNTY2NjM0NA.Gjo_x6.Mz1sSjNvkHQk2AXkh9dAvwfra9HR4U60FzBTXg")