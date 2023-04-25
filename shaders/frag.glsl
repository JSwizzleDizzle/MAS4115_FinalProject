# version 330 core

struct LightData
{
    vec3 diffuse;
    vec3 ambient;
    vec3 specular;
};

struct DirectionLight
{
    LightData data;
    vec3 direction;
};

struct PointLight
{
    LightData data;
    vec3 position;
    vec3 attenuation;
    float radius;
    float intensity;
};



in vec3 wsPosition;
in vec3 wsNormal;
in vec2 tsUV;
in vec4 fColor;

out vec4 outColor;

uniform vec3 uCameraPos;
uniform DirectionLight uDirLight;
uniform sampler2D uDiffuse;


vec3 calcDirLight(DirectionLight light, vec3 normal, vec3 camPos);

void main()
{
    vec3 nNormal = normalize(wsNormal);
    vec3 nCameraPos = normalize(uCameraPos);

    vec3 lightColor = calcDirLight(uDirLight, nNormal, nCameraPos);
    outColor = texture(uDiffuse, tsUV) * vec4(lightColor, 1.0);
}



vec3 calcDirLight(DirectionLight light, vec3 normal, vec3 camPos)
{
    light.direction = normalize(light.direction);
    float diffuseFactor = max(0, dot(normal, -light.direction));
    float specularFactor = pow(max(0, dot(camPos, reflect(light.direction, normal))), 8);
    return uDirLight.data.ambient + diffuseFactor * uDirLight.data.diffuse + specularFactor * uDirLight.data.specular;
}


