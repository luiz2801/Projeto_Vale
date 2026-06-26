import os
import shutil

# Pastas que serão organizadas
PASTAS_ALVO = [
    os.path.join(os.getcwd(), "resultados"),
    os.path.join(os.getcwd(), "notebooks")
]

# Prefixos dos meses identificados no seu projeto
MESES_VALIDOS = ["jan", "feb", "marco", "apr", "may", "jun"]

def organizar_por_mes():
    total_arquivos_movidos = 0

    for pasta_origem in PASTAS_ALVO:
        if not os.path.exists(pasta_origem):
            print(f"Aviso: A pasta '{pasta_origem}' não foi encontrada. Pulando...")
            continue

        print(f"\nOrganizando a pasta: {os.path.basename(pasta_origem)}/...")
        arquivos = os.listdir(pasta_origem)
        arquivos_na_pasta = 0

        for arquivo in arquivos:
            caminho_completo = os.path.join(pasta_origem, arquivo)

            # Garante que estamos movendo apenas arquivos (ignora pastas já criadas)
            if os.path.isfile(caminho_completo):
                for mes in MESES_VALIDOS:
                    # Verifica se o arquivo começa com o mês (ex: "jan_" ou "jan_limpo")
                    if arquivo.startswith(f"{mes}_") or arquivo.startswith(f"{mes}."):
                        pasta_destino = os.path.join(pasta_origem, mes)

                        # Cria a subpasta do mês dentro de notebooks ou resultados se não existir
                        os.makedirs(pasta_destino, exist_ok=True)

                        # Move o arquivo
                        novo_caminho = os.path.join(pasta_destino, arquivo)
                        shutil.move(caminho_completo, novo_caminho)

                        print(f"  -> {arquivo} movido para {os.path.basename(pasta_origem)}/{mes}/")
                        arquivos_na_pasta += 1
                        break
        
        total_arquivos_movidos += arquivos_na_pasta
        if arquivos_na_pasta == 0:
            print("  Nenhum arquivo pendente encontrado nesta pasta.")

    print(f"\n[FIM] Organização concluída! Total de arquivos movidos: {total_arquivos_movidos}")

if __name__ == "__main__":
    organizar_por_mes()