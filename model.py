''''
Projeto Vendedores ambulante UFRN

Authors: Maria Luiza
         Rosa Pedrosa
'''
import json
from typing import List, Tuple
import tkinter as tk
import tkintermapview as tkmv
from tkinter import messagebox


class Vendedor:

  def __init__(self, nome, pagamento, lista_prod, local, lat, lon):
    self._nome = nome
    self._pagamento = pagamento
    self._latitude = lat
    self._longitude = lon
    self._local = local
    self.produtos = lista_prod

  def __repr__(self) -> str:
    return self._nome

  @property
  def nome(self) -> str:
    '''
        Retorna o nome do vendedor.
        '''
    return self._nome

  @property
  def latitude(self) -> float:
    '''
        Retorna a latitude do vendedor
        em que o vendedor está
        '''
    return self._lat

  @property
  def longitude(self) -> float:
    '''
        Retorna a longitude
        em que o vendedor está
        '''
    return self._lon


class BDVendedor:
  '''
    Representa um banco de dados de
    vendedores
    (classe de busca do programa).
    '''

  def __init__(self):
    with open("bd_vendedores.json", encoding='utf-8') as bd_vendedores:
      self._dados = json.load(bd_vendedores)

  def processa(self, vendedores: List[Vendedor]):
    '''
        Adiciona os dados dos vendedores ao banco de dados.
        '''
    for vendedor in vendedores:
      dados_vendedor = {
        'nome': vendedor._nome,
        'produtos': vendedor.produtos,
        'pagamento': vendedor._pagamento,
        'longitude': vendedor._longitude,
        'latitude': vendedor._latitude,
      }
      self._dados.append(dados_vendedor)

    # Salvar os dados atualizados no arquivo JSON
    with open("bd_vendedores.json", 'w', encoding='utf-8') as bd_vendedores:
      json.dump(self._dados, bd_vendedores, ensure_ascii=False, indent=2)

  @property
  def qnt_vendedores(self) -> int:
    '''
        Retorna a quantidade de vendedores
        no banco de dados.
        '''
    cont = 0
    for i in range(len(self._dados)):
      cont = cont + 1

    return cont

  def todos(self) -> List[Vendedor]:
    '''
        Imprime todas os vendedores disponiveis
        no banco de dados.        '''
    self.todos = list()
    for vendedor in self._dados:
      self.todos.append(vendedor)

    return self.todos

  def busca_por_nome(self, texto: str) -> List[Vendedor]:
    '''
        Retorna uma lista contendo
        todos os vendedores do banco de dados
        cujo nome contenha o texto passado
        como parâmetro.
        '''
    self.texto = texto
    vendedores = []
    cont = 0
    for vendedor in self._dados:
      if vendedor["nome"] == self.texto:
        vendedores.append(vendedor)
        cont += 1

    if cont <= 0:
      self.erro_nao_contem_vendedor()
    else:
      return vendedores

  def erro_nao_contem_vendedor(self):
    messagebox.showerror("Erro",
                         "Vendedor não encontrado! Insira um nome válido!")


  def busca_por_produto(self, produto: str) -> List[Vendedor]:
    vendedores_com_produto = []
    cont = 0
    for vendedor in self._dados:
      if produto in vendedor["produtos"]:
        vendedores_com_produto.append(vendedor)
        cont += 1

    if cont <= 0:
      self.erro_nao_possui_produto()
    else:
      return vendedores_com_produto

  def erro_nao_possui_produto(self):
    messagebox.showerror("Erro",
                         "Produto não encontrado. Insira um produto válido!")

  def busca_por_local(self, local: str) -> List[Vendedor]:
    '''
    Retorna uma lista contendo todos os vendedores do banco de dados
    cujo local é passado como parâmetro.
    '''
    vendedores_no_local = []
    cont = 0
    for vendedor in self._dados:
      if local in vendedor['local']:
        vendedores_no_local.append(vendedor)
        cont += 1
    return vendedores_no_local


def main():
  bd = BDVendedor()
  
if __name__ == '__main__':
  main()