import sqlite3


def iniciar_banco(caminho) -> None:
    conexao = sqlite3.connect(caminho)

    conexao.execute("""
        CREATE TABLE IF NOT EXISTS mensagens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero TEXT, papel TEXT, texto TEXT
        )
    """)
    conexao.commit()

    conexao.close()

def salvar_mensagem(caminho, numero: str, papel: str, texto: str) -> None:
    conexao = sqlite3.connect(caminho)

    conexao.execute(
        "INSERT INTO mensagens (numero, papel, texto) VALUES (?, ?, ?)",
        (numero, papel, texto),
        )
    conexao.commit()

    conexao.close()

def buscar_historico(caminho, numero: str, limite: int = 10) -> list:
    conexao = sqlite3.connect(caminho)
    buscar = conexao.execute("""
            SELECT papel, texto 
            FROM mensagens
            WHERE numero = ?
            ORDER BY id DESC LIMIT ?
    """, (numero, limite))

    res = buscar.fetchall()
    
    conexao.close()

    return res[::-1]