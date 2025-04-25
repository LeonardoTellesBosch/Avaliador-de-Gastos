import pandas as pd
import customtkinter
from tkinter.filedialog import askopenfilename



# Configurações iniciais do customtkinter
customtkinter.set_appearance_mode("dark")       # ou "light"
customtkinter.set_default_color_theme("dark-blue")

# Função de cálculo
def clicar():
    caminho_arquivo = askopenfilename(title="Selecione o arquivo CSV", filetypes=[("Planilhas CSV", "*.csv")])
    if not caminho_arquivo:
        return

    try:
        tabela = pd.read_csv(caminho_arquivo)
        nome_coluna_gasto = entrada_gasto.get()
        nome_coluna_renda = entrada_renda.get()

        if nome_coluna_gasto not in tabela.columns or nome_coluna_renda not in tabela.columns:
            resultado_renda.configure(text="Coluna inválida")
            resultado_gasto.configure(text="")
            resultado_final.configure(text="")
            resultado_finalN.configure(text="")
            return

        valor_total = tabela[nome_coluna_gasto].sum()
        renda_mensal = tabela[nome_coluna_renda].sum()
        renda_anual = renda_mensal * 12
        valor_final = renda_anual - valor_total

        resultado_renda.configure(text=f"Renda anual: R$ {renda_anual:.2f}")
        resultado_gasto.configure(text=f"Gastos totais: R$ {valor_total:.2f}")
        resultado_final.configure(text=f"Saldo final: R$ {valor_final:.2f}")
        if renda_anual < valor_total:
            meses = valor_total / renda_anual
            resultado_finalN.configure(text=f"Está devendo cerca de {meses:.1f} meses")
        else:
            resultado_finalN.configure(text="")
        import matplotlib.pyplot as plt

        sobra = renda_anual - valor_total

        if sobra >= 0:
            labels = ['Gastos', 'Sobra da Renda']
            values = [valor_total, sobra]
        else:
            labels = ['Gastos', 'Dívida']
            values = [renda_anual, abs(sobra)]
        plt.figure(figsize=(5,5))
        plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
        plt.title("Distribuição de renda anual")
        plt.axis('equal')
        plt.show()


    except Exception as e:
        resultado_renda.configure(text="Erro ao processar arquivo")
        resultado_gasto.configure(text=str(e))
        resultado_final.configure(text="")
        resultado_finalN.configure(text="")




# Criar janela
janela = customtkinter.CTk()
janela.title("Tabela de Rendas/Gastos Métricas")
janela.geometry("500x400")

# Entradas
customtkinter.CTkLabel(janela, text="Digite o nome da coluna de gastos:").pack(pady=5)
entrada_gasto = customtkinter.CTkEntry(janela)
entrada_gasto.pack(pady=5)

customtkinter.CTkLabel(janela, text="Digite o nome da coluna de rendas:").pack(pady=5)
entrada_renda = customtkinter.CTkEntry(janela)
entrada_renda.pack(pady=5)

# Botão
customtkinter.CTkButton(janela, text="Enviar", command=clicar).pack(pady=10)

# Resultados
resultado_renda = customtkinter.CTkLabel(janela, text="", text_color="white")
resultado_renda.pack(pady=2)

resultado_gasto = customtkinter.CTkLabel(janela, text="", text_color="white")
resultado_gasto.pack(pady=2)

resultado_final = customtkinter.CTkLabel(janela, text="", text_color="white")
resultado_final.pack(pady=2)

resultado_finalN = customtkinter.CTkLabel(janela, text="", text_color="white")
resultado_finalN.pack(pady=2)

# Loop da interface
janela.mainloop()
