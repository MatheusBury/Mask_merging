from PIL import Image
import os

def find_first_jpg(directory):
    """Encontra o primeiro arquivo JPG em um diretório."""
    for file in os.listdir(directory):
        if file.lower().endswith(".jpg"):
            return os.path.join(directory, file)
    raise FileNotFoundError("Nenhuma imagem JPG encontrada no diretório especificado.")

def merge_images(path_image_mask, path_image, save_path):
    # Carregar as imagens
    png_image = Image.open(path_image_mask)  # Caminho da imagem PNG
    jpg_image = Image.open(path_image)  # Caminho da imagem JPG

    # Redimensionar PNG para coincidir com o tamanho do JPG, se necessário
    png_image = png_image.resize(jpg_image.size)

    # Criar uma nova imagem com o fundo JPG
    merged_image = Image.new('RGBA', jpg_image.size)
    merged_image.paste(jpg_image.convert('RGBA'), (0, 0))
    merged_image.paste(png_image, (0, 0), png_image)

    # Converter para RGB antes de salvar como JPEG
    merged_image = merged_image.convert('RGB')

    # Preparar o nome do arquivo e o caminho de salvamento
    file_name = os.path.basename(path_image_mask)
    split, _ = os.path.splitext(file_name)
    new_name = f'{split}.jpg'
    full_save_path = os.path.join(save_path, new_name)

    # Criar diretório de salvamento se não existir
    os.makedirs(save_path, exist_ok=True)

    # Salvar a imagem mesclada
    merged_image.save(full_save_path)
    print(f'Imagem salva em: {full_save_path}')
    return full_save_path

def merge_images_in_subfolders(base_path_mask, path_image_dir, save_base_path):
    # Encontra a primeira imagem JPG no diretório especificado
    path_image = find_first_jpg(path_image_dir)

    for root, dirs, files in os.walk(base_path_mask):
        for file in files:
            if file.lower().endswith(".jpg"):
                # Caminho completo da máscara
                path_image_mask = os.path.join(root, file)
                
                # Estrutura de pasta para o salvamento
                relative_path = os.path.relpath(root, base_path_mask)
                save_path = os.path.join(save_base_path, relative_path)

                # Realizar o merge e salvar na estrutura de pastas correspondente
                merge_images(path_image_mask, path_image, save_path)

if __name__ == "__main__":
    # Diretórios principais
    base_path_mask = r"C:\Users\matheus.bury_vidyate\Downloads\mv26_3D\descompactada"
    path_image_dir = r"C:\Users\matheus.bury_vidyate\Downloads\IA EX"
    save_base_path = r'G:\Drives compartilhados\OPERATION PHOTOS\Modec\MV26\2024\IA EX escolha'

    merge_images_in_subfolders(base_path_mask, path_image_dir, save_base_path)
