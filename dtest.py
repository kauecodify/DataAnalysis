import tkinter as tk
from tkinter import ttk
import sqlite3
import matplotlib.pyplot as plt

conn = sqlite3.connect("carros.db")
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS carros (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    modelo TEXT NOT NULL,
    ano INTEGER NOT NULL,
    valor INTEGER NOT NULL,
    status TEXT NOT NULL
)''')
conn.commit()

def carregar_carros():
    cursor.execute("SELECT * FROM carros")
    return cursor.fetchall()

def atualizar_metrica():
    cursor.execute("SELECT COUNT(*) FROM carros WHERE status = 'Disponível'")
    disponiveis = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM carros WHERE status = 'Em Negociação'")
    em_negociacao = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM carros WHERE status = 'Vendido'")
    vendidos = cursor.fetchone()[0]

    label_disponiveis.config(text=f"Disponíveis: {disponiveis}")
    label_em_negociacao.config(text=f"Em Negociação: {em_negociacao}")
    label_vendidos.config(text=f"Vendidos: {vendidos}")

def atualizar_lista(status_filtro=None):
    for widget in frame_carros.winfo_children():
        widget.destroy()

    if status_filtro:
        cursor.execute("SELECT * FROM carros WHERE status = ?", (status_filtro,))
    else:
        cursor.execute("SELECT * FROM carros")
    carros_filtrados = cursor.fetchall()

    for carro in carros_filtrados:
        modelo = carro[1]
        ano = carro[2]
        valor = carro[3]
        status = carro[4]
        
        info = f"Modelo: {modelo} | Ano: {ano} | Valor: R${valor:,} | Status: {status}"
        label_carro = tk.Label(frame_carros, text=info, font=("Arial", 12), anchor="w", width=80)
        label_carro.pack(fill="x", pady=5)

    atualizar_metrica()

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

        cursor.execute("INSERT INTO carros (modelo, ano, valor, status) VALUES (?, ?, ?, ?)",
                       (modelo, ano, valor, status))
        conn.commit()
        
        adicionar_window.destroy()
        atualizar_lista()

    adicionar_window = tk.Toplevel(root)
    adicionar_window.title("Adicionar Novo Carro")
    adicionar_window.geometry("500x600")

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
        cursor.execute("DELETE FROM carros WHERE modelo = ?", (modelo_remover,))
        conn.commit()
        
        remover_window.destroy()
        atualizar_lista()

    remover_window = tk.Toplevel(root)
    remover_window.title("Remover Carro")
    remover_window.geometry("400x300")

    label_carros = tk.Label(remover_window, text="Escolha um carro para remover:")
    label_carros.pack(pady=5)

    cursor.execute("SELECT modelo FROM carros")
    modelos_carros = [row[0] for row in cursor.fetchall()]
    combo_carros_remover = tk.StringVar(remover_window)
    if modelos_carros:
        combo_carros_remover.set(modelos_carros[0])
    combo = tk.OptionMenu(remover_window, combo_carros_remover, *modelos_carros)
    combo.pack(pady=10)

    botao_remover = tk.Button(remover_window, text="Remover", command=remover_selecionado)
    botao_remover.pack(pady=10)

def mostrar_todos_carros():
    atualizar_lista()

def mostrar_dados_bd():
    dados_window = tk.Toplevel(root)
    dados_window.title("Dados do Banco de Dados")
    dados_window.geometry("600x400")

    tree = ttk.Treeview(dados_window, columns=("ID", "Modelo", "Ano", "Valor", "Status"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Modelo", text="Modelo")
    tree.heading("Ano", text="Ano")
    tree.heading("Valor", text="Valor")
    tree.heading("Status", text="Status")
    tree.pack(fill="both", expand=True)

    cursor.execute("SELECT * FROM carros")
    rows = cursor.fetchall()
    for row in rows:
        tree.insert("", "end", values=row)

def analisar_dados():
    analise_window = tk.Toplevel(root)
    analise_window.title("Análise dos Dados")
    analise_window.geometry("600x400")

    cursor.execute("SELECT COUNT(*) FROM carros")
    total_carros = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM carros WHERE status = 'Vendido'")
    total_vendidos = cursor.fetchone()[0]
    porcentagem_vendidos = (total_vendidos / total_carros) * 100 if total_carros > 0 else 0
    
    cursor.execute("SELECT SUM(valor) FROM carros WHERE status = 'Disponível'")
    valor_disponiveis = cursor.fetchone()[0] or 0
    cursor.execute("SELECT SUM(valor) FROM carros WHERE status = 'Em Negociação'")
    valor_em_negociacao = cursor.fetchone()[0] or 0
    cursor.execute("SELECT SUM(valor) FROM carros WHERE status = 'Vendido'")
    valor_vendidos = cursor.fetchone()[0] or 0

    valor_projecao = valor_disponiveis + valor_em_negociacao + valor_vendidos

    tk.Label(analise_window, text=f"Total de Carros Vendidos: {total_vendidos}", font=("Arial", 12)).pack(pady=5)
    tk.Label(analise_window, text=f"Porcentagem de Vendas: {porcentagem_vendidos:.2f}%", font=("Arial", 12)).pack(pady=5)
    tk.Label(analise_window, text=f"Valor Total Vendido: R${valor_vendidos:,}", font=("Arial", 12)).pack(pady=5)
    tk.Label(analise_window, text=f"Valor em Negociação: R${valor_em_negociacao:,}", font=("Arial", 12)).pack(pady=5)
    tk.Label(analise_window, text=f"Valor Disponível: R${valor_disponiveis:,}", font=("Arial", 12)).pack(pady=5)
    tk.Label(analise_window, text=f"Projeção Total se Todos Vendidos: R${valor_projecao:,}", font=("Arial", 12, "bold")).pack(pady=5)

    gerar_grafico(valor_disponiveis, valor_em_negociacao, valor_vendidos)

def gerar_grafico(disponiveis, em_negociacao, vendidos):
    fig, ax = plt.subplots(figsize=(8, 6))
    categorias = ['Disponíveis', 'Em Negociação', 'Vendidos']
    valores = [disponiveis, em_negociacao, vendidos]
    ax.pie(valores, labels=categorias, autopct='%1.1f%%', startangle=90, colors=['#FF9999', '#66B2FF', '#99FF99'])
    ax.axis('equal')

    ax.set_title("Projeção de Carros (Disponíveis, Em Negociação, Vendidos)")

    plt.show()

root = tk.Tk()
root.title("Lista de Carros")
root.geometry("600x700")

frame_carros = tk.Frame(root)
frame_carros.pack(pady=10)

label_titulo = tk.Label(root, text="Carros Disponíveis", font=("Arial", 16))
label_titulo.pack(pady=10)

label_disponiveis = tk.Label(root, text="Disponíveis: 0", font=("Arial", 12))
label_disponiveis.pack()
label_em_negociacao = tk.Label(root, text="Em Negociação: 0", font=("Arial", 12))
label_em_negociacao.pack()
label_vendidos = tk.Label(root, text="Vendidos: 0", font=("Arial", 12))
label_vendidos.pack()

atualizar_lista()

botao_negociacao = tk.Button(root, text="Em Negociação", command=carros_em_negociacao)
botao_negociacao.pack(side="left", padx=20, pady=10)

botao_vendido = tk.Button(root, text="Vendido", command=carros_vendidos)
botao_vendido.pack(side="right", padx=20, pady=10)

botao_adicionar = tk.Button(root, text="Adicionar Carro", command=adicionar_carro)
botao_adicionar.pack(pady=10)

botao_remover = tk.Button(root, text="Remover Carro", command=remover_carro)
botao_remover.pack(pady=10)

botao_todos = tk.Button(root, text="Mostrar Todos os Carros", command=mostrar_todos_carros)
botao_todos.pack(pady=10)

botao_dados_bd = tk.Button(root, text="Dados do Banco", command=mostrar_dados_bd)
botao_dados_bd.pack(pady=10)

botao_analise = tk.Button(root, text="Analisar Dados", command=analisar_dados)
botao_analise.pack(pady=10)

root.mainloop()
