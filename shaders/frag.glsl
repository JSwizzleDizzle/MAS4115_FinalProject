# version 330 core

in vec3 wsPosition;
in vec3 wsNormal;
in vec2 tsUV;
in vec4 fColor;

out vec4 outColor;

uniform sampler2D uDiffuse;

void main()
{
    outColor = texture(uDiffuse, tsUV);
}


