import json
import os

# Caminhos dos arquivos para persistência
POSTS_FILE = "posts.json"
COMENTARIOS_FILE = "comentarios.json"

# Simulando banco de dados de usuários
usuarios = {
    1: {"email": "pedro@example.com", "senha": "123"},
    2: {"email": "laura@example.com", "senha": "456"},
    3: {"email": "ricardo@example.com", "senha": "789"},
}

# Funções para carregar e salvar dados em JSON
def carregar_dados(caminho):
    if os.path.exists(caminho):
        with open(caminho, "r") as f:
            return json.load(f)
    return []

def salvar_dados(caminho, dados):
    with open(caminho, "w") as f:
        json.dump(dados, f, indent=2)

posts_salvos = carregar_dados(POSTS_FILE)
comentarios_salvos = carregar_dados(COMENTARIOS_FILE)

# Menu de login
def login():
    print("\n=== LOGIN ===")
    for uid, user in usuarios.items():
        print(f"{uid} - {user['email']}")
    while True:
        try:
            user_id = int(input("Digite o ID do usuário: "))
            if user_id not in usuarios:
                print("ID inválido. Tente novamente.")
                continue
            senha = input("Digite a senha: ")
            if usuarios[user_id]["senha"] == senha:
                print("Login bem-sucedido!")
                return user_id
            else:
                print("Senha incorreta.")
        except:
            print("Entrada inválida. Tente novamente.")

# Visualizar posts
def ver_todos_os_posts():
    if not posts_salvos:
        print("Nenhum post cadastrado ainda.")
        return
    for post in posts_salvos:
        print(f"\nPost ID: {post['id']} | Autor: {post['user_id']}")
        print(f"Título: {post['title']}\nConteúdo: {post['body']}")
        for comentario in comentarios_salvos:
            if comentario['post_id'] == post['id']:
                autor_nome = usuarios.get(comentario['user_id'], {}).get('email', 'Desconhecido')
                print(f"  Comentário {comentario['id']} ({comentario['user_id']} - {autor_nome}): {comentario['body']}")

# Ver meus posts
def ver_meus_posts(user_id):
    meus = [p for p in posts_salvos if p['user_id'] == user_id]
    if not meus:
        print("Você não tem posts ainda.")
        return
    for post in meus:
        print(f"\nPost ID: {post['id']}\nTítulo: {post['title']}\nConteúdo: {post['body']}")

# Ver posts de outro usuário
def ver_posts_de_outro():
    while True:
        try:
            uid = int(input("ID do usuário: "))
            if uid not in usuarios:
                print("ID inválido. Tente novamente.")
                continue
            posts = [p for p in posts_salvos if p['user_id'] == uid]
            if not posts:
                print("Este usuário não tem posts.")
            for post in posts:
                print(f"\nPost ID: {post['id']}\nTítulo: {post['title']}\nConteúdo: {post['body']}")
            break
        except:
            print("Entrada inválida. Tente novamente.")

# Criar post
def criar_post(user_id):
    title = input("Título do post: ")
    body = input("Conteúdo do post: ")
    novo_post = {
        "id": len(posts_salvos) + 1,
        "user_id": user_id,
        "title": title,
        "body": body
    }
    posts_salvos.append(novo_post)
    salvar_dados(POSTS_FILE, posts_salvos)
    print("Post criado com sucesso!")

# Criar comentário
def comentar():
    try:
        post_id = int(input("ID do post para comentar: "))
        post = next((p for p in posts_salvos if p['id'] == post_id), None)
        if not post:
            print("Post não encontrado.")
            return
        uid = int(input("ID do usuário que comenta: "))
        if uid not in usuarios:
            print("Usuário inválido.")
            return
        body = input("Comentário: ")
        novo = {
            "id": len(comentarios_salvos) + 1,
            "post_id": post_id,
            "user_id": uid,
            "body": body
        }
        comentarios_salvos.append(novo)
        salvar_dados(COMENTARIOS_FILE, comentarios_salvos)
        print("Comentário adicionado!")
    except:
        print("Erro ao comentar.")

# Editar comentário
def editar_comentario(user_id):
    cid = int(input("ID do comentário para editar: "))
    for c in comentarios_salvos:
        if c['id'] == cid and c['user_id'] == user_id:
            c['body'] = input("Novo texto: ")
            salvar_dados(COMENTARIOS_FILE, comentarios_salvos)
            print("Comentário atualizado!")
            return
    print("Comentário não encontrado ou você não tem permissão.")

# Excluir post
def excluir_post(user_id):
    pid = int(input("ID do post a excluir: "))
    global posts_salvos, comentarios_salvos
    post = next((p for p in posts_salvos if p['id'] == pid), None)
    if post and post['user_id'] == user_id:
        posts_salvos = [p for p in posts_salvos if p['id'] != pid]
        comentarios_salvos = [c for c in comentarios_salvos if c['post_id'] != pid]
        salvar_dados(POSTS_FILE, posts_salvos)
        salvar_dados(COMENTARIOS_FILE, comentarios_salvos)
        print("Post e comentários excluídos!")
    else:
        print("Post não encontrado ou sem permissão.")

# Excluir comentário em seu post
def excluir_comentario_em_post(user_id):
    cid = int(input("ID do comentário a excluir: "))
    comentario = next((c for c in comentarios_salvos if c['id'] == cid), None)
    if not comentario:
        print("Comentário não encontrado.")
        return
    post = next((p for p in posts_salvos if p['id'] == comentario['post_id']), None)
    if post and post['user_id'] == user_id:
        comentarios_salvos.remove(comentario)
        salvar_dados(COMENTARIOS_FILE, comentarios_salvos)
        print("Comentário excluído do seu post.")
    else:
        print("Sem permissão para excluir esse comentário.")

# Menu principal
def menu():
    while True:
        user_id = login()
        if not user_id:
            continue
        while True:
            print("\n=== MENU ===")
            print("1 - Ver todos os posts")
            print("2 - Ver meus posts")
            print("3 - Ver posts de outro usuário")
            print("4 - Criar post")
            print("5 - Comentar em um post")
            print("6 - Editar um comentário meu")
            print("7 - Excluir um post meu")
            print("8 - Excluir comentário em meu post")
            print("9 - Trocar de usuário")
            print("0 - Sair")
            opcao = input("Escolha: ")
            if opcao == "1":
                ver_todos_os_posts()
            elif opcao == "2":
                ver_meus_posts(user_id)
            elif opcao == "3":
                ver_posts_de_outro()
            elif opcao == "4":
                criar_post(user_id)
            elif opcao == "5":
                comentar()
            elif opcao == "6":
                editar_comentario(user_id)
            elif opcao == "7":
                excluir_post(user_id)
            elif opcao == "8":
                excluir_comentario_em_post(user_id)
            elif opcao == "9":
                break  # Trocar de usuário
            elif opcao == "0":
                print("Saindo...")
                return
            else:
                print("Opção inválida.")

if __name__ == "__main__":
    menu()
