# THREE.ShaderMaterial Documentation

**Source**: Three.js Official API Reference
**Version**: 2026 Compatible

## Overview

`ShaderMaterial` is a material rendered with custom shaders. A shader is a small program written in GLSL that runs on the GPU. You may want to use a custom shader to:

- Implement effects not available with any of the built-in materials.
- Combine many objects into a single Geometry to improve performance.
- Create complex procedural textures or animations.

## Usage

`ShaderMaterial` can only be used with `WebGLRenderer`. Built-in attributes and uniforms (like `projectionMatrix`, `modelViewMatrix`, `position`, `uv`, etc.) are passed to your shaders by default.

### Properties

- **uniforms** (Object): An object of the form `{ "uniformName": { value: 1.0 } }`. These are variables that are the same for all vertices/fragments.
- **vertexShader** (String): GLSL code for the vertex shader.
- **fragmentShader** (String): GLSL code for the fragment shader.
- **wireframe** (Boolean): Render as wireframe.
- **transparent** (Boolean): Defines whether this material has any effect on the rendering of objects with different color.

## Example (GLSL Integration)

```javascript
const material = new THREE.ShaderMaterial({
  uniforms: {
    uTime: { value: 0.0 }
  },
  vertexShader: `
    varying vec2 vUv;
    void main() {
      vUv = uv;
      gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
    }
  `,
  fragmentShader: `
    varying vec2 vUv;
    uniform float uTime;
    void main() {
      gl_FragColor = vec4(vUv, sin(uTime) * 0.5 + 0.5, 1.0);
    }
  `
});
```

## Performance Tips

- Use `THREE.RawShaderMaterial` if you want zero built-in variables.
- Use `#pragma unroll_loop_start` for loop unrolling.
- Minimize expensive calculations in the fragment shader.
