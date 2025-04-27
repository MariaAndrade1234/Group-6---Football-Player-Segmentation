import os
import json
import shutil
from tqdm import tqdm

def remove_duplicates(duplicates_json, images_dir, backup_dir=None, dry_run=False):
    """Remove imagens duplicadas com base no arquivo JSON gerado"""
    
    # Carregar duplicatas
    with open(duplicates_json, 'r') as f:
        duplicates = json.load(f)
    
    # Criar backup se solicitado
    if backup_dir and not dry_run:
        os.makedirs(backup_dir, exist_ok=True)
    
    # Processar duplicatas
    removed_files = []
    kept_files = []
    
    for original, dup_list in tqdm(duplicates.items(), desc="Processando duplicatas"):
        for duplicate in dup_list:
            dup_path = os.path.join(images_dir, duplicate)
            
            # Verificar se arquivo existe
            if not os.path.exists(dup_path):
                continue
                
            if dry_run:
                print(f"[DRY RUN] Removeria: {duplicate} (duplicata de {original})")
                removed_files.append(duplicate)
            else:
                # Mover para backup ou deletar
                if backup_dir:
                    shutil.move(dup_path, os.path.join(backup_dir, duplicate))
                else:
                    os.remove(dup_path)
                removed_files.append(duplicate)
        
        kept_files.append(original)
    
    # Verificar arquivos de anotação correspondentes
    annotations_dir = os.path.join(os.path.dirname(images_dir), "labels")
    if os.path.exists(annotations_dir):
        for dup_file in tqdm(removed_files, desc="Processando anotações"):
            base_name = os.path.splitext(dup_file)[0]
            anno_file = os.path.join(annotations_dir, base_name + ".txt")
            
            if os.path.exists(anno_file):
                if dry_run:
                    print(f"[DRY RUN] Removeria anotação: {anno_file}")
                else:
                    if backup_dir:
                        shutil.move(anno_file, os.path.join(backup_dir, base_name + ".txt"))
                    else:
                        os.remove(anno_file)
    
    print("\nResumo:")
    print(f"Total de arquivos mantidos: {len(kept_files)}")
    print(f"Total de arquivos removidos: {len(removed_files)}")
    
    # Salvar log
    if not dry_run:
        log_file = os.path.join(os.path.dirname(duplicates_json), "duplicates_removal.log")
        with open(log_file, 'w') as f:
            f.write("Arquivos mantidos:\n")
            f.write("\n".join(kept_files) + "\n\n")
            f.write("Arquivos removidos:\n")
            f.write("\n".join(removed_files) + "\n")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--duplicates_json', type=str, required=True, help='Arquivo JSON com duplicatas')
    parser.add_argument('--images_dir', type=str, required=True, help='Diretório com imagens')
    parser.add_argument('--backup_dir', type=str, help='Diretório para backup (opcional)')
    parser.add_argument('--dry_run', action='store_true', help='Simular sem remover')
    args = parser.parse_args()
    
    remove_duplicates(args.duplicates_json, args.images_dir, args.backup_dir, args.dry_run)