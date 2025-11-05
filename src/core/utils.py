import pygame
import os
from pathlib import Path

def get_project_root():
    """Obtiene la ruta raíz del proyecto de forma absoluta y segura"""
    current_file = Path(__file__).resolve()
    project_root = current_file.parent.parent.parent
    return project_root

def load_image(relative_path, scale=None, smoothing=2):
    """
    Carga una imagen de cualquier formato soportado por pygame
    No expone rutas absolutas del sistema en los mensajes
    
    Args:
        relative_path: Ruta relativa de la imagen
        scale: Tupla (width, height) para escalar
        smoothing: Nivel de suavizado (0=ninguno, 1=normal, 2=máximo)
    """
    project_root = get_project_root()
    full_path = project_root / relative_path
    
    supported_formats = ['.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tga', '.tif', '.tiff', '.webp']
    
    try:
        if full_path.exists() and full_path.is_file():
            print(f"  ✅ Cargando: {relative_path}")
            image = pygame.image.load(str(full_path)).convert_alpha()
            
            if scale:
                if smoothing == 0:
                    # Sin suavizado (pixelado)
                    image = pygame.transform.scale(image, scale)
                elif smoothing == 1:
                    # Suavizado normal
                    image = pygame.transform.smoothscale(image, scale)
                else:  # smoothing == 2
                    # Suavizado máximo (escala intermedia)
                    factor = 2
                    temp_scale = (scale[0] * factor, scale[1] * factor)
                    image = pygame.transform.smoothscale(image, temp_scale)
                    image = pygame.transform.smoothscale(image, scale)
            
            return image
        
        file_path = Path(full_path)
        base_name = file_path.stem
        parent_dir = file_path.parent
        
        if parent_dir.exists():
            for ext in supported_formats:
                test_path = parent_dir / f"{base_name}{ext}"
                if test_path.exists():
                    rel_path = test_path.relative_to(project_root)
                    print(f"  ✅ Cargando: {rel_path}")
                    image = pygame.image.load(str(test_path)).convert_alpha()
                    
                    if scale:
                        if smoothing == 0:
                            image = pygame.transform.scale(image, scale)
                        elif smoothing == 1:
                            image = pygame.transform.smoothscale(image, scale)
                        else:
                            factor = 2
                            temp_scale = (scale[0] * factor, scale[1] * factor)
                            image = pygame.transform.smoothscale(image, temp_scale)
                            image = pygame.transform.smoothscale(image, scale)
                    
                    return image
        
        print(f"  ❌ No encontrado: {relative_path}")
        surf = pygame.Surface(scale if scale else (50, 50))
        surf.fill((255, 0, 255))
        return surf
        
    except Exception as e:
        print(f"  ❌ Error: {type(e).__name__}")
        surf = pygame.Surface(scale if scale else (50, 50))
        surf.fill((255, 0, 255))
        return surf

def load_animation_frames(folder_path, num_frames, scale=None, start_index=0, smoothing=2):
    """
    Carga múltiples frames con detección automática de formato y nombres
    
    Args:
        smoothing: Nivel de suavizado (0, 1 o 2)
    """
    frames = []
    project_root = get_project_root()
    folder_full_path = project_root / folder_path
    
    print(f"\n{'='*60}")
    print(f"Cargando animación desde: {folder_path}")
    print(f"{'='*60}")
    
    if not folder_full_path.exists():
        print(f"  ❌ Carpeta no encontrada")
        for i in range(num_frames):
            surf = pygame.Surface(scale if scale else (50, 50))
            surf.fill((255, 215, 0) if i % 2 == 0 else (255, 0, 0))
            frames.append(surf)
        return frames
    
    files_in_folder = list(folder_full_path.glob('*'))
    
    patterns = [
        lambda i: f"runnning ({i})",
        lambda i: f"running_dog ({i})",
        lambda i: f"frame_{i}",
        lambda i: f"frame{i}",
        lambda i: f"{i}",
    ]
    
    for i in range(start_index, start_index + num_frames):
        frame_loaded = False
        
        for pattern_func in patterns:
            base_name = pattern_func(i)
            
            for file in files_in_folder:
                if file.stem == base_name or file.name.startswith(base_name):
                    relative = file.relative_to(project_root)
                    frame = load_image(str(relative), scale, smoothing)
                    frames.append(frame)
                    frame_loaded = True
                    break
            
            if frame_loaded:
                break
        
        if not frame_loaded:
            print(f"  ⚠️ Frame {i} no encontrado")
            surf = pygame.Surface(scale if scale else (50, 50))
            surf.fill((255, 100, 100))
            frames.append(surf)
    
    print(f"✅ Frames cargados: {len(frames)}\n")
    return frames

def load_sound(relative_path):
    """Carga un archivo de sonido"""
    project_root = get_project_root()
    full_path = project_root / relative_path
    
    try:
        if full_path.exists():
            return pygame.mixer.Sound(str(full_path))
        else:
            print(f"  ⚠️ Sonido no encontrado: {relative_path}")
            return None
    except Exception as e:
        print(f"  ❌ Error al cargar sonido: {type(e).__name__}")
        return None
