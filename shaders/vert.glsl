# version 330 core

layout(location = 0) in vec3 osPosition;
layout(location = 1) in vec3 osNormal;
layout(location = 2) in vec2 osUV;

out vec3 wsPosition;
out vec3 wsNormal;
out vec2 tsUV;
out vec4 fColor;

uniform mat4 uModel = mat4(1.0);
uniform mat4 uNormalModel = mat4(1.0);
uniform mat4 uView = mat4(1.0);
uniform mat4 uProjection = mat4(1.0);



void main()
{
    fColor = vec4(0.5 * osPosition + 0.5, 1.0);

    wsPosition = vec3(uModel * vec4(osPosition, 1.0));
    wsNormal = vec3(uNormalModel * vec4(osNormal, 0.0));
    tsUV = osUV;
    

    gl_Position = uProjection * uView * uModel * vec4(osPosition, 1.0);
}


