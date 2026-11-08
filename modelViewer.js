import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

let modalEl = null;
let canvasEl = null;
let spinnerEl = null;
let progressEl = null;
let titleEl = null;
let catEl = null;
let originEl = null;
let autoRotateBtn = null;
let wireframeBtn = null;
let resetBtn = null;

let scene = null;
let camera = null;
let renderer = null;
let controls = null;
let currentModel = null;
let animId = null;
let isAutoRotating = true;
let isWireframe = false;
let initialCameraPos = new THREE.Vector3();
let initialControlsTarget = new THREE.Vector3();

export function initModelViewer() {
  if (modalEl) return;

  // Create Modal DOM
  modalEl = document.createElement('div');
  modalEl.id = 'model-modal';
  modalEl.className = 'model-modal-overlay';
  modalEl.innerHTML = `
    <div class="model-modal-dialog">
      <div class="model-modal-header">
        <div class="model-modal-info">
          <span class="model-modal-badge" id="model-modal-cat">CATEGORY</span>
          <h2 class="model-modal-title" id="model-modal-title">Aircraft 3D Model</h2>
          <span class="model-modal-origin" id="model-modal-origin">Origin / Manufacturer</span>
        </div>
        <button class="model-modal-close" id="model-modal-close" aria-label="Close 3D Viewer">&times;</button>
      </div>

      <div class="model-canvas-wrapper" id="model-canvas-wrapper">
        <div class="model-loading-spinner" id="model-loading-spinner">
          <div class="spinner-ring"></div>
          <div class="spinner-text">Loading 3D Aircraft Model...</div>
          <div class="spinner-bar"><div class="spinner-bar-fill" id="spinner-progress"></div></div>
        </div>
        <canvas id="model-viewer-canvas"></canvas>
        <div class="model-canvas-hint">
          <span>🖱️ Left-Click + Drag: Rotate 360°</span>
          <span>🔍 Scroll: Zoom In/Out</span>
          <span>✋ Right-Click: Pan</span>
        </div>
      </div>

      <div class="model-modal-toolbar">
        <button class="model-tool-btn active" id="model-btn-autorotate">
          <span class="icon">🔄</span> Auto-Rotate: <b>ON</b>
        </button>
        <button class="model-tool-btn" id="model-btn-wireframe">
          <span class="icon">📐</span> Wireframe: <b>OFF</b>
        </button>
        <button class="model-tool-btn" id="model-btn-reset">
          <span class="icon">🎯</span> Reset View
        </button>
      </div>
    </div>
  `;

  document.body.appendChild(modalEl);

  canvasEl = document.getElementById('model-viewer-canvas');
  spinnerEl = document.getElementById('model-loading-spinner');
  progressEl = document.getElementById('spinner-progress');
  titleEl = document.getElementById('model-modal-title');
  catEl = document.getElementById('model-modal-cat');
  originEl = document.getElementById('model-modal-origin');

  autoRotateBtn = document.getElementById('model-btn-autorotate');
  wireframeBtn = document.getElementById('model-btn-wireframe');
  resetBtn = document.getElementById('model-btn-reset');

  const closeBtn = document.getElementById('model-modal-close');
  closeBtn.addEventListener('click', closeModelViewer);

  // Close on backdrop click
  modalEl.addEventListener('click', (e) => {
    if (e.target === modalEl) closeModelViewer();
  });

  // Close on Escape key
  window.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && modalEl.classList.contains('active')) {
      closeModelViewer();
    }
  });

  // Toolbar actions
  autoRotateBtn.addEventListener('click', () => {
    isAutoRotating = !isAutoRotating;
    if (controls) controls.autoRotate = isAutoRotating;
    autoRotateBtn.classList.toggle('active', isAutoRotating);
    autoRotateBtn.innerHTML = `<span class="icon">🔄</span> Auto-Rotate: <b>${isAutoRotating ? 'ON' : 'OFF'}</b>`;
  });

  wireframeBtn.addEventListener('click', () => {
    isWireframe = !isWireframe;
    if (currentModel) {
      currentModel.traverse((child) => {
        if (child.isMesh && child.material) {
          if (Array.isArray(child.material)) {
            child.material.forEach(m => m.wireframe = isWireframe);
          } else {
            child.material.wireframe = isWireframe;
          }
        }
      });
    }
    wireframeBtn.classList.toggle('active', isWireframe);
    wireframeBtn.innerHTML = `<span class="icon">📐</span> Wireframe: <b>${isWireframe ? 'ON' : 'OFF'}</b>`;
  });

  resetBtn.addEventListener('click', () => {
    if (controls && initialCameraPos.lengthSq() > 0) {
      camera.position.copy(initialCameraPos);
      controls.target.copy(initialControlsTarget);
      controls.update();
    }
  });

  // Handle window resize for viewer
  window.addEventListener('resize', onWindowResize);
}

function onWindowResize() {
  if (!modalEl || !modalEl.classList.contains('active') || !renderer || !camera) return;
  const wrapper = document.getElementById('model-canvas-wrapper');
  if (!wrapper) return;
  const width = wrapper.clientWidth;
  const height = wrapper.clientHeight;
  camera.aspect = width / height;
  camera.updateProjectionMatrix();
  renderer.setSize(width, height);
}

export function openModelViewer(planeName, modelFile, planeData = {}) {
  initModelViewer();

  // Populate Header Info
  titleEl.textContent = planeName;
  catEl.textContent = planeData.category || 'AIRCRAFT 3D';
  originEl.textContent = planeData.origin || 'Aerospace Engineering';

  // Reset toolbar states
  isAutoRotating = true;
  isWireframe = false;
  autoRotateBtn.classList.add('active');
  autoRotateBtn.innerHTML = `<span class="icon">🔄</span> Auto-Rotate: <b>ON</b>`;
  wireframeBtn.classList.remove('active');
  wireframeBtn.innerHTML = `<span class="icon">📐</span> Wireframe: <b>OFF</b>`;

  // Show Modal
  modalEl.classList.add('active');
  document.body.style.overflow = 'hidden';

  // Setup Three.js scene
  setupViewerScene();

  // Load Model
  loadAircraftModel(modelFile);
}

