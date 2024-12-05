from PIL import Image
import os

def merge_images(path_image_mask, path_image, save_path):
    print('to aqui')
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


def find_commom(imgs, mask, new_path):
    # Obter apenas os nomes dos arquivos (sem extensão) das imagens .jpg
    img_names = {os.path.splitext(os.path.basename(img))[0]: img for img in imgs if img.lower().endswith('.jpg')}
    print(img_names)

    for file in mask:
        # Extrair nome do arquivo sem extensão e a pasta
        file_name_no_ext = os.path.splitext(os.path.basename(file))[0]
        folder_name = os.path.basename(os.path.dirname(file))
        print(f'MASK {file_name_no_ext}')

        if file_name_no_ext in img_names:
            # Obter o caminho da imagem correspondente com .jpg
            path_file_img = img_names[file_name_no_ext]
            print(path_file_img)

            # Criar o novo caminho mantendo a estrutura
            new_path_file = os.path.join(new_path, folder_name)
            print(new_path_file)
            os.makedirs(new_path_file, exist_ok=True)

            # Chamar a função de merge com os arquivos nos caminhos corretos
            merge_images(file, path_file_img, new_path_file)
        else:
            # Caso o arquivo não seja encontrado
            pass


def percorrer(path_image):
    list_path_image = []
    for root, _, files in os.walk(path_image):
        for file in files:
            path_file = os.path.join(root,file)
            list_path_image.append(path_file)
            #print(path_file)
    return list_path_image


if __name__ == "__main__":

    base_path_mask = r"C:\Users\matheus.bury_vidyate\Downloads\mask teste de comparacao\dataset - 01072024"
    path_image_dir = r"C:\Users\matheus.bury_vidyate\Downloads\drive-download-20241205T122850Z-001\img"
    save_base_path = r'C:\Users\matheus.bury_vidyate\Downloads\img com ia'

    img_path = percorrer(path_image_dir)
    mask_path = percorrer(base_path_mask)

    find_commom(img_path,mask_path,save_base_path)

    # path_image_mask = r"C:\Users\matheus.bury_vidyate\Downloads\mask CS\bai\IMG_20180109_213557_00_169.png"
    # path_file_img = r"C:\Users\matheus.bury_vidyate\Downloads\original\IMG_20180109_213557_00_169.jpg"
    # new_path_file = r'C:\Users\matheus.bury_vidyate\Downloads\merger'



    # merge_images(path_image_mask,path_file_img,new_path_file)