from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import cryptocode
import string
import random

class Criptografia():
    def __init__(self) -> None:
        self.root = Tk()
        self.Encriptografar()
        self.root.mainloop()
        pass
    

    def Encriptografar(self):
        self.root.title("MAIA PASS - Criptografe e decriptografe mensagens ")
        self.root.geometry("480x620")
        self.favicon = PhotoImage(file="icones/favicon512.png")
        self.root.iconphoto(True,self.favicon)
        barraDeMenu = Menu(self.root)
        menuArquivo=Menu(barraDeMenu, tearoff=0)
        barraDeMenu.add_cascade(label="Arquivo",menu=menuArquivo)
        menuArquivo.add_command(label="Abrir chave", command=self.AbrirChave)
        self.root.config(menu=barraDeMenu)
        self.painelMaster = Frame(self.root,bg="#333333")
        self.painelMaster.pack(side=TOP,fill=BOTH, expand=1)
        # PAINEL TOP
        self.painelTop = Frame(self.painelMaster, bg="#454545",padx=5,pady=5)
        self.painelTop.place(relx=0,rely=0,relwidth=1, relheight=0.1)
        TamanhoFonteTop = 18
        self.btnGerarChave4096 = Button(self.painelTop, text="Chave", font=("Comic Sans MS",TamanhoFonteTop),bg="#d1d1d1", command=self.GerarChave)
        self.btnGerarChave4096.pack(side=LEFT,expand=1, fill=BOTH,)
        self.btnCriptografar = Button(self.painelTop, text="Criptografar", font=("Comic Sans MS",TamanhoFonteTop),bg="#d1d1d1", command=self.Criptografar)
        self.btnCriptografar.pack(side=LEFT,expand=1, fill=BOTH)
        self.btnDescriptografar = Button(self.painelTop, text="Descriptografar", font=("Comic Sans MS",TamanhoFonteTop),bg="#d1d1d1", command=self.Descriptografar)
        self.btnDescriptografar.pack(side=LEFT,expand=1, fill=BOTH)
        # PAINEL MIDDLE
        self.painelMiddle = Frame(self.painelMaster, bg="#333333",padx=5,pady=0)
        self.painelMiddle.place(relx=0,rely=0.15,relwidth=1, relheight=0.3)
        self.labelMsnMiddle = Label(self.painelMiddle, text="Mensagem", font=("Comic Sans MS",14),fg="#E4E4E4", bg="#333333")
        self.labelMsnMiddle.pack(side=TOP,expand=1,fill=BOTH)
        self.textMensagemMiddle = Text(self.painelMiddle,font=("Comic Sans MS",18))
        self.textMensagemMiddle.pack(side=TOP,expand=1, fill=BOTH)
        
        # PAINEL BOTTOM
        self.painelBottom = Frame(self.painelMaster, bg="#333333",padx=5,pady=5)
        self.painelBottom.place(relx=0,rely=0.5,relwidth=1, relheight=0.9)
        self.labelMsnBottom = Label(self.painelBottom, text="Visualize aqui sua criptografia", font=("Comic Sans MS",14),fg="#E4E4E4", bg="#333333")
        self.labelMsnBottom.place(relx=0, rely=0,relwidth=1,relheight=0.05)
        self.textMensagemBottom = Text(self.painelBottom,font=("Comic Sans MS",18))
        self.textMensagemBottom.place(relx=0,rely=0.06, relwidth=1, relheight=0.32)
        self.btnSalvar = Button(self.painelBottom,text="Salvar",font=("Comic Sans MS",24), bg="#d1d1d1", command=self.Salvar)
        self.btnSalvar.place(relx=0, rely=0.4, relwidth=1, relheight=0.15)
       
   
    # Criar botão Cript e Decript
    def GerarChave(self):
        print("Gerar chave")
        self.chave = ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits + '^!\$%&/()=?{[]}+~#-_.:,;<>|\\') for _ in range(0, 4096))
        print(self.chave)
        pass
    
    def AbrirChave(self):  
        try: 
            filename = filedialog.askopenfilename(initialdir = "./chaves",title = "SELECIONE A CHAVE",filetypes = (
                ("FORMATO DA CHAVE","*.maiakey"),
                ("ALL FILES","*.maiakey"))) 
            
            if filename.endswith(".maiakey"):
                self.caminhoDoArquivoDaChave = filename
                print(self.caminhoDoArquivoDaChave)
                if self.caminhoDoArquivoDaChave != "":
                    with open(self.caminhoDoArquivoDaChave, "r") as arquivoDaChave:
                        self.chave = arquivoDaChave.read()
                        print("CHAVE CARREGADA: "+self.chave)
                        arquivoDaChave.close()
                        messagebox.showinfo(title="Aviso", message="CHAVE CARREGADA")
            else:
                print(self.caminhoDoArquivoDaChave)
            
        except:
            messagebox.showinfo(title="Aviso", message="NENHUMA CHAVE maiakey ABERTA")
    
    def Criptografar(self):
        try:
            if self.chave != "":
                mensagem = self.textMensagemMiddle.get("1.0","end")        
                self.mensagemCriptografada = cryptocode.encrypt(mensagem, self.chave)
                print("Sua mensagem criptografada: " + self.mensagemCriptografada)
                self.textMensagemBottom.insert("1.0",self.mensagemCriptografada)
                self.textMensagemMiddle.delete("1.0","end")
        except:
              messagebox.showinfo(title="Aviso", message="Precisa da chave gerada para criptografar")
    
    def Descriptografar(self):
        try:
            if self.chave != "":
                mensagemCriptografada = self.textMensagemMiddle.get("1.0","end")        
                self.mensagemDescriptografada = cryptocode.decrypt(mensagemCriptografada,  self.chave)
                print("Sua mensagem Descriptografada: " + self.mensagemDescriptografada)
                self.textMensagemBottom.insert("1.0",self.mensagemDescriptografada)
        except:
              messagebox.showinfo(title="AVISO", message="PRECISA DA CHAVE GERADA PARA DESCRIPTOGRAFAR")
       
    
    def Salvar(self):
        self.Salvar_Chave()
        self.Salvar_Mensagem()
        
    def Salvar_Chave(self):
        try:          
            filename = filedialog.asksaveasfilename(initialdir = "./chaves", defaultextension=".maiakey", title = "GRAVAR CHAVE", filetypes = (
                ("FORMATO DA CHAVE",".maiakey"),
                ("ALL FILES",".maiakey")))
            
            if filename.endswith(".maiakey"):
                self.caminhoDoArquivoChave = filename
                print(self.caminhoDoArquivoChave)
                if self.caminhoDoArquivoChave != "":
                    with open(self.caminhoDoArquivoChave, "w") as arquivoDaChave:           
                        arquivoDaChave.write(self.chave)
                        arquivoDaChave.close()                  
                        self.textMensagemMiddle.delete("1.0","end")
                        messagebox.showinfo(title="CHAVE GRAVADA", message="CHAVE GRAVADA COM SUCESSO")
            else:
                print(self.caminhoDoArquivoChave)
        except:
            messagebox.showinfo(title="Aviso", message="DIGITE A EXTENSÃO CERTA")
                
    
    def Salvar_Mensagem(self):
        try:
            filename = filedialog.asksaveasfilename(initialdir = "./mensagens", defaultextension=".txt", title = "GRAVAR MENSAGEM", filetypes = (
                ("FORMATO DO TEXTO",".txt"),
                ("ALL FILES",".txt")))
            
            if filename.endswith(".txt"):
                self.caminhoDoArquivoMensagem = filename
                print(self.caminhoDoArquivoMensagem)
                if self.caminhoDoArquivoMensagem != "":
                    with open(self.caminhoDoArquivoMensagem, "w") as arquivoDaMensagem:           
                        arquivoDaMensagem.write(self.textMensagemBottom.get("1.0","end"))
                        arquivoDaMensagem.close()                  
                        self.textMensagemMiddle.delete("1.0","end")
                        messagebox.showinfo(title="MENSAGEM GRAVADA", message="MENSAGEM GRAVADA COM SUCESSO")
            else:
                print(self.caminhoDoArquivoMensagem)
        except:
            messagebox.showinfo(title="Aviso", message="DIGITE A EXTENSÃO CERTA")