#version 330 core

in vec3 vWorldPos;
in vec3 vNormal;
in vec2 vUV;

uniform vec3  uColor;
uniform float uAlpha;       // transparency of this ring band
uniform vec3  uLightPos;
uniform vec3  uLightColor;
uniform float uAmbient;

out vec4 FragColor;

void main()
{
    vec3 N = normalize(vNormal);
    vec3 L = normalize(uLightPos - vWorldPos);

    // The rings are lit from both sides: the Sun can be above or below
    // the ring plane, so we use the absolute value of N.L.
    float diff = abs(dot(N, L));

    vec3 lighting = (uAmbient + diff) * uLightColor;
    FragColor = vec4(uColor * lighting, uAlpha);
}