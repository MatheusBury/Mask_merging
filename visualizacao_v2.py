import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk


class ImageZoomWindow(tk.Toplevel):
    def __init__(self, master, image_path, model_name, bg_color, update_zoom_callback, sync_position_callback):
        super().__init__(master)

        # Define a cor de fundo da janela
        self.configure(bg=bg_color)

        # Criação do Frame para borda personalizada
        self.frame = tk.Frame(self, bg='gray')
        self.frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Frame principal da janela com o conteúdo
        self.content_frame = tk.Frame(self.frame, bg=bg_color)
        self.content_frame.pack(fill="both", expand=True)

        # Adiciona o título personalizado
        self.title_label = tk.Label(self.content_frame, text=model_name, font=("Helvetica", 16, "bold"), bg=bg_color, anchor="w")
        self.title_label.pack(fill="x", padx=10, pady=5)

        # Configura o canvas
        self.canvas = tk.Canvas(self.content_frame, bg=bg_color, highlightthickness=0)
        self.scroll_y = tk.Scrollbar(self.content_frame, orient="vertical", command=self.canvas.yview)
        self.scroll_y.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill=tk.BOTH, expand=True)

        # Criação de um frame para o conteúdo da imagem
        self.frame_in_canvas = tk.Frame(self.canvas, bg=bg_color)
        self.canvas.create_window((0, 0), window=self.frame_in_canvas, anchor="nw")

        self.image = Image.open(image_path)
        self.zoom_factor = 1.0

        # Criação da imagem redimensionada
        self.photo_image = ImageTk.PhotoImage(self.image.resize((int(self.image.width * self.zoom_factor), int(self.image.height * self.zoom_factor))))
        self.image_id = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo_image)

        # Callbacks para zoom e sincronização
        self.update_zoom_callback = update_zoom_callback
        self.sync_position_callback = sync_position_callback

        # Configura eventos de rolagem e movimentação
        self.canvas.bind("<MouseWheel>", self.zoom)
        self.canvas.bind("<Configure>", self.on_resize)
        self.canvas.config(yscrollcommand=self.scroll_y.set)

        self.canvas.bind("<ButtonPress-1>", self.start_move)
        self.canvas.bind("<B1-Motion>", self.move_image)

        self.last_mouse_x = 0
        self.last_mouse_y = 0

    def zoom(self, event):
        if event.delta > 0:
            self.zoom_factor *= 1.1
        else:
            self.zoom_factor /= 1.1

        self.update_image()
        self.update_zoom_callback(self.zoom_factor)

    def update_image(self):
        resized_image = self.image.resize((int(self.image.width * self.zoom_factor), int(self.image.height * self.zoom_factor)))
        self.photo_image = ImageTk.PhotoImage(resized_image)
        self.canvas.itemconfig(self.image_id, image=self.photo_image)
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def start_move(self, event):
        self.last_mouse_x = event.x
        self.last_mouse_y = event.y

    def move_image(self, event):
        delta_x = event.x - self.last_mouse_x
        delta_y = event.y - self.last_mouse_y
        self.canvas.move(self.image_id, delta_x, delta_y)

        self.sync_position_callback(delta_x, delta_y)

        self.last_mouse_x = event.x
        self.last_mouse_y = event.y

    def on_resize(self, event):
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def update_position(self, delta_x, delta_y):
        self.canvas.move(self.image_id, delta_x, delta_y)


class ImageZoomApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Image Zoom Application")

        self.zoom_factor = 1.0

        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()

        window_width = screen_width // 3
        window_height = screen_height

        # Área para entrada da imagem
        self.input_frame = tk.Frame(self.master)
        self.input_frame.pack(pady=10)

        self.entry_label = tk.Label(self.input_frame, text="Digite o nome da imagem (sem a extensão .jpg):")
        self.entry_label.pack(side="left")

        self.image_entry = tk.Entry(self.input_frame)
        self.image_entry.pack(side="left")

        self.apply_button = tk.Button(self.input_frame, text="Aplicar", command=self.update_image_paths)
        self.apply_button.pack(side="left")

        self.models = [
            ('bai_1495', 'lightblue'),
            ('bai_1495_murphy', 'lightgreen'),
            ('exp_murphy_bai14952', 'lightpink'),
            ('exp_murphy_equinor_red', 'lightcyan'),
            ('exp_murphy_equinor_red2', 'lightgray'),
            ('exp_murphy_equinor22', 'lightyellow'),
            ('exp_mv30_baseline', 'darkgray'),
            ('exp_mv30_modec', 'darkgreen'),
            ('modec_mv30', 'darkmagenta'),
            ('unify', 'darkred'),
        ]

        self.selected_models = []

        self.checkbox_frame = tk.Frame(self.master)
        self.checkbox_frame.pack(pady=10)

        self.checkboxes = []
        for model in self.models:
            var = tk.BooleanVar()
            checkbox = tk.Checkbutton(self.checkbox_frame, text=model[0], variable=var, command=self.limit_selection)
            checkbox.pack(anchor="w")
            self.checkboxes.append((checkbox, var))

        self.windows = []  # Para armazenar as janelas abertas

    def limit_selection(self):
        selected_count = sum(var.get() for _, var in self.checkboxes)
        if selected_count > 3:
            for checkbox, var in self.checkboxes:
                if not var.get():
                    checkbox.config(state="disabled")
        else:
            for checkbox, var in self.checkboxes:
                checkbox.config(state="normal")

    def update_image_paths(self):
        input_image = self.image_entry.get()
        if not input_image:
            return  # Se não houver input, nada acontece

        self.selected_models = [
            model for (model, _), (_, var) in zip(self.models, self.checkboxes) if var.get()
        ]

        # Fechar as janelas antigas
        self.close_windows()

        # Caminhos das imagens para cada modelo
        self.paths = [
            fr"C:\Users\matheus.bury_vidyate\Downloads\img com ia\{model}\{input_image}.jpg"
            for model in self.selected_models
        ]

        # Cria as janelas de zoom
        self.create_zoom_windows()

        # Após adicionar as janelas, reseta o campo de entrada para nova imagem
        self.image_entry.delete(0, tk.END)

    def close_windows(self):
        # Fecha todas as janelas de zoom abertas
        for window in self.windows:
            window.destroy()
        self.windows.clear()

    def create_zoom_windows(self):
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()

        window_width = screen_width // 3
        window_height = screen_height

        for i, (path, model) in enumerate(zip(self.paths, self.selected_models)):
            bg_color = next(color for m, color in self.models if m == model)
            window = ImageZoomWindow(self.master, path, model, bg_color, self.update_zoom, self.sync_image_position)
            window.geometry(f"{window_width}x{window_height}+{i * window_width}+0")
            self.windows.append(window)

    def update_zoom(self, new_zoom_factor):
        self.zoom_factor = new_zoom_factor
        for window in self.windows:
            window.zoom_factor = self.zoom_factor
            window.update_image()

    def sync_image_position(self, delta_x, delta_y):
        for window in self.windows:
            if window is not self.windows[0]:
                window.update_position(delta_x, delta_y)


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageZoomApp(root)
    root.mainloop()
