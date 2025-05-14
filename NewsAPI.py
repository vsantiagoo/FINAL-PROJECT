import requests
import os
from dotenv import load_dotenv

load_dotenv()


API_KEY = os.getenv('API_KEY_NEWS')
BASE_URL = 'https://newsapi.org/v2/everything'  

historico_temas = []
total_noticias = 0

def buscar_noticias(tema, quantidade):
    global total_noticias

    if not API_KEY:
        print("❌ API Key não encontrada. Verifique seu arquivo .env.")
        return

    # Parâmetros da requisição
    params = {
        'q': tema,
        'pageSize': quantidade,
        'apiKey': API_KEY,
        'sortBy': 'publishedAt',
        'language': 'pt'
    }

    try:
        resposta = requests.get(BASE_URL, params=params)
        print("🔎 URL gerada:", resposta.url)  
        dados = resposta.json()

        if resposta.status_code != 200 or dados.get("status") != "ok":
            print("❌ Erro ao buscar notícias.")
            print("🔍 Status code:", resposta.status_code)
            print("🔍 Detalhes do erro:", dados.get("message", "Sem mensagem da API"))
            print("📬 Cabeçalhos da resposta:", resposta.headers)
            return

        artigos = dados.get("articles", [])
        if not artigos:
            print("⚠️ Nenhuma notícia encontrada para o tema:", tema)
            return

        print(f"\n📰 Notícias sobre '{tema}':")
        for i, artigo in enumerate(artigos, 1):
            titulo = artigo.get('title', 'Sem título')
            fonte = artigo.get('source', {}).get('name', 'Fonte desconhecida')
            autor = artigo.get('author', 'Autor desconhecido')
            url = artigo.get('url', 'Sem URL')

            print(f"\n[{i}] Título: {titulo}")
            print(f"     Fonte: {fonte}")
            print(f"     Autor: {autor}")
            print(f"     URL: {url}")

        historico_temas.append((tema, quantidade))
        total_noticias += len(artigos)

    except Exception as e:
        print("❌ Erro na requisição:", e)

def menu_interativo():
    while True:
        print("\n===== MENU DE NOTÍCIAS =====")
        print("1. Buscar notícias")
        print("2. Sair e mostrar histórico")
        opcao = input("Escolha uma opção (1 ou 2): ") 

        if opcao == '1':
            tema = input("Informe o tema da notícia: ").strip()

            while True:
                try:
                    quantidade = int(input("Quantas notícias deseja (máx 5)? "))
                    if 1 <= quantidade <= 5:
                        break
                    else:
                        print("❗ Por favor, escolha entre 1 e 5 notícias.")
                except ValueError:
                    print("❗ Entrada inválida. Digite um número inteiro.")

            buscar_noticias(tema, quantidade)

        elif opcao == '2':
            print("\n===== HISTÓRICO DE BUSCAS =====")
            for tema, quant in historico_temas:
                print(f"- Tema: {tema} | Notícias solicitadas: {quant}")
            print(f"\nTotal de notícias retornadas: {total_noticias}")
            print("Saindo... 👋")
            break
        else:
            print("❗ Opção inválida. Tente novamente.")

if __name__ == '__main__':
    menu_interativo()
