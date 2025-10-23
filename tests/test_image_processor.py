"""
Unit tests for Image Processor
Tests downscaling, sharpening, and format conversion
"""
import pytest
from PIL import Image
import io
from image_processor import ImageProcessor


class TestImageProcessor:
    """Test suite for ImageProcessor class"""
    
    @pytest.fixture
    def sample_image(self):
        """Create a sample test image"""
        # Create a simple 512x512 test image
        img = Image.new('RGB', (512, 512), color='blue')
        return img
    
    def test_downscale_image(self, sample_image):
        """Test image downscaling"""
        target_size = 192
        downscaled = ImageProcessor.downscale_image(sample_image, target_size)
        
        assert downscaled.size == (target_size, target_size)
        assert downscaled.mode == sample_image.mode
    
    def test_downscale_with_sharpening(self, sample_image):
        """Test downscaling with sharpening filter"""
        target_size = 64
        downscaled = ImageProcessor.downscale_image(
            sample_image, 
            target_size, 
            apply_sharpen=True
        )
        
        assert downscaled.size == (target_size, target_size)
    
    def test_enhance_contrast(self, sample_image):
        """Test contrast enhancement"""
        enhanced = ImageProcessor.enhance_contrast(sample_image, factor=1.3)
        
        assert enhanced.size == sample_image.size
        assert enhanced.mode == sample_image.mode
    
    def test_create_favicon(self, sample_image):
        """Test favicon creation (16x16)"""
        # Create a 192x192 source for favicon
        source = sample_image.resize((192, 192))
        favicon = ImageProcessor.create_favicon(source)
        
        assert favicon.size == (16, 16)
    
    def test_image_to_base64_png(self, sample_image):
        """Test PNG to base64 conversion"""
        base64_str = ImageProcessor.image_to_base64(sample_image, format='PNG')
        
        assert base64_str.startswith('data:image/png;base64,')
        assert len(base64_str) > 100  # Should have substantial data
    
    def test_image_to_base64_jpeg(self, sample_image):
        """Test JPEG to base64 conversion"""
        base64_str = ImageProcessor.image_to_base64(sample_image, format='JPEG')
        
        assert base64_str.startswith('data:image/jpeg;base64,')
    
    def test_process_all_sizes(self, sample_image):
        """Test processing all PWA icon sizes"""
        img_512 = sample_image
        img_192 = sample_image.resize((192, 192))
        
        all_sizes = ImageProcessor.process_all_sizes(img_512, img_192)
        
        # Check all sizes are present
        assert '512' in all_sizes
        assert '192' in all_sizes
        assert '164' in all_sizes
        assert '16' in all_sizes
        
        # Check dimensions
        assert all_sizes['512'].size == (512, 512)
        assert all_sizes['192'].size == (192, 192)
        assert all_sizes['164'].size == (164, 164)
        assert all_sizes['16'].size == (16, 16)
    
    def test_images_to_base64_dict(self, sample_image):
        """Test batch base64 conversion"""
        images = {
            '512': sample_image,
            '192': sample_image.resize((192, 192))
        }
        
        base64_dict = ImageProcessor.images_to_base64_dict(images, format='PNG')
        
        assert '512' in base64_dict
        assert '192' in base64_dict
        assert base64_dict['512'].startswith('data:image/png;base64,')
        assert base64_dict['192'].startswith('data:image/png;base64,')


class TestImageQuality:
    """Test suite for image quality validation"""
    
    @pytest.fixture
    def high_res_image(self):
        """Create a high-resolution test image with gradient"""
        img = Image.new('RGB', (512, 512))
        pixels = img.load()
        for i in range(512):
            for j in range(512):
                pixels[i, j] = (i % 256, j % 256, (i + j) % 256)
        return img
    
    def test_downscale_preserves_quality(self, high_res_image):
        """Test that downscaling maintains acceptable quality"""
        sizes = [256, 192, 164, 64, 16]
        
        for size in sizes:
            downscaled = ImageProcessor.downscale_image(
                high_res_image, 
                size, 
                apply_sharpen=True
            )
            
            # Basic quality checks
            assert downscaled.size == (size, size)
            assert downscaled.mode == 'RGB'
            
            # Check it's not completely black or white (gradient preserved)
            pixels = list(downscaled.getdata())
            unique_colors = len(set(pixels))
            assert unique_colors > 1  # Should have variety


if __name__ == '__main__':
    pytest.main([__file__, '-v'])