import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageDraw  # Adicionado ImageDraw
from database import conexao, criar_tabela, inserir_palavra, obter_palavra_aleatoria
from game_logic import JogoDaForca
import os

class JogoDaForcaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Jogo da Forca")
        self.root.geometry("800x600")

        self.database = "database/palavras.db"
        self.carregar_imagens()
        self.criar_widgets()  # Move this before iniciar_jogo
        self.iniciar_jogo()

    def carregar_imagens(self):
        self.imagens = []
        for i in range(7):  # 0 a 6
            try:
                img_path = f"imagens/{i}.png"
                img = Image.open(img_path)
                img = img.resize((300, 300), Image.LANCZOS)
                self.imagens.append(ImageTk.PhotoImage(img))
            except FileNotFoundError:
                # Cria imagem padrão branca com texto
                img = Image.new('RGB', (300, 300), color='white')
                draw = ImageDraw.Draw(img)
                draw.text((100, 140), f"Estágio {i}", fill='black')
                self.imagens.append(ImageTk.PhotoImage(img))
                print(f"Imagem {i}.png não encontrada. Usando substituto.")

    def iniciar_jogo(self):
        conn = conexao(self.database)
        if conn:
            resultado = obter_palavra_aleatoria(conn)
            conn.close()
            
            if resultado:
                palavra, tema = resultado
                self.jogo = JogoDaForca(palavra, tema)
            else:
                # Fallback se não houver palavras no banco
                self.jogo = JogoDaForca("PYTHON", "Linguagem")
            self.atualizar_tela()

    def criar_widgets(self):
        main_frame = tk.Frame(self.root, padx=10, pady=10)
        main_frame.pack(expand=True, fill=tk.BOTH)

        img_frame = tk.Frame(main_frame)
        img_frame.pack(side=tk.TOP, pady=5)

        self.label_imagem = tk.Label(img_frame)
        self.label_imagem.pack()

        game_frame = tk.Frame(main_frame)
        game_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

        self.label_tema = tk.Label(game_frame, text="Tema: ", font=("Arial", 16))
        self.label_tema.pack(pady=20)

        self.label_palavra = tk.Label(game_frame, text="", font=("Arial", 24))  # Add this line
        self.label_palavra.pack(pady=10)  # Add this line

        self.label_erradas = tk.Label(game_frame, text="Letras erradas: ", font=("Arial", 16))
        self.label_erradas.pack(pady=5)
        self.label_letras_erradas = tk.Label(game_frame, text="", font=("Arial", 16))
        self.label_letras_erradas.pack()

        self.label_tentativas = tk.Label(game_frame, text="Tentativas restantes: ", font=("Arial", 16))
        self.label_tentativas.pack(pady=5)

        self.entry_letra = tk.Frame(game_frame)
        self.entry_letra.pack(pady=10)

        tk.Label(self.entry_letra, text="Digite uma letra: ", font=("Arial", 16)).pack(side=tk.LEFT)
        self.entry = tk.Entry(self.entry_letra, font=("Arial", 16), width=5)
        self.entry.pack(side=tk.LEFT)
        self.entry.bind("<Return>", lambda e: self.adivinhar_letra())

        self.button_adivinhar = tk.Button(self.entry_letra, text="Adivinhar", font=("Arial", 16), command=self.adivinhar_letra)
        self.button_adivinhar.pack(side=tk.LEFT, padx=5)

        self.button_reiniciar = tk.Button(game_frame, text="Reiniciar", font=("Arial", 16), command=self.reiniciar_jogo)
        self.button_reiniciar.pack(pady=10)

    def adivinhar_letra(self):
        letra = self.entry.get().upper()
        self.entry.delete(0, tk.END)
        
        if not letra.isalpha() or len(letra) != 1:
            messagebox.showwarning("Entrada inválida", "Digite apenas uma letra.")
            return
        
        resultado = self.jogo.adivinhar_letra(letra)
        
        if resultado is None:
            messagebox.showinfo("Tentativa repetida", "Você já tentou essa letra.")
            return
        elif not resultado:
            self.root.bell()
        
        self.atualizar_tela()
        
        if self.jogo.verificar_vitoria():
            messagebox.showinfo("Vitória!", f"Você adivinhou a palavra: {self.jogo.palavra}")
            self.reiniciar_jogo()
        elif self.jogo.verificar_derrota():
            messagebox.showinfo("Derrota!", f"Você perdeu! A palavra era: {self.jogo.palavra}")
            self.reiniciar_jogo()
        
    def atualizar_tela(self):
        status = self.jogo.get_status()
        
        self.label_imagem.config(image=self.imagens[status['tentativas_feitas']])
        
        # Corrigido para mostrar a palavra oculta
        self.label_palavra.config(text=self.jogo.palavra_descoberta())
        
        self.label_tema.config(text=f"Tema: {status['tema']}")
        
        self.label_letras_erradas.config(text=" ".join(sorted(status['letras_erradas'])))
        
        self.label_tentativas.config(text=f"Tentativas restantes: {status['tentativas_max'] - status['tentativas_feitas']}")

    def reiniciar_jogo(self):
        self.iniciar_jogo()

if __name__ == "__main__":

    if not os.path.exists("imagens"):
        os.makedirs("imagens")

    root = tk.Tk()
    app = JogoDaForcaGUI(root)
    root.mainloop()


