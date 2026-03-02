<script>
  import { T, useFrame } from "@threlte/core";
  import { ContactShadows, Float, Grid, OrbitControls } from "@threlte/extras";

  // Svelte 5 Rune for state
  let rotation = $state(0);

  useFrame((state, delta) => {
    rotation += delta * 0.5;
  });
</script>

<T.PerspectiveCamera makeDefault position={[10, 10, 10]}>
  <OrbitControls
    enableDamping
    enablePan={false}
    autoRotate
    autoRotateSpeed={0.5}
    minDistance={5}
    maxDistance={30}
  />
</T.PerspectiveCamera>

<!-- SIMPLE GIGANTIC LIGHTS FOR VISIBILITY -->
<T.AmbientLight intensity={2} />
<T.PointLight position={[20, 20, 20]} intensity={50} color="#ffffff" />
<T.PointLight position={[-20, -20, -20]} intensity={30} color="#00f3ff" />

<Grid
  position.y={-5}
  cellColor="#00f3ff"
  sectionColor="#00f3ff"
  cellSize={2}
  sectionSize={10}
  sectionThickness={2.5}
  fadeDistance={50}
  infiniteGrid
/>

<Float speed={2} rotationIntensity={0.5} floatIntensity={1}>
  <T.Group rotation.y={rotation}>
    <!-- MAIN VISUAL OBJECT (CUBE) -->
    <T.Mesh>
      <T.BoxGeometry args={[5, 5, 5]} />
      <T.MeshStandardMaterial
        color="#00f3ff"
        metalness={0.8}
        roughness={0.2}
        transparent={true}
        opacity={0.8}
        side={2}
      />
    </T.Mesh>

    <!-- WIREFRAME OVERLAY -->
    <T.Mesh scale={1.01}>
      <T.BoxGeometry args={[5, 5, 5]} />
      <T.MeshStandardMaterial
        color="#ffffff"
        wireframe={true}
        emissive="#ffffff"
        emissiveIntensity={2}
      />
    </T.Mesh>

    <!-- CENTER SPHERE -->
    <T.Mesh>
      <T.SphereGeometry args={[1.5, 32, 32]} />
      <T.MeshStandardMaterial
        color="#ffffff"
        emissive="#00f3ff"
        emissiveIntensity={10}
      />
    </T.Mesh>
  </T.Group>
</Float>

<!-- SHADOWS -->
<ContactShadows
  position.y={-5}
  opacity={0.5}
  scale={30}
  blur={2}
  far={10}
  color="#00f3ff"
/>
