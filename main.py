"""
Interface grafica do Controle de Estacionamento.

A camada de apresentacao conversa apenas com a camada de negocio para registrar
entradas e saidas. A leitura das listas em memoria continua centralizada em
dados.py para manter o desenho em camadas do projeto original.
"""

import tkinter as tk
from datetime import datetime
from tkinter import messagebox, ttk

import dados
import estilos
import negocio


class ControleEstacionamentoApp(tk.Tk):
    """Janela principal do sistema de estacionamento."""

    def __init__(self):
        super().__init__()
        self.title("Controle de Estacionamento")
        self.geometry("1120x720")
        self.minsize(980, 640)
        self.configure(bg=estilos.CORES["fundo"])

        self.placa_var = tk.StringVar()
        self.busca_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Pronto para registrar movimentos.")
        self.relogio_var = tk.StringVar()

        self.style = estilos.configurar_estilos(self)
        self._montar_layout()
        self._configurar_atalhos()
        self.atualizar_tela()
        self._atualizar_relogio()

    def _montar_layout(self):
        pagina = ttk.Frame(self, padding=24)
        pagina.pack(fill="both", expand=True)
        pagina.columnconfigure(0, weight=1)
        pagina.rowconfigure(2, weight=1)

        topo = ttk.Frame(pagina)
        topo.grid(row=0, column=0, sticky="ew")
        topo.columnconfigure(0, weight=1)

        ttk.Label(topo, text="Controle de Estacionamento", style="Title.TLabel").grid(
            row=0, column=0, sticky="w"
        )
        ttk.Label(
            topo,
            text="Painel operacional para entradas, saidas, vagas e historico.",
            style="Subtitle.TLabel",
        ).grid(row=1, column=0, sticky="w", pady=(2, 0))

        ttk.Label(topo, textvariable=self.relogio_var, style="Subtitle.TLabel").grid(
            row=0, column=1, rowspan=2, sticky="e"
        )

        self._montar_metricas(pagina)
        self._montar_conteudo(pagina)
        self._montar_barra_status(pagina)

    def _montar_metricas(self, parent):
        metricas = ttk.Frame(parent)
        metricas.grid(row=1, column=0, sticky="ew", pady=(22, 16))
        for coluna in range(4):
            metricas.columnconfigure(coluna, weight=1, uniform="metricas")

        self.ocupadas_var = tk.StringVar()
        self.livres_var = tk.StringVar()
        self.receita_var = tk.StringVar()
        self.movimentos_var = tk.StringVar()
        self.ocupacao_var = tk.DoubleVar(value=0)

        self._cartao_metrica(metricas, 0, "Vagas ocupadas", self.ocupadas_var, "agora")
        self._cartao_metrica(metricas, 1, "Vagas livres", self.livres_var, "disponiveis")
        self._cartao_metrica(metricas, 2, "Receita do dia", self.receita_var, "historico")
        self._cartao_metrica(metricas, 3, "Movimentos", self.movimentos_var, "saidas registradas")

    def _cartao_metrica(self, parent, coluna, titulo, variavel, legenda):
        frame = ttk.Frame(parent, style="Surface.TFrame", padding=16)
        frame.grid(row=0, column=coluna, sticky="nsew", padx=(0 if coluna == 0 else 10, 0))
        frame.columnconfigure(0, weight=1)

        ttk.Label(frame, text=titulo, style="Muted.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(frame, textvariable=variavel, style="Metric.TLabel").grid(
            row=1, column=0, sticky="w", pady=(4, 0)
        )
        ttk.Label(frame, text=legenda, style="Muted.TLabel").grid(row=2, column=0, sticky="w")

        if coluna == 0:
            self.ocupacao_barra = ttk.Progressbar(
                frame,
                variable=self.ocupacao_var,
                maximum=100,
                style="Horizontal.TProgressbar",
            )
            self.ocupacao_barra.grid(row=3, column=0, sticky="ew", pady=(12, 0))

    def _montar_conteudo(self, parent):
        conteudo = ttk.Frame(parent)
        conteudo.grid(row=2, column=0, sticky="nsew")
        conteudo.columnconfigure(0, weight=0)
        conteudo.columnconfigure(1, weight=1)
        conteudo.rowconfigure(0, weight=1)

        self._montar_painel_acoes(conteudo)
        self._montar_tabelas(conteudo)

    def _montar_painel_acoes(self, parent):
        painel = ttk.Frame(parent, style="Surface.TFrame", padding=18)
        painel.grid(row=0, column=0, sticky="ns", padx=(0, 16))
        painel.columnconfigure(0, weight=1)

        ttk.Label(painel, text="Operacao rapida", style="CardTitle.TLabel").grid(
            row=0, column=0, sticky="w"
        )
        ttk.Label(
            painel,
            text="Digite a placa no formato AAA1234 ou AAA1A23.",
            style="Muted.TLabel",
            wraplength=260,
        ).grid(row=1, column=0, sticky="w", pady=(4, 14))

        placa_entry = ttk.Entry(
            painel,
            textvariable=self.placa_var,
            font=("Segoe UI", 18, "bold"),
            justify="center",
            width=12,
        )
        placa_entry.grid(row=2, column=0, sticky="ew")
        placa_entry.focus()
        placa_entry.bind("<KeyRelease>", self._formatar_placa)

        botoes = ttk.Frame(painel, style="Surface.TFrame")
        botoes.grid(row=3, column=0, sticky="ew", pady=(14, 18))
        botoes.columnconfigure(0, weight=1)
        botoes.columnconfigure(1, weight=1)

        ttk.Button(
            botoes,
            text="Registrar entrada",
            command=self.registrar_entrada,
            style="Primary.TButton",
        ).grid(row=0, column=0, sticky="ew", padx=(0, 8))
        ttk.Button(
            botoes,
            text="Registrar saida",
            command=self.registrar_saida,
            style="Success.TButton",
        ).grid(row=0, column=1, sticky="ew")

        ttk.Separator(painel).grid(row=4, column=0, sticky="ew", pady=(4, 18))

        ttk.Label(painel, text="Busca", style="CardTitle.TLabel").grid(row=5, column=0, sticky="w")
        ttk.Entry(painel, textvariable=self.busca_var, font=("Segoe UI", 11)).grid(
            row=6, column=0, sticky="ew", pady=(8, 10)
        )
        self.busca_var.trace_add("write", lambda *_: self.atualizar_tabela_veiculos())

        ttk.Button(
            painel,
            text="Limpar busca",
            command=self.limpar_busca,
            style="Ghost.TButton",
        ).grid(row=7, column=0, sticky="ew")

    def _montar_tabelas(self, parent):
        area_tabelas = ttk.Frame(parent)
        area_tabelas.grid(row=0, column=1, sticky="nsew")
        area_tabelas.columnconfigure(0, weight=1)
        area_tabelas.rowconfigure(1, weight=1)

        ttk.Label(
            area_tabelas,
            text="Dica: selecione uma placa e de duplo clique para registrar a saida do veiculo.",
            style="Subtitle.TLabel",
        ).grid(row=0, column=0, sticky="w", pady=(0, 8))

        abas = ttk.Notebook(area_tabelas)
        abas.grid(row=1, column=0, sticky="nsew")

        aba_veiculos = ttk.Frame(abas, padding=14)
        aba_historico = ttk.Frame(abas, padding=14)
        abas.add(aba_veiculos, text="Veiculos estacionados")
        abas.add(aba_historico, text="Historico de saidas")

        aba_veiculos.rowconfigure(0, weight=1)
        aba_veiculos.columnconfigure(0, weight=1)
        aba_historico.rowconfigure(0, weight=1)
        aba_historico.columnconfigure(0, weight=1)

        self.tabela_veiculos = self._criar_tabela(
            aba_veiculos,
            ("placa", "entrada", "permanencia", "valor_estimado"),
            {
                "placa": "Placa",
                "entrada": "Entrada",
                "permanencia": "Permanencia",
                "valor_estimado": "Valor estimado",
            },
        )
        self.tabela_veiculos.bind("<<TreeviewSelect>>", self._selecionar_placa_da_tabela)
        self.tabela_veiculos.bind("<Double-1>", self.registrar_saida_selecionada)

        self.tabela_historico = self._criar_tabela(
            aba_historico,
            ("placa", "entrada", "saida", "cobrado", "valor"),
            {
                "placa": "Placa",
                "entrada": "Entrada",
                "saida": "Saida",
                "cobrado": "Cobrado",
                "valor": "Valor",
            },
        )

    def _criar_tabela(self, parent, colunas, cabecalhos):
        container = ttk.Frame(parent)
        container.grid(row=0, column=0, sticky="nsew")
        container.rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)

        tabela = ttk.Treeview(container, columns=colunas, show="headings", selectmode="browse")
        barra = ttk.Scrollbar(container, orient="vertical", command=tabela.yview)
        tabela.configure(yscrollcommand=barra.set)

        larguras = {
            "placa": 120,
            "entrada": 130,
            "saida": 130,
            "permanencia": 150,
            "valor_estimado": 150,
            "cobrado": 100,
            "valor": 120,
        }
        for coluna in colunas:
            tabela.heading(coluna, text=cabecalhos[coluna])
            tabela.column(coluna, width=larguras.get(coluna, 120), anchor="center")

        tabela.tag_configure("par", background=estilos.CORES["superficie"])
        tabela.tag_configure("impar", background=estilos.CORES["linha"])
        tabela.grid(row=0, column=0, sticky="nsew")
        barra.grid(row=0, column=1, sticky="ns")
        return tabela

    def _montar_barra_status(self, parent):
        barra = ttk.Frame(parent, style="Surface.TFrame", padding=(14, 10))
        barra.grid(row=3, column=0, sticky="ew", pady=(16, 0))
        barra.columnconfigure(0, weight=1)
        ttk.Label(barra, textvariable=self.status_var, style="Muted.TLabel").grid(
            row=0, column=0, sticky="w"
        )
        ttk.Button(
            barra,
            text="Atualizar",
            command=self.atualizar_tela,
            style="Ghost.TButton",
        ).grid(row=0, column=1, sticky="e")

    def _configurar_atalhos(self):
        self.bind("<Return>", lambda _: self.registrar_entrada())
        self.bind("<Control-Return>", lambda _: self.registrar_saida())
        self.bind("<F5>", lambda _: self.atualizar_tela())
        self.bind("<Escape>", lambda _: self.limpar_formulario())

    def _formatar_placa(self, _event=None):
        texto = negocio.normalizar_placa(self.placa_var.get())[:7]
        if texto != self.placa_var.get():
            self.placa_var.set(texto)

    def _atualizar_relogio(self):
        self.relogio_var.set(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        if dados.total_estacionados() > 0:
            self.atualizar_tabela_veiculos()
        self.after(1000, self._atualizar_relogio)

    def registrar_entrada(self):
        placa = self.placa_var.get()
        sucesso, mensagem = negocio.registrar_entrada(placa)
        self._notificar(sucesso, mensagem)
        if sucesso:
            self.limpar_formulario()
        self.atualizar_tela()

    def registrar_saida(self):
        placa = self.placa_var.get()
        sucesso, mensagem = negocio.registrar_saida(placa)
        self._notificar(sucesso, mensagem)
        if sucesso:
            self.limpar_formulario()
        self.atualizar_tela()

    def registrar_saida_selecionada(self, _event=None):
        placa = self._obter_placa_selecionada()
        if not placa:
            self.status_var.set("Selecione um veiculo na lista para registrar a saida.")
            return

        confirmar = messagebox.askyesno(
            "Confirmar saida",
            f"Deseja registrar a saida do veiculo {placa}?",
        )
        if not confirmar:
            return

        sucesso, mensagem = negocio.registrar_saida(placa)
        self._notificar(sucesso, mensagem)
        if sucesso:
            self.limpar_formulario()
        self.atualizar_tela()

    def _notificar(self, sucesso, mensagem):
        self.status_var.set(mensagem.replace("\n", " "))
        if sucesso:
            self.bell()
            return
        messagebox.showwarning("Atencao", mensagem)

    def limpar_formulario(self):
        self.placa_var.set("")

    def limpar_busca(self):
        self.busca_var.set("")
        self.atualizar_tabela_veiculos()

    def atualizar_tela(self):
        total = dados.get_capacidade_total()
        ocupadas = dados.total_estacionados()
        livres = negocio.vagas_disponiveis()
        ocupacao = (ocupadas / total) * 100 if total else 0
        historico = dados.listar_historico()
        receita = sum(item["valor"] for item in historico)

        self.ocupadas_var.set(f"{ocupadas}/{total}")
        self.livres_var.set(str(livres))
        self.receita_var.set(f"R$ {receita:.2f}")
        self.movimentos_var.set(str(len(historico)))
        self.ocupacao_var.set(ocupacao)

        self.atualizar_tabela_veiculos()
        self.atualizar_tabela_historico()

    def atualizar_tabela_veiculos(self):
        termo = self.busca_var.get().strip().upper()
        self.tabela_veiculos.delete(*self.tabela_veiculos.get_children())

        agora = datetime.now()
        veiculos = sorted(dados.listar_veiculos_estacionados().items())
        for indice, (placa, info) in enumerate(veiculos):
            if termo and termo not in placa:
                continue
            entrada = info["hora_entrada"]
            horas_cobradas, valor = negocio.calcular_valor(entrada, agora)
            permanencia = self._formatar_duracao(agora - entrada)
            tag = "par" if indice % 2 == 0 else "impar"
            self.tabela_veiculos.insert(
                "",
                "end",
                values=(
                    placa,
                    entrada.strftime("%H:%M:%S"),
                    permanencia,
                    f"R$ {valor:.2f} ({horas_cobradas}h)",
                ),
                tags=(tag,),
            )

    def atualizar_tabela_historico(self):
        self.tabela_historico.delete(*self.tabela_historico.get_children())
        historico = list(reversed(dados.listar_historico()))
        for indice, item in enumerate(historico):
            tag = "par" if indice % 2 == 0 else "impar"
            self.tabela_historico.insert(
                "",
                "end",
                values=(
                    item["placa"],
                    item["hora_entrada"].strftime("%H:%M:%S"),
                    item["hora_saida"].strftime("%H:%M:%S"),
                    f"{item['horas_cobradas']}h",
                    f"R$ {item['valor']:.2f}",
                ),
                tags=(tag,),
            )

    def _selecionar_placa_da_tabela(self, _event=None):
        placa = self._obter_placa_selecionada()
        if placa:
            self.placa_var.set(placa)
            self.status_var.set(f"Placa {placa} selecionada. De duplo clique para registrar a saida.")

    def _obter_placa_selecionada(self):
        selecionado = self.tabela_veiculos.selection()
        if not selecionado:
            return None
        valores = self.tabela_veiculos.item(selecionado[0], "values")
        if valores:
            return valores[0]
        return None

    @staticmethod
    def _formatar_duracao(duracao):
        segundos = max(0, int(duracao.total_seconds()))
        horas, resto = divmod(segundos, 3600)
        minutos, segundos = divmod(resto, 60)
        if horas:
            return f"{horas}h {minutos:02d}min"
        if minutos:
            return f"{minutos}min {segundos:02d}s"
        return f"{segundos}s"


def main():
    app = ControleEstacionamentoApp()
    app.mainloop()


if __name__ == "__main__":
    main()
