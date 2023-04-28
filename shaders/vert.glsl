// GLSL version
# version 330 core

// Stored vertex attributes
layout(location = 0) in vec3 osPosition;
layout(location = 1) in vec3 osNormal;
layout(location = 2) in vec2 osUV;

// Outputs to the fragment hsder
out vec3 wsPosition;
out vec3 wsNormal;
out vec2 tsUV;
out vec4 fColor;

// Input transformation matrices
uniform mat4 uModel = mat4(1.0);
uniform mat4 uNormalModel = mat4(1.0);
uniform mat4 uView = mat4(1.0);
uniform mat4 uProjection = mat4(1.0);



void main()
{
    // Calculate position transformations
    vec4 ws4Position = uModel * vec4(osPosition, 1.0);
    gl_Position = uProjection * uView * ws4Position;
    wsPosition = vec3(ws4Position);

    // Transform surface normals to world space
    wsNormal = vec3(uNormalModel * vec4(osNormal, 0.0));

    // Keep UVs
    tsUV = osUV;
}


