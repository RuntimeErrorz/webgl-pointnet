<template>
  <body></body>
</template>

<script>
import * as THREE from "three";
import { PLYLoader } from "three/examples/jsm/loaders/PLYLoader";
import Stats from "three/examples/jsm/libs/stats.module";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls";

let pointCloudData = [];
let spheres = [];
let renderer;
let camera, mapCamera;
let scene, mapScene;
let controls, stats;
let frame;

let maxX = -Infinity;
let maxY = -Infinity;
let minX = Infinity;
let minY = Infinity;

let halfFrameLength = 20;

const halfFrameLengthInit = halfFrameLength;
const halfsideLength = 50;
const mainCameraHeight = 40;
const raycaster = new THREE.Raycaster();
const pointer = new THREE.Vector2();

function calcFrameVertex(flag) {
  let cameraX = camera.position.x;
  let cameraY = camera.position.y;
  let x =
    ((cameraX - minX) / (maxX - minX)) * 2 * halfsideLength - halfsideLength;
  let y =
    ((cameraY - minY) / (maxY - minY)) * 2 * halfsideLength - halfsideLength;
  let x1 = x - halfFrameLength;
  let x2 = x + halfFrameLength;
  let y1 = y - halfFrameLength;
  let y2 = y + halfFrameLength;
  if (flag === 0)
    return [
      new THREE.Vector3(x1, y2, 0),
      new THREE.Vector3(x2, y2, 0),
      new THREE.Vector3(x2, y1, 0),
      new THREE.Vector3(x1, y1, 0),
      new THREE.Vector3(x1, y2, 0),
    ];
  else return [x1, x2, y1, y2];
}

function onWindowResize() {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  mapCamera.aspect = window.innerWidth / window.innerHeight;
  mapCamera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
}

function initScene() {
  scene = new THREE.Scene();
  mapScene = new THREE.Scene();
  window.addEventListener("resize", onWindowResize);
}

function initRender() {
  renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setSize(window.innerWidth, window.innerHeight);
  document.body.appendChild(renderer.domElement);
  renderer.autoClear = false;
}

function initSpheres() {
  const sphere = new THREE.Mesh(
    new THREE.SphereGeometry(1, 32, 32),
    new THREE.MeshBasicMaterial({ color: 0xff0000 })
  );
  sphere.scale.set(0, 0, 0);
  scene.add(sphere);
  spheres.push(sphere);
  document.addEventListener("mousedown", (event) => {
    pointer.x = (event.clientX / window.innerWidth) * 2 - 1;
    pointer.y = -(event.clientY / window.innerHeight) * 2 + 1;
    raycaster.setFromCamera(pointer, camera);
    let intersects = raycaster.intersectObjects(pointCloudData);
    intersects = intersects.length > 0 ? intersects[0] : null;
    if (intersects !== null) {
      console.log(intersects.point);
      spheres[0].position.copy(intersects.point);
      spheres[0].scale.set(1, 1, 1);
    }
  });
}

function initCamera() {
  camera = new THREE.PerspectiveCamera(
    75,
    window.innerWidth / window.innerHeight,
    0.1,
    1000
  );
  camera.position.set(50, 0, mainCameraHeight);
  mapCamera = new THREE.PerspectiveCamera(
    160,
    window.innerWidth / window.innerHeight,
    0.1,
    1000
  );
  mapCamera.position.set(0, 0, 40);
}

function initModel() {
  scene.add(new THREE.AxesHelper(50));
  mapScene.add(new THREE.AxesHelper(50));
  let loader = new PLYLoader();
  return new Promise((resolve) => {
    for (let i = 0; i < 1; ++i) {
      loader.load("../data/Toronto_3D/dwarf.ply", (geometry) => {
        for (let j = 0; j < geometry.attributes.position.count; j += 3) {
          let x = geometry.attributes.position.array[j];
          let y = geometry.attributes.position.array[j + 1];
          maxX = Math.max(maxX, x);
          maxY = Math.max(maxY, y);
          minX = Math.min(minX, x);
          minY = Math.min(minY, y);
        }
        let PointCloud = new THREE.Points(
          geometry,
          new THREE.PointsMaterial({
            size: 0.01,
            vertexColors: true,
          })
        );
        pointCloudData.push(PointCloud);
        scene.add(PointCloud);
        resolve([maxX, maxY, minX, minY]);
      });
    }
  });
}

function initStats() {
  stats = new Stats();
  document.body.appendChild(stats.domElement);
}

function initControls() {
  controls = new OrbitControls(camera, renderer.domElement);
  controls.maxPolarAngle = Infinity;
  controls.enablePan = true;
  controls.target.set(50, 0, 0);
  controls.addEventListener("change", () => {
    halfFrameLength =
      Math.pow(
        controls.target.distanceTo(controls.object.position) / mainCameraHeight,
        0.5
      ) * halfFrameLengthInit;
    updateFrame();
  });
}

async function initMaps() {
  let mapVertexs = [];
  mapVertexs.push(new THREE.Vector3(-halfsideLength, halfsideLength, 0));
  mapVertexs.push(new THREE.Vector3(halfsideLength, halfsideLength, 0));
  mapVertexs.push(new THREE.Vector3(halfsideLength, -halfsideLength, 0));
  mapVertexs.push(new THREE.Vector3(-halfsideLength, -halfsideLength, 0));
  mapVertexs.push(new THREE.Vector3(-halfsideLength, halfsideLength, 0));
  mapScene.add(
    new THREE.Line(
      new THREE.BufferGeometry().setFromPoints(mapVertexs),
      new THREE.LineBasicMaterial({ color: 0x0000ff })
    )
  );

  frame = new THREE.Line(
    new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(0, 0, 0)])
  );
  mapScene.add(frame); //占位frame，不知道为什么监听OrbitControls的Change事件，初始化的时候明明没有Change也会触发更新

  await initModel();
  mapScene.remove(frame);

  frame = new THREE.Line(
    new THREE.BufferGeometry().setFromPoints(calcFrameVertex(0)),
    new THREE.LineBasicMaterial({ color: 0xdc143c })
  );
  frame.geometry.attributes.position.needsUpdate = true;
  mapScene.add(frame);
}

function updateFrame() {
  const positions = frame.geometry.attributes.position.array;
  let [x1, x2, y1, y2] = calcFrameVertex(1);
  positions[0] = x1;
  positions[1] = y2;
  positions[3] = x2;
  positions[4] = y2;
  positions[6] = x2;
  positions[7] = y1;
  positions[9] = x1;
  positions[10] = y1;
  positions[12] = x1;
  positions[13] = y2;
  frame.geometry.attributes.position.needsUpdate = true;
}

function update() {
  stats.update();
  controls.update();
}

function render() {
  let w = window.innerWidth;
  let h = window.innerHeight;

  renderer.setViewport(0, 0, w, h);
  renderer.render(scene, camera);

  renderer.setViewport(0.44 * w, -0.37 * h, w, h); //距离左边10px，上边1200px
  renderer.render(mapScene, mapCamera);
}

function animate() {
  requestAnimationFrame(animate);
  render();
  update();
}

function draw() {
  initScene();
  initCamera();
  initRender();

  initControls();
  initStats();

  initMaps();
  initSpheres();
  animate();
}

draw();
</script>

<style>
body {
  margin: 0px;
}
</style>
