# Zenith Navigator

Mini navegador local em Python usando PyQt6 e PyQt6-WebEngine.

## Recursos implementados
- Navegador GUI com abas, barra de endereço, voltar/avançar/recarregar/home
- Homepage local estilo Google com barra de pesquisa web funcional
- Menu de idiomas para Português e Inglês
- Permissões de câmera, microfone, geolocalização e notificações
- Console avançado acessível via Configurações
- Engine selector para HTML, CSS, JS, TS e Legacy PHP
- Mini-games locais: Calculadora, Jogo da Cobrinha e Jogo do Dino
- Página offline de exemplo
- DevTools para inspeção web
- Estilo moderno com transparência e blur

## Como usar
1. Instale as dependências:

```powershell
py -m pip install PyQt6 PyQt6-WebEngine
```

2. Execute o navegador:

```powershell
py main.py
```

3. Abra o menu `Apps` para acessar jogos e ferramentas locais.
4. Use o menu `Visualizar` para alternar DevTools ou selecionar o tipo de engine.
5. Ative o console avançado em `Configurações` para comandos internos.

## Arquivos principais
- `main.py` - navegador e interface principal
- `home_page.html` - homepage local
- `home_page.css` - estilo da homepage
- `localpy.py` - utilitário local para cálculo seguro
- `snake.html` - jogo da cobrinha local
- `dino.html` - jogo do Dino local
- `calc.html` - calculadora local
- `offline.html` - página exibida em modo sem conexão
- `installer.py` - script de instalação e atalho
- `requirements.txt` - dependências do projeto

## Preparado para GitHub
Inclui estrutura para publicação, `README.md` com instruções, `requirements.txt`, `.gitignore` e histórico do projeto.
