"""
Image Processing Service for Cool PWA Icon Generator
Handles downscaling, sharpening, and format conversion
"""
from PIL import Image, ImageFilter, ImageEnhance
import io
import base64
from typing import Tuple, Dict
import config


class ImageProcessor:
    """Handles all image processing operations"""
    
    @staticmethod
    def downscale_image(
        image: Image.Image,
        target_size: int,
        apply_sharpen: bool = True,
        source_size: int = 512
    ) -> Image.Image:
        """
        Downscale image using high-quality Lanczos resampling with size-adaptive sharpening
        
        Args:
            image: Source PIL Image
            target_size: Target width/height (assumes square)
            apply_sharpen: Whether to apply sharpening filter
            source_size: Source image size (for adaptive sharpening)
            
        Returns:
            Downscaled PIL Image
        """
        # Use LANCZOS (highest quality) for downscaling
        downscaled = image.resize(
            (target_size, target_size),
            Image.Resampling.LANCZOS
        )
        
        # Apply size-adaptive sharpening
        if apply_sharpen and config.SHARPEN_SMALL_ICONS:
            # Calculate downscale ratio for adaptive sharpening
            ratio = source_size / target_size
            downscaled = ImageProcessor._apply_adaptive_sharpening(downscaled, ratio)
            
        return downscaled
    
    @staticmethod
    def _apply_adaptive_sharpening(image: Image.Image, downscale_ratio: float) -> Image.Image:
        """
        Apply size-adaptive unsharp mask to enhance edges and details
        Stronger sharpening for larger downscale ratios
        
        Args:
            image: PIL Image to sharpen
            downscale_ratio: Ratio of source/target size (e.g., 512/192 = 2.67)
            
        Returns:
            Sharpened PIL Image
        """
        # Adaptive sharpening based on downscale ratio
        # Larger ratios (more downscaling) need stronger sharpening
        if downscale_ratio >= 32:  # 512→16 = 32x
            # Extreme sharpening for favicon
            radius = 2.0
            percent = 200
            threshold = 2
        elif downscale_ratio >= 3:  # 512→164 = 3.1x
            # Strong sharpening for medium downscaling
            radius = 1.5
            percent = 160
            threshold = 3
        elif downscale_ratio >= 2:  # 512→192 = 2.67x
            # Moderate sharpening for mild downscaling
            radius = 1.0
            percent = 130
            threshold = 3
        else:
            # Light sharpening
            radius = 0.8
            percent = 120
            threshold = 3
        
        # Apply unsharp mask filter
        sharpened = image.filter(
            ImageFilter.UnsharpMask(
                radius=radius,
                percent=percent,
                threshold=threshold
            )
        )
        return sharpened
    
    @staticmethod
    def enhance_contrast(image: Image.Image, factor: float = 1.2) -> Image.Image:
        """
        Enhance contrast for better visibility at small sizes
        
        Args:
            image: PIL Image
            factor: Enhancement factor (1.0 = no change, >1.0 = more contrast)
            
        Returns:
            Enhanced PIL Image
        """
        enhancer = ImageEnhance.Contrast(image)
        return enhancer.enhance(factor)
    
    @staticmethod
    def image_to_base64(
        image: Image.Image,
        format: str = "PNG"
    ) -> str:
        """
        Convert PIL Image to base64 string
        
        Args:
            image: PIL Image
            format: Output format (PNG or JPEG)
            
        Returns:
            Base64 encoded string
        """
        buffer = io.BytesIO()
        
        # Convert RGBA to RGB if saving as JPEG
        if format.upper() == "JPEG" and image.mode == "RGBA":
            # Create white background
            rgb_image = Image.new("RGB", image.size, (255, 255, 255))
            rgb_image.paste(image, mask=image.split()[3])  # Use alpha as mask
            rgb_image.save(buffer, format=format, quality=95)
        else:
            image.save(buffer, format=format)
        
        buffer.seek(0)
        img_bytes = buffer.getvalue()
        base64_str = base64.b64encode(img_bytes).decode()
        
        return f"data:image/{format.lower()};base64,{base64_str}"
    
    @staticmethod
    def save_image(
        image: Image.Image,
        file_path: str,
        format: str = "PNG"
    ) -> None:
        """
        Save PIL Image to file
        
        Args:
            image: PIL Image
            file_path: Output file path or BytesIO
            format: Output format (PNG, JPEG, or ICO)
        """
        # Convert RGBA to RGB if saving as JPEG
        if format.upper() == "JPEG" and image.mode == "RGBA":
            rgb_image = Image.new("RGB", image.size, (255, 255, 255))
            rgb_image.paste(image, mask=image.split()[3])
            rgb_image.save(file_path, format=format, quality=95)
        elif format.upper() == "ICO":
            # ICO format - Pillow supports it natively
            image.save(file_path, format="ICO", sizes=[(image.width, image.height)])
        else:
            image.save(file_path, format=format)
    
    @staticmethod
    def create_favicon(image: Image.Image, source_size: int = 512) -> Image.Image:
        """
        Create optimized favicon from source image
        Direct downscale with aggressive sharpening - no crop needed with enhanced prompts
        
        Args:
            image: Source PIL Image (512x512 master)
            source_size: Source image size for adaptive sharpening
            
        Returns:
            16x16 favicon with enhanced visibility
        """
        # Direct downscale to 16x16 with aggressive adaptive sharpening
        favicon = ImageProcessor.downscale_image(
            image,
            16,
            apply_sharpen=True,
            source_size=source_size
        )
        
        # Extra contrast boost for tiny size visibility
        favicon = ImageProcessor.enhance_contrast(favicon, factor=1.5)
        
        return favicon
    
    @staticmethod
    def process_all_sizes(
        img_512: Image.Image
    ) -> Dict[str, Image.Image]:
        """
        Process all four PWA icon sizes from single 512x512 master image
        Ensures perfect visual consistency across all icon sizes
        
        Args:
            img_512: 512x512 AI-generated master image
            
        Returns:
            Dictionary with all four sizes (512, 192, 164, 16)
        """
        return {
            "512": img_512,
            "192": ImageProcessor.downscale_image(img_512, 192, apply_sharpen=True, source_size=512),
            "164": ImageProcessor.downscale_image(img_512, 164, apply_sharpen=True, source_size=512),
            "16": ImageProcessor.create_favicon(img_512, source_size=512)
        }
    
    @staticmethod
    def images_to_base64_dict(
        images: Dict[str, Image.Image],
        format: str = "PNG"
    ) -> Dict[str, str]:
        """
        Convert dictionary of images to base64 strings
        
        Args:
            images: Dict of size -> PIL Image
            format: Output format
            
        Returns:
            Dict of size -> base64 string
        """
        return {
            size: ImageProcessor.image_to_base64(img, format)
            for size, img in images.items()
        }