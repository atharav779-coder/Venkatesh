import * as THREE from 'three';

// Clean up any existing canvas (useful for HMR in Vite)
const container = document.getElementById('bg-canvas-container');
container.innerHTML = '';

// 1. Setup Scene, Camera, Renderer
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });

renderer.setSize(window.innerWidth, window.innerHeight);
// Cap pixel ratio to 2 for performance on high-DPI screens
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2)); 
container.appendChild(renderer.domElement);

const mainGroup = new THREE.Group();
scene.add(mainGroup);

// 2. The Globe (Subtle wireframe representing global aviation)
// Icosahedron with detail 2 is low-poly but looks beautifully geometric
const globeGeo = new THREE.IcosahedronGeometry(3, 2);
const globeMat = new THREE.MeshBasicMaterial({
    color: 0x94a3b8, // Slate gray to match light theme
    wireframe: true,
    transparent: true,
    opacity: 0.15
});
const globe = new THREE.Mesh(globeGeo, globeMat);
mainGroup.add(globe);

// 3. Flight Paths (Torus rings orbiting the globe)
const ringGeo1 = new THREE.TorusGeometry(3.5, 0.008, 16, 100);
const ringMat1 = new THREE.MeshBasicMaterial({ 
    color: 0xf97316, // Premium orange accent from the SkyVault theme
    transparent: true, 
    opacity: 0.5 
});
const ring1 = new THREE.Mesh(ringGeo1, ringMat1);
ring1.rotation.x = Math.PI / 3;
mainGroup.add(ring1);

const ringGeo2 = new THREE.TorusGeometry(3.8, 0.006, 16, 100);
const ringMat2 = new THREE.MeshBasicMaterial({ 
    color: 0x64748b, // Deeper slate
    transparent: true, 
    opacity: 0.3 
});
const ring2 = new THREE.Mesh(ringGeo2, ringMat2);
ring2.rotation.y = Math.PI / 4;
mainGroup.add(ring2);

// 4. Atmospheric Particles (Abstract clouds / high-altitude dust)
const particlesCount = 600;
const posArray = new Float32Array(particlesCount * 3);
for(let i = 0; i < particlesCount * 3; i++) {
    posArray[i] = (Math.random() - 0.5) * 25; // Spread over a large volume
}
const particlesGeo = new THREE.BufferGeometry();
particlesGeo.setAttribute('position', new THREE.BufferAttribute(posArray, 3));
const particlesMat = new THREE.PointsMaterial({
    size: 0.03,
    color: 0xf97316,
    transparent: true,
    opacity: 0.3
});
const particles = new THREE.Points(particlesGeo, particlesMat);
scene.add(particles);

// Position the whole assembly dynamically based on screen width
const updateAssemblyPosition = () => {
    if (window.innerWidth < 768) {
        mainGroup.position.set(0, 2, 0); // Center-top for mobile
    } else {
        mainGroup.position.set(2.5, 0, 0); // Offset to the right for desktop
    }
};
updateAssemblyPosition();
camera.position.z = 8;

// 5. Handle resizing
window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
    updateAssemblyPosition();
});

// 6. Smooth Mouse Parallax
let mouseX = 0;
let mouseY = 0;
window.addEventListener('mousemove', (e) => {
    mouseX = (e.clientX / window.innerWidth) - 0.5;
    mouseY = (e.clientY / window.innerHeight) - 0.5;
});

// 7. Animation Loop (Strictly ONE requestAnimationFrame)
function animate() {
    requestAnimationFrame(animate);

    // Global slow rotation
    mainGroup.rotation.y += 0.001;
    mainGroup.rotation.x += 0.0005;

    // Independent flight path rotations
    ring1.rotation.y += 0.002;
    ring2.rotation.x += 0.0015;

    // Slowly drifting atmosphere
    particles.rotation.y -= 0.0003;
    particles.rotation.x += 0.0001;
    
    // Parallax camera movement (smooth interpolation)
    camera.position.x += (mouseX * 1.0 - camera.position.x) * 0.05;
    camera.position.y += (-mouseY * 1.0 - camera.position.y) * 0.05;
    camera.lookAt(scene.position);

    renderer.render(scene, camera);
}

animate();
