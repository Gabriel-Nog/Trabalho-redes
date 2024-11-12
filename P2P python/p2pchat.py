import socket
import threading
import tkinter as tk
from tkinter.scrolledtext import ScrolledText

# Cifra de César para criptografar/descriptografar as mensagens
def caesar_cipher(text, shift):
    result = []
    for char in text:
        result.append(chr((ord(char) + shift) % 256))  # Criptografa com mod 256 para garantir que seja um byte válido
    return ''.join(result)

def caesar_decipher(text, shift):
    return caesar_cipher(text, -shift)

class P2PClient:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Chat P2P")
        
        self.chat_area = ScrolledText(self.window)
        self.chat_area.pack(padx=10, pady=10)
        self.chat_area.config(state='disabled')
        
        self.username_entry = tk.Entry(self.window, width=50)
        self.username_entry.insert(0, 'Nome de Usuário')
        self.username_entry.pack(padx=10, pady=10)
        
        self.peer_ip_entry = tk.Entry(self.window, width=50)
        self.peer_ip_entry.insert(0, 'IP do Peer')
        self.peer_ip_entry.pack(padx=10, pady=10)
        
        self.connect_button = tk.Button(self.window, text="Conectar", command=self.connect_to_peer)
        self.connect_button.pack(padx=10, pady=10)
        
        self.message_entry = tk.Entry(self.window, width=50)
        self.message_entry.pack(padx=10, pady=10)
        
        self.send_button = tk.Button(self.window, text="Enviar", command=self.send_message)
        self.send_button.pack(padx=10, pady=10)
        
        self.socket = None
        self.peer_socket = None
        self.username = ""
        
        threading.Thread(target=self.listen_for_connections).start()
        
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)
        self.window.mainloop()

    def display_message(self, message):
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, message + "\n")
        self.chat_area.config(state='disabled')
    
    def send_message(self):
        message = self.message_entry.get()
        self.display_message(f"Você: {message}")
        self.message_entry.delete(0, tk.END)
        encrypted_message = caesar_cipher(f"{self.username}: {message}", 3)
        if self.peer_socket:
            self.peer_socket.send(encrypted_message.encode('utf-8'))
        
    
        
    def listen_for_connections(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('0.0.0.0', 9999))
        self.socket.listen(1)
        while True:
            conn, addr = self.socket.accept()
            self.peer_socket = conn
            self.display_message(f"Conectado a {addr}")
            threading.Thread(target=self.receive_messages).start()
    
    def receive_messages(self):
        while True:
            try:
                message = self.peer_socket.recv(1024).decode('utf-8')
                decrypted_message = caesar_decipher(message, 3)
                self.display_message(decrypted_message)
            except ConnectionResetError:
                self.display_message("Peer desconectado.")
                break
    
    def connect_to_peer(self):
        self.username = self.username_entry.get()
        peer_ip = self.peer_ip_entry.get()
        self.peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.peer_socket.connect((peer_ip, 9999))
        self.display_message(f"Conectado ao peer {peer_ip}")
        threading.Thread(target=self.receive_messages).start()

        self.logout_button = tk.Button(self.window, text="Desconectar", command=self.logout)
        self.logout_button.pack(padx=10, pady=10)

    def on_close(self):
        if self.peer_socket:
            self.peer_socket.close()
        if self.socket:
            self.socket.close()
        self.window.destroy()
    
    def logout(self):
        if self.peer_socket:
            self.peer_socket.close()
        if self.socket:
            self.socket.close()
        
        self.display_message("Desconectado")
        self.peer_ip_entry.delete(0, tk.END)
        self.logout_button.destroy()
        
if __name__ == "__main__":
    P2PClient()