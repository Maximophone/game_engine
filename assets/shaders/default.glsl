#type vertex
#version 330 core

layout (location=0) in vec2 aPos;
layout (location=1) in vec4 aColor;

uniform mat4 uProj;
uniform mat4 uView;

out vec4 fColor;

void main()
{
    fColor = aColor;
    gl_Position = uProj * uView * vec4(aPos, 0.0,  1.0);
}

#type fragment
#version 330 core

in vec4 fColor;

out vec4 color;

void main()
{
    color = fColor;
}