function setupViewerScene() {
  cleanupViewerScene();

  const wrapper = document.getElementById('model-canvas-wrapper');
  const width = wrapper.clientWidth || 800;
  const height = wrapper.clientHeight || 500;

  scene = new THREE.Scene();
  scene.background = new THREE.Color(0x0c1017); // Sleek modern dark aerospace tone

  // Subtle ground grid
  const grid = new THREE.GridHelper(30, 30, 0xf97316, 0x1e293b);
  grid.position.y = -2;
  scene.add(grid);

  camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 1000);

  renderer = new THREE.WebGLRenderer({
    canvas: canvasEl,
    antialias: true,
    alpha: false,
    powerPreference: 'high-performance'
  });
  renderer.setSize(width, height);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.3;
  renderer.shadowMap.enabled = true;

  // Controls
  controls = new OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;
  controls.dampingFactor = 0.05;
  controls.autoRotate = isAutoRotating;
  controls.autoRotateSpeed = 1.8;
  controls.minDistance = 1;
  controls.maxDistance = 150;

  // Lighting
  const ambient = new THREE.AmbientLight(0xffffff, 0.9);
  scene.add(ambient);

  const keyLight = new THREE.DirectionalLight(0xffffff, 2.2);
  keyLight.position.set(15, 25, 20);
  scene.add(keyLight);

  const fillLight = new THREE.DirectionalLight(0xdbeafe, 1.2);
  fillLight.position.set(-15, 10, -15);
  scene.add(fillLight);

  const rimLight = new THREE.DirectionalLight(0xf97316, 0.9);
  rimLight.position.set(0, -10, 10);
  scene.add(rimLight);

  // Start Animation Loop
  function animate() {
    animId = requestAnimationFrame(animate);
    if (controls) controls.update();
    if (renderer && scene && camera) {
      renderer.render(scene, camera);
    }
  }
  animate();
}

function loadAircraftModel(modelFile) {
  spinnerEl.style.display = 'flex';
  progressEl.style.width = '0%';

  const loader = new GLTFLoader();
  const modelUrl = `/models/planes/${modelFile}`;

  loader.load(
    modelUrl,
    (gltf) => {
      currentModel = gltf.scene;

      // Compute bounding box and auto-center
      const box = new THREE.Box3().setFromObject(currentModel);
      const center = box.getCenter(new THREE.Vector3());
      const size = box.getSize(new THREE.Vector3());
      const maxDim = Math.max(size.x, size.y, size.z);

      currentModel.position.x += (currentModel.position.x - center.x);
      currentModel.position.y += (currentModel.position.y - center.y);
      currentModel.position.z += (currentModel.position.z - center.z);

      // Enhance materials
      currentModel.traverse((child) => {
        if (child.isMesh) {
          child.castShadow = true;
          child.receiveShadow = true;
          if (child.material) {
            child.material.side = THREE.DoubleSide;
          }
        }
      });

      scene.add(currentModel);

      // Position Camera perfectly to frame the plane
      const fov = camera.fov * (Math.PI / 180);
      let cameraDist = Math.abs(maxDim / 2 / Math.tan(fov / 2)) * 1.45;
      if (cameraDist < 2) cameraDist = 6;

      camera.position.set(cameraDist * 0.75, cameraDist * 0.45, cameraDist * 0.9);
      camera.lookAt(0, 0, 0);

      controls.target.set(0, 0, 0);
      controls.update();

      initialCameraPos.copy(camera.position);
      initialControlsTarget.copy(controls.target);

      // Hide loading spinner
      spinnerEl.style.display = 'none';
    },
    (xhr) => {
      if (xhr.lengthComputable && xhr.total > 0) {
        const percent = Math.round((xhr.loaded / xhr.total) * 100);
        progressEl.style.width = `${percent}%`;
      }
    },
    (err) => {
      console.error("Error loading 3D model:", err);
      spinnerEl.innerHTML = `
        <div style="color: #ef4444; font-weight: 700;">⚠️ Model failed to load</div>
        <div style="font-size: 0.85rem; color: #94a3b8; margin-top: 0.5rem;">Could not load ${modelFile}</div>
      `;
    }
  );
}

export function closeModelViewer() {
  if (!modalEl) return;
  modalEl.classList.remove('active');
  document.body.style.overflow = '';
  cleanupViewerScene();
}

function cleanupViewerScene() {
  if (animId) {
    cancelAnimationFrame(animId);
    animId = null;
  }
  if (currentModel && scene) {
    scene.remove(currentModel);
    currentModel.traverse((child) => {
      if (child.isMesh) {
        if (child.geometry) child.geometry.dispose();
        if (child.material) {
          if (Array.isArray(child.material)) {
            child.material.forEach(m => m.dispose());
          } else {
            child.material.dispose();
          }
        }
      }
    });
    currentModel = null;
  }
  if (controls) {
    controls.dispose();
    controls = null;
  }
  if (renderer) {
    renderer.dispose();
    renderer = null;
  }
  scene = null;
  camera = null;
}


if (typeof window !== 'undefined') {
  window.openModelViewer = openModelViewer;
  window.initModelViewer = initModelViewer;
  window.closeModelViewer = closeModelViewer;
  document.addEventListener('DOMContentLoaded', () => {
    initModelViewer();
  });
}
