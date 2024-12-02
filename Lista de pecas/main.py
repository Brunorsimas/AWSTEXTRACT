import json
import boto3
from botocore.exceptions import ClientError
from pathlib import Path


def detect_file_text() -> list[str]:
    """
    Processa a imagem 'pecas.png' localizada no mesmo diretório do script 
    usando AWS Textract e retorna as linhas de texto detectadas.

    :return: Lista de textos detectados na imagem.
    """
    # Inicializa o cliente Textract
    client = boto3.client("textract", region_name="us-east-1")

    # Caminho do arquivo (mesmo diretório do script)
    file_path = Path(__file__).parent / "pecas.png"

    # Verifica se o arquivo existe
    if not file_path.exists():
        print(f"Erro: Arquivo 'pecas.png' não encontrado no diretório: {file_path.parent}")
        return []

    # Lê o arquivo como bytes
    with open(file_path, "rb") as f:
        document_bytes = f.read()

    try:
        # Chama o Textract para detectar texto na imagem
        response = client.detect_document_text(Document={"Bytes": document_bytes})

        # Filtra apenas as linhas de texto detectadas
        return [block["Text"] for block in response["Blocks"] if block["BlockType"] == "LINE"]
    except ClientError as e:
        print(f"Erro processando a imagem: {e}")
        return []


if __name__ == "__main__":
    # Processa a imagem
    lines = detect_file_text()

    # Exibe os resultados
    if lines:
        print("Peças detectadas na imagem:")
        for line in lines:
            print(f"- {line}")
    else:
        print("Nenhum texto detectado ou erro no processamento.")
