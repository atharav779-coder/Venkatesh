import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { animate } from 'animejs';
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

// 2. Realism Upgrade: Lighting
const ambientLight = new THREE.AmbientLight(0xffffff, 0.8);
scene.add(ambientLight);

const directionalLight = new THREE.DirectionalLight(0xffffff, 2.5);
directionalLight.position.set(5, 10, 7);
scene.add(directionalLight);

// Glowing neon rim light (Cyan/Blue)
const rimLight = new THREE.PointLight(0x00f0ff, 100, 50);
rimLight.position.set(-5, 0, -5);
scene.add(rimLight);

// Warm orange engine/thruster light
const engineLight = new THREE.PointLight(0xf97316, 100, 50);
engineLight.position.set(5, -5, 5);
scene.add(engineLight);

// Animation Hierarchy Setup
// We use nested groups to prevent Anime.js and GSAP from fighting over the same properties!
const scrollGroup = new THREE.Group(); // GSAP controls this (Scroll)
scene.add(scrollGroup);

const hoverGroup = new THREE.Group(); // Anime.js controls this (Hovering)
scrollGroup.add(hoverGroup);

// Position based on screen size
const updateAssemblyPosition = () => {
    if (window.innerWidth < 768) {
        scrollGroup.position.set(0, 2, 0); 
    } else {
        scrollGroup.position.set(3, 0, 0); 
    }
};
updateAssemblyPosition();

// 3. Import & Configure the 3D Model
const loader = new GLTFLoader();

loader.load('/models/jet_engine/scene.gltf', (gltf) => {
    const model = gltf.scene;
    
    // Automatically center and scale the loaded model so it perfectly fits the screen
    const box = new THREE.Box3().setFromObject(model);
    const center = box.getCenter(new THREE.Vector3());
    const size = box.getSize(new THREE.Vector3());
    const maxDim = Math.max(size.x, size.y, size.z);
    
    const scale = 5 / maxDim; // Normalize size
    model.scale.setScalar(scale);
    model.position.sub(center.multiplyScalar(scale)); // Center it exactly
    
    // Realism Upgrade: Advanced Materials
    model.traverse((child) => {
        if (child.isMesh) {
            const oldMat = child.material;
            // Upgrade to a premium glossy/metal material
            child.material = new THREE.MeshPhysicalMaterial({
                color: oldMat.color || 0xdddddd,
                metalness: 0.8,
                roughness: 0.2,
                clearcoat: 1.0,
                clearcoatRoughness: 0.1,
                side: THREE.DoubleSide
            });
        }
    });

    // Angle it dynamically to look cool
    hoverGroup.rotation.y = -Math.PI / 6;
    hoverGroup.rotation.x = Math.PI / 12;
    hoverGroup.add(model);

    // Part 2: Anime.js Continuous Vector Motion (Hovering)
    animate(hoverGroup.position, {
        y: '+=0.6',
        duration: 2000,
        direction: 'alternate',
        loop: true,
        ease: 'easeInOutSine'
    });

    animate(hoverGroup.rotation, {
        x: '+=0.05',
        z: '+=0.02',
        duration: 3000,
        direction: 'alternate',
        loop: true,
        ease: 'easeInOutSine'
    });

    // Part 3: GSAP Scroll Choreography
    const tl = gsap.timeline({
        scrollTrigger: {
            trigger: "body",
            start: "top top",
            end: "bottom bottom",
            scrub: 1.5 // Smooth interpolation
        }
    });

    // Sequence 1: Dive Bomb (Rotate 90 degrees down)
    tl.to(scrollGroup.rotation, {
        z: -Math.PI / 2, // 90 degree dive
        y: Math.PI / 4,
        ease: "power2.inOut"
    }, 0);

    // Sequence 2: Fly off screen at the very bottom
    tl.to(scrollGroup.position, {
        y: -15, // Drop down off screen
        x: -5,
        ease: "power3.in"
    }, 0.5); // Starts halfway through the scroll

}, undefined, (error) => {
    console.error('Error loading GLTF:', error);
});

// Handle resizing dynamically
window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
    updateAssemblyPosition();
});

// The High-Performance Loop
function renderLoop() {
    requestAnimationFrame(renderLoop);
    renderer.render(scene, camera);
}
renderLoop();
