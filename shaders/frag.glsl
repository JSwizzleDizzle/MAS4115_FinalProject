// GLSL version
# version 330 core

// Light color information
struct LightData
{
    vec3 ambient;
    vec3 diffuse;
    vec3 specular;
};

// Light color with a uniform direction (like sunlight)
struct DirectionLight
{
    LightData data;
    vec3 direction;
};


// Input vectors from the vertex shader
in vec3 wsPosition;
in vec3 wsNormal;
in vec2 tsUV;
in vec4 fColor;

// Final fragment color
out vec4 outColor;

// Camera position, light parameters, and texture inputs
uniform vec3 uCameraPos;
uniform DirectionLight uDirLight;
uniform sampler2D uDiffuse;


// Calculates light color from a directional light source
vec3 calcDirLight(DirectionLight light, vec3 normal, vec3 camPos)
{
    light.direction = normalize(light.direction);
    float diffuseFactor = max(0, dot(normal, -light.direction));
    float specularFactor = pow(max(0, dot(camPos, reflect(light.direction, normal))), 8);
    return uDirLight.data.ambient + diffuseFactor * uDirLight.data.diffuse + specularFactor * uDirLight.data.specular;
}



void main()
{
    vec3 nNormal = normalize(wsNormal);
    vec3 nCameraPos = normalize(uCameraPos);

    // Multiply light and texture color component-wise for final color
    vec3 lightColor = calcDirLight(uDirLight, nNormal, nCameraPos);
    outColor = texture(uDiffuse, tsUV) * vec4(lightColor, 1.0);
}


