import * as THREE from 'three';
import { animate } from 'animejs';

// Clean up any existing canvas (useful for HMR in Vite)
const container = document.getElementById('bg-canvas-container');
container.innerHTML = '';

// 1. Setup Scene, Camera, Renderer
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });

renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(window.devicePixelRatio);
container.appendChild(renderer.domElement);

// 2. Placeholder Shape for Step 1
const geometry = new THREE.BoxGeometry(2, 2, 2);
const material = new THREE.MeshBasicMaterial({ 
    color: 0x00f0ff, // Glowing cyan placeholder
    wireframe: true 
});
const placeholder = new THREE.Mesh(geometry, material);
scene.add(placeholder);

camera.position.z = 5;

// 3. Resize Handler
window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});

// 4. Anime.js integration (Anime v4 syntax)
animate(placeholder.rotation, {
    x: Math.PI * 2,
    y: Math.PI * 2,
    duration: 5000,
    ease: 'linear',
    loop: true
});

// 5. Render Loop
function renderLoop() {
    requestAnimationFrame(renderLoop);
    // Anime.js engine ticks automatically behind the scenes
    renderer.render(scene, camera);
}

renderLoop();
