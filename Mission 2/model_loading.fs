#version 330 core

vec2 poissonDisk[16] = vec2[](
   vec2( -0.94201624, -0.39906216 ),
   vec2( 0.94558609, -0.76890725 ),
   vec2( -0.094184101, -0.92938870 ),
   vec2( 0.34495938, 0.29387760 ),
   vec2( -0.91588581, 0.45771432 ),
   vec2( -0.81544232, -0.87912464 ),
   vec2( -0.38277543, 0.27676845 ),
   vec2( 0.97484398, 0.75648379 ),
   vec2( 0.44323325, -0.97511554 ),
   vec2( 0.53742981, -0.47373420 ),
   vec2( -0.26496911, -0.41893023 ),
   vec2( 0.79197514, 0.19090188 ),
   vec2( -0.24188840, 0.99706507 ),
   vec2( -0.81409955, 0.91437590 ),
   vec2( 0.19984126, 0.78641367 ),
   vec2( 0.14383161, -0.14100790 )
);

in VS_OUT {
    vec3 FragPos;
    vec3 Normal;
    vec2 TexCoords;
    vec4 LightSpace;
} fs_in;

out vec4 Color;

uniform sampler2D texture_diffuse1;
uniform sampler2D shadow_map;
uniform vec3 lightPos;
uniform vec3 viewPos;

float random(vec3 seed, int i){
    vec4 seed4 = vec4(seed,i);
    float dot_product = dot(seed4, vec4(12.9898,78.233,45.164,94.673));
    return fract(sin(dot_product) * 43758.5453);
}

float shadow_caculation(vec4 light_space)
{
    
    vec3 coords = light_space.xyz / light_space.w;
    coords = coords * 0.5 + 0.5;
    float closest_depth = texture(shadow_map, coords.xy).r;
    float current_depth = coords.z;
    vec3 normal = normalize(fs_in.Normal);
    vec3 light_d = normalize(lightPos - fs_in.FragPos);
    float bias = max(0.05 * (1.0 - dot(normal, light_d)), 0.005);
    
    float shadow = 0.0;
    
    // PCF
    vec2 tex_size = 1.0 / textureSize(shadow_map, 0);
    for(int x = -1; x <= 1; x ++){
        for(int y = -1; y <= 1; y ++){
            float pcf_depth = texture(shadow_map, coords.xy + vec2(x, y) * tex_size).r;
            shadow += current_depth - bias > pcf_depth ? 1.0 : 0.0;
        }
    }
    shadow /= 9.0;
    
    // Possion
    shadow = 0.0;
    for(int x = 0; x < 4; x ++){
        int index = x;
        float poisson_depth = texture(shadow_map, coords.xy + poissonDisk[x] / 700.0).r;
        shadow += current_depth - bias > poisson_depth ? 0.2 : 0.0;
    }
    
    if(coords.z > 1.0)
    shadow = 0.0;
    
    return shadow;
}

void main()
{
    
    vec3 color = texture(texture_diffuse1, fs_in.TexCoords).rgb;
    vec3 ambient = vec3(0.8);
    
    vec3 light_color = vec3(0.4);
    
    vec3 lightDir = normalize(lightPos - fs_in.FragPos);
    vec3 normal = normalize(fs_in.Normal);
    float diff = max(dot(lightDir, normal), 0.0);
    vec3 diffuse = diff * light_color;
    

    vec3 viewDir = normalize(viewPos - fs_in.FragPos);
    vec3 reflectDir = reflect(-lightDir, normal);
    float spec = 0.0;
    
    //use blinn-phong
    vec3 halfwayDir = normalize(lightDir + viewDir);
    spec = pow(max(dot(normal, halfwayDir), 0.0), 64.0);
    
    vec3 specular = light_color * spec;
    float shadow = shadow_caculation(fs_in.LightSpace);
    shadow = min(shadow, 0.75); 
    vec3 color_r;
    
    color_r = ((1 - shadow) * (diffuse + specular))* color + ambient * color;
    
    Color = vec4(color_r, 1.0f);
    
}


