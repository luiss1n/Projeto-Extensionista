import tkinter as tk
from tkinter import ttk, messagebox

root = tk.Tk()
root.iconbitmap("snoopy.ico")
root.title("Anotação Manual de Pedidos")
root.geometry("500x650")
root.configure(bg="#F5F5F5")

pedidos = []

# Tabela dos preços
precos_lanches = {
    "Misto": 8, "Hamburguer": 10, "Americano": 11, "X-Burguer": 12,
    "Egg-burguer": 14, "X-Salada": 13, "Egg-Salada": 14.5, "X-Especial": 14,
    "Egg-Especial": 15, "X-Frango": 16, "Egg-Frango": 17, "X-Calabresa": 17,
    "Egg-Calabresa": 18, "X-Bacon": 17, "Egg-Bacon": 18, "X-Tudo": 22
}

precos_refri = {
    "Coca 200ml": 3, "Guaraná 200ml": 3, "Coca Lata": 5, "Guaraná Lata": 5,
    "Coca 2L": 13, "Guaraná 2L": 7
}

# Função de soma

def calcular_valor():
    lanche1 = combo_lanche.get()
    lanche2 = combo_lanche2.get()
    entrega = var_entrega.get()
    refe = var_refrigerante.get()
    horario = combo_horario.get()

    # Horário obrigatório
    if horario == "Selecione o horário":
        messagebox.showerror("Erro", "Selecione o horário do pedido.")
        return

    # Primeiro lanche obrigatório
    if lanche1 == "Selecione o lanche":
        messagebox.showerror("Erro", "Selecione o primeiro lanche.")
        return

    preco = precos_lanches[lanche1]

    # Segundo lanche opcional
    if lanche2 != "Nenhum":
        preco += precos_lanches[lanche2]

    # Entrega
    if entrega == "Sim":
        endereco = entry_endereco.get().strip()
        if not endereco:
            messagebox.showerror("Erro", "Digite o endereço do cliente.")
            return
        preco += 5
    else:
        endereco = "Retirar no local"

    # Refrigerante
    if refe == "Sim":
        bebida = combo_refri.get()
        if bebida == "Selecione o refrigerante":
            messagebox.showerror("Erro", "Selecione o refrigerante.")
            return
        preco += precos_refri[bebida]

    obs = entry_obs.get().strip() if entry_obs.get().strip() else "Sem observações"

    pedido = f"{lanche1}{' + ' + lanche2 if lanche2 != 'Nenhum' else ''} | Horário: {horario} | {endereco} | Obs: {obs} | Total: R$ {preco:.2f}"
    pedidos.append(pedido)
    lista_pedidos.insert(tk.END, pedido)

    tela_pedido.pack_forget()
    tela_lista.pack(fill="both", expand=True)


def finalizar_pedido():
    sel = lista_pedidos.curselection()
    if sel:
        lista_pedidos.delete(sel)

def alterar_pedido():
    sel = lista_pedidos.curselection()
    if not sel:
        return
    item = lista_pedidos.get(sel)
    partes = item.split("|")
    lanche_part = partes[0].strip().split("+")
    combo_lanche.set(lanche_part[0].strip())
    if len(lanche_part) > 1:
        combo_lanche2.set(lanche_part[1].strip())
    else:
        combo_lanche2.set("Nenhum")
    combo_horario.set(partes[1].replace("Horário:","").strip())
    end_val = partes[2].strip()
    if end_val != "Retirar no local":
        var_entrega.set("Sim")
        entry_endereco.delete(0, tk.END)
        entry_endereco.insert(0, end_val)
    else:
        var_entrega.set("Não")
        entry_endereco.delete(0, tk.END)
    entry_obs.delete(0, tk.END)
    entry_obs.insert(0, partes[3].replace("Obs:","").strip())
    lista_pedidos.delete(sel)
    tela_lista.pack_forget()
    tela_pedido.pack(fill="both", expand=True)
    sel = lista_pedidos.curselection()
    if sel:
        lista_pedidos.delete(sel)

