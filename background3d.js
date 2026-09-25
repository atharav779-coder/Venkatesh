import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

gsap.registerPlugin(ScrollTrigger);

// Clean up
const container = document.getElementById('bg-canvas-container');
container.innerHTML = '';

// 1. Setup Scene, Camera, Renderer
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(50, window.innerWidth / window.innerHeight, 0.1, 1000);
camera.position.set(0, 0, 10);

const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
container.appendChild(renderer.domElement);

// Photorealistic Studio Environment
const pmremGenerator = new THREE.PMREMGenerator( renderer );
pmremGenerator.compileEquirectangularShader();
scene.environment = pmremGenerator.fromScene( new RoomEnvironment(), 0.04 ).texture;

// 2. Realism Upgrade: Lighting
const ambientLight = new THREE.AmbientLight(0xffffff, 0.8);
scene.add(ambientLight);

const directionalLight = new THREE.DirectionalLight(0xffffff, 2.5);
directionalLight.position.set(5, 10, 7);
scene.add(directionalLight);

const rimLight = new THREE.PointLight(0x00f0ff, 100, 50);
rimLight.position.set(-5, 0, -5);
scene.add(rimLight);

const engineLight = new THREE.PointLight(0xf97316, 100, 50);
engineLight.position.set(5, -5, 5);
scene.add(engineLight);

const scrollGroup = new THREE.Group(); 
scene.add(scrollGroup);

const hoverGroup = new THREE.Group(); 
scrollGroup.add(hoverGroup);

// Position centered
const updateAssemblyPosition = () => {
    scrollGroup.position.set(0, 0, 0); 
};
updateAssemblyPosition();

// 3. Import & Configure the 3D Model
const loader = new GLTFLoader();

loader.load('/models/jet_engine/scene.gltf', (gltf) => {
    const model = gltf.scene;
    
    // Scale slightly smaller as requested (10 instead of 14)
    const box = new THREE.Box3().setFromObject(model);
    const center = box.getCenter(new THREE.Vector3());
    const size = box.getSize(new THREE.Vector3());
    const maxDim = Math.max(size.x, size.y, size.z);
    
    const scale = 11 / maxDim; // Decreased size a bit
    model.scale.setScalar(scale);
    model.position.sub(center.multiplyScalar(scale)); 
    
    model.traverse((child) => {
        if (child.isMesh) {
            const oldMat = child.material;
            child.material = new THREE.MeshPhysicalMaterial({
                color: oldMat.color || 0xcccccc,
                metalness: 1.0,           
                roughness: 0.15,          
                clearcoat: 1.0,           
                clearcoatRoughness: 0.1,
                envMapIntensity: 2.0,     
                side: THREE.DoubleSide
            });
        }
    });

    // Idle static angle so we can see inside the engine beautifully
    hoverGroup.rotation.y = Math.PI / 4;  // 45 degrees
    hoverGroup.rotation.x = Math.PI / 12; // Slight tilt down
    hoverGroup.add(model);

    // --- PRECISE BLADE TARGETING ---
    // The previous algorithm selected the thin front cowl.
    // The true rotating assembly (shaft + blades) is the one that spans deep into the engine.
    window.engineBlade = null;
    model.traverse((child) => {
        if (child.isMesh) {
            child.geometry.computeBoundingBox();
            const mSize = new THREE.Vector3();
            child.geometry.boundingBox.getSize(mSize);
            
            // The shaft+blades assembly has a Z-length of roughly 66.8 
            // and X/Y radius of roughly 28.8.
            // We find the mesh with Z > 60 and Z < 70
            if (mSize.z > 60 && mSize.z < 70 && mSize.x > 25 && mSize.x < 35) {
                window.engineBlade = child;
            }
        }
    });

    // We know the engine is aligned along the Z axis from our previous analysis
    window.thrustAxis = 'z';
}, undefined, (error) => {
    console.error('Error loading GLTF:', error);
});

// Handle resizing
window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
    updateAssemblyPosition();
});

// The High-Performance Loop
function renderLoop() {
    requestAnimationFrame(renderLoop);
    
    // Rotate ONLY the specific internal blade mesh, keeping the engine idle
    if (window.engineBlade) {
        window.engineBlade.rotation[window.thrustAxis] += 0.4; // Very fast spin
    }
    
    renderer.render(scene, camera);
}
renderLoop();
