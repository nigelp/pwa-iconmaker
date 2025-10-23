"""
ZIP Bundling Service for Cool PWA Icon Generator
Creates bundled downloads with all icon sizes and manifest template
"""
import zipfile
import io
import json
from pathlib import Path
from typing import Dict, Optional
from PIL import Image
import config
from image_processor import ImageProcessor


class ZipBundler:
    """Handles creation of ZIP bundles with PWA icons"""
    
    @staticmethod
    def create_pwa_bundle(
        images: Dict[str, Image.Image],
        format: str = "png",
        include_manifest: bool = True,
        app_name: str = "My PWA App"
    ) -> io.BytesIO:
        """
        Create a ZIP bundle with all PWA icon sizes
        
        Args:
            images: Dict mapping size -> PIL Image (e.g., {"512": img, ...})
            format: Output format (png or jpeg)
            include_manifest: Whether to include manifest.json template
            app_name: App name for manifest template
            
        Returns:
            BytesIO object containing ZIP file
        """
        zip_buffer = io.BytesIO()
        
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            # Add each icon to ZIP
            for size, image in images.items():
                # Use ICO format for favicon, specified format for others
                icon_format = "ICO" if size == "16" else format
                filename = ZipBundler._get_icon_filename(size, format)
                
                # Convert image to bytes
                img_buffer = io.BytesIO()
                ImageProcessor.save_image(image, img_buffer, icon_format)
                img_buffer.seek(0)
                
                # Add to ZIP
                zip_file.writestr(filename, img_buffer.getvalue())
                print(f"Added {filename} to ZIP bundle")
            
            # Add manifest.json template if requested
            if include_manifest:
                manifest = ZipBundler._create_manifest_template(
                    app_name=app_name,
                    format=format
                )
                zip_file.writestr(
                    "manifest.json",
                    json.dumps(manifest, indent=2)
                )
                print("Added manifest.json template to ZIP bundle")
            
            # Add README with instructions
            readme = ZipBundler._create_readme()
            zip_file.writestr("README.txt", readme)
            print("Added README.txt to ZIP bundle")
        
        zip_buffer.seek(0)
        return zip_buffer
    
    @staticmethod
    def _get_icon_filename(size: str, format: str) -> str:
        """
        Generate appropriate filename for icon
        
        Args:
            size: Icon size (e.g., "512", "192", "164", "16")
            format: File format
            
        Returns:
            Filename string
        """
        # Special handling for favicon - always use ICO format
        if size == "16":
            return "favicon.ico"
        else:
            ext = format.lower()
            return f"icon-{size}x{size}.{ext}"
    
    @staticmethod
    def _create_manifest_template(
        app_name: str,
        format: str
    ) -> Dict:
        """
        Create PWA manifest.json template
        
        Args:
            app_name: Application name
            format: Icon format
            
        Returns:
            Manifest dictionary
        """
        ext = format.lower()
        mime_type = f"image/{ext}"
        
        manifest = {
            "name": app_name,
            "short_name": app_name,
            "description": "Progressive Web App",
            "start_url": "/",
            "display": "standalone",
            "theme_color": "#000000",
            "background_color": "#ffffff",
            "icons": [
                {
                    "src": f"icon-512x512.{ext}",
                    "sizes": "512x512",
                    "type": mime_type,
                    "purpose": "any maskable"
                },
                {
                    "src": f"icon-192x192.{ext}",
                    "sizes": "192x192",
                    "type": mime_type,
                    "purpose": "any maskable"
                },
                {
                    "src": f"icon-164x164.{ext}",
                    "sizes": "164x164",
                    "type": mime_type
                }
            ]
        }
        
        return manifest
    
    @staticmethod
    def _create_readme() -> str:
        """
        Create README with usage instructions
        
        Returns:
            README text
        """
        return """Cool PWA Icon Generator - Generated Icons
========================================
Offline AI-Powered Progressive Web App Icon Maker

This package contains all the icon sizes needed for your Progressive Web App (PWA).

INCLUDED FILES:
--------------
- icon-512x512.*     : Large icon (app launcher, splash screen)
- icon-192x192.*     : Medium icon (app launcher, home screen)
- icon-164x164.*     : Small icon (various UI elements)
- favicon.ico        : Favicon for browser tabs (ICO format)
- manifest.json      : PWA manifest template
- README.txt         : This file

INSTALLATION INSTRUCTIONS:
-------------------------
1. Copy all icon files to your app's public/images directory
2. Update manifest.json with your app details:
   - Change "name" and "short_name" to your app name
   - Update "theme_color" and "background_color" to match your brand
   - Adjust "start_url" if needed

3. Reference the manifest in your HTML <head>:
   <link rel="manifest" href="/manifest.json">

4. Add favicon reference:
   <link rel="icon" type="image/png" href="/images/favicon-16x16.png">

5. For best results, also add these meta tags:
   <meta name="theme-color" content="#000000">
   <link rel="apple-touch-icon" href="/images/icon-192x192.png">

PWA MANIFEST ICON PURPOSES:
---------------------------
- "any": Icon can be used for any purpose
- "maskable": Icon designed to work with adaptive icon masks
  (Note: For true maskable icons, ensure your design has important 
  content in the center 'safe zone' with padding around edges)

BROWSER SUPPORT:
---------------
- Chrome/Edge: Full support for all features
- Firefox: Full support for all features
- Safari: Partial support (manifest.json support varies)

For more information about PWAs:
https://web.dev/progressive-web-apps/

Generated by PWA Icon Generator
https://github.com/yourusername/pwa-icon-generator
"""
    
    @staticmethod
    def get_bundle_size(zip_buffer: io.BytesIO) -> float:
        """
        Get size of ZIP bundle in MB
        
        Args:
            zip_buffer: BytesIO containing ZIP
            
        Returns:
            Size in megabytes
        """
        return len(zip_buffer.getvalue()) / (1024 * 1024)
    
    @staticmethod
    def create_single_icon_download(
        image: Image.Image,
        size: str,
        format: str = "png"
    ) -> io.BytesIO:
        """
        Create download buffer for single icon
        
        Args:
            image: PIL Image
            size: Size identifier (e.g., "512")
            format: Output format
            
        Returns:
            BytesIO with image data
        """
        buffer = io.BytesIO()
        ImageProcessor.save_image(image, buffer, format)
        buffer.seek(0)
        return buffer