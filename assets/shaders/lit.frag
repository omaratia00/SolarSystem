#version 330 core

in vec3 vWorldPos;
in vec3 vNormal;
in vec2 vUV;

uniform vec3  uColor;       // surface color (textures replace this in Phase 6)
uniform vec3  uLightPos;    // Sun position (world space)
uniform vec3  uLightColor;
uniform vec3  uViewPos;     // camera position (world space)
uniform float uAmbient;     // minimum light on the dark side

out vec4 FragColor;

const float SHININESS     = 32.0;
const float SPEC_STRENGTH = 0.25;

void main()
{
    vec3 N = normalize(vNormal);                    // surface normal
    vec3 L = normalize(uLightPos - vWorldPos);      // towards the light
    vec3 V = normalize(uViewPos  - vWorldPos);      // towards the camera
    vec3 H = normalize(L + V);                      // Blinn-Phong half vector

    float diff = max(dot(N, L), 0.0);               // Lambert diffuse
    float spec = 0.0;
    if (diff > 0.0)
        spec = pow(max(dot(N, H), 0.0), SHININESS);

    vec3 lighting = (uAmbient + diff) * uLightColor;
    vec3 result   = uColor * lighting + SPEC_STRENGTH * spec * uLightColor;

    FragColor = vec4(result, 1.0);
}