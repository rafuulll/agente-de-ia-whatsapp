from app.memoria import buscar_historico, iniciar_banco, salvar_mensagem


def test_salva_e_busca_na_ordem(tmp_path):
    banco = tmp_path / "teste.db"
    iniciar_banco(banco)

    salvar_mensagem(banco, "5515000000001", "cliente", "quero cílios")
    salvar_mensagem(banco, "5515000000001", "agente", "temos fio a fio")

    assert buscar_historico(banco, "5515000000001") == [
        ("cliente", "quero cílios"),
        ("agente", "temos fio a fio"),
    ]


def test_numeros_diferentes_nao_se_misturam(tmp_path):
    banco = tmp_path / "teste.db"
    iniciar_banco(banco)

    salvar_mensagem(banco, "5515000000001", "cliente", "quero cílios")
    salvar_mensagem(banco, "5515000000002", "cliente", "quero sobrancelha")

    assert buscar_historico(banco, "5515000000001") == [("cliente", "quero cílios")]


def test_limite_devolve_so_as_ultimas(tmp_path):
    banco = tmp_path / "teste.db"
    iniciar_banco(banco)
    for i in range(5):
        salvar_mensagem(banco, "5515000000001", "cliente", f"mensagem {i}")

    assert buscar_historico(banco, "5515000000001", limite=2) == [("cliente", "mensagem 3"), ("cliente", "mensagem 4")]