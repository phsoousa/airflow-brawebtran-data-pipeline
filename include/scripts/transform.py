from pathlib import Path
from datetime import datetime
import zipfile
import pandas as pd


BASE_PATH = Path("/usr/local/airflow/desktop_downloads")
DATA_HOJE = datetime.now().strftime("%Y-%m-%d")

PASTA_ORIGEM = BASE_PATH / DATA_HOJE
PASTA_TRATADA = BASE_PATH / DATA_HOJE / "processed"

PASTA_TRATADA.mkdir(parents=True, exist_ok=True)


def encontrar_arquivo_mais_recente(pasta: Path):
    arquivos = [
        arquivo for arquivo in pasta.iterdir()
        if arquivo.is_file()
    ]

    if not arquivos:
        raise FileNotFoundError(f"Nenhum arquivo encontrado em {pasta}")

    return max(arquivos, key=lambda arquivo: arquivo.stat().st_mtime)


def ler_arquivo(caminho_arquivo: Path):
    extensao = caminho_arquivo.suffix.lower()

    if extensao == ".zip":
        pasta_extraida = caminho_arquivo.parent / "extracted"
        pasta_extraida.mkdir(parents=True, exist_ok=True)

        with zipfile.ZipFile(caminho_arquivo, "r") as zip_ref:
            zip_ref.extractall(pasta_extraida)

        arquivos_extraidos = [
            arquivo for arquivo in pasta_extraida.iterdir()
            if arquivo.is_file()
        ]

        if not arquivos_extraidos:
            raise FileNotFoundError("Nenhum arquivo encontrado dentro do ZIP.")

        arquivo_interno = arquivos_extraidos[0]
        print(f"Arquivo extraído: {arquivo_interno}")

        return ler_arquivo(arquivo_interno)

    if extensao == ".csv":
        return pd.read_csv(
            caminho_arquivo,
            sep=";",
            encoding="latin1",
            on_bad_lines="skip"
        )

    if extensao == ".txt":
        return pd.read_csv(
            caminho_arquivo,
            sep=";",
            encoding="latin1",
            on_bad_lines="skip"
        )

    if extensao in [".xlsx", ".xls"]:
        return pd.read_excel(caminho_arquivo)

    raise ValueError(f"Formato não suportado: {extensao}")


def tratar_dados(df: pd.DataFrame):
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )

    linhas_antes = len(df)

    df = df.dropna(how="all")
    df = df.drop_duplicates()

    for coluna in df.select_dtypes(include="object").columns:
        df[coluna] = df[coluna].astype(str).str.strip()

    df["data_processamento"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    linhas_depois = len(df)
    duplicados_removidos = linhas_antes - linhas_depois

    print(f"Linhas antes do tratamento: {linhas_antes}")
    print(f"Linhas depois do tratamento: {linhas_depois}")
    print(f"Linhas removidas: {duplicados_removidos}")

    return df


def salvar_dados(df: pd.DataFrame):
    caminho_csv = PASTA_TRATADA / "dados_tratados.csv"
    caminho_parquet = PASTA_TRATADA / "dados_tratados.parquet"

    df.to_csv(caminho_csv, index=False, encoding="utf-8-sig")
    df.to_parquet(caminho_parquet, index=False)

    print(f"CSV tratado salvo em: {caminho_csv}")
    print(f"Parquet tratado salvo em: {caminho_parquet}")


def main():
    arquivo = encontrar_arquivo_mais_recente(PASTA_ORIGEM)

    print(f"Arquivo encontrado: {arquivo}")

    df = ler_arquivo(arquivo)

    df_tratado = tratar_dados(df)

    salvar_dados(df_tratado)


if __name__ == "__main__":
    main()