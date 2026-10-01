from PIL import Image, ImageOps, UnidentifiedImageError
class ImageService:
    """A deterministic 64-D RGB foreground descriptor, not a neural model."""
    def encode(self,path):
        try:
            with Image.open(path) as source:
                rgb=ImageOps.exif_transpose(source).convert('RGB')
                rgb=ImageOps.contain(rgb,(64,64))
                canvas=Image.new('RGB',(64,64),'white')
                canvas.paste(rgb,((64-rgb.width)//2,(64-rgb.height)//2))
        except (OSError,UnidentifiedImageError) as exc:
            raise ValueError('Cannot read image: '+str(path)) from exc
        vector=[]
        for y in range(4):
            for x in range(4):
                pixels=[canvas.getpixel((xx,yy)) for yy in range(y*16,(y+1)*16) for xx in range(x*16,(x+1)*16)]
                fg=[p for p in pixels if min(p)<235]
                # Foreground occupancy retains black/white shape information.
                vector.extend([sum(1-p[c]/255 for p in pixels)/256 for c in range(3)])
                vector.append(len(fg)/256)
        if not any(vector): raise ValueError('Image has no detectable foreground')
        return vector
