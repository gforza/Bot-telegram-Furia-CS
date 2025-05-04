# 🤖 Bot da FURIA - Telegram

Um bot do Telegram que fornece informações atualizadas sobre a FURIA no cenário de Counter-Strike.

## 📋 Funcionalidades

### Comandos Disponíveis

- `/start` - Inicia o bot e mostra o menu principal
- `/Sobre` - Exibe a história da FURIA no CS
- `/Jogadores` - Menu para visualizar a line atual
  - `/LineNomes` - Mostra apenas os nomes dos jogadores
  - `/LineFotos` - Mostra fotos e nomes dos jogadores
- `/Estatisticas` - Menu de estatísticas
  - `/mapas` - Mostra estatísticas por mapa dos últimos 3 meses
- `/Proximos_eventos` - Lista os próximos campeonatos
- `/Proximas_partidas` - Mostra as próximas partidas agendadas
- `/Resultados` - Exibe os últimos resultados do time
- `/Noticias` - Mostra as últimas notícias da FURIA
- `/MaisNoticias` - Carrega mais notícias (pode ser usado com número: `/MaisNoticias 4`)
- `/Ajuda` - Exibe a lista de comandos disponíveis

## 🛠️ Tecnologias Utilizadas

- Python 3.x
- Telebot (API do Telegram)
- Selenium (Web Scraping)
- BeautifulSoup4 (Parser HTML)
- Chrome WebDriver (Automação)

## 📦 Dependências

```
telebot
requests
selenium
beautifulsoup4
```

## ⚙️ Configuração

1. Clone o repositório:
```bash
git clone [URL_DO_REPOSITÓRIO]
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Configure o token do bot:
- Substitua o token no arquivo `main.py` pelo seu token do BotFather

4. Instale o Chrome WebDriver:
- Certifique-se de ter o Google Chrome instalado
- Baixe a versão do ChromeDriver compatível com sua versão do Chrome

## 🚀 Executando o Bot

```bash
python main.py
```

## 🔄 Fontes de Dados

- HLTV.org - Informações sobre jogadores, estatísticas e partidas
- TheMove.gg - Notícias e atualizações do cenário

## ⚠️ Limitações

- O bot depende de conexão com a internet
- As fontes de dados podem ter limitações de acesso
- O WebDriver precisa estar atualizado e compatível com o Chrome

## 🤝 Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. Faça um Fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 📧 Contato

Para sugestões ou reportar bugs, abra uma issue no GitHub. 