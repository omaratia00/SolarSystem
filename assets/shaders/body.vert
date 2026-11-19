#version 330 core

layout (location = 0) in vec3 aPos;
layout (location = 1) in vec3 aNormal;
layout (location = 2) in vec2 aUV;

uniform mat4 uModel;         // object space -> world space
uniform mat4 uView;          // world space  -> camera space
uniform mat4 uProjection;    // camera space -> clip space (perspective)
uniform mat3 uNormalMatrix;  // inverse-transpose of the model's 3x3 part

out vec3 vWorldPos;
out vec3 vNormal;
out vec2 vUV;

void main()
{
    vec4 worldPos = uModel * vec4(aPos, 1.0);

    vWorldPos = worldPos.xyz;
    vNormal   = uNormalMatrix * aNormal;
    vUV       = aUV;               // used for textures from Phase 6

    gl_Position = uProjection * uView * worldPos;
}