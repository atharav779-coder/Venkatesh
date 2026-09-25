import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';

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

    // --- SMART BLADE DETECTION LOGIC ---
    const allMeshes = [];
    model.traverse((child) => {
        if (child.isMesh) {
            allMeshes.push(child);
        }
    });

    let largestMesh = null;
    let maxVolume = 0;
    
    // Find the outer casing (largest volume)
    allMeshes.forEach(mesh => {
        mesh.geometry.computeBoundingBox();
        const bbox = mesh.geometry.boundingBox;
        const meshSize = new THREE.Vector3();
        bbox.getSize(meshSize);
        const volume = meshSize.x * meshSize.y * meshSize.z;
        if (volume > maxVolume) {
            maxVolume = volume;
            largestMesh = mesh;
        }
    });

    // Detect thrust axis based on the casing's longest dimension
    const casingSize = new THREE.Vector3();
    largestMesh.geometry.boundingBox.getSize(casingSize);
    let thrustAxis = 'z';
    if (casingSize.x >= casingSize.y && casingSize.x >= casingSize.z) thrustAxis = 'x';
    if (casingSize.y >= casingSize.x && casingSize.y >= casingSize.z) thrustAxis = 'y';
    window.thrustAxis = thrustAxis;

    // Detect the blades: they are usually thin disks.
    // We calculate the ratio of thickness (along thrust axis) to radius (average of other two axes).
    // The mesh with the lowest ratio is the most "disk-like" and is almost certainly the fan blade.
    let bestBlade = null;
    let lowestRatio = 9999;

    allMeshes.forEach(mesh => {
        if (mesh === largestMesh) return; // Skip casing
        
        const mSize = new THREE.Vector3();
        mesh.geometry.boundingBox.getSize(mSize);
        
        let thickness, radius;
        if (thrustAxis === 'z') {
            thickness = mSize.z;
            radius = (mSize.x + mSize.y) / 2;
        } else if (thrustAxis === 'y') {
            thickness = mSize.y;
            radius = (mSize.x + mSize.z) / 2;
        } else {
            thickness = mSize.x;
            radius = (mSize.y + mSize.z) / 2;
        }
        
        const ratio = thickness / radius;
        if (ratio < lowestRatio) {
            lowestRatio = ratio;
            bestBlade = mesh;
        }
    });

    // Save only the exact blade mesh for rotation
    if (bestBlade) {
        window.engineBlade = bestBlade;
    }

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
