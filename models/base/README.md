# Base Models and Templates

This directory contains the base models and templates for the AI cartoon figurine generation system.

## Body Templates

Body templates are 3D meshes that serve as the foundation for figurine generation. Each template includes:

- **Geometry**: Base mesh in OBJ format
- **Texture coordinates**: UV mapping for texture application
- **Articulation points**: Joint locations for posing
- **Metadata**: Dimensions, style information, and compatibility notes

### Available Templates (MVP Week 1 - Placeholders)

1. **default** - Standard cartoon figurine template
   - File: `default_body.obj` (to be added)
   - Dimensions: 180mm x 60mm x 40mm
   - Style: Classic cartoon proportions
   - Gender: Neutral

2. **superhero** - Dynamic superhero stance
   - File: `superhero_body.obj` (to be added)
   - Dimensions: 190mm x 65mm x 45mm
   - Style: Heroic pose with cape attachment point
   - Gender: Neutral

3. **casual** - Relaxed everyday pose
   - File: `casual_body.obj` (to be added)
   - Dimensions: 175mm x 58mm x 38mm
   - Style: Natural standing pose
   - Gender: Neutral

## Model Integration Placeholders

### Stylization Models
- **SDXL + LoRA**: To be integrated for 2D cartoon stylization
- **Model path**: `stylization/sdxl_cartoon_lora.safetensors`
- **Config**: `stylization/config.json`

### Face Analysis Models
- **ArcFace**: For face similarity evaluation
- **Model path**: `face_analysis/arcface_r100.onnx`
- **CLIP**: For style consistency evaluation
- **Model path**: `clip/ViT-B-32.pt`

## File Structure

```
models/base/
├── README.md (this file)
├── body_templates/
│   ├── default_body.obj (to be added)
│   ├── superhero_body.obj (to be added)
│   ├── casual_body.obj (to be added)
│   └── templates_metadata.json (to be added)
├── stylization/
│   ├── sdxl_cartoon_lora.safetensors (to be added)
│   └── config.json (to be added)
├── face_analysis/
│   ├── arcface_r100.onnx (to be added)
│   └── clip_vit_b32.pt (to be added)
└── texture_assets/
    ├── base_materials.mtl (to be added)
    └── default_textures/ (to be added)
```

## Usage

### Loading Body Templates

```python
from services.fusion.fuse import get_available_body_templates

# Get available templates
templates = get_available_body_templates()
print(f"Available templates: {list(templates.keys())}")

# Use in fusion process
from services.fusion.fuse import fuse_face_body

result = fuse_face_body(
    face_image="path/to/face.jpg",
    body_template="default"
)
```

### Model Requirements

- **File formats**: OBJ for geometry, MTL for materials, PNG/JPG for textures
- **Scale**: Models should be in millimeters for 3D printing
- **Topology**: Clean manifold geometry suitable for 3D printing
- **Textures**: 1024x1024 resolution minimum

## Development Notes

This is MVP Week 1 scaffolding. Real model files will be added in subsequent PRs:

1. **Geometry Processing**: Integration with trimesh/pykdtree for mesh operations
2. **Texture Pipeline**: Automatic texture generation and mapping
3. **Model Validation**: Geometry checks for printability
4. **Caching System**: Model loading optimization
5. **Version Management**: Model versioning and compatibility tracking

## Adding New Templates

To add a new body template:

1. Place OBJ file in `body_templates/`
2. Update `templates_metadata.json` with template info
3. Add template to `get_available_body_templates()` in `services/fusion/fuse.py`
4. Test with fusion service
5. Update documentation