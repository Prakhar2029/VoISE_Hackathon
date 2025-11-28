import sys
import os

# Add the current directory to sys.path
sys.path.append(os.getcwd())

print("Verifying modules...")

try:
    print("Importing app.vision.camera...")
    from app.vision import camera
    print("Importing app.vision.detector...")
    from app.vision import detector
    
    print("Importing app.audio.recorder...")
    from app.audio import recorder
    print("Importing app.audio.transcriber...")
    from app.audio import transcriber
    
    print("Importing app.logic.symptoms...")
    from app.logic import symptoms
    print("Importing app.logic.scoring...")
    from app.logic import scoring
    
    print("Importing app.components.dashboard...")
    from app.components import dashboard
    
    print("\n✅ All modules imported successfully!")
    
except ImportError as e:
    print(f"\n❌ Import failed: {e}")
    sys.exit(1)
except Exception as e:
    print(f"\n❌ Error: {e}")
    sys.exit(1)
