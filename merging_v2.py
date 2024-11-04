from PIL import Image
import os

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


def find_commom(imgs,mask,new_path):

    img_names = [os.path.basename(img).lower() for img in imgs]

   
    for file in mask:
        file_name = os.path.basename(file).lower()
        folder_name = os.path.basename(os.path.dirname(file))

        if file_name in img_names:

            path_file_img = os.path.join(r"C:\Users\matheus.bury_vidyate\Downloads\IA EX",file_name)
            
            new_path_file = os.path.join(new_path,folder_name)
            os.makedirs(new_path_file,exist_ok=True)
            merge_images(file,path_file_img,new_path_file)


def percorrer(path_image):
    list_path_image = []
    for root, _, files in os.walk(path_image):
        for file in files:
            path_file = os.path.join(root,file)
            list_path_image.append(path_file)
            #print(path_file)
    return list_path_image


if __name__ == "__main__":

    base_path_mask = r"C:\Users\matheus.bury_vidyate\Downloads\mv26_3D\descompactada"
    path_image_dir = r"C:\Users\matheus.bury_vidyate\Downloads\IA EX"
    save_base_path = r'G:\Drives compartilhados\OPERATION PHOTOS\Modec\MV26\2024\IA EX escolha'

    img_path = percorrer(path_image_dir)
    mask_path = percorrer(base_path_mask)

    find_commom(img_path,mask_path,save_base_path)