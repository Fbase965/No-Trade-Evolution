# Como Gerar e Editar os Arquivos do Mod com o pk3DS

O **pk3DS** é a ferramenta padrão e mais completa da comunidade para edição de dados da 6ª geração de Pokémon (X, Y, Omega Ruby, Alpha Sapphire).

---

## 🛠️ Passo a Passo para Gerar os Arquivos de Modificação

### 1. Obter o pk3DS
* Baixe a versão mais recente do **pk3DS** (disponível no GitHub / ProjectPokemon).

### 2. Carregar a ROM / Pasta do Jogo
1. Abra o **pk3DS.exe**.
2. Clique em **File -> Open**.
3. Selecione a pasta onde estão os arquivos descriptografados da RomFS do Pokémon X ou Pokémon Y (ou uma ROM `.3ds` descriptografada).

### 3. Modificar as Evoluções
1. No menu principal do pk3DS, clique em **Personal Stats** (ou **Evolution Table**).
2. Para cada Pokémon da lista de trocas (consulte `docs/TABELA_EVOLUCOES.md`):
   * Selecione o Pokémon (ex: `Kadabra`).
   * No quadro de evoluções à direita:
     * Troque o método **`Trade`** por **`Level Up`** e defina o valor para **`37`**.
   * Para Pokémon que usavam itens na troca (ex: `Scyther` ou `Onix`):
     * Troque para **`Use Item`** e selecione o item correspondente (`Metal Coat`).
3. Clique em **Save** em cada Pokémon alterado.

### 4. Exportar a Pasta de Mod (LayeredFS)
1. Feche a janela de edição de evoluções.
2. O pk3DS gerará automaticamente o arquivo modificado dentro da pasta `a/0/1/8` (ou salvará na estrutura da RomFS).
3. Copie o arquivo `8` gerado (caminho: `romfs/a/0/1/8`) para o pacote de distribuição:
   * `Mod-Package/3DS_Luma3DS/luma/titles/0004000000055D00/romfs/a/0/1/8` (Pokémon X)
   * `Mod-Package/3DS_Luma3DS/luma/titles/0004000000055E00/romfs/a/0/1/8` (Pokémon Y)

---

## 📂 Formato Técnico dos Dados (GARC a/0/1/8)
* Em Pokémon X & Y, o arquivo `a/0/1/8` é um arquivo de contêiner GARC que contém até 8 slots de evolução por espécie de Pokémon (com ID do método, parâmetro de nível/item e ID do Pokémon resultante).
* Quando o Luma3DS intercepta a leitura do jogo pelo LayeredFS, ele substitui apenas esse arquivo na memória do console, mantendo todo o restante do jogo 100% original e intacto.
