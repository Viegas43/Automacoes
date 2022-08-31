from os import scandir, rename
from os.path import splitext, exists, join
from shutil import move
from time import sleep

import logging

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


pasta_dowloads = r""
pasta_audios_whatsapp = r""
pasta_musica = r""
pasta_video = r""
pasta_imagem = r""
pasta_documentos = r""
pasta_python = r""
pasta_pdf = r""


image_extensions = [".jpg", ".jpeg", ".jpe", ".jif", ".jfif", ".jfi", ".png",
                    ".gif", ".webp", ".tiff", ".tif", ".psd", ".raw", ".arw",
                    ".cr2", ".nrw", ".k25", ".bmp", ".dib", ".heif", ".heic",
                    ".ind", ".indd", ".indt", ".jp2", ".j2k", ".jpf",
                    ".jpf", ".jpx", ".jpm", ".mj2", ".svg", ".svgz", ".ai",
                    ".eps", ".ico"]
video_extensions = [".webm", ".mpg", ".mp2", ".mpeg", ".mpe", ".mpv",
                    ".mp4", ".mp4v", ".m4v", ".avi", ".wmv", ".mov", ".qt",
                    ".flv", ".swf", ".avchd"]
audio_extensions = [".m4a", ".flac", "mp3", ".wav", ".wma", ".aac", ".ogg"]
document_extensions = [".doc", ".docx", ".odt",
                       ".pdf", ".xls", ".xlsx", ".ppt", ".pptx"]
arquivos_py = [".py"]


def virar_unitario(destino, nome):
    nome_arquivo, extension = splitext(nome)
    counter = 1
    # * SE O ARQUIVO EXISTIR, ADICIONA UM NUMERO AO FINAL DO NOME DO ARQUIVO
    # (caso vc baixe um arquivo duas vezes ou apresente o mesmo nome)
    while exists(f"{destino}/{nome}"):
        nome = f"{nome_arquivo}({str(counter)}){extension}"
        counter += 1

    return nome


def mover_arquivo(destino, entrada, nome):
    if exists(f"{destino}/{nome}"):
        nome_unico = virar_unitario(destino, nome)
        nome_antigo = join(destino, nome)
        nome_novo = join(destino, nome_unico)
        rename(nome_antigo, nome_novo)
    move(entrada, destino)


class ManipuladorDeMudancas(FileSystemEventHandler):
    # * ESSA FUNCAO IRA RODAR TODA VEZ QUE HOUVER ALGUMA MUDANCA NA VARIAVEL "pasta_downloads" (se qualquer arquivo for baixado enquando tiver rodando o programa)
    # *.UPPER É PARA NAO PERDER NENHUM ARQUIVO QUE ESTEJA EM CAIXA ALTA
    def on_modified(self, event):
        with scandir(pasta_dowloads) as entries:
            for entrada in entries:
                nome = entrada.name
                self.checando_arquivo_de_audio(entrada, nome)
                self.checando_arquivo_de_video(entrada, nome)
                self.checando_arquivo_de_imagem(entrada, nome)
                self.checando_arquivo_de_documentos(entrada, nome)
                self.checando_arquivo_py(entrada, nome)

    def checando_arquivo_de_audio(self, entrada, nome):  # * CHECA TODOS OS ARQUIVOS DE AUDIO
        for audio_extension in audio_extensions:
            if nome.endswith(audio_extension) or nome.endswith(audio_extension.upper()):
                if entrada.stat().st_size < 1_000_000:
                    destino = pasta_audios_whatsapp
                else:
                    destino = pasta_musica
                mover_arquivo(destino, entrada, nome)
                logging.info(f"Arquivo de audio movido: {nome}")

    def checando_arquivo_de_video(self, entrada, nome):  # * CHECA TODOS OS ARQUIVOS DE VIDEO
        for video_extension in video_extensions:
            if nome.endswith(video_extension) or nome.endswith(video_extension.upper()):
                mover_arquivo(pasta_video, entrada, nome)
                logging.info(f"Arquivo de video movido: {nome}")

    def checando_arquivo_de_imagem(self, entrada, nome):  # * CHECA TODOS OS ARQUIVOS DE IMAGEM
        for image_extension in image_extensions:
            if nome.endswith(image_extension) or nome.endswith(image_extension.upper()):
                mover_arquivo(pasta_imagem, entrada, nome)
                logging.info(f"Arquivo de imagem movido: {nome}")

    def checando_arquivo_de_documentos(self, entrada, nome):  # * CHECA TODOS OS ARQUIVOS DE DOCUMENTOS
        for documents_extension in document_extensions:
            if nome.endswith(documents_extension) or nome.endswith(documents_extension.upper()):
                if nome.endswith('.pdf'):
                    destino = pasta_pdf
                else:
                    destino = pasta_documentos
                mover_arquivo(destino, entrada, nome)
                logging.info(f"Documento movido: {nome}")

    def checando_arquivo_py(self, entrada, nome):  # * CHECA TODOS OS ARQUIVOS DE PYTHON
        for arquivo_py in arquivos_py:
            if nome.endswith(arquivo_py) or nome.endswith(arquivo_py.upper()):
                mover_arquivo(pasta_python, entrada, nome)
                logging.info(f"Arquivo python movido {nome}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = pasta_dowloads
    event_handler = ManipuladorDeMudancas()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
