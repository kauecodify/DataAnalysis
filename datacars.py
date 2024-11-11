import tkinter as tk
import random

carros = [
    {"modelo": "Fusca", "ano": 1965, "valor": 15000, "status": random.choice(["Disponível", "Em Negociação", "Vendido"])},
    {"modelo": "Gol", "ano": 2010, "valor": 25000, "status": random.choice(["Disponível", "Em Negociação", "Vendido"])},
    {"modelo": "Civic", "ano": 2018, "valor": 60000, "status": random.choice(["Disponível", "Em Negociação", "Vendido"])},
    {"modelo": "Corolla", "ano": 2020, "valor": 90000, "status": random.choice(["Disponível", "Em Negociação", "Vendido"])},
    {"modelo": "Saveiro", "ano": 2015, "valor": 35000, "status": random.choice(["Disponível", "Em Negociação", "Vendido"])}
]

def atualizar_lista(status_filtro=None):
    for widget in frame_carros.winfo_children():
        widget.destroy()

    if status_filtro:
        carros_filtrados = [carro for carro in carros if carro["status"] == status_filtro]
    else:
        carros_filtrados = carros

    for carro in carros_filtrados:
        modelo = carro["modelo"]
        ano = carro["ano"]
        valor = carro["valor"]
        status = carro["status"]
        
        info = f"Modelo: {modelo} | Ano: {ano} | Valor: R${valor:,} | Status: {status}"
        label_carro = tk.Label(frame_carros, text=info, font=("Arial", 12), anchor="w", width=80)
        label_carro.pack(fill="x", pady=5)

def carros_em_negociacao():
    atualizar_lista(status_filtro="Em Negociação")

def carros_vendidos():
    atualizar_lista(status_filtro="Vendido")

def adicionar_carro():
    def salvar_novo_carro():
        modelo = entry_modelo.get()
        ano = int(entry_ano.get())
        valor = int(entry_valor.get())
        status = combo_status.get()

        novos_dados = {"modelo": modelo, "ano": ano, "valor": valor, "status": status}
        carros.append(novos_dados)
        adicionar_window.destroy()
        atualizar_lista()

    adicionar_window = tk.Toplevel(root)
    adicionar_window.title("Adicionar Novo Carro")
    adicionar_window.geometry("500x00")

    label_modelo = tk.Label(adicionar_window, text="Modelo:")
    label_modelo.pack(pady=5)
    entry_modelo = tk.Entry(adicionar_window)
    entry_modelo.pack(pady=5)

    label_ano = tk.Label(adicionar_window, text="Ano:")
    label_ano.pack(pady=5)
    entry_ano = tk.Entry(adicionar_window)
    entry_ano.pack(pady=5)

    label_valor = tk.Label(adicionar_window, text="Valor:")
    label_valor.pack(pady=5)
    entry_valor = tk.Entry(adicionar_window)
    entry_valor.pack(pady=5)

    label_status = tk.Label(adicionar_window, text="Status:")
    label_status.pack(pady=5)
    combo_status = tk.StringVar(adicionar_window)
    combo_status.set("Disponível")
    status_opcoes = ["Disponível", "Em Negociação", "Vendido"]
    combo = tk.OptionMenu(adicionar_window, combo_status, *status_opcoes)
    combo.pack(pady=5)

    botao_salvar = tk.Button(adicionar_window, text="Salvar", command=salvar_novo_carro)
    botao_salvar.pack(pady=10)

def remover_carro():
    def remover_selecionado():
        modelo_remover = combo_carros_remover.get()
        for carro in carros:
            if carro["modelo"] == modelo_remover:
                carros.remove(carro)
                break
        remover_window.destroy()
        atualizar_lista()

    remover_window = tk.Toplevel(root)
    remover_window.title("Remover Carro")
    remover_window.geometry("400x300")

    label_carros = tk.Label(remover_window, text="Escolha um carro para remover:")
    label_carros.pack(pady=5)

    modelos_carros = [carro["modelo"] for carro in carros]
    combo_carros_remover = tk.StringVar(remover_window)
    combo_carros_remover.set(modelos_carros[0])
    combo = tk.OptionMenu(remover_window, combo_carros_remover, *modelos_carros)
    combo.pack(pady=10)

    botao_remover = tk.Button(remover_window, text="Remover", command=remover_selecionado)
    botao_remover.pack(pady=10)

root = tk.Tk()
root.title("Lista de Carros")
root.geometry("600x700")

frame_carros = tk.Frame(root)
frame_carros.pack(pady=10)

label_titulo = tk.Label(root, text="Carros Disponíveis", font=("Arial", 16))
label_titulo.pack(pady=10)

atualizar_lista()

botao_negociacao = tk.Button(root, text="Em Negociação", command=carros_em_negociacao)
botao_negociacao.pack(side="left", padx=20, pady=10)

botao_vendido = tk.Button(root, text="Vendido", command=carros_vendidos)
botao_vendido.pack(side="right", padx=20, pady=10)

botao_adicionar = tk.Button(root, text="Adicionar Carro", command=adicionar_carro)
botao_adicionar.pack(pady=10)

botao_remover = tk.Button(root, text="Remover Carro", command=remover_carro)
botao_remover.pack(pady=10)

root.mainloop()
