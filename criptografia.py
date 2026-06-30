import customtkinter as ctk
from tkinter import messagebox, filedialog, PhotoImage, Menu
import cryptocode
import string
import secrets
import sys
import os

# Configuração global de aparência e cores do CustomTkinter
ctk.set_appearance_mode("System")  # Detecta o modo do sistema operacional (Escuro/Claro)
ctk.set_default_color_theme("blue")  # Tema padrão de cores

def resource_path(relative_path):
    """
    Retorna o caminho absoluto de um recurso.
    Compatível com execução direta e com executável gerado pelo PyInstaller (--onefile).
    """
    try:
        # Quando executado via PyInstaller, sys._MEIPASS aponta para a pasta temporária
        base_path = sys._MEIPASS
    except AttributeError:
        # Em modo de desenvolvimento, usa o diretório do próprio arquivo script
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

class Criptografia(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        self.chave = ""
        self.Encriptografar()
        self.mainloop()
    
    def Encriptografar(self):
        # Configurações básicas da janela
        self.title("MAIA PASS - Criptografar e decriptografar mensagens")
        self.geometry("780x660")
        self.minsize(700, 600)
        
        # Carregamento do favicon dinâmico baseado no Sistema Operacional
        try:
            favicon_png = resource_path(os.path.join("icones", "favicon512.png"))
            favicon_ico = resource_path(os.path.join("icones", "favicon.ico"))
            
            if sys.platform.startswith('win'):
                if os.path.exists(favicon_ico):
                    self.iconbitmap(favicon_ico)
                elif os.path.exists(favicon_png):
                    self.favicon = PhotoImage(file=favicon_png)
                    self.iconphoto(True, self.favicon)
            else:
                if os.path.exists(favicon_png):
                    self.favicon = PhotoImage(file=favicon_png)
                    self.iconphoto(True, self.favicon)
        except Exception as e:
            sys.stderr.write(f"Aviso: Não foi possível carregar o ícone: {e}\n")

        # Barra de menus clássica no topo (mantendo compatibilidade)
        try:
            barraDeMenu = Menu(self)
            menuArquivo = Menu(barraDeMenu, tearoff=0)
            barraDeMenu.add_cascade(label="Arquivo", menu=menuArquivo)
            menuArquivo.add_command(label="Abrir chave", command=self.AbrirChave)
            self.config(menu=barraDeMenu)
        except Exception as e:
            sys.stderr.write(f"Aviso: Erro ao carregar menu superior: {e}\n")

        # Configuração do layout principal em grade (Grid)
        self.grid_columnconfigure(0, weight=0)  # Barra lateral estática
        self.grid_columnconfigure(1, weight=1)  # Conteúdo principal responsivo
        self.grid_rowconfigure(0, weight=1)

        # ==========================================
        # BARRA LATERAL (Painel de Chaves e Temas)
        # ==========================================
        self.sidebar_frame = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(7, weight=1)  # Espaçador dinâmico inferior

        # Nome/Logo do Aplicativo
        self.lbl_logo = ctk.CTkLabel(self.sidebar_frame, text="MAIA PASS", font=("Segoe UI", 22, "bold"))
        self.lbl_logo.grid(row=0, column=0, padx=20, pady=(20, 5))
        
        self.lbl_sub = ctk.CTkLabel(self.sidebar_frame, text="Segurança & Criptografia", font=("Segoe UI", 11, "italic"), text_color="#A9A9B3")
        self.lbl_sub.grid(row=1, column=0, padx=20, pady=(0, 25))

        # Indicador de Status da Chave
        self.lbl_status_header = ctk.CTkLabel(self.sidebar_frame, text="STATUS DA CHAVE:", font=("Segoe UI", 10, "bold"), text_color="#A9A9B3")
        self.lbl_status_header.grid(row=2, column=0, padx=20, pady=(10, 0), sticky="w")
        
        self.lbl_status_chave = ctk.CTkLabel(self.sidebar_frame, text="Sem Chave ✖", font=("Segoe UI", 13, "bold"), text_color="#FF1744")
        self.lbl_status_chave.grid(row=3, column=0, padx=20, pady=(0, 25), sticky="w")

        # Ações de Chave
        self.btnGerarChave = ctk.CTkButton(
            self.sidebar_frame, 
            text="Gerar Chave", 
            font=("Segoe UI", 12, "bold"),
            fg_color="#7C4DFF", 
            hover_color="#651FFF", 
            command=self.GerarChave
        )
        self.btnGerarChave.grid(row=4, column=0, padx=20, pady=8, sticky="ew")

        self.btnCarregarChave = ctk.CTkButton(
            self.sidebar_frame, 
            text="Carregar Chave", 
            font=("Segoe UI", 12, "bold"), 
            command=self.AbrirChave
        )
        self.btnCarregarChave.grid(row=5, column=0, padx=20, pady=8, sticky="ew")

        self.btnSalvarChave = ctk.CTkButton(
            self.sidebar_frame, 
            text="Salvar Chave", 
            font=("Segoe UI", 12, "bold"), 
            command=self.Salvar_Chave
        )
        self.btnSalvarChave.grid(row=6, column=0, padx=20, pady=8, sticky="ew")

        # Seleção de Modo Visual (Claro / Escuro)
        self.lbl_modo = ctk.CTkLabel(self.sidebar_frame, text="MODO VISUAL:", font=("Segoe UI", 10, "bold"), text_color="#A9A9B3")
        self.lbl_modo.grid(row=8, column=0, padx=20, pady=(20, 0), sticky="w")
        
        self.opt_modo = ctk.CTkOptionMenu(
            self.sidebar_frame, 
            values=["Sistema", "Escuro", "Claro"], 
            font=("Segoe UI", 12),
            command=self.mudar_modo_aparencia
        )
        self.opt_modo.grid(row=9, column=0, padx=20, pady=(5, 20), sticky="ew")

        # ==========================================
        # PAINEL PRINCIPAL (Edição e Tradução)
        # ==========================================
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=25, pady=25)
        
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(2, weight=1)  # Campo de entrada cresce proporcionalmente
        self.main_frame.grid_rowconfigure(5, weight=1)  # Campo de saída cresce proporcionalmente

        # Título do Painel Principal
        self.lbl_titulo = ctk.CTkLabel(self.main_frame, text="Painel de Criptografia", font=("Segoe UI", 18, "bold"))
        self.lbl_titulo.grid(row=0, column=0, sticky="w", pady=(0, 15))

        # Seção Entrada (Cabeçalho com botão de carregar arquivo)
        self.entrada_header_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.entrada_header_frame.grid(row=1, column=0, sticky="ew", pady=(0, 5))
        self.entrada_header_frame.grid_columnconfigure(0, weight=1)
        self.entrada_header_frame.grid_columnconfigure(1, weight=0)

        self.lbl_entrada = ctk.CTkLabel(self.entrada_header_frame, text="Mensagem / Texto para processar:", font=("Segoe UI", 12, "bold"))
        self.lbl_entrada.grid(row=0, column=0, sticky="w")

        self.btnCarregarArquivo = ctk.CTkButton(
            self.entrada_header_frame, 
            text="Importar Arquivo 📂", 
            font=("Segoe UI", 11, "bold"), 
            height=26,
            width=140,
            command=self.CarregarMensagemArquivo
        )
        self.btnCarregarArquivo.grid(row=0, column=1, sticky="e")
        
        self.textMensagemMiddle = ctk.CTkTextbox(self.main_frame, font=("Segoe UI", 13), corner_radius=8, border_width=1)
        self.textMensagemMiddle.grid(row=2, column=0, sticky="nsew", pady=(0, 15))

        # Linha de botões de Ação
        self.acoes_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.acoes_frame.grid(row=3, column=0, sticky="ew", pady=(0, 20))
        self.acoes_frame.grid_columnconfigure((0, 1), weight=2)
        self.acoes_frame.grid_columnconfigure(2, weight=1)
        
        self.btnCriptografar = ctk.CTkButton(
            self.acoes_frame, 
            text="Criptografar 🔒", 
            font=("Segoe UI", 13, "bold"), 
            fg_color="#7C4DFF", 
            hover_color="#651FFF", 
            command=self.Criptografar
        )
        self.btnCriptografar.grid(row=0, column=0, padx=(0, 10), sticky="ew")

        self.btnDescriptografar = ctk.CTkButton(
            self.acoes_frame, 
            text="Descriptografar 🔓", 
            font=("Segoe UI", 13, "bold"), 
            fg_color="#2A2A3C", 
            hover_color="#38384F",
            command=self.Descriptografar
        )
        self.btnDescriptografar.grid(row=0, column=1, padx=(10, 10), sticky="ew")

        self.btnLimpar = ctk.CTkButton(
            self.acoes_frame, 
            text="Limpar", 
            font=("Segoe UI", 13), 
            fg_color="transparent", 
            border_width=1, 
            border_color="#5C5C6D", 
            hover_color=("#E4E4E4", "#2A2A3C"),
            text_color=("#2A2A3C", "#FFFFFF"),
            command=self.LimparCampos
        )
        self.btnLimpar.grid(row=0, column=2, padx=(10, 0), sticky="ew")

        # Seção Saída / Resultado
        self.lbl_saida = ctk.CTkLabel(self.main_frame, text="Resultado:", font=("Segoe UI", 12, "bold"))
        self.lbl_saida.grid(row=4, column=0, sticky="w", pady=(0, 5))
        
        self.textMensagemBottom = ctk.CTkTextbox(self.main_frame, font=("Segoe UI", 13), corner_radius=8, border_width=1)
        self.textMensagemBottom.grid(row=5, column=0, sticky="nsew", pady=(0, 15))

        # Linha de botões de Saída
        self.saida_acoes_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.saida_acoes_frame.grid(row=6, column=0, sticky="ew")
        self.saida_acoes_frame.grid_columnconfigure((0, 1), weight=1)

        self.btnCopiar = ctk.CTkButton(
            self.saida_acoes_frame, 
            text="Copiar Resultado 📋", 
            font=("Segoe UI", 13, "bold"), 
            fg_color="#00C853", 
            hover_color="#00E676",
            command=self.copiar_resultado
        )
        self.btnCopiar.grid(row=0, column=0, padx=(0, 10), sticky="ew")

        self.btnSalvar = ctk.CTkButton(
            self.saida_acoes_frame, 
            text="Salvar Mensagem 💾", 
            font=("Segoe UI", 13, "bold"), 
            command=self.Salvar_Mensagem
        )
        self.btnSalvar.grid(row=0, column=1, padx=(10, 0), sticky="ew")

    # ==========================================
    # LÓGICA E MÉTODOS DE SUPORTE
    # ==========================================
    
    def GerarChave(self):
        # Uso de secrets para geração de chave criptograficamente segura
        alphabet = string.ascii_letters + string.digits + "^!$%&/()=?{[]}+~#-_.:,;<>|\\"
        self.chave = ''.join(secrets.choice(alphabet) for _ in range(4096))
        
        # Atualiza a interface
        self.lbl_status_chave.configure(text="Chave Carregada ✔", text_color="#00E676")
        messagebox.showinfo(title="Chave Gerada", message="Uma chave criptograficamente segura foi gerada e carregada com sucesso!")
        
    def AbrirChave(self):  
        try: 
            os.makedirs("./chaves", exist_ok=True)
            filename = filedialog.askopenfilename(
                initialdir="./chaves",
                title="SELECIONE A CHAVE",
                filetypes=(("FORMATO DA CHAVE", "*.maiakey"), ("ALL FILES", "*.*"))
            ) 
            
            if filename:
                with open(filename, "r", encoding="utf-8") as arquivoDaChave:
                    self.chave = arquivoDaChave.read().strip()
                self.lbl_status_chave.configure(text="Chave Carregada ✔", text_color="#00E676")
                messagebox.showinfo(title="Aviso", message="CHAVE CARREGADA COM SUCESSO!")
        except Exception as e:
            messagebox.showerror(title="Erro", message=f"Não foi possível carregar a chave: {e}")

    def CarregarMensagemArquivo(self):
        try:
            os.makedirs("./mensagens", exist_ok=True)
            filename = filedialog.askopenfilename(
                initialdir="./mensagens",
                title="SELECIONE O ARQUIVO DE TEXTO",
                filetypes=(("ARQUIVO DE TEXTO", "*.txt"), ("ALL FILES", "*.*"))
            )
            
            if filename:
                try:
                    with open(filename, "r", encoding="utf-8") as arquivo:
                        conteudo = arquivo.read()
                except UnicodeDecodeError:
                    with open(filename, "r", encoding="cp1252") as arquivo:
                        conteudo = arquivo.read()
                
                self.textMensagemMiddle.delete("1.0", "end")
                self.textMensagemMiddle.insert("1.0", conteudo)
                messagebox.showinfo(title="Sucesso", message="Mensagem importada com sucesso!")
        except Exception as e:
            messagebox.showerror(title="Erro", message=f"Não foi possível carregar a mensagem: {e}")
    
    def Criptografar(self):
        if not self.chave:
            messagebox.showwarning(title="Aviso", message="Por favor, gere ou carregue uma chave para criptografar.")
            return
            
        mensagem = self.textMensagemMiddle.get("1.0", "end-1c")
        if not mensagem.strip():
            messagebox.showwarning(title="Aviso", message="Digite a mensagem que deseja criptografar.")
            return
            
        try:
            self.mensagemCriptografada = cryptocode.encrypt(mensagem, self.chave)
            self.textMensagemBottom.delete("1.0", "end")
            self.textMensagemBottom.insert("1.0", self.mensagemCriptografada)
            # Limpa o texto original por motivos de segurança
            self.textMensagemMiddle.delete("1.0", "end")
        except Exception as e:
            messagebox.showerror(title="Erro", message=f"Ocorreu um erro ao criptografar: {e}")
    
    def Descriptografar(self):
        if not self.chave:
            messagebox.showwarning(title="Aviso", message="Por favor, gere ou carregue uma chave para descriptografar.")
            return
            
        mensagemCriptografada = self.textMensagemMiddle.get("1.0", "end-1c").strip()
        if not mensagemCriptografada:
            messagebox.showwarning(title="Aviso", message="Insira um texto criptografado para descriptografar.")
            return
            
        try:
            self.mensagemDescriptografada = cryptocode.decrypt(mensagemCriptografada, self.chave)
            if self.mensagemDescriptografada is False:
                messagebox.showerror(title="Erro", message="Falha ao descriptografar. A chave está incorreta ou o texto foi corrompido.")
                return
                
            self.textMensagemBottom.delete("1.0", "end")
            self.textMensagemBottom.insert("1.0", self.mensagemDescriptografada)
        except Exception as e:
            messagebox.showerror(title="Erro", message=f"Ocorreu um erro ao descriptografar: {e}")
       
    def Salvar(self):
        # Mantendo para compatibilidade externa caso invocada
        self.Salvar_Chave()
        self.Salvar_Mensagem()
        
    def Salvar_Chave(self):
        if not self.chave:
            messagebox.showwarning(title="Aviso", message="Não há nenhuma chave ativa para salvar. Gere ou carregue uma primeiro.")
            return
            
        try:          
            os.makedirs("./chaves", exist_ok=True)
            filename = filedialog.asksaveasfilename(
                initialdir="./chaves", 
                defaultextension=".maiakey", 
                title="GRAVAR CHAVE", 
                filetypes=(("FORMATO DA CHAVE", "*.maiakey"), ("ALL FILES", "*.*"))
            )
            
            if filename:
                with open(filename, "w", encoding="utf-8") as arquivoDaChave:           
                    arquivoDaChave.write(self.chave)
                messagebox.showinfo(title="CHAVE GRAVADA", message="CHAVE GRAVADA COM SUCESSO!")
        except Exception as e:
            messagebox.showerror(title="Erro", message=f"Não foi possível salvar a chave: {e}")
                
    def Salvar_Mensagem(self):
        conteudo = self.textMensagemBottom.get("1.0", "end-1c").strip()
        if not conteudo:
            messagebox.showwarning(title="Aviso", message="Não há mensagem de resultado para salvar.")
            return
            
        try:
            os.makedirs("./mensagens", exist_ok=True)
            filename = filedialog.asksaveasfilename(
                initialdir="./mensagens", 
                defaultextension=".txt", 
                title="GRAVAR MENSAGEM", 
                filetypes=(("FORMATO DO TEXTO", "*.txt"), ("ALL FILES", "*.*"))
            )
            
            if filename:
                with open(filename, "w", encoding="utf-8") as arquivoDaMensagem:           
                    arquivoDaMensagem.write(conteudo)
                messagebox.showinfo(title="MENSAGEM GRAVADA", message="MENSAGEM GRAVADA COM SUCESSO!")
        except Exception as e:
            messagebox.showerror(title="Erro", message=f"Não foi possível salvar a mensagem: {e}")

    def LimparCampos(self):
        self.textMensagemMiddle.delete("1.0", "end")
        self.textMensagemBottom.delete("1.0", "end")

    def mudar_modo_aparencia(self, novo_modo):
        modo_map = {
            "Sistema": "system",
            "Escuro": "dark",
            "Claro": "light"
        }
        ctk.set_appearance_mode(modo_map.get(novo_modo, "system"))

    def copiar_resultado(self):
        resultado = self.textMensagemBottom.get("1.0", "end-1c").strip()
        if not resultado:
            messagebox.showwarning(title="Aviso", message="Não há resultado para ser copiado.")
            return
            
        self.clipboard_clear()
        self.clipboard_append(resultado)
        self.update()  # Mantém os dados no clipboard após fechar o aplicativo
        
        # Feedback rápido no botão
        self.btnCopiar.configure(text="Copiado! ✓", fg_color="#00E676", hover_color="#00C853")
        self.after(2000, self.restaurar_botao_copiar)

    def restaurar_botao_copiar(self):
        self.btnCopiar.configure(text="Copiar Resultado 📋", fg_color="#00C853", hover_color="#00E676")