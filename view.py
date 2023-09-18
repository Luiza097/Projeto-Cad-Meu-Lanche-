import tkinter as tk
from tkinter import ttk
import tkintermapview as tkmv
from model import *
import os


class View:

  def __init__(self, root):
    self.root = root
    self.telainicial()
    self.marcadores = []

  def inicializa_gui(self):
    #----- Frame do Mapa -----#
    #PARTE PARA LIMPAR O FRAME DA TELA INICIAL
    self.f1.destroy()
    #PARTE PARA LIMPAR O FRAME DA TELA INICIAL

    bd = BDVendedor()
    self.todos = bd.todos()

    local = ["ECT", "IMD", "Setor IV", "Departamento de Comunicações",
            "Departamento de Educação Física",]

    self.f1 = tk.Frame(self.root, bd=1, bg='black')
    self.f1.pack(side=tk.RIGHT)

    self.map = tkmv.TkinterMapView(self.f1,
                                   width=400,
                                   height=400,
                                   corner_radius=0)
    self.map.set_tile_server(
      "https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga",
      max_zoom=22)
    self.map.set_position(-5.836297, -35.203743)
    self.map.set_zoom(15)
    self.map.pack()

    self.f2 = tk.Frame(self.root, bd=1)
    self.f2.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
    self.nome_vendedor = tk.Label(self.f2, text='Nome do vendedor:')
    self.nome_produto = tk.Label(self.f2, text='Nome do produto:')
    self.local = tk.Label(self.f2, text='Local:')

    #INSERIR A COMBOBOX
    self.entrada_produto = tk.Entry(self.f2, width=50)
    self.entrada_nome = tk.Entry(self.f2, width=50)
    self.entrada_local = ttk.Combobox(self.f2, values=local, width=47)
    self.local_selecionado = self.entrada_local.get()
    self.entrada_local.bind("<<ComboboxSelected>>", self.local_selecionado)

    self.nome_vendedor.grid(row=0, column=0)
    self.nome_produto.grid(row=1, column=0)
    self.local.grid(row=2, column=0)
    self.entrada_nome.grid(row=0, column=1)
    self.entrada_produto.grid(row=1, column=1)
    self.entrada_local.grid(row=2, column=1)

    for vendedor in self.todos:
      latitude = float(vendedor["latitude"])
      longitude = float(vendedor["longitude"])
      marcador = self.map.set_marker(latitude, longitude)
      self.marcadores.append(marcador)
   

    #----- Botões -----#
    self.selecionado = tk.IntVar()

    def obter():
      self.resultado = self.selecionado.get()
      return (self.resultado)

    #AJUSTE DA BUSCA
    def fazer_busca():
      # Limpar marcadores antigos
      self.limpar_marcadores()

      self.todos = []
      if self.resultado == 1:
        self.todos = bd.busca_por_nome(self.entrada_nome.get())
      if self.resultado == 2:
        self.todos = bd.busca_por_produto(self.entrada_produto.get())
      if self.resultado == 3:
        self.todos = bd.busca_por_local(self.entrada_local.get())
      print(self.todos)


      for i in range(0, len(self.todos)):
        vendedor = self.todos[i]
        latitude = float(vendedor['latitude'])
        longitude = float(vendedor['longitude'])
        print(latitude, longitude)
        marcador = self.map.set_marker(latitude, longitude)
        self.marcadores.append(marcador)

    self.buscas = tk.Label(self.f2, text='Fazer busca por:')
    self.buscas.grid(row=3, column=0, columnspan=3, pady=10),

    self.radio_btn01 = tk.Radiobutton(self.f2,
                                      text="Vendedor",
                                      command=obter,
                                      value=1,
                                      variable=self.selecionado)
    self.radio_btn02 = tk.Radiobutton(self.f2,
                                      text="Produto",
                                      command=obter,
                                      value=2,
                                      variable=self.selecionado)
    self.radio_btn03 = tk.Radiobutton(self.f2,
                                      text="Localização",
                                      command=obter,
                                      value=3,
                                      variable=self.selecionado)
    self.btn_buscar = tk.Button(self.f2,
                                text="Fazer busca",
                                command=lambda: fazer_busca())

    self.radio_btn01.grid(row=4, column=0)
    self.radio_btn02.grid(row=4, column=1)
    self.radio_btn03.grid(row=4, column=2)
    self.btn_buscar.grid(row=5, column=0, columnspan=3, pady=10)

  def limpar_marcadores(self):
    # Remover todos os marcadores da lista e do mapa
    for marcador in self.marcadores:
      self.map.delete(marcador)
    self.marcadores = []

  def telainicial(self):
    self.f1 = tk.Frame(self.root)
    self.f1.pack(expand=1)
    self.f1.configure(bg='white')
    #PARTE DE INSERÇÃO DA IMAGEM
    self.pastaApp = os.path.dirname(__file__)
    self.imgLogo = tk.PhotoImage(file=self.pastaApp + "\\logo.png")
    self.l_logo = tk.Label(self.f1, image=self.imgLogo)
    self.l_logo.grid(row=0, column=0)
    #PARTE DE INSERÇÃO DA IMAGEM

    atualiza = tk.Button(self.f1,
                         text='Encontrar Vendedor',
                         command=lambda: self.inicializa_gui())
    atualiza.grid(row=3, column=0, columnspan=2)


def main():
  meuApp = tk.Tk()
  meuApp.geometry('1000x400')
  meuApp.title('Cadê meu lanche?')
  meuApp.configure(bg='white')
  meuApp.wm_iconbitmap('icon.ico')
  meuAppView = View(meuApp)

  tk.mainloop()

if __name__ == "__main__":
  main()
