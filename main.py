"""
FastAPI Backend for Cool PWA Icon Generator
Offline AI-Powered Progressive Web App Icon Maker
"""
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, Dict
import uuid
import time
from datetime import datetime, timedelta
import config
from icon_generator import IconGenerator
from image_processor import ImageProcessor
from zip_bundler import ZipBundler

# Initialize FastAPI app
app = FastAPI(
    title="Cool PWA Icon Generator",
    description="Offline AI-Powered Progressive Web App Icon Maker",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global storage for generated icons (in-memory cache)
# In production, consider using Redis or similar
generation_cache: Dict[str, Dict] = {}

# Global generator instance
generator: Optional[IconGenerator] = None


class GenerationRequest(BaseModel):
    """Request model for icon generation"""
    prompt: str = Field(..., min_length=1, max_length=500, description="Text prompt for icon generation")
    steps: int = Field(20, description="Number of inference steps (20 or 50)")
    format: str = Field("png", description="Output format (png or jpeg)")
    use_gpu: bool = Field(True, description="Enable GPU acceleration")
    
    class Config:
        json_schema_extra = {
            "example": {
                "prompt": "A modern blue gradient app icon",
                "steps": 20,
                "format": "png",
                "use_gpu": True
            }
        }


class GenerationResponse(BaseModel):
    """Response model for icon generation"""
    generation_id: str
    icons: Dict[str, str]  # size -> base64 encoded image
    metadata: Dict


@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    global generator
    print("Starting Cool PWA Icon Generator API...")
    print(f"Server: http://{config.HOST}:{config.PORT}")
    # Generator will be lazy-loaded on first request


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    global generator
    if generator:
        generator.unload_model()
    print("Cool PWA Icon Generator API shut down")


def cleanup_old_generations():
    """Remove generations older than configured retention time"""
    current_time = datetime.now()
    to_remove = []
    
    for gen_id, data in generation_cache.items():
        if current_time - data['timestamp'] > timedelta(hours=config.TEMP_FILE_RETENTION_HOURS):
            to_remove.append(gen_id)
    
    for gen_id in to_remove:
        del generation_cache[gen_id]
        print(f"Cleaned up generation {gen_id}")


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "name": "Cool PWA Icon Generator API",
        "version": "1.0.0",
        "tagline": "Offline AI-Powered Progressive Web App Icon Maker",
        "endpoints": {
            "generate": "/api/generate",
            "download_bundle": "/api/download/bundle/{generation_id}",
            "download_single": "/api/download/single/{generation_id}/{size}",
            "status": "/api/status"
        },
        "documentation": "/docs"
    }


@app.get("/api/status")
async def get_status():
    """Get API and model status"""
    global generator
    
    status = {
        "api": "online",
        "model_loaded": generator is not None and generator.pipe is not None,
        "device": generator.device if generator else "not initialized",
        "cached_generations": len(generation_cache),
        "config": {
            "available_steps": config.AVAILABLE_STEPS,
            "available_formats": config.AVAILABLE_FORMATS,
            "icon_sizes": config.ICON_SIZES
        }
    }
    
    if generator and generator.device == "cuda":
        try:
            memory_info = generator.get_memory_usage()
            status["gpu_memory"] = memory_info
        except:
            pass
    
    return status


@app.post("/api/generate", response_model=GenerationResponse)
async def generate_icons(
    request: GenerationRequest,
    background_tasks: BackgroundTasks
):
    """
    Generate all PWA icon sizes from a text prompt
    
    Returns base64-encoded images for preview
    """
    global generator
    
    # Validate steps
    if request.steps not in config.AVAILABLE_STEPS:
        raise HTTPException(
            status_code=400,
            detail=f"Steps must be one of {config.AVAILABLE_STEPS}"
        )
    
    # Validate format
    if request.format.lower() not in config.AVAILABLE_FORMATS:
        raise HTTPException(
            status_code=400,
            detail=f"Format must be one of {config.AVAILABLE_FORMATS}"
        )
    
    try:
        # Initialize generator if needed
        if generator is None:
            print(f"Initializing generator (GPU: {request.use_gpu})...")
            generator = IconGenerator(use_gpu=request.use_gpu)
        
        # Load model
        generator.load_model()
        
        # Generate AI icon (512x512 master image)
        start_time = time.time()
        img_512, seed, generation_time = generator.generate_pwa_icons(
            prompt=request.prompt,
            steps=request.steps,
            guidance_scale=config.DEFAULT_GUIDANCE_SCALE
        )
        
        # Process all sizes (192, 164, 16 created via high-quality downscaling)
        all_icons = ImageProcessor.process_all_sizes(img_512)
        
        # Convert to base64 for preview
        base64_icons = ImageProcessor.images_to_base64_dict(
            all_icons,
            format=request.format.upper()
        )
        
        total_time = time.time() - start_time
        
        # Generate unique ID for this generation
        generation_id = str(uuid.uuid4())
        
        # Cache the generation
        generation_cache[generation_id] = {
            'icons': all_icons,
            'format': request.format.lower(),
            'prompt': request.prompt,
            'seed': seed,
            'timestamp': datetime.now(),
            'generation_time': generation_time,
            'total_time': total_time
        }
        
        # Schedule cleanup in background
        background_tasks.add_task(cleanup_old_generations)
        
        # Get memory usage if GPU
        memory_info = generator.get_memory_usage() if request.use_gpu else {}
        
        # Prepare metadata
        metadata = {
            "seed": seed,
            "steps": request.steps,
            "format": request.format,
            "generation_time_seconds": round(total_time, 2),
            "timing_breakdown": {
                "ai_generation": round(generation_time, 2),
                "image_processing": round(total_time - generation_time, 2),
                "total": round(total_time, 2)
            },
            "device": generator.device,
            "memory_usage_gb": memory_info,
            "model": "Stable Diffusion 1.5 + LoRA",
            "optimization": "Single 512x512 generation + high-quality downscaling"
        }
        
        return GenerationResponse(
            generation_id=generation_id,
            icons=base64_icons,
            metadata=metadata
        )
        
    except torch.cuda.OutOfMemoryError:
        raise HTTPException(
            status_code=507,
            detail="Insufficient GPU memory. Try reducing steps or disabling GPU."
        )
    except Exception as e:
        print(f"Generation error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Generation failed: {str(e)}"
        )


