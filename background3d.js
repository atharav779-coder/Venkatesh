import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

gsap.registerPlugin(ScrollTrigger);

// Clean up
const container = document.getElementById('bg-canvas-container');
if (container) container.innerHTML = '';

// 1. Setup Scene, Camera, Renderer
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(50, window.innerWidth / window.innerHeight, 0.1, 1000);
camera.position.set(0, 0, 10);

const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
if (container) container.appendChild(renderer.domElement);

// Photorealistic Studio Environment
const pmremGenerator = new THREE.PMREMGenerator(renderer);
pmremGenerator.compileEquirectangularShader();
scene.environment = pmremGenerator.fromScene(new RoomEnvironment(), 0.04).texture;

// 2. Realism Lighting
const ambientLight = new THREE.AmbientLight(0xffffff, 0.9);
scene.add(ambientLight);

const directionalLight = new THREE.DirectionalLight(0xffffff, 2.8);
directionalLight.position.set(6, 10, 8);
scene.add(directionalLight);

const rimLight = new THREE.PointLight(0x0284c7, 120, 60);
rimLight.position.set(-6, 0, -6);
scene.add(rimLight);

const engineLight = new THREE.PointLight(0xf97316, 120, 60);
engineLight.position.set(6, -5, 6);
scene.add(engineLight);

// 3. Coordinate Groups
const scrollGroup = new THREE.Group(); 
scene.add(scrollGroup);

const hoverGroup = new THREE.Group(); 
scrollGroup.add(hoverGroup);

// Position centered
const updateAssemblyPosition = () => {
    scrollGroup.position.set(0, 0, 0); 
};
updateAssemblyPosition();

// 4. Floating 3D Telemetry Navigation Rings
const ringGeo1 = new THREE.RingGeometry(6.6, 6.64, 96);
const ringMat1 = new THREE.MeshBasicMaterial({
    color: 0xf97316,
    side: THREE.DoubleSide,
    transparent: true,
    opacity: 0.28
});
const telemetryRing1 = new THREE.Mesh(ringGeo1, ringMat1);
telemetryRing1.rotation.x = Math.PI / 2;
scrollGroup.add(telemetryRing1);

const ringGeo2 = new THREE.RingGeometry(5.2, 5.23, 72);
const ringMat2 = new THREE.MeshBasicMaterial({
    color: 0x0284c7,
    side: THREE.DoubleSide,
    transparent: true,
    opacity: 0.22
});
const telemetryRing2 = new THREE.Mesh(ringGeo2, ringMat2);
telemetryRing2.rotation.x = Math.PI / 2.25;
telemetryRing2.rotation.y = Math.PI / 6;
scrollGroup.add(telemetryRing2);

// 5. Floating Aerodynamic Particle Field
const particleCount = 650;
const particleGeo = new THREE.BufferGeometry();
const particlePositions = new Float32Array(particleCount * 3);

for (let i = 0; i < particleCount; i++) {
    particlePositions[i * 3] = (Math.random() - 0.5) * 36;
    particlePositions[i * 3 + 1] = (Math.random() - 0.5) * 36;
    particlePositions[i * 3 + 2] = (Math.random() - 0.5) * 36;
}
particleGeo.setAttribute('position', new THREE.BufferAttribute(particlePositions, 3));

// Procedural soft-glow particle texture
const pCanvas = document.createElement('canvas');
pCanvas.width = 32;
pCanvas.height = 32;
const pCtx = pCanvas.getContext('2d');
const pGrad = pCtx.createRadialGradient(16, 16, 0, 16, 16, 16);
pGrad.addColorStop(0, 'rgba(249, 115, 22, 1)');
pGrad.addColorStop(0.35, 'rgba(249, 115, 22, 0.45)');
pGrad.addColorStop(1, 'rgba(249, 115, 22, 0)');
pCtx.fillStyle = pGrad;
pCtx.fillRect(0, 0, 32, 32);

const particleTexture = new THREE.CanvasTexture(pCanvas);
const particleMat = new THREE.PointsMaterial({
    size: 0.35,
    map: particleTexture,
    transparent: true,
    blending: THREE.AdditiveBlending,
    depthWrite: false,
    opacity: 0.55
});

const particles = new THREE.Points(particleGeo, particleMat);
scene.add(particles);

// 6. Import & Configure the 3D Model
const loader = new GLTFLoader();
const clock = new THREE.Clock();

loader.load('/models/jet_engine/scene.gltf', (gltf) => {
    const model = gltf.scene;
    
    const box = new THREE.Box3().setFromObject(model);
    const center = box.getCenter(new THREE.Vector3());
    const size = box.getSize(new THREE.Vector3());
    const maxDim = Math.max(size.x, size.y, size.z);
    
    const scale = 11 / maxDim; 
    model.scale.setScalar(scale);
    model.position.sub(center.multiplyScalar(scale)); 
    
    model.traverse((child) => {
        if (child.isMesh) {
            const oldMat = child.material;
            child.material = new THREE.MeshPhysicalMaterial({
                color: oldMat.color || 0xd1d5db,
                metalness: 0.95,           
                roughness: 0.18,          
                clearcoat: 1.0,           
                clearcoatRoughness: 0.1,
                envMapIntensity: 2.2,     
                side: THREE.DoubleSide
            });
        }
    });

    // Face forward
    hoverGroup.rotation.y = Math.PI / 2;
    hoverGroup.rotation.x = 0;
    hoverGroup.add(model);

    // --- GSAP SCROLL CHOREOGRAPHY ---
    const tl = gsap.timeline({
        scrollTrigger: {
            trigger: "body",
            start: "top top",
            end: "bottom bottom",
            scrub: 1.5
        }
    });

    tl.to(scrollGroup.rotation, {
        y: Math.PI * 2,
        ease: "none"
    }, 0);

}, undefined, (error) => {
    console.error('Error loading GLTF:', error);
});

// 7. Interactive Mouse Parallax Tracking
let mouseX = 0, mouseY = 0;
let targetCamX = 0, targetCamY = 0;

window.addEventListener('mousemove', (e) => {
    mouseX = (e.clientX / window.innerWidth) * 2 - 1;
    mouseY = -(e.clientY / window.innerHeight) * 2 + 1;
    targetCamX = mouseX * 1.2;
    targetCamY = mouseY * 0.9;
});

// Handle resizing
window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
    updateAssemblyPosition();
});

// 8. The High-Performance Render Loop with Zero-Gravity Levitation
function renderLoop() {
    requestAnimationFrame(renderLoop);
    
    const time = clock.getElapsedTime();
    
    // Smooth zero-gravity floating levitation
    hoverGroup.position.y = Math.sin(time * 1.1) * 0.18;
    hoverGroup.rotation.z = Math.sin(time * 0.7) * 0.025;
    
    // Subtle rotation of telemetry rings
    telemetryRing1.rotation.z += 0.0025;
    telemetryRing2.rotation.z -= 0.0018;
    
    // Subtle particle drift
    particles.rotation.y = time * 0.025;
    particles.rotation.x = Math.sin(time * 0.02) * 0.08;
    
    // Smooth camera mouse parallax with lerp
    camera.position.x += (targetCamX - camera.position.x) * 0.045;
    camera.position.y += (targetCamY - camera.position.y) * 0.045;
    camera.lookAt(0, 0, 0);
    
    renderer.render(scene, camera);
}
renderLoop();