# TELAS

tela_pedido = tk.Frame(root, bg="#F5F5F5", padx=20, pady=20)
tela_pedido.pack(fill="both", expand=True)

cabecalho = tk.Label(tela_pedido, text="ANOTAÇÃO MANUAL DE PEDIDOS", font=("Arial", 16, "bold"), bg="#F5F5F5")
cabecalho.pack(pady=10)

# Primeiro lanche
combo_lanche = ttk.Combobox(tela_pedido, values=list(precos_lanches.keys()), state="readonly", width=30)
combo_lanche.pack(pady=5)
combo_lanche.set("Selecione o lanche")

# Segundo lanche
combo_lanche2 = ttk.Combobox(tela_pedido, values=["Nenhum"] + list(precos_lanches.keys()), state="readonly", width=30)
combo_lanche2.pack(pady=5)
combo_lanche2.set("Nenhum")

# Entrega
var_entrega = tk.StringVar(value="Não")
frame_entrega = tk.Frame(tela_pedido, bg="#F5F5F5")
frame_entrega.pack(pady=5)
tk.Label(frame_entrega, text="Para entregar?", bg="#F5F5F5").pack(side="left")
tk.Radiobutton(frame_entrega, text="Sim", variable=var_entrega, value="Sim", bg="#F5F5F5").pack(side="left")
tk.Radiobutton(frame_entrega, text="Não", variable=var_entrega, value="Não", bg="#F5F5F5").pack(side="left")

# Endereço
label_end = tk.Label(tela_pedido, text="Qual o endereço?", bg="#F5F5F5")
label_end.pack()
entry_endereco = tk.Entry(tela_pedido, width=40)
entry_endereco.pack(pady=5)

# Refrigerante
var_refrigerante = tk.StringVar(value="Não")
frame_refri = tk.Frame(tela_pedido, bg="#F5F5F5")
frame_refri.pack(pady=5)
tk.Label(frame_refri, text="Com refrigerante?", bg="#F5F5F5").pack(side="left")
tk.Radiobutton(frame_refri, text="Sim", variable=var_refrigerante, value="Sim", bg="#F5F5F5").pack(side="left")
tk.Radiobutton(frame_refri, text="Não", variable=var_refrigerante, value="Não", bg="#F5F5F5").pack(side="left")

combo_refri = ttk.Combobox(tela_pedido, values=list(precos_refri.keys()), state="readonly", width=30)
combo_refri.pack(pady=5)
combo_refri.set("Selecione o refrigerante")

# Horário
horarios = [f"{h:02d}:{m:02d}" for h in range(19, 23) for m in (0, 30)]
combo_horario = ttk.Combobox(tela_pedido, values=horarios, state="readonly", width=20)
combo_horario.pack(pady=5)
combo_horario.set("Selecione o horário")

# Observações
label_obs = tk.Label(tela_pedido, text="Observações", bg="#F5F5F5")
label_obs.pack()
entry_obs = tk.Entry(tela_pedido, width=45)
entry_obs.pack(pady=5)

btn_calcular = tk.Button(tela_pedido, text="Registrar Pedido", command=calcular_valor, bg="#D0E6FF")
btn_calcular.pack(pady=10)

# Tela de lista

tela_lista = tk.Frame(root, padx=20, pady=20)
lista_pedidos = tk.Listbox(tela_lista)
lista_pedidos.pack(fill="both", expand=True)

btn_alterar = tk.Button(tela_lista, text="Alterar Pedido", command=alterar_pedido)
btn_alterar.pack(pady=5)

btn_finalizar = tk.Button(tela_lista, text="Pedido Finalizado", command=finalizar_pedido)
btn_finalizar.pack(pady=5)

btn_voltar = tk.Button(tela_lista, text="Voltar", command=lambda: (tela_lista.pack_forget(), tela_pedido.pack(fill="both", expand=True)))
btn_voltar.pack(pady=5)

root.mainloop()
