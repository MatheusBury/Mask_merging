import os
import tkinter as tk
from PIL import Image, ImageTk

class ImageZoomWindow(tk.Toplevel):
    def __init__(self, master, image_path, update_zoom_callback, sync_position_callback):
        super().__init__(master)

        # Define o título com o nome da pasta da imagem
        folder_name = os.path.basename(os.path.dirname(image_path))
        self.title(folder_name)

        self.canvas = tk.Canvas(self, bg='white')
        self.scroll_y = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scroll_y.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill=tk.BOTH, expand=True)

        # Cria uma estrutura de frame dentro do canvas para permitir o movimento
        self.frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")

        self.image = Image.open(image_path)
        self.zoom_factor = 1.0

        # Armazena a referência da imagem redimensionada
        self.photo_image = ImageTk.PhotoImage(self.image.resize((int(self.image.width * self.zoom_factor), int(self.image.height * self.zoom_factor))))
        self.image_id = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo_image)  # Create image on the canvas

        # Callback para atualizar o zoom e sincronizar a posição
        self.update_zoom_callback = update_zoom_callback
        self.sync_position_callback = sync_position_callback

        # Bind mouse wheel for zooming
        self.canvas.bind("<MouseWheel>", self.zoom)
        self.canvas.bind("<Configure>", self.on_resize)

        # Configure scrollbar
        self.canvas.config(yscrollcommand=self.scroll_y.set)

        # Bind mouse drag event to move the image
        self.canvas.bind("<ButtonPress-1>", self.start_move)
        self.canvas.bind("<B1-Motion>", self.move_image)

        # Store last mouse position
        self.last_mouse_x = 0
        self.last_mouse_y = 0

    def zoom(self, event):
        if event.delta > 0:
            self.zoom_factor *= 1.1  # Zoom in
        else:
            self.zoom_factor /= 1.1  # Zoom out

        # Atualiza a imagem com o novo fator de zoom
        self.update_image()
        self.update_zoom_callback(self.zoom_factor)  # Notifica a classe principal para atualizar as outras janelas

    def update_image(self):
        resized_image = self.image.resize((int(self.image.width * self.zoom_factor), int(self.image.height * self.zoom_factor)))
        self.photo_image = ImageTk.PhotoImage(resized_image)
        self.canvas.itemconfig(self.image_id, image=self.photo_image)  # Update image on the canvas
        self.canvas.config(scrollregion=self.canvas.bbox("all"))  # Atualiza a região de rolagem do canvas

    def start_move(self, event):
        self.last_mouse_x = event.x
        self.last_mouse_y = event.y

    def move_image(self, event):
        delta_x = event.x - self.last_mouse_x
        delta_y = event.y - self.last_mouse_y
        self.canvas.move(self.image_id, delta_x, delta_y)  # Move a imagem na direção do movimento do mouse
        
        # Sincroniza a posição da imagem com as outras janelas
        self.sync_position_callback(delta_x, delta_y)
        
        self.last_mouse_x = event.x
        self.last_mouse_y = event.y

    def on_resize(self, event):
        self.canvas.config(scrollregion=self.canvas.bbox("all"))  # Atualiza a região de rolagem ao redimensionar

    def update_position(self, delta_x, delta_y):
        self.canvas.move(self.image_id, delta_x, delta_y)  # Move a imagem na direção do movimento do mouse

class ImageZoomApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Image Zoom Application")

        self.zoom_factor = 1.0  # Fator de zoom compartilhado

        # Obtém as dimensões da tela
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()

        # Define a largura e a altura de cada janela (ajuste conforme necessário)
        window_width = screen_width // 3
        window_height = screen_height

        # Caminhos das imagens
        input_image = input("Digite o nome da imagem (sem a extensão .jpg): ")

        # Usando f-strings para formatar os caminhos
        paths = [
            fr"G:\Drives compartilhados\OPERATION PHOTOS\Modec\MV26\2024\IA EX escolha\bai_1495_murphy\{input_image}.jpg",
            fr"G:\Drives compartilhados\OPERATION PHOTOS\Modec\MV26\2024\IA EX escolha\experiment_model_segm_mv30_31_33_modec\{input_image}.jpg",
            fr"G:\Drives compartilhados\OPERATION PHOTOS\Modec\MV26\2024\IA EX escolha\experiment_model_segm_mv31_modec\{input_image}.jpg"
        ]

        # Cria uma janela para cada imagem
        self.windows = []
        for i, path in enumerate(paths):
            window = ImageZoomWindow(self.master, path, self.update_zoom, self.sync_image_position)
            window.geometry(f"{window_width}x{window_height}+{i * window_width}+0")  # Define tamanho e posição
            self.windows.append(window)

    def update_zoom(self, new_zoom_factor):
        self.zoom_factor = new_zoom_factor
        for window in self.windows:
            window.zoom_factor = self.zoom_factor
            window.update_image()  # Atualiza a imagem na janela com o novo fator de zoom

    def sync_image_position(self, delta_x, delta_y):
        for window in self.windows:
            if window is not self.windows[0]:  # Evita chamadas recursivas
                window.update_position(delta_x, delta_y)

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageZoomApp(root)
    root.mainloop()