@app.get("/api/download/bundle/{generation_id}")
async def download_bundle(generation_id: str, format: Optional[str] = None):
    """
    Download all icons as a ZIP bundle
    
    Args:
        generation_id: ID from generation response
        format: Optional format override (png or jpeg)
    """
    if generation_id not in generation_cache:
        raise HTTPException(
            status_code=404,
            detail="Generation not found or expired"
        )
    
    cached = generation_cache[generation_id]
    icons = cached['icons']
    output_format = format.lower() if format else cached['format']
    
    # Validate format
    if output_format not in config.AVAILABLE_FORMATS:
        raise HTTPException(
            status_code=400,
            detail=f"Format must be one of {config.AVAILABLE_FORMATS}"
        )
    
    try:
        # Create ZIP bundle
        zip_buffer = ZipBundler.create_pwa_bundle(
            images=icons,
            format=output_format,
            include_manifest=True,
            app_name="My PWA App"
        )
        
        # Check size
        bundle_size_mb = ZipBundler.get_bundle_size(zip_buffer)
        if bundle_size_mb > config.MAX_ZIP_SIZE_MB:
            raise HTTPException(
                status_code=413,
                detail=f"Bundle too large: {bundle_size_mb:.2f}MB (max: {config.MAX_ZIP_SIZE_MB}MB)"
            )
        
        # Return as streaming response
        return StreamingResponse(
            zip_buffer,
            media_type="application/zip",
            headers={
                "Content-Disposition": f"attachment; filename=pwa-icons-{generation_id[:8]}.zip"
            }
        )
        
    except Exception as e:
        print(f"Bundle creation error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create bundle: {str(e)}"
        )


@app.get("/api/download/single/{generation_id}/{size}")
async def download_single_icon(
    generation_id: str,
    size: str,
    format: Optional[str] = None
):
    """
    Download a single icon size
    
    Args:
        generation_id: ID from generation response
        size: Icon size (512, 192, 164, or 16)
        format: Optional format override
    """
    if generation_id not in generation_cache:
        raise HTTPException(
            status_code=404,
            detail="Generation not found or expired"
        )
    
    cached = generation_cache[generation_id]
    icons = cached['icons']
    output_format = format.lower() if format else cached['format']
    
    # Validate size
    if size not in icons:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid size. Must be one of: {list(icons.keys())}"
        )
    
    # Validate format
    if output_format not in config.AVAILABLE_FORMATS:
        raise HTTPException(
            status_code=400,
            detail=f"Format must be one of {config.AVAILABLE_FORMATS}"
        )
    
    try:
        # Use ICO format for favicon, specified format for others
        download_format = "ico" if size == "16" else output_format
        
        # Create single icon download
        icon_buffer = ZipBundler.create_single_icon_download(
            image=icons[size],
            size=size,
            format=download_format
        )
        
        # Determine filename and media type
        if size == "16":
            filename = "favicon.ico"
            media_type = "image/x-icon"
        else:
            filename = f"icon-{size}x{size}.{output_format}"
            media_type = f"image/{output_format}"
        
        # Return as streaming response
        return StreamingResponse(
            icon_buffer,
            media_type=media_type,
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )
        
    except Exception as e:
        print(f"Single download error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to download icon: {str(e)}"
        )


# Import torch after defining app to avoid circular imports
import torch


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=config.HOST,
        port=config.PORT,
        reload=config.RELOAD
    )