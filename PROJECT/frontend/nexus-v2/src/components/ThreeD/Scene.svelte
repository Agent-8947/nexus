<script>
  import { Canvas } from "@threlte/core";
  import NexusCore from "./NexusCore.svelte";
</script>

<div
  class="canvas-container w-full h-full relative"
  style="background: rgba(255,0,0,0.1);"
>
  <div
    class="absolute inset-0 flex items-center justify-center pointer-events-none z-50"
  >
    <div
      class="text-[8px] font-mono text-white opacity-20 animate-pulse uppercase tracking-[2em]"
    >
      // STANDBY: NEXUS CORE INITIALIZATION //
    </div>
  </div>

  <Canvas>
    <NexusCore />
  </Canvas>
</div>

<style>
  .canvas-container {
    /* Temporary hint to see the container */
    min-height: 100vh;
  }
</style>
