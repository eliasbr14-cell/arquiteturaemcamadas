"""
Configuracao visual da interface.

O Tkinter nao utiliza arquivos CSS. Por isso, os estilos foram separados neste
modulo para deixar o codigo da tela principal mais organizado.
"""

from tkinter import ttk


CORES = {
    "fundo": "#eef2f7",
    "superficie": "#ffffff",
    "borda": "#d9e2ef",
    "texto": "#172033",
    "muted": "#68758a",
    "primaria": "#2563eb",
    "primaria_escura": "#1d4ed8",
    "sucesso": "#16a34a",
    "linha": "#f8fafc",
}


def configurar_estilos(janela):
    """Aplica o tema visual usado pelos componentes da interface."""
    estilo = ttk.Style(janela)
    estilo.theme_use("clam")

    estilo.configure("TFrame", background=CORES["fundo"])
    estilo.configure(
        "Surface.TFrame",
        background=CORES["superficie"],
        bordercolor=CORES["borda"],
        relief="solid",
    )
    estilo.configure(
        "Title.TLabel",
        background=CORES["fundo"],
        foreground=CORES["texto"],
        font=("Segoe UI", 24, "bold"),
    )
    estilo.configure(
        "Subtitle.TLabel",
        background=CORES["fundo"],
        foreground=CORES["muted"],
        font=("Segoe UI", 10),
    )
    estilo.configure(
        "CardTitle.TLabel",
        background=CORES["superficie"],
        foreground=CORES["texto"],
        font=("Segoe UI", 12, "bold"),
    )
    estilo.configure(
        "Metric.TLabel",
        background=CORES["superficie"],
        foreground=CORES["texto"],
        font=("Segoe UI", 24, "bold"),
    )
    estilo.configure(
        "Muted.TLabel",
        background=CORES["superficie"],
        foreground=CORES["muted"],
        font=("Segoe UI", 9),
    )
    estilo.configure(
        "Primary.TButton",
        background=CORES["primaria"],
        foreground="#ffffff",
        borderwidth=0,
        focusthickness=0,
        font=("Segoe UI", 10, "bold"),
        padding=(14, 10),
    )
    estilo.map(
        "Primary.TButton",
        background=[("active", CORES["primaria_escura"])],
    )
    estilo.configure(
        "Success.TButton",
        background=CORES["sucesso"],
        foreground="#ffffff",
        borderwidth=0,
        font=("Segoe UI", 10, "bold"),
        padding=(14, 10),
    )
    estilo.map("Success.TButton", background=[("active", "#15803d")])
    estilo.configure(
        "Ghost.TButton",
        background=CORES["superficie"],
        foreground=CORES["texto"],
        borderwidth=1,
        bordercolor=CORES["borda"],
        font=("Segoe UI", 10),
        padding=(12, 9),
    )
    estilo.map("Ghost.TButton", background=[("active", "#f1f5f9")])
    estilo.configure(
        "Treeview",
        background=CORES["superficie"],
        fieldbackground=CORES["superficie"],
        foreground=CORES["texto"],
        rowheight=34,
        borderwidth=0,
        font=("Segoe UI", 10),
    )
    estilo.configure(
        "Treeview.Heading",
        background="#e8eef7",
        foreground=CORES["texto"],
        borderwidth=0,
        font=("Segoe UI", 9, "bold"),
        padding=(8, 8),
    )
    estilo.map("Treeview", background=[("selected", "#dbeafe")])
    estilo.configure(
        "Horizontal.TProgressbar",
        troughcolor="#dbe3ef",
        background=CORES["primaria"],
        bordercolor=CORES["borda"],
        lightcolor=CORES["primaria"],
        darkcolor=CORES["primaria"],
    )

    return estilo
