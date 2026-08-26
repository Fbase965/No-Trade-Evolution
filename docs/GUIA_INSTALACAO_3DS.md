# Guia de Instalação no Nintendo 3DS Original (Luma3DS)

Este guia explica como instalar e ativar o Mod de "Evoluções Sem Troca" diretamente em um Nintendo 3DS com Luma3DS (CFW), funcionando tanto para cópias digitais (instaladas no SD) quanto para cartuchos físicos originais de Pokémon X ou Pokémon Y.

---

## 📋 Pré-requisitos
1. Um **Nintendo 3DS / 2DS** com desbloqueio padrão (**Luma3DS** instalado - versão 7.0 ou superior).
2. Cartão SD do console inserido no computador (ou acessado via FTP / microSD Management).
3. Jogo **Pokémon X** ou **Pokémon Y** (em cartucho físico ou baixado digitalmente).

---

## 🎮 Passo 1: Copiar os Arquivos do Mod para o Cartão SD

1. Conecte o cartão SD do seu 3DS ao computador.
2. Na pasta do Mod, acesse a pasta `Mod-Package/3DS_Luma3DS/`.
3. Copie a pasta `luma` inteira para a raiz (`root`) do cartão SD do 3DS.
   
A estrutura de pastas dentro do SD ficará assim:

* **Para Pokémon X:**
  `SD:/luma/titles/0004000000055D00/romfs/a/0/1/8`
* **Para Pokémon Y:**
  `SD:/luma/titles/0004000000055E00/romfs/a/0/1/8`

*(Nota: `0004000000055D00` é o Title ID universal de Pokémon X e `0004000000055E00` é o de Pokémon Y).*

---

## ⚙️ Passo 2: Ativar o "Game Patching" no Luma3DS

Para que o 3DS leia a pasta de modificações sem alterar o jogo original:

1. Coloque o cartão SD de volta no console 3DS.
2. Segure o botão **`SELECT`** do 3DS e aperte o botão de ligar (**`POWER`**).
3. O menu de configuração do **Luma3DS** vai abrir na tela.
4. Navegue com o direcional (D-Pad) até a opção:
   * **`(x) Enable game patching`**
5. Pressione **`A`** para marcar a opção com um `(x)`.
6. Pressione **`START`** para salvar e iniciar o console normalmente.

---

## 🌟 Passo 3: Jogar e Evoluir seus Pokémon!

1. Inicie o **Pokémon X** ou **Pokémon Y** normalmente pelo menu inicial do 3DS.
2. Durante o jogo:
   * Suba o nível do seu **Kadabra, Machoke, Haunter, Graveler, etc.** para o nível indicado na tabela (ex: Nível 37).
   * Eles irão iniciar a animação oficial de evolução automaticamente!
   * Use os itens (ex: *Metal Coat* no *Scyther*, *King's Rock* no *Poliwhirl*) diretamente da mochila.
3. O savegame é 100% normal e compatível! Não há risco de corrupção.

---

## 🛑 Como Desativar o Mod
Se você quiser voltar ao jogo 100% original:
* Basta apagar a pasta `romfs` de dentro de `SD:/luma/titles/0004000000055D00/` (ou `0004000000055E00/`), ou desmarcar a opção *Enable game patching* no menu do Luma3DS.
