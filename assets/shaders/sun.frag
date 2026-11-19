#version 330 core

in vec3 vWorldPos;
in vec3 vNormal;
in vec2 vUV;

uniform vec3 uColor;
uniform vec3 uViewPos;

out vec4 FragColor;

void main()
{
    // The Sun is self-illuminated: it ignores the light source.
    // A slight darkening towards the edge gives it a rounder look.
    vec3 N = normalize(vNormal);
    vec3 V = normalize(uViewPos - vWorldPos);
    float facing = max(dot(N, V), 0.0);

    vec3 color = uColor * (0.75 + 0.25 * facing);
    FragColor = vec4(color, 1.0);
}