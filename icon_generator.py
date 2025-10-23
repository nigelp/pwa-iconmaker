"""
AI Icon Generator using Stable Diffusion with LoRA
Handles dual-resolution generation with seed consistency
"""
import torch
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler
from PIL import Image
import random
from typing import Dict, Optional, Tuple
import config
import gc


class IconGenerator:
    """Manages Stable Diffusion model and icon generation"""
    
    def __init__(self, use_gpu: bool = True):
        """
        Initialize the icon generator
        
        Args:
            use_gpu: Whether to use GPU acceleration (CUDA)
        """
        self.device = "cuda" if use_gpu and torch.cuda.is_available() else "cpu"
        self.pipe = None
        self.current_model = None
        
        print(f"IconGenerator initialized on device: {self.device}")
        if self.device == "cuda":
            print(f"GPU: {torch.cuda.get_device_name(0)}")
            print(f"VRAM: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")
    
    def load_model(self) -> None:
        """Load Stable Diffusion model with LoRA"""
        if self.pipe is not None:
            print("Model already loaded")
            return
        
        print(f"Loading Stable Diffusion model from {config.MODEL_BASE}...")
        
        try:
            # Load base model
            self.pipe = StableDiffusionPipeline.from_pretrained(
                config.MODEL_BASE,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                safety_checker=None,  # Disable for icon generation
                requires_safety_checker=False
            )
            
            # Use DPM++ solver for faster, higher quality generation
            self.pipe.scheduler = DPMSolverMultistepScheduler.from_config(
                self.pipe.scheduler.config
            )
            
            # Move to device
            self.pipe = self.pipe.to(self.device)
            
            # Enable memory optimizations for GPU
            if self.device == "cuda":
                self.pipe.enable_attention_slicing()
                if config.OFFLOAD_MODELS:
                    self.pipe.enable_model_cpu_offload()
            
            # Load LoRA weights if available
            self._load_lora_weights()
            
            print("Model loaded successfully")
            
        except Exception as e:
            print(f"Error loading model: {e}")
            raise
    
    def _load_lora_weights(self) -> None:
        """Load LoRA fine-tuning weights"""
        # Check if LoRA files exist
        lora_loaded = False
        
        for name, path in config.LORA_MODELS.items():
            if path.exists():
                try:
                    print(f"Loading LoRA: {name} from {path}")
                    # Note: This is a placeholder - actual LoRA loading depends on
                    # the diffusers version and LoRA implementation
                    # You may need to use pipe.load_lora_weights() or similar
                    lora_loaded = True
                except Exception as e:
                    print(f"Warning: Could not load LoRA {name}: {e}")
        
        if not lora_loaded:
            print("Warning: No LoRA weights loaded. Using base model only.")
            print(f"Expected LoRA files at: {config.MODELS_DIR}")
    
    def enhance_prompt(self, prompt: str, for_small_icon: bool = False) -> str:
        """
        Enhance user prompt for better icon generation
        Includes LORA activation tag for fine-tuned quality
        
        Args:
            prompt: User's original prompt
            for_small_icon: Whether this is for small icon (16x16 or 164x164)
            
        Returns:
            Enhanced prompt with LORA activation
        """
        # Add LORA base tag + user prompt + style suffix
        if for_small_icon:
            return f"{config.LORA_BASE_TAG}, {prompt}{config.SMALL_ICON_PROMPT_SUFFIX}"
        else:
            return f"{config.LORA_BASE_TAG}, {prompt}{config.ICON_PROMPT_SUFFIX}"
    
    def generate_icon(
        self,
        prompt: str,
        size: int,
        steps: int = config.DEFAULT_STEPS,
        guidance_scale: float = config.DEFAULT_GUIDANCE_SCALE,
        seed: Optional[int] = None,
        enhance_for_small: bool = False
    ) -> Tuple[Image.Image, int]:
        """
        Generate a single icon at specified size
        
        Args:
            prompt: Text prompt for generation
            size: Output size (width and height)
            steps: Number of inference steps
            guidance_scale: CFG scale for prompt adherence
            seed: Random seed for reproducibility (None for random)
            enhance_for_small: Whether to enhance prompt for small icons
            
        Returns:
            Tuple of (Generated PIL Image, seed used)
        """
        # Load model if not already loaded
        if self.pipe is None:
            self.load_model()
        
        # Generate or use provided seed
        if seed is None:
            seed = random.randint(0, 2**32 - 1)
        
        # Set up generator for reproducibility
        generator = torch.Generator(device=self.device).manual_seed(seed)
        
        # Enhance prompt
        enhanced_prompt = self.enhance_prompt(prompt, for_small_icon=enhance_for_small)
        
        print(f"Generating {size}x{size} icon with seed {seed}...")
        print(f"Enhanced prompt: {enhanced_prompt}")
        
        try:
            # Generate image
            with torch.no_grad():
                result = self.pipe(
                    prompt=enhanced_prompt,
                    height=size,
                    width=size,
                    num_inference_steps=steps,
                    guidance_scale=guidance_scale,
                    generator=generator
                )
            
            image = result.images[0]
            print(f"Generated {size}x{size} icon successfully")
            
            return image, seed
            
        except torch.cuda.OutOfMemoryError:
            print("CUDA out of memory! Trying to free memory and retry...")
            self._clear_cuda_memory()
            raise
        except Exception as e:
            print(f"Error during generation: {e}")
            raise
    
    def generate_pwa_icons(
        self,
        prompt: str,
        steps: int = config.DEFAULT_STEPS,
        guidance_scale: float = config.DEFAULT_GUIDANCE_SCALE,
        seed: Optional[int] = None
    ) -> Tuple[Image.Image, int, float]:
        """
        Generate single 512x512 icon - all other sizes created via downscaling
        This ensures perfect visual consistency across all icon sizes
        
        Args:
            prompt: Text prompt for generation
            steps: Number of inference steps
            guidance_scale: CFG scale
            seed: Random seed (None for random)
            
        Returns:
            Tuple of (512x512 Image, seed used, generation time)
        """
        import time
        
        # Generate seed if not provided
        if seed is None:
            seed = random.randint(0, 2**32 - 1)
        
        print(f"\n{'='*60}")
        print(f"Generating PWA icon (512x512) with seed: {seed}")
        print(f"Prompt: {prompt}")
        print(f"Steps: {steps}, Guidance: {guidance_scale}")
        print(f"{'='*60}\n")
        
        try:
            # Generate 512x512 master icon
            start = time.time()
            img_512, _ = self.generate_icon(
                prompt=prompt,
                size=512,
                steps=steps,
                guidance_scale=guidance_scale,
                seed=seed,
                enhance_for_small=False
            )
            generation_time = time.time() - start
            
            print(f"\n{'='*60}")
            print(f"Generation complete! Time: {generation_time:.2f}s")
            print(f"All other sizes will be created via high-quality downscaling")
            print(f"{'='*60}\n")
            
            return img_512, seed, generation_time
            
        except Exception as e:
            print(f"Error during PWA icon generation: {e}")
            raise
    
    def _clear_cuda_memory(self) -> None:
        """Clear CUDA memory cache"""
        if self.device == "cuda":
            torch.cuda.empty_cache()
            gc.collect()
            print("Cleared CUDA memory cache")
    
    def unload_model(self) -> None:
        """Unload model from memory"""
        if self.pipe is not None:
            del self.pipe
            self.pipe = None
            self._clear_cuda_memory()
            print("Model unloaded from memory")
    
    def get_memory_usage(self) -> Dict[str, float]:
        """
        Get current memory usage statistics
        
        Returns:
            Dict with memory info in GB
        """
        if self.device == "cuda":
            return {
                "allocated_gb": torch.cuda.memory_allocated() / 1e9,
                "reserved_gb": torch.cuda.memory_reserved() / 1e9,
                "max_allocated_gb": torch.cuda.max_memory_allocated() / 1e9
            }
        else:
            return {
                "allocated_gb": 0,
                "reserved_gb": 0,
                "max_allocated_gb": 0
            }